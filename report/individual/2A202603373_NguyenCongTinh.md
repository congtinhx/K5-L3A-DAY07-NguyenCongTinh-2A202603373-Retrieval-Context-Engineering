# Báo cáo Day 7 — Nguyễn Công Tĩnh (2A202603373, L3A)

Mọi số liệu dưới đây lấy từ `results/` (sinh lại bằng `python run.py report` → `results/report_tables.md`). Ngày chạy: 14/11/2026. Nhãn chấm tay (grounded, citation, abstention, context) đề xuất sau khi đọc từng trace và nguyên văn chunk; mỗi nhãn có trường `reason` và `labeled_by` trong `reviews.json`. 

## Dữ liệu và benchmark

- **Nguồn, quyền sử dụng, số trang và số chunk:** World Bank, *World Development Report 2024: The Middle-Income Trap*, trích Part 1 (PDF 44 trang, 41 trang nội dung theo quy tắc Day 6 ≥ 1000 ký tự), giấy phép CC BY 3.0 IGO. Dùng lại index **B** của Day 6 (chunk theo câu/heading, ≤ 1000 ký tự): **157 chunk**, ID `B:wdr2024_part1:pNNN:cNNN`, metadata `section`, `printed_page`, `char_start/end`.
- **Vector store, embedding model, phiên bản và số chiều:** PostgreSQL 16 + pgvector 0.8.7 (Docker `pgvector/pgvector:0.8.7-pg16`, cosine `<=>`, exact search), truy cập qua `PgVectorStore` của Day 6. Embedding `intfloat/multilingual-e5-small` (sentence-transformers 6.3.0, CPU, **384 chiều**, chuẩn hóa L2, tiền tố `query:`/`passage:`) qua `MyEmbedder` Day 6, nên query embedding tương thích index. Không tạo index mới. `run.py check --db`: DB có 157 chunk, **khớp từng ký tự** với `data/day6_chunks.json` (`results/check_db.json`).
- **Agent model, cách chạy và phân chia dev/test:** OpenAI `gpt-4o-mini`, temperature 0, Chat Completions + tool calling (client stdlib `src/rag7/llm.py`). Chạy bằng venv Day 6 (Python 3.14), lệnh trong `RUN.md`.
  - **dev:** 16 câu có đáp án + 2 câu thiếu evidence (u01, u02).
  - **test_v1:** 6 câu có đáp án + 2 câu thiếu evidence (u03, u04), lấy từ benchmark Day 6. Đã chạy một lần với agent v1 **và đã xem kết quả trước khi sửa agent**, nên không còn là test độc lập (giữ lại để báo cáo trung thực).
  - **test (mới):** 6 câu có đáp án (n01–n06) + 2 câu thiếu evidence (x01, x02). Viết sau khi chốt cấu hình và sửa agent dựa trên dev, lấy từ các trang chưa có trong benchmark (p11, p18, p28, p29, p31). Chưa từng chạy hệ thống trên các câu này trước lần đánh giá cuối. **Đây là test độc lập.**
  - Tổng: 34 câu, gồm 28 câu có đáp án và 6 câu thiếu evidence.
- **Cách xác định câu có/thiếu evidence và tiêu chí chấm:**
  - Câu có đáp án: evidence phải nằm trọn trong một chunk đúng `source_id` + `page` (cùng định nghĩa `starter/baseline.py`). Một số câu có evidence thay thế ở trang khác (q01, q02, q04, t05). 3 evidence lấy từ Day 6 (q15, t01, t05) được sửa ký tự (dấu nháy cong, gạch ngang dài) cho khớp nguyên văn PDF.
  - Câu thiếu evidence: các câu **gần chủ đề**, kiểm tra bằng grep toàn văn `pdftotext` và 157 chunk. Gồm: Thailand không xuất hiện trong tài liệu; R&D của Bulgaria (tài liệu chỉ có số của Estonia và Poland); mục tiêu thu nhập cao của Indonesia; tỷ lệ thất nghiệp của Viet Nam; R&D của Estonia năm 2010 (tài liệu chỉ có năm 2021); thuế carbon. Lý do ghi trong `absence_reason`. Các câu này không vào mẫu số của retrieval metrics.
  - Gold không bao giờ đi vào agent hay retriever: `public_question` chỉ truyền câu hỏi và filter.
