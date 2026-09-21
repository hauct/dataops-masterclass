# Buổi 3 — Viết DAG & các khái niệm nâng cao

**Ngày 16/07 · 20h–22h · Bật stack: `make up`**

> Đây là buổi **bản lề** của khóa. Buổi 1 cho nguyên lý, buổi 2 cho kiến trúc — buổi 3 dạy bạn *viết DAG
> đúng chuẩn vận hành*: idempotent, an toàn khi chạy lại & backfill, có retry/alert. Mọi pipeline ở các
> buổi sau (SQL, Spark, CI/CD) đều dựa trên những gì học hôm nay.

## Mục tiêu buổi học

- Viết DAG bằng **TaskFlow API** (Airflow 3) đúng chuẩn, hiểu DAG / Task / Operator.
- Hiểu & áp dụng **idempotency + atomicity** *ngay trong cách viết task* (không chỉ ở SQL).
- Nắm **scheduling**: cron vs preset, `logical date` vs `now()`, `catchup`, và **backfill an toàn**.
- Cấu hình **retry, timeout, SLA/Deadline, alert** đúng cách.
- Khai báo **dependency** giữa task & giữa DAG.
- Biết dùng **XCom, Variable, Connection, Pool, Sensor** — và giới hạn của chúng.
- Làm quen **Assets** (data-aware scheduling) — cách hiện đại thay cho lịch cứng.

---

## 1. DAG, Task, Operator & hai phong cách viết

- **DAG**: cả workflow. Khai báo bằng `@dag` (TaskFlow) hoặc `with DAG(...) as dag:` (classic).
- **Task**: một mắt xích. Bằng `@task` (TaskFlow) hoặc khởi tạo một Operator (classic).
- **Operator**: "khuôn" cho một loại việc: `PythonOperator`, `BashOperator`, `SQLExecuteQueryOperator`,
  sensor... TaskFlow thực chất sinh ra `PythonOperator` ở bên dưới.

### TaskFlow API (khuyến nghị cho khóa này)

```python
from airflow.sdk import dag, task

@dag(schedule="@daily", start_date=..., catchup=False, tags=["..."])
def my_pipeline():
    @task
    def extract() -> list[dict]:
        return [{"id": 1, "amount": 100}]

    @task
    def load(rows: list[dict]) -> None:
        print(f"ghi {len(rows)} dòng")

    load(extract())   # giá trị trả về tự đi qua XCom; dependency tự suy ra

my_pipeline()
```

TaskFlow gọn, dependency suy ra **tự động** từ việc truyền giá trị, và truyền dữ liệu nhỏ qua XCom trông
như gọi hàm Python bình thường. Classic vẫn cần khi dùng operator có sẵn (vd: chạy SQL, gọi Bash, sensor).

> **Quy tắc:** dùng **TaskFlow** cho logic Python; dùng **Operator có sẵn** khi điều phối hệ khác (SQL,
> Spark-submit, S3...). Trộn được trong cùng một DAG.

---

## 2. Idempotency & Atomicity — viết task để chạy lại an toàn

Nhắc lại buổi 1: pipeline production **sẽ** chạy lại (retry, backfill, chạy tay). Cách *viết task* phải đảm
bảo chạy lại không hỏng dữ liệu. Ba kỹ thuật cốt lõi:

### 2.1. Gắn mọi thứ vào "logical date", KHÔNG dùng `now()`

Airflow chạy mỗi DAG run cho một **khoảng thời gian logic** (data interval). Hãy xử lý dữ liệu *của khoảng
đó*, lấy từ context — đừng bao giờ dùng `datetime.now()`.

```python
from airflow.sdk import get_current_context

@task
def process():
    ctx = get_current_context()
    ds = ctx["ds"]                      # 'YYYY-MM-DD' của run hiện tại (logical date)
    start = ctx["data_interval_start"]  # mốc đầu khoảng dữ liệu
    # -> xử lý đúng dữ liệu của ngày `ds`; chạy lại ngày đó luôn cho cùng kết quả (reproducible)
```

Vì sao quan trọng: dùng `now()` thì backfill ngày 01/07 hôm nay sẽ lấy dữ liệu *hôm nay* — sai hoàn toàn.
Dùng `ds` thì backfill bao nhiêu lần cũng đúng dữ liệu ngày đó.

### 2.2. Ghi đè theo partition (delete-then-write / overwrite), không append mù

