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
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
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
import androidx.compose.material3.Icon
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.biodino.edge.domain.model.DiagnosisResult
import com.biodino.edge.presentation.theme.AlertAmber
import com.biodino.edge.presentation.theme.AlertCrimson
import com.biodino.edge.presentation.theme.BorderHighlight
import com.biodino.edge.presentation.theme.EmeraldAccent
import androidx.compose.material3.CircularProgressIndicator
import com.biodino.edge.presentation.theme.EmeraldNeon
import com.biodino.edge.presentation.theme.ForestDark
import com.biodino.edge.presentation.theme.ForestSurface
import com.biodino.edge.presentation.theme.ForestSurfaceGlass
import com.biodino.edge.presentation.theme.TextPrimary
import com.biodino.edge.presentation.theme.TextSecondary
import java.util.Locale

private fun getLocalizedDiseaseName(rawKey: String, commonName: String, isFarsi: Boolean): String {
    if (!isFarsi) return commonName
    return when {
        rawKey.contains("Apple___Apple_scab", ignoreCase = true) -> "اسکب سیب (لکه سیاه)"
        rawKey.contains("Apple___Black_rot", ignoreCase = true) -> "پوسیدگی سیاه سیب (چشم‌قورباغه‌ای)"
        rawKey.contains("Apple___Cedar_apple_rust", ignoreCase = true) -> "زنگ سیب و سرو کوهی"
        rawKey.contains("Apple___healthy", ignoreCase = true) -> "برگ سالم سیب"
        rawKey.contains("Grape___Black_rot", ignoreCase = true) -> "پوسیدگی سیاه انگور"
        rawKey.contains("Grape___Esca", ignoreCase = true) -> "اسکا انگور (سرخک سیاه / راه‌راه ببری)"
        rawKey.contains("Grape___Leaf_blight", ignoreCase = true) -> "سوختگی برگ انگور (بلایت)"
        rawKey.contains("Grape___healthy", ignoreCase = true) -> "برگ سالم مو (انگور)"
        else -> commonName
    }
}

private fun getLocalizedHostPlant(hostPlant: String, isFarsi: Boolean): String {
    if (!isFarsi) return hostPlant
    return when {
        hostPlant.contains("Apple", ignoreCase = true) -> "درخت سیب (Malus domestica)"
        hostPlant.contains("Grape", ignoreCase = true) -> "مو / درخت انگور (Vitis vinifera)"
        else -> hostPlant
    }
}

