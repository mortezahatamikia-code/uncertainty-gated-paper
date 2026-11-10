---
title: "TASK-CLEAN-001: DRY Refactoring of Inference Pipelines and Duplicate Math Functions"
type: task
task_id: TASK-CLEAN-001
phase: 5
tags:
  - task
  - research/phase-5
  - clean-code
  - dry
  - refactor
  - done
status: done
priority: High
depends_on: "TASK-OPT-001, TASK-OPT-002"
blocks: "TASK-CLEAN-002"
spec: "Specs/SPEC-MORPHOPATH-001.md"
created: 2026-11-09
completed: 2026-11-09
generated: { by: okf-enforcer/0.6, at: 2026-11-09T14:20:16Z }
---

<div dir="rtl" style="font-family: inherit;">

# 📌 TASK-CLEAN-001: یکپارچه‌سازی و بازآفرینی DRY در توابع ریاضی و خطوط لوله استنتاج

## ۱. صورت مسئله
در اسکریپت‌های مختلف بنچمارک (`benchmark_plantvillage.py`، `benchmark_monte_carlo.py`، و `benchmark_ablation.py`) بخش‌هایی از منطق انقباض کوواریانس و فاصله‌سنجی بازنویسی شده بودند که پتانسیل بروز خطای ناهماهنگی داشتند.

## ۲. اقدامات اجرایی انجام‌شده
1. **انتقال و تمرکز محاسبات ریاضی در `pipeline/morphopath_math.py`**:
   - `l2_normalize`: پروجکشن برداری به کره واحد با پشتیبانی از بافر خروجی `out`.
   - `tukey_power_transform`: تبدیل توان توکی علامت‌دار همراه با نرمال‌سازی L2.
   - `center_and_normalize`: تصحیح منیفلد تست‌تایم و برآورد سنتروئید منیفلد (ADR-005).
   - `softmax_prob`: سافت‌مکس برداری عددی پایدار بدون هزینه‌ی تبدیل به تانسور پای‌تورچ.
   - `calculate_differential_confidence`: شاخص قطعیت تفریقی آنتروپی شانون (ADR-003).
   - `fit_shrunk_lda`: برازش تحلیل تمایز فیشر با انقباض لدویت-ولف (ADR-002).
   - `compute_prototypes`: تجمیع سنتروئیدهای ساپورت بر حسب کلاس.
2. **یکپارچه‌سازی اسکریپت‌های بنچمارک با ماژول اصلی**:
   - `benchmark_ablation.py`، `benchmark_monte_carlo.py`، و `benchmark_plantvillage.py` مستقیماً توابع ریاضی و موتور را فراخوانی کرده و کدهای تکراری حذف شدند.
   - حذف متغیرها و ماژول‌های ایمپورت‌شده بی‌استفاده مانند `LinearDiscriminantAnalysis` غیرضروری و `fit_fisher_lda`.
3. **صحت‌سنجی ۱۰۰٪ خروجی‌ها**:
   - بازتولید دقیق دقت baseline برابر با ۶۲.۳۰٪ و بهینه برابر با ۶۳.۴۹٪ و مهار سایبان برابر با ۶۳.۸۹٪ در PlantDoc.

---
- وضعیت: ✅ **انجام شد (Done)**
- بازگشت به [[Project Board.canvas|تخته کانبان]]

</div>
