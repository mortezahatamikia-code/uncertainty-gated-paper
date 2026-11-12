package com.biodino.edge.data.engine

import android.app.ActivityManager
import android.content.Context
import android.graphics.Bitmap
import android.os.Build
import ai.onnxruntime.*
import com.biodino.edge.domain.model.CustomEnrolledDisease
import com.biodino.edge.domain.model.DiagnosisResult
import com.biodino.edge.data.image.ImageQualityEvaluator
import com.biodino.edge.data.network.ModelDownloadManager
import com.biodino.edge.data.repository.PathologyCatalog
import java.io.InputStream
import kotlin.math.ln
import kotlin.math.max

/**
 * Manages the ONNX Runtime session, NNAPI hardware delegate, and custom prototype classification.
 */
class BioDinoOnnxEngine(context: Context) : AutoCloseable {

    private val appContext = context.applicationContext
    private val ortEnv: OrtEnvironment = OrtEnvironment.getEnvironment("BioDINO-Mobile")
    private val preallocatedTensor = PreallocatedTensor()

    private var baseSession: OrtSession
    private var baseModelBytes: ByteArray
    private var customSession: OrtSession? = null

    var isNnapiActive: Boolean = false
        private set

    var isUsingCustomModel: Boolean = false
        private set

    init {
        baseModelBytes = appContext.assets.open("biodino_mobile_int8.onnx").use { input: InputStream ->
            input.readBytes()
        }
        val (bSess, nnapi) = initSession(baseModelBytes)
        baseSession = bSess
        isNnapiActive = nnapi

        initCustomSessionIfAvailable()
    }

    private fun initCustomSessionIfAvailable() {
        if (ModelDownloadManager.isCustomModelActive(appContext)) {
            try {
                val customFile = ModelDownloadManager.getCustomModelFile(appContext)
                val bytes = customFile.readBytes()
                if (bytes.size >= 5 * 1024 * 1024) {
                    val (cSess, _) = initSession(bytes)
                    customSession = cSess
                    isUsingCustomModel = true
                    return
                }
            } catch (_: Exception) {
                customSession = null
                isUsingCustomModel = false
            }
        }
        customSession = null
        isUsingCustomModel = false
    }

