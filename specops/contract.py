#!/usr/bin/env python3
"""FR3K SpecOps offline contract validator. No network, shell, scheduling or authorization.
An ACCEPTED result means the supplied record satisfies structural gates only.
Fleet is authoritative for leases, permission, identity and terminal receipts.
"""
import hashlib
import json
import re
import unittest
from datetime import datetime, timezone

ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}")
SHA = re.compile(r"[a-f0-9]{64}")
AUTHORITY = {"OBSERVE", "AUTO", "APPROVAL", "PHYSICAL"}
OUTCOMES = {"VERIFIED", "FAILED", "BLOCKED", "UNKNOWN", "SIMULATION"}
KINDS = {"source", "build", "runtime", "physical", "deployment", "rollback"}

def require(condition, message):
    if not condition:
        raise ValueError(message)

def identifier(value):
    return isinstance(value, str) and ID.fullmatch(value) is not None

def digest(value):
    return isinstance(value, str) and SHA.fullmatch(value) is not None

def canonical_hash(record):
    return hashlib.sha256(json.dumps(record, sort_keys=True, separators=(",", ":"),
                                     allow_nan=False, ensure_ascii=False).encode()).hexdigest()

def utc(value):
    require(isinstance(value, str), "timestamp missing")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(parsed.tzinfo is not None, "timestamp must have timezone")
    return parsed.astimezone(timezone.utc)

def validate_task(task):
    require(isinstance(task, dict), "task must be object")
    allowed = {"version", "task_id", "spec_id", "dependencies", "requirements",
               "authority", "capability", "timeout_s", "attempt_limit", "idempotency_key"}
    require(set(task) == allowed, "unexpected/missing task fields")
    require(type(task["version"]) is int and task["version"] == 1, "unsupported version")
    for key in ("task_id", "spec_id", "capability", "idempotency_key"):
        require(identifier(task[key]), "invalid " + key)
    require(isinstance(task["authority"], str) and task["authority"] in AUTHORITY,
            "unknown authority")
    deps = task["dependencies"]
    require(isinstance(deps, list) and all(identifier(d) for d in deps), "invalid dependencies")
    require(len(set(deps)) == len(deps) and task["task_id"] not in deps, "duplicate/self dependency")
    for k, limit in (("timeout_s", 1800), ("attempt_limit", 10)):
        require(type(task[k]) is int and 1 <= task[k] <= limit, "invalid " + k)
    reqs = task["requirements"]
    require(isinstance(reqs, dict) and bool(reqs), "no acceptance requirements")
    for key, kind in reqs.items():
        require(identifier(key) and isinstance(kind, str) and kind in KINDS, "invalid requirement")
    return canonical_hash(task)

def validate_graph(tasks):
    ids = {}
    keys = set()
    for task in tasks:
        validate_task(task)
        require(task["task_id"] not in ids, "duplicate task")
        require(task["idempotency_key"] not in keys, "duplicate idempotency key")
        ids[task["task_id"]] = task
        keys.add(task["idempotency_key"])
    visiting, visited = set(), set()
    def visit(key):
        require(key in ids, "unknown dependency")
        require(key not in visiting, "dependency cycle")
        if key in visited:
            return
        visiting.add(key)
        for dep in ids[key]["dependencies"]:
            visit(dep)
        visiting.remove(key)
        visited.add(key)
    for key in ids:
        visit(key)
    return True

