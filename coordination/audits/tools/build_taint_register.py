#!/usr/bin/env python3
"""build_taint_register.py -- generate eval/capability-map/TAINT-REGISTER-v1.yaml.

Read-only over all evidence.  Standard library plus PyYAML.  Deterministic:
running it twice produces a byte-identical file, because nothing in the output
depends on the wall clock, on dictionary iteration order, or on the order in
which the filesystem returns names.

What it does
------------
For every one of the cells in `eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml`
it records, in machine-readable form:

  * which named problems (from a closed vocabulary) touch that cell,
  * how many of its trials are settled, excluded, or merely descriptive,
  * what the sealed results files recorded versus what the literal frozen
    elimination rule produces (both the strict and the lenient reading),
  * whether a production router may rest a route decision on it today,
  * and which Controller ruling, if any, is blocking it.

It decides nothing.  Where a question is open, the register says so and names
the open question.

Safety
------
The register is only meaningful against the exact map it was built from, so the
generator refuses to run when the map's sha256 is not the one recorded below.
That way the register can never silently drift from the map.

Usage
-----
    python3 coordination/audits/tools/build_taint_register.py [--check]

`--check` regenerates into memory and reports whether the committed register
would change, without writing anything.

No model call, no network call, no cloud command.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import importlib.util
import os
import sys

import yaml

# --------------------------------------------------------------------------
# the exact map this generator was built against
# --------------------------------------------------------------------------

MAP_PATH = os.path.join("eval", "capability-map", "ROUTING-EVIDENCE-MAP-v0.yaml")
MAP_SHA256 = "50f0d355440027f7cee8a9b146577f0850ab55f1dd0f6d6ddff0c531f8028e6f"
MAP_CELL_COUNT = 61

OUT_PATH = os.path.join("eval", "capability-map", "TAINT-REGISTER-v1.yaml")

RECOMPUTE_PATH = os.path.join(
    "coordination", "audits", "tools", "recompute_elimination.py"
)
RULES_PATH = os.path.join(
    "eval", "empirical-planning", "STAGE-A-FREEZE-2026-09", "ELIMINATION-RULES.md"
)
RUNS_DIR = os.path.join("eval", "experiments", "EVAL-040", "runs")

RECOMPUTE_AUDIT = "coordination/audits/AUDIT-2026-09-10-EVIDENCE-RECOMPUTE.md"
REPORT_A = "coordination/audits/AUDIT-2026-09-10-REPORT-A.md"
REPORT_B = "coordination/audits/AUDIT-2026-09-10-REPORT-B.md"
DECISIONS = "coordination/audits/AUDIT-2026-09-10-CONTROLLER-DECISIONS.md"

# Report A, "Missing scientific/product proof" item 4 ("More than two draws for
# decisions that materially control customer routing") and Report B part 4 item
# 1 plus its P1 ("the map's rules rest on four draws per cell instead of two").
# Four settled draws is therefore the floor a cell must clear before its number
# is treated as more than directional.  This is a threshold quoted from the two
# audits, not a judgement made here.
MIN_SETTLED_DRAWS = 4

# One plain-English gloss per open question, so a non-engineer reading a cell's
# `reason` is told what is actually undecided.  These are descriptions of the
# open items, never answers to them.
RULING_GLOSS = {
    "C-3": (
        "whether a provider balance lock or a harness fault counts inside the "
        "denominator"
    ),
    "C-4": (
        "whether a cell touched by a duplicated identity, a smoke draw sharing its "
        "name, or an excluded infrastructure failure counts as product learning only"
    ),
    "C-6b": "how a draw that failed once and was sent again counts",
    "C-6c": (
        "how the two cells that share one route key and one arm are told apart, and "
        "what the four contested draws actually established"
    ),
    "OPEN-1": (
        "whether a route is eliminated per question, as the frozen rule says, or per "
        "case, as two runs applied it"
    ),
}

PROBLEM_VOCABULARY = [
    "duplicate_dispatched_identity",
    "smoke_shared_identity",
    "redo_undeclared",
    "infra_refusal_excluded",
    "denominator_convention_differs",
    "contradictory_verdicts",
    "judged_stricter_than_contract",
]

STATUS_VOCABULARY = [
    "clean_observed",
    "directional_only",
    "awaiting_controller_ruling",
    "method_tainted",
    "insufficient",
]


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------


def repo_root() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
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


def sha256_of(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_recompute(root: str):
    """Import the audit's recompute tool as a library.  It is the single source
    of every number here; this generator adds no arithmetic of its own."""
    path = os.path.join(root, RECOMPUTE_PATH)
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("recompute_elimination", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def guard_map_version(root: str) -> None:
    path = os.path.join(root, MAP_PATH)
    if not os.path.isfile(path):
        sys.stderr.write("routing evidence map not found at %s\n" % MAP_PATH)
        raise SystemExit(2)
    actual = sha256_of(path)
    if actual != MAP_SHA256:
        sys.stderr.write(
            "REFUSING TO RUN.\n"
            "  %s has changed since this generator was written.\n"
            "    expected sha256 : %s\n"
            "    actual   sha256 : %s\n"
            "  The taint register must never drift from the map it describes.\n"
            "  Re-read the map, update MAP_SHA256 in this file deliberately,\n"
            "  and re-check every cell before regenerating.\n"
            % (MAP_PATH, MAP_SHA256, actual)
        )
        raise SystemExit(3)


# --------------------------------------------------------------------------
# the plain-English header written into the register itself
# --------------------------------------------------------------------------

HEADER_COMMENT = """\
# =============================================================================
# TAINT-REGISTER-v1 -- what each number in the routing map is worth
# =============================================================================
#
# READ THIS FIRST. It is written for a reader who is not an engineer.
#
# The routing map next door lists, for every job the project can do, which
# model routes were tried and how many of their outputs were accepted. This
# file sits beside it and answers a different question about each of those
# entries: HOW MUCH WEIGHT CAN THIS NUMBER TAKE?
#
# An audit on 10 September 2026 found that some numbers in the map were
# produced under a counting rule that was not the one written down before the
# money was spent, that some draws were sent twice under the same name, and
# that in one place the same four draws carry two different answers. None of
# that means the work was wasted. It means a machine must not quietly use those
# numbers to choose a route for a paying customer as if they were settled.
#
# This file exists so that a production router can be told, for every single
# entry: use this, ask a human first, or do not use this at all.
#
# -----------------------------------------------------------------------------
# THE FIVE STATUSES, IN PLAIN ENGLISH
# -----------------------------------------------------------------------------
#
# clean_observed
#   WHAT IT MEANS: the number reproduces exactly when the frozen rule is applied
#     literally to the sealed files, and none of the known problems touch it.
#     There are at least four settled draws behind it.
#   WHAT IT DOES NOT MEAN: it does not mean the route is good, cheap, or the
#     best choice; it does not mean the sample is large enough to be reliable in
#     a statistical sense; and it does NOT mean the route is cleared for launch
#     traffic. Four to eight draws judged by one person over two evenings is
#     honest evidence, not proof.
#
# directional_only
#   WHAT IT MEANS: the number reproduces and nothing is wrong with it, but it
#     rests on fewer than four settled draws. It is a signal, not a measurement.
#   WHAT IT DOES NOT MEAN: it does not mean the number is wrong. It means a
#     route that scored 2 out of 2 may simply be a coin that landed twice, so
#     the number should not decide a route on its own.
#
# awaiting_controller_ruling
#   WHAT IT MEANS: a specific question is open, and the answer to it changes
#     this entry's number, or whether the route is kept or dropped, or whether
#     the entry may be counted at all. The open question is named in
#     `blocking_ruling` (an item on the Controller's decision sheet) or in
#     `blocking_open_question` (a question the audits raised for which the sheet
#     carries no numbered item yet).
#   WHAT IT DOES NOT MEAN: it does not mean the evidence is worthless or that
#     the route is bad. It means nobody may pretend the question has been
#     answered. This file never guesses the answer.
#
# method_tainted
#   WHAT IT MEANS: a known problem affects the number and no ruling can repair
#     it -- the only fix is to run the draws again, cleanly.
#   WHAT IT DOES NOT MEAN: it does not mean anyone acted in bad faith, and it
#     does not mean what was learned from those outputs is untrue. It means the
#     number cannot be defended.
#
# insufficient
#   WHAT IT MEANS: there is not enough evidence here to say anything at all.
#   WHAT IT DOES NOT MEAN: it does not mean the route failed.
#
# -----------------------------------------------------------------------------
# WHAT THIS FILE DELIBERATELY DOES NOT CONTAIN
# -----------------------------------------------------------------------------
#
# There is no launch-eligibility status anywhere in this file, and there never
# will be. Whether an entry may carry real customer traffic is a Controller
# ruling plus a runtime decision. This file only reports the state of the
# evidence. The runtime's own policy profile decides which of these statuses it
# is willing to route on automatically -- for example, a cautious profile might
# auto-route only on `clean_observed` and send everything else to a person.
#
# `production_use_allowed` is this file's reading of the evidence, not a
# permission:
#     true         the evidence behind this entry is settled and reproduces
#     manual_only  a person must look before this entry decides anything
#     false        do not rest a route decision on this entry
#
# `replacement_needed: true` means no ruling can finish this entry -- it needs
# fresh draws before its number can carry a production decision.
#
# Nothing in this file was decided by its author. Every open question is named
# and left open.
#
# Generated by coordination/audits/tools/build_taint_register.py -- regenerate,
# do not hand-edit. The generator refuses to run if the routing map has changed.
# =============================================================================
"""


# --------------------------------------------------------------------------
# classification
# --------------------------------------------------------------------------


def cell_problems(ctx, key, trials, occurrences, map_cell, rec_list, literal, collision):
    """The named problems touching one cell, drawn only from the closed
    vocabulary.  Every branch names the sealed evidence it rests on."""
    problems = set()
    evidence = []

    # -- duplicated dispatched identities and undeclared re-dos -------------
    for trial_id in sorted(trials):
        rows = occurrences.get(trial_id) or []
        non_smoke = [r for r in rows if r["kind"] != "smoke"]
        smoke = [r for r in rows if r["kind"] == "smoke"]
        if len(non_smoke) > 1:
            problems.add("duplicate_dispatched_identity")
            evidence.append(
                "%s was dispatched in %s"
                % (trial_id, " then ".join(r["run_id"] for r in non_smoke))
            )
        if smoke:
            problems.add("smoke_shared_identity")
            evidence.append(
                "%s was also dispatched, paid for and never judged in %s"
                % (trial_id, ", ".join(r["run_id"] for r in smoke))
            )
        if any(r["kind"] == "redo (undeclared)" for r in non_smoke):
            problems.add("redo_undeclared")
            evidence.append(
                "%s was re-sent in %s, whose PLAN.yaml records redo_of: null"
                % (
                    trial_id,
                    ", ".join(
                        r["run_id"]
                        for r in non_smoke
                        if r["kind"] == "redo (undeclared)"
                    ),
                )
            )

    # -- contradictory verdicts on one identity -----------------------------
    for trial_id in sorted(trials):
        if trials[trial_id].get("conflict"):
            problems.add("contradictory_verdicts")
            evidence.append(
                "%s carries two different Controller verdicts in two runs" % trial_id
            )
    if collision:
        problems.add("contradictory_verdicts")
        evidence.append(
            "this cell shares route_key %r and arm %r with map cell %r, and the two "
            "carry different acceptance numbers" % (key[1], key[2], collision)
        )

    # -- infrastructure refusals excluded from the count --------------------
    rec_infra = sum((e.get("infra_refusals_not_counted") or 0) for _d, e in rec_list)
    rec_refusals = sum((e.get("refusals_or_errors") or 0) for _d, e in rec_list)
    if rec_list and (rec_infra > 0 or literal["strict_refusals"] > rec_refusals):
        problems.add("infra_refusal_excluded")
        evidence.append(
            "the sealed results file records refusals_or_errors=%d and "
            "infra_refusals_not_counted=%d where the literal rule counts %d "
            "refusal(s) or error(s)"
            % (rec_refusals, rec_infra, literal["strict_refusals"])
        )

    # -- denominator conventions -------------------------------------------
    map_trials = ((map_cell.get("human_blind_acceptance") or {}).get("trials"))
    rec_judged = [e.get("n_judged") for _d, e in rec_list if e.get("n_judged")]
    rec_planned = sum((e.get("n_planned") or 0) for _d, e in rec_list)
    if isinstance(map_trials, int) and map_trials != literal["n_planned"]:
        problems.add("denominator_convention_differs")
        evidence.append(
            "the routing map divides by %d where the frozen rule's planned "
            "denominator is %d" % (map_trials, literal["n_planned"])
        )
    if any(n != literal["n_planned"] for n in rec_judged):
        problems.add("denominator_convention_differs")
        evidence.append(
            "the sealed results file divides by n_judged=%s where the frozen "
            "rule's planned denominator is %d"
            % (", ".join(str(n) for n in rec_judged), literal["n_planned"])
        )
    if rec_list and rec_planned and rec_planned != literal["n_planned"]:
        problems.add("denominator_convention_differs")
        evidence.append(
            "the sealed results file's elimination entries plan %d trial(s) "
            "where the plans hold %d" % (rec_planned, literal["n_planned"])
        )

    # -- elimination applied at a stricter scope than the frozen contract ---
    if len(rec_list) > 1:
        problems.add("judged_stricter_than_contract")
        evidence.append(
            "the run eliminated this route case by case (%d separate entries) "
            "where rule E4 makes elimination per (route, question)" % len(rec_list)
        )

    return sorted(problems), sorted(set(evidence))


def classify_trials(trials, occurrences, rec_list):
    """Split a cell's logical trials into settled, excluded and descriptive.

    settled     -- one dispatch, one settled outcome, counted under the literal
                   rule (an accept, a reject, or a refusal that was counted)
    excluded    -- present in the sealed record but kept out of the recorded
                   number (an infrastructure refusal the run dropped, or a draw
                   the harness refused before anything was sent)
    descriptive -- the outcome depends on an unruled convention: the identity
                   was sent more than once, or it carries two verdicts
    """
    rec_infra = sum((e.get("infra_refusals_not_counted") or 0) for _d, e in rec_list)
    settled, excluded, descriptive = [], [], []
    for trial_id in sorted(trials):
        trial = trials[trial_id]
        rows = occurrences.get(trial_id) or []
        non_smoke = [r for r in rows if r["kind"] != "smoke"]
        if trial["strict"] == "pre_dispatch_refusal":
            excluded.append((trial_id, "harness refused before anything was sent"))
        elif len(non_smoke) > 1 or trial.get("conflict") or trial["strict"] != trial["lenient"]:
            descriptive.append(
                (
                    trial_id,
                    "sent more than once or judged twice; the count depends on an "
                    "unruled convention",
                )
            )
        elif trial["strict"] == "refusal_or_error" and rec_infra > 0:
            excluded.append(
                (trial_id, "a refusal or error the run kept out of its denominator")
            )
        else:
            settled.append((trial_id, "one dispatch, one settled outcome"))
    return settled, excluded, descriptive


def decide_status(problems, settled_n, has_trials):
    """The status, the blocking ruling and the reading of production use.

    NOTHING here resolves an open question.  The mapping from a named problem to
    the Controller item that governs it is taken from the decision sheet's own
    wording.
    """
    blocking_ruling = None
    blocking_open_question = None

    if not has_trials:
        return "insufficient", None, None

    if problems:
        if "contradictory_verdicts" in problems:
            blocking_ruling = "C-6c"
        elif "duplicate_dispatched_identity" in problems or "redo_undeclared" in problems:
            blocking_ruling = "C-6b"
        elif (
            "infra_refusal_excluded" in problems
            or "denominator_convention_differs" in problems
        ):
            blocking_ruling = "C-3"
        elif "judged_stricter_than_contract" in problems:
            # The decision sheet carries no numbered item for elimination SCOPE.
            blocking_open_question = "OPEN-1"
        elif "smoke_shared_identity" in problems:
            blocking_ruling = "C-4"

        if blocking_ruling is None and blocking_open_question is None:
            # A named problem with no ruling that could repair it: only fresh
            # draws can settle the number.
            return "method_tainted", None, None
        return "awaiting_controller_ruling", blocking_ruling, blocking_open_question

    if settled_n < MIN_SETTLED_DRAWS:
        return "directional_only", None, None
    return "clean_observed", None, None


# --------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------


def build(root: str) -> str:
    rc = load_recompute(root)

    cwd = os.getcwd()
    os.chdir(root)
    try:
        runs = rc.load_runs(root)
        occurrences = rc.build_occurrences(runs)
        verdicts = rc.judged_verdicts(runs)
        groups = rc.build_groups(runs, occurrences, verdicts)
        recorded = rc.recorded_entries(runs, list(groups.keys()))
        with open(MAP_PATH, "r", encoding="utf-8") as handle:
            cmap = yaml.safe_load(handle)
        map_sha = sha256_of(MAP_PATH)
        recompute_sha = sha256_of(RECOMPUTE_PATH)
        rules_sha = sha256_of(RULES_PATH)
    finally:
        os.chdir(cwd)

    # (route_key, arm) pairs that more than one cell in the same question uses
    collisions = {}
    for question in sorted(cmap["questions"]):
        by_pair = collections.defaultdict(list)
        for cell_name, cell in sorted(cmap["questions"][question]["cells"].items()):
            by_pair[(cell.get("route_key"), cell.get("arm"))].append(cell_name)
        for pair, names in by_pair.items():
            if len(names) > 1:
                for name in names:
                    collisions[(question, name)] = sorted(n for n in names if n != name)

    cells_out = []
    for question in sorted(cmap["questions"]):
        for cell_name in sorted(cmap["questions"][question]["cells"]):
            cell = cmap["questions"][question]["cells"][cell_name]
            route_key = cell.get("route_key")
            arm = cell.get("arm")
            key = (question, route_key, arm)
            trials = groups.get(key) or {}
            rec_list = recorded.get(key) or []
            hba = cell.get("human_blind_acceptance") or {}
            elim = hba.get("elimination") or {}

            n_planned = rc.planned_denominator(runs, key)
            strict_acc = sum(1 for t in trials.values() if t["strict"] == "accept")
            strict_ref = sum(
                1 for t in trials.values() if t["strict"] == "refusal_or_error"
            )
            lenient_acc = sum(1 for t in trials.values() if t["lenient"] == "accept")
            lenient_ref = sum(
                1 for t in trials.values() if t["lenient"] == "refusal_or_error"
            )
            strict_by = rc.verdict_for(n_planned, strict_ref, strict_acc)
            lenient_by = rc.verdict_for(n_planned, lenient_ref, lenient_acc)
            literal = {
                "n_planned": n_planned,
                "strict_accepts": strict_acc,
                "strict_refusals": strict_ref,
                "lenient_accepts": lenient_acc,
                "lenient_refusals": lenient_ref,
            }

            collision_names = collisions.get((question, cell_name))
            collision = collision_names[0] if collision_names else None

            problems, problem_evidence = cell_problems(
                None, key, trials, occurrences, cell, rec_list, literal, collision
            )
            settled, excluded, descriptive = classify_trials(
                trials, occurrences, rec_list
            )
            # draws the harness stopped before anything was sent: declared, no
            # provider behaviour observed, no money moved
            pre_dispatch_n = sum(
                1 for t in trials.values() if t.get("pre_dispatch_refusal_runs")
            )

            # What the sealed results file says.
            if rec_list:
                res_accepts = sum((e.get("accepts") or 0) for _d, e in rec_list)
                res_elim = any(e.get("eliminated") for _d, e in rec_list)
                res_by = sorted(
                    {b for _d, e in rec_list for b in (e.get("eliminated_by") or [])}
                )
                res_den = None
                for _d, entry in rec_list:
                    if entry.get("n_judged"):
                        res_den = entry.get("n_judged")
                        break
                if res_den is None:
                    res_den = sum((e.get("n_planned") or 0) for _d, e in rec_list)
                results_verdict = (
                    "eliminated:%s" % "+".join(res_by) if res_elim else "kept"
                )
                results_number = "%d/%d" % (res_accepts, res_den)
            else:
                res_accepts, res_elim, res_den = None, None, None
                results_verdict = "not_recorded"
                results_number = None

            # What the routing map itself carries -- this is what a router would
            # read, so it is the "recorded" side of the comparison.  Where two map
            # cells share one (route_key, arm) the two differ, and that difference
            # is the collision the register exists to make visible.
            rec_accepts = hba.get("accepts")
            rec_den = hba.get("trials")
            if elim:
                rec_elim = bool(elim.get("eliminated"))
                rec_by = sorted(elim.get("eliminated_by") or [])
                recorded_verdict = (
                    "eliminated:%s" % "+".join(rec_by) if rec_elim else "kept"
                )
            else:
                rec_elim = None
                recorded_verdict = "not_recorded"
            recorded_number = (
                "%s/%s" % (rec_accepts, rec_den)
                if rec_accepts is not None and rec_den is not None
                else None
            )

            literal_verdict = {
                "strict": "eliminated:%s" % "+".join(strict_by) if strict_by else "kept",
                "lenient": "eliminated:%s" % "+".join(lenient_by)
                if lenient_by
                else "kept",
                "strict_number": "%d/%d" % (strict_acc, n_planned),
                "lenient_number": "%d/%d" % (lenient_acc, n_planned),
                "readings_agree": bool(strict_by) == bool(lenient_by)
                and strict_acc == lenient_acc,
            }

            if rec_elim is None:
                verdict_changes = None
            else:
                verdict_changes = (
                    bool(strict_by) != rec_elim or bool(lenient_by) != rec_elim
                )
            number_changes = None
            if rec_accepts is not None:
                number_changes = (
                    rec_accepts != strict_acc
                    or rec_accepts != lenient_acc
                    or (rec_den is not None and rec_den != n_planned)
                )

            eliminated_everywhere = bool(strict_by) and bool(lenient_by) and (
                rec_elim in (True, None)
            )
            eliminated_anywhere = bool(strict_by) or bool(lenient_by) or bool(rec_elim)

            status, blocking_ruling, blocking_open = decide_status(
                problems, len(settled), bool(trials)
            )

            if status == "clean_observed":
                production = False if eliminated_anywhere else True
            elif status == "directional_only":
                production = False if eliminated_anywhere else "manual_only"
            elif status == "awaiting_controller_ruling":
                production = "manual_only"
            else:
                production = False

            replacement_needed = False
            if status in ("method_tainted", "insufficient"):
                replacement_needed = True
            elif "contradictory_verdicts" in problems:
                replacement_needed = True
            elif len(settled) < MIN_SETTLED_DRAWS and not eliminated_everywhere:
                replacement_needed = True

            # one plain sentence
            if status == "clean_observed" and production is True:
                reason = (
                    "The literal frozen rule reproduces the recorded %s exactly, no "
                    "named problem touches it, and %d settled draws sit behind it."
                    % (recorded_number or literal_verdict["strict_number"], len(settled))
                )
            elif status == "clean_observed":
                reason = (
                    "The number reproduces cleanly on %d settled draws, but the route "
                    "is eliminated, so no traffic may rest on it." % len(settled)
                )
            elif status == "directional_only" and production == "manual_only":
                reason = (
                    "Nothing is wrong with this number, but %d settled draw(s) is "
                    "below the four the audits ask for before a number decides a "
                    "customer route." % len(settled)
                )
            elif status == "directional_only":
                reason = (
                    "The number is clean on %d settled draw(s) and the route is "
                    "eliminated either way." % len(settled)
                )
            elif status == "awaiting_controller_ruling":
                named = blocking_ruling or blocking_open
                if verdict_changes:
                    effect = "flips this route between kept and dropped"
                elif number_changes:
                    effect = "changes this cell's number"
                else:
                    effect = "decides whether this cell may be counted at all"
                reason = (
                    "Open question %s -- %s -- %s, so a person must look before this "
                    "cell decides anything."
                    % (named, RULING_GLOSS.get(named, "see the decision sheet"), effect)
                )
            elif status == "method_tainted":
                reason = (
                    "%s affects the number and no ruling can repair it; only fresh "
                    "draws can." % ", ".join(problems)
                )
            else:
                reason = "There is no judged evidence behind this cell."

            # sealed sources for every count above
            run_ids, plans, results_files, run_logs = set(), set(), set(), set()
            for trial_id in trials:
                for row in occurrences.get(trial_id) or []:
                    run_ids.add(row["run_id"])
            for run_id in sorted(run_ids):
                plans.add(os.path.join(RUNS_DIR, run_id, "PLAN.yaml"))
                run_logs.add(os.path.join(RUNS_DIR, run_id, "RUN-LOG.jsonl"))
                if runs[run_id].get("results_path"):
                    results_files.add(runs[run_id]["results_path"])
            for run_dir, _entry in rec_list:
                if runs[run_dir].get("results_path"):
                    results_files.add(runs[run_dir]["results_path"])

            # F-7: the image rounds committed to a salted fingerprint of the blind
            # mapping; the video and audio rounds did not.  Read straight from the
            # sealed results files, never asserted here.
            commitments = set()
            for run_id in sorted(run_ids):
                results = runs[run_id].get("results")
                if results and "commitment_verified" in results:
                    commitments.add(bool(results.get("commitment_verified")))
            if commitments == {True}:
                blinding = True
            elif commitments == {False}:
                blinding = False
            elif commitments:
                blinding = "mixed"
            else:
                blinding = None

            trial_rows = []
            for bucket, items in (
                ("clean", settled),
                ("excluded", excluded),
                ("descriptive", descriptive),
            ):
                for trial_id, why in items:
                    attempts = []
                    for row in occurrences.get(trial_id) or []:
                        judged = verdicts.get((row["run_id"], trial_id))
                        attempts.append(
                            {
                                "run_id": row["run_id"],
                                "kind": row["kind"],
                                "status": row["status"],
                                "error_class": row["error_class"],
                                "verdict": (judged or {}).get("verdict"),
                                "in_results_file": judged is not None,
                            }
                        )
                    trial_rows.append(
                        {
                            "trial_id": trial_id,
                            "counted_as": bucket,
                            "strict": trials[trial_id]["strict"],
                            "lenient": trials[trial_id]["lenient"],
                            "why": why,
                            "attempts": attempts,
                        }
                    )
            trial_rows.sort(key=lambda r: (r["counted_as"], r["trial_id"]))

            if not problems and (verdict_changes or number_changes):
                raise SystemExit(
                    "internal inconsistency: %s/%s has no named problem yet its "
                    "recorded number or verdict does not reproduce; the problem "
                    "vocabulary does not cover what happened here."
                    % (question, cell_name)
                )

            entry = collections.OrderedDict()
            entry["cell_key"] = "%s/%s" % (question, cell_name)
            entry["question"] = question
            entry["route_key"] = route_key
            entry["arm"] = arm
            entry["map_cell_name"] = cell_name
            entry["run_ids"] = sorted(run_ids)
            entry["problem"] = problems
            entry["problem_evidence"] = problem_evidence
            entry["clean_trials"] = len(settled)
            entry["excluded_trials"] = len(excluded)
            entry["descriptive_trials"] = len(descriptive)
            entry["pre_dispatch_refusal_trials"] = pre_dispatch_n
            entry["planned_trials_frozen_rule"] = n_planned
            entry["map_reported_trials"] = hba.get("trials")
            entry["map_reported_accepts"] = hba.get("accepts")
            entry["recorded_verdict"] = recorded_verdict
            entry["recorded_number"] = recorded_number
            entry["recorded_in_results_file"] = collections.OrderedDict(
                [
                    ("verdict", results_verdict),
                    ("number", results_number),
                    ("files", sorted({runs[d]["results_path"] for d, _e in rec_list})),
                ]
            )
            entry["literal_verdict"] = literal_verdict
            entry["verdict_changes"] = verdict_changes
            entry["number_changes"] = number_changes
            entry["evidence_status"] = status
            entry["production_use_allowed"] = production
            entry["blocking_ruling"] = blocking_ruling
            entry["blocking_open_question"] = blocking_open
            entry["replacement_needed"] = replacement_needed
            entry["reason"] = reason
            if collision_names:
                entry["shares_route_key_and_arm_with"] = [
                    "%s/%s" % (question, n) for n in collision_names
                ]
            entry["blinding_commitment_verified"] = blinding
            entry["sources"] = collections.OrderedDict(
                [
                    ("plans", sorted(plans)),
                    ("results", sorted(results_files)),
                    ("run_logs", sorted(run_logs)),
                    ("elimination_rules", RULES_PATH),
                ]
            )
            entry["trials"] = trial_rows
            cells_out.append(entry)

    cells_out.sort(key=lambda c: c["cell_key"])

    # ---------------------------------------------------------------- summary
    by_status = collections.Counter(c["evidence_status"] for c in cells_out)
    by_production = collections.Counter(str(c["production_use_allowed"]) for c in cells_out)
    by_ruling = collections.Counter(
        c["blocking_ruling"] for c in cells_out if c["blocking_ruling"]
    )
    by_open = collections.Counter(
        c["blocking_open_question"] for c in cells_out if c["blocking_open_question"]
    )
    by_problem = collections.Counter(p for c in cells_out for p in c["problem"])

    doc = collections.OrderedDict()
    doc["schema"] = "TAINT-REGISTER-v1"
    doc["status"] = (
        "evidence-status register for ROUTING-EVIDENCE-MAP-v0; this file reports "
        "the state of the evidence and decides nothing"
    )
    doc["decides_nothing"] = True
    doc["no_launch_eligibility_here"] = (
        "This file contains no launch-eligibility judgement of any kind. Whether a "
        "cell may carry customer traffic is a Controller ruling plus a runtime "
        "decision. The runtime's policy profile decides which evidence_status "
        "values it will auto-route on."
    )
    doc["generated_by"] = "coordination/audits/tools/build_taint_register.py"
    doc["sources"] = collections.OrderedDict(
        [
            ("routing_evidence_map", MAP_PATH),
            ("routing_evidence_map_sha256", map_sha),
            ("routing_evidence_map_generated_utc", cmap.get("generated_utc")),
            ("routing_evidence_map_cell_count", cmap.get("cell_count")),
            ("recompute_tool", RECOMPUTE_PATH),
            ("recompute_tool_sha256", recompute_sha),
            ("elimination_rules", RULES_PATH),
            ("elimination_rules_sha256", rules_sha),
            ("recompute_audit", RECOMPUTE_AUDIT),
            ("audit_report_a", REPORT_A),
            ("audit_report_b", REPORT_B),
            ("controller_decisions", DECISIONS),
        ]
    )
    doc["cell_count"] = len(cells_out)
    doc["settled_draw_floor"] = collections.OrderedDict(
        [
            ("value", MIN_SETTLED_DRAWS),
            (
                "basis",
                "Report A 'Missing scientific/product proof' item 4 and Report B "
                "part 4 item 1 with its P1 ('four draws per cell instead of two'). "
                "Quoted from the audits, not decided here.",
            ),
        ]
    )
    doc["evidence_status_vocabulary"] = collections.OrderedDict(
        [
            (
                "clean_observed",
                "the literal frozen rule reproduces the recorded number exactly, no "
                "named problem touches the cell, and at least four settled draws sit "
                "behind it; it does NOT mean the route is cleared for launch",
            ),
            (
                "directional_only",
                "reproduces, but fewer than four settled draws, so it must not carry "
                "a production decision on its own",
            ),
            (
                "awaiting_controller_ruling",
                "a named open ruling changes this cell's number, its keep/drop "
                "verdict, or whether it may be counted at all",
            ),
            (
                "method_tainted",
                "a named problem affects the number and no ruling can repair it "
                "without new draws",
            ),
            ("insufficient", "not enough evidence to say anything"),
        ]
    )
    doc["problem_vocabulary"] = PROBLEM_VOCABULARY
    doc["production_use_allowed_vocabulary"] = collections.OrderedDict(
        [
            ("true", "the evidence behind this cell is settled and reproduces"),
            ("manual_only", "a person must look before this cell decides anything"),
            ("false", "do not rest a route decision on this cell"),
        ]
    )
    doc["notes"] = [
        collections.OrderedDict(
            [
                ("id", "NOTE-ROUTE-KEY-COLLISION"),
                (
                    "text",
                    "IMG-TEXT holds two cells -- flux-2-pro+C_composite_textless_base "
                    "and flux-2-pro+code_overlay -- with the SAME route_key "
                    "('flux-2-pro') and the SAME arm ('C_composite_textless_base'), "
                    "carrying different acceptance numbers (1 of 4 and eliminated "
                    "versus 4 of 4). A router keyed on (route_key, arm) CANNOT TELL "
                    "THEM APART and would get an ambiguous answer. Both cells rest on "
                    "the same four trial identities, which carry two different "
                    "Controller verdicts. Until C-6c is ruled, no automatic route may "
                    "be selected by (route_key, arm) inside IMG-TEXT.",
                ),
                (
                    "cells",
                    [
                        "IMG-TEXT/flux-2-pro+C_composite_textless_base",
                        "IMG-TEXT/flux-2-pro+code_overlay",
                    ],
                ),
                ("blocking_ruling", "C-6c"),
            ]
        ),
        collections.OrderedDict(
            [
                ("id", "NOTE-THREE-DENOMINATORS"),
                (
                    "text",
                    "The routing map currently runs three denominator conventions at "
                    "once: the planned count (8), a double count of failed plus "
                    "re-sent draws (14, VID-I2V/wan-2.2-a14b-i2v), and a count with "
                    "the failed draws deleted (2, VID-2SPK/kling-v3-pro-audio). "
                    "C-6b has to say which convention the map uses everywhere.",
                ),
                ("blocking_ruling", "C-6b"),
            ]
        ),
        collections.OrderedDict(
            [
                ("id", "NOTE-BLINDNESS-BY-CONDUCT"),
                (
                    "text",
                    "Report B finding F-7. The two image rounds were blind by "
                    "construction: the true mapping was held outside the repository "
                    "and only a salted fingerprint was committed, and both "
                    "fingerprints re-compute. Every video and audio round was blind "
                    "by conduct only -- MAPPING.json sits beside the answer sheet, "
                    "the results files say commitment_verified: false, and the blind "
                    "copies the Controller actually watched were never sealed. A "
                    "clean_observed status on a video or audio cell therefore means "
                    "the ARITHMETIC reproduces; it does not mean the blinding can be "
                    "proved after the fact. Each cell carries "
                    "blinding_commitment_verified read from its own sealed results "
                    "file. This is not in the problem vocabulary and changes no "
                    "status here.",
                ),
                ("blocking_ruling", None),
            ]
        ),
        collections.OrderedDict(
            [
                ("id", "NOTE-UNTESTED-PRICING-SURFACE"),
                (
                    "text",
                    "Report B finding F-9. Every paid call behind this register ran "
                    "on fal, Vertex, Sarvam or ElevenLabs. No call has ever run on "
                    "the Gemini Developer API, yet the nano-banana-2, "
                    "nano-banana-pro, nano-banana-pro-edit and gemini-omni routes are "
                    "now priced against it. Where such a cell is clean_observed, the "
                    "ACCEPTANCE evidence is clean; the PRICE is quoted on a surface "
                    "that has never carried a call. C-13 is the smoke that would "
                    "close it.",
                ),
                ("blocking_ruling", None),
            ]
        ),
        collections.OrderedDict(
            [
                ("id", "NOTE-WHY-NO-METHOD-TAINTED-CELLS"),
                (
                    "text",
                    "No cell is method_tainted today, and that is a statement about "
                    "REPAIRABILITY, not about safety. Every problem the closed "
                    "vocabulary can name turned out to have a live Controller item "
                    "attached to it (C-3, C-4, C-6b, C-6c) or a named open question "
                    "(OPEN-1), and the audit's recompute could rebuild every number "
                    "from the sealed bytes under both readings. Twenty-one cells are "
                    "therefore waiting on a ruling rather than on fresh draws. If any "
                    "of those rulings lands the way that withdraws a number, the cell "
                    "moves to needing new draws; the generator's own guard will refuse "
                    "to run against a changed map, so this file must be rebuilt "
                    "deliberately when that happens.",
                ),
                ("blocking_ruling", None),
            ]
        ),
        collections.OrderedDict(
            [
                ("id", "NOTE-REGISTRY-UNAFFECTED"),
                (
                    "text",
                    "This register covers the human-acceptance tier only. The 575 "
                    "deterministic Registry rows are untouched by every problem named "
                    "here: they never read a Controller verdict. Where one trial "
                    "identity was sent twice the Registry holds two rows for it, "
                    "distinguishable by run_ids; they must never be added together.",
                ),
            ]
        ),
    ]
    doc["open_questions"] = [
        collections.OrderedDict(
            [
                ("id", "OPEN-1"),
                (
                    "question",
                    "Is elimination per (route, question), as frozen rule E4 says, or "
                    "per (route, case), as two runs actually applied it?",
                ),
                ("raised_in", "%s -- Decision 4" % RECOMPUTE_AUDIT),
                (
                    "no_numbered_controller_item",
                    "The Controller decision sheet carries no numbered item for "
                    "elimination SCOPE. C-3 covers the denominator, not the scope. "
                    "This question is open and unassigned.",
                ),
                ("status", "open"),
            ]
        ),
        collections.OrderedDict(
            [
                ("id", "OPEN-2"),
                (
                    "question",
                    "What is done about the three undeclared re-do runs "
                    "(vid-wan2-i2v, vid-2spk-kling, img-r1-composite), whose plans "
                    "record redo_of: null?",
                ),
                ("raised_in", "%s -- Decision 5" % RECOMPUTE_AUDIT),
                (
                    "related_ruling",
                    "C-6b decides how a re-sent draw COUNTS; it does not say whether "
                    "the sealed record is corrected.",
                ),
                ("status", "open"),
            ]
        ),
        collections.OrderedDict(
            [
                ("id", "OPEN-3"),
                (
                    "question",
                    "Were the four IMG-TEXT composite draws the same picture judged "
                    "twice, or two different pictures sharing one identity?",
                ),
                ("raised_in", "%s -- verification note" % RECOMPUTE_AUDIT),
                (
                    "why_unresolved",
                    "img-r1/RESULTS.yaml carries no artifact hash on any row, so the "
                    "sealed record cannot settle it. A byte comparison of the two "
                    "runs' artifact directories was outside the audit's scope.",
                ),
                ("related_ruling", "C-6c"),
                ("status", "open"),
            ]
        ),
    ]
    doc["summary"] = collections.OrderedDict(
        [
            (
                "by_evidence_status",
                collections.OrderedDict(
                    (s, by_status.get(s, 0)) for s in STATUS_VOCABULARY
                ),
            ),
            (
                "by_production_use_allowed",
                collections.OrderedDict(
                    (k, by_production.get(k, 0))
                    for k in ("True", "manual_only", "False")
                ),
            ),
            (
                "by_blocking_ruling",
                collections.OrderedDict(sorted(by_ruling.items())),
            ),
            (
                "by_blocking_open_question",
                collections.OrderedDict(sorted(by_open.items())),
            ),
            ("by_problem", collections.OrderedDict(sorted(by_problem.items()))),
            (
                "replacement_needed",
                sum(1 for c in cells_out if c["replacement_needed"]),
            ),
        ]
    )
    doc["cells"] = cells_out

    yaml.add_representer(
        collections.OrderedDict,
        lambda dumper, data: dumper.represent_mapping(
            "tag:yaml.org,2002:map", data.items()
        ),
    )
    body = yaml.dump(
        doc,
        default_flow_style=False,
        sort_keys=False,
        width=100,
        allow_unicode=True,
    )
    return HEADER_COMMENT + body


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="report whether the committed register would change; write nothing",
    )
    args = parser.parse_args()

    root = repo_root()
    guard_map_version(root)
    text = build(root)

    out = os.path.join(root, OUT_PATH)
    if args.check:
        if not os.path.isfile(out):
            print("MISSING: %s" % OUT_PATH)
            return 1
        with open(out, "r", encoding="utf-8") as handle:
            current = handle.read()
        if current == text:
            print("UNCHANGED: %s" % OUT_PATH)
            return 0
        print("WOULD CHANGE: %s" % OUT_PATH)
        return 1

    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as handle:
        handle.write(text)
    print("wrote %s (%d bytes)" % (OUT_PATH, len(text.encode("utf-8"))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
