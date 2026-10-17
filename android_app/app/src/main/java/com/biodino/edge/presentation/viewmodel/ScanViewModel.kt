package com.biodino.edge.presentation.viewmodel

import android.app.Application
import android.graphics.Bitmap
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.biodino.edge.data.engine.BioDinoOnnxEngine
import com.biodino.edge.data.engine.ImageQualityEvaluator
import com.biodino.edge.data.service.TtsManager
import com.biodino.edge.domain.model.CustomEnrolledDisease
import com.biodino.edge.domain.repository.CustomPrototypesRepository
import com.biodino.edge.domain.repository.ScanHistoryRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.util.concurrent.atomic.AtomicBoolean
import kotlin.math.sqrt

class ScanViewModel(application: Application) : AndroidViewModel(application) {

    private val engine by lazy { BioDinoOnnxEngine(application.applicationContext) }
    private val ttsManager by lazy { TtsManager(application.applicationContext) }
    private val historyRepo by lazy { ScanHistoryRepository(application.applicationContext) }
    private val customPrototypesRepo by lazy { CustomPrototypesRepository(application.applicationContext) }

    private val isAnalyzing = AtomicBoolean(false)
    private var lastFrameTimestamp = 0L
    private var lastRecordedHistoryKey: String? = null
    private var lastRecordedTimestamp = 0L

    private val _uiState = MutableStateFlow(
        ScanUiState(
            isHardwareAccelerated = true
        )
    )
    val uiState: StateFlow<ScanUiState> = _uiState.asStateFlow()

    init {
        // Collect history stream
        viewModelScope.launch {
            historyRepo.history.collect { items ->
                _uiState.update { it.copy(scanHistory = items) }
            }
        }

        // Collect custom enrolled classes stream
        viewModelScope.launch {
            customPrototypesRepo.customPrototypes.collect { customClasses ->
                _uiState.update { it.copy(customEnrolledDiseases = customClasses) }
            }
        }

        // Initialize engine state asynchronously
        viewModelScope.launch(Dispatchers.Default) {
            try {
                val nnapi = engine.isNnapiActive
                _uiState.update { it.copy(isHardwareAccelerated = nnapi) }
            } catch (e: Exception) {
                _uiState.update { it.copy(errorMessage = "Engine init warning: ${e.message}") }
            }
        }
    }

    fun onPermissionResult(granted: Boolean) {
        _uiState.update { it.copy(isCameraPermissionGranted = granted) }
    }

    fun toggleScanningPause() {
        _uiState.update { it.copy(isScanningPaused = !it.isScanningPaused) }
    }

    fun toggleTorch() {
        _uiState.update { it.copy(isTorchActive = !it.isTorchActive) }
    }

    fun toggleEcoMode() {
        _uiState.update { it.copy(isEcoMode = !it.isEcoMode) }
    }

    fun toggleTts() {
        val next = !_uiState.value.isTtsEnabled
        if (!next) {
            ttsManager.stop()
        }
        _uiState.update { it.copy(isTtsEnabled = next) }
    }

    fun toggleFarsi() {
        _uiState.update { it.copy(isFarsi = !it.isFarsi) }
    }

    fun openAtlas(open: Boolean) {
        _uiState.update { it.copy(isAtlasOpen = open) }
    }

    fun openHistory(open: Boolean) {
        _uiState.update { it.copy(isHistoryOpen = open) }
    }

    fun openEnrollment(open: Boolean) {
        _uiState.update { it.copy(isEnrollmentOpen = open) }
    }

    fun openCalculator(open: Boolean) {
        _uiState.update { it.copy(isCalculatorOpen = open) }
    }

    fun openWeather(open: Boolean) {
        _uiState.update { it.copy(isWeatherOpen = open) }
    }

    fun openSplitView(open: Boolean) {
        _uiState.update { it.copy(isSplitViewOpen = open) }
    }

    fun clearHistory() {
        historyRepo.clearAll()
    }

    fun clearGalleryImage() {
        _uiState.update { it.copy(galleryBitmap = null) }
    }

    fun deleteCustomDisease(id: String) {
        customPrototypesRepo.deleteCustomDisease(id)
    }

    fun speakCurrentDiagnosis() {
        val diag = _uiState.value.latestDiagnosis ?: return
        val percent = (diag.confidence * 100).toInt()
        ttsManager.speakDiagnosis(
            diag.diseaseInfo.commonName,
            percent,
            diag.diseaseInfo.isHealthy,
            force = true
        )
    }

