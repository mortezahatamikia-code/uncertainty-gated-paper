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
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.LocalFlorist
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import com.biodino.edge.data.locale.AppLanguage
import com.biodino.edge.data.locale.I18n
import com.biodino.edge.domain.repository.PathologyCatalog
import com.biodino.edge.presentation.theme.AlertAmber
import com.biodino.edge.presentation.theme.BorderHighlight
import com.biodino.edge.presentation.theme.EmeraldAccent
import com.biodino.edge.presentation.theme.EmeraldNeon
import com.biodino.edge.presentation.theme.ForestDark
import com.biodino.edge.presentation.theme.ForestSurface
import com.biodino.edge.presentation.theme.TextPrimary
import com.biodino.edge.presentation.theme.TextSecondary

@Composable
fun AtlasSheet(
    isFarsi: Boolean = false,
    language: AppLanguage = if (isFarsi) AppLanguage.PERSIAN else AppLanguage.ENGLISH,
    onDismiss: () -> Unit
) {
    val strings = I18n.getStrings(language)
    var searchQuery by remember { mutableStateOf("") }
    var selectedFilter by remember { mutableStateOf("All") }
    val focusManager = LocalFocusManager.current

    val allDiseases = PathologyCatalog.NOVEL_DISEASES
    val filteredDiseases = remember(searchQuery, selectedFilter, language) {
        allDiseases.filter { disease ->
            val matchesFilter = when (selectedFilter) {
                "Apple" -> disease.rawKey.startsWith("Apple")
                "Grape" -> disease.rawKey.startsWith("Grape")
                "Potato" -> disease.rawKey.startsWith("Potato")
                "Pathologies" -> !disease.isHealthy
                "Healthy" -> disease.isHealthy
                else -> true
            }

            val query = searchQuery.trim().lowercase()
            val matchesSearch = query.isEmpty() ||
                    disease.getLocalizedName(language).lowercase().contains(query) ||
                    disease.commonName.lowercase().contains(query) ||
                    disease.latinTaxonomy.lowercase().contains(query) ||
                    disease.getLocalizedSymptom(language).lowercase().contains(query) ||
                    disease.getLocalizedAdvice(language).lowercase().contains(query) ||
                    disease.getLocalizedHost(language).lowercase().contains(query)

            matchesFilter && matchesSearch
        }
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
                                    imageVector = Icons.Default.LocalFlorist,
                                    contentDescription = null,
                                    tint = EmeraldNeon,
                                    modifier = Modifier.size(20.dp)
                                )
                            }
                            Spacer(modifier = Modifier.width(10.dp))
                            Column {
                                Text(
                                    text = strings.atlasTitle,
                                    color = TextPrimary,
                                    fontSize = 18.sp,
                                    fontWeight = FontWeight.Bold
                                )
                                Text(
                                    text = strings.atlasSub,
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

                    // Quick Search Bar
                    OutlinedTextField(
                        value = searchQuery,
                        onValueChange = { searchQuery = it },
                        placeholder = {
                            Text(
                                text = strings.searchPlaceholder,
                                fontSize = 12.sp,
                                color = TextSecondary
                            )
                        },
                        leadingIcon = {
                            Icon(
                                Icons.Default.Search,
                                contentDescription = null,
                                tint = TextSecondary,
                                modifier = Modifier.size(18.dp)
                            )
                        },
                        trailingIcon = {
                            if (searchQuery.isNotEmpty()) {
                                IconButton(onClick = { searchQuery = "" }) {
                                    Icon(
                                        Icons.Default.Clear,
                                        contentDescription = "Clear",
                                        tint = TextSecondary,
                                        modifier = Modifier.size(16.dp)
                                    )
                                }
                            }
                        },
                        singleLine = true,
                        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                        keyboardActions = KeyboardActions(onSearch = { focusManager.clearFocus() }),
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(52.dp),
                        shape = RoundedCornerShape(14.dp),
                        colors = OutlinedTextFieldDefaults.colors(
                            focusedContainerColor = ForestSurface,
                            unfocusedContainerColor = ForestSurface,
                            focusedBorderColor = EmeraldNeon,
                            unfocusedBorderColor = BorderHighlight,
                            focusedTextColor = TextPrimary,
                            unfocusedTextColor = TextPrimary
                        )
                    )

                    Spacer(modifier = Modifier.height(10.dp))

                    // Filter Chips (Dynamic RTL/LTR)
                    val filterOptions = listOf("All", "Apple", "Grape", "Potato", "Pathologies", "Healthy")
                    LazyRow(
                        horizontalArrangement = Arrangement.spacedBy(8.dp),
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        items(filterOptions) { filter ->
                            val isSelected = selectedFilter == filter
                            val label = when (filter) {
                                "All" -> strings.filterAll
                                "Apple" -> strings.filterApple
                                "Grape" -> strings.filterGrape
                                "Potato" -> strings.filterPotato
                                "Pathologies" -> strings.filterPathologies
                                "Healthy" -> strings.filterHealthy
                                else -> filter
                            }

                            Box(
                                modifier = Modifier
                                    .clip(RoundedCornerShape(10.dp))
                                    .background(if (isSelected) EmeraldNeon else ForestSurface)
                                    .border(1.dp, if (isSelected) EmeraldNeon else BorderHighlight, RoundedCornerShape(10.dp))
                                    .clickable { selectedFilter = filter }
                                    .padding(horizontal = 12.dp, vertical = 6.dp)
                            ) {
                                Text(
                                    text = label,
                                    color = if (isSelected) ForestDark else TextPrimary,
                                    fontSize = 11.sp,
                                    fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Medium
                                )
                            }
                        }
                    }

                    Spacer(modifier = Modifier.height(14.dp))

                    // Disease Cards List
                    if (filteredDiseases.isEmpty()) {
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .weight(1f),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(
                                text = String.format(strings.noDiseasesMatch, searchQuery),
                                color = TextSecondary,
                                fontSize = 13.sp
                            )
                        }
                    } else {
                        LazyColumn(
                            modifier = Modifier
                                .fillMaxWidth()
                                .weight(1f),
                            verticalArrangement = Arrangement.spacedBy(10.dp)
                        ) {
                            items(filteredDiseases) { disease ->
                                val plantEmoji = when {
                                    disease.isHealthy -> "🌿"
                                    disease.rawKey.startsWith("Apple") -> "🍎"
                                    disease.rawKey.startsWith("Grape") -> "🍇"
                                    disease.rawKey.startsWith("Potato") -> "🥔"
                                    else -> "🌱"
                                }

                                Card(
                                    colors = CardDefaults.cardColors(containerColor = ForestSurface),
                                    shape = RoundedCornerShape(14.dp),
                                    modifier = Modifier
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
                        }
                    }
                }
            }
        }
    }
}
