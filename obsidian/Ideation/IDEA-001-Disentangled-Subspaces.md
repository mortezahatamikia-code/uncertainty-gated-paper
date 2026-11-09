---
title: "IDEA-001: Orthogonal Disentanglement of Morphology and Pathology"
type: idea
idea_id: IDEA-001
phase: 1
tags:
  - idea
  - research/phase-1
  - math
status: rejected
expected_gain: "+4% to +8% reduction in cross-species symptom entanglement"
measured_impact: "-2.38% to -28.57% accuracy degradation (Rejected due to pathogen-host anatomical coupling)"
mechanism: "Orthogonal SVD projection separating geometric shape from cellular necrosis"
created: 2026-11-08
validated_date: 2026-11-08
---

<div dir="rtl" style="font-family: inherit;">

# 💡 IDEA-001: تفکیک متعامد زیرفضاهای ریخت‌شناسی و آسیب‌شناسی

> [!CAUTION] وضعیت ارزیابی تجربی: ❌ رد شد (Rejected)
> در آزمایش‌های فاز ۱ روی ۲۵۲ تصویر مزرعه‌ای PlantDoc، اعمال تصویر متعامد SVD و حذف ابعاد مشترک کوواریانس متقابل، دقت تشخیص را به شدت کاهش داد (از ۵۰.۰۰٪ تا ۲۱.۴۳٪) و دقت روتر را از ۹۱.۶۷٪ به ۴۲.۸۶٪ ساقط کرد. علت این امر، درهم‌تنیدگی زیستی پاتوژن با رگبرگ‌ها و بافت آناتومیک میزبان است که نمی‌تواند به صورت برداری تفکیک شود.

## ۱. فرضیه علمی (Scientific Hypothesis)
در استخراج ویژگی ترکیبی ۸۹۶ بعدی BioDINO-Edge ($384 + 512$)، ویژگی‌های پس‌زمینه علف‌های هرز و کانتور برگ با الگوهای لکه‌های بیماری درهم‌تنیده (Entangled) می‌شوند. 
**فرضیه اولیه:** اگر ویژگی‌های DINOv2 صرفاً برای قفل کردن «فرم و فیلوتاکسی برگ» و ویژگی‌های BioCLIP صرفاً برای ارزیابی «بافت بیماری» محدود شوند، استقلال آماری دو منیفولد افزایش یافته و تداخل تشخیصی کاهش می‌یابد.

## ۲. نتایج اعتبارسنجی تجربی (Empirical Findings)
- محاسبه ماتریس کوواریانس متقابل $C_{cross} = \frac{1}{N} Z_{dino}^T Z_{bio}$ و تجزیه مقادیر منفرد (SVD).
- با حذف $k$ بعد اول مشترک:
  - $k=1$: افت دقت به ۴۷.۶۲٪ (-۲.۳۸٪)
  - $k=2$: افت دقت به ۴۶.۴۳٪ (-۳.۵۷٪)
  - $k=4$: افت دقت به ۴۱.۶۷٪ (-۸.۳۳٪)
  - $k=16$: سقوط دقت به ۲۸.۱۷٪ (-۲۱.۸۳٪)
  - $k=32$: سقوط کامل به ۲۱.۴۳٪ (-۲۸.۵۷٪)
- **دلیل زیستی رد ایده:** پاتولوژی گیاهی از هندسه برگ جداپذیر نیست؛ ضایعات پاتولوژیک بر بستر رگبرگ‌ها، حاشیه‌ها و مزوفیل ساختار می‌یابند و حذف اشتراک این فضاها اطلاعات حیاتی بافتی را از بین می‌برد.

---
- 📊 مشاهده لاگ کامل آزمایش: [[Logs/Log-Phase1-Empirical-Validation|گزارش بنچمارک فاز ۱]]
- 📌 بازگشت به [[Ideation/Index|فهرست ایده‌ها]]

</div>
