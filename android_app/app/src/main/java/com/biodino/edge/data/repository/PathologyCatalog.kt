package com.biodino.edge.data.repository

import com.biodino.edge.domain.model.DiagnosisResult
import com.biodino.edge.domain.model.DiseaseInfo

/**
 * Plant pathology catalog mapping model outputs to taxonomy and treatment advice.
 */
object PathologyCatalog {

    val NOVEL_DISEASES = listOf(
        DiseaseInfo(
            id = 0,
            rawKey = "Apple___Apple_scab",
            commonName = "Apple Scab",
            commonNameFa = "اسکب سیب (لکه سیاه)",
            latinTaxonomy = "Venturia inaequalis",
            hostPlant = "Malus domestica (Apple)",
            hostPlantFa = "درخت سیب (Malus domestica)",
            isHealthy = false,
            primarySymptom = "Velvety olive-green to dark brownish spots with irregular margins on upper leaf surfaces, causing leaf distortion.",
            primarySymptomFa = "لکه‌های مخملی زیتونی متمایل به قهوه‌ای تیره با حاشیه‌های نامنظم بر سطح رویی برگ و زبری بافت پهنک.",
            actionableAdvice = "Apply protective fungicides (Captan 50% or Mancozeb 80%) at green-tip bud break; prune canopy for air flow.",
            actionableAdviceFa = "محلول‌پاشی قارچ‌کش‌های حفاظتی (کاپتان ۵۰٪ یا مانکوزب ۸۰٪) در مرحله نوک‌سبز جوانه‌ها؛ هرس شاخه‌های متراکم جهت تهویه هوا."
        ),
        DiseaseInfo(
            id = 1,
            rawKey = "Apple___Black_rot",
            commonName = "Apple Black Rot (Frog-Eye)",
            commonNameFa = "پوسیدگی سیاه سیب (لکه چشم‌قورباغه‌ای)",
            latinTaxonomy = "Botryosphaeria obtusa",
            hostPlant = "Malus domestica (Apple)",
            hostPlantFa = "درخت سیب (Malus domestica)",
            isHealthy = false,
            primarySymptom = "Circular frog-eye necrotic spots with tan centres and dark purple/red outer rings on foliar lamina.",
            primarySymptomFa = "لکه‌های نکروتیک مدور شبیه چشم قورباغه با مرکز برنزه/خاکستری و هاله‌های قرمز و بنفش تیره در حاشیه.",
            actionableAdvice = "Excise diseased cankers during dormant pruning; remove mummified fruit mummies from orchard floor; apply Captan sprays.",
            actionableAdviceFa = "تراشیدن و هرس شاخه‌های دارای شانکر؛ جمع‌آوری میوه‌های مومیایی‌شده کف باغ؛ محلول‌پاشی کاپتان یا مانکوزب."
        ),
        DiseaseInfo(
            id = 2,
            rawKey = "Apple___Cedar_apple_rust",
            commonName = "Cedar Apple Rust",
            commonNameFa = "زنگ سیب و سرو کوهی (سدر)",
            latinTaxonomy = "Gymnosporangium juniperi-virginianae",
            hostPlant = "Malus domestica (Apple)",
            hostPlantFa = "درخت سیب (Malus domestica)",
            isHealthy = false,
            primarySymptom = "Vibrant yellow-orange spots on upper leaf surfaces with cylindrical aecial tubes projecting from underside.",
            primarySymptomFa = "لکه‌های زرد-نارنجی براق در سطح رویی برگ با ساختارهای استوانه‌ای و لوله‌ای تولید اسپور در سطح زیرین.",
            actionableAdvice = "Eradicate alternate host red cedar/juniper trees within 1-2 miles; apply triazole myclobutanil sprays from pink bud stage.",
            actionableAdviceFa = "حذف پایه‌های میزبان واسط (سرو کوهی و ارس) در مجاورت باغ؛ محلول‌پاشی تریازول‌ها (مایکلووبوتانیل/سیستال)."
        ),
        DiseaseInfo(
            id = 3,
            rawKey = "Apple___healthy",
            commonName = "Healthy Apple Foliage",
            commonNameFa = "برگ سالم سیب",
            latinTaxonomy = "Malus domestica",
            hostPlant = "Malus domestica (Apple)",
            hostPlantFa = "درخت سیب (Malus domestica)",
            isHealthy = true,
            primarySymptom = "Uniform chlorophyll pigmentation, symmetrical leaf venation, intact margin, active photosynthetic mesophyll.",
            primarySymptomFa = "رنگ سبز کلروفیلی یکنواخت، رگبرگ‌های متقارن و بدون تغییر شکل، پهنک برگ صاف و بدون هرگونه ضایعه نکروتیک.",
            actionableAdvice = "No chemical intervention needed. Maintain routine foliar nutrient monitoring and balanced drip irrigation.",
            actionableAdviceFa = "سلامت کامل بافت برگی؛ عدم نیاز به سم‌پاشی شیمیایی؛ حفظ تغذیه کودی متعادل و پایش دوره‌ای مزرعه."
        ),
        DiseaseInfo(
            id = 4,
            rawKey = "Grape___Black_rot",
            commonName = "Grape Black Rot",
            commonNameFa = "پوسیدگی سیاه انگور (بلک روت)",
            latinTaxonomy = "Guignardia bidwellii",
            hostPlant = "Vitis vinifera (Grape)",
            hostPlantFa = "مو / درخت انگور (Vitis vinifera)",
            isHealthy = false,
            primarySymptom = "Reddish-brown circular necrotic lesions with small black pycnidia spore dots arranged in concentric rings near borders.",
            primarySymptomFa = "لکه‌های دایره‌ای قهوه‌ای مایل به قرمز با نقاط ریز سیاه پیکنید (جوش‌های هاگ‌زا) که در حاشیه لکه ظاهر می‌شوند.",
            actionableAdvice = "Apply DMI or Strobilurin protective fungicides (Mancozeb or Captan) from early pre-bloom through 4 weeks post-bloom.",
            actionableAdviceFa = "محلول‌پاشی قارچ‌کش‌های گروه DMI یا مانکوزب/کاپتان از مرحله پیش از گلدهی تا ۴ هفته پس از تشکیل دانه."
        ),
        DiseaseInfo(
            id = 5,
            rawKey = "Grape___Esca_(Black_Measles)",
            commonName = "Grape Esca (Black Measles)",
            commonNameFa = "اسکا انگور (سرخک سیاه / راه‌راه ببری)",
            latinTaxonomy = "Phaeomoniella chlamydospora / Fomitiporia",
            hostPlant = "Vitis vinifera (Grape)",
            hostPlantFa = "مو / درخت انگور (Vitis vinifera)",
            isHealthy = false,
            primarySymptom = "Severe interveinal chlorotic and necrotic striping forming a distinctive 'tiger-stripe' pattern; marginal foliar desiccation.",
            primarySymptomFa = "کلروز و نکروز شدید بین رگبرگی که طرح راه‌راه ببری متمایزی روی برگ مو ایجاد می‌کند؛ خشکیدگی حاشیه‌ای برگ.",
            actionableAdvice = "Protect large pruning wounds with mastic sealant; apply biocontrol Trichoderma harzianum agents; sanitize pruning shears.",
            actionableAdviceFa = "ضدعفونی و پوشاندن زخم‌های هرس با چسب باغبانی محافظ؛ استفاده از عوامل بیولوژیک قارچ تریکودرما (Trichoderma)."
        ),
        DiseaseInfo(
            id = 6,
            rawKey = "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
            commonName = "Grape Leaf Blight (Isariopsis)",
            commonNameFa = "سوختگی و لکه برگی انگور (ایزاریوپسیس)",
            latinTaxonomy = "Pseudocercospora cladosporioides / vitis",
            hostPlant = "Vitis vinifera (Grape)",
            hostPlantFa = "مو / درخت انگور (Vitis vinifera)",
            isHealthy = false,
            primarySymptom = "Angular, polygonal dark brown necrotic lesions strictly delimited by secondary and tertiary foliar veins.",
            primarySymptomFa = "لکه‌های زاویه‌دار و چندضلعی قهوه‌ای تیره که به طور مشخص توسط رگبرگ‌های فرعی پهنک برگ محدود شده‌اند.",
            actionableAdvice = "Apply copper hydroxide or dithiocarbamate sprays post-harvest to reduce overwintering fungal inocula.",
            actionableAdviceFa = "محلول‌پاشی ترکیبات مسی (اکسی‌کلرور/هیدروکسید مس) یا مانکوزب بلافاصله پس از برداشت جهت مهار اسپورهای زمستان‌گذران."
        ),
        DiseaseInfo(
            id = 7,
            rawKey = "Grape___healthy",
            commonName = "Healthy Grape Foliage",
            commonNameFa = "برگ سالم مو (انگور)",
            latinTaxonomy = "Vitis vinifera",
            hostPlant = "Vitis vinifera (Grape)",
            hostPlantFa = "مو / درخت انگور (Vitis vinifera)",
            isHealthy = true,
            primarySymptom = "Palmate lobed leaf structure with healthy serrated margins, robust cell turgidity, deep green chlorophyll density.",
            primarySymptomFa = "ساختار برگ پنجه‌ای با لبه‌های دندانه‌دار منظم، تورژسنس شاداب سلولی و رنگ سبز غنی عاری از هرگونه علائم آلودگی.",
            actionableAdvice = "Optimal foliage health. Continue integrated pest management (IPM) scouting and balanced potassium nutrition.",
            actionableAdviceFa = "سلامت ایده‌آل شاخ‌وبرگ؛ بدون نیاز به مداخله شیمیایی؛ ادامه مدیریت تلفیقی آفات (IPM) و محلول‌پاشی عناصر ریزمغذی."
        ),
        DiseaseInfo(
            id = 8,
            rawKey = "Potato___Early_blight",
            commonName = "Potato Early Blight",
            commonNameFa = "بلایت زودرس سیب‌زمینی (آلترناریا)",
            latinTaxonomy = "Alternaria solani",
            hostPlant = "Solanum tuberosum (Potato)",
            hostPlantFa = "بوته سیب‌زمینی (Solanum tuberosum)",
            isHealthy = false,
            primarySymptom = "Dark brown circular necrotic lesions with concentric target-board rings surrounded by a chlorotic yellow halo.",
            primarySymptomFa = "لکه‌های دایره‌ای قهوه‌ای تیره با دوایر متحدالمرکز شبیه سیبل تیراندازی (Target-board) محصور در هاله‌ای زردکلروتیک.",
            actionableAdvice = "Apply protective fungicides (Chlorothalonil 72% or Mancozeb); avoid overhead sprinkler irrigation; rotate with non-solanaceous crops.",
            actionableAdviceFa = "محلول‌پاشی قارچ‌کش‌های حفاظتی (داکونیل/کلروتالونیل یا مانکوزب)؛ پرهیز از آبیاری بارانی؛ تناوب زراعی با غیربادمجانیان."
        ),
        DiseaseInfo(
            id = 9,
            rawKey = "Potato___Late_blight",
            commonName = "Potato Late Blight",
            commonNameFa = "بلایت دیررس / بادزدگی سیب‌زمینی (فیتوفتورا)",
            latinTaxonomy = "Phytophthora infestans (Oomycete)",
            hostPlant = "Solanum tuberosum (Potato)",
            hostPlantFa = "بوته سیب‌زمینی (Solanum tuberosum)",
            isHealthy = false,
            primarySymptom = "Water-soaked dark lesions rapidly expanding into necrotic collapse with white downy mildew sporulation on lower leaf surface.",
            primarySymptomFa = "لکه‌های آب‌سوخته و تیره با گسترش بسیار سریع به بافت‌مردگی که در رطوبت بالا با کپک سفید اسپورزا در زیر برگ همراه است.",
            actionableAdvice = "Urgent: Apply systemic oomycete-targeted fungicides (Metalaxyl-M / Ridomil Gold, Cymoxanil); destroy cull piles immediately.",
            actionableAdviceFa = "اقدام فوری: محلول‌پاشی قارچ‌کش‌های سیستمیک نفوذی (ریدومیل گلد/متالاکسیل-ام یا سیموکسانیل)؛ حذف و امحای فوری بوته‌های آلوده."
        ),
        DiseaseInfo(
            id = 10,
            rawKey = "Potato___healthy",
            commonName = "Healthy Potato Foliage",
            commonNameFa = "برگ سالم سیب‌زمینی",
            latinTaxonomy = "Solanum tuberosum",
            hostPlant = "Solanum tuberosum (Potato)",
            hostPlantFa = "بوته سیب‌زمینی (Solanum tuberosum)",
            isHealthy = true,
            primarySymptom = "Clean vibrant green compound leaflets, intact margins, robust apical growth, active photosynthetic mesophyll tissue.",
            primarySymptomFa = "برگچه‌های مرکب شاداب و سرسبز، لبه‌های سالم، رشد فعال جوانه انتهایی و بدون هرگونه بافت‌مردگی یا لکه بیماری.",
            actionableAdvice = "Optimal vegetative vigor. Maintain routine hilling, balanced nitrogen:potassium ratio, and preventive scouting.",
            actionableAdviceFa = "رشد رویشی بهینه و عالی؛ عدم نیاز به سموم قارچ‌کش؛ حفظ مدیریت آبیاری قطره‌ای و خاک‌دهی مناسب پای بوته‌ها."
        )
    )

    fun buildDiagnosis(
        probabilities: FloatArray,
        confidence: Float,
        latencyMs: Float,
        foliageScore: Float = 1.0f,
        isTooDark: Boolean = false
    ): DiagnosisResult {
        var topIdx = 0
        var topProb = probabilities[0]
        for (i in probabilities.indices) {
            if (probabilities[i] > topProb) {
                topProb = probabilities[i]
                topIdx = i
            }
        }
        val disease = NOVEL_DISEASES.getOrElse(topIdx) { NOVEL_DISEASES[0] }
        val isFoliage = foliageScore >= 0.12f && !isTooDark
        val effectiveConfidence = if (isFoliage && !isTooDark) confidence else 0f
        return DiagnosisResult(
            diseaseInfo = disease,
            probability = topProb,
            confidence = effectiveConfidence,
            latencyMs = latencyMs,
            allProbabilities = probabilities,
            foliageScore = foliageScore,
            isFoliage = isFoliage,
            isTooDark = isTooDark
        )
    }
}
