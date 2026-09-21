# Bài tập về nhà — Buổi 8

Tự chấm bằng [`checklist.md`](./checklist.md).

## Bài 1 — Vì sao CI/CD cho pipeline (lý thuyết)

Nêu 3 sự cố thực tế có thể tránh được nhờ CI/CD cho pipeline dữ liệu. Vì sao "data test" cần thiết bên cạnh
unit test thông thường?

## Bài 2 — Kim tự tháp test (phân loại)

Xếp mỗi test sau vào lớp phù hợp (unit / logic-data / DAG integrity / data quality) và giải thích:

1. Kiểm tra hàm `mask_email` trả về đúng định dạng.
2. Kiểm tra chạy lại pipeline 1 ngày không nhân đôi dữ liệu.
3. Kiểm tra bảng `daily_revenue` không có `total_amount` âm trên dữ liệu thật.
4. Kiểm tra file DAG import được, không sai tên operator.

## Bài 3 — Đọc workflow CI (vận dụng)

Mở `.github/workflows/ci.yml`. Liệt kê thứ tự các bước. Nếu bước "quét secret" đặt **sau** "deploy" thì có ý
nghĩa gì không? Vì sao thứ tự "fail sớm" quan trọng?

## Bài 4 — Rollback (tình huống)

Bạn deploy lúc 22h, 22h30 phát hiện DAG mới ghi sai dữ liệu. Mô tả các bước rollback an toàn theo GitOps.
`git revert` khác `git reset --hard` thế nào, và vì sao revert an toàn hơn trên nhánh chung?

## Bài 5 — Môi trường (thiết kế)

Vì sao nên deploy qua Dev → Staging → Prod thay vì thẳng lên Prod? Staging nên giống Prod ở điểm nào và khác
ở điểm nào (gợi ý: dữ liệu)?

## Bài 6 — Code (cốt lõi)

Viết thêm một test trong `tests/` cho pipeline của bạn (vd: test rằng reconciliation **raise** khi nguồn ≠
đích). Chạy `make ci` xanh. Nộp test + ảnh CI pass.