```python
# ✅ idempotent: xóa partition của ngày rồi ghi lại
output = f"/opt/airflow/data/output/dt={ds}/data.parquet"
overwrite_partition(output, rows)   # chạy lại ngày `ds` -> thay thế, không nhân đôi
```

(Ở buổi 4 là `DELETE … WHERE dt=ds; INSERT …` hoặc `MERGE`; buổi 5 là Delta `replaceWhere`.)

### 2.3. Atomicity: ghi tạm rồi swap

Đừng ghi trực tiếp vào đích. Ghi ra file/thư mục **tạm**, xong xuôi mới **đổi tên (rename)** vào vị trí
cuối. Nếu task chết giữa chừng, đích vẫn nguyên vẹn — không có dữ liệu nửa vời.

```python
tmp = dest + ".tmp"
write(tmp, data)      # nếu chết ở đây, dest chưa bị đụng tới
os.replace(tmp, dest) # rename là thao tác gần như nguyên tử trên cùng filesystem
```

> Lab buổi 3 sẽ cho bạn viết một DAG idempotent + atomic theo đúng 3 kỹ thuật này và *tự kiểm chứng* bằng
> cách chạy lại nhiều lần.

---

## 3. Scheduling, catchup & backfill

### 3.1. Khai báo lịch

```python
@dag(schedule="@daily", start_date=datetime(2026, 7, 1), catchup=False)
```

- `schedule`: có thể là preset (`@daily`, `@hourly`), cron (`"0 6 * * *"`), `None` (chạy tay), hoặc
  `timedelta`, hoặc **Asset** (mục 7). *(Airflow 3 dùng `schedule=`, bỏ `schedule_interval`.)*
- `start_date`: mốc bắt đầu *logic* — Airflow sinh run cho từng khoảng kể từ đây.
- `catchup`:
  - `False` (khuyến nghị mặc định): chỉ chạy từ hiện tại, **không** tự chạy bù quá khứ.
  - `True`: tự sinh & chạy mọi khoảng đã lỡ từ `start_date` → nay. Mạnh nhưng dễ "bão run" nếu start_date xa.

> **Bẫy kinh điển:** đặt `start_date` xa trong quá khứ + `catchup=True` → Airflow lập tức tạo hàng trăm
> run. Mặc định nên `catchup=False`, rồi backfill có chủ đích khi cần.

### 3.2. Backfill an toàn

**Backfill** = chạy lại pipeline cho khoảng thời gian quá khứ (vd: phát hiện logic sai, cần nạp lại 30 ngày).
Backfill chỉ *an toàn* khi task **idempotent** (mục 2). Airflow 3 có backfill do scheduler quản lý, trigger
được từ UI/CLI:

```bash
# chạy lại từ 01/07 đến 07/07 (trong container scheduler)
airflow backfill create --dag-id my_pipeline --from-date 2026-07-01 --to-date 2026-07-07
```

Nếu task idempotent: backfill cho cùng khoảng nhiều lần vẫn ra cùng kết quả. Nếu không: nhân đôi/hỏng dữ liệu.

---

## 4. Retry, timeout, SLA & alert

Đây là "lớp tự vệ" giúp pipeline reliable trước lỗi tạm thời và phát hiện chậm trễ.

```python
from datetime import timedelta

@task(
    retries=3,                          # thử lại 3 lần khi fail
    retry_delay=timedelta(minutes=2),   # chờ giữa các lần
    retry_exponential_backoff=True,     # giãn dần thời gian chờ
    execution_timeout=timedelta(minutes=30),  # quá thì kill (tránh treo vô hạn)
)
def call_flaky_api():
    ...
```

| Cơ chế | Dùng để | Lưu ý |
|--------|---------|-------|
| `retries` + `retry_delay` | Vượt qua lỗi *tạm thời* (mạng, API chập chờn) | Chỉ hữu ích khi task idempotent; đừng retry lỗi logic |
| `execution_timeout` | Chặn task treo vô hạn chiếm tài nguyên | Đặt hợp lý theo thời gian chạy thật |
| **SLA / Deadline** | Cảnh báo khi task/DAG chạy *chậm hơn cam kết* | Liên quan SLO/SLI (buổi 9) |
| `on_failure_callback` | Bắn alert (email/Slack) khi fail | Cấu hình kênh alert ở buổi 9 |

