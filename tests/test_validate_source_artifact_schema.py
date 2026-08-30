"""Tests for the CANON-014 source-artifact validator.

Two regressions this suite exists for
-------------------------------------
1. The CANON-013 experimental validator reported PASS on a package whose `scs_sa8_002` was missing
   SPEC-03's required `evidence.system_level_uncertainty`, because it never checked required-field
   presence on SourceConceptSystem at all.
2. The first CANON-014 validator fixed that by checking PRESENCE, and still passed free prose in
   `evidence.source_uncertainty`, invented relation names in `intra_source_relations`, and an
   invalid `label_origin` - because it did not check most of the specs' controlled VOCABULARIES.

The battery below therefore asserts, for every controlled vocabulary in SPEC-03, SPEC-04 and
SPEC-05, that an invalid value actually fails. A validator that passes malformed examples is not
done.
"""

import copy
import os
import sys

import pytest
import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from canon.validation.validate_source_artifact_schema import (  # noqa: E402
    SCS_EVIDENCE_REQUIRED,
    SCS_REQUIRED,
    SK_EVIDENCE_REQUIRED,
    SK_REQUIRED,
    check_package,
    check_source_dir,
)

REPO = os.path.join(os.path.dirname(__file__), "..")

MINIMAL_SK = {
    "source_id": "demo_source",
    "source_knowledge": [
        {
            "sk_id": "sk_demo_0001",
            "source_id": "demo_source",
            "concept_label": "a_demo_claim",
            "label_origin": "extractor_assigned",
            "claim": "The source says something.",
            "claim_type": "explicit_source_claim",
            "mechanism": {"stated_by_source": False, "text": None},
            "scope": {"domain_discussed_by_source": ["demo"], "conditions": "demo conditions"},
            "caveats": [{"text": "a caveat", "origin": "source_stated"}],
            "intra_source_relations": [
                {"relation": "qualifies", "target": "sk_demo_0002", "note": "n"},
                {"relation": "member_of_system", "target": "scs_demo_001"},
            ],
            "evidence": {
                "characteristics": ["explicitly_stated"],
                "source_uncertainty": "none",
                "extraction_uncertainty": "none",
            },
            "provenance": {
                "chapter": "1", "section": "opening", "page_start": None, "page_end": None,
                "locator": "ch.1 opening", "source_support": "text",
                "inspected": {"text": True, "figures": []},
            },
        },
        {
            "sk_id": "sk_demo_0002",
            "source_id": "demo_source",
            "concept_label": "a_second_claim",
            "label_origin": "source_verbatim",
            "claim": "The source says something else.",
            "claim_type": "explicit_source_claim",
            "mechanism": {"stated_by_source": False, "text": None},
            "scope": {"domain_discussed_by_source": ["demo"], "conditions": "demo conditions"},
            "evidence": {
                "characteristics": ["explicitly_stated"],
                "source_uncertainty": "none",
                "extraction_uncertainty": "none",
            },
            "provenance": {
                "chapter": "1", "section": "second", "page_start": None, "page_end": None,
                "locator": "ch.1 second", "source_support": "text",
                "inspected": {"text": True, "figures": []},
            },
        },
    ],
}

MINIMAL_SCS = {
    "source_id": "demo_source",
    "source_concept_systems": [
        {
            "scs_id": "scs_demo_001",
            "source_id": "demo_source",
            "label": "a_demo_system",
            "label_origin": "extractor_assigned",
            "system_type": "interacting_set",
            "system_type_origin": "extractor_inferred",
            "description": "A demo system.",
            "whole_system_claim": {
                "text": "The members interact.",
                "origin": "extractor_synthesis",
                "interpretation_basis": "The source never says this; the grouping is ours.",
                "source_ref": None,
            },
            "members": [
                {"sk_ref": "sk_demo_0001", "role_in_system": "dimension", "order": 1,
                 "membership_origin": "extractor_inferred"}
            ],
            "internal_structure": {
                "ordering": {"scheme": "none", "origin": "extractor_inferred"},
                "dependencies": [], "tradeoffs": [], "conflicts": [],
            },
            "source_warns_against_isolated_use": False,
            "source_warning_ref": None,
            "evidence": {
                "characteristics": ["explicitly_stated"],
                "source_uncertainty": "none",
                "extraction_uncertainty": "none",
                "system_level_uncertainty": "The grouping is the extractor's.",
            },
            "provenance": {"section": "ch.1", "page_start": None, "page_end": None,
                           "source_support": "text"},
        }
    ],
}

