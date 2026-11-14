# Colibrì + DeepSeek V4 Flash — FR3K evaluation

**Research ID:** FR3K-LLM-COLIBRI-DSV4-001  
**Opened:** 2026-11-14  
**Status:** PREFLIGHT COMPLETE · ENGINE BUILDS PASS · MODEL DOWNLOAD NOT APPROVED · NO MODEL INFERENCE  
**Primary target:** DeepSeek V4 Flash 0731 (284B total parameters)  
**Runtime:** [JustVugg/colibri](https://github.com/JustVugg/colibri)

> Connect machines. Measure reality. Delegate work. Verify results.

## Current decision

The best current full-model candidate for the Omarchy workstation is **AtomicChat AD-IQ2_XS GGUF**, an 85.1 GB four-shard quant of the full 284B DeepSeek V4 Flash architecture. The model card reports 79.24% next-token top-1 agreement and mean KLD 0.3947 against its AD-BF16 reference on the publisher's own evaluation harness. These are publisher measurements, not FR3K results.

The current model volume has 93.88 GB free, leaving approximately 8.8 GB after the listed model files. This is a **tight nominal fit**, not yet a verified download budget. Colibrì's importer defaults to `--mode link`, so it can read the GGUF in place without making a second 85 GB copy. Recheck exact free bytes immediately before download.

The official 166.9 GB checkpoint is currently blocked: Colibrì's catalogue says it needs 172 GB free, while the target volume has 93.88 GB. The Unsloth UD-IQ2_XXS GGUF is 90.9 GB and also leaves insufficient operational headroom. REAP 150B is a separate expert-pruned fallback, not the full model.

## Start here

1. [Implementation plan](IMPLEMENTATION-PLAN.md) — phases, dependencies and exit gates.
2. [Model and hardware fit](MODEL-AND-HARDWARE-FIT.md) — actual Omarchy inventory and candidate fit.
3. [Quantization comparison](MODEL-QUANTIZATION-COMPARISON.md) — full-model quant choices and publisher-reported quality.
4. [Local preflight report](LOCAL-PREFLIGHT-2026-11-14.md) — observed hardware, storage and blockers.
5. [Build and smoke tests](BUILD-AND-SMOKE-TESTS.md) — source pin, build commands, checksums and test outcomes.
6. [Benchmark and acceptance](BENCHMARK-AND-ACCEPTANCE.md) — correctness, speed and acceptance.
7. [FR3K integration](FR3K-INTEGRATION.md) — provider boundary, tool authority and failure handling.
8. [Runbook](RUNBOOK.md) — safe preflight and later installation procedure.
9. [Execution tasks](TASKS.md) — ordered work queue and current states.
10. [Evidence register](EVIDENCE.md) — source claims versus local observations.
11. [Decision log](DECISIONS.md) — explicit choices and unresolved questions.

## Hardware and runtime progress

- Omarchy: Intel i3-12100 (4C/8T), 32 GB RAM, RTX 3060 12 GB, driver 615.78.08, CUDA toolkit 13.4, compute capability 8.6.
- Colibrì v2.1.0 source commit: `704a3f68184b78367a04cb5526e428dc2f90f05b`.
- CPU DeepSeek V4 engine build: PASS.
- CUDA sm_86 DeepSeek V4 engine build: PASS.
- CUDA runtime vector-add smoke test: PASS on RTX 3060.
- Generic Colibrì Vulkan device initialization: PASS on RTX 3060; this is not yet a DeepSeek V4 model inference test.
- DeepSeek V4 expert-store registry unit test: PASS.
- No model weights downloaded; no actual DeepSeek inference performed.
- Existing llama.cpp + Qwen baseline remains untouched.

## Candidate hierarchy

| Priority | Candidate | What it is | Current decision |
|---|---|---|---|
| P0 — preferred full-model test | AtomicChat AD-IQ2_XS GGUF | Full 284B architecture; 85.1 GB; 4 shards; publisher top-1 79.24% | Nominally fits with ~8.8 GB left; recheck and obtain download approval |
| P1 — smaller full-model quant | AtomicChat AD-IQ2_XXS GGUF | Full 284B architecture; 78.5 GB; publisher top-1 77.46% | More disk headroom, lower reported fidelity |
| P2 — alternate publisher | Unsloth UD-IQ1_S GGUF | Full 284B architecture; 82.5 GB; publisher comparison table top-1 75.16% | Lower reported fidelity than AtomicChat AD-IQ2_XS |
| P3 — fallback | DeepSeek V4 Flash REAP 150B | 150B expert-pruned; 132 rather than 256 routed experts | Separate model; use only if full-model options fail |
| Fidelity reference | Official DeepSeek V4 Flash 0731 | Full 284B safetensors; 166.9 GB | Blocked by current disk capacity |

## Non-negotiable operating rules

- Preserve the current llama.cpp + Qwen baseline; do not replace it during evaluation.
- No large model download until the selected artifact and exact disk budget are rechecked and approved.
- Start with CPU-canonical correctness. Tune one variable at a time.
- Keep the server bound to loopback with API authentication. Do not expose an unauthenticated inference endpoint to the LAN or tailnet.
- FR3K remains the sole authority for tool execution, job state, physical actions and approvals.
- A running server is not acceptance. A benchmark number without correctness evidence is not an accepted result.
- Store raw logs locally; publish only sanitised measurements. Never commit tokens, private paths, prompts containing personal data, machine identifiers or private infrastructure details.


## Pinned model download preparation

- [Exact four-shard manifest](DOWNLOAD-MANIFEST.md) — full Hugging Face revision, byte sizes, upstream ETag/Xet headers and storage arithmetic.
- [Safe resumable downloader](scripts/download-ad-iq2-xs.sh) — requires the explicit `--confirm-download` argument, checks free space plus reserve, pins the model revision and verifies every shard size. It has **not** been run.
