#!/usr/bin/env python3
"""qualify_screen: does the VLM screen (instruments/vlm_screen.py) agree with the Controller's blind verdicts?

    python3 eval/harness-v2/qualify_screen.py --results 'eval/experiments/EVAL-040/runs/*/RESULTS.yaml' --dry-run
    python3 eval/harness-v2/qualify_screen.py --results '...' --auth <file with screen_cap_usd> --out QUALIFICATION-REPORT.yaml

For every judged trial (Controller verdict accept / reject) whose sealed artifact resolves under the run's
artifacts/media/, the runner would hand the artifact and the case's acceptance_contract (TEST-CASES.yaml) to the
instrument and compare the instrument's overall verdict with the Controller's. Audio trials are planned as
cannot_judge (no call). It writes, per run, SCREEN-RESULTS.yaml (schema SCREEN-RESULTS-v0: per trial the
instrument's overall + per-rule verdicts + config hash) beside RESULTS.yaml (or under --screen-out-dir), and one
QUALIFICATION-REPORT.yaml: agreement, Cohen's kappa, per-question and per-route confusion, every disagreement with
the Controller's note, spend, and `qualification_verdict` against instruments/SCREEN-QUALIFICATION-CRITERIA-v0.yaml.
That file is UNFROZEN: the report keeps `would_verdict` and writes `screened_not_qualified` until the Controller
freezes it (the PASS-CRITERIA rule, applied to a judge).

Money rules. `--dry-run` prints the plan (calls, images, frames) and a cost estimate ONLY when a Gemini API price is
pinned under eval/empirical-planning/price-pins-2026-09/ (PIN-INDEX.yaml entry named in the criteria file);
otherwise it prints "price not pinned" and no number. A live run refuses without `--auth <file>` carrying
`screen_cap_usd` (missing = 0 = forbidden), refuses when the price is not pinned (a cap nobody can enforce is no cap),
projects every call against the cap before it is made and stops at the first call that would cross it. 0 retries.
A live run writes its OWN counters (calls sent, calls refused, which limit stopped it) into every SCREEN-RESULTS file
under `call_counters`. An offline rebuild reports THAT number and never recomputes one from the screened rows - a row
is not a call (audio is cannot_judge with no call). With no live counter the report prints no call number at all and
says in words that the count is not known. The report always states the authorised screen_max_calls and flags plainly
when the recorded count is at or above it.
The key is read by NAME (GOOGLE_API_KEY) at the first call and never printed. Only transports.py opens a socket.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import yaml

import evidence_map as EM
import hv2_paths
from instruments import vlm_screen as VS

RUNS_ROOT = hv2_paths.EVAL_ROOT / "experiments" / "EVAL-040" / "runs"
SCREEN_RESULTS_FILE = "SCREEN-RESULTS.yaml"
REPORT_FILE = "QUALIFICATION-REPORT.yaml"
DEFAULT_REPORT = hv2_paths.EVAL_ROOT / "experiments" / "EVAL-040" / "screening" / REPORT_FILE
JUDGED = ("accept", "reject")
D = Decimal


class ScreenRefused(RuntimeError):
    """Nothing was sent."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _sha256_file(p: Path | str) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def _rel(p: Path | str) -> str:
    try:
        return str(Path(p).resolve().relative_to(hv2_paths.REPO_ROOT.resolve()))
    except ValueError:
        return str(p)


# ------------------------------------------------------------------------------ inputs
def load_cases(path: Path | str | None = None) -> dict:
    p = Path(path) if path else hv2_paths.TEST_CASES
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    cases = {c["case_id"]: c for c in data.get("cases", []) if isinstance(c, dict) and c.get("case_id")}
    if not cases:
        raise ScreenRefused(f"{p}: no cases")
    return {"_path": str(p), "_sha256": _sha256_file(p), "cases": cases}


def question_of(trial: dict) -> str:
    q = trial.get("question")
    if q:
        return str(q)
    cid = str(trial.get("case_id") or "")
    return cid.rsplit("-", 1)[0] if "-" in cid else cid


def resolve_artifact(results_path: Path, doc: dict, trial: dict, runs_root: Path | None) -> tuple:
    """(path | None, reason). The judged file is artifacts/media/<trial_id>.<ext> of the trial's run (trial.run_id if that run
    directory exists under runs_root, else the directory of the RESULTS.yaml); a `composited: true` trial names the
    `.composite.<ext>` file; a `sha256` on the trial (the composite run) must match the bytes."""
    tid = str(trial.get("trial_id") or "")
    if not tid:
        return None, "no trial_id"
    run_dir = results_path.parent
    rid = trial.get("run_id")
    if rid and runs_root is not None and (Path(runs_root) / str(rid)).is_dir():
        run_dir = Path(runs_root) / str(rid)
    media = run_dir / "artifacts" / "media"
    if not media.is_dir():
        return None, f"no media directory under {run_dir.name}"
    cands = sorted(p for p in media.glob(tid + ".*") if p.is_file())
    comp = [p for p in cands if p.name[len(tid):].startswith(".composite.")]
    plain = [p for p in cands if p not in comp]
    chosen = comp if trial.get("composited") else plain or comp
    if trial.get("sha256"):
        chosen = [p for p in cands if _sha256_file(p) == trial["sha256"]] or []
        if not chosen:
            return None, "no sealed file hashes to the trial's sha256"
    if not chosen:
        return None, "no sealed artifact (E5: judged without a file)"
    return chosen[0], "ok"