- **Filter:** 5 câu có filter `section` do người dùng nêu trong câu hỏi (q10, q14, t03, t05, n06). Filter áp dụng cho mọi lượt search và được ghi trong trace; không suy ra filter từ gold.

## Retrieval và thử nghiệm

**Điều kiện chung:** cùng 157 chunk, cùng câu hỏi gốc (retrieval benchmark dùng nguyên văn câu hỏi, không viết lại), cùng nhãn.
- Hit@1 và Evidence Hit@3 tính trên 3 kết quả đầu, kể cả cấu hình top-5.
- Context Evidence Rate = số câu có evidence trong context cuối / số câu có đáp án.
- Context budget đo bằng ký tự, gồm cả header nguồn/trang.
- Thời gian là median mỗi truy vấn trên CPU laptop, gồm cả embedding query.
- Retrieval chạy local nên chi phí $0. Thời gian tải model: embedder ~31–35 s, cross-encoder ~21 s.

| Cấu hình | Phương pháp, top-k, filter, rerank, context budget | Giả thuyết / thay đổi | Split | Hit@1 | Evidence Hit@3 | Context Evidence Rate | Thời gian / chi phí |
|---|---|---|---|---|---|---|---|
| Baseline `dense_k3` | Dense pgvector Day 6, k=3, filter người dùng, budget 3200 | Baseline Day 6 | dev | 13/16 (81%) | 15/16 (94%) | 15/16 (94%) | 184 ms / $0 |
| Phương pháp 2 `bm25_k3` | BM25 (k1 1.5, b 0.75, stopword EN), k=3, budget 3200 | Câu hỏi có số, tên riêng → khớp từ khóa | dev | 13/16 (81%) | 16/16 (100%) | 16/16 (100%) | 1,9 ms / $0 |
| Phương pháp 3 `hybrid_k3` | RRF(dense 20, BM25 20), k_rrf=60, k=3, budget 3200 | Gộp ngữ nghĩa + từ khóa | dev | 14/16 (88%) | 16/16 (100%) | 16/16 (100%) | 210 ms / $0 |
| Cải thiện 1 `hybrid_rerank_k3` | Hybrid 20 candidate → cross-encoder `ms-marco-MiniLM-L-6-v2`, k=3 | Rerank tăng Hit@1 | dev | 13/16 (81%) | 16/16 (100%) | 16/16 (100%) | 2658 ms / $0 |
| Cải thiện 2 `hybrid_k5_neighbors` | Hybrid k=5 + chunk lân cận cùng trang, budget 6400 | Context đủ evidence hơn, đổi lại context ~2× | dev | 14/16 (88%) | 16/16 (100%) | 16/16 (100%) | 193 ms / $0 |
| Cấu hình đã chọn `hybrid_k5_neighbors` | như trên | Chốt bằng `run.py select` lúc 22:37 | test | 5/6 (83%) | 6/6 (100%) | 6/6 (100%) | 175 ms / $0 |
| Baseline `dense_k3` | như trên | | test | 5/6 (83%) | 6/6 (100%) | 6/6 (100%) | 179 ms / $0 |
| (tham khảo) đã chọn | | | test_v1 | 4/6 (67%) | 5/6 (83%) | 5/6 (83%) | 221 ms |
| (tham khảo) baseline | | | test_v1 | 3/6 (50%) | 5/6 (83%) | 5/6 (83%) | 101 ms |

MRR@k trên dev: dense 0,865; BM25 0,896; hybrid 0,917; rerank 0,906; hybrid_k5 0,917.

