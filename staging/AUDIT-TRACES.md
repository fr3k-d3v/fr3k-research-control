# Audit: moe-anywhere-routing-traces

## Candidate identity
- ID: `moe-anywhere-routing-traces`
- URL: https://huggingface.co/datasets/carlosfelipe/moe-anywhere-routing-traces
- Dataset commit: 323f524347d1239825a03e267a2bcb1e026aa5d9
- Source batch: SCOUT-2026-11-09-BATCH-12 (item 1)

## What is verified from source text
- Dataset includes expert-routing traces captured on RTX 5050 8GB, i9-12900HK, 31GB RAM, Sage-A1.5 Q4_K_M, llama.cpp CUDA, CPU expert offload.
- Described capture setup is unusually useful for offline expert-cache/prefetch simulation and workload-aware eviction without running a model.
- Dataset commit 323f524347d1239825a03e267a2bcb1e026aa5d9 adds e3d-bench.tsv (+13 lines) and README (+2/-1).
- Verified metadata only, not proof of runtime speedup.

## What is NOT verified
- Full dataset schema, column definitions, file sizes, licence, maintainer status: UNKNOWN (not inspected; only batch summary available).
- Whether traces are replayable without the original model: UNKNOWN.
- Whether expert IDs, layer counts, or activation patterns transfer to Qwen3-Coder-30B-A3B: UNKNOWN (different model).
- Whether trace capture overhead affects timing data: UNKNOWN.
- Dataset completeness or selection bias: UNKNOWN.
- No independent reproduction of any claim.

## Compatibility assessment
- Hardware: RTX 5050 8GB vs FR3K RTX 3060 12GB — different VRAM, different PCIe generation (UNKNOWN), different CPU.
- Model: Sage-A1.5 Q4_K_M vs Qwen3-Coder-30B-A3B Q4_K_M — different architecture, different expert count, different layer count.
- Traces are model-specific. Cannot directly replay expert routing for Qwen3-Coder.
- Offline simulation value: HIGH for algorithm design (eviction policy, prefetch timing), but no performance claim transferable.

## Negative results / caveats
- Performance claims are author reports, not FR3K measurements.
- Model differs from FR3K. Source: web search 2026-11-09.
- Dataset commit adds e3d-bench.tsv (+13 lines) and README (+2/-1); verified metadata, not proof of runtime speedup.

## Next action
- Fetch dataset card metadata (licence, schema, file sizes) via Hugging Face API without downloading trace files.
- Record schema columns, row counts, file sizes in this audit.
- Update candidates.json entry with verified metadata.
- Do NOT download large trace files.
- Do NOT claim transferable speedup.

## Evidence tier
- Current: unverified-lead (metadata only)
- Required for promotion: independent reproduction on FR3K hardware with exact commit, model, quant, context, and correctness check.