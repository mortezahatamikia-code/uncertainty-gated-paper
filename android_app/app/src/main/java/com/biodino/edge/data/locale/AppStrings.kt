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

    // Language Selector
    val selectLanguageTitle: String
    val btnCancel: String

    // Errors & Alerts
    val errorUnableToDecodeGallery: String
    val errorLoadingGallery: (String) -> String
}

object EnglishStrings : AppStrings {
    override val brandName = "BioDINO"
    override val brandTag = "EDGE"
    override val cameraPermissionTitle = "Camera Permission Required"
    override val cameraPermissionDesc = "BioDINO-Edge runs real-time plant pathology vision on your device. Camera access is needed to scan foliage."
    override val btnEnableCamera = "Enable Camera Access"
    override val cameraStandbyTitle = "Camera in Battery-Saver Standby"
    override val cameraStandbyDesc = "Camera hardware & frame inference paused to conserve battery.\nTap anywhere to resume live scouting."
    override val btnTurnOnCamera = "Turn On Camera 🟢"
    override val btnTurnOffCamera = "Turn Off Camera (Save Battery) ⏸️"
    override val galleryModeReturnHint = "Gallery View • Tap to return to Live Camera"

    override val tabLiveScan = "Live Scan"
    override val tabGallery = "Gallery"
    override val tabAtlas = "Atlas"
    override val tabDosage = "Dosage"
    override val tabHistory = "History"
    override val tabEnrollClass = "+ Enroll Class (5-Shot)"
    override val tabEcoMode = "Eco Mode"
    override val ecoModeTag = "ECO"

    override val reticleAlignLeaf = "ALIGN LEAF IN RETICLE"
    override val reticleAnalyzing = "ANALYZING SYMPTOMS..."
    override val reticleLocked = "LEAF LOCKED (%d%%)"
    override val reticleSteadyBlur = "HOLD CAMERA STEADY (BLUR)"
    override val reticlePaused = "PAUSED"
    override val reticleEco15Fps = "ECO 15 FPS"

    override val sceneTooDark = "Scene is too dark or lens covered"
    override val sceneTooDarkDesc = "Provide adequate illumination or point camera directly at foliage."
    override val objectNonLeaf = "Object is not a plant leaf"
    override val objectNonLeafDesc = "Visual features do not match foliage manifold. Please point camera at plant leaves."
    override val seekingFoliage = "Seeking foliar pathology..."
    override val pointCameraHint = "Point camera at leaf lesion or upload from gallery."

    override val tagHealthy = "HEALTHY 🌿"
    override val tagPathology = "PATHOLOGY ⚠️"
    override val tagProbable = "PROBABLE 🔍"
    override val confidenceHigh = "Confidence: High"
    override val confidenceModerate = "Confidence: Moderate"
    override val confidenceScanning = "Confidence: Scanning..."
    override val protocolAgronomy = "Agronomy Protocol"
    override val protocolTreatment = "Immediate Treatment Protocol"
    override val viewScientificDetails = "View Scientific Details & Symptoms"
    override val hideScientificDetails = "Hide Lab Analysis"
    override val pathogenLabel = "Pathogen: "
    override val symptomLabel = "Symptoms: "
    override val inferenceTimeLabel = "Inference: %.1f ms • Hardware: %s"
    override val hardwareNnapi = "NNAPI INT8"
    override val hardwareCpu = "Multi-Core CPU"
    override val btnSpeak = "Listen"
    override val btnDosage = "Dosage"
    override val btnCareGuide = "Plant Care 🌿"
    override val btnShareReport = "Share Report"
    override val reportTitle = "🌿 BioDINO-Edge Field Diagnosis Report:"
    override val reportCondition = "• Condition: %s (%s)"
    override val reportHost = "• Host Plant: %s"
    override val reportCertainty = "• Certainty: %s"
    override val reportProtocol = "• Protocol: %s"

    override val atlasTitle = "Pathology Atlas"
    override val atlasSub = "Clinical Disease & Fungicide Reference"
    override val searchPlaceholder = "Search symptoms, fungi, or sprays..."
    override val filterAll = "All (11)"
    override val filterApple = "🍎 Apple (4)"
    override val filterGrape = "🍇 Grape (4)"
    override val filterPotato = "🥔 Potato (3)"
    override val filterPathologies = "⚠️ Pathologies (8)"
    override val filterHealthy = "🌿 Healthy (3)"
    override val noDiseasesMatch = "No diseases match \"%s\""

