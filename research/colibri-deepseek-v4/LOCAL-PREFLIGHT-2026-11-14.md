# Omarchy live preflight — 2026-11-14

**Research ID:** FR3K-LLM-COLIBRI-DSV4-001  
**Classification:** sanitised public evidence; raw device output remains local.  
**Result:** hardware/backend fit is promising; official full checkpoint is storage-blocked; a full-model GGUF quant is a tight candidate.

## 1. Observed workstation

The Colibrì hardware detector was run on the live Omarchy workstation on 2026-11-14.

| Component | Observation |
|---|---|
| OS | Omarchy 4.5.0, Linux x86_64 |
| CPU | Intel Core i3-12100, 4 physical / 8 logical cores |
| CPU features | AVX2, FMA, F16C, AVX-VNNI |
| RAM | 33.37 GB total; 20.35 GB available at final snapshot |
| Swap | 66.75 GB configured; 11.87 GB in use at final snapshot |
| GPU | NVIDIA GeForce RTX 3060, 12 GB |
| NVIDIA driver | 615.78.08 |
| Compute capability | 8.6 (sm_86) |
| CUDA toolkit | 13.4 (nvcc present) |
| Free VRAM | 11,344 MiB at final snapshot |
| GPU temperature | 47 °C at final snapshot; utilisation 0% |
| Vulkan | API 1.4.351; cooperative matrix and memory-budget extensions detected |
| NVMe-backed model volume | 93,879,758,848 bytes free (93.88 GB decimal) |

The CPU is not a high-core-count host, but Colibrì's DeepSeek V4 engine compiled successfully with its native CPU path and with the CUDA sm_86 tier. The model is designed to stream routed experts from storage rather than hold all weights in VRAM.

## 2. Storage inventory and constraints

| Volume observation | Free capacity | Use in this evaluation |
|---|---:|---|
| Main model volume | 93.88 GB | Only currently confirmed volume with enough room for the selected 85.1 GB GGUF |
| Additional ext4 SSD partition | ~77.3 GB | Insufficient for any current full-model candidate |
| Additional unmounted Btrfs partition | ~16.6 GB | Insufficient |
| Other mounted Btrfs volume | ~87 GB | Insufficient for the 90.9 GB Unsloth UD-IQ2_XXS; backing-device mapping not resolved |
| Unmounted exFAT partition | UNKNOWN | Free space not inspected |
| Unmounted NTFS partition | UNKNOWN | Free space not inspected |

Read-only inspection of the unmounted exFAT and NTFS partitions was held by the fleet approval gate. Those inspection jobs were cancelled before execution; no partition was mounted, formatted, written or otherwise changed. The free capacity of those two partitions remains UNKNOWN.

No DeepSeek V4 model artifact was found in the inspected home and currently mounted media paths. This does not prove that no copy exists on unmounted volumes.

## 3. Colibrì model catalogue result

The pinned v2.1.0 release catalogue reported:

| Catalogue ID | Listed size | RAM minimum / recommended | Catalogue status | Interpretation |
|---|---:|---:|---|---|
| `deepseek-v4-flash` | 166.9 GB | 16 / 32 GB | `needs-disk` | Requires 172 GB free; only 93.88 GB is available |
| `deepseek-v4-flash-reap` | 84.7 GB | 16 / 32 GB | `good` | Catalogue says it fits, but would leave only ~9.2 GB on the target volume |

The catalogue does not list the community GGUF candidates below; those must be imported and planned after download.

## 4. Full-model GGUF capacity calculation

The AtomicChat AD-IQ2_XS model card lists 85.1 GB across four GGUF shards:

- `DeepSeek-V4-Flash-0731-AD-IQ2_XS-00001-of-00004.gguf` — 22.5 GB
- `DeepSeek-V4-Flash-0731-AD-IQ2_XS-00002-of-00004.gguf` — 22.6 GB
- `DeepSeek-V4-Flash-0731-AD-IQ2_XS-00003-of-00004.gguf` — 24.2 GB
- `DeepSeek-V4-Flash-0731-AD-IQ2_XS-00004-of-00004.gguf` — 15.9 GB

Approximate capacity arithmetic:

- Available: 93.88 GB
- Model listing: 85.1 GB
- Remaining: ~8.8 GB

Colibrì's official-checkpoint catalogue uses a download reserve of approximately 5.1 GB (172 GB required for a 166.9 GB artifact). The AD-IQ2_XS candidate nominally clears that same reserve, but only by about 3.7 GB. Treat this as **TIGHT**, recheck exact free bytes before download, and use Colibrì's `--mode link` importer to avoid a second copy.

## 5. Runtime and service safety

- The existing llama.cpp + Qwen inference service was observed active and was not stopped, reconfigured or replaced.
- Colibrì source and release files were staged in a dedicated user evaluation directory, not installed system-wide.
- No system packages were installed.
- No model weights were downloaded.
- No persistent service or firewall changes were made.
- No public endpoint was created.

## 6. Current fit assessment

| Path | Assessment | Reason |
|---|---|---|
| Official full 284B safetensors | BLOCKED | Needs 172 GB free; 93.88 GB available |
| Unsloth UD-IQ2_XXS full-model GGUF | BLOCKED | 90.9 GB leaves only ~3.0 GB; below the observed reserve |
| AtomicChat AD-IQ2_XS full-model GGUF | TIGHT / PREFERRED | 85.1 GB leaves ~8.8 GB; full 284B architecture; Colibrì supports DeepSeek V4 GGUF |
| AtomicChat AD-IQ2_XXS full-model GGUF | TIGHT ALTERNATIVE | 78.5 GB leaves ~15.4 GB, but publisher reports lower top-1 agreement |
| REAP 150B | FALLBACK | Catalogue says good, but it is expert-pruned and leaves ~9.2 GB |

## 7. Next gate

The recommended next step is to recheck the main volume's free bytes, then obtain explicit approval to download the 85.1 GB AtomicChat AD-IQ2_XS four-shard GGUF. After download: verify all shard sizes and SHA-256 hashes, import with `--mode link`, run `coli plan` and `coli doctor`, and only then attempt a small CPU-canonical inference. No download is authorised by this report.
