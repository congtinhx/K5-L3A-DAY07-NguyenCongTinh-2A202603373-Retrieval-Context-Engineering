# Bảng kết quả (sinh tự động từ results/)

## Retrieval — dev

| Cấu hình | Phương pháp, top-k, context | Hit@1 | Evidence Hit@3 | Context Evidence Rate | MRR | Ctx chars TB | Median ms | Chi phí |
|---|---|---|---|---|---|---|---|---|
| bm25_k3 | bm25, k=3, cand=-, rank, budget=3200 | 13/16 (81%) | 16/16 (100%) | 16/16 (100%) | 0.8958 | 2607.4 | 1.9 | $0 |
| dense_k3 | dense, k=3, cand=-, rank, budget=3200 | 13/16 (81%) | 15/16 (94%) | 15/16 (94%) | 0.8646 | 2618.9 | 184.3 | $0 |
| hybrid_k3 | hybrid, k=3, cand=20, rank, budget=3200 | 14/16 (88%) | 16/16 (100%) | 16/16 (100%) | 0.9167 | 2702.2 | 209.8 | $0 |
| hybrid_rerank_k3 | hybrid_rerank, k=3, cand=20, rank, budget=3200 | 13/16 (81%) | 16/16 (100%) | 16/16 (100%) | 0.9062 | 2611.6 | 2657.9 | $0 |
| hybrid_k5_neighbors | hybrid, k=5, cand=20, rank_neighbors, budget=6400 | 14/16 (88%) | 16/16 (100%) | 16/16 (100%) | 0.9167 | 5822.3 | 193.4 | $0 |

## Retrieval — test_v1

| Cấu hình | Phương pháp, top-k, context | Hit@1 | Evidence Hit@3 | Context Evidence Rate | MRR | Ctx chars TB | Median ms | Chi phí |
|---|---|---|---|---|---|---|---|---|
| dense_k3 | dense, k=3, cand=-, rank, budget=3200 | 3/6 (50%) | 5/6 (83%) | 5/6 (83%) | 0.6389 | 2871.6 | 100.5 | $0 |
| hybrid_k5_neighbors | hybrid, k=5, cand=20, rank_neighbors, budget=6400 | 4/6 (67%) | 5/6 (83%) | 5/6 (83%) | 0.7833 | 6110.2 | 221.2 | $0 |

## Retrieval — test

| Cấu hình | Phương pháp, top-k, context | Hit@1 | Evidence Hit@3 | Context Evidence Rate | MRR | Ctx chars TB | Median ms | Chi phí |
|---|---|---|---|---|---|---|---|---|
| dense_k3 | dense, k=3, cand=-, rank, budget=3200 | 5/6 (83%) | 6/6 (100%) | 6/6 (100%) | 0.9167 | 2698.8 | 178.6 | $0 |
| hybrid_k5_neighbors | hybrid, k=5, cand=20, rank_neighbors, budget=6400 | 5/6 (83%) | 6/6 (100%) | 6/6 (100%) | 0.9167 | 6042.1 | 174.6 | $0 |

## Agent — dev_v1

| Cấu hình | Tool use | Số lượt search | Grounded 0/1/2 (TB /2) | Citation hợp lệ | Câu có citation | Abstention đúng | Từ chối nhầm | Ctx evidence | Median s | Token in/out | Chi phí |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bm25_k3 | 18/18 (100%) | {'1': 17, '3': 1} | chưa chấm | chưa chấm | chưa chấm | chưa chấm | chưa chấm | 16/16 (100%) | 2.95 | 26901/1816 | $0.0051 |
| dense_k3 | 18/18 (100%) | {'1': 17, '3': 1} | chưa chấm | chưa chấm | chưa chấm | chưa chấm | chưa chấm | 15/16 (94%) | 3.33 | 26909/1853 | $0.0052 |
| hybrid_k3 | 18/18 (100%) | {'1': 18} | chưa chấm | chưa chấm | chưa chấm | chưa chấm | chưa chấm | 16/16 (100%) | 3.14 | 23468/1826 | $0.0046 |
| hybrid_k5_neighbors | 18/18 (100%) | {'1': 17, '2': 1} | chưa chấm | chưa chấm | chưa chấm | chưa chấm | chưa chấm | 16/16 (100%) | 3.26 | 38219/1911 | $0.0069 |
| hybrid_rerank_k3 | 18/18 (100%) | {'1': 17, '3': 1} | chưa chấm | chưa chấm | chưa chấm | chưa chấm | chưa chấm | 16/16 (100%) | 8.38 | 26505/1976 | $0.0052 |

