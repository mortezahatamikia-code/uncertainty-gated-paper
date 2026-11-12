---
title: "TASK-OPT-019: Spatial Lesion Patch Attention Slicing (Loupe Mechanism)"
type: task
task_id: TASK-OPT-019
phase: 4
tags:
  - task
  - research/phase-4
  - patch-tokens
  - vision-transformer
  - spatial-attention
  - breakthrough-72
status: rejected
priority: High
depends_on: "TASK-OPT-016"
blocks: "TASK-OPT-021"
spec: "Specs/SPEC-MORPHOPATH-001.md"
idea: "IDEA-023-Spatial-Lesion-Patch-Attention-Slicing.md"
created: 2026-11-11
updated: 2026-11-11
generated: { by: okf-enforcer/0.6, at: 2026-11-11T20:03:29Z }
---

<div dir="rtl" style="font-family: inherit;">

# 📌 TASK-OPT-019: ارزیابی اسلایسینگ توکن‌های پچ فضایی (Loupe Mechanism) - [مردود / REJECTED]

## ۱. هدف و صورت مسئله
تلاش برای استخراج ۱۹۶ توکن پچ ViT و بزرگنمایی روی ۱۰٪ پچ‌های ناهنجاری نکروتیک بدون اجرای مجدد شبکه به منظور جلوگیری از رقیق‌شدگی سیگنال ضایعه توسط بافت سالم برگ.

## ۲. نتایج ارزیابی تجربی (Empirical Benchmark & Token Audit)
- **Top-1 Accuracy:**
  - پایه توکن CLS سراسری: ۵۲.۳۸٪ (در پایپ‌لاین سلسله‌مراتبی فاز ۱).
  - میانگین‌گیری یکنواخت پچ‌ها (Mean Patch Pooling): **۴۸.۴۱٪** (-۳.۹۷٪ افت).
  - توجه وزن‌دار برجستگی (Soft Saliency Patch Pooling): **۴۸.۸۱٪** (-۳.۵۷٪ افت).
  - آستانه‌گذاری ۵۰٪ پچ‌های پیش‌زمینه (Hard Top-50%): **۴۹.۶۰٪** (-۲.۷۸٪ افت).
  - ادغام CLS و Saliency: **۵۱.۹۸٪** (-۰.۴۰٪ افت).
- **Scanning Latency:** > ۱۸۵ میلی‌ثانیه بر روی پردازنده لبه (نقض شدید شرط کاربر: سقوط FPS به زیر ۵ فریم بر ثانیه!).
- **Memory Overhead:** نگهداری ۱۹۶ توکن در رم نیازمند بیش از ۲۰۰ مگابایت کش برداری است (بیش از ۴۰ برابر سقف مجاز ۵ مگابایت).

## ۳. تحلیل علل شکست ریاضی و گیاه‌پزشکی (Mathematical & Biological Post-Mortem)
1. **از دست رفتن بافت کلی ساختار برگ (Loss of Global Spatial Morphology):** تک‌تک پچ‌های ۱۶×۱۶ در فضای توکن‌های نهایی ViT، زمینه کانتور برگ و جهت‌گیری آوندها را از دست می‌دهند. پچ‌های حاشیه برگ و سایه‌روشن‌های خاک به شدت با علائم نکروز اشتباه گرفته می‌شوند.
2. **نقض سهمگین بودجه محاسباتی سخت‌افزار لبه:** استخراج و مقایسه ماتریسی ۱۹۶ توکن برای هر فریم، تاخیر اسکن دوربین را از ۰.۱۶ میلی‌ثانیه به بیش از ۱۸۵ میلی‌ثانیه افزایش می‌دهد و تجربه کاربری نرم‌افزار موبایل را به طور کامل فلج می‌کند.

## ۴. تصمیم نهایی
ایده به طور قطعی **مردود (Rejected)** اعلام شد.

</div>
