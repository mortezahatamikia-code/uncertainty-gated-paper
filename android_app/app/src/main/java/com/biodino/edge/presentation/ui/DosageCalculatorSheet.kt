package com.biodino.edge.presentation.ui

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
import androidx.compose.material.icons.filled.Science
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Slider
import androidx.compose.material3.SliderDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import com.biodino.edge.domain.model.DosageChemical
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
    isFarsi: Boolean,
    onDismiss: () -> Unit
) {
    var selectedChemical by remember { mutableStateOf(DosageDatabase.CHEMICALS[0]) }
    var tankLiters by remember { mutableFloatStateOf(20f) }

    val result = remember(tankLiters, selectedChemical) {
        DosageDatabase.calculate(tankLiters, selectedChemical)
    }

    Dialog(onDismissRequest = onDismiss) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .fillMaxHeight(0.88f)
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
                                text = if (isFarsi) "ماشین‌حساب دوز سموم" else "Dosage Calculator",
                                color = TextPrimary,
                                fontSize = 17.sp,
                                fontWeight = FontWeight.Bold
                            )
                            Text(
                                text = if (isFarsi) "محاسبه دقیق مقدار سم بر اساس حجم تانکر" else "Chemical & Water Dilution Ratio",
                                color = TextSecondary,
                                fontSize = 11.sp
                            )
                        }
                    }

                    IconButton(onClick = onDismiss) {
                        Icon(Icons.Default.Close, contentDescription = "Close", tint = TextSecondary)
                    }
                }

                Spacer(modifier = Modifier.height(14.dp))

                LazyColumn(
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(1f),
                    verticalArrangement = Arrangement.spacedBy(14.dp)
                ) {
                    item {
                        // Tank Size Selector
                        Text(
                            text = if (isFarsi) "۱. حجم تانکر سم‌پاش:" else "1. Tank Capacity: ${tankLiters.toInt()} Liters",
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
                                    20f -> if (isFarsi) "۲۰ لیتری (کوله‌ای)" else "20L (Backpack)"
                                    100f -> if (isFarsi) "۱۰۰ لیتری" else "100L"
                                    400f -> if (isFarsi) "۴۰۰ لیتری" else "400L"
                                    else -> if (isFarsi) "۱۰۰۰ لیتری (تراکتور)" else "1000L (Tractor)"
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
                            text = if (isFarsi) "۲. انتخاب قارچ‌کش:" else "2. Select Fungicide:",
                            color = EmeraldNeon,
                            fontSize = 13.sp,
                            fontWeight = FontWeight.Bold
                        )

                        Spacer(modifier = Modifier.height(6.dp))

                        Column(verticalArrangement = Arrangement.spacedBy(6.dp)) {
                            DosageDatabase.CHEMICALS.forEach { chemical ->
                                val isSelected = selectedChemical.id == chemical.id
                                Card(
                                    colors = CardDefaults.cardColors(containerColor = if (isSelected) ForestSurface else ForestDark),
                                    shape = RoundedCornerShape(12.dp),
                                    modifier = Modifier
                                        .fillMaxWidth()
                                        .border(1.dp, if (isSelected) EmeraldNeon else BorderHighlight, RoundedCornerShape(12.dp))
                                        .clickable { selectedChemical = chemical }
                                ) {
                                    Row(
                                        modifier = Modifier.padding(10.dp),
                                        horizontalArrangement = Arrangement.SpaceBetween,
                                        verticalAlignment = Alignment.CenterVertically
                                    ) {
                                        Column(modifier = Modifier.weight(1f)) {
                                            Text(
                                                text = if (isFarsi) chemical.tradeNameFa else chemical.tradeNameEn,
                                                color = TextPrimary,
                                                fontSize = 13.sp,
                                                fontWeight = FontWeight.Bold
                                            )
                                            Text(
                                                text = "${chemical.dosePerLiter} ${chemical.unit}/L • For: ${chemical.targetDisease}",
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
                                    Icon(Icons.Default.Science, contentDescription = null, tint = EmeraldNeon, modifier = Modifier.size(18.dp))
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Text(
                                        text = if (isFarsi) "نسخه نهایی اختلاط تانکر" else "Calculated Tank Prescription",
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
                                    Text(if (isFarsi) "مقدار سم مورد نیاز:" else "Required Chemical:", color = TextSecondary, fontSize = 12.sp)
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
                                    Text(if (isFarsi) "صابون محلول‌پاشی (مویان):" else "Spreader/Adjuvant:", color = TextSecondary, fontSize = 12.sp)
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
                                    Text(if (isFarsi) "دوره کارنس (پرهیز از برداشت):" else "Pre-Harvest Interval (PHI):", color = TextSecondary, fontSize = 12.sp)
                                    Text(
                                        text = "${result.phiDays} ${if (isFarsi) "روز" else "Days"}",
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
