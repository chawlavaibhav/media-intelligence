#!/usr/bin/env python3
"""Q1 - deterministic CV geometry qualification run over the 102-item cv-geometry pack, at USD 0.

    python3 eval/harness-v2/q1/run_q1.py --preregister      write the PREREGISTRATION record (R_q, T_rgb, gates, pack hash)
    python3 eval/harness-v2/q1/run_q1.py --run              refuses unless the pre-registration exists and its
                                                            configuration_hash equals the detector's; verifies the
                                                            protected pack before and after; R_q full passes; writes
                                                            per-item observations (JSONL) and one record per judgement
                                                            family; never overwrites an existing result.
Nothing here contacts a provider. The pack manifest is a protected baseline and is only read.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import hv2_paths  # noqa: E402
from q1 import detector as D  # noqa: E402
from instruments import registry_gate as RG  # noqa: E402

PACK_DIR = hv2_paths.EVAL_ROOT / "v1" / "instruments" / "fixtures" / "cv-geometry"
MANIFEST = PACK_DIR / "manifest.json"
BUILD_SCRIPT = hv2_paths.EVAL_ROOT / "v1" / "instruments" / "build_cv_fixtures.py"
PROTECTED = hv2_paths.EMP001 / "protected-baselines.sha256"
SCHEMA = hv2_paths.EVAL_ROOT / "v1" / "instruments" / "qualification-result-schema.yaml"
QR_DIR = hv2_paths.EVAL_ROOT / "v1" / "instruments" / "qualification-records"
STEM = "Q1-deterministic-cv-geometry-2026-09"
PRE_PATH = QR_DIR / f"{STEM}-PREREGISTRATION.yaml"
RESULT_PATH = QR_DIR / f"{STEM}.yaml"
OBS_PATH = QR_DIR / f"{STEM}-observations.jsonl"
R_Q = 3
FAMILIES = ("object_count", "spatial_relationship_2d", "size_aspect", "attribute_binding")
CATEGORY_TO_FAMILY = {"count": "object_count", "relative_position": "spatial_relationship_2d",
                      "absolute_placement": "spatial_relationship_2d", "size_aspect": "size_aspect",
                      "attribute_binding": "attribute_binding"}
CONDITIONS = {
    "render_class": "flat-colour synthetic renders on a white background (constructed by code, no photograph)",
    "frame": "640x480, 8-bit RGB PNG, filter type 0, non-interlaced",
    "palette": "five named sRGB colours + white background + one grey shadow trap (185,185,185)",
    "shapes": "axis-aligned squares, circles and horizontal bars, 45-140 px",
    "degradation_class": "none", "lighting": "none (flat fill)", "language": "not_applicable", "script": "not_applicable",
    "qualified_domain_statement": "the record covers ONLY this synthetic domain; NO transfer to photographic or generated outputs is claimed",
}


class PreregistrationMissing(RuntimeError):
    pass


class PreregistrationMismatch(RuntimeError):
    pass


class RunRefused(RuntimeError):
    pass


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def pack_facts() -> dict:
    manifest_bytes = MANIFEST.read_bytes()
    m = json.loads(manifest_bytes)
    combined = hashlib.sha256()
    for it in m["items"]:
        combined.update(it["sha256"].encode("ascii"))
    baseline = None
    for line in PROTECTED.read_text(encoding="utf-8").splitlines():
        if line.strip().endswith("eval/v1/instruments/fixtures/cv-geometry/manifest.json"):
            baseline = line.split()[0]
    return {"pack_ref": str(MANIFEST.relative_to(hv2_paths.REPO_ROOT)), "pack_version": m["pack"], "pack_seed": m["seed"],
            "manifest_sha256": sha256_bytes(manifest_bytes), "protected_baseline_sha256": baseline,
            "manifest_matches_protected_baseline": baseline == sha256_bytes(manifest_bytes),
            "pack_hash": combined.hexdigest(), "pack_hash_rule": "sha256 over the per-image sha256 strings in manifest order (the exact bytes judged)",
            "items_total": m["counts"]["total"], "scoreable": m["counts"]["scoreable"], "negative_controls": m["counts"]["negative_controls"],
            "by_category": m["by_category"]}


def verify_pack() -> dict:
    r = subprocess.run([sys.executable, str(BUILD_SCRIPT), "--verify"], capture_output=True, text=True, cwd=hv2_paths.REPO_ROOT)
    ok = r.returncode == 0 and "PASS" in r.stdout
    return {"command": "python3 eval/v1/instruments/build_cv_fixtures.py --verify", "exit_code": r.returncode, "pass": ok,
            "last_line": (r.stdout.strip().splitlines() or [""])[-1], "at": now()}


# ------------------------------------------------------------------------------ preregistration
def write_preregistration(path: Path = PRE_PATH) -> Path:
    if path.exists():
        raise RunRefused(f"{path} already exists; a pre-registration is written once, before the run, and never edited")
    if RESULT_PATH.exists() or OBS_PATH.exists():
        raise RunRefused("a result already exists; pre-registering after a run is an experiment mutation")
    facts = pack_facts()
    rec = {
        "record_type": "instrument_qualification_preregistration", "task": "EVAL-039C", "written_utc": now(),
        "written_before_any_run": True, "rule": "R_q, T_rgb and every gate below are fixed here; changing any of them after seeing output is an EXPERIMENT MUTATION stop",
        "R_q": R_Q, "R_q_rule_ref": "eval/v1/instruments/QUALIFICATION-MASTER-SPEC.md#3 (>= 3 full repeats for any status above screened)",
        "instrument_id": D.CONFIG["detector"], "instrument_version": D.CONFIG["version"], "instrument_family": "2",
        "detector_module": "eval/harness-v2/q1/detector.py", "detector_source_sha256": sha256_bytes((HERE / "detector.py").read_bytes()),
        "configuration_hash": D.config_hash(), "configuration": D.CONFIG,
        "T_rgb": {"value": D.CONFIG["T_rgb"], "space": "sRGB 8-bit, Euclidean", "role": "the detector confidence: a pixel is an object pixel only within T_rgb of a palette colour, else background",
                  "declared_here": True, "hash_covered": True,
                  "approval": "FAMILY-2 says the colour tolerance is a judgement call needing Controller approval before the run; none exists tonight, so attribute_binding is reported with qualified: null (MD-C2)"},
        "gate_rules": {
            "ref": "eval/v1/instruments/FAMILY-2-DETERMINISTIC-CV.md#Gate",
            "object_count": "exact agreement of the detected component count with truth.object_count on every count fixture (30) and 0 objects on the blank negative control",
            "spatial_relationship_2d": "exact agreement on truth.relation for every relative_position fixture (25; subject = red square, object = blue circle, dominant-axis rule) and on truth.quadrant for every absolute_placement fixture (15; one object)",
            "size_aspect": "exact agreement on truth.larger (green vs purple by pixel area) and truth.frame_aspect (W:H of the decoded frame) on every size_aspect fixture (15)",
            "attribute_binding": "exact agreement on truth.square_colour and truth.circle_colour on every attribute_binding fixture (15); the colour judgement depends on T_rgb, which needs Controller approval, so qualified is null whatever the agreement",
            "negative_controls": "blank -> exactly 0 objects; corrupt -> ProbeError (fail closed). Either failing disqualifies the WHOLE run",
            "no_tolerance": "counts, relations, quadrants and size orderings are exact; there is no partial credit",
            "supplementary": "object_count agreement on non-count categories is reported as observation only and gates nothing",
        },
        "pack": facts, "conditions": CONDITIONS,
        "output_files": {"result": str(RESULT_PATH.relative_to(hv2_paths.REPO_ROOT)), "observations": str(OBS_PATH.relative_to(hv2_paths.REPO_ROOT))},
        "registry_use": "registry_use_permitted will be false in every record regardless of status; Registry use is a Controller ruling (MD-C2); the result schema is PROPOSED_NOT_IN_FORCE",
        "spend": {"currency": "USD", "amount": 0, "calls": 0, "human_hours": 0},
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# Q1 PRE-REGISTRATION - written before the run; never edited. Task EVAL-039C §4.\n"
                    + yaml.safe_dump(rec, sort_keys=False, allow_unicode=True, width=140), encoding="utf-8")
    return path


def load_preregistration(path: Path = PRE_PATH) -> dict:
    if not Path(path).exists():
        raise PreregistrationMissing(f"no pre-registration at {path}; run --preregister first (R_q is fixed before any output is seen)")
    raw = Path(path).read_bytes()
    rec = yaml.safe_load(raw.decode("utf-8")) or {}
    if rec.get("configuration_hash") != D.config_hash():
        raise PreregistrationMismatch(f"pre-registered configuration_hash {str(rec.get('configuration_hash'))[:12]} != detector {D.config_hash()[:12]}; "
                                      f"the detector changed after pre-registration (experiment mutation)")
    if rec.get("R_q") != R_Q:
        raise PreregistrationMismatch(f"pre-registered R_q {rec.get('R_q')} != runner {R_Q}")
    rec["_sha256"] = sha256_bytes(raw)
    return rec


# ------------------------------------------------------------------------------ judging
def judge(item: dict, png_path: Path) -> dict:
    cat, truth = item["category"], item["truth"]
    out = {"id": item["id"], "category": cat, "family": CATEGORY_TO_FAMILY.get(cat, "negative_control"), "error": None,
           "detected": None, "expected": None, "agree": None, "supplementary_count_agree": None}
    try:
        det = D.detect(png_path.read_bytes())
    except D.ProbeError as exc:
        out["error"] = f"ProbeError: {exc}"
        if cat == "negative_control" and "FAIL CLOSED" in str(truth.get("expected_behaviour", "")):
            out.update({"expected": "ProbeError", "detected": "ProbeError", "agree": True, "family": "negative_control"})
        else:
            out["agree"] = False
        return out
    out["object_count"] = det["object_count"]
    if cat == "negative_control":
        out.update({"expected": truth.get("object_count", "ProbeError"), "detected": det["object_count"],
                    "agree": (truth.get("object_count") == det["object_count"]) if "object_count" in truth else False})
        return out
    if "object_count" in truth:
        out["supplementary_count_agree"] = (det["object_count"] == truth["object_count"])
    if cat == "count":
        out.update({"expected": truth["object_count"], "detected": det["object_count"], "agree": det["object_count"] == truth["object_count"]})
    elif cat == "relative_position":
        rel = D.relation(det, ("square", truth["subject"]["colour"]), ("circle", truth["object"]["colour"]))
        out.update({"expected": truth["relation"], "detected": rel, "agree": rel == truth["relation"]})
    elif cat == "absolute_placement":
        q = D.quadrant(det["objects"][0], det["width"], det["height"]) if det["object_count"] == 1 else None
        out.update({"expected": truth["quadrant"], "detected": q, "agree": q == truth["quadrant"]})
    elif cat == "size_aspect":
        big = D.larger(det, "green", "purple")
        asp = f"{det['width']}:{det['height']}"
        out.update({"expected": {"larger": truth["larger"], "frame_aspect": truth["frame_aspect"]},
                    "detected": {"larger": big, "frame_aspect": asp},
                    "agree": big == truth["larger"] and asp == truth["frame_aspect"]})
    elif cat == "attribute_binding":
        sq = [o["colour"] for o in det["objects"] if o["shape"] == "square"]
        ci = [o["colour"] for o in det["objects"] if o["shape"] == "circle"]
        got = {"square_colour": sq[0] if len(sq) == 1 else None, "circle_colour": ci[0] if len(ci) == 1 else None}
        out.update({"expected": {"square_colour": truth["square_colour"], "circle_colour": truth["circle_colour"]}, "detected": got,
                    "agree": got == {"square_colour": truth["square_colour"], "circle_colour": truth["circle_colour"]}})
    return out


def run(pre: dict) -> dict:
    if RESULT_PATH.exists() or OBS_PATH.exists():
        raise RunRefused(f"{RESULT_PATH.name} / observations already exist; a re-run is a new record id, never an overwrite")
    verify_before = verify_pack()
    facts = pack_facts()
    if not verify_before["pass"] or not facts["manifest_matches_protected_baseline"]:
        raise RunRefused(f"pack verification failed before the run: {verify_before} / {facts['manifest_matches_protected_baseline']}")
    if facts["pack_hash"] != pre["pack"]["pack_hash"]:
        raise RunRefused("pack_hash differs from the pre-registration; the pack changed")
    manifest = json.loads(MANIFEST.read_bytes())
    t0 = time.time()
    observations = []
    with OBS_PATH.open("w", encoding="utf-8") as fh:
        for rep in range(1, R_Q + 1):
            for it in manifest["items"]:
                obs = judge(it, PACK_DIR / it["image"])
                obs.update({"repeat": rep, "image_sha256": it["sha256"], "configuration_hash": D.config_hash(), "at": now()})
                observations.append(obs)
                fh.write(json.dumps(obs, sort_keys=True, ensure_ascii=False) + "\n")
    elapsed = time.time() - t0
    verify_after = verify_pack()
    facts_after = pack_facts()
    return build_result(pre, observations, elapsed, verify_before, verify_after, facts, facts_after, manifest)


def build_result(pre, observations, elapsed, verify_before, verify_after, facts, facts_after, manifest) -> dict:
    by_item: dict = {}
    for o in observations:
        by_item.setdefault(o["id"], []).append(o)
    consistency = {}
    for fam in FAMILIES + ("negative_control",):
        ids = [i for i, obs in by_item.items() if obs[0]["family"] == fam]
        same = sum(1 for i in ids if len({json.dumps(o["detected"], sort_keys=True) for o in by_item[i]}) == 1)
        consistency[fam] = (same / len(ids)) if ids else None
    neg = [o for o in observations if o["family"] == "negative_control"]
    neg_ok = bool(neg) and all(o["agree"] for o in neg)
    blank_ok = all(o["agree"] for o in neg if o["expected"] == 0)
    corrupt_ok = all(o["agree"] for o in neg if o["expected"] == "ProbeError")
    records = []
    for fam in FAMILIES:
        fam_obs = [o for o in observations if o["family"] == fam]
        first = [o for o in fam_obs if o["repeat"] == 1]
        n = len(first)
        agree = sum(1 for o in first if o["agree"])
        disagree = [o for o in first if not o["agree"]]
        refusals = sum(1 for o in first if o["error"])
        no_answer = sum(1 for o in first if o["detected"] is None or (isinstance(o["detected"], dict) and None in o["detected"].values()))
        all_reps_agree = all(o["agree"] for o in fam_obs)
        n_opp = n + (1 if fam == "object_count" else 0)          # the blank control is one more counting opportunity
        gate_pass = all_reps_agree and refusals == 0 and neg_ok and (blank_ok if fam == "object_count" else True)
        if not neg_ok:
            status, qualified, why = "disqualified", False, "a negative control failed: the whole run is disqualified"
        elif not gate_pass:
            status, qualified = "disqualified", False
            why = f"{len(disagree)}/{n} first-pass disagreements: " + "; ".join(f"{o['id']} expected {o['expected']} detected {o['detected']}" for o in disagree[:8])
        elif fam == "attribute_binding":
            status, qualified = "provisional", None
            why = "exact agreement observed, but the colour judgement rests on T_rgb, which FAMILY-2 says needs Controller approval before the run; qualified stays null until MD-C2"
        else:
            status, qualified, why = "qualified", True, f"exact agreement on all {n} items in every one of R_q={R_Q} passes; registry use still needs MD-C2"
        upper = RG.clopper_pearson(len(disagree), n)[1] if n else None
        by_dir = Counter()
        for o in disagree:
            if fam == "object_count" and isinstance(o["detected"], int):
                by_dir["under_count" if o["detected"] < o["expected"] else "over_count"] += 1
            else:
                by_dir["no_answer" if o["detected"] is None else "wrong_answer"] += 1
        records.append({
            "record_id": f"qual_q1_{fam}_2026-09",
            "instrument_id": pre["instrument_id"], "instrument_version": pre["instrument_version"],
            "configuration_hash": pre["configuration_hash"], "instrument_family": "2", "judgement_family": fam,
            "pack_ref": facts["pack_ref"], "pack_version": facts["pack_version"], "pack_hash": facts["pack_hash"],
            "conditions": CONDITIONS,
            "gate": {"n_opportunities": n_opp, "false_passes": len(disagree), "false_fails": 0, "refusals": refusals,
                     "gate_verdict": "pass" if gate_pass else "fail", "gate_rule_ref": "eval/v1/instruments/FAMILY-2-DETERMINISTIC-CV.md#Gate",
                     "gate_mapping_note": "a known-answer geometry pack has agreement/disagreement, not pass/fail on generated work; every disagreement is counted under false_passes (the dangerous direction, conservatively) and false_fails is 0 by construction",
                     "agreements": agree, "disagreements": len(disagree), "disagreement_direction": dict(by_dir),
                     "all_repeats_agree": all_reps_agree, "negative_controls_ok": neg_ok, "n_items": n,
                     "opportunity_note": "one generator made every fixture from one seed; items are NOT independent opportunities"},
            "diagnosis": {"n_scored": n, "correct_class": agree, "wrong_class": len(disagree) - no_answer, "no_class_offered": no_answer,
                          "silent_correction": 0, "note": "the detector never sees the intended answer, so silent correction cannot occur"},
            "repeats": {"full_passes": R_Q, "shapes_covered": [fam], "repeat_consistency": consistency[fam],
                        "consistency_threshold_applied": 1.0, "threshold_status": "PROPOSED_NOT_EMPIRICALLY_BACKED (deterministic code; 1.0 expected)"},
            "reference_calculation": {"iid_reference_upper_bound_95pct": upper, "independence_status": "NOT ESTABLISHED",
                                      "caveat": "Clopper-Pearson upper bound on the disagreement rate over items under an iid model the pack does not establish; a sizing reference, NOT the detector's real-world error rate"},
            "blind_check": {"required": False, "performed_before_run": True, "method": "the detector API takes image bytes only; truth is read by the runner after detection (code inspection of q1/run_q1.py judge())", "result": "clean"},
            "human_reference": {"used": False, "n_reviewers": 0, "qualification": "none", "what_the_human_decided": "nothing - truth is constructed by code", "epistemic_status": "ground truth by construction (build_cv_fixtures.py, seed 20260826)"},
            "status": status, "qualified": qualified, "status_reason": why,
            "registry_use_permitted": False, "controller_ratification_required": "MD-C2",
            "qualified_date": datetime.now(timezone.utc).date().isoformat() if status == "qualified" else None,
            "requalification_triggers": ["instrument_version_change", "configuration_hash_change", "pack_version_change", "conditions_outside_qualified_range", "scheduled_interval_elapsed"],
            "cost": {"calls": 0, "currency": "USD", "spend": 0, "human_hours": 0},
        })
    supp = [o for o in observations if o["repeat"] == 1 and o["supplementary_count_agree"] is not None]
    result = {
        "record_type": "instrument_qualification", "schema_ref": str(SCHEMA.relative_to(hv2_paths.REPO_ROOT)),
        "schema_status": "PROPOSED_NOT_IN_FORCE", "task": "EVAL-039C", "run_utc": now(),
        "preregistration": {"path": str(PRE_PATH.relative_to(hv2_paths.REPO_ROOT)), "sha256": pre["_sha256"], "R_q": pre["R_q"], "T_rgb": pre["T_rgb"]["value"]},
        "run": {"elapsed_s": round(elapsed, 2), "under_10_minutes": elapsed < 600, "items_per_pass": len(manifest["items"]), "passes": R_Q,
                "observations": str(OBS_PATH.relative_to(hv2_paths.REPO_ROOT)), "n_observations": len(observations),
                "verify_before": verify_before, "verify_after": verify_after,
                "manifest_sha256_before": facts["manifest_sha256"], "manifest_sha256_after": facts_after["manifest_sha256"],
                "manifest_unchanged": facts["manifest_sha256"] == facts_after["manifest_sha256"] == facts["protected_baseline_sha256"],
                "python": sys.version.split()[0], "spend_usd": 0},
        "negative_controls": {"blank_gives_zero_objects": blank_ok, "corrupt_fails_closed": corrupt_ok, "all_ok": neg_ok,
                              "repeat_consistency": consistency["negative_control"]},
        "supplementary_observation": {"object_count_agreement_on_non_count_categories": f"{sum(1 for o in supp if o['supplementary_count_agree'])}/{len(supp)}",
                                      "gates_nothing": True},
        "qualified_domain": CONDITIONS["qualified_domain_statement"],
        "records": records,
    }
    return result


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--preregister", action="store_true")
    ap.add_argument("--run", action="store_true")
    a = ap.parse_args(argv)
    if a.preregister:
        p = write_preregistration()
        print(f"pre-registration written: {p} (config {D.config_hash()[:12]}, R_q={R_Q}, T_rgb={D.CONFIG['T_rgb']})")
    if a.run:
        pre = load_preregistration()
        result = run(pre)
        RESULT_PATH.write_text("# Q1 qualification result - one record per judgement family; registry_use_permitted is false in every record (MD-C2).\n"
                               + yaml.safe_dump(result, sort_keys=False, allow_unicode=True, width=140), encoding="utf-8")
        for r in result["records"]:
            print(f"{r['judgement_family']:26s} status={r['status']:13s} qualified={r['qualified']} agree={r['gate']['agreements']}/{r['gate']['n_items']} refusals={r['gate']['refusals']}")
        print(f"negative controls ok={result['negative_controls']['all_ok']} elapsed={result['run']['elapsed_s']}s manifest_unchanged={result['run']['manifest_unchanged']}")
        print(f"result: {RESULT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
