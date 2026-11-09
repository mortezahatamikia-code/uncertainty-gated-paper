---
title: "TASK-CLEAN-004: Modular Decomposition of Monolithic Engine into Focused Sub-Modules (Single Responsibility)"
type: task
task_id: TASK-CLEAN-004
phase: 5
tags:
  - task
  - research/phase-5
  - modularization
  - clean-code
  - single-responsibility
  - pending
status: todo
priority: High
depends_on: "TASK-CLEAN-003"
blocks: ""
spec: "Specs/SPEC-MORPHOPATH-001.md"
created: 2026-11-09
generated: { by: okf-enforcer/0.6, at: 2026-11-09T18:06:33Z }
---

<div dir="rtl" style="font-family: inherit;">

# 📌 TASK-CLEAN-004: شکستن فایل یکپارچه (Monolithic) موتور استنتاج به ماژول‌های مستقل و کوچک (Single Responsibility)

## ۱. انگیزه و صورت مسئله (Problem Statement)
فایل `pipeline/morphopath_engine.py` در اثر افزودن قابلیت‌های مختلف به بیش از ۹۰۰ خط کد رسیده است و مسئولیت‌های متعددی (تعاریف ساختار داده، فرمول‌های ریاضی و توان توکی، نگاشت آرکی‌تایپ‌های گیاه‌شناسی، فیلترهای نوری، و کلاس اصلی موتور استنتاج) در یک فایل تجمیع شده‌اند که با اصل **Single Responsibility Principle (SRP)** و استانداردهای Clean Code مغایرت دارد.

## ۲. برنامه تفکیک و شکستن فایل (Modular Architecture)
شکستن فایل به ماژول‌های متمرکز و خوانا با حفظ سازگاری ۱۰۰٪ به عقب (Backward Compatibility):
1. **`pipeline/morphopath_types.py`**:
   - دیتاکلاس‌های خروجی (`MorphoPathOutput`)، کدهای وضعیت، تایپ هینتینگ و ساختارهای داده.
2. **`pipeline/morphopath_math.py`**:
   - توابع مستقل ریاضی و منیفلد: نرمال‌سازی L2، تبدیل توان توکی، ماتریس‌های کوواریانس و فاصله‌سنجی.
3. **`pipeline/morphopath_archetypes.py`**:
   - تعاریف ۴ کهن‌الگوی گیاه‌شناسی، دیکشنری‌های نگاشت گونه به آرکی‌تایپ، و توابع تشخیص سلامت فیزیولوژیک.
4. **`pipeline/morphopath_engine.py` (ماژول اصلی و Facade)**:
   - کلاس محوری `MorphoPathEngine` که از ماژول‌های فوق ایمپورت کرده و تمام نمادهای عمومی را با `__all__` مجدداً اکسپورت می‌کند تا هیچ‌یک از اسکریپت‌های بنچمارک یا کالبک‌ها نشکنند.

## ۳. معیارهای پذیرش (Acceptance Criteria)
- [ ] هیچ فایلی طولی بیش از ۳۰۰ الی ۴۰۰ خط نداشته باشد.
- [ ] تمام تست‌ها و اسکریپت‌های بنچمارک (`benchmark_monte_carlo.py`، `benchmark_plantvillage.py`، `benchmark_edge_profiling.py`) بدون کوچک‌ترین تغییر در ایمپورت‌ها به طور کامل اجرا شوند.
- [ ] کدها کاملاً انسانی، تمیز و همراه با Type Hinting استاندارد PEP 484 باشند.

---
- وضعیت: ⏳ **در انتظار انجام (Pending - پس از اتمام کارهای جاری گام ۵)**
- بازگشت به [[Project Board.canvas|تخته کانبان]]

</div>

