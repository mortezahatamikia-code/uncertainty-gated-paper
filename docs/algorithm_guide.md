# راهنمای جامع معماری، مبانی تئوریک و پیاده‌سازی فریم‌ورک BioDINO-Edge

این مستندات به عنوان **مرجع جامع فنی، ریاضی و عملیاتی** پروژه BioDINO-Edge تدوین شده است و تمامی جزئیات نظری، فرمولاسیون ریاضی، اثبات‌های هندسی، مکانیزم‌های سخت‌افزاری لبه و مراحل اجرای گام‌به‌گام را با بالاترین دقت علمی تشریح می‌کند.

---

## ۱. تبیین مسئله و انگیزه پژوهشی (Problem Formulation)

### الف) تعریف مسئله یادگیری اندک‌نمونه پاتولوژی گیاهی (Few-Shot Pathology)
در پاتولوژی هوشمند مزارع، هدف شناسایی گونه و نوع بیماری گیاه بر اساس تعداد بسیار محدودی نمونه تصویر آموزشی ($K=5$ شات) از کلاس‌های دیده‌نشده ($\mathcal{Y}_{\text{novel}}$) است.
مجموعه داده‌ها شامل دو زیرمجموعه متنافی است:
$$\mathcal{Y}_{\text{base}} \cap \mathcal{Y}_{\text{novel}} = \emptyset$$
در طول مرحله آزمون (Inference/Evaluation)، مدل با ۸ کلاس کاملاً دیده‌نشده بیماری و سلامت روی دو سرده مهم باغی (سیب `Malus domestica` و انگور `Vitis vinifera`) در قالب **۷,۱۹۳ تصویر آزمون** از دیتاست استاندارد PlantVillage ارزیابی می‌شود:
1. `Apple___Apple_scab` (اسکب سیب ناشی از قارچ *Venturia inaequalis*)
2. `Apple___Black_rot` (پوسیدگی سیاه / لکه چشم‌قورباغه‌ای سیب ناشی از *Botryosphaeria obtusa*)
3. `Apple___Cedar_apple_rust` (زنگ سیب ناشی از قارچ *Gymnosporangium juniperi-virginianae*)
4. `Apple___healthy` (برگ کاملاً سالم سیب)
5. `Grape___Black_rot` (پوسیدگی سیاه انگور ناشی از قارچ *Guignardia bidwellii*)
6. `Grape___Esca_(Black_Measles)` (عارضه پیچیده اسکا / سیاهول انگور ناشی از کمپلکس قارچی *Phaeomoniella*)
7. `Grape___Leaf_blight_(Isariopsis_Leaf_Spot)` (بلایت برگ انگور ناشی از *Pseudocercospora vitis*)
8. `Grape___healthy` (برگ کاملاً سالم انگور)

### ب) چالش‌های سه‌گانه و چرایی شکست روش‌های قبلی
1. **شکست مدل‌های بنیادی عمومی (Generic VLM Representation Collapse):**  
   مدل‌های بینایی-زبانی متداول مانند OpenAI CLIP روی داده‌های اینترنتی چندمیلیاردی از اشیاء ماکروسکوپیک (خودرو، حیوانات خانگی، ساختمان‌ها) آموزش دیده‌اند. این مدل‌ها به دلیل فقدان درک میکروسکوپی و بیولوژیکی، در تفکیک الگوهای ظریف کلروز (زردی)، بافت‌های نکروز (سوختگی) و اسپورهای قارچی دچار اشتباهات فاحش می‌شوند (به عنوان مثال، حساسیت مدل پایه CLIP روی اسکب سیب تنها ۵۶.۰٪ با نرخ خطای منفی کاذب ۴۴٪ بود).
2. **معضل تداخل درون‌گونه‌ای نکروزهای مشابه (Intra-Species Phenotypic Overlap):**  
   در روش‌های سنتی چندشات، بیش از ۶۰٪ کل خطاهای طبقه‌بندی صرفاً ناشی از تداخل ظاهری دو بیماری انگور (`Grape Black rot` و `Grape Esca`) با یکدیگر بود؛ زیرا هر دو لکه‌های قهوه‌ای تیره نکروتیک روی برگ ایجاد می‌کنند و میانگین‌گیری کلی تصویر (Global Average Pooling) امضای محلی لزیون را محو می‌کند.
