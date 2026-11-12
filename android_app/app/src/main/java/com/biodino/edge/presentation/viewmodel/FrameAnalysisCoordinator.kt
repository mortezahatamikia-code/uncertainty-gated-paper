package com.biodino.edge.presentation.viewmodel

import android.graphics.Bitmap
import com.biodino.edge.data.engine.BioDinoOnnxEngine
import com.biodino.edge.data.image.ImageQualityEvaluator
import com.biodino.edge.data.locale.I18n
import com.biodino.edge.data.service.TtsManager
import com.biodino.edge.data.repository.ScanHistoryRepository
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.util.concurrent.atomic.AtomicBoolean

class FrameAnalysisCoordinator(
    private val engine: BioDinoOnnxEngine,
    private val historyRepo: ScanHistoryRepository,
    private val ttsManager: TtsManager,
    private val uiState: MutableStateFlow<ScanUiState>,
    private val scope: CoroutineScope
) {
    private val isAnalyzing = AtomicBoolean(false)
    private var lastFrameTimestamp = 0L
    private var lastRecordedHistoryKey: String? = null
    private var lastRecordedTimestamp = 0L

    fun analyzeFrame(bitmap: Bitmap) {
        val currentState = uiState.value
        if (currentState.isScanningPaused || !currentState.isCameraActive || currentState.galleryBitmap != null) return

        val now = System.currentTimeMillis()
        // Eco mode frame throttle (~15 fps)
        if (currentState.isEcoMode && (now - lastFrameTimestamp) < 66L) {
            return
        }

        if (!isAnalyzing.compareAndSet(false, true)) {
            return
        }

        lastFrameTimestamp = now

        scope.launch(Dispatchers.Default) {
            try {
                val blurred = ImageQualityEvaluator.isBlurred(bitmap)
                val tooDark = ImageQualityEvaluator.isTooDark(bitmap)

                // Run inference
                val result = engine.classify(bitmap, currentState.customEnrolledDiseases)

                val effectiveDark = result.isTooDark || tooDark
                val isNonLeaf = !result.isFoliage && !effectiveDark

                // Zero confidence if dark or non-leaf
                val frameScore = if (result.isFoliage && !effectiveDark) result.confidence else 0f

                // Smooth confidence and latency (EMA)
                val prevConf = if (currentState.smoothedConfidence == 0f) frameScore else currentState.smoothedConfidence
                val smoothedConf = (0.65f * prevConf) + (0.35f * frameScore)

                val prevLat = if (currentState.averageLatencyMs == 0f) result.latencyMs else currentState.averageLatencyMs
                val smoothedLat = (0.80f * prevLat) + (0.20f * result.latencyMs)

                uiState.update {
                    it.copy(
                        isBlurred = blurred,
                        isTooDark = effectiveDark,
                        isNonLeaf = isNonLeaf,
                        latestDiagnosis = result,
                        smoothedConfidence = smoothedConf,
                        averageLatencyMs = smoothedLat,
                        errorMessage = null
                    )
                }

                // Record scan and speak diagnosis when locked
                if (smoothedConf >= 0.35f && result.isFoliage && !effectiveDark && !isNonLeaf) {
                    val key = result.diseaseInfo.rawKey
                    val timeSinceLastRecord = now - lastRecordedTimestamp

                    if (key != lastRecordedHistoryKey || timeSinceLastRecord > 15000L) {
                        lastRecordedHistoryKey = key
                        lastRecordedTimestamp = now
                        historyRepo.addFromDiagnosis(result)

                        if (uiState.value.isTtsEnabled) {
                            val percent = (smoothedConf * 100).toInt()
                            ttsManager.speakDiagnosis(
                                result.diseaseInfo.commonName,
                                percent,
                                result.diseaseInfo.isHealthy
                            )
                        }
                    }
                }
            } catch (e: Exception) {
                val errorString = I18n.getStrings(uiState.value.currentLanguage).errImageAnalysis
                uiState.update { it.copy(errorMessage = "$errorString: ${e.localizedMessage ?: ""}") }
            } finally {
                isAnalyzing.set(false)
            }
        }
    }

    fun onGalleryError(msg: String) {
        uiState.update { it.copy(errorMessage = msg) }
    }

    fun analyzeGalleryImage(bitmap: Bitmap) {
        // 1. Immediately present the gallery photo to the user with a scanning state
        uiState.update {
            it.copy(
                galleryBitmap = bitmap,
                latestDiagnosis = null,
                smoothedConfidence = 0f,
                isTooDark = false,
                isNonLeaf = false,
                errorMessage = null
            )
        }

        scope.launch(Dispatchers.Default) {
            try {
                val blurred = ImageQualityEvaluator.isBlurred(bitmap)
                val tooDark = ImageQualityEvaluator.isTooDark(bitmap)
                val result = engine.classify(bitmap, uiState.value.customEnrolledDiseases)

                val effectiveDark = result.isTooDark || tooDark
                val isNonLeaf = !result.isFoliage && !effectiveDark

                // For static gallery images, true confidence is calibrated Shannon margin * foliage gate
                val displayConfidence = if (result.isFoliage && !effectiveDark) result.confidence else 0f

                uiState.update {
                    it.copy(
                        isBlurred = blurred,
                        isTooDark = effectiveDark,
                        isNonLeaf = isNonLeaf,
                        latestDiagnosis = result,
                        smoothedConfidence = displayConfidence,
                        averageLatencyMs = result.latencyMs,
                        errorMessage = null
                    )
                }

                // Only record to history and trigger TTS if valid foliage and not dark
                if (result.isFoliage && !effectiveDark && !isNonLeaf && displayConfidence >= 0.35f) {
                    historyRepo.addFromDiagnosis(result)

                    if (uiState.value.isTtsEnabled) {
                        val percent = (displayConfidence * 100).toInt()
                        ttsManager.speakDiagnosis(
                            result.diseaseInfo.commonName,
                            percent,
                            result.diseaseInfo.isHealthy,
                            force = true
                        )
                    }
                }
            } catch (e: Throwable) {
                val strings = I18n.getStrings(uiState.value.currentLanguage)
                uiState.update { it.copy(errorMessage = "${strings.errImageAnalysis}: ${e.message}") }
            }
        }
    }
}

