#!/usr/bin/env python3
"""Validate canon/ontology/PROPOSED-domain-vocabulary-v1.yaml against the accepted corpus.

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

FAIL CLOSED. Nothing in the vocabulary file is trusted: the label census is recomputed from
canon/knowledge/current/*/source-knowledge.yaml (accepted sources only; HOLD material in
canon/candidates/ is never read) and every recorded figure is checked against the recomputation.

What a PASS establishes:
  - the recorded accepted census (mentions / unique labels / singletons) equals the recomputed one;
  - every recomputed label appears exactly once — in `mapping` OR `review_queue`, never both,
    never neither, and the file names no label the corpus does not contain (no silent drops,
    no phantom rows);
  - every per-label count in mapping and queue equals the recomputed count;
  - every mapping target is a member of the closed 22-term enum, with at most one medium term and
    at most one subject term per label, and at least one term;
  - recomputed mapped-mention coverage >= 90%, and the file's recorded coverage block matches;
  - the reserved term m_short_form_feed_video has zero mapped labels and carries a non-empty
    rationale in the vocabulary section;
  - every review-queue row carries a non-empty reason and its true source dirs.

What a PASS does NOT establish: that any term assignment is semantically right. Assignments are
authored judgements; the review queue is where contested ones go.

Deterministic: output depends only on file contents; errors are sorted before printing.

Run: python3 canon/validation/validate_domain_vocabulary.py [vocabulary.yaml]
"""
from __future__ import annotations

import collections
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
KNOWLEDGE = ROOT / "canon/knowledge/current"
DEFAULT = ROOT / "canon/ontology/PROPOSED-domain-vocabulary-v1.yaml"

MEDIUM_TERMS = (
    "m_moving_image_editing", "m_moving_image_production", "m_cinematography_lighting",
    "m_photography", "m_graphic_print_design", "m_typography", "m_colour",
    "m_web_interactive", "m_outdoor_print_media", "m_fine_art", "m_short_form_feed_video",
)
SUBJECT_TERMS = (
    "s_advertising_craft", "s_advertising_effectiveness", "s_marketing_strategy",
    "s_india_market_culture", "s_narrative_storytelling", "s_persuasion_psychology",
    "s_creative_practice_process", "s_org_management", "s_regulation_compliance",
    "s_composition_attention", "s_category_specific",
)
RESERVED = "m_short_form_feed_video"
MIN_COVERAGE = 0.90


def recompute_census(knowledge_dir: pathlib.Path = KNOWLEDGE):
    """Count scope.domain_discussed_by_source over accepted extractions only."""
    counts = collections.Counter()
    dirs = collections.defaultdict(set)
    files = sorted(knowledge_dir.glob("*/source-knowledge.yaml"))
    for f in files:
        data = yaml.safe_load(f.read_text())
        for obj in data["source_knowledge"]:
            for label in (obj.get("scope") or {}).get("domain_discussed_by_source") or []:
                counts[label] += 1
                dirs[label].add(f.parent.name)
    return counts, dirs, len(files)


