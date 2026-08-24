#!/usr/bin/env python3
"""
EVAL-003 · Deterministic candidate-pool builder for Devanagari checker calibration.

WHAT THIS DOES
    Selects a small pool of real photographed Devanagari word regions from the CVIT lineage
    (IndicSTR12 + IIIT-ILST) so a Hindi first-language reader can later establish what they
    actually say, and candidate checkers can then be tested against those readings.

WHAT THIS IS NOT
    Not a benchmark. Not ground truth. Not a capability measurement. The source-provided
    transcriptions carried here are ONE ANNOTATION TEAM'S OBSERVATIONS and this pipeline
    never promotes them to project truth.

GUARANTEES
    * Deterministic: same repository state + same seed => byte-identical manifest.
    * BSTD is never opened. It is the unseen cross-source reserve.
    * Files byte-identical across the two CVIT sources are excluded from the pool entirely,
      so one photograph cannot enter twice under two dataset names.
    * Duplicate copies inside one source collapse to one candidate.
    * Devanagari is detected by SCRIPT IN THE TRANSCRIPTION, never by language label.
    * No network call. No model call. No image is modified or rewritten.

Usage:
    python3 build-candidate-pool.py [--corpus-root PATH] [--out-dir PATH]
                                    [--target-n 54] [--seed 20260824]
"""
import argparse, csv, hashlib, json, os, re, sys, unicodedata
from pathlib import Path

# ---------------------------------------------------------------------------
# Fixed vocabulary and rules. Changing any of these changes what the pool means.
# ---------------------------------------------------------------------------
DEVANAGARI = (0x0900, 0x097F)          # Unicode block
VIRAMA, NUKTA, ANUSVARA, CHANDRABINDU = "्", "़", "ं", "ँ"
MATRAS = set("ािीुूृॄेैोौ")
# Nukta appears two ways in Unicode: as the combining mark U+093C, or baked into a precomposed
# codepoint (क़ ख़ ग़ ज़ ड़ ढ़ फ़ य़ = U+0958..U+095F). Checking only the combining mark undercounts.
PRECOMPOSED_NUKTA = set(chr(c) for c in range(0x0958, 0x0960))
def has_nukta(s: str) -> bool:
    return (NUKTA in s) or any(c in PRECOMPOSED_NUKTA for c in s) \
        or any(NUKTA in unicodedata.normalize("NFD", c) for c in s)

CVIT_SOURCES = ("src_indicstr12_devanagari", "src_iiit_ilst_devanagari")
RESERVED_UNSEEN = ("src_bstd_devanagari",)   # never opened by this script

def has_devanagari(s: str) -> bool:
    return any(DEVANAGARI[0] <= ord(c) <= DEVANAGARI[1] for c in s)

def nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s).strip()

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

# ---------------------------------------------------------------------------
# Loaders — one per source annotation format
# ---------------------------------------------------------------------------
def load_indicstr12(root: Path):
    """IndicSTR12: per-image `<name>_gt.txt`, tab-separated: idx x1 y1 x2 y2 x3 y3 x4 y4 text."""
    d = root / CVIT_SOURCES[0]
    out = {}
    if not d.is_dir():
        return out
    for gt in sorted(d.glob("*_gt.txt")):
        img = d / (gt.name[:-len("_gt.txt")] + ".jpeg")
        if not img.exists():
            continue
        regions = []
        for line in gt.read_text(encoding="utf-8", errors="replace").splitlines():
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 10:
                continue
            try:
                xs = [int(parts[i]) for i in (1, 3, 5, 7)]
                ys = [int(parts[i]) for i in (2, 4, 6, 8)]
            except ValueError:
                continue
            regions.append({"text": nfc(parts[9]),
                            "box": [min(xs), min(ys), max(xs), max(ys)]})
        if regions:
            out[img] = regions
    return out

def load_iiit_ilst(root: Path):
    """IIIT-ILST: per-image `.xml`, PASCAL-VOC style <object><name>text</name><bndbox>."""
    d = root / CVIT_SOURCES[1]
    out = {}
    if not d.is_dir():
        return out
    for xml in sorted(d.glob("*.xml")):
        img = d / (xml.stem + ".jpg")
        if not img.exists():
            continue
        t = xml.read_text(encoding="utf-8", errors="replace")
        regions = []
        for m in re.finditer(r"<object>(.*?)</object>", t, re.S):
            o = m.group(1)
            name = re.search(r"<name>(.*?)</name>", o, re.S)
            bb = {k: re.search(rf"<{k}>(-?\d+)</{k}>", o) for k in ("xmin", "ymin", "xmax", "ymax")}
            if name and all(bb.values()):
                regions.append({"text": nfc(name.group(1)),
                                "box": [int(bb[k].group(1)) for k in ("xmin", "ymin", "xmax", "ymax")]})
        if regions:
            out[img] = regions
    return out

