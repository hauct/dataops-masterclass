# Lab Buổi 4 — SQL pipeline reliable trên Data Warehouse

Mục tiêu: chạy một pipeline SQL idempotent có reconciliation, do Airflow điều phối, và **tự kiểm chứng**
chạy lại không nhân đôi — y như nguyên lý buổi 1 nhưng bằng SQL.

> Cần: `make up-warehouse` (bật cả Airflow core lẫn Postgres warehouse). Connection `warehouse` đã có sẵn.
> DAG: `session04_sql_dwh` (tag `buoi-04`). SQL ở [`sql/`](./sql/).

---

## Phần 1 — Khởi động & kiểm tra kết nối

```bash
make up-warehouse
make ps        # thấy thêm container `warehouse`
```

Kiểm tra connection trên UI: **Admin → Connections**, có `warehouse` (Postgres). Hoặc test bằng psql:

```bash
docker compose exec warehouse psql -U dwh -d analytics -c "\dt"   # chưa có bảng -> bình thường
```

## Phần 2 — Đọc SQL trước khi chạy

Mở thư mục [`sql/`](./sql/):
- `01_ddl.sql` — tạo bảng (idempotent).
- `02_transform_upsert.sql` — upsert staging → mart (`ON CONFLICT`).
- `03_merge_example.sql` — (tham khảo) cùng logic viết bằng `MERGE`.
- `04_reconcile.sql` — đối soát nguồn ↔ đích.

**Câu hỏi:** trong `02_transform_upsert.sql`, điều gì khiến nó idempotent? Nếu bỏ `ON CONFLICT ... DO UPDATE`
và chỉ `INSERT`, chạy lại 2 lần sẽ ra sao?

## Phần 3 — Chạy DAG & kiểm chứng idempotency

1. Bật & **Trigger** `session04_sql_dwh`. Xem Graph: `create_tables → load_staging → transform_upsert → reconcile` xanh.
2. Xem dữ liệu mart:
   ```bash
   docker compose exec warehouse psql -U dwh -d analytics -c "SELECT * FROM daily_revenue ORDER BY order_date;"
   ```
3. **Trigger lại** đúng ngày đó 1–2 lần nữa. Query lại `daily_revenue`.

**Câu hỏi:** số dòng & `total_amount` của ngày đó có thay đổi sau khi chạy lại không? So sánh với
`pipeline_risky.py` (buổi 1) — vì sao lần này an toàn?

Kiểm tra log task `reconcile`: thấy dòng "✅ RECONCILE khớp...".

## Phần 4 — Backfill nhiều ngày

```bash
docker compose exec airflow-scheduler \
  airflow backfill create --dag-id session04_sql_dwh \
  --from-date 2026-06-20 --to-date 2026-06-24
```

```bash
docker compose exec warehouse psql -U dwh -d analytics \
  -c "SELECT order_date, order_count, total_amount FROM daily_revenue ORDER BY order_date;"
```

**Câu hỏi:** chạy lại lệnh backfill lần nữa — `daily_revenue` có sinh dòng trùng cho các ngày đó không? Vì sao?

## Phần 5 — Làm "vỡ" reconciliation (quan sát cơ chế chặn)

Mục tiêu: thấy pipeline **dừng** khi dữ liệu lệch, thay vì âm thầm đưa số sai xuống báo cáo.

1. Chạy DAG cho một ngày (vd hôm nay) cho tới khi `daily_revenue` đã có dòng.
2. Cố tình làm lệch *đích* (giả lập dữ liệu hỏng):
   ```bash
   docker compose exec warehouse psql -U dwh -d analytics \
     -c "UPDATE daily_revenue SET total_amount = total_amount + 999 WHERE order_date = CURRENT_DATE;"
   ```
3. Trên UI, **Clear** riêng task `reconcile` của run đó để nó chạy lại (không chạy lại transform).

**Câu hỏi:** task `reconcile` lần này thế nào? Đọc log — nó báo gì? Đây là nguyên lý nào của buổi 1?

> (Sau đó trigger lại cả DAG để transform_upsert ghi lại số đúng → reconcile khớp trở lại.)

---

## Phần 6 — Tự làm (mini)

Trong bản copy repo của bạn:
1. Thêm bảng mart thứ hai `revenue_by_customer` (theo `order_date, customer_email`).
2. Viết `transform` upsert cho bảng đó (khóa gồm 2 cột).
3. Thêm task vào DAG, nối phụ thuộc sau `load_staging`, và reconcile riêng.

---

## Nộp gì sau lab

- Ảnh Graph view `session04_sql_dwh` chạy xanh + ảnh kết quả query `daily_revenue`.
- Trả lời các "câu hỏi" ở Phần 2, 3, 4, 5.
- (Phần 6) SQL + DAG đã mở rộng trong repo cá nhân.

> Dọn: `docker compose exec warehouse psql -U dwh -d analytics -c "TRUNCATE stg_orders, daily_revenue;"`
> Tắt stack: `make down`.
