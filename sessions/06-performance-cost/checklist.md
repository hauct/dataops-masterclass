# Checklist tự đánh giá — Buổi 6

## Tư duy

- [ ] Tôi hiểu "đúng trước, nhanh sau" và "đủ nhanh để đạt mục tiêu thì dừng".
- [ ] Tôi luôn kèm con số **before/after** khi tối ưu, không tối ưu theo cảm tính.

## Đọc kế hoạch thực thi

- [ ] Tôi đọc được `EXPLAIN ANALYZE` (Postgres): phân biệt Seq Scan vs Index Scan, đọc `actual time`.
- [ ] Tôi đọc được `df.explain()` của Spark: nhận ra `Exchange` (shuffle), `BroadcastHashJoin` vs `SortMergeJoin`.
- [ ] Tôi biết tìm bottleneck trên Spark UI (Stages, shuffle, task lệch).

## Ba bottleneck & cách xử lý

- [ ] **Shuffle**: tôi biết broadcast join / lọc sớm để giảm shuffle.
- [ ] **Data skew**: tôi nhận ra qua task lệch và biết khái niệm salting / AQE.
- [ ] **Small files**: tôi biết `coalesce`/`repartition` khi ghi và OPTIMIZE trên Delta.

## Kỹ thuật

- [ ] Tôi biết khi nào broadcast join (bảng nhỏ) và rủi ro khi broadcast bảng lớn.
- [ ] Tôi hiểu partition pruning và tác hại của partition quá mịn.
- [ ] Tôi biết caching chỉ hữu ích khi tái sử dụng ≥ 2 lần.

## Thực hành

- [ ] Tôi chạy được `explain_demo.sql` và thấy khác biệt trước/sau index.
- [ ] Tôi chạy được `perf_spark_demo` và đọc được số file + 2 physical plan.

## FinOps

- [ ] Tôi nêu được ≥ 3 cách giảm chi phí cloud và cách đo hiệu quả.

> ≥ 90% → sẵn sàng buổi 7 (bảo mật & dữ liệu nhạy cảm). < 70% → ôn lại mục 2–3 (đọc plan) & 4 (3 kỹ thuật).
