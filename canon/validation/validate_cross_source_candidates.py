#!/usr/bin/env python3
"""Validate the REP-02 cross-source join candidate ledger.

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

Enforces, mechanically, the rules the REP-02 ledger and the CANON-00X cross-source-layer
addendum proposal write down:

  E_SCHEMA            ledger/record shape is wrong (missing field, wrong type)
  E_STATUS            a row's status is not `proposed`
  E_RELATION_ENUM     a relation outside the closed 12-value enum
  E_CONFIDENCE        confidence grade outside {high, medium, low}
  E_USABLE            usable flag outside {accepted_only, involves_hold, false}
  E_UNRESOLVED_ID     a referenced id resolves neither in canon/knowledge/current
                      nor under canon/candidates/
  E_HOLD_ID_ON_ACCEPTED_ROW
                      an id resolving only under canon/candidates/ appears on a row whose
                      usable flag is accepted_only
  E_UNKNOWN_SOURCE_DIR an independence entry names a directory with no audit record
  E_INDEPENDENCE_MISMATCH
                      a quoted audit_relation does not match the verdict recomputed from
                      canon/audit/records/*.audit.yaml lineage.related_sources_in_corpus
                      (absent entries must be quoted as the sentinel
                      no_entry_in_either_audit_record)
  E_AGREEMENT_WITHOUT_INDEPENDENT_ORIGINS
                      a row asserting agreement/equivalence (maps_to, same_mechanism,
                      same_observed_effect, same_failure_family) has fewer than two
                      pairwise-independent origins under the audit records
  E_ORIGIN_COUNT      a declared independent_origins value differs from the recomputed
                      maximum pairwise-independent subset size
  E_FRAME_NOTE        an in_tension_with row lacks a frame_note
  E_MEMBERS           a row that must have members (all kinds except anchor_gap and
                      hold_blocked_observation) has fewer than two
  E_DUPLICATE_ADJUDICATION
                      the set of adjudicates_duplicate_term rows does not match, one-to-one,
                      the recomputed set of term strings duplicated across source directories
  E_IMPORT_MISSING / E_IMPORT_USABLE
                      a (from, relation, to) triple of
                      canon/candidates/canon-014/CROSS-SOURCE-RELATIONSHIPS.yaml is absent,
                      duplicated, or present without usable: involves_hold

The ledger-completeness checks (E_DUPLICATE_ADJUDICATION, E_IMPORT_*) run only when the ledger
header says `ledger_complete: true`; fixtures set it false so each can pin one refusal.

Usage: python3 canon/validation/validate_cross_source_candidates.py [ledger.yaml]
Exit 0 iff no errors.
"""
from __future__ import annotations

import sys
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
CURRENT = REPO_ROOT / "canon/knowledge/current"
CANDIDATES = REPO_ROOT / "canon/candidates"
AUDIT_RECORDS = REPO_ROOT / "canon/audit/records"
DEFAULT_LEDGER = REPO_ROOT / "canon/candidates/ontology-join/cross-source-candidates-v0.yaml"
CANON014_CROSSREF = REPO_ROOT / "canon/candidates/canon-014/CROSS-SOURCE-RELATIONSHIPS.yaml"

# The closed enum proposed by PROPOSED-METHOD-CHANGE-CANON-00X-CROSS-SOURCE-LAYER.md §2.2:
# SPEC-05's ten Layer-2 relations plus the two proposed cross-source additions.
RELATION_ENUM = {
    "maps_to", "broader_than", "narrower_than", "related_to", "potentially_equivalent_to",
    "distinct_from", "same_failure_family", "same_mechanism", "same_observed_effect",
    "uncertain", "contradicts_across_sources", "in_tension_with",
}
# Relations that assert agreement/equivalence and therefore require >= 2 independent origins
# (SPEC-05 Governance rule 5). potentially_equivalent_to is deliberately excluded: it is not
# identity and is the relation dependent pairs are recorded under.
AGREEMENT_RELATIONS = {"maps_to", "same_failure_family", "same_mechanism", "same_observed_effect"}

CONFIDENCE_GRADES = {"high", "medium", "low"}
USABLE_VALUES = {"accepted_only", "involves_hold", False}
KINDS = {
    "convergence", "tension", "negative", "dependent_pair", "canonical_concept_proposal",
    "retrieval_merge_proposal", "metadata_quarantine", "anchor_gap",
    "hold_blocked_observation", "imported_observation",
}
MEMBERLESS_KINDS = {"anchor_gap", "hold_blocked_observation"}

