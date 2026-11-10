---
title: Research Command Center & Knowledge Graph
type: dashboard
tags:
  - dashboard
  - research/control-center
updated: 2026-11-08
generated: { by: okf-enforcer/0.6, at: 2026-11-09T14:12:18Z }
---

<div dir="rtl" style="font-family: inherit;">

# ⚡ مرکز فرماندهی و گراف پژوهش ایجنتیک (Research Hub)

> [!IMPORTANT] تخته بصری ۸ مرحله‌ای پژوهش (طرح مارپیچی Meander)
> - 📌 **تخته بصری کانبان در ابسیدین**: [[Project Board.canvas]] را باز کنید تا هر ۸ گام جریان ریسرچ را در الگوی مارپیچی ۲ ردیفه بدون لیبل‌های مزاحم مشاهده نمایید.
> - 📜 **منشور و اهداف پژوهش**: [[Specs/00 - Research Protocol|مطالعه پروتکل جامع پژوهش (SPEC-MASTER-001)]]
> - 🎯 **گام ۴ (بهینه‌سازی کمینه‌گرا - تکمیل شد ✅)**: [[Tasks/TASK-OPT-001|جبران و سبقت کامل از بیس‌لاین ۲ با دقت ۸۹.۵۷٪ و سبقت از بایودینو با ۹۵.۲۹٪]]
> - 🧼 **گام ۵ (کد تمیز، DRY و ماژولارسازی عمیق - تکمیل شد ✅)**: [[Tasks/TASK-CLEAN-004|تفکیک ماژولار موتور]] و [[Tasks/TASK-CLEAN-005|شکستن عمیق به میکرومیکرومژول‌های زیر ۲۵۰ خط]]
> - 🔍 **گام ۸ (ممیزی و سابمیت - در انتظار اجرا)**: [[Tasks/TASK-AUDIT-001|استرس‌تست داور ۲، اعتبارسنجی بازتولیدپذیری و پکیج نهایی سابمیت]]
> - 🏆 **گزارش مقایسه جامع و توجیه علمی مقاله دوم**: [[Architecture/Master-Comparative-Benchmark-BioDINO-vs-MorphoPath|مطالعه بنچمارک تطبیقی کامل (PlantDoc، PlantVillage و لبه)]]
> - 🕸️ **نمای گراف سراسری روابط**: کلید میانبر `Ctrl + G` را در ابسیدین فشار دهید.

---

## 💡 فاز ۱: فرضیات و ایده‌های اولیه (Ideation & Hypotheses)

```dataview
TABLE WITHOUT ID
  file.link AS "عنوان فرضیه / ایده",
  mechanism AS "مکانیزم نوآورانه",
  expected_gain AS "دستاورد مورد انتظار",
  status AS "وضعیت بررسی"
FROM "Ideation" AND #idea
SORT file.ctime DESC
```

---

## 🧪 فاز ۲: ترکیب، غربالگری و سوابق تصمیم معماری (Synthesis & ADRs)

```dataview
TABLE WITHOUT ID
  file.link AS "شماره و عنوان ADR",
  status AS "وضعیت تصمیم (Accepted/Rejected)",
  impact AS "اثر روی دقت و سرعت",
  date AS "تاریخ تصمیم"
FROM "Architecture/ADR" AND #adr
SORT file.name ASC
```

---

## ⚡ فاز ۳: پیاده‌سازی و بنچمارک هوش مصنوعی (AI Engine Implementation)

```dataview
TABLE WITHOUT ID
  file.link AS "نام و شناسه تسک",
  status AS "وضعیت اجرا",
  priority AS "اولویت",
  depends_on AS "پیش‌نیازها",
  blocks AS "مسدودکننده"
FROM "Tasks" AND #task
SORT priority DESC, file.name ASC
```

---

## 📝 فاز ۴: نگارش علمی و پیش‌نویس بخش‌های مقاله (Scientific Drafting)

```dataview
TABLE WITHOUT ID
  file.link AS "عنوان بخش مقاله",
  target_section AS "سکشن ژورنال",
  status AS "وضعیت نگارش",
  word_count AS "حجم تقریبی (کلمات)"
FROM "Drafts" AND #draft
SORT file.name ASC
```

---

## ✍️ فاز ۵: انسانی‌نویسی، ویرایش ضد-AI و غنی‌سازی بصری (Humanizing & Polish)

```dataview
TABLE WITHOUT ID
  file.link AS "سند بازنویسی / غنی‌سازی",
  target_section AS "بخش هدف",
  anti_ai_status AS "وضعیت پیرایش لحن",
  figures_tables AS "وضعیت نمودارها و جداول"
FROM "Reviews" AND #humanize
SORT file.name ASC
```

---

## 🔍 فاز ۶: ممیزی داوری، استرس‌تست و افق‌های آینده (Audit & Horizons)

```dataview
TABLE WITHOUT ID
  file.link AS "عنوان ممیزی / افق آتی",
  type AS "نوع سند (Review/Horizon)",
  focus AS "محور تمرکز",
  status AS "وضعیت"
FROM "Reviews" AND (#audit OR #horizon)
SORT file.name ASC
```

---

## 🔗 ناوبری سریع دایرکتوری‌های پروژه

| دایرکتوری | محتوا و هدف | پیوند دسترسی |
| :--- | :--- | :--- |
| **💡 Ideation/** | حوضچه ایده‌ها و فرضیات اولیه علمی | [[Ideation/Index\|ورود به مخزن ایده‌ها]] |
| **📜 Specs/** | اسناد نیازمندی‌ها، سناریوها و پروتکل پژوهش | [[Specs/Index\|ورود به مشخصات (Specs)]] |
| **🏛️ Architecture/** | معماری سیستم و سوابق تصمیمات فنی (ADR) | [[Architecture/System Overview\|نمای معماری]] \| [[Architecture/ADR/Index\|فهرست ADRها]] |
| **📌 Tasks/** | تسک‌های اجرایی پیاده‌سازی و ارزیابی کد | [[Tasks/Index\|فهرست تجمیعی تسک‌ها]] |
| **📝 Drafts/** | پیش‌نویس بخش‌های مختلف مقاله برای ژورنال | [[Drafts/Index\|مخزن پیش‌نویس مقاله]] |
| **✍️ Reviews/** | چک‌لیست‌های انسانی‌نویسی، ممیزی داوری و افق‌های آینده | [[Reviews/Index\|اسناد ممیزی و پیرایش]] |
| **📜 Logs/** | لاگ‌های متنی بنچمارک‌ها، تاریخچه اجرا و خروجی‌ها | [[Logs/Index\|لاگ جلسات و نتایج]] |

</div>
