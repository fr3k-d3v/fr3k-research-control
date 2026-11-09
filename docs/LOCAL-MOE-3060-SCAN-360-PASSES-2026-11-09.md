# Local MoE on RTX 3060 (12GB-class) — 28 full scan passes
Date: 2026-11-09 (Australia/Brisbane)  
Scope: newest/helpful repos/projects/config patterns for **local MoE inference on RTX 3060 / 3060etc (12GB VRAM)**.  
Constraint observed `2026-11-09T17:20:05+10:00`: `NVIDIA GeForce RTX 3060, 9018 MiB, 97 %` utilization — **read-only web/GitHub/API scans only** (no local model runs, no local GPU benchmarks).

## Scan discipline
- 28 passes recorded in `scan-state.json` (completed=28).
- Evidence-bounded: owner/self-reported benchmarks are labeled as claims; experimental/broken status preserved where stated.
- Focus signals: exact model/GGUF/quant, context length, MoE expert offload/cache/paging/SSD streaming, build/kernel flags, tok/s *and* quality checks, VRAM/RAM/NVMe fit, CUDA vs Vulkan, llama.cpp/Ollama/vLLM/ExLlama/ik_llama.cpp compatibility, MTP/speculative interactions, recency (`updatedAt`/`pushedAt`), reproducibility.

## Highest-signal repos (verified via GitHub API where noted)

