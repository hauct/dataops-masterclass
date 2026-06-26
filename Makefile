# Lệnh tắt để quản lý stack. Gõ `make help` để xem tất cả.
.DEFAULT_GOAL := help
COMPOSE := docker compose

help: ## Hiện danh sách lệnh
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-16s\033[0m %s\n",$$1,$$2}'

up: ## Bật core (Airflow + metadata DB) — buổi 2,3
	$(COMPOSE) --profile core up -d --build

up-warehouse: ## Bật core + Postgres warehouse — buổi 4
	$(COMPOSE) --profile core --profile warehouse up -d --build

up-lakehouse: ## Bật core + MinIO object storage — buổi 5,6
	$(COMPOSE) --profile core --profile lakehouse up -d --build

up-monitoring: ## Bật core + Prometheus + Grafana — buổi 9
	$(COMPOSE) --profile core --profile monitoring up -d --build

up-all: ## Bật toàn bộ stack
	$(COMPOSE) --profile all up -d --build

ps: ## Xem trạng thái các service
	$(COMPOSE) ps

logs: ## Xem logs (vd: make logs S=airflow-scheduler)
	$(COMPOSE) logs -f $(S)

down: ## Tắt toàn bộ (giữ lại dữ liệu)
	$(COMPOSE) --profile all down

clean: ## Tắt & xóa luôn volumes (mất hết dữ liệu — cẩn thận!)
	$(COMPOSE) --profile all down -v

fernet: ## Sinh Fernet key để mã hóa secrets trong Airflow
	@python -c "from cryptography.fernet import Fernet; print('AIRFLOW_FERNET_KEY='+Fernet.generate_key().decode())"
