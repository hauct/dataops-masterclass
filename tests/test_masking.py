"""Unit test cho các hàm masking PII (buổi 7). Chạy: pytest tests/test_masking.py"""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "mask_demo", ROOT / "sessions" / "07-security-pii" / "lab" / "mask_demo.py"
)
mask = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mask)


def test_mask_email_che_phan_ten():
    assert mask.mask_email("andrew@example.com") == "a***@example.com"


def test_mask_phone_giu_3_so_cuoi():
    assert mask.mask_phone("0901234567") == "***567"


def test_pseudonymize_on_dinh():
    # Cùng input -> cùng output (join được).
    assert mask.pseudonymize("a@b.com") == mask.pseudonymize("a@b.com")


def test_pseudonymize_khac_nhau_cho_input_khac():
    assert mask.pseudonymize("a@b.com") != mask.pseudonymize("c@b.com")


def test_pseudonymize_khong_lo_ban_goc():
    # Hash không chứa chuỗi gốc.
    assert "a@b.com" not in mask.pseudonymize("a@b.com")


def test_encrypt_decrypt_roundtrip():
    plaintext = "an.nguyen@example.com"
    assert mask.decrypt_demo(mask.encrypt_demo(plaintext)) == plaintext
