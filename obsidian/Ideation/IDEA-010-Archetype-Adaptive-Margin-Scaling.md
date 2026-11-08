---
title: "IDEA-010: Archetype-Adaptive Margin Scaling & Cardinality-Scaled Temperature"
type: idea
idea_id: IDEA-010
phase: 1
tags:
  - idea
  - research/phase-1
  - metric-learning
  - temperature
status: rejected
empirical_result: "Dilation of temperature via 1/sqrt(K_A) reduces Top-1 from 53.57% to 52.78% by flattening logit discriminability in large clusters. Margin penalty provides marginal gains only as a post-rectification stabilizer (+0.79% in synergy), not as a standalone solution."
validation_log: "[[Logs/Log-Solanoid-Ceiling-Validation]]"
expected_gain: "+2% to +5% through entropy regularization and confusion-margin subtraction"
mechanism: "Scale Softmax temperature by sqrt(K_A) and apply pairwise additive cosine margin penalties to crowded prototypes"
created: 2026-11-08
---

<div dir="rtl" style="font-family: inherit;">

# 💡 IDEA-010: مقیاس‌بندی حاشیه تفکیک‌پذیری و دمای متناسب با کاردینالیتی (Adaptive Margin Scaling)

## ۱. فرضیه علمی (Scientific Hypothesis)
در کهن‌الگوی سولانوئید با ۱۰ کلاس، زاویه بین پروتوتایپ‌ها بسیار فشرده است و استفاده از دمای ثابت ($\tau=15$ یا $\tau=20$) باعث بیش‌اطمینانی (Overconfidence) یا عدم تمایز در رتبه‌بندی احتمالات می‌شود.
**فرضیه:** تنظیم دمای سافت‌مکس متناسب با ریشه تعداد کلاس‌های کهن‌الگو ($T_A = \tau / \sqrt{K_A}$) به همراه اعمال جریمه حاشیه زاویه‌ای تطبیقی ($S_{ij} = \cos(x, P_i) - m_{ij}$) روی کلاس‌های پرابهام گوجه‌فرنگی، تفکیک‌پذیری مرزهای تصمیم‌گیری فیشر را افزایش می‌دهد.

## ۲. مکانیزم اعتبارسنجی تجربی
- ارزیابی شبکه‌ای مقادیر دما و جریمه حاشیه روی کلاس‌های سولانوئید.
- محاسبه تغییرات دقت در سناریوی بدون تغییر حجم مدل.

## ۳. نتیجه ارزیابی تجربی (Empirical Verdict)
> [!CAUTION] رد به عنوان فرضیه مستقل (Rejected as Standalone)
> - **دمای کاردینالیتی معکوس:** دقت کل به **۵۲.۷۸٪** افت کرد زیرا تعدیل دما قله‌های احتمالات را در کهن‌الگوهای پرجمعیت سولانوئید و روسوئید بیش از حد نرم و غیرمتمایز ساخت.
> - **جریمه حاشیه متقارن:** به تنهایی روی مدل پایه تغییری ایجاد نکرد (ثابت روی ۵۳.۵۷٪)، اما پس از حل شیفت دامنه‌ای در منیفولد توسط IDEA-011، جریمه نامتقارن $m=0.05$ روی کلاس دارای نشت (Late Blight) توانست دقت را به **۶۲.۳۰٪** برساند (+۰.۷۹٪ سود هم‌افزا).
> - گزارش کامل: [[Logs/Log-Solanoid-Ceiling-Validation|گزارش ارزیابی سقف سولانوئید]].

---
- 📌 بازگشت به [[Ideation/Index|فهرست ایده‌ها]]

</div>

