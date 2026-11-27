#!/usr/bin/env python3
"""Local evidence journal, not an execution queue or authority.
Only sanitized projections and artifact hashes belong here. A chain detects
accidental/tamper changes relative to a separately trusted checkpoint, not
malicious replacement of the whole database. No cryptographic signature.
"""
import hashlib
import json
import re
import sqlite3
import tempfile
import unittest
from pathlib import Path

HEX=re.compile(r"[a-f0-9]{64}")
ID=re.compile(r"[A-Za-z0-9][A-Za-z0-9_.:-]{0,127}")
STATES={"EXECUTION_SUCCEEDED","EXECUTION_FAILED","BLOCKED","UNKNOWN"}
ZERO="0"*64

def canonical(x):
    return json.dumps(x,sort_keys=True,separators=(",",":"),allow_nan=False)

def digest(x):
    return hashlib.sha256(canonical(x).encode()).hexdigest()

def validate(x):
    if not isinstance(x,dict) or set(x)!={"task_hash","attempt_id","state","receipt_sha256","output_sha256"}:
        raise ValueError("invalid record fields")
    if not isinstance(x["task_hash"],str) or not HEX.fullmatch(x["task_hash"]):
        raise ValueError("invalid task hash")
    if not isinstance(x["attempt_id"],str) or not ID.fullmatch(x["attempt_id"]):
        raise ValueError("invalid attempt identity")
    if not isinstance(x["state"],str) or x["state"] not in STATES:
        raise ValueError("invalid state")
    for k in ("receipt_sha256","output_sha256"):
        if k=="output_sha256" and x[k] is None and x["state"]!="EXECUTION_SUCCEEDED":
            continue
        if not isinstance(x[k],str) or not HEX.fullmatch(x[k]):
            raise ValueError("invalid digest")
    return canonical(x)

class Journal:
    def __init__(self,path):
        self.db=sqlite3.connect(path,isolation_level=None,timeout=5)
        self.db.execute("PRAGMA busy_timeout=5000")
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS observations(
          seq INTEGER PRIMARY KEY, attempt_id TEXT UNIQUE NOT NULL,
          payload TEXT NOT NULL, previous TEXT NOT NULL, digest TEXT NOT NULL
        );
        CREATE TRIGGER IF NOT EXISTS no_update BEFORE UPDATE ON observations
        BEGIN SELECT RAISE(ABORT,'immutable observation'); END;
        CREATE TRIGGER IF NOT EXISTS no_delete BEFORE DELETE ON observations
        BEGIN SELECT RAISE(ABORT,'immutable observation'); END;
        """)
    def close(self):
        self.db.close()
    def verify(self,expected_head=None):
        head=ZERO
        count=0
        for seq,aid,payload,previous,stored in self.db.execute(
                "SELECT seq,attempt_id,payload,previous,digest FROM observations ORDER BY seq"):
            count+=1
            data=json.loads(payload)
            if seq!=count or aid!=data.get("attempt_id") or validate(data)!=payload or previous!=head:
                raise ValueError("journal continuity violation")
            head=digest({"seq":seq,"previous":previous,"payload":data})
            if head!=stored:
                raise ValueError("journal digest mismatch")
        if expected_head is not None and head!=expected_head:
            raise ValueError("checkpoint mismatch")
        return {"count":count,"head":head,"authenticated":False,"promotion_authorized":False}
    def append(self,record):
        payload=validate(record)
        self.db.execute("BEGIN IMMEDIATE")
        try:
            state=self.verify()
            row=self.db.execute("SELECT payload,digest FROM observations WHERE attempt_id=?",
                                (record["attempt_id"],)).fetchone()
            if row:
                if row[0]!=payload:
                    raise ValueError("attempt replay with changed receipt")
                self.db.execute("COMMIT")
                return {"duplicate":True,"digest":row[1]}
            seq=state["count"]+1
            head=digest({"seq":seq,"previous":state["head"],"payload":record})
            self.db.execute("INSERT INTO observations VALUES(?,?,?,?,?)",
                            (seq,record["attempt_id"],payload,state["head"],head))
            self.db.execute("COMMIT")
            return {"duplicate":False,"digest":head}
        except BaseException:
            self.db.execute("ROLLBACK")
            raise

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.path=Path(self.tmp.name)/"evidence.sqlite"
        self.j=Journal(self.path)
        self.r=dict(task_hash="a"*64,attempt_id="attempt-1",state="EXECUTION_FAILED",
                    receipt_sha256="b"*64,output_sha256="c"*64)
    def tearDown(self):
        self.j.close()
        self.tmp.cleanup()
    def test_restart(self):
        first=self.j.append(self.r)
        self.j.close(); self.j=Journal(self.path)
        self.assertEqual(self.j.verify(first["digest"])["count"],1)
        self.assertFalse(self.j.verify()["promotion_authorized"])
    def test_idempotent(self):
        a=self.j.append(self.r)
        b=self.j.append(self.r)
        self.assertTrue(b["duplicate"]); self.assertEqual(a["digest"],b["digest"])
        self.assertEqual(self.j.verify()["count"],1)
    def test_conflicting_replay(self):
        self.j.append(self.r)
        with self.assertRaises(ValueError):
            self.j.append(dict(self.r,state="BLOCKED"))
        self.assertEqual(self.j.verify()["count"],1)
    def test_second_attempt(self):
        a=self.j.append(self.r)
        b=self.j.append(dict(self.r,attempt_id="attempt-2",state="EXECUTION_SUCCEEDED"))
        self.assertNotEqual(a["digest"],b["digest"])
        self.assertEqual(self.j.verify(b["digest"])["count"],2)
    def test_no_mutation(self):
        self.j.append(self.r)
        with self.assertRaises(sqlite3.IntegrityError):
            self.j.db.execute("UPDATE observations SET payload='invalid'")
        with self.assertRaises(sqlite3.IntegrityError):
            self.j.db.execute("DELETE FROM observations")
    def test_checkpoint(self):
        self.j.append(self.r)
        with self.assertRaises(ValueError): self.j.verify(ZERO)
    def test_no_raw_fields(self):
        with self.assertRaises(ValueError): self.j.append(dict(self.r,stdout="private"))
    def test_success_missing_output(self):
        with self.assertRaises(ValueError):
            self.j.append(dict(self.r,state="EXECUTION_SUCCEEDED",output_sha256=None))
    def test_tamper_detection(self):
        self.j.append(self.r)
        self.j.db.execute("DROP TRIGGER no_update")
        self.j.db.execute("UPDATE observations SET digest=?",("f"*64,))
        with self.assertRaises(ValueError): self.j.verify()
    def test_concurrent_connections(self):
        second=Journal(self.path)
        try:
            a=self.j.append(self.r)
            b=second.append(self.r)
            self.assertTrue(b["duplicate"]); self.assertEqual(a["digest"],b["digest"])
        finally:
            second.close()

if __name__=="__main__":
    unittest.main(verbosity=2)
