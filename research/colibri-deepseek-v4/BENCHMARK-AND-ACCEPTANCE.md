# Benchmark and acceptance protocol

## Principles

- Correctness before speed.
- Same model revision, quant, prompt, context, sampler, output ceiling and engine commit for paired comparisons.
- Cold and warm runs are separate measurements.
- Randomise experiment order; repeat enough runs to report median and p95.
- Keep raw logs and device telemetry before producing summaries.
- Do not compare official safetensors against a GGUF quant as if they were the same artifact.
- A fast answer is not evidence of a correct answer.
- Do not run parallel GPU experiments. Use an exclusive GPU lease and record competing workloads.

## Stage A — preflight snapshot

Capture, with timestamps:

- Colibrì commit/tag and build flags.
- Model repository revision, exact file list and SHA-256 checksums.
- CPU model, cores/threads, ISA, governor and load.
- RAM total/available, swap, page faults and peak RSS.
- GPU model, driver, compute capability, free/total VRAM, clocks, power, temperature and competing processes.
- CUDA toolkit and Vulkan runtime/ICD.
- NVMe model, free bytes, filesystem, temperature/health and direct/random-read throughput.
- Existing llama.cpp baseline service/model/config.
- Model planner output and exact context/cache plan.

## Stage B — baseline correctness

For each selected artifact:

1. Verify every downloaded file against upstream size/checksum metadata.
2. Run Colibrì's doctor and plan.
3. Run the engine self-test.
4. Start CPU-canonical inference with a small context and output budget.
5. Capture output and token IDs where available.
6. Repeat the same prompts with CUDA or Vulkan enabled.
7. Compare greedy output. Where backend arithmetic is documented to differ, use the upstream engine's supported correctness metric (fixed-text perplexity / score or logits comparison) and document the limitation.

No performance result is accepted without a corresponding correctness record.

## Stage C — workload suite

Use a fixed, sanitised prompt set with no private client or personal data:

| ID | Workload | What it tests |
|---|---|---|
| DS-01 | Short factual response | Startup, first token and basic decode |
| DS-02 | Multi-step reasoning | Reasoning stability and output termination |
| DS-03 | Code analysis and patch plan | Code reasoning |
| DS-04 | Small code edit with tests | Tool schema, call/return loop and task completion |
| DS-05 | JSON-only structured response | JSON validity; grammar is not assumed |
| DS-06 | Tool selection from 3 tools | Correct function name and arguments |
| DS-07 | Multi-tool sequential workflow | Continuation and tool-result incorporation |
| DS-08 | Long document with exact-source question | Retrieval fidelity and context handling |
| DS-09 | 10-turn conversation | KV reuse and context growth |
| DS-10 | Malformed tool response / timeout | Error handling and recovery |

Tool calls must be executed by a test harness with a harmless allowlist. The model must never receive unrestricted shell, filesystem, network, phone, fleet or physical-device authority.

## Stage D — context sweep

Run only after the 4K correctness baseline is stable:

- 4K
- 8K
- 16K
- 32K
- 64K

At each tier, record actual prompt token count, requested and actual context, KV allocation, peak VRAM/RSS, swap, time-to-first-token, prefill throughput, decode throughput and task correctness.

Do not jump to the model's advertised maximum context. The Colibrì DeepSeek V4 guide documents one KV slot; context and concurrency must be measured on the actual build.

## Stage E — backend matrix

### Official safetensors (same weights)

| Arm | Backend | Purpose |
|---|---|---|
| A | CPU canonical | Correctness reference and baseline |
| B | CUDA generic sm_86 | Primary RTX 3060 acceleration attempt |
| C | CUDA with one documented tuning change | Determine whether the change helps |
| D | Vulkan, only if the exact checkpoint path is supported and planner confirms | Independent GPU path |

### Full-model GGUF UD-IQ2_XXS (same quant)

