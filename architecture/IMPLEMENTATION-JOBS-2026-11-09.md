# FR3K Fabric implementation jobs — prepared 2026-11-09

**Execution policy:** Prepare and test on CPU/isolated sandbox. Do not touch the active Omarchy GPU acceptance job or modify production Fleet MCP state. Any production migration requires independently verified backups, rollback and authority.

## Existing code reconciliation (important)
The private `fr3k-d3v/fr3k-fleet-mcp` repository already contains `fleet_mcp/jobs.py`, `tests/test_job_recovery.py`, `tests/test_fencing_conformance.py`, `scripts/fencing_probe.py`, `scripts/fencing_conformance.py`, `tests/test_c009_approval_envelope.py`, and `docs/F004-FENCING-CONFORMANCE-20261026.md`. The fencing report explicitly says its isolated evidence is **NOT DEPLOYED**. Do **not** build a parallel job engine before auditing these components and any pending branches/PRs. Earlier proposal for a fresh Postgres orchestrator is a **candidate**, not an approved replacement for the existing SQLite-backed fleet store.

## Queue, order, authority and gates
1. **J01 — existing-code inventory** (OBSERVE; CPU): review job storage, recovery, fencing, approval envelope, migrations, existing PRs, service contracts. Deliver file/function map, baseline tests, gap table. Exit: no duplicated subsystem proposal.
2. **J02 — adversarial conformance** (AUTO isolated; depends J01): run existing fencing and job-recovery suites in temp DB; add scenarios for duplicate dispatch, stale lease, late result, cancellation and restart. Exit: reproducible before/after evidence.
3. **J03 — typed integration contract** (AUTO repo only; depends J01): minimal adapter schema for device capabilities, job IDs, resource leases, evidence digest and authority class. Preserve existing Fleet MCP API compatibility. Exit: schema fixtures and validation tests.
4. **J04 — CPU-only Contabo→Omarchy dry-run** (APPROVAL if live write; depends J02/J03): submit a benign non-GPU task, simulate lost acknowledgment and reconnect, verify exactly one accepted terminal result and artifact SHA. Exit: real cross-host trace with no secrets.
5. **J05 — Android Appium emulator spike** (AUTO sandbox; depends J03): inspect existing overlay tests; add UI smoke for queue order, rotation and crash detection. Exit: emulator artifact and deterministic test report.
6. **J06 — GPU candidate matrix** (AUTO after GPU acceptance only; depends J02): compare baseline and research candidates at 4K/16K/64K with coding quality/tool calls/VRAM/power and rollback. Exit: verified measured candidate, never upstream claim alone.
7. **J07 — GitHub→Contabo Gitea mirroring** (APPROVAL/auth required; depends J01): confirm authenticated Gitea access, preserve private visibility, verify per-repo refs and commit hashes, enable idempotent timer. Exit: mirror proof and alert on drift.

## Stop conditions
Existing GPU acceptance not terminal; any conflict with GPU lock; unexpected credential exposure; stale approval; failed integrity hash; inconsistent job authority; failed rollback; repository privacy mismatch. Mark BLOCKED with evidence rather than claim completion.
