#!/usr/bin/env python3
"""EVAL-037 — the common lane runner.

One lane = one model x one condition x 18 trials, in one isolated execution session.

Usage (real execution, by a lane worker):
    python3 tools/runner.py --lane lanes/sonnet-full-canon.yaml

Usage (substrate tests, no network, no spend):
    python3 tools/runner.py --lane lanes/sonnet-full-canon.yaml --fake clean --out /tmp/x

Contract this file enforces, mechanically:

  * exactly 18 trials, in the lane's declared order
  * a fresh stateless request per trial - no message, tool result or state from any
    previous trial or attempt is carried in
  * initial attempt + at most 2 technical retries, and a retry ONLY after a
    technical failure class
  * at most ONE format-only repair per trial
  * NO retry on creative grounds - the runner has no quality notion and cannot judge
  * every output retained, including failed and malformed ones
  * NO_CANON never imports canon_tools and never touches canon/
  * the runner must be committed before the first real call (--fake exempts tests)
  * no media generation anywhere
"""
import argparse
import datetime as dt
import hashlib
import json
import pathlib
import subprocess
import sys
import time

import yaml

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
REPO = ROOT.parents[2]

SECTIONS = ["DELIVERABLE", "OBJECTIVE_INTERPRETATION", "CORE_CREATIVE_IDEA",
            "MESSAGE_AND_INFORMATION_HIERARCHY", "VISUAL_SYSTEM", "PRODUCTION_RECIPE",
            "GENERATION_PROMPTS", "DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS",
            "AUDIO_AND_EDIT", "FAILURE_PREVENTION", "HARD_CONSTRAINT_CHECK",
            "KNOWLEDGE_AND_WEBSITE_USE"]

MAX_TECHNICAL_RETRIES = 2
MAX_FORMAT_REPAIRS = 1

FORMAT_REPAIR_INSTRUCTION = (
    "Your previous response did not use the required output structure. Return the same "
    "answer again, unchanged in substance, using exactly the required "
    "FINAL_PRODUCTION_PACKAGE section headings. Do not add, remove, improve or "
    "reconsider any creative content."
)


def sha256_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha256_file(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def sections_present(text):
    """Mechanical presence check. Presence only - never a quality opinion."""
    up = text or ""
    return [s for s in SECTIONS if s in up]


def is_well_formed(text):
    return "FINAL_PRODUCTION_PACKAGE" in (text or "") and len(sections_present(text)) == len(SECTIONS)


# --------------------------------------------------------------------------
def preflight(lane, fake=None):
    """Verify the substrate before the first call. Fails closed."""
    problems, notes = [], []
    root = ROOT

    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                          capture_output=True, text=True).stdout.strip()
    base = lane["base_commit"]
    mb = subprocess.run(["git", "merge-base", head, base], cwd=REPO,
                        capture_output=True, text=True).stdout.strip()
    if mb != base:
        problems.append(f"HEAD does not descend from base_commit {base} (merge-base {mb or '?'})")
    notes.append(f"head={head} base={base}")

    got = sha256_file(root / lane["prompt"]["system_prompt_path"])
    if got != lane["prompt"]["system_prompt_sha256"]:
        problems.append(f"system prompt digest mismatch: {got}")

    for bid, b in lane["briefs"].items():
        got = sha256_file(root / b["path"])
        if got != b["sha256"]:
            problems.append(f"brief {bid} digest mismatch: {got}")
        site = b.get("website")
        if site:
            for k, dk in (("snapshot_html", "snapshot_html_sha256"),
                          ("snapshot_text", "snapshot_text_sha256")):
                got = sha256_file(root / site[k])
                if got != site[dk]:
                    problems.append(f"{bid} {k} digest mismatch: {got}")

    if lane["condition"] == "FULL_CANON":
        fps = lane["condition_detail"]["fingerprints"]
        live = canon_fingerprints()
        if live["full_knowledge"] != fps["full_knowledge"]["combined_digest"]:
            problems.append(f"full-knowledge fingerprint mismatch: {live['full_knowledge']}")
        if live["qa"] != fps["qa"]["combined_digest"]:
            problems.append(f"Q&A fingerprint mismatch: {live['qa']}")
        notes.append(f"canon full_knowledge={live['full_knowledge'][:16]}… qa={live['qa'][:16]}…")

    plan = lane["execution"]["trials_plan"]
    if len(plan) != 18:
        problems.append(f"trials_plan has {len(plan)} entries, expected 18")
    if len({t["trial_id"] for t in plan}) != 18:
        problems.append("trial ids are not unique")

    if fake is None:
        dirty = subprocess.run(["git", "status", "--porcelain", "--", str(HERE.relative_to(REPO))],
                               cwd=REPO, capture_output=True, text=True).stdout.strip()
        if dirty:
            problems.append("runner tree is dirty: freeze and COMMIT the runner before the "
                            f"first experimental call.\n{dirty}")
        notes.append("model preflight is the worker's responsibility: confirm the EXACT model id "
                     "resolves before trial 1, and STOP rather than substitute.")
    else:
        notes.append(f"FAKE PROVIDER ({fake}) — no network, no spend, no experimental call")
    return problems, notes