MINIMAL_BND = {
    "source_id": "demo_source",
    "operational_bindings": [
        {
            "binding_id": "bnd_demo_0001",
            "source_knowledge_refs": ["sk_demo_0001"],
            "source_system_refs": [],
            "target_type": "governance",
            "target_path": None,
            "role": ["flags"],
            "rationale": "r",
            "governance_consumer": "taxonomy_governance",
            "evidence_basis": "derived_from_source",
            "empirical_refs": [],
            "failure_ontology_refs": ["t_demo_0002"],
            "repair_ontology_refs": ["t_demo_0003"],
            "status": "proposed",
        }
    ],
}

MINIMAL_ONT = {
    "source_id": "demo_source",
    "extraction_date": "2026-08-30",
    "terms": [
        {"term_id": "t_demo_0001", "term": "a_source_word", "origin": "source",
         "origin_ref": "demo_source", "kind": "entity",
         "definition_in_origin_frame": "A word the source uses.", "arising_from": ["sk_demo_0001"]},
        {"term_id": "t_demo_0002", "term": "a_failure", "origin": "extractor",
         "origin_ref": "demo_source", "kind": "problem",
         "definition_in_origin_frame": "A failure shape."},
        {"term_id": "t_demo_0003", "term": "a_repair", "origin": "extractor",
         "origin_ref": "demo_source", "kind": "remedy",
         "definition_in_origin_frame": "A repair.", "executable_by": ["human_edit"]},
    ],
    "relationships": [
        {"from": "t_demo_0002", "to": "t_demo_0003", "relation": "related_to",
         "confidence_basis": "extractor_inferred", "note": "problem and remedy"}
    ],
    "concepts": [
        {"concept_id": "sc_demo_001", "kind": "source_specific_concept", "origin_ref": "demo_source",
         "label": "a_concept", "children_terms": ["t_demo_0001"], "origin": "extractor_inferred",
         "basis": "b", "asserts_agreement_between_sources": False}
    ],
}


def write_pkg(tmp_path, sk=None, scs=None, bnd=None, ont=None):
    d = tmp_path / "demo-source"
    d.mkdir(exist_ok=True)
    for fname, doc in [
        ("source-knowledge.yaml", sk if sk is not None else MINIMAL_SK),
        ("source-concept-systems.yaml", scs if scs is not None else MINIMAL_SCS),
        ("operational-bindings.yaml", bnd if bnd is not None else MINIMAL_BND),
        ("ontology-mappings.yaml", ont if ont is not None else MINIMAL_ONT),
    ]:
        (d / fname).write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    return str(d)


def test_minimal_valid_package_passes(tmp_path):
    assert check_source_dir(write_pkg(tmp_path)) == []


# ══════════════════════════════════════════════════════════════════════════════
# The two original regressions
# ══════════════════════════════════════════════════════════════════════════════

def test_missing_system_level_uncertainty_is_caught(tmp_path):
    """The exact omission the CANON-013 validator let through as PASS."""
    scs = copy.deepcopy(MINIMAL_SCS)
    del scs["source_concept_systems"][0]["evidence"]["system_level_uncertainty"]
    errors = check_source_dir(write_pkg(tmp_path, scs=scs))
    assert any("system_level_uncertainty" in e for e in errors), errors


def test_free_prose_in_source_uncertainty_is_caught(tmp_path):
    """The exact defect the first CANON-014 validator let through.

    `source_uncertainty` is a controlled vocabulary. Free prose describing how weak the evidence is
    is an EXTRACTOR observation and belongs in a caveat, not in this field.
    """
    sk = copy.deepcopy(MINIMAL_SK)
    sk["source_knowledge"][0]["evidence"]["source_uncertainty"] = \
        "The source supplies no date, market or outcome for this execution."
    errors = check_source_dir(write_pkg(tmp_path, sk=sk))
    assert any("source_uncertainty" in e for e in errors), errors


