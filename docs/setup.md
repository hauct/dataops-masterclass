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

## 6. Troubleshooting

- **Airflow UI không lên / lỗi 502:** chờ 1–2 phút lần đầu (build image + `db migrate`). Xem log: `make logs S=airflow-apiserver`.
- **Cổng bị chiếm (port already in use):** đổi cổng trong `docker-compose.yml` hoặc tắt service đang chiếm.
- **Máy yếu/RAM thấp:** chỉ bật profile cần thiết cho buổi đó, đừng `make up-all`.
- **Image build chậm:** lần đầu kéo image apache/airflow khá nặng; những lần sau dùng cache.
- **Windows:** chạy lệnh trong Git Bash hoặc WSL2 để `make` hoạt động; hoặc gõ trực tiếp lệnh `docker compose` tương ứng trong Makefile.
