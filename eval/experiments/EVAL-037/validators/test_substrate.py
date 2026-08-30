#!/usr/bin/env python3
"""EVAL-037 — behavioural tests. Zero network, zero spend, zero experimental calls.

A validator that only accepts is not a validator, so most of these are NEGATIVE
tests: they break exactly one rule and assert the substrate rejects it.

    python3 validators/test_substrate.py
"""
import copy
import io
import contextlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

import yaml

HERE = pathlib.Path(__file__).resolve().parent
PKG = HERE.parent
REPO = PKG.parents[2]
sys.path.insert(0, str(PKG / "tools"))

from jsonschema_mini import validate            # noqa: E402
import canon_tools                              # noqa: E402
from canon_tools import Canon, CanonStatusError, ACCEPTED, HOLD  # noqa: E402

RESULT_SCHEMA = json.loads((PKG / "schemas/result.schema.json").read_text())
LEDGER_SCHEMA = json.loads((PKG / "schemas/attempt-ledger.schema.json").read_text())

PASSED, FAILED = [], []


def check(name, ok, detail=""):
    (PASSED if ok else FAILED).append(name)
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))


def run_lane(lane, scenario, target=None):
    """Run a lane end-to-end on the fake provider. No network."""
    out = pathlib.Path(tempfile.mkdtemp())
    cmd = [sys.executable, str(PKG / "tools/runner.py"), "--lane", str(PKG / "lanes" / lane),
           "--fake", scenario, "--out", str(out)]
    if target:
        cmd += ["--fake-target", target]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=REPO)
    if p.returncode != 0:
        raise AssertionError(f"runner failed: {p.stderr[-800:]}")
    return (json.loads((out / "result.json").read_text()),
            json.loads((out / "attempt-ledger.json").read_text()), out)


# =========================================================================
def t_clean():
    r, l, out = run_lane("sonnet-no-canon.yaml", "clean")
    check("T01 clean run produces exactly 18 trials", r["trial_count"] == 18 and len(r["trials"]) == 18)
    check("T02 clean run: every trial complete on the first attempt",
          all(t["status"] == "complete" and t["attempts_used"] == 1 for t in r["trials"]))
    check("T03 clean run validates against result.schema.json", not validate(r, RESULT_SCHEMA),
          "; ".join(validate(r, RESULT_SCHEMA)[:2]))
    check("T04 clean run ledger validates against attempt-ledger.schema.json",
          not validate(l, LEDGER_SCHEMA), "; ".join(validate(l, LEDGER_SCHEMA)[:2]))
    check("T05 every package retained on disk",
          all((out / t["package_path"]).exists() for t in r["trials"]))
    shutil.rmtree(out, ignore_errors=True)


def t_fresh_context():
    """Every trial must be a brand-new request. Two trials on the same brief must
    produce the SAME request digest — proving nothing accumulated between them."""
    r, l, out = run_lane("sonnet-no-canon.yaml", "clean")
    by_brief = {}
    for at in l["attempts"]:
        by_brief.setdefault(at["brief_id"], set()).add(at["request_digest"])
    check("T06 the 3 repetitions of a brief send an IDENTICAL request (no carried state)",
          all(len(v) == 1 for v in by_brief.values()),
          f"{ {k: len(v) for k, v in by_brief.items()} }")
    check("T07 different briefs send different requests",
          len({next(iter(v)) for v in by_brief.values()}) == 6)
    check("T08 every attempt flags fresh_context", all(a["fresh_context"] for a in l["attempts"]))
    shutil.rmtree(out, ignore_errors=True)


def t_technical_retry():
    target = "E037-sonnet-no-canon-B03-R2"
    r, l, out = run_lane("sonnet-no-canon.yaml", "flaky", target)
    t = next(x for x in r["trials"] if x["trial_id"] == target)
    others = [x for x in r["trials"] if x["trial_id"] != target]
    check("T09 one technical failure → exactly one retry, then success",
          t["status"] == "complete" and t["technical_retries_used"] == 1
          and t["attempts_used"] == 2)
    check("T10 the technical failure is retained in the ledger with a failure class",
          any(a["trial_id"] == target and a["outcome"] == "technical_failure"
              and a["technical_failure_class"] == "timeout" for a in l["attempts"]))
    check("T11 a retry in one trial does not disturb any other trial",
          all(x["attempts_used"] == 1 for x in others))
    shutil.rmtree(out, ignore_errors=True)


