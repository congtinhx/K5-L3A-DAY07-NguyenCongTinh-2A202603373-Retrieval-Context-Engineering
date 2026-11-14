"""Context selection: dedup, rank order, optional same-page neighbours, hard character budget."""
import re

_CID = re.compile(r'^(?P<prefix>.*:p\d+:c)(?P<idx>\d+)$')


def neighbour_ids(chunk_id: str) -> list[str]:
    m = _CID.match(chunk_id)
    if not m:
        return []
    i, width = int(m['idx']), len(m['idx'])
    return [f"{m['prefix']}{j:0{width}d}" for j in (i - 1, i + 1) if j >= 0]


def block(c: dict) -> str:
    return f"[{c['id']} | {c['source']} | page {c['page']} | section {c['metadata'].get('section')}]\n{c['text']}"


def select_context(ranked: list[dict], *, budget_chars: int, policy: str = 'rank',
                   by_id: dict[str, dict] | None = None, already: list[dict] | None = None) -> tuple[list[dict], list[dict]]:
    """Return (selected, dropped). `already` = chunks kept from earlier searches (kept first).

    policy 'rank': take results in rank order while they fit.
    policy 'rank_neighbors': after each kept chunk, also try its previous/next chunk on the same page.
    Chunks that do not fit are skipped (smaller later chunks can still fit) and reported as dropped.
    """
    if budget_chars < 1:
        raise ValueError('budget_chars phải > 0')
    selected = list(already or [])
    seen = {c['id'] for c in selected}
    used = len('\n\n'.join(block(c) for c in selected))
    dropped = []

    def try_add(c: dict, reason: str) -> bool:
        nonlocal used
        if c['id'] in seen:
            return False
        extra = len(block(c)) + (2 if selected else 0)
        if used + extra > budget_chars:
            dropped.append({'id': c['id'], 'reason': f'budget ({reason})'})
            return False
        selected.append({**c, 'context_reason': reason})
        seen.add(c['id'])
        used += extra
        return True

    for c in ranked:
        if try_add(c, f"rank {c.get('rank')}") and policy == 'rank_neighbors' and by_id:
            for nid in neighbour_ids(c['id']):
                if nid in by_id and by_id[nid]['page'] == c['page']:
                    try_add(by_id[nid], f"neighbour of {c['id']}")
    if policy not in ('rank', 'rank_neighbors'):
        raise ValueError(f'context policy không hỗ trợ: {policy}')
    return selected, dropped


def render(selected: list[dict]) -> str:
    return '\n\n'.join(block(c) for c in selected)
