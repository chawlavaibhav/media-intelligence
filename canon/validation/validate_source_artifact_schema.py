"""Required-field conformance for SPEC-03 / SPEC-04 / SPEC-05 source artifacts.

Why this module exists
----------------------
The CANON-013-era experimental validator
(`canon/experimental/book-expansion-qa-v1/validate_experimental.py`) reported PASS on a package
in which `scs_sa8_002` was missing the SPEC-03-required
`evidence.system_level_uncertainty`. The omission was found by a lane reading the object, not by
the validator, because that validator only ever checked a hand-picked subset of fields:
for SourceConceptSystem it checked `whole_system_claim.interpretation_basis` and member
resolution, and nothing else.

Patching that one field would have left the hole open. CANON-014 therefore compared the package
against the *complete* required-field sets in the specs and found the reported omission to be one
member of a class:

  * 3 systems missing `evidence.system_level_uncertainty` (not 1)
  * 84 `dependencies` / `tradeoffs` / `conflicts` entries missing `origin`, which SPEC-03 requires
    at every structural level
  * 22 artifact files missing the top-level `source_id` that Audit Gate rule 2 resolves against

This module enumerates required fields positively, so a future omission of ANY of them fails
rather than passing silently.

What a PASS from this module does and does not mean
---------------------------------------------------
It means the implemented structural checks passed. It is NOT Canon admission. Admission is
`canon/audit/AUDIT-GATE-v0.2.md`, which asks questions about representation, evidence origin,
lineage and technology contingency that no structural validator can answer.
"""

from __future__ import annotations

import os

import yaml

# ── SPEC-03 SourceKnowledge ────────────────────────────────────────────────────
SK_REQUIRED = [
    "sk_id", "source_id", "concept_label", "label_origin", "claim", "claim_type",
    "mechanism", "scope", "evidence", "provenance",
]
SK_EVIDENCE_REQUIRED = ["characteristics", "source_uncertainty", "extraction_uncertainty"]
SK_CLAIM_TYPES = {"explicit_source_claim", "source_interpretation"}
SK_SOURCE_SUPPORT = {"text", "visual", "text_and_visual"}

# ── SPEC-03 SourceConceptSystem ───────────────────────────────────────────────
SCS_REQUIRED = [
    "scs_id", "source_id", "label", "label_origin", "system_type", "system_type_origin",
    "description", "whole_system_claim", "members", "internal_structure",
    "source_warns_against_isolated_use", "evidence", "provenance",
]
# system_level_uncertainty is the field the old validator did not check.
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

# ── SPEC-04 OperationalBinding ────────────────────────────────────────────────
BND_REQUIRED = ["binding_id", "target_type", "role", "rationale", "evidence_basis", "status"]
# SPEC-04 says "target_type from the fixed list" (validation rule 2) but never enumerates that
# list; it only shows four worked examples. CANON-014 found that `benchmark` is used by 13 bindings
# across ACCEPTED live Canon sources, and that the Audit Gate's own `application_fit` consumer
# vocabulary lists `benchmark` explicitly. Accepted live Canon governs over an unenumerated list, so
# `benchmark` is admitted here and the SPEC-04 gap is routed to the Controller as a finding rather
# than "fixed" by invalidating audited sources.
BND_TARGET_TYPES = {"creative_ir", "production", "evaluation", "governance", "benchmark"}


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


