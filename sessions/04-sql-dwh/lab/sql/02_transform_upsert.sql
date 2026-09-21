-- Transform: tổng hợp staging -> mart, idempotent bằng UPSERT (INSERT ... ON CONFLICT).
-- Chạy lại cho cùng một ngày chỉ CẬP NHẬT dòng của ngày đó, không thêm trùng.
-- %(ds)s là tham số ngày (logical date) do Airflow/PostgresHook truyền vào.

INSERT INTO daily_revenue (order_date, total_amount, order_count, updated_at)
SELECT order_date,
       SUM(amount)  AS total_amount,
       COUNT(*)     AS order_count,
       now()        AS updated_at
FROM stg_orders
WHERE order_date = %(ds)s
GROUP BY order_date
ON CONFLICT (order_date) DO UPDATE
    SET total_amount = EXCLUDED.total_amount,
        order_count  = EXCLUDED.order_count,
        updated_at   = EXCLUDED.updated_at;
