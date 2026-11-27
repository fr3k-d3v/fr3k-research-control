#!/usr/bin/env python3
"""Pure bounded convergence planner; no I/O, execution, authority or promotion.

All inputs are assertions, not authenticated evidence. A plan is a proposal
for the existing Fleet orchestrator, never a queue or permission grant.
"""
import hashlib
import json
import re
import unittest

ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}$")
DIGEST = re.compile(r"^[0-9a-f]{64}$")
ATTEMPT_STATES = {"QUEUED", "RUNNING", "SUCCEEDED", "FAILED", "BLOCKED", "UNKNOWN"}
OBS_STATES = {"PASS", "FAIL", "MISSING", "UNKNOWN", "SIMULATION"}

def check(ok, reason):
    if not ok:
        raise ValueError(reason)

def ident(value):
    return isinstance(value, str) and ID.fullmatch(value) is not None

def sha(value):
    return isinstance(value, str) and DIGEST.fullmatch(value) is not None

def hash_record(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"),
                                    allow_nan=False).encode()).hexdigest()

def reconcile(spec, attempts, observations):
    """Return deterministic next-action proposal, never a verified outcome."""
    check(isinstance(spec, dict) and set(spec) ==
          {"task_id", "task_hash", "requirements", "attempt_limit"}, "invalid spec fields")
    check(ident(spec["task_id"]) and sha(spec["task_hash"]), "invalid task identity")
    reqs = spec["requirements"]
    check(isinstance(reqs, list) and reqs and all(ident(x) for x in reqs), "invalid requirements")
    check(len(set(reqs)) == len(reqs), "duplicate requirement")
    limit = spec["attempt_limit"]
    check(type(limit) is int and 1 <= limit <= 10, "invalid attempt limit")
    check(isinstance(attempts, list) and len(attempts) <= limit, "invalid attempt history")
    check(isinstance(observations, dict) and set(observations).issubset(reqs),
          "unknown observation requirement")
    seen = set()
    for i, attempt in enumerate(attempts):
        check(isinstance(attempt, dict) and set(attempt) ==
              {"attempt_id", "task_hash", "status", "receipt_sha256"}, "invalid attempt")
        aid = attempt["attempt_id"]
        check(ident(aid) and aid not in seen, "duplicate/invalid attempt")
        seen.add(aid)
        check(attempt["task_hash"] == spec["task_hash"], "task revision drift")
        state = attempt["status"]
        check(isinstance(state,str) and state in ATTEMPT_STATES, "unknown attempt status")
        if state in {"SUCCEEDED", "FAILED", "BLOCKED"}:
            check(sha(attempt["receipt_sha256"]), "missing terminal receipt digest")
        else:
            check(i == len(attempts)-1, "nonterminal historical attempt")
    for rid, obs in observations.items():
        check(isinstance(obs, dict) and set(obs) == {"status", "evidence_sha256"},
              "invalid observation")
        state = obs["status"]
        check(isinstance(state,str) and state in OBS_STATES, "invalid observation status")
        if state in {"PASS", "FAIL", "SIMULATION"}:
            check(sha(obs["evidence_sha256"]), "missing observation digest")
        else:
            check(obs["evidence_sha256"] is None, "unexpected unknown evidence digest")
    base = {"task_id": spec["task_id"], "task_hash": spec["task_hash"],
            "promotion_authorized": False, "dispatch_authorized": False,
            "evidence_authenticated": False, "attempts_used": len(attempts),
            "attempt_limit": limit}
    def result(state, reason, **fields):
        return dict(base, state=state, reason=reason, **fields)
    if attempts:
        last = attempts[-1]["status"]
        if last in {"QUEUED","RUNNING"}:
            return result("WAIT_FOR_FLEET", "existing active attempt")
        if last in {"BLOCKED","UNKNOWN"}:
            return result("BLOCKED", "blocked or unconfirmed previous attempt")
    remaining = [rid for rid in sorted(reqs)
                 if observations.get(rid, {}).get("status") != "PASS"]
    if not remaining:
        return result("REVIEW_REQUIRED", "all input assertions pass; authenticate evidence independently")
    if len(attempts) >= limit:
        return result("BLOCKED", "attempt budget exhausted", unresolved=remaining)
    if any(observations.get(rid, {}).get("status") == "UNKNOWN" for rid in remaining):
        return result("BLOCKED", "uncertain evidence; observe before correction", unresolved=remaining)
    actions = [{"requirement_id": rid,
                "action": "PROPOSE_FIX" if observations.get(rid, {}).get("status") == "FAIL"
                          else "COLLECT_ACTUAL_EVIDENCE"} for rid in remaining]
    proposal = {"task_hash": spec["task_hash"], "attempt_number": len(attempts)+1,
                "actions": actions, "previous_attempt_ids": [a["attempt_id"] for a in attempts]}
    return result("PROPOSE_CORRECTION", "requires authoritative Fleet review",
                  correction_id="correction-"+hash_record(proposal),
                  proposal=proposal)

