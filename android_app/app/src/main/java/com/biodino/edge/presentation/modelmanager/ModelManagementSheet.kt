package com.biodino.edge.presentation.modelmanager

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.CloudDownload
import androidx.compose.material.icons.filled.Download
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Memory
import androidx.compose.material.icons.filled.RestartAlt
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import com.biodino.edge.data.network.ModelDownloadManager
import com.biodino.edge.data.locale.AppLanguage
import com.biodino.edge.data.locale.AppStrings
import com.biodino.edge.presentation.theme.AlertAmber
import com.biodino.edge.presentation.theme.AlertCrimson
import com.biodino.edge.presentation.theme.BorderHighlight
import com.biodino.edge.presentation.theme.EmeraldAccent
import com.biodino.edge.presentation.theme.EmeraldNeon
import com.biodino.edge.presentation.theme.ForestDark
import com.biodino.edge.presentation.theme.ForestSurface
import com.biodino.edge.presentation.theme.ForestSurfaceGlass
import com.biodino.edge.presentation.theme.TextPrimary
import com.biodino.edge.presentation.theme.TextSecondary
import com.biodino.edge.presentation.common.SheetCloseButton
import com.biodino.edge.presentation.common.SheetDragHandle
import java.util.Locale

@Composable
fun ModelManagementSheet(
    language: AppLanguage,
    strings: AppStrings,
    isUsingCustomModel: Boolean,
    customModelSizeMb: Float,
    isDownloading: Boolean,
    downloadProgress: Float,
    downloadedBytes: Long,
    totalBytes: Long,
    errorMessage: String?,
    currentUrl: String,
    onStartDownload: (String) -> Unit,
    onRevertDefaultModel: () -> Unit,
    onClose: () -> Unit
) {
    var urlText by remember(currentUrl) { mutableStateOf(currentUrl) }
    val scrollState = rememberScrollState()

    Dialog(onDismissRequest = onClose) {
        CompositionLocalProvider(
            LocalLayoutDirection provides (if (language.isRtl) LayoutDirection.Rtl else LayoutDirection.Ltr)
        ) {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .fillMaxHeight(0.92f)
                    .clip(RoundedCornerShape(28.dp))
                    .background(ForestDark)
                    .border(1.dp, BorderHighlight, RoundedCornerShape(28.dp))
                    .padding(20.dp)
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .verticalScroll(scrollState)
                ) {
                    SheetDragHandle(modifier = Modifier.align(Alignment.CenterHorizontally))

                    Spacer(modifier = Modifier.height(14.dp))

                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Row(
                            modifier = Modifier.weight(1f),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Box(
                                modifier = Modifier
                                    .size(38.dp)
                                    .clip(CircleShape)
                                    .background(if (isUsingCustomModel) Color(0xFF00B0FF).copy(alpha = 0.2f) else EmeraldNeon.copy(alpha = 0.2f)),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(
                                    imageVector = if (isUsingCustomModel) Icons.Default.Memory else Icons.Default.CloudDownload,
                                    contentDescription = null,
                                    tint = if (isUsingCustomModel) Color(0xFF00B0FF) else EmeraldNeon,
                                    modifier = Modifier.size(22.dp)
                                )
                            }
                            Spacer(modifier = Modifier.width(10.dp))
                            Column(modifier = Modifier.padding(end = 8.dp)) {
                                Text(
                                    text = strings.modelManagerTitle,
                                    color = TextPrimary,
                                    fontSize = 15.sp,
                                    fontWeight = FontWeight.Bold
                                )
                                Text(
                                    text = if (isUsingCustomModel) strings.modelActiveCompanionTag else strings.modelActiveDefaultTag,
                                    color = if (isUsingCustomModel) Color(0xFF00B0FF) else EmeraldNeon,
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Medium
                                )
                            }
                        }

                        SheetCloseButton(onClick = onClose)
                    }

                    Spacer(modifier = Modifier.height(16.dp))

                    // Current Active Model Info Card
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        shape = RoundedCornerShape(16.dp),
                        colors = CardDefaults.cardColors(containerColor = ForestSurface),
                        border = CardDefaults.outlinedCardBorder().copy(
                            brush = androidx.compose.ui.graphics.SolidColor(
                                if (isUsingCustomModel) Color(0xFF00B0FF).copy(alpha = 0.5f) else BorderHighlight
                            )
                        )
                    ) {
                        Column(modifier = Modifier.padding(14.dp)) {
                            Text(
                                text = if (isUsingCustomModel) "⚡ BioDINO Companion (Tier-2)" else "🌿 BioDINO Fast Path (Tier-1)",
                                color = TextPrimary,
                                fontSize = 13.sp,
                                fontWeight = FontWeight.Bold
                            )

                            Spacer(modifier = Modifier.height(4.dp))

                            Box(
                                modifier = Modifier
                                    .clip(RoundedCornerShape(8.dp))
                                    .background(
                                        if (isUsingCustomModel) Color(0xFF00B0FF).copy(alpha = 0.2f) else EmeraldNeon.copy(alpha = 0.2f)
                                    )
                                    .padding(horizontal = 8.dp, vertical = 2.dp)
                            ) {
                                Text(
                                    text = if (isUsingCustomModel) {
                                        String.format(Locale.US, "~%.1f MB", customModelSizeMb)
                                    } else {
                                        "~22.0 MB"
                                    },
                                    color = if (isUsingCustomModel) Color(0xFF00B0FF) else EmeraldNeon,
                                    fontSize = 10.sp,
                                    fontWeight = FontWeight.Bold
                                )
                            }

                            Spacer(modifier = Modifier.height(6.dp))

                            Text(
                                text = if (isUsingCustomModel) strings.modelCompanionDesc else strings.modelDefaultDesc,
                                color = TextSecondary,
                                fontSize = 11.sp,
                                lineHeight = 16.sp
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(10.dp))

                    ModelDownloadCard(
                        urlText = urlText,
                        onUrlChange = { urlText = it },
                        isDownloading = isDownloading,
                        downloadProgress = downloadProgress,
                        downloadedBytes = downloadedBytes,
                        totalBytes = totalBytes,
                        errorMessage = errorMessage,
                        isUsingCustomModel = isUsingCustomModel,
                        onStartDownload = onStartDownload,
                        onRevertDefaultModel = onRevertDefaultModel,
                        strings = strings
                    )

                    Spacer(modifier = Modifier.height(16.dp))

                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(14.dp))
                            .background(ForestSurfaceGlass)
                            .border(1.dp, BorderHighlight, RoundedCornerShape(14.dp))
                            .padding(12.dp)
                    ) {
                        Row(verticalAlignment = Alignment.Top) {
                            Icon(
                                imageVector = Icons.Default.Info,
                                contentDescription = null,
                                tint = EmeraldAccent,
                                modifier = Modifier
                                    .size(18.dp)
                                    .padding(top = 2.dp)
                            )
                            Spacer(modifier = Modifier.width(10.dp))
                            Text(
                                text = strings.modelDownloadNote,
                                color = TextSecondary,
                                fontSize = 11.sp,
                                lineHeight = 16.sp
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(16.dp))
                }
            }
        }
    }
}
