

## Exact pinned GGUF HEAD verification — 2026-11-14

The Hugging Face model API resolved repository revision `17eb08debccb00a8d4dba11642ed1997f85c9d1c` (last modified 2026-10-28). HTTP HEAD requests pinned to that revision returned exact Content-Length values totalling 85,141,812,960 bytes.

With the final preflight free space of 93,879,758,848 bytes, the exact projected remainder is 8,737,945,888 bytes. This clears the approximate 5.1 GB Colibrì catalogue reserve by about 3.64 GB. It remains a tight budget; the prepared downloader repeats the free-space calculation at execution time.

The workstation has `curl`, but no `hf` / `huggingface-cli` executable and no system Python `pip`. The prepared downloader therefore uses pinned direct HTTPS URLs and does not require package installation.
