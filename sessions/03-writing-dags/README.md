# Buổi 3 — Viết DAG & các khái niệm nâng cao

> 🚧 **Đang biên soạn đầy đủ.** File này hiện là outline. Bài giảng chi tiết + lab + bài tập sẽ được bổ sung.

**Ngày:** 16/07  ·  **Bật stack:** `make up`

## Nội dung

- DAG, Task, Operator & TaskFlow API — viết DAG đúng chuẩn
- Idempotency & atomicity — vì sao cực kỳ quan trọng
- Scheduling: cron, schedule, catchup; backfill an toàn
- Retry, timeout, SLA/Deadline, alert; dependency giữa Task & giữa DAG
- XCom, Pool, Connection, Variable, Sensor
- Giới thiệu Assets (data-aware scheduling)

## Thực hành

- Viết & chạy DAG đúng chuẩn vận hành
- Backfill an toàn — chạy lại không nhân đôi dữ liệu
- Cấu hình retry/alert & dependency giữa các DAG

## Tài liệu trong buổi

- `README.md` — bài giảng (đang biên soạn)
- `lab/` — code thực hành (đang biên soạn)
- `exercises.md` · `checklist.md` (đang biên soạn)
