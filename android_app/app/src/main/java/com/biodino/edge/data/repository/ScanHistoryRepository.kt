package com.biodino.edge.data.repository

import android.content.Context
import com.biodino.edge.domain.model.DiagnosisResult
import com.biodino.edge.domain.model.ScanHistoryItem
import com.biodino.edge.domain.repository.IScanHistoryRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import java.util.UUID

class ScanHistoryRepository(context: Context) : IScanHistoryRepository {

    private val prefs = context.getSharedPreferences("biodino_history_prefs", Context.MODE_PRIVATE)
    private val _history = MutableStateFlow<List<ScanHistoryItem>>(emptyList())
    override val history: StateFlow<List<ScanHistoryItem>> = _history.asStateFlow()

    init {
        loadFromPrefs()
    }

    private fun loadFromPrefs() {
        val raw = prefs.getString("history_items", null) ?: return
        try {
            val items = raw.split(";;;").filter { it.isNotBlank() }.mapNotNull { line ->
                val parts = line.split("|||")
                if (parts.size >= 9) {
                    ScanHistoryItem(
                        id = parts[0],
                        timestamp = parts[1].toLongOrNull() ?: 0L,
                        commonName = parts[2],
                        latinName = parts[3],
                        hostPlant = parts[4],
                        confidence = parts[5].toFloatOrNull() ?: 0f,
                        latencyMs = parts[6].toFloatOrNull() ?: 0f,
                        isHealthy = parts[7].toBoolean(),
                        actionableAdvice = parts[8]
                    )
                } else null
            }
            _history.value = items
        } catch (_: Exception) {}
    }

    private fun saveToPrefs(items: List<ScanHistoryItem>) {
        val serialized = items.take(50).joinToString(";;;") { item ->
            listOf(
                item.id,
                item.timestamp.toString(),
                item.commonName,
                item.latinName,
                item.hostPlant,
                item.confidence.toString(),
                item.latencyMs.toString(),
                item.isHealthy.toString(),
                item.actionableAdvice
            ).joinToString("|||")
        }
        prefs.edit().putString("history_items", serialized).apply()
    }

    override fun addFromDiagnosis(result: DiagnosisResult) {
        val now = System.currentTimeMillis()
        val disease = result.diseaseInfo
        val newItem = ScanHistoryItem(
            id = UUID.randomUUID().toString(),
            timestamp = now,
            commonName = disease.commonName,
            latinName = disease.latinTaxonomy,
            hostPlant = disease.hostPlant,
            confidence = result.confidence,
            latencyMs = result.latencyMs,
            isHealthy = disease.isHealthy,
            actionableAdvice = disease.actionableAdvice
        )

        val updated = listOf(newItem) + _history.value.take(49)
        _history.value = updated
        saveToPrefs(updated)
    }

    override fun clearAll() {
        _history.value = emptyList()
        prefs.edit().remove("history_items").apply()
    }
}
