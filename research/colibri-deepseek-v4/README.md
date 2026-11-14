
## Pinned model download preparation

- [Exact four-shard manifest](DOWNLOAD-MANIFEST.md) — full Hugging Face revision, byte sizes, upstream ETag/Xet headers and storage arithmetic.
- [Safe resumable downloader](scripts/download-ad-iq2-xs.sh) — requires the explicit `--confirm-download` argument, checks free space plus reserve, pins the model revision and verifies every shard size. It has **not** been run.
