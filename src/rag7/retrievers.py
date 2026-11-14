"""Retrieval methods: dense (Day 6 pgvector), BM25, hybrid RRF and cross-encoder rerank.

Every retriever returns ranked dicts with: id, text, source_id, source, page,
metadata, score, rank, method (+ component ranks for fusion). Errors propagate;
there is no fallback to fake vectors or fake results.
"""
import math
import sys
import time
from collections import Counter
from typing import Any

from . import config
from .data import tokenize

ALLOWED_FILTERS = {'section', 'document_id', 'page'}

# Small English stopword list (corpus is English); kept explicit for reproducibility.
STOPWORDS = set('''a an and are as at be by did do does for from has have how in into is it its of on or
that the their this to was were what when where which who why with according'''.split())


def _check_filters(filters: dict | None) -> dict:
    filters = dict(filters or {})
    bad = set(filters) - ALLOWED_FILTERS
    if bad:
        raise ValueError(f'filter không được phép: {sorted(bad)}')
    return filters


def _matches(chunk: dict, filters: dict) -> bool:
    for key, value in filters.items():
        actual = chunk['source_id'] if key == 'document_id' else chunk['page'] if key == 'page' else chunk['metadata'].get(key)
        if actual != value:
            return False
    return True


def _ranked(rows: list[dict], method: str) -> list[dict]:
    return [{**r, 'rank': i + 1, 'method': method} for i, r in enumerate(rows)]


class BM25Retriever:
    """Okapi BM25 over the exported Day 6 chunks (same corpus / chunk IDs as the vector index)."""
    name = 'bm25'

    def __init__(self, chunks: list[dict], k1: float = 1.5, b: float = 0.75, stopwords: bool = True):
        self.chunks, self.k1, self.b = chunks, k1, b
        self.stop = STOPWORDS if stopwords else set()
        self.docs = [Counter(t for t in tokenize(c['text']) if t not in self.stop) for c in chunks]
        self.lengths = [sum(d.values()) for d in self.docs]
        self.avgdl = sum(self.lengths) / max(len(self.lengths), 1)
        df = Counter(t for d in self.docs for t in d)
        n = len(chunks)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def search(self, query: str, *, filters: dict | None = None, top_k: int = 3) -> list[dict]:
        filters = _check_filters(filters)
        terms = [t for t in tokenize(query) if t not in self.stop]
        scored = []
        for chunk, doc, length in zip(self.chunks, self.docs, self.lengths):
            if filters and not _matches(chunk, filters):
                continue
            s = 0.0
            for t in terms:
                f = doc.get(t)
                if f:
                    s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * length / self.avgdl))
            if s > 0:
                scored.append({**chunk, 'score': s})
        scored.sort(key=lambda c: (-c['score'], c['id']))
        return _ranked(scored[:top_k], self.name)


class DenseRetriever:
    """Query the Day 6 PostgreSQL + pgvector index with the Day 6 embedder (E5 'query: ' prefix)."""
    name = 'dense'

    def __init__(self, strategy: str = 'B'):
        config.load_env()
        if str(config.DAY6_STARTER) not in sys.path:
            sys.path.insert(0, str(config.DAY6_STARTER))
        try:
            from src import config as day6_config            # Day 6 package
            from src.embeddings import MyEmbedder
            from src.store import PgVectorStore
        except ImportError as exc:
            raise RuntimeError(f'Không import được code Day 6 tại {config.DAY6_STARTER}: {exc}. '
                               'Đặt DAY6_DIR và chạy bằng venv Day 6.') from exc
        t0 = time.perf_counter()
        self.embedder = MyEmbedder(day6_config.EMBEDDING_MODEL)
        self.model_load_seconds = time.perf_counter() - t0
        self.store = PgVectorStore(day6_config.DATABASE_URL, self.embedder.dimensions)
        self.strategy = strategy
        self.describe = {**self.embedder.describe(), 'vector_store': 'PostgreSQL + pgvector (Day 6)',
                         'index_strategy': strategy, 'distance': 'cosine <=> (exact)'}

    def search(self, query: str, *, filters: dict | None = None, top_k: int = 3) -> list[dict]:
        filters = _check_filters(filters)
        vector = self.embedder.embed_query(query)
        rows = self.store.search(self.strategy, vector, top_k=top_k, filters=filters)
        out = [{'id': r['chunk_id'], 'text': r['text'], 'source_id': r['document_id'], 'source': r['source'],
                'page': r['page'], 'metadata': {'section': r.get('section'), 'printed_page': r.get('printed_page')},
                'score': r['score']} for r in rows]
        return _ranked(out, self.name)

    def export_chunks(self) -> list[dict]:
        """Read every chunk of the chosen strategy from pgvector (used to build the lexical index)."""
        with self.store._connect() as conn:
            rows = conn.execute(
                'SELECT chunk_id, document_id, source, page, printed_page, section, char_start, char_end, text, model_name '
                'FROM chunks WHERE strategy=%s ORDER BY chunk_id', (self.strategy,)).fetchall()
        return [{'id': r[0], 'text': r[8], 'source_id': r[1], 'source': r[2], 'page': r[3],
                 'metadata': {'section': r[5], 'printed_page': r[4], 'char_start': r[6], 'char_end': r[7],
                              'index_strategy': self.strategy, 'embedding_model': r[9]}} for r in rows]


