package com.biodino.edge.data.engine

import android.content.Context
import android.graphics.Bitmap
import ai.onnxruntime.*
import com.biodino.edge.domain.model.CustomEnrolledDisease
import com.biodino.edge.domain.model.DiagnosisResult
import com.biodino.edge.domain.repository.PathologyCatalog
import java.io.InputStream
import kotlin.math.ln
import kotlin.math.max

/**
 * Encapsulates the ONNX Runtime Mobile session, hardware acceleration (NNAPI),
 * and dynamic support for on-device Few-Shot learning with custom enrolled prototypes.
 */
class BioDinoOnnxEngine(context: Context) : AutoCloseable {

    private val ortEnv: OrtEnvironment = OrtEnvironment.getEnvironment("BioDINO-Mobile")
    private var session: OrtSession
    private val preallocatedTensor = PreallocatedTensor()
    private val modelBytes: ByteArray

    var isNnapiActive: Boolean = false
        private set

    init {
        modelBytes = context.assets.open("biodino_mobile_int8.onnx").use { input: InputStream ->
            input.readBytes()
        }

        session = try {
            val nnapiOptions = OrtSession.SessionOptions().apply {
                addNnapi()
                setOptimizationLevel(OrtSession.SessionOptions.OptLevel.ALL_OPT)
            }
            val s = ortEnv.createSession(modelBytes, nnapiOptions)
            isNnapiActive = true
            s
        } catch (e: Exception) {
            isNnapiActive = false
            val cpuOptions = OrtSession.SessionOptions().apply {
                setInterOpNumThreads(2)
                setIntraOpNumThreads(4)
                setOptimizationLevel(OrtSession.SessionOptions.OptLevel.ALL_OPT)
            }
            ortEnv.createSession(modelBytes, cpuOptions)
        }
    }

    private fun runSession(tensor: OnnxTensor): OrtSession.Result {
        return try {
            session.run(mapOf("input_leaf" to tensor))
        } catch (e: OrtException) {
            if (isNnapiActive) {
                // NNAPI runtime kernel failure - seamlessly fallback to CPU execution
                isNnapiActive = false
                val cpuOptions = OrtSession.SessionOptions().apply {
                    setInterOpNumThreads(2)
                    setIntraOpNumThreads(4)
                    setOptimizationLevel(OrtSession.SessionOptions.OptLevel.ALL_OPT)
                }
                session.close()
                session = ortEnv.createSession(modelBytes, cpuOptions)
                session.run(mapOf("input_leaf" to tensor))
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
            runSession(tensor).use { results ->
                @Suppress("UNCHECKED_CAST")
                val features = (results[2].value as Array<FloatArray>)[0]
                return features.copyOf()
            }
        }
    }

    /**
     * Executes real-time forward pass on the input bitmap and dynamically enriches
     * the prediction manifold if custom enrolled few-shot prototypes exist.
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
            runSession(tensor).use { results ->
                @Suppress("UNCHECKED_CAST")
                val baseProbabilities = (results[0].value as Array<FloatArray>)[0]

                @Suppress("UNCHECKED_CAST")
                val baseConfidence = (results[1].value as Array<FloatArray>)[0][0]

                val latencyMs = (System.nanoTime() - t0) / 1_000_000.0f

                val foliageScore = if (results.size() > 3) {
                    @Suppress("UNCHECKED_CAST")
                    (results[3].value as Array<FloatArray>)[0][0]
                } else {
                    1.0f
                }

                val isDark = ImageQualityEvaluator.isTooDark(bitmap)

                if (customPrototypes.isEmpty()) {
                    return PathologyCatalog.buildDiagnosis(baseProbabilities, baseConfidence, latencyMs, foliageScore, isDark)
                }

                // If custom classes exist, evaluate similarity against custom support vectors
                @Suppress("UNCHECKED_CAST")
                val queryFeatures = (results[2].value as Array<FloatArray>)[0]

                val baseClassesCount = baseProbabilities.size
                val totalClasses = baseClassesCount + customPrototypes.size
                val combinedLogits = FloatArray(totalClasses)

                // Base class logits reconstructed from probabilities
                for (i in 0 until baseClassesCount) {
                    val p = max(baseProbabilities[i], 1e-12f)
                    combinedLogits[i] = ln(p)
                }

                // Custom class logits: 20.0 * dot(query, proto)
                for (j in customPrototypes.indices) {
                    val proto = customPrototypes[j].prototypeEmbedding
                    var dot = 0f
                    for (k in 0 until 384) {
                        dot += queryFeatures[k] * proto[k]
                    }
                    combinedLogits[baseClassesCount + j] = 20.0f * dot
                }

                // Softmax over all classes
                var maxLogit = Float.NEGATIVE_INFINITY
                for (l in combinedLogits) {
                    if (l > maxLogit) maxLogit = l
                }
                var sumExp = 0.0
                val combinedProbs = FloatArray(totalClasses)
                for (i in 0 until totalClasses) {
                    val e = Math.exp((combinedLogits[i] - maxLogit).toDouble())
                    combinedProbs[i] = e.toFloat()
                    sumExp += e
                }
                for (i in 0 until totalClasses) {
                    combinedProbs[i] = (combinedProbs[i] / sumExp).toFloat()
                }

                // Dynamic Shannon Confidence calculation
                var top1 = 0f
                var top2 = 0f
                var topIdx = 0
                for (i in 0 until totalClasses) {
                    val p = combinedProbs[i]
                    if (p > top1) {
                        top2 = top1
                        top1 = p
                        topIdx = i
                    } else if (p > top2) {
                        top2 = p
                    }
                }

                val margin = top1 - top2
                val lnK = ln(totalClasses.toDouble()).toFloat()
                var entropy = 0.0
                for (p in combinedProbs) {
                    if (p > 1e-12f) {
                        entropy -= p * ln(p.toDouble())
                    }
                }
                val normEntropy = (entropy / lnK).toFloat()
                val isFoliage = foliageScore >= 0.40f && !isDark
                val foliageGate = if (isFoliage) kotlin.math.min(1.0f, kotlin.math.max(0.0f, (foliageScore - 0.35f) / 0.20f)) else 0.0f
                val dynamicConfidence = margin * max(0f, 1.0f - normEntropy) * foliageGate

                val selectedDisease = if (topIdx < baseClassesCount) {
                    PathologyCatalog.NOVEL_DISEASES.getOrElse(topIdx) { PathologyCatalog.NOVEL_DISEASES[0] }
                } else {
                    customPrototypes[topIdx - baseClassesCount].toDiseaseInfo(topIdx)
                }

                return DiagnosisResult(
                    diseaseInfo = selectedDisease,
                    probability = top1,
                    confidence = dynamicConfidence,
                    latencyMs = latencyMs,
                    allProbabilities = combinedProbs,
                    foliageScore = foliageScore,
                    isFoliage = isFoliage,
                    isTooDark = isDark
                )
            }
        }
    }

    override fun close() {
        session.close()
        ortEnv.close()
    }
}