def canon_fingerprints():
    """Recompute both corpus digests. Reads only bytes, never interprets content."""
    import glob
    import os
    arts = ["source-knowledge.yaml", "source-concept-systems.yaml",
            "operational-bindings.yaml", "ontology-mappings.yaml", "visual-evidence-ledger.yaml"]

    def collect(rel):
        out = []
        base = REPO / rel
        for d in sorted(os.listdir(base)):
            p = base / d
            if p.is_dir():
                out += [f"{rel}/{d}/{a}" for a in arts if (p / a).is_file()]
        return out

    def fp(paths):
        rows = [(p, sha256_file(REPO / p)) for p in sorted(paths)]
        return hashlib.sha256("".join(f"{p}:{h}\n" for p, h in rows).encode()).hexdigest()

    full = collect("canon/knowledge/current") + collect("canon/candidates/canon-014")
    qa = sorted(str(pathlib.Path(p).relative_to(REPO))
                for p in glob.glob(str(REPO / "canon/qa/canon-014/*-qa-bank.yaml")))
    return {"full_knowledge": fp(full), "qa": fp(qa)}


# --------------------------------------------------------------------------
def build_adapter(lane, fake=None, fake_target=None):
    condition = lane["condition"]
    tool_schemas, canon = [], None
    if condition == "FULL_CANON":
        sys.path.insert(0, str(HERE))
        import canon_tools                       # imported ONLY in FULL_CANON
        canon = canon_tools.Canon(REPO, condition="FULL_CANON")
        tool_schemas = canon_tools.TOOL_SCHEMAS
        dispatch = lambda name, args: canon_tools.dispatch(canon, name, args)
    else:
        dispatch = None
    mk = lane["model"]["key"]
    mid = lane["model"]["model_id"]
    if fake:
        from fake_provider import FakeAdapter
        return FakeAdapter(mid, tool_schemas, scenario=fake, target_trial=fake_target,
                           model_key=mk), dispatch
    sys.path.insert(0, str(HERE))
    from providers import ADAPTERS
    return ADAPTERS[mk](mid, tool_schemas), dispatch


def system_prompt_for(lane):
    text = (ROOT / lane["prompt"]["system_prompt_path"]).read_text(encoding="utf-8")
    if lane["condition"] == "FULL_CANON":
        cond = yaml.safe_load(
            (ROOT / lane["condition_detail"]["addendum_path"]).read_text(encoding="utf-8"))
        text = text.rstrip("\n") + "\n\n" + cond[lane["condition_detail"]["addendum_key"]].rstrip("\n") + "\n"
    return text


