# Model and hardware fit

**Assessment date:** 2026-11-14  
**Target hardware (prior inventory; re-observation required):** Omarchy Linux, NVIDIA RTX 3060 LHR 12 GB, 32 GB system RAM.  
**Fit status:** PLAUSIBLE / TIGHT / NOT YET VERIFIED.

## Do not confuse these model names

This work targets **DeepSeek V4 Flash 0731**, not DeepSeek V4.1 Flash.

- DeepSeek V4 Flash: 284B total parameters, 43 layers, 256 routed experts plus one shared expert, top-6 routing. The official checkpoint uses FP4 routed experts and FP8 dense weights.
- DeepSeek V4.1 Flash: a separate 552B model, approximately 510 GB on disk, with a different engine and additional engram state. It is outside this evaluation.

## Candidate artifacts

| Artifact | Size | Architecture / precision | Runtime path | Status |
|---|---:|---|---|---|
| Official deepseek-ai/DeepSeek-V4-Flash-0731 | ~167 GB | Full 284B; FP4 experts, FP8 dense; official safetensors | Colibrì deepseek_v4; CPU-canonical with optional CUDA | PREFERRED fidelity reference |
| Unsloth UD-IQ2_XXS GGUF | Colibrì README: ~85 GB; Hugging Face listing: 90.9 GB | Full 284B model architecture; very low-bit dynamic quant | coli import, deepseek_v4; CPU/Vulkan/CUDA GGUF paths | PREFERRED lower-disk full-model experiment |
| puwaer/DeepSeek-V4-Flash-0731-reap-150b | ~85 GB | 150B expert-pruned; 132 rather than 256 routed experts | Colibrì native deepseek_v4 safetensors path | FALLBACK, distinct model |
| puwaer/DeepSeek-V4-Flash-0731-reap-150b-gguf | Variant-dependent | Pruned model with additional GGUF quantization | GGUF import | Optional fallback only; validate exact file |

**Size reconciliation:** Colibrì's README rounds the Unsloth UD-IQ2_XXS GGUF to 85 GB; the Hugging Face model listing reports 90.9 GB. Treat 90.9 GB as the safer download-planning figure until the exact file manifest is captured. Do not mix GB and GiB in benchmark reports.

**Quantisation warning:** UD-IQ2_XXS is not the official FP4/FP8 checkpoint. It is the full model architecture in a very low-bit GGUF representation. Quality must be measured; it must not be described as numerically equivalent to the official checkpoint.

**REAP warning:** REAP removes 124 of the original 256 routed experts per layer. It is not the full model, even though it shares the DeepSeek V4 Flash family and loads with the same Colibrì engine.

## Known Omarchy fit

| Resource | Known inventory | What must be observed |
|---|---|---|
| GPU | RTX 3060 LHR, 12 GB VRAM | Free VRAM, driver, compute capability, GPU contention, display allocation |
| GPU architecture | RTX 3060 is Ampere / sm_86 | Confirm with nvidia-smi and Colibrì hardware detector |
| System RAM | 32 GB installed | Available RAM at idle and under baseline load; swap; memory pressure |
| CPU | UNKNOWN | Exact model, cores/threads, ISA, sustained clocks |
| Storage | NVMe is expected in the workstation | Device model, filesystem, free space, temperature, health, random-read bandwidth |
| CUDA | UNKNOWN | Driver, toolkit, nvcc, CUDA version and sm_86 build compatibility |
| Vulkan | UNKNOWN | Vulkan ICD, device, driver and runtime feature support |
| Current inference | llama.cpp + Qwen3-Coder-30B-A3B Q4_K_M (recorded in research repo) | Re-observe exact process, config, endpoint and accepted baseline |

## Official checkpoint memory and GPU implications

Colibrì's DeepSeek V4 guide documents:

- 43 layers, hidden size 4096, 256 routed experts per sparse layer, top-k 6.
- Dense weights approximately 6.27 GiB and a resident BF16 output head approximately 1.06 GiB.
- Routed expert weights approximately 137 GiB on disk, about 12.6 MB per expert.
- Expert caching is sized from available RAM; --ram is a planner budget, not an OS-enforced limit.
- The official checkpoint loads directly from sharded safetensors without conversion.