def check_receipt(task, receipt):
    """Reject structurally incomplete evidence. Never authenticate a receipt."""
    task_hash = validate_task(task)
    allowed = {"task_hash", "attempt_id", "worker_id", "verifier_id", "fleet_receipt_sha256",
               "started_at", "finished_at", "outcome", "exit_code", "evidence"}
    require(isinstance(receipt, dict) and set(receipt) == allowed, "receipt fields")
    require(receipt["task_hash"] == task_hash, "task drift")
    for k in ("attempt_id", "worker_id", "verifier_id"):
        require(identifier(receipt[k]), "invalid " + k)
    require(receipt["worker_id"] != receipt["verifier_id"], "self verification")
    require(digest(receipt["fleet_receipt_sha256"]), "missing fleet receipt digest")
    start, end = utc(receipt["started_at"]), utc(receipt["finished_at"])
    require(0 <= (end-start).total_seconds() <= task["timeout_s"], "time budget exceeded")
    outcome = receipt["outcome"]
    require(isinstance(outcome, str) and outcome in OUTCOMES, "invalid outcome")
    code = receipt["exit_code"]
    require(code is None or type(code) is int, "invalid exit code")
    evidence = receipt["evidence"]
    require(isinstance(evidence, list), "evidence must be list")
    seen = set()
    for item in evidence:
        require(isinstance(item, dict) and set(item) ==
                {"requirement_id", "kind", "sha256", "result", "simulated"}, "evidence fields")
        rid = item["requirement_id"]
        require(identifier(rid) and rid in task["requirements"] and rid not in seen,
                "duplicate/unknown requirement")
        require(item["kind"] == task["requirements"][rid], "wrong evidence kind")
        require(digest(item["sha256"]), "missing evidence digest")
        require(item["result"] in ("PASS", "FAIL", "UNKNOWN"), "invalid result")
        require(type(item["simulated"]) is bool, "simulation flag must be boolean")
        seen.add(rid)
    if outcome == "VERIFIED":
        require(code == 0, "nonzero/unknown exit")
        require(seen == set(task["requirements"]), "incomplete evidence")
        require(all(e["result"] == "PASS" and not e["simulated"] for e in evidence),
                "failed, unknown or simulated evidence")
    return {"structurally_valid": True, "authenticated": False,
            "promotion_authorized": False, "receipt_sha256": canonical_hash(receipt)}

class ContractTests(unittest.TestCase):
    def setUp(self):
        self.t = dict(version=1, task_id="T1", spec_id="S1", dependencies=[],
                      requirements={"R1":"physical"}, authority="PHYSICAL",
                      capability="device.test", timeout_s=60, attempt_limit=3,
                      idempotency_key="T1-v1")
        self.r = dict(task_hash=canonical_hash(self.t), attempt_id="A1", worker_id="W1",
                      verifier_id="V1", fleet_receipt_sha256="a"*64,
                      started_at="2026-11-27T00:00:00Z", finished_at="2026-11-27T00:00:30Z",
                      outcome="VERIFIED", exit_code=0, evidence=[
                          dict(requirement_id="R1", kind="physical", sha256="b"*64,
                               result="PASS", simulated=False)])
    def reject(self):
        with self.assertRaises(ValueError):
            check_receipt(self.t, self.r)
    def test_valid_structure_not_auth(self):
        result = check_receipt(self.t, self.r)
        self.assertTrue(result["structurally_valid"])
        self.assertFalse(result["authenticated"])
        self.assertFalse(result["promotion_authorized"])
    def test_simulation(self):
        self.r["evidence"][0]["simulated"] = True
        self.reject()
    def test_missing_evidence(self):
        self.r["evidence"] = []
        self.reject()
    def test_wrong_evidence_kind(self):
        self.r["evidence"][0]["kind"] = "build"
        self.reject()
    def test_wrong_digest(self):
        self.r["evidence"][0]["sha256"] = "unknown"
        self.reject()
    def test_worker_self_review(self):
        self.r["verifier_id"] = "W1"
        self.reject()
    def test_nonzero(self):
        self.r["exit_code"] = 1
        self.reject()
    def test_boolean_exit(self):
        self.r["exit_code"] = False
        self.reject()
    def test_timeout(self):
        self.r["finished_at"] = "2026-11-27T00:01:01Z"
        self.reject()
    def test_drift(self):
        self.t["attempt_limit"] = 4
        self.reject()
    def test_unsafe_authority(self):
        self.t["authority"] = "UNRESTRICTED"
        self.reject()
    def test_unknown_dependency(self):
        self.t["dependencies"] = ["T2"]
        with self.assertRaises(ValueError):
            validate_graph([self.t])
    def test_cycle(self):
        self.t["dependencies"] = ["T2"]
        other = dict(self.t, task_id="T2", dependencies=["T1"], idempotency_key="T2-v1")
        with self.assertRaises(ValueError):
            validate_graph([self.t, other])
    def test_duplicate_idempotency(self):
        other = dict(self.t, task_id="T2")
        with self.assertRaises(ValueError):
            validate_graph([self.t, other])
    def test_blocked_is_not_promoted(self):
        self.r.update(outcome="BLOCKED", exit_code=None, evidence=[])
        self.assertFalse(check_receipt(self.t, self.r)["promotion_authorized"])

if __name__ == "__main__":
    unittest.main(verbosity=2)
