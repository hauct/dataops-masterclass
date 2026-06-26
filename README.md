# Master Class: DataOps for Data Platforms — From Pipeline to Production

> Khóa học vận hành (operate) data platform ở mức production: viết pipeline **reliable**,
> kiểm thử chất lượng dữ liệu, giám sát & cảnh báo, bảo mật dữ liệu nhạy cảm, và xử lý sự cố
> theo quy trình. Toàn bộ khóa học là **một codebase chạy được hoàn toàn trên máy local bằng Docker**.

[![Stack](https://img.shields.io/badge/stack-Airflow%203%20%7C%20Spark%20%7C%20Delta%20%7C%20Postgres-blue)]()
[![Run](https://img.shields.io/badge/run-Docker%20Compose-2496ED)]()
[![Lang](https://img.shields.io/badge/lang-Vietnamese%20%2B%20EN%20terms-success)]()

---

## 1. Khóa học này dành cho ai?

- Học viên đã có nền tảng **Data Engineering** muốn học cách **VẬN HÀNH** hệ thống dữ liệu ở production.
- Data Engineer muốn nâng kỹ năng về **reliability, security, monitoring & xử lý sự cố**.
- System Engineer / DevOps muốn chuyển hướng sang lĩnh vực Data.
- Người muốn định hướng sang vai trò **DataOps / Platform Engineer**.

**Yêu cầu đầu vào:** Python cơ bản · SQL cơ bản (JOIN, GROUP BY) · quen Docker & command line.
Từng làm pipeline ETL/ELT là một lợi thế (không bắt buộc).

## 2. Sau khóa học bạn làm được gì?

Đây là phần quan trọng nhất — output để **cạnh tranh khi đi xin việc**:

- Hiểu tư duy DataOps và vì sao **reliability** quan trọng (idempotency, reconciliation, reproducibility).
- Viết pipeline an toàn với **Airflow 3** và triển khai ổn định bằng Docker.
- Vận hành reliable trên **2 stack**: SQL Data Warehouse (Postgres) & PySpark Lakehouse (Delta Lake + MinIO).
- Tối ưu hiệu năng & chi phí ở mức thực dụng (đọc query plan, Spark UI, FinOps cơ bản).
- Áp dụng security: secrets management, masking PII, phân quyền theo least-privilege.
- Thiết lập **CI/CD**, **monitoring** (Prometheus + Grafana) & **data quality** (Great Expectations / GX Core).
- Dùng **lineage** để truy vết sự cố, viết **runbook**, nắm khái niệm backup/DR (RTO/RPO).
- Hoàn thiện **1 project DataOps end-to-end** để đưa vào CV/Portfolio.

> 💡 **Điểm khác biệt với hồ sơ Data Engineer thuần:** portfolio của bạn nhấn vào *độ tin cậy & khả năng vận hành* — đúng thứ mà thị trường tuyển dụng 2026 đang đề cao (reliability engineering, observability, data contracts, SLO/SLI).

## 3. Lộ trình 11 buổi (20h–22h, Thứ 2 & Thứ 5)

| # | Buổi | Chủ đề | Output chính |
|---|------|--------|--------------|
| 1 | 09/07 | Tư duy DataOps & nguyên lý vận hành | Môi trường Docker + repo + phân tích rủi ro pipeline |
| 2 | 13/07 | Airflow 3: kiến trúc & triển khai | Airflow chạy ổn định trên Docker |
| 3 | 16/07 | Viết DAG & khái niệm nâng cao | DAG idempotent, backfill an toàn |
| 4 | 20/07 | SQL in DataOps — stack Data Warehouse | Pipeline SQL MERGE/upsert + reconciliation |
| 5 | 23/07 | PySpark in Modern Lakehouse | Job PySpark idempotent trên Delta Lake |
| 6 | 27/07 | Tối ưu hiệu năng & chi phí | Tối ưu job/truy vấn, đo before/after |
| 7 | 30/07 | Bảo mật & dữ liệu nhạy cảm | Pipeline có masking PII + secrets + RBAC |
| 8 | 03/08 | CI/CD cho data pipeline | Pipeline CI/CD chạy trên Docker |
| 9 | 06/08 | Monitoring, cảnh báo & Data Quality | Dashboard Grafana + GX suite + alert Slack |
| 10 | 10/08 | Sự cố, RCA & phục hồi | Lineage + runbook + diễn tập sự cố |
| 11 | 13/08 | Project & Demo cuối khóa | Demo pipeline end-to-end + career roadmap |

Chi tiết đầy đủ: xem [`CURRICULUM.md`](./CURRICULUM.md).
Đề bài cuối khóa: xem [`final-project/README.md`](./final-project/README.md).

## 4. Cách dùng repo này

Mỗi buổi nằm trong `sessions/NN-ten-buoi/` gồm:

- `README.md` — bài giảng lý thuyết chi tiết (đọc trước/sau buổi học).
- `lab/` — code thực hành: starter + solution + dữ liệu mẫu, hướng dẫn từng bước.
- `exercises.md` — bài tập về nhà.
- `checklist.md` — checklist tự đánh giá "đã nắm bài chưa".

### Bắt đầu nhanh

```bash
git clone <your-fork-url> dataops-masterclass
cd dataops-masterclass
cp .env.example .env          # điền secrets local
make up                       # dựng toàn bộ stack bằng Docker
make ps                       # kiểm tra các service đã chạy
```

Hướng dẫn cài đặt chi tiết (Docker Desktop, RAM tối thiểu, troubleshooting): [`docs/setup.md`](./docs/setup.md).

## 5. Tech stack (chuẩn hóa, pin version)

Toàn bộ chạy local bằng Docker — **không cần tài khoản cloud**. Lý do chọn từng công cụ & version: [`docs/tech-stack.md`](./docs/tech-stack.md).

| Lớp | Công cụ | Vì sao |
|-----|---------|--------|
| Orchestration | **Apache Airflow 3.x** | Chuẩn ngành; bản 3 có DAG versioning, asset/event-driven scheduling |
| DWH (stack 1) | **PostgreSQL 16** | SQL warehouse mô phỏng, MERGE/upsert, transaction |
| Lakehouse (stack 2) | **PySpark + Delta Lake** trên **MinIO** (S3-compatible) | Table format ACID, time travel, object storage thật |
| Data Quality | **Great Expectations (GX Core 1.0)** | Kiểm thử dữ liệu chuẩn, gắn vào pipeline |
| Monitoring | **Prometheus + Grafana** | Metrics + dashboard + alerting |
| CI/CD | **GitHub Actions** (+ chạy được local) | Lint, test, deploy tự động |
| Secrets | **.env + Airflow Connections/Variables** | Không hardcode |

## 6. Mentor

**Nguyễn Hoàng Quốc Anh** — Senior Data Engineer / Senior DataOps (Techcombank).
Kinh nghiệm sâu Data/Ops Engineer (Banking & E-Commerce): xây pipeline quy mô lớn (batch & streaming),
vận hành data platform trên Kubernetes, streaming hàng triệu event/ngày latency thấp,
data quality / reconciliation / governance cho dữ liệu tài chính.

## 7. License

[MIT](./LICENSE) — tự do dùng cho mục đích học tập.
