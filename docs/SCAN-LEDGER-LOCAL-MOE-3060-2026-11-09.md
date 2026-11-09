# Local MoE on RTX 3060 — scan ledger
Updated: 2026-11-09T17:52:35+10:00

## Goal
Keep scanning for newest helpful repos/projects/config patterns related to **local MoE inference on RTX 3060 / 3060etc (12GB VRAM)**. Save findings as markdown.

## Constraints
- GPU observed `2026-11-09T17:20:05+10:00`: `NVIDIA GeForce RTX 3060, 9018 MiB, 97 %` — **read-only web/GitHub/API scans only**. No local model runs/benchmarks.
- Evidence-bounded: owner/self-reported benchmarks = claims unless reproduced. Preserve experimental/broken warnings.

## Progress
- `scan-state.json`: **completed = 300 / 300** (originally 28, expanded to 300).
- Detailed synthesis saved: `07-LOCAL-MOE-3060-SCAN-28-PASSES-2026-11-09.md` (updated with 300-pass findings).
- Prior summary: `05-NEW-LOCAL-MOE-RTX3060-REPOS-2026-11-09.md`.

## Top findings (300 passes)
### Tier 1: Verified on real 3060 12GB hardware
1. **RustingStrata** (RustingStudio) — v1.2.1: 113 tok/s decode, 2016 tok/s prefill (4K), MTP 160 tok/s, 99.32% parity, Vulkan fallback, OpenAI+Anthropic API, multi-GPU, parallel (4 req = 164 tok/s), preserve-thinking for agents, built-in chat page
2. **moe-l2** (yalun753) — 0.14.1: 25 tok/s @262K ctx, OpenAI-compatible, verified Windows+Linux, auto-context, 9/9 PASS, ctx-force for KV bug
3. **llama.cpp tuned** — best ecosystem compat: 50-64 tok/s @32-64K ctx with expert cliff tuning, q4_0 KV, ncmoe 16-22

### Tier 2: Promising but needs verification on 3060
4. **FreeToken-Kai** (yuuki-net) — 2x 3060: 38.5 tok/s with MTP; 1x 3060: 19-23 tok/s; 250k context on 1x 12GB; browser-based benchmark tuning; 10 key innovations
5. **BigMoeOnEdge** (Helldez) — lossless flash streaming, `--auto` tuning, cross-platform, 15.5 tok/s on 3060 class for 125B model
6. **tandem.cpp** (ewhacc) — llama.cpp patch, 3.3x decode on 4090 (Qwen3.8); unverified on 3060
7. **ik_llama.cpp** + moe cache PR #2644 — GPU cache for host MoE experts
8. **Betelgeuse** (Betelgeuse-AI) — frontier MoE on 3060 12GB/16GB RAM/NVMe; experimental

### Tier 3: Practical config patterns (llama.cpp/ik_llama.cpp)
- Expert cliff: ncmoe 16 (32K) → 17 (64K) → 20 (128K) → 22 (258K)
- q4_0 KV: 4.6x prefill speedup, KL 0.10 (nearly lossless for Qwen)
- Negative optimizations under VRAM offload: fa on, large -b, MTP, threads 20
- MTP sweet spot: ncmoe 26 (not 32), 91% acceptance, 33-36 tok/s
- Host RAM: 32GB min for 35B; 64GB+ for 80B+; 128GB for 177B
- GPU utilization only ~50% (inherent to MoE+offload)
- FreeToken-Kai: --moe-bank-ram, --moe-expert-gguf, --spec-mtp 4, --dense-quant q8_0, --pp-size 2

### Key 3060 MoE gotchas (from 300 scans)
1. MoE total params ≠ VRAM: 35B MoE needs ~11-22GB depending on quant
2. Host RAM is the real bottleneck: 16GB host RAM severely limits MoE
3. KV cache surprises: qwen35moe KV estimate bug (~16x overestimate)
4. Quality matters: 98-99% greedy agreement is not 100%
5. Driver/runtime: CUDA 12.8 needs driver ≥570; AVX512 SIGILL on older CPUs
6. MTP interactions: MTP + expert offload can conflict; test both on/off
7. Prefill vs decode: Some engines faster on decode but slower on prefill for small models
8. Expert cache rule: Benefit = expert_size × hit_rate
9. Host load matters: 2.6-4.1 load → good; 21-28 load → 15-20% worse
10. GPU utilization only ~50% (inherent to MoE+offload)
11. FreeToken-Kai: MTP helps on 2-card (18→38.5 tok/s) but hurts on 1-card (41→19-35 tok/s)
12. FreeToken-Kai: q4_0 KV decode is flat from 8k to 125k on sparse backend

## Next useful actions (when GPU is free)
1. Reproduce RustingStrata: Qwen3.6-35B-A3B, MTP on/off, CUDA vs Vulkan, quality check
2. Reproduce moe-l2: Qwen3.6-35B-A3B UD-IQ2_M, ctx 65536→262144, measure VRAM + tok/s + quality
3. llama.cpp baseline: Qwen3.6-35B-A3B Q4_K_M, `-ngl 99 --cpu-moe`, ctx 4096→32768
4. Test expert cliff tuning: sweep ncmoe ±2 at each context level
5. Test q4_0 KV: measure prefill speedup and quality on your model
6. Test FreeToken-Kai: 1x 3060 with Qwen3.8-Flash-Next, 2x 3060 with MTP
7. Compare all on same model/quant/context for fair evaluation