3. **تنگناهای سخت‌افزاری پردازنده‌های لبه (Edge Computing Bottleneck):**  
   ربات‌های سم‌پاش هوشمند و پهپادهای گشت‌زنی مزرعه از پردازنده‌های کم‌مصرف تعبیه‌شده (ARM / Embedded CPU) با حافظه محدود (کمتر از ۲ گیگابایت) و باتری محدود بهره می‌برند. اجرای مدل‌های سنگین چندمیلیارد پارامتری یا ترنسفورمرهای بزرگ روی لبه از نظر تاخیر زمانی (Latency) و مصرف توان غیرممکن است.

---

## ۲. معماری شناختی دوگانه BioDINO-Edge

فریم‌ورک **BioDINO-Edge** با الهام از تئوری پردازش دوگانه شناختی (Dual-Process Cognitive Theory) طراحی شده است:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           تصویر برگ ورودی Query (x)                         │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│         مسیر سریع Fast-Path: DINOv2 Small (vit_small_patch14_dinov2)        │
│          ۲۲.۱ میلیون پارامتر | تاخیر روی CPU INT8: ۲۰.۱۰ میلی‌ثانیه         │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                 گیت عدم‌قطعیت مارجین-آنتروپی شانون (Uncertainty Gate)        │
│                C(x) = (p_(1) - p_(2)) * (1.0 - H_norm(x))                   │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
                 ┌─────────────────────┴─────────────────────┐
                 │                                           │
         [C(x) >= tau_conf]                          [C(x) < tau_conf]
                 │                                           │
                 ▼                                           ▼
┌─────────────────────────────────┐         ┌─────────────────────────────────┐
│       خروج سریع Fast-Exit       │         │    مسیر عمیق زیستی Deep-Path:   │
│     (دقت ۸۹.۰٪ در ۲۰ میلی‌ثانیه) │         │     BioCLIP ViT-B/16 (TreeOfLife)│
│       توان پردازشی > ۴۵ FPS     │         │    استخراج بردار ۵۱۲ بعدی زیستی │
└─────────────────────────────────┘         └────────────────┬────────────────┘
                                                             │
                                                             ▼
                                            ┌─────────────────────────────────┐
                                            │      الحاق در منیفولد مشترک     │
                                            │ z = [f_bio (512), f_dino (384)] │
                                            │        ابعاد کل: ۸۹۶ بعد         │
                                            └────────────────┬────────────────┘
                                                             │
                                                             ▼
                                            ┌─────────────────────────────────┐
                                            │  نگاشت تفکیک خطی منظم فیشر     │
                                            │ Regularized Fisher-LDA (LW-Cov) │
                                            │     حذف نویز رویشی پس‌زمینه      │
                                            └────────────────┬────────────────┘
                                                             │
                                                             ▼
                                            ┌─────────────────────────────────┐
                                            │ تلفیق با چندپرامپتی تکسونومیک   │
                                            │ 0.75 * P_fisher + 0.25 * P_text │
                                            │    (دقت قله تجربی: ۹۷.۳۴٪)      │
                                            └─────────────────────────────────┘
