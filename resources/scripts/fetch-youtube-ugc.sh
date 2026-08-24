#!/usr/bin/env bash
# RES-001 :: src_youtube_ugc :: YouTube-UGC (Google / YouTube Media Algorithms)
#
# Official page : https://media.withyoutube.com/
# Distribution  : public Google Cloud Storage bucket `ugc-dataset`, anonymous HTTP.
#                 NOT scraped from youtube.com. No YouTube endpoint is touched.
# Access        : ungated, anonymous listing returns HTTP 200. No login/form/agreement.
# Licence       : EXPLICIT. gs://ugc-dataset/LICENSE is a Creative Commons Public License.
#                 gs://ugc-dataset/ATTRIBUTION names each clip's original title, author and
#                 "licensed under CC BY 4.0".
# Selection     : deterministic and content-blind — within the smallest-resolution tier (360P),
#                 keys are sorted lexicographically and the FIRST clip of each source-defined
#                 category is taken, in sorted category order, until the byte budget is reached.
#                 The category axis is the distributor's own directory structure, not our
#                 judgement about content. No file is chosen for what it depicts or how good
#                 it looks.
set -euo pipefail
cd "$(dirname "$0")/../.."
source resources/scripts/guard.sh

SRC=src_youtube_ugc
BUCKET="https://storage.googleapis.com/ugc-dataset"
DEST="resources/corpus/raw/$SRC"
SOURCE_BUDGET_BYTES=${SOURCE_BUDGET_BYTES:-900000000}   # ~0.84 GB
mkdir -p "$DEST"

echo "[$SRC] fetching licence and attribution..."
curl -sS --retry 3 -o "$DEST/LICENSE" "$BUCKET/LICENSE"
curl -sS --retry 3 -o "$DEST/ATTRIBUTION" "$BUCKET/ATTRIBUTION"

echo "[$SRC] listing bucket (paginated, rate-limited)..."
python3 - "$BUCKET" "$DEST" "$SOURCE_BUDGET_BYTES" <<'PY'
import sys, time, urllib.request, xml.etree.ElementTree as ET, json
bucket, dest, budget = sys.argv[1], sys.argv[2], int(sys.argv[3])
NS = "{http://doc.s3.amazonaws.com/2006-03-01}"
keys, marker = [], ""
while True:
    url = f"{bucket}?max-keys=1000" + (f"&marker={urllib.parse.quote(marker)}" if marker else "")
    root = ET.fromstring(urllib.request.urlopen(url, timeout=90).read())
    page = [(c.find(NS+"Key").text, int(c.find(NS+"Size").text)) for c in root.findall(NS+"Contents")]
    keys += page
    if root.findtext(NS+"IsTruncated") != "true": break
    marker = root.findtext(NS+"NextMarker") or page[-1][0]
    time.sleep(1)          # rate-limit: polite, never parallel
vids = sorted(k for k in keys if k[0].startswith("original_videos/") and k[0].endswith(".mkv"))
p360 = [k for k in vids if "/360P/" in k[0]]
first_per_cat, seen = [], set()
for k, s in p360:                       # already sorted -> first per category is deterministic
    cat = k.split("/")[1]
    if cat in seen: continue
    seen.add(cat); first_per_cat.append((k, s))
sel, tot = [], 0
for k, s in first_per_cat:
    if tot + s > budget: continue
    sel.append((k, s)); tot += s
json.dump({"total_video_keys": len(vids), "tier_360P": len(p360),
           "selected": [k for k, _ in sel], "selected_bytes": tot},
          open(f"{dest}/_selection.json", "w"), indent=1)
print(f"  bucket objects listed : {len(keys)}")
print(f"  video keys            : {len(vids)}  (360P tier: {len(p360)})")
print(f"  deterministic pick    : {len(sel)} files, {tot/1e9:.2f} GB")
PY

BYTES=$(python3 -c "import json;print(json.load(open('$DEST/_selection.json'))['selected_bytes'])")
check_budget "$BYTES" "$BYTES"

echo "[$SRC] downloading selection sequentially..."
python3 -c "import json;[print(k) for k in json.load(open('$DEST/_selection.json'))['selected']]" | while read -r key; do
  out="$DEST/$(basename "$key")"
  [ -s "$out" ] && { echo "  skip $(basename "$key")"; continue; }
  curl -sS -L -C - --retry 3 -o "$out" "$BUCKET/$key"
  echo "  got  $(basename "$key") ($(stat -f%z "$out") bytes)"
  sleep 1
done
echo "[$SRC] done."
