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
| SRC-01 | VERIFIED FACT | [Colibrì main](https://github.com/JustVugg/colibri/tree/0a5504a1dc64f86fcd0fe7db298b0448c730e7e6) | main HEAD 0a5504a1dc64f86fcd0fe7db298b0448c730e7e6, observed 2026-11-14 | Includes DeepSeek V4 engine and documentation |
| SRC-02 | VERIFIED FACT | [Colibrì dev](https://github.com/JustVugg/colibri/tree/fd7ed68afa1f88706eae08ef172a5bc02c42bd77) | dev HEAD fd7ed68afa1f88706eae08ef172a5bc02c42bd77, observed 2026-11-14 | Development snapshot; not the stable release |
| SRC-03 | VERIFIED FACT | [Colibrì v2.1.0](https://github.com/JustVugg/colibri/releases/tag/v2.1.0) | Latest release observed 2026-11-14 | Published release tag |
| SRC-04 | VERIFIED FACT | [DeepSeek V4 engine guide](https://github.com/JustVugg/colibri/blob/0a5504a1dc64f86fcd0fe7db298b0448c730e7e6/docs/deepseek-v4.md) | Pinned main snapshot | Official safetensors, model geometry, CUDA path and memory plan |
| SRC-05 | VERIFIED FACT | [Colibrì Vulkan guide](https://github.com/JustVugg/colibri/blob/0a5504a1dc64f86fcd0fe7db298b0448c730e7e6/docs/vulkan.md) | Pinned main snapshot | Vulkan expert-tier measurements for full-model GGUF |
| SRC-06 | VERIFIED FACT | [Colibrì GGUF guide](https://github.com/JustVugg/colibri/blob/0a5504a1dc64f86fcd0fe7db298b0448c730e7e6/docs/gguf.md) | Pinned main snapshot | deepseek4 GGUF architecture support and import behavior |
| SRC-07 | VERIFIED FACT | [Colibrì API guide](https://github.com/JustVugg/colibri/blob/0a5504a1dc64f86fcd0fe7db298b0448c730e7e6/docs/api.md) | Pinned main snapshot | Local API, bearer key, OpenAI/Anthropic tool calls |
| SRC-08 | VERIFIED FACT | [Official DeepSeek V4 Flash 0731](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731) | Observed 2026-11-14 | Official model card; MIT licence |
| SRC-09 | VERIFIED FACT | [Unsloth DeepSeek V4 Flash GGUF](https://huggingface.co/unsloth/DeepSeek-V4-Flash-0731-GGUF) | Observed 2026-11-14 | GGUF quant variants; model page reports MIT licence |
| SRC-10 | VERIFIED FACT | [REAP 150B checkpoint](https://huggingface.co/puwaer/DeepSeek-V4-Flash-0731-reap-150b) | Observed 2026-11-14 | Pruned 150B fallback; model page reports MIT licence |

## Upstream measurements (CLAIM, not FR3K observations)

- Colibrì's main README reports the official 284B safetensors model at approximately 167 GB and 16 GB minimum / 32 GB recommended RAM. It reports CPU measurements of 0.93 tok/s on a Ryzen 7 5800X with 32 GB and 1.24 tok/s on a Ryzen 9 5950X with 63 GB; a CUDA result of 1.5–1.6 tok/s used an RTX 5080, 32 GB RAM and two NVMe drives.
- Colibrì's Vulkan guide reports the full-model DeepSeek V4 Flash 0731 UD-IQ2_XXS GGUF at approximately 85 GB. On an RTX PRO 4000 24 GB with 62 GB RAM, it reports 6.18–6.25 decode tok/s and 19.7–20.4 prompt tok/s after the documented expert-tier changes. The same guide describes a 41 GiB host pool at 5.5–5.6 decode tok/s versus 5.9–6.2 with a 5 GiB pool and the engine's store intact.
- Hugging Face's Unsloth listing reports 90.9 GB for UD-IQ2_XXS; this likely reflects a GB/GiB or listing convention difference from Colibrì's rounded 85 GB. Resolve using the exact files manifest before download.

These measurements must not be copied into an FR3K benchmark table as if they were obtained on the Omarchy 3060.

## Local observations

| ID | Type | Date | Finding |
|---|---|---|---|
| LOC-00 | OBSERVATION (inventory memory; recheck required) | 2026-11-14 | Target recorded as Omarchy RTX 3060 12 GB / 32 GB RAM |
| LOC-01 | UNKNOWN | — | Current free RAM, free VRAM, CPU, CUDA, Vulkan, NVMe capacity and I/O |
| LOC-02 | UNKNOWN | — | Colibrì installed state on Omarchy |
| LOC-03 | UNKNOWN | — | Any DeepSeek V4 Flash artifact present locally |
| LOC-04 | UNKNOWN | — | Local model quality, speed, stability and FR3K integration |

## Local evidence policy

Raw command output, full logs, private model paths, .coli_usage, tokens and any private prompt material stay local. Public reports should include sanitised summaries, exact software/model hashes, non-sensitive configuration and reproducible commands. Every local result must link to a run ID from the benchmark template.
