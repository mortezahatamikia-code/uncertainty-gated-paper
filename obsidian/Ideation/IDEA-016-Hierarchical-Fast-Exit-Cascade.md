---
title: "IDEA-016: Hierarchical Fast-Exit Decision Cascade (Early Triage Speedup)"
type: idea
idea_id: IDEA-016
phase: 1
tags:
  - idea
  - research/phase-1
  - edge
  - latency
  - fast-exit
status: pending
expected_gain: "Cut decision head latency by 59% (0.185 ms -> 0.075 ms), boost streaming FPS to ~22.1 FPS"
mechanism: "Early confidence triage exiting on confident manifold predictions, reserving LDA/prompts for ambiguous queries"
created: 2026-11-11
---

<div dir="rtl" style="font-family: inherit;">

# 💡 IDEA-016: خروج زودهنگام آبشاری لبه (Hierarchical Fast-Exit Decision Cascade)

### ۱. انگیزه و بیان مسئله
در استریم پیوسته ویدئویی دوربین مزرعه، بیش از ۷۰ تا ۸۰ درصد فریم‌ها تصاویری کاملاً واضح از برگ سالم یا یک بیماری کلاسیک بارز هستند. اجرای تمام لایه‌های محاسباتی (LDA، پرامپت‌های متنی و مهار سایبان) برای این موارد واضح، مصرف غیرضروری باتری و اتلاف توان پردازشی است.

### ۲. مکانیزم پیشنهادی
طراحی گیت تصمیم‌گیری دو مرحله‌ای:
1. **مسیر سریع (Fast-Path):** اگر در انتهای مرحله تطبیق منیفولد توکی، اطمینان کلاس اول $p_1 > 0.88$ و مارجین تفاضلی با رتبه دوم $(p_1 - p_2) > 0.45$ بود، موتور فوراً پاسخ را برگردانده و از سایر مراحل صرف‌نظر می‌کند (تاخیر کمتر از ۰.۰۵۵ میلی‌ثانیه).
2. **مسیر تشخیصی عمیق (Deep Diagnostic Path):** تنها در صورت ابهام بالینی، فازهای تکمیلی LDA و پرامپت اجرا می‌شوند.

### ۳. بودجه و محدودیت لبه
- **وزن اضافه:** ۰.۰ مگابایت.
- **بهبود تاخیر:** کاهش تاخیر هد تصمیم‌گیرنده به کمتر از ۰.۰۷۵ میلی‌ثانیه و صعود فریم‌ریت بلادرنگ به ۲۲.۱ FPS.

</div>

