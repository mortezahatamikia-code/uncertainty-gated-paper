package com.biodino.edge.presentation.ui

import androidx.compose.animation.AnimatedVisibility
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
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
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Calculate
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Eco
import androidx.compose.material.icons.filled.ExpandLess
import androidx.compose.material.icons.filled.ExpandMore
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Science
import androidx.compose.material.icons.filled.WbSunny
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Slider
import androidx.compose.material3.SliderDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import com.biodino.edge.data.locale.AppLanguage
import com.biodino.edge.data.locale.I18n
import com.biodino.edge.domain.model.DiseaseInfo
import com.biodino.edge.domain.model.DosageDatabase
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
fun DosageCalculatorSheet(
    isFarsi: Boolean = false,
    language: AppLanguage = if (isFarsi) AppLanguage.PERSIAN else AppLanguage.ENGLISH,
    targetDisease: DiseaseInfo? = null,
    onDismiss: () -> Unit
) {
    val strings = I18n.getStrings(language)

    // Automatically match and pre-select clinically recommended chemical if disease is diagnosed
    val initialRecommended = remember(targetDisease) {
        if (targetDisease != null && !targetDisease.isHealthy) {
            DosageDatabase.getRecommendedChemicalForDisease(targetDisease.rawKey)
        } else null
    }

    var selectedChemical by remember(initialRecommended) {
        mutableStateOf(initialRecommended ?: DosageDatabase.CHEMICALS[0])
    }
    var tankLiters by remember { mutableFloatStateOf(20f) }
    var isWeatherExpanded by remember { mutableStateOf(false) }

    val result = remember(tankLiters, selectedChemical) {
        DosageDatabase.calculate(tankLiters, selectedChemical)
    }

    Dialog(onDismissRequest = onDismiss) {
        CompositionLocalProvider(
            LocalLayoutDirection provides (if (language.isRtl) LayoutDirection.Rtl else LayoutDirection.Ltr)
        ) {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .fillMaxHeight(0.92f)
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
                                    imageVector = Icons.Default.Calculate,
                                    contentDescription = null,
                                    tint = EmeraldNeon,
                                    modifier = Modifier.size(22.dp)
                                )
                            }
                            Spacer(modifier = Modifier.width(10.dp))
                            Column {
                                Text(
                                    text = strings.dosageTitle,
                                    color = TextPrimary,
                                    fontSize = 16.sp,
                                    fontWeight = FontWeight.Bold
                                )
                                Text(
                                    text = strings.dosageSub,
                                    color = TextSecondary,
                                    fontSize = 11.sp
                                )
                            }
                        }

                        IconButton(onClick = onDismiss) {
                            Icon(Icons.Default.Close, contentDescription = "Close", tint = TextSecondary)
                        }
                    }

                    Spacer(modifier = Modifier.height(12.dp))

                    LazyColumn(
                        modifier = Modifier
                            .fillMaxWidth()
                            .weight(1f),
                        verticalArrangement = Arrangement.spacedBy(14.dp)
                    ) {
                        // Integrated Weather Spray Advisory Card
                        item {
                            Card(
                                colors = CardDefaults.cardColors(containerColor = ForestSurface),
                                shape = RoundedCornerShape(14.dp),
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .border(1.dp, EmeraldNeon.copy(alpha = 0.6f), RoundedCornerShape(14.dp))
                                    .clickable { isWeatherExpanded = !isWeatherExpanded }
                            ) {
                                Column(modifier = Modifier.padding(12.dp)) {
                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween,
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Row(
                                            verticalAlignment = Alignment.CenterVertically,
                                            modifier = Modifier.weight(1f)
                                        ) {
                                            Box(
                                                modifier = Modifier
                                                    .size(30.dp)
                                                    .clip(CircleShape)
                                                    .background(EmeraldNeon.copy(alpha = 0.18f)),
                                                contentAlignment = Alignment.Center
                                            ) {
                                                Icon(
                                                    imageVector = Icons.Default.WbSunny,
                                                    contentDescription = null,
                                                    tint = EmeraldNeon,
                                                    modifier = Modifier.size(18.dp)
                                                )
                                            }
                                            Spacer(modifier = Modifier.width(8.dp))
                                            Column {
                                                Text(
                                                    text = strings.weatherWindowOptimal,
                                                    color = EmeraldNeon,
                                                    fontSize = 12.sp,
                                                    fontWeight = FontWeight.Bold
                                                )
                                                Text(
                                                    text = strings.weatherWindowSub,
                                                    color = TextSecondary,
                                                    fontSize = 10.sp
                                                )
                                            }
                                        }
                                        Icon(
                                            imageVector = if (isWeatherExpanded) Icons.Default.ExpandLess else Icons.Default.ExpandMore,
                                            contentDescription = null,
                                            tint = EmeraldAccent,
                                            modifier = Modifier.size(20.dp)
                                        )
                                    }

                                    AnimatedVisibility(visible = isWeatherExpanded) {
                                        Column(modifier = Modifier.padding(top = 10.dp)) {
                                            Row(
                                                modifier = Modifier.fillMaxWidth(),
                                                horizontalArrangement = Arrangement.spacedBy(6.dp)
                                            ) {
                                                WeatherStatPill(
                                                    label = strings.tempLabel,
                                                    value = "22°C",
                                                    hint = if (language.isRtl) "ایده‌آل" else "Ideal",
                                                    modifier = Modifier.weight(1f)
                                                )
                                                WeatherStatPill(
                                                    label = strings.windLabel,
                                                    value = "6 km/h",
                                                    hint = if (language.isRtl) "بدون دریفت" else "No drift",
                                                    modifier = Modifier.weight(1f)
                                                )
                                                WeatherStatPill(
                                                    label = strings.humidityLabel,
                                                    value = "58%",
                                                    hint = if (language.isRtl) "جذب عالی" else "Good",
                                                    modifier = Modifier.weight(1f)
                                                )
                                                WeatherStatPill(
                                                    label = strings.rainLabel,
                                                    value = "0%",
                                                    hint = if (language.isRtl) "ایمن" else "Safe",
                                                    modifier = Modifier.weight(1f)
                                                )
                                            }

                                            Spacer(modifier = Modifier.height(8.dp))

                                            Text(
                                                text = strings.weatherTip,
                                                color = TextPrimary,
                                                fontSize = 11.sp,
                                                lineHeight = 16.sp
                                            )
                                        }
                                    }
                                }
                            }
                        }

                        // Notice if current diagnosed leaf is Healthy
                        if (targetDisease != null && targetDisease.isHealthy) {
                            item {
                                Card(
                                    colors = CardDefaults.cardColors(containerColor = EmeraldNeon.copy(alpha = 0.12f)),
                                    shape = RoundedCornerShape(14.dp),
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .border(1.dp, EmeraldNeon, RoundedCornerShape(14.dp))
                                ) {
                                    Row(
                                        modifier = Modifier.padding(12.dp),
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Icon(
                                            Icons.Default.Eco,
                                            contentDescription = null,
                                            tint = EmeraldNeon,
                                            modifier = Modifier.size(22.dp)
                                        )
                                        Spacer(modifier = Modifier.width(10.dp))
                                        Column {
                                            Text(
                                                text = strings.currentLeafHealthyWarning,
                                                color = EmeraldNeon,
                                                fontSize = 12.sp,
                                                fontWeight = FontWeight.Bold
                                            )
                                            Text(
                                                text = strings.currentLeafHealthyWarningDesc,
                                                color = TextPrimary,
                                                fontSize = 11.sp
                                            )
                                        }
                                    }
                                }
                            }
                        } else if (targetDisease != null && !targetDisease.isHealthy) {
                            // Highlight targeted pathology match
                            item {
                                Card(
                                    colors = CardDefaults.cardColors(containerColor = AlertAmber.copy(alpha = 0.12f)),
                                    shape = RoundedCornerShape(14.dp),
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .border(1.dp, AlertAmber.copy(alpha = 0.7f), RoundedCornerShape(14.dp))
                                ) {
                                    Row(
                                        modifier = Modifier.padding(12.dp),
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Icon(
                                            Icons.Default.Info,
                                            contentDescription = null,
                                            tint = AlertAmber,
                                            modifier = Modifier.size(20.dp)
                                        )
                                        Spacer(modifier = Modifier.width(10.dp))
                                        Column {
                                            Text(
                                                text = String.format(strings.diagnosedCondition, targetDisease.getLocalizedName(language)),
                                                color = AlertAmber,
                                                fontSize = 12.sp,
                                                fontWeight = FontWeight.Bold
                                            )
                                            if (initialRecommended != null) {
                                                val tradeName = if (language == AppLanguage.PERSIAN) initialRecommended.tradeNameFa else initialRecommended.tradeNameEn
                                                Text(
                                                    text = String.format(strings.chemicalAutoSelected, tradeName),
                                                    color = TextPrimary,
                                                    fontSize = 11.sp
                                                )
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        item {
                            // Tank Size Selector
                            Text(
                                text = String.format(strings.stepTankCapacity, tankLiters.toInt()),
                                color = EmeraldNeon,
                                fontSize = 13.sp,
                                fontWeight = FontWeight.Bold
                            )

                            Spacer(modifier = Modifier.height(6.dp))

                            val presets = listOf(20f, 100f, 400f, 1000f)
                            LazyRow(
                                horizontalArrangement = Arrangement.spacedBy(8.dp),
                                modifier = Modifier.fillMaxWidth()
                            ) {
                                items(presets) { preset ->
                                    val isSelected = tankLiters == preset
                                    val label = when (preset) {
                                        20f -> when (language) {
                                            AppLanguage.PERSIAN -> "۲۰ لیتری (کوله‌ای)"
                                            AppLanguage.GERMAN -> "20L (Rückenspritze)"
                                            AppLanguage.FRENCH -> "20L (À dos)"
                                            AppLanguage.ENGLISH -> "20L (Backpack)"
                                        }
                                        100f -> "100L"
                                        400f -> "400L"
                                        else -> when (language) {
                                            AppLanguage.PERSIAN -> "۱۰۰۰ لیتری (تراکتور)"
                                            AppLanguage.GERMAN -> "1000L (Traktor)"
                                            AppLanguage.FRENCH -> "1000L (Tracteur)"
                                            AppLanguage.ENGLISH -> "1000L (Tractor)"
                                        }
                                    }

                                    Box(
                                        modifier = Modifier
                                            .clip(RoundedCornerShape(10.dp))
                                            .background(if (isSelected) EmeraldNeon else ForestSurface)
                                            .border(1.dp, if (isSelected) EmeraldNeon else BorderHighlight, RoundedCornerShape(10.dp))
                                            .clickable { tankLiters = preset }
                                            .padding(horizontal = 12.dp, vertical = 6.dp)
                                    ) {
                                        Text(
                                            text = label,
                                            color = if (isSelected) ForestDark else TextPrimary,
                                            fontSize = 11.sp,
                                            fontWeight = FontWeight.Bold
                                        )
                                    }
                                }
                            }

                            Spacer(modifier = Modifier.height(6.dp))

                            Slider(
                                value = tankLiters,
                                onValueChange = { tankLiters = it },
                                valueRange = 10f..1000f,
                                steps = 98,
                                colors = SliderDefaults.colors(
                                    thumbColor = EmeraldNeon,
                                    activeTrackColor = EmeraldNeon,
                                    inactiveTrackColor = BorderHighlight
                                )
                            )
                        }

                        item {
                            // Chemical Selector
                            Text(
                                text = strings.stepSelectFungicide,
                                color = EmeraldNeon,
                                fontSize = 13.sp,
                                fontWeight = FontWeight.Bold
                            )

                            Spacer(modifier = Modifier.height(6.dp))

                            Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                                DosageDatabase.CHEMICALS.forEach { chemical ->
                                    val isSelected = selectedChemical.id == chemical.id
                                    val isRecommendedForThis = initialRecommended?.id == chemical.id

                                    Card(
                                        colors = CardDefaults.cardColors(
                                            containerColor = if (isSelected) ForestSurface else ForestDark
                                        ),
                                        shape = RoundedCornerShape(12.dp),
                                        modifier = Modifier
                                            .fillMaxWidth()
                                            .border(
                                                1.dp,
                                                if (isSelected) EmeraldNeon else if (isRecommendedForThis) AlertAmber else BorderHighlight,
                                                RoundedCornerShape(12.dp)
                                            )
                                            .clickable { selectedChemical = chemical }
                                    ) {
                                        Row(
                                            modifier = Modifier.padding(10.dp),
                                            horizontalArrangement = Arrangement.SpaceBetween,
                                            verticalAlignment = Alignment.CenterVertically
                                        ) {
                                            Column(modifier = Modifier.weight(1f)) {
                                                Row(verticalAlignment = Alignment.CenterVertically) {
                                                    Text(
                                                        text = if (language == AppLanguage.PERSIAN) chemical.tradeNameFa else chemical.tradeNameEn,
                                                        color = TextPrimary,
                                                        fontSize = 13.sp,
                                                        fontWeight = FontWeight.Bold
                                                    )
                                                    if (isRecommendedForThis) {
                                                        Spacer(modifier = Modifier.width(6.dp))
                                                        Box(
                                                            modifier = Modifier
                                                                .clip(RoundedCornerShape(6.dp))
                                                                .background(AlertAmber.copy(alpha = 0.2f))
                                                                .padding(horizontal = 6.dp, vertical = 2.dp)
                                                        ) {
                                                            Text(
                                                                text = strings.targetMatch,
                                                                color = AlertAmber,
                                                                fontSize = 9.sp,
                                                                fontWeight = FontWeight.Bold
                                                            )
                                                        }
                                                    }
                                                }
                                                Text(
                                                    text = "${chemical.dosePerLiter} ${chemical.unit}/L • ${chemical.targetDisease}",
                                                    color = TextSecondary,
                                                    fontSize = 10.sp
                                                )
                                            }

                                            if (isSelected) {
                                                Box(
                                                    modifier = Modifier
                                                        .size(10.dp)
                                                        .clip(CircleShape)
                                                        .background(EmeraldNeon)
                                                )
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        item {
                            // Result Card
                            Spacer(modifier = Modifier.height(6.dp))
                            Card(
                                colors = CardDefaults.cardColors(containerColor = ForestSurface),
                                shape = RoundedCornerShape(16.dp),
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .border(1.5.dp, EmeraldNeon, RoundedCornerShape(16.dp))
                            ) {
                                Column(modifier = Modifier.padding(14.dp)) {
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Icon(
                                            Icons.Default.Science,
                                            contentDescription = null,
                                            tint = EmeraldNeon,
                                            modifier = Modifier.size(18.dp)
                                        )
                                        Spacer(modifier = Modifier.width(8.dp))
                                        Text(
                                            text = strings.calculatedPrescription,
                                            color = EmeraldNeon,
                                            fontSize = 14.sp,
                                            fontWeight = FontWeight.Bold
                                        )
                                    }

                                    Spacer(modifier = Modifier.height(10.dp))

                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween
                                    ) {
                                        Text(strings.requiredChemical, color = TextSecondary, fontSize = 12.sp)
                                        Text(
                                            text = String.format(Locale.US, "%.1f %s", result.totalChemicalAmount, result.chemical.unit),
                                            color = TextPrimary,
                                            fontSize = 14.sp,
                                            fontWeight = FontWeight.Bold
                                        )
                                    }

                                    Spacer(modifier = Modifier.height(4.dp))

                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween
                                    ) {
                                        Text(strings.spreaderAdjuvant, color = TextSecondary, fontSize = 12.sp)
                                        Text(
                                            text = String.format(Locale.US, "%.1f ml", result.totalAdjuvantAmount),
                                            color = EmeraldAccent,
                                            fontSize = 12.sp,
                                            fontWeight = FontWeight.Bold
                                        )
                                    }

                                    Spacer(modifier = Modifier.height(4.dp))

                                    Row(
                                        modifier = Modifier.fillMaxWidth(),
                                        horizontalArrangement = Arrangement.SpaceBetween
                                    ) {
                                        Text(strings.phiLabel, color = TextSecondary, fontSize = 12.sp)
                                        Text(
                                            text = "${result.phiDays} ${strings.daysUnit}",
                                            color = AlertAmber,
                                            fontSize = 12.sp,
                                            fontWeight = FontWeight.Bold
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

@Composable
private fun WeatherStatPill(
    label: String,
    value: String,
    hint: String,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .clip(RoundedCornerShape(8.dp))
            .background(ForestDark)
            .border(1.dp, BorderHighlight, RoundedCornerShape(8.dp))
            .padding(vertical = 6.dp, horizontal = 4.dp),
        contentAlignment = Alignment.Center
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Text(text = label, color = TextSecondary, fontSize = 9.sp)
            Text(text = value, color = EmeraldNeon, fontSize = 11.sp, fontWeight = FontWeight.Bold)
            Text(text = hint, color = TextSecondary, fontSize = 8.sp)
        }
    }
}
