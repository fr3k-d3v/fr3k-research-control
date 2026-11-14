# Decision log

Append decisions. Do not silently rewrite an earlier decision; supersede it with a new dated entry.

## D-001 — target model family

- **Date:** 2026-11-14
- **Decision:** Target DeepSeek V4 Flash 0731, not DeepSeek V4.1 Flash.
- **Reason:** Colibrì documents separate `deepseek_v4` and `deepseek_v41` engines.
- **Status:** RECORDED.

## D-002 — model hierarchy

- **Date:** 2026-11-14
- **Decision:** Prefer the official full 284B checkpoint as the fidelity reference; test full-model GGUFs before using the REAP 150B fallback.
- **Reason:** GGUF keeps the full architecture/expert set but changes precision. REAP prunes experts and is a different model.
- **Status:** SUPERSEDED IN DETAIL BY D-006.

## D-003 — runtime role

- **Date:** 2026-11-14
- **Decision:** Colibrì is an optional inference provider, not the FR3K orchestrator.
- **Reason:** FR3K retains job lifecycle, authority, tool execution, approvals, evidence and recovery.
- **Status:** RECORDED.

## D-004 — preserve existing inference baseline

- **Date:** 2026-11-14
- **Decision:** Keep current llama.cpp + Qwen3-Coder baseline untouched during evaluation.
- **Reason:** A valid comparison requires a recoverable accepted baseline.
- **Status:** RECORDED AND VERIFIED UNCHANGED.

## D-005 — no model download without artifact approval

- **Date:** 2026-11-14
- **Decision:** Preflight, source checkout, builds and smoke tests may proceed. A large model download requires explicit approval of the exact artifact and a final free-space recheck.
- **Reason:** Model downloads are 80–170+ GB and storage headroom is tight.
- **Status:** ACTIVE.

## D-006 — preferred full-model GGUF candidate

- **Date:** 2026-11-14
- **Decision:** Prefer AtomicChat DeepSeek V4 Flash 0731 AD-IQ2_XS GGUF (85.1 GB, four shards) for the first full-284B experiment.
- **Reason:** It retains the full architecture and all routed experts; it nominally fits the observed 93.88 GB free volume with ~8.8 GB remaining; AtomicChat's own same-harness table reports 79.240% top-1 agreement and mean KLD 0.3947, better than its AD-IQ2_XXS and listed Unsloth UD-IQ1_S rows.
- **Caveat:** These are publisher-reported quant metrics, not FR3K measurements. Colibrì import compatibility and actual model quality/performance remain unverified.
- **Status:** SELECTED AS CANDIDATE ONLY — DOWNLOAD NOT APPROVED.

## D-007 — runtime build target

- **Date:** 2026-11-14
- **Decision:** Pin Colibrì v2.1.0 and build the generic CUDA engine for sm_86; keep CPU canonical and Vulkan as separate test arms.
- **Reason:** The Omarchy RTX 3060 is compute capability 8.6; the sm_120a DeepGEMM path is not applicable.
- **Status:** BUILD VERIFIED; MODEL INFERENCE PENDING.

## Open decisions

- Explicit approval to download AtomicChat AD-IQ2_XS (85.1 GB).
- Does the exact imported GGUF pass `coli plan` and `coli doctor` with safe headroom?
- Does DeepSeek V4 GGUF inference pass CPU-canonical correctness?
- Does CUDA sm_86 or Vulkan provide a useful task-level gain on the RTX 3060?
- What context size is stable on 32 GB RAM with existing swap pressure?
- Does one-KV-slot serving meet initial FR3K workloads?
