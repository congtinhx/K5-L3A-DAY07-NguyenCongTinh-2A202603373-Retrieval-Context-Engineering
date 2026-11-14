"""Experiment commands: export, check, retrieval benchmark, selection, agent benchmark, review, metrics, report."""
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from . import config
from .config import read_json, write_json
from .context import render, select_context
from .data import evidence_hit, is_answerable, public_question, validate_chunks, validate_questions
from .retrievers import DenseRetriever, build_retriever


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')


def load_chunks() -> list[dict]:
    chunks = read_json(config.CHUNKS_FILE)
    validate_chunks(chunks)
    return chunks


def load_questions(split: str | None = None) -> list[dict]:
    qs = read_json(config.QUESTIONS_FILE)
    return [q for q in qs if split is None or q['split'] == split]


def ratio(n: int, d: int) -> dict:
    return {'n': n, 'N': d, 'rate': round(n / d, 4) if d else None}


# ------------------------------------------------------------------ data
def export_chunks(source: str = 'db', strategy: str = 'B') -> dict:
    """db: read the real Day 6 pgvector table. pdf: re-run Day 6 ingestion+chunking code (no DB needed)."""
    if source == 'db':
        retriever = DenseRetriever(strategy)
        chunks = retriever.export_chunks()
        meta = {'exported_from': 'Day 6 PostgreSQL+pgvector table `chunks`', **retriever.describe}
    else:
        if str(config.DAY6_STARTER) not in sys.path:
            sys.path.insert(0, str(config.DAY6_STARTER))
        from src.run import build_chunks, load_pages   # Day 6 code
        pages, _errors = load_pages()
        chunks = [{'id': c.chunk_id, 'text': c.text, 'source_id': c.document_id, 'source': c.source, 'page': c.page,
                   'metadata': {'section': c.metadata.get('section'), 'printed_page': c.metadata.get('printed_page'),
                                'char_start': c.metadata.get('char_start'), 'char_end': c.metadata.get('char_end'),
                                'index_strategy': strategy}} for c in build_chunks(strategy, pages)]
        chunks.sort(key=lambda c: c['id'])
        meta = {'exported_from': 'Day 6 code (src.run.load_pages + build_chunks) re-run on doc1.pdf'}
    validate_chunks(chunks)
    write_json(config.CHUNKS_FILE, chunks)
    info = {'exported_at': now(), 'chunks': len(chunks), 'strategy': strategy, **meta}
    write_json(config.RESULTS_DIR / 'chunk_export.json', info)
    return info


def check(db: bool = False) -> dict:
    chunks = load_chunks()
    stats = validate_questions(load_questions(), chunks)
    out = {'chunks': len(chunks), 'benchmark': stats}
    if db:
        retr = DenseRetriever('B')
        db_chunks = {c['id']: c['text'] for c in retr.export_chunks()}
        file_chunks = {c['id']: c['text'] for c in chunks}
        out['db_chunks'] = len(db_chunks)
        out['db_matches_file'] = db_chunks == file_chunks
        out['embedder'] = retr.describe
        out['dense_smoke_test'] = [r['id'] for r in retr.search('middle-income trap', top_k=3)]
        write_json(config.RESULTS_DIR / 'check_db.json', out)
    return out


