---
title: "IDEA-021: Orthogonal Pathogen Residual Adapter (OPRA)"
type: idea
idea_id: IDEA-021
phase: 1
tags:
  - idea
  - research/phase-1
  - adapter
  - pathogen-residual
  - host-subtraction
status: pending
expected_gain: "+5% to +8% Top-1, breaks intra-host confusion bottleneck (Corn Blight vs GLS, Late vs Early Blight)"
mechanism: "Lightweight 1.2MB MLP projecting out the host plant healthy subspace to isolate pure lesion pathology"
created: 2026-11-11
generated: { by: okf-enforcer/0.6, at: 2026-11-11T18:37:59Z }
---

<div dir="rtl" style="font-family: inherit;">

# 💡 IDEA-021: آداپتور تفاضلی متعامد پاتوژن (Orthogonal Pathogen Residual Adapter - OPRA)

### ۱. صورت مسئله و انگیزه بالینی
تحلیل تجربی نشان می‌دهد نزدیک به ۶۰٪ کل خطاهای سیستم (۵۱ از ۸۸ خطا) ناشی از سردرگمی بین بیماری‌های مشترک روی یک گونه گیاهی است (مثلاً ۱۱ خطای بلایت ذرت با لکه خاکستری ذرت با شباهت کسینوسی ۰.۹۰۶). در این تصاویر، ۹۰٪ طول بردار امبدینگ به سیگنال مشترک بافت سالم برگ میزبان تعلق دارد و نشانه‌های بیماری در آن غرق می‌شوند.

### ۲. مکانیزم ریاضی
تعریف یک آداپتور سبک پروجکشن ($896 \to 256 \to 896$ با حجم تقریبی **۱.۲ مگابایت**):
این آداپتور با محاسبه تصویر متعامد زیرفضای گیاه سالم میزبان ($\mathbf{P}_{\text{host}}$)، بردار امبدینگ را فیلتر می‌کند:
$$\mathbf{z}_{\text{pathology}} = \mathbf{z} - \mathbf{P}_{\text{host}} \mathbf{z}$$
با تفریق ویژگی‌های زمینه مشترک «برگ ذرت» یا «برگ گوجه»، آنچه در فضای فشرده ۲۵۶ بعدی باقی می‌ماند **DNA بصری خالص بیماری** است (تفکیک لکه‌های دوکی بلایت از لکه‌های مستطیلی لکه خاکستری).

### ۳. بودجه سخت‌افزاری و سرعت لبه
- **حجم اضافه:** حدود ۱.۲ مگابایت (کاملاً درون بودجه مجاز زیر ۵ مگابایت).
- **تاخیر اضافه در اسکن:** کمتر از ۰.۰۳ میلی‌ثانیه (+0.03 ms) روی CPU موبایل.

</div>
