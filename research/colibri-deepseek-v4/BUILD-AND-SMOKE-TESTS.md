# Colibrì v2.1.0 — build and smoke-test evidence

**Research ID:** FR3K-LLM-COLIBRI-DSV4-001  
**Date:** 2026-11-14  
**Result:** source checkout, CPU build, CUDA sm_86 build and CUDA runtime smoke passed. Generic Vulkan device initialization passed. No DeepSeek V4 weights were loaded.

## 1. Source pin and release integrity

- Repository: https://github.com/JustVugg/colibri
- Release: `v2.1.0`
- Release source commit: `704a3f68184b78367a04cb5526e428dc2f90f05b`
- Main branch snapshot observed: `0a5504a1dc64f86fcd0fe7db298b0448c730e7e6`
- Dev branch snapshot observed: `fd7ed68afa1f88706eae08ef172a5bc02c42bd77`
- Linux x86_64 release archive SHA-256: `d54b4c57c12417fc9e784b649249ac1aa3480eec44ece2777d4cbc639a25e66a`
- Release CLI reports: `colibri 2.1.0`

The source checkout and extracted release were staged under a dedicated user evaluation directory. No system-wide install or package change occurred.

## 2. CPU engine build

Command, from Colibrì `c/`:

~~~bash
make -f Makefile.deepseek-v4 deepseek-v4
~~~

- Result: exit code 0
- Duration: approximately 48.2 seconds
- Binary usage banner: DeepSeek V4 engine recognised; command-line interface rendered.
- CPU binary SHA-256: `0869afe7ce1b71e274718b4c5bba75e68e11fbb6497e29ce82efc2ad114c7895`

This proves compilation and executable startup only. It does not prove model inference.

## 3. CUDA sm_86 engine build

Command:

~~~bash
CUDA_HOME=/opt/cuda make -f Makefile.deepseek-v4 deepseek-v4 CUDA=1 CUDA_ARCH=sm_86
~~~

- CUDA toolkit: 13.4
- Target architecture: sm_86 (RTX 3060)
- Result: exit code 0
- Duration: approximately 59.1 seconds
- Linked runtime libraries resolved: `libcudart.so.13`, `libcuda.so.1`, `libcublasLt.so.13`
- CUDA binary SHA-256: `5aac8b379efa7d9e93fa472fd78ebb7f1b46a7a22224606457d65ab610ed7458`

The build did not use the sm_120a DeepGEMM target; that target is not for the RTX 3060.

## 4. CUDA runtime smoke test

A temporary standalone CUDA program allocated device buffers, launched a 4,096-element vector-add kernel, synchronised, copied results back and verified every element.

Observed result:

~~~text
CUDA_OK device=NVIDIA GeForce RTX 3060 cc=8.6 vector_add=4096 elements
~~~

This verifies CUDA 13.4 runtime/device execution on the RTX 3060. It is not a DeepSeek V4 model correctness test.

## 5. Vulkan device initialization

The pinned v2.1.0 release binary was run with `COLI_VULKAN=1` and a temporary config-only probe directory. It printed:

~~~text
[VK] ready: NVIDIA GeForce RTX 3060
[VK] expert tier active
~~~

The probe then exited with code 1 because the intentionally minimal GLM test config omitted `n_group=1`. Therefore:

- VERIFIED: the release's generic Vulkan loader opens the RTX 3060 and activates the expert tier.
- NOT VERIFIED: DeepSeek V4-specific Vulkan inference or correctness.
- No weights were loaded and no model download was involved.

## 6. Unit test

Command:

~~~bash
make -f Makefile.deepseek-v4 deepseek-v4-test-registry
~~~

Result: exit code 0; output ended with `ALL OK`. This covers the expert-store registry unit test, not the full model engine.

## 7. Deferred tiny-model test

The repository's `deepseek_v4_tiny` fixture currently contains configuration, tokenizer and oracle metadata but no generated weight file. Its generator requires pinned PyTorch, Transformers with the official DeepSeek V4 implementation, and safetensors. Those dependencies are not installed on the workstation.

No dependencies were installed merely to force this test. The tiny-model CPU/CUDA end-to-end test remains NOT RUN.

## 8. What has not happened

- No full or quantized DeepSeek model weights downloaded.
- No DeepSeek model inference performed.
- No throughput, TTFT, prefill, context, tool-call or quality benchmark claimed.
- No Colibrì server started.
- No FR3K provider route changed.
- No existing llama.cpp service/model changed.

## 9. Next engineering gates

1. Approve and download the selected full-model GGUF.
2. Verify all four shard sizes and SHA-256 hashes.
3. Run `coli import --mode link`; confirm `deepseek4` architecture recognition.
4. Run `coli plan` and `coli doctor` against the imported model.
5. Generate the tiny fixture in an isolated venv and run CPU/CUDA/Vulkan correctness tests.
6. Run the full model's CPU-canonical short prompt before enabling GPU acceleration.
