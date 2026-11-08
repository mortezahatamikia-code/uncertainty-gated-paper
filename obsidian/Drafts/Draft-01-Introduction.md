---
title: "Draft 01: Introduction & Literature Landscape"
type: draft
section: "01_introduction"
phase: 4
tags:
  - draft
  - paper-2
  - introduction
  - literature
created: 2026-11-08
status: completed
---

<div dir="rtl" style="font-family: inherit;">

# 📝 پیش‌نویس بخش اول: مقدمه مقاله MorphoPath-Edge و چشم‌انداز مراجع علمی

## ۱. خلاصه ساختار قیفی مقدمه (Historical Funnel Architecture)

بخش مقدمه مقاله در فایل `paper_morphopath/sections/01_introduction.tex` بر اساس ۷ لایه استدلالی کلان و پیوسته تدوین گردید:
1. **امنیت غذایی و پویایی عوامل بیماری‌زا:** تبیین خسارت ۲۲۰ میلیارد دلاری سالانه بیماری‌های گیاهی در جهان و محدودیت‌های روش‌های آزمایشگاهی (qPCR و ELISA).
2. **سیر تکامل تاریخی بینایی کامپیوتر در کشاورزی:** گذار از ویژگی‌های بافتی دستی (GLCM، HOG) به شبکه‌های پیچشی عمیق (ResNet، DenseNet بر روی دادگان آزمایشگاهی PlantVillage) و معضل نیاز به داده‌های حجیم برچسب‌دار.
3. **بحران کمیابی داده و یادگیری چندشاتی (Few-Shot Learning):** بررسی شبکه‌های متریک و متا-لرنینگ (MAML، ProtoNet) و چرایی فروپاشی آن‌ها در مواجهه با نویزهای شدید مزرعه در دادگان PlantDoc.
4. **معمای مدل‌های بنیادین بینایی (VFM Dichotomy):** تقابل هندسه ساختاری ماکرو ارگان برگ در DINOv2 با نشانگان پاتولوژی سلولی و کلروز در BioCLIP و اثبات غیرهمپوشان بودن این دو فضا.
5. **معضل خطای آبشاری روتر گونه‌ها و وابستگی به انسان:** شکست روترهای ۱۳ گونه‌ای سنتی (افت به ۴۳.۶۵٪) و ضرورت حذف اوراکل انسانی در مزارع غیرآزمایشگاهی.
6. **پارادایم راهگشای MorphoPath-Edge:** معرفی کهن‌الگوهای ۴ گانه برگ، تصحیح منیفولد بدون پارامتر (ADR-005) و تریاژ افتراقی بیزی.
7. **فهرست چهارگانه سهم‌های علمی (Key Contributions):** کهن‌الگوهای ماکرو، تصحیح بدون گرادیان منیفولد، تمایز انقباضی فیشر با آنسامبل پرامپت‌ها، و ثبت رکوردهای تجربی در سخت‌افزار لبه (۱۸.۶۶ FPS و ۲۲.۸۸ MB).

---

## ۲. خلاصه مراجع تدوین‌شده در `references.bib`

تعداد **۴۳ مقاله معتبر، تاییدشده و فاقد هرگونه توهم علمی** در دسته‌بندی‌های زیر گردآوری شد:
- امنیت غذایی و اکولوژی گیاه‌پزشکی: Savary et al. (Nature Ecol. Evol.), Bebber et al. (Nature Clim. Change), Strange & Scott (Annu. Rev. Phytopathol.), Carvajal-Yepes et al. (Science).
- پردازش تصویر سنتی و بینایی اولیه: Haralick et al. (IEEE Trans. SMC), Dalal & Triggs (CVPR), Camargo & Smith, Barbedo, Pydipati et al.
- یادگیری عمیق در پاتولوژی: Mohanty et al. (Front. Plant Sci.), Hughes & Salathé, Ferentinos, Too et al., Singh et al. (PlantDoc 2020).
- یادگیری چندشاتی و متریک: Vinyals et al. (Matching Nets), Snell et al. (ProtoNet), Finn et al. (MAML), Sung et al., Li et al., Argüeso et al.
- ریاضیات ماتریس و انطباق زمان آزمون: Ledoit & Wolf (2004), Tukey (1977), Wang et al. (Tent), Boudiaf et al. (TIM), Hu et al., Zhang et al., Bateni et al.
- مدل‌های بنیادین: Oquab et al. (DINOv2), Stevens et al. (BioCLIP), Radford et al. (CLIP), Caron et al., Dosovitskiy et al.
- سیستم‌های لبه و سلسله‌مراتبی: Silla & Freitas, Deng et al., Redmon & Farhadi, Jacob et al., Howard et al., Alsaadi & Zadeh (BioDINO-Edge 2026), Wu et al., Bi et al.

---
- 📌 بازگشت به [[Tasks/TASK-DRAFT-001|تسک TASK-DRAFT-001]]
- 📑 مطالعه تسک بعدی: [[Tasks/TASK-DRAFT-002|تسک TASK-DRAFT-002]]

</div>

