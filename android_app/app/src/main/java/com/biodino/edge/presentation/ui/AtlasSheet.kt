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
import androidx.compose.material3.FilterChip
import androidx.compose.material3.FilterChipDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.text.font.FontStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import com.biodino.edge.domain.repository.PathologyCatalog
import com.biodino.edge.presentation.theme.AlertAmber
import com.biodino.edge.presentation.theme.BorderHighlight
import com.biodino.edge.presentation.theme.EmeraldAccent
import com.biodino.edge.presentation.theme.EmeraldNeon
import com.biodino.edge.presentation.theme.ForestDark
import com.biodino.edge.presentation.theme.ForestSurface
import com.biodino.edge.presentation.theme.ForestSurfaceGlass
import com.biodino.edge.presentation.theme.TextPrimary
import com.biodino.edge.presentation.theme.TextSecondary

private fun getLocalizedDiseaseName(rawKey: String, commonName: String, isFarsi: Boolean): String {
    if (!isFarsi) return commonName
    return when {
        rawKey.contains("Apple___Apple_scab", ignoreCase = true) -> "اسکب سیب (لکه سیاه)"
        rawKey.contains("Apple___Black_rot", ignoreCase = true) -> "پوسیدگی سیاه سیب (چشم‌قورباغه‌ای)"
        rawKey.contains("Apple___Cedar_apple_rust", ignoreCase = true) -> "زنگ سیب و سرو کوهی"
        rawKey.contains("Apple___healthy", ignoreCase = true) -> "برگ سالم سیب"
        rawKey.contains("Grape___Black_rot", ignoreCase = true) -> "پوسیدگی سیاه انگور"
        rawKey.contains("Grape___Esca", ignoreCase = true) -> "اسکا انگور (سرخک سیاه / راه‌راه ببری)"
        rawKey.contains("Grape___Leaf_blight", ignoreCase = true) -> "سوختگی برگ انگور (بلایت)"
        rawKey.contains("Grape___healthy", ignoreCase = true) -> "برگ سالم مو (انگور)"
        else -> commonName
    }
}

@Composable
fun AtlasSheet(
    isFarsi: Boolean = false,
    onDismiss: () -> Unit
) {
    var searchQuery by remember { mutableStateOf("") }
    var selectedFilter by remember { mutableStateOf("All") }
    val focusManager = LocalFocusManager.current

    val allDiseases = PathologyCatalog.NOVEL_DISEASES
    val filteredDiseases = remember(searchQuery, selectedFilter) {
        allDiseases.filter { disease ->
            val matchesFilter = when (selectedFilter) {
                "Apple" -> disease.rawKey.startsWith("Apple")
                "Grape" -> disease.rawKey.startsWith("Grape")
                "Pathologies" -> !disease.isHealthy
                "Healthy" -> disease.isHealthy
                else -> true
            }

            val query = searchQuery.trim().lowercase()
            val matchesSearch = query.isEmpty() ||
                    disease.commonName.lowercase().contains(query) ||
                    disease.latinTaxonomy.lowercase().contains(query) ||
                    disease.primarySymptom.lowercase().contains(query) ||
                    disease.actionableAdvice.lowercase().contains(query)

            matchesFilter && matchesSearch
        }
    }

    Dialog(onDismissRequest = onDismiss) {
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .fillMaxHeight(0.90f)
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
                                text = if (isFarsi) "اطلس بیماری‌های گیاهی" else "Pathology Atlas",
                                color = TextPrimary,
                                fontSize = 18.sp,
                                fontWeight = FontWeight.Bold
                            )
                            Text(
                                text = if (isFarsi) "مرجع جامع قارچ‌شناسی و پروتکل درمان" else "Clinical Disease & Fungicide Reference",
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
                    placeholder = { Text(if (isFarsi) "جستجوی علائم، نام قارچ یا سموم..." else "Search symptoms, fungi, or sprays...", fontSize = 13.sp, color = TextSecondary) },
                    leadingIcon = { Icon(Icons.Default.Search, contentDescription = null, tint = TextSecondary, modifier = Modifier.size(18.dp)) },
                    trailingIcon = {
                        if (searchQuery.isNotEmpty()) {
                            IconButton(onClick = { searchQuery = "" }) {
                                Icon(Icons.Default.Clear, contentDescription = "Clear", tint = TextSecondary, modifier = Modifier.size(16.dp))
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

                // Filter Chips
                val filterOptions = listOf("All", "Apple", "Grape", "Pathologies", "Healthy")
                LazyRow(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    modifier = Modifier.fillMaxWidth()
                ) {
                    items(filterOptions) { filter ->
                        val isSelected = selectedFilter == filter
                        val label = when (filter) {
                            "All" -> if (isFarsi) "همه (۸)" else "All (8)"
                            "Apple" -> if (isFarsi) "🍎 سیب (۴)" else "🍎 Apple (4)"
                            "Grape" -> if (isFarsi) "🍇 انگور (۴)" else "🍇 Grape (4)"
                            "Pathologies" -> if (isFarsi) "⚠️ بیماری‌ها (۶)" else "⚠️ Pathologies (6)"
                            "Healthy" -> if (isFarsi) "🌿 سالم (۲)" else "🌿 Healthy (2)"
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
                            text = if (isFarsi) "موردی با عنوان «$searchQuery» یافت نشد" else "No diseases match \"$searchQuery\"",
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
                                            Text(plantEmoji, fontSize = 20.sp, modifier = Modifier.padding(end = 8.dp))
                                            Column {
                                                Text(
                                                    text = getLocalizedDiseaseName(disease.rawKey, disease.commonName, isFarsi),
                                                    color = TextPrimary,
                                                    fontSize = 15.sp,
                                                    fontWeight = FontWeight.Bold
                                                )
                                                Text(
                                                    text = disease.latinTaxonomy,
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
                                                text = if (disease.isHealthy) (if (isFarsi) "سالم 🌿" else "HEALTHY") else (if (isFarsi) "بیماری ⚠️" else "PATHOLOGY"),
                                                color = if (disease.isHealthy) EmeraldNeon else AlertAmber,
                                                fontSize = 9.sp,
                                                fontWeight = FontWeight.Bold
                                            )
                                        }
                                    }

                                    Spacer(modifier = Modifier.height(8.dp))
                                    Text(
                                        text = if (isFarsi) "علائم بالینی: ${disease.primarySymptom}" else "Symptoms: ${disease.primarySymptom}",
                                        color = TextSecondary,
                                        fontSize = 12.sp,
                                        lineHeight = 16.sp
                                    )

                                    if (!disease.isHealthy) {
                                        Spacer(modifier = Modifier.height(8.dp))
                                        Box(
                                            modifier = Modifier
                                                .fillMaxWidth()
                                                .clip(RoundedCornerShape(8.dp))
                                                .background(ForestDark.copy(alpha = 0.6f))
                                                .border(1.dp, AlertAmber.copy(alpha = 0.35f), RoundedCornerShape(8.dp))
                                                .padding(8.dp)
                                        ) {
                                            Text(
                                                text = if (isFarsi) "دستور اقدام زراعی: ${disease.actionableAdvice}" else "Protocol: ${disease.actionableAdvice}",
                                                color = AlertAmber,
                                                fontSize = 11.sp,
                                                lineHeight = 15.sp,
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