# ------------------------------------------------------------------ retrieval benchmark
def eval_retrieval(split: str, names: list[str]) -> dict:
    exp = config.load_experiments()
    chunks = load_chunks()
    by_id = {c['id']: c for c in chunks}
    questions = load_questions(split)
    validate_questions(questions, chunks)
    if split.startswith('test'):
        names = _guard_test(names, exp)
    cache: dict = {}
    summaries = {}
    for name in names:
        cfg = {'index_strategy': exp.get('index_strategy', 'B'), **exp['retrieval_configs'][name]}
        t0 = time.perf_counter()
        retriever = build_retriever(cfg, chunks, cache)
        build_s = time.perf_counter() - t0
        traces = []
        for q in questions:
            pq = public_question(q)                       # no gold reaches the retriever
            t1 = time.perf_counter()
            results = retriever.search(pq['question'], filters=pq['filter'], top_k=max(cfg['top_k'], 3))
            ranked_ms = (time.perf_counter() - t1) * 1000
            top = results[:cfg['top_k']]
            ctx, dropped = select_context(top, budget_chars=cfg['budget_chars'],
                                          policy=cfg.get('context', 'rank'), by_id=by_id)
            row = {'query_id': q['id'], 'split': split, 'question': q['question'], 'filter': q.get('filter'),
                   'answerable': is_answerable(q), 'config': name, 'latency_ms': round(ranked_ms, 1),
                   'results': [{'id': r['id'], 'rank': r['rank'], 'score': round(r['score'], 5), 'page': r['page'],
                                'section': r['metadata'].get('section'), 'components': r.get('components'),
                                'pre_rerank_rank': r.get('pre_rerank_rank')} for r in results],
                   'context_ids': [c['id'] for c in ctx], 'context_chars': len(render(ctx)), 'dropped': dropped}
            if row['answerable']:
                gold = q['gold']
                hits = [evidence_hit(r, gold) for r in results]
                row.update({'hit1': bool(hits[:1] and hits[0]), 'hit3': any(hits[:3]),
                            'first_hit_rank': next((i + 1 for i, h in enumerate(hits) if h), None),
                            'context_hit': any(evidence_hit(c, gold) for c in ctx)})
            traces.append(row)
        ans = [t for t in traces if t['answerable']]
        lat = sorted(t['latency_ms'] for t in traces)
        summary = {'config': name, 'split': split, 'settings': cfg, 'run_at': now(),
                   'answerable': len(ans), 'unanswerable_excluded': len(traces) - len(ans),
                   'hit1': ratio(sum(t['hit1'] for t in ans), len(ans)),
                   'evidence_hit3': ratio(sum(t['hit3'] for t in ans), len(ans)),
                   'context_evidence_rate': ratio(sum(t['context_hit'] for t in ans), len(ans)),
                   'mrr_at_k': round(sum(1 / t['first_hit_rank'] for t in ans if t['first_hit_rank']) / len(ans), 4) if ans else None,
                   'avg_context_chars': round(statistics.mean(t['context_chars'] for t in traces), 1),
                   'median_latency_ms': round(statistics.median(lat), 1),
                   'p95_latency_ms': round(lat[int(0.95 * (len(lat) - 1))], 1),
                   'build_seconds': round(build_s, 2), 'cost_usd': 0.0,
                   'misses_hit3': [t['query_id'] for t in ans if not t['hit3']],
                   'misses_context': [t['query_id'] for t in ans if not t['context_hit']]}
        out_dir = config.RESULTS_DIR / 'retrieval' / split / name
        write_json(out_dir / 'traces.json', traces)
        write_json(out_dir / 'summary.json', summary)
        summaries[name] = summary
        print(f"{name:22s} Hit@1 {summary['hit1']['n']}/{summary['hit1']['N']}  "
              f"Hit@3 {summary['evidence_hit3']['n']}/{summary['evidence_hit3']['N']}  "
              f"Ctx {summary['context_evidence_rate']['n']}/{summary['context_evidence_rate']['N']}  "
              f"{summary['median_latency_ms']} ms")
    all_path = config.RESULTS_DIR / 'retrieval' / split / 'summary.json'
    merged = read_json(all_path) if all_path.exists() else {}
    merged.update(summaries)
    write_json(all_path, merged)
    return summaries


def _guard_test(names: list[str], exp: dict) -> list[str]:
    if not config.SELECTED_FILE.exists():
        raise SystemExit('Chưa chốt cấu hình trên dev: chạy `python run.py select` trước khi chạy test.')
    selected = read_json(config.SELECTED_FILE)['selected']
    allowed = {exp['baseline'], selected}
    names = [selected if n == 'selected' else exp['baseline'] if n == 'baseline' else n for n in names]
    extra = set(names) - allowed
    if extra:
        raise SystemExit(f'Test chỉ chạy baseline và cấu hình đã chốt {sorted(allowed)}; không chạy {sorted(extra)}.')
    return list(dict.fromkeys(names))