    /**
     * Executes In-Field Few-Shot Calibration across 5 captured leaf photos:
     * 1. Extracts 384-dimensional DINOv2 embeddings for all 5 shots.
     * 2. Computes the normalized centroid prototype vector in R^384.
     * 3. Persists new prototype for live inference.
     */
    fun enrollCustomClass(
        name: String,
        hostPlant: String,
        latin: String,
        isHealthy: Boolean,
        advice: String,
        photos: List<Bitmap>
    ) {
        if (photos.isEmpty()) return

        viewModelScope.launch(Dispatchers.Default) {
            try {
                val sumEmbedding = FloatArray(384)
                for (bmp in photos) {
                    val emb = engine.extractEmbedding(bmp)
                    for (i in 0 until 384) {
                        sumEmbedding[i] += emb[i]
                    }
                }

                // Average & L2 Normalization
                val count = photos.size.toFloat()
                var sumSq = 0.0
                for (i in 0 until 384) {
                    val avg = sumEmbedding[i] / count
                    sumEmbedding[i] = avg
                    sumSq += (avg * avg)
                }

                val norm = sqrt(sumSq).toFloat()
                val calibratedPrototype = FloatArray(384)
                for (i in 0 until 384) {
                    calibratedPrototype[i] = if (norm > 0f) sumEmbedding[i] / norm else 0f
                }

                customPrototypesRepo.enrollNewDisease(
                    commonName = name,
                    hostPlant = hostPlant,
                    latinName = latin,
                    isHealthy = isHealthy,
                    symptom = "Calibrated on-device via ${photos.size} live foliar shots.",
                    advice = advice,
                    calibratedPrototype = calibratedPrototype
                )

                _uiState.update {
                    it.copy(
                        isEnrollmentOpen = false,
                        errorMessage = "Enrolled \"$name\" ($photos.size-shot prototype) successfully!"
                    )
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(errorMessage = "Enrollment error: ${e.message}") }
            }
        }
    }

    /**
     * Ingests a camera frame for real-time inference with dynamic support for custom prototypes.
     */
    fun analyzeFrame(bitmap: Bitmap) {
        val currentState = _uiState.value
        if (currentState.isScanningPaused || currentState.galleryBitmap != null) return

        val now = System.currentTimeMillis()
        // Eco Mode: throttle to ~15 FPS (66ms) instead of 60 FPS
        if (currentState.isEcoMode && (now - lastFrameTimestamp) < 66L) {
            return
        }

        if (!isAnalyzing.compareAndSet(false, true)) {
            return
        }

        lastFrameTimestamp = now

        viewModelScope.launch(Dispatchers.Default) {
            try {
                // Blur check
                val blurred = ImageQualityEvaluator.isBlurred(bitmap)
                _uiState.update { it.copy(isBlurred = blurred) }

                // Classification taking into account any custom enrolled prototypes
                val result = engine.classify(bitmap, currentState.customEnrolledDiseases)

                // Exponential Moving Average
                val prevConf = if (currentState.smoothedConfidence == 0f) result.confidence else currentState.smoothedConfidence
                val smoothedConf = (0.65f * prevConf) + (0.35f * result.confidence)

                val prevLat = if (currentState.averageLatencyMs == 0f) result.latencyMs else currentState.averageLatencyMs
                val smoothedLat = (0.80f * prevLat) + (0.20f * result.latencyMs)

                _uiState.update {
                    it.copy(
                        latestDiagnosis = result,
                        smoothedConfidence = smoothedConf,
                        averageLatencyMs = smoothedLat,
                        errorMessage = null
                    )
                }

                // If confident lock is achieved, trigger TTS and record to history
                if (smoothedConf >= 0.35f) {
                    val key = result.diseaseInfo.rawKey
                    val timeSinceLastRecord = now - lastRecordedTimestamp

                    if (key != lastRecordedHistoryKey || timeSinceLastRecord > 15000L) {
                        lastRecordedHistoryKey = key
                        lastRecordedTimestamp = now
                        historyRepo.addFromDiagnosis(result)

                        if (_uiState.value.isTtsEnabled) {
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
                _uiState.update { it.copy(errorMessage = "Inference failed: ${e.localizedMessage}") }
            } finally {
                isAnalyzing.set(false)
            }
        }
    }

    fun analyzeGalleryImage(bitmap: Bitmap) {
        viewModelScope.launch(Dispatchers.Default) {
            try {
                val blurred = ImageQualityEvaluator.isBlurred(bitmap)
                val result = engine.classify(bitmap, _uiState.value.customEnrolledDiseases)

                _uiState.update {
                    it.copy(
                        galleryBitmap = bitmap,
                        isBlurred = blurred,
                        latestDiagnosis = result,
                        smoothedConfidence = result.confidence,
                        averageLatencyMs = result.latencyMs
                    )
                }

                historyRepo.addFromDiagnosis(result)

                if (_uiState.value.isTtsEnabled) {
                    val percent = (result.confidence * 100).toInt()
                    ttsManager.speakDiagnosis(
                        result.diseaseInfo.commonName,
                        percent,
                        result.diseaseInfo.isHealthy,
                        force = true
                    )
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(errorMessage = "Gallery scan failed: ${e.message}") }
            }
        }
    }

    override fun onCleared() {
        super.onCleared()
        try {
            ttsManager.shutdown()
            engine.close()
        } catch (_: Exception) {}
    }
}
