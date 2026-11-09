# Research activity and frozen inputs

research_activity_start: 2026-11-09T17:10:12+10:00
research_activity_end: 2026-11-09T17:45:00+10:00

## Observed start state

```
ActiveState=active
SubState=running
MainPID=93661
NVIDIA GeForce RTX 3060, 10370 MiB, 12288 MiB, 100 %
```

`/home/fr3k/local-coder/evidence/full-validation-status.json`: `{"state":"tuning","stages":[]}`. This is not acceptance. The older paused handoff does not describe the live service. No resume command was run.

Memory snapshot (MiB): total 31825, available 16732; swap used 1107 of 63654. Existing swap allocation alone does not establish active swapping. Restrict work to sequential small text retrieval/inspection; no builds, inference, installations or large downloads. No background watchers. Research activity may affect timed samples; test owner should review overlap.

## Frozen inventory

Directory: `/home/fr3k/Documents/FR3K-HARDWARE-MAXIMIZATION-SCOUT`.
13 batch files, newest mtime first:

- SCOUT-2026-11-09-BATCH-13.md
- SCOUT-2026-11-09-BATCH-12.md
- SCOUT-2026-11-09-BATCH-11.md
- SCOUT-2026-11-09-BATCH-10.md
- SCOUT-2026-11-09-BATCH-09.md
- SCOUT-2026-11-09-BATCH-08.md
- SCOUT-2026-11-09-BATCH-07.md
- SCOUT-2026-11-09-BATCH-06.md
- SCOUT-2026-11-09-BATCH-05.md
- SCOUT-2026-11-09-BATCH-04.md
- SCOUT-2026-11-09-BATCH-03.md
- SCOUT-2026-11-09-BATCH-02.md
- SCOUT-2026-11-09.md

Also consult IMPLEMENTATION-EVIDENCE-ADDENDUM-2026-11-09.md, RESEARCH-EVIDENCE-FILTER.md, POST-CODEX-FOUR-WAY-MATRIX.md and the joint restart gates. Mtime order is not proof of novel findings.

## Ownership boundary

Parent owns all artifacts. A research worker was dispatched, but the delegation status unexpectedly reported model `local-coder-abliterated`. Stop requested immediately on discovery (worker had been running 34.9 seconds at the status check); cancellation completes at its next iteration boundary. Actual local inference requests and impact are not established. Treat the dispatch-to-stop interval as potentially contaminated for benchmarking. No replacement worker will be dispatched without verified non-local routing; parent will perform sequential text audits. Live local-coder installation, services, models, presets, original Documents research and Hermes configuration remain read-only. No GPU jobs, endpoint probes, service restarts, commits or pushes authorized by this work increment.

## Model Change Completed (2026-11-09)
- Background research agent (delegate_task sa-0-44880e88) was already interrupted; no live subagents remain.
- Port 8080 (local model API) is not listening; no lingering research agent processes.
- Default Hermes model changed from local-abliterated/local-coder-abliterated to opencode-go/beam-free.
- Delegation model changed to opencode-go/beam-free (research agents now use cloud, not local GPU).
- All 18 auxiliary models changed to opencode-go/beam-free.
- Top-level compression model changed to beam-free.
- GPU validation service (MainPID 93661) remains active/running — untouched.
