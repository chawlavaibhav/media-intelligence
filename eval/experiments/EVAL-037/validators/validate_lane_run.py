#!/usr/bin/env python3
"""EVAL-037 — validate one lane's sealed evidence. Fails closed.

    python3 validators/validate_lane_run.py --lane lanes/X.yaml --run runs/X
"""
import argparse
import hashlib
import json
import pathlib
import subprocess
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent
PKG = HERE.parent
REPO = PKG.parents[2]
sys.path.insert(0, str(PKG / "tools"))
from jsonschema_mini import validate            # noqa: E402
import providers as P                           # noqa: E402

FULL_FP = "cbd321aa3be7464e785a0d42de1764cdccc8bdd33bc023a376740f8f196bde60"
QA_FP = "1313c0babe2194a7bc71c1628f9fbec5fa4f35ca5ff5edc7f594662101dc62bd"
CANON_BASE = "c6f8d910f7a3cdaaeafa2280313abfb9b898cddd"
WEB_BRIEFS = {"B01", "B02"}
MEDIA_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".mp4", ".mov", ".webm",
             ".mp3", ".wav", ".m4a", ".avi", ".mkv"}
FAILURES = []
GATES = {"n": 0}


def gate(name, ok, detail=""):
    GATES["n"] += 1
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        FAILURES.append(name)
    return ok


