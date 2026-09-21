# Bài tập về nhà — Buổi 7

Tự chấm bằng [`checklist.md`](./checklist.md).

## Bài 1 — Secrets (đọc & sửa)

Tìm và sửa các vấn đề bảo mật trong đoạn sau:

```python
DB_PASS = "Prod#2026!"
API_KEY = "sk-live-abc123"
def run():
    conn = connect(host="db.prod", user="root", password=DB_PASS)
    logging.info(f"connecting with {DB_PASS}")
```

(Có ít nhất 3 vấn đề: hardcode secret, log secret, dùng user quyền cao.)

## Bài 2 — Chọn kỹ thuật PII (phán đoán)

Với mỗi cột, chọn masking / pseudonymization / encryption + lý do:

1. `email` — dùng để gửi mail marketing sau này.
2. `national_id` (CCCD) — chỉ để đếm số khách duy nhất theo vùng.
3. `phone` — hiển thị trên màn hình hỗ trợ để nhân viên đối chiếu nhanh.

## Bài 3 — RBAC (thiết kế)

Thiết kế phân quyền cho 3 nhóm trên warehouse: **data engineer** (đọc/ghi mọi bảng), **analyst** (chỉ đọc
mart đã masking), **auditor** (chỉ đọc `audit_log`). Viết các câu GRANT/REVOKE tương ứng.

## Bài 4 — Pseudonymization (hiểu sâu)

Vì sao `email_pseudo = md5(email)` vẫn **join được giữa các bảng** nhưng không lộ danh tính? Hạn chế của
hashing không salt là gì (gợi ý: tấn công từ điển / rainbow table)? Cách khắc phục?

## Bài 5 — Governance (vận dụng)

Liệt kê 4 cơ chế kỹ thuật giúp đáp ứng yêu cầu "quyền được lãng quên" (xóa dữ liệu một khách khi họ yêu cầu)
trong một pipeline có nhiều lớp (raw → mart → backup). Khó khăn ở đâu?

## Bài 6 — Code (cốt lõi)

Hoàn thành Phần 6 lab: thêm bước che PII + audit vào pipeline buổi 4/5 của bạn, tách bản thô + REVOKE cho vai
trò hạn chế. Nộp code + bằng chứng vai trò hạn chế không đọc được PII thô.