def t_retry_ceiling():
    target = "E037-sonnet-no-canon-B01-R1"
    r, l, out = run_lane("sonnet-no-canon.yaml", "hard_fail", target)
    t = next(x for x in r["trials"] if x["trial_id"] == target)
    atts = [a for a in l["attempts"] if a["trial_id"] == target]
    check("T12 permanent technical failure stops at 1 initial + 2 retries",
          t["status"] == "failed_technical" and t["technical_retries_used"] == 2
          and len(atts) == 3)
    check("T13 a technically failed trial produces no package and is not eligible",
          t["package_path"] is None and t["eligible_for_media_generation"] is False)
    check("T14 the lane still reports exactly 18 trials after a hard failure",
          r["trial_count"] == 18)
    shutil.rmtree(out, ignore_errors=True)


def t_format_repair():
    target = "E037-sonnet-no-canon-B05-R1"
    r, l, out = run_lane("sonnet-no-canon.yaml", "malformed", target)
    t = next(x for x in r["trials"] if x["trial_id"] == target)
    atts = sorted((a for a in l["attempts"] if a["trial_id"] == target),
                  key=lambda x: x["attempt_index"])
    check("T15 a malformed answer triggers exactly one format repair",
          t["status"] == "format_repaired" and t["format_repairs_used"] == 1
          and len(atts) == 2 and atts[1]["attempt_kind"] == "format_repair")
    check("T16 the malformed output is retained, not discarded",
          atts[0]["outcome"] == "format_invalid" and "raw_response_path" in atts[0])
    sys.path.insert(0, str(PKG / "tools"))
    import runner as _r
    instr = _r.FORMAT_REPAIR_INSTRUCTION
    check("T17 the repair is format-only (the repair prompt changes no creative content)",
          "unchanged in substance" in instr
          and "Do not add, remove, improve or reconsider any creative content" in instr
          and "concept" not in instr and "better" not in instr)
    shutil.rmtree(out, ignore_errors=True)


def t_repair_ceiling():
    target = "E037-sonnet-no-canon-B05-R1"
    r, l, out = run_lane("sonnet-no-canon.yaml", "always_malformed", target)
    t = next(x for x in r["trials"] if x["trial_id"] == target)
    atts = [a for a in l["attempts"] if a["trial_id"] == target]
    check("T18 a persistently malformed answer is repaired ONCE and then accepted as-is",
          t["format_repairs_used"] == 1 and len(atts) == 2)
    check("T19 the output is still retained and still eligible (no quality gate)",
          t["package_path"] is not None and t["eligible_for_media_generation"] is True)
    shutil.rmtree(out, ignore_errors=True)


def t_no_creative_retry():
    """There must be no code path that retries on quality. Prove it by absence."""
    src = (PKG / "tools/runner.py").read_text()
    banned = ["quality", "score", "judge", "better", "improve the", "rewrite", "best_of"]
    hits = [b for b in banned if f"{b}(" in src or f".{b}" in src or f"if {b}" in src]
    check("T20 the runner contains no quality/judging code path", not hits, f"{hits}")
    check("T21 retries are licensed only by a technical failure class or a format check",
          src.count("MAX_TECHNICAL_RETRIES") >= 2 and src.count("MAX_FORMAT_REPAIRS") >= 2
          and "is_well_formed" in src)


def t_no_canon_isolation():
    r, l, out = run_lane("sonnet-no-canon.yaml", "canon_user")
    check("T22 NO_CANON exposes no Canon tool, so no Canon call can occur",
          all(t["canon_tool_calls"] == 0 and t["canon_used"] is None for t in r["trials"]))
    check("T23 NO_CANON result records no Canon fingerprints", "canon_fingerprints" not in r)
    sp = (PKG / "common/system-prompt.txt").read_text()
    lane = yaml.safe_load((PKG / "lanes/sonnet-no-canon.yaml").read_text())
    sys.path.insert(0, str(PKG / "tools"))
    import runner
    check("T24 the NO_CANON system prompt is the common prompt verbatim, nothing appended",
          runner.system_prompt_for(lane) == sp)
    blob = (PKG / "lanes/sonnet-no-canon.yaml").read_text()
    corpus = ["canon/knowledge/", "canon/candidates/", "canon/qa/",
              "cbd321aa3be7464e785a0d42de1764cdccc8bdd33bc023a376740f8f196bde60",
              "1313c0babe2194a7bc71c1628f9fbec5fa4f35ca5ff5edc7f594662101dc62bd"]
    leaks = [x for x in corpus if x in blob]
    check("T25 the NO_CANON lane names no Canon corpus path and no fingerprint",
          not leaks and "canon/**" in blob, f"leaks={leaks}" if leaks else
          "canon/** appears only as a forbidden read")
    shutil.rmtree(out, ignore_errors=True)


