---
title: "TASK-OPT-001: Root Cause Analysis and Minimalist Recovery of the ~2% Accuracy Drop on PlantVillage"
type: task
task_id: TASK-OPT-001
phase: 4
tags:
  - task
  - research/phase-4
  - optimization
  - plantvillage
  - ponytail
  - completed
status: done
priority: High
depends_on: "TASK-MORPHOPATH-005"
blocks: "TASK-OPT-002, TASK-CLEAN-001"
spec: "Specs/SPEC-MORPHOPATH-001.md"
created: 2026-11-09
completed: 2026-11-09
generated: { by: okf-enforcer/0.6, at: 2026-11-09T14:19:47Z }
---

<div dir="rtl" style="font-family: inherit;">

# 📌 TASK-OPT-001: تحلیل ریشه‌ای و جبران کمینه‌گرای افت ۲ درصدی دقت در PlantVillage

## ۱. صورت مسئله و شواهد تجربی (Problem Statement)
در بنچمارک ۳۸ کلاسی دادگان PlantVillage، معماری اولیه MorphoPath-Edge به دقت **۸۶.۵۳٪ $\pm$ ۱.۰۰٪** رسید، در حالی که بیس‌لاین ۲ (روتر صلب ۱۴ گونه) به دقت **۸۸.۲۹٪ $\pm$ ۱.۱۸٪** دست یافته بود (**افت ۱.۷۶٪- Top-1**). همچنین در زیرمجموعه ۱۱ گونه نوول، دقت ۹۳.۸۳٪ در برابر ۹۵.۰۸٪ ثبت شده بود (افت ۱.۲۵٪- نسبت به BioDINO).

## ۲. ریشه‌یابی و راهکار کمینه‌گرا (Root Cause & Minimalist Fix)
1. **ریشه‌یابی:** الحاق مستقیم بردارها ($[bio, dino]$) به دلیل انرژی اقلیدسی نامتقارن، نویز هندسی DINOv2 را بر تمایزبخشی غنی پاتولوژیک BioCLIP تحمیل می‌کرد.
2. **اصلاح کمینه‌گرا (Ponytail):** تفکیک زیرفضاها و وزن‌دهی مجزا ($S_{\text{vis}} = 0.65 S_{\text{bio, rect}} + 0.35 S_{\text{dino, rect}}$) همراه با اتصال احتمال پسین LDA انقباضی ($w_{\text{lda}} = 0.30$) و دروازه‌بانی بیزی نرم ($\beta = 0.20$).

## ۳. نتایج تجربی نهایی و اعتبارسنجی (Final Empirical Results)
- **دقت ۳۸ کلاسی PlantVillage:** از ۸۶.۵۳٪ به **۸۹.۵۷٪ $\pm$ ۱.۲۷٪** جهش یافت (**+۳.۰۴٪ رشد**، برتری **+۱.۲۸٪** بر بیس‌لاین ۲ با سطح معنی‌داری خارق‌العاده $p = 1.07 \times 10^{-10}$).
- **دقت زیرمجموعه ۱۱ کلاس نوول:** از ۹۳.۸۳٪ به **۹۵.۲۹٪ $\pm$ ۱.۵۳٪** رسید و با موفقیت رکورد ۹۵.۰۸٪ مدل BioDINO را شکست.
- **نرخ منفی کاذب بالینی (FNR):** از ۳.۸۲٪ به **۲.۴۰٪** کاهش یافت.
- **نرخ مثبت کاذب بالینی (FPR):** از ۱.۹۱٪ به **۱.۳۲٪** بهبود یافت.
- **پارامتر افزوده:** **۰.۰ مگابایت** (صفر وزن اضافه).

---
- وضعیت: ✅ **انجام شد (Done / Completed)**
- گزارش تفصیلی: [[Log-Phase4-Minimalist-Optimization|گزارش جامع بهینه‌سازی فاز ۴]]
- بازگشت به [[Project Board.canvas|تخته کانبان]]

</div>