`hybrid_rerank_k3` vừa là phương pháp thứ 4 vừa là cải thiện 1. `hybrid_k5_neighbors` là cải thiện cấu hình (top-k, context) của hybrid.

**Tiêu chí chọn (ghi trong `configs/experiments.json` trước khi chạy, chỉ dùng dev):** (1) Context Evidence Rate; (2) Evidence Hit@3; (3) Hit@1; (4) median latency; (5) cấu hình đơn giản hơn. Có 4 cấu hình hòa ở (1) và (2). `hybrid_k3` và `hybrid_k5_neighbors` cùng có Hit@1 14/16, và `hybrid_k5_neighbors` thắng ở bước (4) với 193 ms so với 210 ms. Đây là chênh lệch nhỏ, nằm trong mức dao động đo; hai cấu hình gần như tương đương về retrieval. `hybrid_k5_neighbors` đổi lấy context dài gấp ~2,2 lần (5822 so với 2702 ký tự).

**Kết quả giả thuyết:**
- Cải thiện 1 (rerank) **không** tăng Hit@1: 13/16 so với 14/16 của hybrid. Cross-encoder MS MARCO đẩy q09 từ rank 1 xuống rank 2 (dù kéo q13 và q14 từ rank 3 lên rank 2), đồng thời chậm hơn ~13 lần. Kết luận: không đáng dùng trên corpus này.
- Cải thiện 2 không đổi ranking so với hybrid nhưng cho agent nhiều context hơn. Trên test mới, hybrid_k5 tìm được n06 ngay lượt đầu, còn dense thì không (xem lỗi 3).

**Lỗi dev và cách xử lý:**
1. **Retrieval, q14 (dense):** evidence "tax credits for royalty payments or R&D" không có trong top-3 dense; giả thuyết: chunk gold p025:c001 bắt đầu bằng đoạn "Postwar Europe…" nên vector của chunk bị pha loãng. BM25 xếp chunk này rank 1 nhờ từ "subsidize/Korea/tax credits". Hybrid đưa lên rank 3, nên Context Evidence Rate dev tăng từ 15/16 lên 16/16. Giả thuyết "kết hợp lexical cứu câu mà dense bỏ sót" được xác nhận.
2. **Agent v1, từ chối nhầm hàng loạt:** ở lần chạy đầu (`results/agent/dev_v1`), 5–10/16 câu dev có đáp án bị chuyển thành abstain (ví dụ dense_k3: 9 câu). Nguyên nhân (đọc `raw_answer`/`raw_citations` trong event `invalid_or_missing_citations`): model trả đúng đáp án và liệt kê ID hợp lệ trong `citations`, nhưng không ghi `[id]` trong câu trả lời, nên bộ kiểm tra nghiêm ngặt loại bỏ. **Sửa (agent v2):** (a) prompt bắt buộc ghi `[id]` cuối mỗi câu và kiểm tra đúng đối tượng (quốc gia, năm, chỉ số); (b) nếu mọi ID trong `citations` đều nằm trong context thì tự chèn marker còn thiếu và ghi event `citations_appended_inline`. ID ngoài context vẫn bị loại. Sau khi sửa, từ chối nhầm trên dev còn **0/16** cho cả 5 cấu hình.
3. **Agent, u01 bịa (dense):** câu "Thailand đặt mục tiêu năm nào" được trả lời "2047", lấy từ câu về India ở p006:c000. Ở v1, lỗi này bị chặn một cách tình cờ nhờ lỗi định dạng; ở v2 vẫn còn với dense_k3 (abstention dev 1/2). Các cấu hình hybrid và BM25 thì từ chối đúng. Prompt kiểm tra đối tượng chưa đủ với dense, vì context dense đưa đúng đoạn có năm 2047. Lỗi chưa xử lý triệt để; xem phần giới hạn.