# ---------------------------------------------------------------------------
# Deterministic feature derivation — metadata and geometry only.
# Nothing here requires a Hindi judgement or an AI judgement.
# ---------------------------------------------------------------------------
def region_features(text, box, img_w, img_h, n_regions_in_image):
    x0, y0, x1, y1 = box
    w, h = max(0, x1 - x0), max(0, y1 - y0)
    area = w * h
    img_area = (img_w * img_h) if (img_w and img_h) else None
    chars = [c for c in text if has_devanagari(c)]
    return {
        "crop_w": w, "crop_h": h, "crop_area_px": area,
        "crop_aspect": round(w / h, 3) if h else None,
        "crop_fraction_of_image": round(area / img_area, 5) if img_area else None,
        "regions_in_source_image": n_regions_in_image,
        "transcription_char_len": len(text),
        "devanagari_char_count": len(chars),
        "contains_conjunct_virama": VIRAMA in text,
        "contains_nukta": has_nukta(text),
        "contains_matra": any(c in MATRAS for c in text),
        "contains_anusvara_or_chandrabindu": (ANUSVARA in text) or (CHANDRABINDU in text),
        # Deterministic in principle, NOT COMPUTED here: no image library (Pillow/numpy) is
        # available in this environment, so per-pixel blur/contrast was not measured. Recorded
        # as null with a reason rather than guessed — see README §"What we could not measure".
        "blur_estimate": None,
        "contrast_estimate": None,
        "pixel_metrics_state": "not_computed_no_image_library",
    }

def size_bucket(area):
    if area is None:            return "unknown"
    if area < 2_000:            return "tiny"
    if area < 10_000:           return "small"
    if area < 50_000:           return "medium"
    return "large"

def clutter_bucket(n):
    if n <= 2:   return "isolated"
    if n <= 8:   return "moderate"
    return "cluttered"

# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    here = Path(__file__).resolve().parent
    repo = here.parents[2]
    ap.add_argument("--corpus-root", default=None,
                    help="Directory containing src_* corpus folders. Default: <repo>/resources/corpus/raw. "
                         "The raw corpus is git-ignored and may live in another worktree; point this at it.")
    ap.add_argument("--out-dir", default=str(here))
    ap.add_argument("--res-manifest", default=None,
                    help="Resources item manifest, used only to fill image width/height by sha256. "
                         "Default: <repo>/resources/manifests/corpus-pilot-v0.jsonl")
    ap.add_argument("--target-n", type=int, default=54, help="candidates to select (task range 45-60)")
    ap.add_argument("--seed", type=int, default=20260824, help="recorded for provenance; selection is sort-based, not RNG-based")
    args = ap.parse_args()

    corpus = Path(args.corpus_root) if args.corpus_root else (repo / "resources" / "corpus" / "raw")
    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    res_manifest = Path(args.res_manifest) if args.res_manifest else (
        repo / "resources" / "manifests" / "corpus-pilot-v0.jsonl")

    # Image dimensions by sha256, taken from the Resources manifest (repo-local, already
    # validated by RES-001). Used only to compute how much of the frame a region occupies.
    dims_by_sha = {}
    if res_manifest.exists():
        for line in res_manifest.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if r.get("sha256") and r.get("width") and r.get("height"):
                dims_by_sha.setdefault(r["sha256"], (r["width"], r["height"]))

    if not corpus.is_dir():
        sys.exit(f"ERROR: corpus root not found: {corpus}\n"
                 f"Raw media is git-ignored. Pass --corpus-root explicitly.")

    # --- integrity attestation for the reserve, WITHOUT opening any BSTD image -------------
    reserve = {}
    for s in RESERVED_UNSEEN:
        d = corpus / s
        reserve[s] = {
            "present": d.is_dir(),
            "file_count": sum(1 for _ in d.rglob("*") if _.is_file()) if d.is_dir() else 0,
            "opened_by_this_script": False,
            "note": "Counted by directory traversal only. No file was read, decoded, inspected "
                    "or selected. Preserved as the unseen cross-source lineage reserve.",
        }

    # --- load CVIT labels ------------------------------------------------------------------
    ind = load_indicstr12(corpus)
    ilst = load_iiit_ilst(corpus)
    if not ind and not ilst:
        sys.exit("ERROR: no labelled CVIT images found. Check --corpus-root.")

    per_source = {CVIT_SOURCES[0]: ind, CVIT_SOURCES[1]: ilst}

    # --- hash every labelled image ---------------------------------------------------------
    hashes = {}   # path -> sha
    for regs in per_source.values():
        for p in regs:
            hashes[p] = sha256_file(p)

    by_source_shas = {s: {hashes[p] for p in regs} for s, regs in per_source.items()}
    cross_overlap = by_source_shas[CVIT_SOURCES[0]] & by_source_shas[CVIT_SOURCES[1]]

    # --- build candidates ------------------------------------------------------------------
    seen_sha, candidates, within_source_dupes = set(), [], []
    for source in CVIT_SOURCES:                       # stable source order
        for img in sorted(per_source[source]):        # stable path order
            sha = hashes[img]
            if sha in cross_overlap:
                continue                              # RULE 1: excluded entirely
            if sha in seen_sha:
                within_source_dupes.append({"source_id": source, "path": str(img), "sha256": sha})
                continue                              # RULE 2: one candidate per distinct file
            seen_sha.add(sha)

            regions = per_source[source][img]
            dev = [r for r in regions if has_devanagari(r["text"])]   # RULE 3: script, not language
            if not dev:
                continue

            # RULE 4: one region per file, chosen deterministically — largest area, then
            # top-left-most, then lexicographic. No visual judgement is exercised.
            def key(r):
                x0, y0, x1, y1 = r["box"]
                return (-( (x1-x0) * (y1-y0) ), y0, x0, r["text"])
            chosen = sorted(dev, key=key)[0]

            # Dimensions: Resources manifest first (validated, covers both sources), then the
            # source annotation as a fallback. Null if neither supplies them — never guessed.
            iw, ih = dims_by_sha.get(sha, (None, None))
            if iw is None and source == CVIT_SOURCES[1]:
                try:
                    t = (img.with_suffix(".xml")).read_text(encoding="utf-8", errors="replace")
                    mw, mh = re.search(r"<width>(\d+)</width>", t), re.search(r"<height>(\d+)</height>", t)
                    if mw and mh: iw, ih = int(mw.group(1)), int(mh.group(1))
                except Exception:
                    pass

            f = region_features(chosen["text"], chosen["box"], iw, ih, len(regions))
            candidates.append({
                "candidate_id": f"dev-v0-{sha[:12]}",
                "source_id": source,
                "source_lineage": "CVIT/IIIT-Hyderabad",
                "source_image_relpath": str(img.relative_to(corpus)),
                "source_image_sha256": sha,
                "crop_box_xyxy": chosen["box"],
                "source_image_width": iw, "source_image_height": ih,
                # PROVENANCE ONLY. Hidden from the reviewer's first pass. Never ground truth.
                "source_provided_transcription": chosen["text"],
                "source_transcription_status": "source_observation_not_project_ground_truth",
                "all_source_regions_in_image": len(regions),
                "strata": {"size": size_bucket(f["crop_area_px"]),
                           "clutter": clutter_bucket(len(regions))},
                "features": f,
            })

    # --- deterministic stratified selection -------------------------------------------------
    # Round-robin across (size, clutter) strata, taking candidates in sha order within each,
    # so the pool spans visual conditions instead of 54 near-identical easy crops.
    strata = {}
    for c in candidates:
        strata.setdefault((c["strata"]["size"], c["strata"]["clutter"]), []).append(c)
    for k in strata:
        strata[k].sort(key=lambda c: c["source_image_sha256"])
    order = sorted(strata)
    selected, i = [], 0
    while len(selected) < min(args.target_n, len(candidates)):
        progressed = False
        for k in order:
            if i < len(strata[k]):
                selected.append(strata[k][i]); progressed = True
                if len(selected) >= args.target_n: break
        if not progressed: break
        i += 1
    for rank, c in enumerate(selected, 1):
        c["selection_rank"] = rank

    # --- cross-source annotator disagreement (evidence, NOT candidates) ---------------------
    def iou(a, b):
        ix = max(0, min(a[2], b[2]) - max(a[0], b[0])); iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
        inter = ix * iy
        u = (a[2]-a[0])*(a[3]-a[1]) + (b[2]-b[0])*(b[3]-b[1]) - inter
        return inter / u if u > 0 else 0.0
    rev = {hashes[p]: p for p in ilst}
    matched = agree = 0; disagreements = []
    strip = lambda s: "".join(c for c in s if c not in (VIRAMA, NUKTA, ANUSVARA, CHANDRABINDU))
    for p in sorted(ind):
        sha = hashes[p]
        if sha not in cross_overlap: continue
        q = rev[sha]
        for ra in ind[p]:
            best, bi = None, 0.0
            for rb in ilst[q]:
                v = iou(ra["box"], rb["box"])
                if v > bi: bi, best = v, rb
            if bi >= 0.5 and best is not None:
                matched += 1
                if ra["text"] == best["text"]:
                    agree += 1
                else:
                    disagreements.append({
                        "sha256": sha, "iou": round(bi, 3), "box": ra["box"],
                        "indicstr12_text": ra["text"], "iiit_ilst_text": best["text"],
                        "convention_only": strip(ra["text"]) == strip(best["text"]),
                    })

    # --- write outputs ----------------------------------------------------------------------
    (out / "candidate-manifest.jsonl").write_text(
        "".join(json.dumps(c, ensure_ascii=False) + "\n" for c in selected), encoding="utf-8")

    cols = ["selection_rank","candidate_id","source_id","source_image_relpath","source_image_sha256",
            "crop_box_xyxy","crop_w","crop_h","crop_area_px","regions_in_source_image",
            "size_stratum","clutter_stratum","transcription_char_len","contains_conjunct_virama",
            "contains_nukta","contains_matra"]
    with open(out / "candidate-manifest.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(cols)
        for c in selected:
            f = c["features"]
            w.writerow([c["selection_rank"], c["candidate_id"], c["source_id"], c["source_image_relpath"],
                        c["source_image_sha256"], json.dumps(c["crop_box_xyxy"]), f["crop_w"], f["crop_h"],
                        f["crop_area_px"], f["regions_in_source_image"], c["strata"]["size"],
                        c["strata"]["clutter"], f["transcription_char_len"], f["contains_conjunct_virama"],
                        f["contains_nukta"], f["contains_matra"]])
    # NOTE: the CSV deliberately omits source_provided_transcription so it can be opened
    # alongside review work without leaking an expected answer.

    conv = sum(1 for d in disagreements if d["convention_only"])
    report = {
        "generated_by": "eval/calibration/devanagari-v0/build-candidate-pool.py",
        "SYNTHETIC": False,
        "IS_GROUND_TRUTH": False,
        "note": "Cross-source annotator disagreement measured on files that are byte-identical "
                "across the two CVIT datasets. These files are EXCLUDED from the candidate pool. "
                "This is evidence about label reliability, not a candidate set.",
        "byte_identical_files": len(cross_overlap),
        "regions_matched_iou_ge_0.5": matched,
        "identical_transcription": agree,
        "different_transcription": len(disagreements),
        "agreement_rate": round(agree / matched, 4) if matched else None,
        "of_disagreements_convention_only": conv,
        "of_disagreements_substantive": len(disagreements) - conv,
        "convention_only_definition": "identical after removing virama, nukta, anusvara and "
                                      "chandrabindu — same letters, different conjunct/diacritic convention",
        "examples": disagreements[:25],
    }
    (out / "annotator-disagreement.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    summary = {
        "task": "EVAL-003",
        "seed": args.seed,
        "determinism": "selection is by stable sort on sha256 within strata; no RNG is used",
        "corpus_root_used": str(corpus),
        "res_manifest_used": str(res_manifest) if res_manifest.exists() else None,
        "reserve_untouched": reserve,
        "labelled_images_found": {s: len(r) for s, r in per_source.items()},
        "cross_source_byte_identical_excluded": len(cross_overlap),
        "within_source_duplicates_collapsed": len(within_source_dupes),
        "eligible_candidates_after_exclusions": len(candidates),
        "selected": len(selected),
        "strata_available": {f"{k[0]}/{k[1]}": len(v) for k, v in sorted(strata.items())},
        "strata_selected": {},
    }
    for c in selected:
        k = f'{c["strata"]["size"]}/{c["strata"]["clutter"]}'
        summary["strata_selected"][k] = summary["strata_selected"].get(k, 0) + 1
    (out / "selection-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"labelled images        : {summary['labelled_images_found']}")
    print(f"cross-source excluded  : {len(cross_overlap)} byte-identical files")
    print(f"within-source dupes    : {len(within_source_dupes)}")
    print(f"eligible candidates    : {len(candidates)}")
    print(f"selected               : {len(selected)}")
    print(f"strata selected        : {summary['strata_selected']}")
    print(f"reserve untouched      : {reserve}")
    print(f"annotator agreement    : {agree}/{matched} = {report['agreement_rate']}")
    print(f"wrote -> {out}")

if __name__ == "__main__":
    main()
