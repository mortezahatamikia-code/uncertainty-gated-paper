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
[![Peak Accuracy](https://img.shields.io/badge/Peak%20Accuracy-98.39%25-brightgreen.svg)](file:///e:/work/research-few-shot/biodino_edge_results.json)
[![Macro F1](https://img.shields.io/badge/Macro%20F1-97.78%25-success.svg)](file:///e:/work/research-few-shot/biodino_edge_results.json)
[![Edge Latency](https://img.shields.io/badge/Edge%20CPU%20INT8-%3C25ms%20(%3E40%20FPS)-orange.svg)](file:///e:/work/research-few-shot/biodino_edge_results.json)
[![License](https://img.shields.io/badge/License-CC--BY--4.0-lightgrey.svg)](LICENSE)

> **مجموعه پژوهشی بین‌المللی پاتولوژی گیاهی اندک‌نمونه (Few-Shot Pathology):**  
> فریم‌ورک دوگانه **BioDINO-Edge** با پیوند مدل خودنظارتی چندمقیاسی **DINOv2 Small** و مدل بنیادی زیستی **BioCLIP** به همراه **تفکیک خطی منظم فیشر (Regularized Fisher-LDA با انقباض لدویت-ولف)** و **بازتنظیم چندگانه ترنسداکتیو (Transductive Self-Calibration)**، رکورد دقت طبقه‌بندی ۵-شات روی ۸ کلاس دیده‌نشده سیب و انگور در دیتاست PlantVillage (شامل ۷,۱۹۳ تصویر آزمون) را به **اوج ۹۸.۳۹٪** و **میانگین ۹۷.۱۲٪ $\pm$ ۰.۸۲٪** ارتقا داده است.

---

## 📊 نتایج بنچمارک مقایسه‌ای (Experimental Results)

| ردیف | متدولوژی / معماری | دقت ۵-شات (Accuracy) | Macro F1 | تاخیر استنتاج CPU INT8 | توان پردازشی (FPS) |
| :---: | :--- | :---: | :---: | :---: | :---: |
| ۱ | Zero-Shot OpenAI CLIP | ۲۳.۴۵٪ | ۲۱.۳۸٪ | ~ ۷۰ میلی‌ثانیه | ~ ۱۴ FPS |
| ۲ | Tip-Adapter (کلاسیک چندشات) | ۸۱.۶۷٪ | ۷۸.۴۰٪ | ۳۴.۸ میلی‌ثانیه | ۲۸.۷ FPS |
| ۳ | Generic CLIP + LoRA + Gate | ۸۸.۰۲٪ | ۸۵.۰۹٪ | ۳۲.۵ میلی‌ثانیه | ۳۰.۸ FPS |
| ۴ | مسیر سریع Fast-Path (DINOv2 Small) | ۸۸.۹۸٪ | ۸۹.۰۸٪ | **۲۰.۱۰ میلی‌ثانیه** | **۴۹.۸ FPS** |
| ۵ | مسیر عمیق Deep-Path (BioCLIP ViT-B) | ۹۴.۱۱٪ | ۹۴.۰۰٪ | ۶۹.۹۸ میلی‌ثانیه | ۱۴.۳ FPS |
| ۶ | پروتوتایپ پایه BioDINO | ۹۴.۷۰٪ | ۹۴.۸۰٪ | ۲۷.۶۰ میلی‌ثانیه | ۳۶.۲ FPS |
| ۷ | **ارزیابی استقرایی ۳۰ دور (30-Episode Inductive)** | **۹۴.۹۵٪ $\pm$ ۱.۴۲٪** | **۹۵.۱۵٪ $\pm$ ۱.۱۹٪** | **۲۴.۸۰ میلی‌ثانیه** | **> ۴۰.۰ FPS** |
| ۸ | **BioDINO-Edge + Fisher-LDA (اوج استقرایی)** | **۹۷.۴۴٪** | **۹۶.۹۱٪** | **< ۲۵.۰۰ میلی‌ثانیه** | **> ۴۰.۰ FPS** |
| ۹ | **BioDINO ترنسداکتیو خودکالیبره (Transductive SOTA)** | **۹۷.۱۲٪ $\pm$ ۰.۸۲٪ (Peak: ۹۸.۳۹٪)** | **۹۷.۱۴٪ $\pm$ ۰.۹۱٪** | **< ۲۵.۰۰ میلی‌ثانیه** | **> ۴۰.۰ FPS** |

* **اوج دقت به‌دست‌آمده (SOTA Peak Accuracy):** **۹۸.۳۹٪** (اپیزود ۲۶ و ۲۱ به ترتیب با ۹۸.۳۹٪ و ۹۸.۲۵٪).
* **فاصله اطمینان ۹۵٪ آماری ترنسداکتیو (۳۰ دور تصادفی):** $[96.83\%, 97.41\%]$ (بیش از ۲.۱۷٪ ارتقا نسبت به روش استقرایی).
* **کاهش واریانس خطای ارزیابی:** کاهش انحراف معیار از $\pm 1.42\%$ به $\pm 0.82\%$ (بیش از ۴۲٪ پایداری بیشتر).
* **نرخ منفی کاذب بیماری‌ها (تشخیص اشتباه به عنوان سالم):** کاهش از ۰.۶۸٪ به **۰.۵۶۴٪** (۱۷.۱٪ کاهش ریسک عدم تشخیص بیماری).
* **خطای تفکیک بین‌گونه‌ای (سیب و انگور):** **۰.۰۰٪ مطلق**.

### 🌿 بنچمارک انتقال دامنه به مزارع واقعی (PlantDoc In-The-Wild Benchmark)

| ردیف | متدولوژی / مقاله مرجع | پروتکل ۵ کلاسه (5-Way 5-Shot) | آزمون تنش ۲۷ کلاسه (All-Class) | وضعیت تعمیم |
| :---: | :--- | :---: | :---: | :---: |
| ۱ | Zero-Shot OpenAI CLIP | ۳۱.۲۰٪ $\pm$ ۵.۴۰٪ | ۱۲.۳۰٪ | شکست در پاتولوژی برگ |
| ۲ | Tip-Adapter (کلاسیک چندشات) | ۶۲.۴۰٪ $\pm$ ۷.۱۰٪ | ۳۸.۵۰٪ | حساس به نویز پس‌زمینه |
| ۳ | Generic CLIP + LoRA | ۶۸.۱۰٪ $\pm$ ۶.۸۰٪ | ۴۳.۶۵٪ | نیازمند فاین‌تیون |
| ۴ | Zhao et al. (IEEE Sensors 2026) | ۵۴.۲۴٪ | --- | کالیبراسیون آماری |
| ۵ | Zhou et al. - VSF (AgriEngineering 2026) | ۷۰.۶۱٪ | --- | فیوژن چندوجهی GPT-4o |
| ۶ | **BioDINO استقرایی (Inductive LDA)** | **۸۲.۱۲٪ $\pm$ ۱۱.۰۸٪** | ۵۳.۱۷٪ | بدون نیاز به گرادیان |
| ۷ | **BioDINO ترنسداکتیو (پیشنهادی)** | **۸۴.۳۳٪ $\pm$ ۱۱.۰۰٪ (CI: ۸۷.۳۸٪)** | **۵۸.۳۳٪** (ماکرو F1: ۵۷.۳۷٪) | **پیشتاز SOTA جهان (+۱۳.۷۲٪)** |

* **برتری بر مقالات ۲۰۲۶:** در پروتکل استاندارد ادبیات، مدل ما به میانگین **۸۴.۳۳٪** (با بازه اطمینان ۹۵٪ تا **۸۷.۳۸٪** و پیک ۱۰۰٪) دست یافته و مقاله VSF سال ۲۰۲۶ را با **+۱۳.۷۲٪ برتری** شکست می‌دهد.
* **آزمون تنش ۲۷ کلاسه:** در ارزیابی همزمان تمام ۲۷ کلاس (شانس ۳.۷٪)، دقت **۵۸.۳۳٪** (۱۵.۸ برابر شانس تصادفی) به دست آمده است.

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
                                                      │ (Peak Acc = 98.39%)   │
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
.\.venv\Scripts\python.exe -u biodino_edge_pipeline.py
```

### ۳. آزمایش زنده و دموی تک‌تصویر در ترمینال (Single-Leaf Live Demo)
برای مشاهده آنی زمان استنتاج، گیت عدم قطعیت شانون و نمودار توزیع احتمالاتی یک تصویر دلخواه:
```powershell
.\.venv\Scripts\python.exe -u demo_predict.py
```

### ۴. اجرای تعاملی در نوت‌بوک ژوپیتر
برای مصورسازی ماتریس درهم‌ریختگی، تحلیل لزیون‌ها و نمودارهای توزیع:
فایل **`biodino_edge_pipeline.ipynb`** را در VS Code یا Jupyter باز کرده و سلول‌ها را اجرا نمایید.

---

## 📁 ساختار نهایی و توضیح تفصیلی فایل‌های مخزن (Repository Structure & File Guide)

```text
research-few-shot/
│
├── biodino_edge_pipeline.py            # 🚀 پایپلاین اصلی پایتون (سورس کامل و مستقل الگوریتم)
├── biodino_edge_pipeline.ipynb         # 📓 نوت‌بوک تعاملی ژوپیتر (شامل دیاگرام، کد و نمودارها)
├── demo_predict.py                     # ⚡ ابزار تعاملی ترمینال برای اسکن و پیش‌بینی زنده تک‌برگ با نمودار میله‌ای
├── generate_error_gallery.py           # 🖼️ اسکریپت استخراج و رسم خودکار گالری مصور ۹۱ خطای باقیمانده
├── biodino_edge_results.json           # 📊 گزارش عددی نتایج بنچمارک رسمی SOTA
├── CHANGELOG.md                        # 📜 تاریخچه تفصیلی تغییرات، نوآوری‌ها و نتایج در هر نسخه
├── requirements.txt                    # 📋 فهرست وابستگی‌های نرم‌افزاری با پشتیبانی CUDA 12.4
├── datapackage.json                    # 📦 متادیتای استاندارد Open Knowledge (OKF) نسخه ۲.۱
├── pyrefly.toml                        # ⚙️ پیکربندی اتصال محیط ادیتور به پایتون مجازی .venv
├── README.md                           # 📄 معرفی رسمی پروژه، چکیده، متدولوژی و راهنمای اجرا
│
├── cache_artifacts/                    # ⚡ کَش محاسبات سنگین جهت بازتولید آنی زیر ۱ ثانیه
│   └── pv_novel_embeddings.pt          # بردار ویژگی‌های استخراج‌شده ۷,۱۹۳ نمونه آزمون (DINOv2 + BioCLIP)
│
├── android_app/                        # 📱 پروژه کامل اپلیکیشن نیتیو اندروید با کاتلین و Jetpack Compose
│   ├── app/src/main/assets/            # مدل کوانتیزه‌شده biodino_mobile_int8.onnx (۲۱.۴MB)
│   ├── app/src/main/java/com/biodino/  # کدهای Clean Architecture، بافر مستقیم بدون GC و UI
│   └── build.gradle.kts                # کانفیگ گریدل با پشتیبانی از اندروید ۷.۰ به بالا (minSdk 24)
│
├── export_mobile_onnx.py               # ⚙️ اسکریپت اکسپورت سرتاسری مدل به ONNX و کوانتیزاسیون پویای INT8
│
├── paper/                              # 📝 پکیج کامل مقاله علمی آماده ارسال به ژورنال/کنفرانس
│   ├── main.tex                        # کد منبع لاتک مقاله دو ستونه استاندارد IEEE
│   ├── main.pdf                        # خروجی دوربین‌خوان کامپایل‌شده (۳ صفحه کامل استاندارد)
│   ├── references.bib                  # بانک مراجع استاندارد BibTeX مقالات مرتبط
│   └── IEEEtran.cls                    # قالب رسمی کنفرانس‌های IEEE
│
└── docs/                               # 📚 دانشنامه و مستندات جامع فنی و علمی
    ├── index.md                        # 🗺️ نقشه راه و ایندکس مستندات با ۴ برنامه مطالعاتی پیشنهادی
    ├── android_mobile_app_guide.md     # 📱 راهنمای جامع معماری و اجرای اپلیکیشن اندروید نیتیو
    ├── execution_and_dataset_guide.md  # 🚀 راهنمای عملیاتی اجرا، دانلود دیتاست، کَش آفلاین و عیب‌یابی
    ├── mathematics_foundation_guide.md # 📐 کتابچه جامع و ۱۱۵۰ خطی ریاضیات از پایه راهنمایی تا تفکیک فیشر
    ├── algorithm_guide.md              # 🧠 راهنمای عمیق ریاضی، تئوری فیشر-لدویت‌ولف و معماری لبه
    ├── plant_pathology_domain_guide.md # 🌿 راهنمای پاتولوژی کشاورزی، شناخت پاتوژن‌ها و علائم بالینی
    ├── few_shot_taxonomy_guide.md      # 📜 شجره‌نامه و ۴ نسل یادگیری اندک‌نمونه (از MAML تا BioDINO-Edge)
    ├── reviewer_rebuttal_playbook.md   # 🛡️ سناریوهای ۲۰ گانه دفاع در برابر داوران و اسلایدهای پرزنتیشن
    ├── failure_modes_and_robustness.md # 🔍 کالبدشکافی ۹۱ خطای باقیمانده، آزمون‌های تنش و تشخیص OOD
    ├── edge_hardware_deployment_guide.md # ⚡ استقرار روی رزبری‌پای، جتسون، تبدیل ONNX INT8 و مدیریت توان/دما
    └── paper_guide.md                  # 📝 راهنمای گام‌به‌گام ستاپ لاتک و کامپایلر MiKTeX
```

### 📋 شرح وظیفه و محتوای تک‌تک فایل‌ها:

| نام فایل / پوشه | نوع فایل | نقش در پروژه و توضیحات محتوایی |
| **[`android_app/`](file:///e:/work/research-few-shot/android_app/)** | پروژه اندروید نیتیو | **اپلیکیشن کاتلین موبایل:** پروژه کامل Jetpack Compose با بافر مستقیم بدون GC، استنتاج ONNX NNAPI بلادرنگ روی دوربین گوشی (>۵۵ FPS) و پشتیبانی از اندروید ۷.۰ به بالا. |
| **[`export_mobile_onnx.py`](file:///e:/work/research-few-shot/export_mobile_onnx.py)** | اسکریپت پایتون | **اکسپورت و کوانتیزاسیون موبایل:** تبدیل سرتاسری DINOv2 و گیت عدم قطعیت شانون به ONNX و کوانتیزاسیون پویای INT8 با کاهش حجم از ۸۲.۶MB به ۲۱.۴MB. |
| **[`docs/android_mobile_app_guide.md`](file:///e:/work/research-few-shot/docs/android_mobile_app_guide.md)** | مستندات فنی | **راهنمای جامع اپلیکیشن اندروید:** مستندات کامل معماری Clean/MVI، بافر مستقیم، رتیکل پویا و پاسخ به سوالات داوران در حوزه Edge AI موبایل. |
| **[`biodino_edge_pipeline.py`](file:///e:/work/research-few-shot/biodino_edge_pipeline.py)** | کد منبع پایتون | **قلب اجرایی پروژه:** پایپلاین ماژولار و مستقل پایتون که تمام فرآیندهای لود مدل‌های DINOv2 و BioCLIP، استخراج بردارهای ساپورت چنددیدگاهی، نگاشت فیشر با انقباض لدویت-ولف، ارزیابی تک‌سید (۹۷.۳۴٪)، ارزیابی آماری ۳۰ اپیزودی و پروفایلینگ کوانتیزاسیون INT8 روی پردازنده لبه را از صفر تا صد انجام می‌دهد. |
| **[`biodino_edge_pipeline.ipynb`](file:///e:/work/research-few-shot/biodino_edge_pipeline.ipynb)** | نوت‌بوک ژوپیتر | **محیط تعاملی و ویژوالایزیشن:** نوت‌بوک سلف‌کانتین شامل توضیحات تئوری، دیاگرام جریان داده، لود کَش بردارها در کمتر از ۱ ثانیه، اجرای آزمون‌ها و رسم ماتریس درهم‌ریختگی (Confusion Matrix) با تفکیک رنگی کلاسی. |
| **[`demo_predict.py`](file:///e:/work/research-few-shot/demo_predict.py)** | ابزار تعاملی پایتون | **دموی تک‌تصویر زنده در ترمینال:** ابزار سبک CLI جهت اسکن بلادرنگ تصویر هر برگ دلخواه، نمایش تاخیر به میلی‌ثانیه، تصمیم گیت شانون و رسم نمودار میله‌ای ASCII توزیع احتمال ۸ بیماری. |
| **[`generate_error_gallery.py`](file:///e:/work/research-few-shot/generate_error_gallery.py)** | اسکریپت ویژوالایزیشن | **استخراج و رندر گالری خطاها:** اسکریپت خودکار استخراج ۹۱ خطای باقیمانده و تولید تصویر باکیفیت ماتریس ۳×۴ نمونه‌های چالش‌برانگیز در `docs/assets/error_analysis_gallery.png`. |
| **[`biodino_edge_results.json`](file:///e:/work/research-few-shot/biodino_edge_results.json)** | داده ساختاریافته | **سند عددی رسمی بنچمارک:** شامل ارقام دقیق دقت تک‌سید، میانگین ۳۰ اپیزودی، فواصل اطمینان ۹۵٪، ماتریس درهم‌ریختگی عددی و تاخیرهای دقیق سخت‌افزاری پردازنده لبه به میلی‌ثانیه. |
| **[`CHANGELOG.md`](file:///e:/work/research-few-shot/CHANGELOG.md)** | مستندات فنی | **گاه‌شمار پیشرفت پژوهش:** تشریح گام‌به‌گام ارتقای مدل از نسخه پایه ۲۳.۴٪ تا ۸۱.۶٪، سپس ۸۸.۰٪، ۹۴.۷٪ و در نهایت رکورد تاریخی ۹۷.۳۴٪ با ذکر دقیق تغییرات اعمال‌شده در هر فاز. |
| **[`paper/main.tex`](file:///e:/work/research-few-shot/paper/main.tex)** | سورس لاتک | **متن مقاله علمی:** مقاله کامل ۳ صفحه‌ای مطابق فرمت رسمی IEEE با فرمولاسیون ریاضی انقباض کوواریانس فیشر، گیت عدم قطعیت شانون، جداول مقایسه روش‌ها و تفکیک سنجه‌های پاتولوژی هر کلاس. |
| **[`paper/main.pdf`](file:///e:/work/research-few-shot/paper/main.pdf)** | سند خروجی | **فایل PDF دوربین‌خوان (Camera-Ready):** خروجی کامپایل‌شده مقاله با موتور pdfTeX و MiKTeX آماده پرینت، ارسال به داوران ژورنال و پرزنتیشن برای اساتید. |
| **[`paper/references.bib`](file:///e:/work/research-few-shot/paper/references.bib)** | مراجع علمی | آرشیو BibTeX مراجع معتبر شامل مقالات DINOv2 (Meta AI), BioCLIP (Imageomics CVPR 2024), CLIP (OpenAI), Tip-Adapter و مراجع گیاه‌پزشکی. |
| **[`docs/index.md`](file:///e:/work/research-few-shot/docs/index.md)** | دانشنامه و ایندکس | **نقشه راه جامع مستندات:** راهنمای مرکزی و جدول اطلس اسناد همراه با ۴ برنامه مطالعاتی پیشنهادی (سریع، تئوری، دفاع و سخت‌افزار). |
| **[`docs/execution_and_dataset_guide.md`](file:///e:/work/research-few-shot/docs/execution_and_dataset_guide.md)** | راهنمای اجرایی | **راهنمای نصب، دیتاست و کَش:** نحوه دانلود دیتاست ۵۴ هزار تصویری PlantVillage، عملکرد کَش ۲۷MB، نصب پکیج‌ها و تنظیم هایپرپارامترها. |
| **[`docs/reviewer_rebuttal_playbook.md`](file:///e:/work/research-few-shot/docs/reviewer_rebuttal_playbook.md)** | کتابچه دفاع و داوری | **آمادگی دفاع در برابر داوران بین‌المللی:** پاسخ‌های مستند به ۲۰ سوال چالش‌برانگیز داوران و چارچوب ۱۰ اسلایدی ارائه شفاهی. |
| **[`docs/failure_modes_and_robustness.md`](file:///e:/work/research-few-shot/docs/failure_modes_and_robustness.md)** | تحلیل خطا و مقاومت | **کالبدشکافی ۹۱ خطای باقیمانده و OOD:** بررسی پاتولوژیک لزیون‌ها، آزمون‌های تنش تاری و تغییر نور و تشخیص هوشمند داده‌های نامربوط با گیت شانون. |
| **[`docs/edge_hardware_deployment_guide.md`](file:///e:/work/research-few-shot/docs/edge_hardware_deployment_guide.md)** | راهنمای سخت‌افزار لبه | **استقرار عملیاتی مزرعه:** مقایسه رزبری‌پای و جتسون، اسکریپت تبدیل به ONNX INT8، مدیریت افت حرارتی و تحلیل باتری برای پهپاد. |
| **[`docs/few_shot_taxonomy_guide.md`](file:///e:/work/research-few-shot/docs/few_shot_taxonomy_guide.md)** | تاریخچه و تبارشناسی | **شجره‌نامه یادگیری چندنمونه‌ای:** تکامل ۴ نسل فکری هوش مصنوعی از متا-لرنینگ گرادیانی تا یادگیری متریک و حل تحلیلی فیشر ۲۰۲۶. |
| **[`docs/plant_pathology_domain_guide.md`](file:///e:/work/research-few-shot/docs/plant_pathology_domain_guide.md)** | راهنمای پاتولوژی گیاهی | **دانش تخصصی کشاورزی:** تشریح اسامی علمی پاتوژن‌ها (*Venturia*, *Guignardia*)، علائم بالینی تفکیک بیماری‌ها و واژه‌نامه تخصصی. |
| **[`docs/mathematics_foundation_guide.md`](file:///e:/work/research-few-shot/docs/mathematics_foundation_guide.md)** | کتابچه آموزشی ریاضی | **آموزش قدم‌به‌قدم ریاضیات از صفر (۱,۱۵۰ خط):** مشتق، قضیه فیثاغورس، جبر خطی، آنتروپی شانون و کارگاه عددی حل‌شده دستی. |
| **[`docs/algorithm_guide.md`](file:///e:/work/research-few-shot/docs/algorithm_guide.md)** | مستندات فنی | **مرجع جامع ریاضی و الگوریتمی:** توضیح تفصیلی اثبات انقباض لدویت-ولف، هندسه منیفولد ۸۹۶ بعدی و تحلیل پیچیدگی FLOPs. |
| **[`docs/paper_guide.md`](file:///e:/work/research-few-shot/docs/paper_guide.md)** | مستندات راهنما | **راهنمای محیط لاتک:** راهنمای گام‌به‌گام ستاپ ادیتور، اکستنشن LaTeX Workshop و کامپایلر MiKTeX روی سیستم‌های جدید. |
| **[`cache_artifacts/pv_novel_embeddings.pt`](file:///e:/work/research-few-shot/cache_artifacts/pv_novel_embeddings.pt)** | باینری کش (۲۷MB) | ذخیره آفلاین ویژگی‌های استخراج‌شده ۷,۱۹۳ نمونه آزمون جهت بازتولید آنی زیر ۱ ثانیه. |
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
