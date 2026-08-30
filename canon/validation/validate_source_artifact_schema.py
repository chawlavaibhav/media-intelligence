"""Mechanical conformance for SPEC-03 / SPEC-04 / SPEC-05 source artifacts.

History of this file
--------------------
The CANON-013-era experimental validator reported PASS on a package in which `scs_sa8_002` was
missing SPEC-03's required `evidence.system_level_uncertainty`, because it checked only a
hand-picked subset of fields. CANON-014 replaced it with a required-field checker, which closed
that hole and immediately found two defects in accepted live Canon.

The CANON-014 web-cleanup lane then found that the required-field checker was still not enough:
it verified that fields were PRESENT and, for a handful of them, that values were in range - but
it did not check most of the specs' controlled vocabularies at all. Free prose sat in
`evidence.source_uncertainty`, invented relation names sat in `intra_source_relations`, and an
invalid `label_origin` passed, because nothing compared those values against the specs.

This version enumerates every controlled vocabulary in SPEC-03, SPEC-04 and SPEC-05 and checks
membership, in addition to presence and reference resolution. The tests assert that each invalid
value actually fails; a validator that passes malformed examples is not done.

What a PASS from this module does and does not mean
---------------------------------------------------
It means the implemented structural checks passed. It is NOT Canon admission. Admission is
`canon/audit/AUDIT-GATE-v0.2.md`, which asks questions about representation, evidence origin,
lineage and technology contingency that no structural validator can answer.
"""

from __future__ import annotations

import os

import yaml

# ══════════════════════════════════════════════════════════════════════════════
# SPEC-03 — SourceKnowledge
# ══════════════════════════════════════════════════════════════════════════════

SK_REQUIRED = [
    "sk_id", "source_id", "concept_label", "label_origin", "claim", "claim_type",
    "mechanism", "scope", "evidence", "provenance",
]
SK_EVIDENCE_REQUIRED = ["characteristics", "source_uncertainty", "extraction_uncertainty"]

LABEL_ORIGINS = {"extractor_assigned", "source_verbatim"}
SK_CLAIM_TYPES = {"explicit_source_claim", "source_interpretation"}
SK_SOURCE_SUPPORT = {"text", "visual", "text_and_visual"}
CAVEAT_ORIGINS = {"source_stated", "extractor_observed"}

EVIDENCE_CHARACTERISTICS = {
    "explicitly_stated", "visually_demonstrated", "controlled_comparison", "argued",
    "practitioner_assertion", "anecdotal", "outcome_claimed", "empirical_within_source",
    "repeated_within_source", "mechanism_given", "mechanism_absent",
    "culturally_bounded", "historical_claim",
}
SOURCE_UNCERTAINTY = {
    "none", "source_hedges", "source_asks_open_question",
    "source_states_it_as_tradition", "source_concedes_difficulty",
}
EXTRACTION_UNCERTAINTY = {
    "none", "column_interleaving", "figure_not_inspected", "ocr_degraded",
    "inferred_from_layout", "ambiguous_referent",
}
# SPEC-03 line 95-97. `member_of_system` targets a scs_id; the rest target an sk_id.
SK_RELATIONS = {
    "qualifies", "qualified_by", "trades_off_with", "depends_on",
    "generalises", "specialises", "contradicts", "demonstrated_together_with",
    "member_of_system",
}

# ══════════════════════════════════════════════════════════════════════════════
# SPEC-03 — SourceConceptSystem
# ══════════════════════════════════════════════════════════════════════════════

