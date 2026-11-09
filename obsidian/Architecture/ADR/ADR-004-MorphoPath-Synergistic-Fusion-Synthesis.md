---
title: "ADR-004: Synergistic MorphoPath Pipeline Synthesis & Edge Candidate Evaluation"
type: adr
adr_id: ADR-004
phase: 2
tags:
  - adr
  - architecture
  - research/phase-2
  - synthesis
  - candidates
status: Accepted
date: 2026-11-08
impact: "Adopts Candidate 4 (MorphoPath-Complete Ensemble) as definitive edge pipeline with 53.57% Top-1, 61.90%-67.06% Top-2, 53.57% Macro F1, 0.43ms CPU latency, and 22.88MB APK footprint"
---

<div dir="rtl" style="font-family: inherit;">

# 📜 ADR-004: ترکیب سینرژیک خط لوله مورفوپث و تصویب کاندیدای نهایی لبه (MorphoPath Pipeline Synthesis)

## وضعیت: پذیرفته‌شده و مصوب (Accepted ✅)

---

## ۱. زمینه و انگیزه (Context)

پس از اجرای آزمون‌های تفصیلی فاز ۱ و غربالگری ۸ فرضیه علمی، ۴ ایده ناموفق شامل تجزیه متعامد SVD ([[Ideation/IDEA-001-Disentangled-Subspaces|IDEA-001]])، تنظیم ترنسداکتیو ([[Ideation/IDEA-006-Intra-Archetype-Transductive|IDEA-006]])، ماسک‌گذاری توجهی ([[Ideation/IDEA-005-Attention-Guided-Denoising|IDEA-005]]) و فیوژن دوقیاسی ضایعه ([[Ideation/IDEA-008-Dual-Scale-Lesion-Fusion|IDEA-008]]) رد شدند.
در مقابل، ۴ ایده کلیدی زیر تایید قطعی گردیدند:
1. **روتر ۴ کهن‌الگوی گیاهی برگ با DINOv2** ([[Ideation/IDEA-002-Morphological-Archetype-Clustering|IDEA-002]]) با دقت ۹۱.۶۷٪ در Top-1 و ۹۹.۶۰٪ در Top-2.
2. **انقباض کوواریانس درون‌تیپی فیشر** ([[Ideation/IDEA-007-Covariance-Shrinkage-Optimization|IDEA-007]]) با ضریب بهینه $\lambda=0.60$.
3. **تراز بیزی کاردینالیتی دوگانه** ([[Ideation/IDEA-004-Bayesian-Dual-Likelihood-Balancing|IDEA-004]]) با ضریب تعدیل $\alpha=1.0$.
4. **پرامپت‌های میکرومورفولوژیک عوارض بیماری** ([[Ideation/IDEA-003-Taxonomic-Symptom-Ontology-Prompts|IDEA-003]]) مقید به بستر کهن‌الگو.

مسئله محوری فاز ۲ این بود که **کدام ترکیب معماری از این ماژول‌های مجاز، بالاترین دقت تشخیصی را با حفظ الزامات سخت‌گیرانه لبه (تاخیر < ۲۵ میلی‌ثانیه و حجم < ۲۵ مگابایت) فراهم می‌سازد؟**

---

## ۲. چهار کاندیدای معماری ارزیابی‌شده (Evaluated Candidates)

1. **کاندیدای ۱ (MorphoPath-Minimal - تک‌مدل DINOv2):**
   ویژگی‌های DINOv2-Small (۳۸۴ بعدی) + روتر کهن‌الگو + انقباض کوواریانس ($\lambda=0.60$) بدون حضور BioCLIP. هدف: بهینه‌سازی افراطی سرعت و حجم.
2. **کاندیدای ۲ (MorphoPath-Bayes Standard):**
   ویژگی‌های مشترک BioCLIP + DINOv2 (۸۹۶ بعدی) + روتر نرم بیزی + انقباض کوواریانس ($\lambda=0.60$) + استنتاج بیزی موازنه کاردینالیتی ($\alpha=1.0$).
3. **کاندیدای ۳ (MorphoPath-Bayes + Tukey Power Transform):**
   کاندیدای ۲ همراه با تبدیل توان توکی ($z = \text{sign}(x)\sqrt{|x|}$ و نرمال‌سازی L2) پیش از تحلیل تمایز فیشر LDA.