def plan_trials(results_paths: list, cases: dict, runs_root: Path | None = RUNS_ROOT, n_frames: int = VS.VIDEO_FRAMES) -> list:
    rows = []
    for rp in results_paths:
        rp = Path(rp)
        doc = yaml.safe_load(rp.read_text(encoding="utf-8")) or {}
        run_id = doc.get("run_id") or rp.parent.name
        for t in doc.get("trials", []) or []:
            row = {"results_path": str(rp), "run_id": str(t.get("run_id") or run_id), "results_run_id": str(run_id), "trial_id": t.get("trial_id"),
                   "case_id": t.get("case_id"), "question": question_of(t), "route_key": t.get("route_key"), "arm": t.get("arm"),
                   "controller_verdict": t.get("verdict"), "controller_note": t.get("note") or "", "verdict_basis": t.get("verdict_basis"),
                   "artifact": None, "media_kind": None, "images": 0, "calls": 0, "n_rules": 0, "skip": None}
            if row["controller_verdict"] not in JUDGED:
                row["skip"] = f"controller verdict {row['controller_verdict']!r} is not accept / reject"
                rows.append(row)
                continue
            case = cases["cases"].get(str(row["case_id"]))
            if case is None or not case.get("acceptance_contract"):
                row["skip"] = f"case {row['case_id']!r} has no acceptance_contract in TEST-CASES"
                rows.append(row)
                continue
            row["n_rules"] = len(VS.parse_contract(case["acceptance_contract"]))
            path, why = resolve_artifact(rp, doc, t, runs_root)
            if path is None:
                row["skip"] = why
                rows.append(row)
                continue
            kind = VS.media_kind_of(path)
            row.update({"artifact": str(path), "media_kind": kind})
            if kind == "image":
                row.update({"images": 1, "calls": 1})
            elif kind == "video":
                row.update({"images": n_frames, "calls": 1})
            elif kind == "audio":
                row["skip"] = "audio: planned as cannot_judge, no call"
            else:
                row["skip"] = f"unsupported artifact type {path.suffix!r}"
            rows.append(row)
    return rows


# ------------------------------------------------------------------------------ price pin + auth
def price_pin(criteria: dict, index_path: Path | str | None = None) -> dict | None:
    """The PIN-INDEX entry the criteria file names, only if it carries every required field. None -> 'price not pinned'."""
    spec = criteria.get("price_pin") or {}
    idx = Path(index_path) if index_path else (hv2_paths.REPO_ROOT / str(spec.get("index", "")))
    if not spec.get("route_key") or not idx.exists():
        return None
    try:
        entries = yaml.safe_load(idx.read_text(encoding="utf-8")) or []
    except yaml.YAMLError:
        return None
    if isinstance(entries, dict):
        entries = entries.get("pins") or entries.get("entries") or []
    need = list(spec.get("required_fields") or [])
    for e in entries:
        if isinstance(e, dict) and e.get("route_key") == spec["route_key"] and all(e.get(f) is not None for f in need):
            pin_file = e.get("pin_file")
            if pin_file and not (hv2_paths.REPO_ROOT / str(pin_file)).exists():
                return None
            return {"index": _rel(idx), "route_key": e["route_key"], "pin_file": pin_file, "sha256": e.get("sha256"), "url": e.get("url"),
                    "fetched_utc": str(e.get("fetched_utc") or ""), **{f: e[f] for f in need}}
    return None


def per_call_estimate_usd(images: int, pin: dict, criteria: dict) -> Decimal:
    """Image tokens at the pinned price plus the criteria file's text / output allowances (Planner assumptions, labelled)."""
    a = criteria.get("estimate_assumptions") or {}
    text_in = int(a.get("text_tokens_per_call_allowance", 0) or 0)
    out = int(a.get("output_tokens_per_call_allowance", 0) or 0)
    in_tokens = D(images) * D(str(pin["tokens_per_image"])) + D(text_in)
    usd = in_tokens * D(str(pin["usd_per_1m_input_tokens"])) / D(1_000_000) + D(out) * D(str(pin["usd_per_1m_output_tokens"])) / D(1_000_000)
    return usd.quantize(D("0.000001"), rounding=ROUND_HALF_UP)


def actual_usd(usage: dict, pin: dict | None) -> Decimal | None:
    if not pin or not usage:
        return None
    p_in = D(str(usage.get("promptTokenCount") or 0)) * D(str(pin["usd_per_1m_input_tokens"])) / D(1_000_000)
    p_out = D(str((usage.get("candidatesTokenCount") or 0) + (usage.get("thoughtsTokenCount") or 0))) * D(str(pin["usd_per_1m_output_tokens"])) / D(1_000_000)
    return (p_in + p_out).quantize(D("0.000001"), rounding=ROUND_HALF_UP)


