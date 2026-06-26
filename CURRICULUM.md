# Curriculum chi tiết — DataOps Master Class

11 buổi × 2 giờ + Final Project. Mỗi buổi: ~40% lý thuyết, ~50% thực hành, ~10% thảo luận case study.
Thuật ngữ kỹ thuật giữ nguyên tiếng Anh; giải thích bằng tiếng Việt.

> Trạng thái nội dung: ✅ = đã viết đầy đủ (lesson + lab + exercises + checklist) · 🚧 = đang biên soạn (mới có outline).

---

## Buổi 1 — Tư duy DataOps & Nguyên lý vận hành ✅
**Ngày 09/07 · [`sessions/01-dataops-mindset/`](./sessions/01-dataops-mindset/)**

Nội dung:
- DataOps là gì & ranh giới với Data Engineer / Data Analytics; vai trò của DataOps trong tổ chức.
- Vì sao reliability quan trọng — nhất là với dữ liệu tài chính / giao dịch.
- Nguyên lý cốt lõi: **idempotency, reproducibility, reconciliation**.
- Thế nào là một pipeline chuẩn trên production.
- Tổng quan tech stack & lộ trình khóa học.

Thực hành: cài Docker & dựng môi trường · khởi tạo Git repo & cấu trúc dự án · phân tích 1 pipeline để chỉ ra điểm rủi ro · thảo luận case study sự cố dữ liệu thực tế.

Mục tiêu: phân biệt rõ DataOps vs DE vs DA · hiểu idempotency & reconciliation và vì sao quan trọng · nắm các nguyên lý nền tảng dùng xuyên suốt khóa.

---

## Buổi 2 — Airflow 3: Kiến trúc & Triển khai 🚧
**Ngày 13/07 · [`sessions/02-airflow-architecture/`](./sessions/02-airflow-architecture/)**

Nội dung: Airflow là gì & vai trò trong DataOps · các component (Scheduler, Executor, Webserver/API server, Metadata DB, Worker, Triggerer) · các loại Executor (Local / Celery / Kubernetes) · các hướng triển khai (local Docker, Docker Compose, Kubernetes qua Helm) · giới thiệu HA & GitOps cho Airflow · **điểm mới ở Airflow 3** (DAG versioning, FastAPI UI, Task Execution API/Task SDK).

Thực hành: cài & chạy Airflow bằng Docker · làm quen UI, đọc logs, cấu trúc thư mục · quan sát demo Airflow trên K8s (Minikube) qua Helm · so sánh các hướng triển khai.

---

## Buổi 3 — Viết DAG & các khái niệm nâng cao 🚧
**Ngày 16/07 · [`sessions/03-writing-dags/`](./sessions/03-writing-dags/)**

Nội dung: DAG, Task, Operator & TaskFlow API · **idempotency & atomicity** vì sao cực kỳ quan trọng · scheduling (cron, `schedule`, catchup, backfill an toàn) · retry, timeout, SLA/Deadline, alert · dependency giữa Task & giữa DAG · XCom, Pool, Connection, Variable, Sensor · giới thiệu Assets (data-aware scheduling).

Thực hành: viết & chạy DAG đúng chuẩn vận hành · backfill an toàn (chạy lại không nhân đôi dữ liệu) · cấu hình retry/alert & dependency.

---

## Buổi 4 — SQL in DataOps — Stack Data Warehouse 🚧
**Ngày 20/07 · [`sessions/04-sql-dwh/`](./sessions/04-sql-dwh/)**

Nội dung: SQL pipeline reliable (MERGE/upsert, partition overwrite) · transaction & chạy lại không nhân đôi · **reconciliation** (đối soát số liệu nguồn vs đích) · quản lý dependency giữa các bước SQL.

Thực hành: viết SQL transform (MERGE/Upsert) · reconciliation nguồn↔đích · điều phối các bước SQL bằng Airflow · mô phỏng chạy lại & kiểm tra không trùng.

---

## Buổi 5 — PySpark in Modern Lakehouse 🚧
**Ngày 23/07 · [`sessions/05-pyspark-lakehouse/`](./sessions/05-pyspark-lakehouse/)**

Nội dung: khi nào cần Lakehouse · triển khai stack Lakehouse · PySpark pipeline reliable (atomic & idempotent writes, partition overwrite an toàn) · **table format (Delta/Iceberg)**: ACID & time travel · case study migrate DWH → Data Lake minimal-downtime.

