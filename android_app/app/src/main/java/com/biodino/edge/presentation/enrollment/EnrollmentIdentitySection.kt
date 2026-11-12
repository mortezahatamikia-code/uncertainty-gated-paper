package com.biodino.edge.presentation.enrollment

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.biodino.edge.data.locale.AppStrings
import com.biodino.edge.presentation.theme.BorderHighlight
import com.biodino.edge.presentation.theme.EmeraldNeon
import com.biodino.edge.presentation.theme.ForestSurface
import com.biodino.edge.presentation.theme.TextPrimary

@Composable
fun EnrollmentIdentitySection(
    diseaseName: String,
    onDiseaseNameChange: (String) -> Unit,
    hostPlant: String,
    onHostPlantChange: (String) -> Unit,
    adviceText: String,
    onAdviceTextChange: (String) -> Unit,
    strings: AppStrings,
    modifier: Modifier = Modifier
) {
    Column(modifier = modifier.fillMaxWidth()) {
        Text(
            text = strings.step1Ident,
            color = EmeraldNeon,
            fontSize = 13.sp,
            fontWeight = FontWeight.Bold
        )

        Spacer(modifier = Modifier.height(6.dp))

        OutlinedTextField(
            value = diseaseName,
            onValueChange = onDiseaseNameChange,
            label = { Text(strings.fieldName) },
            singleLine = true,
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(12.dp),
            colors = OutlinedTextFieldDefaults.colors(
                focusedContainerColor = ForestSurface,
                unfocusedContainerColor = ForestSurface,
                focusedBorderColor = EmeraldNeon,
                unfocusedBorderColor = BorderHighlight,
                focusedTextColor = TextPrimary,
                unfocusedTextColor = TextPrimary
            )
        )

        Spacer(modifier = Modifier.height(8.dp))

        OutlinedTextField(
            value = hostPlant,
            onValueChange = onHostPlantChange,
            label = { Text(strings.fieldHost) },
            singleLine = true,
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(12.dp),
            colors = OutlinedTextFieldDefaults.colors(
                focusedContainerColor = ForestSurface,
                unfocusedContainerColor = ForestSurface,
                focusedBorderColor = EmeraldNeon,
                unfocusedBorderColor = BorderHighlight,
                focusedTextColor = TextPrimary,
                unfocusedTextColor = TextPrimary
            )
        )

        Spacer(modifier = Modifier.height(8.dp))

        OutlinedTextField(
            value = adviceText,
            onValueChange = onAdviceTextChange,
            label = { Text(strings.fieldAdvice) },
            singleLine = true,
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(12.dp),
            colors = OutlinedTextFieldDefaults.colors(
                focusedContainerColor = ForestSurface,
                unfocusedContainerColor = ForestSurface,
                focusedBorderColor = EmeraldNeon,
                unfocusedBorderColor = BorderHighlight,
                focusedTextColor = TextPrimary,
                unfocusedTextColor = TextPrimary
            )
        )
    }
}