    override val dosageTitle = "Dosage & Spray Prescription"
    override val dosageSub = "Disease-Targeted Dilution & Weather Window"
    override val weatherWindowOptimal = "Spray Weather Window: Optimal ✅"
    override val weatherWindowSub = "Temp 22°C • Wind 6 km/h • 0% Rain (Tap for details)"
    override val weatherTip = "💡 Agronomic Tip: Mild wind and moderate temperature prevent spray drift and volatilization. Best applied in early morning (6-9 AM) or late afternoon (5-8 PM)."
    override val tempLabel = "Temp"
    override val windLabel = "Wind"
    override val humidityLabel = "Humidity"
    override val rainLabel = "Rain 24h"
    override val stepTankCapacity = "1. Tank Capacity: %d Liters"
    override val stepSelectFungicide = "2. Select Fungicide:"
    override val targetMatch = "Target Match 🎯"
    override val calculatedPrescription = "Calculated Tank Prescription"
    override val requiredChemical = "Required Chemical:"
    override val spreaderAdjuvant = "Spreader/Adjuvant:"
    override val phiLabel = "Pre-Harvest Interval (PHI):"
    override val daysUnit = "Days"
    override val currentLeafHealthyWarning = "Inspected Foliage is Healthy 🌿"
    override val currentLeafHealthyWarningDesc = "No chemical fungicide needed for this leaf. If spraying other orchard blocks, calculate below."
    override val diagnosedCondition = "Diagnosed Condition: %s"
    override val chemicalAutoSelected = "Recommended fungicide \"%s\" pre-selected."

    override val careTitle = "Foliar Nutrition & Care Guide"
    override val careSub = "Organic Foliar Health & Vigor"
    override val healthyBannerTitle = "Foliage in Peak Physiological Health 🌿"
    override val healthyBannerSub = "No chemical fungicide intervention needed. Focus on preventive agronomic vigor."
    override val whyNoSprayTitle = "🚫 Why avoid chemical sprays right now?"
    override val whyNoSprayDesc = "Spraying healthy leaves disrupts beneficial phyllosphere microflora, induces pathogen chemical resistance, risks phytotoxicity, and incurs unnecessary input costs."
    override val carePracticesTitle = "📋 Recommended Agronomic Care Practices:"
    override val practice1Title = "1. Amino Acids & Foliar Biostimulants"
    override val practice1Desc = "Foliar application of free L-amino acids and seaweed extract stimulates systemic acquired resistance (SAR) against stress."
    override val practice2Title = "2. Hygiene-Focused Irrigation"
    override val practice2Desc = "Avoid overhead watering; maintain drip systems to keep foliar canopy dry and prevent free moisture required for spore germination."
    override val practice3Title = "3. Canopy Aeration Pruning"
    override val practice3Desc = "Selective canopy pruning improves air circulation and sunlight penetration, decreasing microclimate relative humidity."
    override val practice4Title = "4. Regular Scouting with BioDINO-Edge"
    override val practice4Desc = "Weekly mobile scouting across canopy strata ensures rapid early-stage detection before pathogens can spread."
    override val btnCloseReturn = "Close & Return to Scanner"

    override val historyTitle = "Scan History"
    override val historySub = "%d Total Inspections"
    override val statTotal = "Total"
    override val statInfections = "Infections"
    override val statHealthy = "Healthy"
    override val btnExportReport = "Export Official Report"
    override val btnClearHistory = "Clear"
    override val emptyHistory = "No scans recorded yet."

    override val enrollTitle = "Field Few-Shot Learning"
    override val enrollSub = "5-Shot Adaptive Prototype Registration"
    override val step1Ident = "1. Class Identification"
    override val fieldName = "Disease / Symptom Name *"
    override val fieldHost = "Host Plant (e.g. Tomato, Olive)"
    override val fieldAdvice = "Agronomic Treatment Advice"
    override val step2Photos = "2. Support Leaf Exemplars (5 Photos)"
    override val btnImportPhotos = "Import Photos from Gallery"
    override val btnCalibrateEnroll = "Calibrate & Enroll Class"
    override val activeClasses = "Active In-Field Classes"

    override val selectLanguageTitle = "Select Application Language"
    override val btnCancel = "Cancel"

    override val errorUnableToDecodeGallery = "Unable to decode foliage image from storage."
    override val errorLoadingGallery: (String) -> String = { err -> "Failed to load image: $err" }
}

object PersianStrings : AppStrings {
    override val brandName = "BioDINO"
    override val brandTag = "EDGE"
    override val cameraPermissionTitle = "مجوز دسترسی به دوربین الزامی است"
    override val cameraPermissionDesc = "سامانه BioDINO-Edge برای اسکن برگ‌ها و تشخیص زنده بیماری‌های گیاهی به دسترسی دوربین نیاز دارد."
    override val btnEnableCamera = "تایید و فعال‌سازی دوربین"
    override val cameraStandbyTitle = "دوربین در حالت صرفه‌جویی باتری (استندبای)"
    override val cameraStandbyDesc = "سنسور سخت‌افزاری دوربین و پردازش فریم‌ها برای کاهش مصرف باتری غیرفعال شد.\nبرای شروع مجدد اسکن لمس کنید."
    override val btnTurnOnCamera = "روشن کردن دوربین 🟢"
    override val btnTurnOffCamera = "خاموش کردن دوربین (صرفه‌جویی باتری) ⏸️"
    override val galleryModeReturnHint = "حالت بازبینی گالری • لمس برای بازگشت به دوربین زنده"

