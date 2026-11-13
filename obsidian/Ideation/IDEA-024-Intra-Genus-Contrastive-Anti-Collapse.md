---
title: "IDEA-024: Intra-Genus Contrastive Anti-Collapse Projection Head"
type: idea
idea_id: IDEA-024
phase: 1
tags:
  - idea
  - research/phase-1
  - contrastive-learning
  - cosface
  - cluster-repulsion
status: pending
expected_gain: "+6% to +9% Top-1, forces 10° compressed intra-genus clusters to 60° separation"
mechanism: "Lightweight 2.5MB projection MLP trained with angular contrastive margin to push apart confused sister classes"
created: 2026-11-11
generated: { by: okf-enforcer/0.6, at: 2026-11-11T18:39:58Z }
---

<div dir="rtl" style="font-family: inherit;">

# 💡 IDEA-024: هد دافعه زاویه‌ای هم‌جنس (Intra-Genus Contrastive Anti-Collapse Head)

### ۱. صورت مسئله و انگیزه
کلاس‌های مربوط به گوجه (۸ بیماری) و ذرت (۳ بیماری) در فضای منیفولد به دلیل ویژگی‌های مورفولوژیک مشترک، مثل فنر فشرده شده‌اند و زاویه بین آن‌ها کمتر از ۱۰ درجه است (فاصله کسینوسی > ۰.۹۰). در نتیجه کوچک‌ترین نویز نوری، کلاس را به بیماری مجاور می‌اندازد.

### ۲. مکانیزم ریاضی
یک هد پروجکشن چندلایه‌ای سبک ($896 \to 512 \to 256$ با حجم تقریبی **۲.۵ مگابایت**):
آموزش با تابع هزینه زاویه‌ای متضاد (Supervised Contrastive + CosFace Margin) در فاز بارگذاری اولیه/بک‌گراند (`fit()`) با یک ماموریت اختصاصی: **اعمال نیروی دافعه کلاستری (Cluster Repulsion Force)** تا زاویه بین بلایت ذرت و لکه خاکستری از ۱۰ درجه به ۶۰ درجه باز شود.

### ۳. رعایت اکید شرط سرعت اسکن دوربین (قانون کاربر)
- **در زمان اسکن زنده (Inference per frame):** فقط ۲ ضرب ماتریسی سبک انجام می‌شود که تاخیر آن کمتر از **۰.۰۲۵ میلی‌ثانیه** (۲۵ میکروثانیه!) است. هیچ‌گونه کندی در زمان اسکن رخ نمی‌دهد.
- **فاز آموزش و بهینه‌سازی دافعه:** منحصراً یک‌بار در بارگذاری اولیه در پس‌زمینه (Background Loading) اجرا می‌شود و سرعت اسکن دوربین به هیچ وجه دچار وقفه چندثانیه‌ای نخواهد شد.
- **حجم اضافه:** حدود ۲.۵ مگابایت (کاملاً درون بودجه مجاز زیر ۵ مگابایت).

</div>