Vì lỗi 2 được sửa **sau khi** đã xem kết quả test_v1, mình tạo bộ test mới và chỉ chạy test mới **sau khi** kiểm tra dev v2 (lệnh test bị khóa trong code nếu chưa có `selected_config.json`).

## Agent và đánh giá

- **Tool, số lượt gọi, điều kiện dừng, cách chọn context và xử lý lỗi:**
  - Agent có hai tool: `search_documents(query)` (retriever theo cấu hình) và `submit_answer(answer, citations, abstain)`, với `tool_choice=required` và một tool call mỗi lượt.
  - Tối đa **3 lượt search**; sau đó chỉ còn `submit_answer`, tối đa 5 lượt gọi model. Chọn mức 3 để đủ cho việc viết lại truy vấn mà vẫn chặn được vòng lặp. Trên dev, 17–18/18 câu chỉ cần 1 lượt.
  - Context tích lũy qua các lượt: dedup theo ID, theo thứ tự rank, có thêm chunk lân cận nếu cấu hình yêu cầu, tổng ≤ 6400 ký tự (~1600 token). Chunk vượt budget được ghi vào `dropped`.
  - Prompt nêu rõ tài liệu là dữ liệu, không phải chỉ dẫn.
  - Lỗi HTTP 429/5xx được retry 3 lần. Lỗi model hoặc vector store được ghi `status: error` và báo riêng. Số lỗi trong mọi lần chạy: **0**.

| Cấu hình / split | Tool use | Số lượt gọi (search: số câu) | Grounded answer 0/1/2 (TB /2) | Citation hợp lệ | Câu có citation | Abstention đúng | Từ chối nhầm |
|---|---|---|---|---|---|---|---|
| dense_k3 / dev (v2) | 18/18 | 1:17, 2:1 | 0/0/16 (2,00) | 18/19 (95%) | 17/17 | 1/2 | 0/16 |
| bm25_k3 / dev (v2) | 18/18 | 1:17, 2:1 | 0/1/15 (1,94) | 16/16 | 16/16 | 2/2 | 0/16 |
| hybrid_k3 / dev (v2) | 18/18 | 1:18 | 0/0/16 (2,00) | 17/17 | 16/16 | 2/2 | 0/16 |
| hybrid_rerank_k3 / dev (v2) | 18/18 | 1:17, 3:1 | 0/0/16 (2,00) | 18/18 | 16/16 | 2/2 | 0/16 |
| hybrid_k5_neighbors / dev (v2) | 18/18 | 1:18 | 0/0/16 (2,00) | 16/16 | 16/16 | 2/2 | 0/16 |
| dense_k3 / test_v1 (agent v1) | 8/8 | 1:5, 2:3 | 4/0/2 (0,67) | 4/4 | 3/3 | 2/2 | 3/6 |
| hybrid_k5_neighbors / test_v1 (agent v1) | 8/8 | 1:7, 2:1 | 3/0/3 (1,00) | 5/5 | 4/4 | 2/2 | 2/6 |
| **dense_k3 (baseline) / test** | 8/8 | 1:6, 3:2 | 1/0/5 (1,67) | 5/6 (83%) | 5/5 | 2/2 | 1/6 |
| **hybrid_k5_neighbors (đã chọn) / test** | 8/8 | 1:7, 3:1 | **0/0/6 (2,00)** | **6/6** | 6/6 | **2/2** | **0/6** |

Chấm context 0/1/2 (`context_grade`) trên test: baseline có 5 câu mức 2 và 1 câu mức 0 (n06); cấu hình chọn có 6 câu mức 2. Trên test_v1: baseline 4×2 + 2×0; cấu hình chọn 5×2 + 1×0.

