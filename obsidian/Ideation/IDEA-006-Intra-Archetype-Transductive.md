---
title: "IDEA-006: Intra-Archetype Transductive Prototype Recalibration"
type: idea
idea_id: IDEA-006
phase: 1
tags:
  - idea
  - research/phase-1
  - transductive
  - prototypes
status: rejected
expected_gain: "+4% to +8% intra-archetype accuracy under domain shift"
mechanism: "Unsupervised pseudo-label iterative refinement of support prototypes using test batch distribution within archetype"
created: 2026-11-08
---

<div dir="rtl" style="font-family: inherit;">

# 💡 IDEA-006: بازتنظیم ترنسداکتیو پروتوتایپ‌ها درون هر کهن‌الگو (Intra-Archetype Transductive Recalibration)

## ۱. فرضیه علمی (Scientific Hypothesis)
در سناریوی لبه‌ای، نور محیط، دوربین گوشی و مرحله بیماری در مزرعه با داده‌های آموزش (Support) تفاوت دامنه‌ای (Domain Shift) دارند.
**فرضیه:** اگر پس از انتساب نمونه‌ها به کهن‌الگوی مورفولوژیک (Archetype Router)، از کوئری‌های همان کهن‌الگو به صورت ترنسداکتیو (Transductive Prototype Adaptation یا Optimal Transport Sinkhorn) برای شیفت دادن مراکز دسته‌ها به سمت توزیع واقعی استفاده کنیم، تفکیک بیماری‌های بسیار شبیه به هم (نظیر Early Blight در برابر Late Blight در گوجه‌فرنگی) بدون نیاز به فاین‌تیونینگ یا افزایش حافظه تا حد چشمگیری بهبود می‌یابد.

## ۲. مکانیزم اعتبارسنجی تجربی
- اعمال یک مرحله به‌روزرسانی نرم کوئری‌ها بر روی پروتوتایپ‌های هر کلاستر کهن‌الگو ($P_c \leftarrow \alpha P_c + (1-\alpha) \sum w_{qc} q$).
- بررسی تغییر دقت در کهن‌الگوی سولانوئید (گوجه و سیب‌زمینی ۱۰ کلاسه) و کل مجموعه داده PlantDoc.

---
- 📌 بازگشت به [[Ideation/Index|فهرست ایده‌ها]]

</div>

