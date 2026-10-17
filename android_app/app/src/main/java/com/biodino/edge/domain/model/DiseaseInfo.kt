package com.biodino.edge.domain.model

/**
 * Encapsulates biological and clinical metadata for a plant foliar disease category.
 */
data class DiseaseInfo(
    val id: Int,
    val rawKey: String,
    val commonName: String,
    val latinTaxonomy: String,
    val hostPlant: String,
    val isHealthy: Boolean,
    val primarySymptom: String,
    val actionableAdvice: String
)