# --------------------------------------------------------------------------
def run_trial(trial, lane, adapter, dispatch, system_prompt, outdir, fake):
    """One trial. Every attempt is a brand-new request built from scratch."""
    brief_path = ROOT / trial["brief_path"]
    brief = brief_path.read_text(encoding="utf-8")
    attempts, tech_retries, repairs = [], 0, 0
    status, package, package_path = None, None, None
    t0 = time.time()

    attempt_index = 0
    while True:
        kind = ("initial" if attempt_index == 0
                else "format_repair" if attempt_index == 3 else "technical_retry")
        # FRESH request every attempt. Nothing from any previous attempt or trial.
        user = brief if kind != "format_repair" else brief + "\n\n" + FORMAT_REPAIR_INSTRUCTION
        request = adapter.build_request(system_prompt, user)
        row = {"trial_id": trial["trial_id"], "brief_id": trial["brief_id"],
               "repetition": trial["repetition"], "attempt_index": attempt_index,
               "attempt_kind": kind, "started_at": now(), "fresh_context": True,
               "request_digest": adapter.request_digest(request)}
        try:
            kw = {"canon_dispatch": dispatch}
            if fake:
                kw.update(trial_id=trial["trial_id"], attempt=attempt_index)
            resp = adapter.call(request, **kw)
        except Exception as e:                       # noqa: BLE001 - classified below
            fc = getattr(e, "failure_class", "sdk_error")
            row.update(ended_at=now(), outcome="technical_failure",
                       technical_failure_class=fc, error=str(e)[:500])
            attempts.append(row)
            if tech_retries < MAX_TECHNICAL_RETRIES:
                tech_retries += 1
                attempt_index = tech_retries      # 1, then 2
                continue
            status = "failed_technical"
            break

        text = resp["text"]
        raw_path = outdir / "raw" / f"{trial['trial_id']}-a{attempt_index}.json"
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_text(json.dumps(resp["raw"], indent=2, default=str))
        row.update(ended_at=now(), response_digest=sha256_text(text),
                   raw_response_path=str(raw_path.relative_to(outdir)),
                   tool_calls=resp.get("tool_calls", []))
        site = trial.get("website_snapshot")
        row["website_snapshot_read"] = []          # snapshot reads are the model's own choice

        if is_well_formed(text):
            row["outcome"] = "ok"
            attempts.append(row)
            package, status = text, ("format_repaired" if repairs else "complete")
            break

        row["outcome"] = "format_invalid"
        row["note"] = "required section structure absent — mechanical check only"
        attempts.append(row)
        if repairs < MAX_FORMAT_REPAIRS:
            repairs += 1
            attempt_index = 3                      # the single permitted format repair
            continue
        # Out of repairs. The output is RETAINED and the trial is not retried on
        # creative grounds — there is no such retry in this experiment.
        package, status = text, "format_repaired"
        break

    if package is not None:
        package_path = outdir / "packages" / f"{trial['trial_id']}.txt"
        package_path.parent.mkdir(parents=True, exist_ok=True)
        package_path.write_text(package, encoding="utf-8")

    tool_calls = [tc for a in attempts for tc in a.get("tool_calls", [])]
    result = {
        "trial_id": trial["trial_id"], "brief_id": trial["brief_id"],
        "brief_digest": sha256_file(brief_path), "repetition": trial["repetition"],
        "order_index": trial["order_index"], "status": status,
        "attempts_used": len(attempts), "technical_retries_used": tech_retries,
        "format_repairs_used": repairs, "fresh_context": True,
        "package_path": str(package_path.relative_to(outdir)) if package_path else None,
        "package_digest": sha256_text(package) if package else None,
        "sections_present": sections_present(package) if package else [],
        "eligible_for_media_generation": package is not None,
        "canon_used": (bool(tool_calls) if lane["condition"] == "FULL_CANON" else None),
        "canon_tool_calls": len(tool_calls),
        "canon_items_returned": {
            "accepted": sum(t.get("accepted_items", 0) for t in tool_calls),
            "hold": sum(t.get("hold_items", 0) for t in tool_calls),
            "qa": sum(t.get("qa_items", 0) for t in tool_calls)},
        "website_snapshot_used": False,
        "wall_clock_ms": int((time.time() - t0) * 1000),
    }
    return result, attempts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--fake", default=None,
                    help="run against the fake provider (no network, no spend)")
    ap.add_argument("--fake-target", default=None)
    ap.add_argument("--preflight-only", action="store_true")
    a = ap.parse_args()

    lane = yaml.safe_load(pathlib.Path(a.lane).read_text(encoding="utf-8"))
    problems, notes = preflight(lane, fake=a.fake)
    for n in notes:
        print(f"  note: {n}")
    if problems:
        for p in problems:
            print(f"  PREFLIGHT FAIL: {p}", file=sys.stderr)
        print("STOPPING. Do not substitute anything. Escalate.", file=sys.stderr)
        return 2
    print("preflight OK")
    if a.preflight_only:
        return 0

    outdir = pathlib.Path(a.out) if a.out else (REPO / lane["evidence"]["root"])
    outdir.mkdir(parents=True, exist_ok=True)
    adapter, dispatch = build_adapter(lane, fake=a.fake, fake_target=a.fake_target)
    system_prompt = system_prompt_for(lane)

    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                          capture_output=True, text=True).stdout.strip()
    trials, all_attempts = [], []
    for trial in lane["execution"]["trials_plan"]:
        res, atts = run_trial(trial, lane, adapter, dispatch, system_prompt, outdir, a.fake)
        trials.append(res); all_attempts += atts
        print(f"  [{res['order_index']:2d}/18] {res['trial_id']}  {res['status']}  "
              f"attempts={res['attempts_used']}")

    ledger = {"experiment": "EVAL-037", "lane_id": lane["lane_id"], "branch": lane["branch"],
              "base_commit": lane["base_commit"], "runner_commit": head,
              "model": lane["model"]["model_id"], "condition": lane["condition"],
              "attempts": all_attempts}
    result = {"experiment": "EVAL-037", "lane_id": lane["lane_id"], "branch": lane["branch"],
              "base_commit": lane["base_commit"], "runner_commit": head,
              "provider": lane["model"]["provider"], "model": lane["model"]["model_id"],
              "condition": lane["condition"], "trial_count": len(trials), "trials": trials}
    if lane["condition"] == "FULL_CANON":
        fps = lane["condition_detail"]["fingerprints"]
        result["canon_fingerprints"] = {"full_knowledge": fps["full_knowledge"]["combined_digest"],
                                        "qa": fps["qa"]["combined_digest"]}
    (outdir / "attempt-ledger.json").write_text(json.dumps(ledger, indent=2, default=str))
    (outdir / "result.json").write_text(json.dumps(result, indent=2, default=str))
    print(f"wrote {outdir}/attempt-ledger.json and {outdir}/result.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