# Mirrors canon/validation/validate_audit_gate_v02.py — kept literal here so this validator has
# no import-time dependency on that module's CLI plumbing.
DEPENDENT_RELATIONS = {
    "shared_author", "same_series", "companion_volume", "derivative_of",
    "shared_primary_informant",
}
NO_ENTRY = "no_entry_in_either_audit_record"


# ── corpus and audit loading ─────────────────────────────────────────────────────────────────

def _load_ontology_ids(directory: Path) -> set[str]:
    ids: set[str] = set()
    om = directory / "ontology-mappings.yaml"
    if om.is_file():
        data = yaml.safe_load(om.read_text()) or {}
        for term in data.get("terms") or []:
            if isinstance(term, dict) and term.get("term_id"):
                ids.add(term["term_id"])
        for concept in data.get("concepts") or []:
            if isinstance(concept, dict) and concept.get("concept_id"):
                ids.add(concept["concept_id"])
    sk = directory / "source-knowledge.yaml"
    if sk.is_file():
        data = yaml.safe_load(sk.read_text()) or {}
        for obj in data.get("source_knowledge") or []:
            if isinstance(obj, dict) and obj.get("sk_id"):
                ids.add(obj["sk_id"])
    scs = directory / "source-concept-systems.yaml"
    if scs.is_file():
        data = yaml.safe_load(scs.read_text()) or {}
        for system in data.get("systems") or []:
            if isinstance(system, dict) and system.get("system_id"):
                ids.add(system["system_id"])
    return ids


@lru_cache(maxsize=1)
def load_current_index() -> dict[str, str]:
    """id -> source directory name, over canon/knowledge/current."""
    index: dict[str, str] = {}
    for directory in sorted(CURRENT.iterdir()):
        if directory.is_dir():
            for i in _load_ontology_ids(directory):
                index[i] = directory.name
    return index


@lru_cache(maxsize=1)
def load_candidate_ids() -> frozenset[str]:
    """All ids declared anywhere under canon/candidates/ (the HOLD lane)."""
    ids: set[str] = set()
    for om in CANDIDATES.rglob("ontology-mappings.yaml"):
        ids |= _load_ontology_ids(om.parent)
    return frozenset(ids)


@lru_cache(maxsize=1)
def load_audit() -> tuple[dict[str, dict], dict[str, str]]:
    """(dir -> audit record, source_id -> dir)."""
    records: dict[str, dict] = {}
    sid_to_dir: dict[str, str] = {}
    for path in sorted(AUDIT_RECORDS.glob("*.audit.yaml")):
        record = yaml.safe_load(path.read_text()) or {}
        dirname = path.name[: -len(".audit.yaml")]
        records[dirname] = record
        if record.get("source_id"):
            sid_to_dir[record["source_id"]] = dirname
    return records, sid_to_dir


def recorded_pair_relation(a: str, b: str, records: dict[str, dict]) -> str | None:
    """The relation recorded for the (a, b) directory pair, looked up in BOTH audit records'
    lineage.related_sources_in_corpus. None when neither record carries an entry."""
    found: list[str] = []
    for first, second in ((a, b), (b, a)):
        record = records.get(first) or {}
        lineage = record.get("lineage") if isinstance(record.get("lineage"), dict) else {}
        other_sid = (records.get(second) or {}).get("source_id")
        for entry in lineage.get("related_sources_in_corpus") or []:
            if isinstance(entry, dict) and entry.get("source_id") == other_sid:
                found.append(entry.get("relation"))
    if not found:
        return None
    # Reciprocal entries in this corpus always agree; fail loudly if they ever stop agreeing.
    if len(set(found)) > 1:
        return f"CONFLICTING_ENTRIES:{sorted(set(found))}"
    return found[0]


def pair_is_independent(a: str, b: str, records: dict[str, dict]) -> bool:
    """Mirrors independent_origins_ok() in validate_audit_gate_v02.py, keyed by directory."""
    if a == b:
        return False
    if a not in records or b not in records:
        return False
    relation = recorded_pair_relation(a, b, records)
    if relation in DEPENDENT_RELATIONS:
        return False
    for dirname in (a, b):
        lineage = (records[dirname].get("lineage") or {})
        if lineage.get("independence_verdict") == "independence_not_established":
            return False
    return True


