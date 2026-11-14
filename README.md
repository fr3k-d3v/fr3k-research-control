# FR3K Research Control — evidence-driven hardware optimization

Connect machines. Measure reality. Delegate work. Verify results.

**Status:** Research/control documentation. Experimental runtimes are not automatically accepted. **Hardware:** Omarchy RTX 3060 12GB; Parrot retired. **Current inference baseline:** llama.cpp + Qwen3-Coder-30B-A3B Q4_K_M, preserved and unchanged. Hermes cloud default `opencode-go/beam-free` is independent of local inference.

## Start here
- [Operational playbook](docs/OPERATIONS.md): OBSERVE → VERIFY → RECONCILE → IMPROVE → TEST → RECORD.
- [Research and experiment protocol](docs/EXPERIMENTS.md): immutable baselines, compatibility, four-way matrix, acceptance gates.
- [Fleet orchestration](docs/FLEET.md): delegated workers, leases, approvals and authority boundaries.
- [Candidate ledger](ledger/CANDIDATES.md): latest leads, evidence tiers, negative findings and next actions.
- [Live-state handoff](docs/HANDOFF.md): observed vs pending and how to refresh evidence.

This repository is the **new research coordination entrypoint**, not a replacement for a future canonical `fr3kd3v/fr3k` monorepo. Prefer merging this material into the monorepo once its authoritative remote is confirmed. Never mirror private fleet configuration, tokens, local paths, raw user data, or internal infrastructure.

## Connection-layer architecture
- [FR3K Fabric: research-backed connection and orchestration plan](architecture/FR3K-CONNECTION-LAYER-PLAN.md) — secure device identity, typed jobs, leases, evidence, hardware routing, alternatives, failure tests and milestone exit criteria.
- [Reuse-first GitHub landscape and build-vs-buy decisions](architecture/REUSE-FIRST-GITHUB-LANDSCAPE-2026-11-09.md) — upstream repository checks and specific components to reuse rather than rebuild.
- [Prepared implementation jobs and duplicate-work reconciliation](architecture/IMPLEMENTATION-JOBS-2026-11-09.md) — ordered work, dependencies, existing Fleet MCP code and gates.

## Inference runtime evaluations
- [Colibrì + DeepSeek V4 Flash evaluation](research/colibri-deepseek-v4/README.md) — dedicated model/hardware fit, runtime build evidence, quantization review, install gates, benchmark protocol and FR3K provider integration.
- [Omarchy preflight report](research/colibri-deepseek-v4/LOCAL-PREFLIGHT-2026-11-14.md) — live hardware, memory, storage and current blockers.
- [Build and smoke-test report](research/colibri-deepseek-v4/BUILD-AND-SMOKE-TESTS.md) — pinned runtime, CPU/CUDA build results, CUDA runtime smoke and Vulkan device initialization.

**Latest state (2026-11-14):** Colibrì v2.1.0 source checkout and CPU/CUDA sm_86 builds succeeded; CUDA runtime smoke passed; generic Vulkan device initialization passed. The preferred full-model GGUF candidate is AtomicChat AD-IQ2_XS (85.1 GB), pending final free-space recheck and explicit download approval. No model weights were downloaded and the existing llama.cpp baseline was not changed.
