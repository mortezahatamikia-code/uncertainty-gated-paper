---
title: "IDEA-022: Fine-Grained Clinical Concept Bottleneck Matrix (CBM)"
type: idea
idea_id: IDEA-022
phase: 1
tags:
  - idea
  - research/phase-1
  - concept-bottleneck
  - xai
  - pathology-keys
status: pending
expected_gain: "+3% to +5% Top-1, 100% explainable botanical lesion attributes"
mechanism: "25 atomic pathological micro-symptom prompts mapped through botanical diagnostic decision matrix"
created: 2026-11-11
generated: { by: okf-enforcer/0.6, at: 2026-11-11T18:38:44Z }
---

<div dir="rtl" style="font-family: inherit;">

# 💡 IDEA-022: بطری‌گردن مفاهیم تشخیصی گیاه‌پزشکی (Clinical Concept Bottleneck Matrix - CBM)

### ۱. صورت مسئله و انگیزه
مدل‌های طبقه‌بندی سنتی تلاش می‌کنند کل تصویر را یکباره به نام کلاس مپ کنند. در گیاه‌پزشکی، تشخیص بر اساس «کلیدهای دوگانه عوارض بالینی» (Dichotomous Lesion Keys) انجام می‌شود: آیا ضایعه دارای حاشیه بافت‌مرده آغشته‌به‌آب است؟ آیا لکه بین دو رگبرگ موازی محبوس شده است؟

### ۲. مکانیزم ریاضی
تعریف ۲۵ پرامپت اتمی برای نشانه‌های میکروسکوپی در BioCLIP (نظیر `cigar_shaped_elliptical_lesion`, `rectangular_vein_delimited_lesion`, `concentric_target_board_rings`, `water_soaked_greasy_halo`).
تشخیص بر اساس ضرب ماتریس تطابق بالینی $\mathbf{M} \in \mathbb{R}^{27 \times 25}$ صورت می‌گیرد:
$$P(\text{class}) = \text{Softmax}\left( \mathbf{M} \cdot \cos(\mathbf{q}_{\text{bio}}, \mathbf{T}_{\text{concepts}}) \right)$$

### ۳. بودجه سخت‌افزاری و سرعت لبه
- **حجم اضافه:** کمتر از ۰.۰۵ مگابایت (تنها ۵۰ کیلوبایت ماتریس ثابت).
- **تاخیر اضافه در اسکن:** کمتر از ۰.۰۰۸ میلی‌ثانیه (+0.008 ms).

</div>
