# Audit: moe-hotcache

## Candidate identity
- ID: `moe-hotcache`
- Repo: https://github.com/ap03906101/moe-hotcache
- Commits audited:
  1. `268a6128f4abe3daeed165fffb096e95a474f137` (initial implementation)
  2. `7e5ebf119c2ab98f0a7c9ceb03ac3ade046f61d9` (correctness fix)
  3. `beda4496714f03e74bded372402cba5224e29baf` (external developer report)
- Source: IMPLEMENTATION-EVIDENCE-ADDENDUM-2026-11-09.md, SCOUT-2026-11-09-BATCH-10.md

## Commit 1: 268a6128f4abe3daeed165fffb096e95a474f137
- Files: ggml/src/ggml-cuda/expert-pin.cu, expert-pin.cuh, mmvq.cu, ggml-cuda.cu, common/arg.cpp, ggml-cpu.c
- Evidence type: actual code-file change (not merely README)
- Implementation: per-expert pointer table, pinned host memory, dynamic frequency counter, side-stream promotions/demotions, per-tensor cache budget
- Author claim (2x RDNA4 16GB ROCm): Qwen3.8 FN 131B-A6B Q3 decode 11.9 -> 19.89 tok/s; OLMoE 6.4 -> 15-16.8 tok/s
- Negative: large-batch prefill through DMA path routed to CPU
- Audit status: code files exist (per addendum), but exact diff, function signatures, allocation ownership, synchronization, and CPU fallback logic NOT inspected (no network access to fetch full diff). UNKNOWN.

## Commit 2: 7e5ebf119c2ab98f0a7c9ceb03ac3ade046f61d9
- Files: ggml/src/ggml-backend.cpp, src/llama-model-loader.cpp
- Evidence type: correctness fix
- Fix: batch scheduling for MUL_MAT_ID, forces real VRAM copies for offloaded host weights to avoid wrong outputs and HSA Q8_0 memory fault
- Supports partial pinning with mmap/file-backed layers
- Author report: partial-pin FN-131B 20 layers correct Thai/EN, zero swap, warm prefill 156-276 tok/s, decode 13.0-13.4; earlier unverified numbers retracted
- Audit status: code files identified but diff NOT inspected. Correctness claims require independent verification on CUDA.

## Commit 3: beda4496714f03e74bded372402cba5224e29baf
- Evidence type: external developer report (not commit-linked code change)
- Report: 17 -> 2.6 prefill tok/s with 12GB pinned + 45GB host file pages / NVMe rereads
- Root-cause attribution: author hypothesis (pinning reduces OS page-cache headroom, increasing model-file I/O)
- Audit status: external report only. Exact repo, hardware, commit, measurement protocol UNKNOWN. Causality unproven.

## Compatibility assessment
- Hardware: AMD ROCm (RDNA4) vs FR3K NVIDIA CUDA (RTX 3060) — different backend, different memory architecture
- Model: Qwen3.8 FN 131B-A6B Q3 vs Qwen3-Coder-30B-A3B Q4_K_M — different size, quant, architecture
- Ancestry: claimed written from scratch; requires verification against upstream llama.cpp
- CUDA portability: UNKNOWN (ROCm-specific code may not compile/run on CUDA)

## Negative results / caveats
- Large-batch prefill through DMA path (author-reported limitation)
- External developer reports severe prefill regression (17 -> 2.6 tok/s) with pinned host memory
- Earlier unverified numbers retracted by author
- Hardware and model differ from Omarchy
- Strong correctness gate candidate (commit 2 requires independent verification)

## Next action
- Fetch exact diffs for all three commits via GitHub API (read-only)
- Verify ancestry against upstream llama.cpp
- Check for CUDA-specific code paths vs ROCm-only
- Record allocation ownership, synchronization, CPU fallback logic
- Update candidates.json with verified metadata
- Do NOT compile or run on GPU

## Evidence tier
- Current: author-claim (code exists per addendum, but diffs not independently inspected)
- Required for promotion: CUDA compile + correctness check + FR3K hardware benchmark with exact commit, model, quant, context, and task correctness.