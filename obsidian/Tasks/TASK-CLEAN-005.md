---
title: "TASK-CLEAN-005: Deep Modular Decomposition of Engine into Clean Micro-Modules (<250 lines)"
type: task
task_id: TASK-CLEAN-005
phase: 5
tags:
  - task
  - research/phase-5
  - modularization
  - clean-code
  - single-responsibility
  - done
status: done
priority: High
depends_on: "TASK-CLEAN-004"
blocks: "TASK-AUDIT-001"
spec: "Specs/SPEC-MORPHOPATH-001.md"
created: 2026-11-09
completed: 2026-11-09
generated: { by: okf-enforcer/0.6, at: 2026-11-09T17:55:00Z }
---

<div dir="rtl" style="font-family: inherit;">

# 📌 TASK-CLEAN-005: شکستن عمیق و تفکیک فایل موتور به ماژول‌های مستقل و کوچک (<250 خط)

## ۱. انگیزه و صورت مسئله (Problem Statement)
فایل `pipeline/morphopath_engine.py` علی‌رغم جداسازی اولیه‌ی توابع ریاضی و ساختارهای پایه، هنوز شامل ۷۲۰ خط کد و آمیخته‌ای از منطق استنتاج، متریک‌های بالینی/ارزیابی و اسکریپت‌های سنگین تست و اعتبارسنجی بنچمارک بود. برای رعایت کامل اصول Clean Code، SRP (اصل مسئولیت واحد) و استانداردهای توسعه‌ی پایدار، این فایل به ماژول‌های میکروسکوپی و متمرکز با طول کمتر از ۲۵۰ خط شکسته شد.

## ۲. برنامه اجرایی تفکیک ماژول‌ها (Target Architecture)
1. **`pipeline/morphopath_eval.py` (۱۱۶ خط - کمتر از ۱۵۰ خط)**:
   - تفکیک کامل متد ارزیابی `evaluate_engine` و توابع محاسبه متریک‌های بالینی (`compute_clinical_metrics` برای FNR/FPR و `compute_archetype_metrics` برای کهن‌الگوها).
2. **`tests/test_morphopath_engine.py` (۱۵۸ خط - کمتر از ۱۸۰ خط)**:
   - انتقال کدهای تست مصنوعی `_run_self_tests()` و اعتبارسنجی سنگین بنچمارک رسمی PlantDoc `run_plantdoc_validation()` از فایل اصلی استنتاج به پوشه اختصاصی تست‌ها با قابلیت اجرای مستقیم `run_all_tests()`.
3. **`pipeline/morphopath_types.py` (۷۴ خط - کمتر از ۲۵۰ خط)**:
   - انتقال تابع تولید خروجی غربالگری تشخیصی `build_morphopath_output`.
4. **`pipeline/morphopath_engine.py` (۲۴۸ خط - کمتر از ۲۵۰ خط)**:
   - پالایش نهایی کلاس `MorphoPathEngine` به عنوان یک اینجین و فاساد خالص استنتاجی (Inference-only Engine Facade) با ۲۴۸ خط کد کاملاً تمیز و خوانا.
   - حفظ ۱۰۰٪ سازگاری به عقب (Backward Compatibility) با تمام اسکریپت‌های بنچمارک و تست‌ها از طریق `__all__` و متد نمایندگی `evaluate`.

## ۳. شاخص‌های موفقیت و پذیرش (Acceptance Criteria)
- [x] هیچ فایلی در ماژول‌های `pipeline/morphopath_*.py` طولی بیشتر از ۲۵۰ خط ندارد (تمام فایل‌ها با Python `readlines()` زیر ۲۵۰ خط هستند).
- [x] تست‌های واحد و بنچمارک‌های اعتبارسنجی بدون کوچک‌ترین خطا اجرا شده و دقت‌های رسمی (62.30%، 63.49%، 63.89% در PlantDoc) ۱۰۰٪ بازتولید شدند.
- [x] تخته کانبان و داشبورد گراف ابسیدین با وضعیت تسک همگام‌سازی شدند (`node-clean-task-5` به رنگ سبز تغییر یافت).

## ۴. گزارش نهایی طول خطوط و آزمون‌ها (Execution Log)

### جدول شمارش خطوط ماژول‌ها:
| مسیر فایل | وظیفه / مسئولیت | تعداد خطوط | وضعیت سقف مجاز |
| :--- | :--- | :---: | :---: |
| `pipeline/morphopath_archetypes.py` | تعریف کهن‌الگوها و نقشه‌های گیاه‌شناسی | ۱۰۴ | ✅ کمتر از ۲۵۰ خط |
| `pipeline/morphopath_types.py` | ساختارهای داده خروجی و بیلدر تریاژ تشخیصی | ۷۴ | ✅ کمتر از ۲۵۰ خط |
| `pipeline/morphopath_math.py` | تبدیلات تاکی، بهنجارسازی و فیشر انقباضی | ۲۳۷ | ✅ کمتر از ۲۵۰ خط |
| `pipeline/morphopath_eval.py` | متریک‌های بالینی FNR/FPR و ارزیابی تشخیصی | ۱۱۶ | ✅ کمتر از ۱۵۰ خط |
| `pipeline/morphopath_engine.py` | فاساد و اینجین اصلی استنتاج دوگانه | ۲۴۸ | ✅ کمتر از ۲۵۰ خط |
| `tests/test_morphopath_engine.py` | آزمون‌های سنتتیک و رانر اعتبارسنجی بنچمارک | ۱۵۸ | ✅ کمتر از ۱۸۰ خط |

### نتایج اعتبارسنجی بنچمارک رسمی PlantDoc:
- **Baseline (Joint Rectification, w_bio=None)**:
  - Top-1 Accuracy: 62.30%
  - Top-2 Differential Accuracy: 80.95%
  - FNR: 6.79% | FPR: 12.22%
- **Optimized Engine (Decoupled Weighting, w_bio=0.65)**:
  - Top-1 Accuracy: 63.49%
  - Top-2 Differential Accuracy: 80.95%
  - Macro F1: 62.01% | Router Top-1: 91.67%
- **Suppressed Engine (Canopy Clutter & Glare Gating)**:
  - Top-1 Accuracy: 63.89%
  - Top-2 Differential Accuracy: 80.95%
  - FPR: 8.89%

---
- وضعیت: ✅ **تکمیل شده (Done)**
- بازگشت به [[Project Board.canvas|تخته کانبان]]

</div>
