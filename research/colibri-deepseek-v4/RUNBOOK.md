

## Pinned, resumable download route

The Omarchy workstation does not currently have the Hugging Face CLI or Python pip installed. Do not install packages just to download this model. Use the prepared curl-based script instead:

~~~bash
bash scripts/download-ad-iq2-xs.sh --confirm-download <APPROVED_MODEL_DIRECTORY>
~~~

The script is intentionally not run as part of preflight. It requires the explicit `--confirm-download` argument, pins model revision `17eb08debccb00a8d4dba11642ed1997f85c9d1c`, checks the remaining bytes plus a 5.1 GB reserve, downloads sequentially with resume support, verifies exact byte counts, and writes a local SHA-256SUMS file. It does not import or launch the model.

See [DOWNLOAD-MANIFEST.md](DOWNLOAD-MANIFEST.md) for the exact 85,141,812,960-byte four-shard manifest and upstream HEAD metadata.
