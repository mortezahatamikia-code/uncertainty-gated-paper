package com.biodino.edge.presentation.atlas

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
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.biodino.edge.data.locale.AppLanguage
import com.biodino.edge.data.locale.AppStrings
import com.biodino.edge.domain.model.DiseaseInfo
import com.biodino.edge.presentation.theme.AlertAmber
import com.biodino.edge.presentation.theme.BorderHighlight
import com.biodino.edge.presentation.theme.EmeraldAccent
import com.biodino.edge.presentation.theme.EmeraldNeon
import com.biodino.edge.presentation.theme.ForestDark
import com.biodino.edge.presentation.theme.ForestSurface
import com.biodino.edge.presentation.theme.TextPrimary
import com.biodino.edge.presentation.theme.TextSecondary

@Composable
fun PathologyAtlasCard(
    disease: DiseaseInfo,
    language: AppLanguage,
    strings: AppStrings,
    modifier: Modifier = Modifier
) {
    val isCustom = disease.rawKey.startsWith("Custom___")
    val plantEmoji = when {
        disease.rawKey.startsWith("Apple") -> "🍎"
        disease.rawKey.startsWith("Grape") -> "🍇"
        disease.rawKey.startsWith("Potato") -> "🥔"
        isCustom -> "🔬"
        else -> "🌱"
    }

    Card(
        colors = CardDefaults.cardColors(containerColor = ForestSurface),
        shape = RoundedCornerShape(14.dp),
        modifier = modifier
            .fillMaxWidth()
            .border(1.dp, BorderHighlight.copy(alpha = 0.5f), RoundedCornerShape(14.dp))
    ) {
        Column(modifier = Modifier.padding(14.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.weight(1f)
                ) {
                    Text(plantEmoji, fontSize = 22.sp, modifier = Modifier.padding(end = 8.dp))
                    Column {
                        Text(
                            text = disease.getLocalizedName(language),
                            color = TextPrimary,
                            fontSize = 15.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            text = "${disease.latinTaxonomy} • ${disease.getLocalizedHost(language)}",
                            color = EmeraldAccent,
                            fontSize = 11.sp,
                            fontStyle = FontStyle.Italic
                        )
                    }
                }

                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(6.dp)
                ) {
                    if (isCustom) {
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(8.dp))
                                .background(EmeraldAccent.copy(alpha = 0.25f))
                                .padding(horizontal = 7.dp, vertical = 3.dp)
                        ) {
                            Text(
                                text = strings.filterCustom,
                                color = EmeraldAccent,
                                fontSize = 9.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }

                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(8.dp))
                            .background(if (disease.isHealthy) EmeraldNeon.copy(alpha = 0.2f) else AlertAmber.copy(alpha = 0.2f))
                            .padding(horizontal = 8.dp, vertical = 3.dp)
                    ) {
                        Text(
                            text = if (disease.isHealthy) strings.tagHealthy else strings.tagPathology,
                            color = if (disease.isHealthy) EmeraldNeon else AlertAmber,
                            fontSize = 9.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }
            }

            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = "${strings.symptomLabel}${disease.getLocalizedSymptom(language)}",
                color = TextSecondary,
                fontSize = 12.sp,
                lineHeight = 17.sp
            )

            Spacer(modifier = Modifier.height(8.dp))
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .clip(RoundedCornerShape(8.dp))
                    .background(ForestDark.copy(alpha = 0.6f))
                    .border(
                        1.dp,
                        if (disease.isHealthy) EmeraldNeon.copy(alpha = 0.35f) else AlertAmber.copy(alpha = 0.35f),
                        RoundedCornerShape(8.dp)
                    )
                    .padding(8.dp)
            ) {
                Text(
                    text = "${if (disease.isHealthy) strings.protocolAgronomy else strings.protocolTreatment}: ${disease.getLocalizedAdvice(language)}",
                    color = if (disease.isHealthy) EmeraldNeon else AlertAmber,
                    fontSize = 11.sp,
                    lineHeight = 16.sp,
                    fontWeight = FontWeight.Medium
                )
            }
        }
    }
}

