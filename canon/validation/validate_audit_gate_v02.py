#!/usr/bin/env python3
"""Mechanical validator for the adopted Audit Gate v0.2 records.

Authoritative method: canon/audit/AUDIT-GATE-v0.2.md
Active records:       canon/audit/records/*.audit.yaml
Adopted by:           canon/decisions/CANON-004-ADOPT-AUDIT-GATE-2026-08-25.md (applied by CANON-005)

The Audit Gate is a POST-EXTRACTION layer. This validator reads the frozen SPEC-03/04/05 artifacts
under canon/knowledge/current/ but never writes to them, and never re-judges source meaning.

It checks five things the adopted method claims:
  - the audit's references actually resolve into the frozen record;
  - the controlled vocabularies are respected;
  - no field acts as a credibility score;
  - two sources cannot count as independent origins when lineage says otherwise;
  - the audited source artifacts are still byte-identical to the ones on disk now.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable

import yaml

# The single active location. There is deliberately no second editable copy; the former
# experimental directory is a historical pointer only (CANON-005).
RECORDS_SUBPATH = Path("canon/audit/records")
RETIRED_RECORDS_SUBPATH = Path("canon/experiments/audit-gate-v0.2/records")
KNOWLEDGE_SUBPATH = Path("canon/knowledge/current")

# ── the source snapshot ─────────────────────────────────────────────────────────────────────
# An Audit Gate record describes a source representation at one moment. If that representation
# later changes, the audit is stale and must not keep validating - it is about to gate cross-source
# promotion and product use, so a stale pass is worse than no gate.
#
# The snapshot is the ONLY enforced version mechanism. `recorded_at_commit` is informational
# provenance and is deliberately not read by this validator; see canon/audit/AUDIT-GATE-v0.2.md.
#
# Membership rule: a file is in the snapshot when the audit's assertions are falsified by a change
# to it. Each of the five below is justified individually; PROVENANCE.md is excluded because it is
# narrative prose whose factual content is restated inside the audit's own fields.
SNAPSHOT_FILES = (
    # sk_refs resolve into it; evidence_origin is cross-checked against its
    # `empirical_within_source` characteristics; `source_id` must match it.
    "source-knowledge.yaml",
    # application_fit findings cite binding_ids from it, and a binding may carry source_system_refs.
    "operational-bindings.yaml",
    # bindings resolve system refs into it, and audit prose cites system-level fields such as
    # `source_warns_against_isolated_use` and `priority_order`.
    "source-concept-systems.yaml",
    # the layer whose cross_source_concept promotion the lineage audit governs; audit prose also
    # cites remedy `executable_by` values from it.
    "ontology-mappings.yaml",
    # representation_integrity is derived from it; nothing else would detect a change to Area A.
    "visual-evidence-ledger.yaml",
)
SNAPSHOT_ALGORITHM = "sha256-of-sorted-path-and-content"

# ── controlled vocabularies (see canon/audit/AUDIT-GATE-v0.2.md) ─────────────────────────────
# The one adopted Audit Gate version. There is deliberately no migration or version-negotiation
# machinery: exactly one authoritative contract exists, and a record declaring anything else -
# including the pre-adoption "v0.2-experimental" - is refused rather than tolerated.
AUDIT_RECORD_VERSION = "v0.2"

AUDIT_STATUS = {"complete", "evidence_insufficient"}

DELIVERY_FORMATS = {
    "authored_print_scan", "publisher_epub", "native_digital_pdf", "converted_pdf",
    "repository_text_extract", "unknown",
}
PAGE_ADDRESSABILITY = {
    "authored_pages", "no_pages_reflowable", "converter_pages_not_authored", "pages_unknown",
}
INSPECTION_STATES = {
    "inspected_page_level", "inspected_figure_level", "inspected_no_page_available",
    "inspected_but_required_dimension_destroyed", "not_inspected_access_blocked",
}
VISUAL_ARGUMENT_ROLES = {
    "no_visual_argument", "illustrative_only", "figure_carries_content",
    "page_layout_is_the_argument", "source_is_its_own_specimen",
}
LOSS_PATTERNS = {
    "no_authored_page", "false_page_affordance", "heading_carried_as_image", "in_figure_text_absent",
    "required_visual_dimension_destroyed", "figure_inspected_claim_underdetermined",
    "named_loss_with_unstated_content", "announced_loss_placeholder", "text_layer_order_damage",
    "demonstration_performs_the_claim", "caption_coverage_uneven", "source_evidence_never_printed",
    "display_type_ocr_damage", "no_loss_detected",
}
DETECTABILITY = {"silent", "named_by_text", "announced_by_placeholder", "detected_by_independent_check"}
RECOVERABILITY = {
    "recovered_in_this_copy", "recoverable_not_attempted", "unrecoverable_in_this_copy",
    "not_applicable",
}
CLAIM_RESOLUTION = {"all_resolved", "some_underdetermined", "not_applicable"}

ORIGIN_SCOPES = {"all_objects", "notable_objects_only", "evidence_insufficient"}
ORIGIN_CATEGORIES = {
    "source_own_measurement_reported", "measurement_claimed_result_not_supplied",
    "third_party_measurement_reported", "mixed_own_and_third_party", "source_author_assertion",
    "source_quotes_named_third_party", "source_quotes_unnamed_third_party", "origin_unresolved",
}
# Categories that assert the source supplied its OWN measured result.
ORIGIN_OWN_MEASUREMENT = {"source_own_measurement_reported"}
# Categories that assert the measurement was not the source's own, or had no result.
ORIGIN_NOT_OWN_MEASUREMENT = {
    "third_party_measurement_reported", "measurement_claimed_result_not_supplied",
}

APPLICATION_CONSUMERS = [
    "creative_ir", "production_ir", "evaluation", "governance", "benchmark",
    "deterministic_composition", "human_workflow",
]
APPLICATION_OUTCOMES = {
    "binding_exists", "candidate_no_binding_made", "no_current_binding",
    "blocked_target_schema_absent",
}

LINEAGE_RELATIONS = {
    "shared_author", "same_series", "companion_volume", "derivative_of", "cites_source",
    "shares_publisher_only", "no_known_relation",
}
# Relations that defeat independence for cross-source promotion.
DEPENDENT_RELATIONS = {"shared_author", "same_series", "companion_volume", "derivative_of"}
INDEPENDENCE_VERDICTS = {
    "independent_origin", "not_independent_of_named_sources", "independence_not_established",
}

CONTINGENCY_CLASSES = {
    "durable_mechanism", "technology_contingent", "historical_convention", "uncertain",
}

# ── the anti-score rule ─────────────────────────────────────────────────────────────────────
# The Audit Gate records WHAT KIND of thing something is, never HOW GOOD it is. A key whose name
# implies an ordering is refused outright, at any depth, so a credibility score cannot be smuggled
# in under a plausible name.
FORBIDDEN_KEY_PATTERN = re.compile(
    r"(score|rank|rating|grade|quality|strength|weight|tier|confidence|credibility)", re.IGNORECASE
)


def _load_yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - reported as a validation error, not raised
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


def _collect_sk_refs(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "sk_refs":
                found.extend(str(x) for x in _list(child))
            else:
                found.extend(_collect_sk_refs(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(_collect_sk_refs(child))
    return found


def _collect_binding_refs(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "existing_binding_refs":
                found.extend(str(x) for x in _list(child))
            else:
                found.extend(_collect_binding_refs(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(_collect_binding_refs(child))
    return found


def compute_source_snapshot(root: Path, knowledge_dir: str) -> dict[str, Any]:
    """Deterministic content fingerprint of the frozen source artifacts an audit describes.

    Read-only. Paths are relative to `knowledge_dir` and are hashed in lexicographic order, so the
    result depends only on file contents and never on filesystem order, clock or git state.

    Returns {"algorithm", "files": [{"path", "digest"}], "combined_digest", "missing": [path]}.
    A missing file is reported rather than skipped: silently omitting it would let a deleted
    artifact produce a snapshot that still matched.
    """
    book = root / knowledge_dir
    files: list[dict[str, str]] = []
    missing: list[str] = []
    for name in sorted(SNAPSHOT_FILES):
        path = book / name
        if not path.is_file():
            missing.append(name)
            continue
        files.append({"path": name, "digest": hashlib.sha256(path.read_bytes()).hexdigest()})
    canonical = "".join(f"{f['path']}:{f['digest']}\n" for f in files)
    return {
        "algorithm": SNAPSHOT_ALGORITHM,
        "files": files,
        "combined_digest": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
        "missing": missing,
    }


def _validate_snapshot(record: dict[str, Any], root: Path, rid: str, knowledge_dir: str) -> list[str]:
    """Prove the audited artifacts are still byte-identical to the ones on disk now."""
    errors: list[str] = []
    declared = record.get("source_snapshot")
    if not isinstance(declared, dict):
        return [
            f"{rid}: source_snapshot missing - an audit must record the exact source artifacts it "
            f"was written against, or it cannot be shown to be current"
        ]

    if declared.get("algorithm") != SNAPSHOT_ALGORITHM:
        errors.append(
            f"{rid}: source_snapshot.algorithm {declared.get('algorithm')!r} is not "
            f"{SNAPSHOT_ALGORITHM!r}"
        )

    actual = compute_source_snapshot(root, knowledge_dir)
    for name in actual["missing"]:
        errors.append(
            f"{rid}: snapshot artifact {name} is missing from {knowledge_dir}; the audited source "
            f"representation is incomplete"
        )

    declared_files = {
        str(entry.get("path")): str(entry.get("digest"))
        for entry in _list(declared.get("files"))
        if isinstance(entry, dict)
    }
    actual_files = {entry["path"]: entry["digest"] for entry in actual["files"]}

    for name in sorted(set(SNAPSHOT_FILES) - set(declared_files)):
        errors.append(f"{rid}: source_snapshot does not cover required artifact {name}")
    for name in sorted(set(declared_files) - set(SNAPSHOT_FILES)):
        errors.append(f"{rid}: source_snapshot covers unexpected artifact {name}")

    for name in sorted(set(declared_files) & set(actual_files)):
        if declared_files[name] != actual_files[name]:
            errors.append(
                f"{rid}: STALE AUDIT - {name} has changed since this audit was written "
                f"(audited {declared_files[name][:12]}, now {actual_files[name][:12]}); "
                f"re-run the Audit Gate for this source"
            )

    if not errors and declared.get("combined_digest") != actual["combined_digest"]:
        errors.append(
            f"{rid}: source_snapshot.combined_digest does not match the recomputed digest; "
            f"the snapshot is internally inconsistent"
        )
    return errors


def _frozen_record(root: Path, knowledge_dir: str) -> dict[str, Any]:
    """Read the frozen SPEC-03/04 artifacts an audit record points at. Read-only."""
    book = root / knowledge_dir
    sk_doc = _load_yaml(book / "source-knowledge.yaml") or {}
    bind_doc = _load_yaml(book / "operational-bindings.yaml") or {}
    objects = _list(sk_doc.get("source_knowledge"))
    empirical = {
        obj.get("sk_id")
        for obj in objects
        if isinstance(obj, dict)
        and "empirical_within_source"
        in _list((obj.get("evidence") or {}).get("characteristics") if isinstance(obj.get("evidence"), dict) else [])
    }
    return {
        "source_id": sk_doc.get("source_id"),
        "sk_ids": {obj.get("sk_id") for obj in objects if isinstance(obj, dict)},
        "binding_ids": {
            b.get("binding_id") for b in _list(bind_doc.get("operational_bindings")) if isinstance(b, dict)
        },
        "empirical_within_source": empirical,
    }


def validate_record(record: dict[str, Any], root: Path) -> list[str]:
    errors: list[str] = []
    rid = record.get("audit_id") or "<no audit_id>"

    for field in ("audit_record_version", "audit_id", "source_id", "knowledge_dir", "audit_status"):
        if not _nonempty(record.get(field)):
            errors.append(f"{rid}: missing required field {field}")

    # Fail closed on any version other than the single adopted one.
    version = record.get("audit_record_version")
    if _nonempty(version) and version != AUDIT_RECORD_VERSION:
        errors.append(
            f"{rid}: unsupported audit_record_version {version!r}; the only authoritative Audit "
            f"Gate record version is {AUDIT_RECORD_VERSION!r}"
        )

    status = record.get("audit_status")
    if status not in AUDIT_STATUS:
        errors.append(f"{rid}: invalid audit_status {status}")
    if status == "evidence_insufficient" and not _nonempty(record.get("evidence_insufficient_reason")):
        errors.append(f"{rid}: evidence_insufficient requires evidence_insufficient_reason")

    # Anti-score rule.
    for key in sorted({k for k in _walk_keys(record) if FORBIDDEN_KEY_PATTERN.search(k)}):
        errors.append(f"{rid}: forbidden score-like key {key!r} (Audit Gate records kind, not quality)")

    knowledge_dir = record.get("knowledge_dir")
    frozen: dict[str, Any] | None = None
    if knowledge_dir:
        book = root / str(knowledge_dir)
        if not book.is_dir():
            errors.append(f"{rid}: knowledge_dir does not exist: {knowledge_dir}")
        else:
            errors.extend(_validate_snapshot(record, root, rid, str(knowledge_dir)))
            try:
                frozen = _frozen_record(root, str(knowledge_dir))
            except ValueError as exc:
                errors.append(f"{rid}: {exc}")

    if frozen is not None:
        if record.get("source_id") != frozen["source_id"]:
            errors.append(
                f"{rid}: source_id {record.get('source_id')!r} does not match frozen record "
                f"{frozen['source_id']!r}"
            )
        for ref in _collect_sk_refs(record):
            if ref not in frozen["sk_ids"]:
                errors.append(f"{rid}: unresolved sk_ref {ref}")
        for ref in _collect_binding_refs(record):
            if ref not in frozen["binding_ids"]:
                errors.append(f"{rid}: unresolved binding ref {ref}")

    errors.extend(_validate_representation(record, rid))
    errors.extend(_validate_evidence_origin(record, rid, frozen))
    errors.extend(_validate_application_fit(record, rid))
    errors.extend(_validate_lineage(record, rid))
    errors.extend(_validate_contingency(record, rid))
    return errors


def _validate_representation(record: dict[str, Any], rid: str) -> list[str]:
    errors: list[str] = []
    rep = record.get("representation_integrity")
    if not isinstance(rep, dict):
        return [f"{rid}: representation_integrity missing"]

    checks = [
        ("delivery_format", DELIVERY_FORMATS),
        ("page_addressability", PAGE_ADDRESSABILITY),
        ("inspection_state", INSPECTION_STATES),
        ("visual_argument_role", VISUAL_ARGUMENT_ROLES),
    ]
    for field, allowed in checks:
        if rep.get(field) not in allowed:
            errors.append(f"{rid}: invalid/missing representation_integrity.{field} {rep.get(field)!r}")

    resolution = rep.get("claim_resolution_after_inspection")
    if resolution is not None and resolution not in CLAIM_RESOLUTION:
        errors.append(f"{rid}: invalid claim_resolution_after_inspection {resolution!r}")

    patterns = _list(rep.get("observed_loss_patterns"))
    if not patterns:
        errors.append(f"{rid}: observed_loss_patterns is empty (use no_loss_detected instead)")
    for entry in patterns:
        if not isinstance(entry, dict):
            errors.append(f"{rid}: observed_loss_patterns entry is not a mapping")
            continue
        if entry.get("pattern") not in LOSS_PATTERNS:
            errors.append(f"{rid}: invalid loss pattern {entry.get('pattern')!r}")
        if entry.get("detectability") not in DETECTABILITY:
            errors.append(f"{rid}: invalid/missing detectability {entry.get('detectability')!r}")
        if entry.get("recoverability") not in RECOVERABILITY:
            errors.append(f"{rid}: invalid/missing recoverability {entry.get('recoverability')!r}")
        if not _nonempty(entry.get("evidence")):
            errors.append(f"{rid}: loss pattern {entry.get('pattern')!r} has no evidence")
    return errors


def _validate_evidence_origin(
    record: dict[str, Any], rid: str, frozen: dict[str, Any] | None
) -> list[str]:
    errors: list[str] = []
    origin = record.get("evidence_origin")
    if not isinstance(origin, dict):
        return [f"{rid}: evidence_origin missing"]

    if origin.get("audit_scope") not in ORIGIN_SCOPES:
        errors.append(f"{rid}: invalid/missing evidence_origin.audit_scope {origin.get('audit_scope')!r}")

    seen: set[str] = set()
    for entry in _list(origin.get("categories")):
        if not isinstance(entry, dict):
            errors.append(f"{rid}: evidence_origin category entry is not a mapping")
            continue
        category = entry.get("category")
        if category not in ORIGIN_CATEGORIES:
            errors.append(f"{rid}: invalid evidence origin category {category!r}")
            continue
        if category in seen:
            errors.append(f"{rid}: duplicate evidence origin category {category}")
        seen.add(category)
        if not _nonempty(entry.get("evidence")):
            errors.append(f"{rid}: evidence origin category {category} has no evidence")

        if frozen is None:
            continue
        refs = [str(x) for x in _list(entry.get("sk_refs"))]
        # Consistency with the frozen SPEC-03 characteristic. The audit never edits it.
        if category in ORIGIN_OWN_MEASUREMENT:
            for ref in refs:
                if ref in frozen["sk_ids"] and ref not in frozen["empirical_within_source"]:
                    errors.append(
                        f"{rid}: {ref} claimed as the source's own reported measurement but the frozen "
                        f"record does not carry empirical_within_source"
                    )
        elif category in ORIGIN_NOT_OWN_MEASUREMENT:
            for ref in refs:
                if ref in frozen["empirical_within_source"]:
                    errors.append(
                        f"{rid}: {ref} categorised as {category} but the frozen record carries "
                        f"empirical_within_source"
                    )
    return errors


def _validate_application_fit(record: dict[str, Any], rid: str) -> list[str]:
    errors: list[str] = []
    fit = record.get("application_fit")
    if not isinstance(fit, dict):
        return [f"{rid}: application_fit missing"]

    audited = fit.get("audited")
    if not isinstance(audited, bool):
        errors.append(f"{rid}: application_fit.audited must be a boolean")
        return errors

    findings = _list(fit.get("findings"))
    if not audited:
        # "not audited" is structurally distinct from "audited, and nothing binds".
        if not _nonempty(fit.get("not_audited_reason")):
            errors.append(f"{rid}: application_fit.audited false requires not_audited_reason")
        if findings:
            errors.append(f"{rid}: application_fit.audited false must not carry findings")
        return errors

    seen: list[str] = []
    for entry in findings:
        if not isinstance(entry, dict):
            errors.append(f"{rid}: application_fit finding is not a mapping")
            continue
        consumer = entry.get("consumer")
        if consumer not in APPLICATION_CONSUMERS:
            errors.append(f"{rid}: invalid application consumer {consumer!r}")
            continue
        seen.append(consumer)
        if entry.get("outcome") not in APPLICATION_OUTCOMES:
            errors.append(f"{rid}: invalid/missing application outcome for {consumer}: {entry.get('outcome')!r}")
        if entry.get("outcome") == "binding_exists" and not _list(entry.get("existing_binding_refs")):
            errors.append(f"{rid}: {consumer} outcome binding_exists with no existing_binding_refs")

    missing = [c for c in APPLICATION_CONSUMERS if c not in seen]
    if missing:
        errors.append(f"{rid}: application_fit does not cover consumers: {', '.join(missing)}")
    duplicated = sorted({c for c in seen if seen.count(c) > 1})
    if duplicated:
        errors.append(f"{rid}: application_fit covers consumers more than once: {', '.join(duplicated)}")
    return errors


def _validate_lineage(record: dict[str, Any], rid: str) -> list[str]:
    errors: list[str] = []
    lineage = record.get("lineage")
    if not isinstance(lineage, dict):
        return [f"{rid}: lineage missing"]

    if not _list(lineage.get("authors")):
        errors.append(f"{rid}: lineage.authors is empty")
    if lineage.get("independence_verdict") not in INDEPENDENCE_VERDICTS:
        errors.append(f"{rid}: invalid/missing independence_verdict {lineage.get('independence_verdict')!r}")
    if not _nonempty(lineage.get("independence_basis")):
        errors.append(f"{rid}: lineage.independence_basis is empty")

    for entry in _list(lineage.get("related_sources_in_corpus")):
        if not isinstance(entry, dict):
            errors.append(f"{rid}: related_sources_in_corpus entry is not a mapping")
            continue
        if entry.get("relation") not in LINEAGE_RELATIONS:
            errors.append(f"{rid}: invalid lineage relation {entry.get('relation')!r}")
        if not _nonempty(entry.get("source_id")):
            errors.append(f"{rid}: related source entry has no source_id")
        if not _nonempty(entry.get("evidence")):
            errors.append(f"{rid}: related source {entry.get('source_id')!r} has no evidence")

    exposure = lineage.get("extractor_exposure")
    if not isinstance(exposure, dict):
        errors.append(f"{rid}: lineage.extractor_exposure missing")
    elif exposure.get("spec_contains_examples_from_this_source") not in (True, False, "unknown"):
        errors.append(
            f"{rid}: spec_contains_examples_from_this_source must be true, false or 'unknown'"
        )
    return errors


def _validate_contingency(record: dict[str, Any], rid: str) -> list[str]:
    errors: list[str] = []
    tech = record.get("technology_contingency")
    if not isinstance(tech, dict):
        return [f"{rid}: technology_contingency missing"]

    applicable = tech.get("applicable")
    if not isinstance(applicable, bool):
        errors.append(f"{rid}: technology_contingency.applicable must be a boolean")
        return errors
    if not _nonempty(tech.get("applicability_basis")):
        errors.append(f"{rid}: technology_contingency.applicability_basis is empty")

    assessed = tech.get("assessed")
    classes = _list(tech.get("classes"))
    if applicable and assessed is not True:
        errors.append(f"{rid}: technology_contingency applicable but not assessed")
    if applicable and assessed is True and not classes:
        errors.append(f"{rid}: technology_contingency assessed with no classes recorded")
    for entry in classes:
        if not isinstance(entry, dict):
            errors.append(f"{rid}: technology_contingency class entry is not a mapping")
            continue
        if entry.get("class") not in CONTINGENCY_CLASSES:
            errors.append(f"{rid}: invalid technology contingency class {entry.get('class')!r}")
        if not _nonempty(entry.get("evidence")):
            errors.append(f"{rid}: technology contingency class {entry.get('class')!r} has no evidence")
    return errors


# ── cross-record checks ─────────────────────────────────────────────────────────────────────

def _lineage_map(records: dict[str, dict[str, Any]]) -> dict[str, dict[str, str]]:
    """source_id -> {other_source_id: relation}."""
    out: dict[str, dict[str, str]] = {}
    for record in records.values():
        sid = record.get("source_id")
        if not sid:
            continue
        lineage = record.get("lineage") if isinstance(record.get("lineage"), dict) else {}
        out[sid] = {
            str(e.get("source_id")): str(e.get("relation"))
            for e in _list(lineage.get("related_sources_in_corpus"))
            if isinstance(e, dict) and e.get("source_id")
        }
    return out


def independent_origins_ok(
    source_a: str, source_b: str, records: dict[str, dict[str, Any]]
) -> tuple[bool, str]:
    """The promotion rule.

    Two sources count as independent origins for a SPEC-05 cross_source_concept only when neither
    audit record declares the other with a dependence-creating relation, and neither carries an
    unresolved or negative independence verdict. Returns (ok, reason).
    """
    by_source = {r.get("source_id"): r for r in records.values() if r.get("source_id")}
    if source_a == source_b:
        return False, "the same source cannot be two independent origins"
    for sid in (source_a, source_b):
        if sid not in by_source:
            return False, f"no audit record for {sid}; independence not established"

    relations = _lineage_map(records)
    for first, second in ((source_a, source_b), (source_b, source_a)):
        relation = relations.get(first, {}).get(second)
        if relation in DEPENDENT_RELATIONS:
            return False, f"{first} declares {relation} with {second}"

    # The source-level verdict is deliberately NOT consulted for `not_independent_of_named_sources`.
    # Independence is a property of a PAIR, not of a source: Grammar of the Shot is not an
    # independent origin against its companion volume and is a perfectly good one against every
    # other source in the corpus. Only a genuinely unresolved lineage blocks globally.
    for sid in (source_a, source_b):
        lineage = by_source[sid].get("lineage") or {}
        verdict = lineage.get("independence_verdict")
        # Fail closed on a verdict outside the controlled vocabulary. Passing an unrecognised value
        # through would let a malformed record silently qualify for promotion.
        if verdict not in INDEPENDENCE_VERDICTS:
            return False, f"{sid} carries an unrecognised independence_verdict {verdict!r}"
        if verdict == "independence_not_established":
            return False, f"{sid} carries independence_verdict independence_not_established"
    return True, "no dependence-creating relation declared by either source"


def validate_record_set(records: dict[str, dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    seen_audit: dict[str, str] = {}
    seen_source: dict[str, str] = {}
    for name, record in sorted(records.items()):
        for field, seen in (("audit_id", seen_audit), ("source_id", seen_source)):
            value = record.get(field)
            if not value:
                continue
            if value in seen:
                errors.append(f"record set: duplicate {field} {value} in {seen[value]} and {name}")
            else:
                seen[value] = name

    relations = _lineage_map(records)
    for source, targets in relations.items():
        for other, relation in targets.items():
            if other not in relations:
                errors.append(f"record set: {source} names unknown related source {other}")
                continue
            # Symmetry is required only for relations that DEFEAT independence. A dependence must
            # never be declarable from one side alone, because a promotion check reading only the
            # other record would miss it. Relations that do not defeat independence are left
            # asymmetric on purpose: shares_publisher_only is uninformative to mirror, and
            # cites_source is genuinely one-directional. Requiring symmetry for those was tested
            # against the 16-book corpus and produced only reciprocal bookkeeping.
            if relation not in DEPENDENT_RELATIONS:
                continue
            back = relations[other].get(source)
            if back not in DEPENDENT_RELATIONS:
                errors.append(
                    f"record set: {source} declares {relation} with {other} but {other} declares "
                    f"{back if back else 'nothing'} back; a dependence must be declared from both sides"
                )
    return errors


def validate_repository(root: Path) -> dict[str, Any]:
    records_dir = root / RECORDS_SUBPATH
    knowledge_root = root / KNOWLEDGE_SUBPATH
    errors: list[str] = []
    records: dict[str, dict[str, Any]] = {}

    if not records_dir.is_dir():
        return {"error_count": 1, "errors": [f"records directory missing: {RECORDS_SUBPATH}"], "records": {}}

    for path in sorted(records_dir.glob("*.audit.yaml")):
        try:
            doc = _load_yaml(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not isinstance(doc, dict):
            errors.append(f"{path.name}: record is not a mapping")
            continue
        records[path.name] = doc
        errors.extend(validate_record(doc, root))

    errors.extend(validate_record_set(records))

    covered = {r.get("knowledge_dir") for r in records.values()}
    if knowledge_root.is_dir():
        for book in sorted(p for p in knowledge_root.iterdir() if p.is_dir()):
            rel = str(KNOWLEDGE_SUBPATH / book.name)
            if rel not in covered:
                errors.append(f"coverage: no audit record for accepted book {book.name}")

    # Exactly one active copy. A duplicate under the retired experimental path would let the two
    # drift and leave downstream tooling without an unambiguous source of truth.
    retired = root / RETIRED_RECORDS_SUBPATH
    if retired.is_dir():
        duplicates = sorted(p.name for p in retired.glob("*.audit.yaml"))
        if duplicates:
            errors.append(
                f"duplicate active records: {len(duplicates)} audit record(s) still present under "
                f"{RETIRED_RECORDS_SUBPATH}; the only active location is {RECORDS_SUBPATH}"
            )

    return {
        "records_path": str(RECORDS_SUBPATH),
        "record_count": len(records),
        "records": sorted(records),
        "error_count": len(errors),
        "errors": errors,
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
