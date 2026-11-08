---
title: "TASK-MORPHOPATH-005: PlantVillage 38-Class Benchmark & BioDINO-Edge Comparison"
type: task
task_id: TASK-MORPHOPATH-005
phase: 3
tags:
  - task
  - research/phase-3
  - plantvillage
  - benchmarking
  - biodino-comparison
status: done
priority: Critical
depends_on: "TASK-MORPHOPATH-001, TASK-MORPHOPATH-002, TASK-MORPHOPATH-003, TASK-MORPHOPATH-004"
blocks: "DRAFT-MORPHOPATH-001"
spec: "Specs/SPEC-MORPHOPATH-001.md"
created: 2026-11-08
completed: 2026-11-08
log: "Logs/Log-PlantVillage-Validation.md"
---

<div dir="rtl" style="font-family: inherit;">

# 📌 TASK-MORPHOPATH-005: بنچمارک جامع ۳۸ کلاسی PlantVillage و مقایسه پارامتر به پارامتر با BioDINO-Edge

## وضعیت: تکمیل‌شده (Done ✅)

## هدف تسک
ارزیابی تجربی و اعتبارسنجی مقیاس‌پذیری معماری **MorphoPath-Edge** روی کلیه ۳۸ کلاس دادگان استاندارد جهانی **PlantVillage** (رژیم ۳۸-کلاسه ۵-شات در ۳۰ اپیزود مستقل مونت‌کارلو) و تدوین جدول مقایسه جامع پارامتر به پارامتر با معماری پیشین (**BioDINO-Edge**):
1. بارگذاری و استخراج ویژگی‌های DINOv2 (۳۸۴ بعدی) و BioCLIP (۵۱۲ بعدی) بر روی GPU برای کلیه ۳۸ کلاس.
2. نگاشت دقیق ۳۸ کلاس به ۴ آرکی‌تایپ ساختاری کلان گیاه‌شناسی:
   - آرکی‌تایپ ۰ (سولانوئید): گوجه‌فرنگی (۱۰) + سیب‌زمینی (۳) = ۱۳ کلاس.
   - آرکی‌تایپ ۱ (ویتوئید / کوکوربیت): انگور (۴) + کدو (۱) = ۵ کلاس.
   - آرکی‌تایپ ۲ (پوئید): ذرت (۴) = ۴ کلاس.
   - آرکی‌تایپ ۳ (روزویید / پهن‌برگ خزان‌دار): سیب (۴)، بلوبری (۱)، گیلاس (۲)، پرتقال (۱)، هلو (۲)، فلفل دلمه‌ای (۲)، تمشک (۱)، سویا (۱)، توت‌فرنگی (۲) = ۱۶ کلاس.
3. اجرای خط لوله استنتاج MorphoPathEngine و استخراج شاخص‌های Top-1، Top-2، Macro F1، دقت روتر، نرخ‌های بالینی FNR/FPR، و تاخیر محاسباتی CPU.
4. ارزیابی زیرمجموعه ۱۱ کلاس novel جهت مقایسه مستقیم و دقیق با BioDINO-Edge.
5. ذخیره‌سازی داده‌های ساخت‌یافته در `experiments/phase3_morphopath/plantvillage_benchmark_results.json`.
6. تدوین لاگ جامع در [[Logs/Log-PlantVillage-Validation|Log-PlantVillage-Validation]].

## نتایج حاصله و شواهد تجربی (Execution Summary)
- **طبقه‌بندی سراسری ۳۸ کلاسی (PlantVillage 38-Way 5-Shot):**
  - میانگین دقت Top-1: **۸۶.۵۳٪ $\pm$ ۱.۰۰٪** (بازه اطمینان ۹۵٪: $[86.17\%, 86.89\%]$، اوج: **۸۸.۱۶٪**).
  - میانگین دقت تریاژ افتراقی Top-2: **۹۴.۲۵٪ $\pm$ ۰.۷۶٪** (بازه اطمینان ۹۵٪: $[93.98\%, 94.53\%]$، اوج: **۹۵.۷۰٪**).
  - میانگین Macro F1-Score: **۸۶.۰۳٪ $\pm$ ۱.۰۶٪**.
  - میانگین دقت روتر آرکی‌تایپی: **۹۳.۰۱٪ $\pm$ ۰.۵۸٪**.
  - نرخ‌های بالینی: FNR معادل **۳.۸۲٪ $\pm$ ۰.۷۹٪** و FPR معادل **۱.۹۱٪ $\pm$ ۱.۲۴٪**.
- **ارزیابی ۱۱ کلاس جدید (11-Class Novel Subset):**
  - میانگین دقت Top-2: **۹۹.۲۰٪ $\pm$ ۰.۵۳٪** (اوج: **۱۰۰.۰۰٪**).
  - میانگین دقت Top-1: **۹۳.۸۳٪ $\pm$ ۱.۸۳٪** (اوج: **۹۶.۹۷٪**).
  - دقت روتر گیاه‌شناسی: **۹۹.۱۴٪ $\pm$ ۰.۴۸٪**.
- **تاخیر سخت‌افزاری و شتاب استنتاج:**
  - تاخیر هد تصمیم‌گیری CPU: **۰.۱۳۵۶ میلی‌ثانیه** (نرخ فریم: **۷,۳۷۵ کوئری در ثانیه**).
  - تاخیر موثر خط لوله آبشاری کوانتیزه INT8: **۵۳.۶۰ میلی‌ثانیه (۱۸.۶۶ فریم بر ثانیه)** در برابر ۷۴۶.۳۷ میلی‌ثانیه BioDINO (**شتاب ۱۳۹۲ درصدی / 13.92x Speedup**).
  - حجم پکیج نصبی Standalone APK: **۲۲.۸۸ مگابایت** (۷۸٪ سبک‌تر از ۱۰۴.۷ مگابایت BioDINO).
  - مصرف حافظه رم Peak Heap: **۶۶.۹۵ مگابایت** (۸۵٪ کاهش نسبت به ۴۵۰+ مگابایت BioDINO).
- **گزارش رسمی:** [[Logs/Log-PlantVillage-Validation|Log-PlantVillage-Validation]]
- **داده‌های ساخت‌یافته:** `experiments/phase3_morphopath/plantvillage_benchmark_results.json`

## معیارهای پذیرش (Acceptance Criteria)
- [x] اجرای کامل ارزیابی ۳۰ اپیزودی مونت‌کارلو روی تمام ۳۸ کلاس PlantVillage با $k=5$ شات.
- [x] استخراج و کش ویژگی‌های ترکیبی DINOv2 و BioCLIP روی GPU.
- [x] نگاشت کامل ۳۸ کلاس به ۴ آرکی‌تایپ گیاه‌شناسی (۱۳، ۵، ۴، ۱۶ کلاس).
- [x] ارزیابی مقایسه‌ای مستقیم زیرمجموعه ۱۱ کلاسه با BioDINO-Edge.
- [x] تدوین جدول مقایسه جامع پارامتر به پارامتر در کلیه شاخص‌های دقت، F1، تاخیر، حجم APK و رم.

---
- 📌 بازگشت به [[Tasks/Index|فهرست تسک‌ها]]

</div>
