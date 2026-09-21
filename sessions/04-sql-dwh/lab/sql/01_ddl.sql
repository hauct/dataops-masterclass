-- DDL: tạo bảng staging & mart. Idempotent (CREATE IF NOT EXISTS) -> chạy lại không lỗi.

-- Lớp staging: dữ liệu giao dịch thô theo ngày.
CREATE TABLE IF NOT EXISTS stg_orders (
    order_id       TEXT,
    order_date     DATE,
    customer_email TEXT,
    amount         BIGINT
);
CREATE INDEX IF NOT EXISTS idx_stg_orders_date ON stg_orders (order_date);

-- Lớp mart: số liệu tổng hợp, 1 dòng / ngày.
-- order_date là PRIMARY KEY -> cần cho upsert ON CONFLICT (mục 2.2 bài giảng).
CREATE TABLE IF NOT EXISTS daily_revenue (
    order_date   DATE PRIMARY KEY,
    total_amount BIGINT,
    order_count  INTEGER,
    updated_at   TIMESTAMPTZ DEFAULT now()
);
