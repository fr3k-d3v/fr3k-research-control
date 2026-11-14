# Runbook — safe preflight, install and operation

**Current state:** Colibrì v2.1.0 is staged in an isolated evaluation directory; CPU and CUDA sm_86 engine builds pass. The model download is not approved and has not started.

## Phase 0 — read-only observation (completed)

The following commands were used on Omarchy:

~~~bash
date -Is
uname -a
lscpu
free -h
swapon --show
nvidia-smi
nvidia-smi --query-gpu=name,memory.total,memory.free,driver_version,compute_cap --format=csv
command -v nvcc && nvcc --version
lsblk -o NAME,MODEL,SIZE,ROTA,TYPE,FSTYPE,MOUNTPOINTS
df -hT
~~~

Colibrì hardware and catalogue probes:

~~~bash
python3 c/setup_hw.py --json
python3 c/coli setup --list --json
~~~

Do not run `coli setup --yes`, `hf download`, `coli import` or package installation during preflight.

## Phase 1 — isolated runtime (completed in part)

Pinned runtime:

- Source: https://github.com/JustVugg/colibri
- Release: v2.1.0
- Commit: `704a3f68184b78367a04cb5526e428dc2f90f05b`
- Release archive SHA-256: `d54b4c57c12417fc9e784b649249ac1aa3480eec44ece2777d4cbc639a25e66a`

Build CPU reference:

~~~bash
cd c
make -f Makefile.deepseek-v4 deepseek-v4
~~~

Build CUDA for RTX 3060:

~~~bash
CUDA_HOME=/opt/cuda make -f Makefile.deepseek-v4 deepseek-v4 CUDA=1 CUDA_ARCH=sm_86
~~~

Both builds passed on the target. See BUILD-AND-SMOKE-TESTS.md.

## Phase 2 — selected model download (WAIT FOR APPROVAL)

Selected candidate: AtomicChat AD-IQ2_XS, four shards, 85.1 GB total listing.

Repository: https://huggingface.co/AtomicChat/DeepSeek-V4-Flash-0731-GGUF  
Variant: `AD-IQ2_XS/`  
Folder revision shown by Hugging Face: `8c7a581` (resolve the full revision before download).

Before downloading:

1. Recheck `df -B1` on the target volume.
2. Confirm at least 90.2 GB free (85.1 GB artifact plus approximately 5.1 GB reserve) and preferably more.
3. Confirm the destination path and that no other download is using the volume.
4. Obtain explicit user approval for this exact 85.1 GB model.
5. Pin the full model-repository revision and record all four expected files.

Illustrative download using the Hugging Face CLI after it is available in an isolated environment:

~~~bash
hf download AtomicChat/DeepSeek-V4-Flash-0731-GGUF \
  --revision <PINNED_MODEL_REVISION> \
  --include 'AD-IQ2_XS/*' \
  --local-dir <APPROVED_MODEL_DIRECTORY>
~~~

Do not start this command until approval is recorded. Use resumable downloads. After completion, record exact file sizes and SHA-256 hashes.

## Phase 3 — import in place (after successful download)

The Colibrì importer supports `deepseek4` GGUF and defaults to link mode. Use explicit link mode to avoid an additional 85 GB copy:

~~~bash
coli import \
  <APPROVED_MODEL_DIRECTORY>/AD-IQ2_XS/DeepSeek-V4-Flash-0731-AD-IQ2_XS-00001-of-00004.gguf \
  --mode link \
  --out <APPROVED_MODEL_DIRECTORY>/DeepSeek-V4-Flash-0731-AD-IQ2_XS.colibri
~~~

Then run:

~~~bash
coli plan --model <APPROVED_MODEL_DIRECTORY>/DeepSeek-V4-Flash-0731-AD-IQ2_XS.colibri
coli doctor --model <APPROVED_MODEL_DIRECTORY>/DeepSeek-V4-Flash-0731-AD-IQ2_XS.colibri
~~~

Do not start inference unless the planner reports a safe memory/disk plan.

## Phase 4 — correctness before speed

- Run a short CPU-canonical prompt with a low output limit.
- Capture output, token IDs where available, stop reason, logs and resource telemetry.
- Repeat the same prompt on CUDA sm_86.
- Test Vulkan separately; do not conflate generic device initialization with DeepSeek V4 inference.
- Only after correctness passes, begin context and throughput sweeps.

## Phase 5 — local API

Use loopback only and a locally generated API key:

~~~bash
COLI_API_KEY='<local-secret-from-secret-store>' \
  coli serve --host 127.0.0.1 --port 8000 \
  --model <APPROVED_MODEL_DIRECTORY>/DeepSeek-V4-Flash-0731-AD-IQ2_XS.colibri
~~~

The exact command and model ID must be checked against the installed v2.1.0 launcher. Do not place tokens in shell history, logs or Git. Do not expose the endpoint to LAN, Tailscale or public internet before a separate threat review.

## Phase 6 — stop and rollback

- Stop only the Colibrì evaluation process.
- Verify it has exited and GPU memory has been released.
- Restore FR3K's provider route to the accepted llama.cpp endpoint.
- Do not delete the model or logs until evidence is archived and cleanup is approved.

## Local-only evidence

Raw logs, model files, `.coli_usage`, tokens, private paths and full hardware identifiers stay local. Publish sanitised summaries, artifact hashes and reproducible commands only.
