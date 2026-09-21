# Lab Buổi 7 — Bảo mật & bảo vệ PII

Mục tiêu: quét secret hardcode, che PII trong pipeline, áp RBAC least-privilege, và rà soát/vá lỗ hổng.

> Phần PII/RBAC cần `make up-warehouse`. Phần `mask_demo.py` & `scan_secrets.py` chạy bằng Python thuần (không cần infra).

---

## Phần 1 — Hiểu 3 kỹ thuật bảo vệ PII (không cần infra)

```bash
python sessions/07-security-pii/lab/mask_demo.py
```

Quan sát output: cùng một email được **masking** (che), **pseudonymize** (hash), **encrypt** (mã hóa rồi
giải mã lại).

**Câu hỏi:** với mỗi nhu cầu sau, chọn kỹ thuật nào?
(a) Dashboard hỗ trợ khách cần thấy "dạng" email; (b) Phân tích số đơn theo từng người mà không cần biết
danh tính; (c) Lưu số thẻ để sau này hoàn tiền.

## Phần 2 — Quét secret hardcode

```bash
python sessions/07-security-pii/lab/scan_secrets.py
```

Kỳ vọng: `✅ Không phát hiện secret hardcode` (repo này không hardcode secret — dùng `.env` + Connection).

Giờ **tự tạo lỗ hổng** để thấy nó bắt được: thêm tạm vào một file `.py` dòng
`api_key = "sk-1234567890abcdef"` rồi chạy lại scanner → nó phải báo đỏ và exit code ≠ 0 (đây chính là cách
CI chặn ở buổi 8). Nhớ xóa dòng đó sau khi thử.

## Phần 3 — Che PII trong pipeline

```bash
make up-warehouse
```

Bật & **Trigger** DAG `session07_pii_masking` (tag `buoi-07`). Luồng: `create_tables → load_raw → mask → audit`.

So sánh bản thô vs bản đã che:

```bash
docker compose exec warehouse psql -U dwh -d analytics -c \
  "SELECT customer_id, full_name, email, phone FROM customers_raw LIMIT 5;"
docker compose exec warehouse psql -U dwh -d analytics -c \
  "SELECT customer_id, name_masked, email_masked, email_pseudo, phone_masked FROM customers_masked LIMIT 5;"
```

**Câu hỏi:** `email_masked` và `email_pseudo` khác nhau thế nào? Cái nào dùng để *hiển thị*, cái nào để *join/đếm*?

## Phần 4 — RBAC least-privilege

Áp quy tắc "chỉ thấy bản đã che":

```bash
docker compose exec -T warehouse psql -U dwh -d analytics \
  < sessions/07-security-pii/lab/sql/03_rbac.sql
```

Giả lập là `analyst_ro` rồi thử đọc:

```bash
docker compose exec warehouse psql -U dwh -d analytics -c \
  "SET ROLE analyst_ro; SELECT * FROM v_customers_safe LIMIT 3;"      # OK
docker compose exec warehouse psql -U dwh -d analytics -c \
  "SET ROLE analyst_ro; SELECT * FROM customers_raw LIMIT 3;"          # ❌ permission denied
```

**Câu hỏi:** vì sao `analyst_ro` đọc được `v_customers_safe` nhưng không đọc được `customers_raw`? Đây là nguyên tắc gì?

## Phần 5 — Audit & rà soát lỗ hổng

1. Xem audit log: `... -c "SELECT * FROM audit_log ORDER BY ts DESC LIMIT 5;"`. *Câu hỏi:* audit có ghi giá
   trị PII không? Vì sao không nên?
2. Rà soát một DAG bất kỳ trong `dags/`: nó có hardcode secret không? Có in PII ra log không? Ghi lại phát
   hiện + cách vá (dùng Connection, che PII trước khi log).

---

## Phần 6 — Tự làm (mini)

Trong repo của bạn: thêm vào pipeline buổi 4 (hoặc 5) một bước **che PII** trước khi dữ liệu xuống mart, và
một dòng **audit**. Đảm bảo bản thô PII tách riêng + có REVOKE cho vai trò hạn chế.

---

## Nộp gì sau lab

- Output `mask_demo.py` + trả lời Phần 1.
- Bằng chứng `scan_secrets.py` bắt được secret bạn cố tình thêm (Phần 2).
- Ảnh so sánh `customers_raw` vs `customers_masked` (Phần 3).
- Bằng chứng `analyst_ro` bị từ chối đọc bản thô (Phần 4).
- Ghi chú rà soát lỗ hổng (Phần 5) + bước che PII tự thêm (Phần 6).

> Dọn: `... -c "DROP TABLE IF EXISTS customers_raw, customers_masked, audit_log CASCADE; DROP ROLE IF EXISTS analyst_ro;"`
