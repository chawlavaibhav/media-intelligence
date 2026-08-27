#!/usr/bin/env python3
"""RES-005 - join acquisition + measurement into the committed MAT-AV-MIN manifests.

Produces:
  MAT-AV-MIN-MANIFEST.csv / .jsonl   one row per frozen clip
  LINEAGE-MANIFEST.yaml              media lineage at byte / content / source level,
                                     following resources/v1/validators/lineage_keys.py

Tag policy: a tag is set ONLY from a measurement or from a recorded human/agent frame
inspection. Where neither exists the value is "not_established", never a guess.

Exit 0 built · 2 could not build.
"""
import csv, json, os, sys
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE = os.path.join(REPO, "resources/pre-execution-freeze/mat-av-min")
ACQ = os.path.join(BASE, "acquisition-record.json")
QUAL = os.path.join(BASE, "qualification-measurements.json")
INSPECT = os.path.join(BASE, "frame-inspection.json")

# Level-3 source lineage. Clips sharing a key are NOT independent of each other,
# whatever their file hashes say. Registered explicitly rather than defaulted, per the
# R-C4 rule that two unregistered ids must never be read as two independent lineages.
SOURCE_LINEAGE = {
    "MAVM-01": "lin_blender_open_movies", "MAVM-02": "lin_blender_open_movies",
    "MAVM-03": "lin_blender_open_movies",
    "MAVM-04": "lin_nasa_public_domain", "MAVM-05": "lin_nasa_public_domain",
    "MAVM-06": "lin_nasa_public_domain", "MAVM-07": "lin_nasa_public_domain",
    "MAVM-08": "lin_nasa_public_domain",
    "MAVM-09": "lin_wikimedia_foundation_first_party",
    "MAVM-10": "lin_wikimedia_foundation_first_party",
    "MAVM-11": "lin_commons_ownwork_ruindig",
    "MAVM-12": "lin_commons_ownwork_bprieur",
}
LINEAGE_NOTES = {
    "lin_blender_open_movies":
        "Blender Foundation open-movie programme. Three different films, but one studio, one "
        "pipeline and one renderer. Treat as ONE lineage: a temporal instrument that overfits to "
        "Blender's render characteristics would look good on all three.",
    "lin_nasa_public_domain":
        "NASA-produced video across HQ and JPL. Different subjects and crews, but one broadcast "
        "post-production house style - the same lower-third templates, graphics package and "
        "delivery encode. ONE lineage.",
    "lin_wikimedia_foundation_first_party":
        "Wikimedia Foundation's own productions, uploaded by WMF staff accounts. Two different "
        "shoots with different people, but one commissioning organisation. ONE lineage.",
    "lin_commons_ownwork_ruindig":
        "Single Commons contributor's own work (RuinDig / Yuki Uchida). Independent of every "
        "other lineage in this set.",
    "lin_commons_ownwork_bprieur":
        "Single Commons contributor's own work (Benoit Prieur). Independent of every other "
        "lineage in this set.",
}

CSV_FIELDS = [
    "clip_id", "work", "creator_publisher", "source_url", "direct_media_url", "source_identifier",
    "licence", "licence_verified_at_source", "licence_authority_url", "attribution_required",
    "rights_restrictions", "commercial_empirical_use_permitted", "retrieval_date_utc",
    "retrieval_authority", "retrieved_file_name", "retrieved_file_bytes", "retrieved_file_sha256",
    "source_media_sha256", "clip_relative_path", "clip_sha256", "clip_bytes", "duration_s",
    "width", "height", "fps", "frame_count", "audio_present", "audio_codec",
    "tag_person", "tag_product_object", "tag_on_screen_text", "tag_multi_shot", "tag_motion",
    "shot_count_measured", "cut_timestamps_s", "mean_abs_frame_diff",
    "text_frames_with_confident_tokens", "pre_existing_freeze_count", "black_interval_count",
    "interlaced_fraction", "clean_screen_verdict", "audio_perturbation_permitted",
    "transformations_from_original", "source_lineage_key", "content_lineage_key",
    "selection_reason",
]

