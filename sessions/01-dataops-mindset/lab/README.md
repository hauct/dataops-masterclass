# Lab Buổi 1 — Dựng môi trường & "bắt bệnh" pipeline

Lab gồm 3 phần. Phần 1 & 2 chuẩn bị nền cho cả khóa; phần 3 là phần "đắt" nhất — bạn sẽ **tận mắt thấy**
một pipeline không idempotent làm hỏng dữ liệu, rồi sửa nó.

> Phần 3 chỉ cần **Python 3.11+** (dùng sqlite có sẵn) — chạy được ngay cả khi Docker chưa xong.

---

## Phần 1 — Dựng môi trường khóa học (Docker)

1. Cài Docker Desktop & Git theo [`docs/setup.md`](../../../docs/setup.md).
2. Tại thư mục gốc repo:
   ```bash
   cp .env.example .env
   make fernet            # copy dòng kết quả vào .env (AIRFLOW_FERNET_KEY=...)
   make up                # dựng Airflow + metadata DB
   make ps                # chờ tới khi airflow-apiserver "healthy"
   ```
3. Mở http://localhost:8080 (admin/admin). Thấy giao diện Airflow là đạt. *(Buổi 2 sẽ đi sâu.)*
4. Tắt khi xong để tiết kiệm RAM: `make down`.

> Nếu máy yếu hoặc Docker chưa cài kịp: **bỏ qua phần 1 hôm nay**, làm phần 3 trước (không cần Docker), cài
> Docker sau. Buổi 2 mới thực sự cần Airflow chạy.

## Phần 2 — Khởi tạo repo cá nhân

Bạn sẽ phát triển Final Project trong chính repo của mình suốt khóa.

1. **Fork** repo khóa học trên GitHub về tài khoản của bạn, rồi clone về máy.
2. Tạo nhánh làm việc: `git checkout -b hoc-vien/<ten-cua-ban>`.
3. Kiểm tra cấu trúc đã có: `sessions/`, `dags/`, `data/`, `docs/`, `final-project/`.
4. Commit thử: `git commit --allow-empty -m "chore: bắt đầu khóa DataOps"` rồi `git push`.

> Vì sao bắt đầu bằng Git? Vì **reproducibility** (nguyên lý 4.3) bắt đầu từ version control. Mọi thứ trong
> khóa — code, config, runbook — đều sống trong Git.

## Phần 3 — "Bắt bệnh" pipeline (phần chính) 🔬

### Bước 1 — Chứng kiến lỗi double-counting

```bash
cd sessions/01-dataops-mindset/lab
python pipeline_risky.py        # lần 1
python pipeline_risky.py        # lần 2  <-- chú ý con số!
```

**Câu hỏi:** sau lần chạy thứ 2, tổng doanh thu ngày 09/07 thay đổi thế nào? Vì sao? Đây là vi phạm nguyên
lý nào trong buổi học?

> Dọn dẹp để chạy lại từ đầu: `rm warehouse.db`

### Bước 2 — Đọc & phân tích rủi ro

Mở `pipeline_risky.py`. Dùng **checklist pipeline production** (mục 5 của bài giảng) chấm điểm nó. Ghi
phân tích của bạn vào [`analysis_template.md`](./analysis_template.md) — file này chính là một bài tập nộp.

### Bước 3 — Chạy bản đã sửa & so sánh

```bash
rm -f warehouse.db
python pipeline_fixed.py 2026-07-09
python pipeline_fixed.py 2026-07-09      # chạy lại: con số CÓ đổi không?
python pipeline_fixed.py 2026-07-10
```

**Câu hỏi:** lần chạy lại 09/07 cho kết quả gì? So sánh với `pipeline_risky.py`. Đọc code và chỉ ra **chính
xác dòng nào** thực thi từng nguyên lý: idempotency, atomicity, reproducibility, reconciliation.

### Bước 4 — Thử phá reconciliation (nâng cao, tùy chọn)

Sửa 1 con số `amount` trong `sample_orders.csv` *sau khi* đã nạp, rồi nghĩ xem: nếu nguồn và đích lệch nhau,
cơ chế reconciliation trong `pipeline_fixed.py` sẽ phản ứng ra sao? (Gợi ý: thử tự tạo tình huống lệch và
quan sát thông báo `RECONCILIATION FAIL`.)

---

## Nộp gì sau lab

- `analysis_template.md` đã điền (phân tích rủi ro `pipeline_risky.py`).
- Repo cá nhân đã fork + push (link).
- (Tùy chọn) ảnh chụp Airflow UI chạy được trên máy bạn.