Thực hành: viết PySpark job idempotent & retry-safe · ghi qua Delta + thử time travel · chạy job qua Airflow · mô phỏng job fail giữa chừng & chạy lại không hỏng dữ liệu.

---

## Buổi 6 — Tối ưu hiệu năng & chi phí 🚧
**Ngày 27/07 · [`sessions/06-performance-cost/`](./sessions/06-performance-cost/)**

Nội dung: tư duy tối ưu (đủ nhanh, không over-engineer) · đọc query plan (DWH) & Spark UI (Lakehouse) · bottleneck phổ biến (data skew, small-files, shuffle) · partitioning, caching, broadcast join · tối ưu chi phí cloud (FinOps cơ bản).

Thực hành: phân tích job/truy vấn chậm · tối ưu & đo before/after · xử lý small-files / data skew.

---

## Buổi 7 — Bảo mật & Dữ liệu nhạy cảm 🚧
**Ngày 30/07 · [`sessions/07-security-pii/`](./sessions/07-security-pii/)**

Nội dung: secrets management (tuyệt đối không hardcode) · xử lý PII (masking, encryption, anonymization) · phân quyền least-privilege · governance cho dữ liệu regulated (tài chính/ngân hàng) · audit logging cơ bản.

Thực hành: masking PII · quản lý secrets bằng env/secret manager · áp dụng phân quyền · rà soát pipeline & vá lỗ hổng.

---

## Buổi 8 — CI/CD cho Data Pipeline 🚧
**Ngày 03/08 · [`sessions/08-cicd/`](./sessions/08-cicd/)**

Nội dung: Git flow & vì sao cần CI/CD cho pipeline · test cho pipeline (unit test Python/SQL/Spark & data test) · CI (lint + test tự động) · CD (deploy lên môi trường) · GitOps & rollback.

Thực hành: viết test cơ bản · dựng luồng CI/CD chạy local/Docker · auto test & deploy · diễn tập rollback.

---

## Buổi 9 — Monitoring, Cảnh báo & Data Quality 🚧
**Ngày 06/08 · [`sessions/09-monitoring-dq/`](./sessions/09-monitoring-dq/)**

Nội dung: vì sao giám sát cả pipeline lẫn chất lượng dữ liệu · metrics & dashboard với Prometheus + Grafana · alerting đúng cách (tránh alert fatigue) · data quality testing với GX Core (schema, null, duplicate, business rules) · data freshness & reconciliation tự động.

Thực hành: dashboard giám sát · alert theo ngưỡng · suite test dữ liệu với GX gắn vào pipeline · mô phỏng dữ liệu bẩn & pipeline chặn lại · alert đến Slack.

---

## Buổi 10 — Sự cố, Root Cause Analysis (RCA) & Phục hồi 🚧
**Ngày 10/08 · [`sessions/10-incident-rca/`](./sessions/10-incident-rca/)**

Nội dung: quy trình điều tra nguyên nhân (RCA) · dùng metadata & lineage truy vết tác động & nguồn gốc lỗi · runbook · backup & disaster recovery (RTO/RPO) · case study: trợ lý DataOps tự động điều tra sự cố & gợi ý runbook (LLM agent). + Hướng dẫn Final Project (đề bài, tiêu chí, gợi ý kiến trúc).

Thực hành: truy vết lineage tìm nguồn gốc lỗi · viết runbook · diễn tập sự cố theo runbook · thảo luận chiến lược backup/DR.

---

## Buổi 11 — Project & Demo cuối khóa 🚧
**Ngày 13/08 · [`sessions/11-final-demo/`](./sessions/11-final-demo/)**

Học viên hoàn thiện & demo dự án DataOps end-to-end · trình bày quyết định thiết kế (reliability, security, monitoring) · review chéo & feedback mentor · tổng kết & **career roadmap: DataOps / Platform Engineer**.

---

## Final Project (Presentation)
Xem chi tiết: [`final-project/README.md`](./final-project/README.md).

Thiết kế, xây dựng & vận hành một pipeline dữ liệu **reliable end-to-end** xử lý dữ liệu giao dịch
(eCommerce/POS hoặc tài chính): idempotent, an toàn khi chạy lại/backfill, có reconciliation, data quality
testing, monitoring & alerting, masking PII & phân quyền, CI/CD trên Docker, runbook xử lý sự cố.
Chọn 1 trong 2 stack: **DWH (SQL/Postgres)** hoặc **Lakehouse (PySpark + Delta)**.
