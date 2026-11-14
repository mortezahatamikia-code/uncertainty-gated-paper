package com.biodino.edge.benchmark

import android.content.Context
import android.graphics.Bitmap
import ai.onnxruntime.OnnxTensor
import ai.onnxruntime.OrtEnvironment
import ai.onnxruntime.OrtSession
import com.biodino.edge.data.engine.PreallocatedTensor
import com.biodino.edge.data.network.ModelDownloadManager
import java.io.File
import java.nio.FloatBuffer

/**
 * CPU-only ONNX sessions for benchmarking, pinned to 4 intra-op / 2 inter-op threads
 * with INT8 models and NO NNAPI delegate, matching the paper's edge testbed protocol.
 *
 * Tier-1 (biodino_mobile_int8.onnx) is bundled in assets.
 * Tier-2 (biodino_companion_int8.onnx) is loaded from, in order:
 *   1. <externalFilesDir>/biodino_companion_int8.onnx  (adb-pushed for the benchmark)
 *   2. the app's downloaded companion file (ModelDownloadManager), if present.
 */
class EdgeSessions(context: Context) : AutoCloseable {

    val env: OrtEnvironment = OrtEnvironment.getEnvironment("BioDINO-Bench")
    private val prealloc = PreallocatedTensor()
    private val appContext = context.applicationContext

    lateinit var baseSession: OrtSession
        private set
    var companionSession: OrtSession? = null
        private set
    var tier2Available: Boolean = false
        private set

    // Load-time measurements (milliseconds), filled by [load].
    var tier1AssetReadMs: Double = 0.0
    var tier1SessionCreateMs: Double = 0.0
    var tier2FileReadMs: Double = 0.0
    var tier2SessionCreateMs: Double = 0.0
    var tier2Source: String = "none"

    private fun cpuOptions(): OrtSession.SessionOptions =
        OrtSession.SessionOptions().apply {
            setIntraOpNumThreads(4)
            setInterOpNumThreads(2)
            setOptimizationLevel(OrtSession.SessionOptions.OptLevel.ALL_OPT)
            // Deliberately no addNnapi(): CPU-only for a controlled, comparable measurement.
        }

    fun load() {
        var t0 = System.nanoTime()
        val baseBytes = appContext.assets.open("biodino_mobile_int8.onnx").use { it.readBytes() }
        var t1 = System.nanoTime()
        tier1AssetReadMs = (t1 - t0) / 1e6
        baseSession = env.createSession(baseBytes, cpuOptions())
        tier1SessionCreateMs = (System.nanoTime() - t1) / 1e6

        val companionFile = resolveCompanionFile()
        if (companionFile != null) {
            t0 = System.nanoTime()
            val bytes = companionFile.readBytes()
            t1 = System.nanoTime()
            tier2FileReadMs = (t1 - t0) / 1e6
            companionSession = env.createSession(bytes, cpuOptions())
            tier2SessionCreateMs = (System.nanoTime() - t1) / 1e6
            tier2Available = true
        }
    }

    private fun resolveCompanionFile(): File? {
        val pushed = File(appContext.getExternalFilesDir(null), "biodino_companion_int8.onnx")
        if (pushed.exists() && pushed.length() >= 5L * 1024 * 1024) {
            tier2Source = "adb_pushed"
            return pushed
        }
        if (ModelDownloadManager.isCustomModelActive(appContext)) {
            tier2Source = "downloaded"
            return ModelDownloadManager.getCustomModelFile(appContext)
        }
        return null
    }

    fun preprocess(bitmap: Bitmap): FloatBuffer = prealloc.loadFromBitmap(bitmap)

    fun inputTensor(buffer: FloatBuffer): OnnxTensor =
        OnnxTensor.createTensor(env, buffer, longArrayOf(1, 3, 224, 224))

    private fun baseInputName(): String =
        if (baseSession.inputNames.contains("input_leaf")) "input_leaf" else baseSession.inputNames.first()

    /** Tier-1: DINOv2 INT8 + cosine prototypes + Shannon gate (all baked in the graph). */
    fun runTier1(input: OnnxTensor): Tier1Out {
        baseSession.run(mapOf(baseInputName() to input)).use { r ->
            @Suppress("UNCHECKED_CAST")
            val probs = (r[0].value as Array<FloatArray>)[0]
            @Suppress("UNCHECKED_CAST")
            val conf = (r[1].value as Array<FloatArray>)[0][0]
            @Suppress("UNCHECKED_CAST")
            val dino = (r[2].value as Array<FloatArray>)[0]
            val foliage = if (r.size() > 3) {
                @Suppress("UNCHECKED_CAST")
                (r[3].value as Array<FloatArray>)[0][0]
            } else 1.0f
            return Tier1Out(probs, conf, dino, foliage)
        }
    }

    /** Tier-2 incremental: BioCLIP INT8 + 896-D Fisher + text fusion (single baked graph). */
    fun runTier2(input: OnnxTensor, dino: FloatArray): Tier2Out {
        val session = companionSession ?: throw IllegalStateException("Tier-2 companion not loaded")
        val leafName = if (session.inputNames.contains("input_leaf")) "input_leaf" else session.inputNames.first()
        val map = HashMap<String, OnnxTensor>()
        map[leafName] = input
        var dinoTensor: OnnxTensor? = null
        if (session.inputNames.contains("dino_features")) {
            dinoTensor = OnnxTensor.createTensor(env, FloatBuffer.wrap(dino), longArrayOf(1, dino.size.toLong()))
            map["dino_features"] = dinoTensor
        }
        try {
            session.run(map).use { r ->
                @Suppress("UNCHECKED_CAST")
                val probs = (r[0].value as Array<FloatArray>)[0]
                val bio = if (r.size() > 1) {
                    @Suppress("UNCHECKED_CAST")
                    (r[1].value as Array<FloatArray>)[0]
                } else FloatArray(512)
                return Tier2Out(probs, bio)
            }
        } finally {
            dinoTensor?.close()
        }
    }

    override fun close() {
        try { companionSession?.close() } catch (_: Exception) {}
        try { baseSession.close() } catch (_: Exception) {}
    }
}

data class Tier1Out(val probs: FloatArray, val confidence: Float, val dino: FloatArray, val foliage: Float)
data class Tier2Out(val probs: FloatArray, val bio: FloatArray)