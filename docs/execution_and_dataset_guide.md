# راهنمای جامع راه‌اندازی، دانلود دیتاست و اجرای فنی پایپلاین
### (Execution, Dataset Engineering & Technical Troubleshooting Guide)

> **هدف این سند:**  
> این سند راهنمای عملیاتی و اجرایی صفر تا صد پروژه **BioDINO-Edge** است. تمامی مراحل دانلود دیتاست، ساختار کَش هوشمند، نصب وابستگی‌های نرم‌افزاری، اجرای اسکریپت پایتون و ژوپیتر نوت‌بوک، تنظیم هایپرپارامترها و نحوه رفع تمامی خطاهای احتمالی سیستمی در این راهنما به طور شفاف تشریح شده است.

---

## ۱. آشنایی با دیتاست و نحوه دانلود در صورت نیاز (Dataset Engineering)

پروژه بر پایه دیتاست بین‌المللی **PlantVillage** بنا شده است که استاندارد طلایی پاتولوژی گیاهی در جامعه بین‌المللی بینایی ماشین است.

### ساختار پوشه‌های دیتاست در پروژه:
مسیر محلی دیتاست در مخزن:
```text
research-few-shot/
└── plantvillage/
    └── plantvillage dataset/
        └── color/
            ├── Apple___Apple_scab/             (630 تصویر)
            ├── Apple___Black_rot/              (621 تصویر)
            ├── Apple___Cedar_apple_rust/       (275 تصویر)
            ├── Apple___healthy/                (1,645 تصویر)
            ├── Grape___Black_rot/              (1,180 تصویر)
            ├── Grape___Esca_(Black_Measles)/   (1,383 تصویر)
            ├── Grape___Leaf_blight/            (1,076 تصویر)
            ├── Grape___healthy/                (423 تصویر)
            ├── Potato___Early_blight/          (1,000 تصویر)
            ├── Potato___Late_blight/           (1,000 تصویر)
            ├── Potato___healthy/               (152 تصویر)
            └── ... (۲۷ کلاس پایه دیگر از گوجه‌فرنگی، فلفل، ذرت و ...)
```

* **کل تصاویر دیتاست:** ۵۴,۳۰۵ تصویر با پس‌زمینه رنگی استاندارد.
* **کلاس‌های پایه (Base Classes):** ۳۰ کلاس گیاهی متفرقه برای پیش‌آموزش و استخراج متریک‌های عمومی.
* **کلاس‌های دیده‌نشده (Novel Classes):** ۱۱ کلاس استراتژیک سیب، انگور و سیب‌زمینی با مجموع **۹,۳۳۰ تصویر آزمون**.

