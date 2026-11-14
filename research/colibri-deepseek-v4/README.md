# Colibrì + DeepSeek V4 Flash — FR3K evaluation

**Research ID:** FR3K-LLM-COLIBRI-DSV4-001  
**Opened:** 2026-11-14  
**Status:** PREFLIGHT COMPLETE · ENGINE BUILDS PASS · ABLITERATED MODEL SELECTED · DOWNLOAD BLOCKED BY LOCAL STORAGE / HOST GATE · NO MODEL INFERENCE  
**Primary target:** DeepSeek V4 Flash 0731 (284B total parameters)  
**Runtime:** [JustVugg/colibri](https://github.com/JustVugg/colibri)

## Current decision

The active target is **Huihui DeepSeek V4 Flash 0731 Abliterated GGUF — Q2**, pinned to revision `a8dfba9c1e43bdf324ee2c7787ed01c70975ffb4`. Exact file size: 86,720,111,488 bytes. SHA-256: `73d17d12b2988b31df519ae381096bcaa737361664d76ce2c88a9ed6b68ff756`. This supersedes the ordinary AtomicChat AD-IQ2_XS candidate.

The publisher describes this as a proof-of-concept abliteration and says not all expert modules were ablated. Q2 may still refuse some requests; Q4 variants use stronger ablation intensity but are much larger. This is a research target, not an inference acceptance.

Private preflight identified a larger local NTFS data volume with sufficient capacity. Its filesystem is marked dirty and read-write access was refused. Device identifiers, volume labels, UUIDs, mount paths and exact capacity figures are intentionally excluded from this public repository. No model bytes have been downloaded.

See [model selection](ABLITERATED-MODEL-SELECTION-2026-11-14.md), [download manifest](ABLITERATED-DOWNLOAD-MANIFEST-2026-11-14.md), and [storage gate assessment](STORAGE-DESTINATION-ASSESSMENT-2026-11-14.md).

## Runtime progress

- Private preflight used a consumer NVIDIA workstation profile with 12 GB VRAM and 32 GB system RAM; exact machine identifiers are withheld.
- Colibrì v2.1.0 CPU and CUDA sm_86 engine builds passed.
- CUDA runtime vector-add smoke passed.
- Generic Vulkan device initialization passed; this is not DeepSeek V4 inference.
- No model weights downloaded; no actual DeepSeek inference performed.
- Existing inference baseline remains untouched.

## Candidate hierarchy

| Priority | Candidate | What it is | Current decision |
|---|---|---|---|
| P0 — selected | Huihui DeepSeek V4 Flash 0731 Abliterated Q2 GGUF | Full 284B architecture; 86.72 GB | SELECTED; download blocked by local storage write gate |
| P1 — stronger ablation | Huihui DeepSeek V4 Flash 0731 Abliterated Q4 MXFP4 | 155.98 GB; stronger publisher-reported ablation | Not selected for first run |
| P2 — Q2_K variant | Huihui DeepSeek V4 Flash 0731 Abliterated Q2_K | 97.59 GB | Not selected for first run |
| Historical baseline | AtomicChat AD-IQ2_XS GGUF | Ordinary, non-abliterated full 284B checkpoint | Superseded |
| Fidelity reference | Official DeepSeek V4 Flash 0731 | Full 284B safetensors | Not selected |

## Operating rules

- Preserve the existing local inference baseline.
- No large download until the destination is writable and rechecked.
- Start with CPU-canonical correctness; tune one variable at a time.
- Keep inference servers on loopback with authentication.
- FR3K remains the authority for tool execution, job state and approvals.
- A running server or benchmark number is not acceptance.
- Raw logs, private paths, filesystem identifiers, tokens and local prompts stay local.

## Pinned abliterated model acquisition

- [Model selection](ABLITERATED-MODEL-SELECTION-2026-11-14.md)
- [Exact manifest](ABLITERATED-DOWNLOAD-MANIFEST-2026-11-14.md)
- [Guarded resumable downloader](scripts/download-huihui-abliterated-q2.sh)
- Download script has not been executed; filesystem repair and target-host availability remain blockers.
