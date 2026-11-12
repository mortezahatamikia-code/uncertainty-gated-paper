package com.biodino.edge.presentation.dosage

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
import com.biodino.edge.presentation.common.SheetCloseButton
import com.biodino.edge.presentation.common.SheetDragHandle
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
                    SheetDragHandle(modifier = Modifier.align(Alignment.CenterHorizontally))

                    Spacer(modifier = Modifier.height(14.dp))

                    // Header
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Row(
                            modifier = Modifier.weight(1f),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
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
                            Column(modifier = Modifier.padding(end = 8.dp)) {
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

                        SheetCloseButton(onClick = onDismiss)
                    }

                    Spacer(modifier = Modifier.height(12.dp))

                    LazyColumn(
                        modifier = Modifier
                            .fillMaxWidth()
                            .weight(1f),
                        verticalArrangement = Arrangement.spacedBy(14.dp)
                    ) {
                        item {
                            DosageWeatherAdvisory(
                                isExpanded = isWeatherExpanded,
                                onToggleExpand = { isWeatherExpanded = !isWeatherExpanded },
                                language = language,
                                strings = strings
                            )
                        }

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
                            DosageTankSelector(
                                tankLiters = tankLiters,
                                onTankLitersChange = { tankLiters = it },
                                language = language,
                                strings = strings
                            )
                        }

                        item {
                            DosageChemicalSelector(
                                selectedChemical = selectedChemical,
                                onChemicalSelected = { selectedChemical = it },
                                initialRecommended = initialRecommended,
                                language = language,
                                strings = strings
                            )
                        }

                        item {
                            Spacer(modifier = Modifier.height(6.dp))
                            DosageResultCard(
                                result = result,
                                strings = strings
                            )
                        }
                    }
                }
            }
        }
    }
}
