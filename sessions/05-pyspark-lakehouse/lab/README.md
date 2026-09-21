# Lab Buổi 5 — PySpark + Delta Lake reliable

Mục tiêu: chạy PySpark job ghi Delta, **tự kiểm chứng** idempotency, mô phỏng fail, và thử **time travel** —
áp dụng nguyên lý buổi 1 lên stack Lakehouse.

> Cần: `make up-lakehouse` (bật Airflow core + MinIO + container `spark`). Code job ở [`jobs/`](./jobs/).
> ⚠️ Lần `make spark-job` ĐẦU TIÊN sẽ tải jar Delta từ Maven (cần internet, ~1–2 phút). Lần sau dùng cache.

---

## Phần 1 — Khởi động

```bash
make up-lakehouse
make ps                  # thấy thêm: minio, minio-init, spark
```

- MinIO console: http://localhost:9001 (minioadmin/minioadmin) — đã tạo sẵn bucket `lakehouse`.
- Container `spark` chạy nền, ta sẽ `exec` vào để submit job (qua `make spark-job`).

## Phần 2 — Ghi Delta & kiểm chứng idempotency (cốt lõi)

### Bước 1 — Đọc job trước

Mở [`jobs/orders_delta_job.py`](./jobs/orders_delta_job.py). Tìm dòng dùng `replaceWhere` — giải thích vì
sao nó làm job **idempotent**. So sánh với cách buổi 3 (file `.tmp`→rename) và buổi 4 (DELETE+INSERT/upsert).

### Bước 2 — Chạy lần đầu

```bash
make spark-job JOB=orders_delta_job DS=2026-06-20
```

Quan sát log: `[LOAD] ... ghi 25 dòng`, `[RECONCILE] ... khớp`, và bảng số dòng mỗi ngày. Xem dữ liệu Delta
xuất hiện trong repo: `data/lakehouse/orders/` (có thư mục `order_date=2026-06-20/` và `_delta_log/`).

### Bước 3 — Chạy LẠI cùng ngày (kiểm chứng idempotent)

```bash
make spark-job JOB=orders_delta_job DS=2026-06-20
make spark-job JOB=orders_delta_job DS=2026-06-20
```

**Câu hỏi:** số dòng của ngày 20/06 có tăng lên không sau 3 lần chạy? Vì sao? (So với `pipeline_risky.py` buổi 1.)

### Bước 4 — Thêm ngày khác (backfill thủ công)

```bash
make spark-job JOB=orders_delta_job DS=2026-06-21
make spark-job JOB=orders_delta_job DS=2026-06-22
```

Giờ bảng có 3 partition ngày, mỗi lần ghi chỉ đụng đúng partition của ngày đó (nhờ `replaceWhere`).

## Phần 3 — Time travel

```bash
make spark-job JOB=time_travel_demo
```

Quan sát: bảng `[HISTORY]` liệt kê các version (mỗi lần ghi = 1 version), và so sánh **version 0** với mới
nhất.

**Câu hỏi:** version 0 có bao nhiêu dòng, mới nhất bao nhiêu? Time travel giúp ích gì khi vận hành lỡ ghi sai dữ liệu?

## Phần 4 — Mô phỏng "fail giữa chừng" (ACID)

1. Chạy `orders_delta_job` cho một ngày để có dữ liệu.
2. Mở job, thêm tạm một dòng gây lỗi *sau* phần `df = ...` nhưng *trước* `.save(...)` — ví dụ
   `raise RuntimeError("giả lập fail")` — rồi chạy lại cùng ngày.

**Câu hỏi:** sau khi job fail, đọc lại bảng (`make spark-job JOB=time_travel_demo`) — partition của ngày đó
có bị hỏng/mất không? Vì sao Delta bảo vệ được (gợi ý: ACID, ghi là transaction)? (Nhớ xóa dòng raise sau khi thử.)

## Phần 5 — (Tùy chọn, nâng cao) Ghi Delta lên MinIO thật

Mặc định lab ghi ra filesystem local. Để dùng **object storage thật** (đúng tinh thần Lakehouse):

```bash
docker compose exec \
  -e LAKE_BASE=s3a://lakehouse \
  spark /opt/spark/bin/spark-submit \
  --packages io.delta:delta-spark_2.12:3.2.0,org.apache.hadoop:hadoop-aws:3.3.4 \
  --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
  --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog \
  /opt/project/sessions/05-pyspark-lakehouse/lab/jobs/orders_delta_job.py 2026-06-20
```

Khác biệt: thêm `LAKE_BASE=s3a://lakehouse` và package `hadoop-aws` (để Spark nói chuyện S3A với MinIO).
Sau đó vào MinIO console (http://localhost:9001) xem bucket `lakehouse/orders/` có dữ liệu Delta.

**Câu hỏi:** code job có phải sửa gì để chạy trên MinIO không? (Gợi ý: xem `common.py` xử lý `LAKE_BASE`.)

---

## Phần 5b — (Tùy chọn) Chạy trên Spark Standalone cluster

Mặc định job chạy **local mode** (1 JVM). Để thấy job chạy **phân tán** trên cụm thật (1 master + 2 worker):

```bash
make up-cluster                                   # dựng thêm spark-master + 2 spark-worker
make spark-job-cluster JOB=orders_delta_job DS=2026-06-20
```

Khác biệt duy nhất so với `make spark-job` là thêm `--master spark://spark-master:7077` (submit tới master
thay vì chạy local). Mở **Spark Master UI** tại http://localhost:8085 để thấy:
- 2 worker đã đăng ký (ALIVE), tổng số core/RAM.
- Application đang/đã chạy, executors nằm trên các worker khác nhau.

**Câu hỏi:** code job có phải sửa gì khi chuyển từ local sang cluster không? (Gợi ý: không — chỉ đổi
`--master`. Đây là lý do tách "logic job" khỏi "cách chạy".) Vì sao job vẫn idempotent trên cluster?

> Lưu ý: cụm này dùng chung bind mount `data/` nên mọi worker đọc/ghi cùng bảng Delta. Trong production
> thật, storage là object storage chung (S3/MinIO) chứ không phải đĩa local — xem Phần 5.

## Phần 6 — Tự làm (mini)

Trong repo của bạn: thêm một job `daily_revenue_delta.py` đọc bảng `orders` (Delta) và ghi ra bảng Delta thứ
hai `daily_revenue` (tổng hợp theo `order_date`), cũng idempotent bằng `replaceWhere`. Thêm reconciliation.

---

## Nộp gì sau lab

- Log/ảnh chạy `orders_delta_job` + chứng minh chạy lại không nhân đôi.
- Log `time_travel_demo` (history + version 0 vs mới nhất).
- Trả lời các "câu hỏi" Phần 2, 3, 4, (5).
- (Phần 6) job mới trong repo cá nhân.

> Dọn: `rm -rf data/lakehouse`. Tắt stack: `make down`.
