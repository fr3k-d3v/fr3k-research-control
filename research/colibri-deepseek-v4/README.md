# Colibrì + DeepSeek V4 Flash — FR3K evaluation

**Research ID:** FR3K-LLM-COLIBRI-DSV4-001  
**Opened:** 2026-11-14  
**Status:** RESEARCH PLAN RECORDED · PREFLIGHT NOT RUN · NO MODEL DOWNLOADED · NOT ACCEPTED  
**Primary target:** official DeepSeek V4 Flash 0731 (284B total parameters)  
**Runtime candidate:** [JustVugg/colibri](https://github.com/JustVugg/colibri)

> Connect machines. Measure reality. Delegate work. Verify results.

## Executive decision

Evaluate Colibrì as an optional FR3K local-inference provider, with **DeepSeek V4 Flash 0731 as the preferred model family**. Do not substitute DeepSeek V4.1 Flash, and do not silently replace the full 284B model with the expert-pruned REAP 150B variant.

The most practical first attempt may be the full 284B architecture in the **UD-IQ2_XXS GGUF** quant (approximately 85 GiB / 90.9 decimal GB in upstream listings), because it reduces disk demand while retaining the full model's expert set. The preferred fidelity reference remains the official safetensors checkpoint (approximately 167 GB). The REAP 150B checkpoint is a fallback only if the full model cannot be run usefully on the available machine.

The known Omarchy target is an RTX 3060 12 GB and 32 GB system RAM. This is **plausible but not yet verified**. Colibrì's own catalogue lists 16 GB minimum / 32 GB recommended RAM for full DeepSeek V4 Flash and 12 GB VRAM as a tight configuration for the full CUDA prefill path. Actual free RAM, GPU headroom, CUDA toolkit, Vulkan driver, NVMe capacity and random-read performance are UNKNOWN until observed on the machine.

## Start here

1. [Implementation plan](IMPLEMENTATION-PLAN.md) — phases, dependencies and exit gates.
2. [Model and hardware fit](MODEL-AND-HARDWARE-FIT.md) — full model, GGUF and REAP variants; 3060 compatibility.
3. [Benchmark and acceptance protocol](BENCHMARK-AND-ACCEPTANCE.md) — reproducible measurements and correctness gates.
4. [FR3K integration architecture](FR3K-INTEGRATION.md) — provider boundary, tool authority and failure handling.
5. [Runbook](RUNBOOK.md) — safe preflight and later installation procedure.
6. [Execution tasks](TASKS.md) — ordered work queue.
7. [Evidence register](EVIDENCE.md) — source claims versus local observations.
8. [Decision log](DECISIONS.md) — explicit choices and unresolved questions.

## Candidate hierarchy

| Priority | Candidate | What it is | Decision |
|---|---|---|---|
| P0 — preferred | Official deepseek-ai/DeepSeek-V4-Flash-0731 | Full 284B checkpoint; FP4 routed experts, FP8 dense; ~167 GB | Test if disk and RAM preflight pass |
| P0 — practical full-model route | Unsloth UD-IQ2_XXS GGUF | Full 284B architecture, quantized weights; ~85 GiB / ~90.9 GB listing | First lower-disk option; measure quality and speed |
| P1 — fallback | puwaer/DeepSeek-V4-Flash-0731-reap-150b | Expert-pruned 150B variant; 132 rather than 256 routed experts; ~85 GB | Only if full model is blocked or too slow |
| Excluded from this target | DeepSeek V4.1 Flash | Separate 552B / ~510 GB model and engine path | Do not confuse with V4 Flash |

## Current evidence state

- **VERIFIED FACT — upstream source:** Colibrì main was observed at commit 0a5504a1dc64f86fcd0fe7db298b0448c730e7e6 on 2026-11-14; the dev branch was observed at fd7ed68afa1f88706eae08ef172a5bc02c42bd77. The latest published release observed was v2.1.0.
- **VERIFIED FACT — upstream documentation:** Colibrì documents a native DeepSeek V4 engine, official safetensors loading without conversion, optional CUDA acceleration, GGUF import, a Vulkan expert tier, and OpenAI/Anthropic tool-call translation.
- **CLAIM — upstream benchmark:** the 85 GiB-class full-model GGUF UD-IQ2_XXS was measured on an RTX PRO 4000 24 GB / 62 GB RAM system at approximately 6.18–6.25 decode tok/s and 19.7–20.4 prompt tok/s after the documented tier improvements. This is not an Omarchy result.
- **OBSERVATION:** the known Omarchy target inventory is RTX 3060 12 GB / 32 GB RAM. It must be re-observed before any benchmark.
- **UNKNOWN:** exact CPU, free RAM, free NVMe capacity, NVMe random-read bandwidth, CUDA toolkit/driver compatibility, Vulkan device and current GPU contention.
- **NOT DONE:** no Colibrì installation, model download, service change, GPU tuning or local benchmark has been performed by this research entry.

## Non-negotiable operating rules

- Preserve the current llama.cpp + Qwen3-Coder baseline; do not replace it during evaluation.
- Preflight before download. Show model size, target path, available capacity and hardware fit before authorising a large download.
- No system package installation or model download without explicit approval.
- Start with stock defaults and CPU-canonical correctness. Tune only one variable at a time.
- Keep the server bound to loopback with API authentication. Do not expose an unauthenticated inference endpoint to the LAN or tailnet.
- FR3K remains the sole authority for tool execution, job state, physical actions and approvals.
- A running server is not acceptance. A benchmark number without correctness evidence is not an accepted result.
- Store raw logs locally; publish only sanitised measurements. Never commit tokens, private paths, prompts containing personal data, machine identifiers or private infrastructure details.

## Primary upstream references

- [Colibrì repository](https://github.com/JustVugg/colibri)
- [Pinned Colibrì main snapshot](https://github.com/JustVugg/colibri/tree/0a5504a1dc64f86fcd0fe7db298b0448c730e7e6)
- [DeepSeek V4 engine guide](https://github.com/JustVugg/colibri/blob/0a5504a1dc64f86fcd0fe7db298b0448c730e7e6/docs/deepseek-v4.md)
- [Colibrì Vulkan guide](https://github.com/JustVugg/colibri/blob/0a5504a1dc64f86fcd0fe7db298b0448c730e7e6/docs/vulkan.md)
- [Colibrì GGUF guide](https://github.com/JustVugg/colibri/blob/0a5504a1dc64f86fcd0fe7db298b0448c730e7e6/docs/gguf.md)
- [Colibrì API guide](https://github.com/JustVugg/colibri/blob/0a5504a1dc64f86fcd0fe7db298b0448c730e7e6/docs/api.md)
- [Official DeepSeek V4 Flash 0731 checkpoint](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731)
- [Unsloth DeepSeek V4 Flash GGUF variants](https://huggingface.co/unsloth/DeepSeek-V4-Flash-0731-GGUF)
- [REAP 150B fallback checkpoint](https://huggingface.co/puwaer/DeepSeek-V4-Flash-0731-reap-150b)
