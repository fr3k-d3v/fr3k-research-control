# Implementation plan

**Research ID:** FR3K-LLM-COLIBRI-DSV4-001  
**Status:** PHASES 0–3 PARTIALLY/COMPLETED; MODEL DOWNLOAD AND INFERENCE NOT STARTED.

## Objective

Determine whether Colibrì can run DeepSeek V4 Flash 0731 usefully and reliably on the Omarchy RTX 3060 12 GB / 32 GB RAM workstation, then expose it to FR3K through a controlled local provider adapter if it passes correctness, performance, security and recovery gates.

The target is not merely to make the binary start. The target is a reproducible, quality-checked local inference service that FR3K can route work to without handing model-generated output authority over the system.

## Current progress snapshot — 2026-11-14

| Phase | Status | Evidence |
|---|---|---|
| 0 — source and scope freeze | COMPLETE | Colibrì v2.1.0 source/release pinned; model families and candidate quants reviewed |
| 1 — read-only Omarchy preflight | PARTIAL | Hardware, RAM, GPU, CUDA, Vulkan and mounted storage observed; unmounted volume free space and storage throughput remain UNKNOWN |
| 2 — choose artifact | PARTIAL | AtomicChat AD-IQ2_XS selected as preferred full-model candidate; exact download still gated on approval and free-space recheck |
| 3 — install/build in isolation | PARTIAL | Isolated source/release staged; CPU and CUDA sm_86 engine builds pass; generic Vulkan device init passes; no system install |
| 4 — first inference and correctness | NOT STARTED | No model weights downloaded |
| 5 — performance/resource tuning | NOT STARTED | No model benchmark |
| 6 — FR3K provider integration | NOT STARTED | Existing llama.cpp route preserved |
| 7 — soak, promotion and record | NOT STARTED | No acceptance decision |

## Phase 0 — source and scope freeze

- [x] Identify Colibrì repository and current main/dev snapshots.
- [x] Identify DeepSeek V4 Flash versus V4.1 distinction.
- [x] Pin Colibrì v2.1.0 source and release archive checksum.
- [x] Identify official checkpoint, full-model GGUF candidates and REAP fallback.
- [x] Review AtomicChat quantization table and exact AD-IQ2_XS shard listing.

**Exit:** tested code and model artifacts are pinned by commit/revision and checksum.

## Phase 1 — read-only Omarchy preflight

- [x] Observe CPU, RAM, swap, RTX 3060, driver and free VRAM.
- [x] Observe CUDA toolkit and compute capability.
- [x] Observe Vulkan device/API/cooperative matrix.
- [x] Observe primary model-volume free bytes and catalogue fit output.
- [ ] Inspect unmounted exFAT and NTFS volume free capacity (requires operator approval for read-only mount).
- [ ] Measure NVMe random-read and sustained sequential throughput.
- [ ] Recheck free disk immediately before model download.

**Exit:** timestamped sanitized hardware report, disk budget and backend matrix. See LOCAL-PREFLIGHT.

## Phase 2 — choose the artifact

Current priority:

1. AtomicChat AD-IQ2_XS full-model GGUF (85.1 GB, full 284B architecture), pending approval and final disk recheck.
2. AtomicChat AD-IQ2_XXS (78.5 GB) if extra storage headroom is more important than the publisher-reported quality delta.
3. REAP 150B only as a separate expert-pruned fallback.
4. Official full safetensors only if a volume with at least 172 GB free becomes available.

Before download, record exact repository revision, included files, total bytes, destination, available bytes, checksum method and expected additional working space.

## Phase 3 — install Colibrì in isolation

- [x] Create isolated v2.1.0 source checkout.
- [x] Verify release archive SHA-256.
- [x] Build CPU DeepSeek V4 engine.
- [x] Build generic CUDA sm_86 engine with CUDA 13.4.
- [x] Run CUDA runtime smoke test.
- [x] Run expert-store registry unit test.
- [x] Probe generic Vulkan device initialization.
- [ ] Generate tiny fixture in isolated test environment and run CPU/CUDA/Vulkan correctness tests.
- [ ] Run `coli import`, `coli plan` and `coli doctor` against the selected real GGUF.

Do not change system packages or the existing llama.cpp service.

## Phase 4 — first inference and correctness

- Download and checksum the approved model artifact.
- Import with `--mode link`; do not make a second copy.
- Run CPU-canonical inference with a short prompt and low output ceiling.
- Repeat the same prompt with CUDA and Vulkan where supported.
- Capture generated output/token IDs, stop reason, usage, logs, backend banners and correctness evidence.
- Validate ordinary prose, reasoning, code, JSON, long-context retrieval and tool-call syntax.
- Verify graceful stop, restart, failed load, interrupted request and recovery.

**Exit:** correctness is demonstrated for the selected model/quant and backend; failures are retained.

## Phase 5 — performance and resource tuning

- Establish cold-start and warm-start results.
- Sweep contexts 4K, 8K, 16K, 32K and 64K only while the previous tier is stable.
- Measure TTFT, prefill tok/s, decode tok/s, end-to-end latency, peak VRAM/RSS, available RAM, swap, disk I/O, expert hit/miss rate, GPU temperature/power and OOM/recovery.
- Test one variable at a time: RAM budget, CUDA dense mirrors, prefill expert bank, Vulkan host-pool size, loader lanes and context.
- Keep an unmodified baseline between tuned arms.

## Phase 6 — FR3K provider integration

- Implement a provider adapter against Colibrì's local OpenAI-compatible endpoint.
- Keep routing, leases, approvals, idempotency, job state, evidence and physical authority in FR3K.
- Add bounded timeouts, cancellation, backpressure, health/readiness distinction, request IDs and fallback to the current llama.cpp provider.
- Keep local API authentication enabled and network exposure disabled by default.

## Phase 7 — soak, promotion and record

- Run a bounded soak only after correctness and recovery gates pass.
- Compare against the accepted llama.cpp baseline on the same tasks.
- Publish sanitised logs, config, commit/model hashes, measurement summary and negative results.
- Promote only if measured task-level benefit justifies the operational cost.

## Rollback

Stop only the Colibrì evaluation process, restore the previous FR3K provider route to the accepted llama.cpp endpoint, preserve logs and checksums, and do not delete or overwrite the current model/service/config.
