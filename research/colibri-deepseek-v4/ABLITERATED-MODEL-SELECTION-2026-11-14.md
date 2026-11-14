# Abliterated model selection — 2026-11-14

**Research ID:** FR3K-LLM-COLIBRI-DSV4-001  
**Decision:** Huihui DeepSeek V4 Flash 0731 Abliterated GGUF — Q2.  
**Execution state:** SELECTED · DOWNLOAD BLOCKED — LOCAL STORAGE WRITE GATE / HOST AVAILABILITY · NO WEIGHTS DOWNLOADED

## Selected artifact

- Publisher: [huihui-ai](https://huggingface.co/huihui-ai)
- Repository: [Huihui-DeepSeek-V4-Flash-0731-abliterated-GGUF](https://huggingface.co/huihui-ai/Huihui-DeepSeek-V4-Flash-0731-abliterated-GGUF)
- Base checkpoint: `deepseek-ai/DeepSeek-V4-Flash-0731`
- Architecture: DeepSeek4 MoE, 284B total parameters
- License declared by model card: MIT
- Pinned revision: `a8dfba9c1e43bdf324ee2c7787ed01c70975ffb4`
- File: `DeepSeek-V4-Flash-Q2-0731.gguf`
- Exact size: 86,720,111,488 bytes (86.72 GB decimal; ~80.77 GiB)
- SHA-256: `73d17d12b2988b31df519ae381096bcaa737361664d76ce2c88a9ed6b68ff756`
- Hugging Face Xet object hash: `d5fecfc8e73fe95f9cb6dfa1b50f7346e79d61cf2c305099854ced4b5f0138ad`

The repository describes this as an abliteration proof-of-concept and says the expert modules were not all ablated. Its README says Q4 variants use stronger ablation intensity than Q2, so Q2 can retain some refusals. Do not describe it as guaranteed zero-refusal.

## Quantisation alternatives

| Variant | Exact bytes | SHA-256 | Decision |
|---|---:|---|---|
| Q2 | 86,720,111,488 | `73d17d12b2988b31df519ae381096bcaa737361664d76ce2c88a9ed6b68ff756` | SELECTED |
| Q2_K | 97,591,747,456 | `4a459b2ceb344fc2d651f328ec8d2fc29f1e14e252f97e501d32c68d5bc65d38` | Larger; multi-GPU ds4 example |
| Q4 MXFP4 | 155,976,458,848 | `897c9d82ec412e1d983dcda579c96bd256454414b5b80d2570452477abe7beed` | Stronger ablation; larger |
| Q4_K | 164,633,502,592 | `cef5fe745703f67c3cc799c312b597ced82a86cf10611dd7ec553ae27be1eacd` | Stronger ablation; largest |

Q2 is selected as the first acquisition to reduce storage and runtime pressure. Q4 is a separate future comparison, not an automatic upgrade.

## Colibrì compatibility and hardware limits

Colibrì's GGUF documentation lists the `deepseek4` architecture and supports in-place GGUF linking. Current upstream documentation describes DeepSeek V4 GGUF block handling, including IQ2_XXS and Q2_K types. This makes the Huihui Q2 file a reasonable compatibility candidate, but the exact artifact has not yet been imported or run in Colibrì.

Private preflight used a consumer NVIDIA workstation profile with 12 GB VRAM and 32 GB system RAM. Colibrì v2.1.0 CPU and CUDA sm_86 builds passed, but no actual model inference was performed. Upstream performance data on RTX PRO 4000 24 GB + 62 GB RAM is not a performance claim for this smaller profile or this abliterated artifact.

Require `coli plan` and `coli doctor` to pass before model load. Start with short context and low output limits; stop on memory pressure, OOM or unsafe disk paging.

## Download route

The guarded downloader:
- requires `--confirm-download`;
- requires local operator-supplied mount and filesystem UUID environment variables;
- verifies a read-write mount and configured filesystem;
- checks at least 92,000,000,000 free bytes;
- pins the full Hugging Face revision;
- resumes partial downloads;
- verifies exact size and SHA-256;
- does not import or launch the model.

Local mount configuration belongs in an untracked environment file or shell environment. Do not commit volume UUIDs, hostnames, device paths or private mount details. The generic default mount root is `/mnt/models`.

## Current blockers

1. Local NTFS volume requires a proper Windows filesystem check before writes.
2. Target workstation was unavailable through Fleet at last check.
3. Recheck all local drives and measure read performance before download/inference acceptance.
4. Exact Huihui GGUF import and runtime compatibility remain UNKNOWN.

## Sources

- Model card: https://huggingface.co/huihui-ai/Huihui-DeepSeek-V4-Flash-0731-abliterated-GGUF
- Pinned revision: https://huggingface.co/huihui-ai/Huihui-DeepSeek-V4-Flash-0731-abliterated-GGUF/tree/a8dfba9c1e43bdf324ee2c7787ed01c70975ffb4
- File metadata: https://huggingface.co/huihui-ai/Huihui-DeepSeek-V4-Flash-0731-abliterated-GGUF/blob/a8dfba9c1e43bdf324ee2c7787ed01c70975ffb4/DeepSeek-V4-Flash-Q2-0731.gguf
- Colibrì GGUF support: https://github.com/JustVugg/colibri/blob/main/docs/gguf.md
- Colibrì memory notes: https://github.com/JustVugg/colibri/blob/main/docs/vulkan.md
- DS4 model guidance: https://github.com/antirez/ds4/blob/main/docs/MODELS.md
