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

up-cluster: ## Bật lakehouse + Spark Standalone cluster (master + 2 worker)
	$(COMPOSE) --profile core --profile lakehouse --profile cluster up -d --build

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

# ---- CI/CD (buổi 8) ----
lint: ## Lint code bằng ruff
	ruff check dags tests

test: ## Chạy unit & data tests
	pytest -q

scan: ## Quét secret hardcode
	python sessions/07-security-pii/lab/scan_secrets.py

ci: lint scan test ## Chạy TOÀN BỘ kiểm tra CI ở local (giống GitHub Actions)
	python -m py_compile dags/*.py
	@echo "✅ CI local PASS"

test-dags: ## Validate DAG sâu bằng Airflow thật (cần `make up`, dùng DagBag)
	docker compose exec airflow-scheduler airflow dags list

deploy-local: ## "Deploy" local: nạp lại DAG (mô phỏng CD). DAG mount sẵn -> chỉ cần Airflow đang chạy.
	docker compose restart airflow-dag-processor airflow-scheduler
	@echo "✅ Đã nạp lại DAG (CD local)."

# Buổi 5: chạy Spark job với Delta. Vd: make spark-job JOB=orders_delta_job DS=2026-06-20
# Lần chạy ĐẦU sẽ tải jar Delta từ Maven (cần internet); các lần sau dùng cache.
SESSION ?= 05-pyspark-lakehouse
JOB ?= orders_delta_job
DS  ?= 2026-06-20
spark-job: ## Chạy Spark job LOCAL (vd: make spark-job SESSION=06-performance-cost JOB=perf_spark_demo)
	docker compose exec spark /opt/spark/bin/spark-submit \
	  --packages io.delta:delta-spark_2.12:3.2.0 \
	  --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
	  --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog \
	  /opt/project/sessions/$(SESSION)/lab/jobs/$(JOB).py $(DS)

spark-job-cluster: ## Chạy Spark job trên CLUSTER (cần `make up-cluster` trước)
	docker compose exec spark /opt/spark/bin/spark-submit \
	  --master spark://spark-master:7077 \
	  --packages io.delta:delta-spark_2.12:3.2.0 \
	  --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
	  --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog \
	  /opt/project/sessions/$(SESSION)/lab/jobs/$(JOB).py $(DS)
