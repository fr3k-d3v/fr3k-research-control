# Candidate ledger — 2026-11-09

All entries below are **unverified leads**, not demonstrated Omarchy performance gains.

| Candidate | Source | Evidence and compatibility | Next gate |
|---|---|---|---|
| RustingStrata | https://github.com/RustingStudio/RustingStrata | Author-reported RTX3060 benefits; model/engine compatibility unverified | Source, license, CUDA and benchmark audit |
| Betelgeuse | https://github.com/Betelgeuse-AI/Betelgeuse | Experimental expert caching; reported broken paths | Correctness and crash audit |
| tinygiant | https://github.com/jerryjokesalot/tinygiant | Prototype SSD expert streaming | Disk I/O and correctness instrumentation |
| moe-hotcache | https://github.com/ap03906101/moe-hotcache | AMD/other-model results, not NVIDIA/Qwen3-Coder proof; reported prefill regression with pinned memory | Audit scheduling, DMA, CUDA portability and negative findings |
| weight-streaming | https://github.com/i-mrDed/weight-streaming | Instrumentation using different model, not speedup evidence | Validate metric definitions and overhead |
| routing traces | https://huggingface.co/datasets/carlosfelipe/moe-anywhere-routing-traces | Different GPU and model | Metadata/license audit; simulation only |
| RTX3060 reference benchmarks | https://github.com/harshithmohan/local-llm-benchmarks | Comparison reference, not FR3K result | Reproduce same model/quant |
| RTX3060 configurations | https://github.com/Ajay9o9/runs-on-a-3060 | Configuration examples | Compatibility review |

Source snapshots and negative findings must be updated by canonical URL + upstream commit, with immutable observations. Do not silently overwrite old entries.
