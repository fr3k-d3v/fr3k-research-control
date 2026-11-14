# AtomicChat AD-IQ2_XS — pinned download manifest

**Research ID:** FR3K-LLM-COLIBRI-DSV4-001  
**Status:** HEAD requests completed · no model bytes downloaded · download requires explicit approval.

## Repository pin

- Repository: https://huggingface.co/AtomicChat/DeepSeek-V4-Flash-0731-GGUF
- Model repository revision: `17eb08debccb00a8d4dba11642ed1997f85c9d1c`
- Last modified: 2026-10-28T13:13:25Z
- Variant: `AD-IQ2_XS`
- Licence shown by model page: MIT
- Architecture tag: `deepseek_v4`
- Folder page last-change short commit: `8c7a581`

The full repository revision above was resolved through the Hugging Face model API. The four file sizes below were independently checked with HTTP HEAD requests pinned to that revision. No model content was fetched.

## Exact shard manifest

| File | Exact bytes | Decimal GB | Upstream x-linked-etag | Upstream x-xet-hash |
|---|---:|---:|---|---|
| `DeepSeek-V4-Flash-0731-AD-IQ2_XS-00001-of-00004.gguf` | 22,479,254,144 | 22.4793 | `0b035076aee8dcf0cf191c5f9571c9609a42c59cc0ca6c8f91f8e6622867d93d` | `c50c868b1a0080638eec557664aefffe6cc3e9bf34beeb068120b827eb93a531` |
| `DeepSeek-V4-Flash-0731-AD-IQ2_XS-00002-of-00004.gguf` | 22,598,912,960 | 22.5990 | `1b36b9fd688d28c5476061b8280530ebfb482e5a4306bf32bd20b9f855ad37c7` | `ad3a05871ce3f62e4429e39f10a476514ddc08650814aebbfea7dd49fe0754cc` |
| `DeepSeek-V4-Flash-0731-AD-IQ2_XS-00003-of-00004.gguf` | 24,209,525,696 | 24.2095 | `839a23787dd29ff2620fd2159935c645964fe4c6a6694f44f1a0125ba04d54eb` | `af618f2121b69b90f4d04c58796752a075fb65a30d908d922c9d70db37640053` |
| `DeepSeek-V4-Flash-0731-AD-IQ2_XS-00004-of-00004.gguf` | 15,854,120,160 | 15.8541 | `b30ddea479706e52c45d21e196d7147144717496d1b70d21ae66a0f304c3545f` | `7b5b7493dabc8c4c7deed95281a781d8c77d286f34ef57b03dfabba6e08eb3e0` |

**Total:** 85,141,812,960 bytes = 85.1418 GB decimal = 79.2945 GiB.

The `x-linked-etag` and `x-xet-hash` values are recorded exactly as returned by the upstream HEAD response. They are not labelled as local SHA-256 checksums. After download, calculate local SHA-256 for every shard and retain the resulting manifest.

## Disk budget at preflight

- Available on the selected model volume: 93,879,758,848 bytes.
- Exact model bytes: 85,141,812,960 bytes.
- Estimated free after complete download: 8,737,945,888 bytes (8.74 GB decimal).
- Colibrì catalogue reserve inferred from official checkpoint sizing: approximately 5.1 GB.
- Remaining beyond that reserve: approximately 3.64 GB.

**Assessment: TIGHT.** The script rechecks the destination volume at execution time and requires the remaining download bytes plus a 5.1 GB reserve. It downloads sequentially, resumes partial shards and does not import or start the model.

## Safe download

Use [`scripts/download-ad-iq2-xs.sh`](scripts/download-ad-iq2-xs.sh). It refuses to download unless the operator passes the explicit `--confirm-download` flag. It checks free space, pins the full repository revision, verifies exact shard byte counts, and creates a local SHA-256 manifest.

After download, use Colibrì's `coli import --mode link`; do not use copy mode on this volume.