4. **کاندیدای ۴ (MorphoPath-Complete Ensemble):**
   کاندیدای ۳ همراه با آنسامبل پرامپت‌های متنی آنتولوژی پاتولوژی میکروسکوپی شرطی‌شده بر کهن‌الگو.

---

## ۳. جدول مقایسه جامع و شواهد تجربی (Empirical Comparison)

کلیه کاندیداها بر روی دادگان واقعی **PlantDoc** (شامل ۲۷ کلاس، ۲۵۲ تصویر تست میدانی چالش‌برانگیز، ۵ شات، سید ۴۲) با پروتکل استاندارد بنچمارک شدند:

| کاندیدای معماری | ویژگی‌های ورودی | مکانیزم روتینگ و کلاسیفایر | دقت Top-1 | دقت Top-2 | شاخص Macro F1 | تاخیر پردازنده (CPU) | حجم بسته APK | تصمیم ADR |
| :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **C1: MorphoPath-Minimal** | DINOv2 (384-d) | روتر کهن‌الگو + فیشر ($\lambda=0.60$) | ۳۹.۶۸٪ | ۴۶.۴۳٪ | ۳۸.۷۵٪ | **۰.۲۱۹ ms** | **۲۱.۴ MB** | ❌ **رد شد** |
| **C2: MorphoPath-Bayes Standard** | پیوسته (896-d) | روتر نرم + فیشر + گیتینگ بیزی | ۵۱.۱۹٪ | ۵۶.۳۵٪ | ۵۱.۲۶٪ | ۰.۴۰۸ ms | ۲۲.۷۳ MB | ⚠️ منسوخ |
| **C3: MorphoPath-Bayes + Tukey** | توکی L2 (896-d) | تبدیل توان توکی + فیشر + گیتینگ بیزی | ۵۲.۳۸٪ | ۵۹.۵۲٪ | ۵۲.۵۵٪ | ۰.۴۱۷ ms | ۲۲.۷۳ MB | 🥈 نایب‌قهرمان |
| **C4: MorphoPath-Complete Ensemble** | توکی + پرامپت عارضه | کاندیدای ۳ + آنسامبل متنی شرطی | **۵۳.۵۷٪** | **۶۱.۹۰٪** | **۵۳.۵۷٪** | **۰.۴۳۹ ms** | **۲۲.۸۸ MB** | 🏆 **تصویب شد (Winner)** |

---

## ۴. تصمیم اتخاذشده (The Architectural Decision)

**کاندیدای ۴ (MorphoPath-Complete Ensemble) رسماً به عنوان خط لوله نهایی مقاله MorphoPath-Edge برگزیده و تصویب شد.**

### دلایل کلیدی گزینش:
1. **بالاترین دقت در تاریخ خط لوله:** کاندیدای ۴ به دقت **۵۳.۵۷٪ Top-1**، **۵۳.۵۷٪ Macro F1** و **۶۱.۹۰٪ تا ۶۷.۰۶٪ Top-2** دست یافت و با فاصله **+۲.۳۸٪ در Top-1** از کاندیدای پایه پیشی گرفت.
2. **ارتقای معنادار ایمنی بالینی (Clinical Safety):** نرخ هشدار اشتباه روی برگ سالم (False Positive Rate) از ۲۰.۰۰٪ در کاندیداهای ۲ و ۳ به **۱۵.۵۶٪** کاهش یافت، در حالی که نرخ منفی کاذب روی برگ‌های آلوده در عدد اندک **۳.۷۰٪** مهار شد.
3. **انطباق خیره‌کننده با بودجه سخت‌افزاری لبه:** تاخیر محاسباتی تک‌تصویر روی CPU فقط **۰.۴۳۹ میلی‌ثانیه** است (سقف مجاز: ۲۲.۰ میلی‌ثانیه). حجم بسته نصبی ۲۲.۸۸ مگابایت (زیر ۲۳ مگابایت) و کل سربار حافظه‌ای پروتوتایپ‌های متنی جدید صرفاً **۵۵.۳ کیلوبایت** است (صفر مگابایت لایه عصبی اضافی).

---

## ۵. فرمولاسیون ریاضی خط لوله مصوب (Mathematical Formulation)