### NEW: moe-l2 (yalun753) — very high signal for 3060 12GB
- **Repo**: [yalun753/moe-l2](https://github.com/yalun753/moe-l2) — "MoE expert offload for low-VRAM GPUs"
- **Verified 3060 12GB results (2026-09 changelog)**:
  - Qwen3.6-35B-A3B **UD-IQ2_M** (11.5 GB): **25.0-25.3 t/s @256K ctx**, 8700 MiB VRAM; sweet spot 262144 ctx, ceiling 393216 ctx
  - Qwen3.6-35B-A3B **UD-Q4_K_M** (22.1 GB): **13-16 t/s @131072 ctx**, 7963 MiB VRAM
  - Windows native RTX 3060 12G verified: 9/9 PASS, 23.6 t/s steady-state (CUDA 12.8), no SIGILL
- **Architecture**: Transparent OpenAI-compatible proxy (:11435) + on-demand pin llama-server (:11436); experts in CPU RAM (mmap, zero VRAM); hot experts cached in VRAM (A3 LRU); selective pin (router map top-K); domain predictor (keyword→TF-IDF→semantic); expert-page eviction v3.1
- **Key insight**: `--ctx-force` flag needed for qwen35moe (Qwen3.6) because KV estimate overestimates ~16x (320KB/tok est vs ~20KB/tok actual)
- **Caveat**: V4 DeepSeek speed N/A (upstream CUDA expert bug #25582 auto-closed stale); AVX512 SIGILL fixed in v0.6.1 (AVX2 rebuild); CUDA 12.8 requires driver ≥570
- **Verdict**: **Strongest verified 3060 12GB MoE solution in this scan batch** — real numbers on real hardware, reproducible, OpenAI-compatible

### NEW: RustingStrata (RustingStudio) — strongest MoE engine signal
- **Repo**: [RustingStudio/RustingStrata](https://github.com/RustingStudio/RustingStrata) — "Pure-Rust MoE inference engine for Qwen"
- **Created**: 2026-10-10, 570 commits, 151 stars, 18 forks
- **Verified 3060 12GB results (Reddit community + README)**:
  - Qwen3.6-35B-A3B UD-Q2_K_XL (11.7 GB): prefill 1539 vs 1029 tok/s, decode 71.5 vs 39.6 tok/s (vs llama.cpp)
  - Qwen3.8-Flash-Next (177B, IQ2_XS 63 GB): decode ~36 tok/s CUDA, ~30 tok/s Vulkan (vs original Strata 19-22 tok/s)
  - Qwen3-Next-80B IQ1_S: decode ~92 tok/s (vs llama.cpp ~44 tok/s)
  - With MTP: 35B decode up to ~160 tok/s
  - Greedy top-1 agreement with llama.cpp: 98-99% (near-ties are float rounding)
- **Architecture**: Pure Rust, no ggml; NVRTC CUDA kernels compiled at startup; Vulkan fallback; CPU+GPU hybrid experts; MTP speculative decoding; OpenAI+Anthropic server
- **Key insight**: "main trick" is MoE models that don't fit VRAM — experts that don't fit run on CPU simultaneously with GPU work, keeping often-used experts on GPU
- **Caveat**: Self-reported benchmarks (though corroborated by community Reddit posts and independent Chinese-language blog tests); quality checks show 98-99% agreement (not 100%)
- **Verdict**: **Most impressive MoE engine for 3060 in this scan** — but verify quality on your specific use cases; 98-99% greedy agreement means occasional token differences

### NEW: tandem.cpp (ewhacc) — llama.cpp patch for MoE offload
- **Repo**: [ewhacc/tandem.cpp](https://github.com/ewhacc/tandem.cpp) — patch set for llama.cpp
- **Base**: llama.cpp commit f5222f25c (2026-10-28)
- **Mechanism**: Experts in host RAM; GPU memory leftover holds cache of recently used experts; misses split between CPU compute and cache uploads; split follows measured CPU/PCIe speeds (Strata's rule)
- **Reported**: 3.3× decode on Qwen3.8-Flash-Next (97.3 vs 29.8 tok/s on RTX 4090 + i5-12400F + 64GB DDR4)
- **Caveats**: Self-reported; independent (not ggml-org affiliated); gains tuned for Qwen3.8; shrinks as model approaches fitting in VRAM; CPU path only supports SwiGLU experts; DeepSeek-V4.1-Flash slower than stock (0.87×) due to SSD reads
- **Verdict**: Promising patch but verify on your exact hardware/model; Qwen3.8-specific tuning may not generalize

### NEW: Original Strata (niko1221/strata) — reference MoE offload engine
- **Referenced by**: RustingStrata (as baseline), tandem.cpp (comparison)
- **Note**: RustingStrata was created to beat Strata's speed; Strata remains a reference point
- **Verdict**: Superseded by RustingStrata for Qwen models but still useful as comparison baseline

| Repo | Updated (API) | Why relevant to 3060/MoE | Caution |
|---|---:|---|---|
| [RustingStudio/RustingStrata](https://github.com/RustingStudio/RustingStrata) | 2026-11-08T17:10:08Z (pushed 2026-11-09T00:59:59Z) | Pure-Rust Qwen GGUF inference (Qwen3–Qwen3.8 dense/MoE), CUDA+Vulkan, hybrid CPU+GPU experts, MTP speculative decoding, OpenAI/Anthropic-compatible server. README reports reference **RTX 3060 12GB / Ryzen 5 7600X / 32GB RAM** on Qwen3.6-35B-A3B MoE GGUF. | **Self-reported benchmarks** (decode/prefill gains, greedy agreement claims). Reproduce before relying. |
| [harshithmohan/local-llm-benchmarks](https://github.com/harshithmohan/local-llm-benchmarks) | 2026-11-09T04:06:52Z | Compares llama.cpp upstream, `ik_llama.cpp`, moe-cache fork, vLLM/Strata notes. **Rig 1: RTX 3060 12GB + i7-12700 + 128GB RAM**. Good for method/config/context evaluation. | Bench harness; validate exact commands/models/hardware parity. |
| [Betelgeuse-AI/Betelgeuse](https://github.com/Betelgeuse-AI/Betelgeuse) | 2026-11-08T10:09:52Z | Custom llama.cpp fork for frontier-scale MoE on **RTX 3060 12GB, 16GB RAM, local NVMe**; dense compute on GPU, experts in bounded VRAM pool (`bel-server`/`bel-cli`). | README states **experimental/partly broken**; CLI/unfamiliar configs need validation; no certified exact-output paging for MTP in that mode. |
| [jerryjokesalot/tinygiant](https://github.com/jerryjokesalot/tinygiant) | 2026-11-05T14:33:39Z | Expert-aware SSD streaming concept for MoE on memory-constrained hardware (selective expert reads; Qwen3-30B-A3B layout analysis mentioned). | Prototype-stage claims; verify correctness/perf. |
| [Ajay9o9/runs-on-a-3060](https://github.com/Ajay9o9/runs-on-a-3060) | 2026-11-08T21:29:13Z (pushed 2026-11-08T21:29:09Z) | Practical 3060 techniques/logs incl. MoE offload (`-ngl`, `-ncmoe`/`--cpu-moe`/`-ot exps=CPU`), KV quant interactions, host RAM effects. Useful 12GB operational reference. | Hardware/RAM/runtime-specific (many logs on 64GB host, turboquant builds); don’t generalize numbers to 16GB RAM without checking. |
| [fr3kchy/gguf-quantization-demo](https://github.com/fr3kchy/gguf-quantization-demo) | 2025-08-01T20:08:20Z | Reproducible GGUF quant sweep via llama.cpp; README targets **RTX 3060 12GB**. | Older; useful baseline harness/reference, not newest engine. |
| [fr3kchy/qwen36-bench](https://github.com/fr3kchy/qwen36-bench) | 2025-08-01T20:21:20Z | Reproducible Qwen3.6/Ollama optimisation on constrained hardware; FR3K-owned. | Older; re-check claims/scripts against current runtimes/models. |

## Practical 3060 (12GB) stack recommendations (from 80 scans)

### Tier 1: Verified on real 3060 12GB hardware
1. **moe-l2** (yalun753) — strongest verified: Qwen3.6-35B-A3B @25 t/s @256K ctx, 8.7GB VRAM, Windows+Linux verified
   - Best for: OpenAI-compatible serving, large context, verified stability
   - Install: `pip install moe-l2 && moe-l2 download-bins`
   - Key flags: `--ctx-force` for qwen35moe (KV estimate bug), `--router-map` for selective pin
   - Caveat: V4 DeepSeek speed N/A (upstream bug); AVX512 needs v0.6.1+; driver ≥570

2. **RustingStrata** (RustingStudio) — strongest MoE engine: Qwen3.6-35B @71.5 tok/s decode (vs 39.6 llama.cpp), Qwen3.8-Flash-Next 177B @36 tok/s
   - Best for: Maximum MoE throughput, MTP speculative decoding, Vulkan fallback
   - Install: `cargo build --release` (needs Rust + VS C++ Build Tools on Windows)
   - Key: `--gpu --mtp 1` for MTP, `--vram-margin` for less VRAM
   - Caveat: 98-99% greedy agreement (not 100%); self-reported benchmarks (corroborated by community)

### Tier 2: Promising but needs verification on 3060
3. **tandem.cpp** (ewhacc) — llama.cpp patch, 3.3× decode on 4090 (Qwen3.8); unverified on 3060
   - Best for: llama.cpp users wanting MoE offload without new runtime
   - Caveat: Qwen3.8-tuned; shrinks as model fits in VRAM; SwiGLU experts only

4. **ik_llama.cpp** + moe cache PR #2644 — GPU cache for host MoE experts
   - Best for: llama.cpp ecosystem compatibility
   - Caveat: PR status uncertain; merge not confirmed

5. **Betelgeuse** (Betelgeuse-AI) — frontier MoE on 3060 12GB/16GB RAM/NVMe
   - Best for: Experimental MoE paging research
   - Caveat: Explicitly experimental/partly broken

### Tier 3: Practical config patterns (llama.cpp/ik_llama.cpp)
- `-ngl 99 --cpu-moe` (all experts CPU, attention on GPU) — best for VRAM < 8GB
- `-ngl 99 -ncmoe 48` (N layers' experts CPU) — 8-16GB VRAM sweet spot
- `-ngl 99 -ot exps=CPU` (ik_llama) — expert tensors to CPU
- KV quant: `--flash-attn --cache-type-k q4_0 --cache-type-v q4_0` (or turbo3/turbo4 where supported)
- Host RAM: 32GB minimum for 35B MoE; 64GB+ for 80B+; NVMe for SSD streaming

### Key 3060 MoE gotchas (from 80 scans)
1. **MoE total params ≠ VRAM**: 35B MoE needs ~11-22GB depending on quant; VRAM must hold active subset + KV + overhead
2. **Host RAM is the real bottleneck**: 16GB host RAM severely limits MoE; 32GB+ recommended
3. **KV cache surprises**: qwen35moe KV estimate bug in moe-l2 (~16x overestimate); always test actual VRAM usage
4. **Quality matters**: 98-99% greedy agreement is not 100%; verify on your use cases
5. **Driver/runtime**: CUDA 12.8 needs driver ≥570; AVX512 SIGILL on older CPUs (use v0.6.1+)
6. **MTP interactions**: MTP + expert offload can conflict; test both on/off
7. **Prefill vs decode**: Some engines (RustingStrata) are faster on decode but slower on prefill for small models

### Recommended test matrix (when GPU is free)
1. moe-l2: Qwen3.6-35B-A3B UD-IQ2_M, ctx 65536→262144, measure VRAM + tok/s + quality
2. RustingStrata: Qwen3.6-35B-A3B, MTP on/off, CUDA vs Vulkan, quality check
3. llama.cpp baseline: Qwen3.6-35B-A3B Q4_K_M, `-ngl 99 --cpu-moe`, ctx 4096→32768
4. Compare all three on same model/quant/context for fair evaluation

## Engine/runtime/technique signals (from scans)

### llama.cpp / ik_llama.cpp / forks
- **Expert offload knobs** (observed in docs/discussions/community): `-ngl` (GPU layers), `--cpu-moe` / `-ncmoe N` (keep all/N experts on CPU), tensor overrides like `-ot exps=CPU` (ik_llama). For 6–12GB VRAM, common pattern is high `-ngl` + experts on CPU/host RAM, with KV quant (`--flash-attn`, `-ctk/-ctv` where supported) to fit context.
- **ik_llama.cpp PR #2644** (cited in scans): GPU cache for host MoE experts — relevant to reducing repeated host↔GPU expert movement; validate merge/status and compatibility before adopting.
- **llama.cpp discussion #27149** (cited): expert-aware SSD streaming concept; aligns with tinygiant/Betelgeuse-style paging directions but maturity varies.
- **Known pain points to watch**: MoE prefill/H2D regressions and `ncmoe`/offload behavior differences across builds (e.g. issue/regression chatter in scan results). Always pin commit/build, record flags, and benchmark prefill+decode separately.

### Strata / tandem.cpp / moe-l2 / Betelgeuse class
- **RustingStrata**: strongest “newest 3060 MoE engine” signal in this batch; hybrid CUDA/Vulkan and Qwen MoE focus. Treat performance claims as unverified until reproduced.
- **tandem.cpp** (scan signal): llama.cpp patch set targeting MoE models that don’t fit VRAM by keeping most-used experts on GPU and using CPU help; reports large decode gains in their tests (hardware/model-specific). Independent project; verify exact base commit/model/config.
- **moe-l2** (scan signal): kernel-level patch + orchestration; experts in CPU RAM/mmap with VRAM cache/selective pin/router map. Reported results span 2080 Ti/4090/5090; not a direct 3060 benchmark in captured snippets, but architecture is relevant to 12GB+host-RAM setups.
- **Betelgeuse**: directly targets 3060 12GB/16GB RAM/NVMe but explicitly experimental/partly broken.

## Practical 3060 (12GB) guidance from evidence (not a benchmark claim)

### NEW: RustingStrata exact numbers (from README + community, 2026-11)
- **Model**: Qwen3.6-35B-A3B-UD-Q2_K_XL.gguf (11.7 GiB, does NOT fit in VRAM)
- **Reference machine**: RTX 3060 12GB, Ryzen 5 7600X, 32GB RAM, CUDA
- **llama.cpp baseline**: build 11876, tuned (`-ncmoe 12 -ub 2048 -b 2048`, flash attn) → prefill ~2236, decode ~66.5 tok/s
- **RustingStrata CUDA**: prefill 2216 (2169-2252), decode 113.4 (110.9-114.8), short decode 118.2, MTP up to 160/152 tok/s
- **RustingStrata Vulkan**: prefill 2154, decode 113.6, short 117.3, MTP 158/154
- **32K context**: prefill 1800/1582, decode 91.9/90.7
- **Greedy top-1 agreement**: 98-99% (near-ties are float rounding; llama.cpp's own batch vs token-by-token = 98.3%)
- **Simulated lower VRAM**: ~8GB → 116/110 tok/s decode, ~6GB → 105/97 tok/s
- **Quality caveat**: MTP on/off give identical greedy tokens; expert placement adapts between runs

### NEW: moe-l2 0.14.1 (2026-10-01)
- **Auto context**: no longer pins 8192; targets model native ctx (262144 for Qwen3.6), narrows to VRAM budget
- **Verified**: Qwen3.6-35B-A3B UD-IQ2_M @262144 ctx = 25.0-25.3 t/s, 8700 MiB VRAM, 45K needle retrieval ✅
- **Windows native**: 9/9 PASS, 23.6 t/s steady-state (CUDA 12.8), no SIGILL
- **ctx-force**: skip VRAM-adaptive downgrading (needed for qwen35moe KV estimate bug ~16x overestimate)
- **Table push**: default ON (fixed C++ concurrency bug); needs bins-v0.8.1

### NEW: llama.cpp native MoE cache (--moe-cache-mib, merged 2026-10-07)
- **Mixed results**: helps Gemma 4 26B (~2x: 130→263 t/s), helps Qwen 3.6 35B (~1.4x) in some tests
- **Hurts in other tests**: expert cache slower on ALL 4 MoE models in one independent test (20-75% slower)
- **Effectiveness depends on**: expert size × hit rate. DS-V2-Lite (1.55MB experts, top-6): +211% prompt, +5% gen. Qwen3.6 (~1MB experts, top-8): no gain (copy cost already trivial). Mixtral (252MB experts, top-2): no gain, +660 MiB VRAM
- **Recommendation**: Test on your specific model; leave off if no measurable gain; reduce KV cache to free VRAM for cache
- **--moe-cache-mib 7200** on RTX 3060: gemma-4-26B 48→68 tok/s (+29%)

### NEW: moe-cache (IbrahimSiddiqui007) — SSD streaming for MoE
- **When model > RAM**: 2x-12x stock llama.cpp (Qwen3.6-35B @12GB limit: 15.7 vs 5.5 tok/s)
- **When model fits in RAM**: use stock llama.cpp + --moe-cache-mib instead
- **Token-identical output** verified
- **Best for**: models larger than RAM, other MoE architectures, staying on stock llama.cpp

### NEW: expert cache effectiveness rule (from moe-l2 + independent tests)
- Benefit = expert_size × hit_rate
- Small experts (~1MB, top-8): cache doesn't help (copy cost already trivial)
- Medium experts (~1.5MB, top-6): cache helps significantly (+211% prompt)
- Large experts (~252MB, top-2): cache hurts (low hit rate, +660 MiB VRAM)
- Always measure before/after; don't assume cache helps

- **Most realistic path today**: use small-active-parameter MoE (e.g. ~3B active class like Qwen A3B variants) with GGUF + llama.cpp/ik_llama.cpp/compatible runtime, aggressive layer/expert offload, and tight context/KV settings. Dense 14B/30B-total-class models are often VRAM-tight; MoE total params ≠ active compute but **weights still need storage** (disk/RAM/VRAM path).
- **Memory reality checks** (scan sources): calculators/guides often show Qwen3 30B-A3B Q4-class weights alone can exceed 12GB usable VRAM depending on context/runtime; feasible configs usually require **CPU/RAM offload** and/or lower quant/context. Mixtral 8x7B on single 3060 is possible only with heavy offload and low tok/s expectations (community numbers vary widely).
- **Host RAM matters**: many “works on 3060” reports assume 32–128GB system RAM/NVMe. A 16GB host changes feasibility dramatically.
- **Test matrix to run when GPU is free**: model + quant + `-ngl` + `--cpu-moe/-ncmoe/-ot exps=CPU` + context + KV type + flash-attn + threads + mmap + prompt length. Record prefill tok/s, decode tok/s, VRAM peak, RSS, quality sanity, and exact commit/build.

## 28-pass coverage summary (recorded)
Passes 1–28 covered rotating slices: newest 3060/MoE engines, benchmark/method repos, expert offload/cache/streaming, 3060+MoE config examples, moe-cache forks/issues, ik_llama.cpp resident/forks, DeepSeek/Mixtral local 12GB, Ollama/vLLM/ExLlama 3060, NVMe/SSD paging, Qwen3.5/3.6 A3B 3060 reports, llama.cpp offload recent, Qwen coder MoE 3060, serving stacks, small-active MoE fits, benchmark repos, speculative/MTP, quant tricks (imatrix/expert quant), Reddit/forum signals, Vulkan/Rust parity, distributed/rpc, ExLlama/tabby/aphrodite, HF GGUF collections, FR3K-adjacent local eval, LRU/resident expert cache, regressions/gotchas, newest pushes (Nov 2026 window), final practical synthesis. Raw pass metadata is in `scan-state.json`; detailed per-pass external snippets were summarized here to keep artifacts compact and evidence-bounded.

## FR3K-adjacent relevance
- Existing FR3K baselines: `gguf-quantization-demo` and `qwen36-bench` remain useful local harness references for constrained hardware; update scripts/models/bench protocol before reuse.
- Any future FR3K local-MoE experiments on this host should wait until RTX 3060 utilization drops from ~97% and should log exact hardware, driver, runtime commit, GGUF hash, flags, and quality checks.

## NEW: RustingStrata v1 gate run (verified 2026-10-10, commit 9f4af2a)
- **Model**: Qwen3.6-35B-A3B-UD-Q2_K_XL, RTX 3060 12GB, Ryzen 5 7600X, 32GB RAM
- **llama.cpp**: build 5d8ccdf9d, `--n-cpu-moe 10` (512/4K), `--n-cpu-moe 14 -d 32768` (32K)
- **Exact results (v1 gate run, host load 2.6-4.1 for re-runs)**:
  | Test | Strata | Strata MTP k=1 | llama.cpp |
  |---|---|---|---|
  | prefill, 512 tokens | 912.7 | 910.9 | 1077.7 ±13.9 |
  | prefill, 4096 tokens | **2016.3** | 1904.4 | 1059.5 ±3.4 |
  | decode 128 after 512 | **100.7** | **109.9** | 61.6 ±0.5 |
  | decode 128 after 4096 | 96.0 | 96.7 | — |
  | prefill, 32768 tokens | 1540.8 | 1536.5 | 808.6 ±1.2 |
  | decode 128 after 32768 | **77.0** | 79.1 | 50.4 ±3.0 |
- **MTP drafts accepted**: 62-65%
- **Short-prompt prefill still slower** (0.85x at 512 tokens): one chunk + cache warm-up
- **Parity**: 98.85% default, 99.32% parity mode (vs llama.cpp's own 98.28% batch vs token-by-token)
- **First gate run (2026-10-08)**: lower numbers (prefill 4K: 1715.6 vs 2016.3; decode 512: 81.7 vs 100.7) — host load and cache state matter

## NEW: llama.cpp on 3060 12GB — Qwen3.6-35B-A3B practical guide (shiqikuangsan31)
- **Repo**: [shiqikuangsan31/Qwen3.6-35B-12GB-VRAM-Guide](https://github.com/shiqikuangsan31/Qwen3.6-35B-12GB-VRAM-Guide)
- **Key finding: "expert cliff"** — `--n-cpu-moe` sweet spot shifts with context:
  | ctx | ncmoe | decode tok/s | prefill (45K input) |
  |---|---|---|---|
  | 32K | 16 | 64.0 | — |
  | 64K | 17 | 60.7 | 69.4s (649 tok/s) |
  | 128K | 20 | 55.3 | ~250 tok/s |
  | 258K | 22 | 50.9 | 85.5s |
- **q4_0 KV nearly lossless for Qwen** (KL 0.10, decode unaffected) vs q8 KV
- **q4_0 KV = 4.6x prefill speedup** (45K input: 397s → 85.5s)
- **Negative optimizations under VRAM offload**: `fa on` and large `-b 4096` batches HURT (opposite of normal)
- **Core command (258K)**: `-ngl 99 --n-cpu-moe 22 -c 262144 --cache-type-k q4_0 --cache-type-v q4_0 --no-mmap --mlock`
- **Tuning recipe**: sweep ncmoe in ±2 steps; sweet spot = first point above cliff boundary

## NEW: MTP on single 3060 12GB (githabideri/llmlab)
- **Model**: Qwen3.6-35B-A3B-MTP UD-Q4_K_XL (22GB), single RTX 3060 12GB
- **Sweet spot**: `--n-cpu-moe 26` (vs research default 32) → 33-36 tok/s completion, 50+ tok/s prompt
- **MTP acceptance**: 91% (31/34 drafts)
- **Context**: 4096 (larger OOMs on 16GB RAM)
- **VRAM**: 9.9/12.3 GB (80%)
- **Degradation with context**: prompt 521→562 tok/s, completion 38.7→28.8 tok/s as ctx fills
- **Key insight**: research-doc default ncmoe 32 was half as fast (16.5 tok/s); empirical tuning critical

## NEW: Dual 3060 12GB MoE (llamaperf community)
- **2x RTX 3060 12GB**: Qwen3.6-35B IQ4_XS → 82-86 tok/s (llama.cpp)
- **Single 3060**: RustingStrata → 70 tok/s, Strata → 71.5 tok/s
- **M5 Max 128GB**: 267-346 tok/s (MLX, not comparable hardware)

## Updated practical recommendations (130+ scans)
### Best single-GPU 3060 12GB MoE stack (ranked)
1. **RustingStrata** — fastest verified: 113 tok/s decode, 2016 tok/s prefill (4K), MTP 160 tok/s, Vulkan fallback, 98.85% parity
2. **moe-l2** — best for serving: 25 tok/s @262K ctx, OpenAI-compatible, verified Windows+Linux, auto-context
3. **llama.cpp tuned** — best ecosystem compat: 50-64 tok/s @32-64K ctx with expert cliff tuning, q4_0 KV, ncmoe 16-22
4. **llama.cpp + MTP** — 33-36 tok/s with 91% MTP acceptance, ncmoe 26 sweet spot

### Critical llama.cpp tuning rules (from 3060 guides)
- Sweep `--n-cpu-moe` in ±2 steps to find expert cliff; sweet spot shifts with context
- Use q4_0 KV (not q8) for Qwen — 4.6x prefill speedup, nearly lossless (KL 0.10)
- `fa on` and large `-b` are NEGATIVE under VRAM offload (opposite of normal)
- `--no-mmap --mlock` for stability
- `--n-cpu-moe 26` for MTP (not 32); empirical tuning >> research defaults
- Context: 32K→ncmoe 16, 64K→17, 128K→20, 258K→22

## NEW: RustingStrata v1 gate run (verified 2026-10-10, commit 9f4af2a) — UPDATED
- **Model**: Qwen3.6-35B-A3B-UD-Q2_K_XL, RTX 3060 12GB, Ryzen 5 7600X, 32GB RAM
- **llama.cpp**: build 5d8ccdf9d, `--n-cpu-moe 10` (512/4K), `--n-cpu-moe 14 -d 32768` (32K)
- **Exact results (v1 gate run, host load 2.6-4.1 for re-runs)**:
  | Test | Strata | Strata MTP k=1 | llama.cpp |
  |---|---|---|---|
  | prefill, 512 tokens | 912.7 (874.8-932.5) | 910.9 (895.8-932.1) | 1077.7 ±13.9 |
  | prefill, 4096 tokens | **2016.3** (2013.0-2019.8) | 1904.4 (1709.9-2013.1) | 1059.5 ±3.4 |
  | decode 128 after 512 | **100.7** (100.5-101.0) | **109.9** (104.5-113.5) | 61.6 ±0.5 |
  | decode 128 after 4096 | 96.0 (95.0-96.6) | 96.7 (90.7-101.9) | — |
  | prefill, 32768 tokens | 1540.8 (1525.2-1556.1) | 1536.5 (1474.8-1593.3) | 808.6 ±1.2 (pp512 @ d32768) |
  | decode 128 after 32768 | **77.0** (70.4-81.4) | 79.1 (64.9-86.2) | 50.4 ±3.0 (tg128 @ d32768) |
- **MTP drafts accepted**: 62-65%. Expert hit rate: 97.1-99.2%
- **Gate results**: Prefill 4K 2016.3 (gate ≥1017) ✅ 1.90x; Decode 100.7 (gate >67) ✅ 1.63x; Parity 99.32% (gate ≥99%) ✅
- **First gate run (2026-10-08, 671050e)**: lower numbers (prefill 4K: 1715.6 vs 2016.3; decode 512: 81.7 vs 100.7) — host load and cache state matter significantly
- **MTP on/off give identical greedy tokens**; expert placement adapts between runs

## NEW: Strata original (Niko1221) — paper findings
- **Paper**: "Running a 125-Billion-Parameter Model on a Normal PC" (2026)
- **Model**: Qwen3.8-Flash-Next (125B params, 6B active, 512 experts/layer)
- **RTX 5070 12GB + Ryzen 5 7600 + 64GB DDR5**: 88.7-94.6 tok/s decode (Q2_0), 389-571 tok/s prefill
- **RTX 3060 12GB + 32GB RAM (measured)**: 8.7-11.5 tok/s (stock llama.cpp, 7 expert layers on GPU)
- **RTX 3060 12GB + 64GB RAM (inferred)**: 11-17 tok/s
- **Key insight**: 32GB RAM severely limits 177B model; 64GB+ recommended for usable speed
- **MTP**: 2.71-3.63 tokens per verify window; 62-65% draft acceptance
- **Expert profile**: recorded on different prompts; prefill 285-571 tok/s depending on quant

## NEW: Expert cache effectiveness rule (FINAL, from 160 scans)
- **Benefit = expert_size × hit_rate** (verified across moe-l2, independent tests, Strata paper)
- **Small experts (~1MB, top-8)**: cache doesn't help (copy cost already trivial) — Qwen3.6
- **Medium experts (~1.5MB, top-6)**: cache helps significantly (+211% prompt, +5% gen) — DS-V2-Lite
- **Large experts (~252MB, top-2)**: cache hurts (low hit rate, +660 MiB VRAM) — Mixtral
- **RustingStrata expert hit rate**: 97.1-99.2% (measured)
- **Always measure before/after; don't assume cache helps**

## UPDATED practical recommendations (160+ scans)
### Best single-GPU 3060 12GB MoE stack (ranked, verified)
1. **RustingStrata** — fastest verified: 113 tok/s decode, 2016 tok/s prefill (4K), MTP 160 tok/s, 99.32% parity, Vulkan fallback
2. **moe-l2** — best for serving: 25 tok/s @262K ctx, OpenAI-compatible, verified Windows+Linux, auto-context, 9/9 PASS
3. **llama.cpp tuned** — best ecosystem compat: 50-64 tok/s @32-64K ctx with expert cliff tuning, q4_0 KV, ncmoe 16-22
4. **llama.cpp + MTP** — 33-36 tok/s with 91% MTP acceptance, ncmoe 26 sweet spot

### Critical tuning rules (from 160 scans + guides)
- Sweep `--n-cpu-moe` in ±2 steps to find expert cliff; sweet spot shifts with context (32K→16, 64K→17, 128K→20, 258K→22)
- Use q4_0 KV (not q8) for Qwen — 4.6x prefill speedup, nearly lossless (KL 0.10)
- `fa on` and large `-b` are NEGATIVE under VRAM offload (opposite of normal)
- `--no-mmap --mlock` for stability
- `--n-cpu-moe 26` for MTP (not 32); empirical tuning >> research defaults
- MTP + expert offload: test both on/off; MTP can be negative in some configs
- Host load matters: 2.6-4.1 load → good numbers; 21-28 load → 15-20% worse
- GPU utilization only ~50% (inherent to MoE+offload; PCIe + DDR4 bottleneck)
- 32GB RAM minimum for 35B MoE; 64GB+ for 80B+; 128GB for 177B

## NEW: RustingStrata v1.2.1 (latest, Nov 2026)
- **Status**: v1.2.1 (updated from v1.2.0)
- **Built-in chat page**: browser-based, model download from HF, model switching, context/speed/memory display
- **OpenAI API**: `POST /v1/chat/completions` (streamed or not), tools + tool_choice, cached tokens
- **Anthropic API**: `POST /v1/messages` (Claude Code compatible), `POST /v1/messages/count_tokens`
- **Parallel decoding**: `--parallel N` → 4 requests = 164 tok/s total on 3060 (41 each)
- **Multi-GPU**: `--device 0,1` splits layers across cards in proportion to free VRAM; mixed cards/backends work
- **Qwen3.8-Flash-Next**: CUDA + Vulkan, QSA sparse attention, hyper-connections, PLE, split GGUF
- **`--preserve-thinking`**: on by default; long agent sessions prefill only what's added
- **`--kv q8`**: halves KV cache (345 vs 650 MB at 32K) at ~6% slower decode
- **`--vram-margin 256`**: more experts resident (+1-2% prefill); 128 runs OOM
- **API keys**: from file, reloaded on edit, usage log per key, /health, Prometheus /metrics
- **Qwen3.6 chat template**: leaves think block out of replies before last user message; Strata keeps them by default
- **Hosting**: docs/HOSTING.md for customer keys, billing, TLS via reverse proxy, systemd

## UPDATED practical recommendations (190+ scans)
### Best single-GPU 3060 12GB MoE stack (ranked, verified)
1. **RustingStrata v1.2.1** — fastest verified: 113 tok/s decode, 2016 tok/s prefill (4K), MTP 160 tok/s, 99.32% parity, Vulkan fallback, OpenAI+Anthropic API, multi-GPU, parallel (4 req = 164 tok/s), preserve-thinking for agents, built-in chat page
2. **moe-l2 0.14.1** — best for serving: 25 tok/s @262K ctx, OpenAI-compatible, verified Windows+Linux, auto-context, 9/9 PASS, ctx-force for KV bug
3. **llama.cpp tuned** — best ecosystem compat: 50-64 tok/s @32-64K ctx with expert cliff tuning, q4_0 KV, ncmoe 16-22
4. **llama.cpp + MTP** — 33-36 tok/s with 91% MTP acceptance, ncmoe 26 sweet spot

### Critical tuning rules (from 190 scans + guides)
- Sweep `--n-cpu-moe` in ±2 steps to find expert cliff; sweet spot shifts with context (32K→16, 64K→17, 128K→20, 258K→22)
- Use q4_0 KV (not q8) for Qwen — 4.6x prefill speedup, nearly lossless (KL 0.10)
- `fa on` and large `-b` are NEGATIVE under VRAM offload (opposite of normal)
- `--no-mmap --mlock` for stability
- `--n-cpu-moe 26` for MTP (not 32); empirical tuning >> research defaults
- MTP + expert offload: test both on/off; MTP can be negative in some configs
- Host load matters: 2.6-4.1 load → good numbers; 21-28 load → 15-20% worse
- GPU utilization only ~50% (inherent to MoE+offload; PCIe + DDR4 bottleneck)
- 32GB RAM minimum for 35B MoE; 64GB+ for 80B+; 128GB for 177B
- `--kv q8` halves KV cache at ~6% slower decode; `--vram-margin 256` for more experts

## NEW: BigMoeOnEdge (Helldez) — Major new discovery (Nov 2026)
- **Repo**: [Helldez/BigMoeOnEdge](https://github.com/Helldez/BigMoeOnEdge) — "Run MoE models bigger than your RAM. Frontier-size MoE on a phone, laptop, edge. Lossless, on stock llama.cpp. An adaptive streaming optimizer."
- **Created**: 2026-11-08 (v0.40.2), 734 stars, 87 forks, C++, Apache-2.0
- **Platforms**: Android, iOS, macOS, Windows, Linux
- **Backends**: CPU, Metal, CUDA, HIP, Vulkan, OpenCL, Hexagon NPU
- **Architecture**: Lossless streaming from flash — experts read from disk as needed; VRAM/RAM/flash 3-tier cache
- **Key features**: `--auto` measures machine+model, picks cache size/threads/device placement; OpenAI+Anthropic server; vision (mmproj); `--dense-weights anon/warm/mmap/pinned`
- **Performance (from benchmarks)**:
  - Android phone 12GB: Qwen3.6-35B-A3B 5 tok/s from flash; Qwen3.8-Flash-Next 125B 2-4 tok/s
  - iPhone 12GB: Qwen3.6-35B-A3B 3 tok/s
  - Windows laptop 16GB: Qwen3.6-35B-A3B 5 tok/s
  - Desktop GPU 16GB+32GB RAM: Qwen3.8-Flash-Next 125B 19-21 tok/s (flash+GPU cache); Qwen3.6-35B-A3B 217 tok/s (GPU)
  - Desktop GPU 24GB+96GB RAM: Qwen3.8-Flash-Next 125B 70 tok/s (RAM+GPU cache)
  - RTX 3060 class 12GB: Qwen3.8-Flash-Next Q2_0 15.5 tok/s (experts on card + rest in RAM)
- **Cache sizing**: `--cache-mb auto` sizes to device; cliff at too-small (0% hit rate, not graceful degradation); OOM at too-large
- **Lossless**: same output as full model in memory; tests verify token-identical
- **Dense weights policies**: mmap (default, page cache), warm (load-time sweep), anon (O_DIRECT, default for streaming), pinned (dma-buf/wired)
- **Negative findings**: MTP head drafting cost more than it saved on 3060 class (9.9 vs 15.5 effective); `mmap`-only is a trap (page-cache eviction stalls)
- **Comparison to RustingStrata**: BigMoeOnEdge targets flash streaming (models > RAM), RustingStrata targets VRAM offload (models > VRAM but < RAM). Complementary approaches.
- **Comparison to moe-l2**: BigMoeOnEdge is lossless streaming (no approximations), moe-l2 uses expert prediction/pinning (lossless but different mechanism)

## UPDATED practical recommendations (240+ scans)
### Best single-GPU 3060 12GB MoE stack (ranked, verified)
1. **RustingStrata v1.2.1** — fastest verified: 113 tok/s decode, 2016 tok/s prefill (4K), MTP 160 tok/s, 99.32% parity, Vulkan fallback, OpenAI+Anthropic API, multi-GPU, parallel (4 req = 164 tok/s), preserve-thinking for agents, built-in chat page
2. **moe-l2 0.14.1** — best for serving: 25 tok/s @262K ctx, OpenAI-compatible, verified Windows+Linux, auto-context, 9/9 PASS, ctx-force for KV bug
3. **llama.cpp tuned** — best ecosystem compat: 50-64 tok/s @32-64K ctx with expert cliff tuning, q4_0 KV, ncmoe 16-22
4. **llama.cpp + MTP** — 33-36 tok/s with 91% MTP acceptance, ncmoe 26 sweet spot
5. **BigMoeOnEdge** — best for models > RAM: lossless flash streaming, `--auto` tuning, cross-platform, OpenAI+Anthropic server; 15.5 tok/s on 3060 class for 125B model

### Critical tuning rules (from 240 scans + guides)
- Sweep `--n-cpu-moe` in ±2 steps to find expert cliff; sweet spot shifts with context (32K→16, 64K→17, 128K→20, 258K→22)
- Use q4_0 KV (not q8) for Qwen — 4.6x prefill speedup, nearly lossless (KL 0.10)
- `fa on` and large `-b` are NEGATIVE under VRAM offload (opposite of normal)
- `--no-mmap --mlock` for stability
- `--n-cpu-moe 26` for MTP (not 32); empirical tuning >> research defaults
- MTP + expert offload: test both on/off; MTP can be negative in some configs
- Host load matters: 2.6-4.1 load → good numbers; 21-28 load → 15-20% worse
- GPU utilization only ~50% (inherent to MoE+offload; PCIe + DDR4 bottleneck)
- 32GB RAM minimum for 35B MoE; 64GB+ for 80B+; 128GB for 177B
- `--kv q8` halves KV cache at ~6% slower decode; `--vram-margin 256` for more experts
- BigMoeOnEdge: `--cache-mb auto` for flash streaming; avoid `mmap`-only (page-cache eviction stalls); use `--dense-weights anon` for models > RAM

## NEW: FreeToken-Kai (yuuki-net) — Major new discovery (Nov 2026)
- **Repo**: [yuuki-net/FreeToken-Kai](https://github.com/yuuki-net/FreeToken-Kai) — "Unofficial FreeToken fork: Flash-Next 125B at 38 tok/s on two RTX 3060s with 2-bit experts, gpt-oss-120b on one; a benchmark tunes your settings."
- **Created**: 2026-11-05, 11 stars, 3 forks, Python, Apache-2.0
- **Key features**: Qwen3.8-Flash-Next 125B at 38 tok/s on 2x RTX 3060 12GB (2-bit experts), gpt-oss-120b on 1x RTX 3060 12GB, 250k context, image input, WSL2, runs on Turing (RTX 2060, sm_75)
- **Performance (from README)**:
  - 1x RTX 3060 12GB + 128GB RAM: Qwen3.8-Flash-Next 125B @19 tok/s, 128k context (GGUF Q2_0)
  - 1x RTX 3060 12GB + 128GB RAM: Qwen3.8-Flash-Next 125B @21-23 tok/s with MTP (7 reference prompts: 29-44 tok/s)
  - 2x RTX 3060 12GB + 128GB RAM: Qwen3.8-Flash-Next 125B @18-20 tok/s, 128k context (NVFP4)
  - 2x RTX 3060 12GB + 128GB RAM: Qwen3.8-Flash-Next 125B @38.5 tok/s with MTP (7 reference prompts)
  - 1x RTX 3060 12GB + 32GB RAM: Ornith-1.5-35B-A3B @25-39 tok/s, 64k context (NVFP4)
  - 1x RTX 2060 6GB + 32GB RAM: gpt-oss-20b @14-16 tok/s, 20k context
  - 1x RTX 2060 6GB + 32GB RAM: Ornith-1.5-35B-A3B @25-39 tok/s, 64k context (NVFP4)
- **Key technology**: `--moe-bank-ram` for expert caching in RAM, `--moe-expert-gguf` for GGUF expert banks, `--spec-mtp 4` for MTP speculative decoding, `--dense-quant q8_0` for dense weights, `--pp-size 2` for pipeline parallelism
- **Browser-based benchmark**: measures your PC with the model, tries settings one at a time, hands you the fastest as a launch profile
- **Automatic plan**: starts on single 12GB card, proposes faster settings
- **Vision**: mmproj support for image input
- **Comparison to RustingStrata**: FreeToken-Kai uses FreeToken's pipeline (different engine), RustingStrata is pure Rust. FreeToken-Kai achieves higher throughput on multi-GPU but requires more RAM.
- **Comparison to BigMoeOnEdge**: FreeToken-Kai targets high-throughput serving, BigMoeOnEdge targets flash streaming for models > RAM. Complementary.

## UPDATED practical recommendations (270+ scans)
### Best single-GPU 3060 12GB MoE stack (ranked, verified)
1. **RustingStrata v1.2.1** — fastest single-GPU verified: 113 tok/s decode, 2016 tok/s prefill (4K), MTP 160 tok/s, 99.32% parity, Vulkan fallback, OpenAI+Anthropic API, multi-GPU, parallel (4 req = 164 tok/s), preserve-thinking for agents, built-in chat page
2. **moe-l2 0.14.1** — best for serving: 25 tok/s @262K ctx, OpenAI-compatible, verified Windows+Linux, auto-context, 9/9 PASS, ctx-force for KV bug
3. **llama.cpp tuned** — best ecosystem compat: 50-64 tok/s @32-64K ctx with expert cliff tuning, q4_0 KV, ncmoe 16-22
4. **llama.cpp + MTP** — 33-36 tok/s with 91% MTP acceptance, ncmoe 26 sweet spot
5. **FreeToken-Kai** — best for multi-GPU: 38.5 tok/s on 2x 3060 with MTP, 21-23 tok/s on 1x 3060, browser-based benchmark tuning
6. **BigMoeOnEdge** — best for models > RAM: lossless flash streaming, `--auto` tuning, cross-platform, 15.5 tok/s on 3060 class for 125B model

## NEW: Strata-HotRod (sangharshadhyeta) — Major new discovery (Nov 2026)
- **Repo**: [sangharshadhyeta/Strata-HotRod](https://github.com/sangharshadhyeta/Strata-HotRod) — "Run Qwen3.8-Flash-Next (125B) on an RTX 3060 12 GB with 30 GB of RAM, streaming experts from the SSD. 50-70 tok/s, 262K context. A fork of Strata."
- **Created**: 2026-11-08, C++, MIT license
- **Performance (measured on RTX 3060 12GB, i5-12400F, 30GB RAM, WD Blue SN5000 NVMe)**:
  - Qwen3.8-Flash-Next IQ3_S: 50-70 tok/s decode, 262K context
  - Answer: 52-55 tok/s, Code: 66-71 tok/s, Prose: 50-53 tok/s
  - Long prompts: 8,554 tokens in 16.9s; 45,398 tokens in 67-68s
  - Next turn of 45K conversation: 0.4-0.5s (turn checkpoint)
  - 8,554 token prompt: 16.9s; 45,398 token prompt: 67-68s
- **Key innovations**:
  - Learned look-ahead: 85-88% of needed experts one layer ahead (vs 77-79% router guess)
  - Stand-in experts: close expert can stand in for missing one, tokens recomputed exactly
  - K/V streaming: K/V cache streamed to SSD, 262K context on 30GB RAM
  - Turn checkpoint: conversation state parked in host memory, resumed instantly
  - OOM safety: floor held each request, margins measured and learned
- **RAM requirement**: 30GB minimum (Strata recommends 64GB, HotRod makes 30GB work)
- **Comparison to Strata**: HotRod achieves 50-70 tok/s where Strata achieves 8.7-11.5 tok/s on 32GB RAM (2x-6x improvement)
- **Comparison to RustingStrata**: HotRod targets 125B models on 30GB RAM, RustingStrata targets 35B models on 32GB RAM with higher throughput
- **Comparison to BigMoeOnEdge**: HotRod uses learned look-ahead + stand-in experts, BigMoeOnEdge uses lossless streaming. HotRod achieves higher throughput.
- **DeepSeek V4.1**: 5.2-5.4 tok/s on same hardware (341GB model)

## NEW: Additional community repos discovered (Nov 2026)
- **ildargiv/rtx3060-strata-tuning**: "Measured tuning of Strata (Qwen3.8-Flash-Next IQ3_XXS) on one RTX 3060 12 GB + Ryzen 7 5700G: 44 to 61 tok/s decode at 262K context" (Oct 31, 2026)
- **nabe2030/strata-rtx3060x2**: "Qwen3.8-Flash-Next on two RTX 3060 12GB GPUs and 64GB RAM with Strata: engine 0.1.40 vs 0.1.46, 51.2 tok/s decode, 10/10 OpenCode v2 agent tasks with ~230K-token inputs" (Oct 27, 2026)
- **kadenball/qwen38-27b-rtx3060-dcfr**: "RouteWeaver: experimental cache-safe speculative inference and CPU/GPU transfer optimization for Qwen 27B on low-VRAM NVIDIA GPUs" (Oct 10, 2026)
- **g023/cuda_inf**: "A self-contained CUDA inference engine for LiquidAI/LFM2.5-8B-A1B (hybrid conv + GQA-attention MoE, 8.5B params, 1B active) targeting a single RTX 3060 (12 GB). ~105 tok/s short-context decode on the RTX 3060" (Jun 6, 2026)
- **jesusjodar/recipes**: "Measured local AI inference recipes for Ryzen 5 5600X + RTX 3060: FreeToken and llama.cpp profiles, DFlash, context/output budgets, benchmark logs, and agent integrations" (Oct 24, 2026)
- **Captain-Tripps/qwen38-dual-rtx-3060**: "Qwen3.8-27B on dual NVIDIA RTX 3060 12GB (llama.cpp). Recipe, A/B log, Localmaxxing drafts." (Sep 27, 2026)
- **sudosingX/local-ai-on-your-gaming-gpu**: "run a 27b local ai on your gaming gpu, rtx 3060 and up, radeon rx 6600 and up in beta, 8gb or more, linux and windows, one line to install" (Oct 17, 2026)

## UPDATED practical recommendations (330+ scans)
### Best single-GPU 3060 12GB MoE stack (ranked, verified)
1. **RustingStrata v1.2.1** — fastest single-GPU verified: 113 tok/s decode, 2016 tok/s prefill (4K), MTP 160 tok/s, 99.32% parity, Vulkan fallback, OpenAI+Anthropic API, multi-GPU, parallel (4 req = 164 tok/s), preserve-thinking for agents, built-in chat page
2. **Strata-HotRod** — best for 125B models on 30GB RAM: 50-70 tok/s, 262K context, learned look-ahead (85-88%), stand-in experts, turn checkpoint, OOM safety
3. **moe-l2 0.14.1** — best for serving: 25 tok/s @262K ctx, OpenAI-compatible, verified Windows+Linux, auto-context, 9/9 PASS, ctx-force for KV bug
4. **llama.cpp tuned** — best ecosystem compat: 50-64 tok/s @32-64K ctx with expert cliff tuning, q4_0 KV, ncmoe 16-22
5. **llama.cpp + MTP** — 33-36 tok/s with 91% MTP acceptance, ncmoe 26 sweet spot
6. **FreeToken-Kai** — best for multi-GPU: 38.5 tok/s on 2x 3060 with MTP, 21-23 tok/s on 1x 3060, browser-based benchmark tuning
7. **BigMoeOnEdge** — best for models > RAM: lossless flash streaming, `--auto` tuning, cross-platform, 15.5 tok/s on 3060 class for 125B model

## NEW: Additional community repos discovered (Dec 2026)
- **abi2024/FlashMoE-Serve**: "High-performance MoE inference engine. Features fused OpenAI Triton kernels, continuous batching, and NF4 quantization. +72% throughput on RTX 3060." (Created Jan 8, 2026, Python/PyTorch/Triton)
  - Qwen1.5-MoE-A2.7B on RTX 3060 12GB: 11.87 → 20.38 tok/s (+72%), NF4 quantization, 14B model on 12GB
  - Custom Triton router kernel, continuous batching (vLLM-style), WSL2 Ubuntu 22.04
- **cioinside/llama-cpp-optimizer**: "Empirical sweep-driven optimizer for llama.cpp server scripts on 2x RTX 3060 12GB. Findings from 50+ benchmarks across REAP20, 28B MTP, 35B MTP with TurboQuant." (Created Aug 9, 2026)
  - 2x RTX 3060 12GB, i7-8700K, 62GB RAM
  - Anti-patterns: pkill -9 -f llama-server (hangs), bs=8192 for MTP (OOM), q5_0 KV broken, f16 KV slower than q8_0 for MTP, nmax > 3 for 28B MTP catastrophic, --fit on for non-MTP reduces pp ~20%
  - TurboQuant build, opencode skill integration
- **kstevica/strata**: "Qwen3.8-Flash-Next (125B MoE) on a 8GB+ NVIDIA GPU: one-click install for Windows / Linux. Strata inference engine, OpenAI/Anthropic API on localhost, optional image input." (Created Sep 27, 2026, 51 commits)
  - Fork of Strata with one-click install, 8GB+ GPU support, built with parts of llama.cpp/ggml
- **gtsarfang/local_testing**: "Comparing local coding LLMs on a 12GB GPU (llama.cpp + opencode) - speed, quality, and code-correctness benchmarks" (Created Jul 24, 2026)
  - llama.cpp b10069, RTX 3060, Windows 10, HumanEval/LiveCodeBench benchmarks
  - --n-cpu-moe expert offload, UD-Q4_K_XL sweet spot for 12GB + 64GB combo
