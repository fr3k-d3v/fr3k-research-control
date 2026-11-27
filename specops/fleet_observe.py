#!/usr/bin/env python3
"""Read-only Fleet receipt reconciliation. No dispatch, credentials, or approval.
Transport functions must be supplied by the caller using an authenticated Fleet
connection. Agreement is a consistency check, not cryptographic authentication.
"""
import hashlib
import json
import re
import unittest

JOB = re.compile(r"^[0-9a-f]{32}$")
TERMINAL = {"succeeded", "failed", "timeout", "cancelled", "denied"}
ACTIVE = {"queued", "running", "cancellation_requested", "approval_required", "unknown"}
FIELDS = ("job_id", "device", "status", "terminal", "exit_code", "duration_ms",
          "requires_approval", "approval_id", "truncated")

def project(record, expected):
    if not isinstance(record, dict) or not set(FIELDS).issubset(record):
        raise ValueError("incomplete Fleet response")
    p = {key: record[key] for key in FIELDS}
    if not isinstance(expected, str) or not JOB.fullmatch(expected) or p["job_id"] != expected:
        raise ValueError("job identity mismatch")
    if not isinstance(p["device"], str) or not p["device"]:
        raise ValueError("missing device")
    state = p["status"]
    if not isinstance(state, str) or state not in TERMINAL | ACTIVE:
        raise ValueError("unrecognized status")
    for field in ("terminal", "requires_approval", "truncated"):
        if type(p[field]) is not bool:
            raise ValueError("invalid boolean")
    if state != "unknown" and p["terminal"] != (state in TERMINAL):
        raise ValueError("terminal flag inconsistent")
    if p["exit_code"] is not None and type(p["exit_code"]) is not int:
        raise ValueError("invalid exit code")
    if state == "succeeded" and p["exit_code"] != 0:
        raise ValueError("success without zero exit")
    if p["duration_ms"] is not None and (type(p["duration_ms"]) is not int or p["duration_ms"] < 0):
        raise ValueError("invalid duration")
    return p

def observe(job_id, read_status, read_output):
    """Call only the two injected read methods; no write capability exists."""
    a = project(read_status(job_id), job_id)
    raw = read_output(job_id)
    b = project(raw, job_id)
    if a != b:
        return {"state": "UNKNOWN", "reason": "status snapshots disagree; refresh",
                "promotion_authorized": False}
    stdout, stderr = raw.get("stdout"), raw.get("stderr")
    complete = isinstance(stdout, str) and isinstance(stderr, str) and not b["truncated"]
    evidence = None
    if complete:
        evidence = hashlib.sha256(json.dumps({"stdout":stdout, "stderr":stderr},
                    sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
    state = b["status"]
    result = ("EXECUTION_SUCCEEDED" if state == "succeeded" and complete
              else "BLOCKED" if state in {"approval_required", "denied"}
              else "EXECUTION_FAILED" if state in TERMINAL - {"succeeded","denied"}
              else "UNKNOWN")
    return {"state": result, "fleet_status": state, "terminal": b["terminal"],
            "exit_code": b["exit_code"], "approval_required": b["requires_approval"],
            "output_sha256": evidence, "cryptographically_authenticated": False,
            "promotion_authorized": False}

class Tests(unittest.TestCase):
    def setUp(self):
        self.id = "a"*32
        self.a = dict(job_id=self.id, device="fixture", status="succeeded", terminal=True,
                      exit_code=0, duration_ms=5, requires_approval=False, approval_id=None,
                      truncated=False)
        self.b = dict(self.a, stdout="marker", stderr="")
    def run_observe(self):
        return observe(self.id, lambda _: self.a, lambda _: self.b)
    def test_success_not_promotion(self):
        r = self.run_observe()
        self.assertEqual(r["state"],"EXECUTION_SUCCEEDED")
        self.assertFalse(r["promotion_authorized"])
        self.assertFalse(r["cryptographically_authenticated"])
    def test_mismatch(self):
        self.b["device"] = "different"
        self.assertEqual(self.run_observe()["state"],"UNKNOWN")
    def test_truncated(self):
        self.a["truncated"] = self.b["truncated"] = True
        self.assertEqual(self.run_observe()["state"],"UNKNOWN")
    def test_failed(self):
        for x in (self.a,self.b):
            x.update(status="failed",exit_code=7)
        self.assertEqual(self.run_observe()["state"],"EXECUTION_FAILED")
    def test_held(self):
        for x in (self.a,self.b):
            x.update(status="approval_required",terminal=False,exit_code=None,requires_approval=True)
        self.assertEqual(self.run_observe()["state"],"BLOCKED")
    def test_missing_field(self):
        del self.b["terminal"]
        with self.assertRaises(ValueError): self.run_observe()
    def test_wrong_job(self):
        self.b["job_id"] = "b"*32
        with self.assertRaises(ValueError): self.run_observe()
    def test_nonzero_success(self):
        self.b["exit_code"] = 1
        with self.assertRaises(ValueError): self.run_observe()
    def test_running_not_success(self):
        for x in (self.a,self.b):
            x.update(status="running",terminal=False,exit_code=None)
        self.assertEqual(self.run_observe()["state"],"UNKNOWN")
    def test_missing_stdout(self):
        del self.b["stdout"]
        self.assertEqual(self.run_observe()["state"],"UNKNOWN")

if __name__ == "__main__":
    unittest.main(verbosity=2)