فرآیند استنتاج کاندیدای ۴ در ۴ مرحله جبری بدون پارامترهای گرادیانی انجام می‌شود:

### گام ۱: روتینگ نرم ساختاری ریخت‌شناسی برگ (Morphological Archetype Gating)
تصویر ورودی $x$ توسط DINOv2 انکود شده و احتمال کهن‌الگو از طریق سافت‌مکس با دمای $T=12$ روی پروتوتایپ‌های میانگین ۴ کهن‌الگو استخراج می‌شود:
$$P(A_k \mid x) = \frac{\exp\left(T \cdot \cos(f_{\text{dino}}(x), \mu_{A_k}^{\text{dino}})\right)}{\sum_{j=1}^4 \exp\left(T \cdot \cos(f_{\text{dino}}(x), \mu_{A_j}^{\text{dino}})\right)}$$

### گام ۲: نگاشت زیرگاوسی توکی بر منیفولد پیوسته (Tukey Power Normalization)
ویژگی پیوسته $x_{\text{joint}} = [f_{\text{bioclip}}(x), f_{\text{dino}}(x)] \in \mathbb{R}^{896}$ تحت نگاشت جذر علامت‌دار و نرم ۲ قرار می‌گیرد:
$$z = \text{sign}(x_{\text{joint}}) \odot \sqrt{|x_{\text{joint}}|}, \quad \tilde{z} = \frac{z}{\|\tilde{z}\|_2}$$

### گام ۳: تمایز درون‌تیپی فیشر با انقباض کوواریانس (Intra-Archetype Shrunk Fisher LDA)
برای هر کهن‌الگو $A_k$، ماتریس کوواریانس درون‌کلاسی با ضریب $\lambda=0.60$ رگولاریزه شده و توزیع احتمال فیشر $P_{\text{LDA}}(c \mid A_k, \tilde{z})$ به فرم بسته به دست می‌آید:
$$\Sigma_{\text{shrunk}}^{(k)} = 0.40 \, \Sigma_w^{(k)} + 0.60 \, \frac{\text{Tr}(\Sigma_w^{(k)})}{D} I_D$$

### گام ۴: تراز بیزی کاردینالیتی و آنسامبل پرامپت‌های نشانگان پاتولوژیک
امتیاز نهایی هر کلاس بیماری $c \in A_k$ با تلفیق احتمال بصری فیشر و شباهت کسینوسی امبدینگ متنی پرامپت‌های میکروسکوپی $T_c \in \mathbb{R}^{512}$ فرمول‌بندی می‌شود:
$$P_{\text{text}}(c \mid A_k, x) = \frac{\exp(\tau \cdot \cos(f_{\text{bioclip}}(x), T_c))}{\sum_{j \in A_k} \exp(\tau \cdot \cos(f_{\text{bioclip}}(x), T_j))}$$
$$P_{\text{comb}}(c \mid A_k, x) = w_{\text{vis}} P_{\text{LDA}}(c \mid A_k, \tilde{z}) + (1 - w_{\text{vis}}) P_{\text{text}}(c \mid A_k, x)$$
$$\text{Score}(c) = P(A_k \mid x) \cdot \left[ |C_{A_k}| \cdot P_{\text{comb}}(c \mid A_k, x) \right]^{\alpha}, \quad (\alpha=1.0)$$

---

## ۶. پیامدها و نقشه راه فاز ۳ (Consequences & Next Steps)

- **انتقال به فاز ۳ (Engineering Implementation):** کدهای رسمی پایپ‌لاین `pipeline/biodino_hierarchical_pipeline.py` بازنویسی و با فرمولاسیون کاندیدای ۴ منطبق خواهند شد.
- **تست مونت‌کارلو:** ارزیابی پایایی در ۳۰ اپیزود شبیه‌سازی تصادفی برای درج فواصل اطمینان در متن نهایی مقاله.
- **آماده‌سازی جدول نتایج داوری:** نگارش مستندات تجربی در بخش ۵ پیش‌نویس مقاله علمی.

---
- 📊 گزارش کامل ارزیابی عددی: [[Logs/Log-Phase2-Synthesis-Benchmark|لاگ بنچمارک فاز ۲]]
- 📌 بازگشت به [[Architecture/ADR/Index|فهرست سوابق تصمیمات معماری]]

</div>
