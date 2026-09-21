# Lab Buổi 6 — Tìm bottleneck & tối ưu (có đo lường)

Mục tiêu: luyện quy trình **đo → tìm bottleneck → sửa → đo lại**, trên cả DWH (query plan) và Spark (plan + UI).

> Phần SQL cần `make up-warehouse`; phần Spark cần `make up-lakehouse` (hoặc `make up-cluster` để xem UI rõ hơn).

---

## Phần 1 — Đọc query plan & tối ưu bằng index (DWH)

Chạy file SQL demo (đọc từ host, đẩy vào psql qua stdin):

```bash
docker compose exec -T warehouse psql -U dwh -d analytics \
  < sessions/06-performance-cost/lab/sql/explain_demo.sql
```

File này: tạo bảng 1 triệu dòng → `EXPLAIN ANALYZE` khi **chưa** có index → thêm index → `EXPLAIN ANALYZE` lại.

**Câu hỏi quan sát:**
- Trước index: kế hoạch dùng **Seq Scan** hay **Index Scan**? `actual time` bao nhiêu?
- Sau index: đổi thành gì? `actual time` giảm bao nhiêu lần?
- Vì sao index giúp truy vấn *lọc theo `order_date`* nhanh hơn?

> Dọn: `docker compose exec warehouse psql -U dwh -d analytics -c "DROP TABLE IF EXISTS perf_orders;"`

## Phần 2 — Spark: small-files & broadcast join

```bash
# local:
make spark-job SESSION=06-performance-cost JOB=perf_spark_demo
# hoặc cluster (để xem Spark UI ở http://localhost:8085):
make up-cluster && make spark-job-cluster SESSION=06-performance-cost JOB=perf_spark_demo
```

> Lưu ý: `SESSION` mặc định là `05-pyspark-lakehouse`. Job buổi 6 nằm ở thư mục khác nên phải truyền
> `SESSION=06-performance-cost`. (Job buổi 5 thì không cần vì dùng mặc định.)

Quan sát output 3 phần:

**A. Small files** — so sánh số file của `repartition(50)` vs `coalesce(2)`.
- *Câu hỏi:* vì sao nhiều file nhỏ làm việc đọc lại chậm? Khi nào nên `coalesce` lúc ghi?

**B. Broadcast join** — đọc 2 physical plan in ra.
- *Câu hỏi:* plan "không broadcast" xuất hiện `SortMergeJoin` và `Exchange` (shuffle) không? Plan "có broadcast"
  đổi thành `BroadcastHashJoin` chứ? Vì sao broadcast bảng *nhỏ* lại bỏ được shuffle của bảng *lớn*?

**C. Đo thời gian** — ghi lại con số giây in ra (thói quen before/after).

## Phần 3 — Quan sát trên Spark UI (nếu chạy cluster)

Khi job đang chạy (hoặc xem lại qua History), mở http://localhost:8085 → vào application → tab **Stages**:
- Tìm stage có **Shuffle Read/Write** lớn — đó là điểm tốn kém.
- Xem phân bố thời gian các task trong một stage: nếu có 1 task lâu vượt trội → **data skew**.

**Câu hỏi:** bạn thấy bao nhiêu stage? Stage nào có shuffle? Có task nào lệch không?

## Phần 4 — (Thử nghiệm) tự tối ưu

Sửa `perf_spark_demo.py` (bản copy của bạn):
1. Tăng dữ liệu fact lên 2 triệu dòng, đo lại thời gian phần C.
2. Thử bỏ `F.broadcast(...)` và để Spark tự quyết — plan có đổi không? (gợi ý: `autoBroadcastJoinThreshold`).
3. (Nâng cao) tạo key lệch (vd 80% dữ liệu cùng `product_id`) và quan sát task lệch trên UI; đọc về **salting**.

---

## Phần 5 — Tự làm (mini, FinOps)

Viết một đoạn ngắn (trong repo, file `notes.md`) cho pipeline buổi 4/5 của bạn: liệt kê **3 cách giảm chi phí**
nếu chạy trên cloud (vd partition pruning để quét ít hơn, auto-suspend warehouse, dùng spot cho Spark), kèm
*cách đo* mỗi cách có hiệu quả không.

---

## Nộp gì sau lab

- Ảnh/log `EXPLAIN ANALYZE` trước & sau index (Phần 1) + nhận xét before/after.
- Log `perf_spark_demo` (số file A, hai plan B, thời gian C) + trả lời câu hỏi.
- (Nếu chạy cluster) ảnh Spark UI Stages.
- `notes.md` FinOps (Phần 5).

> Dọn: `rm -rf data/perf_demo`. Tắt: `make down`.
