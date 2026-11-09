---
title: "IDEA-008: Dual-Scale Micro-Lesion Crop Fusion"
type: idea
idea_id: IDEA-008
phase: 1
tags:
  - idea
  - research/phase-1
  - multi-scale
  - vision
status: rejected
expected_gain: "+3% to +7% resolution preservation of diagnostic micro-lesions (pycnidia, concentric rings)"
mechanism: "Parallel zero-parameter feature concatenation of global leaf context (224x224) and high-magnification center lesion crop (224x224)"
created: 2026-11-08
---

<div dir="rtl" style="font-family: inherit;">

# 💡 IDEA-008: فیوژن دوقیاسی ضایعات میکروسکوپی (Dual-Scale Micro-Lesion Crop Fusion)

## ۱. فرضیه علمی (Scientific Hypothesis)
هنگامی که تصویر اصلی مزرعه با ابعاد بزرگ (مثلاً $1024 \times 1024$) مستقیماً به $224 \times 224$ ریسایز می‌شود، علائم میکروسکوپی تشخیصی مانند حلقه‌های هم‌مرکز Early Blight یا نقاط سیاه سپتوریا (Pycnidia) در میان پیکسل‌های فشرده‌شده محو می‌شوند.
**فرضیه:** استخراج ویژگی در دو مقیاس: (۱) نمای سراسری کل برگ ($224 \times 224$) برای تشخیص مورفولوژی و کهن‌الگو، و (۲) برش بزرگنمایی‌شده مرکزی برگ ($224 \times 224$) برای تحلیل ضایعات میکروسکوپی، و سپس الحاق یا میانگین‌گیری ویژگی‌ها بدون هیچ لایه عصبی جدید، دقت تشخیص بیماری‌های ظریف را ارتقا می‌دهد بدون آنکه پارامتری به مدل اضافه شود.

## ۲. مکانیزم اعتبارسنجی تجربی
- استخراج ویژگی‌های برش سراسری و برش ۷۰٪ مرکزی روی تصاویر PlantDoc.
- ارزیابی عملکرد سیستم تشخیص مورفوپث تحت ادغام دو قیاس.

---
- 📌 بازگشت به [[Ideation/Index|فهرست ایده‌ها]]

</div>

