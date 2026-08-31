#!/usr/bin/env python3
"""Offline retrieval evaluation: what changes between EVAL-037's interface and CANON-015's.

USD 0. No model call, no provider call, no media. Everything measured here is a property
of committed bytes and deterministic code.

Three columns are produced per brief.

  observed_eval_037   what the Sonnet CONTROLLED_CANON lane ACTUALLY received, read out of
                      the committed transcripts. Real behaviour, real byte counts, and the
                      only column that is evidence about a model rather than about code.

  replayed_eval_037   the same queries replayed through EVAL-037's own `canon_tools.py`
                      against today's corpus. Included so the comparison isolates the
                      INTERFACE change from any corpus change; the accepted-Canon bytes
                      are identical, but the held corpus moved on after EVAL-037 froze.

  canon_015           one `canon_context` call per brief, default budgets.

What this evaluation CANNOT tell you: whether the selected knowledge is the RIGHT
knowledge. Nothing in the repository labels a Canon object relevant to a brief, and
inventing such labels to produce a precision number would be manufacturing a ground truth.
Relevance is left to the human rubric in HUMAN-REVIEW-RUBRIC.md, and the numbers below are
about size, composition, spread, purity and reproducibility only.
"""
import argparse
import json
import pathlib
import statistics
import sys

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from canon.retrieval.budgets import COMPACT_BUDGETS, DEFAULT_BUDGETS  # noqa: E402
from canon.retrieval.bundle import build_bundle, model_payload  # noqa: E402
from canon.retrieval.corpus import AcceptedCanon, tokenize  # noqa: E402
from canon.retrieval.rank import TypedIndex  # noqa: E402

EVAL_SET = pathlib.Path(__file__).parent / "EVAL-SET-v0.1.yaml"


def jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def mean_pairwise_jaccard(token_sets):
    """How much the retrieved set repeats itself. 0.0 = no shared vocabulary at all."""
    pairs = [jaccard(token_sets[i], token_sets[j])
             for i in range(len(token_sets)) for j in range(i + 1, len(token_sets))]
    return round(statistics.mean(pairs), 4) if pairs else 0.0


# ── observed EVAL-037 behaviour ─────────────────────────────────────────────────────
def observed_for_trial(trial):
    objects, sources, bytes_total = [], {}, 0
    max_from_one_source_in_a_search = 0
    for search in trial["searches"]:
        bytes_total += search["result_bytes"] or 0
        per_search = {}
        for obj in search["returned_objects"]:
            objects.append(obj)
            sources[obj["source_dir"]] = sources.get(obj["source_dir"], 0) + 1
            per_search[obj["source_dir"]] = per_search.get(obj["source_dir"], 0) + 1
        if per_search:
            max_from_one_source_in_a_search = max(max_from_one_source_in_a_search,
                                                  max(per_search.values()))
    ids = [o["item_id"] for o in objects]
    accepted = [o for o in objects if o["source_status"] == "ACCEPTED"]
    accepted_non_qa = [o for o in accepted if o["kind"] != "qa"]
    kinds = {}
    for obj in objects:
        kinds[obj["kind"]] = kinds.get(obj["kind"], 0) + 1
    return {
        "retrieval_operations": trial["canon_search_calls"] + trial["canon_read_calls"],
        "canon_search_calls": trial["canon_search_calls"],
        "canon_read_calls": trial["canon_read_calls"],
        "bytes_exposed": bytes_total,
        "objects_returned": len(objects),
        "repeat_objects_within_trial": len(ids) - len(set(ids)),
        "accepted_share": round(len(accepted) / len(objects), 4) if objects else 0.0,
        "accepted_non_qa_share": (round(len(accepted_non_qa) / len(objects), 4)
                                  if objects else 0.0),
        "distinct_sources": len(sources),
        "max_objects_from_one_source_in_one_search": max_from_one_source_in_a_search,
        "objects_by_kind": dict(sorted(kinds.items())),
        "declared_knowledge_needs": len(trial["declared_knowledge_needs"]),
    }


def observed_for_brief(trials):
    per_trial = [observed_for_trial(t) for t in trials]

    def mean(field):
        return round(statistics.mean(v[field] for v in per_trial), 2)

    return {
        "trials": len(per_trial),
        "mean_retrieval_operations": mean("retrieval_operations"),
        "mean_bytes_exposed": round(mean("bytes_exposed")),
        "mean_objects_returned": mean("objects_returned"),
        "mean_distinct_sources": mean("distinct_sources"),
        "mean_accepted_share": mean("accepted_share"),
        "mean_accepted_non_qa_share": mean("accepted_non_qa_share"),
        "mean_repeat_objects_within_trial": mean("repeat_objects_within_trial"),
        "max_objects_from_one_source_in_one_search": max(
            v["max_objects_from_one_source_in_one_search"] for v in per_trial),
        "per_trial": {t["trial_id"]: v for t, v in zip(trials, per_trial)},
    }


