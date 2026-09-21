"""
session04_sql_dwh — Pipeline SQL reliable trên stack Data Warehouse (Postgres).

Điều phối 4 bước SQL idempotent, đúng tinh thần buổi 1 & 3 nhưng bằng SQL:
  create_tables -> load_staging -> transform_upsert -> reconcile

  - create_tables   : DDL idempotent (CREATE IF NOT EXISTS).
  - load_staging    : partition overwrite trong 1 transaction (DELETE WHERE date=ds; INSERT) -> atomic + idempotent.
  - transform_upsert: tổng hợp staging -> mart bằng UPSERT (ON CONFLICT) -> chạy lại không nhân đôi.
  - reconcile       : đối soát nguồn (staging) vs đích (mart); lệch là raise -> chặn dữ liệu sai.

Yêu cầu: bật stack warehouse -> `make up-warehouse`. Connection 'warehouse' đã cấu hình sẵn qua env.
File SQL: sessions/04-sql-dwh/lab/sql/  (mount tại /opt/airflow/project/sessions/...).
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sdk import dag, get_current_context, task

log = logging.getLogger(__name__)

CONN_ID = "warehouse"
SQL_DIR = Path("/opt/airflow/project/sessions/04-sql-dwh/lab/sql")


def _hook() -> PostgresHook:
    return PostgresHook(postgres_conn_id=CONN_ID)


def _generate_rows(ds: str) -> list[tuple]:
    """Sinh giao dịch giả ĐỊNH NGHĨA THEO ds -> tái lập được (giống buổi 3)."""
    day = int(ds.split("-")[2])
    n = day + 5
    return [
        (f"{ds}-{i:03d}", ds, f"user{i}@example.com", (i + 1) * 1000 + day)
        for i in range(n)
    ]


@dag(
    dag_id="session04_sql_dwh",
    schedule="@daily",
    start_date=datetime(2026, 6, 1),   # quá khứ -> trigger tay & backfill chạy được
    catchup=False,
    tags=["buoi-04", "sql", "dwh", "idempotency"],
    doc_md=__doc__,
)
def sql_dwh():
    @task
    def create_tables() -> None:
        _hook().run(SQL_DIR.joinpath("01_ddl.sql").read_text())
        log.info("DDL xong: stg_orders, daily_revenue sẵn sàng.")

    @task
    def load_staging() -> int:
        """Partition overwrite trong 1 transaction: atomic + idempotent."""
        ds = get_current_context()["ds"]
        rows = _generate_rows(ds)
        conn = _hook().get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM stg_orders WHERE order_date = %s", (ds,))
                cur.executemany(
                    "INSERT INTO stg_orders (order_id, order_date, customer_email, amount) "
                    "VALUES (%s, %s, %s, %s)",
                    rows,
                )
            conn.commit()   # cả DELETE + INSERT cùng commit; lỗi giữa chừng -> rollback
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
        log.info("LOAD staging ds=%s: ghi đè %s dòng (idempotent).", ds, len(rows))
        return len(rows)

    @task
    def transform_upsert() -> None:
        ds = get_current_context()["ds"]
        sql = SQL_DIR.joinpath("02_transform_upsert.sql").read_text()
        _hook().run(sql, parameters={"ds": ds})
        log.info("TRANSFORM ds=%s: upsert vào daily_revenue (idempotent).", ds)

    @task
    def reconcile() -> None:
        ds = get_current_context()["ds"]
        sql = SQL_DIR.joinpath("04_reconcile.sql").read_text()
        row = _hook().get_first(sql, parameters={"ds": ds})
        src_cnt, dst_cnt, src_total, dst_total, is_match = row
        log.info(
            "RECONCILE ds=%s: nguồn=(%s đơn, %s đ) đích=(%s đơn, %s đ)",
            ds, src_cnt, src_total, dst_cnt, dst_total,
        )
        if not is_match:
            raise ValueError(
                f"❌ RECONCILIATION FAIL ds={ds}: nguồn≠đích. "
                f"Dừng pipeline để không đưa số liệu sai vào báo cáo."
            )
        log.info("✅ RECONCILE khớp. Chạy lại ngày này kết quả vẫn y hệt (idempotent).")

    t1 = create_tables()
    t2 = load_staging()
    t3 = transform_upsert()
    t4 = reconcile()
    t1 >> t2 >> t3 >> t4


sql_dwh()
