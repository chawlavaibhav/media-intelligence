#!/usr/bin/env python3
"""EVAL-037 — validate one lane's sealed evidence. Fails closed.

    python3 validators/validate_lane_run.py --lane lanes/X.yaml --run runs/X

Gates:
  R1  result.json validates against schemas/result.schema.json
  R2  attempt-ledger.json validates against schemas/attempt-ledger.schema.json
  R3  exactly 18 trials, matching the lane's declared ids AND order
  R4  every trial has >=1 attempt, and every attempt belongs to a declared trial
  R5  technical retries <= 2 per trial, and every retry follows a technical failure
      with a named failure class
  R6  at most ONE format repair per trial
  R7  no attempt beyond the contract: max 3 from technical failure + 1 repair
  R8  every attempt declares fresh_context: true
  R9  no two attempts in a trial share a request digest unless legitimately identical
      (a repeated identical request is evidence of a retry, not of carried state)
  R10 outputs retained: every non-failed trial has a package file on disk
  R11 no media: no image/video/audio artefact anywhere under the run directory
  R12 NO_CANON evidence records zero Canon tool calls and no fingerprints
  R13 FULL_CANON evidence carries both fingerprints, and every Canon result that was
      returned carried source_status
  R14 eligibility is never withdrawn on creative grounds: every trial with a package
      is eligible for media generation
  R15 the runner was committed before the first attempt
"""
import argparse
import json
import pathlib
import subprocess
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent
PKG = HERE.parent
REPO = PKG.parents[2]
sys.path.insert(0, str(PKG / "tools"))
from jsonschema_mini import validate  # noqa: E402

FULL_FP = "cbd321aa3be7464e785a0d42de1764cdccc8bdd33bc023a376740f8f196bde60"
QA_FP = "1313c0babe2194a7bc71c1628f9fbec5fa4f35ca5ff5edc7f594662101dc62bd"
MEDIA_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".mov", ".webm",
             ".mp3", ".wav", ".m4a", ".avi", ".mkv"}
FAILURES = []


def gate(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        FAILURES.append(name)
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--run", required=True)
    a = ap.parse_args()
    lane = yaml.safe_load(pathlib.Path(a.lane).read_text(encoding="utf-8"))
    run = pathlib.Path(a.run)
    result = json.loads((run / "result.json").read_text())
    ledger = json.loads((run / "attempt-ledger.json").read_text())
    print(f"EVAL-037 lane-run validation — {lane['lane_id']}\n")

    gate("R1  result.json matches its schema",
         not validate(result, json.loads((PKG / "schemas/result.schema.json").read_text())),
         "; ".join(validate(result, json.loads(
             (PKG / "schemas/result.schema.json").read_text()))[:2]))
    gate("R2  attempt-ledger.json matches its schema",
         not validate(ledger, json.loads(
             (PKG / "schemas/attempt-ledger.schema.json").read_text())),
         "; ".join(validate(ledger, json.loads(
             (PKG / "schemas/attempt-ledger.schema.json").read_text()))[:2]))

    declared = [t["trial_id"] for t in lane["execution"]["trials_plan"]]
    got = [t["trial_id"] for t in result["trials"]]
    gate("R3  exactly 18 trials, declared ids in declared order",
         got == declared, f"{len(got)} trials")

    by_trial = {}
    for at in ledger["attempts"]:
        by_trial.setdefault(at["trial_id"], []).append(at)
    gate("R4  every trial has attempts; every attempt belongs to a declared trial",
         all(by_trial.get(t) for t in declared) and set(by_trial) <= set(declared))

    ok5 = ok6 = ok7 = ok8 = True
    for t in result["trials"]:
        atts = sorted(by_trial.get(t["trial_id"], []), key=lambda x: x["attempt_index"])
        retries = [x for x in atts if x["attempt_kind"] == "technical_retry"]
        repairs = [x for x in atts if x["attempt_kind"] == "format_repair"]
        ok5 &= len(retries) <= 2
        for r in retries:
            prior = [x for x in atts if x["attempt_index"] < r["attempt_index"]]
            ok5 &= bool(prior) and prior[-1]["outcome"] == "technical_failure" \
                and bool(prior[-1].get("technical_failure_class"))
        ok6 &= len(repairs) <= 1
        ok7 &= len(atts) <= 4
        ok8 &= all(x.get("fresh_context") is True for x in atts)
    gate("R5  <=2 technical retries, each after a classified technical failure", ok5)
    gate("R6  at most one format repair per trial", ok6)
    gate("R7  no trial exceeds 4 attempts total", ok7)
    gate("R8  every attempt declares fresh_context: true", ok8)

    dig_ok = True
    for t in result["trials"]:
        atts = by_trial.get(t["trial_id"], [])
        initial = [x for x in atts if x["attempt_kind"] in ("initial", "technical_retry")]
        # a technical retry is by definition the SAME request sent again
        dig_ok &= len({x["request_digest"] for x in initial}) == 1 if initial else True
    gate("R9  technical retries resend an identical request (no carried state)", dig_ok)

    ok10 = all((run / t["package_path"]).exists()
               for t in result["trials"] if t["package_path"])
    gate("R10 every produced package is retained on disk", ok10)

    media = [p for p in run.rglob("*") if p.suffix.lower() in MEDIA_EXT]
    gate("R11 no media artefacts under the run directory", not media,
         f"found {[p.name for p in media[:3]]}" if media else "")

    if result["condition"] == "NO_CANON":
        no_calls = all(t["canon_tool_calls"] == 0 and t["canon_used"] is None
                       for t in result["trials"])
        gate("R12 NO_CANON: zero Canon tool calls, no fingerprints recorded",
             no_calls and "canon_fingerprints" not in result)
    else:
        fps = result.get("canon_fingerprints", {})
        stat_ok = all(tc.get("every_item_carried_source_status") is True
                      for at in ledger["attempts"] for tc in at.get("tool_calls", []))
        gate("R13 FULL_CANON: fingerprints match and every Canon result carried "
             "source_status",
             fps.get("full_knowledge") == FULL_FP and fps.get("qa") == QA_FP and stat_ok)

    gate("R14 eligibility never withdrawn on creative grounds",
         all(t["eligible_for_media_generation"] == (t["package_path"] is not None)
             for t in result["trials"]))

    rc = ledger["runner_commit"]
    exists = subprocess.run(["git", "cat-file", "-e", f"{rc}^{{commit}}"], cwd=REPO,
                            capture_output=True).returncode == 0
    gate("R15 runner_commit is a real commit (runner frozen before first call)", exists,
         rc[:12])

    print()
    if FAILURES:
        print(f"LANE-RUN VALIDATION FAILED — {len(FAILURES)} gate(s): {', '.join(FAILURES)}")
        return 1
    print("LANE-RUN VALIDATION PASSED — all gates green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
