package com.biodino.edge.domain.model

/**
 * Real-time diagnostic prediction payload produced per analyzed camera frame.
 */
data class DiagnosisResult(
    val diseaseInfo: DiseaseInfo,
    val probability: Float,
    val confidence: Float,
    val latencyMs: Float,
    val allProbabilities: FloatArray,
    val foliageScore: Float = 1.0f,
    val isFoliage: Boolean = true,
    val isTooDark: Boolean = false
) {
    val isConfident: Boolean
        get() = isFoliage && !isTooDark && confidence >= 0.35f

    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (javaClass != other?.javaClass) return false
        other as DiagnosisResult
        return diseaseInfo == other.diseaseInfo &&
                probability == other.probability &&
                confidence == other.confidence &&
                latencyMs == other.latencyMs &&
                foliageScore == other.foliageScore &&
                isFoliage == other.isFoliage &&
                isTooDark == other.isTooDark &&
                allProbabilities.contentEquals(other.allProbabilities)
    }

    override fun hashCode(): Int {
        var result = diseaseInfo.hashCode()
        result = 31 * result + probability.hashCode()
        result = 31 * result + confidence.hashCode()
        result = 31 * result + latencyMs.hashCode()
        result = 31 * result + foliageScore.hashCode()
        result = 31 * result + isFoliage.hashCode()
        result = 31 * result + isTooDark.hashCode()
        result = 31 * result + allProbabilities.contentHashCode()
        return result
    }
}
