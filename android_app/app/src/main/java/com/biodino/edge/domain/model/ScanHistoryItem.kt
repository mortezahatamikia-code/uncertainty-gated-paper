package com.biodino.edge.domain.model

import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

data class ScanHistoryItem(
    val id: String,
    val timestamp: Long,
    val commonName: String,
    val latinName: String,
    val hostPlant: String,
    val confidence: Float,
    val latencyMs: Float,
    val isHealthy: Boolean,
    val actionableAdvice: String
) {
    val formattedDate: String
        get() = SimpleDateFormat("MMM dd, yyyy • HH:mm", Locale.getDefault()).format(Date(timestamp))
}
