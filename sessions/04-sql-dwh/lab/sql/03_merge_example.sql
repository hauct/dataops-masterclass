-- (THAM KHẢO) Cùng logic transform nhưng viết bằng MERGE (chuẩn SQL, Postgres 15+).
-- Cú pháp MERGE giống nhiều DWH khác (BigQuery, Snowflake, SQL Server) -> học để dễ chuyển stack.
-- Không dùng trong DAG (DAG dùng ON CONFLICT), để đây cho bạn so sánh & thực hành.

MERGE INTO daily_revenue t
USING (
    SELECT order_date,
           SUM(amount) AS total_amount,
           COUNT(*)    AS order_count
    FROM stg_orders
    WHERE order_date = %(ds)s
    GROUP BY order_date
) s
ON t.order_date = s.order_date
WHEN MATCHED THEN
    UPDATE SET total_amount = s.total_amount,
               order_count  = s.order_count,
               updated_at   = now()
WHEN NOT MATCHED THEN
    INSERT (order_date, total_amount, order_count, updated_at)
    VALUES (s.order_date, s.total_amount, s.order_count, now());
