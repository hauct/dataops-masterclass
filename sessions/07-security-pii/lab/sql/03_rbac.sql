-- RBAC least-privilege: vai trò analyst chỉ thấy bản ĐÃ MASKING, KHÔNG đụng bản thô PII.
-- Chạy thủ công trong psql (xem lab). An toàn để chạy lại nhiều lần.

-- View che PII (hạ nguồn dùng view này thay vì bảng masked trực tiếp cũng được).
CREATE OR REPLACE VIEW v_customers_safe AS
SELECT load_date, customer_id, name_masked, email_masked, email_pseudo, phone_masked, amount
FROM customers_masked;

-- Vai trò chỉ đọc, không đăng nhập trực tiếp (gán cho user thật khi cần).
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'analyst_ro') THEN
        CREATE ROLE analyst_ro NOLOGIN;
    END IF;
END $$;

-- Cấp TỐI THIỂU: chỉ SELECT trên view an toàn.
GRANT USAGE ON SCHEMA public TO analyst_ro;
GRANT SELECT ON v_customers_safe TO analyst_ro;

-- TỪ CHỐI rõ ràng quyền trên bảng thô chứa PII.
REVOKE ALL ON customers_raw FROM analyst_ro;

-- Kiểm chứng: giả lập là analyst rồi thử đọc bản thô (kỳ vọng LỖI permission denied).
--   SET ROLE analyst_ro;
--   SELECT * FROM v_customers_safe LIMIT 5;     -- OK
--   SELECT * FROM customers_raw   LIMIT 5;      -- ❌ permission denied
--   RESET ROLE;