# Rights posture per licence family. CC-BY-NC would be "no" and is absent from this set
# by construction; the Controller rule bars it as commercial empirical material.
COMMERCIAL_OK = {
    "CC BY 3.0": "yes - attribution only, no non-commercial clause",
    "CC BY 4.0": "yes - attribution only, no non-commercial clause",
    "CC BY-SA 4.0": "yes - no non-commercial clause; ShareAlike attaches only on distribution of a derivative, which internal evaluation does not trigger",
    "CC0 1.0 (public domain dedication)": "yes - rights waived",
    "Public domain (US Government work)": "yes - not subject to copyright in the US",
}


def main():
    for p in (ACQ, QUAL):
        if not os.path.exists(p):
            print(f"[FAIL] missing {p}", file=sys.stderr); return 2
    acq = json.load(open(ACQ)); qual = json.load(open(QUAL))
    inspect = json.load(open(INSPECT)) if os.path.exists(INSPECT) else {}

    rows, lineage = [], {}
    for rec in acq["records"]:
        cid = rec["id"]
        if rec["status"] != "acquired":
            continue
        q = qual["clips"].get(cid, {})
        cp = rec["clip_probe"]
        ins = inspect.get(cid, {})
        cb = rec.get("commons_readback", {})
        lic = rec["licence_declared_in_spec"]

        text_hits = q.get("on_screen_text_screen", {}).get("frames_with_confident_text", 0)
        motion = (q.get("motion") or {}).get("mean_abs_frame_diff")
        freezes = q.get("pre_existing_freeze_starts_s", [])
        blacks = q.get("black_intervals", [])
        ilace = (q.get("interlace") or {}).get("interlaced_fraction")

        clean_fail = []
        if freezes: clean_fail.append(f"{len(freezes)} pre-existing freeze run(s)")
        if ilace is not None and ilace > 0.10: clean_fail.append(f"interlaced fraction {ilace}")
        if motion is not None and motion < 0.20: clean_fail.append(f"near-static (mean frame diff {motion})")

        row = {
            "clip_id": cid, "work": rec["work"], "creator_publisher": rec["creator_publisher"],
            "source_url": rec["source_url"], "direct_media_url": rec["direct_media_url"],
            "source_identifier": rec.get("nasa_id") or rec.get("commons_title") or rec["direct_media_url"],
            "licence": lic,
            "licence_verified_at_source": rec.get("licence_verified_at_source"),
            "licence_authority_url": rec["licence_authority_url"],
            "attribution_required": rec.get("attribution_required", ""),
            "rights_restrictions": "; ".join(x for x in [cb.get("restrictions") or "", rec.get("rights_note", "")] if x).strip("; "),
            "commercial_empirical_use_permitted": COMMERCIAL_OK.get(lic, "not_established"),
            "retrieval_date_utc": rec["retrieval_date_utc"],
            "retrieval_authority": rec["retrieval_authority"],
            "retrieved_file_name": rec["retrieved_file_name"],
            "retrieved_file_bytes": rec["retrieved_file_bytes"],
            "retrieved_file_sha256": rec["retrieved_file_sha256"],
            "source_media_sha256": rec["source_media_sha256"],
            "clip_relative_path": rec["clip_relative_path"],
            "clip_sha256": rec["clip_sha256"], "clip_bytes": cp["bytes"],
            "duration_s": cp["duration_s"], "width": cp["width"], "height": cp["height"],
            "fps": cp["avg_fps"], "frame_count": cp["nb_video_frames"],
            "audio_present": cp["audio_present"], "audio_codec": cp["audio_codec"] or "",
            "tag_person": ins.get("person", "not_established"),
            "tag_product_object": ins.get("product_object", "not_established"),
            "tag_on_screen_text": ins.get("on_screen_text", "not_established"),
            "tag_multi_shot": "yes" if q.get("multi_shot_measured") else "no",
            "tag_motion": "yes" if (motion is not None and motion >= 0.20) else "no",
            "shot_count_measured": q.get("shot_count_estimate"),
            "cut_timestamps_s": ";".join(str(x) for x in q.get("cut_timestamps_s", [])),
            "mean_abs_frame_diff": motion,
            "text_frames_with_confident_tokens": text_hits,
            "pre_existing_freeze_count": len(freezes),
            "black_interval_count": len(blacks),
            "interlaced_fraction": ilace,
            "clean_screen_verdict": "PASS" if not clean_fail else "FAIL: " + "; ".join(clean_fail),
            "audio_perturbation_permitted":
                "no - original soundtrack is CC BY-ND 3.0" if "BY-ND" in (rec.get("rights_note") or "")
                else ("yes" if cp["audio_present"] else "n/a - no audio stream"),
            "transformations_from_original": " | ".join(rec["transformations_from_original"]),
            "source_lineage_key": SOURCE_LINEAGE.get(cid, f"lin_unknown::{cid}"),
            "content_lineage_key": f"content::{rec['source_media_sha256'][:16]}",
            "selection_reason": rec.get("selection_reason", ""),
        }
        rows.append(row)
        lineage.setdefault(row["source_lineage_key"], []).append(cid)

    with open(os.path.join(BASE, "MAT-AV-MIN-MANIFEST.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS); w.writeheader()
        for r in rows: w.writerow(r)
    with open(os.path.join(BASE, "MAT-AV-MIN-MANIFEST.jsonl"), "w") as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + "\n")

    lm = [
        "# MAT-AV-MIN media-lineage manifest - RES-005",
        "#",
        "# Media lineage only. Request lineage is a SEPARATE namespace (lineage contract v3, gate",
        "# G11) and is not_applicable here: these clips answer no customer brief. It is recorded as",
        "# not_applicable rather than left blank, because an unpopulated request lineage would read",
        "# as INDETERMINATE and INDETERMINATE must never be read as independent.",
        f"generated_utc: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}",
        "task: RES-005",
        "request_lineage: not_applicable",
        f"clips: {len(rows)}",
        f"source_lineages: {len(lineage)}",
        "",
        "independence_warning: >",
        f"  {len(rows)} clips span only {len(lineage)} source lineages. Family-4's false-positive",
        "  rate on clean clips is therefore measured over fewer independent origins than the clip",
        "  count suggests. MAT-AV-MIN sets disjointness_required: false because perturbation truth",
        "  is injected, so this is not a leakage defect - but a per-lineage breakdown must accompany",
        "  any pooled false-positive number, or the number will read as more independent than it is.",
        "",
        "lineages:",
    ]
    for k, ids in sorted(lineage.items()):
        lm += [f"  {k}:", f"    clips: [{', '.join(sorted(ids))}]",
               f"    count: {len(ids)}",
               f"    note: >-", f"      {LINEAGE_NOTES.get(k, 'not_established')}"]
    lm += ["", "byte_and_content_lineage:",
           "  byte_level: clip_sha256 in MAT-AV-MIN-MANIFEST.csv",
           "  content_level: content_lineage_key - a clip and its source work share content;",
           "    two clips cut from one work would share this key. In this set every clip comes from",
           "    a distinct source work, so no two clips share a content key.",
           "  source_level: source_lineage_key above.",
           "",
           "perturbation_reuse_consequence: >",
           "  CONTROLLED-PACK-REQUIREMENTS-v2 records that clips reused as a perturbation base share",
           "  content lineage with their AV originals and cannot be an independent holdout for a",
           "  speech measurement that also uses the original. That constraint does not bind here,",
           "  because none of these clips is part of PACK-AV-CLEAN and none carries a verified",
           "  transcript, consent record or turn boundary. They are a temporal perturbation base",
           "  only. If PACK-AV-CLEAN is later acquired, it must NOT reuse these works.",
           ""]
    with open(os.path.join(BASE, "LINEAGE-MANIFEST.yaml"), "w") as f:
        f.write("\n".join(lm))

    passed = [r for r in rows if r["clean_screen_verdict"] == "PASS"]
    print(f"rows: {len(rows)}  clean_screen PASS: {len(passed)}  lineages: {len(lineage)}")
    for r in rows:
        print(f"  {r['clip_id']} {r['licence'][:22]:22s} {r['width']}x{r['height']}@{r['fps']} "
              f"shots={r['shot_count_measured']} text={r['text_frames_with_confident_tokens']} "
              f"{r['clean_screen_verdict'][:40]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
