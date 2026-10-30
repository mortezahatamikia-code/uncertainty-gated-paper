package com.biodino.edge.presentation.ui

import android.content.Intent
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.animateContentSize
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.VolumeUp
import androidx.compose.material.icons.filled.Bolt
import androidx.compose.material.icons.filled.Eco
import androidx.compose.material.icons.filled.ExpandLess
import androidx.compose.material.icons.filled.ExpandMore
import androidx.compose.material.icons.filled.Healing
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Science
import androidx.compose.material.icons.filled.Share
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.OutlinedButton
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
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.biodino.edge.data.locale.AppLanguage
import com.biodino.edge.data.locale.I18n
import com.biodino.edge.domain.model.DiagnosisResult
import com.biodino.edge.presentation.theme.AlertAmber
import com.biodino.edge.presentation.theme.AlertCrimson
import com.biodino.edge.presentation.theme.BorderHighlight
import com.biodino.edge.presentation.theme.EmeraldAccent
import com.biodino.edge.presentation.theme.EmeraldNeon
import com.biodino.edge.presentation.theme.ForestDark
import com.biodino.edge.presentation.theme.ForestSurfaceGlass
import com.biodino.edge.presentation.theme.TextPrimary
import com.biodino.edge.presentation.theme.TextSecondary
import java.util.Locale

