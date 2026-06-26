# Glossary — Thuật ngữ DataOps (VN + EN)

Tra cứu nhanh các thuật ngữ dùng xuyên suốt khóa. Thuật ngữ giữ tiếng Anh, giải thích tiếng Việt.

| Thuật ngữ | Giải thích ngắn |
|-----------|-----------------|
| **DataOps** | Áp dụng tư duy & thực hành DevOps/SRE vào vòng đời dữ liệu: tự động hóa, kiểm thử, giám sát, vận hành pipeline như một sản phẩm production. |
| **Idempotency** | Chạy một thao tác nhiều lần cho **cùng kết quả** như chạy một lần. Pipeline idempotent chạy lại không nhân đôi/hỏng dữ liệu. |
| **Atomicity** | "Được ăn cả, ngã về không" — thao tác hoặc thành công trọn vẹn, hoặc không để lại trạng thái nửa vời. |
| **Reproducibility** | Cùng input + cùng code + cùng môi trường → cùng output, ở bất kỳ thời điểm/máy nào. |
| **Reconciliation** | Đối soát số liệu nguồn vs đích (vd: tổng số bản ghi, tổng tiền) để khẳng định dữ liệu **đúng & đủ**. |
| **Backfill** | Chạy lại pipeline cho các mốc thời gian trong quá khứ (vd: nạp lại dữ liệu 30 ngày trước). |
| **Catchup** | Cơ chế Airflow tự động chạy bù các lần lịch bị bỏ lỡ giữa start_date và hiện tại. |
| **DAG** | Directed Acyclic Graph — đồ thị có hướng không chu trình, mô tả các task & thứ tự phụ thuộc trong Airflow. |
| **Operator / Task** | Operator = "khuôn" định nghĩa một việc; Task = một instance của operator trong DAG. |
| **Executor** | Thành phần Airflow quyết định task chạy ở đâu/thế nào (Local / Celery / Kubernetes). |
| **XCom** | Cơ chế truyền dữ liệu nhỏ giữa các task trong Airflow. |
| **Lakehouse** | Kiến trúc kết hợp data lake (object storage rẻ) + tính năng kiểu warehouse (ACID, schema) nhờ table format. |
| **Table format** | Delta Lake / Iceberg / Hudi — lớp metadata trên file parquet để có ACID, time travel, schema evolution. |
| **Time travel** | Truy vấn dữ liệu ở một phiên bản/thời điểm trong quá khứ của bảng. |
| **PII** | Personally Identifiable Information — dữ liệu nhận dạng cá nhân (tên, email, SĐT, CMND...). Cần masking/encryption. |
| **Secrets management** | Quản lý thông tin nhạy cảm (mật khẩu, token) ngoài code, qua env/secret manager. |
| **Least privilege** | Cấp quyền tối thiểu đủ dùng — nguyên tắc phân quyền an toàn. |
| **CI/CD** | Continuous Integration / Continuous Delivery — tự động lint, test, và deploy khi code thay đổi. |
| **Data Quality (DQ)** | Kiểm thử dữ liệu (schema, null, duplicate, business rules) để chặn dữ liệu xấu xuống hạ nguồn. |
| **Data freshness** | Độ "tươi" của dữ liệu — dữ liệu mới nhất cách hiện tại bao lâu. |
| **Observability** | Khả năng "nhìn thấu" hệ thống qua metrics, logs, traces để biết nó khỏe hay bệnh. |
| **Alert fatigue** | Tình trạng nhận quá nhiều cảnh báo (nhiều cái nhiễu) khiến người trực bỏ qua cả cảnh báo thật. |
| **Lineage** | Bản đồ nguồn gốc & dòng chảy dữ liệu — biết một bảng đến từ đâu, ảnh hưởng tới đâu. |
| **Runbook** | Kịch bản các bước xử lý một loại sự cố lặp lại. |
| **RCA** | Root Cause Analysis — quy trình điều tra nguyên nhân gốc của sự cố. |
| **SLO / SLI** | Service Level Objective / Indicator — mục tiêu & chỉ số đo mức dịch vụ (vd: 99% pipeline xong trước 6h sáng). |
| **RTO / RPO** | Recovery Time / Point Objective — thời gian khôi phục tối đa / mức mất dữ liệu tối đa chấp nhận được. |
| **HA / DR** | High Availability / Disaster Recovery — tính sẵn sàng cao & khôi phục sau thảm họa. |
| **Data contract** | Thỏa thuận tường minh giữa bên tạo & bên dùng dữ liệu về schema, ý nghĩa, SLA. |
| **GitOps** | Dùng Git làm "nguồn sự thật" để khai báo & triển khai hạ tầng/pipeline. |
