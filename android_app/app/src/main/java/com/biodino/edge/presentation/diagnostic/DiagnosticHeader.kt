package com.biodino.edge.presentation.diagnostic

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.biodino.edge.data.locale.AppLanguage
import com.biodino.edge.data.locale.AppStrings
import com.biodino.edge.domain.model.DiseaseInfo
import com.biodino.edge.presentation.theme.TextPrimary
import com.biodino.edge.presentation.theme.TextSecondary

@Composable
fun DiagnosticHeader(
    disease: DiseaseInfo,
    themeStatusColor: Color,
    isConfident: Boolean,
    language: AppLanguage,
    strings: AppStrings,
    modifier: Modifier = Modifier
) {
    val plantEmoji = when {
        disease.isHealthy -> "🌿"
        disease.rawKey.startsWith("Apple") -> "🍎"
        disease.rawKey.startsWith("Grape") -> "🍇"
        disease.rawKey.startsWith("Potato") -> "🥔"
        else -> "🌱"
    }

    Row(
        modifier = modifier.fillMaxWidth(),
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
}

