#!/usr/bin/env python3
"""Verify the composition of the two Devanagari scene-text sources, from files on disk.

Reads nothing from the network and changes nothing.

    python3 resources/scripts/verify_devanagari_composition.py

WHY THIS IS STRICT ABOUT CATEGORIES
A first version of this script counted "crop images" with a filename glob. That glob also
matched two annotation .txt files, so the reported categories summed to more media than had
actually been acquired (IndicSTR12 375+2,713 = 3,088 against 3,086 acquired). The individual
counts were each defensible; nothing checked that they formed a partition.

So the media categories here are defined to be MUTUALLY EXCLUSIVE and EXHAUSTIVE over acquired
media, and that property is asserted mechanically rather than trusted:

    scene photographs + crop images == media files acquired      (exhaustive)
    scene photographs & crop images == empty                     (disjoint)
    every media file lands in exactly one category               (total)

MEDIA CATEGORIES (per source, over media files only — .jpg/.jpeg/.png)
  scene_photograph : a full photograph carrying its own region-level annotation file
  crop_image       : a single-word image cut from a scene photograph, living under the
                     distributor's crop directory

Annotation files are NOT media and are counted separately. That distinction is the whole point.

RESOLVABILITY is reported separately and deliberately is NOT a media category. "How many crops
can be tied to a transcription" is a different question from "how many crop files exist", and
conflating them is what produced the original defect.
"""
import collections, glob, json, os, re, statistics, sys
import xml.etree.ElementTree as ET

RAW = "resources/corpus/raw"
MAN = "resources/manifests/corpus-pilot-v0.jsonl"
IND, ILST = "src_indicstr12_devanagari", "src_iiit_ilst_devanagari"
MEDIA_EXT = {".jpg", ".jpeg", ".png"}
ok = True

def check(label, got, want):
    global ok
    good = got == want
    ok &= good
    print(f"  [{'PASS' if good else 'FAIL'}] {label:<56} {got!r}" + ("" if good else f"   expected {want!r}"))

def media_files(src):
    return {os.path.basename(p) for p in glob.glob(f"{RAW}/{src}/*")
            if os.path.isfile(p) and os.path.splitext(p)[1].lower() in MEDIA_EXT}

def assert_partition(src, acquired, cats):
    """cats: {name: set}. Assert disjoint + exhaustive over `acquired`."""
    print(f"\n{src} — media-category partition")
    total = 0
    for name, s in cats.items():
        print(f"         {name:<22} {len(s):>7,}")
        total += len(s)
    union = set().union(*cats.values()) if cats else set()
    names = list(cats)
    overlaps = {(a, b): cats[a] & cats[b] for i, a in enumerate(names) for b in names[i+1:]}
    worst = max((len(v) for v in overlaps.values()), default=0)
    check("categories are pairwise DISJOINT (0 shared files)", worst, 0)
    check("categories sum to acquired media (EXHAUSTIVE)", total, len(acquired))
    check("union equals acquired media exactly (TOTAL)", union == acquired, True)
    unclassified = acquired - union
    check("media files in no category", len(unclassified), 0)
    if unclassified:
        for f in sorted(unclassified)[:5]: print(f"           unclassified: {f}")
    return union

M = [json.loads(l) for l in open(MAN)]
bn = lambda r: os.path.basename(r["relative_path"])

# ================= IndicSTR12 =================
D = f"{RAW}/{IND}"
ind_media = media_files(IND)
# crop images: media under the distributor's cropped_images/ path
ind_crops = {f for f in ind_media if "__cropped_images__" in f}
# scene photographs: media with their own per-scene *_gt.txt (excluding the crop-level gt file)
ind_scene, ind_regions, bycoord = set(), [], {}
for g in glob.glob(f"{D}/*_gt.txt"):
    m = re.match(r"verified_twice__(hindi|marathi)__(.+)_gt\.txt$", os.path.basename(g))
    if not m or m.group(2) == "cropped_images__word_image":
        continue
    lang, parent = m.groups()
    rows = [p for p in (l.rstrip("\n").split("\t") for l in open(g, encoding="utf-8", errors="replace"))
            if len(p) >= 10]
    if not rows: continue
    for p in rows: bycoord[(lang, parent, tuple(p[1:9]))] = p[9]
    hit = next((f"verified_twice__{lang}__{parent}{e}" for e in (".jpeg", ".jpg", ".png")
                if f"verified_twice__{lang}__{parent}{e}" in ind_media), None)
    if hit: ind_scene.add(hit); ind_regions.append(len(rows))

