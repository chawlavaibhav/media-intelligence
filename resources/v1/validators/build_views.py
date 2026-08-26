#!/usr/bin/env python3
"""Build logical Eval-facing views over the committed manifest. No media is copied.

R-C3: views are DETERMINISTIC BUILD PRODUCTS, not evidence. They are generated into build/ and are
NOT committed. What IS committed is this generator, the expected counts, a SHA-256 fingerprint per
view, and a handful of sample records showing the shape. That is enough to prove any rebuild is
byte-identical without carrying ~31 MB of rebuildable JSONL in git.

This is NOT the reproducibility hole the project has been bitten by twice. The EVAL-005 build/ items
and the legacy spike's generated media were irreproducible because they depended on assets outside
git - a proprietary font, raw media. These views depend only on corpus-pilot-v0.jsonl and
lineage_keys.py, both committed. The distinguishing test is whether an artifact needs anything git
does not hold, and this one does not.

Every record carries payload_availability_in_this_session=not_present_git_ignored, because the raw
media is not in GitHub, and a manifest implying otherwise would be the exact "description does not
match the files" defect this stream has already been caught by once.

FAIL-CLOSED: a view resolving to zero items, or a count contradicting its declared expectation,
aborts the whole build and writes nothing. With --check, a fingerprint mismatch is a failure.

Usage:
  build_views.py                       build into build/views and CHECK against committed fingerprints
  build_views.py --update-fingerprints build and REWRITE the committed fingerprints + sample records
  build_views.py --out DIR             build somewhere else
"""
import argparse, collections, hashlib, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lineage_keys as lk

V1 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(V1)
MANIFEST = os.path.join(ROOT, "manifests", "corpus-pilot-v0.jsonl")
DEFAULT_OUT = os.path.join(V1, "build", "views")
FINGERPRINTS = os.path.join(V1, "views", "view-fingerprints.json")
SAMPLES = os.path.join(V1, "views", "SAMPLE-RECORDS.jsonl")

CVIT = ("src_indicstr12_devanagari", "src_iiit_ilst_devanagari")


def fatal(msg):
    print(f"[FAIL] {msg}", file=sys.stderr); sys.exit(2)


def base(r):
    return os.path.basename(r["relative_path"])


def is_crop(r):
    return base(r).count("__") >= 3


def attrs(r):
    a = {}
    sid, n = r["source_id"], base(r)
    if sid == "src_bstd_devanagari":
        p = r["relative_path"].split("/")
        a["distributor_split"] = p[5]
        a["distributor_language_label"] = p[6]
        a["script_note"] = ("language label is NOT a script label: Marathi is written in Devanagari, "
                            "and 364 items sit outside the hindi/marathi folders")
    elif sid in CVIT:
        a["media_category"] = "crop_image" if is_crop(r) else "scene_photograph"
    elif sid == "src_videogen_rewardbench":
        a["generator"] = n.rsplit("_", 1)[0]
    elif sid == "src_youtube_ugc":
        a["distributor_category"] = n.split("_")[0]
        a["audio"] = "removed_by_distributor"
    if r.get("duration_s"):
        a["duration_s"] = r["duration_s"]
    if r.get("width"):
        a["width"], a["height"] = r["width"], r["height"]
    return a


