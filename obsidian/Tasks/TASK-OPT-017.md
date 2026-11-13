---
title: "TASK-OPT-017: Orthogonal Pathogen Residual Adapter (OPRA)"
type: task
task_id: TASK-OPT-017
phase: 4
tags:
  - task
  - research/phase-4
  - adapter
  - pathogen-residual
  - host-subtraction
  - breakthrough-72
status: rejected
priority: Critical
depends_on: "TASK-OPT-016"
blocks: "TASK-OPT-021"
spec: "Specs/SPEC-MORPHOPATH-001.md"
idea: "Ideation/IDEA-021-Orthogonal-Pathogen-Residual-Adapter.md"
created: 2026-11-11
updated: 2026-11-11
generated: { by: okf-enforcer/0.6, at: 2026-11-11T19:58:47Z }
---

<div dir="rtl" style="font-family: inherit;">

# 📌 TASK-OPT-017: ارزیابی تجربی آداپتور تفاضلی متعامد پاتوژن (OPRA) - [مردود / REJECTED]

## ۱. هدف و صورت مسئله
تلاش برای حذف سیگنال زمینه برگ گیاه میزبان سالم از طریق تفریق بردار پروجکشن زیرفضای میزبان ($\mathbf{z}_{\text{pathology}} = \mathbf{z} - \lambda \mathbf{P}_{\text{host}} \mathbf{z}$) جهت ارتقای تمایز بین بیماری‌های هم‌میزبان.

## ۲. نتایج ارزیابی تجربی (Empirical Benchmark)
- **Top-1 Accuracy:** افت از ۶۵.۰۸٪ به **۵۹.۹۲٪** در $\lambda=0.05$ (افت ۵.۱۶٪) و **۵۷.۹۴٪** در $\lambda=0.50$ (افت ۷.۱۴٪).
- **Macro F1-Score:** افت از ۶۳.۵۲٪ به ۵۹.۳۰٪.
- **Scanning Latency:** ۰.۱۷۵۹ میلی‌ثانیه (+0.015 ms overhead).
- **Added Weights:** ۱.۷۵ مگابایت.

## ۳. تحلیل علل شکست ریاضی و گیاه‌پزشکی (Mathematical & Biological Post-Mortem)
1. **غیرخطی بودن فرآیند نکروز سلولی:** بر خلاف فرضیه جمع‌پذیر خطی ($z = z_{\text{host}} + \Delta z_{\text{pathology}}$)، هجوم قارچ‌ها و باکتری‌ها موجب تجزیه کلروفیل و تغییر بنیادین ساختار مزوفیل برگ می‌شود. تفریق زیرفضای برگ سالم، بردار پاتولوژی را تخریب کرده و آن را از منیفولد طبیعی خارج می‌سازد.
2. **از بین رفتن مهار تاکسونومیک گونه (Taxonomic Anchoring):** ویژگی‌های زمینه برگ سالم حامل اطلاعات حیاتی آرک‌تایپ فولیار (مانند رگبرگ‌های موازی تک‌لپه‌ای‌ها) هستند. حذف این بردارها باعث جهش کوئری‌ها به کلاس‌های بی‌ارتباط سایر گونه‌ها (مانند اشتباه گرفتن لکه بلک‌روت انگور با اسکب سیب) گردید.

## ۴. تصمیم نهایی
ایده **مردود (Rejected)** اعلام شد و کد اصلی خط لوله بدون آلودگی حفظ گردید.

</div>
