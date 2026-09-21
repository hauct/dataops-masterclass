-- Reconciliation: đối soát nguồn (staging) vs đích (mart) cho ngày %(ds)s.
-- Trả về 1 dòng gồm các con số 2 bên + cờ khớp/không. DAG sẽ đọc và raise nếu lệch.

WITH src AS (
    SELECT COUNT(*) AS cnt, COALESCE(SUM(amount), 0) AS total
    FROM stg_orders WHERE order_date = %(ds)s
),
dst AS (
    SELECT COALESCE(order_count, 0) AS cnt, COALESCE(total_amount, 0) AS total
    FROM daily_revenue WHERE order_date = %(ds)s
)
SELECT
    src.cnt   AS src_cnt,
    dst.cnt   AS dst_cnt,
    src.total AS src_total,
    dst.total AS dst_total,
    (src.cnt = dst.cnt AND src.total = dst.total) AS is_match
FROM src CROSS JOIN dst;