# ── replayed EVAL-037 interface, today's corpus ─────────────────────────────────────
def replay_eval_037(trials, limit=8):
    """Re-issue the recorded queries through EVAL-037's own tool module, unmodified."""
    sys.path.insert(0, str(REPO_ROOT / "eval/experiments/EVAL-037/tools"))
    import canon_tools

    canon = canon_tools.Canon(REPO_ROOT, condition="FULL_CANON")
    per_trial = []
    for trial in trials:
        objects, bytes_total = [], 0
        for search in trial["searches"]:
            result = canon.canon_search(search["query"], limit=limit)
            # `default=str` because raw corpus items carry YAML dates, which the
            # EVAL-037 harness serialised through its own provider layer rather than
            # json.dumps. The byte count is within a few characters either way.
            bytes_total += len(json.dumps(result, ensure_ascii=False, default=str))
            objects.extend(result["results"])
        accepted = [o for o in objects if o["source_status"] == "ACCEPTED"]
        accepted_non_qa = [o for o in accepted if o["kind"] != "qa"]
        token_sets = [frozenset(tokenize(canon_tools._text_of(o["item"]))) for o in objects]
        per_trial.append({
            "trial_id": trial["trial_id"],
            "searches": len(trial["searches"]),
            "bytes_exposed": bytes_total,
            "objects_returned": len(objects),
            "accepted_share": round(len(accepted) / len(objects), 4) if objects else 0.0,
            "accepted_non_qa_share": (round(len(accepted_non_qa) / len(objects), 4)
                                      if objects else 0.0),
            "distinct_sources": len({o["source_dir"] for o in objects}),
            "mean_pairwise_jaccard": mean_pairwise_jaccard(token_sets),
        })
    return per_trial


# ── CANON-015 ───────────────────────────────────────────────────────────────────────
def canon_015_for_brief(brief, corpus, index, budgets, declared_needs=()):
    bundle = build_bundle(brief["text"], corpus, budgets=budgets, typed_index=index,
                          declared_needs=declared_needs)
    payload = model_payload(bundle)
    token_sets = [frozenset(tokenize(json.dumps(i["content"], ensure_ascii=False)))
                  for i in payload["items"]]
    statuses = {i["epistemics"]["source_status"] for i in payload["items"]}
    return bundle, {
        "retrieval_operations": 1,
        "chars": payload["size"]["total_chars"],
        "estimated_tokens": payload["size"]["estimated_tokens"],
        "items": payload["spread"]["items"],
        "distinct_sources": payload["spread"]["distinct_sources"],
        "distinct_lineage_groups": payload["spread"]["distinct_lineage_groups"],
        "max_items_from_one_source": payload["spread"]["max_items_from_one_source"],
        "items_by_kind": payload["spread"]["items_by_kind"],
        "source_stated_domains": payload["spread"]["source_stated_domains"],
        "accepted_share": 1.0 if statuses == {"ACCEPTED"} else 0.0,
        "accepted_non_qa_share": 1.0 if statuses == {"ACCEPTED"} else 0.0,
        "questions_planned": payload["coverage"]["questions_planned"],
        "questions_with_no_item": payload["coverage"]["questions_with_no_item"],
        "question_coverage": round(
            len(payload["coverage"]["questions_with_at_least_one_item"])
            / max(len(payload["coverage"]["questions_planned"]), 1), 4),
        "mean_pairwise_jaccard": mean_pairwise_jaccard(token_sets),
        "items_delivered_complete_share": payload["size"]["items_delivered_complete_share"],
        "second_read_would_be_needed_for": [i["item_id"] for i in payload["items"]
                                            if not i["delivered_complete"]],
    }