# ------------------------------------------------------------------ selection (dev only)
def select() -> dict:
    exp = config.load_experiments()
    dev = read_json(config.RESULTS_DIR / 'retrieval' / 'dev' / 'summary.json')
    order = list(exp['retrieval_configs'])
    missing = [n for n in order if n not in dev]
    if missing:
        raise SystemExit(f'Thiếu kết quả dev cho {missing}')

    def key(name):
        s = dev[name]
        return (-s['context_evidence_rate']['n'], -s['evidence_hit3']['n'], -s['hit1']['n'],
                s['median_latency_ms'], order.index(name))
    ranking = sorted(order, key=key)
    result = {'selected': ranking[0], 'selected_at': now(), 'criteria': exp['selection_criteria'],
              'ranking': [{'config': n, 'context': dev[n]['context_evidence_rate'], 'hit3': dev[n]['evidence_hit3'],
                           'hit1': dev[n]['hit1'], 'median_latency_ms': dev[n]['median_latency_ms']} for n in ranking],
              'note': 'Chọn chỉ từ kết quả dev; test chưa được chạy tại thời điểm chốt.'}
    if (config.RESULTS_DIR / 'retrieval' / 'test').exists() or (config.RESULTS_DIR / 'agent' / 'test').exists():
        result['warning'] = 'Đã có kết quả test trước khi chốt — cần ghi rõ trong báo cáo.'
    write_json(config.SELECTED_FILE, result)
    return result


# ------------------------------------------------------------------ agent benchmark
def run_agent_bench(split: str, names: list[str], limit: int | None = None) -> dict:
    from .agent import run_agent
    from .llm import OpenAIChat
    config.load_env()
    exp = config.load_experiments()
    agent_cfg = exp['agent']
    chunks = load_chunks()
    by_id = {c['id']: c for c in chunks}
    questions = load_questions(split)[:limit] if limit else load_questions(split)
    if split.startswith('test'):
        names = _guard_test(names, exp)
    llm = OpenAIChat(agent_cfg['model'], temperature=agent_cfg.get('temperature', 0))
    cache: dict = {}
    out = {}
    for name in names:
        cfg = {'index_strategy': exp.get('index_strategy', 'B'), **exp['retrieval_configs'][name]}
        retriever = build_retriever(cfg, chunks, cache)
        traces = []
        for q in questions:
            pq = public_question(q)
            t = run_agent(pq['question'], llm, retriever, filters=pq['filter'], top_k=cfg['top_k'],
                          budget_chars=agent_cfg['budget_chars'], context_policy=cfg.get('context', 'rank'),
                          max_searches=agent_cfg['max_searches'], by_id=by_id)
            t = {'query_id': q['id'], 'split': split, 'question': q['question'], 'answerable': is_answerable(q),
                 'retrieval_config': name, 'model': agent_cfg['model'], **t}
            t['split'] = split
            if t['answerable']:     # scoring only, after the run
                t['context_has_evidence'] = any(evidence_hit(by_id[i], q['gold']) for i in t['context_ids'])
            traces.append(t)
            print(f"[{name}] {q['id']}: {t['status']:8s} searches={t['searches']} cites={t['citations']}")
        summary = agent_summary(traces, agent_cfg, name, split)
        d = config.RESULTS_DIR / 'agent' / split / name
        write_json(d / 'traces.json', traces)
        write_json(d / 'auto_summary.json', summary)
        write_review_files(d, traces, questions, by_id)
        out[name] = summary
    return out


