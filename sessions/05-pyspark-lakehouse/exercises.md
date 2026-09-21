# Bài tập về nhà — Buổi 5

Tự chấm bằng [`checklist.md`](./checklist.md).

## Bài 1 — DWH hay Lakehouse? (phán đoán, nối tiếp buổi 4)

Chọn stack + lý do cho mỗi tình huống:

1. ~80GB log sự kiện JSON lồng nhau mỗi ngày, cần parse & tổng hợp.
2. Bảng mart doanh thu vài trăm nghìn dòng phục vụ BI mỗi sáng.
3. Cần nhiều engine (Spark, Trino, Flink) cùng đọc một bảng lớn trên object storage.

## Bài 2 — Idempotency 3 stack (tổng hợp)

Điền cách đạt idempotency tương ứng mỗi stack:

| Stack | Cách ghi idempotent |
|-------|---------------------|
| File thô (buổi 3) | |
| SQL/DWH (buổi 4) | |
| Lakehouse/Delta (buổi 5) | |

## Bài 3 — `replaceWhere` (đọc & dự đoán)

Cho đoạn:
```python
df.write.format("delta").mode("overwrite").save(path)            # A
df.write.format("delta").mode("overwrite") \
  .option("replaceWhere", "order_date = '2026-06-20'").save(path) # B
df.write.format("delta").mode("append").save(path)               # C
```
Với một bảng đã có dữ liệu nhiều ngày, mỗi lệnh ảnh hưởng tới dữ liệu ra sao? Lệnh nào an toàn cho việc
"nạp lại 1 ngày"? Lệnh nào nguy hiểm?

## Bài 4 — Time travel (vận dụng)

Bạn phát hiện job tối qua ghi sai dữ liệu ngày 22/06 (version mới nhất). Mô tả các bước dùng time travel để:
(a) xác nhận dữ liệu version trước đúng, (b) khôi phục về version đó. (Tìm hiểu thêm `RESTORE` của Delta.)

## Bài 5 — Orchestration (thiết kế)

Bạn cần Airflow chạy `orders_delta_job` mỗi ngày trên K8s. Vì sao **không** nên chạy Spark trong worker
Airflow? Bạn sẽ dùng operator nào để submit, và làm sao đảm bảo backfill an toàn?

## Bài 6 — Code (cốt lõi)

Hoàn thành Phần 6 lab: job `daily_revenue_delta.py` đọc `orders` (Delta) → ghi `daily_revenue` (Delta) tổng
hợp theo ngày, idempotent + reconciliation. Nộp code + bằng chứng chạy lại không nhân đôi.
