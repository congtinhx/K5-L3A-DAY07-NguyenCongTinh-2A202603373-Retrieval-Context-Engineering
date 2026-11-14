# Bài làm Day 7 — Agentic RAG (Nguyễn Công Tĩnh · 2A202603373)

Agent dùng model thật (OpenAI `gpt-4o-mini`, tool calling) tìm bằng chứng trong **vector store Day 6** (PostgreSQL + pgvector, index B, `intfloat/multilingual-e5-small`, 384 chiều), trả lời có citation `[chunk-id]` hoặc từ chối khi thiếu bằng chứng.

## Cấu trúc

| Đường dẫn | Nội dung |
|---|---|
| `src/rag7/retrievers.py` | 4 phương pháp: dense (pgvector Day 6), BM25, hybrid RRF, hybrid + cross-encoder rerank |
| `src/rag7/context.py` | Chọn context: dedup, theo rank, thêm chunk lân cận cùng trang, giới hạn ký tự |
| `src/rag7/agent.py`, `src/rag7/llm.py` | Vòng lặp agent (tool `search_documents`, `submit_answer`), client OpenAI không cần SDK |
| `src/rag7/experiments.py`, `run.py` | Benchmark retrieval, chốt cấu hình trên dev, chạy agent, review sheet, metrics, bảng báo cáo |
| `configs/experiments.json` | Toàn bộ cấu hình, giả thuyết, tiêu chí chọn (công bố trước khi chạy) |
| `data/day6_chunks.json` | 157 chunk index B xuất từ Day 6 (dùng cho BM25 và chấm evidence) |
| `data/benchmark/questions.json` | 26 câu: dev 16 có đáp án + 2 thiếu evidence; test 6 + 2 |
| `tests/test_rag7.py` | Test offline (fake model/dense chỉ kiểm tra code, không phải benchmark) |
| `results/` | Trace, summary, review sheet, nhãn, `report_tables.md` |
| `report/individual/2A202603373_NguyenCongTinh.md` | Báo cáo |

## Chuẩn bị (Windows)

1. Thư mục Day 6 nằm cạnh repo này: `..\K5-L3A-DAY06-NguyenCongTinh-2A202603373-DataIngestion` (hoặc đặt biến `DAY6_DIR`). Dùng **venv của Day 6** (đã có `sentence-transformers`, `psycopg`).
2. Bật database Day 6: `cd ..\K5-L3A-DAY06-...\starter` → `docker compose -p day6_student_starter up -d --wait`.
3. API key: code đọc `OPENAI_API_KEY` từ `.env` ở repo này, nếu không có thì đọc `starter\.env` của Day 6. Không commit `.env`. (Tùy chọn `OPENAI_BASE_URL` cho endpoint tương thích.)
4. Rerank cần tải `cross-encoder/ms-marco-MiniLM-L-6-v2` (~90 MB) lần đầu.

## Chạy

Cách nhanh: chạy `run_all.bat` (làm tuần tự tất cả các bước dưới). Từng bước:

```cmd
set PY=..\K5-L3A-DAY06-NguyenCongTinh-2A202603373-DataIngestion\.venv\Scripts\python.exe
%PY% -m unittest discover -s tests -v
%PY% run.py export-chunks --from db        REM đọc 157 chunk từ pgvector
%PY% run.py check --db                     REM kiểm tra benchmark, DB khớp file, smoke test dense
%PY% run.py retrieval --split dev          REM 5 cấu hình trên dev
%PY% run.py select                         REM chốt cấu hình theo tiêu chí công bố trước (chỉ dev)
%PY% run.py agent --split dev --configs dense_k3 bm25_k3 hybrid_k3 hybrid_rerank_k3 hybrid_k5_neighbors
%PY% run.py retrieval --split test         REM chỉ baseline + cấu hình đã chốt
%PY% run.py agent --split test --configs baseline selected
%PY% run.py report                         REM sinh results\report_tables.md
```

Lệnh `retrieval/agent --split test` **từ chối chạy** nếu chưa có `results/selected_config.json` hoặc nếu yêu cầu cấu hình khác baseline/đã chốt.

## Chấm tay và tổng hợp

Mỗi lần chạy agent tạo `results/agent/<split>/<config>/review_sheet.md` (câu hỏi, query, context, câu trả lời, nguyên văn chunk được trích) và `reviews_template.json`. Đọc review sheet, chép template thành `reviews.json`, điền `answer_grade` (0/1/2), `citation_support` (true/false từng citation), `abstention_correct`, `context_grade`, `reason`. Sau đó:

```cmd
%PY% run.py metrics --split test --config baseline
%PY% run.py metrics --split test --config selected
%PY% run.py report
```

`metrics` dùng `starter/agent_metrics.py` gốc của đề. Lỗi model/vector store được ghi `status: "error"` và báo riêng, không thay bằng kết quả giả.
