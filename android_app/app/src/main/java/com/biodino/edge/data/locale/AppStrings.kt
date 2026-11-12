package com.biodino.edge.data.locale

import androidx.compose.runtime.staticCompositionLocalOf

val LocalAppLanguage = staticCompositionLocalOf { AppLanguage.ENGLISH }
val LocalAppStrings = staticCompositionLocalOf { I18n.getStrings(AppLanguage.ENGLISH) }

object I18n {
    fun getStrings(lang: AppLanguage): AppStrings = when (lang) {
        AppLanguage.PERSIAN -> PersianStrings
        AppLanguage.GERMAN -> GermanStrings
        AppLanguage.FRENCH -> FrenchStrings
        AppLanguage.ENGLISH -> EnglishStrings
    }
}

interface AppStrings {
    // Brand & Hardware
    val brandName: String
    val brandTag: String
    val cameraPermissionTitle: String
    val cameraPermissionDesc: String
    val btnEnableCamera: String
    val cameraStandbyTitle: String
    val cameraStandbyDesc: String
    val btnTurnOnCamera: String
    val btnTurnOffCamera: String
    val galleryModeReturnHint: String

    // Navigation & Tool Dock
    val tabLiveScan: String
    val tabGallery: String
    val tabAtlas: String
    val tabDosage: String
    val tabHistory: String
    val tabEnrollClass: String
    val tabEcoMode: String
    val ecoModeTag: String
    val tabHardwareNnapi: String
    val tabHardwareCpu: String

    // Reticle
    val reticleAlignLeaf: String
    val reticleAnalyzing: String
    val reticleLocked: String
    val reticleSteadyBlur: String
    val reticlePaused: String
    val reticleEco15Fps: String

    // Quality Alerts
    val sceneTooDark: String
    val sceneTooDarkDesc: String
    val objectNonLeaf: String
    val objectNonLeafDesc: String
    val uncertainFoliage: String
    val uncertainFoliageDesc: String
    val seekingFoliage: String
    val pointCameraHint: String

    // Diagnostic Card
    val tagHealthy: String
    val tagPathology: String
    val tagProbable: String
    val confidenceHigh: String
    val confidenceModerate: String
    val confidenceScanning: String
    val protocolAgronomy: String
    val protocolTreatment: String
    val viewScientificDetails: String
    val hideScientificDetails: String
    val pathogenLabel: String
    val symptomLabel: String
    val inferenceTimeLabel: String
    val hardwareNnapi: String
    val hardwareCpu: String
    val btnSpeak: String
    val btnDosage: String
    val btnCareGuide: String
    val btnShareReport: String
    val reportTitle: String
    val reportCondition: String
    val reportHost: String
    val reportCertainty: String
    val reportProtocol: String

    // Atlas
    val atlasTitle: String
    val atlasSub: String
    val searchPlaceholder: String
    val filterAll: String
    val filterApple: String
    val filterGrape: String
    val filterPotato: String
    val filterPathologies: String
    val filterHealthy: String
    val filterCustom: String get() = "Custom"
    val noDiseasesMatch: String

    // Dosage & Weather
    val dosageTitle: String
    val dosageSub: String
    val weatherWindowOptimal: String
    val weatherWindowSub: String
    val weatherTip: String
    val tempLabel: String
    val windLabel: String
    val humidityLabel: String
    val rainLabel: String
    val stepTankCapacity: String
    val stepSelectFungicide: String
    val targetMatch: String
    val calculatedPrescription: String
    val requiredChemical: String
    val spreaderAdjuvant: String
    val phiLabel: String
    val daysUnit: String
    val currentLeafHealthyWarning: String
    val currentLeafHealthyWarningDesc: String
    val diagnosedCondition: String
    val chemicalAutoSelected: String

    // Plant Care (Healthy)
    val careTitle: String
    val careSub: String
    val healthyBannerTitle: String
    val healthyBannerSub: String
    val whyNoSprayTitle: String
    val whyNoSprayDesc: String
    val carePracticesTitle: String
    val practice1Title: String
    val practice1Desc: String
    val practice2Title: String
    val practice2Desc: String
    val practice3Title: String
    val practice3Desc: String
    val practice4Title: String
    val practice4Desc: String
    val btnCloseReturn: String

    // History
    val historyTitle: String
    val historySub: String
    val statTotal: String
    val statInfections: String
    val statHealthy: String
    val btnExportReport: String
    val btnClearHistory: String
    val emptyHistory: String

    // Few-Shot Enrollment
    val enrollTitle: String
    val enrollSub: String
    val step1Ident: String
    val fieldName: String
    val fieldHost: String
    val fieldAdvice: String
    val step2Photos: String
    val btnImportPhotos: String
    val btnCalibrateEnroll: String
    val activeClasses: String
    val step3HealthyPhotos: String
    val btnImportHealthyPhotos: String
    val healthyPhotosHint: String

    // Language Selector
    val selectLanguageTitle: String
    val btnCancel: String

    // Model Manager (Tier-2 Companion Architecture)
    val tabModelDownload: String
    val tabModelActive: String
    val modelManagerTitle: String
    val modelActiveDefaultTag: String
    val modelActiveCompanionTag: String
    val modelDefaultDesc: String
    val modelCompanionDesc: String
    val modelUrlLabel: String
    val optionCompanion85: String
    val optionJoint110: String
    val btnDownloadModel: String
    val btnRevertDefaultModel: String
    val btnResetUrl: String
    val modelDownloadingStatus: String
    val modelDownloadCompleted: String
    val modelDownloadNote: String

    // Errors & Alerts
    val errorUnableToDecodeGallery: String
    val errorLoadingGallery: (String) -> String

    // Standby Guidance Card
    val standbyTipTitle: String
    val standbyTipDesc: String

    // Companion Model
    val companionModelTitle: String
    val companionModelDesc: String
    val btnRedownloadCompanion: String

    // Few-Shot Enrollment
    val fewShotGuidanceDesc: String
    val btnClearAll: String
    val calibratingExtracting: String
    fun classEnrolledSuccess(name: String, shots: Int): String

    // Notification & Error Messages
    val errModelLoadFailedReverted: String
    val errModelDownloadFailed: String
    val errImageAnalysis: String
    val errEnrollmentFailed: String

    // Weather Window Sheet & Advisory
    val weatherSheetTitle: String
    val weatherSheetSub: String
    val weatherOptimalStatus: String
    val weatherOptimalDesc: String
    val weatherWindSafe: String
    val weatherTempIdeal: String
    val weatherHumidityGood: String
    val weatherAgronomyTip: String
    val weatherHintIdeal: String
    val weatherHintNoDrift: String
    val weatherHintGood: String
    val weatherHintSafe: String

    // Tank Presets
    val tankBackpack20L: String
    val tankTractor1000L: String
}