    override val tabLiveScan = "تشخیص زنده"
    override val tabGallery = "گالری"
    override val tabAtlas = "اطلس"
    override val tabDosage = "محاسبه دوز"
    override val tabHistory = "تاریخچه"
    override val tabEnrollClass = "+ افزودن بیماری جدید (۵-شات)"
    override val tabEcoMode = "صرفه‌جویی اِکو"
    override val ecoModeTag = "اِکو"

    override val reticleAlignLeaf = "برگ را درون کادر تنظیم کنید"
    override val reticleAnalyzing = "در حال تحلیل علائم بیماری..."
    override val reticleLocked = "قفل هدف روی برگ (%d%%)"
    override val reticleSteadyBlur = "⚠️ دوربین را ثابت نگه دارید (تاری)"
    override val reticlePaused = "اسکن متوقف شد"
    override val reticleEco15Fps = "مصرف بهینه ۱۵ فریم"

    override val sceneTooDark = "محیط بسیار تاریک است یا لنز پوشانده شده"
    override val sceneTooDarkDesc = "لطفاً نور محیط را تأمین کرده یا دوربین را مستقیماً روی برگ بگیرید."
    override val objectNonLeaf = "سوژه داخل کادر برگ گیاه نیست"
    override val objectNonLeafDesc = "ویژگی‌های بصری با بافت برگ همخوانی ندارد. لطفاً دوربین را روی برگ درخت یا گیاه تنظیم کنید."
    override val seekingFoliage = "در حال جستجو و پایش شاخ‌وبرگ..."
    override val pointCameraHint = "دوربین را روی برگ آلوده یا لکه گیاهی بگیرید یا از گالری بارگذاری کنید."

    override val tagHealthy = "سالم 🌿"
    override val tagPathology = "بیماری قطعی ⚠️"
    override val tagProbable = "تخمین احتمالی 🔍"
    override val confidenceHigh = "ضریب اطمینان مدل: بالا"
    override val confidenceModerate = "ضریب اطمینان: متوسط / تخمینی"
    override val confidenceScanning = "ضریب اطمینان: در حال اسکن..."
    override val protocolAgronomy = "وضعیت زراعی و بهداشت مزرعه"
    override val protocolTreatment = "پروتکل اقدام فوری درمان زراعی"
    override val viewScientificDetails = "مشاهده جزییات علمی، علائم و پاتوژن"
    override val hideScientificDetails = "بستن تحلیل آزمایشگاهی"
    override val pathogenLabel = "عامل پاتوژن: "
    override val symptomLabel = "علائم بالینی: "
    override val inferenceTimeLabel = "زمان استنتاج: %.1f میلی‌ثانیه • سخت‌افزار: %s"
    override val hardwareNnapi = "شتاب سخت‌افزاری NNAPI"
    override val hardwareCpu = "پردازنده چند‌هسته‌ای CPU"
    override val btnSpeak = "پخش صوتی"
    override val btnDosage = "محاسبه دوز"
    override val btnCareGuide = "راهنمای مراقبت 🌿"
    override val btnShareReport = "اشتراک‌گذاری گزارش"
    override val reportTitle = "🌿 گزارش رسمی عارضه‌یابی مزرعه BioDINO-Edge:"
    override val reportCondition = "• وضعیت: %s (%s)"
    override val reportHost = "• گیاه میزبان: %s"
    override val reportCertainty = "• درصد اطمینان مدل: %s"
    override val reportProtocol = "• دستورالعمل زراعی: %s"

    override val atlasTitle = "اطلس بیماری‌های گیاهی"
    override val atlasSub = "مرجع جامع قارچ‌شناسی و پروتکل درمان"
    override val searchPlaceholder = "جستجوی علائم، نام قارچ، بیماری یا سموم..."
    override val filterAll = "همه (۱۱)"
    override val filterApple = "🍎 سیب (۴)"
    override val filterGrape = "🍇 انگور (۴)"
    override val filterPotato = "🥔 سیب‌زمینی (۳)"
    override val filterPathologies = "⚠️ بیماری‌ها (۸)"
    override val filterHealthy = "🌿 سالم (۳)"
    override val noDiseasesMatch = "موردی با عنوان «%s» یافت نشد"