> **Triết lý:** retry để *tự hồi phục* trước lỗi tạm thời; alert để *con người biết* khi tự hồi phục không
> thành. Cả hai phục vụ reliability (buổi 1).

---

## 5. Dependency giữa task & giữa DAG

```python
# Trong 1 DAG — TaskFlow tự suy từ truyền giá trị:
loaded = load(extract())
report(loaded)

# Hoặc khai báo tường minh:
a >> [b, c] >> d        # a xong -> b & c song song -> d

# Giữa các DAG:
# - Asset (khuyến nghị, mục 7): DAG B chạy khi asset do DAG A tạo được cập nhật.
# - TriggerDagRunOperator: DAG A chủ động trigger DAG B.
# - (ExternalTaskSensor: chờ task của DAG khác — dùng dè dặt, dễ gây kẹt.)
```

---

## 6. XCom, Variable, Connection, Pool, Sensor

| Thành phần | Là gì | Khi nào dùng | Cảnh báo |
|-----------|-------|--------------|----------|
| **XCom** | Truyền *metadata nhỏ* giữa task | Đường dẫn file, số dòng, cờ trạng thái | **KHÔNG** truyền DataFrame/khối dữ liệu lớn — truyền *vị trí* dữ liệu thay vì dữ liệu |
| **Variable** | Cấu hình toàn cục (key-value) | Tham số môi trường, ngưỡng | Không để secret trần ở đây (buổi 7) |
| **Connection** | Thông tin kết nối hệ ngoài (DB, S3...) | Postgres, MinIO, API | Lưu credential — quản lý như secret (buổi 7) |
| **Pool** | Giới hạn số task song song dùng chung tài nguyên | Tránh quá tải DB nguồn | Đặt theo sức chịu của hệ phụ thuộc |
| **Sensor** | Task *chờ* một điều kiện (file tới, partition sẵn sàng) | Chờ dữ liệu nguồn | Dùng `mode="reschedule"` hoặc **deferrable** để không chiếm slot |

```python
from airflow.sdk import Variable
threshold = int(Variable.get("revenue_alert_threshold", default=1_000_000))
```

> **XCom — lỗi người mới hay mắc:** nhồi cả bảng dữ liệu vào XCom. XCom lưu trong metadata DB → phình DB,
> chậm, dễ vỡ. Quy tắc: *truyền con trỏ, không truyền hàng hóa* (path tới file trên storage, không phải file).

---

## 7. Assets — data-aware scheduling (điểm hiện đại của Airflow 3)

Thay vì "chạy lúc 6h sáng và *hy vọng* dữ liệu đã sẵn", Airflow 3 cho phép DAG chạy **khi dữ liệu thực sự
sẵn sàng** — gọi là *asset* (trước đây là "Dataset").

```python
from airflow.sdk import Asset, dag, task

orders = Asset("s3://lake/orders")

# DAG sản xuất: khi task này xong, asset `orders` được coi là cập nhật
@dag(schedule="@daily", ...)
def producer():
    @task(outlets=[orders])
    def make_orders(): ...

# DAG tiêu thụ: tự chạy MỖI KHI `orders` được cập nhật — không cần lịch cứng
@dag(schedule=[orders], ...)
def consumer():
    @task
    def build_report(): ...
```

Lợi ích: bớt phụ thuộc lịch đoán mò, pipeline phản ứng theo *dữ liệu thật*, giảm lỗi "chạy khi chưa có
data". Đây là nền cho kiến trúc hướng sự kiện & **data contracts** (xu hướng 2026).

---

## 8. Sang phần thực hành

Ở [`lab/README.md`](./lab/): bạn viết & chạy 2 DAG —
1. `session03_idempotent_partition`: ghi partition theo `ds`, atomic + idempotent; tự kiểm chứng chạy lại
   không nhân đôi; thử backfill.
2. `session03_concepts_demo`: retry, timeout, XCom (truyền con trỏ), Variable, dependency rẽ nhánh.

Sau buổi: [`exercises.md`](./exercises.md) + [`checklist.md`](./checklist.md).

---

## Tài liệu tham khảo

- TaskFlow API — https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html
- Scheduling & catchup — https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/scheduling.html
- Backfill (Airflow 3) — https://airflow.apache.org/docs/apache-airflow/stable/howto/backfill.html
- Assets / data-aware scheduling — https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/assets.html
- XCom — https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/xcoms.html
