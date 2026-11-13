---
title: "IDEA-025: Intermediate Transformer Layer Fusion (ITLF)"
type: idea
idea_id: IDEA-025
phase: 1
tags:
  - idea
  - research/phase-1
  - vit
  - intermediate-layers
  - feature-fusion
  - fine-grained-pathology
  - ponytail
status: rejected
verdict: "Rejected in TASK-OPT-022. Monotonic semantic degradation across all layers 7-11 (Layer 7: 8.73%, Layer 11: 36.11%, best blend: 64.29% vs L12 baseline: 65.08%)."
expected_gain: "+2.0% to +4.5% Top-1, breaks the 0.906 intra-host cosine bottleneck (Corn Blight vs GLS, Late vs Early Blight)"
mechanism: "Zero-parameter multi-layer extraction via forward hooks tapping intermediate ViT layers (e.g. Layer 8/9 texture & lesion geometry + Layer 12 high-level semantics)"
created: 2026-11-12
generated: { by: okf-enforcer/0.6, at: 2026-11-12T15:47:00Z }
---

<div dir="rtl" style="font-family: inherit;">

# 💡 IDEA-025: ادغام ویژگی‌های لایه‌های میانی ترنسفورمر (Intermediate Transformer Layer Fusion)

### ۱. صورت مسئله و انگیزه بالینی
در مدل‌های فعلی، صرفاً بردار توکن نهایی لایه ۱۲ ترنسفورمرها (DINOv2 ViT-S و BioCLIP ViT-B) استخراج و فریز می‌شود. با پیشروی در لایه‌های عمیق ViT، مدل تمایل دارد جزئیات بافتی موضعی و هندسه ریز لکه‌ها را به نفع مفاهیم معنایی کلان انتزاعی (مانند «برگ عمومی میزبان») فشرده یا حذف کند؛ این پدیده عامل اصلی چسبندگی کسینوسی ۰.۹۰۶ بین بیماری‌های هم‌میزبان (نظیر بلایت ذرت و لکه خاکستری ذرت) است.

### ۲. مکانیزم ریاضی و معماری
استفاده از قلاب‌های مستقیم پایتورچ (Forward Hooks) جهت استخراج توکن‌های لایه‌های میانی در حین عبور تک‌مرحله‌ای تصویر از درون شبکه:
* **لایه‌های میانی (Layer 7, 8, 9):** تمرکز غنی بر روی مرزهای ضایعه، بافت لکه‌ها، و الگوی آوندی (Venation Pattern).
* **لایه نهایی (Layer 12):** حفظ هویت تاکسونومیک کلان و ثبات بیولوژیکی.
* **الحاق و نرمال‌سازی کروی:**
  $$\mathbf{z}_{\text{fused}} = \left[ \alpha \cdot \mathbf{z}_{\text{mid}} \,\|\, (1-\alpha) \cdot \mathbf{z}_{\text{deep}} \right], \quad \|\mathbf{z}_{\text{fused}}\|_2 = 1$$
این ترکیب بدون افزودن هیچ وزن آموزش‌پذیری، فضای ویژگی را غنی کرده و اطلاعات پاتولوژی از دست رفته را احیا می‌کند.

### ۳. بودجه سخت‌افزاری و سرعت لبه
* **حجم اضافه (Weights):** **دقیقاً ۰.۰ مگابایت** (وزن‌های لایه‌ها هم‌اکنون درون مدل بارگذاری شده وجود دارند).
* **تاخیر اضافه در اسکن زنده دوربین:** **نزدیک به صفر (< ۰.۰۵ میلی‌ثانیه)**؛ محاسبات لایه‌ها در حین عبور عادی تصویر انجام می‌شود.
* **حافظه رم:** افزایش بعد بردار از ۸۹۶ به ۱۷۹۲ بعد، که در حافظه رم چندصد کیلوبایت بیشتر اشغال نمی‌کند.

</div>
