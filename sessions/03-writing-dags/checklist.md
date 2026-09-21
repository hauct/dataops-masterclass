# Checklist tự đánh giá — Buổi 3

## Viết DAG

- [ ] Tôi viết được một DAG TaskFlow (`@dag` + `@task`) và hiểu dependency suy ra từ truyền giá trị.
- [ ] Tôi biết khi nào dùng TaskFlow, khi nào dùng Operator có sẵn (SQL/Bash/Sensor).

## Idempotency & atomicity (cốt lõi)

- [ ] Tôi giải thích được vì sao phải dùng `ds`/`data_interval_start` thay cho `datetime.now()`.
- [ ] Tôi viết được task ghi đè theo partition (overwrite) thay vì append mù.
- [ ] Tôi áp dụng được mẫu atomic "ghi .tmp → os.replace".
- [ ] Tôi đã **tự kiểm chứng**: chạy lại cùng một ngày, output không nhân đôi.

## Scheduling & backfill

- [ ] Tôi phân biệt `schedule`, `start_date`, `catchup`; biết vì sao nên `catchup=False` mặc định.
- [ ] Tôi chạy được backfill và hiểu vì sao nó chỉ an toàn khi task idempotent.

## Retry / timeout / SLA / alert

- [ ] Tôi cấu hình được `retries`, `retry_delay`, `execution_timeout`.
- [ ] Tôi phân biệt được khi nào retry hữu ích (lỗi tạm thời) vs vô nghĩa (lỗi logic).

## XCom / Variable / Connection / Pool / Sensor

- [ ] Tôi hiểu XCom chỉ để truyền *metadata nhỏ* và biết quy tắc "truyền con trỏ, không truyền hàng hóa".
- [ ] Tôi dùng được `Variable.get(..., default=...)`.
- [ ] Tôi biết Connection/Pool/Sensor để làm gì (dù chưa dùng sâu).

## Assets

- [ ] Tôi hiểu ý tưởng data-aware scheduling (Asset) và vì sao nó tốt hơn lịch cứng trong một số tình huống.

## Thực hành

- [ ] Tôi chạy được cả `session03_idempotent_partition` và `session03_concepts_demo`.
- [ ] Tôi đã tự viết & chạy DAG `*_daily_kpi` idempotent ở Phần 3 lab.

> ≥ 90% → vững nền để bước vào buổi 4 (SQL/DWH). < 70% → ôn lại mục 2 (idempotency) & 3 (scheduling).