SCS_REQUIRED = [
    "scs_id", "source_id", "label", "label_origin", "system_type", "system_type_origin",
    "description", "whole_system_claim", "members", "internal_structure",
    "source_warns_against_isolated_use", "evidence", "provenance",
]
SCS_EVIDENCE_REQUIRED = [
    "characteristics", "source_uncertainty", "extraction_uncertainty", "system_level_uncertainty",
]
SCS_SYSTEM_TYPES = {
    "trade_off_set", "priority_order", "sequence", "decision_framework",
    "causal_model", "interacting_set", "mutual_qualification",
}
ORIGIN_STRUCTURAL = {"source_stated", "extractor_inferred"}
WSC_ORIGINS = {"source_explicit", "extractor_synthesis"}
ORDERING_SCHEMES = {"source_numbered", "causal", "procedural", "none"}

# ══════════════════════════════════════════════════════════════════════════════
# SPEC-04 — OperationalBinding
# ══════════════════════════════════════════════════════════════════════════════

BND_REQUIRED = ["binding_id", "target_type", "role", "rationale", "evidence_basis", "status"]

# SPEC-04 validation rule 2 says target_type comes from "the fixed list" and never enumerates it;
# it shows four worked examples. `benchmark` is used by 13 bindings across ACCEPTED live Canon and
# appears in the Audit Gate's own `application_fit` consumer vocabulary. Accepted live Canon governs
# over an unenumerated list, so `benchmark` is admitted and the SPEC-04 gap is a Controller finding
# rather than something this validator resolves by invalidating audited sources.
BND_TARGET_TYPES = {"creative_ir", "production", "evaluation", "governance", "benchmark"}
BND_ROLES = {"fills", "constrains", "diagnoses", "repairs", "derives", "flags", "evaluates"}
BND_EVIDENCE_BASIS = {
    "derived_from_source", "extractor_inference", "cross_source_supported", "empirically_supported",
}
BND_STATUS = {"proposed", "accepted", "production_candidate", "deprecated", "rejected"}
GOVERNANCE_CONSUMERS = {
    "taxonomy_governance", "retrieval_governance", "conflict_resolution",
    "evidence_interpretation", "rule_application", "cross_source_synthesis",
}
OBSERVATION_UNITS = {
    "frame", "shot", "shot_pair", "sequence", "whole_asset", "asset_set_over_time",
}

# ══════════════════════════════════════════════════════════════════════════════
# SPEC-05 — Ontology
# ══════════════════════════════════════════════════════════════════════════════

TERM_REQUIRED = ["term_id", "term", "origin", "origin_ref", "kind", "definition_in_origin_frame"]
TERM_ORIGINS = {"source", "empirical", "customer", "product", "extractor"}
TERM_KINDS = {"problem", "remedy", "property", "entity"}
ONTOLOGY_RELATIONS = {
    "maps_to", "broader_than", "narrower_than", "related_to", "potentially_equivalent_to",
    "distinct_from", "same_failure_family", "same_mechanism", "same_observed_effect", "uncertain",
}
CONCEPT_KINDS = {"source_specific_concept", "canonical_concept", "cross_source_concept"}
CONCEPT_ORIGINS = {"source_stated", "extractor_inferred"}
REPAIR_EXECUTORS = {
    "physical_production", "generative_respecification", "deterministic_composite",
    "human_edit", "unknown",
}


def _iter(doc, key):
    """Accept either {source_id, <key>: [...]} or a bare top-level list."""
    if isinstance(doc, dict):
        return doc.get(key) or []
    if isinstance(doc, list):
        return doc
    return []


