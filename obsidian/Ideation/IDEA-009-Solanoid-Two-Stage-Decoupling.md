---
title: "IDEA-009: Solanoid Two-Stage Decoupling (Host Genus Filtering before Pathology)"
type: idea
idea_id: IDEA-009
phase: 1
tags:
  - idea
  - research/phase-1
  - solanoid
  - hierarchy
status: rejected
empirical_result: "Solanoid accuracy dropped from 42.57% to 39.60% (overall Top-1 53.97%). Intra-Solanoid errors are 91% intra-tomato pathology confusions, not potato leakage. Two-stage splitting fragments covariance support."
validation_log: "[[Logs/Log-Solanoid-Ceiling-Validation]]"
expected_gain: "+4% to +8% within Solanoid (resolves Tomato vs Potato pathogen confusion)"
mechanism: "Two-stage sub-clustering: separates Solanum lycopersicum from Solanum tuberosum before fine-grained disease classification"
created: 2026-11-08
---

<div dir="rtl" style="font-family: inherit;">

# 💡 IDEA-009: تفکیک دو مرحله‌ای سولانوئید (فیلتر میزبان گوجه/سیب‌زمینی پیش از پاتولوژی)

## ۱. فرضیه علمی (Scientific Hypothesis)
در کهن‌الگوی سولانوئید (۱۰ کلاس)، پاتوژن‌های مشترک (مانند *Alternaria solani* عامل Early Blight و *Phytophthora infestans* عامل Late Blight) هم در گوجه و هم در سیب‌زمینی وجود دارند. این اشتراک زیستی باعث سردرگمی مدل و جابجایی برچسب بین گوجه و سیب‌زمینی می‌شود.
**فرضیه:** اگر درون کهن‌الگوی سولانوئید، ابتدا با استفاده از ویژگی‌های ساختاری DINOv2 برگ گوجه (برگچه‌های دندانه‌دار عمیق) از برگ سیب‌زمینی (برگچه‌های پهن‌تر و بیضوی) تفکیک شود و سپس طبقه‌بندهای فیشر تخصصی ۸ کلاسه گوجه و ۲ کلاسه سیب‌زمینی اجرا شوند، خطای جابجایی پاتوژن مشترک حذف شده و دقت کهن‌الگو جهش خواهد یافت.

## ۲. مکانیزم اعتبارسنجی تجربی
- اعمال فیلتر دو مرحله‌ای در کهن‌الگوی سولانوئید: (۱) تشخیص گوجه در برابر سیب‌زمینی، (۲) طبقه‌بندی بیماری تخصصی میزبان.
- مقایسه دقت کهن‌الگوی سولانوئید و کل PlantDoc.

## ۳. نتیجه ارزیابی تجربی (Empirical Verdict)
> [!CAUTION] رد فرضیه (Rejected)
> - **دقت کهن‌الگوی سولانوئید:** از ۴۲.۵۷٪ به **۳۹.۶۰٪** افت کرد (-۲.۹۷٪ افت).
> - **دقت کل Top-1:** ۵۳.۹۷٪.
> - **دلیل شکست:** تحلیل دقیق نشان داد که ۹۱٪ خطاهای گوجه‌فرنگی ناشی از سردرگمی بین ۸ بیماری گوجه است (مانند لکه سپتوریا در برابر لکه باکتریایی) و فقط ۳ نمونه به سیب‌زمینی نشت کرده است. تفکیک به ۲ زیرخوشه، ماتریس کوواریانس انقباضی فیشر را تکه‌تکه (Fragment) کرده و واریانس را افزایش می‌دهد.
> - گزارش کامل: [[Logs/Log-Solanoid-Ceiling-Validation|گزارش ارزیابی سقف سولانوئید]].

---
- 📌 بازگشت به [[Ideation/Index|فهرست ایده‌ها]]

</div>

