# Runbook — safe preflight, install and operation

This is a staged runbook. **Only Phase 0 is authorised by this research plan.** Installation and model download remain gated on the preflight report and explicit approval of the selected artifact.

## Phase 0 — read-only observation

Run on Omarchy from a normal user shell. These commands inspect state; they should not install packages or download model weights.

~~~bash
# Host and memory
date -Is
uname -a
lscpu
free -h
swapon --show

# GPU, driver, free VRAM and compute capability
nvidia-smi
nvidia-smi --query-gpu=name,memory.total,memory.free,driver_version,pci.bus_id,compute_cap --format=csv
nvidia-smi --query-compute-apps=pid,process_name,used_memory --format=csv

# CUDA compiler/toolkit, if present
command -v nvcc && nvcc --version || true

# Vulkan device / driver, if present
command -v vulkaninfo && vulkaninfo --summary || true

# Storage topology, free space and filesystem
lsblk -o NAME,MODEL,SIZE,ROTA,TYPE,FSTYPE,MOUNTPOINTS
df -hT
~~~

Then use Colibrì's documented read-only hardware and catalogue commands from a pinned checkout:

~~~bash
python3 c/setup_hw.py --json
python3 c/coli setup --list --json
~~~

Do not run coli setup --yes, start-here.sh, hf download, coli import or any package installation in Phase 0.

## Phase 1 — approved isolated checkout

After approval, create a dedicated work directory, clone Colibrì, and pin a reviewed commit or release. Do not build inside the current llama.cpp checkout.

Research snapshot recorded on 2026-11-14:

- Main: 0a5504a1dc64f86fcd0fe7db298b0448c730e7e6
- Dev: fd7ed68afa1f88706eae08ef172a5bc02c42bd77
- Latest release observed: v2.1.0

Use the exact commit selected in the run manifest. Recheck upstream before executing; do not follow a moving branch during a benchmark.

## Phase 2 — choose and download one artifact

### Official full checkpoint

~~~bash
hf download deepseek-ai/DeepSeek-V4-Flash-0731 \
  --local-dir /path/on/approved/nvme/DeepSeek-V4-Flash-0731
~~~

Approximate upstream size: 167 GB. Do not run until free space, model revision and approval are recorded.

### Full-model GGUF quant

Repository: [unsloth/DeepSeek-V4-Flash-0731-GGUF](https://huggingface.co/unsloth/DeepSeek-V4-Flash-0731-GGUF)

Target variant: UD-IQ2_XXS. Capture the exact folder/file manifest and total bytes before download; the Colibrì README rounds this to 85 GB while the Hugging Face listing reports 90.9 GB.

~~~bash
# Illustrative only — confirm the exact file list and revision before executing.
hf download unsloth/DeepSeek-V4-Flash-0731-GGUF \
  --include 'UD-IQ2_XXS/*' \
  --local-dir /path/on/approved/nvme/DeepSeek-V4-Flash-0731-GGUF
~~~

Then import the first GGUF shard according to the current Colibrì GGUF guide. The importer reads linked files in place by default; do not use copy mode unless its extra disk requirement is measured and approved.

### REAP fallback

Repository: [puwaer/DeepSeek-V4-Flash-0731-reap-150b](https://huggingface.co/puwaer/DeepSeek-V4-Flash-0731-reap-150b)

Only use after documenting why the full 284B route is blocked or unsuitable. Record it as a separate 150B pruned model.

## Phase 3 — build and inspect

- Build the CPU-canonical deepseek_v4 engine first.
- Run the self-test and coli doctor.
- Inspect the model placement with coli plan.
- Build generic CUDA for sm_86 only if the observed CUDA toolkit and driver satisfy the pinned Colibrì guide.
- Do not build the sm_120a DeepGEMM target for RTX 3060.
- Treat Vulkan as a separate backend experiment. The DeepSeek V4 Vulkan expert tier is documented for GGUF; do not assume every dense Vulkan chain is enabled or measured for this engine.

Do not change system packages without showing the exact package and obtaining approval.

## Phase 4 — start locally

Use loopback only and a locally generated API key:

~~~bash
COLI_API_KEY='<local-secret-from-secret-store>' \
  python3 c/coli serve --host 127.0.0.1 --port 8000 \
  --model /path/to/approved/model
~~~

The exact model path and model ID depend on the chosen artifact. Read the actual runtime status and GET /v1/models; do not assume the example path or model ID is correct.

Test the endpoint with the bearer token. Do not place the token in shell history, logs, process arguments visible to other users, or Git.

## Phase 5 — stop and rollback

- Stop only the Colibrì evaluation process/service.
- Verify the process has exited and GPU memory has been released.
- Restore FR3K's provider route to the accepted llama.cpp baseline.
- Do not delete the model or logs until evidence is archived and the user approves cleanup.
- If a CUDA context/kernel failure occurs, stop the process and return to the CPU reference. Do not continue GPU requests in a process after a sticky CUDA failure.

## Local-only evidence

Raw logs, .coli_usage, model files, API keys, local host paths and full hardware identifiers stay on the machine. Publish only sanitised, reproducible summaries in this repository.
