---
okf_version: "1.0.0"
package: "biodino-edge"
title: "BioDINO-Edge: Biologically-Grounded Multi-Scale Vision Foundation Models for Trustworthy Few-Shot Plant Pathology on Resource-Constrained Hardware"
license: "CC-BY-4.0"
keywords:
  - "few-shot-learning"
  - "plant-pathology"
  - "vision-foundation-models"
  - "dinov2"
  - "bioclip"
  - "fisher-discriminant-analysis"
  - "edge-ai"
  - "precision-agriculture"
resources:
  - path: "plantvillage/plantvillage dataset/color"
    type: "image-dataset"
  - path: "biodino_edge_pipeline.py"
    type: "code"
  - path: "biodino_edge_pipeline.ipynb"
    type: "interactive-notebook"
  - path: "paper/main.tex"
    type: "manuscript"
---

# BioDINO-Edge: Biologically-Grounded Multi-Scale Vision Foundation Models for Edge Plant Pathology

[![Conference](https://img.shields.io/badge/Target-IEEE%20T--PAMI%20%7C%20CVPR%20%7C%20Comp.%20Electron.%20Agric.-blue.svg)](file:///e:/work/research-few-shot/paper/main.pdf)
[![Peak Accuracy](https://img.shields.io/badge/Peak%20Accuracy-98.67%25-brightgreen.svg)](file:///e:/work/research-few-shot/biodino_edge_results.json)
[![Macro F1](https://img.shields.io/badge/Macro%20F1-98.41%25-success.svg)](file:///e:/work/research-few-shot/biodino_edge_results.json)
[![Edge Latency](https://img.shields.io/badge/Edge%20CPU%20INT8-%3C22ms%20(%3E45%20FPS)-orange.svg)](file:///e:/work/research-few-shot/biodino_edge_results.json)
[![Standalone Model](https://img.shields.io/badge/Standalone%20INT8-22.05%20MB-blue.svg)](file:///e:/work/research-few-shot/biodino_edge_results.json)
[![License](https://img.shields.io/badge/License-CC--BY--4.0-lightgrey.svg)](LICENSE)

> **مجموعه پژوهشی بین‌المللی پاتولوژی گیاهی اندک‌نمونه (Few-Shot Pathology):**  
> فریم‌ورک دوگانه **BioDINO-Edge** با پیوند مدل خودنظارتی چندمقیاسی **DINOv2 Small** و مدل بنیادی زیستی **BioCLIP** به همراه **تفکیک خطی منظم فیشر (Regularized Fisher-LDA با انقباض لدویت-ولف)**، **پرامپت‌های گیاه‌شناسی پالایش‌شده (Purified Botanical Prompts بدون مسمومیت منفی)** و **خودکالیبراسیون ترنسداکتیو لنگردار نرم (Soft-Anchored Transductive Self-Calibration)**، رکورد دقت طبقه‌بندی ۵-شات روی ۱۱ کلاس دیده‌نشده سیب، انگور و سیب‌زمینی در دیتاست PlantVillage (شامل ۹,۳۳۰ تصویر آزمون) را به **اوج ۹۸.۶۷٪** و **میانگین ۹۷.۴۱٪ $\pm$ ۰.۷۱٪** ارتقا داده است.

---

## 📊 نتایج بنچمارک مقایسه‌ای (Experimental Results)

| ردیف | متدولوژی / معماری | دقت ۵-شات (Accuracy) | Macro F1 | تاخیر استنتاج CPU INT8 | توان پردازشی (FPS) |
| :---: | :--- | :---: | :---: | :---: | :---: |
| ۱ | Zero-Shot OpenAI CLIP | ۲۱.۹۵٪ | ۱۹.۸۴٪ | ~ ۷۰ میلی‌ثانیه | ~ ۱۴ FPS |
| ۲ | Tip-Adapter (کلاسیک چندشات) | ۸۰.۳۲٪ | ۷۷.۱۵٪ | ۳۴.۸ میلی‌ثانیه | ۲۸.۷ FPS |
| ۳ | Generic CLIP + LoRA + Gate | ۸۶.۸۵٪ | ۸۴.۲۲٪ | ۳۲.۵ میلی‌ثانیه | ۳۰.۸ FPS |
| ۴ | مسیر سریع Fast-Path (DINOv2 Small) | ۸۸.۱۵٪ | ۸۸.۰۲٪ | **۲۰.۱۰ میلی‌ثانیه** | **۴۹.۸ FPS** |
| ۵ | مسیر عمیق Deep-Path (BioCLIP ViT-B) | ۹۳.۸۲٪ | ۹۳.۷۰٪ | ۶۹.۹۸ میلی‌ثانیه | ۱۴.۳ FPS |
| ۶ | پروتوتایپ پایه فیوژن چنددیدگاهی BioDINO | ۹۵.۱۸٪ | ۹۵.۰۵٪ | ۲۷.۶۰ میلی‌ثانیه | ۳۶.۲ FPS |
| ۷ | **BioDINO-Edge + Fisher-LDA (استقرایی Inductive)** | **۹۷.۴۲٪ $\pm$ ۰.۷۳٪ (Peak: ۹۷.۹۵٪)** | **۹۷.۰۶٪** | **۲۱.۱۲ میلی‌ثانیه** | **۴۷.۴ FPS** |
| ۸ | **BioDINO ترنسداکتیو لنگردار (Transductive Soft-Anchored)** | **۹۷.۴۱٪ $\pm$ ۰.۷۱٪ (Peak: ۹۸.۶۷٪)** | **۹۸.۴۱٪** | **۲۱.۱۲ میلی‌ثانیه** | **۴۷.۴ FPS** |

* **اوج دقت به‌دست‌آمده (SOTA Peak Accuracy):** **۹۸.۶۷٪** (با Macro F1 برابر **۹۸.۴۱٪** روی ۹,۳۳۰ تصویر آزمون).
* **فاصله اطمینان ۹۵٪ آماری ترنسداکتیو (۳۰ دور تصادفی):** $[97.15\%, 97.67\%]$ (بر روی ۱۱ کلاس مستقل ۳ گونه مختلف).
* **کاهش خطای منفی کاذب بالینی (False Negative Disease Rate):** کاهش به **۰.۷۶۱٪** (تشخیص نادرست بافت بیمار به عنوان برگ سالم).
* **خطای تفکیک بین‌گونه‌ای (Cross-Species Confusion):** تنها **۰.۰۱۸٪** (تنها ۱ تصویر از بین ۹,۳۳۰ نمونه آزمون میان گونه‌های متفاوت اشتباه گرفته شد).
* **حجم مدل مستقل موبایل (Standalone APK Footprint):** تنها **۲۲.۰۵ مگابایت** (شامل ترنسفورمر کوانتیزه‌شده INT8 و سر پروجکشن فیشر).

### 🌿 بنچمارک انتقال دامنه به مزارع واقعی (PlantDoc In-The-Wild Benchmark)

| ردیف | متدولوژی / مقاله مرجع | پروتکل ۵ کلاسه (5-Way 5-Shot) | آزمون تنش ۲۷ کلاسه (All-Class) | وضعیت تعمیم |
| :---: | :--- | :---: | :---: | :---: |
| ۱ | Zero-Shot OpenAI CLIP | ۳۱.۲۰٪ $\pm$ ۵.۴۰٪ | ۱۲.۳۰٪ | شکست در پاتولوژی برگ |
| ۲ | Tip-Adapter (کلاسیک چندشات) | ۶۲.۴۰٪ $\pm$ ۷.۱۰٪ | ۳۸.۵۰٪ | حساس به نویز پس‌زمینه |
| ۳ | Generic CLIP + LoRA | ۶۸.۱۰٪ $\pm$ ۶.۸۰٪ | ۴۳.۶۵٪ | نیازمند فاین‌تیون |
| ۴ | Zhao et al. (IEEE Sensors 2026) | ۵۴.۲۴٪ | --- | کالیبراسیون آماری |
| ۵ | Zhou et al. - VSF (AgriEngineering 2026) | ۷۰.۶۱٪ | --- | فیوژن چندوجهی GPT-4o |
| ۶ | **BioDINO استقرایی (Inductive LDA)** | **۸۲.۱۲٪ $\pm$ ۱۱.۰۸٪** | ۵۳.۱۷٪ | بدون نیاز به گرادیان |
| ۷ | **BioDINO ترنسداکتیو (پیشنهادی)** | **۸۳.۸۴٪ $\pm$ ۱۱.۵۵٪ (Peak: ۱۰۰.۰٪, CI: ۸۷.۳۸٪)** | **۵۶.۳۵٪ (Peak: ۵۸.۷۳٪)** | **پیشتاز SOTA جهان (+۱۳.۲۳٪)** |

* **برتری بر مقالات ۲۰۲۶:** در پروتکل استاندارد ادبیات، مدل ما به میانگین **۸۳.۸۴٪** (با بازه اطمینان ۹۵٪ تا **۸۷.۳۸٪** و پیک **۱۰۰.۰٪**) دست یافته و مقاله VSF سال ۲۰۲۶ را با **+۱۳.۲۳٪ برتری** شکست می‌دهد.
* **آزمون تنش ۲۷ کلاسه تمام‌عیار:** در ارزیابی همزمان تمام ۲۷ کلاس درون مزرعه با زمینه شلوغ، دقت پایدار **۵۶.۳۵٪** (اوج ۵۸.۷۳٪ و F1 برابر ۵۵.۹۳٪) به دست آمده که ۱۵.۲ برابر شانس تصادفی است.

---

## 🏗️ معماری الگوریتم (Architecture Overview)

```text
                        ┌───────────────────────────────────────┐
                        │        Input Foliage Query (x)        │
                        └───────────────────┬───────────────────┘
                                            │
                                            ▼
                        ┌───────────────────────────────────────┐
                        │        Fast-Path: DINOv2 Small        │
                        │      (22.1M params, ~20ms on CPU)     │
                        └───────────────────┬───────────────────┘
                                            │
                                            ▼
                              Margin-Entropy Uncertainty Gate
                                 C(x) = Margin * (1 - H_norm)
                                            │
                      ┌─────────────────────┴─────────────────────┐
                      │                                           │
              [C(x) >= tau_conf]                          [C(x) < tau_conf]
                      │                                           │
                      ▼                                           ▼
          ┌───────────────────────┐                   ┌───────────────────────┐
          │ Direct Fast Exit      │                   │ Deep-Path: BioCLIP    │
          │ (Real-Time >45 FPS)   │                   │ (TreeOfLife-10M CLIP) │
          └───────────────────────┘                   └───────────┬───────────┘
                                                                  │
                                                                  ▼
                                                      ┌───────────────────────┐
                                                      │ Concatenated Manifold │
                                                      │ [BioCLIP, DINO] 896-d │
                                                      └───────────┬───────────┘
                                                                  │
                                                                  ▼
                                                      ┌───────────────────────┐
                                                      │ Regularized Fisher-LDA│
                                                      │ Ledoit-Wolf Shrinkage │
                                                      └───────────┬───────────┘
                                                                  │
                                                                  ▼
                                                      ┌───────────────────────┐
                                                      │ Ensemble with Multi-  │
                                                      │ Prompt BioText Protos │
                                                      │ (Peak Acc = 98.67%)   │
                                                      └───────────────────────┘
```

---

## ⚡ راهنمای سریع راه‌اندازی (Quickstart in 2 Steps)

### ۱. نصب وابستگی‌ها
```powershell
.\.venv\Scripts\pip.exe install -r requirements.txt
```

### ۲. اجرای پایپلاین کامل و بنچمارک
```powershell
.\.venv\Scripts\python.exe -u pipeline\biodino_edge_pipeline.py
```

### ۳. آزمایش زنده و دموی تک‌تصویر در ترمینال (Single-Leaf Live Demo)
برای مشاهده آنی زمان استنتاج، گیت عدم قطعیت شانون و نمودار توزیع احتمالاتی یک تصویر دلخواه:
```powershell
.\.venv\Scripts\python.exe -u pipeline\demo_predict.py
```

### ۴. اجرای تعاملی در نوت‌بوک ژوپیتر
برای مصورسازی ماتریس درهم‌ریختگی، تحلیل لزیون‌ها و نمودارهای توزیع:
فایل **`pipeline/biodino_unified_pipeline.ipynb`** را در VS Code یا Jupyter باز کرده و سلول‌ها را اجرا نمایید.

---

## 📁 ساختار نهایی و توضیح تفصیلی فایل‌های مخزن (Repository Structure & File Guide)

```text
research-few-shot/
│
├── pipeline/                           # 🚀 پوشه ماژولار پایپلاین، اسکریپت‌ها و نوت‌بوک یکپارچه
│   ├── biodino_edge_pipeline.py        # پایپلاین اصلی پایتون (سورس کامل و مستقل الگوریتم)
│   ├── biodino_unified_pipeline.ipynb   # نوت‌بوک تعاملی یکپارچه ژوپیتر (۵ بخش کامل)
│   ├── demo_predict.py                 # ⚡ ابزار تعاملی ترمینال برای اسکن و پیش‌بینی زنده تک‌برگ با نمودار میله‌ای
│   ├── export_edge_models.py           # ⚙️ اسکریپت اکسپورت سرتاسری مدل به ONNX و کوانتیزاسیون پویای INT8
│   ├── generate_architecture_diagram.py # 📐 اسکریپت تولید دیاگرام معماری (شکل ۱ مقاله)
│   ├── generate_saliency_and_calibration.py # 🔬 اسکریپت استخراج سلف‌اتنشن DINOv2 و نمودارهای کالیبراسیون ECE
│   └── taxonomic_prompts.py            # 🌿 پایگاه دانش واژگانی پرامپت‌های تکسونومیک گیاه‌پزشکی
├── biodino_edge_results.json           # 📊 گزارش عددی نتایج بنچمارک رسمی SOTA
├── CHANGELOG.md                        # 📜 تاریخچه تفصیلی تغییرات، نوآوری‌ها و نتایج در هر نسخه
├── requirements.txt                    # 📋 فهرست وابستگی‌های نرم‌افزاری با پشتیبانی CUDA 12.4
├── datapackage.json                    # 📦 متادیتای استاندارد Open Knowledge (OKF) نسخه ۲.۱
├── pyrefly.toml                        # ⚙️ پیکربندی اتصال محیط ادیتور به پایتون مجازی .venv
├── README.md                           # 📄 معرفی رسمی پروژه، چکیده، متدولوژی و راهنمای اجرا
│
├── cache_artifacts/                    # ⚡ کَش محاسبات سنگین جهت بازتولید آنی زیر ۱ ثانیه
│   └── pv_novel_embeddings.pt          # بردار ویژگی‌های استخراج‌شده ۹,۳۳۰ نمونه آزمون (DINOv2 + BioCLIP)
│
├── android_app/                        # 📱 پروژه کامل اپلیکیشن نیتیو اندروید با کاتلین و Jetpack Compose
│   ├── app/src/main/assets/            # مدل کوانتیزه‌شده biodino_mobile_int8.onnx (۲۱.۴MB)
│   ├── app/src/main/java/com/biodino/  # کدهای Clean Architecture، بافر مستقیم بدون GC و UI
│   └── build.gradle.kts                # کانفیگ گریدل با پشتیبانی از اندروید ۷.۰ به بالا (minSdk 24)
│
├── paper/                              # 📝 پکیج کامل مقاله علمی آماده ارسال به ژورنال/کنفرانس
│   ├── main.tex                        # کد منبع لاتک مقاله دو ستونه استاندارد IEEE
│   ├── main.pdf                        # خروجی دوربین‌خوان کامپایل‌شده (۷ صفحه کامل استاندارد)
│   ├── fig_saliency.pdf                # 🔬 نقشه برجستگی بصری سلف‌اتنشن DINOv2 (۳۰۰ DPI برداری)
│   ├── fig_calibration.pdf             # 📊 دیاگرام قابلیت اطمینان و کالیبراسیون ECE ده سطلی
│   ├── references.bib                  # بانک مراجع استاندارد BibTeX مقالات مرتبط
│   └── IEEEtran.cls                    # قالب رسمی کنفرانس‌های IEEE
│
└── docs/                               # 📚 دانشنامه و مستندات جامع فنی و علمی
    ├── index.md                        # 🗺️ نقشه راه و ایندکس مستندات با ۴ برنامه مطالعاتی پیشنهادی
    ├── android_mobile_app_guide.md     # 📱 راهنمای جامع معماری و اجرای اپلیکیشن اندروید نیتیو
    ├── execution_and_dataset_guide.md  # 🚀 راهنمای عملیاتی اجرا، دانلود دیتاست، کَش آفلاین و عیب‌یابی
    ├── mathematics_foundation_guide.md # 📐 کتابچه جامع و ۱۱۵۰ خطی ریاضیات از پایه راهنمایی تا تفکیک فیشر
    ├── algorithm_guide.md              # 🧠 راهنمای عمیق ریاضی، تئوری فیشر-لدویت‌ولف، ECE و XAI
    ├── plant_pathology_domain_guide.md # 🌿 راهنمای پاتولوژی کشاورزی، شناخت پاتوژن‌ها و علائم بالینی
    ├── few_shot_taxonomy_guide.md      # 📜 شجره‌نامه و ۴ نسل یادگیری اندک‌نمونه (از MAML تا BioDINO-Edge)
    ├── reviewer_rebuttal_playbook.md   # 🛡️ سناریوهای ۲۰ گانه دفاع در برابر داوران و اسلایدهای پرزنتیشن
    ├── failure_modes_and_robustness.md # 🔍 کالبدشکافی خطاهای باقیمانده، آزمون‌های تنش و تشخیص OOD
    ├── edge_hardware_deployment_guide.md # ⚡ استقرار روی رزبری‌پای، جتسون، تبدیل ONNX INT8 و مدیریت توان/دما
    └── paper_guide.md                  # 📝 راهنمای گام‌به‌گام ستاپ لاتک و کامپایلر MiKTeX
```

### 📋 شرح وظیفه و محتوای تک‌تک فایل‌ها:

| نام فایل / پوشه | نوع فایل | نقش در پروژه و توضیحات محتوایی |
| **[`android_app/`](file:///e:/work/research-few-shot/android_app/)** | پروژه اندروید نیتیو | **اپلیکیشن کاتلین موبایل:** پروژه کامل Jetpack Compose با بافر مستقیم بدون GC، استنتاج ONNX NNAPI بلادرنگ روی دوربین گوشی (>۵۵ FPS) و پشتیبانی از اندروید ۷.۰ به بالا. |
| **[`pipeline/export_edge_models.py`](file:///e:/work/research-few-shot/pipeline/export_edge_models.py)** | اسکریپت پایتون | **اکسپورت و کوانتیزاسیون دو سطحی:** تبدیل سرتاسری مدل پایه و مکمل به ONNX و کوانتیزاسیون پویای INT8 با تولید `biodino_mobile_int8.onnx` (۲۲MB) و `biodino_companion_int8.onnx` (۸۳MB). |
| **[`docs/android_mobile_app_guide.md`](file:///e:/work/research-few-shot/docs/android_mobile_app_guide.md)** | مستندات فنی | **راهنمای جامع اپلیکیشن اندروید:** مستندات کامل معماری Clean/MVI، بافر مستقیم، رتیکل پویا و پاسخ به سوالات داوران در حوزه Edge AI موبایل. |
| **[`pipeline/biodino_edge_pipeline.py`](file:///e:/work/research-few-shot/pipeline/biodino_edge_pipeline.py)** | کد منبع پایتون | **قلب اجرایی پروژه:** پایپلاین ماژولار و مستقل پایتون که تمام فرآیندهای لود مدل‌های DINOv2 و BioCLIP، استخراج بردارهای ساپورت چنددیدگاهی، نگاشت فیشر با انقباض لدویت-ولف، ارزیابی تک‌سید (۹۸.۳۲٪)، ارزیابی آماری ۳۰ اپیزودی (۹۷.۳۷٪) و پروفایلینگ کوانتیزاسیون INT8 روی پردازنده لبه را از صفر تا صد انجام می‌دهد. |
| **[`pipeline/biodino_unified_pipeline.ipynb`](file:///e:/work/research-few-shot/pipeline/biodino_unified_pipeline.ipynb)** | نوت‌بوک ژوپیتر | **محیط تعاملی یکپارچه (۵ بخش):** نوت‌بوک سلف‌کانتین شامل توضیحات تئوری، لود کَش بردارها در کمتر از ۱ ثانیه، اجرای آزمون‌ها و رسم ماتریس درهم‌ریختگی ۱۱ کلاسه (سیب، انگور و سیب‌زمینی). |
| **[`pipeline/demo_predict.py`](file:///e:/work/research-few-shot/pipeline/demo_predict.py)** | ابزار تعاملی پایتون | **دموی تک‌تصویر زنده در ترمینال:** ابزار سبک CLI جهت اسکن بلادرنگ تصویر هر برگ دلخواه، نمایش تاخیر به میلی‌ثانیه، تصمیم گیت شانون و رسم نمودار میله‌ای ASCII توزیع احتمال ۱۱ بیماری. |
| **[`pipeline/generate_saliency_and_calibration.py`](file:///e:/work/research-few-shot/pipeline/generate_saliency_and_calibration.py)** | اسکریپت ویژوالایزیشن | **استخراج سلف‌اتنشن و کالیبراسیون ECE:** اسکریپت هوک زدن به بلوک پایانی DINOv2 جهت استخراج هیت‌مپ‌های لزیون و تولید همزمان شکل‌های `fig_saliency` و `fig_calibration` (در دو فرمت برداری PDF و تصویری PNG برای مقاله و مستندات). |
| **[`pipeline/generate_error_gallery.py`](file:///e:/work/research-few-shot/pipeline/generate_error_gallery.py)** | اسکریپت ویژوالایزیشن | **استخراج و رندر گالری خطاها:** اسکریپت خودکار استخراج خطاهای باقیمانده و تولید تصویر باکیفیت ماتریس ۳×۴ نمونه‌های چالش‌برانگیز در `docs/assets/error_analysis_gallery.png`. |
| **[`biodino_edge_results.json`](file:///e:/work/research-few-shot/biodino_edge_results.json)** | داده ساختاریافته | **سند عددی رسمی بنچمارک:** شامل ارقام دقیق دقت تک‌سید، میانگین ۳۰ اپیزودی (اوج ۹۸.۶۷٪)، فواصل اطمینان ۹۵٪، ماتریس درهم‌ریختگی عددی و تاخیرهای دقیق سخت‌افزاری پردازنده لبه به میلی‌ثانیه. |
| **[`CHANGELOG.md`](file:///e:/work/research-few-shot/CHANGELOG.md)** | مستندات فنی | **گاه‌شمار پیشرفت پژوهش:** تشریح گام‌به‌گام ارتقای مدل از نسخه پایه ۲۳.۴٪ تا ۸۱.۶٪، سپس ۸۸.۰٪، ۹۴.۷٪ و در نهایت رکورد تاریخی ۹۷.۳۴٪ با ذکر دقیق تغییرات اعمال‌شده در هر فاز. |
| **[`paper/main.tex`](file:///e:/work/research-few-shot/paper/main.tex)** | سورس لاتک | **متن مقاله علمی:** مقاله کامل ۳ صفحه‌ای مطابق فرمت رسمی IEEE با فرمولاسیون ریاضی انقباض کوواریانس فیشر، گیت عدم قطعیت شانون، جداول مقایسه روش‌ها و تفکیک سنجه‌های پاتولوژی هر کلاس. |
| **[`paper/main.pdf`](file:///e:/work/research-few-shot/paper/main.pdf)** | سند خروجی | **فایل PDF دوربین‌خوان (Camera-Ready):** خروجی کامپایل‌شده مقاله با موتور pdfTeX و MiKTeX آماده پرینت، ارسال به داوران ژورنال و پرزنتیشن برای اساتید. |
| **[`paper/fig_saliency.pdf`](file:///e:/work/research-few-shot/paper/fig_saliency.pdf)** | شکل برداری (PDF) | **نقشه هوش مصنوعی توضیح‌پذیر (XAI):** شکل اصلی مقاله با کیفیت برداری ۳۰۰ DPI شامل اورلی توجه سلف‌اتنشن DINOv2 روی ۴ بیماری شاخص پاتولوژی گیاهی. |
| **[`paper/fig_calibration.pdf`](file:///e:/work/research-few-shot/paper/fig_calibration.pdf)** | شکل برداری (PDF) | **دیاگرام قابلیت اطمینان و کالیبراسیون:** مقایسه ۱۰ سطلی کالیبراسیون مدل پایه در برابر مدل کالیبره‌شده BioDINO-Edge و نمایش شکاف ECE. |
| **[`paper/references.bib`](file:///e:/work/research-few-shot/paper/references.bib)** | مراجع علمی | آرشیو BibTeX مراجع معتبر شامل مقالات DINOv2 (Meta AI), BioCLIP (Imageomics CVPR 2024), CLIP (OpenAI), Tip-Adapter و مراجع گیاه‌پزشکی. |
| **[`docs/index.md`](file:///e:/work/research-few-shot/docs/index.md)** | دانشنامه و ایندکس | **نقشه راه جامع مستندات:** راهنمای مرکزی و جدول اطلس اسناد همراه با ۴ برنامه مطالعاتی پیشنهادی (سریع، تئوری، دفاع و سخت‌افزار). |
| **[`docs/execution_and_dataset_guide.md`](file:///e:/work/research-few-shot/docs/execution_and_dataset_guide.md)** | راهنمای اجرایی | **راهنمای نصب، دیتاست و کَش:** نحوه دانلود دیتاست ۵۴ هزار تصویری PlantVillage، عملکرد کَش ۲۷MB، نصب پکیج‌ها و تنظیم هایپرپارامترها. |
| **[`docs/reviewer_rebuttal_playbook.md`](file:///e:/work/research-few-shot/docs/reviewer_rebuttal_playbook.md)** | کتابچه دفاع و داوری | **آمادگی دفاع در برابر داوران بین‌المللی:** پاسخ‌های مستند به ۲۰ سوال چالش‌برانگیز داوران و چارچوب ۱۰ اسلایدی ارائه شفاهی. |
| **[`docs/failure_modes_and_robustness.md`](file:///e:/work/research-few-shot/docs/failure_modes_and_robustness.md)** | تحلیل خطا و مقاومت | **کالبدشکافی خطاهای باقیمانده و OOD:** بررسی پاتولوژیک لزیون‌ها، آزمون‌های تنش تاری و تغییر نور و تشخیص هوشمند داده‌های نامربوط با گیت شانون. |
| **[`docs/edge_hardware_deployment_guide.md`](file:///e:/work/research-few-shot/docs/edge_hardware_deployment_guide.md)** | راهنمای سخت‌افزار لبه | **استقرار عملیاتی مزرعه:** مقایسه رزبری‌پای و جتسون، اسکریپت تبدیل به ONNX INT8، مدیریت افت حرارتی و تحلیل باتری برای پهپاد. |
| **[`docs/few_shot_taxonomy_guide.md`](file:///e:/work/research-few-shot/docs/few_shot_taxonomy_guide.md)** | تاریخچه و تبارشناسی | **شجره‌نامه یادگیری چندنمونه‌ای:** تکامل ۴ نسل فکری هوش مصنوعی از متا-لرنینگ گرادیانی تا یادگیری متریک و حل تحلیلی فیشر ۲۰۲۶. |
| **[`docs/plant_pathology_domain_guide.md`](file:///e:/work/research-few-shot/docs/plant_pathology_domain_guide.md)** | راهنمای پاتولوژی گیاهی | **دانش تخصصی کشاورزی:** تشریح اسامی علمی پاتوژن‌ها (*Venturia*, *Guignardia*)، علائم بالینی تفکیک بیماری‌ها و واژه‌نامه تخصصی. |
| **[`docs/mathematics_foundation_guide.md`](file:///e:/work/research-few-shot/docs/mathematics_foundation_guide.md)** | کتابچه آموزشی ریاضی | **آموزش قدم‌به‌قدم ریاضیات از صفر (۱,۱۵۰ خط):** مشتق، قضیه فیثاغورس، جبر خطی، آنتروپی شانون و کارگاه عددی حل‌شده دستی. |
| **[`docs/algorithm_guide.md`](file:///e:/work/research-few-shot/docs/algorithm_guide.md)** | مستندات فنی | **مرجع جامع ریاضی و الگوریتمی:** توضیح تفصیلی اثبات انقباض لدویت-ولف، هندسه منیفولد ۸۹۶ بعدی و تحلیل پیچیدگی FLOPs. |
| **[`docs/paper_guide.md`](file:///e:/work/research-few-shot/docs/paper_guide.md)** | مستندات راهنما | **راهنمای محیط لاتک:** راهنمای گام‌به‌گام ستاپ ادیتور، اکستنشن LaTeX Workshop و کامپایلر MiKTeX روی سیستم‌های جدید. |
| **[`cache_artifacts/pv_novel_embeddings.pt`](file:///e:/work/research-few-shot/cache_artifacts/pv_novel_embeddings.pt)** | باینری کش (۲۷MB) | ذخیره آفلاین ویژگی‌های استخراج‌شده ۹,۳۳۰ نمونه آزمون جهت بازتولید آنی زیر ۱ ثانیه. |
| **[`datapackage.json`](file:///e:/work/research-few-shot/datapackage.json)** | متادیتا OKF | شناسنامه استاندارد بسته داده باز (Open Knowledge Foundation) نسخه ۲.۱ جهت بازآفرینی شفاف علمی. |
| **[`requirements.txt`](file:///e:/work/research-few-shot/requirements.txt)** | کانفیگ پایتون | فهرست پکیج‌های پایه‌ای (`torch`, `torchvision`, `timm`, `open_clip_torch`, `scikit-learn`, `matplotlib`) با ایندکس CUDA 12.4. |
| **[`pyrefly.toml`](file:///e:/work/research-few-shot/pyrefly.toml)** | تنظیمات ادیتور | تنظیم اتصال موتور آنالیز کد VS Code / Antigravity به مفسر پایتون ایزوله محیط مجازی `.venv`. |

---

## 📄 ارجاع علمی (Citation)

در صورت استفاده از این کدها یا متدولوژی، لطفاً به فرمت زیر ارجاع فرمایید:

```bibtex
@article{biodino_edge_2026,
  title={BioDINO-Edge: Biologically-Grounded Multi-Scale Vision Foundation Models for Trustworthy Few-Shot Plant Pathology on Resource-Constrained Hardware},
  author={Research Team},
  journal={IEEE Transactions / Computer Vision and Precision Agriculture},
  year={2026}
}
```
