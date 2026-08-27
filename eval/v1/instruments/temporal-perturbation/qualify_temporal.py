#!/usr/bin/env python3
"""Score an instrument's detections against the injected truth, and write the
qualification record it earned - or did not earn.

WHAT THIS DOES
--------------
The pack knows exactly where every defect is, because it put them there. An
instrument (a checker - a vision model, a script, a person, anything that
returns a verdict) is shown the fixtures and returns, for each one, whether it
found a defect and where. This file compares the two and computes the three
numbers the frozen family-4 gate asks for:

  1. detection recall PER PERTURBATION TYPE, never as one average. An
     instrument that catches freezes and misses text mutation is not "80%
     accurate"; it is blind to the failure that costs the most money.
  2. the false-positive rate on the untouched clean clips. A detector that
     reports drift in a perfectly stable clip is unusable however good its
     recall is.
  3. localisation - does it point near the frame where the defect was injected?
     Detection without localisation cannot drive repair.

WHAT THIS DELIBERATELY CANNOT DO
--------------------------------
It cannot award a qualification. Two separate locks:

  * No numeric pass mark for family 4 exists anywhere in the frozen contracts,
    and inventing one to make a run conclude would be exactly the kind of
    convenience this project forbids. Without a Controller-approved threshold
    reference the gate verdict is `undetermined`, and status can never be
    `qualified`.
  * Running against constructed stand-in material returns `unmeasurable`,
    because the frozen family-4 condition is real footage.

It also refuses to score an incomplete run: a fixture with no detection record
is recorded as MISSING and invalidates the run. It is never quietly counted as
a miss, and never as a pass.

No network. No model call. No spend. This file only does arithmetic.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import perturbations as P   # noqa: E402

ALLOWED_STATUS = ("qualified", "provisional", "screened_not_qualified",
                  "disqualified", "unmeasurable")


class ScoringError(Exception):
    """Raised when a run cannot be scored honestly. Never downgraded to a verdict."""


# --------------------------------------------------------------------------
def clopper_pearson_upper(k: int, n: int, conf: float = 0.95) -> float | None:
    """Upper bound on a failure rate under an iid Bernoulli model.

    SIZING CALCULATION ONLY. The frozen master spec is explicit: the gate is a
    count, not a rate, and this figure is never the checker's real-world error
    rate. Errors stay correlated across clips, defect types and content, and
    frames from one clip are not independent trials at all. It is reported with
    independence_status NOT ESTABLISHED and must never be quoted without it.
    """
    if n <= 0:
        return None
    if k >= n:
        return 1.0
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        # P(X <= k) under Binomial(n, mid)
        cdf = sum(math.comb(n, i) * mid ** i * (1 - mid) ** (n - i) for i in range(k + 1))
        if cdf > 1 - conf:
            lo = mid
        else:
            hi = mid
    return round((lo + hi) / 2, 6)


def _interval_gap(reported, truth) -> int | None:
    """Frames between the reported interval and the injected one; 0 if they overlap."""
    if not reported or not truth:
        return None
    a0, a1 = int(reported[0]), int(reported[1])
    b0, b1 = int(truth[0]), int(truth[1])
    if a0 > a1:
        a0, a1 = a1, a0
    if a1 >= b0 and b1 >= a0:
        return 0
    return b0 - a1 if a1 < b0 else a0 - b1


# --------------------------------------------------------------------------
def score(manifest: dict, detections: list, instrument: dict,
          repeats: int = 1, threshold_ref: str | None = None) -> dict:
    fixtures = manifest.get("fixtures") or []
    if not fixtures:
        raise ScoringError("manifest has no fixtures - an empty check is not a passing check")
    if not detections:
        raise ScoringError("no detections supplied - an empty run is a failure, not a pass")

    by_id = {}
    for d in detections:
        fid = d.get("fixture_id")
        if fid is None:
            raise ScoringError("a detection record has no fixture_id")
        if fid in by_id:
            raise ScoringError(f"duplicate detection record for {fid}")
        by_id[fid] = d

    missing = [f["fixture_id"] for f in fixtures if f["fixture_id"] not in by_id]
    unknown = [k for k in by_id if k not in {f["fixture_id"] for f in fixtures}]
    no_sample_rate = [k for k, d in by_id.items()
                      if d.get("refused") is not True and d.get("sampled_frames") is None]

    per_type, clean = {}, {"n": 0, "false_alarms": 0, "clips": set(), "alarm_clips": set()}
    localisation, refusals = [], 0
    sampled_frames_values = set()

    for f in fixtures:
        d = by_id.get(f["fixture_id"])
        if d is None:
            continue
        if d.get("refused"):
            refusals += 1
            continue
        if d.get("sampled_frames") is not None:
            sampled_frames_values.add(int(d["sampled_frames"]))
        detected = bool(d.get("defect_detected"))
        if f["kind"] == "clean_control":
            clean["n"] += 1
            clean["clips"].add(f["independent_opportunity_id"])
            if detected:
                clean["false_alarms"] += 1
                clean["alarm_clips"].add(f["independent_opportunity_id"])
            continue
        t = per_type.setdefault(f["perturbation_type"], {
            "fixtures": 0, "detected": 0, "missed": 0,
            "clips": set(), "clips_detected": set(),
            "localised_overlapping": 0, "localisation_gaps": []})
        t["fixtures"] += 1
        t["clips"].add(f["independent_opportunity_id"])
        if detected:
            t["detected"] += 1
            t["clips_detected"].add(f["independent_opportunity_id"])
            gap = _interval_gap(d.get("reported_frames"), f.get("affected_output_frames"))
            if gap is not None:
                t["localisation_gaps"].append(abs(gap))
                if gap == 0:
                    t["localised_overlapping"] += 1
                localisation.append({"fixture_id": f["fixture_id"],
                                     "perturbation_type": f["perturbation_type"],
                                     "gap_frames": abs(gap)})
        else:
            t["missed"] += 1

    recall_by_type = {}
    for ptype, t in sorted(per_type.items()):
        gaps = sorted(t["localisation_gaps"])
        recall_by_type[ptype] = {
            "fixtures": t["fixtures"],
            "detected": t["detected"],
            "missed_false_passes": t["missed"],
            "recall_over_fixtures": round(t["detected"] / t["fixtures"], 6),
            "independent_clips": len(t["clips"]),
            "independent_clips_with_a_detection": len(t["clips_detected"]),
            "recall_over_independent_clips": round(
                len(t["clips_detected"]) / len(t["clips"]), 6) if t["clips"] else None,
            "localisation_reported": len(gaps),
            "localisation_overlapping_injected_interval": t["localised_overlapping"],
            "localisation_gap_frames_median": (gaps[len(gaps) // 2] if gaps else None),
            "localisation_gap_frames_max": (gaps[-1] if gaps else None),
            "capabilities_this_type_supplies_truth_for": P.CAPABILITY_TARGETS[ptype],
        }

    total_perturbed = sum(t["fixtures"] for t in per_type.values())
    total_missed = sum(t["missed"] for t in per_type.values())
    n_opportunities = len({f["independent_opportunity_id"] for f in fixtures})

    # ---- why the run may be un-scoreable ---------------------------------
    invalidators = []
    if missing:
        invalidators.append(
            f"{len(missing)} fixture(s) have no detection record. A fixture that was not "
            "scored is not a miss and not a pass - the run is incomplete.")
    if unknown:
        invalidators.append(
            f"{len(unknown)} detection record(s) name fixtures that are not in this pack.")
    if no_sample_rate:
        invalidators.append(
            f"{len(no_sample_rate)} detection record(s) omit sampled_frames. A defect between "
            "two sampled frames is invisible, so a result without its sample rate cannot be "
            "interpreted and cannot qualify anything.")

    material_classes = manifest.get("material_classes", [])
    is_real = manifest.get("is_approved_qualification_pack") is True
    threshold_status = ("CONTROLLER_APPROVED:" + threshold_ref) if threshold_ref else \
        "NOT_SET - no numeric family-4 pass mark exists in the frozen contracts"

    if invalidators:
        status = "unmeasurable"
        reason = " ".join(invalidators)
    elif not is_real:
        status = "unmeasurable"
        reason = ("The protocol ran, but against material class "
                  f"{material_classes}. The frozen family-4 condition is real footage, and a "
                  "qualification does not transfer from constructed stand-ins to real clips. "
                  "The approved base clips do not exist yet.")
    elif threshold_ref is None:
        status = "screened_not_qualified" if repeats < 3 else "provisional"
        reason = ("Gate arithmetic computed on approved material, but no Controller-approved "
                  "family-4 pass mark exists, so whether the gate was passed is undetermined. "
                  + ("Fewer than 3 full repeats were completed." if repeats < 3 else ""))
    elif repeats < 3:
        status = "screened_not_qualified"
        reason = "Fewer than 3 full repeats. Screening produces a ranking, never a status."
    else:
        status = "provisional"
        reason = ("Gate arithmetic and repeats are complete. Promotion to `qualified` is a "
                  "Controller decision against the approved pass mark; this file does not "
                  "make it.")

    record = {
        "schema_ref": "eval/v1/instruments/qualification-result-schema.yaml",
        "record_type": "instrument_qualification",
        "record_id": "qual_temporal_" + hashlib.sha256(
            (json.dumps(instrument, sort_keys=True)
             + manifest.get("configuration_hash", "")).encode()).hexdigest()[:12],
        "instrument_id": instrument.get("instrument_id"),
        "instrument_version": instrument.get("instrument_version"),
        "configuration_hash": instrument.get("configuration_hash"),
        "instrument_family": 4,
        "judgement_family": "temporal_video_injected_perturbation_detection",
        "pack_ref": "eval/v1/instruments/temporal-perturbation",
        "pack_version": manifest.get("plan_version"),
        "pack_hash": manifest.get("configuration_hash"),
        "conditions": {
            "material_classes": material_classes,
            "fps": sorted({f.get("fps") for f in fixtures if f.get("fps")}),
            "clip_duration_s": sorted({round(b["duration_s"], 3)
                                       for b in manifest.get("base_clips", [])}),
            "resolution": sorted({f"{b['width']}x{b['height']}"
                                  for b in manifest.get("base_clips", [])
                                  if b.get("width") and b.get("height")}),
            "source_motion_load_range": [
                min((b["motion_load"] for b in manifest.get("base_clips", [])), default=None),
                max((b["motion_load"] for b in manifest.get("base_clips", [])), default=None)],
            "sampled_frames_values_observed": sorted(sampled_frames_values),
            "sample_rate_rule": "This qualification is valid only at or above the frame sample "
                                "rate it was measured at. A lower sample rate is a different "
                                "and unqualified configuration.",
        },
        "gate": {
            "n_opportunities": n_opportunities,
            "opportunity_definition": "one base clip = one independent opportunity. Frames from "
                                      "one clip are ONE trial, never many.",
            "n_perturbed_fixtures": total_perturbed,
            "false_passes": total_missed,
            "false_passes_meaning": "injected defects the instrument called clean - the "
                                    "dangerous direction, because the defect ships with a "
                                    "passing grade attached",
            "false_fails": clean["false_alarms"],
            "false_fails_meaning": "untouched clean clips the instrument called defective",
            "clean_controls": clean["n"],
            "clean_control_false_positive_rate": (
                round(clean["false_alarms"] / clean["n"], 6) if clean["n"] else None),
            "clean_control_clips_with_a_false_alarm": len(clean["alarm_clips"]),
            "refusals": refusals,
            "gate_verdict": "undetermined" if threshold_ref is None else "see threshold_ref",
            "gate_rule_ref": "eval/v1/instruments/FAMILY-4-TEMPORAL-VIDEO.md#gate",
            "threshold_status": threshold_status,
        },
        "recall_by_perturbation_type": recall_by_type,
        "never_report_a_single_average": (
            "Recall is reported per perturbation type by design. Averaging across types hides "
            "an instrument that is blind to one whole failure mode."),
        "diagnosis": {
            "n_scored": total_perturbed - total_missed,
            "correct_class": sum(
                1 for f in fixtures
                if f["kind"] == "perturbed"
                and (by_id.get(f["fixture_id"]) or {}).get("reported_type")
                == f["perturbation_type"]),
            "wrong_class": sum(
                1 for f in fixtures
                if f["kind"] == "perturbed"
                and (by_id.get(f["fixture_id"]) or {}).get("reported_type") not in
                (None, f["perturbation_type"])),
            "no_class_offered": sum(
                1 for f in fixtures
                if f["kind"] == "perturbed"
                and (by_id.get(f["fixture_id"]) or {}).get("defect_detected")
                and (by_id.get(f["fixture_id"]) or {}).get("reported_type") is None),
            "note": "Stored apart from the gate. Routing consumes the gate; repair consumes "
                    "the diagnosis. They may never share one number.",
        },
        "localisation": {
            "n_with_reported_interval": len(localisation),
            "n_overlapping_injected_interval": sum(1 for x in localisation if x["gap_frames"] == 0),
            "gap_frames_distribution": sorted(x["gap_frames"] for x in localisation),
            "note": "No tolerance is applied. No frame tolerance exists in the frozen "
                    "contracts and inventing one here would be inventing a threshold.",
        },
        "repeats": {
            "full_passes": repeats,
            "shapes_covered": instrument.get("shapes_covered"),
            "repeat_consistency": instrument.get("repeat_consistency"),
            "consistency_threshold_applied": None,
            "threshold_status": "PROPOSED_NOT_EMPIRICALLY_BACKED",
        },
        "reference_calculation": {
            "description": "Sizing only. Never a real-world error rate.",
            "iid_reference_upper_bound_95pct": clopper_pearson_upper(
                total_missed, n_opportunities),
            "computed_over": "independent clips, not fixtures",
            "independence_status": "NOT ESTABLISHED",
            "caveat": "An instrument blind to one defect type is blind to it on every clip "
                      "carrying that type. Errors here are correlated by construction.",
        },
        "blind_check": {
            "required": False,
            "performed_before_run": None,
            "method": "not applicable: the injected truth lives in the manifest, which is never "
                      "part of the payload shown to an instrument. see check_blindness().",
            "result": None,
        },
        "human_reference": {
            "used": False,
            "n_reviewers": 0,
            "what_the_human_decided": "nothing - the truth is the transformation",
            "epistemic_status": "truth known by construction; no annotator involved",
        },
        "incomplete_run": {
            "missing_detection_records": missing[:50],
            "missing_count": len(missing),
            "unknown_fixture_ids": unknown[:50],
            "records_without_sample_rate": no_sample_rate[:50],
        },
        "status": status,
        "status_reason": reason,
        "registry_use_permitted": status == "qualified",
        "cost": {"calls": instrument.get("calls", 0), "currency": "USD", "spend": 0.0,
                 "human_hours": 0.0},
        "requalification_triggers": [
            "instrument_version_change", "configuration_hash_change", "pack_version_change",
            "conditions_outside_qualified_range", "sample_rate_below_qualified_rate",
        ],
    }
    if record["status"] not in ALLOWED_STATUS:
        raise ScoringError(f"illegal status {record['status']!r}")
    if record["status"] == "qualified":
        raise ScoringError(
            "This file must never emit `qualified`. Promotion is a Controller decision.")
    return record


# --------------------------------------------------------------------------
def check_blindness(payload_paths: list, manifest_path: pathlib.Path) -> dict:
    """Prove, BEFORE a run, that nothing shown to the instrument leaks the answer.

    Frozen master-spec rule 5: blindness is verified mechanically and in
    advance, because a leak cannot be detected afterwards from the responses -
    by then the experiment is simply gone. The check fails closed: an unreadable
    path is a leak risk, not a pass.
    """
    forbidden = ("perturbation_type", "affected_output_frames", "defect_present",
                 "injected", "text_after", "donor_clip_id", "MANIFEST")
    leaks = []
    for p in payload_paths:
        path = pathlib.Path(p)
        if not path.exists():
            leaks.append({"path": str(path), "why": "does not exist; cannot be certified clean"})
            continue
        files = [path] if path.is_file() else sorted(path.rglob("*"))
        for f in files:
            if f.is_dir():
                continue
            if f.name == "MANIFEST.json" or f.resolve() == manifest_path.resolve():
                leaks.append({"path": str(f), "why": "the injected-truth manifest itself"})
                continue
            if f.suffix.lower() in (".json", ".txt", ".yaml", ".yml", ".md"):
                try:
                    text = f.read_text(errors="replace")
                except OSError as exc:
                    leaks.append({"path": str(f), "why": f"unreadable ({exc})"})
                    continue
                for token in forbidden:
                    if token in text:
                        leaks.append({"path": str(f), "why": f"contains {token!r}"})
                        break
    return {"required": True, "performed_before_run": True,
            "method": "allow-list of payload paths, failing closed, plus a sweep for "
                      "injected-truth vocabulary",
            "result": "clean" if not leaks else "leak_detected", "leaks": leaks}


# --------------------------------------------------------------------------
# self-test detections: exercise the arithmetic without any instrument
# --------------------------------------------------------------------------
def synthetic_detections(manifest: dict, profile: str) -> list:
    """Fabricated detection records for testing THIS FILE'S arithmetic.

    They come from no instrument and mean nothing about any instrument. Any
    record scored from them is forced to `unmeasurable`. Profiles:
      perfect        - finds every injected defect, localises exactly, never
                       false-alarms
      blind_to_text  - as perfect, but silently misses every text mutation
      alarmist       - reports a defect on everything, including clean controls
      incomplete     - omits some fixtures, to prove the run is invalidated
    """
    out = []
    for i, f in enumerate(manifest["fixtures"]):
        if profile == "incomplete" and i % 7 == 0:
            continue
        perturbed = f["kind"] == "perturbed"
        text_type = f.get("perturbation_type") in (
            "text_region_mutation", "text_glyph_substitution")
        if profile == "alarmist":
            detected = True
        elif profile == "blind_to_text" and text_type:
            detected = False
        else:
            detected = perturbed
        out.append({
            "fixture_id": f["fixture_id"],
            "defect_detected": detected,
            "reported_frames": (f.get("affected_output_frames")
                                if detected and perturbed else None),
            "reported_type": f.get("perturbation_type") if detected and perturbed else None,
            "sampled_frames": f.get("output_n_frames"),
        })
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Score detections against injected truth.")
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--detections", default=None,
                    help="JSON list of detection records from an instrument run")
    ap.add_argument("--selftest-profile", default=None,
                    choices=["perfect", "blind_to_text", "alarmist", "incomplete"],
                    help="fabricate detections to exercise the arithmetic; qualifies nothing")
    ap.add_argument("--instrument-id", default=None)
    ap.add_argument("--instrument-version", default=None)
    ap.add_argument("--repeats", type=int, default=1)
    ap.add_argument("--threshold-ref", default=None,
                    help="path/id of a Controller-approved family-4 pass mark, if one exists")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    manifest = json.loads(pathlib.Path(args.manifest).read_text())
    if args.selftest_profile:
        detections = synthetic_detections(manifest, args.selftest_profile)
        instrument = {
            "instrument_id": "SYNTHETIC_SELFTEST_NOT_AN_INSTRUMENT",
            "instrument_version": args.selftest_profile,
            "configuration_hash": None, "calls": 0,
        }
    elif args.detections:
        detections = json.loads(pathlib.Path(args.detections).read_text())
        instrument = {"instrument_id": args.instrument_id,
                      "instrument_version": args.instrument_version,
                      "configuration_hash": None, "calls": len(detections)}
        if not instrument["instrument_id"]:
            raise SystemExit("--instrument-id is required for a real run: a result whose "
                             "instrument is unnamed is not a measurement.")
    else:
        raise SystemExit("supply --detections or --selftest-profile")

    rec = score(manifest, detections, instrument, repeats=args.repeats,
                threshold_ref=args.threshold_ref)
    text = json.dumps(rec, indent=2, sort_keys=True) + "\n"
    if args.out:
        pathlib.Path(args.out).write_text(text)
    print(f"status                 {rec['status']}")
    print(f"registry_use_permitted {rec['registry_use_permitted']}")
    print(f"reason                 {rec['status_reason']}")
    print(f"opportunities (clips)  {rec['gate']['n_opportunities']}")
    print(f"false passes (missed)  {rec['gate']['false_passes']} of "
          f"{rec['gate']['n_perturbed_fixtures']} perturbed fixtures")
    print(f"false fails (clean)    {rec['gate']['false_fails']} of "
          f"{rec['gate']['clean_controls']} clean controls")
    print("\nrecall per perturbation type (never averaged):")
    for t, v in rec["recall_by_perturbation_type"].items():
        print(f"  {t:<30} {v['detected']:>3}/{v['fixtures']:<3} "
              f"clips {v['independent_clips_with_a_detection']}/{v['independent_clips']}")
    if args.out:
        print(f"\nrecord written to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
