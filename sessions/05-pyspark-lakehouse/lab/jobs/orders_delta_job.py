"""
orders_delta_job — PySpark job IDEMPOTENT & RETRY-SAFE ghi Delta Lake (buổi 5).

Áp dụng nguyên lý buổi 1 vào stack Lakehouse:
  - IDEMPOTENT: ghi đè đúng partition của ngày bằng Delta `replaceWhere` -> chạy lại không nhân đôi.
  - ATOMIC: Delta là table format ACID -> mỗi lần ghi là một transaction; fail giữa chừng không để dữ liệu nửa vời.
  - RECONCILIATION: đọc lại từ Delta, đối soát số dòng nguồn vs đích.

Chạy:  make spark-job JOB=orders_delta_job DS=2026-06-20
Hoặc:  docker compose exec spark /opt/spark/bin/spark-submit --packages io.delta:delta-spark_2.12:3.2.0 \
          --conf spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension \
          --conf spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog \
          /opt/project/sessions/05-pyspark-lakehouse/lab/jobs/orders_delta_job.py 2026-06-20
"""

from __future__ import annotations

import sys

from common import ORDERS_PATH, ORDERS_SCHEMA, generate_rows, get_spark


def main(ds: str) -> None:
    spark = get_spark("orders_delta_job")

    # 1) Đọc 'nguồn' cho đúng ngày logic ds (deterministic).
    rows = generate_rows(ds)
    src_count = len(rows)
    df = spark.createDataFrame(rows, schema=ORDERS_SCHEMA)

    # 2) Ghi Delta IDEMPOTENT: overwrite CHỈ partition order_date = ds (replaceWhere).
    #    Lần đầu chưa có bảng -> tự tạo. Chạy lại cùng ngày -> thay thế đúng partition đó.
    (
        df.write.format("delta")
        .mode("overwrite")
        .option("replaceWhere", f"order_date = '{ds}'")
        .partitionBy("order_date")
        .save(ORDERS_PATH)
    )
    print(f"[LOAD] ds={ds}: ghi {src_count} dòng vào {ORDERS_PATH} (replaceWhere, ACID).")

    # 3) RECONCILIATION: đọc lại từ Delta, đối soát.
    dst_count = spark.read.format("delta").load(ORDERS_PATH).where(f"order_date = '{ds}'").count()
    print(f"[RECONCILE] ds={ds}: nguồn={src_count}, đích={dst_count}")
    if dst_count != src_count:
        raise SystemExit(f"❌ RECONCILE FAIL: nguồn {src_count} != đích {dst_count}")
    print("✅ RECONCILE khớp. Chạy lại ngày này kết quả không đổi (idempotent).")

    # Tổng quan toàn bảng (các partition đang có).
    print("[TABLE] số dòng mỗi ngày:")
    spark.read.format("delta").load(ORDERS_PATH).groupBy("order_date").count().orderBy("order_date").show()

    spark.stop()


if __name__ == "__main__":
    ds_arg = sys.argv[1] if len(sys.argv) > 1 else "2026-06-20"
    main(ds_arg)
