# Lab Buổi 2 — Dựng Airflow & quan sát kiến trúc

Mục tiêu: *nhìn tận mắt* các thành phần kiến trúc ở bài giảng đang phối hợp với nhau, qua một DAG demo.
Chưa cần hiểu cú pháp DAG (buổi 3) — buổi này tập trung **vận hành & quan sát**.

> Cần: stack core đang chạy (`make up`) và vào được http://localhost:8080 (admin/admin).

---

## Phần 1 — Khởi động & kiểm tra các thành phần

```bash
make up
make ps
```

Quan sát: bạn thấy các container `airflow-apiserver`, `airflow-scheduler`, `airflow-dag-processor`,
`airflow-meta` (Postgres). Đối chiếu với sơ đồ kiến trúc (mục 2 bài giảng): API Server + Scheduler +
DAG Processor + Metadata DB. *(Ở Airflow 3, DAG Processor là tiến trình **riêng** — thiếu nó thì DAG không
được parse. Executor LocalExecutor chạy bên trong scheduler.)*

**Soi log từng thành phần** (tập thói quen debug):
```bash
make logs S=airflow-scheduler     # thấy scheduler heartbeat & quét DAG
make logs S=airflow-apiserver     # thấy request từ UI
# Ctrl-C để thoát xem log
```

## Phần 2 — Quan sát DAG được DAG Processor "bắt"

Hai DAG demo đã nằm sẵn ở thư mục `dags/` của repo (đã mount vào container):
`session02_architecture_demo` và `session02_retry_demo`.

1. Mở http://localhost:8080. Ở danh sách DAG, tìm theo tag `buoi-02` (dùng ô filter tag).
2. Nếu chưa thấy: chờ ~30s (DAG Processor quét theo chu kỳ) rồi refresh. *(Đây chính là vai trò DAG
   Processor ở bài giảng — file `.py` → DAG trong UI.)*
3. Mở `session02_architecture_demo` → tab **Docs**: đọc mô tả (lấy từ `doc_md`).

## Phần 3 — Chạy DAG & quan sát Scheduler + Worker

1. Bật (unpause) DAG `session02_architecture_demo` bằng nút toggle.
2. Bấm **Trigger** (▶) để chạy tay.
3. Vào **Graph view**: quan sát thứ tự — `extract` và `validate` chạy **song song**, `load` chờ cả hai,
   rồi tới `report`. Đối chiếu với hình DAG trong bài giảng.
4. Mở **Grid view**, bấm vào ô một task → **Logs**: đọc các dòng log bạn thấy trong code (`EXTRACT: ...`).
   *(Đây là Worker thực sự chạy code & ghi log.)*

**Câu hỏi quan sát:**
- Trong lúc `extract`/`validate` đang chạy (có `time.sleep`), trạng thái của chúng là gì? Còn `load`?
- Vì sao `extract` và `validate` chạy được song song mà `load` thì không bắt đầu ngay?

## Phần 4 — Quan sát cơ chế retry (reliability)

1. Bật & **Trigger** DAG `session02_retry_demo`.
2. Vào Grid/Graph, theo dõi task `flaky`: nó sẽ **fail 2 lần đầu** rồi **success ở lần 3**.
3. Bấm vào task → xem được từng lần thử (try 1, 2, 3) và log tương ứng.

**Câu hỏi:** ai là người quyết định retry — Scheduler, Executor hay Worker? Việc tự retry này thể hiện
nguyên lý nào của buổi 1?

## Phần 5 — Thử nghiệm "bắt bệnh" kiến trúc (mini)

Làm 1 trong 2 (ghi lại quan sát):

- **A.** Tạm dừng scheduler: `docker compose stop airflow-scheduler`. Trigger một DAG → điều gì xảy ra với
  trạng thái run? Bật lại: `docker compose start airflow-scheduler` → nó "đuổi kịp" thế nào?
- **B.** Sửa nhẹ `dags/session02_architecture_demo.py` (vd: đổi dòng log trong `report`), lưu lại. Sau
  ~30s, mở lại UI: thay đổi có được phản ánh không? Thành phần nào chịu trách nhiệm việc đó?

---

## Nộp gì sau lab

- Ảnh chụp **Graph view** của `session02_architecture_demo` đã chạy thành công (4 task xanh).
- Ảnh chụp task `flaky` cho thấy nó retry rồi success.
- Trả lời ngắn các "câu hỏi quan sát" ở Phần 3, 4, 5 (vào `exercises.md` hoặc file riêng).

> Dọn dẹp khi xong: `make down` (giữ dữ liệu) — tiết kiệm RAM cho hôm sau.
