"""Day 7 CLI. Run from the repo root with the Day 6 venv (it has sentence-transformers + psycopg).

  python run.py export-chunks [--from db|pdf]
  python run.py check [--db]
  python run.py retrieval --split dev                       # all configs in configs/experiments.json
  python run.py select                                      # lock the config using dev only
  python run.py retrieval --split test                      # baseline + selected only
  python run.py agent --split dev --configs dense_k3 <best> # real model
  python run.py agent --split test --configs baseline selected
  python run.py metrics --split test --config selected      # after filling reviews.json
  python run.py report
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / 'src'))
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

from rag7 import config, experiments as ex  # noqa: E402


def main():
    p = argparse.ArgumentParser(description='Day 7 Agentic RAG experiments')
    sub = p.add_subparsers(dest='cmd', required=True)
    e = sub.add_parser('export-chunks')
    e.add_argument('--from', dest='source', choices=('db', 'pdf'), default='db')
    c = sub.add_parser('check')
    c.add_argument('--db', action='store_true', help='also connect to the Day 6 pgvector store')
    r = sub.add_parser('retrieval')
    r.add_argument('--split', choices=('dev', 'test', 'test_v1'), required=True)
    r.add_argument('--configs', nargs='*')
    sub.add_parser('select')
    a = sub.add_parser('agent')
    a.add_argument('--split', choices=('dev', 'test', 'test_v1'), required=True)
    a.add_argument('--configs', nargs='+', required=True)
    a.add_argument('--limit', type=int, help='only the first N questions (smoke test)')
    m = sub.add_parser('metrics')
    m.add_argument('--split', choices=('dev', 'test', 'test_v1'), required=True)
    m.add_argument('--config', required=True)
    sub.add_parser('report')
    args = p.parse_args()
    exp = config.load_experiments()
    if args.cmd == 'export-chunks':
        out = ex.export_chunks(args.source)
    elif args.cmd == 'check':
        out = ex.check(args.db)
    elif args.cmd == 'retrieval':
        names = args.configs or (list(exp['retrieval_configs']) if args.split == 'dev' else ['baseline', 'selected'])
        out = {k: {x: v[x] for x in ('hit1', 'evidence_hit3', 'context_evidence_rate', 'median_latency_ms')}
               for k, v in ex.eval_retrieval(args.split, names).items()}
    elif args.cmd == 'select':
        out = ex.select()
    elif args.cmd == 'agent':
        out = ex.run_agent_bench(args.split, args.configs, args.limit)
    elif args.cmd == 'metrics':
        out = ex.metrics(args.split, args.config)
    else:
        print(ex.report_tables())
        return
    print(json.dumps(out, ensure_ascii=False, indent=2, default=str))


if __name__ == '__main__':
    main()
