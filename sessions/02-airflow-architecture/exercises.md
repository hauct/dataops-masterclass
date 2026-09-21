# Bài tập về nhà — Buổi 2

Tự chấm bằng [`checklist.md`](./checklist.md).

## Bài 1 — Bản đồ kiến trúc (lý thuyết)

Vẽ lại (tay hoặc số) sơ đồ kiến trúc Airflow với các thành phần: API Server, Scheduler, DAG Processor,
Triggerer, Executor, Worker, Metadata DB. Với mỗi thành phần, ghi 1 câu nhiệm vụ.

## Bài 2 — Chẩn đoán sự cố (vận dụng)

Với mỗi triệu chứng, cho biết bạn nghi thành phần nào hỏng và sẽ kiểm tra gì đầu tiên:

1. Đã thêm file DAG mới vào `dags/` nhưng 5 phút rồi vẫn không thấy trong UI.
2. DAG hiện trong UI, đã bật, nhưng không có run nào được tạo theo lịch.
3. Task nằm mãi ở trạng thái `queued`, không bao giờ `running`.
4. Web UI trả về lỗi 502, không truy cập được.
5. Một deferrable sensor "chờ file" bị treo, dù file đã có.

## Bài 3 — Chọn Executor (tình huống)

Đề xuất Executor phù hợp + lý do (2–3 câu) cho mỗi tình huống:

1. Startup nhỏ, 15 DAG, chạy trên 1 VM duy nhất.
2. Doanh nghiệp có ~800 DAG, cao điểm hàng nghìn task song song, đã có hạ tầng on-prem.
3. Công ty đã chuẩn hóa mọi thứ trên Kubernetes, workload data lúc nhiều lúc ít, muốn tiết kiệm chi phí khi nhàn rỗi.

## Bài 4 — Airflow 2 vs 3 (đọc & tóm tắt)

Đọc bài [Airflow 3 GA](https://airflow.apache.org/blog/airflow-three-point-oh-is-here/). Liệt kê **3 thay
đổi** bạn thấy ảnh hưởng nhiều nhất tới *vận hành* (DataOps) và giải thích vì sao (mỗi cái 1–2 câu).

## Bài 5 — Thực hành (code nhẹ)

1. Tạo một DAG mới của riêng bạn trong `dags/` tên `dags/<ten-ban>_hello.py`: gồm 3 task TaskFlow đơn giản
   (`a -> b -> c`), mỗi task log một câu. Đặt `schedule=None`, `tags=["buoi-02","tu-lam"]`.
2. Trigger và xác nhận chạy xanh cả 3 task.
3. (Tùy chọn) Thêm dependency rẽ nhánh: `a -> [b, c] -> d` và quan sát song song.

> Nộp: file DAG trong repo cá nhân + ảnh Graph view chạy thành công.

## Bài 6 — Suy ngẫm (mở)

Tổ chức bạn (hoặc một tổ chức bạn biết) đang điều phối pipeline bằng gì (cron, script tay, tool khác)?
Chuyển sang Airflow sẽ được/mất gì? (3–5 câu.)
