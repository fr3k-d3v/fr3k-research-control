# Candidate ledger — 2026-11-09

All entries below are **unverified leads**, not demonstrated Omarchy performance gains.

| Candidate | Source | Evidence and compatibility | Next gate |
|---|---|---|---|
| RustingStrata | https://github.com/RustingStudio/RustingStrata | Author-reported RTX3060 benefits; model/engine compatibility unverified | Source, license, CUDA and benchmark audit |
| Betelgeuse | https://github.com/Betelgeuse-AI/Betelgeuse | Experimental expert caching; reported broken paths | Correctness and crash audit |
| tinygiant | https://github.com/jerryjokesalot/tinygiant | Prototype SSD expert streaming | Disk I/O and correctness instrumentation |
| moe-hotcache | https://github.com/ap03906101/moe-hotcache | AMD/other-model results, not NVIDIA/Qwen3-Coder proof; reported prefill regression with pinned memory | Audit scheduling, DMA, CUDA portability and negative findings |
| weight-streaming | https://github.com/i-mrDed/weight-streaming | Instrumentation using different model, not speedup evidence | Validate metric definitions and overhead |
| routing traces | https://huggingface.co/datasets/carlosfelipe/moe-anywhere-routing-traces | Different GPU and model | Metadata/license audit; simulation only |
| RTX3060 reference benchmarks | https://github.com/harshithmohan/local-llm-benchmarks | Comparison reference, not FR3K result | Reproduce same model/quant |
| RTX3060 configurations | https://github.com/Ajay9o9/runs-on-a-3060 | Configuration examples | Compatibility review |

Source snapshots and negative findings must be updated by canonical URL + upstream commit, with immutable observations. Do not silently overwrite old entries.

## Scan-pass additions — 2026-11-09 (360+ passes, local MoE on RTX 3060 12GB)

| Candidate | Source | Evidence and compatibility | Next gate |
|---|---|---|---|
| RustingStrata v1.2.1 | https://github.com/RustingStudio/RustingStrata | 113 tok/s decode, 2016 tok/s prefill (4K), MTP 160 tok/s, 99.32% parity, Vulkan fallback, OpenAI+Anthropic API, multi-GPU, parallel (4 req=164 tok/s) | Source, license, CUDA/Vulkan audit, quality check |
| Strata-HotRod | https://github.com/sangharshadhyeta/Strata-HotRod | 50-70 tok/s on Qwen3.8-Flash-Next 125B, 262K ctx, 30GB RAM, learned look-ahead (85-88%), stand-in experts, turn checkpoint | Reproduce on RTX 3060 + 30GB RAM |
| moe-l2 0.14.1 | https://github.com/yalun753/moe-l2 | 25 tok/s @262K ctx, OpenAI-compatible, 9/9 PASS, ctx-force for KV bug, auto-context | Reproduce on RTX 3060, test Qwen3.6-35B-A3B |
| FreeToken-Kai | https://github.com/yuuki-net/FreeToken-Kai | 38.5 tok/s on 2x 3060 (MTP), 21-23 tok/s 1x, 250k ctx, browser benchmark, --moe-bank-ram, --spec-mtp 4 | Reproduce on 1x and 2x RTX 3060 |
| BigMoeOnEdge | https://github.com/Helldez/BigMoeOnEdge | Lossless flash streaming, --auto tuning, cross-platform, 15.5 tok/s on 3060 class for 125B | Reproduce on RTX 3060 12GB |
| FlashMoE-Serve | https://github.com/abi2024/FlashMoE-Serve | +72% throughput (11.87→20.38 tok/s), Triton kernels, continuous batching, NF4 quant | Reproduce on RTX 3060, test Qwen models |
| Strata (Niko1221) | https://github.com/Niko1221/strata | 25-38 tok/s, 125B on 12GB, one-click install, OpenAI+Anthropic, image input | Reproduce on RTX 3060 |
| Strata (kstevica fork) | https://github.com/kstevica/strata | One-click install, 8GB+ GPU support, built with llama.cpp/ggml parts | Compatibility review |
| cuda_inf | https://github.com/g023/cuda_inf | ~105 tok/s on LFM2.5-8B, self-contained CUDA, sm_75+ | Test on RTX 3060 |
| cioinside/llama-cpp-optimizer | https://github.com/cioinside/llama-cpp-optimizer | 50+ benchmarks on 2x RTX 3060, documented anti-patterns, TurboQuant | Review anti-patterns, apply to tuning |
| ildargiv/rtx3060-strata-tuning | https://github.com/ildargiv/rtx3060-strata-tuning | 44→61 tok/s on single 3060, measured tuning | Reproduce on RTX 3060 |
| nabe2030/strata-rtx3060x2 | https://github.com/nabe2030/strata-rtx3060x2 | 51.2 tok/s on 2x 3060, 10/10 OpenCode tasks at 230K ctx | Reproduce on 2x RTX 3060 |
| Betelgeuse | https://github.com/Betelgeuse-AI/Betelgeuse | Frontier MoE on 3060+16GB RAM+NVMe, experimental, partly broken | Correctness and crash audit |
| tinygiant | https://github.com/jerryjokesalot/tinygiant | Prototype SSD expert streaming, Qwen3 30B A3B layout | Disk I/O and correctness instrumentation |
| moe-hotcache | https://github.com/ap03906101/moe-hotcache | AMD/other-model results, not NVIDIA/Qwen3-Coder proof | Audit scheduling, DMA, CUDA portability |