def load_auth(path: Path | str | None) -> dict:
    """{screen_cap_usd: Decimal, screen_max_calls: int | None, ...}. No file, no block, no cap -> cap 0 -> forbidden."""
    if not path:
        return {"path": None, "screen_cap_usd": D("0"), "screen_max_calls": None, "present": False}
    p = Path(path)
    if not p.exists():
        raise ScreenRefused(f"--auth {p} does not exist; nothing was sent")
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    block = data
    for key in ("screen_authorisation", "machine_authorisation"):
        if isinstance(data.get(key), dict) and "screen_cap_usd" in data[key]:
            block = data[key]
            break
    raw = block.get("screen_cap_usd")
    try:
        cap = D(str(raw)) if raw is not None else D("0")
    except Exception:  # noqa: BLE001
        raise ScreenRefused(f"--auth {p.name}: screen_cap_usd {raw!r} is not a number; nothing was sent") from None
    mc = block.get("screen_max_calls")
    return {"path": str(p), "sha256": _sha256_file(p), "screen_cap_usd": cap, "screen_max_calls": (int(mc) if mc is not None else None),
            "approved_by": block.get("approved_by"), "approved_at": str(block.get("approved_at") or ""), "present": True}


def assert_live_allowed(auth: dict, pin: dict | None) -> None:
    if not auth.get("present"):
        raise ScreenRefused("live screening needs --auth <file> carrying screen_cap_usd; without it the cap is 0 and every call is forbidden. Nothing was sent.")
    if auth["screen_cap_usd"] <= 0:
        raise ScreenRefused(f"--auth {Path(auth['path']).name}: screen_cap_usd is {auth['screen_cap_usd']} (missing = 0 = forbidden). Nothing was sent.")
    if pin is None:
        raise ScreenRefused("price not pinned: no PIN-INDEX entry with the required Gemini API price fields, so the cap cannot be enforced. Nothing was sent.")


# ------------------------------------------------------------------------------ statistics
def confusion(pairs: list) -> dict:
    """pairs = [(controller, screen)] over accept / reject only. Confusion keyed controller -> screen."""
    c = {"accept": {"accept": 0, "reject": 0}, "reject": {"accept": 0, "reject": 0}}
    for ctrl, scr in pairs:
        if ctrl in JUDGED and scr in JUDGED:
            c[ctrl][scr] += 1
    return c


def cohens_kappa(c: dict) -> float | None:
    aa, ar, ra, rr = c["accept"]["accept"], c["accept"]["reject"], c["reject"]["accept"], c["reject"]["reject"]
    n = aa + ar + ra + rr
    if n == 0:
        return None
    po = (aa + rr) / n
    pe = ((aa + ar) * (aa + ra) + (ra + rr) * (ar + rr)) / (n * n)
    if pe >= 1.0:
        return 1.0 if po >= 1.0 else 0.0
    return (po - pe) / (1 - pe)


def agreement_stats(pairs: list) -> dict:
    c = confusion(pairs)
    aa, ar, ra, rr = c["accept"]["accept"], c["accept"]["reject"], c["reject"]["accept"], c["reject"]["reject"]
    n = aa + ar + ra + rr
    k = cohens_kappa(c)
    return {"n_compared": n, "agree": aa + rr, "agreement_rate": (round((aa + rr) / n, 4) if n else None),
            "cohens_kappa": (round(k, 4) if k is not None else None),
            "false_accept_rate": (round(ra / (ra + rr), 4) if (ra + rr) else None), "false_accepts": ra, "controller_rejects": ra + rr,
            "false_reject_rate": (round(ar / (aa + ar), 4) if (aa + ar) else None), "false_rejects": ar, "controller_accepts": aa + ar,
            "confusion_controller_x_screen": c}


def qualification(stats: dict, coverage: dict, criteria: dict) -> dict:
    t = criteria.get("thresholds") or {}
    reasons = []
    n = stats["n_compared"]
    if n < int(t.get("min_compared_trials", 0)):
        would = "insufficient_n"
        reasons.append(f"compared trials {n} < min_compared_trials {t.get('min_compared_trials')}")
    else:
        ok = True
        k, far, cov = stats["cohens_kappa"], stats["false_accept_rate"], coverage.get("coverage_fraction")
        if k is None or k < float(t.get("cohens_kappa_min", 1.0)):
            ok = False
            reasons.append(f"cohens_kappa {k} < {t.get('cohens_kappa_min')}")
        if far is None or far > float(t.get("false_accept_rate_max", 0.0)):
            ok = False
            reasons.append(f"false_accept_rate {far} > {t.get('false_accept_rate_max')}" if far is not None else "false_accept_rate undefined (no Controller rejects compared)")
        if cov is None or cov < float(t.get("min_coverage_fraction", 1.0)):
            ok = False
            reasons.append(f"coverage_fraction {cov} < {t.get('min_coverage_fraction')}")
        would = "qualified" if ok else "screened_not_qualified"
    frozen = bool(criteria.get("_frozen"))
    verdict = would if (frozen and would == "qualified") else "screened_not_qualified"
    if not frozen:
        reasons.append("SCREEN-QUALIFICATION-CRITERIA-v0.yaml is not frozen: the verdict stays screened_not_qualified whatever the numbers say")
    return {"qualification_verdict": verdict, "would_verdict": would, "criteria_frozen": frozen, "thresholds": dict(t), "reasons": reasons,
            "binding": frozen, "note": "qualified never makes a screen verdict a Registry row: registry_gate admits no capability for vlm_screen"}


