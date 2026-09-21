"""
session02_architecture_demo — DAG đầu tiên để QUAN SÁT kiến trúc Airflow.

Mục tiêu buổi 2 KHÔNG phải dạy viết DAG (đó là buổi 3), mà để bạn:
  - Thấy DAG Processor "bắt" được file này và hiện trong UI.
  - Thấy Scheduler lên lịch & Worker chạy từng task.
  - Quan sát quan hệ phụ thuộc (dependency) và việc 2 task chạy SONG SONG.
  - Đọc log của từng task.

Dùng TaskFlow API của Airflow 3 (`airflow.sdk`) — cú pháp hiện đại, sẽ học kỹ ở buổi 3.

Hình dạng DAG:

        extract ─┐
                 ├─> load ─> report
        validate ┘

(extract & validate không phụ thuộc nhau -> chạy song song; load chờ cả hai xong.)
"""

from __future__ import annotations

import logging
import time

from airflow.sdk import dag, task

log = logging.getLogger(__name__)


@dag(
    dag_id="session02_architecture_demo",
    schedule=None,              # chạy tay (trigger thủ công) — Airflow 3 dùng `schedule=`
    catchup=False,
    tags=["buoi-02", "demo", "kien-truc"],
    doc_md=__doc__,             # hiện chính docstring này trong tab "Docs" của DAG
)
def architecture_demo():
    @task
    def extract() -> int:
        log.info("EXTRACT: đang 'đọc' dữ liệu nguồn... (giả lập)")
        time.sleep(3)  # giả lập việc mất thời gian -> dễ quan sát trạng thái running
        n_rows = 10
        log.info("EXTRACT: đọc được %s dòng.", n_rows)
        return n_rows  # giá trị này đi qua XCom (metadata nhỏ) — học kỹ ở buổi 3

    @task
    def validate() -> bool:
        log.info("VALIDATE: kiểm tra sơ bộ dữ liệu nguồn... (giả lập)")
        time.sleep(3)
        log.info("VALIDATE: OK. (Buổi 9 sẽ thay bằng Great Expectations thật.)")
        return True

    @task
    def load(n_rows: int, ok: bool) -> None:
        log.info("LOAD: nhận n_rows=%s, validate_ok=%s", n_rows, ok)
        if not ok:
            raise ValueError("Dữ liệu không hợp lệ — dừng để không ghi dữ liệu xấu.")
        log.info("LOAD: đã 'ghi' %s dòng vào đích. (idempotent — học ở buổi 3,4)", n_rows)

    @task
    def report(n_rows: int) -> None:
        log.info("REPORT: pipeline xong. Tổng %s dòng được xử lý.", n_rows)

    # Khai báo dependency: load phụ thuộc extract + validate; report phụ thuộc load.
    n = extract()
    ok = validate()
    loaded = load(n, ok)
    report(n) << loaded   # report chạy sau khi load xong


architecture_demo()
