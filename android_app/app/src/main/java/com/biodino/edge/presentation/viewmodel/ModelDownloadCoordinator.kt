package com.biodino.edge.presentation.viewmodel

import android.content.Context
import com.biodino.edge.data.engine.BioDinoOnnxEngine
import com.biodino.edge.data.network.ModelDownloadManager
import com.biodino.edge.data.locale.I18n
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

class ModelDownloadCoordinator(
    private val context: Context,
    private val engine: BioDinoOnnxEngine,
    private val uiState: MutableStateFlow<ScanUiState>,
    private val scope: CoroutineScope
) {
    fun openModelManager(open: Boolean) {
        uiState.update {
            it.copy(
                isModelManagerOpen = open,
                modelDownloadError = null
            )
        }
    }

    fun setModelDownloadUrl(url: String) {
        uiState.update { it.copy(modelDownloadUrl = url) }
    }

    fun startModelDownload(customUrl: String? = null) {
        val targetUrl = customUrl ?: uiState.value.modelDownloadUrl
        if (targetUrl.isBlank() || uiState.value.isDownloadingModel) return

        uiState.update {
            it.copy(
                isDownloadingModel = true,
                modelDownloadProgress = 0f,
                modelDownloadBytes = 0L,
                modelTotalBytes = 0L,
                modelDownloadError = null
            )
        }

        scope.launch {
            val result = ModelDownloadManager.downloadModel(
                context = context,
                downloadUrl = targetUrl
            ) { downloaded, total, progress ->
                uiState.update {
                    it.copy(
                        modelDownloadBytes = downloaded,
                        modelTotalBytes = total,
                        modelDownloadProgress = progress
                    )
                }
            }

            result.fold(
                onSuccess = { targetFile ->
                    val reloadOk = engine.reloadModel()
                    val sizeMb = targetFile.length() / (1024f * 1024f)
                    val strings = I18n.getStrings(uiState.value.currentLanguage)
                    uiState.update {
                        it.copy(
                            isDownloadingModel = false,
                            modelDownloadProgress = 1f,
                            isUsingCustomModel = engine.isUsingCustomModel,
                            customModelSizeMb = sizeMb,
                            isHardwareAccelerated = engine.isNnapiActive,
                            modelDownloadError = if (!reloadOk) strings.errModelLoadFailedReverted else null
                        )
                    }
                },
                onFailure = { error ->
                    val strings = I18n.getStrings(uiState.value.currentLanguage)
                    uiState.update {
                        it.copy(
                            isDownloadingModel = false,
                            modelDownloadError = error.message ?: strings.errModelDownloadFailed
                        )
                    }
                }
            )
        }
    }

    fun revertToDefaultModel() {
        ModelDownloadManager.deleteCustomModel(context)
        engine.reloadModel()
        uiState.update {
            it.copy(
                isUsingCustomModel = engine.isUsingCustomModel,
                customModelSizeMb = 0f,
                isHardwareAccelerated = engine.isNnapiActive,
                modelDownloadError = null
            )
        }
    }
}

