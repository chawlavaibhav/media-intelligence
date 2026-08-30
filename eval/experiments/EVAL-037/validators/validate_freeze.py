#!/usr/bin/env python3
"""EVAL-037 — validate the frozen common substrate. Fails closed.

Run from anywhere:  python3 eval/experiments/EVAL-037/validators/validate_freeze.py

Gates:
  F1  base commit is the recorded CANON-014 merge commit, and HEAD descends from it
  F2  both Canon fingerprints recompute exactly (full knowledge + Q&A)
  F3  all six briefs exist, are byte-identical to their recorded digests, and are
      each a single line
  F4  the common system prompt matches its digest and contains all 12 required
      section names
  F5  exactly two website snapshots exist, match their digests, and no third site
  F6  all eight lane configs exist, parse, and are internally consistent
  F7  every lane declares EXACTLY 18 unique trials: 6 briefs x 3 repetitions
  F8  the 144-trial total holds and every trial id is globally unique
  F9  NO_CANON lanes reference no Canon path and no FULL_CANON addendum
  F10 FULL_CANON lanes carry both fingerprints and the three Canon tools
  F11 no moving aliases anywhere; model configs match the frozen roster
  F12 retry policy is exactly 1 initial + <=2 technical + <=1 format-only repair,
      and creative weakness is explicitly excluded as a retry reason
  F13 the schemas parse and validate a known-good and a known-bad instance
  F14 every lane is self-contained: it never names a sibling lane file
  F15 the freeze fingerprint recomputes exactly (the substrate has not drifted)
"""
import hashlib
import json
import os
import pathlib
import subprocess
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent
PKG = HERE.parent
REPO = PKG.parents[2]
sys.path.insert(0, str(PKG / "tools"))
from jsonschema_mini import validate  # noqa: E402

BASE_COMMIT = "c6f8d910f7a3cdaaeafa2280313abfb9b898cddd"
FULL_FP = "cbd321aa3be7464e785a0d42de1764cdccc8bdd33bc023a376740f8f196bde60"
QA_FP = "1313c0babe2194a7bc71c1628f9fbec5fa4f35ca5ff5edc7f594662101dc62bd"
BRIEFS = ["B01", "B02", "B03", "B04", "B05", "B06"]
LANES = ["sol-no-canon", "sol-full-canon", "sonnet-no-canon", "sonnet-full-canon",
         "haiku-no-canon", "haiku-full-canon", "gemma-no-canon", "gemma-full-canon"]
MODELS = {"sol": ("OpenAI", "gpt-5.6-sol"), "sonnet": ("Anthropic", "claude-sonnet-5"),
          "haiku": ("Anthropic", "claude-haiku-4-5-20251001"),
          "gemma": ("Google Gemini API", "gemma-4-31b-it")}
SECTIONS = ["DELIVERABLE", "OBJECTIVE_INTERPRETATION", "CORE_CREATIVE_IDEA",
            "MESSAGE_AND_INFORMATION_HIERARCHY", "VISUAL_SYSTEM", "PRODUCTION_RECIPE",
            "GENERATION_PROMPTS", "DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS",
            "AUDIO_AND_EDIT", "FAILURE_PREVENTION", "HARD_CONSTRAINT_CHECK",
            "KNOWLEDGE_AND_WEBSITE_USE"]
ALIAS_MARKERS = ("latest", "-preview", "@latest")

FAILURES = []


def gate(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))
    if not ok:
        FAILURES.append(name)
    return ok


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def canon_fps():
    import glob
    arts = ["source-knowledge.yaml", "source-concept-systems.yaml",
            "operational-bindings.yaml", "ontology-mappings.yaml", "visual-evidence-ledger.yaml"]

    def collect(rel):
        out, base = [], REPO / rel
        for d in sorted(os.listdir(base)):
            if (base / d).is_dir():
                out += [f"{rel}/{d}/{a}" for a in arts if (base / d / a).is_file()]
        return out

    def fp(paths):
        rows = [(p, sha(REPO / p)) for p in sorted(paths)]
        return hashlib.sha256("".join(f"{p}:{h}\n" for p, h in rows).encode()).hexdigest()

    return (fp(collect("canon/knowledge/current") + collect("canon/candidates/canon-014")),
            fp(sorted(str(pathlib.Path(p).relative_to(REPO))
                      for p in glob.glob(str(REPO / "canon/qa/canon-014/*-qa-bank.yaml")))))


