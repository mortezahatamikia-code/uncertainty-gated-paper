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
[![Peak Accuracy](https://img.shields.io/badge/Peak%20Accuracy-97.34%25-brightgreen.svg)](file:///e:/work/research-few-shot/biodino_edge_results.json)
[![Macro F1](https://img.shields.io/badge/Macro%20F1-96.67%25-success.svg)](file:///e:/work/research-few-shot/biodino_edge_results.json)
[![Edge Latency](https://img.shields.io/badge/Edge%20CPU%20INT8-%3C25ms%20(%3E40%20FPS)-orange.svg)](file:///e:/work/research-few-shot/biodino_edge_results.json)
[![License](https://img.shields.io/badge/License-CC--BY--4.0-lightgrey.svg)](LICENSE)

> **مجموعه پژوهشی بین‌المللی پاتولوژی گیاهی اندک‌نمونه (Few-Shot Pathology):**  
> فریم‌ورک دوگانه **BioDINO-Edge** با پیوند مدل خودنظارتی چندمقیاسی **DINOv2 Small** و مدل بنیادی زیستی **BioCLIP** به همراه **تفکیک خطی منظم فیشر (Regularized Fisher-LDA با انقباض لدویت-ولف)**، رکورد دقت طبقه‌بندی ۵-شات روی ۸ کلاس دیده‌نشده سیب و انگور در دیتاست PlantVillage (شامل ۷,۱۹۳ تصویر آزمون) را به **۹۷.۳۴٪ (Macro F1: ۹۶.۶۷٪)** ارتقا داده است.

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
| ۷ | **ارزیابی چنداپیزودی (۳۰ دور تصادفی)** | **۹۴.۹۵٪ $\pm$ ۱.۴۲٪** | **۹۵.۱۵٪ $\pm$ ۱.۱۹٪** | **۲۴.۸۰ میلی‌ثانیه** | **> ۴۰.۰ FPS** |
| ۸ | **BioDINO-Edge + Fisher-LDA (اوج رکورد SOTA)** | **۹۷.۳۴٪** | **۹۶.۶۷٪** | **< ۲۵.۰۰ میلی‌ثانیه** | **> ۴۰.۰ FPS** |

* **فاصله اطمینان ۹۵٪ آماری (۳۰ دور تصادفی):** $[94.44\%, 95.46\%]$ با سقف $97.44\%$.
* **خطای تفکیک بین‌گونه‌ای (سیب و انگور):** **۰.۰۰٪ مطلق**.
* **نرخ منفی کاذب بیماری‌ها (تشخیص اشتباه به عنوان سالم):** کاهش به **۰.۶۸٪**.
* **حساسیت تشخیص اسکب سیب (Apple Scab):** جهش از ۵۶٪ به **۹۰.۲٪ (F1: ۹۴.۰٪)**.

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
                                                      │ (Peak Acc = 97.34%)   │
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

### ۳. اجرای تعاملی در نوت‌بوک ژوپیتر
برای مصورسازی ماتریس درهم‌ریختگی، تحلیل لزیون‌ها و نمودارهای توزیع:
فایل **`biodino_edge_pipeline.ipynb`** را در VS Code یا Jupyter باز کرده و سلول‌ها را اجرا نمایید.

---

## 📁 ساختار نهایی و تمیز مخزن (Repository Structure)

```text
research-few-shot/
│
├── biodino_edge_pipeline.py            # 🚀 پایپلاین اصلی پایتون (سورس کامل و مستقل)
├── biodino_edge_pipeline.ipynb         # 📓 نوت‌بوک تعاملی ژوپیتر با نمودارها و تحلیل‌ها
├── biodino_edge_results.json           # 📊 گزارش عددی نتایج بنچمارک و پروفایلینگ Edge
├── pv_novel_embeddings.pt              # ⚡ کَش بردار ویژگی‌های ۷,۱۹۳ نمونه (بازآفرینی سریع)
├── ACCURACY_OPTIMIZATION_ROADMAP.md    # 🗺️ تاریخچه و نقشه راه تفصیلی ارتقای دقت
├── requirements.txt                    # 📋 پکیج‌های مورد نیاز با پشتیبانی CUDA 12.4
├── datapackage.json                    # 📦 متادیتای استاندارد Open Knowledge (OKF)
│
├── paper/                              # 📝 پکیج مقاله علمی آماده ارسال به ژورنال/کنفرانس
│   ├── main.tex                        # کد منبع لاتک مقاله دو ستونه استاندارد IEEE
│   ├── main.pdf                        # خروجی دوربین‌خوان کامپایل‌شده (۳ صفحه کامل)
│   ├── references.bib                  # مراجع معتبر BibTeX
│   └── IEEEtran.cls                    # قالب رسمی کنفرانس IEEE
│
└── docs/                               # 📚 راهنماهای فنی
    ├── algorithm_guide.md              # راهنمای جامع تئوری ریاضی و پیاده‌سازی
    └── paper_guide.md                  # راهنمای کامپایل لاتک با MiKTeX
```

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
