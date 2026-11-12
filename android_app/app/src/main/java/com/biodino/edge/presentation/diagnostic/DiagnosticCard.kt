package com.biodino.edge.presentation.diagnostic

import androidx.compose.animation.*
import androidx.compose.animation.core.tween
import androidx.compose.foundation.*
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
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
    val maxCardHeight = configuration.screenHeightDp.dp * 0.65f
    val scrollState = rememberScrollState()

    CompositionLocalProvider(
        LocalLayoutDirection provides (if (language.isRtl) LayoutDirection.Rtl else LayoutDirection.Ltr)
    ) {
        Box(
            modifier = modifier
                .fillMaxWidth()
                .heightIn(max = maxCardHeight)
                .clip(RoundedCornerShape(topStart = 32.dp, topEnd = 32.dp))
                .background(ForestDark)
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

                val isUncertain = latestDiagnosis != null &&
                    !effectiveDark &&
                    !effectiveNonLeaf &&
                    (if (isGalleryMode) latestDiagnosis.confidence < 0.22f else smoothedConfidence < 0.20f)

                val isIdle = if (isGalleryMode) {
                    latestDiagnosis == null
                } else {
                    latestDiagnosis == null || (smoothedConfidence < 0.15f && !isUncertain)
                }

                if (effectiveDark || effectiveNonLeaf || isUncertain || isIdle) {
                    DiagnosticGuidanceState(
                        isDark = effectiveDark,
                        isNonLeaf = effectiveNonLeaf,
                        isUncertain = isUncertain,
                        isIdle = isIdle,
                        isGalleryMode = isGalleryMode,
                        strings = strings
                    )
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

                    // Header Row: Plant Icon + Localized Common Name + Status Badge
                    DiagnosticHeader(
                        disease = disease,
                        themeStatusColor = themeStatusColor,
                        isConfident = isConfident,
                        language = language,
                        strings = strings
                    )

                    Spacer(modifier = Modifier.height(12.dp))

                    // Confidence Gauge Bar
                    DiagnosticConfidenceBar(
                        displayConfidence = displayConfidence,
                        isConfident = isConfident,
                        isGalleryMode = isGalleryMode,
                        themeStatusColor = themeStatusColor,
                        strings = strings
                    )

                    Spacer(modifier = Modifier.height(12.dp))

                    // Actionable Treatment Protocol Card
                    TreatmentProtocolCard(
                        disease = disease,
                        language = language,
                        strings = strings
                    )

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

                    // Expanded details
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

                            // Symptoms
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

                            // Hardware & latency info
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                modifier = Modifier.padding(vertical = 2.dp)
                            ) {
                                Icon(
                                    Icons.Default.Bolt,
                                    contentDescription = null,
                                    tint = if (isHardwareAccelerated) EmeraldNeon else AlertAmber,
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
                                    color = if (isHardwareAccelerated) EmeraldNeon else TextSecondary,
                                    fontSize = 11.sp
                                )
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(14.dp))

                    // Bottom Action Buttons
                    DiagnosticActionsRow(
                        disease = disease,
                        smoothedConfidence = smoothedConfidence,
                        language = language,
                        strings = strings,
                        onSpeakDiagnosis = onSpeakDiagnosis,
                        onOpenCalculator = onOpenCalculator,
                        onOpenCareGuide = onOpenCareGuide
                    )
                }
            }
        }
    }
}