# ------------------------------------------------------------------------------ the run
def screen_rows(rows: list, cases: dict, inst, pin: dict | None, cap_usd: Decimal, criteria: dict, max_calls: int | None = None, log=print) -> dict:
    """Runs the instrument over the planned rows in order, projecting each call against the cap BEFORE it is made."""
    spent = D("0")
    calls = 0                 # calls SENT. Incremented once per dispatch, never recomputed from the rows afterwards.
    refused = 0               # screenable calls NOT sent because the run had already stopped
    out = []
    stopped = None
    stopped_by = None
    for row in rows:
        rec = {k: row[k] for k in ("run_id", "results_run_id", "trial_id", "case_id", "question", "route_key", "arm", "controller_verdict", "controller_note", "media_kind")}
        rec["artifact"] = {"path": _rel(row["artifact"]) if row["artifact"] else None}
        rec["call_sent"] = False
        if row["skip"] and row["media_kind"] != "audio":
            rec.update({"screen_overall": None, "verdict": "absent", "absence_reason": "not_measured", "note": f"skipped: {row['skip']}", "rules": [], "agree": None})
            out.append(rec)
            continue
        case = cases["cases"][row["case_id"]]
        if row["calls"]:
            if stopped:
                refused += 1
                rec.update({"screen_overall": None, "verdict": "absent", "absence_reason": "not_measured", "note": stopped, "rules": [], "agree": None})
                out.append(rec)
                continue
            est = per_call_estimate_usd(row["images"], pin, criteria) if pin else D("0")
            if max_calls is not None and calls >= max_calls:
                stopped = f"stopped: screen_max_calls {max_calls} reached; nothing further was sent"
                stopped_by = "screen_max_calls"
                refused += 1
                rec.update({"screen_overall": None, "verdict": "absent", "absence_reason": "not_measured", "note": stopped, "rules": [], "agree": None})
                out.append(rec)
                continue
            # reservation-first, like the battery ledger: every call reserves its estimate and the reservations may never exceed
            # the cap; the settled spend (tokens x pinned price) is checked as well so an under-estimate cannot run past it
            if spent + est > cap_usd or (calls + 1) * est > cap_usd:
                stopped = (f"stopped: call {calls + 1} would cross screen_cap_usd {cap_usd} (reserved {calls} x USD {est} + USD {est}; settled USD {spent}); "
                           f"nothing further was sent")
                stopped_by = "screen_cap_usd"
                refused += 1
                rec.update({"screen_overall": None, "verdict": "absent", "absence_reason": "not_measured", "note": stopped, "rules": [], "agree": None})
                out.append(rec)
                continue
            calls += 1
            rec["call_sent"] = True
        r = inst.fn(row["artifact"], {"instrument_inputs": {"acceptance_contract": case["acceptance_contract"], "case_row": case}}, "acceptance_contract_screen")
        m = r.get("measurement") or {}
        usd = actual_usd(m.get("usage") or {}, pin)
        if usd is not None:
            spent += usd
        rec.update({"screen_overall": r.get("overall"), "verdict": r["verdict"], "absence_reason": r.get("absence_reason"), "note": r.get("note"),
                    "rules": r.get("rules") or [], "http_status": m.get("http_status"), "usage": m.get("usage"), "frames": m.get("frames"),
                    "artifact": {"path": rec["artifact"]["path"], "sha256": m.get("artifact_sha256"), "media_kind": m.get("media_kind")},
                    "usd_at_pinned_price": (str(usd) if usd is not None else None),
                    "agree": ((r.get("overall") == row["controller_verdict"]) if r.get("overall") in JUDGED else None)})
        out.append(rec)
        log(f"  {row['trial_id']}: controller={row['controller_verdict']} screen={r.get('overall')} ({r['verdict']}{'/' + str(r.get('absence_reason')) if r.get('absence_reason') else ''})")
    return {"rows": out, "calls": calls, "refused": refused, "spent_usd": spent, "stopped": stopped, "stopped_by": stopped_by}


COUNTERS_KEY = "call_counters"
COUNTERS_SCHEMA = "SCREEN-CALL-COUNTERS-v0"
BASIS_LIVE = "live_counter"
BASIS_MISSING = "not_recorded_by_the_live_run"
NO_LIVE_COUNT = ("this report was rebuilt offline from SCREEN-RESULTS files that carry no live call counter, so the number of "
                 "calls the screening run actually sent is NOT KNOWN from the repository. Counting screened rows is not the same "
                 "number: a row is not a call (audio rows are decided cannot_judge without any call, and a skipped or refused row "
                 "sends nothing). Re-run the screening to record a counter, or read the run log.")


def call_counters(calls: int, refused: int, stopped: str | None, stopped_by: str | None, auth: dict,
                  this_file: int | None = None) -> dict:
    """The live run's own account of what it sent. Written into every SCREEN-RESULTS file so a later offline rebuild
    reports THIS number instead of recomputing one from the rows (a row is not a call)."""
    return {"schema": COUNTERS_SCHEMA, "source": BASIS_LIVE,
            "screening_calls_sent": int(calls), "screening_calls_refused": int(refused),
            "calls_sent_for_trials_in_this_file": (int(this_file) if this_file is not None else None),
            "screen_max_calls": auth.get("screen_max_calls"),
            "screen_cap_usd": (str(auth["screen_cap_usd"]) if auth.get("present") else None),
            "stopped": stopped, "stopped_by": stopped_by}


