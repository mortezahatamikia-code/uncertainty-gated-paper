---
title: "TASK-HUMANIZE-005: High-Resolution Figure Generation (Architecture, Leaf Archetypes, and Statistical Boxplots)"
type: task
task_id: TASK-HUMANIZE-005
phase: 5
tags:
  - task
  - research/phase-5
  - figures
  - visualization
status: done
priority: High
depends_on: "TASK-HUMANIZE-004"
blocks: "TASK-HUMANIZE-006"
spec: "Specs/SPEC-MORPHOPATH-001.md"
created: 2026-11-08
---

<div dir="rtl" style="font-family: inherit;">

# 📌 TASK-HUMANIZE-005: تولید تصاویر باکیفیت بالا (معماری، اعمال روی برگ، و نمودارهای آماری)

## هدف تسک
تولید و تعبیه تصاویر علمی باکیفیت انتشار (۳۰۰ DPI) در پوشه `paper_morphopath/figures/` جهت غنای بصری و تبیین مفاهیم مقاله:
1. **تصویر معماری سیستم (`fig_architecture.png`):** دیاگرام دقیق و چندرنگ از خط لوله استنتاج دوعاملی MorphoPath-Edge (ورودی تصویر برگ مزرعه، استخراج ویژگی‌های DINOv2 و BioCLIP، تبدیل توان توکی، مرکززدایی منیفولد بدون پارامتر، روتر ۴ کهن‌الگو، فیشر انقباضی و گیتینگ بیزی تریاژ دوگانه).
2. **تصویر اعمال روی برگ و ۴ کهن‌الگوی گیاهی (`fig_archetypes.png`):** کلاژ بصری از برگ‌های واقعی مزرعه در ۴ کهن‌الگوی کلان زیستی (سولانوئید، ویتوئید، پوئید، روزوئید) همراه با نمایش تفاوت ویژگی‌های هندسی ارگان برگ در برابر علائم میکروسکوپی ضایعات پاتولوژی و اثر ماسک‌گذاری/مرکززدایی.
3. **نمودار آماری ۳۰ اپیزود مونت‌کارلو (`fig_monte_carlo.png`):** نمودار جعبه‌ای/توزیعی مقایسه عملکرد آماری MorphoPath-Edge در برابر مدل مسطح و روتر صلب، نمایش فواصل اطمینان ۹۵٪ و برتری قطعی معنادار آماری ($p < 10^{-14}$).
4. **نمودار دوبعدی t-SNE منیفولد (`tsne_manifold_rectification.png`):** تفکیک خوشه‌های منیفولد ویژگی قبل و بعد از تصحیح زمان آزمون.

## معیارهای پذیرش (Acceptance Criteria)
- [ ] تولید تصاویر در ابعاد استاندارد IEEE (عرض تک‌ستون یا دوستون) با رزولوشن ۳۰۰ DPI.
- [ ] ارجاع صریح به کلیه اشکال در متن مقاله (`\ref{fig:...}`).

---
- 📌 بازگشت به [[Tasks/Index|فهرست تسک‌ها]]

</div>