| Arm | Backend | Purpose |
|---|---|---|
| A | CPU | Quant-specific correctness and baseline |
| B | Vulkan expert tier | Primary GGUF GPU route |
| C | CUDA GGUF path, if build and planner support it | Compare CUDA versus Vulkan |
| D | Vulkan with one measured host-pool/cache adjustment | Test RAM split |

### REAP 150B fallback

Treat as its own model. Compare quality and task completion against the full model on the same prompt suite. Do not use its faster result as evidence that the full model has passed.

## Stage F — tuning variables

Change one variable per experiment, preserving the stock-default result:

- RAM planner budget / expert cache size.
- CUDA dense mirrors.
- CUDA prefill expert bank on/off.
- CUDA attention batch on/off.
- Vulkan host-pool size and expert-tier settings.
- Loader lanes and read depth.
- Context size.
- Expert history / warm-start state.
- Second SSD model mirror, only after a single-drive baseline.

Never copy 16 GB / 24 GB / 32 GB GPU settings onto the 12 GB 3060 without recalculating free VRAM and reserves. Do not tune several environment variables at once.

## Required metrics

| Metric | Required reporting |
|---|---|
| TTFT | Cold and warm p50 / p95 |
| Prefill | Tokens/s and total prompt time |
| Decode | Tokens/s, generated token count and stop reason |
| Task | End-to-end latency and success/failure |
| Correctness | Token comparison or named alternative metric |
| Memory | Peak/steady RSS, available RAM, swap, peak VRAM |
| Storage | Read bandwidth, IOPS, bytes read per token, temperature |
| Cache | Expert hits/misses, cache size, host-pool occupancy |
| GPU | Utilisation, clocks, power, temperature, fallback counts |
| Stability | OOM, crash, timeout, restart and recovery |
| Agent | Valid tool-call rate, schema-valid arguments, completed tool cycles |

## Acceptance gates

- [ ] Source and model artifacts pinned by commit/revision and checksums.
- [ ] Preflight shows sufficient RAM and disk headroom.
- [ ] CPU reference starts and passes self-test.
- [ ] GPU path passes correctness checks or is explicitly rejected.
- [ ] 4K, 16K and 64K context behavior is recorded; 64K is stable before any long-context claim.
- [ ] No swap storm, OOM, thermal runaway or unbounded disk pressure.
- [ ] Tool calls pass schema validation and the bounded test harness.
- [ ] Timeouts, cancellation, restart and fallback work.
- [ ] Repeat runs show a real task-level benefit versus the accepted llama.cpp baseline.
- [ ] Sanitised evidence is committed and failures are recorded.

## Promotion rule

Promote only if all correctness, security, stability and recovery gates pass, and repeated end-to-end tasks show a useful improvement or a clearly justified capability gain. Otherwise record REJECTED or BLOCKED; preserve the accepted llama.cpp route.

## Run record template

Copy this block for every run:

~~~yaml
experiment_id: FR3K-LLM-COLIBRI-DSV4-001
run_id: ""
observed_at: ""
status: UNKNOWN
source:
  colibri_repo: https://github.com/JustVugg/colibri
  colibri_commit: ""
  build_flags: ""
model:
  repo: ""
  revision: ""
  artifact: ""
  quant: ""
  sha256_manifest: ""
host:
  cpu: ""
  ram_total_gib: null
  ram_available_gib: null
  gpu: ""
  vram_total_gib: null
  vram_free_gib: null
  driver: ""
  cuda: ""
  vulkan: ""
  storage: ""
  free_disk_gib: null
workload:
  prompt_id: ""
  prompt_tokens: null
  context_tokens: null
  output_limit: null
  sampler: ""
backend: ""
measurements:
  ttft_ms: null
  prefill_tok_s: null
  decode_tok_s: null
  end_to_end_ms: null
  peak_rss_gib: null
  peak_vram_gib: null
  disk_read_gib: null
  expert_hit_rate: null
  temperature_c: null
  power_w: null
correctness:
  reference: ""
  result: UNKNOWN
  evidence_path_local: ""
failure: ""
notes: ""
~~~
