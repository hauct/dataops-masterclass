"""
Unit test cho IDEMPOTENCY của pipeline SQL (buổi 4) — mô phỏng bằng sqlite (pure Python, không cần Postgres).

Kiểm chứng: chạy lại cùng một ngày KHÔNG nhân đôi dữ liệu ở bảng mart (nhờ upsert/partition overwrite).
Đây là "data/logic test" trong CI — chặn regression làm hỏng tính idempotent.
"""

from __future__ import annotations

import sqlite3

import pytest


def _generate_rows(ds: str) -> list[tuple]:
    day = int(ds.split("-")[2])
    n = day + 5
    return [(f"{ds}-{i:03d}", ds, (i + 1) * 1000 + day) for i in range(n)]


def _setup(con: sqlite3.Connection) -> None:
    con.executescript(
        """
        CREATE TABLE stg_orders(order_id TEXT, order_date TEXT, amount INTEGER);
        CREATE TABLE daily_revenue(order_date TEXT PRIMARY KEY, total_amount INTEGER, order_count INTEGER);
        """
    )


def _run_day(con: sqlite3.Connection, ds: str) -> None:
    # load_staging: partition overwrite trong transaction (atomic + idempotent)
    con.execute("BEGIN")
    con.execute("DELETE FROM stg_orders WHERE order_date = ?", (ds,))
    con.executemany("INSERT INTO stg_orders VALUES (?, ?, ?)", _generate_rows(ds))
    con.commit()
    # transform: upsert (ON CONFLICT) — tương đương Postgres
    con.execute(
        """
        INSERT INTO daily_revenue(order_date, total_amount, order_count)
        SELECT order_date, SUM(amount), COUNT(*) FROM stg_orders WHERE order_date = ? GROUP BY order_date
        ON CONFLICT(order_date) DO UPDATE SET
            total_amount = excluded.total_amount, order_count = excluded.order_count
        """,
        (ds,),
    )
    con.commit()


@pytest.fixture()
def con():
    c = sqlite3.connect(":memory:")
    _setup(c)
    yield c
    c.close()


def test_chay_lai_khong_nhan_doi(con):
    ds = "2026-06-20"
    _run_day(con, ds)
    first = con.execute("SELECT total_amount, order_count FROM daily_revenue WHERE order_date=?", (ds,)).fetchone()
    # Chạy lại 2 lần nữa
    _run_day(con, ds)
    _run_day(con, ds)
    rows = con.execute("SELECT COUNT(*) FROM daily_revenue WHERE order_date=?", (ds,)).fetchone()[0]
    after = con.execute("SELECT total_amount, order_count FROM daily_revenue WHERE order_date=?", (ds,)).fetchone()
    assert rows == 1, "mart phải có đúng 1 dòng/ngày (không nhân đôi)"
    assert first == after, "giá trị không đổi sau khi chạy lại (idempotent)"


def test_reconciliation_khop(con):
    ds = "2026-06-21"
    _run_day(con, ds)
    src = con.execute("SELECT COUNT(*), SUM(amount) FROM stg_orders WHERE order_date=?", (ds,)).fetchone()
    dst = con.execute("SELECT order_count, total_amount FROM daily_revenue WHERE order_date=?", (ds,)).fetchone()
    assert src == dst, "nguồn và đích phải khớp (reconciliation)"


def test_data_deterministic():
    # Cùng ds -> cùng dữ liệu nguồn (reproducible).
    assert _generate_rows("2026-06-20") == _generate_rows("2026-06-20")
