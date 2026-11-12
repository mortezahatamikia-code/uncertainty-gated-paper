package com.biodino.edge.presentation.diagnostic

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.biodino.edge.data.locale.AppStrings
import com.biodino.edge.presentation.theme.TextSecondary
import java.util.Locale

@Composable
fun DiagnosticConfidenceBar(
    displayConfidence: Float,
    isConfident: Boolean,
    isGalleryMode: Boolean,
    themeStatusColor: Color,
    strings: AppStrings,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier.fillMaxWidth()) {
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
    }
}

