# Bài tập về nhà — Buổi 3

Tự chấm bằng [`checklist.md`](./checklist.md).

## Bài 1 — `now()` vs logical date (đọc & sửa)

Đoạn task sau sai ở đâu về tính reproducibility? Sửa lại:

```python
@task
def daily_sales():
    today = datetime.now().strftime("%Y-%m-%d")   # ❌
    rows = read_orders(date=today)
    write(f"/data/sales/dt={today}/data.json", rows)
```

Giải thích: nếu backfill ngày 01/07 vào hôm nay, đoạn trên lấy dữ liệu ngày nào? Đúng hay sai?

## Bài 2 — catchup (tình huống)

Bạn tạo DAG `@daily` với `start_date=datetime(2025,1,1)` và `catchup=True`, bật hôm nay. Điều gì xảy ra ngay
lập tức? Vì sao nguy hiểm? Hai cách xử lý an toàn?

## Bài 3 — XCom (phán đoán)

Với mỗi thứ sau, cho biết có nên truyền qua XCom không (Có/Không + lý do):

1. Đường dẫn `s3://lake/orders/dt=2026-07-09/`.
2. Một `pandas.DataFrame` 2 triệu dòng.
3. Số bản ghi đã xử lý (một số nguyên).
4. Nội dung file CSV 500MB.

## Bài 4 — Thiết kế retry/timeout/alert (vận dụng)

Cho 3 task, đề xuất cấu hình `retries`, `retry_delay`, `execution_timeout` và có cần alert không:

1. Gọi REST API bên thứ ba (đôi khi timeout mạng).
2. Chạy một truy vấn tổng hợp nặng trên warehouse (bình thường ~10 phút).
3. Một bước transform thuần Python, lỗi thường do bug code.

## Bài 5 — Idempotency (code, cốt lõi)

Mở rộng `session03_idempotent_partition` (bản copy trong repo của bạn):
1. Thêm task `quality_check`: chặn nếu có `amount <= 0` (tiền đề buổi 9).
2. Thêm cấu hình `retries=2` cho `extract`.
3. Chứng minh idempotent: viết lại các bước bạn đã làm để xác nhận chạy lại 1 ngày không đổi dữ liệu.

## Bài 6 — Assets (tìm hiểu)

Đọc mục 7 (Assets) trong bài giảng + docs. Mô tả một tình huống thực tế mà data-aware scheduling (Asset)
tốt hơn lịch cứng `@daily`. (3–5 câu.)
