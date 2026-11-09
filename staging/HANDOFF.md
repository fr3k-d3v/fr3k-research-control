# Handoff: research staging complete

## Status
Research staging artifacts written. All six files are substantive (not placeholders). No GPU work, no inference, no builds, no installations, no large downloads performed. GPU validation remains active and untouched.

## Artifacts produced
1. `/home/fr3k/Documents/FR3K-RESEARCH-STAGING-2026-11-09/STATE.md` — observed live state, frozen 13-batch inventory, ownership boundary, model change record
2. `/home/fr3k/Documents/FR3K-RESEARCH-STAGING-2026-11-09/candidates.json` — deduplicated candidate ledger with 6 entries, source paths, commits, evidence tiers, compatibility, negative results, next actions
3. `/home/fr3k/Documents/FR3K-RESEARCH-STAGING-2026-11-09/AUDIT-TRACES.md` — audit of moe-anywhere-routing-traces (dataset metadata, compatibility, negative results)
4. `/home/fr3k/Documents/FR3K-RESEARCH-STAGING-2026-11-09/AUDIT-HOTCACHE.md` — audit of moe-hotcache (3 commits, correctness, ROCm vs CUDA, negative results)
5. `/home/fr3k/Documents/FR3K-RESEARCH-STAGING-2026-11-09/AUDIT-PAGING.md` — audit of weight-streaming (2 commits, instrumentation, metric gaps)
6. `/home/fr3k/Documents/FR3K-RESEARCH-STAGING-2026-11-09/AUDIT-PREFETCH.md` — audit of 3 prefetch candidates (predictor, negative-result, paper)
7. `/home/fr3k/Documents/FR3K-RESEARCH-STAGING-2026-11-09/OFFLINE-EXPERIMENT-SPEC.md` — four-arm offline experiment specification

## Deduplication decisions
- neutronstar (Batch 11): shared SHA f53c4653cc96bae4974b34579043c123d61c7d92 across two repos — counted as ONE shared commit, not independent evidence. NOT in candidate ledger (not among 6 seed IDs).
- weight-streaming (Batch 10 + 11): same repo, two commits (8434ff9f and 6466811a) — counted once. Primary commit 6466811a used.
- moe-hotcache (Batch 10 + addendum): three commits (268a6128, 7e5ebf11, beda4496) — counted once. Primary commit 268a6128 used.
- All other batch candidates not in seed list — preserved in original batch files, not duplicated here.

## Ownership boundary
- Parent owns all artifacts.
- No replacement research worker dispatched (contamination risk from first worker using local model).
- Sequential text audits performed by parent only.
- No GPU jobs, endpoint probes, service restarts, commits or pushes authorized by this work increment.

## GPU validation status (updated 2026-11-09 17:26)
- Service: local-coder-full-validation.service — FAILED (exit code 1) at 17:26:47
- Status file: "state": "failed-baseline-restored", stages: tuning (exit 0, 3583s), final-route-audit (exit 1, 3.2s)
- Error: "final-route-audit failed (exit 1)"
- Baseline restored by safe-resume.sh
- This failure occurred during research staging; NOT caused by research work (no GPU or service interaction)
- Test owner must investigate final-route-audit failure independently
- No restart attempted (per ownership boundary)

## Model change (completed earlier)
- Default Hermes model: opencode-go / beam-free (was local-abliterated / local-coder-abliterated)
- Delegation model: opencode-go / beam-free
- All 18 auxiliary models: opencode-go / beam-free
- Research agents now use cloud model, not local GPU

## Next steps (for test owner)
1. Review all 7 artifacts for accuracy and completeness.
2. Verify candidates.json schema against plan validator.
3. Decide whether to fetch full diffs for moe-hotcache and weight-streaming commits.
4. After Codex full validation passes, consider executing offline experiment spec.
5. Update STATE.md research_activity_end timestamp when review is complete.