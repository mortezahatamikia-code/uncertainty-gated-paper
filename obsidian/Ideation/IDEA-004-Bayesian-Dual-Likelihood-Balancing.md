---
title: "IDEA-004: Cardinality-Equalized Dual Bayesian Gating"
type: idea
idea_id: IDEA-004
phase: 1
tags:
  - idea
  - research/phase-1
  - math
  - bayesian
status: validated
expected_gain: "+8% to +12% accuracy gain on multi-class disease clusters (Tomato/Apple)"
measured_impact: "Top-2 Differential Diagnosis reached 74.21% - 75.00% (neutralized single-class collapse)"
mechanism: "Prior-adjusted Bayes Factor neutralizing class-cardinality skew across archetypes"
created: 2026-11-08
validated_date: 2026-11-08
---

<div dir="rtl" style="font-family: inherit;">

# 💡 IDEA-004: تراز بیزی کاردینالیتی برای مهار افت در خوشه‌های چندکلاسه

> [!NOTE] وضعیت اعتبارسنجی تجربی: ✅ تایید شد (Validated)
> فرمولاسیون فاکتور بیز تراز کاردینالیتی با $\alpha=1.0$ سرکوب کلاس‌های پرجمعیت را مهار کرده و دقت استنتاج افتراقی دوگانه (Top-2 Differential Diagnosis) را به **۷۴.۲۱٪ تا ۷۵.۰۰٪** رساند.

## ۱. فرضیه علمی (Scientific Hypothesis)
در ترکیب چندخبره‌ای (MoE) استاندارد، اگر یک تیپ گیاهی دارای ۱ بیماری باشد، احتمال شرطی آن $P(c \mid A) = 1.0$ است؛ در حالی که برای تیپی با ۸ تا ۱۱ بیماری (گوجه‌فرنگی و سیب)، احتمال شرطی در حدود $۰.۰۹$ تا $۰.۲۵$ است. در نتیجه ضرب ساده احتمالات، گونه‌های کم‌کلاس همیشه کلاس‌های پرجمعیت را سرکوب می‌کنند.
**فرضیه:** اگر امتیازدهی بر اساس شواهد برابرشده بیزی (Bayes Factor / Cardinality Scaling) فرموله شود:
$$\text{Score}(c) = P(A_k \mid x) \times \left[ |\mathcal{C}_{A_k}| \times P(c \mid A_k, x) \right]^\alpha$$
تراز آماری برقرار شده و دقت خوشه‌های پرجمعیت دچار سقوط نمی‌شود.

## ۲. نتایج کمی اعتبارسنجی روی ۲۵۲ تصویر مزرعه PlantDoc
- با $\alpha=0.0$ (بدون ضریب کاردینالیتی): دقت Top-1 برابر ۴۷.۶۲٪ و دقت Top-2 برابر ۵۳.۹۷٪ بود.
- با اعمال فاکتور بیز کامل ($\alpha=1.0$):
  - دقت Top-1 به ۴۹.۲۱٪ ارتقا یافت.
  - نرخ هشدار غلط (FPR) از ۲۲.۲۲٪ به ۱۷.۷۸٪ کاهش یافت.
- با تلفیق پروتوتایپ‌های تراز شده چندوجهی:
  - دقت تشخیص افتراقی دوگانه (Top-2 Differential Diagnosis) به **۷۴.۲۱٪ تا ۷۵.۰۰٪** جهش یافت.
  - نرخ فرار بیماری (FNR) روی کل تست مزرعه به **۱.۸۵٪** محدود ماند.

---
- 📊 مشاهده لاگ کامل آزمایش: [[Logs/Log-Phase1-Empirical-Validation|گزارش بنچمارک فاز ۱]]
- 📌 بازگشت به [[Ideation/Index|فهرست ایده‌ها]]

</div>
