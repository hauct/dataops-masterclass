# Final Project — Pipeline dữ liệu reliable end-to-end

> Sản phẩm "đinh" trong portfolio của bạn. Mục tiêu: chứng minh bạn không chỉ *xây* được pipeline mà
> còn *vận hành* nó như một hệ thống production — đúng thứ nhà tuyển dụng DataOps/Platform tìm kiếm.

## Bối cảnh nghiệp vụ

Xây dựng pipeline đưa dữ liệu **giao dịch** (eCommerce/POS hoặc tài chính) thành các bảng phân tích sạch,
phục vụ báo cáo doanh thu hằng ngày. Dữ liệu đến theo lô (batch) mỗi ngày, có thể trễ, trùng, hoặc sai —
pipeline phải xử lý an toàn.

## Yêu cầu đầu ra (bắt buộc)

1. **Idempotent & an toàn khi chạy lại / backfill** — chạy lại một ngày không nhân đôi/hỏng dữ liệu.
2. **Reconciliation** — đối soát nguồn ↔ đích (số bản ghi, tổng tiền) và báo lệch.
3. **Data quality testing** — chặn dữ liệu xấu trước khi xuống hạ nguồn (schema, null, duplicate, business rule).
4. **Monitoring & alerting** — dashboard sức khỏe pipeline + cảnh báo khi sự cố.
5. **Bảo mật** — PII được masking/encryption; secrets không nằm trong code; phân quyền least-privilege.
6. **CI/CD** — tự động lint + test + deploy, chạy trên local/Docker.
7. **Runbook** — kịch bản xử lý ít nhất 2 loại sự cố.

## Kiến trúc tổng quan (chọn 1 trong 2 stack)

- **Stack DWH:** SQL trên Data Warehouse (Postgres/BigQuery...).
- **Stack Lakehouse:** PySpark + table format (Delta/Iceberg) trên object storage (MinIO/S3).

Chung cho cả hai: điều phối bằng **Apache Airflow** · CI/CD trên **Docker** · monitoring bằng
**Prometheus + Grafana** · data quality bằng **Great Expectations** · triển khai bằng **Docker Compose** ·
có **runbook** xử lý sự cố.

## Tiêu chí đánh giá (rubric)

| Hạng mục | Trọng số | Tốt = … |
|----------|----------|---------|
| Reliability (idempotency, backfill, atomic) | 30% | Chạy lại nhiều lần kết quả không đổi; có bằng chứng test |
| Data quality & reconciliation | 20% | Có suite test + đối soát tự động, chặn được dữ liệu bẩn |
| Monitoring & alerting | 15% | Dashboard + alert có ý nghĩa, không alert fatigue |
| Security | 15% | Không có secret trong repo; PII được che; phân quyền rõ |
| CI/CD | 10% | Pipeline tự động lint/test/deploy; có rollback |
| Trình bày & runbook | 10% | Giải thích được quyết định thiết kế; runbook dùng được |

## Kiến thức & kỹ năng đạt được

Thiết kế & vận hành pipeline reliable theo tư duy DataOps · viết pipeline idempotent & reconciliation ·
vận hành trên stack DWH hoặc Lakehouse · áp dụng security cơ bản · thiết lập CI/CD, monitoring & DQ ·
viết runbook & xử lý sự cố cơ bản.

## Lợi ích sau khi hoàn thành

- Có **portfolio DataOps thực tế**, nhấn vào độ tin cậy & vận hành.
- **Khác biệt** với hồ sơ Data Engineer thuần.
- Nền tảng vững để học sâu **HA, streaming nâng cao & disaster recovery**.

## Nộp bài

- Repo Git công khai (fork từ repo khóa học) với code + README mô tả kiến trúc & quyết định thiết kế.
- Slide/demo 10–15 phút ở buổi 11.
- Checklist tự đánh giá theo rubric ở trên trước khi nộp.
