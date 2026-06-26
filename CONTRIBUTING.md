# Đóng góp & quy ước

Repo này là tài liệu học. Hoan nghênh học viên gửi PR sửa lỗi, bổ sung ví dụ, cải thiện lab.

## Quy ước commit

Dùng [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`.
Ví dụ: `docs(session-01): bổ sung case study sự cố reconciliation`.

## Cấu trúc một buổi học

```
sessions/NN-ten-buoi/
├── README.md       # bài giảng lý thuyết
├── lab/            # code thực hành (starter + solution)
├── exercises.md    # bài tập về nhà
└── checklist.md    # checklist tự đánh giá
```

## Trước khi gửi PR

- Code Python theo chuẩn: `ruff check .` và `ruff format .` không báo lỗi.
- DAG mới phải import được (không lỗi syntax): `python dags/your_dag.py`.
- Không commit file `.env` hay bất kỳ secret nào.
