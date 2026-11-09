"""Deterministic, dependency-free token-budget planner.

This module does not tokenize: callers MUST provide counts from the target
model's tokenizer, including chat template/tool overhead.
"""
from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True)
class ContextItem:
    id: str
    tokens: int
    priority: int
    required: bool = False
    source_ref: str = ""

@dataclass(frozen=True)
class Plan:
    kept: tuple[str, ...]
    dropped: tuple[str, ...]
    used_tokens: int
    reserved_output: int
    capacity: int

class ContextOverflow(ValueError):
    pass

def plan_context(items: Sequence[ContextItem], *, capacity: int = 65536,
                 output_reserve: int = 10240, fixed_overhead: int = 0) -> Plan:
    """Never drop required items; evict optional items deterministically.

    Priority is an integer; higher values win. Ties preserve original order.
    The planner is pure and never truncates a context item.
    """
    if capacity <= 0 or output_reserve < 0 or fixed_overhead < 0:
        raise ValueError("invalid budget")
    if len({x.id for x in items}) != len(items):
        raise ValueError("duplicate context item id")
    if any(x.tokens < 0 for x in items):
        raise ValueError("negative token count")
    budget = capacity - output_reserve - fixed_overhead
    if budget < 0:
        raise ContextOverflow("fixed overhead and output reserve exceed capacity")
    mandatory = sum(x.tokens for x in items if x.required)
    if mandatory > budget:
        raise ContextOverflow("required context exceeds available input budget")
    chosen = {x.id for x in items if x.required}
    remaining = budget - mandatory
    for _, item in sorted(enumerate(items), key=lambda pair: (-pair[1].priority, pair[0])):
        if item.required:
            continue
        if item.tokens <= remaining:
            chosen.add(item.id)
            remaining -= item.tokens
    kept = tuple(x.id for x in items if x.id in chosen)
    dropped = tuple(x.id for x in items if x.id not in chosen)
    used = fixed_overhead + sum(x.tokens for x in items if x.id in chosen)
    assert used + output_reserve <= capacity
    return Plan(kept, dropped, used, output_reserve, capacity)