def check_source_dir(dirpath, *, require_visual_ledger=False):
    """Return a list of error strings for one source directory. Empty list == pass."""
    errors = []
    name = os.path.basename(dirpath.rstrip("/"))

    def err(msg):
        errors.append(f"[{name}] {msg}")

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
    sk_ids = {o.get("sk_id") for o in sk_items if isinstance(o, dict)}
    scs_ids = {o.get("scs_id") for o in scs_items if isinstance(o, dict)}

    # ── SourceKnowledge ───────────────────────────────────────────────────────
    for o in sk_items:
        if not isinstance(o, dict):
            err("source_knowledge entry is not a mapping")
            continue
        oid = o.get("sk_id", "<no sk_id>")
        for f in SK_REQUIRED:
            if f not in o:
                err(f"{oid}: missing required SourceKnowledge field '{f}'")
        if o.get("claim_type") not in SK_CLAIM_TYPES:
            err(f"{oid}: claim_type {o.get('claim_type')!r} not in {sorted(SK_CLAIM_TYPES)}")
        if o.get("claim_type") == "source_interpretation" and not o.get("interpretation_basis"):
            err(f"{oid}: source_interpretation requires interpretation_basis")
        ev = o.get("evidence") or {}
        for f in SK_EVIDENCE_REQUIRED:
            if f not in ev:
                err(f"{oid}: missing required evidence.{f}")
        if not (ev.get("characteristics") or []):
            err(f"{oid}: evidence.characteristics is empty")
        mech = o.get("mechanism")
        if not isinstance(mech, dict) or "stated_by_source" not in mech:
            err(f"{oid}: mechanism.stated_by_source missing (false is a normal value)")
        prov = o.get("provenance") or {}
        if prov.get("source_support") not in SK_SOURCE_SUPPORT:
            err(f"{oid}: provenance.source_support {prov.get('source_support')!r} invalid")
        # SPEC-03 rule 3: a page range OR an equivalent locator.
        if (prov.get("page_start") is None and not prov.get("locator")
                and not prov.get("chapter") and not prov.get("section")):
            err(f"{oid}: provenance resolves to neither a page range nor an equivalent locator")
        # SPEC-03 rule 4
        if prov.get("source_support") == "visual" and not (prov.get("inspected") or {}).get("figures"):
            err(f"{oid}: source_support 'visual' with no inspected figures (SPEC-03 rule 4)")
        for c in (o.get("caveats") or []):
            if isinstance(c, dict) and "origin" not in c:
                err(f"{oid}: caveat missing origin")

    # ── SourceConceptSystem ───────────────────────────────────────────────────
    for o in scs_items:
        if not isinstance(o, dict):
            err("source_concept_systems entry is not a mapping")
            continue
        oid = o.get("scs_id", "<no scs_id>")
        for f in SCS_REQUIRED:
            if f not in o:
                err(f"{oid}: missing required SourceConceptSystem field '{f}'")
        ev = o.get("evidence") or {}
        for f in SCS_EVIDENCE_REQUIRED:
            if f not in ev:
                err(f"{oid}: missing required evidence.{f}")
        if o.get("system_type") not in SCS_SYSTEM_TYPES:
            err(f"{oid}: system_type {o.get('system_type')!r} not in {sorted(SCS_SYSTEM_TYPES)}")
        if o.get("system_type_origin") not in ORIGIN_STRUCTURAL:
            err(f"{oid}: system_type_origin {o.get('system_type_origin')!r} invalid")
        wsc = o.get("whole_system_claim") or {}
        if "text" not in wsc:
            err(f"{oid}: whole_system_claim.text missing")
        if wsc.get("origin") not in WSC_ORIGINS:
            err(f"{oid}: whole_system_claim.origin {wsc.get('origin')!r} invalid")
        if wsc.get("origin") == "extractor_synthesis" and not wsc.get("interpretation_basis"):
            err(f"{oid}: extractor_synthesis whole_system_claim requires interpretation_basis")
        for m in (o.get("members") or []):
            if not isinstance(m, dict):
                continue
            if "membership_origin" not in m:
                err(f"{oid}: member missing membership_origin")
            elif m["membership_origin"] not in ORIGIN_STRUCTURAL:
                err(f"{oid}: member membership_origin {m['membership_origin']!r} invalid")
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
            elif ordering["scheme"] not in ORDERING_SCHEMES:
                err(f"{oid}: ordering.scheme {ordering['scheme']!r} invalid")
            if ordering.get("origin") not in ORIGIN_STRUCTURAL:
                err(f"{oid}: internal_structure.ordering.origin missing or invalid")
            # SPEC-03: origin is required at EVERY structural level.
            for key in ("dependencies", "tradeoffs", "conflicts"):
                for e in (ist.get(key) or []):
                    if not isinstance(e, dict):
                        continue
                    if "origin" not in e:
                        err(f"{oid}: {key} entry missing origin")
                    elif e["origin"] not in ORIGIN_STRUCTURAL:
                        err(f"{oid}: {key} entry origin {e['origin']!r} invalid")

    # ── OperationalBinding ────────────────────────────────────────────────────
    for o in bnd_items:
        if not isinstance(o, dict):
            err("operational_bindings entry is not a mapping")
            continue
        oid = o.get("binding_id", "<no binding_id>")
        for f in BND_REQUIRED:
            if f not in o:
                err(f"{oid}: missing required binding field '{f}'")
        tt = o.get("target_type")
        if tt not in BND_TARGET_TYPES:
            err(f"{oid}: target_type {tt!r} not in {sorted(BND_TARGET_TYPES)}")
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
        # PROJECT-CONTRACT separation 2: Production IR does not exist yet.
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
        if tt == "evaluation" and "observation_unit" not in o:
            err(f"{oid}: evaluation binding missing observation_unit")

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
