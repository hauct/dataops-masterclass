# Buổi 2 — Airflow 3: Kiến trúc & Triển khai

> 🚧 **Đang biên soạn đầy đủ.** File này hiện là outline. Bài giảng chi tiết + lab + bài tập sẽ được bổ sung.

**Ngày:** 13/07  ·  **Bật stack:** `make up`

## Nội dung

- Airflow là gì & vai trò trong DataOps
- Các component: Scheduler, Executor, API server (Webserver), Metadata DB, Worker, Triggerer
- Các loại Executor: Local / Celery / Kubernetes — khác nhau ra sao
- Các hướng triển khai: local Docker, Docker Compose, Kubernetes (Helm)
- Giới thiệu HA & GitOps cho Airflow
- Điểm mới Airflow 3: DAG versioning, FastAPI UI, Task Execution API / Task SDK

## Thực hành

- Cài & chạy Airflow bằng Docker (`make up`)
- Làm quen Airflow UI, đọc logs, cấu trúc thư mục
- Quan sát demo Airflow trên K8s (Minikube) qua Helm
- So sánh các hướng triển khai & khi nào dùng cái nào

## Tài liệu trong buổi

- `README.md` — bài giảng (đang biên soạn)
- `lab/` — code thực hành (đang biên soạn)
- `exercises.md` · `checklist.md` (đang biên soạn)
