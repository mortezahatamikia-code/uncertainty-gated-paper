---
title: "TASK-OPT-007: Asymmetric Contrastive Symptom Prompts with Dual Negative Margin"
type: task
task_id: TASK-OPT-007
phase: 4
tags:
  - task
  - research/phase-4
  - nlp
  - bioclip
  - negative-prompts
  - ponytail
status: todo
priority: High
depends_on: "TASK-OPT-005"
blocks: "TASK-OPT-011"
spec: "Specs/SPEC-MORPHOPATH-001.md"
idea: "Ideation/IDEA-013-Asymmetric-Contrastive-Text-Prompts.md"
created: 2026-11-11
---

<div dir="rtl" style="font-family: inherit;">

# 📌 TASK-OPT-007: پیاده‌سازی و ارزیابی پرامپت کنتراستی دوگانه نامتقارن (Asymmetric Contrastive Text Prompts)

## ۱. هدف و صورت مسئله
کاهش نرخ هشدار کاذب سم‌پاشی (Clinical FPR) از ۸.۸۹٪ به زیر ۶٪ از طریق تمایز علائم فعال بیماری از آسیب‌های مکانیکی، پیری برگ و علائم غیربیماری.

## ۲. دستورالعمل پیاده‌سازی
1. تعریف پرامپت‌های متنی منفی به ازای کلاس‌ها (مثلاً بافت سالم، فقدان هاله زرد، پیری طبیعی کلروفیل).
2. استخراج آفلاین بردار ۵۱۲ بعدی BioCLIP برای پرامپت منفی و ذخیره به عنوان بردار ثابت سبک.
3. در خط استنتاج موتور:
   $$S_{\text{txt}}(q, c) = \cos(q_{\text{bio}}, t_c^{+}) - \eta \cdot \cos(q_{\text{bio}}, t_c^{-})$$
4. آزمایش مقدار $\eta \in [0.10, 0.40]$.
5. سنجش تغییرات FPR و Macro F1 روی دادگان PlantDoc و PlantVillage.
6. در صورت بهبود معنادار شاخص‌های بالینی بدون افزایش تاخیر، حفظ شود؛ در غیر این صورت گزارش رد ثبت گردد.

</div>

