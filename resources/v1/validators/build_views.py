#!/usr/bin/env python3
"""Build logical Eval-facing views over the committed manifest. No media is copied.

A view is a SELECTION, not a copy. Each line references a committed item_id and sha256 and carries
the three lineage keys plus whatever descriptive attributes are derivable from committed metadata.

Every record carries payload_availability_in_this_session=not_present_git_ignored, because the raw
media is not in GitHub and a manifest that implied otherwise would be the exact "description does
not match the files" defect this stream has already been caught by once.

Descriptive attributes only. No creative label, no quality judgement, no protected role.
FAIL-CLOSED: any view that resolves to zero items, or whose count contradicts its declared
expectation, aborts the whole build and writes nothing.
"""
import json, os, sys, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lineage_keys as lk

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MANIFEST = os.path.join(ROOT, "manifests", "corpus-pilot-v0.jsonl")
OUT = os.path.join(ROOT, "v1", "views")

CVIT = ("src_indicstr12_devanagari", "src_iiit_ilst_devanagari")


def fatal(msg):
    print(f"[FAIL] {msg}", file=sys.stderr); sys.exit(2)


def base(r):
    return os.path.basename(r["relative_path"])


def is_crop(r):
    return base(r).count("__") >= 3


def attrs(r):
    """Descriptive attributes derivable from committed metadata alone."""
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


def main():
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

    # view_id -> (selector, expected_count)
    views = {
        "deva_bstd_full":            (lambda r: r["source_id"] == "src_bstd_devanagari", 25246),
        "deva_cvit_lineage_full":    (lambda r: r["source_id"] in CVIT, 4476),
        "deva_cvit_scene_photographs": (lambda r: r["source_id"] in CVIT and not is_crop(r), 551),
        "deva_cvit_word_crops":      (lambda r: r["source_id"] in CVIT and is_crop(r), 3925),
        "imagepref_imagerewarddb":   (lambda r: r["source_id"] == "src_imagerewarddb", 2584),
        "realvideo_konvid1k":        (lambda r: r["source_id"] == "src_konvid1k", 1200),
        "genvideo_videofeedback":    (lambda r: r["source_id"] == "src_videofeedback", 987),
        "genvideo_videogen_rewardbench": (lambda r: r["source_id"] == "src_videogen_rewardbench", 288),
        "realugc_youtube_ugc":       (lambda r: r["source_id"] == "src_youtube_ugc", 5),
    }

    os.makedirs(OUT, exist_ok=True)
    built = {}
    payload = []
    for vid, (sel, expect) in views.items():
        rows = [r for r in recs if sel(r)]
        if not rows:
            fatal(f"view '{vid}' selected zero items")
        if len(rows) != expect:
            fatal(f"view '{vid}' selected {len(rows)} items, expected {expect}")
        lines = []
        for r in rows:
            lines.append(json.dumps({
                "view_id": vid,
                "item_id": r["item_id"],
                "source_id": r["source_id"],
                "sha256": r["sha256"],
                "bytes": r["bytes"],
                "media_type": r["media_type"],
                "lineage_byte": lk.byte_key(r),
                "lineage_content": lk.content_key(r),
                "lineage_source": lk.source_lineage_key(r),
                "attributes": attrs(r),
                "protected_role": "unassigned_pending_eval_experiment_split",
                "payload_availability_in_this_session": "not_present_git_ignored",
            }, ensure_ascii=False, sort_keys=True))
        payload.append((vid, "\n".join(lines) + "\n"))
        built[vid] = rows

    for vid, text in payload:          # write only after every view validated
        with open(os.path.join(OUT, vid + ".jsonl"), "w") as fh:
            fh.write(text)

    print(f"[OK] {len(built)} views written to {OUT}")
    for vid, rows in built.items():
        cg = len({lk.content_key(r) for r in rows})
        ln = sorted({lk.source_lineage_key(r) for r in rows})
        print(f"  {vid:32s} {len(rows):>6,d} items · {cg:>6,d} content groups · lineage {','.join(ln)}")


if __name__ == "__main__":
    main()
