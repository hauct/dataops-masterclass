"""Tiện ích dùng chung cho các Spark job buổi 5."""

from __future__ import annotations

import os

from pyspark.sql import SparkSession

# Mặc định ghi Delta ra filesystem local (mount từ repo: data/lakehouse) -> chạy chắc chắn, không cần S3A.
# Muốn dùng MinIO (object storage thật), đặt biến môi trường LAKE_BASE=s3a://lakehouse và xem README.
LAKE_BASE = os.environ.get("LAKE_BASE", "/opt/data/lakehouse")
ORDERS_PATH = f"{LAKE_BASE}/orders"


def get_spark(app_name: str = "dataops-lakehouse") -> SparkSession:
    """Tạo SparkSession có Delta. Nếu LAKE_BASE là s3a://, cấu hình thêm cho MinIO."""
    builder = (
        SparkSession.builder.appName(app_name)
        # Delta extension (cũng được truyền qua spark-submit --conf, để đây cho chắc)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
    )

    if LAKE_BASE.startswith("s3a://"):
        # Cấu hình S3A trỏ tới MinIO (chỉ dùng khi bạn chọn object storage thật).
        endpoint = os.environ.get("MINIO_ENDPOINT", "http://minio:9000")
        builder = (
            builder.config("spark.hadoop.fs.s3a.endpoint", endpoint)
            .config("spark.hadoop.fs.s3a.access.key", os.environ.get("MINIO_ROOT_USER", "minioadmin"))
            .config("spark.hadoop.fs.s3a.secret.key", os.environ.get("MINIO_ROOT_PASSWORD", "minioadmin"))
            .config("spark.hadoop.fs.s3a.path.style.access", "true")
            .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
            .config(
                "spark.hadoop.fs.s3a.aws.credentials.provider",
                "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
            )
        )

    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark


def generate_rows(ds: str) -> list[tuple]:
    """Sinh giao dịch giả ĐỊNH NGHĨA THEO ds -> tái lập được (giống buổi 3, 4)."""
    day = int(ds.split("-")[2])
    n = day + 5
    return [
        (f"{ds}-{i:03d}", ds, f"user{i}@example.com", (i + 1) * 1000 + day)
        for i in range(n)
    ]


ORDERS_SCHEMA = ["order_id", "order_date", "customer_email", "amount"]
