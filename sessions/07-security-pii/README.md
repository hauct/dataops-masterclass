# Buổi 7 — Bảo mật & Dữ liệu nhạy cảm

**Ngày 30/07 · 20h–22h · Bật stack: `make up-warehouse`**

> Pipeline reliable mà *rò rỉ dữ liệu khách hàng* thì còn tệ hơn pipeline chậm. Buổi này học cách **bảo vệ
> dữ liệu nhạy cảm** xuyên suốt pipeline: không hardcode secrets, che/giấu PII, phân quyền tối thiểu, và ghi
> vết truy cập. Với dữ liệu tài chính/ngân hàng, đây là yêu cầu **bắt buộc** (pháp lý), không phải tùy chọn.

## Mục tiêu buổi học

- **Secrets management**: tuyệt đối không hardcode; quản lý qua env / secret manager.
- Xử lý **PII**: masking, encryption, anonymization — chọn đúng kỹ thuật cho đúng mục đích.
- **Phân quyền least-privilege** (RBAC): mỗi vai trò chỉ thấy đúng thứ cần thấy.
- Hiểu yêu cầu **governance** cho dữ liệu regulated (tài chính, ngân hàng).
- **Audit logging** cơ bản: ai truy cập/đổi gì, khi nào.

---

## 1. Secrets management — không bao giờ hardcode

**Secret** = mật khẩu DB, API key, token, khóa mã hóa... Nguyên tắc số 1: **secret không bao giờ nằm trong
code hay trong Git.** Một secret bị commit là coi như đã lộ (lịch sử Git giữ mãi).

```python
# ❌ TUYỆT ĐỐI KHÔNG
conn = connect(host="db", user="admin", password="P@ssw0rd123")

# ✅ Lấy từ biến môi trường / secret manager / Airflow Connection
import os
password = os.environ["DB_PASSWORD"]
# hoặc trong Airflow: dùng Connection 'warehouse' (đã làm ở buổi 4) — credential không nằm trong DAG
```

Thứ tự ưu tiên (từ tối thiểu → tốt nhất):
1. **Biến môi trường + `.env`** (đã `.gitignore`) — mức tối thiểu khóa này dùng.
2. **Airflow Connections/Variables** (mã hóa bằng Fernet key) — cho pipeline.
3. **Secret manager chuyên dụng** (HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager) — chuẩn production: xoay vòng (rotation), phân quyền, audit truy cập secret.

> Trong repo này: `.env` chứa secret và **đã được `.gitignore`**; chỉ commit `.env.example` (không có giá
> trị thật). Fernet key (`make fernet`) mã hóa secret lưu trong Airflow. Đây là lý do buổi trước có warning
> "empty cryptography key".

---

## 2. PII là gì & ba kỹ thuật bảo vệ

**PII** (Personally Identifiable Information) = dữ liệu nhận dạng cá nhân: tên, email, SĐT, CMND/CCCD, địa chỉ,
số tài khoản... Ba kỹ thuật, **chọn theo mục đích**:

| Kỹ thuật | Làm gì | Khôi phục được? | Dùng khi |
|----------|--------|-----------------|----------|
| **Masking** (che) | Hiển thị một phần: `a***@mail.com`, SĐT `***123` | Không | Cho phép *nhìn dạng* nhưng không lộ đầy đủ (hỗ trợ, dashboard) |
| **Encryption** (mã hóa) | Biến thành ciphertext bằng khóa | **Có** (nếu có khóa) | Cần lưu trữ an toàn nhưng vẫn dùng lại bản gốc sau này |
| **Anonymization / Pseudonymization** | Thay bằng token/hash ổn định (vd `md5(email)`) | Không (hash) | Phân tích/join theo cá nhân mà **không cần biết danh tính** |

```sql
-- Masking để hiển thị (che một phần)
regexp_replace(email, '(^.).*(@.*$)', '\1***\2')      -- an***@example.com

-- Pseudonymization để phân tích (hash ổn định -> vẫn join được, không lộ danh tính)
md5(email)                                            -- (production: SHA-256 + salt qua pgcrypto)
```

> **Quy tắc chọn:** cần *join/đếm theo người* nhưng không cần danh tính → **hash/pseudonymize**. Cần *hiển
> thị* an toàn → **mask**. Cần *lấy lại bản gốc* → **encrypt**. Đừng mã hóa khi chỉ cần che, và đừng che khi
> cần khôi phục.