def live_call_counters(docs: list) -> dict:
    """What the LIVE screening run recorded, read back off its SCREEN-RESULTS documents. Returns calls None (and a basis
    saying why) whenever there is no single live counter to report - the report then prints no number at all."""
    none = {"calls": None, "refused": None, "stopped": None, "stopped_by": None, "basis": BASIS_MISSING}
    counters = [d[COUNTERS_KEY] for d in docs if isinstance((d or {}).get(COUNTERS_KEY), dict)]
    if not counters:
        return none
    sent = {int(c["screening_calls_sent"]) for c in counters if c.get("screening_calls_sent") is not None}
    if len(sent) != 1:
        return {**none, "basis": (f"conflicting_live_counters:{sorted(sent)}" if sent else BASIS_MISSING)}
    return {"calls": sent.pop(), "basis": BASIS_LIVE,
            "refused": max((int(c.get("screening_calls_refused") or 0) for c in counters), default=None),
            "stopped": next((c.get("stopped") for c in counters if c.get("stopped")), None),
            "stopped_by": next((c.get("stopped_by") for c in counters if c.get("stopped_by")), None)}


def calls_section(calls: int | None, basis: str, auth: dict, stopped: str | None, stopped_by: str | None) -> dict:
    """How the report is allowed to talk about the call count. `calls` is None whenever no live counter exists - the
    report then says so in words and prints NO number that could be mistaken for an authoritative one."""
    limit = auth.get("screen_max_calls")
    at_limit = (calls is not None and limit is not None and int(calls) >= int(limit))
    sec = {"calls": (int(calls) if calls is not None else None), "calls_basis": basis,
           "authorised_screen_max_calls": limit,
           "calls_at_or_above_authorised_limit": (at_limit if (calls is not None and limit is not None) else None),
           "stopped": stopped, "stopped_by": stopped_by}
    if calls is None:
        sec["calls_note"] = NO_LIVE_COUNT
    elif limit is None:
        sec["calls_note"] = f"{calls} call(s) sent (live counter); no screen_max_calls was authorised, so there is no limit to compare against"
    elif at_limit:
        sec["calls_note"] = (f"ATTENTION: the live counter records {calls} call(s) sent against an authorised screen_max_calls of {limit}. "
                             f"The run is at or above its authorised limit"
                             + (f" and stopped on {stopped_by}." if stopped_by else "; no stop was recorded, which needs explaining."))
    else:
        sec["calls_note"] = f"{calls} call(s) sent (live counter), within the authorised screen_max_calls of {limit}"
    return sec