def order_key(t):
    return hashlib.sha256(("EVAL-037|" + t).encode()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--run", required=True)
    a = ap.parse_args()
    lane = yaml.safe_load(pathlib.Path(a.lane).read_text(encoding="utf-8"))
    run = pathlib.Path(a.run)
    result = json.loads((run / "result.json").read_text())
    ledger = json.loads((run / "attempt-ledger.json").read_text())
    lid = lane["lane_id"]
    print(f"EVAL-037 lane-run validation — {lid}\n")

    res_s = json.loads((PKG / "schemas/result.schema.json").read_text())
    led_s = json.loads((PKG / "schemas/attempt-ledger.schema.json").read_text())
    gate("R1  result.json matches its schema", not validate(result, res_s),
         "; ".join(validate(result, res_s)[:2]))
    gate("R2  attempt-ledger.json matches its schema", not validate(ledger, led_s),
         "; ".join(validate(ledger, led_s)[:2]))

    # ---- order -------------------------------------------------------------
    declared = [t["trial_id"] for t in lane["execution"]["trials_plan"]]
    got = [t["trial_id"] for t in result["trials"]]
    expected = sorted(declared, key=order_key)
    gate("R3  18 trials, executed in the RECOMPUTED SHA-256 order",
         got == declared == expected and len(got) == 18, f"{len(got)} trials")

    by_trial = {}
    for at in ledger["attempts"]:
        by_trial.setdefault(at["trial_id"], []).append(at)
    gate("R4  every trial has attempts; every attempt belongs to a declared trial",
         all(by_trial.get(t) for t in declared) and set(by_trial) <= set(declared))

    # ---- retry discipline ---------------------------------------------------
    ok5 = ok6 = ok7 = ok8 = ok9 = True
    for t in result["trials"]:
        atts = sorted(by_trial.get(t["trial_id"], []), key=lambda x: x["attempt_index"])
        for i, at in enumerate(atts):
            if at["attempt_kind"] in ("technical_retry", "format_repair_technical_retry"):
                prev = atts[i - 1] if i else None
                ok5 &= (prev is not None
                        and prev["outcome"] == "transient_failure"
                        and prev.get("failure_is_transient") is True
                        and prev.get("failure_class") in P.TRANSIENT_CLASSES)
            # a deterministic failure must be the LAST attempt of its trial
            if at["outcome"] == "deterministic_failure":
                ok6 &= (i == len(atts) - 1
                        and at.get("failure_class") in P.DETERMINISTIC_CLASSES
                        and at.get("failure_is_transient") is False)
        ok7 &= sum(1 for x in atts if x["attempt_kind"] == "format_repair") <= 1
        ok8 &= all(x.get("fresh_context") is True for x in atts)
        creative = [x for x in atts if x["phase"] == "creative"]
        repair = [x for x in atts if x["phase"] == "repair"]
        # a retry resends the IDENTICAL request within its phase
        ok9 &= len({x["request_digest"] for x in creative}) <= 1
        ok9 &= len({x["request_digest"] for x in repair}) <= 1
    gate("R5  every retry follows a TRANSIENT failure with a named class", ok5)
    gate("R6  deterministic failures are never followed by another attempt", ok6)
    gate("R7  at most one format repair per trial", ok7)
    gate("R8  every attempt declares fresh_context: true", ok8)
    gate("R9  retries resend an identical request within their phase", ok9)

    # ---- format repair contract --------------------------------------------
    ok10 = ok11 = True
    for t in result["trials"]:
        reps = [x for x in by_trial.get(t["trial_id"], []) if x["phase"] == "repair"]
        if not reps:
            ok10 &= t["status"] not in ("format_repaired", "failed_format")
            continue
        prior = [x for x in by_trial[t["trial_id"]] if x["phase"] == "creative"
                 and x.get("response_digest")]
        src = reps[0].get("repair_source_response_digest")
        ok10 &= bool(src) and bool(prior) and src == prior[-1]["response_digest"]
        # the repair request on disk must actually CONTAIN the original answer
        rp = run / reps[0]["request_path"]
        if rp.exists():
            body = json.dumps(json.loads(rp.read_text()), default=str)
            raw_prev = run / prior[-1]["raw_response_path"]
            ok11 &= ("BEGIN YOUR PREVIOUS RESPONSE" in body
                     and "unchanged in substance" in body and raw_prev.exists())
        else:
            ok11 = False
    gate("R10 every repair records the digest of the answer it repairs", ok10)
    gate("R11 every repair request on disk carries the original answer verbatim", ok11)
    gate("R12 an invalid repair is failed_format and NOT eligible; never 'repaired'",
         all(t["eligible_for_media_generation"] is False
             for t in result["trials"] if t["status"] == "failed_format")
         and all(t["status"] != "format_repaired"
                 for t in result["trials"] if t["status"] == "failed_format"))

    # ---- retention / no media ------------------------------------------------
    gate("R13 every produced package is retained on disk",
         all((run / t["package_path"]).exists()
             for t in result["trials"] if t["package_path"]))
    gate("R14 the EXACT serialised request is retained for every attempt",
         all((run / at["request_path"]).exists() for at in ledger["attempts"]))
    media = [p for p in run.rglob("*") if p.suffix.lower() in MEDIA_EXT]
    gate("R15 no media artefacts under the run directory", not media,
         f"found {[p.name for p in media[:3]]}" if media else "")

    # ---- usage / cost ---------------------------------------------------------
    ok16 = ok17 = True
    for t in result["trials"]:
        turns = [tn for at in by_trial[t["trial_id"]] for tn in (at.get("provider_turns") or [])]
        ok16 &= t["usage_totals"]["provider_turns"] == len(turns)
        for f in ("input_tokens", "output_tokens", "reasoning_tokens", "cached_input_tokens"):
            vals = [tn[f] for tn in turns if tn.get(f) is not None]
            want = sum(vals) if vals else None
            ok17 &= t["usage_totals"].get(f) == want
    gate("R16 trial totals count EVERY provider turn, tool turns included", ok16)
    gate("R17 trial token totals equal the sum over all provider turns", ok17)
    lane_turns = [tn for at in ledger["attempts"] for tn in (at.get("provider_turns") or [])]
    gate("R18 lane totals equal the sum over every attempt's turns",
         result["lane_usage_totals"]["provider_turns"] == len(lane_turns))
    canon_multi = [t for t in result["trials"] if t["canon_tool_calls"] > 0]
    gate("R19 Canon trials record more than one provider turn (retrieval cost counted)",
         all(t["usage_totals"]["provider_turns"] > 1 for t in canon_multi)
         if canon_multi else True, f"{len(canon_multi)} canon trials")
    gate("R20 cost is computed or explicitly null with a stated basis",
         all(t.get("cost_basis") for t in result["trials"])
         and all(t["calculated_cost_usd"] is not None or t["cost_basis"] != "computed"
                 for t in result["trials"]))

    # ---- Canon transcript ------------------------------------------------------
    if result["condition"] == "NO_CANON":
        gate("R21 NO_CANON: zero Canon tool calls, no fingerprints recorded",
             all(t["canon_tool_calls"] == 0 and t["canon_used"] is None
                 for t in result["trials"]) and "canon_fingerprints" not in result)
    else:
        fps = result.get("canon_fingerprints", {})
        calls = [tc for at in ledger["attempts"] for tc in (at.get("tool_calls") or [])
                 if tc.get("tool_family") == "canon"]
        stat_ok = all(tc.get("every_item_carried_source_status") is True for tc in calls)
        args_ok = all(isinstance(tc.get("arguments"), dict) for tc in calls)
        refs_ok = all("retrieved_refs" in tc for tc in calls)
        ident_ok = all(r.get("source_status") in ("ACCEPTED", "HOLD")
                       for tc in calls for r in tc.get("retrieved_refs", []))
        resolvable = True
        for at in ledger["attempts"]:
            for tc in (at.get("tool_calls") or []):
                ref = tc.get("transcript_ref")
                if not ref:
                    resolvable = False; continue
                path, _, line = ref.partition("#")
                f = run / path
                if not f.exists():
                    resolvable = False; continue
                rows = f.read_text().splitlines()
                if int(line) >= len(rows) or json.loads(rows[int(line)]).get("full_result") is None:
                    resolvable = False
        gate("R22 FULL_CANON: fingerprints match and every item carried source_status",
             fps.get("full_knowledge") == FULL_FP and fps.get("qa") == QA_FP and stat_ok)
        gate("R23 every Canon call retains its REAL arguments, not only a hash", args_ok)
        gate("R24 every Canon call retains per-item identity (id, source, status, kind)",
             refs_ok and ident_ok)
        gate("R25 every transcript_ref resolves to a retained full tool result",
             resolvable)

    # ---- website ---------------------------------------------------------------
    man = yaml.safe_load(
        (PKG / "common/websites/WEBSITE-SNAPSHOT-MANIFEST.yaml").read_text())
    sealed = {s["files"]["page.txt"]["sha256"] for s in man["sites"]}
    noweb = [t for t in result["trials"] if t["brief_id"] not in WEB_BRIEFS]
    web = [t for t in result["trials"] if t["brief_id"] in WEB_BRIEFS]
    gate("R26 B03–B06 have no website tool and no website access",
         all(t["website_tool_exposed"] is False and t["website_tool_calls"] == 0
             and t["website_snapshot_used"] is False for t in noweb))
    gate("R27 B01/B02 have the website tool exposed",
         all(t["website_tool_exposed"] is True for t in web))
    gate("R28 website_snapshot_used is DERIVED from calls, never hardcoded",
         all(t["website_snapshot_used"] == (t["website_tool_calls"] > 0)
             for t in result["trials"]))
    served = {d for t in result["trials"] for d in t["website_snapshot_digests"]}
    gate("R29 every served snapshot digest matches the sealed manifest",
         served <= sealed, f"served={len(served)}")
    wcalls = [tc for at in ledger["attempts"] for tc in (at.get("tool_calls") or [])
              if tc.get("tool_family") == "website"]
    gate("R30 every website call records its digest and asserts no live browsing",
         all(tc.get("snapshot_sha256") in sealed and tc.get("live_browsing") is False
             for tc in wcalls), f"{len(wcalls)} calls")

    # ---- REQUIRED_CANON treatment (supplemental lanes only) ----------------------
    if result.get("treatment") == "REQUIRED_CANON":
        ok34 = ok35 = ok36 = ok37 = True
        for t in result["trials"]:
            calls = [tc for at in by_trial.get(t["trial_id"], [])
                     for tc in (at.get("tool_calls") or [])
                     if tc.get("tool_family") == "canon"]
            searches = [tc for tc in calls if tc.get("name") == "canon_search"]
            reads = [tc for tc in calls if tc.get("name") == "canon_read"]
            # the compliance flag is DERIVED from the transcript, never asserted
            derived = bool(searches) and bool(reads)
            ok34 &= t.get("required_canon_use_satisfied") is derived
            ok34 &= t.get("canon_search_calls") == len(searches)
            ok34 &= t.get("canon_read_calls") == len(reads)
            # catalog alone must never register as compliance
            if not searches and not reads:
                ok35 &= t.get("required_canon_use_satisfied") is False
            # A violation is recorded, retained, and never resampled — but the gate
            # speaks only about a trial the model actually COMPLETED. A provider
            # failure keeps its own status: the model never got its chance to comply,
            # and relabelling a transport fault as non-compliance would misreport it.
            atts = by_trial.get(t["trial_id"], [])
            if not derived and t["format_outcome"] in ("complete", "format_repaired",
                                                       "failed_format"):
                ok36 &= (t["status"] == "failed_required_canon_use"
                         and t["eligible_for_media_generation"] is False)
                # no extra creative attempt was bought by non-compliance
                creative_ok = [x for x in atts if x["phase"] == "creative"
                               and x["outcome"] == "ok"]
                ok36 &= len(creative_ok) <= 1
            elif not derived:
                # provider failure: its own status stands, unmasked by the gate
                ok36 &= t["status"] == t["format_outcome"] != "failed_required_canon_use"
            else:
                ok36 &= t["status"] != "failed_required_canon_use"
            # in NO case does non-compliance buy a retry that was not transient-licensed
            ok36 &= all(x["attempt_kind"] not in ("technical_retry",
                                                  "format_repair_technical_retry")
                        or x.get("failure_is_transient") is not False for x in atts)
            # the model composed its own query; the harness curated nothing
            for tc in searches:
                q = (tc.get("arguments") or {}).get("query")
                ok37 &= isinstance(q, str) and bool(q.strip())
        gate("R34 required-Canon compliance is DERIVED from the transcript, not asserted",
             ok34)
        gate("R35 canon_catalog alone never counts as Canon use", ok35)
        gate("R36 a non-compliant trial is retained, marked, and never resampled", ok36)
        gate("R37 every canon_search carries the model's OWN non-empty query", ok37)
        addendum = (PKG / "conditions/full-canon-required.yaml").read_text()
        base = yaml.safe_load((PKG / "conditions/full-canon.yaml").read_text())["addendum"]
        req = yaml.safe_load(addendum)["addendum"]
        gate("R38 the treatment addendum contains the frozen FULL_CANON text verbatim",
             req.startswith(base.rstrip("\n"))
             and "using the Canon library is required" in req)

    # ---- substrate identity ------------------------------------------------------
    sub = result["substrate"]
    gate("R31 substrate identity records the fingerprint and names the Canon commit "
         "as provenance only",
         sub["canon_base_commit"] == CANON_BASE
         and len(sub["freeze_fingerprint"]) == 64
         and sub["execution_commit"] != CANON_BASE)
    contains = subprocess.run(["git", "ls-tree", "-r", "--name-only", CANON_BASE,
                               "eval/experiments/EVAL-037/"], cwd=REPO,
                              capture_output=True, text=True).stdout.strip()
    gate("R32 the recorded Canon commit provably does NOT contain EVAL-037",
         contains == "")
    rc = ledger["runner_commit"]
    gate("R33 runner_commit is a real commit (runner frozen before first call)",
         subprocess.run(["git", "cat-file", "-e", f"{rc}^{{commit}}"], cwd=REPO,
                        capture_output=True).returncode == 0, rc[:12])

    print()
    if FAILURES:
        print(f"LANE-RUN VALIDATION FAILED — {len(FAILURES)} gate(s): {', '.join(FAILURES)}")
        return 1
    print(f"LANE-RUN VALIDATION PASSED — all {GATES['n']} gates green")
    return 0


if __name__ == "__main__":
    sys.exit(main())
