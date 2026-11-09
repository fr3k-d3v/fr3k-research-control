# Audit: prefetch candidates (predictor, negative-result, paper)

## Candidate 1: qwen35-expert-predictor

- ID: `qwen35-expert-predictor`
- URL: https://huggingface.co/RASMUS/qwen3.5-35b-a3b-fp8-expert-predictor
- Commit: UNKNOWN (no git SHA available; Hugging Face model repo)
- Source: SCOUT-2026-11-09-BATCH-13 (item 1)

### What is verified from source text
- Model card describes 34 small prediction heads, one per MoE layer L06-L39
- Predicts which of 256 experts will be used for token t+1
- Prefetch can stage absent experts ahead of next layer
- Author claims identical output in paired tests
- Model-specific: Qwen3.5-35B-A3B FP8

### What is NOT verified
- Model card full content, licence, training data, code availability: UNKNOWN
- Whether prediction heads are trainable/fine-tunable or fixed
- Whether "identical output" claim has independent verification
- Training data size, convergence, generalization
- Whether predictor adds latency overhead
- No 3060 result

### Compatibility assessment
- Model: Qwen3.5-35B-A3B FP8 vs FR3K Qwen3-Coder-30B-A3B Q4_K_M — different model, different quant, different architecture
- Not directly compatible. Design-only audit.
- Potential offline trace-based predictor research if traces are available

### Negative results / caveats
- Model-specific; not directly compatible with FR3K
- Author claims only; no independent verification
- No 3060 result

### Next action
- Inspect model card and small inference/training source if available via HF API
- Do not download weights
- Record training-data requirements, cache semantics, architecture mismatch
- Update candidates.json with verified metadata

### Evidence tier
- Current: author-claim
- Required for promotion: architecture compatibility analysis + independent output-correctness check on FR3K model

---

## Candidate 2: mlx-nemo-offload

- ID: `mlx-nemo-offload`
- URL: https://huggingface.co/Jakevin/NVIDIA-Nemotron-3.5-Super-120B-A12B-q3-mlx
- Commit: UNKNOWN (no git SHA available; Hugging Face model repo)
- Source: SCOUT-2026-11-09-BATCH-13 (item 2)

### What is verified from source text
- Model card includes `nemo_offload.py` runtime for Apple MLX
- LRU expert slots, `os.preadv` SSD reads
- Cache sizing based on free+purgeable+file-backed memory (0.8 multiplier)
- Swap-growth abort guard
- Author reports 2.24-2.47 tok/s decode with LRU
- Prefetch slower at 1.97-2.07 tok/s (negative result)
- 230-270 MB disk reads per generated token
- Short-prompt prefill 1.3-1.7 tok/s vs 2K-doc ~32 tok/s

### What is NOT verified
- Actual `nemo_offload.py` code/commit: not inspected
- Apple MLX memory accounting specifics: UNKNOWN
- Whether `os.preadv` path is portable to Linux/CUDA: UNKNOWN
- Cache sizing formula validation: UNKNOWN
- Swap-growth abort guard implementation: UNKNOWN
- No NVIDIA CUDA portability claim

### Compatibility assessment
- Platform: Apple MLX only. No NVIDIA CUDA portability claim.
- Model: 120B (not 30B) — different size
- Keep Apple memory-accounting assumptions separate from Linux/CUDA
- Value: methodology (negative prefetch result) is transferable; implementation is not

### Negative results / caveats
- Strong negative prefetch result: naive prefetch can regress (1.97-2.07 vs 2.24-2.47 tok/s)
- 230-270 MB disk reads per generated token (high I/O pressure)
- Short-prompt prefill much slower than long-doc prefill (1.3-1.7 vs ~32 tok/s)
- No NVIDIA CUDA portability

### Next action
- Locate actual nemo_offload.py revision via Hugging Face API
- Read RAM-budget/prefetch sections
- Record cache semantics, memory-accounting assumptions, negative prefetch result with original workload
- Update candidates.json with verified metadata
- Do NOT download weights or model files

### Evidence tier
- Current: author-claim (negative result reported by author, not independently verified)
- Required for promotion: independent reproduction of negative prefetch on FR3K hardware

---

## Candidate 3: prefetch-steered-routing (PSR)

- ID: `prefetch-steered-routing`
- URL: https://huggingface.co/papers?q=prefetching
- Commit: UNKNOWN (paper index search; no implementation commit)
- Source: SCOUT-2026-11-09-BATCH-13 (item 4)

### What is verified from source text
- Paper-index abstract describes deterministic logical cache steering routing
- Separates physical prefetch transfer timing from model semantics
- Important correctness caveat: timing-dependent cache-aware routing can alter model output

### What is NOT verified
- Full paper identity, authors, venue, year: UNKNOWN (only search URL provided)
- Implementation availability: UNKNOWN
- Reproducibility: UNKNOWN
- Whether "deterministic logical cache steering" is actually deterministic or approximate
- Whether output alteration is benign or correctness-breaking

### Compatibility assessment
- No implementation verified. Paper only.
- Correctness caveat is directly relevant to FR3K (output must not change)
- Need full paper before any assessment

### Negative results / caveats
- Timing-dependent cache-aware routing can alter model output (correctness risk)
- No implementation verified
- Paper identity unresolved

### Next action
- Find full paper and implementation via academic search
- Resolve reproducibility and exact commits
- Record whether output alteration is documented and acceptable
- Update candidates.json with verified metadata or mark as unresolvable

### Evidence tier
- Current: unverified-lead (abstract only from paper index)
- Required for promotion: full paper review + implementation audit + independent correctness check