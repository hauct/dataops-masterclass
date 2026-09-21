-- DDL cho demo bảo mật. Idempotent.

-- Bảng THÔ chứa PII (chỉ vùng hạn chế mới được đụng tới).
CREATE TABLE IF NOT EXISTS customers_raw (
    load_date   DATE,
    customer_id TEXT,
    full_name   TEXT,
    email       TEXT,
    phone       TEXT,
    amount      BIGINT
);
CREATE INDEX IF NOT EXISTS idx_customers_raw_date ON customers_raw (load_date);

-- Bảng ĐÃ MASKING (hạ nguồn chỉ dùng bảng này).
CREATE TABLE IF NOT EXISTS customers_masked (
    load_date    DATE,
    customer_id  TEXT,
    name_masked  TEXT,
    email_masked TEXT,
    email_pseudo TEXT,     -- hash ổn định để join/đếm theo người mà không lộ danh tính
    phone_masked TEXT,
    amount       BIGINT,
    PRIMARY KEY (load_date, customer_id)
);

-- Bảng audit tối giản.
CREATE TABLE IF NOT EXISTS audit_log (
    ts     TIMESTAMPTZ DEFAULT now(),
    actor  TEXT,
    action TEXT,
    object TEXT,
    detail TEXT
);