def t_full_canon_prompt():
    sys.path.insert(0, str(PKG / "tools"))
    import runner
    lane = yaml.safe_load((PKG / "lanes/sonnet-full-canon.yaml").read_text())
    sp = runner.system_prompt_for(lane)
    base = (PKG / "common/system-prompt.txt").read_text()
    add = yaml.safe_load((PKG / "conditions/full-canon.yaml").read_text())["addendum"]
    check("T26 FULL_CANON prompt = common prompt + the addendum, in that order",
          sp.startswith(base.rstrip("\n")) and add.rstrip("\n") in sp)
    check("T27 the addendum lives only in conditions/full-canon.yaml",
          "ACCEPTED means the source passed" not in base
          and all("ACCEPTED means the source passed" not in p.read_text()
                  for p in (PKG / "lanes").glob("*.yaml")))


def t_canon_status():
    c = Canon(REPO, condition="FULL_CANON")
    cat = c.canon_catalog()
    check("T28 catalog exposes every source with a real status",
          cat["total"] == 42 and cat["accepted"] == 24 and cat["hold"] == 18
          and all(s["source_status"] in (ACCEPTED, HOLD) for s in cat["sources"]))
    check("T29 every HOLD source carries an explicit caution and a blocker field",
          all("caution" in s and "hold_blocker" in s
              for s in cat["sources"] if s["source_status"] == HOLD))
    check("T30 no HOLD source is ever labelled accepted",
          not any(s["source_status"] == ACCEPTED
                  for s in cat["sources"] if s["source_dir"].startswith("__never__"))
          and all(s["source_status"] == HOLD
                  for s in c.canon_catalog(source_status=HOLD)["sources"]))
    res = c.canon_search("design")
    check("T31 every search result carries source_status",
          all(r["source_status"] in (ACCEPTED, HOLD) for r in res["results"]))
    check("T32 search is unbounded by default (no harness top-K)",
          res["limit_applied"] is None and res["returned"] == res["total_matches"]
          and res["limit_source"] == "none (unbounded)")
    lim = c.canon_search("design", limit=2)
    check("T33 a limit is honoured only when the CALLER asks for one",
          lim["returned"] == 2 and lim["limit_source"] == "caller"
          and lim["total_matches"] == res["total_matches"])
    qa = c.canon_search("logo", kinds=["qa"], limit=1)["results"]
    check("T34 Q&A items are flagged not-benchmark-truth and not corroboration",
          bool(qa) and qa[0]["not_benchmark_ground_truth"] is True
          and qa[0]["independent_corroboration"] is False)
    hold_src = next(s["source_dir"] for s in cat["sources"] if s["source_status"] == HOLD)
    rd = c.canon_read(source_dir=hold_src, artifact="source-knowledge.yaml")
    check("T35 canon_read stamps HOLD on the artifact AND on every item it returns",
          rd["source_status"] == HOLD
          and all(i["source_status"] == HOLD and "caution" in i for i in rd["items"]))
    try:
        canon_tools._assert_status({"source_status": "accepted"})
        ok = False
    except CanonStatusError:
        ok = True
    check("T36 an object with a lowercase/unknown status is REFUSED, not coerced", ok)
    try:
        canon_tools._assert_status({"kind": "knowledge"})
        ok = False
    except CanonStatusError:
        ok = True
    check("T37 an object with no status at all is REFUSED", ok)
    try:
        Canon(REPO, condition="NO_CANON")
        ok = False
    except PermissionError:
        ok = True
    check("T38 constructing Canon under NO_CANON raises", ok)
    try:
        canon_tools.dispatch(c, "canon_write", {})
        ok = False
    except ValueError:
        ok = True
    check("T39 only the three named tools are dispatchable (read-only surface)", ok)
    check("T40 the Canon module opens nothing for writing",
          "open(" in (PKG / "tools/canon_tools.py").read_text()
          and '"w"' not in (PKG / "tools/canon_tools.py").read_text()
          and "'w'" not in (PKG / "tools/canon_tools.py").read_text())


