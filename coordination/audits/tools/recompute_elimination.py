#!/usr/bin/env python3
"""Recompute EVAL-040 elimination under the LITERAL frozen rule.

Read-only.  No network.  Standard library + PyYAML only.

Run from the repository root:

    python3 coordination/audits/tools/recompute_elimination.py

The frozen rule is eval/empirical-planning/STAGE-A-FREEZE-2026-09/ELIMINATION-RULES.md:

  E1  a route is out for a question when refusals or hard errors reach
      ceil(0.375 * n)
  E2  a route is out for a question when accepts are <= floor(0.25 * n)
  E5  "A refusal or error is counted under E1 and is also a reject for E2's
      denominator."
      "Nothing here is changed mid-run; a change is a new task."

n is the PLANNED trial count for the (question, route, arm) group.

Three sections are printed:

  SECTION A  every logical trial id dispatched in more than one run, with the
             run id, mode (smoke / core / redo), status, whether an artifact
             was sealed, and the ledger entry types recorded in that run.
  SECTION B  E1/E2 recomputed for every (question, route, arm) directly from
             the sealed attempts, side by side with what the committed
             RESULTS.yaml recorded.  Two literal readings are shown because the
             frozen rule does not provide for re-dispatching a failed trial:
               STRICT   a logical trial that errored or was refused in any run
                        stays a refusal (and therefore a reject), whatever a
                        later re-dispatch produced.
               LENIENT  the last attempt of a logical trial is the one that
                        counts, so a successful re-dispatch replaces the error.
             Neither reading is recommended here.  The choice is the
             Controller's.
  SECTION C  every routing-map cell and every RR rule whose numbers or wording
             rest on a group where the readings differ.

The script decides nothing.  It only reports.

Rulings applied on 14 September 2026 (record:
coordination/decisions/CONTROLLER-AUDIT-CLOSEOUT-EVIDENCE-RULINGS-2026-09-14.md):

  C-3   the frozen rule is applied literally; infrastructure / request failures
        count wherever the preregistered rule says they count.
  C-6b  STRICT: a draw that failed once stays a failure; a later re-send is
        descriptive product evidence and is never counted.  The STRICT column
        is therefore the counting column; LENIENT is still printed so the
        reader can see what the runs themselves did.
  C-6c  exact-text mechanisms are DIFFERENT routes.  A trial judged in a run
        whose RESULTS.yaml records `layout: composite-v2` (the provider made a
        textless plate; deterministic code composed the exact strings) carries
        the route identity `<route>+code_overlay`.  The four img-r1 /
        img-r1-composite ids therefore no longer collide: the img-r1-composite
        dispatch is `distinct_mechanism (C-6c)`, not a re-send.
  C-6d  elimination is per (route, question), exactly as frozen E4.

The map generator (eval/harness-v2/evidence_map.py) and the taint register
builder (build_taint_register.py) import this file and call `cell_numbers`;
this is the ONLY implementation of the elimination arithmetic.
"""

from __future__ import annotations

import json
import math
import os
import re
import sys
from collections import defaultdict

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("PyYAML is required: python3 -m pip install pyyaml\n")
    raise SystemExit(2)


RUNS_DIR = os.path.join("eval", "experiments", "EVAL-040", "runs")
MAP_PATH = os.path.join("eval", "capability-map", "ROUTING-EVIDENCE-MAP-v0.yaml")
RULES_PATH = os.path.join(
    "eval", "empirical-planning", "STAGE-A-FREEZE-2026-09", "ELIMINATION-RULES.md"
)

ERROR_STATUSES = {"error", "refusal", "refused"}

# C-6c: a run whose RESULTS rows record this layout judged code-composed text
# on a textless plate -- a different route mechanism from the model drawing
# the text itself.  Its trials carry the route identity <route>+CODE_OVERLAY.
COMPOSITE_LAYOUT = "composite-v2"
CODE_OVERLAY_SUFFIX = "+code_overlay"
DISTINCT_MECHANISM = "distinct_mechanism (C-6c)"
RULINGS_RECORD = (
    "coordination/decisions/CONTROLLER-AUDIT-CLOSEOUT-EVIDENCE-RULINGS-2026-09-14.md"
)

# case ids are <QUESTION>-<NN>; VID-T2V-01 -> VID-T2V, MUS-01 -> MUS
CASE_SUFFIX = re.compile(r"-\d+$")


# --------------------------------------------------------------------------
# loading
# --------------------------------------------------------------------------


def repo_root() -> str:
    """The repository root, whether the script is run from root or elsewhere."""
    here = os.path.dirname(os.path.abspath(__file__))
    # coordination/audits/tools -> repo root
    guess = os.path.abspath(os.path.join(here, "..", "..", ".."))
    if os.path.isdir(os.path.join(guess, RUNS_DIR)):
        return guess
    cwd = os.path.abspath(os.getcwd())
    if os.path.isdir(os.path.join(cwd, RUNS_DIR)):
        return cwd
    sys.stderr.write(
        "cannot locate the repository root: %s not found under %s or %s\n"
        % (RUNS_DIR, guess, cwd)
    )
    raise SystemExit(2)


