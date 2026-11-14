

## Download preparation update

- The exact AtomicChat model repository revision and all four shard byte counts have been resolved and recorded in DOWNLOAD-MANIFEST.md.
- A resumable curl downloader is committed at scripts/download-ad-iq2-xs.sh. It requires `--confirm-download`, checks free space plus reserve, and verifies byte counts.
- The script has NOT been executed. DSV4-04 remains BLOCKED pending explicit approval of the 85.14 GB download.