def build_report(screened: list, rows: list, inst, criteria: dict, cases: dict, auth: dict, pin: dict | None, calls: int | None, spent: Decimal,
                 results_paths: list, stopped: str | None, dry: bool, calls_basis: str = BASIS_LIVE, refused: int | None = None,
                 stopped_by: str | None = None) -> dict:
    judged = [r for r in rows if r["controller_verdict"] in JUDGED]
    with_art = [r for r in judged if r["artifact"] and r["media_kind"] in ("image", "video")]
    audio = [r for r in judged if r["media_kind"] == "audio"]
    compared = [s for s in screened if s.get("screen_overall") in JUDGED and s["controller_verdict"] in JUDGED]
    cannot = [s for s in screened if s.get("screen_overall") == "cannot_judge"]
    errors = [s for s in screened if s.get("screen_overall") is None and s["media_kind"] in ("image", "video")]
    pairs = [(s["controller_verdict"], s["screen_overall"]) for s in compared]
    stats = agreement_stats(pairs)
    coverage = {"judged_trials": len(judged), "screenable_trials": len(with_art), "audio_planned_cannot_judge": len(audio),
                "skipped_no_artifact_or_case": len(judged) - len(with_art) - len(audio), "screened": len([s for s in screened if s["media_kind"] in ("image", "video")]),
                "compared": len(compared), "cannot_judge": len(cannot), "errors_or_unscreened": len(errors),
                "coverage_fraction": (round(len(compared) / len(with_art), 4) if with_art else None)}
    by_q, by_r = defaultdict(list), defaultdict(list)
    for s in compared:
        by_q[s["question"]].append((s["controller_verdict"], s["screen_overall"]))
        by_r[s["route_key"]].append((s["controller_verdict"], s["screen_overall"]))
    disagreements = [{"trial_id": s["trial_id"], "run_id": s["run_id"], "question": s["question"], "route_key": s["route_key"], "case_id": s["case_id"],
                      "controller_verdict": s["controller_verdict"], "controller_note": s["controller_note"], "screen_overall": s["screen_overall"],
                      "screen_rules": [{"rule_id": r["rule_id"], "verdict": r["verdict"], "evidence": r["evidence"]} for r in s.get("rules", [])
                                       if r["verdict"] != "pass" or s["controller_verdict"] == "reject"]}
                     for s in compared if s["controller_verdict"] != s["screen_overall"]]
    q = qualification(stats, coverage, criteria)
    return {
        "schema": "QUALIFICATION-REPORT-v0", "generated_utc": _now(), "mode": "dry_run" if dry else "live",
        "instrument": {"id": inst.id, "version": inst.version, "model": inst.session.model, "config_hash": inst.config_hash,
                       "qualification_status_at_run": inst.qualification_status, "surface": VS.SURFACE, "credential_name": VS.KEY_NAME},
        "criteria": {"ref": VS.CRITERIA_REF, "sha256": criteria["_sha256"], "frozen": criteria["_frozen"], "status": criteria.get("status")},
        "inputs": {"results": [_rel(p) for p in results_paths], "test_cases": _rel(cases["_path"]), "test_cases_sha256": cases["_sha256"],
                   "authorisation": ({"path": _rel(auth["path"]), "sha256": auth.get("sha256"), "screen_cap_usd": str(auth["screen_cap_usd"]),
                                      "screen_max_calls": auth.get("screen_max_calls")} if auth.get("present") else None)},
        "coverage": coverage, "agreement": stats,
        "per_question": {k: agreement_stats(v) for k, v in sorted(by_q.items(), key=lambda kv: str(kv[0]))},
        "per_route": {k: agreement_stats(v) for k, v in sorted(by_r.items(), key=lambda kv: str(kv[0]))},   # a None route_key must not crash the report
        "disagreements": disagreements,
        "cannot_judge": [{"trial_id": s["trial_id"], "question": s["question"], "route_key": s["route_key"], "controller_verdict": s["controller_verdict"],
                          "rules_cannot_judge": [r["rule_id"] for r in s.get("rules", []) if r["verdict"] == "cannot_judge"]} for s in cannot],
        "errors": [{"trial_id": s["trial_id"], "note": s.get("note"), "http_status": s.get("http_status")} for s in errors],
        "spend": {**calls_section(calls, calls_basis, auth, stopped, stopped_by),
                  "calls_refused": refused, "screened_rows": len(screened),
                  "price_pinned": pin is not None, "price_pin": pin, "usd_at_pinned_price": (str(spent) if pin else None),
                  "prompt_tokens": inst.session.prompt_tokens, "output_tokens": inst.session.output_tokens, "total_tokens": inst.session.total_tokens},
        "qualification": q,
    }


def screen_results_doc(run_results_path: Path, rows: list, inst, criteria: dict, counters: dict | None = None) -> dict:
    doc = yaml.safe_load(Path(run_results_path).read_text(encoding="utf-8")) or {}
    return {"schema": "SCREEN-RESULTS-v0", "run_id": doc.get("run_id") or Path(run_results_path).parent.name, "results_ref": _rel(run_results_path),
            "draw_class": EM.draw_class_of(doc),
            **({COUNTERS_KEY: counters} if counters else {}),
            "results_sha256": _sha256_file(run_results_path), "screened_utc": _now(),
            "instrument": {"id": inst.id, "version": inst.version, "model": inst.session.model, "config_hash": inst.config_hash,
                           "qualification_status": inst.qualification_status, "surface": VS.SURFACE, "credential_name": VS.KEY_NAME},
            "criteria_sha256": criteria["_sha256"], "registry": False,
            "note": "screened_not_qualified tier input for evidence_map.py; never a Registry row; qualification is decided by QUALIFICATION-REPORT.yaml",
            "trials": rows}


# ------------------------------------------------------------------------------ dry run
def dry_run_text(rows: list, pin: dict | None, criteria: dict, model: str) -> str:
    lines = [f"qualify_screen DRY RUN - model {model} (config, not a claim) - NOTHING IS SENT"]
    per_run: dict = defaultdict(Counter)
    for r in rows:
        c = per_run[r["results_run_id"]]
        c["trials"] += 1
        if r["controller_verdict"] in JUDGED:
            c["judged"] += 1
        if r["calls"]:
            c["calls"] += r["calls"]
            c["images"] += r["images"]
            c["frames"] += (r["images"] if r["media_kind"] == "video" else 0)
            c[r["media_kind"]] += 1
        elif r["media_kind"] == "audio":
            c["audio_cannot_judge"] += 1
        elif r["skip"]:
            c["skipped"] += 1
    tot = Counter()
    for run, c in sorted(per_run.items()):
        tot.update(c)
        lines.append(f"  {run:<18} trials {c['trials']:>3}  judged {c['judged']:>3}  calls {c['calls']:>3}  (images {c['image']:>3}, videos {c['video']:>3} -> {c['frames']:>3} frames)"
                     f"  audio cannot_judge {c['audio_cannot_judge']:>2}  skipped {c['skipped']:>2}")
    lines.append(f"  {'TOTAL':<18} trials {tot['trials']:>3}  judged {tot['judged']:>3}  calls {tot['calls']:>3}  (images {tot['image']:>3}, videos {tot['video']:>3} -> {tot['frames']:>3} frames)"
                 f"  audio cannot_judge {tot['audio_cannot_judge']:>2}  skipped {tot['skipped']:>2}")
    lines.append(f"  inline images to send: {tot['images']} (each video = {VS.VIDEO_FRAMES} PNG frames, longest side <= {VS.FRAME_MAX_SIDE} px)")
    for r in rows:
        if r["skip"] and r["media_kind"] != "audio" and r["controller_verdict"] in JUDGED:
            lines.append(f"    skipped {r['results_run_id']}/{r['trial_id']}: {r['skip']}")
    if pin:
        total = sum((per_call_estimate_usd(r["images"], pin, criteria) for r in rows if r["calls"]), D("0"))
        lines.append(f"  cost estimate at the pinned price ({pin['index']} route_key {pin['route_key']}, fetched {pin['fetched_utc']}): USD {total}")
    else:
        spec = criteria.get("price_pin") or {}
        lines.append(f"  cost estimate: price not pinned (no {spec.get('index', 'PIN-INDEX.yaml')} entry route_key {spec.get('route_key')!r} with {spec.get('required_fields')}); no number")
    lines.append("  a live run needs --auth <file> with screen_cap_usd > 0 AND the pinned price; without either every call is refused")
    return "\n".join(lines)


