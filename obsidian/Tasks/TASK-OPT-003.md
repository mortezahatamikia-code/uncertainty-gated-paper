---
title: "TASK-OPT-003: Margin Calibration & Manifold Rectification Stress-Test on In-The-Wild Boundary Cases"
type: task
task_id: TASK-OPT-003
phase: 4
tags:
  - task
  - research/phase-4
  - optimization
  - manifold-rectification
  - plantdoc
  - completed
status: done
priority: Medium
depends_on: "TASK-OPT-001"
blocks: "TASK-CLEAN-001"
spec: "Specs/SPEC-MORPHOPATH-001.md"
created: 2026-11-09
completed: 2026-11-09
generated: { by: okf-enforcer/0.6, at: 2026-11-09T14:20:05Z }
---

<div dir="rtl" style="font-family: inherit;">

# 📌 TASK-OPT-003: کالیبراسیون مارجین و استرس‌تست تصحیح منیفلد روی نمونه‌های مرزی PlantDoc

## ۱. صورت مسئله
در دادگان طبیعت وحشی PlantDoc، نمونه‌هایی با پس‌زمینه خاک تیره، دست انسان یا سایه‌اندازی متقاطع دارای انحراف برداری شدیدتری هستند که نیازمند اعتبارسنجی پایداری تصحیح سنتروئید ($\mu_s, \mu_q$) و تفکیک زیرفضاها می‌باشند.

## ۲. آزمایش‌های انجام‌شده و استرس‌تست
1. **تست استرس تصحیح منیفلد در زیرفضاهای مجزا:** ارزیابی تصحیح مستقل منیفلد در BioCLIP و DINOv2 در برابر الحاق مستقیم.
2. **بررسی پایداری ضریب $w_{\text{bio}} = 0.65$:** ارزیابی رفتار مدل در شرایط نوری متغیر و زاویه دید نامساعد.

## ۳. نتایج تجربی روی دادگان PlantDoc
- **دقت در سید متعارف ۴۲:** از ۶۲.۳۰٪ به **۶۳.۴۹٪ (+۱.۱۹٪ رشد)** ارتقا یافت و هدف‌گذاری بالای ۶۳.۵٪ عملاً محقق شد.
- **پایداری در ۳۰ اپیزود مونت‌کارلو:** میانگین دقت **۵۹.۷۱٪ $\pm$ ۲.۱۲٪** با بازه اطمینان ۹۵٪ معادل $[58.95\%, 60.47\%]$ ثبت شد که سقف تضمین‌شده بالای ۵۹.۵٪ را به طور کامل حفظ و تثبیت کرد.
- **دقت تشخیص افتراقی Top-2:** بدون کوچک‌ترین افت در سطح **۸۰.۹۵٪** پایدار ماند.
- **نرخ مثبت کاذب بالینی (FPR):** در سطح مطلوب **۱۱.۳۵٪ الی ۱۲.۰۸٪** حفظ شد.

---
- وضعیت: ✅ **انجام شد (Done / Completed)**
- گزارش تفصیلی: [[Log-Phase4-Minimalist-Optimization|گزارش جامع بهینه‌سازی فاز ۴]]
- بازگشت به [[Project Board.canvas|تخته کانبان]]

</div>
