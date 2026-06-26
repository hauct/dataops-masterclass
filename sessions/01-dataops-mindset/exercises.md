# Bài tập về nhà — Buổi 1

Làm sau buổi học. Mục tiêu: củng cố tư duy + nguyên lý nền tảng. Tự chấm bằng [`checklist.md`](./checklist.md).

## Bài 1 — Phân biệt vai trò (lý thuyết)

Với mỗi tình huống, cho biết đó là việc của **DA**, **DE**, hay **DataOps** (có thể nhiều hơn một, giải thích):

1. Dashboard doanh thu sáng nay hiển thị sai, sếp hỏi "số này tin được không?".
2. Cần thêm một bảng `dim_product` để join vào fact bán hàng.
3. Pipeline ETL fail lúc 2h sáng, cần điều tra & khôi phục trước 6h sáng.
4. Phân tích vì sao doanh thu vùng miền Tây giảm 12% tháng này.
5. Thiết lập cảnh báo khi dữ liệu nguồn trễ quá 30 phút.

## Bài 2 — Nhận diện idempotency (đọc code)

Cho 3 đoạn ghi dữ liệu dưới đây, đoạn nào **idempotent**, đoạn nào **không**? Giải thích & sửa đoạn sai:

```sql
-- A
INSERT INTO sales SELECT * FROM staging_sales WHERE dt = '2026-07-09';

-- B
MERGE INTO sales t USING staging_sales s ON t.id = s.id
WHEN MATCHED THEN UPDATE SET amount = s.amount
WHEN NOT MATCHED THEN INSERT (id, amount) VALUES (s.id, s.amount);

-- C
TRUNCATE TABLE sales_today;
INSERT INTO sales_today SELECT * FROM staging_sales WHERE dt = CURRENT_DATE;
```

(Gợi ý cho C: nó idempotent về mặt "chạy lại không nhân đôi", nhưng vi phạm nguyên lý nào khác? Nghĩ về
`CURRENT_DATE` và reproducibility/backfill.)

## Bài 3 — Thiết kế reconciliation (vận dụng)

Bạn nạp dữ liệu giao dịch từ hệ thống nguồn vào warehouse mỗi ngày. Hãy đề xuất **3 phép đối soát** (kèm
ngưỡng chấp nhận) để khẳng định dữ liệu "đúng & đủ". Ví dụ mẫu: "COUNT(*) đích = COUNT(*) nguồn, lệch 0".

## Bài 4 — Cải tiến pipeline (code, cốt lõi)

Mở rộng `lab/pipeline_fixed.py`:

1. Thêm tham số dòng lệnh cho phép **backfill nhiều ngày**: `python pipeline_fixed.py 2026-07-09 2026-07-10`.
2. Đảm bảo backfill vẫn **idempotent** (chạy lại khoảng ngày đó không nhân đôi).
3. Thêm một phép **data quality check** đơn giản trước khi ghi: chặn nếu có `amount <= 0` hoặc `customer_email`
   rỗng (đây là "tiền đề" của buổi 9 — Great Expectations).
4. In ra log rõ ràng cho từng ngày: nạp bao nhiêu đơn, reconciliation khớp/không.

> Nộp: code đã sửa trong repo cá nhân của bạn (nhánh `hoc-vien/<ten>`), kèm 1 đoạn mô tả ngắn bạn đã áp
> dụng nguyên lý nào ở đâu.

## Bài 5 — Suy ngẫm (mở)

Trong công việc/đồ án trước đây của bạn, hãy nhớ lại **một** pipeline hoặc script xử lý dữ liệu bạn từng
viết. Nó vi phạm nguyên lý nào trong buổi 1? Nếu viết lại hôm nay, bạn sẽ đổi gì? (3–5 câu.)