Colibrì's CUDA guide estimates approximately 6.3 GB of dense/attention mirrors, about 0.5 GB of attention/KV/work buffers, and a transient prefill expert bank of about 3.2 GiB for 256 experts. Its 10–12 GB card table says 12 GB can run the full prefill bank but is tight; the minimum decode mirror count is small. Disabling the prefill bank leaves more room for decode mirrors, at the cost of CPU-side prefill expert work.

**Implication:** 12 GB VRAM is not an automatic blocker, but it is not generous. Actual free VRAM and the model planner decide. Do not hardcode the 16 GB or 24 GB card settings from upstream examples.

## CUDA compatibility

Colibrì documents the DeepSeek V4 CUDA path for compute capability 6.0+ and CUDA 12.0+. The generic Linux CUDA build supports RTX 30-series cards; for this RTX 3060 target, use a generic sm_86-capable build if the installed toolkit supports it. The DeepGEMM sm_120a build is for RTX 50-series / Blackwell and is **not** the RTX 3060 path.

The setup guide says CUDA toolkits below 12.8 use NO_TC=1 for the DeepSeek V4 build. Do not guess the toolkit or build flags: observe nvcc and follow the exact current upstream guide.

## RAM implications

Colibrì's catalogue lists the official 284B DeepSeek V4 Flash at 16 GB minimum / 32 GB recommended. The known 32 GB system is therefore at the recommended boundary, not comfortably above it. Available memory after the desktop, current inference service and OS reserve may be materially lower.

The 85 GiB-class GGUF still streams experts from storage and does not become a 90 GB in-memory model. Its Vulkan host pool and the engine's own RAM cache share system memory; their budgets must be planned together. The upstream 41 GiB host-pool experiment used a 62 GB RAM machine and must not be copied to this 32 GB host.

Do not force --ram 32 on a 32 GB physical machine. Let the planner observe available memory first, then set an explicit budget only after a safe headroom calculation.

## Storage budget

Planning reserves below are operational buffers, not upstream requirements:

| Artifact | Listed size | Suggested free space before download |
|---|---:|---:|
| Official safetensors | ~167 GB | At least 200 GB |
| Full-model GGUF UD-IQ2_XXS | ~90.9 GB listing | At least 115 GB |
| REAP 150B safetensors | ~85 GB | At least 110 GB |

The first test should use one fast NVMe. A second independent SSD and COLI_MODEL_MIRROR are optional later experiments; do not mirror the model until a single-drive baseline exists.

## Upstream benchmark references — not Omarchy results

| Candidate / path | Upstream machine | Reported result | How to interpret |
|---|---|---|---|
| Official 284B safetensors, CPU | Ryzen 7 5800X, 32 GB RAM | 0.93 decode tok/s | Reference only |
| Official 284B safetensors, CPU | Ryzen 9 5950X, 63 GB RAM | 1.24 decode tok/s | Different CPU and memory |
| Official 284B safetensors, CUDA | RTX 5080, 32 GB RAM, two NVMe | 1.5–1.6 decode tok/s | Not comparable to RTX 3060 |
| Full-model GGUF UD-IQ2_XXS, Vulkan | RTX PRO 4000 24 GB, 62 GB RAM, NVMe | 6.18–6.25 decode; 19.7–20.4 prompt tok/s | Upstream's tuned/warm measurement; not a 3060 prediction |
| REAP 150B, CUDA | RTX 3090, Ryzen 9 9950X3D, 62 GB RAM, NVMe | GPU-batched prefill 1.70–2.03× CPU union on tested prompts | Pruned checkpoint and different machine |

These results establish that Colibrì has run the model family. They do not establish fit, speed or correctness on the FR3K workstation.

## Fit decision rules

- **FIT:** model catalogue says it fits, planner has headroom, disk budget is satisfied, and no swap/OOM occurs in a short run.
- **TIGHT:** it fits only with constrained context, small cache, reduced GPU tier or low headroom. Do not promote without a soak.
- **BLOCKED:** unsupported backend, insufficient free disk/RAM, CUDA build incompatibility, repeated OOM, or unsafe thermal / storage behavior.
