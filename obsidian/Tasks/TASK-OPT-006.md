---
title: "TASK-OPT-006: Multi-Exemplar Soft-Nearest-Neighbor Prototype Aggregation"
type: task
task_id: TASK-OPT-006
phase: 4
tags:
  - task
  - research/phase-4
  - few-shot
  - multi-prototype
  - ponytail
status: todo
priority: High
depends_on: "TASK-OPT-005"
blocks: "TASK-OPT-011"
spec: "Specs/SPEC-MORPHOPATH-001.md"
idea: "Ideation/IDEA-012-Multi-Exemplar-Soft-Prototype.md"
created: 2026-11-11
---

<div dir="rtl" style="font-family: inherit;">

# 📌 TASK-OPT-006: پیاده‌سازی و ارزیابی تجمیع چند-نمونه‌ای سافت (Multi-Exemplar Soft-NN)

## ۱. هدف و صورت مسئله
جلوگیری از محو شدن فازهای بیماری (لکه‌های اولیه در برابر سوختگی‌های نکروتیک شدید) از طریق تجمیع سافت شات‌های ۵ گانه به جای میانگین‌گیری ساده، بدون افزودن حتی یک وزن عصبی جدید (0.0 MB).

## ۲. دستورالعمل پیاده‌سازی در موتور
1. در `pipeline/morphopath_math.py` یا `pipeline/morphopath_engine.py`:
   - حفظ آرایه ساپورت نرمال‌شده $S \in \mathbb{R}^{K \times 5 \times D}$.
   - محاسبه ضرب ماتریسی شباهت با نمونه‌ها: $S_{c,j} = \cos(q, x_{c,j})$.
   - تجمیع با تابع LogSumExp:
     $$S_c^{\text{multi}} = \frac{1}{\tau_{\text{ex}}} \ln \left( \frac{1}{k} \sum_{j=1}^k \exp(\tau_{\text{ex}} \cdot S_{c,j}) \right)$$
   - بررسی مقدار بهینه $\tau_{\text{ex}}$ در بازه $[5.0, 20.0]$.
2. سنجش روی دادگان `plantdoc_features_seed42.pt` و `plantvillage_features_pool.pt`.
3. بررسی شرط پذیرش: اگر دقت Top-1 در PlantDoc ارتقا یافت و تاخیر هد زیر ۰.۲۵ میلی‌ثانیه ماند، حفظ شود؛ در غیر این صورت، گزارش عدم کارایی ثبت و غیرفعال گردد.

</div>

