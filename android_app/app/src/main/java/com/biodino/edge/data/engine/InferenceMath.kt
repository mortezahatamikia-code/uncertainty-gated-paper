package com.biodino.edge.data.engine

import com.biodino.edge.domain.model.CustomEnrolledDisease
import com.biodino.edge.domain.model.DiagnosisResult
import com.biodino.edge.data.repository.PathologyCatalog
import kotlin.math.ln
import kotlin.math.max
import kotlin.math.min

object InferenceMath {

    fun fuseCustomPrototypes(
        baseProbabilities: FloatArray,
        baseConfidence: Float,
        queryFeatures: FloatArray,
        customPrototypes: List<CustomEnrolledDisease>,
        foliageScore: Float,
        isDark: Boolean,
        latencyMs: Float
    ): DiagnosisResult {
        val baseClassesCount = baseProbabilities.size
        val totalClasses = baseClassesCount + customPrototypes.size
        val combinedLogits = FloatArray(totalClasses)

        // Base class logits reconstructed from probabilities
        for (i in 0 until baseClassesCount) {
            val p = max(baseProbabilities[i], 1e-12f)
            combinedLogits[i] = ln(p)
        }

        // Custom class logits: centered cosine similarity
        var maxCustomDot = 0f
        for (j in customPrototypes.indices) {
            val proto = customPrototypes[j].prototypeEmbedding
            var dot = 0f
            for (k in 0 until 384) {
                dot += queryFeatures[k] * proto[k]
            }
            if (dot > maxCustomDot) maxCustomDot = dot
            val centeredSim = dot - 0.68f
            combinedLogits[baseClassesCount + j] = 22.0f * centeredSim
        }

        // Softmax over all classes
        var maxLogit = Float.NEGATIVE_INFINITY
        for (l in combinedLogits) {
            if (l > maxLogit) maxLogit = l
        }
        var sumExp = 0.0
        val combinedProbs = FloatArray(totalClasses)
        for (i in 0 until totalClasses) {
            val e = Math.exp((combinedLogits[i] - maxLogit).toDouble())
            combinedProbs[i] = e.toFloat()
            sumExp += e
        }
        for (i in 0 until totalClasses) {
            combinedProbs[i] = (combinedProbs[i] / sumExp).toFloat()
        }

        // Dynamic Shannon Confidence calculation
        var top1 = 0f
        var top2 = 0f
        var topIdx = 0
        for (i in 0 until totalClasses) {
            val p = combinedProbs[i]
            if (p > top1) {
                top2 = top1
                top1 = p
                topIdx = i
            } else if (p > top2) {
                top2 = p
            }
        }

        val margin = top1 - top2
        val lnK = ln(totalClasses.toDouble()).toFloat()
        var entropy = 0.0
        for (p in combinedProbs) {
            if (p > 1e-12f) {
                entropy -= p * ln(p.toDouble())
            }
        }
        val normEntropy = (entropy / lnK).toFloat()
        val effectiveFoliageScore = max(foliageScore, maxCustomDot)
        val isFoliage = (effectiveFoliageScore >= 0.12f || maxCustomDot >= 0.45f) && !isDark
        val foliageGate = if (isFoliage) min(1.0f, max(0.60f, (effectiveFoliageScore - 0.08f) / 0.25f)) else 0.0f
        var dynamicConfidence = margin * max(0f, 1.0f - normEntropy) * foliageGate

        // OOD Uncertainty Gate:
        // If a base class won, verify that the foliage is actually consistent with base crops
        if (topIdx < baseClassesCount) {
            if (foliageScore < 0.28f || baseConfidence < 0.20f) {
                dynamicConfidence = min(dynamicConfidence, baseConfidence)
            }
        } else {
            // If a custom class won but dot product is weak (< 0.65), penalize confidence
            if (maxCustomDot < 0.65f) {
                dynamicConfidence = dynamicConfidence.coerceAtMost(0.12f)
            }
        }

        val selectedDisease = if (topIdx < baseClassesCount) {
            PathologyCatalog.NOVEL_DISEASES.getOrElse(topIdx) { PathologyCatalog.NOVEL_DISEASES[0] }
        } else {
            customPrototypes[topIdx - baseClassesCount].toDiseaseInfo(topIdx)
        }

        return DiagnosisResult(
            diseaseInfo = selectedDisease,
            probability = top1,
            confidence = dynamicConfidence,
            latencyMs = latencyMs,
            allProbabilities = combinedProbs,
            foliageScore = effectiveFoliageScore,
            isFoliage = isFoliage,
            isTooDark = isDark
        )
    }
}
