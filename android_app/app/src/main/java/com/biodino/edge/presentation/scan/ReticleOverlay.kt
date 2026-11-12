package com.biodino.edge.presentation.scan

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
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.EnergySavingsLeaf
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.hapticfeedback.HapticFeedbackType
import androidx.compose.ui.platform.LocalHapticFeedback
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.biodino.edge.data.locale.AppLanguage
import com.biodino.edge.data.locale.I18n
import com.biodino.edge.data.locale.LocalAppLanguage
import com.biodino.edge.data.locale.LocalAppStrings
import com.biodino.edge.presentation.theme.AlertAmber
import com.biodino.edge.presentation.theme.AlertCrimson
import com.biodino.edge.presentation.theme.EmeraldNeon
import com.biodino.edge.presentation.theme.ForestDark
import com.biodino.edge.presentation.theme.ForestSurfaceGlass
import com.biodino.edge.presentation.theme.TextPrimary

@Composable
fun ReticleOverlay(
    modifier: Modifier = Modifier,
    language: AppLanguage = LocalAppLanguage.current,
    isFarsi: Boolean = language == AppLanguage.PERSIAN,
    isScanningPaused: Boolean,
    isBlurred: Boolean,
    isEcoMode: Boolean,
    smoothedConfidence: Float,
    isConfidentlyLocked: Boolean
) {
    val haptic = LocalHapticFeedback.current
    val strings = LocalAppStrings.current

    // Haptic pulse on confident lock
    LaunchedEffect(isConfidentlyLocked) {
        if (isConfidentlyLocked) {
            haptic.performHapticFeedback(HapticFeedbackType.LongPress)
        }
    }

    val infiniteTransition = rememberInfiniteTransition(label = "ReticleLaserScan")
    val laserYRatio by infiniteTransition.animateFloat(
        initialValue = 0.08f,
        targetValue = 0.92f,
        animationSpec = infiniteRepeatable(
            animation = tween(durationMillis = if (isEcoMode) 2200 else 1600, easing = LinearEasing),
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
        else -> AlertCrimson.copy(alpha = 0.75f)
    }

    Box(
        modifier = modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        val reticleSizeDp = 270.dp

        Canvas(modifier = Modifier.size(reticleSizeDp)) {
            val width = size.width
            val height = size.height
            val cornerRadius = 32.dp.toPx()
            val strokeWidth = 3.dp.toPx()

            // Outer frame
            drawRoundRect(
                color = reticleColor.copy(alpha = 0.3f),
                size = Size(width, height),
                cornerRadius = CornerRadius(cornerRadius, cornerRadius),
                style = Stroke(width = 1.5.dp.toPx())
            )

            // Corner brackets
            val arcLength = 40.dp.toPx()
            drawLine(reticleColor, Offset(0f, cornerRadius), Offset(0f, cornerRadius + arcLength), strokeWidth, StrokeCap.Round)
            drawLine(reticleColor, Offset(cornerRadius, 0f), Offset(cornerRadius + arcLength, 0f), strokeWidth, StrokeCap.Round)

            drawLine(reticleColor, Offset(width, cornerRadius), Offset(width, cornerRadius + arcLength), strokeWidth, StrokeCap.Round)
            drawLine(reticleColor, Offset(width - cornerRadius, 0f), Offset(width - cornerRadius - arcLength, 0f), strokeWidth, StrokeCap.Round)

            drawLine(reticleColor, Offset(0f, height - cornerRadius), Offset(0f, height - cornerRadius - arcLength), strokeWidth, StrokeCap.Round)
            drawLine(reticleColor, Offset(cornerRadius, height), Offset(cornerRadius + arcLength, height), strokeWidth, StrokeCap.Round)

            drawLine(reticleColor, Offset(width, height - cornerRadius), Offset(width, height - cornerRadius - arcLength), strokeWidth, StrokeCap.Round)
            drawLine(reticleColor, Offset(width - cornerRadius, height), Offset(width - cornerRadius - arcLength, height), strokeWidth, StrokeCap.Round)

            // Center ring & crosshair
            val center = Offset(width / 2f, height / 2f)
            val ringRadius = 24.dp.toPx()

            drawCircle(
                color = reticleColor.copy(alpha = 0.2f),
                radius = ringRadius,
                center = center,
                style = Stroke(width = 2.dp.toPx())
            )

            // Progress sweep
            val sweepAngle = (smoothedConfidence.coerceIn(0f, 1f) * 360f)
            if (sweepAngle > 0f) {
                drawArc(
                    color = reticleColor,
                    startAngle = -90f,
                    sweepAngle = sweepAngle,
                    useCenter = false,
                    topLeft = Offset(center.x - ringRadius, center.y - ringRadius),
                    size = Size(ringRadius * 2, ringRadius * 2),
                    style = Stroke(width = 3.5.dp.toPx(), cap = StrokeCap.Round)
                )
            }

            drawCircle(
                color = reticleColor,
                radius = 3.dp.toPx(),
                center = center
            )

            // Scanning line
            if (!isScanningPaused) {
                val currentLaserY = height * laserYRatio
                drawLine(
                    color = reticleColor.copy(alpha = 0.8f),
                    start = Offset(24.dp.toPx(), currentLaserY),
                    end = Offset(width - 24.dp.toPx(), currentLaserY),
                    strokeWidth = 2.dp.toPx(),
                    cap = StrokeCap.Round
                )
            }
        }

        // Status pill
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier
                .align(Alignment.Center)
                .padding(bottom = reticleSizeDp + 36.dp)
        ) {
            Box(
                modifier = Modifier
                    .clip(RoundedCornerShape(16.dp))
                    .background(ForestSurfaceGlass)
                    .border(1.dp, reticleColor.copy(alpha = 0.5f), RoundedCornerShape(16.dp))
                    .padding(horizontal = 14.dp, vertical = 6.dp)
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Box(
                        modifier = Modifier
                            .size(7.dp)
                            .clip(CircleShape)
                            .background(reticleColor)
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = when {
                            isScanningPaused -> strings.reticlePaused
                            isBlurred -> strings.reticleSteadyBlur
                            isConfidentlyLocked -> "${strings.reticleLocked} (${(smoothedConfidence * 100).toInt()}%)"
                            smoothedConfidence >= 0.20f -> strings.reticleAnalyzing
                            else -> strings.reticleAlignLeaf
                        },
                        color = TextPrimary,
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold,
                        letterSpacing = if (language.isRtl) 0.sp else 0.8.sp
                    )
                }
            }

            if (isEcoMode) {
                Spacer(modifier = Modifier.height(6.dp))
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier
                        .clip(RoundedCornerShape(10.dp))
                        .background(ForestDark.copy(alpha = 0.7f))
                        .padding(horizontal = 8.dp, vertical = 2.dp)
                ) {
                    Icon(
                        imageVector = Icons.Default.EnergySavingsLeaf,
                        contentDescription = null,
                        tint = EmeraldNeon,
                        modifier = Modifier.size(11.dp)
                    )
                    Spacer(modifier = Modifier.width(4.dp))
                    Text(
                        text = strings.reticleEco15Fps,
                        color = EmeraldNeon,
                        fontSize = 9.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            }
        }
    }
}
