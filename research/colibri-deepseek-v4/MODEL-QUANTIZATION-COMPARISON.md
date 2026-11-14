# DeepSeek V4 Flash 0731 — GGUF quantization comparison

**Date:** 2026-11-14  
**Research ID:** FR3K-LLM-COLIBRI-DSV4-001  
**Purpose:** choose a full-284B GGUF artifact that can plausibly fit the Omarchy storage budget without silently substituting a pruned model.

## 1. Important distinction

All candidates below target the **full DeepSeek V4 Flash 0731 284B architecture** unless explicitly labelled REAP. GGUF variants retain the architecture/expert set but quantize weights. REAP 150B is a separate expert-pruned model and must not be described as the full 284B model.

The model card for AtomicChat describes the 284B model as 43 layers, 256 routed experts with six active, and one shared expert. Its AD quantization table reports expert-bit budgets and publisher-measured perplexity, mean KLD and next-token top-1 agreement against its AD-BF16 reference.

## 2. Candidate comparison

| Candidate | Approx. size | Architecture | Publisher-reported quality | Disk fit on 93.88 GB |
|---|---:|---|---|---|
| AtomicChat AD-IQ2_XS | 85.1 GB | Full 284B | PPL 5.4917; mean KLD 0.3947; top-1 79.240% | TIGHT; ~8.8 GB left |
| AtomicChat AD-IQ2_XXS | 78.5 GB | Full 284B | PPL 5.7878; mean KLD 0.4544; top-1 77.459% | TIGHT but more headroom; ~15.4 GB left |
| Unsloth UD-IQ1_S | 82.5 GB | Full 284B | AtomicChat's cross-publisher table: mean KLD 0.4863; top-1 75.162% | TIGHT; ~11.4 GB left |
| Unsloth UD-IQ2_XXS | 90.9 GB | Full 284B | No directly comparable figure used here | BLOCKED; ~3.0 GB left |
| Official safetensors | 166.9 GB | Full 284B, official FP4/FP8 | Fidelity reference | BLOCKED; Colibrì requires 172 GB free |
| REAP 150B | 84.7 GB | Expert-pruned 150B | No directly comparable metric used here | Catalogue says good, but ~9.2 GB left |

**Quality caveat:** the AtomicChat table is the publisher's own Wikitext-2 / fixed-harness evaluation. It is not an FR3K task benchmark and its absolute metrics should not be compared with unrelated model cards. The same table includes the Unsloth cross-publisher rows, making those particular within-table comparisons more useful than comparing unrelated benchmark posts.

## 3. Why AD-IQ2_XS is the current preferred candidate

- It keeps the full 284B architecture and all 256 routed experts.
- Its listed 85.1 GB size is below the currently observed 93.88 GB free on the model volume.
- It leaves approximately 8.8 GB, compared with only ~3.0 GB for Unsloth UD-IQ2_XXS.
- In AtomicChat's same-harness table, AD-IQ2_XS reports better top-1 agreement (79.240%) and lower KLD (0.3947) than AD-IQ2_XXS (77.459%, 0.4544) and the listed Unsloth UD-IQ1_S row (75.162%, 0.4863).
- The folder contains four GGUF shards; the first shard includes the updated chat template.

This remains a **candidate**, not an accepted artifact. Colibrì import compatibility must be demonstrated locally after download.

## 4. Colibrì compatibility evidence

Colibrì v2.1.0's GGUF guide states:

- `deepseek4` is a supported GGUF architecture and routes to the `deepseek_v4` engine.
- GGUF blocks are read as stored, without a second quantization.
- Supported GGUF types span IQ1_S through Q8_0 and MXFP4.
- `coli import --mode link` (the default) reads the GGUF in place and does not copy the model.
- `--mode copy` writes another model container and is not appropriate for this tight disk budget.

The AtomicChat model page labels the repository as GGUF / `deepseek_v4`, identifies the official DeepSeek V4 Flash base model and reports an MIT licence. This makes compatibility plausible; local import and planner output remain the proof gate.

## 5. Download manifest — AD-IQ2_XS

Repository: https://huggingface.co/AtomicChat/DeepSeek-V4-Flash-0731-GGUF  
Variant directory: `AD-IQ2_XS/`  
Variant folder revision shown by the model page: `8c7a581` (short commit; resolve full revision before download).

| Shard | Listed size |
|---|---:|
| `DeepSeek-V4-Flash-0731-AD-IQ2_XS-00001-of-00004.gguf` | 22.5 GB |
| `DeepSeek-V4-Flash-0731-AD-IQ2_XS-00002-of-00004.gguf` | 22.6 GB |
| `DeepSeek-V4-Flash-0731-AD-IQ2_XS-00003-of-00004.gguf` | 24.2 GB |
| `DeepSeek-V4-Flash-0731-AD-IQ2_XS-00004-of-00004.gguf` | 15.9 GB |

The model page reports the folder total as 85.1 GB; individual displayed shard sizes are rounded. Capture exact byte sizes and SHA-256 hashes from the downloaded files.

## 6. Decision

**Preferred full-model experiment:** AtomicChat AD-IQ2_XS, subject to an immediate free-space recheck and explicit approval of the 85.1 GB download.

Do not download UD-IQ2_XXS or the official safetensors to the current volume. Keep REAP 150B as a separate fallback if the full-model GGUF fails quality, import or performance gates.


## Exact revision and shard bytes

The Hugging Face API resolved the model repository to revision `17eb08debccb00a8d4dba11642ed1997f85c9d1c`, last modified 2026-10-28. Pinned HTTP HEAD requests returned the exact shard sizes and upstream ETag/Xet metadata in [DOWNLOAD-MANIFEST.md](DOWNLOAD-MANIFEST.md).

Exact total: 85,141,812,960 bytes (85.1418 GB decimal / 79.2945 GiB). The preflight volume has 93,879,758,848 bytes free, leaving 8,737,945,888 bytes (8.74 GB) after the model. This is a tight fit, not permission to download.
