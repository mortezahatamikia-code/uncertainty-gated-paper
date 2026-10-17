package com.biodino.edge.domain.repository

import com.biodino.edge.domain.model.DiagnosisResult
import com.biodino.edge.domain.model.DiseaseInfo

/**
 * Botanical catalog mapping numerical network outputs to clinical taxonomy and agronomic advice.
 */
object PathologyCatalog {

    val NOVEL_DISEASES = listOf(
        DiseaseInfo(
            id = 0,
            rawKey = "Apple___Apple_scab",
            commonName = "Apple Scab",
            latinTaxonomy = "Venturia inaequalis",
            hostPlant = "Malus domestica (Apple)",
            isHealthy = false,
            primarySymptom = "Velvety olive-green to brownish spots with irregular margins on upper leaf surfaces.",
            actionableAdvice = "Apply protective fungicides (Captan or Mancozeb) at green-tip bud break; prune canopy for air flow."
        ),
        DiseaseInfo(
            id = 1,
            rawKey = "Apple___Black_rot",
            commonName = "Apple Black Rot (Frog-Eye)",
            latinTaxonomy = "Botryosphaeria obtusa",
            hostPlant = "Malus domestica (Apple)",
            isHealthy = false,
            primarySymptom = "Circular frog-eye necrotic spots with tan centres and dark purple/red outer rings.",
            actionableAdvice = "Excise diseased cankers during dormant pruning; remove mummified fruit mummies from orchard floor."
        ),
        DiseaseInfo(
            id = 2,
            rawKey = "Apple___Cedar_apple_rust",
            commonName = "Cedar Apple Rust",
            latinTaxonomy = "Gymnosporangium juniperi-virginianae",
            hostPlant = "Malus domestica (Apple)",
            isHealthy = false,
            primarySymptom = "Vibrant yellow-orange spots on upper leaf surfaces with cylindrical aecial tubes underneath.",
            actionableAdvice = "Eradicate alternate host red cedar/juniper trees within 1-2 miles; apply myclobutanil sprays."
        ),
        DiseaseInfo(
            id = 3,
            rawKey = "Apple___healthy",
            commonName = "Healthy Apple Foliage",
            latinTaxonomy = "Malus domestica",
            hostPlant = "Malus domestica (Apple)",
            isHealthy = true,
            primarySymptom = "Uniform chlorophyll pigmentation, symmetrical leaf venation, intact leaf margin.",
            actionableAdvice = "No chemical intervention needed. Maintain routine foliar nutrient monitoring."
        ),
        DiseaseInfo(
            id = 4,
            rawKey = "Grape___Black_rot",
            commonName = "Grape Black Rot",
            latinTaxonomy = "Guignardia bidwellii",
            hostPlant = "Vitis vinifera (Grape)",
            isHealthy = false,
            primarySymptom = "Reddish-brown circular necrotic lesions with small black pycnidia spore dots near borders.",
            actionableAdvice = "Apply DMI/Strobilurin fungicides from pre-bloom through 4 weeks post-bloom."
        ),
        DiseaseInfo(
            id = 5,
            rawKey = "Grape___Esca_(Black_Measles)",
            commonName = "Grape Esca (Black Measles)",
            latinTaxonomy = "Phaeomoniella chlamydospora / Fomitiporia",
            hostPlant = "Vitis vinifera (Grape)",
            isHealthy = false,
            primarySymptom = "Interveinal chlorotic and necrotic striping forming a distinctive 'tiger-stripe' pattern.",
            actionableAdvice = "Protect large pruning wounds with mastic sealant; apply biocontrol Trichoderma agents."
        ),
        DiseaseInfo(
            id = 6,
            rawKey = "Grape___Leaf_blight",
            commonName = "Grape Leaf Blight (Isariopsis)",
            latinTaxonomy = "Pseudocercospora cladosporioides",
            hostPlant = "Vitis vinifera (Grape)",
            isHealthy = false,
            primarySymptom = "Angular, polygonal dark brown spots strictly delimited by main foliar veins.",
            actionableAdvice = "Apply copper-based or dithiocarbamate sprays post-harvest to reduce overwintering inocula."
        ),
        DiseaseInfo(
            id = 7,
            rawKey = "Grape___healthy",
            commonName = "Healthy Grape Foliage",
            latinTaxonomy = "Vitis vinifera",
            hostPlant = "Vitis vinifera (Grape)",
            isHealthy = true,
            primarySymptom = "Palmate lobed leaf structure with healthy serrated margins and robust turgidity.",
            actionableAdvice = "Optimal foliage health. Continue integrated pest management (IPM) scouting."
        )
    )

    fun buildDiagnosis(probabilities: FloatArray, confidence: Float, latencyMs: Float): DiagnosisResult {
        var topIdx = 0
        var topProb = probabilities[0]
        for (i in probabilities.indices) {
            if (probabilities[i] > topProb) {
                topProb = probabilities[i]
                topIdx = i
            }
        }
        val disease = NOVEL_DISEASES.getOrElse(topIdx) { NOVEL_DISEASES[0] }
        return DiagnosisResult(
            diseaseInfo = disease,
            probability = topProb,
            confidence = confidence,
            latencyMs = latencyMs,
            allProbabilities = probabilities
        )
    }
}