def t_schema_negatives():
    good = _good_result()
    cases = [
        ("T41 a 17-trial result is rejected",
         lambda d: (d["trials"].pop(), d.update(trial_count=17), d)[-1]),
        ("T42 a 19-trial result is rejected",
         lambda d: (d["trials"].append(copy.deepcopy(d["trials"][0])),
                    d.update(trial_count=19), d)[-1]),
        ("T43 a 3rd technical retry is rejected",
         lambda d: (d["trials"][0].update(technical_retries_used=3), d)[-1]),
        ("T44 a 2nd format repair is rejected",
         lambda d: (d["trials"][0].update(format_repairs_used=2), d)[-1]),
        ("T45 a failed_technical trial that still claims a package is rejected",
         lambda d: (d["trials"][0].update(status="failed_technical",
                                          technical_retries_used=2), d)[-1]),
        ("T46 a moving-alias model id is rejected",
         lambda d: (d.update(model="claude-sonnet-latest"), d)[-1]),
        ("T47 a trial id from the wrong lane is rejected",
         lambda d: (d["trials"][0].update(trial_id="E037-sonnet-full-canon-B09-R1"), d)[-1]),
        ("T48 a 4th repetition is rejected",
         lambda d: (d["trials"][0].update(repetition=4), d)[-1]),
        ("T49 fresh_context: false is rejected",
         lambda d: (d["trials"][0].update(fresh_context=False), d)[-1]),
        ("T50 an unknown extra field is rejected",
         lambda d: (d["trials"][0].update(creative_score=7), d)[-1]),
    ]
    for name, mutate in cases:
        d = mutate(copy.deepcopy(good))
        check(name, bool(validate(d, RESULT_SCHEMA)))
    check("T51 the unmutated good result still validates", not validate(good, RESULT_SCHEMA))

    led = _good_ledger()
    check("T52 the good ledger validates", not validate(led, LEDGER_SCHEMA),
          "; ".join(validate(led, LEDGER_SCHEMA)[:2]))
    bad = copy.deepcopy(led)
    bad["attempts"][0]["outcome"] = "technical_failure"
    bad["attempts"][0]["technical_failure_class"] = None
    check("T53 a technical failure with no failure class is rejected",
          bool(validate(bad, LEDGER_SCHEMA)))
    bad = copy.deepcopy(led)
    bad["attempts"][0].update(attempt_kind="format_repair", attempt_index=1)
    check("T54 a format repair at the wrong attempt index is rejected",
          bool(validate(bad, LEDGER_SCHEMA)))
    bad = copy.deepcopy(led)
    bad["attempts"][0]["attempt_index"] = 4
    check("T55 a 5th attempt is rejected", bool(validate(bad, LEDGER_SCHEMA)))


def t_lane_run_validator_negatives():
    """The lane-run validator must actually reject broken evidence."""
    r, l, out = run_lane("sonnet-no-canon.yaml", "clean")

    def run_validator(mutate_result=None, mutate_ledger=None, extra_file=None):
        tmp = pathlib.Path(tempfile.mkdtemp())
        shutil.copytree(out, tmp / "run")
        rr = json.loads((tmp / "run/result.json").read_text())
        ll = json.loads((tmp / "run/attempt-ledger.json").read_text())
        if mutate_result:
            mutate_result(rr)
        if mutate_ledger:
            mutate_ledger(ll)
        (tmp / "run/result.json").write_text(json.dumps(rr))
        (tmp / "run/attempt-ledger.json").write_text(json.dumps(ll))
        if extra_file:
            (tmp / "run" / extra_file).write_bytes(b"\x89PNG\r\n")
        p = subprocess.run(
            [sys.executable, str(PKG / "validators/validate_lane_run.py"),
             "--lane", str(PKG / "lanes/sonnet-no-canon.yaml"), "--run", str(tmp / "run")],
            capture_output=True, text=True, cwd=REPO)
        shutil.rmtree(tmp, ignore_errors=True)
        return p.returncode

    check("T56 the validator PASSES the untouched clean run", run_validator() == 0)
    check("T57 the validator REJECTS a dropped trial",
          run_validator(mutate_result=lambda d: (d["trials"].pop(),
                                                 d.update(trial_count=17))) != 0)
    check("T58 the validator REJECTS reordered trials",
          run_validator(mutate_result=lambda d: d["trials"].reverse()) != 0)
    check("T59 the validator REJECTS a media artefact in the run directory",
          run_validator(extra_file="frame.png") != 0)
    check("T60 the validator REJECTS an unlicensed retry (no technical failure before it)",
          run_validator(mutate_ledger=lambda d: d["attempts"].append(
              {**d["attempts"][0], "attempt_index": 1, "attempt_kind": "technical_retry"})) != 0)
    check("T61 the validator REJECTS a NO_CANON run claiming Canon fingerprints",
          run_validator(mutate_result=lambda d: d.update(
              canon_fingerprints={"full_knowledge": "x" * 64, "qa": "y" * 64})) != 0)
    shutil.rmtree(out, ignore_errors=True)


