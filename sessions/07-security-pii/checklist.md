# Checklist tự đánh giá — Buổi 7

## Secrets management

- [ ] Tôi hiểu vì sao secret không bao giờ được nằm trong code/Git.
- [ ] Tôi biết thứ tự ưu tiên: env/.env → Airflow Connection (Fernet) → secret manager.
- [ ] Tôi chạy được `scan_secrets.py` và thấy nó bắt được secret hardcode khi tôi cố tình thêm.

## PII & 3 kỹ thuật

- [ ] Tôi phân biệt masking / pseudonymization / encryption và chọn đúng theo mục đích.
- [ ] Tôi giải thích được vì sao hash (pseudonym) vẫn join được mà không lộ danh tính.
- [ ] Tôi biết nên che PII càng sớm càng tốt trong pipeline.

## RBAC least-privilege

- [ ] Tôi hiểu nguyên tắc least-privilege và "từ chối mặc định".
- [ ] Tôi áp được GRANT/REVOKE để một vai trò chỉ thấy bản đã masking.
- [ ] Tôi **kiểm chứng** được vai trò hạn chế bị từ chối đọc bảng thô PII.

## Governance & audit

- [ ] Tôi kể được các cơ chế governance: classification, retention, lineage, audit, data contract.
- [ ] Tôi hiểu audit log không được chứa giá trị PII thật.

## Thực hành

- [ ] Tôi chạy được `mask_demo.py` và `session07_pii_masking` (raw → masked → audit).
- [ ] Tôi rà soát được một DAG để tìm secret hardcode / rò rỉ PII và biết cách vá.

> ≥ 90% → sẵn sàng buổi 8 (CI/CD — sẽ dùng lại `scan_secrets.py` trong pipeline kiểm thử). < 70% → ôn lại mục 1 (secrets) & 2 (PII).
