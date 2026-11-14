# Runbook — safe preflight, install and operation

**Current state:** Colibrì v2.1.0 CPU and CUDA sm_86 engine builds pass. Huihui's abliterated Q2 model is selected. Download is blocked by a local filesystem write gate and target-host availability. No model weights are downloaded.

## Phase 0 — read-only observation

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
python3 c/setup_hw.py --json
python3 c/coli setup --list --json
~~~

Do not run `coli setup --yes`, model download, `coli import` or package installation during preflight.

## Phase 1 — isolated runtime

- Source: https://github.com/JustVugg/colibri
- Release: v2.1.0
- Commit: `704a3f68184b78367a04cb5526e428dc2f90f05b`
- Release archive SHA-256: `d54b4c57c12417fc9e784b649249ac1aa3480eec44ece2777d4cbc639a25e66a`

~~~bash
cd c
make -f Makefile.deepseek-v4 deepseek-v4
CUDA_HOME=/opt/cuda make -f Makefile.deepseek-v4 deepseek-v4 CUDA=1 CUDA_ARCH=sm_86
~~~

Both builds passed in private preflight. See BUILD-AND-SMOKE-TESTS.md.

## Phase 2 — selected abliterated model download

- Repository: https://huggingface.co/huihui-ai/Huihui-DeepSeek-V4-Flash-0731-abliterated-GGUF
- Revision: `a8dfba9c1e43bdf324ee2c7787ed01c70975ffb4`
- File: `DeepSeek-V4-Flash-Q2-0731.gguf`
- Exact bytes: `86720111488`
- SHA-256: `73d17d12b2988b31df519ae381096bcaa737361664d76ce2c88a9ed6b68ff756`

Before download:

1. Complete Windows `chkdsk X: /scan` and, if needed, `chkdsk X: /f` on the correct data volume.
2. Fully shut Windows down and return to the target Linux workstation.
3. Confirm Fleet reachability and re-observe all attached storage.
4. Verify the chosen filesystem is clean, mounted read-write and has at least 92,000,000,000 free bytes.
5. Set local-only environment variables; do not commit their values:

~~~bash
export FR3K_MODEL_MOUNT=/mnt/models
export FR3K_MODEL_VOLUME_UUID='<local-only-filesystem-uuid>'
export FR3K_MODEL_FSTYPE=ntfs3
~~~

6. Create the destination directory:

~~~bash
mkdir -p "$FR3K_MODEL_MOUNT/FR3K-Models/DeepSeek-V4-Flash-0731-Abliterated-Q2"
~~~

7. Run the guarded script:

~~~bash
bash research/colibri-deepseek-v4/scripts/download-huihui-abliterated-q2.sh --confirm-download "$FR3K_MODEL_MOUNT/FR3K-Models/DeepSeek-V4-Flash-0731-Abliterated-Q2"
~~~

Do not force-mount NTFS or write to a dirty volume.

## Phase 3 — import in place

~~~bash
coli import \
  "$FR3K_MODEL_MOUNT/FR3K-Models/DeepSeek-V4-Flash-0731-Abliterated-Q2/DeepSeek-V4-Flash-Q2-0731.gguf" \
  --mode link \
  --out "$FR3K_MODEL_MOUNT/FR3K-Models/DeepSeek-V4-Flash-0731-Abliterated-Q2/DeepSeek-V4-Flash-0731-Abliterated-Q2.colibri"

coli plan --model "$FR3K_MODEL_MOUNT/FR3K-Models/DeepSeek-V4-Flash-0731-Abliterated-Q2/DeepSeek-V4-Flash-0731-Abliterated-Q2.colibri"
coli doctor --model "$FR3K_MODEL_MOUNT/FR3K-Models/DeepSeek-V4-Flash-0731-Abliterated-Q2/DeepSeek-V4-Flash-0731-Abliterated-Q2.colibri"
~~~

The exact artifact has not been imported; compatibility remains UNKNOWN until tested. Do not start inference unless planner and doctor report a safe memory/disk plan.

## Phase 4 — correctness before speed

- Run a short CPU-canonical prompt with a low output limit.
- Capture output, stop reason, logs and resource telemetry.
- Repeat the same prompt on CUDA sm_86.
- Test Vulkan separately.
- Only after correctness passes, begin context and throughput sweeps.

## Phase 5 — local API

Use loopback only and a locally generated API key:

~~~bash
COLI_API_KEY='<local-secret-from-secret-store>' \
  coli serve --host 127.0.0.1 --port 8000 \
  --model "$FR3K_MODEL_MOUNT/FR3K-Models/DeepSeek-V4-Flash-0731-Abliterated-Q2/DeepSeek-V4-Flash-0731-Abliterated-Q2.colibri"
~~~

Do not place tokens in shell history, logs or Git. Do not expose the endpoint to LAN, tailnet or public internet before a separate threat review.

## Local-only evidence

Raw logs, model files, tokens, private paths, filesystem identifiers, volume labels and machine identifiers stay local. Publish only sanitised measurements, artifact hashes and reproducible commands.
