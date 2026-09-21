# Checklist tự đánh giá — Buổi 4

## SQL idempotent

- [ ] Tôi giải thích được vì sao `INSERT` thuần không idempotent, còn upsert/`ON CONFLICT` thì có.
- [ ] Tôi viết được partition overwrite (DELETE theo ngày + INSERT) cho lớp staging.
- [ ] Tôi viết được upsert (`ON CONFLICT DO UPDATE`) cho lớp mart.
- [ ] Tôi biết `MERGE` là gì và vì sao nó hữu ích khi chuyển giữa các DWH.

## Transaction & atomicity

- [ ] Tôi hiểu vì sao phải bọc DELETE+INSERT trong một transaction.
- [ ] Tôi mô tả được hậu quả nếu lỗi giữa chừng khi không có transaction.

## Reconciliation

- [ ] Tôi viết được SQL đối soát nguồn ↔ đích (count, sum) cho một ngày.
- [ ] Tôi đã **tự kiểm chứng** pipeline DỪNG khi reconciliation lệch (Phần 5 lab).

## Điều phối bằng Airflow

- [ ] Tôi chạy được `session04_sql_dwh` với dependency đúng thứ tự 4 bước.
- [ ] Tôi dùng được connection `warehouse` và PostgresHook để chạy SQL từ DAG.
- [ ] Tôi chạy được backfill nhiều ngày và xác nhận không nhân đôi.

## Tư duy

- [ ] Tôi biết khi nào DWH/SQL là đủ, khi nào cần chuyển sang Lakehouse/Spark.

> ≥ 90% → sẵn sàng buổi 5 (PySpark Lakehouse). < 70% → ôn lại mục 2 (SQL idempotent) & 3 (reconciliation).
