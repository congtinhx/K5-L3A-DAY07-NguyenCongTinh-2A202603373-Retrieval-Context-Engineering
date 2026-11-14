"""Paths, environment and experiment configuration.

Secrets are read from `.env` (Day 7 root) and, as a fallback, from the Day 6
`starter/.env`. Nothing secret is written to results.
"""
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DAY6_DIR = Path(os.getenv('DAY6_DIR', ROOT.parent / 'K5-L3A-DAY06-NguyenCongTinh-2A202603373-DataIngestion')).resolve()
DAY6_STARTER = DAY6_DIR / 'starter'

CHUNKS_FILE = ROOT / 'data' / 'day6_chunks.json'
QUESTIONS_FILE = ROOT / 'data' / 'benchmark' / 'questions.json'
EXPERIMENTS_FILE = ROOT / 'configs' / 'experiments.json'
RESULTS_DIR = ROOT / 'results'
SELECTED_FILE = RESULTS_DIR / 'selected_config.json'


def _read_env_file(path: Path) -> None:
    """Minimal .env reader (no dependency); never overrides real env vars."""
    if not path.exists():
        return
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, value = line.split('=', 1)
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if value and key not in os.environ:
            os.environ[key] = value


def load_env() -> None:
    _read_env_file(ROOT / '.env')
    _read_env_file(DAY6_STARTER / '.env')


def load_experiments(path: Path = EXPERIMENTS_FILE) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str) + '\n', encoding='utf-8')


def read_json(path: Path):
    return json.loads(Path(path).read_text(encoding='utf-8'))