    override val dosageTitle = "محاسبه دوز و تجویز سموم"
    override val dosageSub = "محاسبه اختلاط بر اساس بیماری و شرایط جوی"
    override val weatherWindowOptimal = "پنجره جوی سم‌پاشی: کاملاً مساعد ✅"
    override val weatherWindowSub = "دما ۲۲°C • باد ۶ km/h • بدون بارش (لمس برای جزئیات)"
    override val weatherTip = "💡 پیشنهاد زراعی: به دلیل دمای زیر ۲۵°C و وزش باد ملایم، بهترین زمان محلول‌پاشی ساعات خنک صبح زود (۶ تا ۹) یا عصرگاه (۱۷ تا ۲۰) است. از سم‌پاشی در ظهر گرم خودداری فرمایید."
    override val tempLabel = "دما"
    override val windLabel = "سرعت باد"
    override val humidityLabel = "رطوبت"
    override val rainLabel = "بارش ۲۴h"
    override val stepTankCapacity = "۱. حجم تانکر سم‌پاش: %d لیتر"
    override val stepSelectFungicide = "۲. انتخاب قارچ‌کش مورد نظر:"
    override val targetMatch = "پیشنهاد اختصاصی 🎯"
    override val calculatedPrescription = "نسخه نهایی اختلاط تانکر"
    override val requiredChemical = "مقدار سم مورد نیاز:"
    override val spreaderAdjuvant = "صابون محلول‌پاشی (مویان):"
    override val phiLabel = "دوره کارنس (پرهیز از برداشت):"
    override val daysUnit = "روز"
    override val currentLeafHealthyWarning = "برگ اسکن‌شده سالم است 🌿"
    override val currentLeafHealthyWarningDesc = "سم‌پاشی شیمیایی نیاز نیست. در صورت سم‌پاشی سایر قطعات باغ، می‌توانید از فرمول زیر استفاده کنید."
    override val diagnosedCondition = "بیماری شناسایی‌شده: %s"
    override val chemicalAutoSelected = "قارچ‌کش اختصاصی «%s» به صورت خودکار فعال شد."

    override val careTitle = "راهنمای بهداشت و تغذیه گیاه"
    override val careSub = "بهداشت ارگانیک و شادابی کانوپی"
    override val healthyBannerTitle = "گیاه در سلامت کامل است 🌿"
    override val healthyBannerSub = "عدم نیاز به هرگونه سم قارچ‌کش شیمیایی. حفظ سلامت طبیعی اولویت دارد."
    override val whyNoSprayTitle = "🚫 چرا سم‌پاشی در این مرحله توصیه نمی‌شود؟"
    override val whyNoSprayDesc = "مصرف بی‌رویه سموم بر روی برگ سالم باعث نابودی میکروفلور مفید، افزایش مقاومت پاتوژن‌ها، سوختگی احتمالی بافت و هزینه غیرضروری می‌شود."
    override val carePracticesTitle = "📋 اقدامات پیشنهادی برای حفظ سرسبزی و باردهی:"
    override val practice1Title = "۱. تغذیه با اسیدهای آمینه و محرک‌های رشد"
    override val practice1Desc = "محلول‌پاشی اسیدهای آمینه آزاد و عصاره جلبک دریایی مقاومت طبیعی دیواره سلولی را در برابر تنش‌های گرمایی و نفوذ قارچ‌ها افزایش می‌دهد."
    override val practice2Title = "۲. مدیریت بهداشت آبیاری"
    override val practice2Desc = "از آبیاری بارانی یا خیس شدن برگ‌ها و طوقه در ساعات غروب خودداری کنید تا از مرطوب ماندن بیش از حد برگ (بستر اولیه رشد اسپور قارچ) پیشگیری شود."
    override val practice3Title = "۳. هرس تهویه و ورود نور خورشید"
    override val practice3Desc = "حذف پاجوش‌ها و شاخه‌های متراکم مرکزی تاج باعث عبور جریان باد و نور آفتاب شده و رطوبت لابلای برگ‌ها را کاهش می‌دهد."
    override val practice4Title = "۴. پایش هفتگی با BioDINO-Edge"
    override val practice4Desc = "هر هفته برگ‌های طبقات مختلف درخت یا بوته را اسکن کنید تا هر نوع علائم اولیه لکه یا زنگ در همان بدو پیدایش مهار شود."
    override val btnCloseReturn = "تایید و بازگشت به دوربین"

    override val historyTitle = "تاریخچه تشخیص‌ها"
    override val historySub = "%d پایش ثبت‌شده"
    override val statTotal = "کل"
    override val statInfections = "آلودگی‌ها"
    override val statHealthy = "سالم"
    override val btnExportReport = "خروجی کارنامه رسمی مزرعه"
    override val btnClearHistory = "پاکسازی"
    override val emptyHistory = "هنوز موردی در تاریخچه ثبت نشده است."

