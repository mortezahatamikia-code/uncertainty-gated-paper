package com.biodino.edge.presentation.ui

import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.biodino.edge.presentation.theme.AlertAmber
import com.biodino.edge.presentation.theme.AlertCrimson
import com.biodino.edge.presentation.theme.EmeraldNeon
import com.biodino.edge.presentation.theme.ForestDark

@Composable
fun ReticleOverlay(
    modifier: Modifier = Modifier,
    isScanningPaused: Boolean,
    isBlurred: Boolean,
    isEcoMode: Boolean,
    smoothedConfidence: Float,
    isConfidentlyLocked: Boolean
) {
    val haptic = LocalHapticFeedback.current

    // Trigger haptic buzz on target lock
    LaunchedEffect(isConfidentlyLocked) {
        if (isConfidentlyLocked) {
            haptic.performHapticFeedback(HapticFeedbackType.LongPress)
        }
    }

    val infiniteTransition = rememberInfiniteTransition(label = "LaserScan")
    val laserYRatio by infiniteTransition.animateFloat(
        initialValue = 0.05f,
        targetValue = 0.95f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = if (isEcoMode) 2400 else 1800, easing = LinearEasing),
            repeatMode = RepeatMode.Reverse
        ),
        label = "LaserY"
    )

    val reticleColor = when {
        isScanningPaused -> Color.Gray
        isBlurred -> AlertAmber
        smoothedConfidence >= 0.50f -> EmeraldNeon
        smoothedConfidence >= 0.35f -> EmeraldNeon.copy(alpha = 0.9f)
        smoothedConfidence >= 0.20f -> AlertAmber
        else -> AlertCrimson.copy(alpha = 0.8f)
    }

    Box(
        modifier = modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        val reticleSizeDp = 260.dp

        Canvas(modifier = Modifier.size(reticleSizeDp)) {
            val width = size.width
            val height = size.height
            val cornerLength = 32.dp.toPx()
            val strokeWidth = 3.5.dp.toPx()

            // 1. Four tactical corners
            // Top-Left
            drawLine(reticleColor, Offset(0f, 0f), Offset(cornerLength, 0f), strokeWidth, StrokeCap.Round)
            drawLine(reticleColor, Offset(0f, 0f), Offset(0f, cornerLength), strokeWidth, StrokeCap.Round)

            // Top-Right
            drawLine(reticleColor, Offset(width, 0f), Offset(width - cornerLength, 0f), strokeWidth, StrokeCap.Round)
            drawLine(reticleColor, Offset(width, 0f), Offset(width, cornerLength), strokeWidth, StrokeCap.Round)

            // Bottom-Left
            drawLine(reticleColor, Offset(0f, height), Offset(cornerLength, height), strokeWidth, StrokeCap.Round)
            drawLine(reticleColor, Offset(0f, height), Offset(0f, height - cornerLength), strokeWidth, StrokeCap.Round)

            // Bottom-Right
            drawLine(reticleColor, Offset(width, height), Offset(width - cornerLength, height), strokeWidth, StrokeCap.Round)
            drawLine(reticleColor, Offset(width, height), Offset(width, height - cornerLength), strokeWidth, StrokeCap.Round)

            // 2. Center crosshair
            val center = Offset(width / 2f, height / 2f)
            val crossSize = 12.dp.toPx()
            drawLine(reticleColor.copy(alpha = 0.4f), Offset(center.x - crossSize, center.y), Offset(center.x + crossSize, center.y), 1.5.dp.toPx())
            drawLine(reticleColor.copy(alpha = 0.4f), Offset(center.x, center.y - crossSize), Offset(center.x, center.y + crossSize), 1.5.dp.toPx())

            // 3. Animated scanning beam if active
            if (!isScanningPaused) {
                val currentLaserY = height * laserYRatio
                drawLine(
                    color = reticleColor.copy(alpha = 0.75f),
                    start = Offset(12.dp.toPx(), currentLaserY),
                    end = Offset(width - 12.dp.toPx(), currentLaserY),
                    strokeWidth = 2.dp.toPx(),
                    cap = StrokeCap.Round
                )
            }
        }

        // Overlay status text above & below reticle
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier
                .align(Alignment.Center)
                .padding(bottom = reticleSizeDp + 36.dp)
        ) {
            Text(
                text = when {
                    isScanningPaused -> "SCANNER PAUSED"
                    isBlurred -> "⚠️ CAMERA BLUR DETECTED"
                    isConfidentlyLocked -> "LEAF TARGET LOCKED"
                    smoothedConfidence >= 0.20f -> "ANALYZING SYMPTOMS..."
                    else -> "CENTER FOLIAGE IN RETICLE"
                },
                color = reticleColor,
                fontSize = 11.sp,
                fontWeight = FontWeight.Bold,
                letterSpacing = 1.2.sp
            )

            if (isEcoMode) {
                Spacer(modifier = Modifier.height(4.dp))
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(6.dp))
                        .background(ForestDark.copy(alpha = 0.7f))
                        .border(1.dp, EmeraldNeon.copy(alpha = 0.4f), RoundedCornerShape(6.dp))
                        .padding(horizontal = 6.dp, vertical = 2.dp)
                ) {
                    Text(
                        text = "ECO MODE (15 FPS)",
                        color = EmeraldNeon,
                        fontSize = 9.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            }
        }
    }
}