def agent_summary(traces: list[dict], agent_cfg: dict, name: str, split: str) -> dict:
    ok = [t for t in traces if t['status'] != 'error']
    ans = [t for t in ok if t['answerable']]
    una = [t for t in ok if not t['answerable']]
    costs = [t['usage']['cost_usd'] for t in traces if t['usage'].get('cost_usd') is not None]
    return {'config': name, 'split': split, 'agent': agent_cfg,
            'agent_version': traces[0].get('agent_version', 1) if traces else None, 'run_at': now(), 'cases': len(traces),
            'provider_errors': len(traces) - len(ok),
            'errors': [{'query_id': t['query_id'], 'event': t['events'][-1]} for t in traces if t['status'] == 'error'],
            'status': {s: sum(t['status'] == s for t in traces) for s in ('answered', 'abstain', 'error')},
            'tool_use': ratio(sum(t['searches'] > 0 for t in ok), len(ok)),
            'searches_distribution': {str(k): sum(t['searches'] == k for t in ok) for k in sorted({t['searches'] for t in ok})},
            'agent_context_evidence_rate': ratio(sum(t.get('context_has_evidence', False) for t in ans), len(ans)),
            'answered_with_citation': ratio(sum(t['status'] == 'answered' and bool(t['citations']) for t in ok),
                                            sum(t['status'] == 'answered' for t in ok)),
            'abstain_on_unanswerable_auto': ratio(sum(t['status'] == 'abstain' for t in una), len(una)),
            'abstain_on_answerable_auto': ratio(sum(t['status'] == 'abstain' for t in ans), len(ans)),
            'median_latency_s': round(statistics.median(t['elapsed_s'] for t in traces), 2) if traces else None,
            'avg_context_chars': round(statistics.mean(t['context_chars'] for t in ok), 1) if ok else None,
            'tokens': {'prompt': sum(t['usage']['prompt_tokens'] for t in traces),
                       'completion': sum(t['usage']['completion_tokens'] for t in traces)},
            'cost_usd_total': round(sum(costs), 5) if costs else None,
            'note': 'Tự động đếm theo status; nhãn grounded/citation/abstention phải chấm tay trong reviews.json.'}


