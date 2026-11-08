---
title: "TASK-MORPHOPATH-004: Comprehensive Component Ablation Study"
type: task
task_id: TASK-MORPHOPATH-004
phase: 3
tags:
  - task
  - research/phase-3
  - ablation
  - validation
status: done
priority: High
depends_on: "TASK-MORPHOPATH-001, TASK-MORPHOPATH-002"
blocks: "DRAFT-MORPHOPATH-001"
spec: "Specs/SPEC-MORPHOPATH-001.md"
created: 2026-11-08
completed: 2026-11-08
log: "Logs/Log-Phase3-Ablation-Study.md"
---

<div dir="rtl" style="font-family: inherit;">

# 📌 TASK-MORPHOPATH-004: مطالعه جامع ابلیشن و حذف تک‌تک اجزای سیستم (Ablation Study)

## وضعیت: تکمیل‌شده (Done ✅)

## هدف تسک
تهیه جدول ابلیشن استاندارد ژورنالی جهت پاسخ به سوالات داوران داوری و اثبات سهم دقیق هر نوآوری:
1. حذف روتر کهن‌الگو (تبدیل به مسطح).
2. حذف انقباض کوواریانس ($\lambda \to 0$ یا بدون رگولاریزاسیون).
3. حذف متوازن‌سازی بیزی ($\alpha \to 0$ یا روتر حتمی).
4. حذف تصحیح منیفولد تست (بدون $\mu_q - \mu_s$).
5. حذف پرامپت‌های متنی عوارض میکروسکوپی.

## نتایج حاصله و شواهد تجربی (Execution Summary)
- **مدل کامل (Full Proposed Model):** دقت Top-1 برابر با **۶۲.۳۰٪**، دقت Top-2 برابر با **۸۰.۹۵٪**، و شاخص Macro F1 برابر با **۶۰.۶۸٪**.
- **حذف تصحیح منیفولد (ADR-005):** افت شدید **۸.۷۳- درصد** در Top-1 (سقوط به ۵۳.۵۷٪) و افت ۶.۳۵- درصد در Top-2.
- **حذف روتر کهن‌الگو (ADR-001) [مدل مسطح Flat]:** افت **۸.۳۳- درصد** در Top-1 (سقوط به ۵۳.۹۷٪).
- **حذف انقباض کوواریانس (ADR-002) [کوواریانس تجربی $\lambda=0.001$]:** سقوط آزاد **۱۰.۷۱- درصدی** در Top-1 (۵۱.۵۹٪) و ریزش فاجعه‌بار **۱۹.۸۴- درصدی** در Top-2 (از ۸۰.۹۵٪ به ۶۱.۱۱٪).
- **حذف پرامپت‌های متنی عوارض (ADR-004):** افت **۱.۹۸- درصد** در Top-1 (۶۰.۳۲٪).
- **حذف گیتینگ بیزی متوازن (ADR-003) [روتر حتمی]:** افت **۳.۹۷- درصد** در Top-1 (۵۸.۳۳٪) و ۵.۱۶- درصد در Top-2 (۷۵.۷۹٪).
- **پروژکشن دوبعدی منیفولد t-SNE:** در فایل `experiments/phase3_morphopath/tsne_manifold_rectification.png` ذخیره شد.
- **گزارش رسمی:** [[Logs/Log-Phase3-Ablation-Study|Log-Phase3-Ablation-Study]]
- **داده‌های ساخت‌یافته:** `experiments/phase3_morphopath/ablation_study_results.json`

## معیارهای پذیرش (Acceptance Criteria)
- [x] جدول کامل ابلیشن با ستون‌های Top-1، Top-2، Macro F1 و دلتای عملکرد برای ۶ کانفیگ استاندارد.
- [x] ترسیم نمودارهای تحلیلی t-SNE از کلاسترها قبل و بعد از تصحیح منیفولد با رزولوشن ۳۰۰ DPI.

---
- 📌 بازگشت به [[Tasks/Index|فهرست تسک‌ها]]

</div>

