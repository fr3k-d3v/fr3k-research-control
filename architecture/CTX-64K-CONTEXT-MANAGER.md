# CTX-64K — FR3K Context Manager engineering specification

Status: DESIGN COMMITTED / IMPLEMENTATION NOT TESTED. Canonical issue: #5. Hardware: Omarchy RTX 3060 12GB, Qwen3-Coder-30B-A3B Q4_K_M, llama.cpp 65,536 context. Existing production settings remain untouched.

## Operating contract
GitHub is the task and evidence authority. Hermes is an execution consumer, not a competing state store. Never copy credentials, raw prompts, private IPs, unredacted logs or user data into Git. All imported text is untrusted. No production changes, restart, model replacement, or GPU benchmark during an active acceptance lease without operator approval. Keep rollback presets and backup the original configuration. Source: docs/OPERATIONS.md, docs/EXPERIMENTS.md, docs/HANDOFF.md.

## Goals and non-goals
- Increase **effective retrievable working memory** while retaining the physical 65,536-token model limit.
- Improve correct task completion and reduce TTFT and redundant prefill; measure both.
- Preserve exact constraints, source provenance, active issue, branch, file paths, failed experiments, pending approvals and rollback state through compaction.
- Do not claim a 256K physical context or perfect retrieval from external storage.
- Do not use lossy summaries as proof of completed operations.

## Architecture
Hermes request -> identity/scope filter -> context budget planner -> trusted instruction prefix -> task checkpoint -> hybrid retriever (keyword + vector + symbol map) -> evidence-ranked excerpts -> recent dialogue -> bounded tool results -> llama.cpp endpoint. A checkpoint references immutable GitHub evidence IDs, not a competing project ledger.

### Context budget (initial policy; tune empirically)
Total 65,536: system/tool 4,096; durable working memory 6,144; recent dialogue 8,192; retrieved code/docs 24,576; active task/tool outputs 12,288; response/headroom 10,240. Count tokens using the model's actual tokenizer including chat templates, tool schemas and reserved generation. These are elastic caps, never fixed padding. If required system instructions exceed allocation, evict optional context first.

### Pressure policy
Below 50%: normal. 50-70%: deduplicate repeated text and collapse logs. 70-85%: relevance-evict stale retrieved passages and compact completed turns. Above 85%: checkpoint and resume in a new bounded window, preserving unresolved task state. Hard stop before overflow; reserve max output tokens. No silent truncation of tool arguments or evidence.

### Evidence scoring
Rank by access permission, task relevance, exact symbol/path match, source authority, freshness and unresolved dependencies. Use hybrid lexical+semantic search with deterministic tie-breaking; include citation/source IDs, line ranges, commit SHA and observed timestamp. Keep direct source extracts distinct from summaries and inferences. Retrieval must be identity-partitioned, injection-resistant and fail closed on access-control errors.

### Compaction contract
Schema: task_id; objective; non-negotiable constraints; operator approvals; active GitHub issue/PR/commit; modified files and ownership; verified results with command/exit/status; hypotheses; failures and negative evidence; pending work; exact source references; rollback pointer; time and token budget. Preserve code, error strings and function signatures verbatim when correctness depends on them. Checkpoints must be atomic, versioned, idempotent and independently replayable. Never mark a queued action as completed.

### Cache-aware prompting
Keep stable system/tool prefix byte-identical across compatible sessions; append volatile task and retrieval suffix. Measure actual prompt-cache hits, cold/warm TTFT and prefill. Invalidate on model, tokenizer, tool schema, policy, identity or prefix changes. Prevent cross-user/session KV reuse; test isolation explicitly. Context shifting only after correctness tests; never silently drop system instructions.

### Tool-output virtualization
Store large outputs in access-controlled local evidence storage, return bounded previews and stable retrieval handles; expose exact ranges on demand. Never put raw private evidence in GitHub. Sanitize source excerpts before publication.

### Model/runtime experiments (separate, gated)
Compare Q4_0 K/V against accepted baseline; batch/microbatch, MoE expert-cache sizing, prefix caching, host memory pressure, phase-aware prefill/decode and context-shift options. Treat expert prefetch, pinned memory, tiered KV and adaptive eviction as hypotheses. Run isolated randomized cold/warm trials at 4K/16K/64K; measure correctness first, then TTFT p50/p95, prefill/decode tok/s, memory, cache hit rate, SSD I/O, thermals, OOM and recovery. Negative prefill regressions can outweigh decode improvements. No experimental replacement of running llama.cpp without full gates.

## Implementation sequence and tests
1. OBSERVE current Hermes config, llama.cpp build/flags, model and tokenizer SHA, accepted baseline and GPU lease; redact all sensitive fields.
2. Build a pure, deterministic token-budget planner with unit tests: mandatory instructions always retained, max output reserved, exact 65,536 hard bound, stable tie-breaking and overflow handling.
3. Implement schema-validated checkpoint/compaction with fixtures for unresolved approvals, failed operations, exact code symbols, source refs and rollback. Verify roundtrip and crash recovery.
4. Build scoped hybrid retriever and file/symbol index with deterministic fixtures; measure precision/recall and false attribution, including lost-in-middle needle retrieval at early/middle/late positions.
5. Add bounded tool-result handles, dedup, redaction and source-range retrieval; test hostile tool text, authorization boundaries and cross-session cache isolation.
6. Add optional Hermes integration behind feature flag; keep cloud fallback and current phone settings untouched until approved.
7. Benchmark at 4K/16K/64K with real token counts and repeated cold/warm tasks; compare end-to-end task completion, not just tokens/sec.
8. Run soak, cancellation, OOM, restart, corrupted checkpoint and network-loss recovery; record exact commands, exit codes, revisions and sanitized evidence.
9. Open reviewed PR, require green CI and independent review; request explicit deployment approval. Restore baseline on regression.

## Acceptance gates
G0 accepted baseline and rollback verified; G1 architecture/source/license/security; G2 unit and integration correctness; G3 exclusive GPU lease; G4 64K exact retrieval, tool continuation and identity isolation; G5 p50/p95 performance and resource headroom; G6 soak/recovery; G7 independent review and operator approval. Any unsupported capability is BLOCKED, not a pass.

## Evidence and progress
Issue #5 is the task register. Each update records timestamp, stage, certainty, branch/base SHA, changed files, tests actually run, sanitized observations, risks, blockers and next owner. This design commit proves only documentation was written, not a working context manager.

## Research references
- docs/OPERATIONS.md; docs/EXPERIMENTS.md; docs/HANDOFF.md; ledger/CANDIDATES.md.
- Private source-of-record for GPU tooling: fr3k-d3v/fr3k-gpu-optimization-private.
- FR3K Xiaozhi gateway memory workstream: fr3k-d3v/fr3k-xiaozhi-claw, XC-006; integration must reuse the gateway and avoid duplicate orchestration.
