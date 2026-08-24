#!/usr/bin/env python3
"""Reproduce every number in the EVAL-003 correction, from files already on disk.

Reads nothing from the network and changes nothing. Run it to re-derive the claims in
`resources/reports/RES-CORRECTION-01-indicstr12-composition.md` and in the two Devanagari
source records:

    python3 resources/scripts/verify_devanagari_composition.py

Written so the correction is checkable rather than taken on trust — the record it supports
replaced a description that was wrong for months without anyone noticing.
"""
import collections, glob, json, os, re, statistics, sys
import xml.etree.ElementTree as ET

RAW = "resources/corpus/raw"
MAN = "resources/manifests/corpus-pilot-v0.jsonl"
IND, ILST = "src_indicstr12_devanagari", "src_iiit_ilst_devanagari"
ok = True
def check(label, got, want):
    global ok
    good = got == want
    ok &= good
    print(f"  [{'PASS' if good else 'FAIL'}] {label:<58} {got!r}" + ("" if good else f"  expected {want!r}"))

M = [json.loads(l) for l in open(MAN)]
bn = lambda r: os.path.basename(r["relative_path"])

# ---------- IndicSTR12: scene photos + gt.txt ----------
gts = sorted(glob.glob(f"{RAW}/{IND}/*_gt.txt"))
imgs = {os.path.basename(p) for e in ("jpeg", "jpg", "png") for p in glob.glob(f"{RAW}/{IND}/*.{e}")}
regions, scene = [], set()
bycoord = {}
for g in gts:
    m = re.match(r"verified_twice__(hindi|marathi)__(.+)_gt\.txt$", os.path.basename(g))
    if not m: continue
    lang, parent = m.groups()
    rows = [l.rstrip("\n").split("\t") for l in open(g, encoding="utf-8", errors="replace") if l.strip()]
    rows = [p for p in rows if len(p) >= 10]
    if not rows: continue
    for p in rows: bycoord[(lang, parent, tuple(p[1:9]))] = p[9]
    hit = next((f"verified_twice__{lang}__{parent}{e}" for e in (".jpeg", ".jpg", ".png")
                if f"verified_twice__{lang}__{parent}{e}" in imgs), None)
    if hit: scene.add(hit); regions.append(len(rows))

print("IndicSTR12 — composition")
check("media files acquired", len(imgs), 3086)
check("annotated scene photographs (paired records)", len(scene), 375)
check("min regions per photograph", min(regions), 1)
check("max regions per photograph", max(regions), 98)
check("median regions per photograph", statistics.median(regions), 4)
check("total annotated regions", sum(regions), 2711)

crops = [os.path.basename(p) for p in glob.glob(f"{RAW}/{IND}/*cropped_images__*")]
res = 0
for c in crops:
    m = re.match(r"verified_twice__(hindi|marathi)__cropped_images__(.+)\.(jpeg|jpg|png)$", c)
    if not m: continue
    lang, parts = m.group(1), m.group(2).split("_")
    if len(parts) >= 10 and (lang, parts[0], tuple(parts[2:10])) in bycoord: res += 1
print("\nIndicSTR12 — crops carry recoverable transcriptions")
check("crop images", len(crops), 2713)
check("crops resolved to a transcription by polygon match", res, 2711)

# ---------- IIIT-ILST ----------
xmls = glob.glob(f"{RAW}/{ILST}/*.xml")
eimgs = {os.path.basename(p) for e in ("jpg", "jpeg", "png") for p in glob.glob(f"{RAW}/{ILST}/*.{e}")}
ebox, ecounts, escene = {}, [], set()
for x in xmls:
    m = re.match(r"IIIT-ILST__Devanagari__(.+)\.xml$", os.path.basename(x))
    if not m: continue
    parent = m.group(1)
    try: root = ET.parse(x).getroot()
    except Exception: continue
    objs = root.findall(".//object")
    for o in objs:
        b = o.find("bndbox"); n = o.find("name")
        if b is None: continue
        ebox[(parent, tuple((b.findtext(k) or "").strip() for k in ("xmin","ymin","xmax","ymax")))] = n.text if n is not None else None
    hit = next((f"IIIT-ILST__Devanagari__{parent}{e}" for e in (".jpg",".jpeg",".png")
                if f"IIIT-ILST__Devanagari__{parent}{e}" in eimgs), None)
    if objs and hit: escene.add(hit); ecounts.append(len(objs))
print("\nIIIT-ILST — composition")
check("media files acquired", len(eimgs), 1390)
check("annotated scene photographs (paired records)", len(escene), 176)
check("max regions per photograph", max(ecounts), 64)
check("total annotated regions", sum(ecounts), 1788)

ecrops = [os.path.basename(p) for p in glob.glob(f"{RAW}/{ILST}/*cropped*")]
eres = sum(1 for c in ecrops
           if (m := re.match(r"IIIT-ILST__Devanagari__cropped__Devanagari__(.+)\.(jpg|jpeg|png)$", c))
           and len(pp := m.group(1).split("_")) >= 6 and (pp[0], tuple(pp[2:6])) in ebox)
check("crop images", len(ecrops), 1215)
check("crops resolved to an XML region by bounding box", eres, 1210)

# ---------- overlap, both denominators ----------
byhash = collections.defaultdict(list)
for r in M:
    if r["sha256"]: byhash[r["sha256"]].append(r)
sh = {h for h, v in byhash.items() if len({x["source_id"] for x in v}) > 1}
ilst_all = [r for r in M if r["source_id"] == ILST]
ilst_sh = [r for r in ilst_all if r["sha256"] in sh]
paired_sh = [r for r in ilst_sh if bn(r) in escene]
ind_hindi_scene = {s for s in scene if "__hindi__" in s}
ind_sh = {bn(r) for r in M if r["source_id"] == IND and r["sha256"] in sh}

print("\nOverlap — both denominators are true")
check("IIIT-ILST acquired images", len(ilst_all), 1390)
check("shared with IndicSTR12 (numerator)", len(ilst_sh), 173)
check("  -> share of ACQUIRED images", f"{100*len(ilst_sh)/len(ilst_all):.1f}%", "12.4%")
check("IIIT-ILST paired records", len(escene), 176)
check("  -> share of PAIRED records", f"{100*len(paired_sh)/len(escene):.1f}%", "98.3%")
check("paired records unique to IIIT-ILST", len(escene) - len(paired_sh), 3)
check("shared set == IndicSTR12's complete Hindi scene set", ind_sh == ind_hindi_scene, True)
check("any cropped word image byte-shared across sources", any("cropped" in f for f in ind_sh), False)

shared_parents = {m.group(1) for r in ilst_sh
                  if (m := re.match(r"IIIT-ILST__Devanagari__(.+)\.(jpg|jpeg|png)$", bn(r)))}
from_shared = sum(1 for c in ecrops
                  if (m := re.match(r"IIIT-ILST__Devanagari__cropped__Devanagari__([^_]+)_", c))
                  and m.group(1) in shared_parents)
print("\nContent-level caveat (hash dedup cannot see this)")
check("IIIT-ILST crops derived from a SHARED photograph", from_shared, 1205)

print("\n" + ("ALL CHECKS PASS" if ok else "SOME CHECKS FAILED"))
sys.exit(0 if ok else 1)
