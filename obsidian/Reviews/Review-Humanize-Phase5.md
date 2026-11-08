---
title: "Review-Humanize-Phase5: Master Audit of Stylistic Densification, Visual Portfolio & 8-Page IEEE Compilation"
type: review
phase: 5
tags:
  - review
  - research/phase-5
  - humanizing
  - compilation
focus: "De-AI Cleansing, Phytopathological Densification, 300-DPI Visual Assets, and Strict 8-Page IEEE Balancing"
status: approved
created: 2026-11-08
generated: { by: okf-enforcer/0.6, at: 2026-11-08T19:05:04Z }
---

<div dir="rtl" style="font-family: inherit;">

# 🔍 گزارش جامع فاز ۵: انسانی‌نویسی، چگال‌سازی علمی، تولید تصاویر و کامپایل ۸ صفحه‌ای IEEE

## ۱. خلاصه اجرایی
تمامی الزامات راهبردی فاز ۵ با هدایت الزامات کاربر («عکس بیشتر»، «بهبود لحن»، «بیان انسانی‌تر و آکادمیک‌تر داده‌ها» و «تثبیت در دقیقاً ۸ صفحه بدون حتی یک خط سرریز») با موفقیت ۱۰۰٪ محقق شد. تمام کدهای دست‌ساز و متون مقاله در پوشه ایزوله `paper_morphopath/` مستقر بوده و پروژه‌های `paper/` و `android_app/` کاملاً دست‌نخورده باقی مانده‌اند.

---

## ۲. گزارش پرتره و دارایی‌های بصری (Visual Portfolio)
سه شکل کلیدی مطابق با دستور راهبردی و استاندارد چاپی ۳۰۰ DPI در متن ادغام شده‌اند:
1. **`figures/fig_archetypes.png` (شکل ۱ - پهنای کامل ۲ ستونه، ارتفاع ۴.۲ سانتی‌متر):**
   - تصویربرداری بیولوژیک از ۴ ابر-کهن‌الگوی گیاه‌شناسی (Solanoid، Vitoid، Pooid، Rosoid).
   - نمونه‌های واقعی برگ از مجموعه PlantDoc (`Tomato_Early_blight_leaf`، `grape_leaf_black_rot`، `Corn_rust_leaf`، `Apple_rust_leaf`).
   - تقابل هندسه ماکروسکوپیک اندام برگی در برابر پاتولوژی میکروسکوپی ضایعات نکروتیک.
2. **`figures/fig_architecture.png` (شکل ۲ - پهنای کامل ۲ ستونه، ارتفاع ۴.۲ سانتی‌متر):**
   - دیاگرام معماری سیستم چندبخشی MorphoPath-Edge منطبق بر استاندارد ژورنال‌های IEEE.
   - نمایش گام‌های: ۱) استخراج ویژگی دوگانه DINOv2 و BioCLIP، ۲) روتینگ ۴ کهن‌الگو، ۳) تصحیح جبری صفر-پارامتر منیفلد ($0.041\,\text{ms}$)، ۴) متریک انقباضی لدویت-ولف ($\lambda=0.60$) و ۵) تریاژ بیزی با توازن کاردینالیتی.
3. **`figures/tsne_manifold_rectification.png` (شکل ۳ - تک‌ستونه، عرض ۰.۸۲ ستون):**
   - مقایسه منیفلد ویژگی قبل و بعد از تصحیح جبری بر روی PlantDoc و اثبات حذف انتقال مرکز ثقل ($\|\Delta\|_2 \approx 0.30$).
*(نکته: داده‌های ۳۰ اپیزود مونت‌کارلو به صورت یکپارچه و با تمام جزییات آماری در جدول ۱ (Table I) ارائه شده و نمودار اختیاری fig_monte_carlo جهت تثبیت ساختار دقیق ۸ صفحه‌ای حذف گردید).*

---

## ۳. پاک‌سازی الگوهای هوش مصنوعی (De-AI Cleansing) و چگال‌سازی علمی
- **ریشه‌کنی واژگان کلیشه‌ای:** حذف کامل کلمات *delve, testament, pivotal, crucial, game-changing, moreover/furthermore تکراری در شروع جملات*.
- **تنوع ریتم و وزن نحوی:** ترکیب گزاره‌های کوتاه و قاطع با جملات مرکب تحلیلی و مستند مطابق الگوی ژورنال‌های تراز اول نظیر IEEE TPAMI و Nature Ecology & Evolution.
- **غنی‌سازی فیتوپاتولوژی:** استفاده از اصطلاحات تخصصی نظیر *actinodromous primary venation, concentric necrotic zonation, fungal pycnidia, uredinia pustules, chlorotic yellow halos, craspedodromous leaflets*.
- **مستندسازی آماری دقیق:** جایگزینی گزاره‌های کیفی مبهم با مقادیر دقیق آزمون آماری t دوطرفه ($t=26.15$, $p=1.03\times 10^{-21}$)، فاصله‌های اطمینان ۹۵٪، مصرف حافظه رم دقیق ($66.95\,\text{MB}$) و حجم APK ($22.88\,\text{MB}$).

---

## ۴. وضعیت کامپایل نهایی و تراز ۸ صفحه‌ای (IEEE Double-Column Layout)
- **موتور کامپایل:** `pdflatex` (MiKTeX 25.12) به همراه `bibtex`.
- **تعداد صفحات دقیق:** **۸ صفحه کامل** (بدون حتی یک خط سرریز در صفحه ۹).
- **وضعیت سرریزها:** صفر خطای Overfull hbox یا Overfull vbox.
- **توازن ستون‌های صفحه پایانی:** استفاده هوشمندانه از دستور `\balance` در ستون اول صفحه ۸ که ستون دوم (نتیجه‌گیری و ۲۰ مرجع کامل کتابنامه) را دقیقاً تا انتهای صفحه تراز کرده است.

</div>
