#!/usr/bin/env bash
# RES-001 :: src_imagerewarddb :: ImageRewardDB (ImageReward, NeurIPS 2023)
#
# Official page : https://huggingface.co/datasets/zai-org/ImageRewardDB
#                 (THUDM/ImageRewardDB now 307-redirects here; org renamed)
# Access        : public, anonymous. No login, token or agreement observed.
# Licence       : dataset card states apache-2.0; code MIT.
# Underlying    : images collected from DiffusionDB (Stable Diffusion generations).
# Subset rule   : the distributor's own complete `validation` split. Using a published
#                 split whole means there is NO selection judgement of ours at all —
#                 the cleanest possible bounded subset. Full dataset is ~23.7 GB, far
#                 beyond the RES-001 budget.
set -euo pipefail
cd "$(dirname "$0")/../.."
source resources/scripts/guard.sh

SRC=src_imagerewarddb
REPO="https://huggingface.co/datasets/zai-org/ImageRewardDB/resolve/main"
DEST="resources/corpus/raw/$SRC"
TMP="resources/corpus/tmp/$SRC"
mkdir -p "$DEST" "$TMP"

FILES="images/validation/validation_1.zip images/validation/validation_2.zip"

BYTES=0
for f in $FILES; do
  b=$(curl -sS -I -L "$REPO/$f" | tr -d '\r' | tr 'A-Z' 'a-z' | awk '/^content-length:/{v=$2}END{print v}')
  BYTES=$((BYTES + b))
done
echo "[$SRC] selection = official validation split, $BYTES bytes"
check_budget "$BYTES" "$BYTES"

echo "[$SRC] fetching metadata + licence-bearing files..."
for m in README.md ImageRewardDB.py; do
  curl -sS -L --retry 3 -o "$DEST/$m" "$REPO/$m" || true
done

for f in $FILES; do
  out="$TMP/$(basename "$f")"
  echo "[$SRC] downloading $(basename "$f")..."
  curl -sS -L -C - --retry 3 -o "$out" "$REPO/$f"
  echo -n "  sha256 (before any deletion): "; shasum -a 256 "$out" | tee -a "$DEST/_archive.sha256" | awk '{print $1}'
  unzip -q -o "$out" -d "$DEST"
done
echo "[$SRC] extracted $(find "$DEST" -type f \( -name '*.png' -o -name '*.jpg' -o -name '*.webp' \) | wc -l | tr -d ' ') images"
