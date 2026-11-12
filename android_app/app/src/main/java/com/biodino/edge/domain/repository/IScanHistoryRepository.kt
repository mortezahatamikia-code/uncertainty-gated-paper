package com.biodino.edge.domain.repository

import com.biodino.edge.domain.model.DiagnosisResult
import com.biodino.edge.domain.model.ScanHistoryItem
import kotlinx.coroutines.flow.StateFlow

/**
 * Domain contract for managing clinical diagnostic scan history items.
 */
interface IScanHistoryRepository {
    val history: StateFlow<List<ScanHistoryItem>>

    fun addFromDiagnosis(result: DiagnosisResult)
    fun clearAll()
}

