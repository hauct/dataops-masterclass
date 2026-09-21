# Bài tập về nhà — Buổi 6

Tự chấm bằng [`checklist.md`](./checklist.md).

## Bài 1 — Tư duy tối ưu (lý thuyết)

Giải thích bằng ví dụ của bạn: vì sao "đúng trước, nhanh sau"? Vì sao mỗi lần tối ưu phải kèm con số
before/after? Cho một ví dụ over-engineering mà bạn từng thấy/làm.

## Bài 2 — Đọc query plan (vận dụng)

Cho kết quả `EXPLAIN ANALYZE` (rút gọn):
```
Seq Scan on perf_orders  (cost=0..18000 rows=5500 width=12) (actual time=0.2..420 rows=5400)
  Filter: (order_date = '2026-03-01')
  Rows Removed by Filter: 994600
```
Vấn đề ở đây là gì? Bạn sẽ làm gì để cải thiện? Sau khi sửa, kế hoạch kỳ vọng đổi thành gì?

## Bài 3 — Bottleneck Spark (chẩn đoán)

Với mỗi triệu chứng trên Spark UI, cho biết bottleneck nào & cách xử lý:

1. Một stage có shuffle read 50GB, chạy rất lâu.
2. Trong một stage 200 task, 199 task xong trong 5s, 1 task chạy 6 phút.
3. Job đọc một thư mục có 40.000 file parquet ~10KB mỗi file.

## Bài 4 — Broadcast vs Sort-merge (phán đoán)

Khi nào nên broadcast join, khi nào KHÔNG nên (gợi ý: kích thước bảng "nhỏ")? Điều gì xảy ra nếu bạn broadcast
một bảng *lớn*?

## Bài 5 — Partitioning (thiết kế)

Bảng giao dịch 3 năm, truy vấn hầu hết lọc theo ngày. Bạn partition theo cột nào? Vì sao **không** nên
partition theo `customer_id`? Vì sao partition theo `giờ` có thể gây small-files?

## Bài 6 — FinOps (vận dụng)

Một job Spark chạy mỗi giờ trên cụm cloud 10 node, nhưng dữ liệu mỗi giờ rất nhỏ. Đề xuất 3 cách giảm chi phí
và cách đo hiệu quả từng cách.