```

### ۱. مسیر سریع Fast-Path (DINOv2 Small):
* **مدل:** `vit_small_patch14_dinov2` با ۲۲.۱ میلیون پارامتر.
* **مکانیزم یادگیری:** خودنظارتی بدون برچسب (Self-Supervised DINO) روی ۱۴۲ میلیون تصویر طبیعی.
* **ویژگی متمایز:** پچ‌های ۱۶×۱۶ این مدل به دلیل اتصالات سلف‌اتنشن، حاشیه‌های لزیون‌های بافت گیاهی و کانون‌های تغییر رنگ را با دقت هندسی فوق‌العاده‌ای برجسته می‌کنند.
* **بردار ویژگی:** $\mathbf{f}_{\text{dino}} \in \mathbb{R}^{384}$ با نرمال‌سازی اقلیدسی ($\ell_2$-normalization).

### ۲. مسیر عمیق Deep-Path (BioCLIP ViT-B/16):
* **مدل:** `hf-hub:imageomics/bioclip` (معماری ViT-B/16 با ۸۶.۶ میلیون پارامتر).
* **داده‌های پیش‌آموزش:** مجموعه عظیم ۱۰ میلیون نمونه بیولوژیکی از درخت حیات (`TreeOfLife-10M`).
* **ویژگی متمایز:** این مدل روابط فیلوژنتیک، تکسونومی ارگانیسم‌ها، ساختارهای قارچی (*Pycnidia*, *Conidia*) و ویژگی‌های میکروسکوپی آلودگی برگ را به خوبی درک می‌کند.
* **بردار ویژگی:** $\mathbf{f}_{\text{bio}} \in \mathbb{R}^{512}$ با نرمال‌سازی اقلیدسی.

---

## ۳. فرمولاسیون چندپرامپتی تکسونومیک بیولوژیکی

به جای استفاده از پرامپت‌های ساده و کلیشه‌ای، برای هر کلاس بیماری یک دیکشنری چندگانه ($M=3$) از عبارات غنی گیاه‌پزشکی تدوین شد:

```python
TAXONOMIC_PROMPTS = {
    "Apple___Apple_scab": [
        "A botanical photograph of Apple (Malus domestica) foliage with olive-green velvety lesions caused by Venturia inaequalis.",
        "Apple scab leaf symptom showing dark circular olive-black scabby fungal spots on leaf surface.",
        "Malus leaf infected with Venturia scab fungal lesions with irregular margins."
    ],
    "Apple___Black_rot": [
        "Apple foliage showing Black rot frogeye leaf spots with purple margins and concentric zones caused by Botryosphaeria obtusa.",
        "Circular brown necrotic lesions with dark border on Malus domestica leaf.",
        "Frogeye leaf spot on apple leaf blade with distinct tan center."
    ],
    "Apple___Cedar_apple_rust": [
        "Apple leaf exhibiting bright yellow-orange circular rust spots with fungal aecia caused by Gymnosporangium juniperi-virginianae.",
        "Bright orange-yellow cedar apple rust lesions on upper leaf surface of Malus domestica.",
        "Characteristic yellow chlorotic rust spots with small dark pycnia dots on apple leaf."
    ],
    "Apple___healthy": [
        "A botanical photo of healthy vigorous foliage of Apple (Malus domestica) showing clean green leaves with no lesions.",
        "Healthy vibrant apple leaf blade completely devoid of fungal spots, necrosis, or chlorosis.",
        "Flawless disease-free green foliage of Malus domestica fruit tree."
    ],
    "Grape___Black_rot": [
        "Grape (Vitis vinifera) foliage showing Black rot reddish-brown circular necrotic spots with minute black pycnidia caused by Guignardia bidwellii.",
        "Circular necrotic spots with dark margins and tiny black specks of fungal fruiting bodies on grape leaf.",
        "Guignardia black rot leaf spot on grape showing distinct circular boundaries and dead brown center."
    ],
    "Grape___Esca_(Black_Measles)": [
        "Grape leaf showing Esca complex Black Measles with interveinal chlorosis and necrosis creating a distinct tiger-stripe pattern.",
        "Tiger-stripe foliar symptoms on Vitis vinifera with yellow and necrotic bands between green veins caused by Phaeomoniella chlamydospora.",
        "Severe interveinal scorching and tiger-striping on grape foliage with green tissue bordering veins."
    ],
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": [
        "Grape leaf exhibiting Isariopsis leaf blight showing irregular angular dark brown foliar lesions caused by Pseudocercospora vitis.",
        "Angular brown necrotic leaf spots bounded by leaf veinlets on Vitis vinifera foliage.",
        "Dark brown irregular angular foliar blight lesions on grape leaf."
    ],
    "Grape___healthy": [
        "A botanical photo of healthy vigorous foliage of Grape (Vitis vinifera) showing smooth green leaves without pathogens.",
        "Healthy vibrant green grape leaf blade without necrotic spots, tiger stripes, or chlorosis.",
        "Completely healthy disease-free foliage of Vitis vinifera vine."
    ]
}
```

### فرمول سنتز پروتوتایپ چندوجهی:
انکودر متن BioCLIP ($\phi_{\text{bio}}$) بردارهای متنی پرامپت‌ها را استخراج کرده و میانگین آن‌ها پروتوتایپ متنی را می‌سازد:
$$\mathbf{P}_{\text{text}}^{(c)} = \text{Normalize}\left(\frac{1}{M}\sum_{m=1}^M \phi_{\text{bio}}(T_c^{(m)})\right)$$
سپس پروتوتایپ بصری چنددیدگاهی حاصل از ۸ تصویر افزوده (Augmented Views) با پروتوتایپ متنی تلفیق می‌شود:
$$\mathbf{P}_{\text{bio}}^{(c)} = \text{Normalize}\left(0.80 \cdot \mathbf{P}_{\text{bio, vis}}^{(c)} + 0.20 \cdot \mathbf{P}_{\text{text}}^{(c)}\right)$$

---

## ۴. تئوری ریاضی تفکیک خطی منظم فیشر با انقباض لدویت-ولف

### الف) نقص اساسی روش‌های سنتی (پروتوتایپ کسینوسی)
در روش‌های Prototypical Networks یا Tip-Adapter، شباهت نمونه با کلاس $c$ صرفاً با ضرب داخلی کسینوسی سنجیده می‌شود:
$$s_c = \langle \mathbf{z}, \boldsymbol{\mu}_c \rangle$$
این معادله به صورت پنهان فرض می‌کند که توزیع ویژگی‌های نمونه‌ها درون هر کلاس کروی، همسانگرد و با ماتریس کوواریانس همانی ($\mathbf{\Sigma} = \mathbf{I}$) است.  
اما در تصاویر واقعی برگ، **واریانس رویشی پس‌زمینه (سبزی کلروفیل، نورپردازی خورشید، زاویه رگبرگ‌ها) چندین برابر بزرگ‌تر از واریانس لکه چند میلی‌متری بیماری است.** در نتیجه، جهت‌های اصلی تغییرات بردار ویژگی، ناشی از برگ است نه بیماری!

### ب) فرمولاسیون فیشر در ابعاد بالا ($d = 896$)
با الحاق ویژگی‌های دو مدل، بردار منیفولد مشترک به ابعاد ۸۹۶ می‌رسد:
$$\mathbf{z} = [\mathbf{f}_{\text{bio}}, \mathbf{f}_{\text{dino}}] \in \mathbb{R}^{896}$$
ماتریس پراکندگی درون‌کلاسی (Within-Class Scatter Matrix) روی نمونه‌های ساپورت $\mathcal{S}_c$ به صورت زیر تعریف می‌شود:
$$\mathbf{S}_W = \sum_{c=1}^C \sum_{\mathbf{x} \in \mathcal{S}_c} (\mathbf{x} - \boldsymbol{\mu}_c)(\mathbf{x} - \boldsymbol{\mu}_c)^T$$
**چالش تکینگی (Singularity Problem):**  
در سناریوی ۵-شات روی ۸ کلاس، تعداد کل بردارهای ساپورت ۴۰ نمونه است (یا ۳۲۰ نمونه در صورت آگمنتاسیون ۸-دیدگاهی). از آنجا که بعد فضا ($d = 896$) بسیار بزرگ‌تر از تعداد نمونه‌ها است ($d > n$)، ماتریس $\mathbf{S}_W$ به‌شدت کم‌رتبه (Singular) و غیرقابل معکوس‌سازی است و دترمینان آن صفر می‌شود ($\det(\mathbf{S}_W) = 0$).

### ج) انقباض تحلیلی لدویت-ولف (Ledoit-Wolf Shrinkage)
برای حل قطعی تکینگی در ابعاد بالا، ماتریس کوواریانس به سمت یک ماتریس همانی ساختاریافته منقبض (Shrunk) می‌شود:
$$\hat{\mathbf{\Sigma}} = (1 - \rho)\mathbf{S}_W + \rho \nu \mathbf{I}_{896}$$
که در آن:
$$\nu = \frac{1}{d}\text{Tr}(\mathbf{S}_W)$$
ضریب انقباض بهینه $\rho \in (0, 1)$ به صورت کاملاً تحلیلی و بدون نیاز به حدس تجربی یا اعتبارسنجی متقاطع سنگین بر اساس کمینه‌سازی خطای میانگین مربعات فروبنیوس (Frobenius Loss) محاسبه می‌شود:
$$\rho^* = \arg\min_\rho \mathbb{E}\left[\|\hat{\mathbf{\Sigma}} - \mathbf{\Sigma}_{\text{true}}\|_F^2\right] = \frac{\sum_{i=1}^n \|\mathbf{z}_i \mathbf{z}_i^T - \mathbf{S}_W\|_F^2}{n^2 \left[\text{Tr}(\mathbf{S}_W^2) - \frac{1}{d}\text{Tr}^2(\mathbf{S}_W)\right]}$$

### د) معادله تفکیک و کاهش خطای لکه سیاه/اسکا
ماتریس وزن طبقه‌بند فیشر به صورت ضرب کوواریانس منظم‌شده در تفاضل میانگین‌ها به دست می‌آید:
$$\mathbf{W}_c = \hat{\mathbf{\Sigma}}^{-1} \boldsymbol{\mu}_c, \quad b_c = -\frac{1}{2} \boldsymbol{\mu}_c^T \hat{\mathbf{\Sigma}}^{-1} \boldsymbol{\mu}_c + \log \pi_c$$
* اثر هندسی: ضرب ماتریسی در $\hat{\mathbf{\Sigma}}^{-1}$ فضا را در جهات واریانس مشترک برگ فشرده (De-correlate) می‌کند و جهت‌هایی که امضای میکروسکوپی بیماری را دارند تقویت می‌نماید.
* **نتیجه تجربی:** خطاهای تداخل تشخیصی بین `Grape Black rot` و `Grape Esca` از ۲۴۲ به ۱۱۹ خطا (کاهش بیش از ۵۰٪) تقلیل یافت و دقت مدل به **۹۷.۳۴٪** جهش کرد.

---

## ۵. گیت عدم‌قطعیت مارجین-آنتروپی شانون (Adaptive Edge Routing)

برای استقرار بلادرنگ روی پردازنده‌های کم‌مصرف، مدل DINOv2 ابتدا توزیع احتمالاتی اولیه را محاسبه می‌کند:
$$\mathbf{z}_{\text{dino}} = \gamma_{\text{dino}} (\mathbf{f}_{\text{dino}} \mathbf{P}_{\text{dino}}^T), \quad \mathbf{p} = \text{softmax}(\mathbf{z}_{\text{dino}})$$

گیت عدم‌قطعیت، دو کمیت کلیدی را ترکیب می‌کند:
1. **آنتروپی نرمالیزه‌شده شانون (Normalized Shannon Entropy):**
   $$\mathcal{H}_{\text{norm}}(\mathbf{x}) = -\frac{1}{\log C} \sum_{c=1}^C p_c \log(p_c + \epsilon)$$
   مقدار آن بین ۰ (اطمینان مطلق) تا ۱ (عدم‌قطعیت و سردرگمی کامل) نرمال می‌شود.
2. **مارجین حاشیه احتمالاتی (Top-Margin Confidence):**
   $$\mathcal{M}(\mathbf{x}) = p_{(1)} - p_{(2)}$$
   اختلاف بین بالاترین احتمال ($p_{(1)}$) و دومین کاندیدای برتر ($p_{(2)}$).

امتیاز اطمینان ترکیبی به صورت زیر تعریف می‌شود:
$$\mathcal{C}(\mathbf{x}) = \mathcal{M}(\mathbf{x}) \cdot \left(1.0 - \mathcal{H}_{\text{norm}}(\mathbf{x})\right)_+$$

### قانون تصمیم‌گیری گیت لبه:
$$\text{Path}(\mathbf{x}) = \begin{cases} 
\text{Fast-Exit (DINOv2 Solo)}, & \text{if } \mathcal{C}(\mathbf{x}) \ge \tau_{\text{conf}} \quad (\tau_{\text{conf}} = 0.35) \\
\text{Deep-Path (BioCLIP + Fisher)}, & \text{if } \mathcal{C}(\mathbf{x}) < \tau_{\text{conf}}
\end{cases}$$
* در تصاویر واضح و بدون ابهام، نمونه در مسیر سریع ۲۰ میلی‌ثانیه‌ای خاتمه می‌یابد.
* تنها در موارد با ابهام ساختاری یا بیماری‌های هم‌پوشان، مسیر عمیق فعال می‌شود.

---

## ۶. تحلیل پیچیدگی پردازشی و بنچمارک استنتاج لبه (Edge Profiling)

| مرحله پردازشی | تعداد عملیات ریاضی (FLOPs) | حجم حافظه RAM | تاخیر روی CPU INT8 | نرخ فریم (FPS) |
| :--- | :---: | :---: | :---: | :---: |
| **مسیر سریع (DINOv2 Small INT8)** | ۴.۳ میلیارد | ۲۲.۱ مگابایت | **۲۰.۱۰ میلی‌ثانیه** | **۴۹.۸ FPS** |
| **مسیر عمیق (BioCLIP ViT-B INT8)** | ۱۷.۶ میلیارد | ۸۸.۵ مگابایت | ۶۹.۹۸ میلی‌ثانیه | ۱۴.۳ FPS |
| **طبقه‌بند فیشر روی بردار ۸۹۶ بعدی** | **۷,۱۶۸ عملیات** | **کمتر از ۱۰ کیلوبایت** | **۰.۰۰۲ میلی‌ثانیه** | **> ۱۰,۰۰۰ FPS** |
| **پایپلاین تطبیقی کسکید BioDINO-Edge** | میانگین ۵.۶ میلیارد | ۱۱۰.۶ مگابایت | **۲۴.۸۰ میلی‌ثانیه** | **> ۴۰.۰ FPS** |

* فیت کردن اولیه ماتریس فیشر روی نمونه‌های ساپورت تنها **۵۰ میلی‌ثانیه** (یک‌بار در زمان روشن شدن سیستم) زمان می‌برد.
* اعمال طبقه‌بند فیشر در زمان استنتاج، صرفاً یک ضرب ماتریسی سبک $\mathbf{z} \mathbf{W}^T + \mathbf{b}$ است که هیچ بار پردازشی ملموسی به لبه تحمیل نمی‌کند.

---

## ۷. پروتکل ارزیابی آماری ۳۰ اپیزودی (Statistical Rigor Benchmark)

برای پاسخ به داوران ژورنال‌ها و اثبات عدم وابستگی مدل به یک بذر تصادفی خاص، سیستم تحت آزمون مونت‌کارلو با ۳۰ اپیزود کاملاً مجزا قرار گرفت:

```python
# ارزیابی مونت‌کارلو ۳۰ اپیزود تصادفی
for ep in range(30):
    rng = random.Random(42 + ep * 17)
    # انتخاب تصادفی ۵ برگ جدید به ازای هر کلاس
    # فیت مجدد ماتریس فیشر و ارزیابی روی مابقی تصاویر
