"""
Kiểm tra mọi file DAG biên dịch được (bắt lỗi cú pháp) — nhẹ, không cần cài Airflow.

Đây là "DAG integrity test" mức cơ bản trong CI. Mức sâu hơn (kiểm tra import lỗi bằng DagBag) chạy
trong container Airflow: xem `make test-dags`.
"""

from __future__ import annotations

import py_compile
from pathlib import Path

import pytest

DAGS = sorted((Path(__file__).resolve().parents[1] / "dags").glob("*.py"))


@pytest.mark.parametrize("dag_file", DAGS, ids=[f.name for f in DAGS])
def test_dag_compiles(dag_file):
    py_compile.compile(str(dag_file), doraise=True)


def test_co_it_nhat_mot_dag():
    assert DAGS, "không tìm thấy file DAG nào trong dags/"