@Composable
fun DiagnosticCard(
    modifier: Modifier = Modifier,
    isFarsi: Boolean = false,
    isGalleryMode: Boolean = false,
    latestDiagnosis: DiagnosisResult?,
    smoothedConfidence: Float,
    averageLatencyMs: Float,
    isHardwareAccelerated: Boolean,
    onSpeakDiagnosis: () -> Unit,
    onOpenCalculator: () -> Unit = {}
) {
    val context = LocalContext.current
    var isExpanded by remember { mutableStateOf(false) }

    Box(
        modifier = modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(topStart = 32.dp, topEnd = 32.dp))
            .background(ForestSurfaceGlass)
            .border(1.dp, BorderHighlight, RoundedCornerShape(topStart = 32.dp, topEnd = 32.dp))
            .animateContentSize(animationSpec = tween(300))
            .padding(horizontal = 20.dp, vertical = 16.dp)
    ) {
        val isIdle = if (isGalleryMode) {
            latestDiagnosis == null
        } else {
            latestDiagnosis == null || (smoothedConfidence < 0.15f && latestDiagnosis.probability < 0.30f)
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
                        text = if (isGalleryMode) {
                            if (isFarsi) "در حال پردازش تصویر با هوش مصنوعی..." else "Analyzing imported leaf with BioDINO..."
                        } else {
                            if (isFarsi) "برگ را درون کادر تنظیم کنید" else "Center leaf inside reticle"
                        },
                        color = TextPrimary,
                        fontSize = 16.sp,
                        fontWeight = FontWeight.SemiBold
                    )
                    Spacer(modifier = Modifier.height(2.dp))
                    Text(
                        text = if (isGalleryMode) {
                            if (isFarsi) "استخراج ویژگی‌های بصری DINOv2 و تطبیق پاتوژن..." else "Extracting 384 DINOv2 visual features & pathology match..."
                        } else {
                            if (isFarsi) "گوشی را در فاصله ۱۵-۲۰ سانتی‌متری برگ نگه دارید." else "Hold phone 15-20 cm from foliage. AI analysis is live."
                        },
                        color = TextSecondary,
                        fontSize = 12.sp
                    )
                }
            }
        } else {
            val diag = latestDiagnosis!!
            val disease = diag.diseaseInfo
            val isConfident = smoothedConfidence >= 0.35f || diag.probability >= 0.40f
            val displayConfidence = maxOf(smoothedConfidence, diag.probability)
            val plantIcon = when {
                disease.isHealthy -> "🌿"
                disease.rawKey.startsWith("Apple") -> "🍎"
                disease.rawKey.startsWith("Grape") -> "🍇"
                else -> "🌱"
            }

            val themeStatusColor = when {
                disease.isHealthy -> EmeraldNeon
                isConfident -> AlertAmber
                else -> AlertCrimson
            }

            Column(modifier = Modifier.fillMaxWidth()) {
                // Drag / Expand Handle
                Box(
                    modifier = Modifier
                        .align(Alignment.CenterHorizontally)
                        .width(36.dp)
                        .height(4.dp)
                        .clip(RoundedCornerShape(2.dp))
                        .background(TextSecondary.copy(alpha = 0.4f))
                )

                Spacer(modifier = Modifier.height(12.dp))

                // Primary Diagnosis Header (Glanceable in 1 second)
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
                            text = plantIcon,
                            fontSize = 26.sp,
                            modifier = Modifier.padding(end = 10.dp)
                        )
                        Column {
                            Text(
                                text = getLocalizedDiseaseName(disease.rawKey, disease.commonName, isFarsi),
                                color = TextPrimary,
                                fontSize = 19.sp,
                                fontWeight = FontWeight.Bold,
                                maxLines = 1
                            )
                            Text(
                                text = getLocalizedHostPlant(disease.hostPlant, isFarsi),
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
                            .border(1.dp, themeStatusColor.copy(alpha = 0.8f), RoundedCornerShape(12.dp))
                            .padding(horizontal = 10.dp, vertical = 5.dp)
                    ) {
                        Text(
                            text = if (isFarsi) {
                                if (disease.isHealthy) "سالم 🌿" else if (isConfident) "بیماری قطعی ⚠️" else "تخمین احتمالی 🔍"
                            } else {
                                if (disease.isHealthy) "HEALTHY" else if (isConfident) "PATHOLOGY" else "PROBABLE"
                            },
                            color = themeStatusColor,
                            fontSize = 11.sp,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 0.6.sp
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
                        text = if (isFarsi) {
                            if (isConfident) "ضریب اطمینان مدل: بالا" else if (isGalleryMode) "ضریب اطمینان: متوسط / تخمینی" else "ضریب اطمینان: در حال اسکن..."
                        } else {
                            if (isConfident) "Confidence: High" else if (isGalleryMode) "Confidence: Moderate" else "Confidence: Scanning..."
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

                // Prominent Actionable Treatment Protocol Card (The #1 thing the farmer cares about)
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(12.dp))
                        .background(ForestDark.copy(alpha = 0.8f))
                        .border(1.dp, if (disease.isHealthy) EmeraldNeon.copy(alpha = 0.4f) else AlertAmber.copy(alpha = 0.5f), RoundedCornerShape(12.dp))
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
                                text = if (isFarsi) {
                                    if (disease.isHealthy) "وضعیت زراعی و بهداشت مزرعه" else "پروتکل اقدام فوری درمان زراعی"
                                } else {
                                    if (disease.isHealthy) "Agronomy Protocol" else "Immediate Treatment Protocol"
                                },
                                color = if (disease.isHealthy) EmeraldNeon else AlertAmber,
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Bold
                            )
                            Spacer(modifier = Modifier.height(2.dp))
                            Text(
                                text = disease.actionableAdvice,
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
                        text = if (isFarsi) {
                            if (isExpanded) "بستن تحلیل آزمایشگاهی" else "مشاهده جزییات علمی، علائم و پاتوژن"
                        } else {
                            if (isExpanded) "Hide Lab Analysis" else "View Scientific Details & Symptoms"
                        },
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
                AnimatedVisibility(
                    visible = isExpanded,
                    enter = fadeIn(),
                    exit = fadeOut()
                ) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(top = 8.dp)
                    ) {
                        // Latin taxonomy
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text("Pathogen: ", color = TextSecondary, fontSize = 12.sp)
                            Text(
                                disease.latinTaxonomy,
                                color = TextPrimary,
                                fontSize = 12.sp,
                                fontStyle = FontStyle.Italic,
                                fontWeight = FontWeight.Bold
                            )
                        }

                        Spacer(modifier = Modifier.height(6.dp))

                        // Full symptom description
                        Row(verticalAlignment = Alignment.Top) {
                            Icon(
                                Icons.Default.Info,
                                contentDescription = null,
                                tint = TextSecondary,
                                modifier = Modifier.size(14.dp).padding(top = 2.dp)
                            )
                            Spacer(modifier = Modifier.width(6.dp))
                            Text(
                                disease.primarySymptom,
                                color = TextSecondary,
                                fontSize = 11.sp,
                                lineHeight = 16.sp
                            )
                        }

                        Spacer(modifier = Modifier.height(8.dp))

                        // Latency and NNAPI tag
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                Icons.Default.Bolt,
                                contentDescription = null,
                                tint = EmeraldNeon,
                                modifier = Modifier.size(14.dp)
                            )
                            Spacer(modifier = Modifier.width(4.dp))
                            Text(
                                text = String.format(Locale.US, "Inference: %.1f ms • Hardware: %s", averageLatencyMs, if (isHardwareAccelerated) "NNAPI INT8" else "Multi-Core CPU"),
                                color = TextSecondary,
                                fontSize = 11.sp
                            )
                        }
                    }
                }

                Spacer(modifier = Modifier.height(14.dp))

                // Bottom Action Buttons (Large, high-contrast, thumb-friendly)
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Button(
                        onClick = onSpeakDiagnosis,
                        colors = ButtonDefaults.buttonColors(
                            containerColor = EmeraldNeon,
                            contentColor = ForestDark
                        ),
                        shape = RoundedCornerShape(12.dp),
                        modifier = Modifier
                            .weight(1f)
                            .height(44.dp)
                    ) {
                        Icon(
                            imageVector = Icons.AutoMirrored.Filled.VolumeUp,
                            contentDescription = "Speak",
                            modifier = Modifier.size(18.dp)
                        )
                        Spacer(modifier = Modifier.width(6.dp))
                        Text(
                            text = if (isFarsi) "پخش صوتی" else "Listen",
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
                                .weight(1f)
                                .height(44.dp)
                        ) {
                            Text(
                                text = if (isFarsi) "محاسبه دوز" else "Dosage",
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }

                    OutlinedButton(
                        onClick = {
                            val text = """
                                🌿 BioDINO-Edge Field Diagnosis Report:
                                • Condition: ${disease.commonName} (${disease.latinTaxonomy})
                                • Host Plant: ${disease.hostPlant}
                                • Certainty: ${String.format(Locale.US, "%.1f%%", smoothedConfidence * 100)}
                                • Protocol: ${disease.actionableAdvice}
                            """.trimIndent()
                            val sendIntent = Intent().apply {
                                action = Intent.ACTION_SEND
                                putExtra(Intent.EXTRA_TEXT, text)
                                type = "text/plain"
                            }
                            context.startActivity(Intent.createChooser(sendIntent, "Share Foliar Diagnosis"))
                        },
                        shape = RoundedCornerShape(12.dp),
                        modifier = Modifier
                            .weight(1f)
                            .height(44.dp)
                            .border(1.dp, BorderHighlight, RoundedCornerShape(12.dp))
                    ) {
                        Icon(
                            imageVector = Icons.Default.Share,
                            contentDescription = "Share",
                            tint = TextPrimary,
                            modifier = Modifier.size(16.dp)
                        )
                        Spacer(modifier = Modifier.width(4.dp))
                        Text(
                            text = if (isFarsi) "ارسال" else "Share",
                            color = TextPrimary,
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }
        }
    }
}
