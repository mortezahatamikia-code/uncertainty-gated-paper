package com.biodino.edge.presentation.diagnostic

import android.content.Context
import android.content.Intent
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.VolumeUp
import androidx.compose.material.icons.filled.Eco
import androidx.compose.material.icons.filled.Science
import androidx.compose.material.icons.filled.Share
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.biodino.edge.data.locale.AppLanguage
import com.biodino.edge.data.locale.AppStrings
import com.biodino.edge.domain.model.DiseaseInfo
import com.biodino.edge.presentation.theme.AlertAmber
import com.biodino.edge.presentation.theme.EmeraldNeon
import com.biodino.edge.presentation.theme.ForestDark
import com.biodino.edge.presentation.theme.TextPrimary
import java.util.Locale

@Composable
fun DiagnosticActionsRow(
    disease: DiseaseInfo,
    smoothedConfidence: Float,
    language: AppLanguage,
    strings: AppStrings,
    onSpeakDiagnosis: () -> Unit,
    onOpenCalculator: () -> Unit,
    onOpenCareGuide: () -> Unit,
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current

    Row(
        modifier = modifier.fillMaxWidth(),
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

