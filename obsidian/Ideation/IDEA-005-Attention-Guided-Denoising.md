---
title: "IDEA-005: DINOv2 Saliency-Guided Background Denoising"
type: idea
idea_id: IDEA-005
phase: 1
tags:
  - idea
  - research/phase-1
  - attention
  - vision
status: rejected
expected_gain: "+3% to +6% reduction in background noise interference (hands, soil, weeds)"
mechanism: "Unsupervised multi-head self-attention rollout mask from DINOv2 for foliar foreground isolation"
created: 2026-11-08
---

<div dir="rtl" style="font-family: inherit;">

# 💡 IDEA-005: ماسک‌گذاری خودتوجهی DINOv2 برای حذف نویز پس‌زمینه مزرعه

## ۱. فرضیه علمی (Scientific Hypothesis)
در تصاویر غیرآزمایشگاهی PlantDoc، پس‌زمینه تصویر (شامل دست کشاورز، خاک مزرعه، ساقه‌های خشک و علف‌های هرز مجاور) بخش قابل‌توجهی از ابعاد بردار ویژگی را اشغال و مسموم می‌کند.
**فرضیه:** از آنجا که DINOv2 دارای نقشه‌های خودتوجهی (Self-Attention Maps) پدیدار شونده است که سوژه اصلی (برگ) را به طور ذاتی تفکیک می‌کند، استفاده از نقشه توجه هد آخر لایه ۱۲ به عنوان ماسک فیلترکننده پچ‌های پس‌زمینه (Attention Rollout Saliency) بدون نیاز به شبکه بخش‌بندی مجزا، اثر نویز مزرعه را حذف و دقت بیماری‌ها را ارتقا می‌دهد.

## ۲. مکانیزم اعتبارسنجی تجربی
- استخراج وزن‌های خودتوجهی توکن [CLS] به پچ‌ها در DINOv2 Small.
- مقایسه بردار ویژگی برگ با و بدون وزن‌دهی توجهی در تفکیک بیماری‌های PlantDoc.

---
- 📌 بازگشت به [[Ideation/Index|فهرست ایده‌ها]]

</div>