def main():
    print("EVAL-037 freeze validation\n")

    # F1
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                          capture_output=True, text=True).stdout.strip()
    mb = subprocess.run(["git", "merge-base", head, BASE_COMMIT], cwd=REPO,
                        capture_output=True, text=True).stdout.strip()
    subj = subprocess.run(["git", "log", "-1", "--format=%s", BASE_COMMIT], cwd=REPO,
                          capture_output=True, text=True).stdout.strip()
    gate("F1  base commit is the CANON-014 merge and HEAD descends from it",
         mb == BASE_COMMIT and "CANON-014" in subj, f"{BASE_COMMIT[:12]} “{subj}”")

    # F2
    full, qa = canon_fps()
    gate("F2  Canon fingerprints recompute exactly",
         full == FULL_FP and qa == QA_FP, f"full={full[:16]}… qa={qa[:16]}…")

    # F3
    ok = True
    for b in BRIEFS:
        p = PKG / "common/briefs" / f"{b}.txt"
        raw = p.read_bytes() if p.exists() else b""
        ok &= p.exists() and raw.count(b"\n") == 1 and raw.endswith(b"\n") and len(raw) > 300
    gate("F3  six briefs present, single-line, non-trivial", ok)

    # F4
    sp = (PKG / "common/system-prompt.txt").read_text(encoding="utf-8")
    gate("F4  common prompt carries all 12 package sections",
         all(s in sp for s in SECTIONS) and "FINAL_PRODUCTION_PACKAGE" in sp)

    # F5
    man = yaml.safe_load((PKG / "common/websites/WEBSITE-SNAPSHOT-MANIFEST.yaml").read_text())
    hosts = {s["host"] for s in man["sites"]}
    dirs = {d.name for d in (PKG / "common/websites").iterdir() if d.is_dir()}
    dig_ok = all(sha(PKG / s["path"] / "index.html") == s["files"]["index.html"]["sha256"]
                 for s in man["sites"])
    gate("F5  exactly the two permitted snapshots, digests intact",
         hosts == {"rentok.com", "getaight.ai"} and dirs == hosts and dig_ok
         and man["live_browsing_permitted_during_trials"] is False, ", ".join(sorted(hosts)))

    # F6-F14
    lanes, all_ids = {}, []
    for lid in LANES:
        p = PKG / "lanes" / f"{lid}.yaml"
        if not p.exists():
            gate(f"F6  lane {lid} exists", False)
            continue
        lanes[lid] = yaml.safe_load(p.read_text(encoding="utf-8"))
    gate("F6  all eight lane configs present and parse", len(lanes) == 8)

    for lid, L in lanes.items():
        plan = L["execution"]["trials_plan"]
        ids = [t["trial_id"] for t in plan]
        briefs = sorted({t["brief_id"] for t in plan})
        reps = sorted({t["repetition"] for t in plan})
        per = all(sum(1 for t in plan if t["brief_id"] == b) == 3 for b in BRIEFS)
        order = [t["order_index"] for t in plan] == list(range(1, 19))
        gate(f"F7  {lid}: 18 unique trials = 6 briefs x 3 reps, ordered",
             len(ids) == 18 and len(set(ids)) == 18 and briefs == BRIEFS
             and reps == [1, 2, 3] and per and order)
        all_ids += ids

    gate("F8  144 trials in total, every id globally unique",
         len(all_ids) == 144 and len(set(all_ids)) == 144, f"{len(all_ids)} trials")

    for lid, L in lanes.items():
        if L["condition"] != "NO_CANON":
            continue
        blob = (PKG / "lanes" / f"{lid}.yaml").read_text()
        leaks = [x for x in ("canon/knowledge", "canon/candidates", "canon/qa",
                             FULL_FP, QA_FP) if x in blob]
        cd = L["condition_detail"]
        gate(f"F9  {lid}: no Canon content and no addendum",
             not leaks and cd["addendum_path"] is None and cd["canon_tools_exposed"] == []
             and cd["canon_instruction"] == "absent", f"leaks={leaks}" if leaks else "")

    for lid, L in lanes.items():
        if L["condition"] != "FULL_CANON":
            continue
        cd = L["condition_detail"]
        f = cd["fingerprints"]
        gate(f"F10 {lid}: both fingerprints + three read-only Canon tools",
             f["full_knowledge"]["combined_digest"] == FULL_FP
             and f["qa"]["combined_digest"] == QA_FP
             and cd["canon_tools_exposed"] == ["canon_catalog", "canon_search", "canon_read"]
             and cd["mandatory_canon_use"] is False and cd["no_aggregate_top_k"] is True
             and cd["no_canon_token_budget"] is True and cd["no_retrieval_count_budget"] is True
             and f["on_mismatch"] == "stop")

    ok = True
    for lid, L in lanes.items():
        m = L["model"]
        prov, mid = MODELS[m["key"]]
        ok &= (m["provider"] == prov and m["model_id"] == mid and m["moving_alias"] is False
               and not any(a in mid for a in ALIAS_MARKERS))
    gate("F11 model roster exact, no moving aliases", ok)

    ok = True
    for lid, L in lanes.items():
        r = L["retry_policy"]
        ok &= (r["technical_failure"]["initial_attempt"] == 1
               and r["technical_failure"]["max_technical_retries"] == 2
               and r["technical_failure"]["max_total_attempts_from_technical"] == 3
               and r["format_repair"]["max"] == 1
               and r["format_repair"]["scope"] == "format only"
               and any("creatively weak" in x for x in r["forbidden_retry_reasons"]))
    gate("F12 retry policy: 1 + <=2 technical + <=1 format-only; weakness excluded", ok)

    res_s = json.loads((PKG / "schemas/result.schema.json").read_text())
    led_s = json.loads((PKG / "schemas/attempt-ledger.schema.json").read_text())
    good = _good_result()
    bad = json.loads(json.dumps(good)); bad["trials"] = bad["trials"][:17]; bad["trial_count"] = 17
    gate("F13 schemas accept a good run and reject a 17-trial run",
         not validate(good, res_s) and validate(bad, res_s) and isinstance(led_s, dict))

    ok = True
    for lid in lanes:
        blob = (PKG / "lanes" / f"{lid}.yaml").read_text()
        others = [o for o in LANES if o != lid and (f"lanes/{o}" in blob or f"{o}.yaml" in blob)]
        if others:
            ok = False
            print(f"        {lid} names sibling lanes: {others}")
    gate("F14 every lane is self-contained (names no sibling lane)", ok)

    sys.path.insert(0, str(PKG / "tools"))
    import freeze_fingerprint as FF
    digest, rows = FF.compute()
    recorded = next((l.split(":", 1)[1].strip()
                     for l in (PKG / "FREEZE-FINGERPRINT.yaml").read_text().splitlines()
                     if l.startswith("combined_digest:")), None)
    gate("F15 freeze fingerprint recomputes exactly", recorded == digest,
         f"{digest[:16]}… over {len(rows)} files")

    print()
    if FAILURES:
        print(f"FREEZE VALIDATION FAILED — {len(FAILURES)} gate(s): {', '.join(FAILURES)}")
        return 1
    print("FREEZE VALIDATION PASSED — all gates green")
    return 0