class Tests(unittest.TestCase):
    def setUp(self):
        self.s = dict(task_id="T1", task_hash="a"*64, requirements=["R1","R2"], attempt_limit=2)
        self.a = []
        self.o = {"R1":dict(status="PASS", evidence_sha256="b"*64),
                  "R2":dict(status="FAIL", evidence_sha256="c"*64)}
    def attempt(self, state="FAILED", aid="A1"):
        return dict(attempt_id=aid, task_hash=self.s["task_hash"], status=state,
                    receipt_sha256="d"*64 if state in {"SUCCEEDED","FAILED","BLOCKED"} else None)
    def run_plan(self):
        return reconcile(self.s,self.a,self.o)
    def test_proposal_not_authority(self):
        x=self.run_plan()
        self.assertEqual(x["state"],"PROPOSE_CORRECTION")
        self.assertEqual(x["proposal"]["actions"],[{"requirement_id":"R2","action":"PROPOSE_FIX"}])
        self.assertFalse(x["dispatch_authorized"])
        self.assertFalse(x["promotion_authorized"])
    def test_deterministic(self):
        self.assertEqual(self.run_plan(),self.run_plan())
    def test_order_independent(self):
        x=self.run_plan(); self.s["requirements"].reverse()
        self.assertEqual(x,self.run_plan())
    def test_new_attempt_new_id(self):
        x=self.run_plan(); self.a.append(self.attempt())
        self.assertNotEqual(x["correction_id"],self.run_plan()["correction_id"])
    def test_all_pass_review_only(self):
        self.o["R2"]["status"]="PASS"
        x=self.run_plan()
        self.assertEqual(x["state"],"REVIEW_REQUIRED")
        self.assertFalse(x["evidence_authenticated"])
    def test_simulation_collects_actual(self):
        self.o["R2"]["status"]="SIMULATION"
        self.assertEqual(self.run_plan()["proposal"]["actions"][0]["action"],"COLLECT_ACTUAL_EVIDENCE")
    def test_missing_collects_actual(self):
        del self.o["R2"]
        self.assertEqual(self.run_plan()["proposal"]["actions"][0]["action"],"COLLECT_ACTUAL_EVIDENCE")
    def test_unknown_blocks(self):
        self.o["R2"]=dict(status="UNKNOWN",evidence_sha256=None)
        self.assertEqual(self.run_plan()["state"],"BLOCKED")
    def test_active_wait(self):
        self.a=[self.attempt("RUNNING")]
        self.assertEqual(self.run_plan()["state"],"WAIT_FOR_FLEET")
    def test_blocked_not_retried(self):
        self.a=[self.attempt("BLOCKED")]
        self.assertEqual(self.run_plan()["state"],"BLOCKED")
    def test_exhaustion(self):
        self.a=[self.attempt(),self.attempt(aid="A2")]
        self.assertEqual(self.run_plan()["state"],"BLOCKED")
    def test_duplicate_attempt(self):
        self.a=[self.attempt(),self.attempt()]
        with self.assertRaises(ValueError): self.run_plan()
    def test_drift(self):
        self.a=[self.attempt()]; self.a[0]["task_hash"]="e"*64
        with self.assertRaises(ValueError): self.run_plan()
    def test_missing_terminal_receipt(self):
        self.a=[self.attempt()]; self.a[0]["receipt_sha256"]=None
        with self.assertRaises(ValueError): self.run_plan()
    def test_no_historical_running(self):
        self.a=[self.attempt("RUNNING"),self.attempt(aid="A2")]
        with self.assertRaises(ValueError): self.run_plan()

if __name__ == "__main__":
    unittest.main(verbosity=2)
