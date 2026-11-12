package com.biodino.edge.domain.model

data class CustomEnrolledDisease(
    val id: String,
    val commonName: String,
    val hostPlant: String,
    val latinTaxonomy: String,
    val isHealthy: Boolean,
    val primarySymptom: String,
    val actionableAdvice: String,
    val prototypeEmbedding: FloatArray,
    val shotCount: Int = 5,
    val enrolledTimestamp: Long = System.currentTimeMillis()
) {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (javaClass != other?.javaClass) return false
        other as CustomEnrolledDisease
        return id == other.id &&
                commonName == other.commonName &&
                prototypeEmbedding.contentEquals(other.prototypeEmbedding)
    }

    override fun hashCode(): Int {
        var result = id.hashCode()
        result = 31 * result + commonName.hashCode()
        result = 31 * result + prototypeEmbedding.contentHashCode()
        return result
    }

    fun toDiseaseInfo(syntheticId: Int): DiseaseInfo {
        return DiseaseInfo(
            id = syntheticId,
            rawKey = "Custom___${commonName.replace(' ', '_')}",
            commonName = commonName,
            latinTaxonomy = latinTaxonomy.ifBlank { "Custom In-Field Prototype" },
            hostPlant = hostPlant.ifBlank { "Field Host" },
            isHealthy = isHealthy,
            primarySymptom = primarySymptom.ifBlank { "Identified by calibrated in-field prototype." },
            actionableAdvice = actionableAdvice.ifBlank { "Custom protocol registered in the field." }
        )
    }
}
