---
title: "IDEA-018: Closed-Form 2-Point Wasserstein Optimal Transport Metric"
type: idea
idea_id: IDEA-018
phase: 1
tags:
  - idea
  - research/phase-1
  - optimal-transport
  - wasserstein
  - energy-distance
status: pending
expected_gain: "+0.4% to +0.8% Top-1 on PlantDoc, models foliar morphological deformation energy"
mechanism: "Closed-form 2-point Optimal Transport distance penalizing structural deformation between morphology and pathology"
created: 2026-11-11
generated: { by: okf-enforcer/0.6, at: 2026-11-11T16:03:10Z }
---

<div dir="rtl" style="font-family: inherit;">

# 💡 IDEA-018: فاصله انرژی ترابری بهینه واسرشتاین فرم‌بسته ۲ نقطه‌ای

### ۱. انگیزه و بیان مسئله
ترکیب خطی یا اقلیدسی سنتی، ویژگی‌های پاتولوژی (BioCLIP) و هندسه (DINOv2) را بردارهای جداگانه‌ای می‌بیند. اما در دیدگاه ترابری بهینه فیزیکی، کوئری و پروتوتایپ دو توزیع جرمی گسسته هستند: $\mu = 0.65 \delta_{\text{bio}} + 0.35 \delta_{\text{dino}}$.

### ۲. مکانیزم ریاضی
محاسبه فاصله واسرشتاین $W_2$ فرم‌بسته تحلیلی جهت سنجش حداقل کار مکانیکی برای نگاشت هندسه برگ به فرم پاتولوژیک:
$$\mathcal{W}_2^2(\mu_q, \mu_c) = 0.65 \|\mathbf{q}_{\text{bio}} - \mathbf{p}_{c,\text{bio}}\|^2 + 0.35 \|\mathbf{q}_{\text{dino}} - \mathbf{p}_{c,\text{dino}}\|^2 - 2\sqrt{0.65 \times 0.35} \, \mathbf{q}_{\text{bio}}^T \mathbf{p}_{c,\text{dino}}$$
اگر ساختار رگبرگی مانع از بروز آن الگوی ضایعه باشد، هزینه ترابری جهش می‌کند و خطای تشخیص خنثی می‌شود.

### ۳. بودجه لبه
- **وزن اضافه:** ۰.۰ مگابایت.
- **تاخیر اضافه:** کمتر از ۳ میکروثانیه (+0.003 ms).

</div>
