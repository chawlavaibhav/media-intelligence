#!/usr/bin/env bash
# RES-002 :: src_bstd_devanagari :: Bharat Scene Text Dataset — Hindi/Devanagari recognition subset
#
# Official repo : https://github.com/Bhashini-IITJ/BharatSceneTextDataset  (Bhashini / IIT Jodhpur)
# Paper         : arXiv:2511.23071
# Distribution  : creator-published Google Drive link for "Task 2: Cropped Word Recognition"
#                 (recognition.zip, 829,120,510 bytes).
# Access        : PUBLIC, no login. An anonymous request receives Google Drive's standard
#                 "Virus scan warning" interstitial for large files. That page is an advisory,
#                 not an access control: it asks for no credential, no account and no agreement,
#                 and any anonymous visitor can proceed. Passing its confirm token is the normal
#                 anonymous download path, not authentication or anti-bot evasion.
#                 >>> Flagged in the Controller Brief as a judgement call for review. <<<
# Licence       : repo states images are under Creative Commons cc-by-sa-4.0.
#                 Annotation/transcription licence: NOT STATED -> recorded not_stated.
# Retention     : TRANSIENT. The 0.83 GB archive is downloaded to tmp, only the Hindi
#                 (Devanagari) members plus the recognition JSON are extracted and kept, and the
#                 archive is deleted after validation. Re-runnable from the same public link.
set -euo pipefail
cd "$(dirname "$0")/../.."
source resources/scripts/guard.sh

SRC=src_bstd_devanagari
FILE_ID=1d8yOLWrStRTmB8nIJG3mi-w5P9IzB_z8
DEST="resources/corpus/raw/$SRC"; TMP="resources/corpus/tmp/$SRC"
mkdir -p "$DEST" "$TMP"

echo "[$SRC] resolving anonymous download..."
curl -sS -L -m 60 -c "$TMP/cookies" \
  "https://drive.usercontent.google.com/download?id=$FILE_ID&export=download" -o "$TMP/confirm.html"
read -r CONF UUID < <(python3 -c "
import re;h=open('$TMP/confirm.html').read()
g=lambda n:(re.search(r'name=\"%s\"\s+value=\"([^\"]*)\"'%n,h) or [None,'']) [1]
print(g('confirm') or 't', g('uuid'))")
URL="https://drive.usercontent.google.com/download?id=$FILE_ID&export=download&confirm=$CONF&uuid=$UUID"
BYTES=$(curl -sS -I -L -m 60 -b "$TMP/cookies" "$URL" | tr -d '\r' | tr 'A-Z' 'a-z' | awk '/^content-length:/{v=$2}END{print v}')
echo "[$SRC] recognition.zip = $BYTES bytes"
check_budget "$BYTES" 200000000   # Hindi-only retention is a small fraction of the archive

echo "[$SRC] downloading archive to TEMPORARY staging..."
curl -sS -L -C - --retry 3 -b "$TMP/cookies" -o "$TMP/recognition.zip" "$URL"
echo -n "[$SRC] archive sha256 (recorded before deletion): "
shasum -a 256 "$TMP/recognition.zip" | tee "$DEST/_archive.sha256" | awk '{print $1}'

echo "[$SRC] listing members and selecting Devanagari only..."
unzip -Z1 "$TMP/recognition.zip" > "$DEST/_all_members.txt"
wc -l < "$DEST/_all_members.txt" | xargs echo "  total members:"
# Selection rule: UNION of (a) annotation language == "hindi" and (b) transcription contains a
# Devanagari codepoint (U+0900-U+097F). Content-blind - it reads the script, never the meaning or
# any quality judgement. (b) matters because Marathi is written in Devanagari and a language filter
# would miss ~5,100 target-script images; it also catches entries mislabelled as other languages.
unzip -p "$TMP/recognition.zip" "Recognition/train_recognition_data.json" > "$TMP/train.json"
unzip -p "$TMP/recognition.zip" "Recognition/test_recognition_data.json"  > "$TMP/test.json"
python3 - "$TMP" "$DEST" <<'PYS'
import json,sys,re,os
tmp,dest=sys.argv[1],sys.argv[2]
DEV=re.compile(r'[\u0900-\u097F]'); sel=set()
for s in ("train","test"):
    for k,v in json.load(open(f"{tmp}/{s}.json")).items():
        p=v.get("path")
        if p and (v.get("language")=="hindi" or DEV.search(v.get("text") or "")): sel.add(p)
sel |= {"Recognition/train_recognition_data.json","Recognition/test_recognition_data.json"}
open(f"{dest}/_selected_members.txt","w").write("\n".join(sorted(sel))+"\n")
PYS
wc -l < "$DEST/_selected_members.txt" | xargs echo "  selected (Hindi + JSON):"

echo "[$SRC] extracting selected members only (member-level, never the whole archive)..."
python3 - "$TMP/recognition.zip" "$DEST" <<'PYX'
import sys, zipfile, os
zp, dest = sys.argv[1], sys.argv[2]
names = [l.rstrip("\n") for l in open(os.path.join(dest, "_selected_members.txt")) if l.strip()]
n = b = 0
with zipfile.ZipFile(zp) as z:
    have = set(z.namelist())
    for m in names:
        if m not in have or m.endswith("/"): continue
        z.extract(m, dest); n += 1
        b += os.path.getsize(os.path.join(dest, m))
print(f"  extracted {n} members, {b/1e6:.1f} MB")
PYX
echo "[$SRC] extracted; retained bytes: $(du -sk "$DEST" | awk '{printf "%.0f MB", $1/1024}')"
