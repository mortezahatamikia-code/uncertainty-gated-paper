---
title: "TASK-REFINE-001: Comprehensive Academic Prose Polish, Humanizing, and IEEE Standards Verification"
type: task
task_id: TASK-REFINE-001
phase: 6
tags:
  - task
  - research/phase-6
  - humanizing
  - ieee-standards
  - peer-review
status: done
priority: High
depends_on: "TASK-HUMANIZE-001, TASK-HUMANIZE-002, TASK-HUMANIZE-003, TASK-HUMANIZE-004, TASK-HUMANIZE-005, TASK-HUMANIZE-006"
blocks: ""
spec: "Specs/SPEC-MORPHOPATH-001.md"
created: 2026-11-08
generated: { by: okf-enforcer/0.6, at: 2026-11-08T19:19:48Z }
---

<div dir="rtl" style="font-family: inherit;">

# 📌 TASK-REFINE-001: بازبینی جامع متنی، انسانی‌نویسی آکادمیک و تطبیق استانداردهای چاپ IEEE

## ۱. تحلیل و یافته‌های بازرسی دقیق (Direct Audit Findings)

### الف) ریشه‌یابی و اصلاح فاصله مراجع (References Spacing & Typography)
- **علت چسبندگی حروف و فشردگی قبلی:** در فایل اصلی، بازتعریف غیراستاندارد محیط `\thebibliography` با سایز `\scriptsize` (حدود ۷ پوینت) و فاصله منفی بین آیتم‌ها (`\itemsep -0.8pt`) اعمال شده بود. این امر باعث می‌شد خطوط مراجع درون یکدیگر فشرده شده و متن ناخوانا و چسبیده به نظر برسد.
- **تطبیق با استاندارد رسمی IEEEtran:**
  1. محیط مراجع به پیاده‌سازی رسمی و بومی کلاس `IEEEtran.cls` با اندازه فونت استاندارد `\footnotesize` برگردانده شد.
  2. فاصله خطوط و پاراگراف‌ها با موتور بومی IEEE هماهنگ شد تا کشیدگی نامتعارف کلمات حذف شود.
  3. در فایل `references.bib`، اسامی خاص و سرواژه‌ها مانند `{PlantDoc}`, `{DINOv2}`, `{BioCLIP}`, `{TENT}`, `{BioDINO-Edge}` درون آکولاد قرار گرفتند تا BibTeX حروف بزرگ آن‌ها را طبق استاندارد IEEE حفظ کند.
  4. رفع شکستگی نامناسب مراجع: با انتقال فراخوانی دستور `\balance` به ستون اول صفحه ۸، تیتر `REFERENCES` و تمام ۲۰ مرجع به صورت یکدست در ستون دوم صفحه ۸ قرار گرفتند و شکستگی ناخوشایند مرجع [1] در ستون اول برطرف شد.

### ب) بهره‌برداری از فضای ۳ خطی انتهای صفحه ۸ (Robotic & Field Feasibility)
- در ستون اول صفحه ۸، زیربخش `VII-C (Field Feasibility on Autonomous Agro-Robotic Systems)` با افزودن حدود ۳ تا ۴ خط تحلیل مهندسی و انسانی غنی‌سازی شد:
  - تشریح هماهنگی زمان‌بندی موتور استنتاج با شیرهای برقی سلونوئیدی مبتنی بر مدولاسیون پهنای پالس (PWM) روی بوم‌های پاشش سمپاش.
  - تعیین دقیق کریدور مکانی ۱۵ سانتی‌متری در سرعت‌های حرکتی متداول تراکتور و ربات‌های صحرایی (۸ تا ۱۲ کیلومتر بر ساعت) جهت جلوگیری از آلودگی محیط زیست و اتلاف سموم شیمیایی.

---

## ۲. چک‌لیست بازنویسی انسانی‌تر و آکادمیک‌تر (Section-by-Section Humanizing)

