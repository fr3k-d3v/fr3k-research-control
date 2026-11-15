"""Schema-validated, non-authoritative task checkpoints.

Checkpoints preserve references to GitHub evidence; they do not assert success
or grant permissions. Persistence is caller-owned and must be atomic.
"""
from dataclasses import dataclass, asdict
import json

VALID_STATES = frozenset({"UNKNOWN", "NOT_TESTED", "INFERRED", "PARTIALLY_VERIFIED", "VERIFIED", "BLOCKED"})

@dataclass(frozen=True)
class Checkpoint:
    schema_version: int
    task_id: str
    objective: str
    constraints: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    pending_actions: tuple[str, ...]
    failures: tuple[str, ...]
    rollback_ref: str
    state: str

def encode(checkpoint: Checkpoint) -> str:
    if checkpoint.schema_version != 1:
        raise ValueError("unsupported checkpoint version")
    if not checkpoint.task_id.strip() or not checkpoint.objective.strip():
        raise ValueError("missing task identity")
    if checkpoint.state not in VALID_STATES:
        raise ValueError("invalid evidence state")
    if any(not isinstance(x, str) for seq in (checkpoint.constraints, checkpoint.evidence_refs,
                                               checkpoint.pending_actions, checkpoint.failures) for x in seq):
        raise TypeError("checkpoint fields must be strings")
    return json.dumps(asdict(checkpoint), sort_keys=True, ensure_ascii=False, separators=(",", ":"))

def decode(payload: str) -> Checkpoint:
    obj = json.loads(payload)
    fields = set(Checkpoint.__dataclass_fields__)
    if not isinstance(obj, dict) or set(obj) != fields:
        raise ValueError("invalid checkpoint fields")
    for key in ("constraints", "evidence_refs", "pending_actions", "failures"):
        if not isinstance(obj[key], list):
            raise ValueError("invalid checkpoint collection")
        obj[key] = tuple(obj[key])
    cp = Checkpoint(**obj)
    encode(cp)
    return cp
