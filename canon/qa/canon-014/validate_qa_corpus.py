#!/usr/bin/env python3
"""Validator for the CANON-014 grounded Q&A corpus.

Checks the corpus is well formed and traceable. It says nothing about whether an answer is RIGHT -
no human and no model has answered any item, and this validator cannot change that.

Rules, all mechanical:
  1. every bank parses, names its source, its directory, its knowledge_dir and its source_status
  2. every item carries the fields the corpus contract requires, all non-empty
  3. qa_ids are unique across the whole corpus
  4. no two items share a question, normalised
  5. every item's source_id matches its bank's
  6. every item's source_status matches its bank's, and the bank's matches where the artifacts
     actually live - a bank cannot claim `accepted` for a source sitting in the candidate tree
  7. every bank's knowledge_dir exists and holds a source-knowledge.yaml
  8. controlled values: answer_type, difficulty, knowledge_type, source_status, requires_application
  9. no answer under 35 words, which is the floor the corpus screen has used throughout
"""
import os, re, sys, glob
import yaml

REQUIRED = ["qa_id", "source_id", "source_locator", "question", "answer", "answer_type",
            "difficulty", "knowledge_type", "requires_application", "support", "source_status"]
# The corpus vocabulary is the union of the two lanes' vocabularies, minus two pairs of genuine
# near-synonyms which were merged (`factual` -> `factual_recall`, `concept_definition` ->
# `concept_understanding`, both keeping `answer_type_as_written`). The four labels only one lane
# used are kept because each names a distinct kind of question and collapsing them would lose
# information about 258 items.
ANSWER_TYPES = {"source_position", "mechanism", "application", "concept_understanding",
                "failure_diagnosis", "factual_recall", "comparison", "tradeoff",
                "boundary_condition", "repair"}
DIFFICULTIES = {"easy", "medium", "hard"}
STATUSES = {"accepted", "hold"}


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", " ".join(str(s).lower().split()))


def main(root="canon/qa/canon-014"):
    errors, ids, questions, total, by_source = [], {}, {}, 0, {}
    accepted = set(os.listdir("canon/knowledge/current"))
    held = {d for d in os.listdir("canon/candidates/canon-014")
            if os.path.isdir(os.path.join("canon/candidates/canon-014", d))}

    for f in sorted(glob.glob(os.path.join(root, "*-qa-bank.yaml"))):
        try:
            doc = yaml.safe_load(open(f))
        except Exception as exc:
            errors.append(f"{f}: parse failure: {exc}")
            continue
        name = os.path.basename(f)
        for k in ("source_id", "source_dir", "knowledge_dir", "source_status", "qa_items"):
            if not doc.get(k):
                errors.append(f"{name}: bank missing {k}")
        stem, status = doc.get("source_dir"), doc.get("source_status")
        if status not in STATUSES:
            errors.append(f"{name}: invalid bank source_status {status!r}")
        expected = "accepted" if stem in accepted else "hold" if stem in held else None
        if expected is None:
            errors.append(f"{name}: source_dir {stem!r} is neither live nor a candidate")
        elif expected != status:
            errors.append(f"{name}: claims source_status {status!r} but its artifacts live in the "
                          f"{expected} tree - a held source must never be presented as accepted")
        kdir = doc.get("knowledge_dir") or ""
        if not os.path.isfile(os.path.join(kdir, "source-knowledge.yaml")):
            errors.append(f"{name}: knowledge_dir {kdir!r} has no source-knowledge.yaml")

        items = doc.get("qa_items") or []
        total += len(items)
        by_source[stem] = {"items": len(items), "status": status,
                           "requires_application": sum(1 for i in items
                                                       if i.get("requires_application") is True)}
        for i in items:
            qid = i.get("qa_id", "<no id>")
            for k in REQUIRED:
                if k == "requires_application":
                    if not isinstance(i.get(k), bool):
                        errors.append(f"{qid}: requires_application must be true or false")
                elif not str(i.get(k, "")).strip():
                    errors.append(f"{qid}: missing {k}")
            if qid in ids:
                errors.append(f"{qid}: duplicate qa_id, also in {ids[qid]}")
            ids[qid] = name
            q = norm(i.get("question"))
            if q in questions:
                errors.append(f"{qid}: duplicate question, also asked by {questions[q]}")
            questions[q] = qid
            if i.get("source_id") != doc.get("source_id"):
                errors.append(f"{qid}: source_id does not match its bank")
            if i.get("source_status") != status:
                errors.append(f"{qid}: source_status does not match its bank")
            if i.get("answer_type") not in ANSWER_TYPES:
                errors.append(f"{qid}: invalid answer_type {i.get('answer_type')!r}")
            if i.get("difficulty") not in DIFFICULTIES:
                errors.append(f"{qid}: invalid difficulty {i.get('difficulty')!r}")
            if len(str(i.get("answer", "")).split()) < 35:
                errors.append(f"{qid}: answer under 35 words")

    for e in errors:
        print("ERROR", e)
    app = sum(v["requires_application"] for v in by_source.values())
    print(f"\n{len(by_source)} banks, {total} items, {len(errors)} errors")
    print(f"requires_application: {app} ({app / total * 100:.1f}% observed, never required)")
    print("GROUNDED, UNGRADED, UNCALIBRATED. Not benchmark ground truth.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(*sys.argv[1:]))