| بخش | عبارت نیازمند اصلاح / کلیشه هوش مصنوعی | بازنویسی آکادمیک، عینی و انسانی‌تر | وضعیت |
| :--- | :--- | :--- | :--- |
| **چکیده (Abstract)** | "is paramount for global food security" (کلیشه AI) | "Autonomous detection of foliar phytopathogens in unconstrained agricultural canopies remains limited by..." | [x] اعمال شد |
| **چکیده (Abstract)** | "decisively shatters the historical 60% barrier" (لحن ژورنالیستی) | "surpasses previous human-in-the-loop and flat baselines by +11.84% ($p = 1.03 \times 10^{-21}$), establishing an autonomous 62.30% field benchmark." | [x] اعمال شد |
| **مقدمه (Sec I)** | "curtail... precipitating... destabilizing" (سه‌گانه افعال دراماتیک) | "account for an estimated 20%–40% reduction in global crop yield annually, imposing economic burdens exceeding $220 billion..." | [x] اعمال شد |
| **مقدمه (Sec I)** | "Prior systems survived this collapse only by assuming an artificial human oracle" | "Prior studies compensated for this degradation by introducing a human-in-the-loop oracle, wherein growers manually specify crop species [15]." | [x] اعمال شد |
| **کارهای مرتبط (Sec II)** | تکرار آغاز جملات با "In natural canopies...", "In natural fields..." | تنوع‌بخشی به فاعل جملات و تمرکز بر محدودیت‌های پهنای باند حافظه در TENT و مدل‌های گرادیانی در لبه | [x] بازبینی شد |
| **فرمول‌بندی (Sec III)** | اثبات گزاره ۱ در خصوص خنثی‌سازی ترنسلیشن توزیع | تصریح ریاضی بر اینکه میانگین‌گیری بسته و کسر $\mu_q$ بردار جابجایی $\Delta = \mu_q - \mu_s$ را دقیقاً صفر می‌کند قبل از تصویر روی کره واحد. | [x] تصریح شد |
| **روش‌شناسی (Sec IV)** | نشانه‌گذاری انتهای روابط ریاضی (Punctuation) | بررسی اینکه تمام معادلات دارای کاما یا نقطه در انتهای خط طبق گرامر استاندارد IEEE باشند. | [x] بازبینی شد |
| **آزمایش‌ها (Sec V)** | Underfull hbox در شکستن کلمات خطوط ۵۱-۵۲ | بازتنظیم فاصله‌بندی و عبارات پاراگراف مقیاس‌پذیری PlantVillage جهت حذف هشدارهای جعبه افقی | [x] اصلاح شد |
| **تحلیل ابلیشن (Sec VI)** | لیست آیتم‌های کهن‌الگو با `\begin{enumerate}` | تبدیل به پاراگراف‌های توپر متنی (`\noindent\textbf{1) Solanoid ($A_0$):}`) برای بهبود زیبایی بصری و تراز ستون | [x] اعمال شد |
| **استقرار لبه (Sec VII)** | محل قرارگیری دستور `\balance` | انتقال به متن بخش پایانی در ستون اول صفحه ۸ جهت حذف کامل اخطار `balance in second column` | [x] اصلاح شد |

### ج) ارتقای شکل ۱ به ماتریس نقشه‌های توجه و گرما‌نگاشت پاتولوژی (Attention & Saliency)
- **رویکرد تلفیقی پیشرفته:** تصویر کلیدی اول (`fig_archetypes.png`) با اسکریپت `experiments/phase3_morphopath/generate_archetypes_saliency_figure.py` ارتقا یافت:
  - **ردیف ۱:** برگ واقعی مزرعه‌ای PlantDoc برای هر ۴ کهن‌الگو (Solanoid, Vitoid, Pooid, Rosoid).
  - **ردیف ۲:** نقشه‌های توجه واقعی DINOv2 استخراج‌شده توسط هوک توجه (`Macro-Geometry Attention`)، که اثبات می‌کند مدل برای مسیریابی کهن‌الگو به رگبرگ‌ها، حاشیه برگ و تقارن فیلوتاکسی تکیه می‌کند.
  - **ردیف ۳:** گرما‌نگاشت تفکیک‌شده پاتولوژی (`Decoupled Lesion Saliency Overlay`) که کانون‌های لکه‌های قارچی، پوسیدگی سیاه، تاول‌های زنگ و زون‌های نکروزه را کاملاً مستقل از فرم برگ برجسته می‌سازد.
- **به‌روزرسانی کپشن و متن:** کپشن `fig:archetypes` در `paper_morphopath/sections/01_introduction.tex` به طور کامل به‌روزرسانی شد تا تفکیک این ۳ ردیف را تشریح کند، در حالی که ارتفاع و ابعاد فیزیکی بنر در ۴.۲ سانتی‌متر تثبیت شد تا بودجه ۸ صفحه‌ای حفظ گردد.

---

## ۳. معیارهای پذیرش نهایی (Acceptance Criteria)
- [x] **تعداد صفحات دقیق:** فایل PDF نهایی (`paper_morphopath/main.pdf`) دقیقاً در **۸ صفحه کامل** بدون هیچ‌گونه سرریز به صفحه ۹.
- [x] **تعداد تصاویر دقیق:** دقیقاً **۳ شکل باکیفیت و استاندارد** (Fig 1: کهن‌الگوها، Fig 2: معماری سیستم، Fig 3: منیفلد تصحیح t-SNE).
- [x] **استاندارد مراجع:** استفاده از فونت `\footnotesize` رسمی IEEE با فاصله خطوط راحت و خوانا، بدون هیچ چسبندگی حروف یا خطوط.
- [x] **توازن ستون‌ها:** توازن زیبای دو ستون در صفحه ۸ با شروع تمیز مراجع از ابتدای ستون دوم.
- [x] **انطباق کامل با قوانین عدم تغییر:** پوشه‌های `paper/` و `android_app/` کاملاً دست‌نخورده و بدون تغییر باقی مانده‌اند.

---
- 📌 بازگشت به [[Tasks/Index|فهرست تسک‌ها]]
- 📌 مشاهده [[Project Board.canvas|تخته کانبان]]

</div>