def _load(path):
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def check_source_dir(dirpath, *, require_visual_ledger=False):  # noqa: C901 - a checklist, not logic
    """Return a list of error strings for one source directory. Empty list == pass."""
    errors = []
    name = os.path.basename(dirpath.rstrip("/"))

    def err(msg):
        errors.append(f"[{name}] {msg}")

    def enum(value, allowed, where, field):
        if value not in allowed:
            err(f"{where}: {field} {value!r} not in {sorted(allowed)}")

    paths = {
        "sk": os.path.join(dirpath, "source-knowledge.yaml"),
        "scs": os.path.join(dirpath, "source-concept-systems.yaml"),
        "bnd": os.path.join(dirpath, "operational-bindings.yaml"),
        "ont": os.path.join(dirpath, "ontology-mappings.yaml"),
    }
    if require_visual_ledger:
        paths["vel"] = os.path.join(dirpath, "visual-evidence-ledger.yaml")

    docs = {}
    for k, p in paths.items():
        if not os.path.exists(p):
            err(f"missing required artifact {os.path.basename(p)}")
            continue
        try:
            docs[k] = _load(p)
        except Exception as exc:  # noqa: BLE001 - report, do not crash the run
            err(f"{os.path.basename(p)} does not parse: {exc}")

    # Audit Gate rule 2 resolves source_id out of these files; a bare list has nowhere to put it.
    for k in ("sk", "scs", "bnd", "ont"):
        d = docs.get(k)
        if d is not None and (not isinstance(d, dict) or "source_id" not in d):
            err(f"{os.path.basename(paths[k])} has no top-level source_id "
                f"(Audit Gate rule 2 cannot resolve against it)")

    sk_items = _iter(docs.get("sk"), "source_knowledge")
    scs_items = _iter(docs.get("scs"), "source_concept_systems")
    bnd_items = _iter(docs.get("bnd"), "operational_bindings")
    ont = docs.get("ont") if isinstance(docs.get("ont"), dict) else {}
    terms = ont.get("terms") or []
    relationships = ont.get("relationships") or []
    concepts = ont.get("concepts") or []

    sk_ids = {o.get("sk_id") for o in sk_items if isinstance(o, dict)}
    scs_ids = {o.get("scs_id") for o in scs_items if isinstance(o, dict)}
    term_ids = {t.get("term_id") for t in terms if isinstance(t, dict)}
    concept_ids = {c.get("concept_id") for c in concepts if isinstance(c, dict)}

    # ── SPEC-03 SourceKnowledge ───────────────────────────────────────────────
    for o in sk_items:
        if not isinstance(o, dict):
            err("source_knowledge entry is not a mapping")
            continue
        oid = o.get("sk_id", "<no sk_id>")
        for f in SK_REQUIRED:
            if f not in o:
                err(f"{oid}: missing required SourceKnowledge field '{f}'")

        enum(o.get("label_origin"), LABEL_ORIGINS, oid, "label_origin")
        enum(o.get("claim_type"), SK_CLAIM_TYPES, oid, "claim_type")
        if o.get("claim_type") == "source_interpretation" and not o.get("interpretation_basis"):
            err(f"{oid}: source_interpretation requires interpretation_basis")

        ev = o.get("evidence") or {}
        for f in SK_EVIDENCE_REQUIRED:
            if f not in ev:
                err(f"{oid}: missing required evidence.{f}")
        chars = ev.get("characteristics") or []
        if not chars:
            err(f"{oid}: evidence.characteristics is empty")
        for c in chars:
            enum(c, EVIDENCE_CHARACTERISTICS, oid, "evidence characteristic")
        if "source_uncertainty" in ev:
            enum(ev.get("source_uncertainty"), SOURCE_UNCERTAINTY, oid, "evidence.source_uncertainty")
        if "extraction_uncertainty" in ev:
            enum(ev.get("extraction_uncertainty"), EXTRACTION_UNCERTAINTY, oid,
                 "evidence.extraction_uncertainty")

        mech = o.get("mechanism")
        if not isinstance(mech, dict) or "stated_by_source" not in mech:
            err(f"{oid}: mechanism.stated_by_source missing (false is a normal value)")

        prov = o.get("provenance") or {}
        enum(prov.get("source_support"), SK_SOURCE_SUPPORT, oid, "provenance.source_support")
        # SPEC-03 rule 3: a page range OR an equivalent locator.
        if (prov.get("page_start") is None and not prov.get("locator")
                and not prov.get("chapter") and not prov.get("section")):
            err(f"{oid}: provenance resolves to neither a page range nor an equivalent locator")
        # SPEC-03 rule 4
        if prov.get("source_support") == "visual" and not (prov.get("inspected") or {}).get("figures"):
            err(f"{oid}: source_support 'visual' with no inspected figures (SPEC-03 rule 4)")

        for c in (o.get("caveats") or []):
            if isinstance(c, dict):
                if "origin" not in c:
                    err(f"{oid}: caveat missing origin")
                else:
                    enum(c["origin"], CAVEAT_ORIGINS, oid, "caveat origin")

        # SPEC-03 relation vocabulary + reference resolution
        for r in (o.get("intra_source_relations") or []):
            if not isinstance(r, dict):
                continue
            rel = r.get("relation")
            enum(rel, SK_RELATIONS, oid, "intra_source_relations relation")
            tgt = r.get("target")
            if tgt is None:
                err(f"{oid}: intra_source_relation has no target")
            elif rel == "member_of_system":
                if tgt not in scs_ids:
                    err(f"{oid}: member_of_system target '{tgt}' does not resolve to a scs_id")
            elif rel in SK_RELATIONS and tgt not in sk_ids:
                err(f"{oid}: intra_source_relation target '{tgt}' does not resolve to an sk_id")

    # ── SPEC-03 SourceConceptSystem ───────────────────────────────────────────
    for o in scs_items:
        if not isinstance(o, dict):
            err("source_concept_systems entry is not a mapping")
            continue
        oid = o.get("scs_id", "<no scs_id>")
        for f in SCS_REQUIRED:
            if f not in o:
                err(f"{oid}: missing required SourceConceptSystem field '{f}'")

        enum(o.get("label_origin"), LABEL_ORIGINS, oid, "label_origin")
        enum(o.get("system_type"), SCS_SYSTEM_TYPES, oid, "system_type")
        enum(o.get("system_type_origin"), ORIGIN_STRUCTURAL, oid, "system_type_origin")

        ev = o.get("evidence") or {}
        for f in SCS_EVIDENCE_REQUIRED:
            if f not in ev:
                err(f"{oid}: missing required evidence.{f}")
        for c in (ev.get("characteristics") or []):
            enum(c, EVIDENCE_CHARACTERISTICS, oid, "evidence characteristic")
        if "source_uncertainty" in ev:
            enum(ev.get("source_uncertainty"), SOURCE_UNCERTAINTY, oid, "evidence.source_uncertainty")
        if "extraction_uncertainty" in ev:
            enum(ev.get("extraction_uncertainty"), EXTRACTION_UNCERTAINTY, oid,
                 "evidence.extraction_uncertainty")

        wsc = o.get("whole_system_claim") or {}
        if "text" not in wsc:
            err(f"{oid}: whole_system_claim.text missing")
        enum(wsc.get("origin"), WSC_ORIGINS, oid, "whole_system_claim.origin")
        if wsc.get("origin") == "extractor_synthesis" and not wsc.get("interpretation_basis"):
            err(f"{oid}: extractor_synthesis whole_system_claim requires interpretation_basis")

        for m in (o.get("members") or []):
            if not isinstance(m, dict):
                continue
            if "membership_origin" not in m:
                err(f"{oid}: member missing membership_origin")
            else:
                enum(m["membership_origin"], ORIGIN_STRUCTURAL, oid, "member membership_origin")
            ref = m.get("sk_ref")
            if ref and ref not in sk_ids:
                err(f"{oid}: member sk_ref '{ref}' does not resolve")

        ist = o.get("internal_structure")
        if not isinstance(ist, dict):
            err(f"{oid}: internal_structure missing or not a mapping")
        else:
            ordering = ist.get("ordering") or {}
            if "scheme" not in ordering:
                err(f"{oid}: internal_structure.ordering.scheme missing")
            else:
                enum(ordering["scheme"], ORDERING_SCHEMES, oid, "ordering.scheme")
            enum(ordering.get("origin"), ORIGIN_STRUCTURAL, oid, "internal_structure.ordering.origin")
            # SPEC-03: origin is required at EVERY structural level.
            for key in ("dependencies", "tradeoffs", "conflicts"):
                for e in (ist.get(key) or []):
                    if not isinstance(e, dict):
                        continue
                    if "origin" not in e:
                        err(f"{oid}: {key} entry missing origin")
                    else:
                        enum(e["origin"], ORIGIN_STRUCTURAL, oid, f"{key} entry origin")
                    for ref in (e.get("between") or []):
                        if ref not in sk_ids:
                            err(f"{oid}: {key} entry references '{ref}', which does not resolve")

    # ── SPEC-04 OperationalBinding ────────────────────────────────────────────
    for o in bnd_items:
        if not isinstance(o, dict):
            err("operational_bindings entry is not a mapping")
            continue
        oid = o.get("binding_id", "<no binding_id>")
        for f in BND_REQUIRED:
            if f not in o:
                err(f"{oid}: missing required binding field '{f}'")

        tt = o.get("target_type")
        enum(tt, BND_TARGET_TYPES, oid, "target_type")
        enum(o.get("evidence_basis"), BND_EVIDENCE_BASIS, oid, "evidence_basis")
        enum(o.get("status"), BND_STATUS, oid, "status")

        roles = o.get("role")
        if not isinstance(roles, list) or not roles:
            err(f"{oid}: role must be a non-empty list")
        else:
            for r in roles:
                enum(r, BND_ROLES, oid, "role")

        refs = o.get("source_knowledge_refs") or []
        srefs = o.get("source_system_refs") or []
        if not refs and not srefs:
            err(f"{oid}: binding references neither SourceKnowledge nor a SourceConceptSystem")
        for r in refs:
            if r not in sk_ids:
                err(f"{oid}: source_knowledge_ref '{r}' does not resolve")
        for r in srefs:
            if r not in scs_ids:
                err(f"{oid}: source_system_ref '{r}' does not resolve")

        # SPEC-04 rule 8: ontology references use SPEC-05 identifiers, never raw strings.
        # A SPEC-05 identifier is a term_id OR a concept_id - live accepted Canon points at both
        # (e.g. grammar-of-the-edit binds `cc_perceived_break_at_a_transition`, a canonical
        # concept). Restricting this to term_ids would invalidate audited sources, so both resolve.
        for key in ("failure_ontology_refs", "repair_ontology_refs"):
            for r in (o.get(key) or []):
                if (term_ids or concept_ids) and r not in term_ids and r not in concept_ids:
                    err(f"{oid}: {key} '{r}' resolves to neither a term_id nor a concept_id "
                        f"in this source's ontology")

        # PROJECT-CONTRACT separation 2: Production IR does not exist.
        if tt == "production":
            if o.get("status") != "production_candidate":
                err(f"{oid}: production binding must carry status 'production_candidate'")
            if o.get("target_path") not in (None, "", "null"):
                err(f"{oid}: production binding must have target_path null "
                    f"(Production IR does not exist)")
        if tt == "creative_ir":
            for f in ("target_path", "target_schema", "target_schema_version"):
                if f not in o:
                    err(f"{oid}: creative_ir binding missing '{f}'")
        if tt == "governance":
            enum(o.get("governance_consumer"), GOVERNANCE_CONSUMERS, oid, "governance_consumer")
        if tt == "evaluation":
            if "observation_unit" not in o:
                err(f"{oid}: evaluation binding missing observation_unit")
            else:
                enum(o["observation_unit"], OBSERVATION_UNITS, oid, "observation_unit")

    # ── SPEC-05 Ontology ──────────────────────────────────────────────────────
    for t in terms:
        if not isinstance(t, dict):
            err("ontology term is not a mapping")
            continue
        tid = t.get("term_id", "<no term_id>")
        for f in TERM_REQUIRED:
            if f not in t:
                err(f"{tid}: missing required ontology term field '{f}'")
        enum(t.get("origin"), TERM_ORIGINS, tid, "term origin")
        enum(t.get("kind"), TERM_KINDS, tid, "term kind")
        for ref in (t.get("arising_from") or []):
            if ref not in sk_ids:
                err(f"{tid}: arising_from '{ref}' does not resolve to an sk_id")
        # SPEC-05: every repair term carries executable_by, so the translation gap stays visible.
        if t.get("kind") == "remedy":
            ex = t.get("executable_by")
            if not ex:
                err(f"{tid}: repair term missing executable_by "
                    f"(SPEC-05 requires it so the generative gap is visible)")
            elif not isinstance(ex, list):
                err(f"{tid}: executable_by must be a list")
            else:
                for e in ex:
                    enum(e, REPAIR_EXECUTORS, tid, "executable_by")

    for r in relationships:
        if not isinstance(r, dict):
            continue
        rid = f"{r.get('from')}->{r.get('to')}"
        enum(r.get("relation"), ONTOLOGY_RELATIONS, rid, "ontology relation")
        for side in ("from", "to"):
            ref = r.get(side)
            if ref is None:
                err(f"{rid}: relationship missing '{side}'")
            elif term_ids and ref not in term_ids:
                err(f"{rid}: relationship '{side}' term '{ref}' does not resolve")

    for c in concepts:
        if not isinstance(c, dict):
            continue
        cid = c.get("concept_id", "<no concept_id>")
        enum(c.get("kind"), CONCEPT_KINDS, cid, "concept kind")
        for ref in (c.get("children_terms") or []):
            if ref not in term_ids:
                err(f"{cid}: children_terms '{ref}' does not resolve to a term_id")
        kind = c.get("kind")
        if kind == "source_specific_concept":
            if "origin_ref" not in c:
                err(f"{cid}: source_specific_concept requires origin_ref")
            enum(c.get("origin"), CONCEPT_ORIGINS, cid, "source_specific_concept origin")
            if c.get("asserts_agreement_between_sources"):
                err(f"{cid}: a source_specific_concept must not assert agreement between sources")
        elif kind == "canonical_concept":
            # SPEC-05: a canonical concept NEVER asserts its children are the same.
            if c.get("asserts_equivalence") is not False:
                err(f"{cid}: canonical_concept requires asserts_equivalence: false")
        elif kind == "cross_source_concept":
            origins = c.get("independent_origins") or []
            if len(origins) < 2:
                err(f"{cid}: cross_source_concept requires 2 or more independent_origins, "
                    f"got {len(origins)}")
            if len(set(origins)) != len(origins):
                err(f"{cid}: cross_source_concept independent_origins contains duplicates")
            if not c.get("definition"):
                err(f"{cid}: cross_source_concept requires a definition")

    return errors


def check_package(root, *, require_visual_ledger=False):
    """Check every source directory under `root`. Returns (errors, n_dirs)."""
    dirs = sorted(
        d for d in os.listdir(root)
        if os.path.isdir(os.path.join(root, d)) and not d.startswith(".")
    )
    errors = []
    for d in dirs:
        errors.extend(
            check_source_dir(os.path.join(root, d), require_visual_ledger=require_visual_ledger)
        )
    return errors, len(dirs)


def main(argv):
    if len(argv) < 2:
        print("usage: validate_source_artifact_schema.py <package-root> [--require-visual-ledger]")
        return 2
    root = argv[1]
    require_vel = "--require-visual-ledger" in argv
    errors, n = check_package(root, require_visual_ledger=require_vel)
    for e in errors:
        print("ERROR", e)
    print(f"\n{n} source directories checked, {len(errors)} errors")
    print("Structural conformance only. This is NOT Canon admission "
          "(see canon/audit/AUDIT-GATE-v0.2.md).")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(os.sys.argv))
