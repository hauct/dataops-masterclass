"""
scan_secrets — Máy quét secret hardcode đơn giản (chạy ngay, không cần infra).

    python scan_secrets.py [thư_mục]      # mặc định quét toàn repo

Bắt chước bước "secret scanning" trong CI (buổi 8): tìm mật khẩu/khóa bị nhúng thẳng vào code.
Đây là bản tối giản để học ý tưởng; thực tế dùng gitleaks / trufflehog / detect-secrets.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

# Các mẫu nghi ngờ là secret hardcode.
PATTERNS = [
    (r'password\s*=\s*[\'"][^\'"]{3,}[\'"]', "hardcoded password"),
    (r'api[_-]?key\s*=\s*[\'"][^\'"]{8,}[\'"]', "hardcoded api key"),
    (r'secret\s*=\s*[\'"][^\'"]{8,}[\'"]', "hardcoded secret"),
    (r'AKIA[0-9A-Z]{16}', "AWS access key id"),
    (r'-----BEGIN [A-Z ]*PRIVATE KEY-----', "private key"),
]

# Bỏ qua các thư mục/đuôi không cần quét.
SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "node_modules", "data", "logs"}
# Chỉ quét file CODE/CONFIG (không quét .md/.txt vì tài liệu cố tình nêu ví dụ secret để dạy).
SCAN_EXT = {".py", ".sql", ".yml", ".yaml", ".env", ".sh", ".toml", ".ini", ".cfg"}


def scan(root: Path) -> list[tuple[str, int, str]]:
    findings = []
    compiled = [(re.compile(p, re.IGNORECASE), label) for p, label in PATTERNS]
    # Dùng os.walk và CẮT NHÁNH thư mục bỏ qua ngay (không chui vào .venv/.git/data...) -> nhanh.
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".")]
        for fn in filenames:
            path = Path(dirpath) / fn
            if path.suffix not in SCAN_EXT:
                continue
            if path.name in {".env.example", "scan_secrets.py"}:  # bỏ file ví dụ & chính nó
                continue
            try:
                for n, line in enumerate(
                    path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1
                ):
                    for rx, label in compiled:
                        if rx.search(line):
                            findings.append((str(path), n, label))
            except Exception:
                continue
    return findings


if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[3]
    print(f"Quét secret hardcode trong: {root}\n")
    results = scan(root)
    if not results:
        print("✅ Không phát hiện secret hardcode (theo các mẫu cơ bản).")
    else:
        print(f"⚠️  Phát hiện {len(results)} điểm nghi ngờ:")
        for f, n, label in results:
            print(f"  {f}:{n}  -> {label}")
        sys.exit(1)   # exit code != 0 để CI fail (buổi 8)