@Composable
fun DiagnosticCard(
    modifier: Modifier = Modifier,
    isFarsi: Boolean = false,
    language: AppLanguage = if (isFarsi) AppLanguage.PERSIAN else AppLanguage.ENGLISH,
    isGalleryMode: Boolean = false,
    isTooDark: Boolean = false,
    isNonLeaf: Boolean = false,
    latestDiagnosis: DiagnosisResult?,
    smoothedConfidence: Float,
    averageLatencyMs: Float,
    isHardwareAccelerated: Boolean,
    onSpeakDiagnosis: () -> Unit,
    onOpenCalculator: () -> Unit = {},
    onOpenCareGuide: () -> Unit = {}
) {
    val context = LocalContext.current
    val strings = I18n.getStrings(language)
    var isExpanded by remember { mutableStateOf(false) }
    val configuration = LocalConfiguration.current
    val maxCardHeight = configuration.screenHeightDp.dp * 0.50f
    val scrollState = rememberScrollState()

    CompositionLocalProvider(
        LocalLayoutDirection provides (if (language.isRtl) LayoutDirection.Rtl else LayoutDirection.Ltr)
    ) {
        Box(
            modifier = modifier
                .fillMaxWidth()
                .heightIn(max = maxCardHeight)
                .clip(RoundedCornerShape(topStart = 32.dp, topEnd = 32.dp))
                .background(ForestSurfaceGlass)
                .border(
                    1.dp,
                    BorderHighlight,
                    RoundedCornerShape(topStart = 32.dp, topEnd = 32.dp)
                )
                .animateContentSize(animationSpec = tween(300))
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .verticalScroll(scrollState)
                    .padding(horizontal = 20.dp, vertical = 18.dp)
            ) {
                val effectiveDark = isTooDark || (latestDiagnosis?.isTooDark == true)
            val effectiveNonLeaf =
                isNonLeaf || (latestDiagnosis != null && !latestDiagnosis.isFoliage && !effectiveDark)

            if (effectiveDark) {
                // Dark scene / Covered lens guidance
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 12.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        modifier = Modifier
                            .size(48.dp)
                            .clip(CircleShape)
                            .background(AlertAmber.copy(alpha = 0.18f)),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = Icons.Default.Bolt,
                            contentDescription = null,
                            tint = AlertAmber,
                            modifier = Modifier.size(26.dp)
                        )
                    }
                    Spacer(modifier = Modifier.width(14.dp))
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = strings.sceneTooDark,
                            color = AlertAmber,
                            fontSize = 16.sp,
                            fontWeight = FontWeight.SemiBold
                        )
                        Spacer(modifier = Modifier.height(2.dp))
                        Text(
                            text = strings.sceneTooDarkDesc,
                            color = TextSecondary,
                            fontSize = 12.sp
                        )
                    }
                }
            } else if (effectiveNonLeaf) {
                // Non-foliage object guidance
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 12.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Box(
                        modifier = Modifier
                            .size(48.dp)
                            .clip(CircleShape)
                            .background(AlertCrimson.copy(alpha = 0.18f)),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            imageVector = Icons.Default.Info,
                            contentDescription = null,
                            tint = AlertCrimson,
                            modifier = Modifier.size(26.dp)
                        )
                    }
                    Spacer(modifier = Modifier.width(14.dp))
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = strings.objectNonLeaf,
                            color = AlertCrimson,
                            fontSize = 16.sp,
                            fontWeight = FontWeight.SemiBold
                        )
                        Spacer(modifier = Modifier.height(2.dp))
                        Text(
                            text = strings.objectNonLeafDesc,
                            color = TextSecondary,
                            fontSize = 12.sp
                        )
                    }
                }
            } else {
                val isIdle = if (isGalleryMode) {
                    latestDiagnosis == null
                } else {
                    latestDiagnosis == null || smoothedConfidence < 0.15f
                }

                if (isIdle) {
                    // Idle / Seeking Foliage or Processing Gallery Image
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 12.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Box(
                            modifier = Modifier
                                .size(48.dp)
                                .clip(CircleShape)
                                .background(EmeraldNeon.copy(alpha = 0.15f)),
                            contentAlignment = Alignment.Center
                        ) {
                            if (isGalleryMode) {
                                CircularProgressIndicator(
                                    modifier = Modifier.size(26.dp),
                                    color = EmeraldNeon,
                                    strokeWidth = 2.5.dp
                                )
                            } else {
                                Icon(
                                    imageVector = Icons.Default.Eco,
                                    contentDescription = null,
                                    tint = EmeraldNeon,
                                    modifier = Modifier.size(26.dp)
                                )
                            }
                        }
                        Spacer(modifier = Modifier.width(14.dp))
                        Column(modifier = Modifier.weight(1f)) {
                            Text(
                                text = strings.seekingFoliage,
                                color = TextPrimary,
                                fontSize = 16.sp,
                                fontWeight = FontWeight.SemiBold
                            )
                            Spacer(modifier = Modifier.height(2.dp))
                            Text(
                                text = strings.pointCameraHint,
                                color = TextSecondary,
                                fontSize = 12.sp
                            )
                        }
                    }
                } else {
                    // Active Confirmed Diagnosis View
                    val diag = latestDiagnosis!!
                    val disease = diag.diseaseInfo
                    val displayConfidence = if (isGalleryMode) diag.confidence else smoothedConfidence
                    val isConfident = displayConfidence >= 0.35f

                    val themeStatusColor = when {
                        disease.isHealthy -> EmeraldNeon
                        isConfident -> AlertAmber
                        else -> AlertCrimson
                    }

                    val plantEmoji = when {
                        disease.isHealthy -> "🌿"
                        disease.rawKey.startsWith("Apple") -> "🍎"
                        disease.rawKey.startsWith("Grape") -> "🍇"
                        disease.rawKey.startsWith("Potato") -> "🥔"
                        else -> "🌱"
                    }

                    // Header Row: Plant Icon + Localized Common Name + Status Badge (Natural RTL/LTR)
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.weight(1f)
                        ) {
                            Text(
                                text = plantEmoji,
                                fontSize = 26.sp,
                                modifier = Modifier.padding(end = 10.dp)
                            )
                            Column {
                                Text(
                                    text = disease.getLocalizedName(language),
                                    color = TextPrimary,
                                    fontSize = 19.sp,
                                    fontWeight = FontWeight.Bold,
                                    maxLines = 1
                                )
                                Text(
                                    text = disease.getLocalizedHost(language),
                                    color = TextSecondary,
                                    fontSize = 12.sp
                                )
                            }
                        }

                        // Health Status Tag Pill
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(12.dp))
                                .background(themeStatusColor.copy(alpha = 0.18f))
                                .border(
                                    1.dp,
                                    themeStatusColor.copy(alpha = 0.8f),
                                    RoundedCornerShape(12.dp)
                                )
                                .padding(horizontal = 10.dp, vertical = 5.dp)
                        ) {
                            Text(
                                text = when {
                                    disease.isHealthy -> strings.tagHealthy
                                    isConfident -> strings.tagPathology
                                    else -> strings.tagProbable
                                },
                                color = themeStatusColor,
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Bold,
                                letterSpacing = if (language.isRtl) 0.sp else 0.6.sp
                            )
                        }
                    }

                    Spacer(modifier = Modifier.height(12.dp))

                    // Confidence Gauge Bar
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Text(
                            text = when {
                                isConfident -> strings.confidenceHigh
                                isGalleryMode -> strings.confidenceModerate
                                else -> strings.confidenceScanning
                            },
                            color = TextSecondary,
                            fontSize = 12.sp
                        )
                        Text(
                            text = String.format(Locale.US, "%.1f%%", displayConfidence * 100f),
                            color = themeStatusColor,
                            fontSize = 13.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }

                    Spacer(modifier = Modifier.height(6.dp))

                    LinearProgressIndicator(
                        progress = { displayConfidence.coerceIn(0f, 1f) },
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(6.dp)
                            .clip(RoundedCornerShape(3.dp)),
                        color = themeStatusColor,
                        trackColor = Color.White.copy(alpha = 0.12f)
                    )

                    Spacer(modifier = Modifier.height(12.dp))

                    // Prominent Actionable Treatment Protocol Card (Fully Localized!)
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(12.dp))
                            .background(ForestDark.copy(alpha = 0.8f))
                            .border(
                                1.dp,
                                if (disease.isHealthy) EmeraldNeon.copy(alpha = 0.4f) else AlertAmber.copy(alpha = 0.5f),
                                RoundedCornerShape(12.dp)
                            )
                            .padding(horizontal = 12.dp, vertical = 10.dp)
                    ) {
                        Row(verticalAlignment = Alignment.Top) {
                            Icon(
                                imageVector = if (disease.isHealthy) Icons.Default.Eco else Icons.Default.Healing,
                                contentDescription = null,
                                tint = if (disease.isHealthy) EmeraldNeon else AlertAmber,
                                modifier = Modifier
                                    .size(20.dp)
                                    .padding(top = 2.dp)
                            )
                            Spacer(modifier = Modifier.width(10.dp))
                            Column {
                                Text(
                                    text = if (disease.isHealthy) strings.protocolAgronomy else strings.protocolTreatment,
                                    color = if (disease.isHealthy) EmeraldNeon else AlertAmber,
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Bold
                                )
                                Spacer(modifier = Modifier.height(2.dp))
                                Text(
                                    text = disease.getLocalizedAdvice(language),
                                    color = TextPrimary,
                                    fontSize = 13.sp,
                                    lineHeight = 18.sp,
                                    fontWeight = FontWeight.Medium
                                )
                            }
                        }
                    }

                    // Expandable Section Toggle
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(top = 10.dp)
                            .clip(RoundedCornerShape(8.dp))
                            .clickable(
                                interactionSource = remember { MutableInteractionSource() },
                                indication = null
                            ) { isExpanded = !isExpanded }
                            .padding(vertical = 4.dp),
                        horizontalArrangement = Arrangement.Center,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Icon(
                            imageVector = Icons.Default.Science,
                            contentDescription = null,
                            tint = EmeraldAccent,
                            modifier = Modifier.size(14.dp)
                        )
                        Spacer(modifier = Modifier.width(6.dp))
                        Text(
                            text = if (isExpanded) strings.hideScientificDetails else strings.viewScientificDetails,
                            color = EmeraldAccent,
                            fontSize = 12.sp,
                            fontWeight = FontWeight.SemiBold
                        )
                        Icon(
                            imageVector = if (isExpanded) Icons.Default.ExpandLess else Icons.Default.ExpandMore,
                            contentDescription = null,
                            tint = EmeraldAccent,
                            modifier = Modifier.size(18.dp)
                        )
                    }

                    // Progressive Disclosure Details
                    AnimatedVisibility(visible = isExpanded, enter = fadeIn(), exit = fadeOut()) {
                        Column(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(top = 8.dp)
                        ) {
                            // Latin taxonomy
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text(strings.pathogenLabel, color = TextSecondary, fontSize = 12.sp)
                                Text(
                                    disease.latinTaxonomy,
                                    color = TextPrimary,
                                    fontSize = 12.sp,
                                    fontStyle = FontStyle.Italic,
                                    fontWeight = FontWeight.Bold
                                )
                            }

                            Spacer(modifier = Modifier.height(6.dp))

                            // Full symptom description (Fully Localized!)
                            Row(verticalAlignment = Alignment.Top) {
                                Icon(
                                    Icons.Default.Info,
                                    contentDescription = null,
                                    tint = TextSecondary,
                                    modifier = Modifier
                                        .size(14.dp)
                                        .padding(top = 2.dp)
                                )
                                Spacer(modifier = Modifier.width(6.dp))
                                Column {
                                    Text(
                                        text = strings.symptomLabel + disease.getLocalizedSymptom(language),
                                        color = TextSecondary,
                                        fontSize = 11.sp,
                                        lineHeight = 16.sp
                                    )
                                }
                            }

                            Spacer(modifier = Modifier.height(8.dp))

                            // Latency and Hardware Accelerator tag (Fully Localized!)
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(
                                    Icons.Default.Bolt,
                                    contentDescription = null,
                                    tint = EmeraldNeon,
                                    modifier = Modifier.size(14.dp)
                                )
                                Spacer(modifier = Modifier.width(4.dp))
                                Text(
                                    text = String.format(
                                        Locale.US,
                                        strings.inferenceTimeLabel,
                                        averageLatencyMs,
                                        if (isHardwareAccelerated) strings.hardwareNnapi else strings.hardwareCpu
                                    ),
                                    color = TextSecondary,
                                    fontSize = 11.sp
                                )
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(14.dp))

                    // Bottom Action Buttons
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Button(
                            onClick = onSpeakDiagnosis,
                            colors = ButtonDefaults.buttonColors(
                                containerColor = EmeraldNeon,
                                contentColor = ForestDark
                            ),
                            shape = RoundedCornerShape(12.dp),
                            modifier = Modifier
                                .weight(1.2f)
                                .height(44.dp)
                        ) {
                            Icon(
                                imageVector = Icons.AutoMirrored.Filled.VolumeUp,
                                contentDescription = "Speak",
                                modifier = Modifier.size(18.dp)
                            )
                            Spacer(modifier = Modifier.width(6.dp))
                            Text(
                                text = strings.btnSpeak,
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }

                        if (!disease.isHealthy) {
                            Button(
                                onClick = onOpenCalculator,
                                colors = ButtonDefaults.buttonColors(
                                    containerColor = AlertAmber,
                                    contentColor = ForestDark
                                ),
                                shape = RoundedCornerShape(12.dp),
                                modifier = Modifier
                                    .weight(1.2f)
                                    .height(44.dp)
                            ) {
                                Icon(
                                    imageVector = Icons.Default.Science,
                                    contentDescription = null,
                                    modifier = Modifier.size(16.dp)
                                )
                                Spacer(modifier = Modifier.width(4.dp))
                                Text(
                                    text = strings.btnDosage,
                                    fontSize = 12.sp,
                                    fontWeight = FontWeight.Bold
                                )
                            }
                        } else {
                            Button(
                                onClick = onOpenCareGuide,
                                colors = ButtonDefaults.buttonColors(
                                    containerColor = EmeraldNeon,
                                    contentColor = ForestDark
                                ),
                                shape = RoundedCornerShape(12.dp),
                                modifier = Modifier
                                    .weight(1.2f)
                                    .height(44.dp)
                            ) {
                                Icon(
                                    imageVector = Icons.Default.Eco,
                                    contentDescription = null,
                                    modifier = Modifier.size(16.dp)
                                )
                                Spacer(modifier = Modifier.width(4.dp))
                                Text(
                                    text = strings.btnCareGuide,
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Bold
                                )
                            }
                        }

                        OutlinedButton(
                            onClick = {
                                val reportText = buildString {
                                    appendLine(strings.reportTitle)
                                    appendLine(String.format(strings.reportCondition, disease.getLocalizedName(language), disease.latinTaxonomy))
                                    appendLine(String.format(strings.reportHost, disease.getLocalizedHost(language)))
                                    appendLine(String.format(strings.reportCertainty, String.format(Locale.US, "%.1f%%", smoothedConfidence * 100)))
                                    appendLine(String.format(strings.reportProtocol, disease.getLocalizedAdvice(language)))
                                }
                                val sendIntent = Intent().apply {
                                    action = Intent.ACTION_SEND
                                    putExtra(Intent.EXTRA_TEXT, reportText)
                                    type = "text/plain"
                                }
                                val shareIntent = Intent.createChooser(sendIntent, strings.btnShareReport)
                                context.startActivity(shareIntent)
                            },
                            shape = RoundedCornerShape(12.dp),
                            modifier = Modifier.size(44.dp),
                            contentPadding = PaddingValues(0.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Default.Share,
                                contentDescription = "Share",
                                tint = TextPrimary,
                                modifier = Modifier.size(18.dp)
                            )
                        }
                    }
                }
            }
        }
    }
}
}
