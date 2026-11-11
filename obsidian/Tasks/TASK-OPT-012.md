---
title: "TASK-OPT-012: Gegenbauer Spherical Harmonic Kernel for Hypersphere Decrowding"
type: task
task_id: TASK-OPT-012
phase: 4
tags:
  - task
  - research/phase-4
  - harmonic-analysis
  - gegenbauer
  - sphere-packing
  - ponytail
status: done
priority: High
depends_on: "TASK-OPT-011"
blocks: "TASK-OPT-016"
spec: "Specs/SPEC-MORPHOPATH-001.md"
idea: "Ideation/IDEA-017-Gegenbauer-Spherical-Harmonic-Kernel.md"
created: 2026-11-11
completed: 2026-11-11
generated: { by: okf-enforcer/0.6, at: 2026-11-11T16:04:18Z }
---

<div dir="rtl" style="font-family: inherit;">

# 📌 TASK-OPT-012: پیاده‌سازی و ارزیابی تجربی تبدیل چندجمله‌ای هارمونیک گگن‌باور روی ابرکره

## ۱. هدف و صورت مسئله
افزایش قدرت تفکیک غیرخطی بیماری‌های بسیار مشابه بر روی ابرکره واحد $\mathbb{S}^{895}$ از طریق تبدیل ارتوگونال چندجمله‌ای گگن‌باور درجه ۲ (الهام‌گرفته از کران‌های بستهبندی کروی Cohn–Elkies).

## ۲. دستورالعمل پیاده‌سازی و فرمول‌بندی
فرم بسته چندجمله‌ای گگن‌باور درجه ۲ روی ماتریس شباهت کسینوسی:
$$K(S) = S + \gamma \cdot \left( \frac{D}{D-1} S^2 - \frac{1}{D-1} \right)$$
که در آن $D=896$ و $\gamma = -0.20$ به عنوان دافعه ضد ازدحام هم‌فعالی‌های نویز زمینه اعمال گردید.

## ۳. نتایج تجربی ارزیابی
- **مزرعه (PlantDoc 27-way 5-shot Seed 42):**
  - دقت Top-1: از ۶۴.۶۸٪ به **۶۵.۰۸٪** ارتقا یافت (+۰.۴۰٪).
  - دقت Top-2: برابر با **۸۰.۱۶٪**.
  - شاخص Macro F1: از ۶۳.۳۲٪ به **۶۳.۵۲٪** بهبود یافت (+۰.۲۰٪).
  - نرخ هشدار کاذب بالینی (FPR): پایدار در **۸.۸۹٪**.
  - نرخ بیماری‌های جامانده (FNR): پایدار در **۶.۷۹٪**.
- **آزمایشگاه (PlantVillage 38-class across 15 episodes):**
  - دقت Top-1: **۸۷.۴۴٪ ± ۰.۹۵٪** (دقیقاً منطبق بر بیس‌لاین SOTA بدون افت).
- **بودجه لبه (Edge Budget):**
  - تاخیر افزوده هد: **۰.۰۰۲۳ میلی‌ثانیه (۲.۳ میکروثانیه)**.
  - پارامترها و وزن اضافه: **۰.۰ مگابایت (Zero Parameters)**.

## ۴. وضعیت پذیرش
**پذیرفته شد (DONE)**: ادغام کامل در `pipeline/morphopath_math.py` و `pipeline/morphopath_engine.py` با پارامتر پیش‌فرض `gamma_gegenbauer = -0.20`.

</div>
