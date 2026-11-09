# Offline Experiment Specification

## Purpose
Define a reproducible offline experiment that can validate expert-cache and prefetch hypotheses using the moe-anywhere routing traces (or equivalent) WITHOUT running the local model on GPU. This spec is text-only; no execution authorized until Codex full validation passes.

## Hypothesis
Workload-aware expert cache eviction and phase-dependent cache placement (prefill vs decode) can reduce expert-cache miss rate and improve effective throughput on MoE models, provided that:
1. Cache budget is adaptive (VRAM + resident RAM + page cache + locked pages + swap + disk I/O).
2. Prefetch is benchmarked by phase, I/O pressure, and context length.
3. Negative prefetch results (from mlx-nemo-offload) are treated as evidence that naive prefetch can regress.

## Four experiment arms
1. **Baseline**: No expert cache. Measure prefill/decode throughput, TTFT, memory, disk I/O.
2. **Cache only**: Expert cache with LRU eviction. No prefetch. Measure same metrics + cache hit rate, miss rate, eviction count.
3. **Adaptive only**: Adaptive VRAM/RAM/page-cache budget allocation. No expert cache. Measure memory pressure, page faults, swap usage.
4. **Combined**: Expert cache + adaptive budget + phase-dependent placement. Measure all metrics.

## Context lengths
- 4K, 16K, 64K (64K correctness and stability are hard gates)

## Required measurements (per arm, per context)
- Prefill throughput (tok/s)
- Decode throughput (tok/s)
- TTFT (ms)
- Task completion (coding correctness: pass/fail on fixed coding tasks)
- Memory: MemAvailable, Cached, Mlocked, Unevictable, SwapFree (MiB)
- Disk I/O: major faults, NVMe read bytes, IOPS
- Expert cache: hit rate, miss rate, eviction count, promotion/demotion count
- Crash/OOM/transfer stall events

## Inputs
- Routing traces from moe-anywhere-routing-traces (or equivalent workload traces)
- Fixed prompt set (coding tasks, not synthetic benchmarks)
- Cold and warm page-cache states (controlled)
- Model: Qwen3-Coder-30B-A3B Q4_K_M (FR3K's actual model, not trace model)

## Controls
- No GPU contention: run only when Codex full validation is complete and service is idle
- Control cold/warm page-cache state between runs
- Protect normal system operation (do not pin all weights blindly)
- Record all results including null and negative results
- 64K correctness and stability are hard gates (no promotion without passing)

## Evidence tiers
- Author claim: external report, not verified
- Independently reproduced: verified on different hardware
- FR3K hardware verified: measured on Omarchy RTX 3060 12GB with exact commit, model, quant, context, and task correctness

## Rollback
- All changes are text/config only. No code changes to local-coder.
- If any arm shows regression, revert to baseline and record negative result.
- No deployment without Codex acceptance.

## Gate
- Codex full validation must pass before any experiment execution.
- No new run until existing Codex sequence passes.
- Preserve every result, including failed and null results.