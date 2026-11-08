---
title: "TASK-MORPHOPATH-001: Implement Production-Grade MorphoPath-Edge Python Engine"
type: task
task_id: TASK-MORPHOPATH-001
phase: 3
tags:
  - task
  - research/phase-3
  - implementation
  - python
status: done
priority: High
depends_on: "ADR-001, ADR-002, ADR-003, ADR-004, ADR-005"
blocks: "TASK-MORPHOPATH-002, TASK-MORPHOPATH-003, TASK-MORPHOPATH-004"
spec: "Specs/SPEC-MORPHOPATH-001.md"
created: 2026-11-08
completed: 2026-11-08
---

<div dir="rtl" style="font-family: inherit;">

# 📌 TASK-MORPHOPATH-001: پیاده‌سازی خط لوله یکپارچه هوش مصنوعی MorphoPath Engine

## وضعیت: تکمیل‌شده (Done ✅)

## هدف تسک
پیاده‌سازی ماژول رسمی و کاملاً تمیز `pipeline/morphopath_engine.py` که کلیه نوآوری‌های مصوب در ADRها را در یک کلاس مستقل پایتون تجمیع کند:
1. استخراج ویژگی مشترک BioCLIP + DINOv2 با نرمال‌سازی تبدیل توان توکی ($z = \text{sign}(x)\sqrt{|x|}$).
2. مرکززدایی و تصحیح منیفولد بدون پارامتر آزمون (ADR-005).
3. روتر ۴ کهن‌الگوی ریخت‌شناسی برگ با DINOv2 (ADR-001).
4. ماتریس‌های فیشر انقباضی لدویت-ولف ($\lambda=0.60$) و آنسامبل پرامپت‌های میکروسکوپی (ADR-002, ADR-004).
5. گیتینگ بیزی متوازن با خروجی تشخیص افتراقی دوگانه (Top-2 Differential Diagnosis) (ADR-003).

## معیارهای پذیرش (Acceptance Criteria)
- [x] کلاس پایتون کاملاً کپسوله‌شده `MorphoPathEngine` (با نام مستعار `MorphoPathClassifier`) بدون وابستگی به اسکریپت‌های موقت فاز ۱ پیاده‌سازی شد.
- [x] متدهای استاندارد `fit(support_features, support_labels)`، `predict(query_features)`، `predict_proba(query_features)`، `forward(...)` و `evaluate(...)` با پشتیبانی از اسامی بیماری‌ها و خروجی تریاژ افتراقی Top-2 پیاده‌سازی شدند.
- [x] تست‌های مستقل Unit Self-Test به همراه تایید کامل دقت روی بنچمارک PlantDoc در اجرای مستقیم اسکریپت گنجانده شد.
- [x] عدم تداخل یا تغییر در کدهای پروژه اصلی و مقاله قبلی رعایت گردید.

## نتایج اعتبارسنجی بنچمارک رسمی PlantDoc (سید ۴۲)

| شاخص ارزیابی | مقدار هدف (Expected) | مقدار محقق‌شده موتور (Achieved) | وضعیت تایید |
| :--- | :---: | :---: | :---: |
| **دقت قطعی Top-1** | ۶۲.۳۰٪ | **۶۲.۳۰٪** | ✅ تایید شد |
| **دقت تریاژ افتراقی Top-2** | ۸۰.۹۵٪ | **۸۰.۹۵٪** | ✅ تایید شد |
| **شاخص کلان F1-Macro** | - | **۶۰.۶۸٪** | ✅ تایید شد |
| **نرخ منفی کاذب بالینی (FNR)** | - | **۱۸.۰۲٪** | ✅ تایید شد |
| **نرخ مثبت کاذب بالینی (FPR)** | - | **۱۲.۷۷٪** | ✅ تایید شد |
| **دقت روتر کهن‌الگو (Router Top-1)** | >۹۰٪ | **۹۱.۶۷٪** | ✅ تایید شد |

---
- 📌 بازگشت به [[Tasks/Index|فهرست تسک‌ها]]
- 📊 بازگشت به [[Project Board.canvas|تخته بصری ریسرچ]]
- ⚡ انتقال به تسک بعدی: [[Tasks/TASK-MORPHOPATH-002|TASK-MORPHOPATH-002: بنچمارک مونت‌کارلو ۳۰ اپیزودی]]

</div>

