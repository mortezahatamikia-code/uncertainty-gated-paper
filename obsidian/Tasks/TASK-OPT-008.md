---
title: "TASK-OPT-008: Cardinality-Scaled Ledoit-Wolf Covariance Shrinkage"
type: task
task_id: TASK-OPT-008
phase: 4
tags:
  - task
  - research/phase-4
  - covariance
  - lda
  - shrinkage
  - ponytail
status: todo
priority: High
depends_on: "TASK-OPT-005"
blocks: "TASK-OPT-011"
spec: "Specs/SPEC-MORPHOPATH-001.md"
idea: "Ideation/IDEA-014-Cardinality-Scaled-Covariance-Shrinkage.md"
created: 2026-11-11
---

<div dir="rtl" style="font-family: inherit;">

# 📌 TASK-OPT-008: پیاده‌سازی و ارزیابی انقباض پویای کوواریانس به تفکیک کهن‌الگو (Cardinality-Scaled Covariance Shrinkage)

## ۱. هدف و صورت مسئله
افزایش قدرت تفکیک بیماری‌های گوجه‌فرنگی و سولانوئید با تنظیم پویای ضریب انقباض فیشر به جای ضریب ثابت ۰.۶۰ برای تمام خوشه‌ها.

## ۲. دستورالعمل پیاده‌سازی
1. در متد `fit()` کلاس `MorphoPathEngine`:
   - استخراج تعداد نمونه‌های ساپورت در هر کهن‌الگو $N_a$.
   - محاسبه ضریب انقباض اختصاصی:
     $$\lambda_a = \mathrm{clip}\left( \frac{\kappa}{\sqrt{N_a}}, 0.25, 0.85 \right)$$
   - آموزش تفکیک‌کننده‌های فیشر (Fisher LDA) هر کهن‌الگو با $\lambda_a$ اختصاصی خود.
2. اعتبارسنجی روی PlantDoc و دقت درون‌خوشه‌ای سولانوئید.
3. در صورت برتری نسبت به انقباض ثابت ۰.۶۰، جایگزین متد قبلی شود.

</div>

