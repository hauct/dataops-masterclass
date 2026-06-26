# Phân tích rủi ro pipeline — `pipeline_risky.py`

> Điền phân tích của bạn. Đây là bài nộp của Phần 3 lab buổi 1.
> Mục tiêu: luyện kỹ năng *nhìn ra* điểm yếu vận hành của một pipeline — kỹ năng cốt lõi của DataOps.

**Họ tên:** ______________   **Ngày:** ______________

## 1. Chấm theo checklist pipeline production

Đánh dấu ✅/❌ và giải thích ngắn (1 câu) cho mỗi mục.

| Tiêu chí | Đạt? | Giải thích |
|----------|------|-----------|
| Chạy lại an toàn (idempotent + atomic) | | |
| Có test dữ liệu trước khi xuống hạ nguồn | | |
| Có đối soát nguồn↔đích (reconciliation) | | |
| Có cảnh báo khi fail / dữ liệu sai | | |
| Code trong Git, môi trường pin version | | |
| Secrets không nằm trong code; PII được che | | |
| Có runbook & truy được nguồn gốc lỗi | | |

## 2. Ba rủi ro nghiêm trọng nhất

Liệt kê 3 rủi ro lớn nhất, xếp theo mức độ ảnh hưởng tới *dữ liệu tài chính*:

1.
2.
3.

## 3. Sự cố cụ thể có thể xảy ra

Mô tả một kịch bản sự cố thực tế bắt nguồn từ pipeline này (vd: chuyện gì xảy ra nếu job retry lúc 1h sáng?):

> _(viết ở đây)_

## 4. Hướng sửa

Với mỗi rủi ro ở mục 2, nêu nguyên lý/biện pháp khắc phục (chưa cần code):

| Rủi ro | Nguyên lý áp dụng | Cách sửa (ý tưởng) |
|--------|-------------------|--------------------|
| | | |
| | | |
| | | |

## 5. Tự đối chiếu với `pipeline_fixed.py`

Sau khi đọc bản đã sửa, có rủi ro nào bạn *bỏ sót* ở mục 2 không? Ghi lại để rút kinh nghiệm:

> _(viết ở đây)_
