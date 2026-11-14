# Evidence register

**Updated:** 2026-11-14  
**Research ID:** FR3K-LLM-COLIBRI-DSV4-001

## Evidence taxonomy

- **CLAIM:** statement made by a project, model card or third party.
- **OBSERVATION:** directly observed state, with timestamp and source.
- **EVIDENCE:** raw log, command output, checksum, trace or reproducible artifact.
- **VERIFIED FACT:** supported by evidence with provenance and scope.
- **HYPOTHESIS:** proposed explanation or expected behavior, not yet tested.
- **SIMULATION:** synthetic or simulated result.
- **UNKNOWN:** not yet established.

## Source snapshots

| ID | Type | Source | Snapshot / date | Finding |
|---|---|---|---|---|
| SRC-01 | VERIFIED FACT | [Colibrì main](https://github.com/JustVugg/colibri/tree/0a5504a1dc64f86fcd0fe7db298b0448c730e7e6) | main HEAD 0a5504a1dc64f86fcd0fe7db298b0448c730e7e6 | DeepSeek V4 engine and docs |
| SRC-02 | VERIFIED FACT | [Colibrì dev](https://github.com/JustVugg/colibri/tree/fd7ed68afa1f88706eae08ef172a5bc02c42bd77) | dev HEAD fd7ed68afa1f88706eae08ef172a5bc02c42bd77 | Development snapshot |
| SRC-03 | VERIFIED FACT | [Colibrì v2.1.0](https://github.com/JustVugg/colibri/releases/tag/v2.1.0) | Release tag commit 704a3f68184b78367a04cb5526e428dc2f90f05b | Pinned runtime release |
| SRC-04 | VERIFIED FACT | [DeepSeek V4 engine guide](https://github.com/JustVugg/colibri/blob/704a3f68184b78367a04cb5526e428dc2f90f05b/docs/deepseek-v4.md) | v2.1.0 source | CPU/CUDA architecture, memory plan and build instructions |
| SRC-05 | VERIFIED FACT | [Colibrì Vulkan guide](https://github.com/JustVugg/colibri/blob/704a3f68184b78367a04cb5526e428dc2f90f05b/docs/vulkan.md) | v2.1.0 source | Vulkan device and expert-tier behavior |
| SRC-06 | VERIFIED FACT | [Colibrì GGUF guide](https://github.com/JustVugg/colibri/blob/704a3f68184b78367a04cb5526e428dc2f90f05b/docs/gguf.md) | v2.1.0 source | `deepseek4` GGUF support; IQ types; link import |
| SRC-07 | VERIFIED FACT | [Colibrì API guide](https://github.com/JustVugg/colibri/blob/704a3f68184b78367a04cb5526e428dc2f90f05b/docs/api.md) | v2.1.0 source | Local API, bearer key, OpenAI/Anthropic tool calls |
| SRC-08 | VERIFIED FACT | [Official DeepSeek V4 Flash 0731](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731) | Observed 2026-11-14 | Official model card; full 284B checkpoint |
| SRC-09 | VERIFIED FACT | [Unsloth DeepSeek V4 Flash GGUF](https://huggingface.co/unsloth/DeepSeek-V4-Flash-0731-GGUF) | Observed 2026-11-14 | GGUF quant variants; UD-IQ2_XXS listed 90.9 GB |
| SRC-10 | VERIFIED FACT | [REAP 150B checkpoint](https://huggingface.co/puwaer/DeepSeek-V4-Flash-0731-reap-150b) | Observed 2026-11-14 | Expert-pruned 150B fallback |
| SRC-11 | VERIFIED FACT | [AtomicChat model card](https://huggingface.co/AtomicChat/DeepSeek-V4-Flash-0731-GGUF) | Observed 2026-11-14 | Full 284B GGUF family; MIT licence; quantization quality table |
| SRC-12 | VERIFIED FACT | [AtomicChat AD-IQ2_XS file listing](https://huggingface.co/AtomicChat/DeepSeek-V4-Flash-0731-GGUF/tree/main/AD-IQ2_XS) | Folder commit shown as 8c7a581 | Four shards, 85.1 GB total listing |
| SRC-13 | VERIFIED FACT | [AtomicChat AD-IQ2_XXS file listing](https://huggingface.co/AtomicChat/DeepSeek-V4-Flash-0731-GGUF/tree/main/AD-IQ2_XXS) | Observed 2026-11-14 | Four shards, 78.5 GB total listing |

## Upstream measurements — CLAIM, not FR3K observations

- Colibrì's catalogue lists the official 284B checkpoint at 166.9 GB, 16 GB minimum / 32 GB recommended RAM, and 172 GB free storage required.
- Colibrì's catalogue lists REAP 150B at 84.7 GB, 16 GB minimum / 32 GB recommended RAM, status `good` on the observed host.
- AtomicChat's same-harness table reports AD-IQ2_XS at 85.1 GB, PPL 5.4917, mean KLD 0.3947 and top-1 match 79.240%; AD-IQ2_XXS at 78.5 GB, PPL 5.7878, mean KLD 0.4544 and top-1 match 77.459%. The same table lists Unsloth UD-IQ1_S at 82.5 GB, mean KLD 0.4863 and top-1 match 75.162%.
- These model-card metrics are publisher measurements against the publisher's reference and evaluation corpus. They are not FR3K task-quality measurements.
- Colibrì's Vulkan guide's published RTX PRO 4000 / 62 GB RAM measurements are not predictions for the Omarchy RTX 3060.

## Local observations — OBSERVATION / EVIDENCE

| ID | Type | Date | Finding |
|---|---|---|---|
| LOC-00 | OBSERVATION | 2026-11-14 | Target Omarchy workstation: Intel i3-12100, 4C/8T, RTX 3060 12 GB, 32 GB RAM |
| LOC-01 | OBSERVATION | 2026-11-14 | RAM total 33.37 GB; available 20.35 GB; swap 11.87 GB used |
| LOC-02 | OBSERVATION | 2026-11-14 | NVIDIA driver 615.78.08; CUDA 13.4; compute capability 8.6 |
| LOC-03 | OBSERVATION | 2026-11-14 | Free VRAM 11,344 MiB; GPU 47 °C, 0% utilisation at final snapshot |
| LOC-04 | OBSERVATION | 2026-11-14 | Vulkan API 1.4.351, cooperative matrix and memory budget detected |
| LOC-05 | OBSERVATION | 2026-11-14 | Primary model volume free bytes 93,879,758,848 (93.88 GB decimal) |
| LOC-06 | OBSERVATION | 2026-11-14 | Colibrì v2.1.0 release catalogue: official model needs-disk; REAP 150B status good |
| LOC-07 | EVIDENCE | 2026-11-14 | CPU DeepSeek V4 engine build exit 0; binary SHA-256 recorded in BUILD-AND-SMOKE-TESTS.md |
| LOC-08 | EVIDENCE | 2026-11-14 | CUDA sm_86 engine build exit 0 with CUDA 13.4; binary SHA-256 recorded |
| LOC-09 | EVIDENCE | 2026-11-14 | Standalone CUDA 4,096-element vector-add runtime smoke passed on RTX 3060 cc 8.6 |
| LOC-10 | EVIDENCE | 2026-11-14 | Generic Colibrì Vulkan device probe printed RTX 3060 ready and expert tier active; probe later exited 1 on deliberately incomplete GLM config |
| LOC-11 | EVIDENCE | 2026-11-14 | DeepSeek V4 expert-store registry unit test ended ALL OK |
| LOC-12 | UNKNOWN | — | DeepSeek V4 model weights not downloaded; no actual model inference or model quality/speed benchmark |
| LOC-13 | UNKNOWN | — | Free capacity on unmounted exFAT and NTFS partitions; storage random-read throughput |
| LOC-14 | OBSERVATION | 2026-11-14 | Existing llama.cpp + Qwen baseline remained active and untouched |

## Local evidence policy

Raw command output, full logs, private model paths, .coli_usage, tokens, serials, UUIDs and private prompt material stay local. Public reports include only sanitised summaries, exact software/model hashes, non-sensitive configuration and reproducible commands. Every local result must link to a run ID.


## Additional upstream artifact evidence — 2026-11-14

- **SRC-14 — VERIFIED FACT:** Hugging Face model API for AtomicChat resolved repository revision `17eb08debccb00a8d4dba11642ed1997f85c9d1c`, last modified 2026-10-28.
- **SRC-15 — EVIDENCE:** HTTP HEAD responses pinned to SRC-14 returned four exact `Content-Length` values totalling 85,141,812,960 bytes. Per-shard `x-linked-etag` and `x-xet-hash` values are recorded in DOWNLOAD-MANIFEST.md.
- **LOC-15 — EVIDENCE:** Current free space minus exact pinned shard total is 8,737,945,888 bytes. No model content was downloaded during these HEAD requests.
- **LOC-16 — OBSERVATION:** `curl` is available; `hf`, `huggingface-cli` and system Python `pip` are absent. A curl-only resumable downloader has been prepared but not executed.