# ══════════════════════════════════════════════════════════════════════════════
# Every controlled vocabulary: an invalid value must fail
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("field,bad", [
    ("label_origin", "source_stated"),          # a real value that is NOT in SPEC-03's list
    ("claim_type", "source_assertion"),
])
def test_invalid_sk_scalar_enums_are_caught(tmp_path, field, bad):
    sk = copy.deepcopy(MINIMAL_SK)
    sk["source_knowledge"][0][field] = bad
    errors = check_source_dir(write_pkg(tmp_path, sk=sk))
    assert any(field in e for e in errors), (field, errors)


@pytest.mark.parametrize("field,bad", [
    ("source_uncertainty", "author_is_vague"),
    ("extraction_uncertainty", "body_copy_illegible"),
])
def test_invalid_uncertainty_enums_are_caught(tmp_path, field, bad):
    sk = copy.deepcopy(MINIMAL_SK)
    sk["source_knowledge"][0]["evidence"][field] = bad
    errors = check_source_dir(write_pkg(tmp_path, sk=sk))
    assert any(field in e for e in errors), (field, errors)


def test_invalid_evidence_characteristic_is_caught(tmp_path):
    sk = copy.deepcopy(MINIMAL_SK)
    sk["source_knowledge"][0]["evidence"]["characteristics"] = ["explicitly_stated", "well_argued"]
    errors = check_source_dir(write_pkg(tmp_path, sk=sk))
    assert any("evidence characteristic" in e for e in errors), errors


@pytest.mark.parametrize("bad", [
    "co_occurs_with", "supports", "supported_by", "exemplifies", "exemplified_by",
    "contrasts_with", "tension_with", "constrained_by",
])
def test_invalid_intra_source_relation_is_caught(tmp_path, bad):
    """Every invented relation the cleanup lane found in the CANON-014 candidates."""
    sk = copy.deepcopy(MINIMAL_SK)
    sk["source_knowledge"][0]["intra_source_relations"] = [
        {"relation": bad, "target": "sk_demo_0002"}]
    errors = check_source_dir(write_pkg(tmp_path, sk=sk))
    assert any("intra_source_relations relation" in e for e in errors), (bad, errors)


def test_unresolvable_relation_target_is_caught(tmp_path):
    sk = copy.deepcopy(MINIMAL_SK)
    sk["source_knowledge"][0]["intra_source_relations"] = [
        {"relation": "qualifies", "target": "sk_does_not_exist"}]
    errors = check_source_dir(write_pkg(tmp_path, sk=sk))
    assert any("does not resolve" in e for e in errors), errors


def test_member_of_system_pointing_at_an_sk_id_is_caught(tmp_path):
    """`member_of_system` targets a scs_id; everything else targets an sk_id."""
    sk = copy.deepcopy(MINIMAL_SK)
    sk["source_knowledge"][0]["intra_source_relations"] = [
        {"relation": "member_of_system", "target": "sk_demo_0002"}]
    errors = check_source_dir(write_pkg(tmp_path, sk=sk))
    assert any("does not resolve to a scs_id" in e for e in errors), errors


def test_invalid_caveat_origin_is_caught(tmp_path):
    sk = copy.deepcopy(MINIMAL_SK)
    sk["source_knowledge"][0]["caveats"] = [{"text": "x", "origin": "extractor_inferred"}]
    errors = check_source_dir(write_pkg(tmp_path, sk=sk))
    assert any("caveat origin" in e for e in errors), errors


@pytest.mark.parametrize("field,bad", [
    ("system_type", "interacting"),
    ("system_type_origin", "extractor_synthesis"),
    ("label_origin", "source_stated"),
])
def test_invalid_scs_enums_are_caught(tmp_path, field, bad):
    scs = copy.deepcopy(MINIMAL_SCS)
    scs["source_concept_systems"][0][field] = bad
    errors = check_source_dir(write_pkg(tmp_path, scs=scs))
    assert any(field in e for e in errors), (field, errors)