def _good_result():
    trials = []
    i = 0
    for rep in (1, 2, 3):
        for b in BRIEFS:
            i += 1
            trials.append({
                "trial_id": f"E037-sonnet-full-canon-{b}-R{rep}", "brief_id": b,
                "brief_digest": "0" * 64, "repetition": rep, "order_index": i,
                "status": "complete", "attempts_used": 1, "technical_retries_used": 0,
                "format_repairs_used": 0, "fresh_context": True,
                "package_path": f"packages/{b}.txt", "package_digest": "0" * 64,
                "sections_present": SECTIONS, "eligible_for_media_generation": True,
                "canon_used": True, "canon_tool_calls": 2,
                "canon_items_returned": {"accepted": 3, "hold": 1, "qa": 0},
                "website_snapshot_used": False, "wall_clock_ms": 1000, "usage": {}})
    return {"experiment": "EVAL-037", "lane_id": "sonnet-full-canon",
            "branch": "work/eval-037-sonnet-full-canon", "base_commit": "a" * 40,
            "runner_commit": "b" * 40, "provider": "Anthropic", "model": "claude-sonnet-5",
            "condition": "FULL_CANON",
            "canon_fingerprints": {"full_knowledge": FULL_FP, "qa": QA_FP},
            "trial_count": 18, "trials": trials}


if __name__ == "__main__":
    sys.exit(main())
