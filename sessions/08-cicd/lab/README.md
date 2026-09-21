# Lab Buổi 8 — Dựng & chạy CI/CD

Mục tiêu: chạy được toàn bộ cửa kiểm tra CI ở local, thấy nó **chặn** thay đổi xấu, và diễn tập rollback.

> Cần: môi trường Python local (venv) đã cài `requirements-dev.txt` (có `pytest`, `ruff`). Phần validate DAG
> sâu cần `make up`.

---

## Phần 1 — Chạy test

```bash
pytest -q                 # hoặc: make test
```

Quan sát: các test ở `tests/` chạy xanh (unit masking, idempotency, dag-compile).

**Câu hỏi:** test `test_chay_lai_khong_nhan_doi` kiểm tra điều gì? Vì sao nó quan trọng với DataOps?

## Phần 2 — Chạy toàn bộ CI ở local

```bash
make ci
```

Lệnh này chạy đúng các bước CI trên GitHub: **lint (ruff) → quét secret → compile DAG → pytest**. Kỳ vọng:
`✅ CI local PASS`.

> Thói quen tốt: luôn `make ci` trước khi `git push` để không đẩy code đỏ lên.

## Phần 3 — Thấy CI CHẶN thay đổi xấu

Làm lần lượt, mỗi lần chạy lại `make ci` để thấy nó đỏ, rồi hoàn tác:

1. **Lỗi lint**: thêm một biến thừa / import không dùng vào một file trong `dags/` → `ruff` báo đỏ.
2. **Secret hardcode**: thêm `api_key = "sk-abcdef123456"` vào một file `.py` → bước quét secret đỏ.
3. **Test gãy**: sửa logic upsert trong `tests/test_idempotency.py` thành `INSERT` thuần (bỏ ON CONFLICT) →
   `test_chay_lai_khong_nhan_doi` fail.

**Câu hỏi:** với mỗi lỗi trên, bước CI nào bắt được? Nếu không có CI, lỗi nào sẽ âm thầm lên prod?

## Phần 4 — Validate DAG sâu (DagBag)

```bash
make up
make test-dags        # chạy `airflow dags list` trong container -> bắt lỗi import DAG thật
```

`test_dags_compile.py` chỉ bắt lỗi *cú pháp*; `make test-dags` bắt cả lỗi *import* (sai tên operator, thiếu
tham số...). **Câu hỏi:** vì sao cần cả hai mức?

## Phần 5 — Mô phỏng CD & rollback

```bash
# "Deploy" local: nạp lại DAG sau khi đổi code
make deploy-local

# Diễn tập rollback bằng Git: giả sử commit vừa rồi gây lỗi
git log --oneline -5
git revert HEAD --no-edit     # tạo commit đảo ngược thay đổi hỏng
make deploy-local             # nạp lại bản đã revert
```

**Câu hỏi:** vì sao "mọi thứ ở trong Git" giúp rollback an toàn & nhanh? Rollback bằng `git revert` khác gì
xóa commit?

---

## Phần 6 — Tự làm (mini)

Viết thêm **1 test** vào `tests/` cho pipeline của bạn (vd: test reconciliation phát hiện lệch, hoặc test
một hàm transform). Đảm bảo `make ci` vẫn xanh. (Tùy chọn) bật job `validate-dags` trong `ci.yml`.

---

## Nộp gì sau lab

- Ảnh `make ci` PASS.
- Bằng chứng CI **chặn** ít nhất 1 lỗi bạn cố tình tạo (Phần 3).
- Mô tả ngắn quy trình rollback bạn vừa diễn tập (Phần 5).
- Test mới bạn viết (Phần 6).