def test_invalid_whole_system_claim_origin_is_caught(tmp_path):
    scs = copy.deepcopy(MINIMAL_SCS)
    scs["source_concept_systems"][0]["whole_system_claim"]["origin"] = "extractor_inferred"
    errors = check_source_dir(write_pkg(tmp_path, scs=scs))
    assert any("whole_system_claim.origin" in e for e in errors), errors


def test_invalid_ordering_scheme_is_caught(tmp_path):
    scs = copy.deepcopy(MINIMAL_SCS)
    scs["source_concept_systems"][0]["internal_structure"]["ordering"]["scheme"] = "alphabetical"
    errors = check_source_dir(write_pkg(tmp_path, scs=scs))
    assert any("ordering.scheme" in e for e in errors), errors


def test_invalid_membership_origin_is_caught(tmp_path):
    scs = copy.deepcopy(MINIMAL_SCS)
    scs["source_concept_systems"][0]["members"][0]["membership_origin"] = "extractor_assigned"
    errors = check_source_dir(write_pkg(tmp_path, scs=scs))
    assert any("membership_origin" in e for e in errors), errors


@pytest.mark.parametrize("key", ["dependencies", "tradeoffs", "conflicts"])
def test_structural_entry_origin_is_required_and_checked(tmp_path, key):
    scs = copy.deepcopy(MINIMAL_SCS)
    scs["source_concept_systems"][0]["internal_structure"][key] = [
        {"between": ["sk_demo_0001", "sk_demo_0002"], "nature": "x"}]
    errors = check_source_dir(write_pkg(tmp_path, scs=scs))
    assert any(f"{key} entry missing origin" in e for e in errors), errors
    scs["source_concept_systems"][0]["internal_structure"][key][0]["origin"] = "extractor_assigned"
    errors = check_source_dir(write_pkg(tmp_path, scs=scs))
    assert any(f"{key} entry origin" in e for e in errors), errors


def test_structural_entry_unresolvable_reference_is_caught(tmp_path):
    scs = copy.deepcopy(MINIMAL_SCS)
    scs["source_concept_systems"][0]["internal_structure"]["tradeoffs"] = [
        {"between": ["sk_demo_0001", "sk_nope"], "nature": "x", "origin": "extractor_inferred"}]
    errors = check_source_dir(write_pkg(tmp_path, scs=scs))
    assert any("does not resolve" in e for e in errors), errors


@pytest.mark.parametrize("field,bad", [
    ("target_type", "retrieval"),
    ("evidence_basis", "extractor_judgement"),
    ("status", "candidate"),
    ("governance_consumer", "canon_governance"),
])
def test_invalid_binding_enums_are_caught(tmp_path, field, bad):
    bnd = copy.deepcopy(MINIMAL_BND)
    bnd["operational_bindings"][0][field] = bad
    errors = check_source_dir(write_pkg(tmp_path, bnd=bnd))
    assert any(field in e for e in errors), (field, errors)


def test_invalid_binding_role_is_caught(tmp_path):
    bnd = copy.deepcopy(MINIMAL_BND)
    bnd["operational_bindings"][0]["role"] = ["flags", "informs"]
    errors = check_source_dir(write_pkg(tmp_path, bnd=bnd))
    assert any("role" in e for e in errors), errors


def test_empty_binding_role_is_caught(tmp_path):
    bnd = copy.deepcopy(MINIMAL_BND)
    bnd["operational_bindings"][0]["role"] = []
    errors = check_source_dir(write_pkg(tmp_path, bnd=bnd))
    assert any("non-empty list" in e for e in errors), errors


def test_invalid_observation_unit_is_caught(tmp_path):
    bnd = copy.deepcopy(MINIMAL_BND)
    bnd["operational_bindings"][0].update(
        {"target_type": "evaluation", "observation_unit": "campaign"})
    bnd["operational_bindings"][0].pop("governance_consumer")
    errors = check_source_dir(write_pkg(tmp_path, bnd=bnd))
    assert any("observation_unit" in e for e in errors), errors