    override val enrollTitle = "یادگیری چند‌نمونه‌ای در مزرعه (Few-Shot)"
    override val enrollSub = "ثبت پروتوتایپ تطبیقی گیاه جدید با ۵ عکس"
    override val step1Ident = "۱. مشخصات بیماری و گیاه جدید"
    override val fieldName = "نام بیماری یا علامت عارضه *"
    override val fieldHost = "گیاه میزبان (مثلاً گوجه‌فرنگی، زیتون)"
    override val fieldAdvice = "توصیه و پروتکل درمان زراعی"
    override val step2Photos = "۲. نمونه تصاویر برگ (دقیقاً ۵ عکس)"
    override val btnImportPhotos = "انتخاب ۵ عکس از گالری"
    override val btnCalibrateEnroll = "کالیبراسیون و ثبت بیماری"
    override val activeClasses = "کلاس‌های فعال در مزرعه"

    override val selectLanguageTitle = "انتخاب زبان برنامه (Language)"
    override val btnCancel = "انصراف"

    override val errorUnableToDecodeGallery = "قالب تصویر قابل پردازش نیست یا حجم تصویر بسیار بالاست."
    override val errorLoadingGallery: (String) -> String = { err -> "خطا در خواندن فایل از حافظه: $err" }
}

object GermanStrings : AppStrings {
    override val brandName = "BioDINO"
    override val brandTag = "EDGE"
    override val cameraPermissionTitle = "Kamerazugriff erforderlich"
    override val cameraPermissionDesc = "BioDINO-Edge führt Echtzeit-Pflanzendiagnostik auf dem Gerät aus. Kamerazugriff ist erforderlich."
    override val btnEnableCamera = "Kamerazugriff aktivieren"
    override val cameraStandbyTitle = "Kamera im Energiesparmodus (Standby)"
    override val cameraStandbyDesc = "Kamerasensor und Inferenz pausiert, um Akku zu sparen.\nTippen Sie auf den Bildschirm, um fortzufahren."
    override val btnTurnOnCamera = "Kamera einschalten 🟢"
    override val btnTurnOffCamera = "Kamera ausschalten (Akku sparen) ⏸️"
    override val galleryModeReturnHint = "Galerieansicht • Tippen für Live-Kamera"

    override val tabLiveScan = "Live-Scan"
    override val tabGallery = "Galerie"
    override val tabAtlas = "Atlas"
    override val tabDosage = "Dosierung"
    override val tabHistory = "Verlauf"
    override val tabEnrollClass = "+ Klasse anlernen (5-Shot)"
    override val tabEcoMode = "Eco-Modus"
    override val ecoModeTag = "ECO"

    override val reticleAlignLeaf = "BLATT IM RASTER AUSRICHTEN"
    override val reticleAnalyzing = "SYMPTOME WERDEN ANALYSIERT..."
    override val reticleLocked = "BLATT ERKANNT (%d%%)"
    override val reticleSteadyBlur = "KAMERA RUHIG HALTEN (UNSCHÄRFE)"
    override val reticlePaused = "PAUSIERT"
    override val reticleEco15Fps = "ECO 15 FPS"

    override val sceneTooDark = "Zu dunkel oder Linse verdeckt"
    override val sceneTooDarkDesc = "Bitte für ausreichend Licht sorgen oder Kamera direkt auf das Blatt richten."
    override val objectNonLeaf = "Objekt ist kein Pflanzenblatt"
    override val objectNonLeafDesc = "Visuelle Merkmale entsprechen keinem Blattgewebe."
    override val seekingFoliage = "Suche nach Blattsymptomen..."
    override val pointCameraHint = "Kamera auf Blattläsion richten oder aus Galerie laden."

    override val tagHealthy = "GESUND 🌿"
    override val tagPathology = "PATHOLOGIE ⚠️"
    override val tagProbable = "WAHRSCHEINLICH 🔍"
    override val confidenceHigh = "Konfidenz: Hoch"
    override val confidenceModerate = "Konfidenz: Moderat"
    override val confidenceScanning = "Konfidenz: Abtasten..."
    override val protocolAgronomy = "Agronomischer Status"
    override val protocolTreatment = "Sofortiges Behandlungsprotokoll"
    override val viewScientificDetails = "Wissenschaftliche Details & Symptome"
    override val hideScientificDetails = "Laboranalyse ausblenden"
    override val pathogenLabel = "Erreger: "
    override val symptomLabel = "Symptome: "
    override val inferenceTimeLabel = "Inferenz: %.1f ms • Hardware: %s"
    override val hardwareNnapi = "NNAPI INT8"
    override val hardwareCpu = "Mehrkern-CPU"
    override val btnSpeak = "Vorlesen"
    override val btnDosage = "Dosierung"
    override val btnCareGuide = "Pflanzenpflege 🌿"
    override val btnShareReport = "Bericht teilen"
    override val reportTitle = "🌿 BioDINO-Edge Felddiagnosebericht:"
    override val reportCondition = "• Zustand: %s (%s)"
    override val reportHost = "• Wirtspflanze: %s"
    override val reportCertainty = "• Sicherheit: %s"
    override val reportProtocol = "• Protokoll: %s"