    /**
     * Probes hardware and OS capabilities to safely determine if NNAPI hardware acceleration
     * should be enabled by default in the background.
     *
     * Strict safeguards for low-end / weak devices:
     * 1. Requires Android 10+ (API >= 29) where NNAPI 1.2+ is mature and stable.
     * 2. Requires total device RAM >= 3.5 GB (avoids OOM on low-RAM phones).
     * 3. Requires at least 6 CPU cores (avoids quad-core low-tier chips with broken vendor HALs).
     * 4. Excludes devices flagged as Low RAM device by Android OS.
     */
    private fun isDeviceNnapiCapable(): Boolean {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.Q) {
            return false
        }
        val activityManager = appContext.getSystemService(Context.ACTIVITY_SERVICE) as? ActivityManager
        if (activityManager?.isLowRamDevice == true) {
            return false
        }
        val memInfo = ActivityManager.MemoryInfo()
        activityManager?.getMemoryInfo(memInfo)
        val totalRamGb = memInfo.totalMem / (1024.0 * 1024.0 * 1024.0)
        if (totalRamGb < 3.5) {
            return false
        }
        val cores = Runtime.getRuntime().availableProcessors()
        if (cores < 6) {
            return false
        }
        return true
    }

    private fun initSession(bytes: ByteArray): Pair<OrtSession, Boolean> {
        if (isDeviceNnapiCapable()) {
            try {
                val nnapiOptions = OrtSession.SessionOptions().apply {
                    addNnapi()
                    setOptimizationLevel(OrtSession.SessionOptions.OptLevel.ALL_OPT)
                }
                val s = ortEnv.createSession(bytes, nnapiOptions)
                return Pair(s, true)
            } catch (e: Exception) {
                // Safe silent fallback to multi-threaded CPU if NNAPI driver binding fails
            }
        }
        val cpuOptions = OrtSession.SessionOptions().apply {
            setInterOpNumThreads(2)
            setIntraOpNumThreads(4)
            setOptimizationLevel(OrtSession.SessionOptions.OptLevel.ALL_OPT)
        }
        return Pair(ortEnv.createSession(bytes, cpuOptions), false)
    }

    /**
     * Dynamically reloads the ONNX model from storage (swapping between default asset
     * and downloaded companion model) without restarting the application.
     */
    @Synchronized
    fun reloadModel(): Boolean {
        return try {
            try {
                customSession?.close()
            } catch (_: Exception) {}
            customSession = null
            isUsingCustomModel = false

            if (ModelDownloadManager.isCustomModelActive(appContext)) {
                val customFile = ModelDownloadManager.getCustomModelFile(appContext)
                val bytes = customFile.readBytes()
                if (bytes.size >= 5 * 1024 * 1024) {
                    val (cSess, _) = initSession(bytes)
                    customSession = cSess
                    isUsingCustomModel = true
                    return true
                }
            }
            true
        } catch (_: Exception) {
            ModelDownloadManager.deleteCustomModel(appContext)
            try { customSession?.close() } catch (_: Exception) {}
            customSession = null
            isUsingCustomModel = false
            false
        }
    }

    private fun runBaseSession(tensor: OnnxTensor): OrtSession.Result {
        val inputName = if (baseSession.inputNames.contains("input_leaf")) "input_leaf" else baseSession.inputNames.first()
        return try {
            baseSession.run(mapOf(inputName to tensor))
        } catch (e: OrtException) {
            if (isNnapiActive) {
                // NNAPI runtime kernel failure - seamlessly fallback to CPU execution
                isNnapiActive = false
                val cpuOptions = OrtSession.SessionOptions().apply {
                    setInterOpNumThreads(2)
                    setIntraOpNumThreads(4)
                    setOptimizationLevel(OrtSession.SessionOptions.OptLevel.ALL_OPT)
                }
                baseSession.close()
                baseSession = ortEnv.createSession(baseModelBytes, cpuOptions)
                baseSession.run(mapOf(inputName to tensor))
            } else {
                throw e
            }
        }
    }

    /**
     * Extracts the 384-dimensional L2-normalized DINOv2 visual embedding from an input image.
     */
    @Synchronized
    fun extractEmbedding(bitmap: Bitmap): FloatArray {
        val buffer = preallocatedTensor.loadFromBitmap(bitmap)
        val inputShape = longArrayOf(1, 3, 224, 224)
        val inputTensor = OnnxTensor.createTensor(ortEnv, buffer, inputShape)

        inputTensor.use { tensor ->
            runBaseSession(tensor).use { results ->
                @Suppress("UNCHECKED_CAST")
                val features = (results[2].value as Array<FloatArray>)[0]
                return features.copyOf()
            }
        }
    }

    /**
     * Runs model inference on the input bitmap and combines base predictions
     * with any custom enrolled prototypes.
     */
    @Synchronized
    fun classify(
        bitmap: Bitmap,
        customPrototypes: List<CustomEnrolledDisease> = emptyList()
    ): DiagnosisResult {
        val t0 = System.nanoTime()

        val buffer = preallocatedTensor.loadFromBitmap(bitmap)
        val inputShape = longArrayOf(1, 3, 224, 224)

        val inputTensor = OnnxTensor.createTensor(ortEnv, buffer, inputShape)

        inputTensor.use { tensor ->
            runBaseSession(tensor).use { results ->
                @Suppress("UNCHECKED_CAST")
                var activeProbabilities = (results[0].value as Array<FloatArray>)[0]

                @Suppress("UNCHECKED_CAST")
                val baseConfidence = (results[1].value as Array<FloatArray>)[0][0]

                @Suppress("UNCHECKED_CAST")
                val queryFeatures = (results[2].value as Array<FloatArray>)[0]

                val latencyMs = (System.nanoTime() - t0) / 1_000_000.0f

                val foliageScore = if (results.size() > 3) {
                    @Suppress("UNCHECKED_CAST")
                    (results[3].value as Array<FloatArray>)[0][0]
                } else {
                    1.0f
                }

                val isDark = ImageQualityEvaluator.isTooDark(bitmap)

                // If companion model is active, run it with input_leaf + dino_features
                val currentCustomSession = customSession
                if (currentCustomSession != null) {
                    try {
                        val inputMap = mutableMapOf<String, OnnxTensor>()
                        val leafName = if (currentCustomSession.inputNames.contains("input_leaf")) "input_leaf" else currentCustomSession.inputNames.first()
                        inputMap[leafName] = tensor

                        var dinoTensor: OnnxTensor? = null
                        if (currentCustomSession.inputNames.contains("dino_features")) {
                            dinoTensor = OnnxTensor.createTensor(
                                ortEnv,
                                java.nio.FloatBuffer.wrap(queryFeatures),
                                longArrayOf(1, queryFeatures.size.toLong())
                            )
                            inputMap["dino_features"] = dinoTensor
                        }

                        try {
                            currentCustomSession.run(inputMap).use { companionResults ->
                                @Suppress("UNCHECKED_CAST")
                                activeProbabilities = (companionResults[0].value as Array<FloatArray>)[0]
                            }
                        } finally {
                            dinoTensor?.close()
                        }
                    } catch (e: Exception) {
                        // Safe fallback to base model if companion model evaluation fails
                        android.util.Log.w("BioDinoEngine", "Companion inference fallback to base: ${e.message}")
                    }
                }

                if (customPrototypes.isEmpty()) {
                    return PathologyCatalog.buildDiagnosis(activeProbabilities, baseConfidence, latencyMs, foliageScore, isDark)
                }

                // If custom classes exist, evaluate similarity against custom support vectors
                return InferenceMath.fuseCustomPrototypes(
                    baseProbabilities = activeProbabilities,
                    baseConfidence = baseConfidence,
                    queryFeatures = queryFeatures,
                    customPrototypes = customPrototypes,
                    foliageScore = foliageScore,
                    isDark = isDark,
                    latencyMs = latencyMs
                )
            }
        }
    }

    override fun close() {
        try { customSession?.close() } catch (_: Exception) {}
        try { baseSession.close() } catch (_: Exception) {}
        ortEnv.close()
    }
}