def test_production_binding_with_a_target_path_is_caught(tmp_path):
    """PROJECT-CONTRACT separation 2: Production IR does not exist."""
    bnd = copy.deepcopy(MINIMAL_BND)
    bnd["operational_bindings"][0].update(
        {"target_type": "production", "status": "production_candidate",
         "target_path": "production.lighting"})
    bnd["operational_bindings"][0].pop("governance_consumer")
    errors = check_source_dir(write_pkg(tmp_path, bnd=bnd))
    assert any("target_path null" in e for e in errors), errors


def test_ontology_ref_resolving_to_nothing_is_caught(tmp_path):
    bnd = copy.deepcopy(MINIMAL_BND)
    bnd["operational_bindings"][0]["failure_ontology_refs"] = ["fo_not_a_real_identifier"]
    errors = check_source_dir(write_pkg(tmp_path, bnd=bnd))
    assert any("neither a term_id nor a concept_id" in e for e in errors), errors


def test_ontology_ref_to_a_concept_id_is_accepted(tmp_path):
    """Live accepted Canon binds canonical concepts, not only terms; both are SPEC-05 identifiers."""
    bnd = copy.deepcopy(MINIMAL_BND)
    bnd["operational_bindings"][0]["failure_ontology_refs"] = ["sc_demo_001"]
    assert check_source_dir(write_pkg(tmp_path, bnd=bnd)) == []


@pytest.mark.parametrize("field,bad", [
    ("kind", "source_specific_concept"),   # a CONCEPT kind wrongly used as a TERM kind
    ("origin", "extractor_assigned"),
])
def test_invalid_ontology_term_enums_are_caught(tmp_path, field, bad):
    ont = copy.deepcopy(MINIMAL_ONT)
    ont["terms"][0][field] = bad
    errors = check_source_dir(write_pkg(tmp_path, ont=ont))
    assert any(field in e or "term kind" in e or "term origin" in e for e in errors), (field, errors)


def test_invalid_ontology_relation_is_caught(tmp_path):
    ont = copy.deepcopy(MINIMAL_ONT)
    ont["relationships"][0]["relation"] = "supports"
    errors = check_source_dir(write_pkg(tmp_path, ont=ont))
    assert any("ontology relation" in e for e in errors), errors


def test_unresolvable_ontology_relation_endpoint_is_caught(tmp_path):
    ont = copy.deepcopy(MINIMAL_ONT)
    ont["relationships"][0]["to"] = "t_nope"
    errors = check_source_dir(write_pkg(tmp_path, ont=ont))
    assert any("does not resolve" in e for e in errors), errors


def test_repair_term_without_executable_by_is_caught(tmp_path):
    """SPEC-05: every repair term carries executable_by so the generative gap stays visible."""
    ont = copy.deepcopy(MINIMAL_ONT)
    del ont["terms"][2]["executable_by"]
    errors = check_source_dir(write_pkg(tmp_path, ont=ont))
    assert any("executable_by" in e for e in errors), errors


def test_invalid_repair_executor_is_caught(tmp_path):
    ont = copy.deepcopy(MINIMAL_ONT)
    ont["terms"][2]["executable_by"] = ["agency_process"]
    errors = check_source_dir(write_pkg(tmp_path, ont=ont))
    assert any("executable_by" in e for e in errors), errors


def test_invalid_concept_kind_is_caught(tmp_path):
    ont = copy.deepcopy(MINIMAL_ONT)
    ont["concepts"][0]["kind"] = "source_concept"
    errors = check_source_dir(write_pkg(tmp_path, ont=ont))
    assert any("concept kind" in e for e in errors), errors


def test_source_specific_concept_asserting_agreement_is_caught(tmp_path):
    """SPEC-05 governance rule 5: it may not be presented as agreement between sources."""
    ont = copy.deepcopy(MINIMAL_ONT)
    ont["concepts"][0]["asserts_agreement_between_sources"] = True
    errors = check_source_dir(write_pkg(tmp_path, ont=ont))
    assert any("must not assert agreement" in e for e in errors), errors