def declared_need_term_coverage(bundle, trials, index):
    """A LEXICAL PROXY, not a relevance measure — read the caveat before using it.

    It answers one narrow question: of the discriminative words the model itself wrote
    when stating what it needed to know, how many appear anywhere in the bundle's content?
    A high number does not mean the bundle answered the need; a low one does not mean it
    failed. It is reported because it is checkable, and labelled because it is weak.
    """
    payload = model_payload(bundle)
    haystack = set(tokenize(json.dumps([i["content"] for i in payload["items"]],
                                       ensure_ascii=False)))
    discriminative = index.discriminative_terms()
    covered = total = 0
    for trial in trials:
        for need in trial["declared_knowledge_needs"]:
            terms = {t for t in tokenize(need) if t in discriminative}
            if not terms:
                continue
            total += len(terms)
            covered += len(terms & haystack)
    return {"declared_need_terms": total,
            "present_in_bundle": covered,
            "share": round(covered / total, 4) if total else None,
            "caveat": ("Lexical overlap only. It is not a relevance score and must not be "
                       "reported as one.")}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-json", default=str(
        pathlib.Path(__file__).parent / "results-v0.1.json"))
    parser.add_argument("--skip-replay", action="store_true",
                        help="skip the EVAL-037 replay column (it loads the full corpus)")
    parser.add_argument("--dump-bundles", default=str(
        pathlib.Path(__file__).parent / "bundles"),
        help="directory to write one model-facing bundle per brief, for human review")
    args = parser.parse_args(argv)

    data = yaml.safe_load(EVAL_SET.read_text(encoding="utf-8"))
    briefs = {b["brief_id"]: b for b in data["briefs"]}
    by_brief = {}
    for trial in data["sonnet_controlled_trials"]:
        by_brief.setdefault(trial["brief_id"], []).append(trial)

    corpus = AcceptedCanon(REPO_ROOT)
    index = TypedIndex(corpus)

    replay = {}
    if not args.skip_replay:
        for brief_id, trials in sorted(by_brief.items()):
            replay[brief_id] = replay_eval_037(trials)

    per_brief = {}
    for brief_id, trials in sorted(by_brief.items()):
        observed = observed_for_brief(trials)
        needs = [n for t in trials for n in t["declared_knowledge_needs"]]
        bundle, after = canon_015_for_brief(briefs[brief_id], corpus, index,
                                            DEFAULT_BUDGETS)
        _, compact = canon_015_for_brief(briefs[brief_id], corpus, index, COMPACT_BUDGETS)
        if args.dump_bundles:
            out_dir = pathlib.Path(args.dump_bundles)
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / f"{brief_id}-canon-context.json").write_text(
                json.dumps(model_payload(bundle), indent=2, ensure_ascii=False),
                encoding="utf-8")
        row = {
            "title": briefs[brief_id]["title"],
            "observed_eval_037": observed,
            "canon_015_default": after,
            "canon_015_compact": compact,
            "declared_need_term_coverage": declared_need_term_coverage(
                bundle, trials, index),
            "declared_needs_recorded": len(needs),
        }
        if brief_id in replay:
            rows = replay[brief_id]
            row["replayed_eval_037"] = {
                "mean_bytes_exposed": round(statistics.mean(
                    r["bytes_exposed"] for r in rows)),
                "mean_objects_returned": round(statistics.mean(
                    r["objects_returned"] for r in rows), 2),
                "mean_accepted_share": round(statistics.mean(
                    r["accepted_share"] for r in rows), 4),
                "mean_accepted_non_qa_share": round(statistics.mean(
                    r["accepted_non_qa_share"] for r in rows), 4),
                "mean_distinct_sources": round(statistics.mean(
                    r["distinct_sources"] for r in rows), 2),
                "mean_pairwise_jaccard": round(statistics.mean(
                    r["mean_pairwise_jaccard"] for r in rows), 4),
            }
        per_brief[brief_id] = row

    def avg(path):
        values = []
        for row in per_brief.values():
            cursor = row
            for key in path:
                cursor = cursor.get(key) if isinstance(cursor, dict) else None
                if cursor is None:
                    break
            if isinstance(cursor, (int, float)):
                values.append(cursor)
        return round(statistics.mean(values), 4) if values else None

    totals = {
        "briefs": len(per_brief),
        "eval_037_total_searches": sum(
            r["observed_eval_037"]["per_trial"][t]["canon_search_calls"]
            for r in per_brief.values() for t in r["observed_eval_037"]["per_trial"]),
        "eval_037_total_reads": sum(
            r["observed_eval_037"]["per_trial"][t]["canon_read_calls"]
            for r in per_brief.values() for t in r["observed_eval_037"]["per_trial"]),
        "eval_037_total_bytes_exposed": sum(
            r["observed_eval_037"]["per_trial"][t]["bytes_exposed"]
            for r in per_brief.values() for t in r["observed_eval_037"]["per_trial"]),
        "eval_037_mean_bytes_per_trial": avg(["observed_eval_037", "mean_bytes_exposed"]),
        "eval_037_mean_retrieval_operations": avg(
            ["observed_eval_037", "mean_retrieval_operations"]),
        "eval_037_mean_accepted_share": avg(["observed_eval_037", "mean_accepted_share"]),
        "eval_037_mean_accepted_non_qa_share": avg(
            ["observed_eval_037", "mean_accepted_non_qa_share"]),
        "eval_037_mean_distinct_sources": avg(
            ["observed_eval_037", "mean_distinct_sources"]),
        "canon_015_mean_chars": avg(["canon_015_default", "chars"]),
        "canon_015_mean_items": avg(["canon_015_default", "items"]),
        "canon_015_mean_distinct_sources": avg(["canon_015_default", "distinct_sources"]),
        "canon_015_mean_lineage_groups": avg(
            ["canon_015_default", "distinct_lineage_groups"]),
        "canon_015_retrieval_operations": 1,
        "canon_015_accepted_share": avg(["canon_015_default", "accepted_share"]),
        "canon_015_mean_question_coverage": avg(
            ["canon_015_default", "question_coverage"]),
        "canon_015_mean_pairwise_jaccard": avg(
            ["canon_015_default", "mean_pairwise_jaccard"]),
        "canon_015_mean_delivered_complete_share": avg(
            ["canon_015_default", "items_delivered_complete_share"]),
        "canon_015_compact_mean_chars": avg(["canon_015_compact", "chars"]),
    }
    if replay:
        totals["replayed_eval_037_mean_bytes"] = avg(
            ["replayed_eval_037", "mean_bytes_exposed"])
        totals["replayed_eval_037_mean_accepted_share"] = avg(
            ["replayed_eval_037", "mean_accepted_share"])
        totals["replayed_eval_037_mean_pairwise_jaccard"] = avg(
            ["replayed_eval_037", "mean_pairwise_jaccard"])

    before = totals["eval_037_mean_bytes_per_trial"]
    after = totals["canon_015_mean_chars"]
    totals["context_reduction_vs_observed_eval_037"] = (
        round(1 - after / before, 4) if before else None)

    report = {
        "evaluation": "CANON-015 offline retrieval evaluation v0.1",
        "spend_usd": 0,
        "model_calls": 0,
        "media_generated": 0,
        "eval_set": data["eval_set_version"],
        "eval_set_provenance": data["provenance"],
        "accepted_corpus_fingerprint": corpus.fingerprint,
        "budgets_default": DEFAULT_BUDGETS.as_dict(),
        "budgets_compact": COMPACT_BUDGETS.as_dict(),
        "what_this_does_not_measure": (
            "Relevance, usefulness, and any effect on an accepted customer outcome. No "
            "item in the corpus is labelled relevant to any brief, so no precision or "
            "recall number is computed. Use HUMAN-REVIEW-RUBRIC.md for relevance and a "
            "controlled model experiment for outcome effect."),
        "unbounded_lane_outcomes": data["unbounded_lane_outcomes"],
        "totals": totals,
        "per_brief": per_brief,
    }
    pathlib.Path(args.out_json).write_text(
        json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"briefs evaluated: {totals['briefs']}")
    print(f"EVAL-037 observed: {totals['eval_037_total_searches']} searches + "
          f"{totals['eval_037_total_reads']} reads over 18 trials; "
          f"{totals['eval_037_total_bytes_exposed']:,} bytes exposed; "
          f"mean {totals['eval_037_mean_bytes_per_trial']:,.0f} bytes/trial")
    print(f"  accepted share {totals['eval_037_mean_accepted_share']:.1%}, "
          f"accepted non-Q&A {totals['eval_037_mean_accepted_non_qa_share']:.1%}, "
          f"mean sources {totals['eval_037_mean_distinct_sources']}")
    print(f"CANON-015 default: 1 operation; mean {totals['canon_015_mean_chars']:,.0f} chars "
          f"({totals['canon_015_mean_items']:.1f} items, "
          f"{totals['canon_015_mean_distinct_sources']:.1f} sources, "
          f"{totals['canon_015_mean_lineage_groups']:.1f} independent origins)")
    print(f"  accepted share {totals['canon_015_accepted_share']:.0%}, "
          f"question coverage {totals['canon_015_mean_question_coverage']:.0%}, "
          f"delivered whole {totals['canon_015_mean_delivered_complete_share']:.0%}")
    print(f"  context reduction vs observed EVAL-037: "
          f"{totals['context_reduction_vs_observed_eval_037']:.1%}")
    if replay:
        print(f"replayed EVAL-037 interface on today's corpus: "
              f"mean {totals['replayed_eval_037_mean_bytes']:,.0f} bytes, "
              f"accepted share {totals['replayed_eval_037_mean_accepted_share']:.1%}")
    print(f"written: {args.out_json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
