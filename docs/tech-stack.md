# Tech stack & lý do chọn (version pinning)

Triết lý: **reproducible** (ai chạy cũng giống nhau) + **gần thực tế production** + **chạy được trên laptop**.
Vì vậy pin version cụ thể, ưu tiên tổ hợp ổn định đã được kiểm chứng rộng rãi thay vì bản mới nhất.

| Lớp | Công cụ | Version (pin) | Bản mới nhất (06/2026) | Ghi chú |
|-----|---------|---------------|------------------------|---------|
| Orchestration | Apache Airflow | **3.0.6** | 3.2.2 | Bản 3.0.x ổn định, tài liệu nhiều. Đã có DAG versioning, FastAPI UI, Task SDK. |
| DWH | PostgreSQL | **16** | 17 | Dùng làm SQL data warehouse mô phỏng (MERGE, transaction). |
| Lakehouse compute | Apache Spark (PySpark) | **3.5.x** | 4.1 | 3.5 + Delta 3.x là tổ hợp cực kỳ ổn định để học local. |
| Table format | Delta Lake | **3.2.x** | 4.2 | ACID + time travel. Sẽ giới thiệu thêm Iceberg & UniForm. |
| Object storage | MinIO | latest | — | S3-compatible, đóng vai trò "data lake" trên laptop. |
| Data Quality | Great Expectations (GX Core) | **1.3.x** | 1.x | API fluent mới (GX Core 1.0), gắn vào pipeline. |
| Monitoring | Prometheus + Grafana | latest | — | Metrics + dashboard + alerting. |
| CI/CD | GitHub Actions | — | — | Lint + test + deploy; chạy được tương đương trên local. |

## Vì sao không luôn dùng bản mới nhất?

Trong DataOps, **độ ổn định và khả năng tái lập** quan trọng hơn việc chạy bản mới nhất. Một stack mà
"hôm nay chạy, mai update là vỡ" là phản DataOps. Ta pin version, ghi rõ trong code, và chỉ nâng cấp có
chủ đích kèm test (đúng tinh thần buổi 8 — CI/CD).

## Những cập nhật mới của ngành (2026) sẽ được nhắc trong khóa

- **Airflow 3:** DAG versioning, **asset/event-driven scheduling** (thay cho Dataset cũ), Task Execution API,
  UI viết lại bằng React + FastAPI. (Buổi 2, 3)
- **Delta Lake 4 / Spark 4:** kiểu dữ liệu `VARIANT` cho semi-structured, **liquid clustering** thay
  partition Hive-style, UniForm (đọc Delta như Iceberg/Hudi). (Buổi 5)
- **Iceberg vs Delta:** khoảng cách tính năng đã thu hẹp; lựa chọn nay dựa vào hệ sinh thái & độ phụ
  thuộc vendor. (Buổi 5)
- **Data contracts, observability, SLO/SLI, FinOps, AI-assisted RCA:** xu hướng tuyển dụng DataOps 2026
  — lồng vào buổi 9, 10. (Đây là phần giúp hồ sơ bạn nổi bật.)

## Nguồn tham khảo chuẩn hóa kiến thức

- Apache Airflow 3 GA — https://airflow.apache.org/blog/airflow-three-point-oh-is-here/
- Delta Lake 4.0 — https://delta.io/blog/delta-lake-4-0/
- GX Core 1.0 — https://greatexpectations.io/blog/introducing-gx-core-1-0/
- DataOps Engineer skills 2026 — https://atlan.com/dataops-engineer-skills/