### Áp dụng trong pipeline

Tốt nhất là **che/giấu PII càng sớm càng tốt** (ngay sau ingest), để các lớp hạ nguồn (mart, dashboard) chỉ
nhìn thấy dữ liệu đã an toàn. Giữ bản gốc (nếu buộc phải) ở một vùng *hạn chế truy cập tối đa*.

---

## 3. Phân quyền least-privilege (RBAC)

> **Nguyên tắc least-privilege:** mỗi người/dịch vụ chỉ được cấp **đúng quyền tối thiểu** để làm việc của
> mình — không hơn.

Ví dụ trên Postgres: tạo vai trò `analyst_ro` chỉ được `SELECT` trên **view đã masking**, **không** đụng được
bảng thô chứa PII.

```sql
CREATE ROLE analyst_ro NOLOGIN;
GRANT SELECT ON v_customers_masked TO analyst_ro;     -- chỉ thấy bản đã che
REVOKE ALL ON customers_raw FROM analyst_ro;          -- không thấy bản gốc
```

Áp dụng tương tự cho: object storage (IAM policy theo bucket/prefix), Airflow (RBAC role), warehouse cloud
(row/column-level security). Ý tưởng chung: **tách vai trò, cấp tối thiểu, từ chối mặc định**.

---

## 4. Governance cho dữ liệu regulated

Dữ liệu tài chính/ngân hàng/ y tế chịu **quy định pháp lý** (vd GDPR, PCI-DSS, hay quy định nội địa). Vài yêu
cầu thường gặp mà DataOps phải đáp ứng:

- **Phân loại dữ liệu** (data classification): đánh dấu cột nào là PII/nhạy cảm.
- **Data retention**: giữ bao lâu, khi nào phải xóa (quyền được lãng quên).
- **Lineage**: chứng minh dữ liệu đi từ đâu tới đâu (buổi 10).
- **Audit**: ghi vết ai truy cập/đổi dữ liệu nhạy cảm.
- **Data contracts**: thỏa thuận schema & mức nhạy cảm giữa bên tạo và bên dùng (xu hướng 2026).

> Bạn không cần thuộc lòng luật, nhưng cần biết **những cơ chế kỹ thuật** (classification, masking, RBAC,
> retention, audit, lineage) để khi tổ chức yêu cầu tuân thủ, bạn hiện thực được.

---

## 5. Audit logging

"Ai đã làm gì, khi nào, trên dữ liệu nào." Audit log giúp điều tra sự cố & chứng minh tuân thủ. Mức cơ bản:

- DB: bật log truy vấn / dùng bảng audit ghi lại thao tác nhạy cảm.
- Pipeline: log mỗi lần đọc/ghi vùng dữ liệu nhạy cảm (ai/role nào, job nào, thời điểm).

```sql
-- Bảng audit tối giản
CREATE TABLE IF NOT EXISTS audit_log (
  ts TIMESTAMPTZ DEFAULT now(), actor TEXT, action TEXT, object TEXT, detail TEXT
);
```

Lưu ý: **audit log cũng có thể chứa dữ liệu nhạy cảm** — đừng ghi nguyên PII vào log (ghi định danh đã hash/ID thay vì giá trị thật).

---

## 6. Sang phần thực hành

Ở [`lab/README.md`](./lab/): bạn (1) chạy `scan_secrets.py` quét repo tìm secret hardcode; (2) chạy DAG
`session07_pii_masking` tạo bảng đã masking từ dữ liệu thô; (3) áp RBAC để vai trò hạn chế chỉ thấy bản
masked; (4) rà soát một DAG "có lỗ hổng" và vá. Code: [`lab/`](./lab/).

Sau buổi: [`exercises.md`](./exercises.md) + [`checklist.md`](./checklist.md).

---

## Tài liệu tham khảo

- Airflow — quản lý Connections & Variables (secrets) — https://airflow.apache.org/docs/apache-airflow/stable/security/secrets/index.html
- Postgres GRANT/REVOKE (RBAC) — https://www.postgresql.org/docs/current/sql-grant.html
- Postgres pgcrypto (hash/encrypt) — https://www.postgresql.org/docs/current/pgcrypto.html
- OWASP — Secrets Management Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
- GDPR (tổng quan) — https://gdpr.eu/what-is-gdpr/