    override val atlasTitle = "Pflanzenpathologie-Atlas"
    override val atlasSub = "Klinische Krankheiten & Fungizid-Referenz"
    override val searchPlaceholder = "Symptome, Pilze oder Spritzmittel suchen..."
    override val filterAll = "Alle (11)"
    override val filterApple = "🍎 Apfel (4)"
    override val filterGrape = "🍇 Weinrebe (4)"
    override val filterPotato = "🥔 Kartoffel (3)"
    override val filterPathologies = "⚠️ Pathologien (8)"
    override val filterHealthy = "🌿 Gesund (3)"
    override val noDiseasesMatch = "Keine Krankheiten gefunden für \"%s\""

    override val dosageTitle = "Dosierung & Spritzplan"
    override val dosageSub = "Gezielte Verdünnung & Wetterfenster"
    override val weatherWindowOptimal = "Spritzwetterfenster: Optimal ✅"
    override val weatherWindowSub = "Temp 22°C • Wind 6 km/h • 0% Regen (Tippen für Details)"
    override val weatherTip = "💡 Agrartipp: Leichter Wind und mäßige Temperatur verhindern Abdrift und Verflüchtigung. Beste Anwendung am frühen Morgen oder späten Nachmittag."
    override val tempLabel = "Temp"
    override val windLabel = "Wind"
    override val humidityLabel = "Feuchte"
    override val rainLabel = "Regen 24h"
    override val stepTankCapacity = "1. Tankvolumen: %d Liter"
    override val stepSelectFungicide = "2. Fungizid auswählen:"
    override val targetMatch = "Zielfund 🎯"
    override val calculatedPrescription = "Berechnete Tankmischung"
    override val requiredChemical = "Benötigtes Pflanzenschutzmittel:"
    override val spreaderAdjuvant = "Netzmittel / Zusatzstoff:"
    override val phiLabel = "Wartezeit (Karenzzeit):"
    override val daysUnit = "Tage"
    override val currentLeafHealthyWarning = "Geprüftes Blatt ist gesund 🌿"
    override val currentLeafHealthyWarningDesc = "Kein Fungizideinsatz erforderlich. Falls andere Parzellen behandelt werden, unten berechnen."
    override val diagnosedCondition = "Diagnostizierter Zustand: %s"
    override val chemicalAutoSelected = "Empfohlenes Fungizid \"%s\" vorausgewählt."

    override val careTitle = "Blattgesundheit & Pflege"
    override val careSub = "Organische Vitalität & Pflege"
    override val healthyBannerTitle = "Blatt in optimaler physiologischer Verfassung 🌿"
    override val healthyBannerSub = "Kein chemischer Pflanzenschutz notwendig. Vorbeugende Pflege steht im Vordergrund."
    override val whyNoSprayTitle = "🚫 Warum jetzt nicht spritzen?"
    override val whyNoSprayDesc = "Unnötiges Spritzen schädigt nützliche Mikroorganismen und fördert Resistenzbildung."
    override val carePracticesTitle = "📋 Empfohlene agronomische Maßnahmen:"
    override val practice1Title = "1. Aminosäuren & Biostimulanzien"
    override val practice1Desc = "Blattdüngung mit Aminosäuren stärkt die natürliche Zellwandabwehr."
    override val practice2Title = "2. Hygienische Bewässerung"
    override val practice2Desc = "Überkopfbewässerung vermeiden; Blätter trocken halten, um Sporenkeimung zu verhindern."
    override val practice3Title = "3. Kronenbelüftung durch Schnitt"
    override val practice3Desc = "Auslichtungsschnitt verbessert Luftzirkulation und reduziert Luftfeuchte."
    override val practice4Title = "4. Regelmäßiges Monitoring"
    override val practice4Desc = "Wöchentliches Scouting mit BioDINO-Edge sichert Früherkennung."
    override val btnCloseReturn = "Schließen & zurück zur Kamera"

    override val historyTitle = "Diagnoseverlauf"
    override val historySub = "%d Gesamtprüfungen"
    override val statTotal = "Gesamt"
    override val statInfections = "Infektionen"
    override val statHealthy = "Gesund"
    override val btnExportReport = "Offiziellen Feldbericht exportieren"
    override val btnClearHistory = "Löschen"
    override val emptyHistory = "Noch keine Scans aufgezeichnet."