def test_canonical_concept_must_declare_asserts_equivalence_false(tmp_path):
    ont = copy.deepcopy(MINIMAL_ONT)
    ont["concepts"][0] = {"concept_id": "cc_demo", "kind": "canonical_concept", "label": "l",
                          "purpose": "retrieval_and_aggregation", "created_by": "extractor",
                          "children_terms": ["t_demo_0001"]}
    errors = check_source_dir(write_pkg(tmp_path, ont=ont))
    assert any("asserts_equivalence" in e for e in errors), errors


def test_cross_source_concept_needs_two_independent_origins(tmp_path):
    ont = copy.deepcopy(MINIMAL_ONT)
    ont["concepts"][0] = {"concept_id": "xs_demo", "kind": "cross_source_concept", "label": "l",
                          "definition": "d", "children_terms": ["t_demo_0001"],
                          "independent_origins": ["demo_source"]}
    errors = check_source_dir(write_pkg(tmp_path, ont=ont))
    assert any("2 or more independent_origins" in e for e in errors), errors


def test_cross_source_concept_duplicate_origins_are_caught(tmp_path):
    """Counting the same origin twice is the failure SPEC-05 governance rule 5 exists to prevent."""
    ont = copy.deepcopy(MINIMAL_ONT)
    ont["concepts"][0] = {"concept_id": "xs_demo", "kind": "cross_source_concept", "label": "l",
                          "definition": "d", "children_terms": ["t_demo_0001"],
                          "independent_origins": ["demo_source", "demo_source"]}
    errors = check_source_dir(write_pkg(tmp_path, ont=ont))
    assert any("duplicates" in e for e in errors), errors


def test_unresolvable_children_term_is_caught(tmp_path):
    ont = copy.deepcopy(MINIMAL_ONT)
    ont["concepts"][0]["children_terms"] = ["t_nope"]
    errors = check_source_dir(write_pkg(tmp_path, ont=ont))
    assert any("children_terms" in e for e in errors), errors


# ══════════════════════════════════════════════════════════════════════════════
# Required-field presence, parametrised so patching one field cannot satisfy the suite
# ══════════════════════════════════════════════════════════════════════════════

@pytest.mark.parametrize("field", [f for f in SK_REQUIRED if f != "source_id"])
def test_every_required_sk_field_is_checked(tmp_path, field):
    sk = copy.deepcopy(MINIMAL_SK)
    del sk["source_knowledge"][0][field]
    assert check_source_dir(write_pkg(tmp_path, sk=sk)), f"deleting SourceKnowledge.{field} passed"


@pytest.mark.parametrize("field", SK_EVIDENCE_REQUIRED)
def test_every_required_sk_evidence_field_is_checked(tmp_path, field):
    sk = copy.deepcopy(MINIMAL_SK)
    del sk["source_knowledge"][0]["evidence"][field]
    errors = check_source_dir(write_pkg(tmp_path, sk=sk))
    assert any(f"evidence.{field}" in e for e in errors), (field, errors)


@pytest.mark.parametrize("field", [f for f in SCS_REQUIRED if f != "source_id"])
def test_every_required_scs_field_is_checked(tmp_path, field):
    scs = copy.deepcopy(MINIMAL_SCS)
    del scs["source_concept_systems"][0][field]
    assert check_source_dir(write_pkg(tmp_path, scs=scs)), f"deleting {field} passed"


@pytest.mark.parametrize("field", SCS_EVIDENCE_REQUIRED)
def test_every_required_scs_evidence_field_is_checked(tmp_path, field):
    scs = copy.deepcopy(MINIMAL_SCS)
    del scs["source_concept_systems"][0]["evidence"][field]
    errors = check_source_dir(write_pkg(tmp_path, scs=scs))
    assert any(f"evidence.{field}" in e for e in errors), (field, errors)


# ══════════════════════════════════════════════════════════════════════════════
# Structural rules that must keep holding
# ══════════════════════════════════════════════════════════════════════════════

