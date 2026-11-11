---
title: "IDEA-012: Multi-Exemplar Soft-Nearest-Neighbor Prototype Aggregation"
type: idea
idea_id: IDEA-012
phase: 1
tags:
  - idea
  - research/phase-1
  - few-shot
  - multi-prototype
status: pending
expected_gain: "+1.0% to +1.8% Top-1 on PlantDoc, resolves multi-stage disease phenotype blur"
mechanism: "LogSumExp soft-max aggregation across all 5 support exemplars per class instead of rigid arithmetic centroid"
created: 2026-11-11
---

<div dir="rtl" style="font-family: inherit;">

# 💡 IDEA-012: تجمیع چند-نمونه‌ای سافت پروتوتایپ‌ها (Multi-Exemplar Soft-Nearest-Neighbor)

### ۱. انگیزه و بیان مسئله
در آموزش چندشات سنتی ($k=5$)، میانگین‌گیری حسابی $\mathbf{p}_c = \frac{1}{k}\sum \mathbf{x}_i$ فرض می‌کند توزیع علائم هر بیماری در فضای ویژگی تک‌وجهی (Unimodal) است. در عمل، بیماری‌های گیاهی دارای فازهای فنوتیپی گوناگون هستند (مثلاً Early Blight دارای فاز لکه کوچک زرد اولیه و فاز سوختگی با حلقه‌های متحدالمرکز سیاه است). میانگین‌گیری ساده باعث ادغام و رقیق‌شدگی این فازها به یک بردار مصنوعی مبهم می‌شود.

### ۲. مکانیزم پیشنهادی
نگهداری تمام ۵ نمونه ساپورت در رم (که هم‌اکنون نیز در متغیر ساپورت بارگذاری شده‌اند و حجم اضافی **۰ بایت** است). برای هر کوئری $q$، محاسبه شباهت با تمام ۵ نمونه کلاس $c$ و تجمیع از طریق عملگر تحلیلی LogSumExp با دمای کنترل‌شده $\tau_{\text{ex}}$:
$$S_c^{\text{multi}} = \frac{1}{\tau_{\text{ex}}} \ln \left( \frac{1}{k} \sum_{j=1}^k \exp(\tau_{\text{ex}} \cdot \cos(\mathbf{q}, \mathbf{x}_{c,j})) \right)$$

### ۳. بودجه و محدودیت لبه
- **وزن اضافه:** ۰.۰ مگابایت (صفر پارامتر یادگیری‌شده).
- **تاخیر اضافه:** کمتر از ۱۵ میکروثانیه (+0.015 ms روی CPU موبایل).

</div>

