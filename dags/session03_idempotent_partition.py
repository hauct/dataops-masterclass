"""
session03_idempotent_partition — Viết DAG IDEMPOTENT + ATOMIC theo đúng buổi 3.

Đây là DAG "khuôn mẫu" cho cả khóa. Nó minh họa 3 kỹ thuật cốt lõi:
  1. Gắn vào LOGICAL DATE (ds) lấy từ context — KHÔNG dùng datetime.now().
  2. Ghi đè theo PARTITION (xóa thư mục dt=<ds> rồi ghi lại) -> chạy lại không nhân đôi.
  3. ATOMIC: ghi ra file .tmp rồi os.replace -> task chết giữa chừng không để lại dữ liệu nửa vời.

Dữ liệu nguồn được SINH XÁC ĐỊNH (deterministic) theo ds, nên chạy lại cùng một ngày luôn cho cùng kết quả
-> bạn tự kiểm chứng được tính idempotent & reproducible.

Output: /opt/airflow/data/output/orders/dt=<ds>/data.json  (tương ứng repo: data/output/...)
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime

from airflow.sdk import dag, get_current_context, task

log = logging.getLogger(__name__)

OUTPUT_ROOT = "/opt/airflow/data/output/orders"


def _generate_rows(ds: str) -> list[dict]:
    """Sinh dữ liệu giả ĐỊNH NGHĨA THEO ds -> tái lập được (reproducible)."""
    day = int(ds.split("-")[2])          # ngày trong tháng
    n = day + 5                          # số đơn phụ thuộc ngày -> cố định cho mỗi ds
    return [
        {"order_id": f"{ds}-{i:03d}", "order_date": ds, "amount": (i + 1) * 1000 + day}
        for i in range(n)
    ]


@dag(
    dag_id="session03_idempotent_partition",
    schedule="@daily",
    # start_date PHẢI ở quá khứ. Nếu để tương lai, trigger tay sẽ tạo run "success" mà KHÔNG chạy task nào.
    start_date=datetime(2026, 6, 1),
    catchup=False,                       # mặc định an toàn: không tự "bão run" quá khứ
    tags=["buoi-03", "idempotency", "backfill"],
    doc_md=__doc__,
)
def idempotent_partition():
    @task
    def extract() -> int:
        """Đọc 'nguồn' cho đúng ngày logic (ds), trả về SỐ DÒNG (con trỏ nhỏ qua XCom)."""
        ds = get_current_context()["ds"]
        rows = _generate_rows(ds)
        # Ghi staging ra file tạm trước (chưa phải đích cuối).
        os.makedirs("/opt/airflow/data/output/_staging", exist_ok=True)
        staging = f"/opt/airflow/data/output/_staging/orders_{ds}.json"
        with open(staging, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False)
        log.info("EXTRACT ds=%s: sinh %s dòng -> staging %s", ds, len(rows), staging)
        return len(rows)                 # XCom: chỉ truyền METADATA nhỏ, không truyền cả list

    @task
    def load_idempotent(n_rows: int) -> str:
        """Ghi ĐÍCH theo partition dt=<ds>: idempotent (overwrite) + atomic (.tmp -> replace)."""
        ds = get_current_context()["ds"]
        staging = f"/opt/airflow/data/output/_staging/orders_{ds}.json"
        with open(staging, encoding="utf-8") as f:
            rows = json.load(f)

        part_dir = f"{OUTPUT_ROOT}/dt={ds}"
        os.makedirs(part_dir, exist_ok=True)
        dest = f"{part_dir}/data.json"
        tmp = dest + ".tmp"

        # ATOMIC: ghi tmp rồi replace. Nếu chết giữa chừng, dest cũ vẫn nguyên.
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False)
        os.replace(tmp, dest)            # IDEMPOTENT: ghi đè đúng partition của ngày này

        log.info("LOAD ds=%s: ghi %s dòng -> %s (overwrite, atomic)", ds, len(rows), dest)
        return dest                      # XCom: truyền ĐƯỜNG DẪN (con trỏ), không truyền dữ liệu

    @task
    def reconcile(n_rows: int, dest: str) -> None:
        """Đối soát: số dòng đã ghi ở đích phải KHỚP số dòng nguồn (buổi 1)."""
        with open(dest, encoding="utf-8") as f:
            written = len(json.load(f))
        log.info("RECONCILE: nguồn=%s, đích=%s", n_rows, written)
        if written != n_rows:
            raise ValueError(f"❌ Lệch dữ liệu: nguồn {n_rows} != đích {written}")
        log.info("✅ RECONCILE khớp. Chạy lại ngày này bao nhiêu lần kết quả vẫn y hệt (idempotent).")

    n = extract()
    dest = load_idempotent(n)
    reconcile(n, dest)


idempotent_partition()
