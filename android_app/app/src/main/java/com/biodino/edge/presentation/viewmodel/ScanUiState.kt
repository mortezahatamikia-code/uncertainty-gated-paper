package com.biodino.edge.presentation.viewmodel

import android.graphics.Bitmap
import com.biodino.edge.data.locale.AppLanguage
import com.biodino.edge.domain.model.CustomEnrolledDisease
import com.biodino.edge.domain.model.DiagnosisResult
import com.biodino.edge.domain.model.ScanHistoryItem

/**
 * Unidirectional UI state model for the plant scanner screen.
 * Fully internationalized with AppLanguage supporting LTR/RTL.
 */
data class ScanUiState(
    val isCameraPermissionGranted: Boolean = false,
    val isCameraActive: Boolean = true,
    val isScanningPaused: Boolean = false,
    val isTorchActive: Boolean = false,
    val isEcoMode: Boolean = false,
    val isTtsEnabled: Boolean = true,
    val currentLanguage: AppLanguage = AppLanguage.ENGLISH,
    val isLanguageDialogVisible: Boolean = false,
    val isBlurred: Boolean = false,
    val isTooDark: Boolean = false,
    val isNonLeaf: Boolean = false,
    val isAtlasOpen: Boolean = false,
    val isHistoryOpen: Boolean = false,
    val isEnrollmentOpen: Boolean = false,
    val isCalculatorOpen: Boolean = false,
    val isCareGuideOpen: Boolean = false,
    val isWeatherOpen: Boolean = false,
    val isSplitViewOpen: Boolean = false,
    val galleryBitmap: Bitmap? = null,
    val latestDiagnosis: DiagnosisResult? = null,
    val smoothedConfidence: Float = 0f,
    val averageLatencyMs: Float = 0f,
    val isHardwareAccelerated: Boolean = true,
    val errorMessage: String? = null,
    val scanHistory: List<ScanHistoryItem> = emptyList(),
    val customEnrolledDiseases: List<CustomEnrolledDisease> = emptyList()
) {
    val isFarsi: Boolean get() = currentLanguage == AppLanguage.PERSIAN
    val isRtl: Boolean get() = currentLanguage.isRtl
    val isConfidentlyLocked: Boolean
        get() = latestDiagnosis != null && !isTooDark && !isNonLeaf && smoothedConfidence >= 0.35f
}
