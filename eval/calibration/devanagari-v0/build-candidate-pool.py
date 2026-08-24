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

def source_language_label(path: Path, source_id: str) -> str:
    """
    The distributor's LANGUAGE label, recorded separately from script.

    Script and language are different things, and this project has already been bitten by
    conflating them: Marathi is written in Devanagari, so a language filter would have discarded
    ~5,100 target-script images. Selection uses SCRIPT. This exists only so the language
    composition of the pool can be reported honestly.
    """
    if source_id == CVIT_SOURCES[0]:          # verified_twice__<language>__NNN.jpeg
        parts = path.stem.split("__")
        return parts[1] if len(parts) >= 3 and parts[1] else "unknown"
    if source_id == CVIT_SOURCES[1]:          # IIIT-ILST__Devanagari__NNN — a script, not a language
        return "unstated_script_labelled_only"
    return "unknown"

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

# ---------------------------------------------------------------------------
# Region matching — lifted out of main() so it can be tested directly.
# ---------------------------------------------------------------------------
def iou(a, b):
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0])); iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    u = (a[2]-a[0])*(a[3]-a[1]) + (b[2]-b[0])*(b[3]-b[1]) - inter
    return inter / u if u > 0 else 0.0

def match_regions_one_to_one(A, B, threshold):
    """
    Strict one-to-one region matching.

    All candidate pairs at or above `threshold` are sorted by descending IoU and accepted
    greedily; once a region on either side has been used it cannot be matched again. Ties break
    on (i, j) so the result is deterministic.

    Returns [(i, j, iou)].

    The exclusivity is the whole point: without it a single region on one side can be counted
    against several regions on the other, inflating both the match count and the apparent
    agreement. See --self-test for the adversarial case.
    """
    pairs = []
    for i, ra in enumerate(A):
        for j, rb in enumerate(B):
            v = iou(ra["box"], rb["box"])
            if v >= threshold:
                pairs.append((-v, i, j))
    pairs.sort()
    usedA, usedB, out = set(), set(), []
    for negv, i, j in pairs:
        if i in usedA or j in usedB:
            continue
        usedA.add(i); usedB.add(j)
        out.append((i, j, -negv))
    return out

def match_regions_superseded(A, B, threshold):
    """
    The superseded method: a partner chosen independently for each A-region with NO exclusivity.
    Retained and exercised so the correction stays visible and the regression has something to
    compare against. Returns [(i, j, iou)].
    """
    out = []
    for i, ra in enumerate(A):
        best, bi = None, 0.0
        for j, rb in enumerate(B):
            v = iou(ra["box"], rb["box"])
            if v > bi:
                bi, best = v, j
        if bi >= threshold and best is not None:
            out.append((i, best, bi))
    return out

def count_contested_partners(A, B, threshold):
    """How many B-regions are within `threshold` of more than one A-region.

    This is the quantity that determines whether the superseded method could have double-counted
    on a given corpus. Computed rather than asserted, so any figure quoted in the findings is
    reproducible from committed code."""
    n = 0
    for rb in B:
        if sum(1 for ra in A if iou(ra["box"], rb["box"]) >= threshold) > 1:
            n += 1
    return n

