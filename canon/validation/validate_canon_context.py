#!/usr/bin/env python3
"""Validate a CANON_CONTEXT object against canon/context/canon-context-schema-v0.1.yaml.

FAIL CLOSED. This is a linkage and admission check in the spirit of
canon/experiments/v1/value-gate/build_oracle_contexts.py: every claim in a context must resolve to
a committed id in accepted Canon, from a source whose Audit Gate record is `complete`, within a
declared budget, answering a question the context itself states.

What a PASS establishes:
  - every ref exists in canon/knowledge/current and is owned by the directory it names;
  - no HOLD/candidate or Q&A material is cited;
  - every cited source passed the Audit Gate;
  - verbatim principles match the committed extraction byte-for-byte after whitespace normalization;
  - the declared budget holds;
  - questions and guidance answer each other with no orphans on either side;
  - conflicts and limits are stated rather than silently resolved.

What a PASS does NOT establish: that the guidance is the right guidance for the brief. No validator
can check that.

Run: python3 canon/validation/validate_canon_context.py <context.yaml> [...]
"""
from __future__ import annotations

import hashlib
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
KNOWLEDGE = ROOT / "canon/knowledge/current"
CANDIDATES = ROOT / "canon/candidates"
RECORDS = ROOT / "canon/audit/records"

SCHEMA_VERSION = "v0.1"
GUIDANCE_FIELDS = ("principle", "applicability", "concrete_implication",
                   "failure_mode", "uncertainty")
TOP_LEVEL = ("canon_context_version", "context_id", "built_for", "budget",
             "production_questions", "key_guidance", "conflicts",
             "do_not_overgeneralize", "source_trace")


def norm(text: str) -> str:
    return " ".join(str(text or "").split())


def digest(text: str) -> str:
    return hashlib.sha256(norm(text).encode("utf-8")).hexdigest()


def load_corpus():
    """Every accepted Canon object, by id, with its owning directory and audit status."""
    objects, owner, source_of = {}, {}, {}
    for directory in sorted(KNOWLEDGE.iterdir()):
        if not directory.is_dir():
            continue
        knowledge = yaml.safe_load((directory / "source-knowledge.yaml").read_text()) or {}
        systems = yaml.safe_load((directory / "source-concept-systems.yaml").read_text()) or {}
        for obj in knowledge.get("source_knowledge") or []:
            objects[obj["sk_id"]] = ("source_knowledge", obj)
            owner[obj["sk_id"]] = directory.name
            source_of[obj["sk_id"]] = knowledge.get("source_id")
        for system in systems.get("source_concept_systems") or []:
            objects[system["scs_id"]] = ("concept_system", system)
            owner[system["scs_id"]] = directory.name
            source_of[system["scs_id"]] = systems.get("source_id")

    audited = {}
    for path in RECORDS.glob("*.audit.yaml"):
        record = yaml.safe_load(path.read_text()) or {}
        name = str(record.get("knowledge_dir", "")).rstrip("/").split("/")[-1]
        audited[name] = record.get("audit_status")
    return objects, owner, source_of, audited


def field_text(kind: str, obj: dict, field: str) -> str | None:
    """The committed text a principle claims to be rendered from."""
    if field in obj:
        return obj[field]
    if kind == "concept_system" and field == "whole_system_claim":
        return (obj.get("whole_system_claim") or {}).get("text")
    return None


