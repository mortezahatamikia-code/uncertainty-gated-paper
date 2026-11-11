---
title: "IDEA-014: Cardinality-Scaled Ledoit-Wolf Covariance Shrinkage & Directional Whitening"
type: idea
idea_id: IDEA-014
phase: 1
tags:
  - idea
  - research/phase-1
  - covariance
  - lda
  - shrinkage
status: pending
expected_gain: "+0.8% to +1.4% Top-1 on PlantDoc, sharpens intra-Solanoid discrimination"
mechanism: "Archetype-dependent shrinkage parameter lambda_a = clip(kappa / sqrt(N_a), 0.30, 0.85) in fit()"
created: 2026-11-11
---

<div dir="rtl" style="font-family: inherit;">

# 💡 IDEA-014: انقباض کوواریانس متناسب با کاردینالیتی کهن‌الگو و سفیدسازی جهت‌دار

### ۱. انگیزه و بیان مسئله
در حال حاضر پارامتر انقباض کوواریانس به صورت ثابت ($\lambda = 0.60$) برای تمام ۴ کهن‌الگو اعمال می‌شود. اما کهن‌الگوی سولانوئید دارای ۱۰ کلاس (۵۰ شات ساپورت) است که در آن $\lambda=0.60$ بیش از حد کوواریانس را صاف و جهت‌های تمایز ظریف گوجه را محو می‌کند؛ در حالی که کهن‌الگوی تک‌لپه‌ای تنها ۳ کلاس (۱۵ شات) دارد و نیازمند انقباض بالاتری است تا ماتریس تکین نشود.

### ۲. مکانیزم پیشنهادی
محاسبه انقباض بهینه به تفکیک هر کهن‌الگو بر پایه تعداد شات‌های ساپورت در متد `.fit()`:
$$\lambda_a = \mathrm{clip}\left( \frac{\kappa}{\sqrt{N_a}}, 0.30, 0.85 \right)$$
در کهن‌الگوی سولانوئید با ۵۰ نمونه، ضریب انقباض به حدود ۰.۳۵ کاهش یافته و دقت تفکیک خطی فیشر (Fisher LDA) به صورت چشمگیری بالا می‌رود.

### ۳. بودجه و محدودیت لبه
- **وزن اضافه:** ۰.۰ مگابایت.
- **تاخیر اضافه:** ۰.۰ میلی‌ثانیه در زمان استنتاج (در زمان راه‌اندازی متد `.fit()` محاسبه می‌شود).

</div>

