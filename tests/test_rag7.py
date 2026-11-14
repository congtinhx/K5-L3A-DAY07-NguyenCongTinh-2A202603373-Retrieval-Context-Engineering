"""Offline tests for src/rag7 (fake model/dense adapters only test code paths, not quality)."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from rag7 import config, experiments as ex                      # noqa: E402
from rag7.agent import run_agent                                  # noqa: E402
from rag7.context import neighbour_ids, select_context            # noqa: E402
from rag7.data import evidence_hit, public_question, validate_questions  # noqa: E402
from rag7.llm import ProviderError, cost_usd                      # noqa: E402
from rag7.retrievers import BM25Retriever, HybridRRF              # noqa: E402


def chunk(cid, text, page=1, section='s1'):
    return {'id': cid, 'text': text, 'source_id': 'doc', 'source': 'doc.pdf', 'page': page,
            'metadata': {'section': section}}


CHUNKS = [chunk('B:doc:p001:c000', 'Refunds are processed within seven working days.'),
          chunk('B:doc:p001:c001', 'Shipping takes three days for domestic orders.'),
          chunk('B:doc:p002:c000', 'Korea raised R&D spending to 1.6 percent of GDP.', page=2, section='s2')]


class FakeDense:
    name = 'dense'

    def __init__(self, order): self.order = order

    def search(self, query, *, filters=None, top_k=3):
        rows = [c for c in CHUNKS if c['id'] in self.order]
        rows.sort(key=lambda c: self.order.index(c['id']))
        return [{**c, 'score': 1 - i / 10, 'rank': i + 1, 'method': 'dense'} for i, c in enumerate(rows[:top_k])]


class FakeLLM:
    """Replays scripted tool calls in OpenAI response format."""
    model = 'gpt-4o-mini'

    def __init__(self, calls): self.calls, self.seen = list(calls), []

    def chat(self, messages, tools, tool_choice='required'):
        self.seen.append([t['function']['name'] for t in tools])
        item = self.calls.pop(0)
        if isinstance(item, Exception):
            raise item
        name, args = item
        return {'choices': [{'message': {'content': None, 'tool_calls': [
            {'id': f'call{len(self.seen)}', 'type': 'function',
             'function': {'name': name, 'arguments': json.dumps(args)}}]}}],
                'usage': {'prompt_tokens': 100, 'completion_tokens': 10}}


class RetrievalTests(unittest.TestCase):
    def test_bm25_ranks_and_filters(self):
        bm = BM25Retriever(CHUNKS)
        self.assertEqual(bm.search('how long do refunds take')[0]['id'], 'B:doc:p001:c000')
        self.assertEqual([r['id'] for r in bm.search('refunds Korea', filters={'section': 's2'})], ['B:doc:p002:c000'])
        self.assertEqual(bm.search('zzzz'), [])
        with self.assertRaises(ValueError):
            bm.search('x', filters={'gold': 1})

    def test_rrf_fuses_both_rankings(self):
        bm = BM25Retriever(CHUNKS)
        dense = FakeDense(['B:doc:p002:c000', 'B:doc:p001:c000', 'B:doc:p001:c001'])
        res = HybridRRF(dense, bm, candidates=3).search('refunds seven days', top_k=3)
        self.assertEqual([r['rank'] for r in res], [1, 2, 3])
        self.assertEqual(res[0]['id'], 'B:doc:p001:c000')          # 1st in BM25 + 2nd in dense beats 1st in dense only
        self.assertIn('bm25', res[0]['components'])

    def test_context_budget_dedup_and_neighbours(self):
        by_id = {c['id']: c for c in CHUNKS}
        ranked = [{**CHUNKS[0], 'rank': 1}, {**CHUNKS[0], 'rank': 2}]
        sel, _ = select_context(ranked, budget_chars=10_000, policy='rank_neighbors', by_id=by_id)
        self.assertEqual([c['id'] for c in sel], ['B:doc:p001:c000', 'B:doc:p001:c001'])
        sel, dropped = select_context(ranked, budget_chars=20)
        self.assertEqual(sel, [])
        self.assertTrue(dropped)
        self.assertEqual(neighbour_ids('B:doc:p001:c000'), ['B:doc:p001:c001'])

    def test_evidence_hit_needs_page_and_text(self):
        gold = [{'source_id': 'doc', 'page': 2, 'evidence': '1.6 percent'}]
        self.assertTrue(evidence_hit(CHUNKS[2], gold))
        self.assertFalse(evidence_hit({**CHUNKS[2], 'page': 3}, gold))

    def test_public_question_hides_gold(self):
        q = {'id': 'q', 'question': 'x?', 'gold': [1], 'expected_answer': 'y', 'filter': {'section': 's'}}
        self.assertEqual(set(public_question(q)), {'id', 'question', 'filter'})


class AgentTests(unittest.TestCase):
    def run_with(self, calls, **kw):
        llm = FakeLLM(calls)
        res = run_agent('How long are refunds?', llm, BM25Retriever(CHUNKS), filters=None, top_k=2,
                        budget_chars=kw.get('budget', 5000), max_searches=kw.get('max_searches', 3))
        return res, llm

    def test_search_then_cited_answer(self):
        cid = 'B:doc:p001:c000'
        res, _ = self.run_with([('search_documents', {'query': 'refunds processed'}),
                                ('submit_answer', {'answer': f'Seven working days [{cid}].', 'citations': [cid], 'abstain': False})])
        self.assertEqual(res['status'], 'answered')
        self.assertEqual(res['searches'], 1)
        self.assertIn(cid, res['context_ids'])
        self.assertEqual(res['usage']['prompt_tokens'], 200)
        self.assertAlmostEqual(res['usage']['cost_usd'], cost_usd('gpt-4o-mini', 200, 20))

    def test_citation_not_in_context_is_rejected(self):
        res, _ = self.run_with([('search_documents', {'query': 'refunds'}),
                                ('submit_answer', {'answer': 'x [B:doc:p002:c000]', 'citations': ['B:doc:p002:c000'], 'abstain': False})])
        self.assertEqual(res['status'], 'abstain')
        self.assertEqual(res['events'][-1]['event'], 'invalid_or_missing_citations')

    def test_v2_repairs_missing_inline_marker_for_valid_ids(self):
        cid = 'B:doc:p001:c000'
        res, _ = self.run_with([('search_documents', {'query': 'refunds processed'}),
                                ('submit_answer', {'answer': 'Seven working days.', 'citations': [cid], 'abstain': False})])
        self.assertEqual(res['status'], 'answered')
        self.assertTrue(res['answer'].endswith(f'[{cid}]'))
        self.assertIn('citations_appended_inline', [e['event'] for e in res['events']])

    def test_explicit_abstain_and_search_limit(self):
        res, llm = self.run_with([('search_documents', {'query': 'a'}),
                                  ('submit_answer', {'answer': 'Not enough evidence', 'citations': [], 'abstain': True})],
                                 max_searches=1)
        self.assertEqual(res['status'], 'abstain')
        self.assertEqual(llm.seen[1], ['submit_answer'])       # search tool removed after the limit

    def test_provider_error_is_reported_not_faked(self):
        res, _ = self.run_with([ProviderError('HTTP 401')])
        self.assertEqual(res['status'], 'error')
        self.assertEqual(res['events'][-1]['event'], 'provider_error')

    def test_retriever_error_is_reported(self):
        class Broken:
            name = 'broken'
            def search(self, *a, **k): raise ConnectionError('db down')
        res = run_agent('q', FakeLLM([('search_documents', {'query': 'q'})]), Broken(), filters=None,
                        top_k=3, budget_chars=1000)
        self.assertEqual(res['status'], 'error')
        self.assertIn('db down', res['events'][-1]['error'])


class BenchmarkTests(unittest.TestCase):
    def test_real_benchmark_resolves_and_meets_minimum(self):
        chunks = json.loads(config.CHUNKS_FILE.read_text(encoding='utf-8'))
        qs = json.loads(config.QUESTIONS_FILE.read_text(encoding='utf-8'))
        stats = validate_questions(qs, chunks)
        self.assertGreaterEqual(stats['dev']['answerable'], 15)
        self.assertGreaterEqual(stats['dev']['unanswerable'], 2)
        self.assertGreaterEqual(stats['test']['answerable'], 5)
        self.assertGreaterEqual(stats['test']['unanswerable'], 2)

    def test_test_split_requires_locked_selection(self):
        old = config.SELECTED_FILE
        with tempfile.TemporaryDirectory() as d:
            config.SELECTED_FILE = Path(d) / 'selected.json'
            exp = {'baseline': 'dense_k3'}
            try:
                with self.assertRaises(SystemExit):
                    ex._guard_test(['baseline'], exp)
                config.SELECTED_FILE.write_text(json.dumps({'selected': 'hybrid_k3'}), encoding='utf-8')
                self.assertEqual(ex._guard_test(['baseline', 'selected'], exp), ['dense_k3', 'hybrid_k3'])
                with self.assertRaises(SystemExit):
                    ex._guard_test(['bm25_k3'], exp)
            finally:
                config.SELECTED_FILE = old


if __name__ == '__main__':
    unittest.main()
