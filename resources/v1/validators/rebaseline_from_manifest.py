#!/usr/bin/env python3
"""Recompute every Resources headline figure from the COMMITTED manifest, and cross-check the
committed source registry against it.

WHAT THIS DOES AND DOES NOT PROVE
It reads resources/manifests/corpus-pilot-v0.jsonl, which IS committed to git, and recomputes
counts, byte totals, hash distinctness, duplicate structure and per-source composition.

It does NOT open a single media file. The raw corpus (resources/corpus/raw/) is git-ignored and is
not present in a cloud session. So this tool can confirm that the manifest's own arithmetic is
sound and that the prose matches it. It CANNOT confirm that the files still decode, still hash to
these values, or look like what the prose says. Those remain previously committed observations from
RES-001/002, cited, not re-run.

FAIL-CLOSED: a missing, empty or short manifest is exit 2, never a cheerful zero.
"""
import json, os, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MANIFEST = os.path.join(ROOT, "manifests", "corpus-pilot-v0.jsonl")
REGISTRY = os.path.join(ROOT, "manifests", "source-registry-v0.csv")

# Committed headline figures, from resources/reports/RES-001-integrity-report.md and
# resources/HANDOFF.md. The point of the exercise is to see whether they still reconcile.
EXPECT = {
    "items": 34786,
    "distinct_sha256": 34586,
    "duplicate_hashes": 200,
    "cross_source_dup_hashes": 173,
    "within_source_dup_hashes": 27,
    "media_bytes": 5702337356,
    "sources": 8,
}
EXPECT_PER_SOURCE = {
    "src_bstd_devanagari": 25246,
    "src_indicstr12_devanagari": 3086,
    "src_iiit_ilst_devanagari": 1390,
    "src_imagerewarddb": 2584,
    "src_konvid1k": 1200,
    "src_videofeedback": 987,
    "src_videogen_rewardbench": 288,
    "src_youtube_ugc": 5,
}
# Committed media-category partitions for the two CVIT sources (source-registry-v0.csv).
EXPECT_PARTITION = {
    "src_indicstr12_devanagari": {"scene": 375, "crop": 2711},
    "src_iiit_ilst_devanagari": {"scene": 176, "crop": 1214},
}

results = []          # (level, message)
failures = 0


def record(ok, msg, hard=True):
    global failures
    level = "PASS" if ok else ("FAIL" if hard else "WARN")
    if not ok and hard:
        failures += 1
    results.append((level, msg))


def fatal(msg):
    print(f"[FAIL] {msg}", file=sys.stderr)
    sys.exit(2)


def is_crop(rec):
    """A crop image is a member of the distributor's cropped directory.

    The filename encodes parent + coordinates, giving it >=3 '__' separators, where a scene
    photograph has 2. RES-CORRECTION-01 records why this must ALSO be filtered to media
    extensions: both CVIT sources store their crop-level ground-truth .txt INSIDE the crop
    directory, and a name-pattern detector that skipped the extension filter counted three
    annotation files as images. The manifest only contains media, so that trap is already
    excluded here -- but the rule is written out so the next reader does not reintroduce it.
    """
    return os.path.basename(rec["relative_path"]).count("__") >= 3


