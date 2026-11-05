package com.biodino.edge.presentation.viewmodel

import android.app.Application
import android.graphics.Bitmap
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.biodino.edge.data.engine.BioDinoOnnxEngine
import com.biodino.edge.data.image.ImageQualityEvaluator
import com.biodino.edge.data.network.ModelDownloadManager
import com.biodino.edge.data.locale.AppLanguage
import com.biodino.edge.data.locale.I18n
import com.biodino.edge.data.service.TtsManager
import com.biodino.edge.domain.model.CustomEnrolledDisease
import com.biodino.edge.data.repository.CustomPrototypesRepository
import com.biodino.edge.data.repository.ScanHistoryRepository
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

    private val frameCoordinator by lazy {
        FrameAnalysisCoordinator(
            engine = engine,
            historyRepo = historyRepo,
            ttsManager = ttsManager,
            uiState = _uiState,
            scope = viewModelScope
        )
    }

    private val modelCoordinator by lazy {
        ModelDownloadCoordinator(
            context = application.applicationContext,
            engine = engine,
            uiState = _uiState,
            scope = viewModelScope
        )
    }

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

        // Initialize engine state and active model status asynchronously
        viewModelScope.launch(Dispatchers.Default) {
            try {
                val nnapi = engine.isNnapiActive
                val isCustom = engine.isUsingCustomModel
                val customSize = ModelDownloadManager.getCustomModelSizeMb(application.applicationContext)
                _uiState.update {
                    it.copy(
                        isHardwareAccelerated = nnapi,
                        isUsingCustomModel = isCustom,
                        customModelSizeMb = customSize
                    )
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(errorMessage = "Engine init warning: ${e.message}") }
            }
        }
    }

    fun onPermissionResult(granted: Boolean) {
        _uiState.update { it.copy(isCameraPermissionGranted = granted) }
    }

    fun toggleCameraActive(active: Boolean? = null) {
        _uiState.update { current ->
            val next = active ?: !current.isCameraActive
            if (!next) {
                ttsManager.stop()
            }
            current.copy(
                isCameraActive = next,
                isTorchActive = if (!next) false else current.isTorchActive,
                isTooDark = if (!next) false else current.isTooDark,
                isNonLeaf = if (!next) false else current.isNonLeaf,
                latestDiagnosis = if (!next) null else current.latestDiagnosis,
                smoothedConfidence = if (!next) 0f else current.smoothedConfidence,
                averageLatencyMs = if (!next) 0f else current.averageLatencyMs
            )
        }
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
        _uiState.update { current ->
            val next = if (current.currentLanguage == AppLanguage.PERSIAN) AppLanguage.ENGLISH else AppLanguage.PERSIAN
            current.copy(currentLanguage = next)
        }
    }

    fun setLanguage(lang: AppLanguage) {
        _uiState.update { it.copy(currentLanguage = lang, isLanguageDialogVisible = false) }
    }

    fun showLanguageDialog(show: Boolean) {
        _uiState.update { it.copy(isLanguageDialogVisible = show) }
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

    fun openCareGuide(open: Boolean) {
        _uiState.update { it.copy(isCareGuideOpen = open) }
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
        _uiState.update { it.copy(galleryBitmap = null, latestDiagnosis = null, smoothedConfidence = 0f, isTooDark = false, isNonLeaf = false, errorMessage = null) }
    }

    fun clearErrorMessage() {
        _uiState.update { it.copy(errorMessage = null) }
    }

    fun clearSuccessMessage() {
        _uiState.update { it.copy(successMessage = null) }
    }

    fun deleteCustomDisease(id: String) {
        customPrototypesRepo.deleteCustomDisease(id)
    }

    fun speakCurrentDiagnosis() {
        val diag = _uiState.value.latestDiagnosis ?: return
        val percent = (diag.confidence * 100).toInt()
        val lang = _uiState.value.currentLanguage
        val localizedName = diag.diseaseInfo.getLocalizedName(lang)
        ttsManager.speakDiagnosis(
            localizedName,
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
        photos: List<Bitmap>,
        healthyPhotos: List<Bitmap> = emptyList()
    ) {
        if (photos.isEmpty()) return

        viewModelScope.launch(Dispatchers.Default) {
            try {
                val proto = computePrototype(photos)
                customPrototypesRepo.enrollNewDisease(
                    commonName = name,
                    hostPlant = hostPlant,
                    latinName = latin,
                    isHealthy = isHealthy,
                    symptom = "Calibrated on-device via ${photos.size} live foliar shots.",
                    advice = advice,
                    calibratedPrototype = proto
                )

                if (healthyPhotos.isNotEmpty()) {
                    val hProto = computePrototype(healthyPhotos)
                    val hName = if (hostPlant.isNotBlank()) "$hostPlant (Healthy)" else "$name (Healthy)"
                    customPrototypesRepo.enrollNewDisease(hName, hostPlant, latin, true, "Healthy baseline foliage.", "Plant is healthy. Continue balanced monitoring.", hProto)
                }

                val strings = I18n.getStrings(_uiState.value.currentLanguage)
                _uiState.update { it.copy(isEnrollmentOpen = false, errorMessage = null, successMessage = strings.classEnrolledSuccess(name, photos.size)) }
            } catch (e: Exception) {
                val errPrefix = I18n.getStrings(_uiState.value.currentLanguage).errEnrollmentFailed
                _uiState.update { it.copy(errorMessage = "$errPrefix: ${e.message ?: ""}") }
            }
        }
    }

    private fun computePrototype(bitmaps: List<Bitmap>): FloatArray {
        val sum = FloatArray(384)
        for (bmp in bitmaps) {
            val emb = engine.extractEmbedding(bmp)
            for (i in 0 until 384) sum[i] += emb[i]
        }
        val count = bitmaps.size.toFloat()
        var sumSq = 0.0
        for (i in 0 until 384) {
            val avg = sum[i] / count
            sum[i] = avg
            sumSq += (avg * avg)
        }
        val norm = sqrt(sumSq).toFloat()
        return FloatArray(384) { i -> if (norm > 0f) sum[i] / norm else 0f }
    }

    fun analyzeFrame(bitmap: Bitmap) = frameCoordinator.analyzeFrame(bitmap)
    fun onGalleryError(msg: String) = frameCoordinator.onGalleryError(msg)
    fun analyzeGalleryImage(bitmap: Bitmap) = frameCoordinator.analyzeGalleryImage(bitmap)

    fun openModelManager(open: Boolean) = modelCoordinator.openModelManager(open)
    fun setModelDownloadUrl(url: String) = modelCoordinator.setModelDownloadUrl(url)
    fun startModelDownload(customUrl: String? = null) = modelCoordinator.startModelDownload(customUrl)
    fun revertToDefaultModel() = modelCoordinator.revertToDefaultModel()

    override fun onCleared() {
        super.onCleared()
        try {
            ttsManager.shutdown()
            engine.close()
        } catch (_: Exception) {}
    }
}