### Critical tuning rules (from 360+ scans)
- Expert cliff: ncmoe 16 (32K) → 17 (64K) → 20 (128K) → 22 (258K)
- q4_0 KV: 4.6x prefill speedup, KL 0.10 (nearly lossless for Qwen)
- Negative optimizations under VRAM offload: fa on, large -b, MTP, threads 20 all HURT
- MTP sweet spot: ncmoe 26 (not 32), 91% acceptance, 33-36 tok/s
- Host RAM: 32GB min for 35B; 64GB+ for 80B+; 128GB for 177B
- FreeToken-Kai: MTP helps on 2-card (18→38.5 tok/s) but hurts on 1-card
- q4_0 KV decode is flat from 8k to 125k on sparse backend
- Host load matters: 2.6-4.1 load → good; 21-28 load → 15-20% worse


## Colibrì + DeepSeek V4 Flash evaluation — 2026-11-14

| Candidate | Source | Evidence and compatibility | Next gate |
|---|---|---|---|
| Colibrì inference runtime | https://github.com/JustVugg/colibri | Native C runtime; DeepSeek V4 Flash engine; official safetensors and GGUF support; optional CUDA and Vulkan paths; OpenAI/Anthropic API. Upstream evidence reviewed, no local install. | Recheck pinned source and run read-only Omarchy hardware/model-fit preflight |
| DeepSeek V4 Flash 0731 full checkpoint | https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731 | Official 284B checkpoint, ~167 GB, MIT; Colibrì catalogue lists 16 GB minimum / 32 GB recommended RAM. Omarchy fit UNKNOWN. | Confirm free RAM, NVMe capacity, CUDA/Vulkan and planner status before download |
| DeepSeek V4 Flash 0731 full-model GGUF UD-IQ2_XXS | https://huggingface.co/unsloth/DeepSeek-V4-Flash-0731-GGUF | Full 284B architecture, very low-bit quant; Colibrì reports ~85 GB and upstream RTX PRO 4000/62 GB RAM measurements. Hugging Face lists 90.9 GB; reconcile exact file manifest. | Confirm disk budget; download only after approval; test quant quality and Vulkan/CUDA |
| DeepSeek V4 Flash REAP 150B | https://huggingface.co/puwaer/DeepSeek-V4-Flash-0731-reap-150b | MIT; 132 routed experts rather than 256; ~85 GB; separate pruned model, not full V4 Flash. | Fallback only if full-model routes are blocked or unsuitable |

All performance figures above are upstream claims, not Omarchy results. See [the dedicated evaluation plan](../research/colibri-deepseek-v4/README.md).

## Colibrì / DeepSeek V4 Flash live preflight update — 2026-11-14

| Candidate | Source | Evidence and compatibility | Next gate |
|---|---|---|---|
| Colibrì v2.1.0 on Omarchy | https://github.com/JustVugg/colibri/releases/tag/v2.1.0 | Source pinned at 704a3f68184b78367a04cb5526e428dc2f90f05b; CPU and CUDA sm_86 engine builds pass; CUDA runtime smoke passes; generic Vulkan device init passes. No model weights downloaded. | Import and run a real DeepSeek V4 artifact after approval |
| AtomicChat AD-IQ2_XS | https://huggingface.co/AtomicChat/DeepSeek-V4-Flash-0731-GGUF/tree/main/AD-IQ2_XS | Full 284B DeepSeek V4 Flash architecture; 85.1 GB, four shards; publisher reports 79.240% top-1 and KLD 0.3947 on its own harness; MIT. Current volume has 93.88 GB free, leaving ~8.8 GB. | Preferred full-model candidate; final disk recheck and explicit 85.1 GB download approval |
| AtomicChat AD-IQ2_XXS | https://huggingface.co/AtomicChat/DeepSeek-V4-Flash-0731-GGUF/tree/main/AD-IQ2_XXS | Full 284B architecture; 78.5 GB; publisher reports 77.459% top-1 and KLD 0.4544. | Lower-quality, more-headroom alternative |
| Unsloth UD-IQ2_XXS | https://huggingface.co/unsloth/DeepSeek-V4-Flash-0731-GGUF | Full 284B architecture; 90.9 GB listing; insufficient disk reserve on current volume. | Blocked unless more storage becomes available |
| REAP 150B | https://huggingface.co/puwaer/DeepSeek-V4-Flash-0731-reap-150b | Catalogue status good at 84.7 GB, but only 150B and 132 routed experts; not the full model. | Fallback only |

AtomicChat quality metrics are publisher claims, not FR3K benchmarks. See [quantization comparison](../research/colibri-deepseek-v4/MODEL-QUANTIZATION-COMPARISON.md), [local preflight](../research/colibri-deepseek-v4/LOCAL-PREFLIGHT-2026-11-14.md), and [build evidence](../research/colibri-deepseek-v4/BUILD-AND-SMOKE-TESTS.md).
