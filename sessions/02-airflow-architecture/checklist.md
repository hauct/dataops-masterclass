# Checklist tự đánh giá — Buổi 2

## Hiểu khái niệm

- [ ] Tôi giải thích được Airflow là gì và vì sao "workflows as code" hợp với DataOps.
- [ ] Tôi nêu được 2–3 việc Airflow **không** nên làm (xử lý dữ liệu lớn, streaming real-time, truyền data lớn qua XCom).
- [ ] Tôi mô tả được nhiệm vụ của: API Server, Scheduler, DAG Processor, Triggerer, Executor, Worker, Metadata DB.
- [ ] Cho một triệu chứng sự cố, tôi đoán được nên soi thành phần nào trước.

## Executor & triển khai

- [ ] Tôi phân biệt được Sequential / Local / Celery / Kubernetes executor và biết khi nào dùng cái nào.
- [ ] Tôi so sánh được 3 hướng triển khai (standalone / Docker Compose / K8s+Helm) về ưu–nhược.
- [ ] Tôi giải thích được ý tưởng HA (scheduler active-active) và GitOps cho Airflow.

## Airflow 3

- [ ] Tôi kể được ít nhất 3 điểm mới của Airflow 3 (DAG versioning, FastAPI UI/API Server, Task Execution API, assets...).
- [ ] Tôi biết Airflow 3 dùng `schedule=` (không còn `schedule_interval`).

## Thực hành

- [ ] Tôi đã `make up` thành công và vào được Airflow UI.
- [ ] Tôi đã chạy `session02_architecture_demo` và thấy `extract`/`validate` chạy song song, `load` chờ cả hai.
- [ ] Tôi đã đọc được log của một task trong UI.
- [ ] Tôi đã chạy `session02_retry_demo` và quan sát task retry rồi success.
- [ ] Tôi đã tự tạo & chạy được một DAG đơn giản của riêng mình (Bài 5).

## Sẵn sàng cho buổi 3

- [ ] Tôi biết buổi 3 sẽ đi sâu viết DAG đúng chuẩn: idempotency, scheduling/backfill, retry/SLA, XCom...
- [ ] Tôi tò mò muốn biết vì sao `extract()` trả về giá trị lại "đi qua XCom".

> ≥ 90% ô tích → vững. < 70% → ôn lại mục 2 (kiến trúc) & 3 (executor) trong `README.md`.