VIEWS = {
    "deva_bstd_full":              (lambda r: r["source_id"] == "src_bstd_devanagari", 25246),
    "deva_cvit_lineage_full":      (lambda r: r["source_id"] in CVIT, 4476),
    "deva_cvit_scene_photographs": (lambda r: r["source_id"] in CVIT and not is_crop(r), 551),
    "deva_cvit_word_crops":        (lambda r: r["source_id"] in CVIT and is_crop(r), 3925),
    "imagepref_imagerewarddb":     (lambda r: r["source_id"] == "src_imagerewarddb", 2584),
    "realvideo_konvid1k":          (lambda r: r["source_id"] == "src_konvid1k", 1200),
    "genvideo_videofeedback":      (lambda r: r["source_id"] == "src_videofeedback", 987),
    "genvideo_videogen_rewardbench": (lambda r: r["source_id"] == "src_videogen_rewardbench", 288),
    "realugc_youtube_ugc":         (lambda r: r["source_id"] == "src_youtube_ugc", 5),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--update-fingerprints", action="store_true")
    args = ap.parse_args()

    if not os.path.isfile(MANIFEST):
        fatal(f"manifest not found: {MANIFEST}")
    recs = []
    with open(MANIFEST) as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if line:
                try:
                    recs.append(json.loads(line))
                except json.JSONDecodeError as e:
                    fatal(f"manifest line {n} unparseable: {e}")
    if len(recs) < 1000:
        fatal(f"only {len(recs)} manifest records; refusing to build views from a truncated manifest")
    lk.build_content_index(recs)

    built, payload = {}, []
    for vid, (sel, expect) in VIEWS.items():
        rows = [r for r in recs if sel(r)]
        if not rows:
            fatal(f"view '{vid}' selected zero items")
        if len(rows) != expect:
            fatal(f"view '{vid}' selected {len(rows)} items, expected {expect}")
        lines = [json.dumps({
            "view_id": vid, "item_id": r["item_id"], "source_id": r["source_id"],
            "sha256": r["sha256"], "bytes": r["bytes"], "media_type": r["media_type"],
            "lineage_byte": lk.byte_key(r), "lineage_content": lk.content_key(r),
            "lineage_source": lk.source_lineage_key(r), "attributes": attrs(r),
            "protected_role": "unassigned_pending_eval_experiment_split",
            "payload_availability_in_this_session": "not_present_git_ignored",
        }, ensure_ascii=False, sort_keys=True) for r in rows]
        payload.append((vid, "\n".join(lines) + "\n"))
        built[vid] = rows

    os.makedirs(args.out, exist_ok=True)
    for vid, text in payload:                       # write only after every view validated
        with open(os.path.join(args.out, vid + ".jsonl"), "w") as fh:
            fh.write(text)

    fp = {vid: {"items": len(built[vid]),
                "content_groups": len({lk.content_key(r) for r in built[vid]}),
                "sha256": hashlib.sha256(text.encode()).hexdigest()}
          for (vid, text) in payload}
    combined = hashlib.sha256("".join(fp[v]["sha256"] for v in sorted(fp)).encode()).hexdigest()

    print(f"[OK] {len(built)} views built into {os.path.relpath(args.out, ROOT)} (not committed — R-C3)")
    for vid in VIEWS:
        ln = sorted({lk.source_lineage_key(r) for r in built[vid]})
        print(f"  {vid:32s} {fp[vid]['items']:>6,d} items · {fp[vid]['content_groups']:>6,d} content groups"
              f" · {fp[vid]['sha256'][:12]}… · {','.join(ln)}")

    if args.update_fingerprints:
        with open(FINGERPRINTS, "w") as fh:
            json.dump({"_comment": "Deterministic fingerprints of the build products in "
                                   "resources/v1/build/views/. The views themselves are not "
                                   "committed (R-C3); these prove any rebuild is byte-identical.",
                       "combined_sha256": combined, "views": fp}, fh, indent=2, sort_keys=True)
            fh.write("\n")
        with open(SAMPLES, "w") as fh:
            fh.write("# One representative record per view, showing the record shape.\n")
            fh.write("# The full views are build products; rebuild with build_views.py.\n")
            for vid, text in payload:
                fh.write(text.split("\n", 1)[0] + "\n")
        print(f"[OK] fingerprints written to {os.path.relpath(FINGERPRINTS, ROOT)}")
        print(f"[OK] {len(payload)} sample records written to {os.path.relpath(SAMPLES, ROOT)}")
        sys.exit(0)

    if not os.path.isfile(FINGERPRINTS):
        fatal(f"committed fingerprints not found at {FINGERPRINTS}; cannot verify determinism")
    ref = json.load(open(FINGERPRINTS))
    bad = []
    for vid, got in fp.items():
        want = ref["views"].get(vid)
        if not want:
            bad.append(f"{vid}: no committed fingerprint")
        elif want != got:
            bad.append(f"{vid}: rebuilt {got} != committed {want}")
    for vid in ref["views"]:
        if vid not in fp:
            bad.append(f"{vid}: committed fingerprint has no corresponding view")
    if combined != ref.get("combined_sha256"):
        bad.append(f"combined fingerprint {combined[:16]}… != committed {str(ref.get('combined_sha256'))[:16]}…")
    if bad:
        for b in bad:
            print(f"[FAIL] {b}")
        print("\nRESULT: rebuilt views do not match the committed fingerprints.")
        sys.exit(1)
    print(f"[PASS] all {len(fp)} views match their committed fingerprints "
          f"(combined sha256 {combined[:16]}…) — rebuild is byte-identical")
    sys.exit(0)


if __name__ == "__main__":
    main()
