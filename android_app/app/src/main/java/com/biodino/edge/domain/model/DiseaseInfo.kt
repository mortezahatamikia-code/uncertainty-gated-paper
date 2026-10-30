package com.biodino.edge.domain.model

import com.biodino.edge.data.locale.AppLanguage

/**
 * Encapsulates biological and clinical metadata for a plant foliar disease category.
 * Fully bilingual (EN / FA) with clinical pathology descriptions and treatment protocols.
 */
data class DiseaseInfo(
    val id: Int,
    val rawKey: String,
    val commonName: String,
    val commonNameFa: String = commonName,
    val latinTaxonomy: String,
    val hostPlant: String,
    val hostPlantFa: String = hostPlant,
    val isHealthy: Boolean,
    val primarySymptom: String,
    val primarySymptomFa: String = primarySymptom,
    val actionableAdvice: String,
    val actionableAdviceFa: String = actionableAdvice
) {
    fun getLocalizedName(isFarsi: Boolean): String = if (isFarsi) commonNameFa else commonName
    fun getLocalizedHost(isFarsi: Boolean): String = if (isFarsi) hostPlantFa else hostPlant
    fun getLocalizedSymptom(isFarsi: Boolean): String = if (isFarsi) primarySymptomFa else primarySymptom
    fun getLocalizedAdvice(isFarsi: Boolean): String = if (isFarsi) actionableAdviceFa else actionableAdvice

    fun getLocalizedName(language: AppLanguage): String = if (language == AppLanguage.PERSIAN) commonNameFa else commonName
    fun getLocalizedHost(language: AppLanguage): String = if (language == AppLanguage.PERSIAN) hostPlantFa else hostPlant
    fun getLocalizedSymptom(language: AppLanguage): String = if (language == AppLanguage.PERSIAN) primarySymptomFa else primarySymptom
    fun getLocalizedAdvice(language: AppLanguage): String = if (language == AppLanguage.PERSIAN) actionableAdviceFa else actionableAdvice
}
