"""
pipeline_risky.py — Pipeline "đời thực nhưng nguy hiểm".

Đây là kiểu pipeline mà rất nhiều Data Engineer viết khi mới vào nghề: nó CHẠY ĐƯỢC và
RA SỐ. Nhưng nó vi phạm gần hết các nguyên lý DataOps ở buổi 1.

Mục tiêu lab: chạy file này 2 lần và TỰ TAY chứng kiến dữ liệu bị nhân đôi
(double-counting) — lỗi kinh điển do thiếu idempotency.

Chỉ dùng thư viện chuẩn của Python (sqlite3, csv) -> chạy được ngay, không cần Docker.

    python pipeline_risky.py            # nạp doanh thu cho ngày 2026-07-09
    python pipeline_risky.py            # chạy LẠI lần nữa -> xem điều gì xảy ra 😱
"""

import csv
import sqlite3
from pathlib import Path

DB = Path(__file__).parent / "warehouse.db"
CSV_FILE = Path(__file__).parent / "sample_orders.csv"
RUN_DATE = "2026-07-09"  # ❌ hardcode "ngày chạy" — vi phạm reproducibility


def setup(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS daily_revenue (
            order_date TEXT,
            total_amount INTEGER,
            order_count INTEGER
        )
        """
    )
    conn.commit()


def run() -> None:
    conn = sqlite3.connect(DB)
    setup(conn)

    # Đọc nguồn, lọc theo ngày
    rows = []
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["order_date"] == RUN_DATE:
                rows.append(r)

    total = sum(int(r["amount"]) for r in rows)
    count = len(rows)

    # ❌ VẤN ĐỀ CỐT LÕI: INSERT thuần, không hề xóa/ghi đè dữ liệu cũ của ngày này.
    #    Chạy lại lần 2 -> thêm một dòng nữa -> doanh thu ngày 09/07 bị tính 2 lần.
    conn.execute(
        "INSERT INTO daily_revenue (order_date, total_amount, order_count) VALUES (?, ?, ?)",
        (RUN_DATE, total, count),
    )
    conn.commit()

    # In ra trạng thái hiện tại của bảng đích
    print(f"Đã nạp ngày {RUN_DATE}: {count} đơn, tổng {total:,} đ")
    print("--- Nội dung bảng daily_revenue ---")
    for row in conn.execute(
        "SELECT order_date, SUM(total_amount), SUM(order_count) "
        "FROM daily_revenue GROUP BY order_date"
    ):
        print(f"  {row[0]}: tổng = {row[1]:,} đ | số đơn = {row[2]}")
    print("(Chạy lại file này thêm lần nữa và so sánh con số!)")

    conn.close()


if __name__ == "__main__":
    run()