| Query ID | Loại câu | Tool call và kết quả | Câu trả lời và citation | Nhãn, lý do |
|---|---|---|---|---|
| n06 (test, hybrid_k5) | Có đáp án, filter `spotlight` | 1 search "Spotlight section global population global GDP table S.1" → p018:c001 vào context | "…account for 62 percent of the global population and 72 percent of global GDP [B:wdr2024_part1:p018:c001]" | Grounded 2, citation đúng nguyên văn |
| x02 (test, hybrid_k5) | Thiếu evidence | 3 search ("carbon tax rate middle-income countries", "recommended carbon tax rate", …) → không có đoạn về thuế carbon | Từ chối, không đưa con số | Abstention đúng |
| n06 (test, dense_k3) | Lỗi: từ chối nhầm | 3 search dense có filter spotlight, không lấy được p018:c001 | Từ chối | Grounded 0: dense xếp chunk chứa "table S.1" thấp, lexical cần thiết |
| u01 (dev, dense_k3) | Lỗi: bịa | 2 search "Thailand high-income status target year…" → p006:c000 (India 2047, Viet Nam 2045) | "Thailand aims … by 2047 [p006:c000]" | Abstention sai, citation không hỗ trợ |
| t01 (test_v1, v1) | Lỗi: định dạng citation | 1 search → p030:c001 có "1.75 percent" | Model trả "1.75 percent" nhưng thiếu `[id]` → bị chuyển thành abstain | Grounded 0, nguyên nhân sửa ở v2 |

- **Đường dẫn trace, nhãn, lệnh chạy, thời gian và chi phí:**
  - Retrieval: `results/retrieval/{dev,test_v1,test}/<config>/{traces,summary}.json`.
  - Agent: `results/agent/{dev_v1,dev,test_v1,test}/<config>/{traces.json,auto_summary.json,review_sheet.md,reviews.json,metrics.json}`.
  - Cấu hình đã chốt: `results/selected_config.json`. Bảng tổng hợp: `results/report_tables.md`. Lệnh chạy: `RUN.md` (`run_all.bat`, `run_v2.bat`, `run_test_v2.bat`).
  - Thời gian agent: median 2,2–3,0 s/câu (rerank 5,0 s).
  - Chi phí: ~$0,005–0,007 cho 18 câu dev mỗi cấu hình, $0,0033 (baseline) và $0,0038 (đã chọn) cho test. Tổng tất cả lần chạy agent: **$0,068**, tính theo giá `gpt-4o-mini` $0,15/1M token vào và $0,60/1M token ra.
- **Kết quả trước/sau, đánh đổi và giới hạn:**
  - Trên test độc lập, cấu hình chọn đạt grounded 2,00/2, abstention 2/2, không từ chối nhầm. Baseline đạt 1,67/2 với 1 từ chối nhầm và 1 citation sai.
  - Sửa agent (v1 → v2) có tác động lớn hơn đổi retrieval: trên dev, từ chối nhầm giảm từ 5–10/16 xuống 0/16.
  - Đánh đổi: hybrid_k5_neighbors dùng nhiều token hơn ~50% so với hybrid_k3 trên dev (38,5k so với 25,2k token vào) để đổi lấy context rộng hơn, độ trễ gần như không đổi. Rerank không đáng chi phí thời gian.
  - **Giới hạn:**
    - Benchmark nhỏ (6 câu test độc lập; 1 câu = 17 điểm %), nên chênh lệch giữa các cấu hình trên dev phần lớn nằm trong sai số.
    - Chỉ có một tài liệu tiếng Anh.
    - Metric khớp nguyên văn không nhận evidence tương đương ở chunk khác (q14, q04 rerank); các trường hợp này đã được đọc tay.
    - BM25 không stemming.
    - Lỗi bịa kiểu u01 vẫn còn với dense, chưa có bước verifier.
    - test_v1 đã được xem trước khi sửa agent nên chỉ để tham khảo.
    - Nhãn do AI đề xuất, cần sinh viên kiểm tra lại.

## Thử thách nâng cao

Không thực hiện: tài liệu Day 6 chỉ có 44 trang, không đủ điều kiện 100 trang có bảng, ảnh và biểu đồ.
