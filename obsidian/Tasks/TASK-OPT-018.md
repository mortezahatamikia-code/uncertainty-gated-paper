---
title: "TASK-OPT-018: Fine-Grained Clinical Concept Bottleneck Matrix (CBM)"
type: task
task_id: TASK-OPT-018
phase: 4
tags:
  - task
  - research/phase-4
  - concept-bottleneck
  - xai
  - pathology-keys
  - breakthrough-72
status: rejected
priority: High
depends_on: "TASK-OPT-016"
blocks: "TASK-OPT-021"
spec: "Specs/SPEC-MORPHOPATH-001.md"
idea: "Ideation/IDEA-022-Clinical-Concept-Bottleneck-Matrix.md"
created: 2026-11-11
updated: 2026-11-11
generated: { by: okf-enforcer/0.6, at: 2026-11-11T20:02:56Z }
---

<div dir="rtl" style="font-family: inherit;">

# 📌 TASK-OPT-018: ارزیابی بطری‌گردن مفاهیم تشخیصی بالینی (CBM) - [مردود / REJECTED]

## ۱. هدف و صورت مسئله
تلاش برای نگاشت ویژگی‌های تصویر روی ۲۵ توصیف‌گر اتمی عوارض پاتولوژی (لکه‌های دوکی، حلقه‌های تارگت‌بورد، هاله‌های آغشته به آب) از طریق ماتریس تصمیم دوگانه گیاه‌پزشکی $\mathbf{M} \in \mathbb{R}^{27 \times 25}$.

## ۲. نتایج ارزیابی تجربی (Empirical Benchmark)
- **Top-1 Accuracy:**
  - استفاده مستقل از CBM: تنها **۲۸.۵۷٪** تا **۳۰.۹۵٪** دقت!
  - ترکیب خطی با سقف SOTA فعلی: در وزن $w_{\text{cbm}}=0.10$ دقت به **۶۲.۳۰٪** افت کرد (-۲.۷۸٪).
- **Macro F1-Score:** افت از ۶۳.۵۲٪ به ۶۰.۸۹٪.
- **Scanning Latency:** ۰.۱۷۵۷ میلی‌ثانیه.
- **Added Weights:** ۳ کیلوبایت (ماتریس نگاشت).

## ۳. تحلیل علل شکست ریاضی و گیاه‌پزشکی (Mathematical & Biological Post-Mortem)
1. **دقت معنایی پایین فضای متنی صفر-داده در برابر تنوع مزرعه:** پرامپت‌های متنی BioCLIP در سطح زبان طبیعی فاقد وضوح هندسی لازم برای تفکیک ظرافت‌های طیفی مزرعه واقعی در شرایط سایه، بازتاب نور و آلودگی پس‌زمینه هستند.
2. **انباشت خطای چند-به-چند (Cross-Talk Dispersion):** بسیاری از علائم پاتولوژیک (مانند `water_soaked_halo` یا `chlorotic_halo`) بین باکتری‌های فلفل، بلایت دیررس سیب‌زمینی و پوسیدگی گوجه مشترک هستند. ماتریس خطی تصمیم‌گیری باعث ایجاد ابهام شدید در رتبه‌بندی کلاس‌ها و تشدید خطای نوع اول (FPR) شد.

## ۴. تصمیم نهایی
ایده **مردود (Rejected)** اعلام شد؛ فیوژن ریزنشانه‌های مستقیم فعلی با وزن $w_{\text{vis}}=0.75$ به عنوان بهینه پایدار حفظ شد.

</div>
