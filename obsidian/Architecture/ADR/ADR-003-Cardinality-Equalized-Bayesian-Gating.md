---
title: "ADR-003: Cardinality-Equalized Soft Bayesian Gating for Top-2 Differential Diagnosis"
type: adr
adr_id: ADR-003
phase: 2
tags:
  - adr
  - architecture
  - research/phase-2
  - bayesian
  - differential-diagnosis
status: Accepted
date: 2026-11-08
impact: "Top-2 Differential Diagnosis jumps to 75.00% - 81.5%, False Positive Rate dropped by 4.44%"
---

<div dir="rtl" style="font-family: inherit;">

# 📜 ADR-003: گیتینگ بیزی نرم با متوازن‌سازی کاردینالیتی برای تشخیص افتراقی Top-2

## وضعیت: پذیرفته‌شده (Accepted ✅)

## ۱. زمینه و انگیزه (Context)
تصمیم‌گیری حتمی (Hard Argmax Routing) هرگونه عدم قطعیت در مرزهای کلاسترها را سرکوب می‌کند. علاوه بر این، نابرابری در تعداد کلاس‌های زیرمجموعه هر کهن‌الگو (سولانوئید با ۱۰ کلاس در برابر پویید با ۳ کلاس) باعث سوگیری احتمالاتی به نفع کلاسترهای خلوت‌تر می‌شد (اثر جریمه کاردینالیتی یکنواخت $1/K_A$).

## ۲. تصمیم اتخاذشده (Decision)
به‌کارگیری استنتاج بیزی نرم با ضریب تعدیل اندازه کهن‌الگو (Cardinality Equalization Factor):
$$P(c \mid x) \propto P(A \mid x) \times \left[ K_A \cdot P_{\text{loc}}(c \mid x, A) \right]^\alpha$$
همچنین خروجی سیستم به جای یک تک‌پاسخ جزمی، به صورت **تشخیص افتراقی دوگانه (Top-2 Differential Diagnosis)** با درصد احتمال اطمینان به کشاورز عرضه می‌شود.

## ۳. شواهد تجربی و پیامدها (Consequences & Evidence)
- با $\alpha = 1.0$، دقت Top-2 سیستم به **۷۵.۰۰٪ تا ۸۱.۵٪** می‌رسد.
- نرخ هشدار کاذب برای برگ‌های سالم (FPR) از ۲۲.۲۲٪ به ۱۷.۷۸٪ افت می‌کند.
- سناریوی واقعی مزرعه پوشش داده می‌شود: اگر دو بیماری بسیار شبیه باشند (مانند سفیدک دروغی و لکه باکتریایی)، هر دو با ذکر درصد احتمال در اختیار کشاورز قرار می‌گیرند.

---
- 📌 بازگشت به [[Architecture/ADR/Index|فهرست سوابق تصمیمات]]

</div>

