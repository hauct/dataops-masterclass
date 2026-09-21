# Hướng dẫn cài đặt môi trường

Mọi thứ chạy local bằng Docker — không cần tài khoản cloud.

## 1. Yêu cầu phần cứng & phần mềm

- **RAM:** tối thiểu 6GB cấp cho Docker, khuyến nghị 8GB+.
- **Đĩa trống:** ~10GB.
- **Phần mềm:**
  - [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/macOS) hoặc Docker Engine + Compose plugin (Linux).
  - [Git](https://git-scm.com/downloads).
  - Trình soạn thảo: VS Code (khuyến nghị) + extension Python, Docker.
  - Python 3.11+ trên máy host (để chạy vài lệnh tiện ích như `make fernet`).

Kiểm tra:
```bash
docker --version          # >= 24
docker compose version    # >= 2.20
git --version
python --version          # >= 3.11
```

## 2. Lấy code & cấu hình

```bash
git clone <your-fork-url> dataops-masterclass
cd dataops-masterclass
cp .env.example .env
make fernet                 # copy dòng AIRFLOW_FERNET_KEY=... vào .env
```

Mở `.env`, dán Fernet key vừa sinh và đổi `AIRFLOW_SECRET_KEY` thành chuỗi ngẫu nhiên.

## 3. Bật stack

| Buổi | Lệnh | Service |
|------|------|---------|
| 2, 3 | `make up` | Airflow + metadata DB |
| 4 | `make up-warehouse` | + Postgres warehouse |
| 5, 6 | `make up-lakehouse` | + MinIO |
| 9 | `make up-monitoring` | + Prometheus + Grafana |
| Tất cả | `make up-all` | toàn bộ |

Kiểm tra: `make ps` — các service ở trạng thái `running`/`healthy`.

## 4. Các URL truy cập

| Dịch vụ | URL | Đăng nhập |
|---------|-----|-----------|
| Airflow UI | http://localhost:8080 | `admin` / `admin` |
| MinIO Console | http://localhost:9001 | `minioadmin` / `minioadmin` |
| Prometheus | http://localhost:9090 | — |
| Grafana | http://localhost:3000 | `admin` / (env) |
| Warehouse (psql) | `localhost:5433` | `dwh` / `dwh` |

## 5. Tắt / dọn dẹp

```bash
make down      # tắt, giữ dữ liệu
make clean     # tắt & xóa volumes (mất dữ liệu)
```

## 5b. Môi trường Python local (venv)

Docker lo phần chạy pipeline; nhưng để **chạy lab, lint code & test** trên máy bạn, hãy tạo một virtual
environment riêng cho project. Tạo **một lần**, dùng cho cả khóa.

### Windows (PowerShell)

```powershell
cd dataops-masterclass
py -m venv .venv                      # tạo venv (Python 3.11+)
.\.venv\Scripts\Activate.ps1          # kích hoạt (thấy "(.venv)" ở đầu dòng)
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

> Nếu PowerShell chặn script: chạy `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` rồi thử lại.
> Dùng Git Bash thì kích hoạt bằng `source .venv/Scripts/activate`.

### macOS / Linux

```bash
cd dataops-masterclass
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
```

### Kiểm tra & dùng

```bash
python --version            # 3.11+
ruff --version              # linter sẵn sàng
python sessions/01-dataops-mindset/lab/pipeline_fixed.py 2026-07-09   # chạy thử lab buổi 1
```

Thoát môi trường: `deactivate`. Thư mục `.venv/` đã được `.gitignore` bỏ qua — không commit lên GitHub.

> Lab buổi 1 chỉ dùng thư viện chuẩn (sqlite, csv) nên chạy được **không cần** cài gì. Cài
> `requirements-dev.txt` để chuẩn bị cho các buổi sau (pandas, ruff, pytest, Great Expectations).

## 5c. Airflow 3 trên Docker Compose: các điểm BẮT BUỘC cấu hình

Airflow 3 thay đổi khá nhiều so với Airflow 2. Dưới đây là 4 điểm hay làm "đứng hình" khi tự dựng — khóa
học đã cấu hình sẵn trong `docker-compose.yml`, ghi lại đây để bạn hiểu vì sao (và tự xử khi gặp ở nơi khác):

1. **Đăng nhập user/password cần FAB auth manager.** Airflow 3 mặc định dùng `SimpleAuthManager` (không có
   form login truyền thống). Để dùng `admin/admin` ta phải: cài `apache-airflow-providers-fab` và đặt
   `AIRFLOW__CORE__AUTH_MANAGER=...FabAuthManager`. Triệu chứng nếu thiếu: **401 Invalid credentials**.

2. **FAB có DB riêng — phải `fab-db migrate`.** Ở Airflow 3, `airflow db migrate` KHÔNG tạo bảng user của
   FAB. Phải chạy thêm `airflow fab-db migrate` (đã thêm vào `airflow-init`). Triệu chứng nếu thiếu:
   trang login báo **"Something bad has happened"**.

3. **DAG Processor là service RIÊNG.** Khác Airflow 2 (scheduler tự parse), Airflow 3 cần tiến trình
   `airflow dag-processor` chạy độc lập. Triệu chứng nếu thiếu: **DAG không xuất hiện trên UI** dù file đã
   nằm trong `dags/`.

4. **Task Execution API: URL + JWT secret dùng chung.** Task chạy ở container scheduler phải gọi API trên
   container apiserver:
   - `AIRFLOW__CORE__EXECUTION_API_SERVER_URL=http://airflow-apiserver:8080/execution/` (không dùng
     `localhost` vì khác container). Triệu chứng nếu sai: task **fail ngay, connection refused**.
   - `AIRFLOW__API_AUTH__JWT_SECRET=<chuỗi cố định>` giống nhau ở MỌI container. Triệu chứng nếu thiếu:
     task fail với **"Invalid auth token: Signature verification failed" (403)**.

> Tất cả đã được set trong `docker-compose.yml` (qua anchor `*-airflow-common` để mọi service nhận cùng
> giá trị). Nếu đổi secret, nhớ `make up` lại để container nạp env mới.

## 6. Troubleshooting

- **Airflow UI không lên / lỗi 502:** chờ 1–2 phút lần đầu (build image + `db migrate`). Xem log: `make logs S=airflow-apiserver`.
- **Cổng bị chiếm (port already in use):** đổi cổng trong `docker-compose.yml` hoặc tắt service đang chiếm.
- **Máy yếu/RAM thấp:** chỉ bật profile cần thiết cho buổi đó, đừng `make up-all`.
- **Image build chậm:** lần đầu kéo image apache/airflow khá nặng; những lần sau dùng cache.
- **Windows:** chạy lệnh trong Git Bash hoặc WSL2 để `make` hoạt động; hoặc gõ trực tiếp lệnh `docker compose` tương ứng trong Makefile.