### اگر دیتاست را روی سیستم جدیدی دانلود می‌کنید:
1. **روش اول: دانلود خودکار از طریق Kaggle CLI:**
```powershell
pip install kaggle
kaggle datasets download -d emmarex/plantdisease
tar -xf plantdisease.zip -C plantvillage/
```
2. **روش دوم: دانلود مستقیم از مخزن باز دانشگاهی:**
می‌توانید نسخه رسمی را مستقیماً از [پایگاه داده Dataverse دانشگاه Penn State](https://dataverse.harvard.edu/) دریافت فرمایید.

---

## ۲. مکانیسم کَش هوشمند بردارها (`cache_artifacts/`)

یکی از بزرگ‌ترین مزیت‌های این پروژه که ساعت‌ها در زمان داوران و پژوهشگران صرفه‌جویی می‌کند، **مکانیزم کَش بردارها (Offline Embedding Cache)** است.

* **فایل کَش:** [`cache_artifacts/pv_novel_embeddings.pt`](file:///e:/work/research-few-shot/cache_artifacts/pv_novel_embeddings.pt) (حجم: ۲۷.۸ مگابایت).
* **محتوا:** بردار ویژگی‌های استخراج‌شده تمام ۹,۳۳۰ تصویر آزمون برای هر دو مدل DINOv2 (۳۸۴ بعد) و BioCLIP (۵۱۲ بعد) به همراه برچسب‌های متناظر.
* **مزیت شگفت‌انگیز سرعت:**  
  * **بدون کَش:** استخراج ویژگی‌های ۹,۳۳۰ تصویر با پردازش سنگین GPU نیازمند حدود **۳۰ تا ۴۵ ثانیه** زمان است.
  * **با کَش:** اجرای پایپلاین و آزمون آماری ۳۰ اپیزودی در **کسری از ثانیه (< ۱ ثانیه)** اجرا و بازتولید می‌شود!

### اگر بخواهید کَش را دوباره از صفر بسازید:
کافی است فایل کَش را حذف یا تغییر نام دهید:
```powershell
Remove-Item cache_artifacts\pv_novel_embeddings.pt
```
پایپلاین پایتون به صورت کاملاً خودکار متوجه عدم وجود فایل شده، تصاویر خام را از پوشه `plantvillage/` لود کرده و با استخراج مجدد ویژگی‌ها با DINOv2 و BioCLIP، فایل کَش جدید را ایجاد و ذخیره می‌نماید.

---

## ۳. مراحل راه‌اندازی گام‌به‌گام محیط اجرایی (Environment Setup)

### گام ۱: باز کردن ترمینال PowerShell در ریشه پروژه
```powershell
cd E:\work\research-few-shot
```

### گام ۲: ایجاد و فعال‌سازی محیط مجازی ایزوله پایتون
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
*(اگر در ویندوز با خطای `Execution_Policies` مواجه شدید، دستور `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` را یک‌بار اجرا کنید).*

### گام ۳: نصب بسته‌های نرم‌افزاری لازم
فایل [`requirements.txt`](file:///e:/work/research-few-shot/requirements.txt) شامل نگارش‌های هماهنگ با PyTorch و شتاب‌دهنده CUDA است:
```powershell
.\.venv\Scripts\pip.exe install -r requirements.txt
```

---

## ۴. اجرای پایپلاین کامل و بازتولید نتایج (Dynamic CLI)

کد اصلی پایپلاین ([`biodino_edge_pipeline.py`](file:///e:/work/research-few-shot/biodino_edge_pipeline.py)) کاملاً داینامیک، ماژولار و مجهز به آرگومان‌های خط فرمان (`argparse`) است:

### الف) اجرای بنچمارک استاندارد PlantVillage (۱۱ کلاس آزمایشگاهی):
```powershell
.\.venv\Scripts\python.exe -u biodino_edge_pipeline.py --dataset plantvillage
```
* **خروجی:** ارزیابی DINOv2 و BioCLIP، تحلیل تفکیک فیشر (دقت استقرایی **۹۷.۹۵٪** و قله فراالقایی **۹۸.۶۷٪**)، و آزمون آماری ۳۰ اپیزودی مونت‌کارلو با فواصل اطمینان ۹۵٪ آماری (**۹۷.۴۱٪ $\pm$ ۰.۷۱٪**).

### ب) اجرای بنچمارک در شرایط واقعی مزرعه PlantDoc (۲۷ کلاس طبیعی):
```powershell
.\.venv\Scripts\python.exe -u biodino_edge_pipeline.py --dataset plantdoc --k_shot 5
```
* **خروجی:** ارزیابی ۲۷ کلاس واقعی در شرایط نویز مزرعه و پس‌زمینه‌های طبیعی، دستیابی به میانگین **۸۳.۸۴٪ $\pm$ ۱۱.۵۵٪** (با سقف بازه ۹۵٪ CI تا **۸۷.۳۸٪** و پیک **۱۰۰.۰٪**) در بنچمارک استاندارد ۵ کلاسه (شکست دادن مدل VSF با ۷۰.۶۱٪) و **۵۶.۳۵٪** (پیک ۵۸.۷۳٪) در آزمون تنش ۲۷ کلاسه.

### ج) اجرای همزمان هر دو بنچمارک و چاپ جدول مقایسه‌ای:
```powershell
.\.venv\Scripts\python.exe -u biodino_edge_pipeline.py --dataset both
```
* **خروجی:** اجرای خودکار روی هر دو دیتاست، محاسبه شاخص‌ها، چاپ جدول مقایسه‌ای جامع درون‌ترمینالی و ذخیره در [`biodino_edge_results.json`](file:///e:/work/research-few-shot/biodino_edge_results.json).

### د) اجرای پروفایلینگ تاخیر کوانتیزاسیون INT8 روی CPU:
```powershell
.\.venv\Scripts\python.exe -u biodino_edge_pipeline.py --dataset plantvillage --profile_latency
```
* **خروجی:** استخراج تاخیر مسیر سریع DINOv2 (**۲۱.۱۲ میلی‌ثانیه** (۴۷.۴ FPS)) و مسیر عمیق BioCLIP با توان عملیاتی بالای ۴۰ FPS روی پردازنده لبه.

### ب) اجرای تعاملی در نوت‌بوک ژوپیتر (Interactive Visualizations):
فایل **`biodino_edge_pipeline.ipynb`** را در VS Code یا مرورگر باز کنید. سلول‌ها به صورت متوالی اجرا می‌شوند و نمودارهای زیر را ترسیم می‌کنند:
* ماتریس درهم‌ریختگی با تفکیک رنگی کلاسی (Confusion Matrix).
* نمودار توزیع اطمینان گیت عدم قطعیت شانون.
* هیستوگرام تغییرات دقت در ۳۰ اپیزود ارزیابی.

---

## ۵. جدول تنظیم هایپرپارامترهای کلیدی و ساختار ماژولار (Hyperparameter Reference & Clean Architecture)

در نسخه بهینه‌سازی‌شده و تمیز پایپلاین (`biodino_edge_pipeline.py`)، تمام هایپرپارامترها درون دیتاکلاس متمرکز [`BioDINOConfig`](file:///e:/work/research-few-shot/biodino_edge_pipeline.py#L52) کپسوله‌سازی شده‌اند و پرامپت‌های گیاه‌شناسی در ماژول مجزای [`taxonomic_prompts.py`](file:///e:/work/research-few-shot/taxonomic_prompts.py) نگهداری می‌شوند:

| فیلد در `BioDINOConfig` | مقدار پیش‌فرض | نقش و عملکرد در مدل |
| :--- | :---: | :--- |
| `tau_conf` | `0.35` | آستانه تصمیم‌گیری گیت مارجین-آنتروپی شانون ($\tau_{\text{conf}}$)؛ فریم‌های با اطمینان بالاتر مستقیماً از مسیر سریع DINOv2 در کمتر از ۲۲ میلی‌ثانیه رد می‌شوند. |
| `lda_ensemble_weight` | `0.75` | وزن فیشر در انسمبل خطی نهایی ($0.75 \times \text{LDA} + 0.25 \times \text{Text}$). |
| `text_fusion_weight` | `0.20` | وزن پرامپت متنی در پروتوتایپ تلفیقی BioCLIP ($0.80 \times \text{Vis} + 0.20 \times \text{Text}$). |
| `base_ensemble_weight` | `0.65` | ضریب تلفیق لاجیت پایه ($0.65 \times \text{BioCLIP} + 0.35 \times \text{DINOv2}$). |
| `logit_scale` | `20.0` | ضریب اسکیل کسینوسی لاجیت‌ها قبل از Softmax. |
| `k_shot` | `5` | تعداد نمونه‌های پشتیبان به ازای هر کلاس در سناریوی Few-Shot. |
| `support_views` | `8` | تعداد نماهای افزوده (۱ تصویر اصلی + ۷ آگمنتیشن چندنما) به ازای هر نمونه ساپورت. |
| `batch_size` | `128` | اندازه دسته‌های استنتاج کوئری برای بالاترین بهره‌وری حافظه GPU/CPU. |

> [!NOTE]
> **تفکیک ماژولار پرامپت‌ها (`taxonomic_prompts.py`):** پرامپت‌های زیستی ۱۱ کلاس PlantVillage و ۲۷ کلاس PlantDoc اکنون در فایلی مجزا قرار دارند تا تغییر یا اضافه کردن توصیف پاتولوژی نیازی به دستکاری در کدهای پردازشی پایپلاین نداشته باشد. همچنین نسخه مونولیتیک اولیه ۹۹۴ خطی در [`biodino_edge_pipeline_legacy.py`](file:///e:/work/research-few-shot/biodino_edge_pipeline_legacy.py) به عنوان پشتیبان محفوظ مانده است.

---

## ۶. جدول رفع خطاهای احتمالی (Troubleshooting FAQ)

| خطای مشاهده‌شده | دلیل فنی | راهکار حل قطعی |
| :--- | :--- | :--- |
| `CUDA out of memory` | حافظه کارت گرافیک برای لود همزمان مدل‌ها کم است. | در خط بارگذاری مدل، آرگومان `device = "cpu"` را تنظیم کنید؛ کل الگوریتم فیشر روی CPU در کسری از ثانیه اجرا می‌شود. |
| `FileNotFoundError: plantvillage` | مسیر تصاویر خام تغییر کرده یا در حال اجرای بدون کَش هستید. | اطمینان حاصل کنید پوشه `plantvillage` در ریشه قرار دارد یا از فایل کَش `cache_artifacts/pv_novel_embeddings.pt` استفاده کنید. |
| `ImportError: open_clip` | پکیج BioCLIP به درستی نصب نشده است. | دستور `pip install open_clip_torch timm` را در محیط `.venv` اجرا فرمایید. |
| خطای فونت در رسم نمودارها | پکیج فونت‌های ماتپلات‌لیب فارسی فعال نیست. | نوت‌بوک به طور خودکار از کدهای اسکی لاتین برای برچسب‌ها استفاده می‌کند تا در تمام سیستم‌عامل‌ها بدون تداخل رندر شود. |
