package com.biodino.edge.presentation.ui

import android.content.Intent
import androidx.compose.foundation.background
import androidx.compose.foundation.border
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
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bolt
import androidx.compose.material.icons.filled.Eco
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Share
import androidx.compose.material.icons.filled.VolumeUp
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
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
import com.biodino.edge.presentation.theme.EmeraldNeon
import com.biodino.edge.presentation.theme.ForestSurfaceGlass
import com.biodino.edge.presentation.theme.TextPrimary
import com.biodino.edge.presentation.theme.TextSecondary
import java.util.Locale

@Composable
fun DiagnosticCard(
    modifier: Modifier = Modifier,
    latestDiagnosis: DiagnosisResult?,
    smoothedConfidence: Float,
    averageLatencyMs: Float,
    isHardwareAccelerated: Boolean,
    onSpeakDiagnosis: () -> Unit
) {
    val context = LocalContext.current

    Box(
        modifier = modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(topStart = 28.dp, topEnd = 28.dp))
            .background(ForestSurfaceGlass)
            .border(1.dp, BorderHighlight, RoundedCornerShape(topStart = 28.dp, topEnd = 28.dp))
            .padding(horizontal = 20.dp, vertical = 18.dp)
    ) {
        if (latestDiagnosis == null || smoothedConfidence < 0.15f) {
            // Idle / Searching State
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 12.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Icon(
                    imageVector = Icons.Default.Eco,
                    contentDescription = null,
                    tint = EmeraldNeon.copy(alpha = 0.6f),
                    modifier = Modifier.size(36.dp)
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "Center leaf in viewfinder",
                    color = TextPrimary,
                    fontSize = 16.sp,
                    fontWeight = FontWeight.SemiBold
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = "Hold steady 15-20 cm from foliage. Real-time BioDINO DINOv2 5-shot active.",
                    color = TextSecondary,
                    fontSize = 12.sp
                )
            }
        } else {
            val disease = latestDiagnosis.diseaseInfo
            val isConfident = smoothedConfidence >= 0.35f
            val statusColor = if (isConfident) {
                if (disease.isHealthy) EmeraldNeon else AlertAmber
            } else {
                AlertCrimson
            }

            Column(modifier = Modifier.fillMaxWidth()) {
                // Top Header Row: Common Name + Health Tag Pill + Speak/Share Actions
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = disease.commonName,
                            color = TextPrimary,
                            fontSize = 19.sp,
                            fontWeight = FontWeight.Bold,
                            maxLines = 1
                        )
                        Text(
                            text = disease.latinTaxonomy,
                            color = EmeraldAccent,
                            fontSize = 12.sp,
                            fontStyle = FontStyle.Italic
                        )
                    }

                    Row(verticalAlignment = Alignment.CenterVertically) {
                        // Quick Speak Button
                        IconButton(
                            onClick = onSpeakDiagnosis,
                            modifier = Modifier.size(34.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Default.VolumeUp,
                                contentDescription = "Speak Diagnosis",
                                tint = EmeraldNeon,
                                modifier = Modifier.size(20.dp)
                            )
                        }

                        // Quick Share Button
                        IconButton(
                            onClick = {
                                val text = """
                                    BioDINO-Edge Diagnosis Report:
                                    • Disease: ${disease.commonName} (${disease.latinTaxonomy})
                                    • Host Plant: ${disease.hostPlant}
                                    • Confidence: ${String.format(Locale.US, "%.1f%%", smoothedConfidence * 100)}
                                    • Protocol: ${disease.actionableAdvice}
                                """.trimIndent()
                                val sendIntent = Intent().apply {
                                    action = Intent.ACTION_SEND
                                    putExtra(Intent.EXTRA_TEXT, text)
                                    type = "text/plain"
                                }
                                context.startActivity(Intent.createChooser(sendIntent, "Share Foliar Diagnosis"))
                            },
                            modifier = Modifier.size(34.dp)
                        ) {
                            Icon(
                                imageVector = Icons.Default.Share,
                                contentDescription = "Share Diagnosis",
                                tint = TextSecondary,
                                modifier = Modifier.size(18.dp)
                            )
                        }

                        Spacer(modifier = Modifier.width(4.dp))

                        // Status Pill
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(10.dp))
                                .background(statusColor.copy(alpha = 0.2f))
                                .border(1.dp, statusColor, RoundedCornerShape(10.dp))
                                .padding(horizontal = 9.dp, vertical = 4.dp)
                        ) {
                            Text(
                                text = if (disease.isHealthy) "HEALTHY" else "PATHOLOGY",
                                color = statusColor,
                                fontSize = 10.sp,
                                fontWeight = FontWeight.Bold,
                                letterSpacing = 0.5.sp
                            )
                        }
                    }
                }

                Spacer(modifier = Modifier.height(12.dp))

                // Shannon Confidence & Latency Gauge Bar
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = "Shannon Confidence: ",
                            color = TextSecondary,
                            fontSize = 12.sp
                        )
                        Text(
                            text = String.format(Locale.US, "%.1f%%", smoothedConfidence * 100f),
                            color = statusColor,
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }

                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(
                            imageVector = Icons.Default.Bolt,
                            contentDescription = null,
                            tint = EmeraldNeon,
                            modifier = Modifier.size(14.dp)
                        )
                        Spacer(modifier = Modifier.width(2.dp))
                        Text(
                            text = String.format(Locale.US, "%.1f ms (%s)", averageLatencyMs, if (isHardwareAccelerated) "NNAPI" else "CPU"),
                            color = TextSecondary,
                            fontSize = 11.sp
                        )
                    }
                }

                Spacer(modifier = Modifier.height(6.dp))

                LinearProgressIndicator(
                    progress = { smoothedConfidence.coerceIn(0f, 1f) },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(6.dp)
                        .clip(RoundedCornerShape(3.dp)),
                    color = statusColor,
                    trackColor = Color.White.copy(alpha = 0.1f)
                )

                Spacer(modifier = Modifier.height(12.dp))

                // Clinical Symptom Description
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.Top
                ) {
                    Icon(
                        imageVector = Icons.Default.Info,
                        contentDescription = null,
                        tint = TextSecondary,
                        modifier = Modifier
                            .size(16.dp)
                            .padding(top = 2.dp)
                    )
                    Spacer(modifier = Modifier.width(6.dp))
                    Text(
                        text = disease.primarySymptom,
                        color = TextPrimary.copy(alpha = 0.9f),
                        fontSize = 12.sp,
                        lineHeight = 17.sp
                    )
                }

                if (!disease.isHealthy) {
                    Spacer(modifier = Modifier.height(10.dp))
                    // Actionable Agronomy Advice Box
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .clip(RoundedCornerShape(8.dp))
                            .background(ForestSurfaceGlass.copy(alpha = 0.6f))
                            .border(1.dp, AlertAmber.copy(alpha = 0.4f), RoundedCornerShape(8.dp))
                            .padding(horizontal = 10.dp, vertical = 8.dp)
                    ) {
                        Row(verticalAlignment = Alignment.Top) {
                            Icon(
                                imageVector = Icons.Default.Warning,
                                contentDescription = null,
                                tint = AlertAmber,
                                modifier = Modifier
                                    .size(16.dp)
                                    .padding(top = 2.dp)
                            )
                            Spacer(modifier = Modifier.width(6.dp))
                            Text(
                                text = disease.actionableAdvice,
                                color = TextPrimary,
                                fontSize = 11.sp,
                                lineHeight = 16.sp
                            )
                        }
                    }
                }
            }
        }
    }
}
