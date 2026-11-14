# Model and hardware fit

**Assessment date:** 2026-11-14  
**Target:** Omarchy Linux, Intel i3-12100, RTX 3060 12 GB, 32 GB RAM.  
**Fit status:** CUDA BUILD PASS · VULKAN DEVICE INIT PASS · FULL MODEL NOT YET RUN.

## Hardware observed

| Resource | Live observation | Interpretation |
|---|---|---|
| CPU | Intel i3-12100, 4C/8T, AVX2/FMA/F16C/AVX-VNNI | Moderate CPU expert-streaming host |
| RAM | 33.37 GB total; 20.35 GB available at final snapshot | Meets catalogue's 32 GB recommended boundary by total capacity; headroom must be monitored |
| Swap | 66.75 GB configured; 11.87 GB used | Existing memory pressure; no new swap tuning performed |
| GPU | NVIDIA RTX 3060, 12 GB | Ampere, compute capability 8.6 |
| NVIDIA driver | 615.78.08 | Observed on target |
| CUDA | Toolkit 13.4; sm_86 engine build succeeded | CUDA build path is compatible at compile time |
| Free VRAM | 11,344 MiB | Good idle headroom; actual model allocation still unknown |
| Vulkan | API 1.4.351; cooperative matrix and memory budget detected | Generic Vulkan device initialization passed |
| Storage | 93.88 GB free on primary model volume | Full model quant fit is tight |

See [live preflight report](LOCAL-PREFLIGHT-2026-11-14.md) for sanitized measurements.

## Model candidates

| Artifact | Size | Architecture / precision | Current assessment |
|---|---:|---|---|
| Official `deepseek-ai/DeepSeek-V4-Flash-0731` | 166.9 GB | Full 284B; FP4 routed experts, FP8 dense | BLOCKED: catalogue requires 172 GB free |
| AtomicChat `AD-IQ2_XS` GGUF | 85.1 GB | Full 284B architecture, 2.25 expert bits | PREFERRED full-model test; ~8.8 GB free after download |
| AtomicChat `AD-IQ2_XXS` GGUF | 78.5 GB | Full 284B architecture, 2.06 expert bits | Smaller, lower publisher-reported fidelity |
| Unsloth `UD-IQ1_S` GGUF | 82.5 GB | Full 284B architecture | Lower publisher-reported fidelity than AtomicChat AD-IQ2_XS in the same comparison table |
| Unsloth `UD-IQ2_XXS` GGUF | 90.9 GB | Full 284B architecture | BLOCKED by insufficient disk reserve |
| `puwaer/DeepSeek-V4-Flash-0731-reap-150b` | 84.7 GB | 150B expert-pruned; 132 instead of 256 routed experts | Separate fallback; not the full model |

See [quantization comparison](MODEL-QUANTIZATION-COMPARISON.md) for the publisher metrics and four-shard manifest.

## RAM and VRAM implications

Colibrì's catalogue lists 16 GB minimum / 32 GB recommended RAM for the official 284B model. The workstation has 33.37 GB total and 20.35 GB available at the final observation. This meets the catalogue's total-RAM recommendation but does not provide large free-RAM headroom. Swap usage is already non-zero and must be monitored during model loading.

Colibrì's DeepSeek V4 CUDA guide describes approximately 6.3 GB of dense/attention mirrors, about 0.5 GB of work buffers and a transient prefill expert bank of about 3.2 GiB for 256 experts. A 12 GB GPU is a tight tier. The engine must use its runtime planner and observed free VRAM; do not hardcode 16 GB / 24 GB card settings.

The CUDA sm_86 engine compiled successfully and a standalone CUDA runtime smoke test passed. This does not prove the full model will fit or run without OOM.

## Storage implications

The official checkpoint catalogue requires 172 GB free for a 166.9 GB download. The current model volume has 93.88 GB free.

AtomicChat AD-IQ2_XS is listed at 85.1 GB and has four shards. It leaves approximately 8.8 GB. Colibrì's GGUF importer defaults to `--mode link`, which reads the files in place and avoids a second copy. This is a tight but plausible path. Recheck exact bytes before download and do not run another download concurrently.

The other unmounted exFAT and NTFS volumes remain uninspected; do not assume they are available model destinations.

## CUDA compatibility

The pinned v2.1.0 guide documents the generic Linux CUDA tier for sm_80+ and a specific sm_86 build option. The workstation has CUDA 13.4 and compute capability 8.6. The following build passed:

~~~bash
CUDA_HOME=/opt/cuda make -f Makefile.deepseek-v4 deepseek-v4 CUDA=1 CUDA_ARCH=sm_86
~~~

Do not use the sm_120a DeepGEMM target on an RTX 3060.

## Vulkan compatibility

Colibrì's hardware detector found the RTX 3060 through Vulkan API 1.4.351 with cooperative-matrix support. The release binary's generic Vulkan probe printed the RTX 3060 as ready and activated the expert tier. The probe then exited because its intentionally minimal GLM config omitted `n_group=1`. This proves device initialization only; DeepSeek V4-specific Vulkan inference is not yet verified.

## Fit decision rules

- **FIT:** model imported, planner has safe RAM/VRAM/disk headroom, short correctness run passes and no swap storm/OOM occurs.
- **TIGHT:** planner accepts only constrained context/cache/backend settings or leaves little storage/memory reserve; do not promote without a soak.
- **BLOCKED:** insufficient disk/RAM, unsupported artifact/backend, repeated OOM, failed correctness or unsafe resource pressure.
