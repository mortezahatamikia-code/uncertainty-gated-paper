package com.biodino.edge.presentation.viewmodel

import android.app.Application
import android.graphics.Bitmap
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.biodino.edge.data.engine.BioDinoOnnxEngine
import com.biodino.edge.data.engine.ImageQualityEvaluator
import com.biodino.edge.data.service.TtsManager
import com.biodino.edge.domain.repository.ScanHistoryRepository
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import java.util.concurrent.atomic.AtomicBoolean

class ScanViewModel(application: Application) : AndroidViewModel(application) {

    private val engine by lazy { BioDinoOnnxEngine(application.applicationContext) }
    private val ttsManager by lazy { TtsManager(application.applicationContext) }
    private val historyRepo by lazy { ScanHistoryRepository(application.applicationContext) }

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

    fun openAtlas(open: Boolean) {
        _uiState.update { it.copy(isAtlasOpen = open) }
    }

    fun openHistory(open: Boolean) {
        _uiState.update { it.copy(isHistoryOpen = open) }
    }

    fun clearHistory() {
        historyRepo.clearAll()
    }

    fun clearGalleryImage() {
        _uiState.update { it.copy(galleryBitmap = null) }
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
     * Ingests a camera frame for real-time inference with Eco-throttling and blur detection.
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

                val result = engine.classify(bitmap)

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

    /**
     * Analyzes a single static picture selected from device gallery.
     */
    fun analyzeGalleryImage(bitmap: Bitmap) {
        viewModelScope.launch(Dispatchers.Default) {
            try {
                val blurred = ImageQualityEvaluator.isBlurred(bitmap)
                val result = engine.classify(bitmap)

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
