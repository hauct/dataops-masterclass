# Bài tập về nhà — Buổi 4

Tự chấm bằng [`checklist.md`](./checklist.md).

## Bài 1 — Idempotent hay không? (đọc SQL)

Với mỗi đoạn, cho biết chạy 2 lần cho ngày `:ds` có nhân đôi dữ liệu không, và sửa nếu cần:

```sql
-- A
INSERT INTO daily_revenue (order_date, total_amount)
SELECT order_date, SUM(amount) FROM stg_orders WHERE order_date = :ds GROUP BY order_date;

-- B
DELETE FROM daily_revenue WHERE order_date = :ds;
INSERT INTO daily_revenue (order_date, total_amount)
SELECT order_date, SUM(amount) FROM stg_orders WHERE order_date = :ds GROUP BY order_date;

-- C
INSERT INTO daily_revenue (order_date, total_amount)
SELECT order_date, SUM(amount) FROM stg_orders WHERE order_date = :ds GROUP BY order_date
ON CONFLICT (order_date) DO UPDATE SET total_amount = EXCLUDED.total_amount;
```

## Bài 2 — ON CONFLICT vs MERGE (so sánh)

Viết lại đoạn C ở Bài 1 bằng `MERGE`. Nêu 1 trường hợp `MERGE` làm được mà `ON CONFLICT` khó/không làm được.

## Bài 3 — Transaction & atomicity (vận dụng)

Trong `load_staging`, vì sao phải bọc `DELETE` + `INSERT` trong **một** transaction? Mô tả điều gì xảy ra với
bảng nếu tiến trình bị kill *sau* `DELETE` nhưng *trước* `INSERT` trong hai trường hợp: (a) có transaction,
(b) không có transaction.

## Bài 4 — Thiết kế reconciliation (vận dụng)

Ngoài `COUNT(*)` và `SUM(amount)`, đề xuất thêm **2 phép đối soát** hữu ích cho dữ liệu giao dịch tài chính
(vd liên quan tới giá trị âm, trùng `order_id`, hoặc khoảng giá trị). Viết câu SQL kiểm tra cho mỗi phép.

## Bài 5 — DWH hay Lakehouse? (phán đoán)

Với mỗi bài toán, chọn DWH/SQL hay Lakehouse/Spark + lý do ngắn:

1. Tổng hợp doanh thu ngày từ ~50 triệu dòng giao dịch có cấu trúc.
2. Phân tích log JSON lồng nhau, ~5TB/ngày, cần parse phức tạp.
3. Báo cáo BI cập nhật mỗi sáng, dữ liệu vài trăm nghìn dòng.

## Bài 6 — Mở rộng pipeline (code)

Hoàn thành Phần 6 lab: thêm mart `revenue_by_customer` (khóa `order_date, customer_email`), transform upsert,
và reconcile riêng. Nộp SQL + DAG đã mở rộng, kèm bằng chứng chạy lại không nhân đôi.
