# Lab Buổi 3 — Viết DAG idempotent & các khái niệm nâng cao

Mục tiêu: tự tay viết/chạy DAG đúng chuẩn vận hành và **kiểm chứng** tính idempotent — không chỉ tin lý thuyết.

> Cần: `make up` đang chạy, đăng nhập được UI (admin/admin). Hai DAG đã có sẵn trong `dags/`:
> `session03_idempotent_partition` và `session03_concepts_demo` (lọc tag `buoi-03`).

---

## Phần 1 — DAG idempotent + atomic (cốt lõi)

### Bước 1 — Đọc code trước khi chạy

Mở `dags/session03_idempotent_partition.py`. Tìm và chỉ ra **chính xác dòng nào** thực hiện:
- Lấy `ds` (logical date) từ context — không dùng `now()`.
- Ghi atomic (`.tmp` → `os.replace`).
- Ghi đè theo partition `dt=<ds>`.
- Reconciliation nguồn ↔ đích.

### Bước 2 — Chạy & kiểm chứng idempotency

1. Bật (unpause) `session03_idempotent_partition`, **Trigger** một run.
2. Xem Graph: `extract → load_idempotent → reconcile` chạy xanh.
3. Xem output ngay trong repo: `data/output/orders/dt=<ngày>/data.json`.
4. **Trigger lại** đúng run đó (hoặc Clear để chạy lại). Mở lại file output:

**Câu hỏi:** số dòng trong file có **tăng gấp đôi** không? Vì sao? So sánh với `pipeline_risky.py` ở buổi 1.

### Bước 3 — Backfill an toàn

Chạy backfill vài ngày quá khứ (trong container scheduler):

```bash
# Lưu ý: dùng ngày trong QUÁ KHỨ (>= start_date 2026-06-01 và <= hôm nay) thì mới chạy.
docker compose exec airflow-scheduler \
  airflow backfill create --dag-id session03_idempotent_partition \
  --from-date 2026-06-20 --to-date 2026-06-24
```

Quan sát trên UI: các run cho 20→24/06 được tạo & chạy. Kiểm tra `data/output/orders/` có các thư mục
`dt=2026-06-20 … dt=2026-06-24`.

**Câu hỏi:** chạy lại lệnh backfill trên lần nữa — dữ liệu các ngày đó có bị nhân đôi không? Nguyên lý nào bảo vệ bạn?

## Phần 2 — Các khái niệm nâng cao

### Bước 4 — Chạy `session03_concepts_demo`

1. Trigger DAG. Quan sát Graph: `transform_a` & `transform_b` chạy **song song**, `combine` chờ cả hai.
2. Mở log task `extract`: thấy nó trả về **đường dẫn file** (con trỏ), không phải cả list dữ liệu.
3. Mở tab **XCom** của task `extract`: giá trị XCom là *path*, không phải khối dữ liệu. *(Đây là quy tắc
   "truyền con trỏ, không truyền hàng hóa".)*

### Bước 5 — Thử Variable

1. Trên UI: **Admin → Variables → +**, tạo `demo_num_rows = 20`.
2. Trigger lại `session03_concepts_demo`. Log `extract` giờ sinh 20 dòng (thay vì default 8).

**Câu hỏi:** nếu xóa Variable đi, DAG có lỗi không? Vì sao (gợi ý: tham số `default`)?

### Bước 6 — Quan sát retry/timeout (đọc code)

Trong `session03_concepts_demo.py`, task `extract` có `retries=2`, `execution_timeout=5 phút`. Giải thích:
khi nào retry *giúp ích*, khi nào retry *vô nghĩa* (gợi ý: lỗi tạm thời vs lỗi logic)?

---

## Phần 3 — Tự viết (mini)

Tạo DAG mới `dags/<ten-ban>_daily_kpi.py`:
- `schedule="@daily"`, `start_date` trong quá khứ gần, `catchup=False`, tag `buoi-03`.
- 3 task TaskFlow: `extract` (sinh dữ liệu theo `ds`) → `aggregate` (tính 1 KPI) → `save` (ghi atomic theo
  partition `dt=<ds>`).
- Đảm bảo **idempotent**: trigger 2 lần cùng ngày, output không đổi.

---

## Nộp gì sau lab

- Ảnh Graph view của `session03_idempotent_partition` chạy xanh + ảnh thư mục `data/output/orders/`.
- Trả lời các "câu hỏi" ở Bước 2, 3, 5, 6.
- DAG tự viết ở Phần 3 (trong repo cá nhân) + bằng chứng chạy lại không nhân đôi.

> Permission khi ghi `data/output/`: nếu gặp lỗi *Permission denied*, chạy trên host
> `mkdir -p data/output && chmod -R 777 data/output` rồi trigger lại. Dọn output: `rm -rf data/output`.
> Tắt stack khi xong: `make down`.