def validate(path: pathlib.Path, corpus) -> list[str]:
    objects, owner, source_of, audited = corpus
    errors: list[str] = []

    def err(message: str) -> None:
        errors.append(f"{path.name}: {message}")

    raw = path.read_bytes()
    try:
        ctx = yaml.safe_load(raw.decode("utf-8")) or {}
    except yaml.YAMLError as exc:
        return [f"{path.name}: unparseable YAML — {exc}"]
    if not isinstance(ctx, dict):
        return [f"{path.name}: top level is not a mapping"]

    for key in TOP_LEVEL:
        if key not in ctx:
            err(f"missing required top-level key `{key}`")
    if errors:
        return errors

    if ctx["canon_context_version"] != SCHEMA_VERSION:
        err(f"canon_context_version is {ctx['canon_context_version']!r}, expected {SCHEMA_VERSION!r}")

    for key in ("request_ref", "outcome_kind"):
        if not norm((ctx.get("built_for") or {}).get(key)):
            err(f"built_for.{key} is empty")
    if "built_at_commit" not in (ctx.get("built_for") or {}):
        err("built_for.built_at_commit is absent (use null if unrecorded)")

    # ── budget (R1) ─────────────────────────────────────────────────────
    budget = ctx.get("budget") or {}
    max_entries = budget.get("max_guidance_entries")
    max_bytes = budget.get("max_serialized_bytes")
    max_principle = budget.get("max_principle_bytes")
    if not isinstance(max_entries, int) or max_entries < 1:
        err("budget.max_guidance_entries must be a positive integer")
        max_entries = None
    if not isinstance(max_bytes, int) or max_bytes < 1:
        err("budget.max_serialized_bytes must be a positive integer")
        max_bytes = None
    if not isinstance(max_principle, int) or max_principle < 1:
        err("budget.max_principle_bytes must be a positive integer")
        max_principle = None
    if not norm(budget.get("basis")):
        err("budget.basis is empty — a budget with no stated basis is a convention, not a constraint")

    guidance = ctx.get("key_guidance") or []
    questions = ctx.get("production_questions") or []
    trace = ctx.get("source_trace") or []

    if max_entries is not None and len(guidance) > max_entries:
        err(f"budget exceeded: {len(guidance)} guidance entries > max_guidance_entries {max_entries}")
    if max_bytes is not None and len(raw) > max_bytes:
        err(f"budget exceeded: {len(raw)} serialized bytes > max_serialized_bytes {max_bytes}")
    principle_bytes = sum(len(norm(g.get("principle")).encode("utf-8")) for g in guidance)
    if max_principle is not None and principle_bytes > max_principle:
        err(f"budget exceeded: {principle_bytes} principle bytes > "
            f"max_principle_bytes {max_principle}")
    if not guidance:
        err("key_guidance is empty")
    if not questions:
        err("production_questions is empty")
    if not ctx.get("do_not_overgeneralize"):
        err("do_not_overgeneralize is empty — R8 requires at least one stated limit")

    # ── source_trace (R4) ───────────────────────────────────────────────
    traced: dict[str, dict] = {}
    for entry in trace:
        ref = entry.get("ref")
        if not ref:
            err("source_trace entry has no ref")
            continue
        if ref in traced:
            err(f"source_trace lists {ref} more than once")
        traced[ref] = entry
        if ref not in objects:
            err(f"{ref}: not found in canon/knowledge/current — "
                "unknown id, or HOLD/candidate/Q&A material, which R4 forbids")
            continue
        kind, _ = objects[ref]
        if entry.get("kind") != kind:
            err(f"{ref}: source_trace says kind={entry.get('kind')!r}, corpus says {kind!r}")
        if entry.get("source_dir") != owner[ref]:
            err(f"{ref}: source_trace says source_dir={entry.get('source_dir')!r}, "
                f"corpus owner is {owner[ref]!r}")
        if entry.get("source_id") != source_of[ref]:
            err(f"{ref}: source_trace says source_id={entry.get('source_id')!r}, "
                f"extraction says {source_of[ref]!r}")
        if not norm(entry.get("locator")):
            err(f"{ref}: source_trace.locator is empty")
        actual = audited.get(owner[ref])
        if actual != "complete":
            err(f"{ref}: Audit Gate status for {owner[ref]} is {actual!r}, not 'complete' — "
                "unaudited material may not be consumed downstream")
        if entry.get("audit_status") != actual:
            err(f"{ref}: source_trace claims audit_status={entry.get('audit_status')!r}, "
                f"the record says {actual!r}")
        if (CANDIDATES / owner[ref]).exists():
            err(f"{ref}: {owner[ref]} also exists under canon/candidates/ — resolve the ambiguity")

    # ── key_guidance (R3, R5, R6) ───────────────────────────────────────
    seen_guidance: dict[str, dict] = {}
    for entry in guidance:
        gid = entry.get("guidance_id")
        if not gid or not re.fullmatch(r"KG-\d{2}", str(gid)):
            err(f"guidance_id {gid!r} does not match KG-NN")
            continue
        if gid in seen_guidance:
            err(f"{gid}: duplicate guidance_id")
        seen_guidance[gid] = entry

        for field in GUIDANCE_FIELDS:
            if not norm(entry.get(field)):
                err(f"{gid}: `{field}` is empty — all six guidance fields are mandatory")

        evidence = entry.get("evidence") or {}
        refs = evidence.get("refs") or []
        if not refs:
            err(f"{gid}: evidence.refs is empty")
        for ref in refs:
            if ref not in traced:
                err(f"{gid}: cites {ref}, which is not in source_trace (R3 — nothing dangling)")
            elif ref in objects and evidence.get("source_dir") != owner[ref]:
                err(f"{gid}: evidence.source_dir={evidence.get('source_dir')!r} "
                    f"but {ref} is owned by {owner[ref]!r}")
        if not evidence.get("characteristics"):
            err(f"{gid}: evidence.characteristics is empty")

        rendered = entry.get("rendered_from") or {}
        ref, field = rendered.get("ref"), rendered.get("field")
        mode = entry.get("render_mode")
        if mode not in ("verbatim_claim", "condensed"):
            err(f"{gid}: render_mode {mode!r} is not verbatim_claim or condensed")
        if not ref or not field:
            err(f"{gid}: rendered_from must name both a ref and a field")
        elif ref not in objects:
            err(f"{gid}: rendered_from.ref {ref} does not resolve in accepted Canon")
        else:
            if ref not in refs:
                err(f"{gid}: rendered_from.ref {ref} is not among evidence.refs")
            kind, obj = objects[ref]
            committed = field_text(kind, obj, field)
            if committed is None:
                err(f"{gid}: {ref} has no field `{field}`")
            elif mode == "verbatim_claim":
                if norm(entry.get("principle")) != norm(committed):
                    err(f"{gid}: principle is not verbatim {ref}.{field} — "
                        "R5 forbids improving on the source by hand")
            elif mode == "condensed":
                if entry.get("rendered_from", {}).get("condensed_review") != "human":
                    err(f"{gid}: condensed principles require rendered_from.condensed_review: human")
                declared = rendered.get("source_digest")
                actual = digest(committed)
                if declared != actual:
                    err(f"{gid}: rendered_from.source_digest {declared!r} does not match "
                        f"the committed {field} ({actual})")

    # ── question/guidance linkage (R2) ──────────────────────────────────
    answered: set[str] = set()
    seen_questions: set[str] = set()
    for question in questions:
        qid = question.get("question_id")
        if not qid or not re.fullmatch(r"PQ-\d{2}", str(qid)):
            err(f"question_id {qid!r} does not match PQ-NN")
            continue
        if qid in seen_questions:
            err(f"{qid}: duplicate question_id")
        seen_questions.add(qid)
        for field in ("question", "why_it_matters"):
            if not norm(question.get(field)):
                err(f"{qid}: `{field}` is empty")
        targets = question.get("answered_by") or []
        if not targets:
            err(f"{qid}: answered_by is empty — R2 forbids a question with no answer")
        for gid in targets:
            if gid not in seen_guidance:
                err(f"{qid}: answered_by names {gid}, which is not in key_guidance")
            else:
                answered.add(gid)
    for gid in seen_guidance:
        if gid not in answered:
            err(f"{gid}: answers no production question — R2 forbids guidance that earned no place")

    # ── conflicts (R7) ──────────────────────────────────────────────────
    seen_conflicts: set[str] = set()
    for conflict in ctx.get("conflicts") or []:
        cid = conflict.get("conflict_id")
        if not cid or not re.fullmatch(r"CF-\d{2}", str(cid)):
            err(f"conflict_id {cid!r} does not match CF-NN")
            continue
        if cid in seen_conflicts:
            err(f"{cid}: duplicate conflict_id")
        seen_conflicts.add(cid)
        between = conflict.get("between") or []
        if len(set(between)) < 2:
            err(f"{cid}: `between` needs at least two distinct refs")
        for ref in between:
            if ref not in traced:
                err(f"{cid}: names {ref}, which is not in source_trace")
        if not norm(conflict.get("nature")):
            err(f"{cid}: `nature` is empty")
        unresolved = conflict.get("unresolved")
        if not isinstance(unresolved, bool):
            err(f"{cid}: `unresolved` must be a boolean")
        elif unresolved and norm(conflict.get("resolution_rule")):
            err(f"{cid}: marked unresolved but also carries a resolution_rule")
        elif not unresolved and not norm(conflict.get("resolution_rule")):
            err(f"{cid}: needs a resolution_rule, or unresolved: true — "
                "R7 forbids silently dropping one side")

    # ── do_not_overgeneralize (R8) ──────────────────────────────────────
    for limit in ctx.get("do_not_overgeneralize") or []:
        gid = limit.get("guidance_id")
        if gid not in seen_guidance:
            err(f"do_not_overgeneralize names {gid!r}, which is not in key_guidance")
        for field in ("limit", "why"):
            if not norm(limit.get(field)):
                err(f"do_not_overgeneralize[{gid}]: `{field}` is empty")

    return errors


def main(argv: list[str]) -> int:
    paths = [pathlib.Path(a) for a in argv[1:]]
    if not paths:
        print(__doc__.strip().splitlines()[-1], file=sys.stderr)
        return 2

    corpus = load_corpus()
    print(f"accepted Canon: {len(corpus[1])} objects across "
          f"{len(set(corpus[1].values()))} live sources")

    failed = 0
    for path in paths:
        if not path.exists():
            print(f"FAIL {path} — no such file")
            failed += 1
            continue
        errors = validate(path, corpus)
        if errors:
            failed += 1
            print(f"FAIL {path}  ({len(errors)} error{'s' if len(errors) != 1 else ''})")
            for message in errors:
                print(f"  - {message}")
        else:
            ctx = yaml.safe_load(path.read_text())
            print(f"PASS {path}  "
                  f"({len(ctx['production_questions'])} questions, "
                  f"{len(ctx['key_guidance'])} guidance, "
                  f"{len(ctx['conflicts'])} conflicts, "
                  f"{len(ctx['source_trace'])} refs, "
                  f"{sum(len(norm(g['principle']).encode('utf-8')) for g in ctx['key_guidance'])}"
                  f"/{path.stat().st_size} principle/total bytes)")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
