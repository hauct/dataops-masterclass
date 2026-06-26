# Airflow 3 image cho khóa học. Pin version để mọi học viên chạy giống nhau (reproducibility).
FROM apache/airflow:3.0.6

# Cài thêm thư viện dùng xuyên suốt khóa (data quality, postgres, s3/minio...).
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
