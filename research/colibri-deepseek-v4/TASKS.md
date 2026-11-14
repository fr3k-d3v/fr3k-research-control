# Execution task register

**Research ID:** FR3K-LLM-COLIBRI-DSV4-001  
**Updated:** 2026-11-14. Terminal states are immutable; repeated attempts get new run IDs.

| ID | Task | Depends on | Status | Exit evidence |
|---|---|---|---|---|
| DSV4-00 | Freeze upstream Colibrì and model revisions | — | COMPLETE | v2.1.0 source commit, release checksum and model-page snapshots recorded |
| DSV4-01 | Read-only target hardware/storage preflight | DSV4-00 | PARTIAL | Non-identifying hardware profile and capacity candidate observed; full I/O benchmark remains unknown |
| DSV4-02 | Run Colibrì model catalogue / fit planner | DSV4-01 | COMPLETE | Official model needs-disk; REAP catalogue good; outputs recorded |
| DSV4-03 | Select full-model artifact | DSV4-02 | SUPERSEDED | Ordinary AtomicChat candidate replaced by abliterated Huihui Q2 |
| DSV4-04 | Obtain instruction to acquire an abliterated model | DSV4-03 | COMPLETE | User explicitly instructed acquisition; Huihui Q2 selected and pinned |
| DSV4-05 | Create isolated Colibrì checkout and build engines | DSV4-00 | PARTIAL | Source/release pinned; CPU and CUDA sm_86 builds pass; generic Vulkan device init pass |
| DSV4-06 | Download and checksum selected abliterated artifact | DSV4-04, DSV4-18, DSV4-19 | BLOCKED — STORAGE / HOST | Exact artifact, SHA-256 manifest and guarded script committed; local filesystem write gate remains |
| DSV4-07 | GGUF import, model doctor and placement plan | DSV4-05, DSV4-06 | NOT STARTED | coli import --mode link, coli plan, coli doctor |
| DSV4-08 | CPU-canonical inference baseline | DSV4-07 | NOT STARTED | Correctness prompt suite and raw metrics |
| DSV4-09 | CUDA sm_86 model inference experiment | DSV4-08 | PARTIAL — BUILD ONLY | CUDA engine build and runtime smoke pass; model correctness not run |
| DSV4-10 | Vulkan GGUF expert-tier model experiment | DSV4-08 | PARTIAL — DEVICE ONLY | Generic Vulkan device init pass; DeepSeek V4 GGUF inference not run |
| DSV4-11 | Context and memory sweep | DSV4-09 or DSV4-10 | NOT STARTED | 4K–64K stability and resource table |
| DSV4-12 | Tool-call / agent workload suite | DSV4-08 | NOT STARTED | Schema-valid multi-step test results |
| DSV4-13 | Tuning sweep | DSV4-11, DSV4-12 | NOT STARTED | One-variable-at-a-time comparison |
| DSV4-14 | Failure, restart and soak tests | DSV4-13 | NOT STARTED | Recovery and stability tests |
| DSV4-15 | FR3K provider adapter | DSV4-12, DSV4-14 | NOT STARTED | End-to-end integration tests |
| DSV4-16 | Promotion decision and public report | DSV4-15 | NOT STARTED | ACCEPTED / REJECTED / BLOCKED with evidence |
| DSV4-17 | Select larger local storage capacity | DSV4-01 | COMPLETE | Capacity candidate identified; device identifiers retained privately |
| DSV4-18 | Repair dirty local NTFS volume | DSV4-17 | BLOCKED — OPERATOR ACTION | Windows chkdsk required; no forced mount or write attempted |
| DSV4-19 | Reconnect target host and re-observe storage | DSV4-18 | BLOCKED — HOST UNAVAILABLE | Fleet could not reach the target host at last check |
| DSV4-20 | Select and pin Huihui DeepSeek V4 Flash 0731 Abliterated Q2 | DSV4-02 | COMPLETE | Full HF revision, exact 86,720,111,488-byte size, SHA-256 and caveats recorded |
| DSV4-21 | Download and verify abliterated Q2 GGUF | DSV4-18, DSV4-19, DSV4-20 | BLOCKED — STORAGE / HOST | Guarded downloader committed; no bytes downloaded |
| DSV4-22 | Import Huihui Q2 GGUF into Colibrì v2.1.0 | DSV4-21 | NOT STARTED | GGUF import, plan and doctor evidence |
| DSV4-23 | Run correctness smoke test and memory-fit evaluation | DSV4-22 | NOT STARTED | CPU-canonical and CUDA tests; record memory, OOM and latency |
| DSV4-24 | Compare ablation/refusal behaviour and capability retention | DSV4-23 | NOT STARTED | Controlled benign/refusal/coding/tool-call suite |

## Dispatch rules

- Read-only preflight and source builds may proceed before model acquisition.
- DSV4-21 must not start until DSV4-18 and DSV4-19 pass.
- Use the guarded downloader; do not bypass the filesystem write gate.
- Only one GPU-intensive experiment may hold the GPU lease at a time.
- Do not dispatch model inference before CPU-canonical correctness passes.
- Keep the existing inference baseline untouched.
- Terminal task states are immutable. Repeated attempts use a new run ID and link to prior evidence.

## Download preparation

- Huihui DeepSeek V4 Flash 0731 Abliterated Q2 is selected and pinned.
- Exact size and SHA-256 are recorded in ABLITERATED-DOWNLOAD-MANIFEST-2026-11-14.md.
- A guarded resumable downloader is committed at scripts/download-huihui-abliterated-q2.sh. It requires --confirm-download, validates locally supplied mount configuration and capacity, then verifies size and SHA-256.
- The script has NOT been executed. Local filesystem repair and target-host availability remain blockers.