print("IndicSTR12 — acquired media and annotations")
check("media files acquired (manifest basis)", len(ind_media), 3086)
check("annotation .txt files (NOT media)", len(glob.glob(f"{D}/*.txt")), 378)
assert_partition(IND, ind_media, {"scene_photograph": ind_scene, "crop_image": ind_crops})

print("\nIndicSTR12 — scene annotation shape")
check("scene photographs", len(ind_scene), 375)
check("min regions per photograph", min(ind_regions), 1)
check("max regions per photograph", max(ind_regions), 98)
check("median regions per photograph", statistics.median(ind_regions), 4)
check("total annotated regions", sum(ind_regions), 2711)

# resolvability — reported separately from the media partition
ind_direct = set()
for lang in ("hindi", "marathi"):
    for l in open(f"{D}/verified_twice__{lang}__cropped_images__word_image_gt.txt",
                  encoding="utf-8", errors="replace"):
        p = l.rstrip("\n").split("\t")
        if len(p) >= 2 and p[0].strip():
            ind_direct.add(f"verified_twice__{lang}__cropped_images__{p[0].strip()}")
ind_poly = set()
for c in ind_crops:
    m = re.match(r"verified_twice__(hindi|marathi)__cropped_images__(.+)\.(jpeg|jpg|png)$", c)
    if m:
        pp = m.group(2).split("_")
        if len(pp) >= 10 and (m.group(1), pp[0], tuple(pp[2:10])) in bycoord: ind_poly.add(c)
print("\nIndicSTR12 — crop resolvability (a statistic, NOT a media category)")
check("crop images", len(ind_crops), 2711)
check("route A: direct crop-level word_image_gt.txt", len(ind_crops & ind_direct), 2711)
check("route B: polygon match into the parent scene", len(ind_poly), 2711)
check("resolvable by either route (union)", len(ind_crops & (ind_direct | ind_poly)), 2711)
check("crops resolvable by NEITHER route", len(ind_crops - (ind_direct | ind_poly)), 0)

# ================= IIIT-ILST =================
E = f"{RAW}/{ILST}"
ilst_media = media_files(ILST)
ilst_crops = {f for f in ilst_media if "__cropped__" in f}
ilst_scene, ilst_regions, ebox = set(), [], {}
for x in glob.glob(f"{E}/*.xml"):
    m = re.match(r"IIIT-ILST__Devanagari__(.+)\.xml$", os.path.basename(x))
    if not m: continue
    parent = m.group(1)
    try: root = ET.parse(x).getroot()
    except Exception: continue
    objs = root.findall(".//object")
    for o in objs:
        b = o.find("bndbox"); n = o.find("name")
        if b is None: continue
        ebox[(parent, tuple((b.findtext(k) or "").strip() for k in ("xmin","ymin","xmax","ymax")))] = \
            n.text if n is not None else None
    hit = next((f"IIIT-ILST__Devanagari__{parent}{e}" for e in (".jpg", ".jpeg", ".png")
                if f"IIIT-ILST__Devanagari__{parent}{e}" in ilst_media), None)
    if objs and hit: ilst_scene.add(hit); ilst_regions.append(len(objs))

print("\n\nIIIT-ILST — acquired media and annotations")
check("media files acquired (manifest basis)", len(ilst_media), 1390)
check("annotation .xml files (NOT media)", len(glob.glob(f"{E}/*.xml")), 176)
assert_partition(ILST, ilst_media, {"scene_photograph": ilst_scene, "crop_image": ilst_crops})

print("\nIIIT-ILST — scene annotation shape")
check("scene photographs", len(ilst_scene), 176)
check("max regions per photograph", max(ilst_regions), 64)
check("total annotated regions", sum(ilst_regions), 1788)

