---
title: System Architecture Overview
type: architecture
tags:
  - arch
  - architecture/overview
---

<div dir="rtl" style="font-family: inherit;">

# 🏛️ معماری کلان سیستم (System Architecture Overview)

این سند معماری پایه و جریان داده‌های چندمدلی را برای سیستم تشخیص خودکار گونه و آسیب‌شناسی گیاهی تشریح می‌کند.

---

## 🧩 اجزای اصلی معماری (Key Architectural Components)

```mermaid
flowchart TD
    In["📷 ورودی تصویر مزرعه (Query Image)"] --> Fast["⚡ مسیر سریع: DINOv2 Small (384-d)"]
    Fast --> Gate{"🎲 گیت آنتروپی شانون (tau)"}
    Gate -- "اطمینان بالا" --> OutFast["✅ خروج سریع (21ms / 45 FPS)"]
    Gate -- "ابهام" --> Deep["🔬 مسیر عمیق: BioCLIP ViT-B (512-d)"]
    
    Deep --> Joint["🧬 منیفولد مشترک ۸۹۶ بعدی (Joint Manifold)"]
    Joint --> Router["🌿 روتر خودکار گونه‌شناسی (Species Router)"]
    Router --> MoE["🎯 مدل ترکیبی خبرگان (Hierarchical MoE)"]
    MoE --> Top2["📊 تشخیص افتراقی دوگانه (Top-2 Differential)"]
    
    style In fill:#f9f,stroke:#333
    style Fast fill:#bbf,stroke:#333
    style Deep fill:#dfd,stroke:#333
    style Router fill:#ffd,stroke:#333
    style MoE fill:#dff,stroke:#333
    style Top2 fill:#fdd,stroke:#333
```

---

## 📚 سوابق تصمیمات فنی و معماری (ADRs)
تصمیمات معماری کلیدی مصوب و ردشده در فاز ۲ را در دایرکتوری [[Architecture/ADR/Index|سوابق تصمیم معماری (ADR)]] دنبال کنید.

- 📌 بازگشت به [[Project Board.canvas|تخته بصری ۶ مرحله‌ای ریسرچ]]
- 📊 بازگشت به [[00 - Dashboard|مرکز فرماندهی]]

</div>
