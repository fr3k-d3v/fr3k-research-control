# FR3K Research Control — evidence-driven hardware optimization

Connect machines. Measure reality. Delegate work. Verify results.

**Status:** Research/control documentation. Not an assertion that experimental engines are installed or accepted. **Hardware:** Omarchy RTX 3060 12GB; Parrot retired. **Current inference:** llama.cpp + Qwen3-Coder-30B-A3B Q4_K_M. Hermes cloud default `opencode-go/beam-free` is independent of local inference.

## Start here
- [Operational playbook](docs/OPERATIONS.md): OBSERVE → VERIFY → RECONCILE → IMPROVE → TEST → RECORD.
- [Research and experiment protocol](docs/EXPERIMENTS.md): immutable baselines, compatibility, four-way matrix, acceptance gates.
- [Fleet orchestration](docs/FLEET.md): delegated workers, leases, approvals and authority boundaries.
- [Candidate ledger](ledger/CANDIDATES.md): latest leads, evidence tiers, negative findings and next actions.
- [Live-state handoff](docs/HANDOFF.md): observed vs pending and how to refresh evidence.

This repository is the **new research coordination entrypoint**, not a replacement for a future canonical `fr3kd3v/fr3k` monorepo. Prefer merging this material into the monorepo once its authoritative remote is confirmed. Never mirror private fleet configuration, tokens, local paths, raw user data, or internal infrastructure.

## Connection-layer architecture
- [FR3K Fabric: research-backed connection and orchestration plan](architecture/FR3K-CONNECTION-LAYER-PLAN.md) — secure device identity, typed jobs, leases, evidence, hardware routing, alternatives, failure tests and milestone exit criteria.
