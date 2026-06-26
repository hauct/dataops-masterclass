# Buổi 5 — PySpark in Modern Lakehouse

> 🚧 **Đang biên soạn đầy đủ.** File này hiện là outline. Bài giảng chi tiết + lab + bài tập sẽ được bổ sung.

**Ngày:** 23/07  ·  **Bật stack:** `make up-lakehouse`

## Nội dung

- Khi nào cần Lakehouse (dữ liệu lớn, object storage + table format)
- Triển khai stack Lakehouse trong DataOps
- PySpark pipeline reliable: atomic & idempotent writes, partition overwrite an toàn
- Table format (Delta/Iceberg): ACID & time travel
- Case study: migrate DWH → Data Lake minimal-downtime

## Thực hành

- Viết PySpark job idempotent & retry-safe
- Ghi dữ liệu qua Delta & thử time travel
- Chạy job qua Airflow
- Mô phỏng job fail giữa chừng & chạy lại không hỏng dữ liệu

## Tài liệu trong buổi

- `README.md` — bài giảng (đang biên soạn)
- `lab/` — code thực hành (đang biên soạn)
- `exercises.md` · `checklist.md` (đang biên soạn)
