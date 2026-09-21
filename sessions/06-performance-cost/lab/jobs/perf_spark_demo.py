"""
perf_spark_demo — Minh họa tối ưu hiệu năng Spark (buổi 6).

Ba phần, mỗi phần in con số / kế hoạch để bạn QUAN SÁT (đo trước, đừng đoán):
  A. SMALL FILES   : ghi nhiều file nhỏ vs gộp lại -> đếm số file.
  B. BROADCAST JOIN: join fact lớn với dim nhỏ; so sánh plan SortMergeJoin vs BroadcastHashJoin.
  C. ĐO THỜI GIAN  : đếm + tổng hợp, in thời gian để tập thói quen "đo before/after".

Chạy local:    make spark-job JOB=perf_spark_demo
Chạy cluster:  make up-cluster && make spark-job-cluster JOB=perf_spark_demo
(JOB cố định, không cần DS.)
"""

from __future__ import annotations

import os
import sys
import time

# Cho phép import common.py nằm ở job buổi 5.
sys.path.insert(0, "/opt/project/sessions/05-pyspark-lakehouse/lab/jobs")
from common import get_spark  # noqa: E402

from pyspark.sql import functions as F  # noqa: E402

TMP = "/opt/data/perf_demo"

def count_files(path: str, suffix: str = ".parquet") -> int:
    total = 0
    for _, _, files in os.walk(path):
        total += sum(1 for f in files if f.endswith(suffix))
    return total


def main() -> None:
    spark = get_spark("perf_spark_demo")

    # Dữ liệu fact lớn (~500k dòng) + dim nhỏ (5 dòng).
    fact = spark.range(0, 500_000).select(
        F.col("id"),
        (F.col("id") % 5).alias("product_id"),
        (F.rand() * 1000).cast("int").alias("amount"),
    )
    dim = spark.createDataFrame(
        [(i, f"product_{i}") for i in range(5)], ["product_id", "product_name"]
    )

    # ---------- A. SMALL FILES ----------
    print("\n===== A. SMALL FILES =====")
    many = f"{TMP}/many_files"
    few = f"{TMP}/few_files"
    # Ghi với 50 partition -> 50 file nhỏ (mô phỏng vấn đề small-files).
    fact.repartition(50).write.mode("overwrite").parquet(many)
    # Ghi gộp còn 2 file.
    fact.coalesce(2).write.mode("overwrite").parquet(few)
    print(f"repartition(50) -> {count_files(many)} file (nhiều file nhỏ -> đọc lại chậm)")
    print(f"coalesce(2)     -> {count_files(few)} file (gộp lại -> đọc nhanh hơn)")

    # ---------- B. BROADCAST JOIN ----------
    print("\n===== B. BROADCAST JOIN (xem physical plan) =====")
    print("--- Không broadcast (có thể là SortMergeJoin + Exchange/shuffle) ---")
    no_bc = fact.join(dim.hint("merge"), "product_id")
    no_bc.explain(mode="formatted")

    print("--- CÓ broadcast dim nhỏ (BroadcastHashJoin -> bỏ shuffle bảng lớn) ---")
    bc = fact.join(F.broadcast(dim), "product_id")
    bc.explain(mode="formatted")

    # ---------- C. ĐO THỜI GIAN ----------
    print("\n===== C. ĐO THỜI GIAN (before/after thói quen) =====")
    t0 = time.time()
    res = bc.groupBy("product_name").agg(F.sum("amount").alias("total")).orderBy("product_name")
    res.show()
    print(f"Tổng hợp với broadcast join mất {time.time() - t0:.2f}s")

    print("\nGợi ý: mở Spark UI (cluster: http://localhost:8085) để xem Stages, shuffle, task lệch.")
    spark.stop()


if __name__ == "__main__":
    main()
