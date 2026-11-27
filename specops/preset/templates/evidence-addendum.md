## FR3K Evidence and Authority Gates

For each requirement assign a stable ID, observed baseline, expected result, evidence kind (source, build, runtime, deployment, physical, rollback), deterministic acceptance test, accountable verifier, required capability, authority and timeout. Record dependencies, idempotency key, attempt budget and rollback.

- [ ] Evidence collected privately before derived interpretation; public summary sanitized.
- [ ] Source, build, runtime, deployment and physical evidence distinguished.
- [ ] Simulation explicitly labeled; no substitution for actual hardware.
- [ ] Fleet identity, authorization, lease and fencing validated by the authoritative server.
- [ ] Independent verifier checks actual artifacts and authenticated receipts.
- [ ] Failed, unknown, blocked and missing evidence remain open.
- [ ] Convergence bounded; retry uses new attempt ID; terminal receipts immutable.

A generated task, successful build, healthy process or heartbeat is not proof of deployed success. No permission is granted by this template.