ilst_direct = set()
for l in open(f"{E}/IIIT-ILST__Devanagari__cropped__Devanagari__WordImagesList.txt",
              encoding="utf-8", errors="replace"):
    p = l.strip().split(None, 1)
    if len(p) == 2: ilst_direct.add(f"IIIT-ILST__Devanagari__cropped__Devanagari__{p[0]}")
ilst_bbox = set()
for c in ilst_crops:
    m = re.match(r"IIIT-ILST__Devanagari__cropped__Devanagari__(.+)\.(jpg|jpeg|png)$", c)
    if m:
        pp = m.group(1).split("_")
        if len(pp) >= 6 and (pp[0], tuple(pp[2:6])) in ebox: ilst_bbox.add(c)
ilst_res = ilst_crops & (ilst_direct | ilst_bbox)
print("\nIIIT-ILST — crop resolvability (a statistic, NOT a media category)")
check("crop images", len(ilst_crops), 1214)
check("route A: direct WordImagesList.txt", len(ilst_crops & ilst_direct), 1150)
check("route B: bbox match into the parent scene XML", len(ilst_bbox), 1210)
check("resolvable by either route (union)", len(ilst_res), 1213)
check("crops resolvable by NEITHER route", len(ilst_crops - ilst_res), 1)
for f in sorted(ilst_crops - ilst_res):
    print(f"           unresolved crop: {f}")

# ================= corpus-wide roll-up =================
print("\n\nBoth sources — roll-up")
check("total media acquired", len(ind_media) + len(ilst_media), 4476)
check("total scene photographs", len(ind_scene) + len(ilst_scene), 551)
check("total crop images", len(ind_crops) + len(ilst_crops), 3925)
check("scene + crop == total media", len(ind_scene)+len(ilst_scene)+len(ind_crops)+len(ilst_crops), 4476)
check("total crops resolvable to a transcription", len(ind_crops & (ind_direct|ind_poly)) + len(ilst_res), 3924)

# ================= overlap, both denominators =================
byhash = collections.defaultdict(list)
for r in M:
    if r["sha256"]: byhash[r["sha256"]].append(r)
sh = {h for h, v in byhash.items() if len({x["source_id"] for x in v}) > 1}
ilst_all = [r for r in M if r["source_id"] == ILST]
ilst_sh = [r for r in ilst_all if r["sha256"] in sh]
paired_sh = [r for r in ilst_sh if bn(r) in ilst_scene]
ind_sh = {bn(r) for r in M if r["source_id"] == IND and r["sha256"] in sh}
ind_hindi_scene = {s for s in ind_scene if "__hindi__" in s}

print("\nOverlap — both denominators are true")
check("IIIT-ILST acquired images", len(ilst_all), 1390)
check("shared with IndicSTR12 (numerator)", len(ilst_sh), 173)
check("  -> share of ACQUIRED images", f"{100*len(ilst_sh)/len(ilst_all):.1f}%", "12.4%")
check("IIIT-ILST scene photographs", len(ilst_scene), 176)
check("  -> share of SCENE PHOTOGRAPHS", f"{100*len(paired_sh)/len(ilst_scene):.1f}%", "98.3%")
check("scene photographs unique to IIIT-ILST", len(ilst_scene) - len(paired_sh), 3)
check("shared set == IndicSTR12's complete Hindi scene set", ind_sh == ind_hindi_scene, True)
check("any crop image byte-shared across sources", bool(ind_sh & ind_crops) or bool({bn(r) for r in ilst_sh} & ilst_crops), False)

shared_parents = {m.group(1) for r in ilst_sh
                  if (m := re.match(r"IIIT-ILST__Devanagari__(.+)\.(jpg|jpeg|png)$", bn(r)))}
from_shared = sum(1 for c in ilst_crops
                  if (m := re.match(r"IIIT-ILST__Devanagari__cropped__Devanagari__([^_]+)_", c))
                  and m.group(1) in shared_parents)
print("\nContent-level caveat (hash dedup cannot see this)")
check("IIIT-ILST crops cut from a SHARED photograph", from_shared, 1205)

print("\n" + ("ALL CHECKS PASS" if ok else "SOME CHECKS FAILED"))
sys.exit(0 if ok else 1)