## Agent — dev

| Cấu hình | Tool use | Số lượt search | Grounded 0/1/2 (TB /2) | Citation hợp lệ | Câu có citation | Abstention đúng | Từ chối nhầm | Ctx evidence | Median s | Token in/out | Chi phí |
|---|---|---|---|---|---|---|---|---|---|---|---|
| bm25_k3 | 18/18 (100%) | {'1': 17, '2': 1} | 0/1/15 (1.94) | 16/16 (100%) | 16/16 (100%) | 2/2 (100%) | 0/16 (0%) | 16/16 (100%) | 2.6 | 26453/1949 | $0.0051 |
| dense_k3 | 18/18 (100%) | {'1': 17, '2': 1} | 0/0/16 (2.00) | 18/19 (95%) | 17/17 (100%) | 1/2 (50%) | 0/16 (0%) | 15/16 (94%) | 2.99 | 27441/2013 | $0.0053 |
| hybrid_k3 | 18/18 (100%) | {'1': 18} | 0/0/16 (2.00) | 17/17 (100%) | 16/16 (100%) | 2/2 (100%) | 0/16 (0%) | 16/16 (100%) | 2.63 | 25228/1982 | $0.0050 |
| hybrid_k5_neighbors | 18/18 (100%) | {'1': 18} | 0/0/16 (2.00) | 16/16 (100%) | 16/16 (100%) | 2/2 (100%) | 0/16 (0%) | 16/16 (100%) | 2.82 | 38505/1976 | $0.0070 |
| hybrid_rerank_k3 | 18/18 (100%) | {'1': 17, '3': 1} | 0/0/16 (2.00) | 18/18 (100%) | 16/16 (100%) | 2/2 (100%) | 0/16 (0%) | 16/16 (100%) | 4.98 | 28442/2059 | $0.0055 |

## Agent — test_v1

| Cấu hình | Tool use | Số lượt search | Grounded 0/1/2 (TB /2) | Citation hợp lệ | Câu có citation | Abstention đúng | Từ chối nhầm | Ctx evidence | Median s | Token in/out | Chi phí |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dense_k3 | 8/8 (100%) | {'1': 5, '2': 3} | 4/0/2 (0.67) | 4/4 (100%) | 3/3 (100%) | 2/2 (100%) | 3/6 (50%) | 4/6 (67%) | 3.72 | 14343/874 | $0.0027 |
| hybrid_k5_neighbors | 8/8 (100%) | {'1': 7, '2': 1} | 3/0/3 (1.00) | 5/5 (100%) | 4/4 (100%) | 2/2 (100%) | 2/6 (33%) | 5/6 (83%) | 3.08 | 19497/800 | $0.0034 |

## Agent — test

| Cấu hình | Tool use | Số lượt search | Grounded 0/1/2 (TB /2) | Citation hợp lệ | Câu có citation | Abstention đúng | Từ chối nhầm | Ctx evidence | Median s | Token in/out | Chi phí |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dense_k3 | 8/8 (100%) | {'1': 6, '3': 2} | 1/0/5 (1.67) | 5/6 (83%) | 5/5 (100%) | 2/2 (100%) | 1/6 (17%) | 5/6 (83%) | 2.56 | 18874/730 | $0.0033 |
| hybrid_k5_neighbors | 8/8 (100%) | {'1': 7, '3': 1} | 0/0/6 (2.00) | 6/6 (100%) | 6/6 (100%) | 2/2 (100%) | 0/6 (0%) | 6/6 (100%) | 2.22 | 22317/732 | $0.0038 |

Cấu hình chốt trên dev: **hybrid_k5_neighbors** (lúc 2026-11-14T22:37:07+07:00). Baseline: **dense_k3**.