def validate(path: pathlib.Path, counts=None, dirs=None) -> list[str]:
    errors: list[str] = []
    if counts is None:
        counts, dirs, _ = recompute_census()
    try:
        doc = yaml.safe_load(path.read_text())
    except Exception as exc:  # unparseable file fails closed
        return [f"{path}: cannot parse YAML: {exc}"]
    if not isinstance(doc, dict):
        return [f"{path}: top level is not a mapping"]

    total = sum(counts.values())
    n_labels = len(counts)
    n_singletons = sum(1 for v in counts.values() if v == 1)

    # 1. recorded accepted census must equal the recomputation
    recorded = ((doc.get("census") or {}).get("accepted") or {})
    for key, want in (("mentions", total), ("unique_labels", n_labels), ("singletons", n_singletons)):
        if recorded.get(key) != want:
            errors.append(f"census.accepted.{key}={recorded.get(key)!r} but recomputed value is {want}")

    mapping = doc.get("mapping") or {}
    queue = doc.get("review_queue") or []
    if not isinstance(mapping, dict):
        return errors + ["mapping is not a dict"]
    if not isinstance(queue, list):
        return errors + ["review_queue is not a list"]
    queue_labels = [row.get("label") for row in queue if isinstance(row, dict)]

    # 2. exact partition: every corpus label exactly once, no phantoms, no duplicates
    dup_queue = [l for l, k in collections.Counter(queue_labels).items() if k > 1]
    for l in sorted(dup_queue):
        errors.append(f"label {l!r} appears more than once in review_queue")
    both = set(mapping) & set(queue_labels)
    for l in sorted(both):
        errors.append(f"label {l!r} appears in BOTH mapping and review_queue")
    claimed = set(mapping) | set(queue_labels)
    for l in sorted(set(counts) - claimed):
        errors.append(f"label {l!r} ({counts[l]} mentions) is in the corpus but in neither mapping nor review_queue (silent drop)")
    for l in sorted(claimed - set(counts)):
        errors.append(f"label {l!r} is in the file but not in the accepted corpus (phantom row)")

    # 3. mapping rows: recomputed counts, closed enum, at most one term per axis
    reserved_members = []
    for label in sorted(mapping):
        row = mapping[label]
        if not isinstance(row, dict):
            errors.append(f"mapping[{label!r}] is not a dict")
            continue
        if label in counts and row.get("count") != counts[label]:
            errors.append(f"mapping[{label!r}].count={row.get('count')!r} but recomputed count is {counts[label]}")
        terms = row.get("terms")
        if not isinstance(terms, list) or not terms:
            errors.append(f"mapping[{label!r}].terms must be a non-empty list")
            continue
        unknown = [t for t in terms if t not in MEDIUM_TERMS + SUBJECT_TERMS]
        for t in unknown:
            errors.append(f"mapping[{label!r}] targets {t!r} which is not in the closed 22-term enum")
        medium = [t for t in terms if t in MEDIUM_TERMS]
        subject = [t for t in terms if t in SUBJECT_TERMS]
        if len(medium) > 1:
            errors.append(f"mapping[{label!r}] maps to {len(medium)} medium terms {medium}; at most one term per axis")
        if len(subject) > 1:
            errors.append(f"mapping[{label!r}] maps to {len(subject)} subject terms {subject}; at most one term per axis")
        if RESERVED in terms:
            reserved_members.append(label)

    # 4. coverage: recomputed, never trusted
    covered = sum(counts[l] for l in mapping if l in counts)
    share = covered / total if total else 0.0
    if share < MIN_COVERAGE:
        errors.append(f"mapped mention coverage {covered}/{total} = {share:.4f} < required {MIN_COVERAGE}")
    cov = doc.get("coverage") or {}
    for key, want in (("mapped_labels", len(mapping)), ("mapped_mentions", covered),
                      ("review_queue_labels", len(queue)), ("review_queue_mentions", total - covered)):
        if cov.get(key) != want:
            errors.append(f"coverage.{key}={cov.get(key)!r} but recomputed value is {want}")
    if abs(float(cov.get("mapped_mention_share") or 0.0) - share) > 0.0001:
        errors.append(f"coverage.mapped_mention_share={cov.get('mapped_mention_share')!r} but recomputed share is {share:.4f}")

    # 5. reserved term: zero members, rationale present
    for l in sorted(reserved_members):
        errors.append(f"reserved term {RESERVED} has mapped label {l!r}; it must have zero members until a Controller admission populates it")
    vocab = doc.get("vocabulary") or {}
    medium_rows = {r.get("term"): r for r in vocab.get("medium") or [] if isinstance(r, dict)}
    subject_rows = {r.get("term"): r for r in vocab.get("subject") or [] if isinstance(r, dict)}
    if sorted(medium_rows) != sorted(MEDIUM_TERMS):
        errors.append(f"vocabulary.medium terms {sorted(medium_rows)} != closed medium enum")
    if sorted(subject_rows) != sorted(SUBJECT_TERMS):
        errors.append(f"vocabulary.subject terms {sorted(subject_rows)} != closed subject enum")
    reserved_row = medium_rows.get(RESERVED) or {}
    if not str(reserved_row.get("rationale") or "").strip():
        errors.append(f"vocabulary entry for {RESERVED} lacks a non-empty rationale field")
    if reserved_row.get("reserved") is not True:
        errors.append(f"vocabulary entry for {RESERVED} lacks reserved: true")

    # 6. review queue rows: reason and true source dirs
    for row in queue:
        if not isinstance(row, dict):
            errors.append("review_queue contains a non-dict row")
            continue
        label = row.get("label")
        if not str(row.get("reason") or "").strip():
            errors.append(f"review_queue[{label!r}] lacks a non-empty reason")
        if label in counts:
            if row.get("count") != counts[label]:
                errors.append(f"review_queue[{label!r}].count={row.get('count')!r} but recomputed count is {counts[label]}")
            if dirs is not None and sorted(row.get("source_dirs") or []) != sorted(dirs[label]):
                errors.append(f"review_queue[{label!r}].source_dirs do not match recomputed dirs {sorted(dirs[label])}")
    return sorted(errors)


def main(argv: list[str]) -> int:
    path = pathlib.Path(argv[1]) if len(argv) > 1 else DEFAULT
    counts, dirs, n_files = recompute_census()
    errors = validate(path, counts, dirs)
    total = sum(counts.values())
    print(f"census recomputed over {n_files} accepted source-knowledge.yaml files: "
          f"{total} mentions / {len(counts)} labels / {sum(1 for v in counts.values() if v == 1)} singletons")
    if errors:
        print(f"FAIL {path} ({len(errors)} errors)")
        for e in errors:
            print("  -", e)
        return 1
    doc = yaml.safe_load(path.read_text())
    covered = sum(counts[l] for l in (doc.get("mapping") or {}) if l in counts)
    print(f"PASS {path}: {len(doc['mapping'])} labels mapped, {covered}/{total} mentions "
          f"({covered/total:.1%}); {len(doc['review_queue'])} labels queued for review; "
          f"{RESERVED} reserved with 0 members")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
