package com.biodino.edge.presentation.history

import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.biodino.edge.domain.model.ScanHistoryItem
import com.biodino.edge.presentation.theme.AlertAmber
import com.biodino.edge.presentation.theme.BorderHighlight
import com.biodino.edge.presentation.theme.EmeraldAccent
import com.biodino.edge.presentation.theme.EmeraldNeon
import com.biodino.edge.presentation.theme.ForestSurface
import com.biodino.edge.presentation.theme.TextPrimary
import com.biodino.edge.presentation.theme.TextSecondary
import java.util.Locale

@Composable
fun HistoryItemCard(
    item: ScanHistoryItem,
    modifier: Modifier = Modifier
) {
    val plantEmoji = when {
        item.isHealthy -> "🌿"
        item.commonName.contains("Apple", ignoreCase = true) || item.commonName.contains("سیب", ignoreCase = true) -> "🍎"
        item.commonName.contains("Grape", ignoreCase = true) || item.commonName.contains("انگور", ignoreCase = true) -> "🍇"
        item.commonName.contains("Potato", ignoreCase = true) || item.commonName.contains("سیب‌زمینی", ignoreCase = true) -> "🥔"
        else -> "🌱"
    }

    Card(
        colors = CardDefaults.cardColors(containerColor = ForestSurface),
        shape = RoundedCornerShape(12.dp),
        modifier = modifier
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
