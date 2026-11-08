---
title: Task Registry Index
type: task-index
tags:
  - dashboard
---

<div dir="rtl" style="font-family: inherit;">

# 📌 فهرست تجمیعی تمام تسک‌ها

این جدول به صورت خودکار توسط **Dataview** از کل یادداشت‌های پوشه `Tasks/` خوانده و به‌روزرسانی می‌شود.

```dataview
TABLE WITHOUT ID
  file.link AS "شناسه و نام تسک",
  status AS "وضعیت",
  priority AS "اولویت",
  spec AS "سند مرتبط",
  depends_on AS "پیش‌نیازها",
  blocks AS "مسدودکننده"
FROM "Tasks" AND #task
SORT file.name ASC
```

- بازگشت به [[00 - Dashboard|مرکز فرماندهی]]
- بازگشت به [[Project Board.canvas|تخته کانبان]]

</div>