def max_independent_subset(dirs: set[str], records: dict[str, dict]) -> int:
    """Size of the largest subset of dirs that is pairwise independent. Exhaustive; member
    source sets are tiny (<= 5)."""
    dirs = sorted(dirs)
    best = 0
    for size in range(len(dirs), 0, -1):
        for subset in combinations(dirs, size):
            if all(pair_is_independent(x, y, records) for x, y in combinations(subset, 2)):
                return size
    return best


# ── validation ───────────────────────────────────────────────────────────────────────────────

@lru_cache(maxsize=1)
def duplicate_term_strings() -> frozenset[str]:
    """Term strings that appear in more than one canon/knowledge/current source directory."""
    by_string: dict[str, set[str]] = defaultdict(set)
    for directory in sorted(CURRENT.iterdir()):
        om = directory / "ontology-mappings.yaml"
        if not om.is_file():
            continue
        data = yaml.safe_load(om.read_text()) or {}
        for term in data.get("terms") or []:
            if isinstance(term, dict) and term.get("term"):
                by_string[term["term"]].add(directory.name)
    return frozenset(s for s, dirs in by_string.items() if len(dirs) > 1)


def validate(ledger: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    current_index = load_current_index()
    candidate_ids = load_candidate_ids()
    audit_records, _sid_to_dir = load_audit()

    if not isinstance(ledger, dict):
        return ["E_SCHEMA: ledger is not a mapping"]
    records = ledger.get("records")
    if not isinstance(records, list) or not records:
        return ["E_SCHEMA: ledger.records is missing or empty"]
    if ledger.get("status") != "proposed":
        errors.append("E_STATUS: ledger header status must be `proposed`")

    seen_record_ids: Counter = Counter()
    adjudications: dict[str, list[str]] = defaultdict(list)
    imported_triples: Counter = Counter()
    imported_usable_ok: dict[tuple, bool] = {}

    for row in records:
        if not isinstance(row, dict):
            errors.append("E_SCHEMA: record is not a mapping")
            continue
        rid = row.get("record_id") or "<no record_id>"
        seen_record_ids[rid] += 1

        kind = row.get("kind")
        if kind not in KINDS:
            errors.append(f"E_SCHEMA: {rid}: unknown kind {kind!r}")
        if row.get("status") != "proposed":
            errors.append(f"E_STATUS: {rid}: status must be `proposed`, got {row.get('status')!r}")
        relation = row.get("relation")
        if relation not in RELATION_ENUM:
            errors.append(f"E_RELATION_ENUM: {rid}: relation {relation!r} is outside the closed enum")
        if row.get("confidence") not in CONFIDENCE_GRADES:
            errors.append(f"E_CONFIDENCE: {rid}: confidence {row.get('confidence')!r} is not high|medium|low")
        usable = row.get("usable", "<absent>")
        if usable not in USABLE_VALUES:
            errors.append(f"E_USABLE: {rid}: usable {usable!r} is not accepted_only|involves_hold|false")
        if relation == "in_tension_with" and not str(row.get("frame_note") or "").strip():
            errors.append(f"E_FRAME_NOTE: {rid}: in_tension_with requires a frame_note")

        members = row.get("members")
        if members is None:
            members = []
        if not isinstance(members, list):
            errors.append(f"E_SCHEMA: {rid}: members is not a list")
            members = []
        if kind not in MEMBERLESS_KINDS and len(members) < 2:
            errors.append(f"E_MEMBERS: {rid}: kind {kind!r} requires at least two members")

        # id resolution over members + supporting_ids
        row_ids = [m.get("id") for m in members if isinstance(m, dict)]
        row_ids += list(row.get("supporting_ids") or [])
        member_dirs: set[str] = set()
        for i in row_ids:
            if not isinstance(i, str) or not i:
                errors.append(f"E_SCHEMA: {rid}: empty or non-string id")
                continue
            if i in current_index:
                member_dirs.add(current_index[i])
            elif i in candidate_ids:
                if usable == "accepted_only":
                    errors.append(
                        f"E_HOLD_ID_ON_ACCEPTED_ROW: {rid}: {i} resolves only under "
                        f"canon/candidates/ but the row is usable: accepted_only"
                    )
            else:
                errors.append(f"E_UNRESOLVED_ID: {rid}: {i} resolves neither in canon/knowledge/current nor under canon/candidates/")

        # independence entries recomputed against the audit records
        for entry in row.get("independence") or []:
            if not isinstance(entry, dict):
                errors.append(f"E_SCHEMA: {rid}: independence entry is not a mapping")
                continue
            a, b, claimed = entry.get("a"), entry.get("b"), entry.get("audit_relation")
            missing = [d for d in (a, b) if d not in audit_records]
            if missing:
                errors.append(f"E_UNKNOWN_SOURCE_DIR: {rid}: no audit record for {missing}")
                continue
            recorded = recorded_pair_relation(a, b, audit_records)
            expected = NO_ENTRY if recorded is None else recorded
            if claimed != expected:
                errors.append(
                    f"E_INDEPENDENCE_MISMATCH: {rid}: pair ({a}, {b}) quoted as {claimed!r}, "
                    f"audit records say {expected!r}"
                )

        # agreement rows need >= 2 pairwise-independent origins, recomputed
        member_only_dirs = {
            current_index[m.get("id")]
            for m in members
            if isinstance(m, dict) and m.get("id") in current_index
        }
        if relation in AGREEMENT_RELATIONS:
            computed = max_independent_subset(member_only_dirs, audit_records)
            if computed < 2:
                errors.append(
                    f"E_AGREEMENT_WITHOUT_INDEPENDENT_ORIGINS: {rid}: relation {relation!r} "
                    f"asserts agreement but only {computed} pairwise-independent origin(s) "
                    f"exist among {sorted(member_only_dirs)}"
                )
            declared = row.get("independent_origins")
            if declared is not None and declared != computed:
                errors.append(
                    f"E_ORIGIN_COUNT: {rid}: declares independent_origins: {declared}, "
                    f"recomputed maximum pairwise-independent subset is {computed}"
                )

        term = row.get("adjudicates_duplicate_term")
        if term:
            adjudications[term].append(rid)

        if kind == "imported_observation":
            if len(members) >= 2 and all(isinstance(m, dict) for m in members[:2]):
                triple = (members[0].get("id"), relation, members[1].get("id"))
                imported_triples[triple] += 1
                imported_usable_ok[triple] = usable == "involves_hold"
            if usable != "involves_hold":
                errors.append(f"E_IMPORT_USABLE: {rid}: imported_observation rows must be usable: involves_hold")

    for rid, n in seen_record_ids.items():
        if n > 1:
            errors.append(f"E_SCHEMA: record_id {rid} appears {n} times")

    # ── ledger-completeness checks ───────────────────────────────────────────────────────────
    if ledger.get("ledger_complete") is True:
        expected_duplicates = duplicate_term_strings()
        for term in sorted(expected_duplicates):
            rows = adjudications.get(term, [])
            if len(rows) != 1:
                errors.append(
                    f"E_DUPLICATE_ADJUDICATION: duplicate term {term!r} has {len(rows)} "
                    f"adjudication rows ({rows}); exactly one is required"
                )
        for term in sorted(set(adjudications) - expected_duplicates):
            errors.append(
                f"E_DUPLICATE_ADJUDICATION: {adjudications[term]} adjudicates {term!r}, which is "
                f"not a cross-directory duplicate term string in canon/knowledge/current"
            )

        crossref = yaml.safe_load(CANON014_CROSSREF.read_text()) or {}
        for src_row in crossref.get("relationships") or []:
            triple = (src_row.get("from"), src_row.get("relation"), src_row.get("to"))
            count = imported_triples.get(triple, 0)
            if count != 1:
                errors.append(
                    f"E_IMPORT_MISSING: CANON-014 crossref row {triple} appears {count} times "
                    f"in the ledger; exactly one imported_observation row is required"
                )
            elif not imported_usable_ok.get(triple):
                errors.append(f"E_IMPORT_USABLE: CANON-014 crossref row {triple} is not usable: involves_hold")

    return errors


def main(argv: list[str]) -> int:
    path = Path(argv[1]) if len(argv) > 1 else DEFAULT_LEDGER
    ledger = yaml.safe_load(path.read_text())
    errors = validate(ledger)
    if errors:
        for error in errors:
            print(error)
        print(f"FAIL: {len(errors)} error(s) in {path}")
        return 1
    n = len(ledger.get("records") or [])
    print(f"OK: {path} — {n} candidate records, all rules hold")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
