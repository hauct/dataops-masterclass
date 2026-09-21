# Checklist tự đánh giá — Buổi 5

## Tư duy & khái niệm

- [ ] Tôi giải thích được Lakehouse = object storage + table format, và khi nào chọn nó thay vì DWH.
- [ ] Tôi hiểu vì sao Spark chạy ở engine riêng, không nhét vào Airflow worker.
- [ ] Tôi biết Delta vs Iceberg khác nhau chủ yếu ở hệ sinh thái (và các điểm mới Delta 4/Spark 4).

## PySpark reliable

- [ ] Tôi giải thích được `replaceWhere` làm job idempotent thế nào.
- [ ] Tôi nêu được cách đạt idempotency ở cả 3 stack (file / SQL / Delta).
- [ ] Tôi hiểu vì sao Delta cho atomicity "miễn phí" (ACID transaction) — không cần tự làm `.tmp`/rename.

## Table format

- [ ] Tôi đọc được dữ liệu ở phiên bản cũ bằng time travel (`versionAsOf`).
- [ ] Tôi xem được lịch sử bảng bằng `DeltaTable.history()`.
- [ ] Tôi hiểu time travel giúp gì cho vận hành/khôi phục sự cố.

## Thực hành

- [ ] Tôi chạy được `orders_delta_job` và thấy dữ liệu Delta trong `data/lakehouse/orders/`.
- [ ] Tôi **tự kiểm chứng** chạy lại cùng ngày không nhân đôi.
- [ ] Tôi chạy được `time_travel_demo` và đọc được version 0.
- [ ] (Tùy chọn) Tôi ghi được Delta lên MinIO qua S3A.

## Orchestration

- [ ] Tôi biết Airflow submit Spark job bằng SparkSubmitOperator / KubernetesPodOperator trong production.

> ≥ 90% → sẵn sàng buổi 6 (tối ưu hiệu năng & chi phí). < 70% → ôn lại mục 3 (`replaceWhere`) & 4 (ACID/time travel).
