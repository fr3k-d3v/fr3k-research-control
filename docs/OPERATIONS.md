# Operational instructions

## Evidence taxonomy
Every claim must be tagged CLAIM, OBSERVATION, EVIDENCE, VERIFIED FACT, HYPOTHESIS, SIMULATION or UNKNOWN. Git commit != deployment; running service != completed job; GPU utilization != task correctness.

## Loop
1. **OBSERVE:** Inventory current devices, services, source commit hashes, raw logs, timestamps, temperature, VRAM/RAM and job IDs. Record original evidence privately before transformation.
2. **VERIFY:** Test source authenticity, license, model/quant/architecture compatibility, reproducibility and negative findings. Record exact command exit status.
3. **RECONCILE:** Deduplicate leads by canonical URL+commit; compare updated files against prior snapshots; link to existing experiment ID. Preserve prior measurements.
4. **IMPROVE:** Write an explicit hypothesis, change list, expected upside, resource budget and rollback. Avoid simultaneous GPU experiments.
5. **TEST:** Run correctness before speed. Use isolated GPU lease, cold/warm repeats, randomized ordering, 4K/16K/64K contexts and identical model SHA, prompts, sampling, tool schema and engine revision.
6. **RECORD:** Commit sanitized reports, scripts, failures and reproducibility metadata; link private evidence by non-sensitive digest, not by private paths or contents.

## Continuous ingestion (implementation specification; not yet deployed)
- Poll known research folders and approved public repositories with bounded cadence; process only changed file hashes/commit IDs.
- Each item gets stable candidate ID, source URL, observed_at, upstream SHA, license, platform/model fit, evidence tier, risk, owner and next gate.
- Use append-only event ledger, idempotent imports, deterministic dedup and retry backoff. No automatic code execution from newly discovered repos.
- Rank: correctness and security compatibility first; then expected throughput, resource fit, maturity and effort. Unverified claims cannot become measured gains.
- Produce proposed experiments as queue entries; dispatch only after baseline acceptance and exclusive GPU slot are verified.
- Run research-only CPU workers concurrently; cap RAM/network/disk I/O so benchmark contamination is bounded and recorded.
- Require human approval for physical, destructive, externally publishing or sensitive operations; read-only observation is distinct from authorization to execute.

## Gates
- Gate 0: healthy accepted baseline and snapshot.
- Gate 1: source/license/security review and architecture match.
- Gate 2: dry-run tests and resource estimate.
- Gate 3: exclusive GPU reservation and no competing benchmarks.
- Gate 4: coding correctness, tool continuation and 64K exact retrieval.
- Gate 5: prefill/decode/TTFT p50/p95, VRAM/RAM, SSD I/O, cache hit/miss, thermal and power measurements.
- Gate 6: recovery/soak; only then candidate promotion. Any failure -> restore accepted baseline, preserve logs and mark blocked.
