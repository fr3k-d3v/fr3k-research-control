# Sanitised local preflight summary — 2026-11-14

**Research ID:** FR3K-LLM-COLIBRI-DSV4-001  
**Classification:** Public-safe summary. Raw command output, local paths, filesystem identifiers, volume labels, hostnames, PIDs and service details remain private.

## Observed hardware class

- Consumer NVIDIA GPU profile: 12 GB VRAM, compute capability 8.6.
- Host memory profile: 32 GB RAM.
- Exact machine identity and storage inventory are not published.

## Runtime observations

- Colibrì v2.1.0 CPU DeepSeek V4 engine build: PASS.
- Colibrì v2.1.0 CUDA sm_86 DeepSeek V4 engine build: PASS.
- CUDA runtime vector-add smoke: PASS.
- Generic Vulkan device initialization: PASS; not a DeepSeek V4 GGUF inference test.
- DeepSeek V4 expert-store registry unit test: PASS.
- No model weights downloaded; no actual DeepSeek inference performed.
- Existing inference baseline preserved.

## Selected model

Huihui DeepSeek V4 Flash 0731 Abliterated Q2 GGUF:
- Revision: `a8dfba9c1e43bdf324ee2c7787ed01c70975ffb4`
- File: `DeepSeek-V4-Flash-Q2-0731.gguf`
- Bytes: 86,720,111,488
- SHA-256: `73d17d12b2988b31df519ae381096bcaa737361664d76ce2c88a9ed6b68ff756`

## Storage and execution gate

Private preflight found a larger local NTFS volume with sufficient capacity. The filesystem was marked dirty; the Linux NTFS driver refused a read-write mount and recommended Windows `chkdsk`. The volume was inspected read-only only. No force mount, repair, format, repartition or data write was performed.

The target workstation was subsequently unavailable through Fleet. Device identifiers, volume UUID, mount path and exact capacity figures remain private.

## Next gates

1. Complete a proper Windows filesystem check on the target data volume.
2. Reconnect the target workstation and re-observe all storage.
3. Verify a clean read-write mount and at least 92,000,000,000 free bytes.
4. Measure storage throughput; capacity does not prove random-read suitability for expert streaming.
5. Run the guarded downloader, verify size and SHA-256, then import in place.
6. Require `coli plan` and `coli doctor` to pass before inference.
