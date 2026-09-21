# Checklist tự đánh giá — Buổi 8

## Khái niệm

- [ ] Tôi giải thích được vì sao pipeline dữ liệu cần CI/CD (pipeline là code).
- [ ] Tôi phân biệt CI (kiểm tra) và CD (triển khai).
- [ ] Tôi hiểu vì sao cần cả unit test lẫn data test cho pipeline.

## Git flow & test

- [ ] Tôi làm việc trên nhánh feature + PR, giữ `main` luôn xanh.
- [ ] Tôi phân loại được 4 lớp test (unit / logic-data / DAG integrity / data quality).
- [ ] Tôi hiểu test idempotency và vì sao nó là "đặc sản" của DataOps.

## CI

- [ ] Tôi chạy được `make ci` (lint + scan secret + compile DAG + pytest) và hiểu từng bước.
- [ ] Tôi đã **tự kiểm chứng** CI chặn được: lỗi lint, secret hardcode, và test gãy.
- [ ] Tôi biết chạy `make ci` trước khi push.

## CD & rollback

- [ ] Tôi hiểu deploy qua Dev → Staging → Prod để giảm rủi ro.
- [ ] Tôi hiểu GitOps (Git là nguồn sự thật) và rollback bằng `git revert`.
- [ ] Tôi diễn tập được một lần rollback.

## Thực hành

- [ ] Tôi chạy được `pytest` xanh và `make test-dags` (DagBag) không lỗi import.
- [ ] Tôi viết thêm được ít nhất 1 test cho pipeline của mình.

> ≥ 90% → sẵn sàng buổi 9 (Monitoring & Data Quality — thêm tầng data quality test vào CI/pipeline). < 70% → ôn lại mục 3 (test) & 4 (CI).
