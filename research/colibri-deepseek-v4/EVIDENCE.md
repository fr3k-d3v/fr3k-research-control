

## Additional upstream artifact evidence — 2026-11-14

- **SRC-14 — VERIFIED FACT:** Hugging Face model API for AtomicChat resolved repository revision `17eb08debccb00a8d4dba11642ed1997f85c9d1c`, last modified 2026-10-28.
- **SRC-15 — EVIDENCE:** HTTP HEAD responses pinned to SRC-14 returned four exact `Content-Length` values totalling 85,141,812,960 bytes. Per-shard `x-linked-etag` and `x-xet-hash` values are recorded in DOWNLOAD-MANIFEST.md.
- **LOC-15 — EVIDENCE:** Current free space minus exact pinned shard total is 8,737,945,888 bytes. No model content was downloaded during these HEAD requests.
- **LOC-16 — OBSERVATION:** `curl` is available; `hf`, `huggingface-cli` and system Python `pip` are absent. A curl-only resumable downloader has been prepared but not executed.
