"""
time_travel_demo — Minh họa TIME TRAVEL & lịch sử phiên bản của Delta (buổi 5).

Table format (Delta) lưu lịch sử mọi lần ghi -> bạn đọc lại được dữ liệu ở phiên bản/thời điểm cũ.
Đây là một "lưới an toàn" cho vận hành: lỡ ghi sai vẫn xem/khôi phục được dữ liệu trước đó.

Chạy SAU khi đã có ít nhất 2 lần ghi (vd chạy orders_delta_job 2 ngày khác nhau):
  make spark-job JOB=time_travel_demo
"""

from __future__ import annotations

from common import ORDERS_PATH, get_spark
from delta.tables import DeltaTable


def main() -> None:
    spark = get_spark("time_travel_demo")

    # 1) Lịch sử các phiên bản (ai ghi, lúc nào, thao tác gì).
    print("[HISTORY] lịch sử các lần ghi bảng:")
    dt = DeltaTable.forPath(spark, ORDERS_PATH)
    dt.history().select("version", "timestamp", "operation", "operationParameters").show(
        truncate=False
    )

    # 2) Đọc phiên bản ĐẦU TIÊN (version 0) so với mới nhất.
    v0 = spark.read.format("delta").option("versionAsOf", 0).load(ORDERS_PATH)
    latest = spark.read.format("delta").load(ORDERS_PATH)
    print(f"[TIME TRAVEL] version 0: {v0.count()} dòng  |  mới nhất: {latest.count()} dòng")

    print("[TIME TRAVEL] số dòng mỗi ngày ở version 0:")
    v0.groupBy("order_date").count().orderBy("order_date").show()

    spark.stop()


if __name__ == "__main__":
    main()
