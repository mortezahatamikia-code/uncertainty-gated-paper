---
title: "TASK-OPT-010: Hierarchical Fast-Exit Decision Cascade"
type: task
task_id: TASK-OPT-010
phase: 4
tags:
  - task
  - research/phase-4
  - edge
  - latency
  - fast-exit
  - ponytail
status: todo
priority: High
depends_on: "TASK-OPT-005"
blocks: "TASK-OPT-011"
spec: "Specs/SPEC-MORPHOPATH-001.md"
idea: "Ideation/IDEA-016-Hierarchical-Fast-Exit-Cascade.md"
created: 2026-11-11
generated: { by: okf-enforcer/0.6, at: 2026-11-11T15:52:15Z }
---

<div dir="rtl" style="font-family: inherit;">

# 📌 TASK-OPT-010: پیاده‌سازی و ارزیابی خروج زودهنگام آبشاری لبه (Hierarchical Fast-Exit Cascade)

## ۱. هدف و صورت مسئله
افزایش نرخ فریم پردازش استریم دوربین موبایل و کاهش مصرف توان با عبور سریع فریم‌های واضح و قطعی بدون ورود به لایه‌های پرهزینه‌تر.

## ۲. دستورالعمل پیاده‌سازی
1. در متد `forward()` کلاس `MorphoPathEngine`:
   - بررسی اطمینان پس از شباهت اولیه منیفولد توکی:
     اگر $p_{(1)} > \tau_{\text{conf}}$ (مثلاً ۰.۸۵) و $(p_{(1)} - p_{(2)}) > \tau_{\text{margin}}$ (مثلاً ۰.۴۰)، خروج فوری با بازگرداندن خروجی استاندارد.
   - در صورت عدم برقراری شرط، ورود به فاز کامل (LDA + پرامپت + سرکوب سایبان).
2. ارزیابی تاخیر دقیق روی CPU و بررسی عدم افت دقت در مقایسه با نسخه بدون فست‌اگسیت.
3. در صورت کاهش چشمگیر تاخیر هد و تثبیت دقت، فعال‌سازی دائم به عنوان قابلیت پیش‌فرض موتور.

</div>

