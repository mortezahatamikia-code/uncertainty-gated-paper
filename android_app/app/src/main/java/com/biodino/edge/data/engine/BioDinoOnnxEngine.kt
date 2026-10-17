package com.biodino.edge.data.engine

import android.content.Context
import android.graphics.Bitmap
import ai.onnxruntime.*
import com.biodino.edge.domain.model.DiagnosisResult
import com.biodino.edge.domain.repository.PathologyCatalog
import java.io.InputStream

/**
 * Encapsulates the ONNX Runtime Mobile runtime session, hardware acceleration (NNAPI),
 * and model lifecycle for BioDINO-Edge.
 */
class BioDinoOnnxEngine(context: Context) : AutoCloseable {

    private val ortEnv: OrtEnvironment = OrtEnvironment.getEnvironment("BioDINO-Mobile")
    private val session: OrtSession
    private val preallocatedTensor = PreallocatedTensor()

    var isNnapiActive: Boolean = false
        private set

    init {
        val sessionOptions = OrtSession.SessionOptions().apply {
            try {
                addNnapi()
                isNnapiActive = true
            } catch (e: Exception) {
                isNnapiActive = false
                // Multi-threaded CPU fallback
                setInterOpNumThreads(2)
                setIntraOpNumThreads(4)
                setOptimizationLevel(OrtSession.SessionOptions.OptLevel.ALL_OPT)
            }
        }

        val modelBytes = context.assets.open("biodino_mobile_int8.onnx").use { input: InputStream ->
            input.readBytes()
        }

        session = ortEnv.createSession(modelBytes, sessionOptions)
    }

    /**
     * Executes real-time forward pass on the input bitmap and computes probabilities and Shannon confidence.
     */
    fun classify(bitmap: Bitmap): DiagnosisResult {
        val t0 = System.nanoTime()

        val buffer = preallocatedTensor.loadFromBitmap(bitmap)
        val inputShape = longArrayOf(1, 3, 224, 224)

        val inputTensor = OnnxTensor.createTensor(ortEnv, buffer, inputShape)

        inputTensor.use { tensor ->
            session.run(mapOf("input_leaf" to tensor)).use { results ->
                @Suppress("UNCHECKED_CAST")
                val probabilities = (results[0].value as Array<FloatArray>)[0]

                @Suppress("UNCHECKED_CAST")
                val confidence = (results[1].value as Array<FloatArray>)[0][0]

                val latencyMs = (System.nanoTime() - t0) / 1_000_000.0f
                return PathologyCatalog.buildDiagnosis(probabilities, confidence, latencyMs)
            }
        }
    }

    override fun close() {
        session.close()
        ortEnv.close()
    }
}
