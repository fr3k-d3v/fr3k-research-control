#!/usr/bin/env bash
set -Eeuo pipefail
umask 022

MODEL_MOUNT="${FR3K_MODEL_MOUNT:-/mnt/models}"
readonly EXPECTED_UUID="${FR3K_MODEL_VOLUME_UUID:-}"
readonly EXPECTED_FSTYPE="${FR3K_MODEL_FSTYPE:-ntfs3}"
readonly MIN_FREE_BYTES=92000000000
readonly EXPECTED_SIZE=86720111488
readonly EXPECTED_SHA256="73d17d12b2988b31df519ae381096bcaa737361664d76ce2c88a9ed6b68ff756"
readonly FILE_NAME="DeepSeek-V4-Flash-Q2-0731.gguf"
readonly REVISION="a8dfba9c1e43bdf324ee2c7787ed01c70975ffb4"
readonly URL="https://huggingface.co/huihui-ai/Huihui-DeepSeek-V4-Flash-0731-abliterated-GGUF/resolve/a8dfba9c1e43bdf324ee2c7787ed01c70975ffb4/DeepSeek-V4-Flash-Q2-0731.gguf?download=true"

usage() {
  echo "Usage: FR3K_MODEL_VOLUME_UUID=<local-only-uuid> $0 --confirm-download <destination-under-model-mount>" >&2
  exit 2
}

[[ "${1:-}" == "--confirm-download" ]] || usage
DEST="${2:-}"
[[ -n "$DEST" && -n "$EXPECTED_UUID" ]] || usage
MODEL_MOUNT="${MODEL_MOUNT%/}"

case "$DEST" in
  "$MODEL_MOUNT"/*) ;;
  *) echo "Destination must be under the configured model mount." >&2; exit 2 ;;
esac
[[ -d "$DEST" ]] || {
  echo "Destination directory must already exist on the repaired, mounted model volume." >&2
  exit 1
}

MOUNT_TARGET="$(findmnt -n -o TARGET -T "$DEST")"
FSTYPE="$(findmnt -n -o FSTYPE -T "$DEST")"
OPTIONS="$(findmnt -n -o OPTIONS -T "$DEST")"
SOURCE="$(findmnt -n -o SOURCE -T "$DEST")"
UUID="$(blkid -s UUID -o value "$SOURCE" 2>/dev/null | tr '[:lower:]' '[:upper:]')"
NORMALIZED_EXPECTED_UUID="$(printf '%s' "$EXPECTED_UUID" | tr '[:lower:]' '[:upper:]')"

[[ "$MOUNT_TARGET" == "$MODEL_MOUNT" ]] || {
  echo "Destination is not on the configured model mount." >&2
  exit 1
}
[[ "$FSTYPE" == "$EXPECTED_FSTYPE" ]] || {
  echo "Unexpected filesystem type: $FSTYPE" >&2
  exit 1
}
[[ ",$OPTIONS," == *",rw,"* ]] || {
  echo "Filesystem is not mounted read-write; refusing download." >&2
  exit 1
}
[[ "$UUID" == "$NORMALIZED_EXPECTED_UUID" ]] || {
  echo "Mounted filesystem does not match the locally supplied UUID." >&2
  exit 1
}

AVAILABLE_BYTES="$(df -B1 --output=avail "$DEST" | tail -n 1 | tr -d ' ')"
[[ "$AVAILABLE_BYTES" =~ ^[0-9]+$ ]] || {
  echo "Could not determine available bytes." >&2
  exit 1
}
(( AVAILABLE_BYTES >= MIN_FREE_BYTES )) || {
  echo "Insufficient free space: $AVAILABLE_BYTES bytes; need at least $MIN_FREE_BYTES." >&2
  exit 1
}

FINAL="$DEST/$FILE_NAME"
PARTIAL="$FINAL.partial"

if [[ -e "$FINAL" ]]; then
  ACTUAL_SIZE="$(stat -c '%s' "$FINAL")"
  [[ "$ACTUAL_SIZE" -eq "$EXPECTED_SIZE" ]] || {
    echo "A file already exists with the wrong size; refusing to overwrite." >&2
    exit 1
  }
  printf '%s  %s\n' "$EXPECTED_SHA256" "$FINAL" | sha256sum -c -
  echo "Verified file already exists; no download needed."
  exit 0
fi

if [[ -f "$PARTIAL" ]]; then
  PARTIAL_SIZE="$(stat -c '%s' "$PARTIAL")"
  (( PARTIAL_SIZE <= EXPECTED_SIZE )) || {
    echo "Partial file is larger than the pinned artifact; preserving it and stopping." >&2
    exit 1
  }
fi

echo "Downloading pinned Huihui DeepSeek V4 Flash 0731 abliterated Q2 GGUF."
echo "Revision: $REVISION"
echo "Bytes: $EXPECTED_SIZE"
echo "Resume is enabled. This script does not import or launch the model."

curl --fail --location --show-error \
  --retry 8 --retry-all-errors --retry-delay 5 \
  --connect-timeout 30 --continue-at - \
  --output "$PARTIAL" "$URL"

ACTUAL_SIZE="$(stat -c '%s' "$PARTIAL")"
[[ "$ACTUAL_SIZE" -eq "$EXPECTED_SIZE" ]] || {
  echo "Size mismatch: expected $EXPECTED_SIZE, received $ACTUAL_SIZE. Partial file retained." >&2
  exit 1
}

printf '%s  %s\n' "$EXPECTED_SHA256" "$PARTIAL" | sha256sum -c -
mv -- "$PARTIAL" "$FINAL"
printf '%s  %s\n' "$EXPECTED_SHA256" "$FINAL" | sha256sum -c -

cat > "$DEST/FR3K-ABLITERATED-MODEL-MANIFEST.txt" <<EOF
repository=huihui-ai/Huihui-DeepSeek-V4-Flash-0731-abliterated-GGUF
revision=$REVISION
file=$FILE_NAME
bytes=$EXPECTED_SIZE
sha256=$EXPECTED_SHA256
downloaded_at=$(date -Is)
EOF

echo "DOWNLOAD AND SHA-256 VERIFICATION COMPLETE."
echo "No model import or inference was started."
