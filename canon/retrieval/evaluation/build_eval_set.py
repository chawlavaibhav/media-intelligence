#!/usr/bin/env python3
"""Extract the CANON-015 offline evaluation set from the frozen EVAL-037 branches.

The evaluation set is not invented. Every brief, every query and every declared knowledge
need in `EVAL-SET-v0.1.yaml` was issued by a real model in a real EVAL-037 lane and is
committed on a branch this script names and reads by `git show`. Re-running it against the
same refs must reproduce the same file; that is what makes the provenance checkable.

Nothing is written into `eval/` and no EVAL-037 artifact is modified. This reads.

    python3 canon/retrieval/evaluation/build_eval_set.py --out canon/retrieval/evaluation/EVAL-SET-v0.1.yaml
"""
import argparse
import hashlib
import json
import pathlib
import subprocess
import sys

SONNET_REF = "origin/work/eval-037-sonnet-controlled-canon"
GEMMA_REF = "origin/work/eval-037-gemma-controlled-canon"
GEMMA_REQUIRED_REF = "origin/work/eval-037-gemma-required-canon"
SONNET_REPAIR_REF = "origin/work/eval-037-sonnet-full-canon-repair"

BRIEF_IDS = ["B01", "B02", "B03", "B04", "B05", "B06"]
BRIEF_TITLES = {
    "B01": "RentOK vertical video ad (Indian hostel/PG software)",
    "B02": "aight festive promotional poster (media-generation API pricing)",
    "B03": "mosambi sparkling drink premium advertising image",
    "B04": "Indian D2C skincare UGC performance video",
    "B05": "two-person café dialogue scene, six shots",
    "B06": "Aster Meridian 38 watch e-commerce hero image",
}


def git_show(ref, path):
    result = subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True,
                            text=True, check=False)
    if result.returncode != 0:
        raise SystemExit(f"cannot read {path} at {ref}: {result.stderr.strip()}\n"
                         f"Fetch the frozen branch first: git fetch origin "
                         f"{ref.split('/', 1)[1]}")
    return result.stdout


def rev(ref):
    return subprocess.run(["git", "rev-parse", ref], capture_output=True, text=True,
                          check=True).stdout.strip()


def transcript_paths(ref, lane):
    listing = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", ref, "--",
         f"eval/experiments/EVAL-037/runs/{lane}/transcripts"],
        capture_output=True, text=True, check=True).stdout.split()
    return sorted(p for p in listing if p.endswith(".jsonl"))


