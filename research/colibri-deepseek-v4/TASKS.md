# Execution task register

**Research ID:** FR3K-LLM-COLIBRI-DSV4-001  
**All tasks initially NOT STARTED unless marked otherwise.**

| ID | Task | Depends on | Status | Exit evidence |
|---|---|---|---|---|
| DSV4-00 | Freeze upstream Colibrì and model revisions | — | PARTIAL | Pinned runtime/model hashes recorded |
| DSV4-01 | Read-only Omarchy hardware preflight | DSV4-00 | NOT STARTED | Sanitised hardware JSON and report |
| DSV4-02 | Run Colibrì model catalogue / fit planner | DSV4-01 | NOT STARTED | good/tight/needs-ram/needs-disk status per artifact |
| DSV4-03 | Select official safetensors vs full-model GGUF | DSV4-02 | BLOCKED ON PREFLIGHT | Signed-off artifact, size and disk budget |
| DSV4-04 | Obtain approval for model download | DSV4-03 | NOT STARTED | Explicit approval recorded |
| DSV4-05 | Create isolated Colibrì checkout and build CPU engine | DSV4-04 | NOT STARTED | Commit, build log, self-test |
| DSV4-06 | Download and checksum selected artifact | DSV4-04 | NOT STARTED | Complete file manifest and checksums |
| DSV4-07 | Model doctor and placement plan | DSV4-05, DSV4-06 | NOT STARTED | Planner output, RAM/VRAM/disk plan |
| DSV4-08 | CPU-canonical inference baseline | DSV4-07 | NOT STARTED | Correctness prompt suite and raw metrics |
| DSV4-09 | CUDA sm_86 experiment | DSV4-08 | NOT STARTED | Correctness evidence and performance |
| DSV4-10 | Vulkan GGUF expert-tier experiment | DSV4-08 | NOT STARTED | Correctness evidence and performance |
| DSV4-11 | Context and memory sweep | DSV4-09 or DSV4-10 | NOT STARTED | 4K–64K stability and resource table |
| DSV4-12 | Tool-call / agent workload suite | DSV4-08 | NOT STARTED | Schema-valid multi-step test results |
| DSV4-13 | Tuning sweep | DSV4-11, DSV4-12 | NOT STARTED | One-variable-at-a-time comparison |
| DSV4-14 | Failure, restart and soak tests | DSV4-13 | NOT STARTED | Recovery and stability evidence |
| DSV4-15 | FR3K provider adapter | DSV4-12, DSV4-14 | NOT STARTED | End-to-end integration tests |
| DSV4-16 | Promotion decision and public report | DSV4-15 | NOT STARTED | ACCEPTED / REJECTED / BLOCKED with evidence |

## Dispatch rules

- DSV4-01 and DSV4-02 are read-only and may run before model download approval.
- Only one GPU-intensive experiment may hold the GPU lease at a time.
- Source audits and documentation work may proceed on CPU while the GPU is reserved, provided they do not contend for model storage or system RAM.
- Do not dispatch DSV4-05 or DSV4-06 before DSV4-04.
- Do not dispatch DSV4-09/10 before the CPU-canonical baseline passes.
- Terminal task states are immutable. If a task must be repeated, create a new run ID and link it to the previous task rather than overwriting evidence.
