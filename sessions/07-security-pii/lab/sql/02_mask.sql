-- Tạo dữ liệu ĐÃ MASKING từ bảng thô cho ngày %(ds)s. Idempotent bằng upsert.
-- Ba kỹ thuật trong một câu:
--   email_masked : MASKING hiển thị (che một phần)        -> a***@example.com
--   email_pseudo : PSEUDONYMIZATION (hash ổn định)         -> md5(email), join được, không lộ danh tính
--   phone_masked : MASKING (chỉ giữ 3 số cuối)
-- (Production: dùng pgcrypto digest(email,'sha256') + salt thay cho md5.)

INSERT INTO customers_masked
    (load_date, customer_id, name_masked, email_masked, email_pseudo, phone_masked, amount)
SELECT
    load_date,
    customer_id,
    left(full_name, 1) || '***'                              AS name_masked,
    regexp_replace(email, '(^.).*(@.*$)', '\1***\2')         AS email_masked,
    md5(email)                                               AS email_pseudo,
    '***' || right(phone, 3)                                 AS phone_masked,
    amount
FROM customers_raw
WHERE load_date = %(ds)s
ON CONFLICT (load_date, customer_id) DO UPDATE SET
    name_masked  = EXCLUDED.name_masked,
    email_masked = EXCLUDED.email_masked,
    email_pseudo = EXCLUDED.email_pseudo,
    phone_masked = EXCLUDED.phone_masked,
    amount       = EXCLUDED.amount;