def _self_test(verbose=True):
    """Adversarial regression for the matching rule.

    Deliberately constructs the case the real corpus does NOT contain: two A-regions that both
    exceed the threshold against, and prefer, the SAME B-region. A rule without exclusivity
    matches both; the corrected rule must use that B-region at most once.
    """
    ok = True
    def check(name, cond, detail=""):
        nonlocal ok
        ok &= bool(cond)
        if verbose:
            print(f"  {'PASS' if cond else 'FAIL'}  {name}{('  ' + detail) if detail else ''}")

    T = 0.5
    # --- Case 1: two A-regions contend for one B-region ---------------------------------------
    A = [{"box": (0, 0, 100, 100), "text": "a1"}, {"box": (5, 5, 105, 105), "text": "a2"}]
    B = [{"box": (2, 2, 102, 102), "text": "b1"}]
    sup, one = match_regions_superseded(A, B, T), match_regions_one_to_one(A, B, T)
    check("two A-regions contend for one B-region: superseded matches both",
          len(sup) == 2, f"(got {len(sup)})")
    check("...corrected rule uses that B-region at most once",
          len(one) == 1 and len({j for _, j, _ in one}) == 1, f"(got {len(one)})")
    check("...and the contested-partner counter sees it",
          count_contested_partners(A, B, T) == 1)

    # --- Case 2: the higher-IoU contender wins, deterministically ------------------------------
    A2 = [{"box": (0, 0, 100, 100), "text": "far"}, {"box": (1, 1, 101, 101), "text": "near"}]
    B2 = [{"box": (1, 1, 101, 101), "text": "target"}]
    m = match_regions_one_to_one(A2, B2, T)
    check("the closer of two contenders is the one matched",
          len(m) == 1 and m[0][0] == 1 and abs(m[0][2] - 1.0) < 1e-9)

    # --- Case 3: three A vs two B — at most min(|A|,|B|) matches -------------------------------
    A3 = [{"box": (0, 0, 50, 50)}, {"box": (1, 1, 51, 51)}, {"box": (2, 2, 52, 52)}]
    B3 = [{"box": (0, 0, 50, 50)}, {"box": (200, 200, 250, 250)}]
    m3 = match_regions_one_to_one(A3, B3, T)
    check("matches never exceed min(len(A), len(B))", len(m3) <= 2, f"(got {len(m3)})")
    check("no B-region reused", len({j for _, j, _ in m3}) == len(m3))
    check("no A-region reused", len({i for i, _, _ in m3}) == len(m3))

    # --- Case 4: below threshold matches nothing; symmetry sanity -------------------------------
    A4 = [{"box": (0, 0, 10, 10)}]
    B4 = [{"box": (9, 9, 19, 19)}]
    check("pairs below threshold are not matched", match_regions_one_to_one(A4, B4, T) == [])
    check("identical inputs match fully",
          len(match_regions_one_to_one(A3, A3, T)) == len(A3))

    # --- Case 5: determinism ---------------------------------------------------------------
    check("repeated calls are identical",
          match_regions_one_to_one(A3, B3, T) == match_regions_one_to_one(A3, B3, T))
    return ok

