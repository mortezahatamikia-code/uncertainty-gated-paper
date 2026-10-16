---
okf_version: "1.0.0"
package: "uncertainty-gated-dual-stage-peft"
title: "Uncertainty-Gated Dual-Stage PEFT: Trustworthy Few-Shot Plant Disease Recognition on Edge Devices"
license: "CC-BY-4.0"
keywords:
  - "few-shot-learning"
  - "plant-disease"
  - "vision-language-models"
  - "clip"
  - "peft"
  - "lora"
  - "entropy-gate"
  - "edge-ai"
resources:
  - path: "plantvillage/plantvillage dataset/color"
    type: "image-dataset"
  - path: "scratch_run_pipeline.py"
    type: "code"
  - path: "paper/main.tex"
    type: "manuscript"
---

# Uncertainty-Gated Dual-Stage PEFT

> **پروژه پژوهشی کنفرانس IEEE:**  
> **عنوان:** Uncertainty-Gated Dual-Stage PEFT: Trustworthy Few-Shot Plant Disease Recognition on Edge Devices  
> **محیط اجرایی:** تست‌شده و بهینه‌سازی‌شده روی Windows 11 با کارت گرافیک NVIDIA GeForce RTX 4070 (8GB VRAM)  
> **فرمت متادیتا:** منطبق با استاندارد Open Knowledge Foundation (OKF) در فایل [datapackage.json](file:///e:/work/research-few-shot/datapackage.json)

---

## ⚡ راهنمای سریع راه‌اندازی (Quickstart in 3 Steps)

### ۱. ساخت محیط مجازی اختصاصی
```powershell
python -m venv .venv
```

### ۲. نصب پکیج‌ها با شتاب‌دهنده GPU (CUDA 12.4)
```powershell
# نصب تمام وابستگی‌های پروژه به همراه نسخه شتاب‌یافته PyTorch با یک دستور
.\.venv\Scripts\pip.exe install -r requirements.txt
```

### ۳. اجرای پایپلاین کامل الگوریتم
```powershell
.\.venv\Scripts\python.exe -u scratch_run_pipeline.py
```
*(یا اجرای تعاملی در نوت‌بوک `uncertainty_gated_peft_colab.ipynb` به صورت محلی یا روی **Google Colab**؛ راهنمای گام‌به‌گام کولب در [docs/algorithm_guide.md](file:///e:/work/research-few-shot/docs/algorithm_guide.md#۸-گامهای-اجرای-نوتبوک-روی-google-colab-قدم-به-قدم)).*

---

## 📁 ساختار مخزن (Repository Structure)

```text
research-few-shot/
│
├── datapackage.json                    # 📦 بسته متادیتای استاندارد Open Knowledge (OKF)
├── requirements.txt                    # 📋 فهرست وابستگی‌ها با ایندکس CUDA 12.4
├── .gitignore                          # 🛡️ قوانین جامع نادیده‌گرفتن فایل‌های حجیم و کش
├── pyrefly.toml                        # پیکربندی اتصال موتور تحلیل کد ادیتور به .venv
│
├── docs/                               # 📚 مستندات تفصیلی و قدم به قدم
│   ├── algorithm_guide.md              # راهنمای کامل معماری مدل، حل مشکلات ویندوز و اجرای پایپلاین
│   └── paper_guide.md                  # راهنمای ستاپ محیط لاتک، کامپایلر MiKTeX و ویرایش زنده PDF
│
├── paper/                              # 📝 پکیج کامل سورس مقاله IEEE
│   ├── main.tex                        # کد منبع لاتک مقاله دو ستونه
│   ├── references.bib                  # بانک مراجع استاندارد BibTeX
│   ├── IEEEtran.cls                    # قالب رسمی کنفرانس‌های IEEE
│   └── main.pdf                        # فایل نهایی خروجی مقاله
│
├── plantvillage/                       # 🌿 دیتاست کامل بیماری‌های گیاهی (۵۴,۳۰۵ تصویر - ۳۸ کلاس)
│   └── plantvillage dataset/color/
│
├── uncertainty_gated_peft_colab.ipynb  # نوت‌بوک تعاملی آزمایش‌ها
├── scratch_run_pipeline.py             # اسکریپت اجرای مستقیم و بدون وقفه پایپلاین
├── .vscode/settings.json               # تنظیمات کامپایلر PDF و مفسر پایتون در ادیتور
└── README.md                           # خلاصه اجرایی پروژه (OKF Format)
```

---

## 📖 مستندات جامع تکمیلی (Detailed Guides)

برای مطالعه جزئیات عمیق هر بخش، به فایل‌های راهنما در پوشه `docs/` مراجعه فرمایید:
- [راهنمای جامع الگوریتم و رفع مشکلات سیستم‌عامل (docs/algorithm_guide.md)](file:///e:/work/research-few-shot/docs/algorithm_guide.md)
- [راهنمای نصب و نگارش مقاله لاتک در ویندوز (docs/paper_guide.md)](file:///e:/work/research-few-shot/docs/paper_guide.md)
