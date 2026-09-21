"""
session07_pii_masking — Pipeline che/giấu PII trong DataOps (buổi 7).

Luồng:  create_tables -> load_raw (PII) -> mask -> audit
  - load_raw : nạp dữ liệu THÔ có PII (email, phone) theo ngày ds, idempotent (overwrite partition).
  - mask     : tạo bảng ĐÃ MASKING (che email/phone + hash pseudonym) -> hạ nguồn chỉ dùng bảng này.
  - audit    : ghi 1 dòng audit (ai/khi nào/làm gì) — KHÔNG ghi giá trị PII thật vào log.

Bài học: PII được che NGAY trong pipeline; bản thô tách riêng để hạn chế truy cập (RBAC ở 03_rbac.sql).
Yêu cầu: make up-warehouse. Connection 'warehouse' (credential KHÔNG nằm trong code).
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.sdk import dag, get_current_context, task

log = logging.getLogger(__name__)

CONN_ID = "warehouse"
SQL_DIR = Path("/opt/airflow/project/sessions/07-security-pii/lab/sql")


def _hook() -> PostgresHook:
    return PostgresHook(postgres_conn_id=CONN_ID)


def _generate_pii_rows(ds: str) -> list[tuple]:
    """Sinh khách hàng giả CÓ PII, deterministic theo ds."""
    day = int(ds.split("-")[2])
    n = day + 5
    rows = []
    for i in range(n):
        rows.append(
            (
                ds,                                   # load_date
                f"C{i:04d}",                          # customer_id
                f"Nguyen Van {chr(65 + i % 26)}",     # full_name (PII)
                f"user{i}.{day}@example.com",         # email (PII)
                f"09{day:02d}{i:05d}"[:10],           # phone (PII)
                (i + 1) * 1000 + day,                 # amount
            )
        )
    return rows


@dag(
    dag_id="session07_pii_masking",
    schedule="@daily",
    start_date=datetime(2026, 6, 1),
    catchup=False,
    tags=["buoi-07", "security", "pii"],
    doc_md=__doc__,
)
def pii_masking():
    @task
    def create_tables() -> None:
        _hook().run(SQL_DIR.joinpath("01_ddl.sql").read_text())
        log.info("DDL xong: customers_raw, customers_masked, audit_log.")

    @task
    def load_raw() -> int:
        ds = get_current_context()["ds"]
        rows = _generate_pii_rows(ds)
        conn = _hook().get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM customers_raw WHERE load_date = %s", (ds,))
                cur.executemany(
                    "INSERT INTO customers_raw "
                    "(load_date, customer_id, full_name, email, phone, amount) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    rows,
                )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
        log.info("LOAD raw ds=%s: %s dòng PII (vùng hạn chế).", ds, len(rows))
        return len(rows)

    @task
    def mask() -> None:
        ds = get_current_context()["ds"]
        _hook().run(SQL_DIR.joinpath("02_mask.sql").read_text(), parameters={"ds": ds})
        log.info("MASK ds=%s: tạo bản đã che PII (customers_masked).", ds)

    @task
    def audit() -> None:
        ds = get_current_context()["ds"]
        # Ghi audit — chú ý: KHÔNG ghi giá trị PII, chỉ ghi đối tượng & ngày.
        _hook().run(
            "INSERT INTO audit_log (actor, action, object, detail) VALUES (%s,%s,%s,%s)",
            parameters=("dag:session07_pii_masking", "MASK_PII", "customers_masked", f"ds={ds}"),
        )
        log.info("AUDIT ds=%s: đã ghi vết thao tác masking.", ds)

    t1 = create_tables()
    t2 = load_raw()
    t3 = mask()
    t4 = audit()
    t1 >> t2 >> t3 >> t4


pii_masking()