# ------------------------------------------------------------------------------ CLI
def expand_results(patterns: list) -> list:
    paths = []
    for pat in patterns:
        is_glob = any(ch in pat for ch in "*?[")
        hits = sorted(glob.glob(pat)) if is_glob else [pat]
        if not [h for h in hits if Path(h).exists()] and not Path(pat).is_absolute():      # a repo-relative pattern from any cwd
            alt = str(hv2_paths.REPO_ROOT / pat)
            hits = sorted(glob.glob(alt)) if is_glob else [alt]
        paths += [Path(h) for h in hits]
    paths = [p for p in paths if p.exists()]
    if not paths:
        raise ScreenRefused(f"no RESULTS.yaml matched {patterns}")
    return paths


class _OfflineSession:
    """Stands in for the live ScreenSession when a report is rebuilt from written SCREEN-RESULTS files."""
    def __init__(self, model, prompt_tokens, output_tokens):
        self.model, self.prompt_tokens, self.output_tokens = model, prompt_tokens, output_tokens
        self.total_tokens = prompt_tokens + output_tokens


class _OfflineInstrument:
    def __init__(self, doc_instrument: dict, session):
        self.id = doc_instrument.get("id"); self.version = doc_instrument.get("version"); self.config_hash = doc_instrument.get("config_hash")
        self.qualification_status = doc_instrument.get("qualification_status", "screened_not_qualified"); self.session = session


def report_from_screen_results(a, rows, cases, criteria, pin, results_paths, log) -> int:
    """Rebuild the report from SCREEN-RESULTS.yaml files already on disk. Nothing is sent; spend is the sum recorded per trial."""
    import glob as _glob
    files = sorted(_glob.glob(a.report_from_screen_results))
    if not files:
        log(f"REFUSED: no SCREEN-RESULTS files match {a.report_from_screen_results!r}")
        return 2
    screened, inst_doc, p_tok, o_tok, spent = [], None, 0, 0, Decimal("0")
    docs = []
    for f in files:
        doc = yaml.safe_load(Path(f).read_text(encoding="utf-8")) or {}
        docs.append(doc)
        inst_doc = inst_doc or doc.get("instrument") or {}
        for t in doc.get("trials", []):
            screened.append(t)
            u = t.get("usage") or {}
            p_tok += int(u.get("promptTokenCount") or 0); o_tok += int((u.get("candidatesTokenCount") or 0) + (u.get("thoughtsTokenCount") or 0))
            spent += Decimal(str(t.get("usd_at_pinned_price") or 0))
    # The call count is the LIVE run's own counter or nothing. It is never recomputed from the screened rows:
    # a row is not a call (an audio row is cannot_judge with no call; a skipped or refused row sends nothing).
    live = live_call_counters(docs)
    calls, refused, stopped, stopped_by, calls_basis = live["calls"], live["refused"], live["stopped"], live["stopped_by"], live["basis"]
    inst = _OfflineInstrument(inst_doc or {}, _OfflineSession((inst_doc or {}).get("model"), p_tok, o_tok))
    auth = load_auth(a.auth) if a.auth else {"present": False}
    report = build_report(screened, rows, inst, criteria, cases, auth, pin, calls, spent, results_paths, stopped, dry=False,
                          calls_basis=calls_basis, refused=refused, stopped_by=stopped_by)
    report["mode"] = "rebuilt_offline_from_screen_results"
    report["rebuilt_from"] = [_rel(Path(f)) for f in files]
    out = Path(a.out); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("# QUALIFICATION-REPORT-v0 - rebuilt OFFLINE by eval/harness-v2/qualify_screen.py from SCREEN-RESULTS.yaml files (no call); criteria unfrozen until the Controller freezes it.\n"
                   + yaml.safe_dump(report, allow_unicode=True, sort_keys=False, width=140), encoding="utf-8")
    q = report["qualification"]
    log(f"wrote {out}: compared {report['agreement']['n_compared']}, agreement {report['agreement']['agreement_rate']}, kappa {report['agreement']['cohens_kappa']}, "
        f"false-accept {report['agreement']['false_accept_rate']}; verdict {q['qualification_verdict']} (would be {q['would_verdict']}); "
        f"calls {calls if calls is not None else 'NOT RECORDED by the live run (see spend.calls_note)'}, USD {spent}")
    return 0


