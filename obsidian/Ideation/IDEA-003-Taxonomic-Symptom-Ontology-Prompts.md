---
title: "IDEA-003: Micro-Symptom Textual Prompt Engineering for BioCLIP"
type: idea
idea_id: IDEA-003
phase: 1
tags:
  - idea
  - research/phase-1
  - nlp
status: validated_conditioned
expected_gain: "+5% to +9% zero-shot symptom alignment across similar necrotic lesions"
measured_impact: "+2.97% gain in Solanoid intra-cluster, +2.53% in Tomato 8-disease complex, +0.79% overall few-shot"
mechanism: "Domain-specific pathological symptom descriptors (pycnidia, target-rings, water-soaked)"
created: 2026-11-08
validated_date: 2026-11-08
---

<div dir="rtl" style="font-family: inherit;">

# 💡 IDEA-003: مهندسی پرامپت میکرومورفولوژیک عوارض بیماری در BioCLIP

> [!NOTE] وضعیت اعتبارسنجی تجربی: ⚠️ تایید مشروط به بستر گونه (Validated with Conditioning)
> پرامپت‌های صرفاً عارضه‌محور بدون نام میزبان به صورت سراسری دچار خطا می‌شوند (۱۱.۱۱٪)، اما وقتی درون تیپ ریخت‌شناسی یا کلاستر گیاهی اعمال شوند، تفکیک بیماری‌های بسیار مشابه را تقویت می‌کنند (**+۲.۹۷٪ در Solanoid** و **+۲.۵۳٪ در گوجه‌فرنگی**).

## ۱. فرضیه علمی (Scientific Hypothesis)
پرامپت‌های متعارف BioCLIP معمولاً بر نام تاکسونومیک گونه و بیماری تمرکز دارند.
**فرضیه اولیه:** پرامپت‌های آسیب‌شناسی متمرکز بر بافت و فرم لکه (مانند *concentric target-board rings* برای بلایت آلترناریا، *circular grayish lesions with black pycnidia specks* برای سپتوریا، و *angular greasy water-soaked halos* برای باکتریال) تفاوت عوارض بافتی را استخراج می‌کنند.

## ۲. نتایج کمی بنچمارک فاز ۱
- **سراسری بدون قید گونه (Global 27-Class Zero-Shot):** سقوط به ۱۱.۱۱٪ (زیرا لکه آب‌سوخته یا نکروز میان گیاهان مختلف شباهت متنی دارد).
- **درون‌خوشه‌ای مقید (Intra-Cluster Fine-Grained):**
  - کلاستر ۸ بیماری گوجه‌فرنگی: ارتقا از ۱۲.۶۶٪ به **۱۵.۱۹٪ (+۲.۵۳٪ جهش)**
  - تیپ ۱۰ کلاسه Solanoid: ارتقا از ۱۱.۸۸٪ به **۱۴.۸۵٪ (+۲.۹۷٪ جهش)**
  - انسامبل ۵ شات چندوجهی (Fused + Text): افزایش دقت کل از ۵۳.۱۷٪ به **۵۳.۹۷٪ (+۰.۷۹٪)**
- **نتیجه‌گیری راهبردی فاز ۲:** پرامپت‌ها باید به شکل تلفیقی (Hybrid: گونه + عارضه پاتولوژیک بافتی) استفاده شوند تا دقت پایدار بماند.

---
- 📊 مشاهده لاگ کامل آزمایش: [[Logs/Log-Phase1-Empirical-Validation|گزارش بنچمارک فاز ۱]]
- 📌 بازگشت به [[Ideation/Index|فهرست ایده‌ها]]

</div>
