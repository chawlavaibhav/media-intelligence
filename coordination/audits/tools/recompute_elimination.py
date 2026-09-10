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


def load_runs(root: str) -> dict:
    """One record per run directory: plan header, planned trials, dispatches,
    sealed artifacts, ledger entry types, and the committed RESULTS.yaml."""
    runs = {}
    base = os.path.join(root, RUNS_DIR)
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
            "results_path": os.path.join(RUNS_DIR, run_dir, "RESULTS.yaml")
            if results is not None
            else None,
            "plan_path": os.path.join(RUNS_DIR, run_dir, "PLAN.yaml"),
        }
    return runs


# --------------------------------------------------------------------------
# section A -- duplicated logical trial ids
# --------------------------------------------------------------------------


def occurrence_class(run: dict, trial_id: str, earlier_core_runs: list) -> str:
    if run["mode"] == "smoke":
        return "smoke"
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
            if kind != "smoke":
                seen_core.append(run_dir)
            rows.append(
                {
                    "run_id": run_dir,
                    "at": disp["at"],
                    "kind": kind,
                    "status": disp["status"],
                    "error_class": disp["error_class"],
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
                "    %-24s %-17s status=%-8s err=%-22s recovered=%-5s sealed=%-5s ledger=%-19s spend_usd=%.2f  %s"
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


def group_of(runs: dict, trial_id: str):
    """(question, route_key, arm) for a logical trial id, from the plans."""
    for run_dir in sorted(runs):
        meta = runs[run_dir]["planned"].get(trial_id)
        if meta:
            return (
                question_of(meta["case_id"]),
                meta["route_key"],
                meta["arm"],
            )
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
    return out


def build_groups(runs: dict, occurrences: dict, verdicts: dict) -> dict:
    """(question, route, arm) -> per-logical-trial outcome under both readings."""
    groups = defaultdict(dict)
    for trial_id, rows in occurrences.items():
        non_smoke = [r for r in rows if r["kind"] != "smoke"]
        if not non_smoke:
            continue
        key = group_of(runs, trial_id)
        if key is None:
            continue

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

    # trial ids the harness refused before anything was sent and that were never
    # dispatched at all still belong to their group
    for run_dir in sorted(runs):
        run = runs[run_dir]
        for trial_id in sorted(run["pre_dispatch_refusals"]):
            key = group_of(runs, trial_id)
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


def planned_denominator(runs: dict, key) -> int:
    """Distinct logical trial ids planned for the group in every non-smoke run."""
    ids = set()
    for run_dir in sorted(runs):
        run = runs[run_dir]
        if run["mode"] == "smoke":
            continue
        for trial_id, meta in run["planned"].items():
            if (
                question_of(meta["case_id"]),
                meta["route_key"],
                meta["arm"],
            ) == key:
                ids.add(trial_id)
    return len(ids)


def verdict_for(n: int, refusals: int, accepts: int):
    out_by = []
    if n > 0 and refusals >= e1_threshold(n):
        out_by.append("E1")
    if n > 0 and accepts <= e2_threshold(n):
        out_by.append("E2")
    return out_by


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
                else bool(rec.get("eliminated"))
            )
            rec_by = sorted(
                {b for _d, e in rec_list for b in (e.get("eliminated_by") or [])}
            )
            rec_den = rec.get("n_judged") if rec.get("n_judged") else n_recorded
            rec_txt = "%s/%s %s%s" % (
                rec_accepts,
                rec_den,
                "OUT" + str(rec_by) if rec_elim else "in",
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
            elim = human.get("elimination") or {}
            info = disagreements.get(key)
            print(
                "  %s / %s   map shows accepts=%s trials=%s eliminated=%s fallback=%s"
                % (
                    question,
                    cell_name,
                    human.get("accepts"),
                    human.get("trials"),
                    elim.get("eliminated"),
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
