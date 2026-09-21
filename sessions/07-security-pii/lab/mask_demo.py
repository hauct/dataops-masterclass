"""
mask_demo — Minh họa 3 kỹ thuật bảo vệ PII bằng Python thuần (chạy ngay, không cần infra).

    python mask_demo.py

So sánh: masking (che) vs pseudonymization (hash) vs encryption (mã hóa - khôi phục được).
"""

from __future__ import annotations

import base64
import hashlib
import re

SAMPLES = [
    ("Nguyen Van An", "an.nguyen@example.com", "0901234567"),
    ("Tran Thi Binh", "binh.tran@example.com", "0912345678"),
]


def mask_email(email: str) -> str:
    """MASKING: che phần tên, giữ domain -> a***@example.com (không khôi phục được)."""
    return re.sub(r"(^.).*(@.*$)", r"\1***\2", email)


def mask_phone(phone: str) -> str:
    """MASKING: chỉ giữ 3 số cuối."""
    return "***" + phone[-3:]


def pseudonymize(value: str, salt: str = "dataops-salt") -> str:
    """PSEUDONYMIZATION: hash ổn định (SHA-256 + salt). Cùng input -> cùng output (join được),
    nhưng KHÔNG suy ngược ra bản gốc."""
    return hashlib.sha256((salt + value).encode()).hexdigest()[:16]


def encrypt_demo(value: str, key: int = 7) -> str:
    """ENCRYPTION (minh họa đơn giản, KHÔNG dùng thật): có thể GIẢI MÃ lại nếu có khóa.
    Production: dùng AES qua thư viện cryptography, khóa quản lý ở secret manager."""
    xored = bytes(b ^ key for b in value.encode())
    return base64.b64encode(xored).decode()


def decrypt_demo(token: str, key: int = 7) -> str:
    xored = base64.b64decode(token.encode())
    return bytes(b ^ key for b in xored).decode()


if __name__ == "__main__":
    print(f"{'GỐC (PII)':<40} {'MASK':<22} {'PSEUDO(hash)':<18} {'ENCRYPT->DECRYPT'}")
    print("-" * 100)
    for name, email, phone in SAMPLES:
        enc = encrypt_demo(email)
        dec = decrypt_demo(enc)
        print(
            f"{email:<40} {mask_email(email):<22} {pseudonymize(email):<18} "
            f"{enc[:12]}...->{dec}"
        )
        print(f"  phone {phone} -> mask {mask_phone(phone)}")
    print("\nGhi nhớ: cần join/đếm theo người -> hash; cần hiển thị an toàn -> mask; cần lấy lại gốc -> encrypt.")
