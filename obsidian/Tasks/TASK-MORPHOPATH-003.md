---
title: "TASK-MORPHOPATH-003: Edge INT8 Quantization, Latency & Memory Profiling"
type: task
task_id: TASK-MORPHOPATH-003
phase: 3
tags:
  - task
  - research/phase-3
  - edge
  - latency
  - profiling
status: done
priority: Medium
depends_on: "TASK-MORPHOPATH-001"
blocks: "TASK-MORPHOPATH-004"
spec: "Specs/SPEC-MORPHOPATH-001.md"
created: 2026-11-08
completed: 2026-11-08
log: "Logs/Log-Phase3-Edge-Profiling.md"
---

<div dir="rtl" style="font-family: inherit;">

# 📌 TASK-MORPHOPATH-003: پروفایلینگ تاخیر، سرعت، مصرف رم و حجم روی سخت‌افزار لبه

## وضعیت: تکمیل‌شده (Done ✅)

## هدف تسک
سنجش دقیق و ممیزی تجربی موتور استنتاج روی شبیه‌ساز سخت‌افزار لبه و پردازنده موبایل:
1. ارزیابی تاخیر بر حسب میلی‌ثانیه برای هر ماژول به تفکیک: (الف) استخراج ویژگی DINOv2، (ب) روتر کهن‌الگو، (ج) تصحیح منیفولد، (د) فیشر بیزی.
2. اندازه‌گیری نرخ فریم بر ثانیه (FPS) و مصرف حافظه رم (Peak RAM Usage).
3. اعتبارسنجی حجم فایل نهایی اپلیکیشن و ثبات آن در زیر ۲۳ مگابایت.

## نتایج حاصله و شواهد تجربی (Execution Summary)
- **تاخیر هد تصمیم‌گیر:** میانگین **۰.۴۸۷۴ میلی‌ثانیه** (میانه: ۰.۴۴۲۹ میلی‌ثانیه، P95: ۰.۷۰۲۳ میلی‌ثانیه، Throughput: **۲,۰۵۱.۸ استنتاج بر ثانیه**).
- **تاخیر DINOv2 ViT-S/14 در فرمت INT8:** میانگین **۴۰.۶۸ میلی‌ثانیه** (۲۴.۶ FPS) با حفظ وفاداری کسینوسی ۹۷.۵۸٪.
- **تاخیر BioCLIP ViT-B/16 در فرمت INT8:** میانگین **۷۱.۰۲ میلی‌ثانیه** (۱۴.۱ FPS).
- **تاخیر موثر پایپ‌لاین آبشاری:** **۶۱.۰۶ میلی‌ثانیه** (۱۶.۴ FPS) در سناریوی ۷۲٪ مسیر سریع / ۲۸٪ مسیر عمیق.
- **حجم بسته نصبی لبه (APK):** **۲۲.۸۸ مگابایت** (زیر سقف ۲۳.۰ مگابایت) با صفر مگابایت وزن جدید شبکه عصبی.
- **گزارش رسمی:** [[Logs/Log-Phase3-Edge-Profiling|Log-Phase3-Edge-Profiling]]
- **داده‌های ساخت‌یافته:** `experiments/phase3_morphopath/edge_profiling_results.json`

## معیارهای پذیرش (Acceptance Criteria)
- [x] اثبات کارکرد هد تصمیم‌گیر زیر ۰.۵ میلی‌ثانیه و مسیر سریع DINOv2 در حدود ۴۰ میلی‌ثانیه روی CPU.
- [x] تایید عدم افت دقت در فرمت کوانتیزه‌شده INT8 و حفظ شباهت کسینوسی بالای ۹۷.۵٪.
- [x] تایید سقف حجم Standalone APK کمتر از ۲۳.۰ مگابایت.

---
- 📌 بازگشت به [[Tasks/Index|فهرست تسک‌ها]]

</div>

