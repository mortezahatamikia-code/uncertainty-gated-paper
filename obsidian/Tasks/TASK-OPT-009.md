---
title: "TASK-OPT-009: Cross-Subspace Bilinear Gating"
type: task
task_id: TASK-OPT-009
phase: 4
tags:
  - task
  - research/phase-4
  - subspace
  - bilinear-gating
  - ponytail
status: todo
priority: High
depends_on: "TASK-OPT-005"
blocks: "TASK-OPT-011"
spec: "Specs/SPEC-MORPHOPATH-001.md"
idea: "Ideation/IDEA-015-Cross-Subspace-Bilinear-Gating.md"
created: 2026-11-11
---

<div dir="rtl" style="font-family: inherit;">

# 📌 TASK-OPT-009: پیاده‌سازی و ارزیابی دروازه‌بانی دوخطی زیرفضاها (Cross-Subspace Bilinear Gating)

## ۱. هدف و صورت مسئله
تعدیل غیرخطی امتیاز پاتولوژی بر اساس همخوانی ریخت‌شناسی برگی DINOv2 جهت مهار خطاهای هشدار کاذب بین گونه‌های گیاهی نامربوط.

## ۲. دستورالعمل پیاده‌سازی
1. در تابع تجمیع امتیازهای بصری:
   $$S_{\text{gated}}(q, c) = S_{\text{bio}}(q, c) \cdot \left( 1 + \alpha \cdot \tanh(S_{\text{dino}}(q, c)) \right)$$
   یا مدولاسیون نرم مشابه با ضریب کنترل $\alpha \approx 0.20$.
2. تست روی PlantDoc و PlantVillage.
3. در صورت بهبود تفکیک رده‌ای و حفظ تاخیر در کسری از میکروثانیه، ادغام شود؛ در غیر این صورت گزارش رد ثبت گردد.

</div>

