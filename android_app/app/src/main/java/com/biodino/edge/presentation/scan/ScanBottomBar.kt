package com.biodino.edge.presentation.scan

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.VideocamOff
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.biodino.edge.data.locale.AppLanguage
import com.biodino.edge.data.locale.AppStrings
import com.biodino.edge.domain.model.DiagnosisResult
import com.biodino.edge.presentation.diagnostic.DiagnosticCard
import com.biodino.edge.presentation.theme.BorderHighlight
import com.biodino.edge.presentation.theme.EmeraldNeon
import com.biodino.edge.presentation.theme.ForestSurfaceGlass
import com.biodino.edge.presentation.theme.TextSecondary

@Composable
fun ScanBottomBar(
    language: AppLanguage,
    strings: AppStrings,
    isFarsi: Boolean,
    isCameraActive: Boolean,
    isGalleryMode: Boolean,
    isUsingCustomModel: Boolean,
    isEcoMode: Boolean,
    isTooDark: Boolean,
    isNonLeaf: Boolean,
    latestDiagnosis: DiagnosisResult?,
    smoothedConfidence: Float,
    averageLatencyMs: Float,
    isHardwareAccelerated: Boolean,
    onToggleCameraActive: (Boolean) -> Unit,
    onClearGalleryImage: () -> Unit,
    onLaunchGallery: () -> Unit,
    onOpenAtlas: () -> Unit,
    onOpenCalculator: () -> Unit,
    onOpenHistory: () -> Unit,
    onOpenEnrollment: () -> Unit,
    onOpenModelManager: () -> Unit,
    onToggleEcoMode: () -> Unit,
    onSpeakDiagnosis: () -> Unit,
    onOpenCareGuide: () -> Unit,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
            .fillMaxWidth()
            .clickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null
            ) { /* Consume clicks so taps on dock/cards do NOT wake camera */ }
    ) {
        // Camera standby toggle
        if (!isGalleryMode && isCameraActive) {
            Box(
                modifier = Modifier
                    .align(Alignment.CenterHorizontally)
                    .padding(bottom = 8.dp)
                    .clip(RoundedCornerShape(20.dp))
                    .background(ForestSurfaceGlass)
                    .border(1.dp, BorderHighlight, RoundedCornerShape(20.dp))
                    .clickable { onToggleCameraActive(false) }
                    .padding(horizontal = 14.dp, vertical = 7.dp)
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Box(
                        modifier = Modifier
                            .size(8.dp)
                            .clip(CircleShape)
                            .background(EmeraldNeon)
                    )
                    Spacer(modifier = Modifier.width(7.dp))
                    Icon(
                        imageVector = Icons.Default.VideocamOff,
                        contentDescription = null,
                        tint = TextSecondary,
                        modifier = Modifier.size(16.dp)
                    )
                    Spacer(modifier = Modifier.width(6.dp))
                    Text(
                        text = strings.btnTurnOffCamera,
                        color = TextSecondary,
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            }
        }

        // Action dock
        ScanFloatingDock(
            strings = strings,
            isGalleryMode = isGalleryMode,
            isUsingCustomModel = isUsingCustomModel,
            isEcoMode = isEcoMode,
            onClearGalleryImage = onClearGalleryImage,
            onLaunchGallery = onLaunchGallery,
            onOpenAtlas = onOpenAtlas,
            onOpenCalculator = onOpenCalculator,
            onOpenHistory = onOpenHistory,
            onOpenEnrollment = onOpenEnrollment,
            onOpenModelManager = onOpenModelManager,
            onToggleEcoMode = onToggleEcoMode,
            modifier = Modifier.align(Alignment.CenterHorizontally)
        )

        // Diagnostic card / standby guidance
        if (!isCameraActive && !isGalleryMode) {
            CameraStandbyGuidanceCard(
                language = language,
                strings = strings
            )
        } else {
            DiagnosticCard(
                language = language,
                isFarsi = isFarsi,
                isGalleryMode = isGalleryMode,
                isTooDark = isTooDark,
                isNonLeaf = isNonLeaf,
                latestDiagnosis = latestDiagnosis,
                smoothedConfidence = smoothedConfidence,
                averageLatencyMs = averageLatencyMs,
                isHardwareAccelerated = isHardwareAccelerated,
                onSpeakDiagnosis = onSpeakDiagnosis,
                onOpenCalculator = onOpenCalculator,
                onOpenCareGuide = onOpenCareGuide
            )
        }
    }
}
