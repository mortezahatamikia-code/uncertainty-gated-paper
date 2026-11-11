---
title: "IDEA-015: Cross-Subspace Bilinear Gating (Morphology-Pathology Co-occurrence Filter)"
type: idea
idea_id: IDEA-015
phase: 1
tags:
  - idea
  - research/phase-1
  - subspace
  - bilinear-gating
status: pending
expected_gain: "+0.4% to +0.9% Top-1 on PlantDoc, eliminates cross-genus false alarms"
mechanism: "Multiplicative hyperbolic modulation amplifying pathology score only when structural morphology matches"
created: 2026-11-11
---

<div dir="rtl" style="font-family: inherit;">

# 💡 IDEA-015: دروازه‌بانی دوخطی زیرفضاها (Cross-Subspace Bilinear Gating)

### ۱. انگیزه و بیان مسئله
ترکیب خطی ایستا ($0.65 S_{\text{bio}} + 0.35 S_{\text{dino}}$) فرض می‌کند هندسه کلان برگ و نشانه‌شناسی آسیب سلولی، دو متغیر مستقل جمع‌پذیر هستند. در حالی که در زیست‌شناسی، یک ضایعه پاتولوژیک خاص در صورت ناهمخوانی کامل با ساختار برگ میزبان، باید به شدت جریمه شود نه اینکه با امتیاز بالا امتیاز کلی را به نفع خود منحرف کند.

### ۲. مکانیزم پیشنهادی
اعمال گیتینگ غیرخطی ضربی ملایم بدون افزودن لایه وزن:
$$S_{\text{final}}(q, c) = S_{\text{bio}}(q, c) \cdot \left( 1 + \alpha \cdot \tanh(S_{\text{dino}}(q, c)) \right) \quad (\alpha \approx 0.20)$$
در صورتی که تطابق هندسی مثبت باشد، امتیاز پاتولوژی تقویت شده و در صورت تناقض ساختاری، امتیاز افت می‌کند.

### ۳. بودجه و محدودیت لبه
- **وزن اضافه:** ۰.۰ مگابایت.
- **تاخیر اضافه:** کمتر از ۴ میکروثانیه (+0.004 ms).

</div>

