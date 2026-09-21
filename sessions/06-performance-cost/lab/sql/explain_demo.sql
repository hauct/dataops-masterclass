-- Demo đọc query plan & tối ưu bằng index trên warehouse (Postgres). Chạy trong psql:
--   docker compose exec warehouse psql -U dwh -d analytics -f /opt/project/sessions/06-performance-cost/lab/sql/explain_demo.sql
-- (Thư mục sessions đã mount vào container Airflow, KHÔNG mount vào warehouse; xem lab để biết cách chạy.)

-- 1) Tạo bảng lớn để thấy khác biệt (1 triệu dòng).
DROP TABLE IF EXISTS perf_orders;
CREATE TABLE perf_orders AS
SELECT
    g                                   AS order_id,
    DATE '2026-01-01' + (g % 180)       AS order_date,
    'user' || (g % 10000)               AS customer,
    (random() * 1000)::int              AS amount
FROM generate_series(1, 1000000) AS g;

ANALYZE perf_orders;   -- cập nhật thống kê để planner ước lượng đúng

-- 2) TRƯỚC tối ưu: lọc theo order_date khi CHƯA có index -> kỳ vọng Seq Scan (quét toàn bảng).
EXPLAIN ANALYZE
SELECT order_date, SUM(amount)
FROM perf_orders
WHERE order_date = DATE '2026-03-01'
GROUP BY order_date;

-- 3) Thêm index trên cột hay lọc.
CREATE INDEX idx_perf_orders_date ON perf_orders (order_date);
ANALYZE perf_orders;

-- 4) SAU tối ưu: chạy lại cùng truy vấn -> kỳ vọng Index Scan / Bitmap Index Scan, nhanh hơn.
EXPLAIN ANALYZE
SELECT order_date, SUM(amount)
FROM perf_orders
WHERE order_date = DATE '2026-03-01'
GROUP BY order_date;

-- So sánh dòng "actual time=..." giữa bước 2 và bước 4 để thấy mức cải thiện (before/after).
