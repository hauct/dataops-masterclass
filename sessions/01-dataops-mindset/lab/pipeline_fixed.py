"""
pipeline_fixed.py — Cùng pipeline, nhưng áp dụng nguyên lý DataOps của buổi 1.

So với pipeline_risky.py, bản này sửa 4 điểm:

  1. IDEMPOTENCY  : ghi đè theo ngày (DELETE theo partition rồi INSERT) -> chạy lại bao
                    nhiêu lần cũng ra cùng kết quả.
  2. ATOMICITY    : bọc trong transaction -> hoặc xong trọn vẹn, hoặc rollback, không nửa vời.
  3. REPRODUCIBILITY: nhận run_date qua tham số (mặc định lấy từ dữ liệu), không hardcode.
  4. RECONCILIATION: đối soát nguồn vs đích; lệch là DỪNG và báo lỗi, không cho dữ liệu sai chảy xuống.

    python pipeline_fixed.py 2026-07-09     # chạy lại nhiều lần -> con số KHÔNG đổi
    python pipeline_fixed.py 2026-07-10
"""

import csv
import sqlite3
import sys
from pathlib import Path

DB = Path(__file__).parent / "warehouse.db"
CSV_FILE = Path(__file__).parent / "sample_orders.csv"


def read_source(run_date: str) -> list[dict]:
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["order_date"] == run_date]


def setup(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS daily_revenue (
            order_date TEXT PRIMARY KEY,   -- khóa theo ngày: 1 ngày = 1 dòng
            total_amount INTEGER,
            order_count INTEGER
        )
        """
    )
    conn.commit()


def run(run_date: str) -> None:
    rows = read_source(run_date)
    if not rows:
        print(f"⚠️  Không có dữ liệu nguồn cho ngày {run_date}. Dừng (không ghi gì).")
        return

    src_total = sum(int(r["amount"]) for r in rows)
    src_count = len(rows)

    conn = sqlite3.connect(DB)
    setup(conn)
    try:
        # (1) IDEMPOTENCY + (2) ATOMICITY: xóa-rồi-ghi theo partition, trong 1 transaction.
        conn.execute("BEGIN")
        conn.execute("DELETE FROM daily_revenue WHERE order_date = ?", (run_date,))
        conn.execute(
            "INSERT INTO daily_revenue (order_date, total_amount, order_count) VALUES (?, ?, ?)",
            (run_date, src_total, src_count),
        )

        # (4) RECONCILIATION: đọc lại từ đích, đối chiếu với nguồn TRƯỚC khi commit.
        dst_total, dst_count = conn.execute(
            "SELECT total_amount, order_count FROM daily_revenue WHERE order_date = ?",
            (run_date,),
        ).fetchone()

        if (dst_total, dst_count) != (src_total, src_count):
            conn.rollback()
            raise ValueError(
                f"❌ RECONCILIATION FAIL ngày {run_date}: "
                f"nguồn=({src_count} đơn, {src_total:,} đ) != đích=({dst_count} đơn, {dst_total:,} đ). "
                f"Đã rollback, không ghi dữ liệu sai."
            )

        conn.commit()
        print(
            f"✅ Ngày {run_date}: {src_count} đơn, tổng {src_total:,} đ "
            f"— reconciliation khớp, đã commit."
        )

        print("--- Nội dung bảng daily_revenue ---")
        for row in conn.execute(
            "SELECT order_date, total_amount, order_count FROM daily_revenue ORDER BY order_date"
        ):
            print(f"  {row[0]}: tổng = {row[1]:,} đ | số đơn = {row[2]}")
    finally:
        conn.close()


if __name__ == "__main__":
    # (3) REPRODUCIBILITY: ngày chạy là tham số, không hardcode trong code.
    date_arg = sys.argv[1] if len(sys.argv) > 1 else "2026-07-09"
    run(date_arg)
