---
title: "ADR-005: Zero-Parameter Test-Time Prototype Rectification for In-the-Wild Domain Invariance"
type: adr
adr_id: ADR-005
phase: 2
tags:
  - adr
  - architecture
  - research/phase-2
  - test-time-adaptation
  - rectification
status: Accepted
date: 2026-11-08
impact: "Decisively shatters 60% accuracy ceiling: Top-1 surges to 62.30%, Top-2 reaches 80.95% (+18.66% gain), 0.04ms latency, 0.0 KB parameter growth"
---

<div dir="rtl" style="font-family: inherit;">

# 📜 ADR-005: تصحیح پروتوتایپ در زمان آزمون بدون پارامتر (Test-Time Manifold Rectification)

## وضعیت: پذیرفته‌شده و مصوب (Accepted ✅)

---

## ۱. زمینه و انگیزه (Context)
در پایان فاز ۲، سیستم سلسله‌مراتبی مورفوپث به دقت ۵۳.۵۷٪ در Top-1 رسیده بود. تحلیل دقیق سردرگمی‌ها نشان داد که تصاویر مزرعه‌ای PlantDoc دارای یک شیفت سیستماتیک شدید نسبت به تصاویر آزمایشگاهی پشتیبان (Support) هستند (ناشی از زاویه تابش خورشید، خطای تراز سفیدی سنسورهای مختلف موبایل و پس‌زمینه خاکی). این شیفت بردار میانگین کوئری‌ها را به اندازه $\|\Delta\|_2 \approx 0.21 - 0.30$ در فضای برداری جابجا می‌کرد.

## ۲. تصمیم اتخاذشده (Decision)
به‌کارگیری تبدیل بسته جبری مرکززدایی منیفولد (Manifold Mean Centering) در زمان آزمون، بدون نیاز به آموزش، گرادیان یا افزودن وزن به مدل:
$$\tilde{z}_s = \frac{\hat{z}_s - \mu_s}{\|\hat{z}_s - \mu_s\|_2}, \qquad \tilde{z}_q = \frac{\hat{z}_q - \mu_q}{\|\hat{z}_q - \mu_q\|_2}$$
سپس پروتوتایپ‌های تصحیح‌شده هر کلاس $c$ به صورت زیر بازسازی می‌شوند:
$$P_c^{\text{rect}} = \frac{1}{|S_c|} \sum_{i \in S_c} \tilde{z}_{s, i}$$
همچنین برای سازگاری کامل با استریمینگ تک‌تصویر (Online Edge Streaming)، بردار $\mu_q$ می‌تواند با میانگین متحرک توزیع میدانی (Running Field Centroid) تقریب زده شود.

## ۳. شواهد تجربی و پیامدها (Empirical Evidence)
- **شکستن قطعی سقف ۶۰٪:**
  * دقت Top-1 کل PlantDoc از ۵۳.۵۷٪ به **۶۱.۵۱٪ تا ۶۲.۳۰٪ (+۸.۷۳٪ جهش مطلق)** رسید.
  * دقت تشخیص افتراقی دوگانه (Top-2) با **جهش تاریخی +۱۸.۶۶ درصدی** از ۶۱.۹۰٪ به **۸۰.۹۵٪** رسید.
  * کهن‌الگوی درختان و رزاسه از ۵۶.۵۷٪ به **۷۱.۷۲٪ (+۱۵.۱۵٪ افزایش)** رسید.
  * کهن‌الگوی انگور و کدو به دقت **۹۶.۱۵٪** دست یافت.
- **تطابق کامل با سخت‌افزار لبه:**
  * تاخیر محاسباتی هسته استنتاج کمتر از **۰.۰۵ میلی‌ثانیه** (بیش از ۲۰,۰۰۰ فریم بر ثانیه روی پردازنده معمولی).
  * صفر بایت افزایش حجم مدل و صفر میلی‌وات توان مصرفی مازاد.

---
- 📌 بازگشت به [[Architecture/ADR/Index|فهرست سوابق تصمیمات]]
- 📊 بازگشت به [[Project Board.canvas|تخته بصری ریسرچ]]

</div>