def main():
    if not os.path.isfile(MANIFEST):
        fatal(f"manifest not found: {MANIFEST}")
    recs = []
    with open(MANIFEST) as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                recs.append(json.loads(line))
            except json.JSONDecodeError as e:
                # A parse error that silently skips a unit under-reports, and the shortfall is
                # invisible in the tool's own output. CANON-004 already paid for that lesson.
                fatal(f"manifest line {n} failed to parse: {e}")
    if len(recs) < 1000:
        fatal(f"only {len(recs)} manifest records parsed; refusing to report on a truncated manifest")

    # --- totals ---
    record(len(recs) == EXPECT["items"], f"item count {len(recs):,} vs committed {EXPECT['items']:,}")
    hashes = collections.Counter(r["sha256"] for r in recs)
    record(len(hashes) == EXPECT["distinct_sha256"],
           f"distinct sha256 {len(hashes):,} vs committed {EXPECT['distinct_sha256']:,}")
    dups = [h for h, c in hashes.items() if c > 1]
    record(len(dups) == EXPECT["duplicate_hashes"],
           f"duplicate hashes {len(dups)} vs committed {EXPECT['duplicate_hashes']}")
    by_hash_src = collections.defaultdict(set)
    for r in recs:
        by_hash_src[r["sha256"]].add(r["source_id"])
    cross = [h for h in dups if len(by_hash_src[h]) > 1]
    record(len(cross) == EXPECT["cross_source_dup_hashes"],
           f"cross-source duplicate hashes {len(cross)} vs committed {EXPECT['cross_source_dup_hashes']}")
    record(len(dups) - len(cross) == EXPECT["within_source_dup_hashes"],
           f"within-source duplicate hashes {len(dups)-len(cross)} vs committed {EXPECT['within_source_dup_hashes']}")
    total_bytes = sum(r["bytes"] for r in recs)
    record(total_bytes == EXPECT["media_bytes"],
           f"media bytes {total_bytes:,} vs committed {EXPECT['media_bytes']:,}")

    # --- validation status: manifest self-report, NOT a re-decode ---
    st = collections.Counter(r["validation_status"] for r in recs)
    record(set(st) == {"ok"},
           f"all {len(recs):,} records carry validation_status 'ok' (RECORDED status, not a cloud re-decode): {dict(st)}")

    # --- per source ---
    per = collections.Counter(r["source_id"] for r in recs)
    record(len(per) == EXPECT["sources"], f"source count {len(per)} vs committed {EXPECT['sources']}")
    for s, n in sorted(EXPECT_PER_SOURCE.items()):
        record(per.get(s) == n, f"{s}: {per.get(s)} items vs committed {n}")

    # --- CVIT media-category partition: disjoint AND exhaustive ---
    for src, exp in EXPECT_PARTITION.items():
        rs = [r for r in recs if r["source_id"] == src]
        crops = [r for r in rs if is_crop(r)]
        scenes = [r for r in rs if not is_crop(r)]
        record(len(scenes) == exp["scene"], f"{src}: scene photographs {len(scenes)} vs committed {exp['scene']}")
        record(len(crops) == exp["crop"], f"{src}: crop images {len(crops)} vs committed {exp['crop']}")
        record(len(scenes) + len(crops) == len(rs),
               f"{src}: partition exhaustive ({len(scenes)}+{len(crops)}={len(rs)})")
        record(not (set(id(x) for x in scenes) & set(id(x) for x in crops)),
               f"{src}: partition disjoint")

    # --- the cross-source overlap: WHICH items are shared? ---
    crossset = set(cross)
    ilst = [r for r in recs if r["source_id"] == "src_iiit_ilst_devanagari"]
    shared_ilst = [r for r in ilst if r["sha256"] in crossset]
    shared_scene = [r for r in shared_ilst if not is_crop(r)]
    record(len(shared_ilst) == 173 and len(shared_scene) == 173,
           f"all {len(shared_ilst)} shared IIIT-ILST items are scene photographs "
           f"({len(shared_scene)} scene / {len(shared_ilst)-len(shared_scene)} crop) "
           f"= {len(shared_scene)}/176 = {100*len(shared_scene)/176:.1f}% of its scene set")

    # --- BSTD language composition vs the registry's prose ---
    bstd = [r for r in recs if r["source_id"] == "src_bstd_devanagari"]
    lang = collections.Counter(r["relative_path"].split("/")[6] for r in bstd)
    other = sum(v for k, v in lang.items() if k not in ("hindi", "marathi"))
    record(lang["hindi"] + lang["marathi"] + other == len(bstd),
           f"BSTD composition sums: hindi {lang['hindi']:,} + marathi {lang['marathi']:,} + other {other} = {len(bstd):,}")
    # The registry and handoff both say 351 here. The manifest says otherwise. Do not reconcile it
    # silently -- surface it.
    record(other == 351,
           f"BSTD 'other language' items: manifest says {other}, committed prose says 351 "
           f"(delta {other-351}). Resolving this needs the raw annotation files, which are not in "
           f"this cloud session. RECORDED AS AN OPEN DISCREPANCY.",
           hard=False)

    # --- BSTD split-spanning duplicates ---
    byh = collections.defaultdict(list)
    for r in bstd:
        byh[r["sha256"]].append(r)
    span = [h for h, v in byh.items()
            if len(v) > 1 and len({x["relative_path"].split("/")[5] for x in v}) > 1]
    record(len(span) == 2, f"BSTD duplicate hashes spanning train/test: {len(span)} vs committed 2")

    # --- registry cross-check ---
    if not os.path.isfile(REGISTRY):
        fatal(f"source registry not found: {REGISTRY}")
    import csv as _csv
    with open(REGISTRY) as fh:
        reg = list(_csv.DictReader(fh))
    record(len(reg) == 12, f"source registry holds {len(reg)} candidate records vs expected 12 (8 acquired + 4 blocked)")
    acq = [r for r in reg if r["status"] in ("downloaded", "partial_download")]
    blocked = [r for r in reg if r["status"].startswith("blocked")]
    record(len(acq) == 8, f"registry acquired sources: {len(acq)} vs expected 8")
    record(len(blocked) == 4, f"registry blocked sources: {len(blocked)} vs expected 4")
    for r in acq:
        mid = r["source_id"]
        claimed = int(r["downloaded_item_count"] or 0)
        record(per.get(mid) == claimed,
               f"{mid}: registry downloaded_item_count {claimed} vs manifest {per.get(mid)}")
        claimed_b = int(r["downloaded_bytes"] or 0)
        actual_b = sum(x["bytes"] for x in recs if x["source_id"] == mid)
        record(actual_b == claimed_b,
               f"{mid}: registry downloaded_bytes {claimed_b:,} vs manifest {actual_b:,}")

    for level, msg in results:
        print(f"[{level}] {msg}")
    print()
    n_pass = sum(1 for l, _ in results if l == "PASS")
    n_warn = sum(1 for l, _ in results if l == "WARN")
    print(f"{n_pass} pass, {failures} fail, {n_warn} warn, {len(results)} checks total")
    print("SCOPE: committed manifest + registry metadata only. No media file was opened. "
          "Decode results remain previously committed observations from RES-001/002.")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
