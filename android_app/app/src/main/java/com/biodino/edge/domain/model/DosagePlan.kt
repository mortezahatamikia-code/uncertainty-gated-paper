package com.biodino.edge.domain.model

data class DosageChemical(
    val id: String,
    val tradeNameEn: String,
    val tradeNameFa: String,
    val activeIngredient: String,
    val dosePerLiter: Float, // grams or ml per liter
    val unit: String,
    val adjuvantPerLiter: Float = 0.5f, // ml soap/spreader per liter
    val phiDays: Int, // Pre-Harvest Interval (دوره کارنس)
    val targetDisease: String
)

object DosageDatabase {
    val CHEMICALS = listOf(
        DosageChemical(
            id = "captan",
            tradeNameEn = "Captan 50% WP",
            tradeNameFa = "قارچ‌کش کاپتان ۵۰٪ (پودر وتابل)",
            activeIngredient = "Captan (Phthalimide)",
            dosePerLiter = 2.5f,
            unit = "g",
            phiDays = 14,
            targetDisease = "Apple Scab / Black Rot"
        ),
        DosageChemical(
            id = "mancozeb",
            tradeNameEn = "Mancozeb 80% WP",
            tradeNameFa = "قارچ‌کش مانکوزب ۸۰٪",
            activeIngredient = "Mancozeb (Dithiocarbamate)",
            dosePerLiter = 2.0f,
            unit = "g",
            phiDays = 15,
            targetDisease = "Apple Rust / Grape Blight"
        ),
        DosageChemical(
            id = "copper",
            tradeNameEn = "Copper Hydroxide 77% WP",
            tradeNameFa = "اکسی‌کلرور / هیدروکسید مس",
            activeIngredient = "Copper Hydroxide",
            dosePerLiter = 1.5f,
            unit = "g",
            phiDays = 7,
            targetDisease = "Bacterial Blight / Downy Mildew"
        ),
        DosageChemical(
            id = "myclobutanil",
            tradeNameEn = "Myclobutanil 20% EW",
            tradeNameFa = "مایکلووبوتانیل (سیستال ۲۰٪)",
            activeIngredient = "Myclobutanil (Triazole DMI)",
            dosePerLiter = 0.4f,
            unit = "ml",
            phiDays = 14,
            targetDisease = "Cedar Apple Rust / Powdery Mildew"
        ),
        DosageChemical(
            id = "trichoderma",
            tradeNameEn = "Trichoderma Biocontrol",
            tradeNameFa = "تریکودرما (بیولوژیک ارگانیک)",
            activeIngredient = "Trichoderma harzianum T-22",
            dosePerLiter = 1.0f,
            unit = "g",
            phiDays = 0,
            targetDisease = "Grape Esca / Trunk Wounds"
        ),
        DosageChemical(
            id = "metalaxyl",
            tradeNameEn = "Ridomil Gold MZ 68 WG",
            tradeNameFa = "ریدومیل گلد (متالاکسیل-ام + مانکوزب)",
            activeIngredient = "Mefenoxam 4% + Mancozeb 64%",
            dosePerLiter = 2.5f,
            unit = "g",
            phiDays = 7,
            targetDisease = "Potato Late Blight / Phytophthora"
        ),
        DosageChemical(
            id = "chlorothalonil",
            tradeNameEn = "Daconil 720 SC",
            tradeNameFa = "داکونیل (کلروتالونیل ۷۲٪)",
            activeIngredient = "Chlorothalonil (Chloronitrile)",
            dosePerLiter = 2.0f,
            unit = "ml",
            phiDays = 7,
            targetDisease = "Potato Early Blight / Alternaria"
        )
    )

    fun calculate(tankLiters: Float, chemical: DosageChemical): DosageResult {
        val totalChemical = tankLiters * chemical.dosePerLiter
        val totalAdjuvant = tankLiters * chemical.adjuvantPerLiter
        return DosageResult(
            chemical = chemical,
            tankLiters = tankLiters,
            totalChemicalAmount = totalChemical,
            totalAdjuvantAmount = totalAdjuvant,
            phiDays = chemical.phiDays
        )
    }

    /**
     * Finds the clinically recommended chemical for a diagnosed plant pathology rawKey.
     * Returns null if foliage is healthy or no chemical intervention is needed.
     */
    fun getRecommendedChemicalForDisease(rawKey: String?): DosageChemical? {
        if (rawKey == null) return null
        val k = rawKey.lowercase()
        return when {
            k.contains("apple_scab") -> CHEMICALS.firstOrNull { it.id == "captan" }
            k.contains("black_rot") && k.contains("apple") -> CHEMICALS.firstOrNull { it.id == "captan" }
            k.contains("cedar_apple_rust") -> CHEMICALS.firstOrNull { it.id == "myclobutanil" }
            k.contains("black_rot") && k.contains("grape") -> CHEMICALS.firstOrNull { it.id == "mancozeb" }
            k.contains("esca") -> CHEMICALS.firstOrNull { it.id == "trichoderma" }
            k.contains("leaf_blight") -> CHEMICALS.firstOrNull { it.id == "copper" }
            k.contains("early_blight") -> CHEMICALS.firstOrNull { it.id == "chlorothalonil" }
            k.contains("late_blight") -> CHEMICALS.firstOrNull { it.id == "metalaxyl" }
            else -> null
        }
    }
}

data class DosageResult(
    val chemical: DosageChemical,
    val tankLiters: Float,
    val totalChemicalAmount: Float,
    val totalAdjuvantAmount: Float,
    val phiDays: Int
)