    override val enrollTitle = "Few-Shot-Lernen im Feld"
    override val enrollSub = "Adaptive 5-Shot-Prototyp-Registrierung"
    override val step1Ident = "1. Klassenidentifikation"
    override val fieldName = "Krankheits- / Symptomname *"
    override val fieldHost = "Wirtspflanze (z.B. Tomate, Olive)"
    override val fieldAdvice = "Behandlungsempfehlung"
    override val step2Photos = "2. Blattbeispiele (5 Fotos)"
    override val btnImportPhotos = "5 Fotos aus Galerie importieren"
    override val btnCalibrateEnroll = "Kalibrieren & Klasse anlernen"
    override val activeClasses = "Aktive Feldklassen"

    override val selectLanguageTitle = "Sprache auswählen (Language)"
    override val btnCancel = "Abbrechen"

    override val errorUnableToDecodeGallery = "Blattbild konnte nicht aus dem Speicher geladen werden."
    override val errorLoadingGallery: (String) -> String = { err -> "Fehler beim Laden des Bildes: $err" }
}

object FrenchStrings : AppStrings {
    override val brandName = "BioDINO"
    override val brandTag = "EDGE"
    override val cameraPermissionTitle = "Autorisation de caméra requise"
    override val cameraPermissionDesc = "BioDINO-Edge effectue une vision phytopathologique en temps réel sur l'appareil."
    override val btnEnableCamera = "Activer l'accès caméra"
    override val cameraStandbyTitle = "Caméra en veille économique"
    override val cameraStandbyDesc = "Capteur et inférence en pause pour économiser la batterie.\nTouchez l'écran pour reprendre."
    override val btnTurnOnCamera = "Allumer la caméra 🟢"
    override val btnTurnOffCamera = "Éteindre la caméra (Économie) ⏸️"
    override val galleryModeReturnHint = "Mode Galerie • Touchez pour revenir à la caméra"

    override val tabLiveScan = "Scan en direct"
    override val tabGallery = "Galerie"
    override val tabAtlas = "Atlas"
    override val tabDosage = "Dosage"
    override val tabHistory = "Historique"
    override val tabEnrollClass = "+ Enregistrer classe (5-Shot)"
    override val tabEcoMode = "Mode Éco"
    override val ecoModeTag = "ÉCO"

    override val reticleAlignLeaf = "ALIGNER LA FEUILLE DANS LE CADRE"
    override val reticleAnalyzing = "ANALYSE DES SYMPTÔMES..."
    override val reticleLocked = "FEUILLE VERROUILLÉE (%d%%)"
    override val reticleSteadyBlur = "MAINTENIR STABLE (FLOU)"
    override val reticlePaused = "EN PAUSE"
    override val reticleEco15Fps = "ÉCO 15 FPS"

    override val sceneTooDark = "Scène trop sombre ou objectif couvert"
    override val sceneTooDarkDesc = "Assurez un éclairage adéquat ou pointez directement sur la feuille."
    override val objectNonLeaf = "L'objet n'est pas une feuille"
    override val objectNonLeafDesc = "Les caractéristiques visuelles ne correspondent pas au feuillage."
    override val seekingFoliage = "Recherche de pathologie foliaire..."
    override val pointCameraHint = "Pointez vers la lésion ou chargez depuis la galerie."

    override val tagHealthy = "SAIN 🌿"
    override val tagPathology = "PATHOLOGIE ⚠️"
    override val tagProbable = "PROBABLE 🔍"
    override val confidenceHigh = "Confiance: Élevée"
    override val confidenceModerate = "Confiance: Modérée"
    override val confidenceScanning = "Confiance: Analyse..."
    override val protocolAgronomy = "Protocole agronomique"
    override val protocolTreatment = "Protocole de traitement immédiat"
    override val viewScientificDetails = "Voir détails scientifiques & symptômes"
    override val hideScientificDetails = "Masquer l'analyse labo"
    override val pathogenLabel = "Pathogène: "
    override val symptomLabel = "Symptômes: "
    override val inferenceTimeLabel = "Inférence: %.1f ms • Matériel: %s"
    override val hardwareNnapi = "NNAPI INT8"
    override val hardwareCpu = "CPU multi-cœurs"
    override val btnSpeak = "Écouter"
    override val btnDosage = "Dosage"
    override val btnCareGuide = "Soin végétal 🌿"
    override val btnShareReport = "Partager le rapport"
    override val reportTitle = "🌿 Rapport de diagnostic BioDINO-Edge:"
    override val reportCondition = "• Diagnostic: %s (%s)"
    override val reportHost = "• Plante hôte: %s"
    override val reportCertainty = "• Certitude: %s"
    override val reportProtocol = "• Protocole: %s"

