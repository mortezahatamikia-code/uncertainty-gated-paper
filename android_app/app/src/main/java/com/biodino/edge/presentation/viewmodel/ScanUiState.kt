package com.biodino.edge.presentation.viewmodel

import android.graphics.Bitmap
import com.biodino.edge.domain.model.DiagnosisResult
import com.biodino.edge.domain.model.ScanHistoryItem

/**
 * Unidirectional UI state model for the plant scanner screen.
 */
data class ScanUiState(
    val isCameraPermissionGranted: Boolean = false,
    val isScanningPaused: Boolean = false,
    val isTorchActive: Boolean = false,
    val isEcoMode: Boolean = false,
    val isTtsEnabled: Boolean = true,
    val isBlurred: Boolean = false,
    val isAtlasOpen: Boolean = false,
    val isHistoryOpen: Boolean = false,
    val galleryBitmap: Bitmap? = null,
    val latestDiagnosis: DiagnosisResult? = null,
    val smoothedConfidence: Float = 0f,
    val averageLatencyMs: Float = 0f,
    val isHardwareAccelerated: Boolean = true,
    val errorMessage: String? = null,
    val scanHistory: List<ScanHistoryItem> = emptyList()
) {
    val isConfidentlyLocked: Boolean
        get() = latestDiagnosis != null && smoothedConfidence >= 0.35f
}
