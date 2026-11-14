# FR3K Research Control — evidence-driven hardware optimization

Connect machines. Measure reality. Delegate work. Verify results.

**Status:** Research/control documentation. Experimental runtimes are not automatically accepted. Hardware inventory and local infrastructure identifiers are maintained privately. The local inference baseline remains preserved and unchanged.

## Start here
- [Operational playbook](docs/OPERATIONS.md): OBSERVE → VERIFY → RECONCILE → IMPROVE → TEST → RECORD.
- [Research and experiment protocol](docs/EXPERIMENTS.md): immutable baselines, compatibility, four-way matrix, acceptance gates.
- [Fleet orchestration](docs/FLEET.md): delegated workers, leases, approvals and authority boundaries.
- [Candidate ledger](ledger/CANDIDATES.md): latest leads, evidence tiers, negative findings and next actions.
- [Live-state handoff](docs/HANDOFF.md): observed vs pending and how to refresh evidence.

This repository is the research coordination entrypoint, not a replacement for a future canonical `fr3kd3v/fr3k` monorepo. Never mirror private fleet configuration, tokens, local paths, raw user data, filesystem identifiers, hostnames or internal infrastructure.

## Connection-layer architecture
- [FR3K Fabric plan](architecture/FR3K-CONNECTION-LAYER-PLAN.md)
- [Reuse-first GitHub landscape](architecture/REUSE-FIRST-GITHUB-LANDSCAPE-2026-11-09.md)
- [Prepared implementation jobs](architecture/IMPLEMENTATION-JOBS-2026-11-09.md)

## Inference runtime evaluations
- [Colibrì + DeepSeek V4 Flash evaluation](research/colibri-deepseek-v4/README.md)
- [Sanitised local preflight summary](research/colibri-deepseek-v4/LOCAL-PREFLIGHT-2026-11-14.md)
- [Build and smoke-test report](research/colibri-deepseek-v4/BUILD-AND-SMOKE-TESTS.md)

**Latest state (2026-11-14):** Colibrì v2.1.0 CPU/CUDA sm_86 builds and CUDA runtime smoke passed; generic Vulkan device initialization passed. Huihui DeepSeek V4 Flash 0731 Abliterated Q2 is selected. No model weights have been downloaded and no DeepSeek model inference has been accepted. Local acquisition remains blocked by a filesystem write gate and target-host availability.
