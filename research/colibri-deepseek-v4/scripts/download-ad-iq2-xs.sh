#!/usr/bin/env bash
set -euo pipefail

# Large model download is deliberately opt-in. This script does not import or
# launch the model. It downloads four pinned shards sequentially and resumes
# partial files without making a second model copy.

if [[ "${1:-}" != "--confirm-download" ]]; then
  echo "Refusing: pass --confirm-download to authorise the 85.14 GB download." >&2
  echo "Usage: $0 --confirm-download [destination-directory]" >&2
  exit 2
fi

DEST="${2:-${HOME}/models/DeepSeek-V4-Flash-0731-AD-IQ2_XS}"
REPO="AtomicChat/DeepSeek-V4-Flash-0731-GGUF"
REV="17eb08debccb00a8d4dba11642ed1997f85c9d1c"
VARIANT="AD-IQ2_XS"
RESERVE_BYTES=5100000000
BASE_URL="https://huggingface.co/${REPO}/resolve/${REV}/${VARIANT}"

FILES=(
  "DeepSeek-V4-Flash-0731-AD-IQ2_XS-00001-of-00004.gguf"
  "DeepSeek-V4-Flash-0731-AD-IQ2_XS-00002-of-00004.gguf"
  "DeepSeek-V4-Flash-0731-AD-IQ2_XS-00003-of-00004.gguf"
  "DeepSeek-V4-Flash-0731-AD-IQ2_XS-00004-of-00004.gguf"
)
SIZES=(
  22479254144
  22598912960
  24209525696
  15854120160
)

for cmd in curl df stat sha256sum; do
  command -v "$cmd" >/dev/null 2>&1 || {
    echo "Required command missing: $cmd" >&2
    exit 3
  }
done

mkdir -p "$DEST/${VARIANT}"
DEST="$(cd "$DEST" && pwd)"
MODEL_DIR="$DEST/${VARIANT}"

remaining_bytes=0
for i in "${!FILES[@]}"; do
  path="$MODEL_DIR/${FILES[$i]}"
  expected="${SIZES[$i]}"
  actual=0
  if [[ -f "$path" ]]; then
    actual="$(stat -c %s "$path")"
  fi
  if (( actual > expected )); then
    echo "Refusing: $path is larger than its pinned expected size." >&2
    exit 4
  fi
  remaining_bytes=$((remaining_bytes + expected - actual))
done

available_bytes="$(df -B1 --output=avail "$DEST" | tail -n 1 | tr -d '[:space:]')"
required_bytes=$((remaining_bytes + RESERVE_BYTES))

echo "Repository: $REPO"
echo "Revision:   $REV"
echo "Variant:    $VARIANT"
echo "Destination:$DEST"
echo "Remaining download bytes: $remaining_bytes"
echo "Required reserve bytes:   $RESERVE_BYTES"
echo "Currently available:      $available_bytes"

if (( available_bytes < required_bytes )); then
  echo "BLOCKED: need $required_bytes bytes free; have $available_bytes." >&2
  exit 5
fi

for i in "${!FILES[@]}"; do
  file="${FILES[$i]}"
  expected="${SIZES[$i]}"
  path="$MODEL_DIR/$file"
  actual=0
  if [[ -f "$path" ]]; then
    actual="$(stat -c %s "$path")"
  fi

  if (( actual == expected )); then
    echo "Already complete: $file"
    continue
  fi

  echo "Downloading/resuming: $file"
  curl --fail --location --retry 5 --retry-delay 3 --retry-all-errors \
    --continue-at - "$BASE_URL/$file" --output "$path"

  actual="$(stat -c %s "$path")"
  if (( actual != expected )); then
    echo "SIZE MISMATCH: $file expected $expected bytes, got $actual." >&2
    exit 6
  fi
done

(
  cd "$MODEL_DIR"
  sha256sum "${FILES[@]}" > SHA256SUMS
  echo
  echo "All four shards match their pinned byte counts."
  echo "Local SHA-256 manifest:"
  cat SHA256SUMS
)

echo
echo "Download complete. No import or server start was performed."
echo "Next gate: verify SHA256SUMS, then run coli import --mode link."
