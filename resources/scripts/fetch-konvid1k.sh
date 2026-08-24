#!/usr/bin/env bash
# RES-001 :: src_konvid1k :: KoNViD-1k (Universitat Konstanz, MMSP/VQA Group)
#
# Official page : https://database.mmsp-kn.de/konvid-1k-database.html
# Archive URL   : https://datasets.vqa.mmsp-kn.de/archives/KoNViD_1k_videos.zip
# Access        : public, ungated. No login, form, cookie or click-through observed.
# robots.txt    : datasets.vqa.mmsp-kn.de -> 404 (none). database.mmsp-kn.de does not
#                 disallow /konvid-1k-database.html.
# Rights        : NOT STATED by the distributor. Acquired under RES-001 clarification 6/7
#                 for INTERNAL RESEARCH AND EVALUATION ONLY. Not redistributable, not
#                 training data, not customer-deliverable, not production-cleared.
# Reproducible  : re-running this script re-fetches the same archive from the same URL.
set -euo pipefail
cd "$(dirname "$0")/../.."
source resources/scripts/guard.sh

SRC=src_konvid1k
URL="https://datasets.vqa.mmsp-kn.de/archives/KoNViD_1k_videos.zip"
DEST="resources/corpus/raw/$SRC"
TMP="resources/corpus/tmp/$SRC"
mkdir -p "$DEST" "$TMP"

echo "[$SRC] resolving remote size..."
BYTES=$(curl -sS -I -L "$URL" | tr -d '\r' | tr 'A-Z' 'a-z' | awk '/^content-length:/{v=$2}END{print v}')
echo "[$SRC] remote content-length: $BYTES bytes"
# zip of already-compressed mp4: extracted size ~= archive size
check_budget "$BYTES" "$BYTES"

echo "[$SRC] downloading (resumable)..."
curl -L -C - --retry 3 --retry-delay 5 -o "$TMP/KoNViD_1k_videos.zip" "$URL"

echo "[$SRC] fingerprinting archive BEFORE any deletion (Amendment 01 condition 4)..."
shasum -a 256 "$TMP/KoNViD_1k_videos.zip" | tee "$DEST/_archive.sha256"

echo "[$SRC] extracting..."
unzip -q -o "$TMP/KoNViD_1k_videos.zip" -d "$DEST"
echo "[$SRC] extracted $(find "$DEST" -type f -name '*.mp4' | wc -l | tr -d ' ') mp4 files"
echo "[$SRC] done. Archive retained at $TMP until validation completes."