def _portable(p, repo: Path) -> str:
    """Render a path relative to the repo root so nothing machine-specific is committed. The raw
    corpus is git-ignored and sits wherever a given checkout puts it."""
    try:
        return str(Path(p).resolve().relative_to(repo.resolve()))
    except ValueError:
        return f"<external>/{Path(p).name}"

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
    ap.add_argument("--self-test", action="store_true",
                    help="run the adversarial matching regression and exit; touches no corpus")
    ap.add_argument("--language-filter", default=None,
                    help="restrict candidates to this distributor language label (e.g. 'hindi'). "
                         "Devanagari is still identified by SCRIPT; this filter is applied on top, "
                         "and is how the Controller-approved Hindi-primary V0 pack is built.")
    ap.add_argument("--overlap-policy", choices=("exclude", "admit-once"), default="exclude",
                    help="What to do with photographs present in BOTH CVIT datasets. "
                         "'exclude' (default, EVAL-003 as written): drop them entirely. "
                         "'admit-once': admit each shared photograph ONCE, attributed to the "
                         "first source in fixed order, so one photograph is still one item. "
                         "This matters because 100%% of Hindi-labelled material sits in the "
                         "overlap: under 'exclude' the pool is entirely Marathi. PROPOSAL ONLY "
                         "— do not switch the default without Controller approval.")
    ap.add_argument("--seed", type=int, default=20260824, help="recorded for provenance; selection is sort-based, not RNG-based")
    args = ap.parse_args()

    if args.self_test:
        print("Adversarial regression for one-to-one region matching:")
        ok = _self_test()
        print("SELF-TEST OK — exclusivity is enforced." if ok else "SELF-TEST FAILED.")
        raise SystemExit(0 if ok else 1)

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
    admitted_overlap = 0
    language_filtered_out = 0
    for source in CVIT_SOURCES:                       # stable source order
        for img in sorted(per_source[source]):        # stable path order
            sha = hashes[img]
            if sha in cross_overlap:
                # RULE 1. Default: excluded entirely, per EVAL-003 as written.
                # Under 'admit-once' the photograph is admitted a single time — the first
                # source in fixed order wins — so one photograph is still exactly one item and
                # independence is preserved. What is lost either way is any pretence that the
                # two datasets provide independent evidence about it.
                if args.overlap_policy == "exclude":
                    continue
                if sha in seen_sha:
                    continue
                admitted_overlap += 1
            if sha in seen_sha:
                within_source_dupes.append({"source_id": source, "path": str(img), "sha256": sha})
                continue                              # RULE 2: one candidate per distinct file
            seen_sha.add(sha)

            # RULE 3: script, not language. The language filter below is an ADDITIONAL
            # restriction for the Hindi-primary pack, never a substitute for the script test.
            lang = source_language_label(img, source)
            if args.language_filter and lang != args.language_filter:
                language_filtered_out += 1
                continue
            regions = per_source[source][img]
            dev = [r for r in regions if has_devanagari(r["text"])]
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
                "source_language_label": lang,
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
    if len(selected) < args.target_n:
        print(f"\nSHORTFALL: asked for {args.target_n} candidates, only {len(selected)} available.")
        print(f"  eligible pool          : {len(candidates)}")
        print(f"  language filter        : {args.language_filter or '(none)'}")
        print(f"  eligible language mix  : "
              f"{ {c['source_language_label']: sum(1 for x in candidates if x['source_language_label']==c['source_language_label']) for c in candidates} }")
        print("  Reporting the shortfall rather than substituting another language.")
        raise SystemExit(3)

    for rank, c in enumerate(selected, 1):
        c["selection_rank"] = rank

    # --- cross-dataset annotation disagreement (evidence, NOT candidates) -------------------
    #
    # SCOPE, stated precisely. This compares the transcriptions that TWO RELEASES FROM THE SAME
    # SOURCE LINEAGE (CVIT / IIIT Hyderabad) attach to byte-identical photographs. The repository
    # holds no provenance showing the two annotation sets were produced by independent annotators.
    # It is therefore CROSS-DATASET ANNOTATION DISAGREEMENT. It is NOT human inter-annotator
    # agreement, NOT a measure of human reading ability, and MUST NOT be used to set an evaluator
    # threshold.
    IOU_THRESHOLD = 0.5
    rev = {hashes[p]: p for p in ilst}

    # Deleting these marks is a MECHANICAL Unicode operation. It does NOT establish that two
    # strings are linguistically or orthographically equivalent — that needs native-language
    # evidence this project does not have. The field name says only what was done.
    REMOVED_MARKS = {"virama": VIRAMA, "nukta": NUKTA,
                     "anusvara": ANUSVARA, "chandrabindu": CHANDRABINDU}
    strip = lambda s: "".join(c for c in s if c not in REMOVED_MARKS.values())

    matched_1to1 = agree_1to1 = 0
    matched_greedy = agree_greedy = 0        # superseded method, recomputed for comparison
    contested_b_regions = 0                  # where the superseded method COULD have double-counted
    total_b_regions = 0
    disagreements = []
    for p in sorted(ind):
        sha = hashes[p]
        if sha not in cross_overlap: continue
        A, B = ind[p], ilst[rev[sha]]

        total_b_regions += len(B)
        contested_b_regions += count_contested_partners(A, B, IOU_THRESHOLD)

        for i, j, v in match_regions_superseded(A, B, IOU_THRESHOLD):
            matched_greedy += 1
            if A[i]["text"] == B[j]["text"]: agree_greedy += 1

        for i, j, v in match_regions_one_to_one(A, B, IOU_THRESHOLD):
            ra, rb = A[i], B[j]
            matched_1to1 += 1
            if ra["text"] == rb["text"]:
                agree_1to1 += 1
            else:
                disagreements.append({
                    "sha256": sha, "iou": round(v, 3), "box": ra["box"],
                    "indicstr12_text": ra["text"], "iiit_ilst_text": rb["text"],
                    "matches_after_selected_diacritic_removal": strip(ra["text"]) == strip(rb["text"]),
                })

    # --- write outputs ----------------------------------------------------------------------
    (out / "candidate-manifest.jsonl").write_text(
        "".join(json.dumps(c, ensure_ascii=False) + "\n" for c in selected), encoding="utf-8")

    cols = ["selection_rank","candidate_id","source_id","source_language_label",
            "source_image_relpath","source_image_sha256","crop_box_xyxy","crop_w","crop_h",
            "crop_area_px","regions_in_source_image","size_stratum","clutter_stratum",
            "transcription_char_len","contains_conjunct_virama","contains_nukta","contains_matra"]
    with open(out / "candidate-manifest.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh); w.writerow(cols)
        for c in selected:
            f = c["features"]
            w.writerow([c["selection_rank"], c["candidate_id"], c["source_id"],
                        c["source_language_label"], c["source_image_relpath"],
                        c["source_image_sha256"], json.dumps(c["crop_box_xyxy"]), f["crop_w"],
                        f["crop_h"], f["crop_area_px"], f["regions_in_source_image"],
                        c["strata"]["size"], c["strata"]["clutter"], f["transcription_char_len"],
                        f["contains_conjunct_virama"], f["contains_nukta"], f["contains_matra"]])
    # The CSV deliberately omits source_provided_transcription so it can be opened alongside
    # review work without leaking an expected answer.

    conv = sum(1 for d in disagreements if d["matches_after_selected_diacritic_removal"])
    report = {
        "generated_by": "eval/calibration/devanagari-v0/build-candidate-pool.py",
        "IS_GROUND_TRUTH": False,
        "what_this_measures":
            "Disagreement between the transcriptions that two releases from the SAME source "
            "lineage (CVIT / IIIT Hyderabad) attach to byte-identical photographs.",
        "what_this_does_NOT_measure": [
            "human inter-annotator agreement — no provenance in this repository shows the two "
            "annotation sets were produced by independent annotators",
            "human reading ability, or any ceiling on it",
            "anything that may legitimately be used to set an evaluator threshold",
        ],
        "supported_conclusion":
            "Source annotations are demonstrably unsafe to promote directly to project ground "
            "truth: two releases from one lineage assign different transcriptions to the same "
            "pixels often enough that adopting either arbitrarily would embed unexamined error.",
        "note": "These files are EXCLUDED from the candidate pool. Evidence about label "
                "reliability, not a candidate set.",
        "byte_identical_files": len(cross_overlap),
        "iou_threshold": IOU_THRESHOLD,
        "matching_method": "strict one-to-one: pairs at IoU >= threshold sorted by descending IoU "
                           "and accepted greedily; each region on either side matches at most once",
        "regions_matched": matched_1to1,
        "identical_transcription": agree_1to1,
        "different_transcription": len(disagreements),
        "agreement_rate": round(agree_1to1 / matched_1to1, 4) if matched_1to1 else None,
        "contested_partner_audit": {
            "definition": "B-regions within the IoU threshold of MORE THAN ONE A-region — the only "
                          "situation in which the superseded method could have double-counted.",
            "b_regions_examined": total_b_regions,
            "contested": contested_b_regions,
            "why_totals_matched": "With zero contested partners the superseded and corrected "
                                  "methods cannot differ on this corpus. That is a property of "
                                  "this data, NOT evidence that the superseded rule was sound. "
                                  "The adversarial regression in --self-test covers the case this "
                                  "corpus does not contain.",
        },
        "superseded_method": {
            "description": "EVAL-003 first pass: best partner chosen per IndicSTR12 region with "
                           "NO exclusivity, so one IIIT-ILST region could be counted against "
                           "several. Retained so the correction is visible.",
            "regions_matched": matched_greedy,
            "identical_transcription": agree_greedy,
            "agreement_rate": round(agree_greedy / matched_greedy, 4) if matched_greedy else None,
        },
        "diacritic_removal_probe": {
            "field": "matches_after_selected_diacritic_removal",
            "marks_removed": {k: "U+%04X" % ord(v) for k, v in REMOVED_MARKS.items()},
            "count_true": conv,
            "count_false": len(disagreements) - conv,
            "meaning": "TRUE means the two strings become identical once those four marks are "
                       "deleted from both. A mechanical Unicode result only.",
            "explicitly_not_claimed": "This does NOT establish that such pairs are semantically or "
                                      "orthographically equivalent, nor that they represent the "
                                      "same reading. That requires native-language evidence which "
                                      "this project does not have.",
        },
        "examples": disagreements[:25],
    }
    (out / "annotator-disagreement.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    total_labelled_records = sum(len(r) for r in per_source.values())
    records_removed_by_overlap = sum(1 for src in CVIT_SOURCES for pth in per_source[src]
                                     if hashes[pth] in cross_overlap)
    lang = {}
    for c in selected:
        lang[c["source_language_label"]] = lang.get(c["source_language_label"], 0) + 1

    summary = {
        "task": "EVAL-003",
        "seed": args.seed,
        "determinism": "selection is by stable sort on sha256 within strata; no RNG is used",
        # Repo-relative, never absolute: the raw corpus is git-ignored and lives wherever a
        # given checkout puts it, so an absolute path would be meaningless elsewhere.
        "corpus_root_used": _portable(corpus, repo),
        "res_manifest_used": _portable(res_manifest, repo) if res_manifest.exists() else None,
        "reserve_untouched": reserve,
        "labelled_images_found": {s: len(r) for s, r in per_source.items()},

        # Reported as RECORDS, not hashes: each shared hash removes a record from BOTH datasets,
        # so "551 - 173 - 3 = 202" would be wrong arithmetic even though it lands on the right
        # number by coincidence of the data.
        "exclusion_arithmetic": {
            "policy": args.overlap_policy,
            "labelled_source_records": total_labelled_records,
            "cross_source_shared_hashes": len(cross_overlap),
            "records_removed_by_overlap_policy": (
                records_removed_by_overlap if args.overlap_policy == "exclude"
                else records_removed_by_overlap - len(cross_overlap)),
            "records_removed_explanation": (
                "both copies of every shared hash are excluded, so each shared hash removes TWO "
                "source records" if args.overlap_policy == "exclude" else
                "the shared photograph is admitted once, so each shared hash removes only the "
                "second copy — ONE source record"),
            "same_source_duplicate_records_removed": len(within_source_dupes),
            "language_filter": args.language_filter,
            "records_removed_by_language_filter": language_filtered_out,
            "eligible_unique_photographs": len(candidates),
            "check": (
                f"{total_labelled_records}"
                f" - {records_removed_by_overlap if args.overlap_policy == 'exclude' else records_removed_by_overlap - len(cross_overlap)} (overlap policy '{args.overlap_policy}')"
                f" - {len(within_source_dupes)} (same-source dupes)"
                + (f" - {language_filtered_out} (language filter '{args.language_filter}')" if args.language_filter else "")
                + f" = {len(candidates)}"),
        },
        "language_filter": args.language_filter,
        "eligible_language_labels": {},
        "overlap_policy": args.overlap_policy,
        "overlap_photographs_admitted_once": admitted_overlap,
        "selected": len(selected),
        "selected_language_labels": lang,
        "language_note": "Distributor's language label, recorded for composition reporting only. "
                         "Devanagari was identified by SCRIPT IN THE TRANSCRIPTION, never by "
                         "language label. Marathi is written in Devanagari.",
        "strata_available": {f"{k[0]}/{k[1]}": len(v) for k, v in sorted(strata.items())},
        "strata_selected": {},
    }
    for c in candidates:
        k = c["source_language_label"]
        summary["eligible_language_labels"][k] = summary["eligible_language_labels"].get(k, 0) + 1
    for c in selected:
        k = f'{c["strata"]["size"]}/{c["strata"]["clutter"]}'
        summary["strata_selected"][k] = summary["strata_selected"].get(k, 0) + 1
    (out / "selection-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    ea = summary["exclusion_arithmetic"]
    print(f"labelled source records : {ea['labelled_source_records']}")
    print(f"shared hashes           : {ea['cross_source_shared_hashes']} -> removes "
          f"{ea['records_removed_by_overlap_policy']} records "
          f"[policy={ea['policy']}]")
    print(f"same-source dupes       : {ea['same_source_duplicate_records_removed']}")
    print(f"eligible photographs    : {ea['eligible_unique_photographs']}   [{ea['check']}]")
    print(f"selected                : {len(selected)}")
    print(f"language filter         : {args.language_filter or '(none)'}")
    print(f"eligible language mix   : {summary['eligible_language_labels']}")
    print(f"selected language mix   : {summary['selected_language_labels']}")
    print(f"contested B-regions     : {contested_b_regions} of {total_b_regions}")
    print(f"BSTD opened             : {reserve['src_bstd_devanagari']['opened_by_this_script']}")
    print(f"cross-dataset agreement : one-to-one {agree_1to1}/{matched_1to1} = "
          f"{report['agreement_rate']}  |  superseded greedy {agree_greedy}/{matched_greedy} = "
          f"{report['superseded_method']['agreement_rate']}")
    print(f"wrote -> {_portable(out, repo)}")

if __name__ == "__main__":
    main()
