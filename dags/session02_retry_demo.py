"""
session02_retry_demo — (tùy chọn) Quan sát cơ chế retry của Airflow.

Task dưới đây cố tình FAIL ở 2 lần chạy đầu, rồi THÀNH CÔNG ở lần thứ 3 — để bạn thấy:
  - Scheduler/Executor tự retry task khi fail (không cần can thiệp tay).
  - Trên UI: task chuyển up_for_retry -> running -> success; xem được từng lần thử (try 1,2,3).

Đây là một biểu hiện của 'reliability' (buổi 1): hệ thống tự hồi phục trước lỗi tạm thời.
Cấu hình retry chi tiết sẽ học ở buổi 3.
"""

from __future__ import annotations

import logging
from datetime import timedelta

from airflow.sdk import dag, get_current_context, task

log = logging.getLogger(__name__)


@dag(
    dag_id="session02_retry_demo",
    schedule=None,
    catchup=False,
    tags=["buoi-02", "demo", "retry"],
    doc_md=__doc__,
)
def retry_demo():
    @task(retries=3, retry_delay=timedelta(seconds=10))
    def flaky() -> str:
        # Lấy context runtime đúng cách trong TaskFlow (Airflow 3): get_current_context().
        # try_number bắt đầu từ 1. Fail nếu là lần thử 1 hoặc 2.
        attempt = get_current_context()["ti"].try_number
        log.info("FLAKY: đây là lần thử (try) số %s", attempt)
        if attempt < 3:
            raise RuntimeError(f"Lỗi tạm thời (giả lập) ở lần thử {attempt} — Airflow sẽ retry.")
        log.info("FLAKY: thành công ở lần thử %s 🎉", attempt)
        return "done"

    flaky()


retry_demo()