def read_yaml(path: str):
    with open(path, "r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def read_jsonl(path: str):
    out = []
    if not os.path.exists(path):
        return out
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            out.append(json.loads(line))
    return out


def question_of(case_id: str) -> str:
    return CASE_SUFFIX.sub("", case_id or "")


def has_token(text: str, token: str) -> bool:
    """True when `token` appears in `text` as a whole identifier, so that
    `flux-2-pro` does not match `flux-2-pro-edit` and `img-r1` does not match
    `img-r1-composite`."""
    if not token:
        return False
    pattern = r"(?<![A-Za-z0-9-])" + re.escape(token) + r"(?![A-Za-z0-9-])"
    return re.search(pattern, text) is not None


def route_identity(route_key: str, composite_layout: bool) -> str:
    """C-6c: the route identity of a trial.  A trial judged in a run that
    records `layout: composite-v2` is the code-overlay mechanism."""
    if composite_layout and route_key and not route_key.endswith(CODE_OVERLAY_SUFFIX):
        return route_key + CODE_OVERLAY_SUFFIX
    return route_key


def load_runs(root: str, runs_dir: str | None = None) -> dict:
    """One record per run directory: plan header, planned trials, dispatches,
    sealed artifacts, ledger entry types, and the committed RESULTS.yaml.

    `runs_dir` defaults to eval/experiments/EVAL-040/runs under `root`; a test
    may point it at a synthetic tree.  Paths recorded on each run stay relative
    to `root` when the default is used."""
    runs = {}
    base_rel = runs_dir if runs_dir else RUNS_DIR
    base = base_rel if os.path.isabs(base_rel) else os.path.join(root, base_rel)
    for run_dir in sorted(os.listdir(base)):
        run_path = os.path.join(base, run_dir)
        plan_path = os.path.join(run_path, "PLAN.yaml")
        if not os.path.isfile(plan_path):
            continue
        plan = read_yaml(plan_path)
        header = plan.get("header") or {}

        planned = {}
        for trial in plan.get("trials") or []:
            planned[trial["trial_id"]] = {
                "case_id": trial.get("case_id"),
                "route_key": trial.get("route_key"),
                "arm": trial.get("arm"),
                "repeat_index": trial.get("repeat_index"),
            }

        dispatched = {}
        recovered = set()
        pre_dispatch_refusals = {}
        for event in read_jsonl(os.path.join(run_path, "RUN-LOG.jsonl")):
            kind = event.get("event")
            if kind == "dispatched":
                dispatched[event["trial_id"]] = {
                    "at": event.get("at"),
                    "status": event.get("status"),
                    "error_class": event.get("error_class"),
                    "artifact_sha256": event.get("artifact_sha256"),
                }
            elif kind == "recovered":
                # the artifact was fetched from the SAME provider request after a
                # slow poll: no second call, no second charge, no new dispatch
                if event.get("trial_id"):
                    recovered.add(event["trial_id"])
            elif kind == "pre_dispatch_refusal":
                # the harness stopped before anything was sent: no provider
                # behaviour was observed and no money moved
                pre_dispatch_refusals[event["trial_id"]] = event.get("reason")

        sealed = set()
        art_dir = os.path.join(run_path, "artifacts")
        if os.path.isdir(art_dir):
            for name in os.listdir(art_dir):
                if name.endswith(".record.json"):
                    sealed.add(name[: -len(".record.json")])

        ledger_types = defaultdict(set)
        ledger_amounts = defaultdict(float)
        ledger_path = os.path.join(run_path, "ledger", run_dir, "spend-ledger.jsonl")
        for entry in read_jsonl(ledger_path):
            trial_id = entry.get("trial_id")
            if not trial_id:
                continue
            ledger_types[trial_id].add(str(entry.get("type")))
            if entry.get("type") == "spend":
                try:
                    ledger_amounts[trial_id] += float(entry.get("amount_usd_equiv") or 0)
                except (TypeError, ValueError):
                    pass

        results = None
        results_path = os.path.join(run_path, "RESULTS.yaml")
        if os.path.isfile(results_path):
            results = read_yaml(results_path)
        composite_layout = bool(results) and any(
            row.get("layout") == COMPOSITE_LAYOUT for row in results.get("trials") or []
        )

        runs[run_dir] = {
            "dir": run_dir,
            "mode": header.get("mode"),
            "redo_of": header.get("redo_of"),
            "planned": planned,
            "dispatched": dispatched,
            "recovered": recovered,
            "pre_dispatch_refusals": pre_dispatch_refusals,
            "sealed": sealed,
            "ledger_types": {k: sorted(v) for k, v in ledger_types.items()},
            "ledger_spend_usd": dict(ledger_amounts),
            "results": results,
            "results_path": os.path.join(base_rel, run_dir, "RESULTS.yaml")
            if results is not None
            else None,
            "plan_path": os.path.join(base_rel, run_dir, "PLAN.yaml"),
            # C-6c: every judged row of this run records layout composite-v2
            "composite_layout": composite_layout,
        }
    return runs


def runs_from_results_docs(docs: list) -> dict:
    """Pseudo-runs built from RESULTS documents alone -- no PLAN.yaml, no
    RUN-LOG.jsonl, no ledger.  Used where no run directory exists (synthetic
    tests, or a generator run in results-only mode).  Every row is one
    dispatch; a row's own `run_id` names its pseudo-run (so a file that merges
    two runs' rows, like vid-wan2 + vid-wan2-i2v, splits into two).  The
    "planned" denominator is then the distinct trial ids PRESENT IN THE ROWS,
    not the plans -- a row deleted from a results file is invisible here, which
    is exactly why the sealed run directories are the production input."""
    runs: dict = {}
    for doc_index, doc in enumerate(docs):
        if not doc:
            continue
        file_run = doc.get("run_id")
        rows = doc.get("trials") or []
        composite_layout = any(row.get("layout") == COMPOSITE_LAYOUT for row in rows)
        first_run = None
        for row_index, row in enumerate(rows):
            trial_id = row.get("trial_id")
            if not trial_id:
                continue
            parts = trial_id.split("__")
            rid = row.get("run_id") or file_run or "results"
            first_run = first_run or rid
            run = runs.setdefault(
                rid,
                {
                    "dir": rid,
                    "mode": "lane",
                    "redo_of": None,
                    "planned": {},
                    "dispatched": {},
                    "recovered": set(),
                    "pre_dispatch_refusals": {},
                    "sealed": set(),
                    "ledger_types": {},
                    "ledger_spend_usd": {},
                    "results": None,
                    "results_path": None,
                    "plan_path": None,
                    "composite_layout": composite_layout,
                },
            )
            run["planned"][trial_id] = {
                "case_id": row.get("case_id") or (parts[0] if parts else None),
                "route_key": row.get("route_key") or (parts[1] if len(parts) > 1 else None),
                "arm": row.get("arm") or (parts[2] if len(parts) > 2 else None),
                "repeat_index": row.get("repeat_index"),
            }
            run["dispatched"][trial_id] = {
                "at": "%03d-%04d" % (doc_index, row_index),
                "status": row.get("status") or "ok",
                "error_class": row.get("error_class"),
                "artifact_sha256": row.get("sha256"),
            }
        if first_run is not None:
            # the whole document is attached once, so judged_verdicts and
            # recorded_entries see every row and every elimination entry once
            owner = file_run if file_run in runs else first_run
            runs[owner]["results"] = doc
    return runs


# --------------------------------------------------------------------------
# section A -- duplicated logical trial ids
# --------------------------------------------------------------------------


def occurrence_class(run: dict, trial_id: str, earlier_core_runs: list) -> str:
    if run["mode"] == "smoke":
        return "smoke"
    if run.get("composite_layout"):
        # C-6c: not a re-send of the same object -- a different route mechanism
        return DISTINCT_MECHANISM
    if run["redo_of"]:
        return "redo (declared)"
    if earlier_core_runs:
        return "redo (undeclared)"
    return "core"


def build_occurrences(runs: dict) -> dict:
    """logical trial id -> ordered list of dispatch occurrences."""
    raw = defaultdict(list)
    for run_dir in sorted(runs):
        run = runs[run_dir]
        for trial_id, disp in sorted(run["dispatched"].items()):
            raw[trial_id].append((run_dir, disp))

    out = {}
    for trial_id in sorted(raw):
        occs = sorted(raw[trial_id], key=lambda pair: (pair[1]["at"] or "", pair[0]))
        seen_core = []
        rows = []
        for run_dir, disp in occs:
            run = runs[run_dir]
            kind = occurrence_class(run, trial_id, seen_core)
            if kind not in ("smoke", DISTINCT_MECHANISM):
                seen_core.append(run_dir)
            rows.append(
                {
                    "run_id": run_dir,
                    "at": disp["at"],
                    "kind": kind,
                    "status": disp["status"],
                    "error_class": disp["error_class"],
                    "composite_layout": bool(run.get("composite_layout")),
                    "recovered": trial_id in run["recovered"],
                    "sealed": trial_id in run["sealed"],
                    "ledger_types": run["ledger_types"].get(trial_id, []),
                    "ledger_spend_usd": run["ledger_spend_usd"].get(trial_id, 0.0),
                }
            )
        out[trial_id] = rows
    return out


def judged_verdicts(runs: dict) -> dict:
    """(run_id recorded in the RESULTS row, trial id) -> verdict row."""
    out = {}
    for run_dir in sorted(runs):
        results = runs[run_dir]["results"]
        if not results:
            continue
        file_run_id = results.get("run_id")
        for row in results.get("trials") or []:
            # img-r1-composite's rows carry no run_id of their own; fall back to
            # the file's
            row_run = row.get("run_id") or file_run_id
            out[(row_run, row["trial_id"])] = {
                "results_dir": run_dir,
                "status": row.get("status"),
                "verdict": row.get("verdict"),
                "verdict_basis": row.get("verdict_basis"),
                "blind_id": row.get("blind_id"),
                "redo_of": row.get("redo_of"),
                "layout": row.get("layout"),
            }
    return out


def print_section_a(occurrences: dict, verdicts: dict) -> list:
    dups = {tid: rows for tid, rows in occurrences.items() if len(rows) > 1}
    print("=" * 100)
    print("SECTION A -- logical trial ids dispatched in more than one run")
    print("=" * 100)
    print("distinct logical trial ids dispatched : %d" % len(occurrences))
    print("total dispatch events                 : %d"
          % sum(len(rows) for rows in occurrences.values()))
    print("logical trial ids dispatched twice+   : %d" % len(dups))
    print()
    print("note (C-6c): a dispatch marked '%s' was judged in a run whose" % DISTINCT_MECHANISM)
    print("      RESULTS.yaml records layout %s -- code composed the exact strings on a" % COMPOSITE_LAYOUT)
    print("      textless plate.  That is a different route mechanism (route identity")
    print("      <route>%s), not a re-send of the same object; it is grouped and" % CODE_OVERLAY_SUFFIX)
    print("      counted on its own.  Ruling record: %s" % RULINGS_RECORD)
    print()
    for trial_id in sorted(dups):
        print(trial_id)
        for row in dups[trial_id]:
            key = (row["run_id"], trial_id)
            judged = verdicts.get(key)
            judged_txt = (
                "judged=%s(%s)" % (judged["verdict"], judged["verdict_basis"])
                if judged
                else "judged=NOT IN ANY RESULTS.yaml"
            )
            print(
                "    %-24s %-26s status=%-8s err=%-22s recovered=%-5s sealed=%-5s ledger=%-19s spend_usd=%.2f  %s"
                % (
                    row["run_id"],
                    row["kind"],
                    row["status"],
                    str(row["error_class"]),
                    str(row["recovered"]),
                    str(row["sealed"]),
                    ",".join(row["ledger_types"]) or "-",
                    row["ledger_spend_usd"],
                    judged_txt,
                )
            )
        print()
    return sorted(dups)


# --------------------------------------------------------------------------
# section B -- literal recompute
# --------------------------------------------------------------------------


def e1_threshold(n: int) -> int:
    return math.ceil(0.375 * n)


def e2_threshold(n: int) -> int:
    return math.floor(0.25 * n)


def group_of(runs: dict, trial_id: str, run_dir: str | None = None):
    """(question, route identity, arm) for a logical trial id, from the plans.

    `run_dir` names the run the attempt belongs to: its plan supplies the
    metadata and, under C-6c, its `composite_layout` flag decides whether the
    route identity carries the +code_overlay suffix.  Without it the first run
    (alphabetically) that plans the id is used, without the suffix."""
    candidates = [run_dir] if run_dir and run_dir in runs else []
    candidates += [d for d in sorted(runs) if d not in candidates]
    for d in candidates:
        meta = runs[d]["planned"].get(trial_id)
        if meta:
            composite = bool(runs[d].get("composite_layout")) if run_dir else False
            return (
                question_of(meta["case_id"]),
                route_identity(meta["route_key"], composite),
                meta["arm"],
            )
    return None


def case_of(runs: dict, trial_id: str) -> str | None:
    """The case id a logical trial id was planned under."""
    for run_dir in sorted(runs):
        meta = runs[run_dir]["planned"].get(trial_id)
        if meta:
            return meta.get("case_id")
    return None


def recorded_entries(runs: dict, group_keys) -> dict:
    """(question, route, arm) -> list of (results dir, recorded elimination).

    Some RESULTS.yaml files leave `arm` null on the elimination entry even
    though the plan's trials carry one (img-r1, half2).  An entry with a null
    arm is matched to every recomputed group with the same question and route.
    """
    by_qr = defaultdict(list)
    out = defaultdict(list)
    for run_dir in sorted(runs):
        results = runs[run_dir]["results"]
        if not results:
            continue
        for entry in results.get("elimination") or []:
            question = entry.get("question")
            route = entry.get("route_key")
            arm = entry.get("arm")
            if arm is None:
                by_qr[(question, route)].append((run_dir, entry))
            else:
                out[(question, route, arm)].append((run_dir, entry))
    for key in group_keys:
        if key in out:
            continue
        loose = by_qr.get((key[0], key[1]))
        if loose:
            out[key] = list(loose)
    # C-6c: the code-overlay run records per_case totals and no elimination
    # table; carry those totals as what the file recorded, verdict unrecorded
    for run_dir in sorted(runs):
        run = runs[run_dir]
        results = run["results"]
        if not results or not run.get("composite_layout") or not results.get("per_case"):
            continue
        for key in group_keys:
            if key in out or not key[1] or not key[1].endswith(CODE_OVERLAY_SUFFIX):
                continue
            if any(group_of(runs, tid, run_dir) == key for tid in run["planned"]):
                pc = results["per_case"]
                out[key] = [
                    (
                        run_dir,
                        {
                            "question": key[0],
                            "route_key": key[1],
                            "arm": key[2],
                            "n_planned": sum(int(v.get("trials") or 0) for v in pc.values()),
                            "accepts": sum(int(v.get("accepted") or 0) for v in pc.values()),
                            "eliminated": None,
                            "eliminated_by": [],
                            "refusals_or_errors": 0,
                            "recorded_from": "per_case totals; the file holds no elimination table",
                        },
                    )
                ]
    return out


def build_groups(runs: dict, occurrences: dict, verdicts: dict) -> dict:
    """(question, route, arm) -> per-logical-trial outcome under both readings."""
    groups = defaultdict(dict)
    for trial_id, rows in occurrences.items():
        all_non_smoke = [r for r in rows if r["kind"] != "smoke"]
        if not all_non_smoke:
            continue
        # C-6c: attempts of one trial id are partitioned by route identity, so
        # a code-overlay judging and a bare-plate judging are two logical
        # trials in two groups, never one contested trial
        by_identity = defaultdict(list)
        for row in all_non_smoke:
            key = group_of(runs, trial_id, row["run_id"])
            if key is not None:
                by_identity[key].append(row)
        for key, non_smoke in by_identity.items():
            _add_group_trial(runs, groups, key, trial_id, non_smoke, verdicts)

    # trial ids the harness refused before anything was sent and that were never
    # dispatched at all still belong to their group
    for run_dir in sorted(runs):
        run = runs[run_dir]
        for trial_id in sorted(run["pre_dispatch_refusals"]):
            key = group_of(runs, trial_id, run_dir)
            if key is None or trial_id in groups.get(key, {}):
                continue
            groups[key][trial_id] = {
                "attempts": [],
                "strict": "pre_dispatch_refusal",
                "lenient": "pre_dispatch_refusal",
                "pre_dispatch_refusal_runs": [run_dir],
                "conflict": False,
            }
    return groups


def _add_group_trial(runs, groups, key, trial_id, non_smoke, verdicts) -> None:
    """One logical trial (one route identity) -> its ordered attempts and its
    outcome under both readings.  Split out of build_groups so that C-6c can
    call it once per route identity of a trial id."""
    attempts = []
    for row in non_smoke:
        judged = verdicts.get((row["run_id"], trial_id))
        # The sealed record wins where one exists: a RESULTS.yaml row is the
        # settled status of that attempt.  Where the attempt never reached a
        # RESULTS.yaml, the run log's status is used, and a `recovered`
        # event (same provider request, no second call, no second charge)
        # settles it as ok.
        if judged is not None and judged["status"] is not None:
            status = judged["status"]
        elif row["recovered"]:
            status = "ok"
        else:
            status = row["status"]
        attempts.append(
            {
                "run_id": row["run_id"],
                "at": row["at"],
                "kind": row["kind"],
                "status": status,
                "log_status": row["status"],
                "error_class": row["error_class"],
                "recovered": row["recovered"],
                "verdict": judged["verdict"] if judged else None,
                "in_results": judged is not None,
            }
        )
    attempts.sort(key=lambda a: (a["at"] or "", a["run_id"]))

    any_error = any(a["status"] in ERROR_STATUSES for a in attempts)
    last = attempts[-1]
    distinct = {a["verdict"] for a in attempts if a["verdict"]}

    if any_error:
        strict = "refusal_or_error"
    elif len(distinct) > 1:
        # two runs judged the same logical trial id and disagreed; the
        # strict reading refuses to pick a winner and does not credit it as
        # an accept
        strict = "ambiguous"
    else:
        strict = "accept" if last["verdict"] == "accept" else "reject"

    if last["status"] in ERROR_STATUSES:
        lenient = "refusal_or_error"
    else:
        lenient = "accept" if last["verdict"] == "accept" else "reject"

    pdr_runs = sorted(
        run_dir
        for run_dir in runs
        if trial_id in runs[run_dir]["pre_dispatch_refusals"]
    )

    distinct_verdicts = {a["verdict"] for a in attempts if a["verdict"]}
    groups[key][trial_id] = {
        "attempts": attempts,
        "strict": strict,
        "lenient": lenient,
        "pre_dispatch_refusal_runs": pdr_runs,
        "conflict": len(distinct_verdicts) > 1,
    }


def planned_denominator(runs: dict, key) -> int:
    """Distinct logical trial ids planned for the group in every non-smoke run."""
    ids = set()
    for run_dir in sorted(runs):
        run = runs[run_dir]
        if run["mode"] == "smoke":
            continue
        composite = bool(run.get("composite_layout"))
        for trial_id, meta in run["planned"].items():
            if (
                question_of(meta["case_id"]),
                route_identity(meta["route_key"], composite),
                meta["arm"],
            ) == key:
                ids.add(trial_id)
    return len(ids)


def planned_ids(runs: dict, key) -> dict:
    """Distinct logical trial ids planned for the group (non-smoke runs) -> case id."""
    ids = {}
    for run_dir in sorted(runs):
        run = runs[run_dir]
        if run["mode"] == "smoke":
            continue
        composite = bool(run.get("composite_layout"))
        for trial_id, meta in run["planned"].items():
            if (
                question_of(meta["case_id"]),
                route_identity(meta["route_key"], composite),
                meta["arm"],
            ) == key:
                ids[trial_id] = meta.get("case_id")
    return ids


def verdict_for(n: int, refusals: int, accepts: int):
    out_by = []
    if n > 0 and refusals >= e1_threshold(n):
        out_by.append("E1")
    if n > 0 and accepts <= e2_threshold(n):
        out_by.append("E2")
    return out_by


def cell_numbers(runs: dict, groups: dict, occurrences: dict, key) -> dict:
    """Every human-acceptance number for one (question, route identity, arm)
    under the frozen rule applied literally -- C-3 (planned denominator,
    failures counted), C-6b (STRICT: the first sending of a draw is the one
    that counts; every later sending is descriptive), C-6d (per (route,
    question), which is what the key is).  Smoke draws never enter.

    The map generator and the taint register builder both call this; neither
    adds arithmetic of its own."""
    trials = groups.get(key) or {}
    n = planned_denominator(runs, key)
    cases = planned_ids(runs, key)

    def count(reading, outcome):
        return sum(1 for t in trials.values() if t[reading] == outcome)

    strict_acc = count("strict", "accept")
    strict_ref = count("strict", "refusal_or_error")
    strict_rej = count("strict", "reject")
    ambiguous = count("strict", "ambiguous")
    lenient_acc = count("lenient", "accept")
    lenient_ref = count("lenient", "refusal_or_error")
    pdr = sum(1 for t in trials.values() if t["pre_dispatch_refusal_runs"])
    strict_by = verdict_for(n, strict_ref, strict_acc)
    lenient_by = verdict_for(n, lenient_ref, lenient_acc)

    per_item: dict = {}
    for trial_id, case in sorted(cases.items()):
        item = per_item.setdefault(case, {"accepts": 0, "trials": 0, "refusals_or_errors": 0})
        item["trials"] += 1
        t = trials.get(trial_id)
        if t and t["strict"] == "accept":
            item["accepts"] += 1
        if t and t["strict"] == "refusal_or_error":
            item["refusals_or_errors"] += 1
    for trial_id, t in trials.items():
        if trial_id in cases:
            continue
        case = case_of(runs, trial_id) or trial_id.split("__")[0]
        item = per_item.setdefault(case, {"accepts": 0, "trials": 0, "refusals_or_errors": 0})
        item["trials"] += 1
        if t["strict"] == "accept":
            item["accepts"] += 1
        if t["strict"] == "refusal_or_error":
            item["refusals_or_errors"] += 1

    resends = []
    for trial_id in sorted(trials):
        for attempt in trials[trial_id]["attempts"][1:]:
            resends.append(
                {
                    "trial_id": trial_id,
                    "run_id": attempt["run_id"],
                    "kind": attempt["kind"],
                    "status": attempt["status"],
                    "error_class": attempt["error_class"],
                    "verdict": attempt["verdict"],
                    "first_sending": "%s:%s%s"
                    % (
                        trials[trial_id]["attempts"][0]["run_id"],
                        trials[trial_id]["attempts"][0]["status"],
                        "/" + str(trials[trial_id]["attempts"][0]["error_class"])
                        if trials[trial_id]["attempts"][0]["error_class"]
                        else "",
                    ),
                }
            )
    smoke = sorted(
        trial_id
        for trial_id in trials
        if any(r["kind"] == "smoke" for r in occurrences.get(trial_id) or [])
    )
    return {
        "n_planned": n,
        "accepts": strict_acc,
        "rejects": strict_rej,
        "refusals_or_errors": strict_ref,
        "ambiguous": ambiguous,
        "pre_dispatch_refusals": pdr,
        "e1_threshold": e1_threshold(n) if n else None,
        "e2_threshold": e2_threshold(n) if n else None,
        "eliminated": bool(strict_by),
        "eliminated_by": strict_by,
        "lenient": {
            "accepts": lenient_acc,
            "refusals_or_errors": lenient_ref,
            "eliminated": bool(lenient_by),
            "eliminated_by": lenient_by,
        },
        "per_item": per_item,
        "resends": resends,
        "smoke_draws_excluded": smoke,
        "trial_ids": sorted(trials),
    }


def recorded_summary(runs: dict, rec_list: list) -> dict:
    """What the sealed RESULTS.yaml elimination table(s) recorded for a group:
    accepts, the denominator the file divided by (n_judged where it recorded
    one, else n_planned), and the verdict.  Transparency only; never counted."""
    if not rec_list:
        return {"accepts": None, "trials": None, "eliminated": None, "eliminated_by": [], "per_case_scope": False, "files": []}
    per_case = len(rec_list) > 1
    accepts = sum((e.get("accepts") or 0) for _d, e in rec_list)
    den = None
    for _d, e in rec_list:
        if e.get("n_judged"):
            den = e.get("n_judged")
            break
    if den is None:
        den = sum((e.get("n_planned") or 0) for _d, e in rec_list)
    elims = [e.get("eliminated") for _d, e in rec_list]
    eliminated = None if all(v is None for v in elims) else any(bool(v) for v in elims)
    return {
        "accepts": accepts,
        "trials": den,
        "eliminated": eliminated,
        "eliminated_by": sorted({b for _d, e in rec_list for b in (e.get("eliminated_by") or [])}),
        "per_case_scope": per_case,
        "files": sorted({runs[d]["results_path"] for d, _e in rec_list if runs.get(d, {}).get("results_path")}),
    }


def print_section_b(runs: dict, groups: dict, recorded: dict) -> dict:
    print("=" * 100)
    print("SECTION B -- E1/E2 recomputed under the literal frozen rule")
    print("=" * 100)
    print("rule file: %s" % RULES_PATH)
    print("E1 out when refusals+errors >= ceil(0.375*n); E2 out when accepts <= floor(0.25*n)")
    print("n = planned trials for the (question, route, arm) group")
    print("pdr = trials the harness refused before anything was sent (no provider behaviour")
    print("      observed, no money moved); folded into neither reading -- reported separately")
    print()
    print("rulings applied (14 Sep 2026, %s):" % RULINGS_RECORD)
    print("  C-3  literal denominators; failures count where the frozen rule counts them")
    print("  C-6b STRICT is the counting column; LENIENT is shown only so the reader can see what the runs did")
    print("  C-6c '<route>%s' is a distinct route identity: rows judged under layout %s" % (CODE_OVERLAY_SUFFIX, COMPOSITE_LAYOUT))
    print("       (code composed the exact strings on a textless plate) are grouped apart from the bare plate")
    print("  C-6d per (route, question), as frozen E4; a per-case entry in a results file is a scope difference")
    print()
    header = (
        "%-10s %-26s %-34s | %-28s | %-30s | %-30s"
        % ("QUESTION", "ROUTE", "ARM", "RECORDED", "LITERAL STRICT", "LITERAL LENIENT")
    )
    print(header)
    print("-" * len(header))

    disagreements = {}
    for key in sorted(groups, key=lambda k: tuple(str(x) for x in k)):
        question, route, arm = key
        trials = groups[key]
        n_plan_from_plans = planned_denominator(runs, key)

        rec_list = recorded.get(key) or []
        per_case_scope = len(rec_list) > 1
        rec = rec_list[0][1] if rec_list else None
        rec_dir = rec_list[0][0] if rec_list else None
        n_recorded = (rec or {}).get("n_planned")
        if per_case_scope:
            # the run judged this route case by case; the question-level
            # denominator is the sum of its entries
            n_recorded = sum(
                e.get("n_planned") or 0 for _d, e in rec_list
            )
        n = n_recorded if isinstance(n_recorded, int) and n_recorded > 0 else n_plan_from_plans

        strict_ref = sum(1 for t in trials.values() if t["strict"] == "refusal_or_error")
        strict_acc = sum(1 for t in trials.values() if t["strict"] == "accept")
        lenient_ref = sum(1 for t in trials.values() if t["lenient"] == "refusal_or_error")
        lenient_acc = sum(1 for t in trials.values() if t["lenient"] == "accept")
        pdr = sum(1 for t in trials.values() if t["pre_dispatch_refusal_runs"])
        amb = sum(1 for t in trials.values() if t["strict"] == "ambiguous")

        strict_by = verdict_for(n, strict_ref, strict_acc)
        lenient_by = verdict_for(n, lenient_ref, lenient_acc)

        if rec:
            rec_accepts = (
                sum(e.get("accepts") or 0 for _d, e in rec_list) if per_case_scope
                else rec.get("accepts")
            )
            rec_elim = (
                any(e.get("eliminated") for _d, e in rec_list) if per_case_scope
                else (None if rec.get("eliminated") is None else bool(rec.get("eliminated")))
            )
            rec_by = sorted(
                {b for _d, e in rec_list for b in (e.get("eliminated_by") or [])}
            )
            rec_den = rec.get("n_judged") if rec.get("n_judged") else n_recorded
            rec_txt = "%s/%s %s%s" % (
                rec_accepts,
                rec_den,
                ("OUT" + str(rec_by) if rec_elim else "in") if rec_elim is not None else "per_case, no table",
                " (per case)" if per_case_scope else "",
            )
        else:
            rec_accepts = None
            rec_txt = "no RESULTS entry"
            rec_elim = None

        strict_txt = "%d/%d ref=%d %s%s" % (
            strict_acc, n, strict_ref,
            ("pdr=%d " % pdr) if pdr else ("amb=%d " % amb) if amb else "",
            "OUT" + str(strict_by) if strict_by else "in",
        )
        lenient_txt = "%d/%d ref=%d %s%s" % (
            lenient_acc, n, lenient_ref,
            ("pdr=%d " % pdr) if pdr else "",
            "OUT" + str(lenient_by) if lenient_by else "in",
        )

        conflicts = sorted(tid for tid, t in trials.items() if t.get("conflict"))
        rec_refusals = (
            sum(e.get("refusals_or_errors") or 0 for _d, e in rec_list) if rec_list else None
        )

        flag = ""
        differs = False
        if rec_elim is not None:
            if bool(strict_by) != rec_elim or bool(lenient_by) != rec_elim:
                differs = True
                flag = "  <== VERDICT DIFFERS"
            elif rec_accepts != strict_acc or rec_accepts != lenient_acc:
                differs = True
                flag = "  <== ACCEPT COUNT DIFFERS"
            elif rec.get("n_judged") and rec.get("n_judged") != n:
                differs = True
                flag = "  <== DENOMINATOR DIFFERS"
            elif rec_refusals is not None and rec_refusals != strict_ref:
                differs = True
                flag = "  <== REFUSAL COUNT DIFFERS (same verdict)"
        if conflicts and not differs:
            differs = True
            flag = "  <== CONFLICTING VERDICTS ON ONE TRIAL ID"

        print(
            "%-10s %-26s %-34s | %-28s | %-30s | %-30s%s"
            % (question, route, str(arm), rec_txt, strict_txt, lenient_txt, flag)
        )

        if differs:
            disagreements[key] = {
                "recorded": rec,
                "recorded_all": rec_list,
                "recorded_accepts": rec_accepts,
                "recorded_eliminated": rec_elim,
                "per_case_scope": per_case_scope,
                "recorded_path": (
                    runs[rec_dir]["results_path"] if rec_dir else None
                ),
                "n": n,
                "n_planned_from_plans": n_plan_from_plans,
                "pdr": pdr,
                "conflicts": conflicts,
                "recorded_refusals": rec_refusals,
                "run_ids": sorted(
                    {
                        a["run_id"]
                        for t in trials.values()
                        for a in t["attempts"]
                    }
                    | set(rec_dir and [rec_dir] or [])
                ),
                "strict": {"accepts": strict_acc, "refusals": strict_ref, "out_by": strict_by},
                "lenient": {"accepts": lenient_acc, "refusals": lenient_ref, "out_by": lenient_by},
                "trials": trials,
            }

    print()
    print("groups recomputed              : %d" % len(groups))
    print("groups where the two disagree  : %d" % len(disagreements))
    print()

    for key in sorted(disagreements, key=lambda k: tuple(str(x) for x in k)):
        info = disagreements[key]
        print("  %s | %s | %s" % key)
        print("    recorded in : %s" % info["recorded_path"])
        if info.get("per_case_scope"):
            print(
                "    NOTE        : the run judged this route case by case; the frozen rule's"
            )
            print(
                "                  E4 makes elimination per (route, question), so the two are"
            )
            print(
                "                  not the same question -- a scope difference, not a maths one"
            )
        rec = info["recorded"] or {}
        print(
            "    recorded    : accepts=%s rejects=%s n_planned=%s n_judged=%s "
            "infra_not_counted=%s refusals_or_errors=%s eliminated=%s %s"
            % (
                rec.get("accepts"),
                rec.get("rejects"),
                rec.get("n_planned"),
                rec.get("n_judged"),
                rec.get("infra_refusals_not_counted"),
                rec.get("refusals_or_errors"),
                rec.get("eliminated"),
                rec.get("eliminated_by"),
            )
        )
        print(
            "    strict      : accepts=%d refusals=%d n=%d -> %s"
            % (
                info["strict"]["accepts"],
                info["strict"]["refusals"],
                info["n"],
                info["strict"]["out_by"] or "survives",
            )
        )
        print(
            "    lenient     : accepts=%d refusals=%d n=%d -> %s"
            % (
                info["lenient"]["accepts"],
                info["lenient"]["refusals"],
                info["n"],
                info["lenient"]["out_by"] or "survives",
            )
        )
        if info.get("conflicts"):
            print(
                "    CONFLICT    : the same logical trial id carries two different Controller"
            )
            print(
                "                  verdicts in two runs: %s"
                % ", ".join(info["conflicts"])
            )
        for trial_id in sorted(info["trials"]):
            t = info["trials"][trial_id]
            if (
                t["strict"] == t["lenient"]
                and len(t["attempts"]) == 1
                and t["strict"] != "refusal_or_error"
                and not t.get("conflict")
            ):
                continue
            chain = " -> ".join(
                "%s:%s%s"
                % (
                    a["run_id"],
                    a["status"],
                    "/" + str(a["error_class"]) if a["error_class"] else "",
                )
                for a in t["attempts"]
            )
            print(
                "      %-52s strict=%-16s lenient=%-16s %s"
                % (trial_id, t["strict"], t["lenient"], chain)
            )
        print()
    return disagreements


# --------------------------------------------------------------------------
# section C -- affected routing-map cells and RR rules
# --------------------------------------------------------------------------


def print_section_c(root: str, disagreements: dict) -> None:
    print("=" * 100)
    print("SECTION C -- routing-map cells and RR rules that rest on an affected number")
    print("=" * 100)
    map_path = os.path.join(root, MAP_PATH)
    if not os.path.isfile(map_path):
        print("routing map not found: %s" % MAP_PATH)
        return
    evidence_map = read_yaml(map_path)

    affected_routes = {(q, r) for (q, r, _a) in disagreements}
    affected_keys = set(disagreements)

    print("affected (question, route, arm) groups: %d" % len(affected_keys))
    print()
    print("-- routing-map cells --")
    hits = 0
    for question in sorted((evidence_map.get("questions") or {})):
        cells = (evidence_map["questions"][question] or {}).get("cells") or {}
        for cell_name in sorted(cells):
            cell = cells[cell_name] or {}
            route = cell.get("route_key")
            arm = cell.get("arm")
            key = (question, route, arm)
            if key not in affected_keys and (question, route) not in affected_routes:
                continue
            hits += 1
            human = cell.get("human_blind_acceptance") or {}
            # since 14 Sep 2026 the map carries `eliminated` computed by this
            # tool; an older map carried the results file's `elimination` block
            eliminated = human.get("eliminated")
            if eliminated is None:
                eliminated = (human.get("elimination") or {}).get("eliminated")
            info = disagreements.get(key)
            print(
                "  %s / %s   map shows accepts=%s trials=%s eliminated=%s fallback=%s"
                % (
                    question,
                    cell_name,
                    human.get("accepts"),
                    human.get("trials"),
                    eliminated,
                    (cell.get("fallback") or {}).get("route"),
                )
            )
            if info:
                print(
                    "      literal strict  : accepts=%d of n=%d -> %s"
                    % (
                        info["strict"]["accepts"],
                        info["n"],
                        info["strict"]["out_by"] or "survives",
                    )
                )
                print(
                    "      literal lenient : accepts=%d of n=%d -> %s"
                    % (
                        info["lenient"]["accepts"],
                        info["n"],
                        info["lenient"]["out_by"] or "survives",
                    )
                )
    if not hits:
        print("  (none)")
    print()

    print("-- fallback ordering within each affected question --")
    for question in sorted({q for (q, _r) in affected_routes}):
        cells = (evidence_map["questions"][question] or {}).get("cells") or {}
        rows = []
        for cell_name in sorted(cells):
            cell = cells[cell_name] or {}
            human = cell.get("human_blind_acceptance") or {}
            accepts = human.get("accepts")
            trials = human.get("trials")
            key = (question, cell.get("route_key"), cell.get("arm"))
            info = disagreements.get(key)
            rate_map = (accepts / trials) if (accepts is not None and trials) else None
            rows.append(
                (
                    cell_name,
                    rate_map,
                    (info["strict"]["accepts"] / info["n"]) if info and info["n"] else rate_map,
                    (info["lenient"]["accepts"] / info["n"]) if info and info["n"] else rate_map,
                )
            )
        print("  %s" % question)
        for label, idx in (("as published", 1), ("literal strict", 2), ("literal lenient", 3)):
            order = sorted(
                rows,
                key=lambda r: (-(r[idx] if r[idx] is not None else -1), r[0]),
            )
            print(
                "    %-16s %s"
                % (
                    label,
                    " > ".join(
                        "%s(%s)"
                        % (r[0], "n/a" if r[idx] is None else ("%.3f" % r[idx]))
                        for r in order
                    ),
                )
            )
        print()

    print("-- routing rules (RR) --")
    named = []
    cited_only = []
    for rule in evidence_map.get("routing_rules") or []:
        blob = " ".join(
            str(rule.get(field) or "")
            for field in ("scope", "rule", "evidence", "caveat", "source")
        )
        direct = []
        for key in sorted(affected_keys, key=lambda k: tuple(str(x) for x in k)):
            question, route, _arm = key
            if not route or not has_token(blob, route):
                continue
            runs_for_key = disagreements[key].get("run_ids") or []
            if has_token(blob.lower(), question.lower()) or any(
                has_token(blob, r) for r in runs_for_key
            ):
                direct.append(key)
        if direct:
            named.append((rule, direct))
            continue
        cites = sorted(
            {
                run_id
                for key in affected_keys
                for run_id in (disagreements[key].get("run_ids") or [])
                if has_token(blob, run_id)
            }
        )
        if cites:
            cited_only.append((rule, cites))

    for rule, keys in named:
        print("  %s (%s)" % (rule.get("id"), rule.get("scope")))
        print(
            "    names an affected route: %s"
            % ", ".join("%s/%s" % (k[0], k[1]) for k in keys)
        )
        for key in keys:
            info = disagreements[key]
            print(
                "      %s %s: wording rests on %s/%s ; strict %s/%s -> %s ; lenient %s/%s -> %s"
                % (
                    key[1],
                    key[2],
                    info.get("recorded_accepts"),
                    (info["recorded"] or {}).get("n_judged") or info["n"],
                    info["strict"]["accepts"],
                    info["n"],
                    info["strict"]["out_by"] or "survives",
                    info["lenient"]["accepts"],
                    info["n"],
                    info["lenient"]["out_by"] or "survives",
                )
            )
        print()

    print("  -- rules that cite an affected run but name no affected route --")
    if not cited_only:
        print("  (none)")
    for rule, cites in cited_only:
        print(
            "  %s (%s): cites %s"
            % (rule.get("id"), rule.get("scope"), ", ".join(cites))
        )
        print("      evidence line: %s" % str(rule.get("evidence"))[:150])
    print()


# --------------------------------------------------------------------------


def main() -> int:
    root = repo_root()
    os.chdir(root)
    runs = load_runs(root)
    occurrences = build_occurrences(runs)
    verdicts = judged_verdicts(runs)

    print("recompute_elimination.py -- read-only recompute of EVAL-040 elimination")
    print("repository root: %s" % root)
    print("runs read      : %d" % len(runs))
    print()

    print_section_a(occurrences, verdicts)
    groups = build_groups(runs, occurrences, verdicts)
    recorded = recorded_entries(runs, list(groups))
    disagreements = print_section_b(runs, groups, recorded)
    print_section_c(root, disagreements)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
