"""Deterministic, scoped lexical retrieval prototype.

This is a safe baseline, NOT semantic vector search. Access control is checked
before ranking; all returned text is untrusted evidence, never instructions.
"""
from dataclasses import dataclass
import re
from typing import Sequence

def terms(text: str) -> frozenset[str]:
    return frozenset(re.findall(r"[a-z0-9_./-]+", text.lower()))

@dataclass(frozen=True)
class Passage:
    id: str
    scope: str
    source_ref: str
    text: str
    observed_at: str = ""

@dataclass(frozen=True)
class Hit:
    id: str
    source_ref: str
    score: int
    text: str

def retrieve(query: str, passages: Sequence[Passage], *,
             allowed_scopes: frozenset[str], limit: int = 5,
             max_chars_per_hit: int = 2000) -> tuple[Hit, ...]:
    if limit < 0 or max_chars_per_hit < 0:
        raise ValueError("negative retrieval budget")
    q = terms(query)
    if not q:
        return ()
    ids = set()
    matches = []
    for i, p in enumerate(passages):
        if p.id in ids:
            raise ValueError("duplicate passage id")
        ids.add(p.id)
        if p.scope not in allowed_scopes:
            continue
        overlap = len(q & terms(p.text))
        exact = 3 if query.lower() in p.text.lower() else 0
        score = overlap + exact
        if score:
            matches.append((score, i, p))
    matches.sort(key=lambda x: (-x[0], x[1]))
    return tuple(Hit(p.id, p.source_ref, score, p.text[:max_chars_per_hit])
                 for score, _, p in matches[:limit])