def write_review_files(d: Path, traces: list[dict], questions: list[dict], by_id: dict) -> None:
    qmap = {q['id']: q for q in questions}
    lines = [f'# Review sheet — {d.parent.name}/{d.name}', '',
             'Đọc từng câu: chấm `answer_grade` (0/1/2, câu có đáp án), `citation_support` (true/false cho từng citation), '
             '`abstention_correct` (câu thiếu evidence), `context_grade` (0/1/2), ghi `reason`. '
             'ID hợp lệ chưa chứng minh nguồn hỗ trợ — phải đọc đoạn trích.', '']
    skeleton = []
    for t in traces:
        q = qmap[t['query_id']]
        lines += [f"## {t['query_id']} — {'có đáp án' if t['answerable'] else 'THIẾU evidence'} — status: {t['status']}",
                  f"**Câu hỏi:** {q['question']}  ", f"**Filter người dùng:** {q.get('filter')}  "]
        if t['answerable']:
            lines.append(f"**Đáp án chuẩn (chỉ để chấm):** {q['expected_answer']} — evidence: "
                         + ' | '.join(f"p{g['page']}: “{g['evidence']}”" for g in q['gold']) + '  ')
        else:
            lines.append(f"**Lý do thiếu evidence:** {q['absence_reason']}  ")
        lines.append(f"**Queries:** {[e['query'] for e in t['events'] if e.get('event') == 'search']}  ")
        lines.append(f"**Context ({t['context_chars']} ký tự):** {t['context_ids']}  ")
        lines += ['', f"**Trả lời:** {t['answer']}", '']
        for cid in t['citations']:
            lines.append(f"> `{cid}` (p{by_id[cid]['page']}): {by_id[cid]['text']}")
            lines.append('')
        if t['status'] == 'error':
            continue                                    # provider errors need no label
        rec = {'query_id': t['query_id'], 'citation_support': [None] * len(t['citations']),
               'context_grade': None, 'reason': ''}
        if t['answerable']:
            rec['answer_grade'] = None
        else:
            rec['abstention_correct'] = None
        skeleton.append(rec)
    (d / 'review_sheet.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    if not (d / 'reviews.json').exists():               # never overwrite human labels
        write_json(d / 'reviews_template.json', skeleton)


def _resolve(name: str) -> str:
    exp = config.load_experiments()
    if name == 'baseline':
        return exp['baseline']
    if name == 'selected':
        return read_json(config.SELECTED_FILE)['selected']
    return name


def metrics(split: str, name: str) -> dict:
    """Aggregate human labels with starter/agent_metrics.py, plus auto stats."""
    sys.path.insert(0, str(config.ROOT / 'starter'))
    from agent_metrics import aggregate
    name = _resolve(name)
    d = config.RESULTS_DIR / 'agent' / split / name
    traces = read_json(d / 'traces.json')
    reviews = read_json(d / 'reviews.json')
    ids = {t['query_id'] for t in traces}
    cases = [{'id': q['id'], 'split': q['split'], 'answerable': is_answerable(q)}
             for q in load_questions(split) if q['id'] in ids]
    result = {'split': split, 'config': name, **aggregate(cases, traces, reviews)}
    grades = [r.get('context_grade') for r in reviews if r.get('context_grade') is not None]
    result['context_grade'] = {**{str(g): grades.count(g) for g in (0, 1, 2)}, 'N': len(grades)}
    result['auto'] = read_json(d / 'auto_summary.json')
    write_json(d / 'metrics.json', result)
    return result


# ------------------------------------------------------------------ report tables
def _fmt(r):
    if not r or not r.get('N'):
        return '0/0 (n/a)'
    return f"{r['n']}/{r['N']} ({r['n'] / r['N']:.0%})"


def report_tables() -> str:
    exp = config.load_experiments()
    lines = ['# Bảng kết quả (sinh tự động từ results/)', '']
    for split in ('dev', 'test_v1', 'test'):
        p = config.RESULTS_DIR / 'retrieval' / split / 'summary.json'
        if not p.exists():
            continue
        lines += [f'## Retrieval — {split}', '',
                  '| Cấu hình | Phương pháp, top-k, context | Hit@1 | Evidence Hit@3 | Context Evidence Rate | MRR | Ctx chars TB | Median ms | Chi phí |',
                  '|---|---|---|---|---|---|---|---|---|']
        for name, s in read_json(p).items():
            st = s['settings']
            desc = (f"{st['method']}, k={st['top_k']}, cand={st.get('candidates', '-')}, "
                    f"{st.get('context', 'rank')}, budget={st['budget_chars']}")
            lines.append(f"| {name} | {desc} | {_fmt(s['hit1'])} | {_fmt(s['evidence_hit3'])} | "
                         f"{_fmt(s['context_evidence_rate'])} | {s['mrr_at_k']} | {s['avg_context_chars']} | "
                         f"{s['median_latency_ms']} | $0 |")
        lines.append('')
    for split in ('dev_v1', 'dev', 'test_v1', 'test'):
        base = config.RESULTS_DIR / 'agent' / split
        if not base.exists():
            continue
        lines += [f'## Agent — {split}', '',
                  '| Cấu hình | Tool use | Số lượt search | Grounded 0/1/2 (TB /2) | Citation hợp lệ | Câu có citation | '
                  'Abstention đúng | Từ chối nhầm | Ctx evidence | Median s | Token in/out | Chi phí |',
                  '|---|---|---|---|---|---|---|---|---|---|---|---|']
        for d in sorted(x for x in base.iterdir() if x.is_dir()):
            a = read_json(d / 'auto_summary.json')
            m = read_json(d / 'metrics.json') if (d / 'metrics.json').exists() else None
            if m:
                g = m['grounded_answer']
                grounded = f"{g['0']}/{g['1']}/{g['2']} ({g['mean']:.2f})" if g['mean'] is not None else 'n/a'
                cit = _fmt(m['citation_validity'])
                cov = _fmt(m['answer_citation_coverage'])
                abst = _fmt(m['abstention'])
                false_abs = _fmt(m['false_abstention'])
            else:
                grounded = cit = cov = abst = false_abs = 'chưa chấm'
            cost = a['cost_usd_total']
            lines.append(f"| {d.name} | {_fmt(a['tool_use'])} | {a['searches_distribution']} | {grounded} | {cit} | {cov} | "
                         f"{abst} | {false_abs} | {_fmt(a['agent_context_evidence_rate'])} | {a['median_latency_s']} | "
                         f"{a['tokens']['prompt']}/{a['tokens']['completion']} | "
                         f"{'$%.4f' % cost if cost is not None else 'n/a'} |")
        lines.append('')
    if config.SELECTED_FILE.exists():
        s = read_json(config.SELECTED_FILE)
        lines += [f"Cấu hình chốt trên dev: **{s['selected']}** (lúc {s['selected_at']}). Baseline: **{exp['baseline']}**.", '']
    text = '\n'.join(lines)
    (config.RESULTS_DIR / 'report_tables.md').write_text(text + '\n', encoding='utf-8')
    return text
