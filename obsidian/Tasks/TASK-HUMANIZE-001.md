---
title: "TASK-HUMANIZE-001: De-AI & Stylistic Polish of Title, Abstract, and Historical Introduction"
type: task
task_id: TASK-HUMANIZE-001
phase: 5
tags:
  - task
  - research/phase-5
  - humanizing
  - introduction
status: done
priority: High
depends_on: "TASK-DRAFT-001, TASK-DRAFT-002, TASK-DRAFT-003, TASK-DRAFT-004"
blocks: "TASK-HUMANIZE-002"
spec: "Specs/SPEC-MORPHOPATH-001.md"
created: 2026-11-08
---

<div dir="rtl" style="font-family: inherit;">

# 📌 TASK-HUMANIZE-001: پالایش لحن هوش مصنوعی، تنوع نحوی و غنی‌سازی چکیده و مقدمه

## هدف تسک
بازنویسی عمیق عنوان، چکیده و بخش مقدمه (`paper_morphopath/sections/01_introduction.tex`) جهت دستیابی به لحن نویسندگان انسانی تراز اول در IEEE TPAMI / CVPR:
1. **ریشه‌کنی الگوهای نوشتاری هوش مصنوعی (De-AI Cleansing):**
   - حذف کامل واژگان کلیشه‌ای مدل‌های زبانی (نظیر: *delve, testament, pivotal, crucial, game-changing, moreover/furthermore تکراری در شروع جملات، سه گانه‌های موازی خسته‌کننده*).
   - اصلاح ساختارهای متقارن مصنوعی و ایجاد تنوع در ریتم جملات (ترکیب جملات گزاره‌ای کوتاه و کوبنده با جملات مرکب تحلیلی و مستند).
2. **فشرده‌سازی اطلاعات و افزایش چگالی علمی (Data Densification):**
   - جایگزینی صفت‌های مبهم (مانند "بهبود چشمگیر") با اعداد دقیق آماری، فواصل اطمینان و شواهد تجربی ($p < 10^{-14}$, فواصل اطمینان ۹۵٪).
   - ارتقای روایت تاریخی با اصطلاحات دقیق گیاه‌پزشکی و فیتوپاتولوژی (مانند *concentric necrotic zonation, fungal pycnidia, foliar chlorosis, specular reflectance*).

## معیارهای پذیرش (Acceptance Criteria)
- [ ] چکیده و مقدمه کاملاً عاری از حس متن تولیدشده توسط AI.
- [ ] افزایش داده‌های ارائه‌شده با کلمات کمتر و علمی‌تر.
- [ ] ذخیره در `paper_morphopath/sections/01_introduction.tex` و خلاصه در `obsidian/Reviews/Review-Humanize-01.md`.

---
- 📌 بازگشت به [[Tasks/Index|فهرست تسک‌ها]]

</div>