def t_no_experimental_calls():
    """Prove the fake path cannot reach a provider."""
    src = (PKG / "tools/fake_provider.py").read_text()
    check("T62 fake_provider imports no SDK and opens no socket",
          not any(x in src for x in ("import openai", "import anthropic", "from google",
                                     "import requests", "import socket", "urllib", "httpx")))
    code = "\n".join(l for l in src.splitlines() if not l.lstrip().startswith("#"))
    code = code.split('"""', 2)[-1]          # drop the module docstring
    check("T63 fake_provider is deterministic (no clock, no randomness in its code)",
          not any(x in code for x in ("import random", "random.", "time.time(",
                                      "datetime.now(", "uuid.", "os.urandom")))


def _good_result():
    sections = ["DELIVERABLE", "OBJECTIVE_INTERPRETATION", "CORE_CREATIVE_IDEA",
                "MESSAGE_AND_INFORMATION_HIERARCHY", "VISUAL_SYSTEM", "PRODUCTION_RECIPE",
                "GENERATION_PROMPTS", "DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS",
                "AUDIO_AND_EDIT", "FAILURE_PREVENTION", "HARD_CONSTRAINT_CHECK",
                "KNOWLEDGE_AND_WEBSITE_USE"]
    trials, i = [], 0
    for rep in (1, 2, 3):
        for b in ["B01", "B02", "B03", "B04", "B05", "B06"]:
            i += 1
            trials.append({"trial_id": f"E037-sol-no-canon-{b}-R{rep}", "brief_id": b,
                           "brief_digest": "0" * 64, "repetition": rep, "order_index": i,
                           "status": "complete", "attempts_used": 1,
                           "technical_retries_used": 0, "format_repairs_used": 0,
                           "fresh_context": True, "package_path": f"packages/{b}.txt",
                           "package_digest": "0" * 64, "sections_present": sections,
                           "eligible_for_media_generation": True, "canon_used": None,
                           "canon_tool_calls": 0,
                           "canon_items_returned": {"accepted": 0, "hold": 0, "qa": 0},
                           "website_snapshot_used": False, "wall_clock_ms": 1})
    return {"experiment": "EVAL-037", "lane_id": "sol-no-canon",
            "branch": "work/eval-037-sol-no-canon", "base_commit": "a" * 40,
            "runner_commit": "b" * 40, "provider": "OpenAI", "model": "gpt-5.6-sol",
            "condition": "NO_CANON", "trial_count": 18, "trials": trials}


def _good_ledger():
    return {"experiment": "EVAL-037", "lane_id": "sol-no-canon",
            "branch": "work/eval-037-sol-no-canon", "base_commit": "a" * 40,
            "runner_commit": "b" * 40, "model": "gpt-5.6-sol", "condition": "NO_CANON",
            "attempts": [{"trial_id": "E037-sol-no-canon-B01-R1", "brief_id": "B01",
                          "repetition": 1, "attempt_index": 0, "attempt_kind": "initial",
                          "started_at": "2026-08-30T12:00:00+00:00",
                          "ended_at": "2026-08-30T12:00:10+00:00", "outcome": "ok",
                          "fresh_context": True, "request_digest": "c" * 64,
                          "response_digest": "d" * 64}]}


def main():
    print("EVAL-037 substrate tests — fake provider only, no network, no spend\n")
    for fn in (t_clean, t_fresh_context, t_technical_retry, t_retry_ceiling,
               t_format_repair, t_repair_ceiling, t_no_creative_retry,
               t_no_canon_isolation, t_full_canon_prompt, t_canon_status,
               t_schema_negatives, t_lane_run_validator_negatives, t_no_experimental_calls):
        fn()
    print(f"\n{len(PASSED)} passed, {len(FAILED)} failed")
    if FAILED:
        print("FAILED: " + ", ".join(FAILED))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