    override val atlasTitle = "Atlas phytopathologique"
    override val atlasSub = "Répertoire des maladies & fongicides"
    override val searchPlaceholder = "Rechercher symptômes, champignons, fongicides..."
    override val filterAll = "Tous (11)"
    override val filterApple = "🍎 Pommier (4)"
    override val filterGrape = "🍇 Vigne (4)"
    override val filterPotato = "🥔 Pomme de terre (3)"
    override val filterPathologies = "⚠️ Pathologies (8)"
    override val filterHealthy = "🌿 Sain (3)"
    override val noDiseasesMatch = "Aucune maladie ne correspond à \"%s\""

    override val dosageTitle = "Dosage & Prescription de pulvérisation"
    override val dosageSub = "Dilution ciblée & Fenêtre météo"
    override val weatherWindowOptimal = "Fenêtre météo de pulvérisation: Optimale ✅"
    override val weatherWindowSub = "Temp 22°C • Vent 6 km/h • 0% Pluie (Touchez pour détails)"
    override val weatherTip = "💡 Conseil agronomique: Un vent faible et une température modérée évitent la dérive et l'évaporation. Appliquer tôt le matin ou en fin d'après-midi."
    override val tempLabel = "Temp"
    override val windLabel = "Vent"
    override val humidityLabel = "Humidité"
    override val rainLabel = "Pluie 24h"
    override val stepTankCapacity = "1. Capacité de la cuve: %d Litres"
    override val stepSelectFungicide = "2. Sélectionner le fongicide:"
    override val targetMatch = "Recommandé 🎯"
    override val calculatedPrescription = "Prescription calculée pour la cuve"
    override val requiredChemical = "Quantité de produit requise:"
    override val spreaderAdjuvant = "Mouillant / Adjuvant:"
    override val phiLabel = "Délai avant récolte (DAR):"
    override val daysUnit = "Jours"
    override val currentLeafHealthyWarning = "Le feuillage inspecté est sain 🌿"
    override val currentLeafHealthyWarningDesc = "Aucun fongicide chimique requis. Si vous traitez d'autres parcelles, calculez ci-dessous."
    override val diagnosedCondition = "État diagnostiqué: %s"
    override val chemicalAutoSelected = "Fongicide recommandé \"%s\" présélectionné."

    override val careTitle = "Santé foliaire & Conseils agronomiques"
    override val careSub = "Vitalité organique et soin foliaire"
    override val healthyBannerTitle = "Feuillage en pleine santé physiologique 🌿"
    override val healthyBannerSub = "Aucun traitement chimique nécessaire. Priorité aux soins préventifs."
    override val whyNoSprayTitle = "🚫 Pourquoi ne pas pulvériser maintenant?"
    override val whyNoSprayDesc = "Les pulvérisations inutiles détruisent la microflore utile et favorisent les résistances."
    override val carePracticesTitle = "📋 Pratiques agronomiques recommandées:"
    override val practice1Title = "1. Acides aminés & Biostimulants"
    override val practice1Desc = "L'application foliaire d'acides aminés renforce la résistance systémique acquise (SAR)."
    override val practice2Title = "2. Gestion de l'irrigation"
    override val practice2Desc = "Évitez l'aspersion sur le feuillage; gardez les feuilles sèches pour bloquer les spores."
    override val practice3Title = "3. Aération du houppier"
    override val practice3Desc = "L'élagage d'aération réduit l'humidité relative du microclimat foliaire."
    override val practice4Title = "4. Surveillance régulière"
    override val practice4Desc = "Un scouting hebdomadaire avec BioDINO-Edge garantit une détection précoce."
    override val btnCloseReturn = "Fermer & retour caméra"

    override val historyTitle = "Historique des diagnostics"
    override val historySub = "%d Inspections totales"
    override val statTotal = "Total"
    override val statInfections = "Infections"
    override val statHealthy = "Sain"
    override val btnExportReport = "Exporter le rapport officiel"
    override val btnClearHistory = "Effacer"
    override val emptyHistory = "Aucun scan enregistré pour le moment."

    override val enrollTitle = "Few-Shot Learning au champ"
    override val enrollSub = "Enregistrement adaptatif avec 5 photos"
    override val step1Ident = "1. Identification de la classe"
    override val fieldName = "Nom de la maladie / symptôme *"
    override val fieldHost = "Plante hôte (ex. Tomate, Olivier)"
    override val fieldAdvice = "Protocole agronomique conseillé"
    override val step2Photos = "2. Échantillons foliaires (5 photos)"
    override val btnImportPhotos = "Importer 5 photos depuis la galerie"
    override val btnCalibrateEnroll = "Calibrer & Enregistrer la classe"
    override val activeClasses = "Classes actives au champ"

    override val selectLanguageTitle = "Choisir la langue (Language)"
    override val btnCancel = "Annuler"

    override val errorUnableToDecodeGallery = "Impossible de décoder l'image foliaire depuis le stockage."
    override val errorLoadingGallery: (String) -> String = { err -> "Échec du chargement de l'image: $err" }
}

