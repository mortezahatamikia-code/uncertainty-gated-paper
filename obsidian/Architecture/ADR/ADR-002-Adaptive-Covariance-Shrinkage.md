---
title: "ADR-002: Regularized Covariance Shrinkage for Singular Intra-Archetype Few-Shot Metrics"
type: adr
adr_id: ADR-002
phase: 2
tags:
  - adr
  - architecture
  - research/phase-2
  - covariance
  - optimization
status: Accepted
date: 2026-11-08
impact: "Eliminates singular covariance matrices (condition number inf -> 1428), +7.54% hierarchical gain"
---

<div dir="rtl" style="font-family: inherit;">

# 📜 ADR-002: انقباض کوواریانس تطبیقی برای تثبیت ماتریس‌های تکین در سناریوی چندشاتی

## وضعیت: پذیرفته‌شده (Accepted ✅)

## ۱. زمینه و انگیزه (Context)
در سناریوی 5-shot با بردار ویژگی با بعد بالا ($D=896$)، تعداد کل نمونه‌های ساپورت در هر کهن‌الگو کمتر از بعد فضا است ($N < D$). این پدیده باعث می‌شود ماتریس کوواریانس درون‌کلاسی ($\Sigma_w$) به طور قطعی تکین (Singular) شده و عدد شرطی آن بی‌نهایت ($\kappa = \infty$) گردد که به فروپاشی طبقه‌بندهای مبتنی بر فاصله ماهالانوبیس یا فیشر می‌انجامد.

## ۲. تصمیم اتخاذشده (Decision)
به کارگیری انقباض تحلیلی لدویت-ولف و رگولاریزاسیون بهینه بر ماتریس‌های کوواریانس درون هر کهن‌الگو به فرم:
$$\Sigma_{\text{shrunk}} = (1 - \lambda) \Sigma_w + \lambda \frac{\text{Tr}(\Sigma_w)}{D} I_D$$
مقدار بهینه تجربی روی دادگان مزرعه $\lambda = 0.60$ تعیین شد.

## ۳. شواهد تجربی و پیامدها (Consequences & Evidence)
- پایداری کامل عددی: عدد شرطی از بی‌نهایت به ۱۴۲۸ کاهش یافت.
- جهش دقت سلسله‌مراتبی بیماری‌ها از **۴۳.۶۵٪ به ۵۱.۱۹٪ (+۷.۵۴٪)**.
- افزایش دقت اوراکل درون کهن‌الگوها به **۵۶.۳۵٪ (+۸.۳۳٪)**.
- بدون کوچک‌ترین هزینه تاخیر در لبه (استفاده از فرم بسته جبری بدون نیاز به بازانتشار گرادیان).

---
- 📌 بازگشت به [[Architecture/ADR/Index|فهرست سوابق تصمیمات]]

</div>

