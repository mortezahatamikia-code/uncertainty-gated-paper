---
title: "IDEA-013: Asymmetric Contrastive Symptom Prompts with Dual Negative Margin"
type: idea
idea_id: IDEA-013
phase: 1
tags:
  - idea
  - research/phase-1
  - nlp
  - bioclip
  - negative-prompts
status: pending
expected_gain: "Drop Clinical FPR from 8.89% to <5.5%, +0.8% Top-1 on PlantDoc"
mechanism: "Dual positive-negative text prompt contrast subtracting non-pathological leaf fatigue features"
created: 2026-11-11
---

<div dir="rtl" style="font-family: inherit;">

# 💡 IDEA-013: پرامپت کنتراستی دوگانه نامتقارن با حاشیه منفی علائم

### ۱. انگیزه و بیان مسئله
پرامپت‌های متنی BioCLIP در حال حاضر صرفاً نشانه‌های مثبت بیماری ("حلقه‌های متحدالمرکز"، "پیکنیدیوم سیاه") را کدگذاری می‌کنند. برگ‌های سالم پیر یا برگ‌های دارای پارگی‌های مکانیکی ناشی از باد، شباهت کسینوسی ضعیف اما مثبتی با پرامپت‌های قارچی نشان داده و باعث جهش هشدار کاذب سم‌پاشی (FPR) می‌شوند.

### ۲. مکانیزم پیشنهادی
برای هر کلاس بیماری، یک جفت پرامپت متنی آفلاین تعریف و استخراج می‌شود: پرامپت مثبت علائم بالینی $\mathbf{t}_c^{+}$ و پرامپت منفی ("بافت سالم اپیدرم، فقدان هاله زرد، کلروفیل یکنواخت بدون نکروز") $\mathbf{t}_c^{-}$:
$$S_{\text{txt}}(q, c) = \cos(\mathbf{q}_{\text{bio}}, \mathbf{t}_c^{+}) - \eta \cdot \cos(\mathbf{q}_{\text{bio}}, \mathbf{t}_c^{-})$$
با ضریب بهینه $\eta \approx 0.25$.

### ۳. بودجه و محدودیت لبه
- **وزن اضافه:** ۰.۰ مگابایت وزن عصبی (تنها ۵۵ کیلوبایت بردارهای متنی ثابت آفلاین).
- **تاخیر اضافه:** کمتر از ۶ میکروثانیه (+0.006 ms).

</div>

