#!/usr/bin/env bash
# RES-001 :: src_videofeedback :: VideoFeedback (TIGER-Lab, VideoScore)
#
# Annotations : https://huggingface.co/datasets/TIGER-Lab/VideoFeedback   (apache-2.0)
# Media       : https://huggingface.co/datasets/hexuan21/VideoFeedback-videos-mp4 (apache-2.0)
# Access      : public, anonymous. No login, token or agreement observed.
# Underlying  : AI-generated video from multiple text-to-video models, plus some real-world
#               video as augmentation. The dataset card does not name the source models, and
#               does not identify which items are the real-world augmentation. Recorded as
#               not_stated; do not infer.
# Subset rule : none needed — every .mp4 present on the media repo's main revision is taken,
#               which is the whole addressable set at time of access (987 files, 0.18 GB).
set -euo pipefail
cd "$(dirname "$0")/../.."
source resources/scripts/guard.sh

SRC=src_videofeedback
MEDIA="https://huggingface.co/datasets/hexuan21/VideoFeedback-videos-mp4/resolve/main"
ANNO="https://huggingface.co/datasets/TIGER-Lab/VideoFeedback/resolve/main"
DEST="resources/corpus/raw/$SRC"
mkdir -p "$DEST"

curl -sS -L -m 120 "https://huggingface.co/api/datasets/hexuan21/VideoFeedback-videos-mp4/tree/main?recursive=true" -o "$DEST/_tree.json"
BYTES=$(python3 -c "
import json;d=json.load(open('$DEST/_tree.json'))
print(sum(e.get('size',0) for e in d if e['type']=='file' and e['path'].endswith('.mp4')))")
echo "[$SRC] addressable mp4 payload: $BYTES bytes"
check_budget "$BYTES" "$BYTES"

echo "[$SRC] fetching annotation metadata (labels stay source-provided observations)..."
curl -sS -L --retry 3 -o "$DEST/_annotations_README.md" "$ANNO/README.md" || true

echo "[$SRC] downloading media (sequential, rate-limited)..."
python3 -c "
import json;d=json.load(open('$DEST/_tree.json'))
[print(e['path']) for e in sorted(d,key=lambda x:x['path']) if e['type']=='file' and e['path'].endswith('.mp4')]" > "$DEST/_filelist.txt"
n=0
while read -r key; do
  out="$DEST/$(echo "$key" | tr '/' '_')"
  [ -s "$out" ] && continue
  curl -sS -L --retry 3 -o "$out" "$MEDIA/$key"
  n=$((n+1)); [ $((n % 100)) -eq 0 ] && echo "  ...$n files"
done < "$DEST/_filelist.txt"
echo "[$SRC] done: $(ls "$DEST"/*.mp4 2>/dev/null | wc -l | tr -d ' ') mp4 files"
