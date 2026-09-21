"""
session03_concepts_demo — Tổng hợp các khái niệm nâng cao của buổi 3 trong 1 DAG.

Minh họa:
  - RETRY + RETRY_DELAY + EXECUTION_TIMEOUT trên một task "chập chờn".
  - XCom đúng cách: truyền CON TRỎ (đường dẫn) thay vì khối dữ liệu.
  - VARIABLE: đọc cấu hình toàn cục có giá trị mặc định.
  - DEPENDENCY rẽ nhánh: extract -> [transform_a, transform_b] -> combine (a,b chạy song song).

Hình dạng DAG:

        ┌─ transform_a ─┐
extract ┤               ├─ combine
        └─ transform_b ─┘
"""

from __future__ import annotations

import json
import logging
import os
from datetime import timedelta

from airflow.sdk import Variable, dag, get_current_context, task

log = logging.getLogger(__name__)


@dag(
    dag_id="session03_concepts_demo",
    schedule=None,                       # chạy tay
    catchup=False,
    tags=["buoi-03", "retry", "xcom", "variable"],
    doc_md=__doc__,
)
def concepts_demo():
    @task(
        retries=2,
        retry_delay=timedelta(seconds=10),
        execution_timeout=timedelta(minutes=5),
    )
    def extract() -> str:
        """Sinh dữ liệu, ghi ra file, trả về ĐƯỜNG DẪN (không trả cả list qua XCom)."""
        ctx = get_current_context()
        run_id = ctx["run_id"].replace(":", "-").replace("+", "-")
        # Đọc ngưỡng từ Variable (có default -> không lỗi nếu chưa tạo Variable trên UI).
        n = int(Variable.get("demo_num_rows", default="8"))
        rows = [{"id": i, "amount": (i + 1) * 100} for i in range(n)]

        os.makedirs("/opt/airflow/data/output/_demo", exist_ok=True)
        path = f"/opt/airflow/data/output/_demo/extract_{run_id}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(rows, f)
        log.info("EXTRACT: ghi %s dòng -> %s (XCom chỉ trả path này)", n, path)
        return path

    @task
    def transform_a(path: str) -> float:
        with open(path, encoding="utf-8") as f:
            rows = json.load(f)
        total = sum(r["amount"] for r in rows)
        log.info("TRANSFORM_A: tổng amount = %s", total)
        return float(total)

    @task
    def transform_b(path: str) -> int:
        with open(path, encoding="utf-8") as f:
            rows = json.load(f)
        log.info("TRANSFORM_B: số dòng = %s", len(rows))
        return len(rows)

    @task
    def combine(total: float, count: int) -> None:
        avg = total / count if count else 0
        log.info("COMBINE: tổng=%s, số dòng=%s, trung bình=%.1f", total, count, avg)

    path = extract()
    # transform_a & transform_b cùng phụ thuộc extract -> chạy SONG SONG; combine chờ cả hai.
    combine(transform_a(path), transform_b(path))


concepts_demo()
