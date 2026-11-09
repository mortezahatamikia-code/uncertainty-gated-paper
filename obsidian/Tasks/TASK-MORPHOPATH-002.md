---
title: "TASK-MORPHOPATH-002: Monte Carlo 30-Episode Statistical Rigor Evaluation"
type: task
task_id: TASK-MORPHOPATH-002
phase: 3
tags:
  - task
  - research/phase-3
  - evaluation
  - monte-carlo
status: done
priority: High
depends_on: "TASK-MORPHOPATH-001"
blocks: "TASK-MORPHOPATH-004"
spec: "Specs/SPEC-MORPHOPATH-001.md"
created: 2026-11-08
completed: 2026-11-08
---

<div dir="rtl" style="font-family: inherit;">

# 📌 TASK-MORPHOPATH-002: بنچمارک مونت‌کارلو ۳۰ اپیزودی با فواصل اطمینان ۹۵٪

## وضعیت: تکمیل‌شده (Done ✅)

## هدف تسک
اجرای ارزیابی استاندارد آکادمیک در ۳۰ تکرار تصادفی مونت‌کارلو (Monte Carlo 30-Episode Few-Shot Sampling) با محاسبه میانگین و فاصله اطمینان ۹۵٪ ($\text{Mean} \pm 1.96 \times \text{SEM}$):
1. مقایسه رودرروی MorphoPath-Edge با بیس‌لاین‌های مسطح (Flat Multimodal Prototype) و روتر صلب (Rigid 13-Species Router) در دادگان مزرعه‌ای **PlantDoc**.
2. ارزیابی در سناریوی استاندارد ۵ شات ($k=5$).
3. استخراج مقادیر دقیق Top-1 Accuracy، Top-2 Differential Accuracy، Macro F1، Router Accuracy، FNR و FPR.
4. آزمون معناداری آماری فرضیات با آزمون تی دونمونه‌ای جفت‌شده (Paired two-sample t-test).

## معیارهای پذیرش (Acceptance Criteria)
- [x] اسکریپت رسمی ارزیابی چند اپیزودی `experiments/phase3_morphopath/benchmark_monte_carlo.py` پیاده‌سازی و اجرا گردید.
- [x] کلیه لاگ‌های خام ۳۰ اپیزود و نتایج تجمیعی در `experiments/phase3_morphopath/monte_carlo_30ep_results.json` ذخیره شد.
- [x] ثبت جدول کامل نتایج آماری در فرمت LaTeX آماده برای درج در پیش‌نویس مقاله.
- [x] اثبات معناداری آماری قطعی برتری ($p < 0.001$) با آزمون تی زوجی برای تمام شاخص‌های کلیدی:
  * برتری بر بیس‌لاین مسطح: **$p = 1.39 \times 10^{-15}$** ($t = 15.52$)
  * برتری بر روتر صلب ۱۳ گونه‌ای: **$p = 1.03 \times 10^{-21}$** ($t = 26.15$)
  * برتری روتر کهن‌الگو: **$p = 6.35 \times 10^{-30}$** ($t = 50.93$)

---

## 📊 نتایج آماری نهایی ۳۰ اپیزود مونت‌کارلو (PlantDoc, k=5)

| مدل معماری | میانگین دقت Top-1 ($\pm \text{Std}$) | فاصله اطمینان ۹۵٪ Top-1 | میانگین دقت تریاژ Top-2 | شاخص Macro F1 | دقت روتر کلان | برتری آماری ($p$-value) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **بیس‌لاین ۱ (مسطح چندحالته)** | ۵۳.۱۶٪ $\pm$ ۲.۰۶٪ | $[52.43\%, 53.90\%]$ | ۷۲.۷۶٪ $\pm$ ۱.۵۹٪ | ۵۲.۱۶٪ $\pm$ ۲.۰۵٪ | — | مبنا |
| **بیس‌لاین ۲ (روتر صلب ۱۳ گونه‌ای)** | ۴۷.۷۴٪ $\pm$ ۲.۱۹٪ | $[46.95\%, 48.52\%]$ | ۶۷.۷۲٪ $\pm$ ۲.۱۹٪ | ۴۵.۷۱٪ $\pm$ ۱.۸۱٪ | ۷۹.۳۵٪ $\pm$ ۱.۰۴٪ | مبنای پیشین |
| **مدل پیشنهادی: MorphoPath-Edge** | **۵۹.۵۸٪ $\pm$ ۱.۹۷٪** | $\mathbf{[58.87\%, 60.28\%]}$ | **۷۹.۲۵٪ $\pm$ ۱.۴۹٪** | **۵۷.۶۳٪ $\pm$ ۱.۸۵٪** | **۹۱.۳۹٪ $\pm$ ۰.۶۰٪** | **$p < 10^{-14}$** (قطعی) |
| **بهبود مطلق بر بیس‌لاین ۱** | **+۶.۴۲٪** | — | **+۶.۴۸٪** | **+۵.۴۶٪** | — | **$t = 15.52, p = 1.39 \times 10^{-15}$** |
| **بهبود مطلق بر بیس‌لاین ۲** | **+۱۱.۸۴٪** | — | **+۱۱.۵۲٪** | **+۱۱.۹۱٪** | **+۱۲.۰۴٪** | **$t = 26.15, p = 1.03 \times 10^{-21}$** |

---
- 📑 مشاهده گزارش تحلیلی کامل و کدهای لاتک: [[Logs/Log-Phase3-Monte-Carlo-Benchmark|گزارش بنچمارک آماری فاز ۳]]
- 📌 بازگشت به [[Tasks/Index|فهرست تسک‌ها]]
- 📊 بازگشت به [[Project Board.canvas|تخته بصری ریسرچ]]
- ⚡ انتقال به تسک بعدی: [[Tasks/TASK-MORPHOPATH-003|TASK-MORPHOPATH-003: ارزیابی تعمیم دامنه‌ای روی PlantVillage]]

</div>
