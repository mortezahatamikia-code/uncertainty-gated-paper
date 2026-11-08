---
title: "IDEA-011: Zero-Parameter Test-Time Prototype Rectification (Query Centering & Dispersion Calibration)"
type: idea
idea_id: IDEA-011
phase: 1
tags:
  - idea
  - research/phase-1
  - test-time-adaptation
  - rectification
status: validated
empirical_result: "Decisively broke the 60% Top-1 barrier: Top-1 jumped from 53.57% to 61.51% standalone (+7.94%), and 62.30% with margin (+8.73%). Top-2 soared from 61.90% to 80.56% (+18.66%). Solanoid accuracy rose from 42.57% to 45.54% (47.52% peak). 0 added parameters, 0.0071 ms latency."
validation_log: "[[Logs/Log-Solanoid-Ceiling-Validation]]"
expected_gain: "+3% to +6% reduction in domain shift gap between support and field queries"
mechanism: "Shift support prototypes into the test query manifold via closed-form mean centering: P_c' = norm(P_c - mean(Q) + mean(S))"
created: 2026-11-08
---

<div dir="rtl" style="font-family: inherit;">

# 💡 IDEA-011: تصحیح پروتوتایپ‌ها در زمان آزمون بدون پارامتر (Zero-Parameter Test-Time Rectification)

## ۱. فرضیه علمی (Scientific Hypothesis)
تصاویر میدانی در PlantDoc دارای شیفت دامنه‌ای سیستماتیک نسبت به داده‌های پشتیبان (نظیر نور شدید خورشید، خطای بالانس رنگ دوربین گوشی و ته‌رنگ خاک مزرعه) هستند. این شیفت باعث می‌شود میانگین کلی کوئری‌ها از میانگین ساپورت فاصله بگیرد.
**فرضیه:** اگر بردار جابجایی توزیع ($\Delta = \mu_{\text{query}} - \mu_{\text{support}}$) در زمان آزمون بدون نیاز به بازانتشار گرادیان به عنوان مرکززدایی (Mean Centering) از بردارهای تست کسر شود، پروتوتایپ‌های ساپورت مستقیماً در منیفولد توزیع تست قرار گرفته و دقت دسته‌بندی به‌ویژه در بیماری‌های چالش‌برانگیز گوجه‌فرنگی ارتقا می‌یابد.

## ۲. مکانیزم اعتبارسنجی تجربی
- اعمال تصحیح مرکززدایی منیفولد (Feature Centering & L2 Normalization) روی ویژگی‌های کوئری و ساپورت در هر کهن‌الگو.
- اندازه‌گیری دقت کل در PlantDoc.

## ۳. نتیجه ارزیابی تجربی (Empirical Verdict)
> [!IMPORTANT] تایید قطعی و پیروزی علمی (Validated - Breakthrough!)
> - **شکستن سقف تاریخی ۶۰٪:** دقت Top-1 از ۵۳.۵۷٪ با جهشی بی‌سابقه به **۶۱.۵۱٪** (۱۵۵ از ۲۵۲ کوئری) و در ترکیب با کالیبراسیون حاشیه به **۶۲.۳۰٪** رسید (+۸.۷۳٪ ارتقای مطلق!).
> - **جهش خارق‌العاده Top-2:** از سقف ۶۱.۹۰٪ به **۸۰.۵۶٪ تا ۸۰.۹۵٪** صعود کرد (+۱۸.۶۶٪ جهش!).
> - **ارتقای کهن‌الگوی سولانوئید:** دقت درون سولانوئید از ۴۲.۵۷٪ به **۴۵.۵۴٪ تا ۴۷.۵۲٪** بهبود یافت.
> - **بهره‌وری لبه:** صفر پارامتر آموزش‌پذیر، بدون نیاز به گرادیان در زمان تست، تاخیر پردازش **۰.۰۰۷۱ میلی‌ثانیه** روی CPU.
> - گزارش کامل: [[Logs/Log-Solanoid-Ceiling-Validation|گزارش ارزیابی سقف سولانوئید]].

---
- 📌 بازگشت به [[Ideation/Index|فهرست ایده‌ها]]

</div>

