# Implementation plan

**Research ID:** FR3K-LLM-COLIBRI-DSV4-001  
**Status:** NOT STARTED — documentation committed; runtime work is gated on preflight and approval.

## Objective

Determine whether Colibrì can run DeepSeek V4 Flash 0731 usefully and reliably on the Omarchy RTX 3060 12 GB / 32 GB RAM workstation, then expose it to FR3K through a controlled local provider adapter if it passes correctness, performance, security and recovery gates.

The target is not merely to make the binary start. The target is a reproducible, quality-checked local inference service that FR3K can route work to without handing model-generated output authority over the system.

## Phase 0 — source and scope freeze

**Status:** PARTIALLY COMPLETE — upstream documentation reviewed; local checkout not created.

- [x] Identify Colibrì repository and current main/dev snapshots.
- [x] Identify DeepSeek V4 Flash versus V4.1 distinction.
- [x] Identify official checkpoint, full-model GGUF and REAP fallback.
- [x] Record upstream model/runtime constraints and published benchmark conditions.
- [ ] Recheck upstream main/dev heads, release and model manifests immediately before installation.
- [ ] Record selected source commit, release checksum, model repo revision and exact quant files in the local experiment manifest.

**Exit:** every tested code and model artifact is pinned by commit/revision and checksum.

## Phase 1 — read-only Omarchy preflight

**Status:** NOT STARTED.

Observe, do not change:

- CPU model, physical cores, ISA and current load.
- Total and available RAM; swap configuration and current use.
- RTX 3060 name, 12 GB capacity, free VRAM, driver, compute capability and current processes.
- CUDA toolkit / nvcc version and whether it can compile for sm_86.
- Vulkan ICD, device name, driver and supported features.
- NVMe devices, filesystem, free capacity, health/temperature and random-read performance.
- Current llama.cpp endpoint, model, config, service state and baseline performance.
- Competing GPU work and whether an exclusive benchmark lease is available.

Run the Colibrì hardware detector and model catalogue in list-only mode. Do not invoke setup with --yes, do not download weights, and do not install packages during this phase.

**Exit:** a timestamped hardware report, a disk budget, a backend matrix and a clear FIT, TIGHT or BLOCKED decision for each model artifact.

## Phase 2 — choose the artifact

Priority order:

1. **Full official checkpoint** if its ~167 GB download and memory plan fit. This is the reference path and preserves the official FP4/FP8 checkpoint.
2. **Full-model GGUF UD-IQ2_XXS** if the official checkpoint is too expensive to stage or if the GGUF has a materially better practical fit. It retains the full model architecture/expert count but is a very low-bit quant and must pass quality gates. Plan against the Hugging Face listed file sizes, not only Colibrì's rounded size.
3. **REAP 150B** only as a separate fallback experiment. It prunes 124 of 256 routed experts per layer; it is not the same model and must never be labelled as the full 284B checkpoint.

Before a download, record exact repository, revision, included files, total bytes, destination, available bytes, checksum method and expected additional working space. Obtain explicit approval for the chosen large download.

**Exit:** one artifact is selected and its storage / memory plan is feasible.

## Phase 3 — install Colibrì in isolation

- Use a dedicated evaluation directory and pinned Colibrì source/release.
- Preserve the existing llama.cpp installation, service, model and default route.
- Build the DeepSeek V4 CPU reference first.
- Build the generic CUDA sm_86 path only if the installed toolkit is compatible; do not use the sm_120-only DeepGEMM target on an RTX 3060.
- Keep Vulkan as a separate backend experiment, not a simultaneous change.
- Verify the build self-test, coli doctor, model planner and artifact checksums.
- Keep setup and server logs outside the public repository.

**Exit:** engine self-test passes; model plan is valid; no OOM or unexpected fallback; service remains loopback-only.

## Phase 4 — first inference and correctness

- Begin with a short, fixed prompt and low output ceiling.
- Run the CPU-canonical path first.
- Repeat the same prompt with the selected GPU backend.
- Capture generated token IDs/text, stop reason, usage, logs, backend banners and numerical correctness evidence.
- Validate ordinary prose, reasoning, code, JSON, long-context retrieval and tool-call syntax.
- Confirm that model output does not invoke tools by itself; the FR3K tool executor remains separate.
- Verify graceful stop, restart, failed load, interrupted request and recovery.

**Exit:** correctness is demonstrated for the selected model/quant and backend; failures are retained.

## Phase 5 — performance and resource tuning

- Establish cold-start and warm-start results.
- Sweep contexts 4K, 8K, 16K, 32K and 64K only while the previous tier is stable.
- Measure TTFT, prefill tok/s, decode tok/s, end-to-end latency, peak VRAM/RSS, available RAM, swap, disk I/O, expert hit/miss rate, GPU temperature/power and OOM/recovery.
- Test one knob at a time: RAM budget, Vulkan host-pool size, CUDA dense mirrors, prefill expert bank, loader lanes, model mirror only if a second independent SSD exists.
- Keep an unmodified baseline run between tuned arms. Randomise run order and repeat cold/warm measurements.
- Do not optimise solely for a short identical prompt; include rotating prompts and multi-turn agent work.

**Exit:** repeatable performance profile with no correctness regression, no swap storm, no thermal instability and safe resource headroom.

## Phase 6 — FR3K provider integration

- Implement a provider adapter against Colibrì's local OpenAI-compatible endpoint.
- Read the served model ID from runtime status rather than hardcoding it.
- Map tool definitions and tool results; validate every returned tool call against FR3K schemas.
- Keep routing, leases, approvals, idempotency, job state, evidence and physical authority in FR3K.
- Add bounded timeouts, cancellation, backpressure, health/readiness distinction, request IDs and fallback to the current llama.cpp provider.
- Keep local API authentication enabled and network exposure disabled by default.
- Add a model capability profile that records context, tool support, grammar limitations, concurrency and quantization.

**Exit:** an FR3K integration test can complete a bounded multi-step tool task, verify outputs and recover from a failed or stopped inference request.

## Phase 7 — soak, promotion and record

- Run a bounded soak only after correctness and recovery gates pass.
- Test repeated requests, idle periods, context growth, memory reclamation and server restart.
- Compare against the accepted llama.cpp baseline on the same tasks.
- Publish sanitised logs, config, commit/model hashes, raw measurement summary and negative results.
- Promote only if the measured task-level benefit justifies the operational cost.

**Exit:** explicit ACCEPTED, REJECTED or BLOCKED decision. No implicit promotion.

## Rollback

- Stop only the Colibrì evaluation process/service.
- Restore the previous FR3K provider route to the accepted llama.cpp endpoint.
- Do not overwrite or delete the current model, service or config.
- Preserve logs, model checksums and failure evidence.
- If a CUDA/Vulkan failure appears sticky, stop the process and return to CPU-only reference; do not continue issuing GPU work in the affected process.
