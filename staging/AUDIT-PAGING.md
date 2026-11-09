# Audit: weight-streaming (paging telemetry)

## Candidate identity
- ID: `weight-streaming`
- Repo: https://github.com/i-mrDed/weight-streaming
- Commits audited:
  1. `6466811a086a740ed65d040d7962d3eb37359d73` (instrumentation, per addendum)
  2. `8434ff9f3bbb22126f40a27d96920b48f1b794b7` (Batch 11 listing)
- Source: IMPLEMENTATION-EVIDENCE-ADDENDUM-2026-11-09.md, SCOUT-2026-11-09-BATCH-10.md, SCOUT-2026-11-09-BATCH-11.md

## Commit 1: 6466811a086a740ed65d040d7962d3eb37359d73
- Files: tests/test_server_config_and_chat.py, weight_stream/backends/llama_cpp.py, weight_stream/server/model_manager.py
- Evidence type: code changes (instrumentation)
- Implementation: public stream_prompt wrapper, generation paging telemetry, periodic page-cache sampling, server path integration
- Author report: 94 passed / 7 skipped tests; Llama-3.2-1B cold paging 17.7 MB/token total, 2.1 MB/token disk
- Audit status: files identified but diffs NOT inspected. Metric definitions, measurement source, sampling frequency, overhead UNKNOWN.

## Commit 2: 8434ff9f3bbb22126f40a27d96920b48f1b794b7
- Source: Batch 11 listing
- Audit status: commit SHA observed; functionality and RTX3060 benefit UNKNOWN. May be earlier or different revision of same repo.

## What is verified from source text
- Repo provides weight streaming ideas with CPU/GPU transfer and NVMe behavior focus
- Batch 10 lists it as a candidate for disk paging, MoE cache, and negative-memory-pressure leads
- Batch 11 confirms commit 8434ff9f3bbb22126f40a27d96920b48f1b794b7 as an observed SHA
- Addendum confirms commit 6466811a086a740ed65d040d7962d3eb37359d73 with code changes in 3 files
- This is instrumentation, NOT proof of reduced I/O or higher throughput

## What is NOT verified
- Exact metric definitions (what counts as "cold paging", "total", "disk")
- Measurement source (OS page cache counters, /proc, custom sampling)
- Sampling frequency and overhead
- Whether 17.7 MB/token is for Llama-3.2-1B only or generalizable
- Whether page-cache sampling affects inference latency
- Repo licence, maintainer status, last update
- Ancestry relationship between the two commits

## Compatibility assessment
- Model: Llama-3.2-1B (not Qwen3-Coder-30B-A3B) — different size, architecture, expert count
- Integration: assumes this project's own server wrapper (not llama.cpp direct)
- Value for FR3K: HIGH for observability/baseline measurement methodology, but acceleration unknown

## Negative results / caveats
- Instrumentation only, not acceleration proof
- 94 passed / 7 skipped tests (author-reported, not independently verified)
- Cold paging 17.7 MB/token total, 2.1 MB/token disk (Llama-3.2-1B only)
- Batch 11 warns: "check whether they are present in Batch 10 before calling them new" — dedupe required

## Next action
- Fetch exact diffs for both commits via GitHub API (read-only)
- Record metric definitions, measurement source, sampling frequency, overhead
- Compare the two commits for ancestry and functional differences
- Update candidates.json with verified metadata
- Do NOT compile or run on GPU

## Evidence tier
- Current: author-claim (instrumentation code exists per addendum, but diffs not independently inspected)
- Required for promotion: independent reproduction of telemetry accuracy on FR3K hardware with exact commit, model, quant, context.