class HybridRRF:
    """Reciprocal Rank Fusion of dense and BM25 rankings (rank-based, so no score normalisation needed)."""
    name = 'hybrid'

    def __init__(self, dense, lexical, candidates: int = 20, rrf_k: int = 60):
        self.dense, self.lexical, self.candidates, self.rrf_k = dense, lexical, candidates, rrf_k

    def search(self, query: str, *, filters: dict | None = None, top_k: int = 3) -> list[dict]:
        fused: dict[str, dict] = {}
        for retr in (self.dense, self.lexical):
            for r in retr.search(query, filters=filters, top_k=self.candidates):
                item = fused.setdefault(r['id'], {**{k: r[k] for k in ('id', 'text', 'source_id', 'source', 'page', 'metadata')},
                                                  'score': 0.0, 'components': {}})
                item['score'] += 1.0 / (self.rrf_k + r['rank'])
                item['components'][retr.name] = {'rank': r['rank'], 'score': r['score']}
        rows = sorted(fused.values(), key=lambda c: (-c['score'], c['id']))
        return _ranked(rows[:top_k], self.name)


class CrossEncoderRerank:
    """Take a larger candidate list from a base retriever, rerank with a cross-encoder."""
    name = 'rerank'

    def __init__(self, base, model_name: str, candidates: int = 20):
        from sentence_transformers import CrossEncoder
        t0 = time.perf_counter()
        self.model = CrossEncoder(model_name, device='cpu')
        self.model_load_seconds = time.perf_counter() - t0
        self.base, self.model_name, self.candidates = base, model_name, candidates

    def search(self, query: str, *, filters: dict | None = None, top_k: int = 3) -> list[dict]:
        cands = self.base.search(query, filters=filters, top_k=self.candidates)
        if not cands:
            return []
        scores = self.model.predict([(query, c['text']) for c in cands])
        rows = [{**c, 'pre_rerank_rank': c['rank'], 'pre_rerank_score': c['score'], 'score': float(s)}
                for c, s in zip(cands, scores)]
        rows.sort(key=lambda c: (-c['score'], c['id']))
        return _ranked(rows[:top_k], f'{self.base.name}+rerank')


def build_retriever(cfg: dict, chunks: list[dict], cache: dict[str, Any] | None = None):
    """Build from a config dict; expensive components (embedder, reranker) are cached across configs."""
    cache = cache if cache is not None else {}
    method = cfg['method']

    def dense():
        if 'dense' not in cache:
            cache['dense'] = DenseRetriever(cfg.get('index_strategy', 'B'))
        return cache['dense']

    def bm25():
        if 'bm25' not in cache:
            cache['bm25'] = BM25Retriever(chunks)
        return cache['bm25']

    if method == 'dense':
        return dense()
    if method == 'bm25':
        return bm25()
    if method in ('hybrid', 'hybrid_rerank'):
        hybrid = HybridRRF(dense(), bm25(), cfg.get('candidates', 20), cfg.get('rrf_k', 60))
        if method == 'hybrid':
            return hybrid
        key = ('rerank', cfg['reranker'])
        if key not in cache:
            cache[key] = CrossEncoderRerank(hybrid, cfg['reranker'], cfg.get('rerank_candidates', 20))
        cache[key].base = hybrid
        return cache[key]
    raise ValueError(f'method không hỗ trợ: {method}')
