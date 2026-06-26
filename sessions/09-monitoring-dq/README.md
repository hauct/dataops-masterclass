# Buổi 9 — Monitoring, Cảnh báo & Data Quality

> 🚧 **Đang biên soạn đầy đủ.** File này hiện là outline. Bài giảng chi tiết + lab + bài tập sẽ được bổ sung.

**Ngày:** 06/08  ·  **Bật stack:** `make up-monitoring`

## Nội dung

- Vì sao cần giám sát cả pipeline lẫn chất lượng dữ liệu
- Metric cơ bản & dashboard với Prometheus + Grafana
- Alerting đúng cách — tránh alert fatigue
- Data quality testing với Great Expectations / GX Core (schema, null, duplicate, business rules)
- Theo dõi data freshness & reconciliation tự động

## Thực hành

- Dựng dashboard giám sát pipeline (Prometheus + Grafana)
- Cấu hình alert theo ngưỡng
- Viết suite test dữ liệu với GX & gắn vào pipeline
- Mô phỏng dữ liệu bẩn & quan sát pipeline chặn lại
- Setup luồng alert đến Slack

## Tài liệu trong buổi

- `README.md` — bài giảng (đang biên soạn)
- `lab/` — code thực hành (đang biên soạn)
- `exercises.md` · `checklist.md` (đang biên soạn)
