"""Opt-in context assembly interface for Hermes-compatible chat messages.

This adapter does not monkeypatch Hermes or change its configuration.
Integrators must supply the exact serialized prompt overhead and approved
retrieval passages. No automatic summarization or tool execution.
"""
from dataclasses import dataclass
from typing import Callable
from budget import ContextItem, ContextOverflow, plan_context

@dataclass(frozen=True)
class Message:
    id: str
    role: str
    content: str
    priority: int = 0
    required: bool = False

def assemble(messages: tuple[Message, ...], *, count_tokens: Callable[[str], int],
             capacity: int = 65536, output_reserve: int = 10240,
             template_overhead: int = 0) -> tuple[dict[str, str], ...]:
    if any(m.role not in {"system","developer","user","assistant","tool"} for m in messages):
        raise ValueError("invalid role")
    if any(m.role in {"system","developer"} and not m.required for m in messages):
        raise ValueError("privileged instructions must be required")
    items = [ContextItem(m.id, count_tokens(m.content), m.priority, m.required)
             for m in messages]
    plan = plan_context(items, capacity=capacity, output_reserve=output_reserve,
                        fixed_overhead=template_overhead)
    keep = set(plan.kept)
    return tuple({"role":m.role,"content":m.content} for m in messages if m.id in keep)