def main(argv=None, transport=None, key_reader=None, log=print) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--results", action="append", required=True, help="RESULTS.yaml path or glob (repeatable)")
    ap.add_argument("--test-cases", default=str(hv2_paths.TEST_CASES))
    ap.add_argument("--runs-root", default=str(RUNS_ROOT), help="where a trial's run_id directory is looked up (redo trials)")
    ap.add_argument("--criteria", default=str(VS.CRITERIA_PATH))
    ap.add_argument("--pin-index", default=None, help="override the PIN-INDEX.yaml named in the criteria file (tests)")
    ap.add_argument("--model", default=VS.DEFAULT_MODEL)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--auth", default=None, help="YAML with screen_cap_usd (and optional screen_max_calls); required for any call")
    ap.add_argument("--out", default=str(DEFAULT_REPORT), help="QUALIFICATION-REPORT.yaml path")
    ap.add_argument("--screen-out-dir", default=None, help="write <dir>/<run_id>/SCREEN-RESULTS.yaml instead of beside each RESULTS.yaml")
    ap.add_argument("--limit", type=int, default=None, help="screen only the first N screenable trials (a smoke)")
    ap.add_argument("--report-from-screen-results", default=None, metavar="GLOB",
                    help="OFFLINE: rebuild QUALIFICATION-REPORT.yaml from already-written SCREEN-RESULTS.yaml files (no call, no spend)")
    a = ap.parse_args(argv)
    try:
        criteria = VS.load_criteria(a.criteria)
        cases = load_cases(a.test_cases)
        results_paths = expand_results(a.results)
        rows = plan_trials(results_paths, cases, Path(a.runs_root) if a.runs_root else None)
        pin = price_pin(criteria, a.pin_index)
        if a.dry_run:
            log(dry_run_text(rows, pin, criteria, a.model))
            return 0
        auth = load_auth(a.auth)
        assert_live_allowed(auth, pin)
    except ScreenRefused as exc:
        log(f"REFUSED: {exc}")
        return 2
    if a.report_from_screen_results:
        return report_from_screen_results(a, rows, cases, criteria, pin, results_paths, log)
    screenable = [r for r in rows if r["calls"]]
    if a.limit is not None:
        keep = {id(r) for r in screenable[:a.limit]}
        for r in screenable:
            if id(r) not in keep:
                r["skip"], r["calls"] = f"--limit {a.limit}", 0
    max_calls = auth.get("screen_max_calls")
    n_calls = sum(r["calls"] for r in rows)
    inst = VS.instrument(transport=transport, model=a.model, key_reader=key_reader, criteria_path=a.criteria,
                         max_calls=min(n_calls, max_calls) if max_calls is not None else n_calls)
    log(f"qualify_screen LIVE: {n_calls} planned calls, cap USD {auth['screen_cap_usd']}, max_calls {max_calls}, price pin {pin['route_key']} ({pin['index']})")
    res = screen_rows(rows, cases, inst, pin, auth["screen_cap_usd"], criteria, max_calls, log=log)
    by_results: dict = defaultdict(list)
    for row, rec in zip(rows, res["rows"]):
        by_results[row["results_path"]].append(rec)
    for rp, recs in by_results.items():
        rp = Path(rp)
        dest = (Path(a.screen_out_dir) / rp.parent.name / SCREEN_RESULTS_FILE) if a.screen_out_dir else rp.parent / SCREEN_RESULTS_FILE
        dest.parent.mkdir(parents=True, exist_ok=True)
        counters = call_counters(res["calls"], res["refused"], res["stopped"], res["stopped_by"], auth,
                                 this_file=sum(1 for r in recs if r.get("call_sent")))
        dest.write_text("# SCREEN-RESULTS-v0 - written by eval/harness-v2/qualify_screen.py; screened_not_qualified tier input; never a Registry row.\n"
                        + yaml.safe_dump(screen_results_doc(rp, recs, inst, criteria, counters), allow_unicode=True, sort_keys=False, width=140), encoding="utf-8")
        log(f"wrote {dest} ({len(recs)} trials)")
    report = build_report(res["rows"], rows, inst, criteria, cases, auth, pin, res["calls"], res["spent_usd"], results_paths, res["stopped"], dry=False,
                          calls_basis=BASIS_LIVE, refused=res["refused"], stopped_by=res["stopped_by"])
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("# QUALIFICATION-REPORT-v0 - written by eval/harness-v2/qualify_screen.py against SCREEN-QUALIFICATION-CRITERIA-v0.yaml (unfrozen until the Controller freezes it).\n"
                   + yaml.safe_dump(report, allow_unicode=True, sort_keys=False, width=140), encoding="utf-8")
    q = report["qualification"]
    log(f"wrote {out}: compared {report['agreement']['n_compared']}, agreement {report['agreement']['agreement_rate']}, kappa {report['agreement']['cohens_kappa']}, "
        f"false-accept {report['agreement']['false_accept_rate']}; verdict {q['qualification_verdict']} (would be {q['would_verdict']}); calls {res['calls']}, USD {res['spent_usd']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
