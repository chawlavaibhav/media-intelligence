#!/usr/bin/env python3
"""Mechanical integration validator for the 16 accepted CANON-003 books.

Checks only constraints reproducible from committed artifacts and frozen SPEC-03/04/05.
It does not re-judge source meaning, visual interpretation, or extraction completeness.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

import yaml

ACCEPTED_BOOK_DIRS = [
    "grammar-of-the-shot-ch4",
    "ogilvy-ch2-advertising-that-sells",
    "light-science-magic-ch3",
    "albers-interaction-of-color",
    "vignelli-canon-intangibles",
    "samara-making-breaking-grid-ch1",
    "freeman-photographers-eye-graphic-guide",
    "alton-painting-with-light-ch2",
    "grammar-of-the-edit-ch3-5",
    "murch-blink-p1-25",
    "hopkins-scientific-advertising-ch1-7",
    "heath-made-to-stick-introduction",
    "sutherland-alchemy-introduction",
    "catmull-creativity-inc-ch5",
    "bayles-orland-art-and-fear",
    "miller-storybrand-sb7",
]

REQUIRED_FILES = {
    "PROVENANCE.md",
    "source-knowledge.yaml",
    "source-concept-systems.yaml",
    "ontology-mappings.yaml",
    "operational-bindings.yaml",
    "visual-evidence-ledger.yaml",
}

EVIDENCE_CHARACTERISTICS = {
    "explicitly_stated", "visually_demonstrated", "controlled_comparison", "argued",
    "practitioner_assertion", "anecdotal", "outcome_claimed", "empirical_within_source",
    "repeated_within_source", "mechanism_given", "mechanism_absent", "culturally_bounded",
    "historical_claim",
}
CLAIM_TYPES = {"explicit_source_claim", "source_interpretation"}
CAVEAT_ORIGINS = {"source_stated", "extractor_observed"}
SYSTEM_TYPES = {
    "trade_off_set", "priority_order", "sequence", "decision_framework", "causal_model",
    "interacting_set", "mutual_qualification",
}
STRUCTURAL_ORIGINS = {"source_stated", "extractor_inferred"}
WHOLE_SYSTEM_ORIGINS = {"source_explicit", "extractor_synthesis"}
INTRA_SOURCE_RELATIONS = {
    "qualifies", "qualified_by", "trades_off_with", "depends_on", "generalises", "specialises",
    "contradicts", "demonstrated_together_with", "member_of_system",
}
TERM_KINDS = {"problem", "remedy", "property", "entity"}
TERM_ORIGINS = {"source", "empirical", "customer", "product"}
ONTOLOGY_RELATIONS = {
    "maps_to", "broader_than", "narrower_than", "related_to", "potentially_equivalent_to",
    "distinct_from", "same_failure_family", "same_mechanism", "same_observed_effect", "uncertain",
}
CONCEPT_KINDS = {"source_specific_concept", "canonical_concept", "cross_source_concept"}
EXECUTABLE_BY = {
    "physical_production", "generative_respecification", "deterministic_composite", "human_edit",
    "unknown",
}
TARGET_TYPES = {"creative_ir", "evaluation", "production", "governance", "benchmark"}
GOVERNANCE_CONSUMERS = {
    "taxonomy_governance", "retrieval_governance", "conflict_resolution", "evidence_interpretation",
    "rule_application", "cross_source_synthesis",
}
OBSERVATION_UNITS = {"frame", "shot", "shot_pair", "sequence", "whole_asset", "asset_set_over_time"}
EVIDENCE_BASES = {"derived_from_source", "extractor_inference", "cross_source_supported", "empirically_supported"}
SOURCE_FORBIDDEN_KEYS = {
    "informs", "target_type", "target_path", "target_schema", "target_schema_version",
    "failure_ontology_refs", "repair_ontology_refs", "governance_consumer", "observation_unit",
    "binding_id",
}


def _load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ValueError(f"{path}: YAML parse failure: {exc}") from exc


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _nonempty(value: Any) -> bool:
    return value is not None and (not isinstance(value, (str, list, dict)) or bool(value))


def _walk_keys(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key)
            yield from _walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_keys(child)


def validate_book_dir(book_dir: Path) -> list[str]:
    errors: list[str] = []
    prefix = book_dir.name
    missing = [f for f in sorted(REQUIRED_FILES) if not (book_dir / f).is_file()]
    errors.extend(f"{prefix}: missing required file {f}" for f in missing)
    if missing:
        return errors

    docs: dict[str, Any] = {}
    for filename in sorted(REQUIRED_FILES - {"PROVENANCE.md"}):
        try:
            docs[filename] = _load_yaml(book_dir / filename) or {}
        except ValueError as exc:
            errors.append(str(exc))
    if len(docs) != len(REQUIRED_FILES) - 1:
        return errors

    sk_doc = docs["source-knowledge.yaml"]
    system_doc = docs["source-concept-systems.yaml"]
    ontology = docs["ontology-mappings.yaml"]
    binding_doc = docs["operational-bindings.yaml"]
    sks = _list(sk_doc.get("source_knowledge")) if isinstance(sk_doc, dict) else []
    systems = _list(system_doc.get("source_concept_systems")) if isinstance(system_doc, dict) else []
    terms = _list(ontology.get("terms")) if isinstance(ontology, dict) else []
    relationships = _list(ontology.get("relationships")) if isinstance(ontology, dict) else []
    concepts = _list(ontology.get("concepts")) if isinstance(ontology, dict) else []
    bindings = _list(binding_doc.get("operational_bindings")) if isinstance(binding_doc, dict) else []

    sk_ids = {x.get("sk_id") for x in sks if isinstance(x, dict) and x.get("sk_id")}
    scs_ids = {x.get("scs_id") for x in systems if isinstance(x, dict) and x.get("scs_id")}
    term_ids = {x.get("term_id") for x in terms if isinstance(x, dict) and x.get("term_id")}

    # SPEC-03 SourceKnowledge mechanical rules.
    for i, obj in enumerate(sks, 1):
        if not isinstance(obj, dict):
            errors.append(f"{prefix}: source_knowledge[{i}] is not a mapping")
            continue
        oid = obj.get("sk_id") or f"source_knowledge[{i}]"
        claim_type = obj.get("claim_type")
        if claim_type not in CLAIM_TYPES:
            errors.append(f"{prefix}:{oid}: invalid or missing claim_type {claim_type}")
        if claim_type == "source_interpretation" and not _nonempty(obj.get("interpretation_basis")):
            errors.append(f"{prefix}:{oid}: source_interpretation missing interpretation_basis")

        evidence = obj.get("evidence") if isinstance(obj.get("evidence"), dict) else {}
        chars = _list(evidence.get("characteristics"))
        if not chars:
            errors.append(f"{prefix}:{oid}: evidence.characteristics is empty")
        for value in chars:
            if value not in EVIDENCE_CHARACTERISTICS:
                errors.append(f"{prefix}:{oid}: invalid evidence characteristic {value}")

        prov = obj.get("provenance") if isinstance(obj.get("provenance"), dict) else {}
        if not any(_nonempty(prov.get(k)) for k in ("page_start", "page_end", "section", "chapter", "locator", "anchor")):
            errors.append(f"{prefix}:{oid}: provenance has no page range or equivalent locator")
        support = prov.get("source_support")
        if not support:
            errors.append(f"{prefix}:{oid}: provenance missing source_support")
        # Frozen SPEC-03 rule 4 requires an inspected figure for visual-only support. It does not
        # impose that requirement on text_and_visual; Lane A explicitly caught this earlier.
        inspected = prov.get("inspected") if isinstance(prov.get("inspected"), dict) else {}
        if support == "visual" and not _list(inspected.get("figures")):
            errors.append(f"{prefix}:{oid}: source_support visual but no inspected figures")

        mechanism = obj.get("mechanism") if isinstance(obj.get("mechanism"), dict) else {}
        if not isinstance(mechanism.get("stated_by_source"), bool):
            errors.append(f"{prefix}:{oid}: mechanism.stated_by_source missing or not boolean")
        for key in sorted(SOURCE_FORBIDDEN_KEYS.intersection(_walk_keys(obj))):
            errors.append(f"{prefix}:{oid}: product-layer key {key} appears in SourceKnowledge")
        for caveat in _list(obj.get("caveats")):
            if not isinstance(caveat, dict) or caveat.get("origin") not in CAVEAT_ORIGINS:
                errors.append(f"{prefix}:{oid}: caveat missing/invalid origin")
        for relation in _list(obj.get("intra_source_relations")):
            if not isinstance(relation, dict):
                errors.append(f"{prefix}:{oid}: intra_source_relation is not a mapping")
                continue
            rel, target = relation.get("relation"), relation.get("target")
            if rel not in INTRA_SOURCE_RELATIONS:
                errors.append(f"{prefix}:{oid}: invalid intra-source relation {rel}")
            if target and target not in sk_ids and target not in scs_ids:
                errors.append(f"{prefix}:{oid}: unresolved intra-source ref {target}")

    # SourceConceptSystems.
    for i, system in enumerate(systems, 1):
        if not isinstance(system, dict):
            errors.append(f"{prefix}: source_concept_systems[{i}] is not a mapping")
            continue
        sid = system.get("scs_id") or f"source_concept_systems[{i}]"
        if system.get("system_type") not in SYSTEM_TYPES:
            errors.append(f"{prefix}:{sid}: invalid system_type {system.get('system_type')}")
        if system.get("system_type_origin") not in STRUCTURAL_ORIGINS:
            errors.append(f"{prefix}:{sid}: invalid system_type_origin {system.get('system_type_origin')}")
        whole = system.get("whole_system_claim") if isinstance(system.get("whole_system_claim"), dict) else {}
        origin = whole.get("origin")
        if origin not in WHOLE_SYSTEM_ORIGINS:
            errors.append(f"{prefix}:{sid}: invalid whole_system_claim.origin {origin}")
        if origin == "extractor_synthesis" and not _nonempty(whole.get("interpretation_basis")):
            errors.append(f"{prefix}:{sid}: extractor_synthesis missing interpretation_basis")
        for member in _list(system.get("members")):
            if not isinstance(member, dict):
                errors.append(f"{prefix}:{sid}: system member is not a mapping")
                continue
            ref = member.get("sk_ref")
            if ref not in sk_ids:
                errors.append(f"{prefix}:{sid}: unresolved SourceKnowledge ref {ref}")
            if member.get("membership_origin") not in STRUCTURAL_ORIGINS:
                errors.append(f"{prefix}:{sid}: invalid membership_origin {member.get('membership_origin')}")
        structure = system.get("internal_structure") if isinstance(system.get("internal_structure"), dict) else {}
        ordering = structure.get("ordering") if isinstance(structure.get("ordering"), dict) else {}
        if ordering and ordering.get("origin") not in STRUCTURAL_ORIGINS:
            errors.append(f"{prefix}:{sid}: invalid ordering.origin {ordering.get('origin')}")
        for field in ("dependencies", "tradeoffs", "conflicts"):
            for rel in _list(structure.get(field)):
                if not isinstance(rel, dict):
                    continue
                if rel.get("origin") not in STRUCTURAL_ORIGINS:
                    errors.append(f"{prefix}:{sid}: {field} entry has invalid origin {rel.get('origin')}")
                refs = [rel.get("from"), rel.get("to")] if field == "dependencies" else _list(rel.get("between"))
                for ref in [x for x in refs if x]:
                    if ref not in sk_ids:
                        errors.append(f"{prefix}:{sid}: unresolved SourceKnowledge ref {ref} in {field}")

    # SPEC-05 ontology.
    for i, term in enumerate(terms, 1):
        if not isinstance(term, dict):
            errors.append(f"{prefix}: terms[{i}] is not a mapping")
            continue
        tid = term.get("term_id") or f"terms[{i}]"
        if term.get("kind") not in TERM_KINDS:
            errors.append(f"{prefix}:{tid}: invalid term kind {term.get('kind')}")
        if term.get("origin") not in TERM_ORIGINS:
            errors.append(f"{prefix}:{tid}: invalid term origin {term.get('origin')}")
        if term.get("kind") == "remedy":
            executors = _list(term.get("executable_by"))
            if not executors:
                errors.append(f"{prefix}:{tid}: remedy missing executable_by")
            for executor in executors:
                if executor not in EXECUTABLE_BY:
                    errors.append(f"{prefix}:{tid}: invalid executable_by {executor}")
        for ref in _list(term.get("arising_from")):
            if ref not in sk_ids:
                errors.append(f"{prefix}:{tid}: unresolved arising_from ref {ref}")

    for i, rel in enumerate(relationships, 1):
        if not isinstance(rel, dict):
            errors.append(f"{prefix}: relationships[{i}] is not a mapping")
            continue
        relation = rel.get("relation")
        if relation not in ONTOLOGY_RELATIONS:
            errors.append(f"{prefix}: invalid ontology relation {relation}")
        for endpoint in ("from", "to"):
            ref = rel.get(endpoint)
            if ref not in term_ids:
                errors.append(f"{prefix}: ontology relationship unresolved {endpoint} term {ref}")

    for i, concept in enumerate(concepts, 1):
        if not isinstance(concept, dict):
            errors.append(f"{prefix}: concepts[{i}] is not a mapping")
            continue
        cid = concept.get("concept_id") or f"concepts[{i}]"
        kind = concept.get("kind")
        if kind not in CONCEPT_KINDS:
            errors.append(f"{prefix}:{cid}: invalid concept kind {kind}")
        refs = list(_list(concept.get("children_terms")))
        for child in _list(concept.get("children")):
            if isinstance(child, dict):
                refs.extend(_list(child.get("terms")))
        for ref in refs:
            if ref not in term_ids:
                errors.append(f"{prefix}:{cid}: unresolved child term {ref}")
        if kind == "cross_source_concept" and len(set(_list(concept.get("independent_origins")))) < 2:
            errors.append(f"{prefix}:{cid}: cross_source_concept has fewer than two independent_origins")

    # SPEC-04 bindings.
    for i, binding in enumerate(bindings, 1):
        if not isinstance(binding, dict):
            errors.append(f"{prefix}: operational_bindings[{i}] is not a mapping")
            continue
        bid = binding.get("binding_id") or f"operational_bindings[{i}]"
        sk_refs, system_refs = _list(binding.get("source_knowledge_refs")), _list(binding.get("source_system_refs"))
        if not sk_refs and not system_refs:
            errors.append(f"{prefix}:{bid}: binding has no source refs")
        for ref in sk_refs:
            if ref not in sk_ids:
                errors.append(f"{prefix}:{bid}: unresolved SourceKnowledge ref {ref}")
        for ref in system_refs:
            if ref not in scs_ids:
                errors.append(f"{prefix}:{bid}: unresolved SourceConceptSystem ref {ref}")
        target = binding.get("target_type")
        if target not in TARGET_TYPES:
            errors.append(f"{prefix}:{bid}: invalid target_type {target}")
        if target == "creative_ir":
            for field in ("target_path", "target_schema", "target_schema_version"):
                if not _nonempty(binding.get(field)):
                    errors.append(f"{prefix}:{bid}: creative_ir binding missing {field}")
        if target == "governance" and binding.get("governance_consumer") not in GOVERNANCE_CONSUMERS:
            errors.append(f"{prefix}:{bid}: invalid governance_consumer {binding.get('governance_consumer')}")
        if target == "production" and binding.get("status") != "production_candidate":
            errors.append(f"{prefix}:{bid}: production binding status must be production_candidate")
        if target == "evaluation" and binding.get("observation_unit") not in OBSERVATION_UNITS:
            errors.append(f"{prefix}:{bid}: invalid/missing observation_unit {binding.get('observation_unit')}")
        if binding.get("evidence_basis") not in EVIDENCE_BASES:
            errors.append(f"{prefix}:{bid}: invalid/missing evidence_basis {binding.get('evidence_basis')}")
        for field in ("failure_ontology_refs", "repair_ontology_refs"):
            for ref in _list(binding.get(field)):
                if not isinstance(ref, str) or not ref or " " in ref:
                    errors.append(f"{prefix}:{bid}: {field} contains raw/non-identifier value {ref!r}")

    return errors


def _ids(book_dir: Path) -> dict[str, list[str]]:
    buckets = {"sk": [], "scs": [], "term": [], "concept": [], "binding": []}
    files = [
        ("source-knowledge.yaml", "source_knowledge", "sk_id", "sk"),
        ("source-concept-systems.yaml", "source_concept_systems", "scs_id", "scs"),
        ("ontology-mappings.yaml", "terms", "term_id", "term"),
        ("ontology-mappings.yaml", "concepts", "concept_id", "concept"),
        ("operational-bindings.yaml", "operational_bindings", "binding_id", "binding"),
    ]
    cache: dict[str, Any] = {}
    for filename, collection, field, bucket in files:
        if filename not in cache:
            cache[filename] = _load_yaml(book_dir / filename) or {}
        doc = cache[filename]
        for obj in _list(doc.get(collection)) if isinstance(doc, dict) else []:
            if isinstance(obj, dict) and obj.get(field):
                buckets[bucket].append(str(obj[field]))
    return buckets


def validate_repository(root: Path) -> dict[str, Any]:
    current = root / "canon" / "knowledge" / "current"
    errors: list[str] = []
    books: dict[str, Any] = {}
    seen = {k: {} for k in ("sk", "scs", "term", "concept", "binding")}
    totals = {"books": 0, "source_knowledge": 0, "systems": 0, "terms": 0, "concepts": 0, "bindings": 0}

    for name in ACCEPTED_BOOK_DIRS:
        book = current / name
        if not book.is_dir():
            errors.append(f"integration: accepted book directory missing: {name}")
            continue
        book_errors = validate_book_dir(book)
        errors.extend(book_errors)
        try:
            ids = _ids(book)
        except ValueError as exc:
            # Parse errors were already reported by validate_book_dir; don't crash the entire run.
            ids = {k: [] for k in seen}
        for kind, values in ids.items():
            for value in values:
                if value in seen[kind]:
                    errors.append(f"integration: duplicate {kind} id {value} in {seen[kind][value]} and {name}")
                else:
                    seen[kind][value] = name

        counts = {}
        for filename, collection, key in [
            ("source-knowledge.yaml", "source_knowledge", "source_knowledge"),
            ("source-concept-systems.yaml", "source_concept_systems", "systems"),
            ("ontology-mappings.yaml", "terms", "terms"),
            ("ontology-mappings.yaml", "concepts", "concepts"),
            ("operational-bindings.yaml", "operational_bindings", "bindings"),
        ]:
            try:
                doc = _load_yaml(book / filename) or {}
                counts[key] = len(_list(doc.get(collection))) if isinstance(doc, dict) else 0
            except ValueError:
                counts[key] = 0
        books[name] = {"errors": book_errors, "counts": counts}
        totals["books"] += 1
        for key, value in counts.items():
            totals[key] += value

    return {
        "accepted_book_dirs": ACCEPTED_BOOK_DIRS,
        "totals": totals,
        "error_count": len(errors),
        "errors": errors,
        "books": books,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--json-report", type=Path)
    args = parser.parse_args()
    report = validate_repository(args.root.resolve())
    text = json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True)
    if args.json_report:
        args.json_report.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 1 if report["error_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
