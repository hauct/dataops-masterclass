# Checklist tự đánh giá — Buổi 1

Tự tích ✅. Nếu còn ô trống, đọc lại mục tương ứng trong `README.md` hoặc hỏi mentor ở buổi sau.

## Hiểu khái niệm

- [ ] Tôi giải thích được DataOps là gì bằng 1–2 câu, và nó **không phải** một công cụ.
- [ ] Tôi phân biệt được DataOps vs DE vs DA qua ví dụ, không cần nhìn bảng.
- [ ] Tôi nêu được ít nhất 2 lý do reliability quan trọng với dữ liệu tài chính.

## Nắm 4 nguyên lý nền tảng

- [ ] **Idempotency:** tôi định nghĩa được và chỉ ra một đoạn code idempotent vs không idempotent.
- [ ] **Atomicity:** tôi giải thích được "không để lại trạng thái nửa vời" nghĩa là gì & vì sao quan trọng.
- [ ] **Reproducibility:** tôi hiểu vì sao hardcode `now()`/`CURRENT_DATE` có thể phá tính tái lập.
- [ ] **Reconciliation:** tôi thiết kế được ít nhất 2 phép đối soát nguồn↔đích kèm ngưỡng.

## Kỹ năng thực hành

- [ ] Tôi đã chạy `pipeline_risky.py` 2 lần và hiểu vì sao dữ liệu bị nhân đôi.
- [ ] Tôi đã chạy `pipeline_fixed.py` nhiều lần và xác nhận kết quả không đổi (idempotent).
- [ ] Tôi chỉ ra được trong `pipeline_fixed.py` dòng nào thực thi từng nguyên lý.
- [ ] Tôi đã điền xong `analysis_template.md`.

## Môi trường & repo

- [ ] Docker stack lên được (`make up`) và tôi mở được Airflow UI (hoặc đã lên kế hoạch cài trước buổi 2).
- [ ] Tôi đã fork + clone repo khóa học và tạo nhánh cá nhân.
- [ ] Tôi biết dùng `make down` để tắt stack tiết kiệm tài nguyên.

## Sẵn sàng cho buổi 2

- [ ] Tôi biết buổi 2 sẽ học Airflow (kiến trúc & triển khai) và stack cần bật là `make up`.
- [ ] Tôi đã đọc lướt outline buổi 2 trong `CURRICULUM.md`.

> **Tự chấm:** ≥ 90% ô đã tích → vững nền, sẵn sàng buổi 2. < 70% → nên ôn lại `README.md` mục 4 & 5.
