"""Benchmark loading, validation and evidence matching (gold is used ONLY for scoring)."""
import re
import unicodedata

# test_v1 = first test set; it was seen before the agent v2 fix, so a new `test` set was written.
SPLITS = ('dev', 'test', 'test_v1')
CHUNK_KEYS = ('id', 'text', 'source_id', 'source', 'page', 'metadata')


def tokenize(text: str) -> list[str]:
    return re.findall(r'\w+', unicodedata.normalize('NFKC', text).casefold())


def validate_chunks(chunks: list[dict]) -> None:
    if not isinstance(chunks, list) or not chunks:
        raise ValueError('chunks phải là JSON array không rỗng')
    seen = set()
    for c in chunks:
        missing = [k for k in CHUNK_KEYS if k not in c or c[k] is None]
        if missing:
            raise ValueError(f'chunk {c.get("id")} thiếu {missing}')
        if c['id'] in seen:
            raise ValueError(f'chunk ID trùng: {c["id"]}')
        seen.add(c['id'])


def is_answerable(q: dict) -> bool:
    return q.get('answerable', True) is not False


def evidence_hit(chunk: dict, gold: list[dict]) -> bool:
    """Same definition as starter/baseline.py: evidence fully inside a chunk of the right source+page."""
    return any(chunk['source_id'] == g['source_id'] and chunk['page'] == g['page'] and g['evidence'] in chunk['text']
               for g in gold)


def validate_questions(questions: list[dict], chunks: list[dict]) -> dict:
    ids, stats = set(), {sp: {'answerable': 0, 'unanswerable': 0} for sp in SPLITS}
    for q in questions:
        qid = q.get('id')
        if not isinstance(qid, str) or qid in ids:
            raise ValueError(f'question id không hợp lệ/trùng: {qid}')
        ids.add(qid)
        if q.get('split') not in SPLITS or not q.get('question', '').strip():
            raise ValueError(f'{qid}: split/question không hợp lệ')
        if is_answerable(q):
            if not q.get('expected_answer') or not q.get('gold'):
                raise ValueError(f'{qid}: câu có đáp án cần expected_answer và gold')
            for g in q['gold']:
                if not any(evidence_hit(c, [g]) for c in chunks):
                    raise ValueError(f'{qid}: evidence không nằm trọn trong chunk đúng nguồn/trang: {g}')
            stats[q['split']]['answerable'] += 1
        else:
            if q.get('expected_behavior') != 'search_and_abstain' or not q.get('absence_reason'):
                raise ValueError(f'{qid}: câu thiếu evidence cần expected_behavior và absence_reason')
            stats[q['split']]['unanswerable'] += 1
    return stats


def public_question(q: dict) -> dict:
    """What the agent/retriever may see: question text and the user-provided filter only."""
    return {'id': q['id'], 'question': q['question'], 'filter': q.get('filter')}