```

### نتایج آماری استخراج‌شده:
* **میانگین دقت (Mean Accuracy):** **۹۴.۹۵٪ $\pm$ ۱.۴۲٪**
* **بیشترین دقت ثبت‌شده (Peak Accuracy):** **۹۷.۴۴٪**
* **میانگین Macro F1:** **۹۵.۱۵٪ $\pm$ ۱.۱۹٪**
* **فاصله اطمینان ۹۵٪ آماری (95% CI):** **$[94.44\%, 95.46\%]$**
* **نرخ منفی کاذب برگ‌های بیمار (تشخیص به عنوان سالم):** **۰.۶۸٪**
* **خطای تفکیک بین‌گونه‌ای (سیب و انگور):** **۰.۰۰٪**

---

## ۸. راهنمای گام‌به‌گام اجرای کدها

### ۱. اجرای اسکریپت پایتون
```powershell
.\.venv\Scripts\python.exe -u biodino_edge_pipeline.py
```
این اسکریپت مدل‌ها را فراخوانی کرده، بردارهای ساپورت را استخراج می‌کند، طبقه‌بند فیشر را فیت می‌نماید و ارزیابی تک‌سید و چنداپیزودی را روی ۷,۱۹۳ تصویر آزمون انجام داده و خروجی را در `biodino_edge_results.json` ذخیره می‌کند.

### ۲. اجرای نوت‌بوک تعاملی ژوپیتر
فایل `biodino_edge_pipeline.ipynb` را در VS Code یا مرورگر باز کنید. سلول‌ها به ترتیب موارد زیر را اجرا می‌کنند:
1. بارگذاری کَش ویژگی‌های ۷,۱۹۳ تصویر (`pv_novel_embeddings.pt`).
2. اجرای الگوریتم فیشر-لدویت‌ولف در کمتر از ۱ ثانیه.
3. رسم ماتریس درهم‌ریختگی به صورت هیت‌مپ رنگی با مات‌پلات‌لیب.
4. مشاهده نمودارهای ارزیابی آماری ۳۰ اپیزودی.
