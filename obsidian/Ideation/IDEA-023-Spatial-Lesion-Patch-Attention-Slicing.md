---
title: "IDEA-023: Spatial Lesion Patch Attention Slicing (Loupe Mechanism)"
type: idea
idea_id: IDEA-023
phase: 1
tags:
  - idea
  - research/phase-1
  - patch-tokens
  - vision-transformer
  - spatial-attention
status: pending
expected_gain: "+4% to +6% Top-1, eliminates background leaf dilution via 10% lesion magnification"
mechanism: "Extracting top 10% highest-anomaly spatial patch tokens within the existing single ViT forward pass"
created: 2026-11-11
generated: { by: okf-enforcer/0.6, at: 2026-11-11T18:39:33Z }
---

<div dir="rtl" style="font-family: inherit;">

# 💡 IDEA-023: برش فضایی توکن‌های پچ بافت آسیب‌دیده (Spatial Lesion Patch Attention Slicing)

### ۱. صورت مسئله و انگیزه
در عکس‌های طبیعی مزرعه، اغلب ۸۰٪ مساحت تصویر شامل بافت سالم برگ، سایه یا خاک است و کانون بیماری تنها ۱۰ تا ۲۰ درصد تصویر را در بر می‌گیرد. توکن سراسری [CLS] تحت تاثیر میانگین‌گیری توجه کل تصویر رقیق می‌شود و لکه‌های ریز از دید پنهان می‌مانند.

### ۲. مکانیزم ریاضی
استفاده از تمام ۱۹۶ توکن پچ فضایی ViT که در همان یک فوروارد استاندارد تولید می‌شوند. محاسبه فاصله هر پچ با بردار پایه برگ سالم و انتخاب ۱۰٪ پچ‌هایی که بالاترین انحراف نکروتیک را دارند. میانگین این پچ‌ها به عنوان بردار «بزرگنمایی روی ضایعه» ($\mathbf{z}_{\text{lesion}}$) عمل می‌کند:
$$\mathbf{z}_{\text{final}} = \mathbf{z}_{\text{CLS}} + \beta \cdot \mathbf{z}_{\text{lesion}}$$
این فرایند کار ذره‌بین گیاه‌پزشک را بدون هیچ فوروارد مجدد شبیه‌سازی می‌کند.

### ۳. بودجه سخت‌افزاری و سرعت لبه
- **حجم اضافه:** ۰.۰ مگابایت (استفاده از توکن‌های از پیش تولید شده در لایه آخر ViT).
- **تاخیر اضافه در اسکن:** کمتر از ۰.۰۱۵ میلی‌ثانیه (+0.015 ms).

</div>
