package com.biodino.edge.presentation.scan

import androidx.compose.runtime.Composable
import com.biodino.edge.data.locale.AppLanguage
import com.biodino.edge.data.locale.AppStrings
import com.biodino.edge.presentation.atlas.AtlasSheet
import com.biodino.edge.presentation.care.PlantCareSheet
import com.biodino.edge.presentation.common.LanguageSelectionDialog
import com.biodino.edge.presentation.dosage.DosageCalculatorSheet
import com.biodino.edge.presentation.enrollment.FewShotEnrollmentSheet
import com.biodino.edge.presentation.history.HistorySheet
import com.biodino.edge.presentation.modelmanager.ModelManagementSheet
import com.biodino.edge.presentation.viewmodel.ScanUiState
import com.biodino.edge.presentation.viewmodel.ScanViewModel
import com.biodino.edge.presentation.weather.WeatherWindowSheet

@Composable
fun ScanSheetsHost(
    state: ScanUiState,
    language: AppLanguage,
    strings: AppStrings,
    isFarsi: Boolean,
    viewModel: ScanViewModel
) {
    if (state.isEnrollmentOpen) {
        FewShotEnrollmentSheet(
            language = language,
            isFarsi = isFarsi,
            customClasses = state.customEnrolledDiseases,
            onEnroll = { name, host, latin, healthy, advice, photos, healthyPhotos ->
                viewModel.enrollCustomClass(name, host, latin, healthy, advice, photos, healthyPhotos)
            },
            onDeleteClass = { id -> viewModel.deleteCustomDisease(id) },
            onDismiss = { viewModel.openEnrollment(false) }
        )
    }

    if (state.isCalculatorOpen) {
        DosageCalculatorSheet(
            language = language,
            isFarsi = isFarsi,
            targetDisease = state.latestDiagnosis?.diseaseInfo,
            onDismiss = { viewModel.openCalculator(false) }
        )
    }

    if (state.isCareGuideOpen) {
        PlantCareSheet(
            language = language,
            isFarsi = isFarsi,
            disease = state.latestDiagnosis?.diseaseInfo,
            onDismiss = { viewModel.openCareGuide(false) }
        )
    }

    if (state.isWeatherOpen) {
        WeatherWindowSheet(
            language = language,
            isFarsi = isFarsi,
            onDismiss = { viewModel.openWeather(false) }
        )
    }

    if (state.isAtlasOpen) {
        AtlasSheet(
            language = language,
            isFarsi = isFarsi,
            customDiseases = state.customEnrolledDiseases,
            onDismiss = { viewModel.openAtlas(false) }
        )
    }

    if (state.isHistoryOpen) {
        HistorySheet(
            language = language,
            isFarsi = isFarsi,
            historyItems = state.scanHistory,
            onClearHistory = { viewModel.clearHistory() },
            onDismiss = { viewModel.openHistory(false) }
        )
    }

    if (state.isModelManagerOpen) {
        ModelManagementSheet(
            language = language,
            strings = strings,
            isUsingCustomModel = state.isUsingCustomModel,
            customModelSizeMb = state.customModelSizeMb,
            isDownloading = state.isDownloadingModel,
            downloadProgress = state.modelDownloadProgress,
            downloadedBytes = state.modelDownloadBytes,
            totalBytes = state.modelTotalBytes,
            errorMessage = state.modelDownloadError,
            currentUrl = state.modelDownloadUrl,
            onStartDownload = { url -> viewModel.startModelDownload(url) },
            onRevertDefaultModel = { viewModel.revertToDefaultModel() },
            onClose = { viewModel.openModelManager(false) }
        )
    }

    if (state.isLanguageDialogVisible) {
        LanguageSelectionDialog(
            currentLanguage = language,
            strings = strings,
            onSelectLanguage = { selected ->
                viewModel.setLanguage(selected)
            },
            onDismiss = { viewModel.showLanguageDialog(false) }
        )
    }
}

