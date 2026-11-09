# RTX 3060 experimental program

## Current measured candidate (not yet accepted)
Qwen3-Coder-30B-A3B-Instruct abliterated Q4_K_M, llama.cpp, 65,536 context, six CPU threads, 2,048 MiB host cache, 5,632 MiB MoE cache, Q4_0 K/V. Historical conservative preset uses Q8 K/V and three CPU threads. Keep Hermes `opencode-go/beam-free` untouched. Record model and engine SHA before new measurements.

## Sequence
1. Finish resumed local acceptance: route audit, service checks, cache isolation, Pi and Hermes agent acceptance, benchmark, 64K, failure/idle and soak. Reboot and tailnet checks remain separate.
2. Freeze accepted configuration and raw measurements. If acceptance fails, restore previous baseline; do not label candidate winner.
3. Four-way experiment: A accepted baseline/cache off/fixed placement; B expert caching only; C adaptive VRAM allocation only; D both. Where a capability is unsupported, mark BLOCKED instead of inventing a result.
4. Run 4K, 16K and 64K tasks: realistic file read/edit/test and multi-turn tools, exact-source retrieval, reasoning and malformed-tool resilience. Verify actual prompt token counts and no truncation.
5. Randomize trial order; multiple cold and warm runs. Track median and p95 end-to-end task latency, TTFT, prefill tok/s, decode tok/s, successful tool calls, peak VRAM, available RAM, paging/SSD I/O, GPU clocks, temperature, power, expert hit rate, OOM and recovery.
6. Audit RustingStrata, Betelgeuse, moe-hotcache, weight-streaming and tinygiant in disposable worktrees/containers before isolated comparison. No production substitution without matching correctness and repeatable gain.
7. Publish sanitized benchmark results including failures and null results. Keep upstream performance claims separate from Omarchy observations.

## Promotion rule
No correctness regression, stable 64K behavior, reproducible end-to-end task benefit, acceptable memory headroom and clean recovery. Fast token output alone is insufficient.