def test_bare_list_file_without_top_level_source_id_is_caught(tmp_path):
    d = write_pkg(tmp_path)
    (tmp_path / "demo-source" / "source-knowledge.yaml").write_text(
        yaml.safe_dump(MINIMAL_SK["source_knowledge"], sort_keys=False), encoding="utf-8")
    errors = check_source_dir(d)
    assert any("no top-level source_id" in e for e in errors), errors


def test_extractor_synthesis_without_interpretation_basis_is_caught(tmp_path):
    scs = copy.deepcopy(MINIMAL_SCS)
    del scs["source_concept_systems"][0]["whole_system_claim"]["interpretation_basis"]
    errors = check_source_dir(write_pkg(tmp_path, scs=scs))
    assert any("interpretation_basis" in e for e in errors), errors


def test_source_interpretation_without_interpretation_basis_is_caught(tmp_path):
    sk = copy.deepcopy(MINIMAL_SK)
    sk["source_knowledge"][0]["claim_type"] = "source_interpretation"
    errors = check_source_dir(write_pkg(tmp_path, sk=sk))
    assert any("interpretation_basis" in e for e in errors), errors


def test_visual_support_without_inspected_figures_is_caught(tmp_path):
    """SPEC-03 rule 4."""
    sk = copy.deepcopy(MINIMAL_SK)
    sk["source_knowledge"][0]["provenance"]["source_support"] = "visual"
    errors = check_source_dir(write_pkg(tmp_path, sk=sk))
    assert any("SPEC-03 rule 4" in e for e in errors), errors


def test_provenance_with_no_locator_at_all_is_caught(tmp_path):
    sk = copy.deepcopy(MINIMAL_SK)
    for k in ("locator", "chapter", "section"):
        sk["source_knowledge"][0]["provenance"][k] = None
    errors = check_source_dir(write_pkg(tmp_path, sk=sk))
    assert any("neither a page range nor an equivalent locator" in e for e in errors), errors


def test_missing_visual_ledger_is_caught_when_required(tmp_path):
    d = write_pkg(tmp_path)
    errors = check_source_dir(d, require_visual_ledger=True)
    assert any("visual-evidence-ledger" in e for e in errors), errors


# ══════════════════════════════════════════════════════════════════════════════
# The corpus itself
# ══════════════════════════════════════════════════════════════════════════════

def test_canon014_candidates_are_conformant():
    """The two sources this lane brings to READY must be clean."""
    for d in ("parameswaran-nawabs-nudes-noodles", "pandey-pandeymonium"):
        p = os.path.join(REPO, "canon", "knowledge", "current", d)
        if not os.path.isdir(p):
            pytest.skip(f"{d} not present on this branch")
        assert check_source_dir(p, require_visual_ledger=True) == [], d


def test_held_desai_candidate_is_structurally_conformant():
    """HOLD is an evidence judgement, not a structural excuse: the held material still conforms."""
    p = os.path.join(REPO, "canon", "candidates", "canon-014", "desai-mother-pious-lady")
    if not os.path.isdir(p):
        pytest.skip("held candidate not present on this branch")
    assert check_source_dir(p, require_visual_ledger=True) == []


def test_live_canon_scs_provenance_defect_is_recorded_not_silently_fixed():
    """CANON-014 finding F-01.

    Three SourceConceptSystems in the accepted `sutherland-alchemy-introduction` have no
    `provenance`, which SPEC-03 requires. This lane is not authorised to edit accepted knowledge,
    and editing it would stale its audit record, so the defect is routed to the Controller. This
    test pins it: if someone repairs the source WITHOUT re-running the Audit Gate, or if a NEW live
    defect appears, this fails and forces the finding to be revisited.
    """
    root = os.path.join(REPO, "canon", "knowledge", "current")
    if not os.path.isdir(root):
        pytest.skip("live canon not present")
    errors, _ = check_package(root)
    sutherland = [e for e in errors if "sutherland-alchemy-introduction" in e]
    others = [e for e in errors if "sutherland-alchemy-introduction" not in e]
    assert others == [], f"a NEW live-Canon defect appeared: {others}"
    assert len(sutherland) == 3, sutherland
    assert all("provenance" in e for e in sutherland), sutherland