def build():
    briefs = {}
    for brief_id in BRIEF_IDS:
        text = git_show(SONNET_REF, f"eval/experiments/EVAL-037/common/briefs/{brief_id}.txt")
        briefs[brief_id] = {
            "brief_id": brief_id,
            "title": BRIEF_TITLES[brief_id],
            "text": text.strip(),
            "sha256_of_committed_file": hashlib.sha256(text.encode()).hexdigest(),
        }

    sonnet_result = json.loads(git_show(
        SONNET_REF, "eval/experiments/EVAL-037/runs/sonnet-controlled-canon/result.json"))

    # Per-search evidence comes from the transcripts, which carry the FULL tool result and
    # therefore the status and kind of every object the model actually saw. The result.json
    # summary records byte counts but not what was inside them.
    observed = {}
    for path in transcript_paths(SONNET_REF, "sonnet-controlled-canon"):
        trial_id = pathlib.Path(path).name.split("-a0")[0]
        searches = []
        for line in git_show(SONNET_REF, path).splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            call = record["call"]
            if call["name"] != "canon_search":
                continue
            results = (record.get("full_result") or {}).get("results", [])
            searches.append({
                "query": call["arguments"].get("query"),
                "limit_requested": call["arguments"].get("limit"),
                "result_bytes": call.get("result_bytes"),
                "results_returned": len(results),
                "total_matches_in_corpus": (record.get("full_result") or {}).get(
                    "total_matches"),
                "returned_objects": [
                    {"item_id": r["item_id"], "kind": r["kind"],
                     "source_dir": r["source_dir"], "source_status": r["source_status"]}
                    for r in results],
            })
        observed[trial_id] = searches

    trials = []
    for trial in sorted(sonnet_result["trials"], key=lambda t: t["trial_id"]):
        controlled = trial["controlled_retrieval"]
        trials.append({
            "trial_id": trial["trial_id"],
            "brief_id": trial["brief_id"],
            "repetition": trial["repetition"],
            "status": trial["status"],
            "declared_knowledge_needs": list(controlled["declared_knowledge_needs"]),
            "canon_search_calls": controlled["canon_search_calls"],
            "canon_read_calls": controlled["canon_read_calls"],
            "canon_catalog_calls": controlled["canon_catalog_calls"],
            "searches": observed.get(trial["trial_id"], []),
        })

    gemma_result = json.loads(git_show(
        GEMMA_REF, "eval/experiments/EVAL-037/runs/gemma-controlled-canon/result.json"))
    gemma_queries = []
    for trial in sorted(gemma_result["trials"], key=lambda t: t["trial_id"]):
        for entry in (trial.get("canon_governor") or {}).get("governor_ledger", []):
            if entry.get("tool") == "canon_search" and entry.get("query"):
                gemma_queries.append({
                    "trial_id": trial["trial_id"], "brief_id": trial["brief_id"],
                    "query": entry["query"], "applied_limit": entry.get("applied_limit"),
                    "results_returned": entry.get("results_returned"),
                    "trial_status": trial["status"]})

    gemma_required = json.loads(git_show(
        GEMMA_REQUIRED_REF,
        "eval/experiments/EVAL-037/runs/gemma-required-canon/result.json"))
    sonnet_repair = json.loads(git_show(
        SONNET_REPAIR_REF,
        "eval/experiments/EVAL-037/runs/sonnet-full-canon-repair-001/result.json"))

    def statuses(result):
        out = {}
        for trial in result["trials"]:
            out[trial["status"]] = out.get(trial["status"], 0) + 1
        return out

    return {
        "eval_set_version": "canon-015-offline-retrieval-eval-v0.1",
        "what_this_is": (
            "Real retrieval behaviour recorded during EVAL-037, extracted for offline "
            "comparison against the CANON-015 retriever. It is a set of QUESTIONS models "
            "actually asked and a record of WHAT CAME BACK. It is not a relevance "
            "benchmark: no item here is labelled relevant or irrelevant, because nobody "
            "has judged them. Relevance needs the human rubric in "
            "HUMAN-REVIEW-RUBRIC.md."),
        "provenance": {
            "generated_by": "canon/retrieval/evaluation/build_eval_set.py",
            "sonnet_controlled_canon": {"ref": SONNET_REF, "commit": rev(SONNET_REF),
                                        "lane": "sonnet-controlled-canon"},
            "gemma_controlled_canon": {"ref": GEMMA_REF, "commit": rev(GEMMA_REF),
                                       "lane": "gemma-controlled-canon"},
            "gemma_required_canon": {"ref": GEMMA_REQUIRED_REF,
                                     "commit": rev(GEMMA_REQUIRED_REF),
                                     "lane": "gemma-required-canon"},
            "sonnet_full_canon_repair": {"ref": SONNET_REPAIR_REF,
                                         "commit": rev(SONNET_REPAIR_REF),
                                         "lane": "sonnet-full-canon-repair-001"},
            "canon_fingerprints_used_by_eval_037": sonnet_result["canon_fingerprints"],
            "note": ("EVAL-037 searched the FULL status-aware corpus: accepted Canon, HOLD "
                     "candidates and the Q&A banks. CANON-015 retrieves accepted Canon "
                     "only. The accepted bytes are identical in both — the accepted-Canon "
                     "fingerprint on main recomputes to the value the corpus index "
                     "records — so a size and composition comparison is fair, and the "
                     "difference in what is REACHABLE is itself one of the findings."),
        },
        "briefs": [briefs[b] for b in BRIEF_IDS],
        "sonnet_controlled_trials": trials,
        "gemma_controlled_queries": gemma_queries,
        "unbounded_lane_outcomes": {
            "note": ("Why an unbounded retrieval default is not an option. Neither lane is "
                     "re-run by CANON-015; both are quoted from their committed results."),
            "sonnet_full_canon_repair_001": {
                "model": sonnet_repair.get("model"),
                "trial_count": sonnet_repair.get("trial_count"),
                "statuses": statuses(sonnet_repair)},
            "gemma_required_canon": {
                "model": gemma_required.get("model"),
                "trial_count": gemma_required.get("trial_count"),
                "statuses": statuses(gemma_required)},
        },
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    import yaml
    data = build()
    text = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100)
    pathlib.Path(args.out).write_text(text, encoding="utf-8")
    trials = data["sonnet_controlled_trials"]
    print(f"wrote {args.out}: {len(data['briefs'])} briefs, {len(trials)} Sonnet trials, "
          f"{sum(len(t['searches']) for t in trials)} Sonnet searches, "
          f"{len(data['gemma_controlled_queries'])} Gemma queries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
