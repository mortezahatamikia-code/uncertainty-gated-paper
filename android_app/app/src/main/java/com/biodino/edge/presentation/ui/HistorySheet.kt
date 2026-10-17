package com.biodino.edge.presentation.ui

import android.content.Intent
import androidx.compose.foundation.background
import androidx.compose.foundation.border
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
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.DeleteSweep
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.Share
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import com.biodino.edge.domain.model.ScanHistoryItem
import com.biodino.edge.presentation.theme.AlertAmber
import com.biodino.edge.presentation.theme.BorderHighlight
import com.biodino.edge.presentation.theme.EmeraldAccent
import com.biodino.edge.presentation.theme.EmeraldNeon
import com.biodino.edge.presentation.theme.ForestDark
import com.biodino.edge.presentation.theme.ForestSurface
import com.biodino.edge.presentation.theme.TextPrimary
import com.biodino.edge.presentation.theme.TextSecondary
import java.util.Locale

@Composable
fun HistorySheet(
    historyItems: List<ScanHistoryItem>,
    onClearHistory: () -> Unit,
    onDismiss: () -> Unit
) {
    val context = LocalContext.current
    val healthyCount = historyItems.count { it.isHealthy }
    val pathologyCount = historyItems.size - healthyCount

    Dialog(onDismissRequest = onDismiss) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .fillMaxHeight(0.90f)
                .clip(RoundedCornerShape(28.dp))
                .background(ForestDark)
                .border(1.dp, BorderHighlight, RoundedCornerShape(28.dp))
                .padding(20.dp)
        ) {
            Column(modifier = Modifier.fillMaxWidth()) {
                // Drag Handle
                Box(
                    modifier = Modifier
                        .align(Alignment.CenterHorizontally)
                        .width(36.dp)
                        .height(4.dp)
                        .clip(RoundedCornerShape(2.dp))
                        .background(TextSecondary.copy(alpha = 0.4f))
                )

                Spacer(modifier = Modifier.height(14.dp))

                // Header
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(36.dp)
                                .clip(CircleShape)
                                .background(EmeraldNeon.copy(alpha = 0.15f)),
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Default.History,
                                contentDescription = null,
                                tint = EmeraldNeon,
                                modifier = Modifier.size(20.dp)
                            )
                        }
                        Spacer(modifier = Modifier.width(10.dp))
                        Column {
                            Text(
                                text = "Scan History",
                                color = TextPrimary,
                                fontSize = 18.sp,
                                fontWeight = FontWeight.Bold
                            )
                            Text(
                                text = "${historyItems.size} Total Inspections",
                                color = TextSecondary,
                                fontSize = 11.sp
                            )
                        }
                    }

                    IconButton(onClick = onDismiss) {
                        Icon(
                            imageVector = Icons.Default.Close,
                            contentDescription = "Close",
                            tint = TextSecondary
                        )
                    }
                }

                Spacer(modifier = Modifier.height(14.dp))

                // Summary Stats Bar
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(12.dp))
                        .background(ForestSurface)
                        .border(1.dp, BorderHighlight.copy(alpha = 0.4f), RoundedCornerShape(12.dp))
                        .padding(horizontal = 14.dp, vertical = 10.dp),
                    horizontalArrangement = Arrangement.SpaceAround,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(text = "${historyItems.size}", color = TextPrimary, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                        Text(text = "Total", color = TextSecondary, fontSize = 10.sp)
                    }
                    Box(modifier = Modifier.width(1.dp).height(20.dp).background(BorderHighlight))
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(text = "$pathologyCount", color = AlertAmber, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                        Text(text = "Infections", color = TextSecondary, fontSize = 10.sp)
                    }
                    Box(modifier = Modifier.width(1.dp).height(20.dp).background(BorderHighlight))
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(text = "$healthyCount", color = EmeraldNeon, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                        Text(text = "Healthy", color = TextSecondary, fontSize = 10.sp)
                    }
                }

                Spacer(modifier = Modifier.height(14.dp))

                // Action Bar: Export & Clear
                if (historyItems.isNotEmpty()) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.spacedBy(8.dp)
                    ) {
                        Button(
                            onClick = {
                                val report = buildString {
                                    appendLine("=== BioDINO-Edge Agronomic Field Report ===")
                                    appendLine("Generated by BioDINO-Edge On-Device AI")
                                    appendLine("Total Inspected Foliage: ${historyItems.size}")
                                    appendLine("Pathology Detections: $pathologyCount")
                                    appendLine("Healthy Foliage: $healthyCount")
                                    appendLine("===========================================")
                                    appendLine()
                                    historyItems.forEachIndexed { i, item ->
                                        appendLine("${i + 1}. [${item.formattedDate}]")
                                        appendLine("   Diagnosis: ${item.commonName} (${item.latinName})")
                                        appendLine("   Host: ${item.hostPlant}")
                                        appendLine("   Certainty: ${String.format(Locale.US, "%.1f%%", item.confidence * 100)}")
                                        appendLine("   Hardware Latency: ${item.latencyMs} ms")
                                        appendLine("   Agronomy Advice: ${item.actionableAdvice}")
                                        appendLine()
                                    }
                                }

                                val sendIntent = Intent().apply {
                                    action = Intent.ACTION_SEND
                                    putExtra(Intent.EXTRA_TEXT, report)
                                    type = "text/plain"
                                }
                                val shareIntent = Intent.createChooser(sendIntent, "Export Agronomic Field Report")
                                context.startActivity(shareIntent)
                            },
                            colors = ButtonDefaults.buttonColors(
                                containerColor = EmeraldNeon,
                                contentColor = ForestDark
                            ),
                            shape = RoundedCornerShape(12.dp),
                            modifier = Modifier
                                .weight(1f)
                                .height(42.dp)
                        ) {
                            Icon(Icons.Default.Share, contentDescription = null, modifier = Modifier.size(16.dp))
                            Spacer(modifier = Modifier.width(6.dp))
                            Text("Export Official Report", fontSize = 12.sp, fontWeight = FontWeight.Bold)
                        }

                        OutlinedButton(
                            onClick = onClearHistory,
                            shape = RoundedCornerShape(12.dp),
                            modifier = Modifier.height(42.dp)
                        ) {
                            Icon(Icons.Default.DeleteSweep, contentDescription = null, modifier = Modifier.size(16.dp), tint = AlertAmber)
                        }
                    }

                    Spacer(modifier = Modifier.height(12.dp))
                }

                // History Items List
                if (historyItems.isEmpty()) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .weight(1f),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = "No recorded diagnoses yet.\nPoint camera at plant foliage to inspect.",
                            color = TextSecondary,
                            fontSize = 13.sp,
                            lineHeight = 18.sp
                        )
                    }
                } else {
                    LazyColumn(
                        modifier = Modifier
                            .fillMaxWidth()
                            .weight(1f),
                        verticalArrangement = Arrangement.spacedBy(10.dp)
                    ) {
                        items(historyItems) { item ->
                            val plantEmoji = when {
                                item.isHealthy -> "🌿"
                                item.commonName.contains("Apple", ignoreCase = true) -> "🍎"
                                item.commonName.contains("Grape", ignoreCase = true) -> "🍇"
                                else -> "🌱"
                            }

                            Card(
                                colors = CardDefaults.cardColors(containerColor = ForestSurface),
                                shape = RoundedCornerShape(12.dp),
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .border(1.dp, BorderHighlight.copy(alpha = 0.4f), RoundedCornerShape(12.dp))
                            ) {
                                Column(modifier = Modifier.padding(12.dp)) {
                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween,
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Row(verticalAlignment = Alignment.CenterVertically) {
                                            Text(plantEmoji, fontSize = 18.sp, modifier = Modifier.padding(end = 6.dp))
                                            Column {
                                                Text(
                                                    text = item.commonName,
                                                    color = TextPrimary,
                                                    fontSize = 14.sp,
                                                    fontWeight = FontWeight.Bold
                                                )
                                                Text(
                                                    text = item.latinName,
                                                    color = EmeraldAccent,
                                                    fontSize = 10.sp,
                                                    fontStyle = FontStyle.Italic
                                                )
                                            }
                                        }

                                        Text(
                                            text = String.format(Locale.US, "%.1f%%", item.confidence * 100),
                                            color = if (item.isHealthy) EmeraldNeon else AlertAmber,
                                            fontSize = 13.sp,
                                            fontWeight = FontWeight.Bold
                                        )
                                    }

                                    Spacer(modifier = Modifier.height(6.dp))
                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween
                                    ) {
                                        Text(
                                            text = item.formattedDate,
                                            color = TextSecondary,
                                            fontSize = 10.sp
                                        )
                                        Text(
                                            text = "${item.latencyMs} ms",
                                            color = TextSecondary,
                                            fontSize = 10.sp
                                        )
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
