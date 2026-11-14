# Decision log

Append decisions. Do not silently rewrite an earlier decision; supersede it with a new dated entry.

## D-001 — target model family

- **Date:** 2026-11-14
- **Decision:** Target DeepSeek V4 Flash 0731, not DeepSeek V4.1 Flash.
- **Reason:** The requested model is DeepSeek Flash V4. Colibrì documents a distinct deepseek_v4 engine and a separate deepseek_v41 engine.
- **Status:** RECORDED.

## D-002 — model hierarchy

- **Date:** 2026-11-14
- **Decision:** Prefer the official full 284B checkpoint as the fidelity reference; evaluate the full-model UD-IQ2_XXS GGUF as the lower-disk route; keep REAP 150B as a clearly labelled fallback.
- **Reason:** The GGUF keeps the full model architecture/expert set but changes weight precision. REAP prunes 124 of 256 routed experts and is a different model.
- **Status:** RECORDED; final artifact selection depends on hardware preflight.

## D-003 — runtime role

- **Date:** 2026-11-14
- **Decision:** Colibrì is an optional inference provider, not the FR3K orchestrator.
- **Reason:** FR3K must retain job lifecycle, authority, tool execution, approvals, evidence and recovery.
- **Status:** RECORDED.

## D-004 — preserve existing inference baseline

- **Date:** 2026-11-14
- **Decision:** Keep current llama.cpp + Qwen3-Coder-30B-A3B Q4_K_M configuration untouched during evaluation.
- **Reason:** A valid comparison requires a recoverable accepted baseline.
- **Status:** RECORDED.

## D-005 — no download or system changes in the initial task

- **Date:** 2026-11-14
- **Decision:** This change creates research documentation and an execution plan only. Runtime installation, model downloads, package installation and service changes wait for preflight and explicit approval of the chosen artifact.
- **Reason:** The full model is a large download and actual storage/RAM fit is not yet observed.
- **Status:** RECORDED.

## Open decisions

- Which artifact is selected after preflight: official safetensors, full-model GGUF, or REAP fallback?
- Is the current CUDA toolkit suitable for a generic sm_86 build?
- Does the Vulkan driver support the documented GGUF expert-tier path?
- Is there sufficient NVMe headroom and random-read bandwidth?
- What context size and throughput make the model operationally useful for FR3K?
- Does the one-KV-slot serving behavior meet the initial FR3K workload?
