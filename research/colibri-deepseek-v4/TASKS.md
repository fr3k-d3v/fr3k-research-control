# Execution task register

**Research ID:** FR3K-LLM-COLIBRI-DSV4-001  
**Updated:** 2026-11-14. Terminal states are immutable; repeated attempts get new run IDs.

| ID | Task | Depends on | Status | Exit evidence |
|---|---|---|---|---|
| DSV4-00 | Freeze upstream Colibrì and model revisions | — | COMPLETE | v2.1.0 source commit, release checksum and model-page snapshots recorded |
| DSV4-01 | Read-only Omarchy hardware preflight | DSV4-00 | PARTIAL | CPU/RAM/GPU/CUDA/Vulkan and primary disk observed; unmounted storage and I/O benchmark remain unknown |
| DSV4-02 | Run Colibrì model catalogue / fit planner | DSV4-01 | COMPLETE | Official model `needs-disk`; REAP catalogue `good`; outputs recorded |
| DSV4-03 | Select full-model artifact and verify disk budget | DSV4-02 | PARTIAL | AtomicChat AD-IQ2_XS preferred; 85.1 GB vs 93.88 GB free; tight fit requires final recheck |
| DSV4-04 | Obtain explicit approval for 85.1 GB model download | DSV4-03 | BLOCKED — APPROVAL | User approval for exact AtomicChat AD-IQ2_XS artifact |
| DSV4-05 | Create isolated Colibrì checkout and build engines | DSV4-00 | PARTIAL | Source/release pinned; CPU and CUDA sm_86 builds pass; generic Vulkan device init pass |
| DSV4-06 | Download and checksum selected artifact | DSV4-04 | BLOCKED — APPROVAL | Four shards, exact byte sizes and SHA-256 manifest |
| DSV4-07 | GGUF import, model doctor and placement plan | DSV4-05, DSV4-06 | NOT STARTED | `coli import --mode link`, `coli plan`, `coli doctor` |
| DSV4-08 | CPU-canonical inference baseline | DSV4-07 | NOT STARTED | Correctness prompt suite and raw metrics |
| DSV4-09 | CUDA sm_86 model inference experiment | DSV4-08 | PARTIAL — BUILD ONLY | CUDA engine build and CUDA runtime smoke pass; model correctness not run |
| DSV4-10 | Vulkan GGUF expert-tier model experiment | DSV4-08 | PARTIAL — DEVICE ONLY | Generic Vulkan device init pass; DeepSeek V4 GGUF inference not run |
| DSV4-11 | Context and memory sweep | DSV4-09 or DSV4-10 | NOT STARTED | 4K–64K stability and resource table |
| DSV4-12 | Tool-call / agent workload suite | DSV4-08 | NOT STARTED | Schema-valid multi-step test results |
| DSV4-13 | Tuning sweep | DSV4-11, DSV4-12 | NOT STARTED | One-variable-at-a-time comparison |
| DSV4-14 | Failure, restart and soak tests | DSV4-13 | NOT STARTED | Recovery and stability evidence |
| DSV4-15 | FR3K provider adapter | DSV4-12, DSV4-14 | NOT STARTED | End-to-end integration tests |
| DSV4-16 | Promotion decision and public report | DSV4-15 | NOT STARTED | ACCEPTED / REJECTED / BLOCKED with evidence |

## Dispatch rules

- DSV4-01 and DSV4-02 are read-only and may run before model download approval.
- Source checkout, compilation and smoke tests may proceed independently of model download approval.
- DSV4-06 must not start before DSV4-04 is explicitly approved.
- Only one GPU-intensive experiment may hold the GPU lease at a time.
- Do not dispatch DSV4-09/10 model inference before DSV4-08 CPU-canonical correctness passes.
- Keep the existing llama.cpp + Qwen baseline untouched.
- Terminal task states are immutable. Repeated attempts use a new run ID and link to prior evidence.
