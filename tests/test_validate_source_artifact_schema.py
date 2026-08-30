"""Tests for the CANON-014 required-field validator.

The regression these tests exist for
------------------------------------
The CANON-013-era experimental validator reported PASS on a package in which `scs_sa8_002` was
missing SPEC-03's required `evidence.system_level_uncertainty`, because that validator never
checked required-field presence for SourceConceptSystem at all. `test_missing_system_level_
uncertainty_is_caught` is the direct regression test; the tests around it assert that the same
protection covers every other required field of every artifact, so that patching one field could
not have satisfied the suite.
"""

import copy
import os
import sys
import textwrap

import pytest
import yaml

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from canon.validation.validate_source_artifact_schema import (  # noqa: E402
    SCS_EVIDENCE_REQUIRED,
    SCS_REQUIRED,
    SK_EVIDENCE_REQUIRED,
    SK_REQUIRED,
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
            "scope": {"domain_discussed_by_source": ["demo"], "conditions": "demo"},
            "caveats": [{"text": "a caveat", "origin": "source_stated"}],
            "evidence": {
                "characteristics": ["explicitly_stated"],
                "source_uncertainty": "none",
                "extraction_uncertainty": "none",
            },
            "provenance": {
                "chapter": "1",
                "section": "opening",
                "page_start": None,
                "page_end": None,
                "locator": "ch.1 opening",
                "source_support": "text",
                "inspected": {"text": True, "figures": []},
            },
        }
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
                "dependencies": [],
                "tradeoffs": [],
                "conflicts": [],
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

MINIMAL_BND = {"source_id": "demo_source", "operational_bindings": []}
MINIMAL_ONT = {"source_id": "demo_source", "terms": [], "relationships": [], "concepts": []}


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


# ── the direct regression ─────────────────────────────────────────────────────

def test_missing_system_level_uncertainty_is_caught(tmp_path):
    """The exact omission the previous validator let through as PASS."""
    scs = copy.deepcopy(MINIMAL_SCS)
    del scs["source_concept_systems"][0]["evidence"]["system_level_uncertainty"]
    errors = check_source_dir(write_pkg(tmp_path, scs=scs))
    assert any("system_level_uncertainty" in e for e in errors), errors


# ── and the whole class it belongs to ─────────────────────────────────────────

@pytest.mark.parametrize("field", SCS_EVIDENCE_REQUIRED)
def test_every_required_scs_evidence_field_is_checked(tmp_path, field):
    scs = copy.deepcopy(MINIMAL_SCS)
    del scs["source_concept_systems"][0]["evidence"][field]
    errors = check_source_dir(write_pkg(tmp_path, scs=scs))
    assert any(f"evidence.{field}" in e for e in errors), (field, errors)


@pytest.mark.parametrize("field", [f for f in SCS_REQUIRED if f != "source_id"])
def test_every_required_scs_field_is_checked(tmp_path, field):
    scs = copy.deepcopy(MINIMAL_SCS)
    del scs["source_concept_systems"][0][field]
    errors = check_source_dir(write_pkg(tmp_path, scs=scs))
    assert errors, f"deleting SourceConceptSystem.{field} produced no error"


@pytest.mark.parametrize("field", [f for f in SK_REQUIRED if f != "source_id"])
def test_every_required_sk_field_is_checked(tmp_path, field):
    sk = copy.deepcopy(MINIMAL_SK)
    del sk["source_knowledge"][0][field]
    errors = check_source_dir(write_pkg(tmp_path, sk=sk))
    assert errors, f"deleting SourceKnowledge.{field} produced no error"


@pytest.mark.parametrize("field", SK_EVIDENCE_REQUIRED)
def test_every_required_sk_evidence_field_is_checked(tmp_path, field):
    sk = copy.deepcopy(MINIMAL_SK)
    del sk["source_knowledge"][0]["evidence"][field]
    errors = check_source_dir(write_pkg(tmp_path, sk=sk))
    assert any(f"evidence.{field}" in e for e in errors), (field, errors)


# ── the other two defect classes CANON-014 found ──────────────────────────────

@pytest.mark.parametrize("key", ["dependencies", "tradeoffs", "conflicts"])
def test_structural_entry_without_origin_is_caught(tmp_path, key):
    """SPEC-03 requires an origin at every structural level; 84 entries lacked one."""
    scs = copy.deepcopy(MINIMAL_SCS)
    scs["source_concept_systems"][0]["internal_structure"][key] = [
        {"between": ["sk_demo_0001"], "nature": "x"}
    ]
    errors = check_source_dir(write_pkg(tmp_path, scs=scs))
    assert any(f"{key} entry missing origin" in e for e in errors), errors


def test_member_without_membership_origin_is_caught(tmp_path):
    scs = copy.deepcopy(MINIMAL_SCS)
    del scs["source_concept_systems"][0]["members"][0]["membership_origin"]
    errors = check_source_dir(write_pkg(tmp_path, scs=scs))
    assert any("membership_origin" in e for e in errors), errors


def test_bare_list_file_without_top_level_source_id_is_caught(tmp_path):
    """Audit Gate rule 2 resolves source_id out of the file; a bare list has nowhere to hold it."""
    d = write_pkg(tmp_path)
    (tmp_path / "demo-source" / "source-knowledge.yaml").write_text(
        yaml.safe_dump(MINIMAL_SK["source_knowledge"], sort_keys=False), encoding="utf-8")
    errors = check_source_dir(d)
    assert any("no top-level source_id" in e for e in errors), errors


# ── SPEC-03/04 rules that must keep holding ───────────────────────────────────

def test_unresolvable_member_ref_is_caught(tmp_path):
    scs = copy.deepcopy(MINIMAL_SCS)
    scs["source_concept_systems"][0]["members"][0]["sk_ref"] = "sk_does_not_exist"
    errors = check_source_dir(write_pkg(tmp_path, scs=scs))
    assert any("does not resolve" in e for e in errors), errors


def test_extractor_synthesis_without_interpretation_basis_is_caught(tmp_path):
    scs = copy.deepcopy(MINIMAL_SCS)
    del scs["source_concept_systems"][0]["whole_system_claim"]["interpretation_basis"]
    errors = check_source_dir(write_pkg(tmp_path, scs=scs))
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


def test_production_binding_must_not_carry_a_target_path(tmp_path):
    """PROJECT-CONTRACT separation 2: Production IR does not exist."""
    bnd = {"source_id": "demo_source", "operational_bindings": [{
        "binding_id": "bnd_demo_001",
        "source_knowledge_refs": ["sk_demo_0001"],
        "target_type": "production",
        "target_path": "production.lighting",
        "role": ["derives"],
        "rationale": "x",
        "evidence_basis": "derived_from_source",
        "status": "production_candidate",
    }]}
    errors = check_source_dir(write_pkg(tmp_path, bnd=bnd))
    assert any("target_path null" in e for e in errors), errors


def test_evaluation_binding_requires_observation_unit(tmp_path):
    bnd = {"source_id": "demo_source", "operational_bindings": [{
        "binding_id": "bnd_demo_002",
        "source_knowledge_refs": ["sk_demo_0001"],
        "target_type": "evaluation",
        "role": ["diagnoses"],
        "rationale": "x",
        "evidence_basis": "derived_from_source",
        "status": "proposed",
    }]}
    errors = check_source_dir(write_pkg(tmp_path, bnd=bnd))
    assert any("observation_unit" in e for e in errors), errors


def test_benchmark_target_type_is_accepted(tmp_path):
    """13 bindings across ACCEPTED live Canon use it; SPEC-04 never enumerates its fixed list."""
    bnd = {"source_id": "demo_source", "operational_bindings": [{
        "binding_id": "bnd_demo_003",
        "source_knowledge_refs": ["sk_demo_0001"],
        "target_type": "benchmark",
        "role": ["diagnoses"],
        "rationale": "x",
        "evidence_basis": "derived_from_source",
        "status": "proposed",
    }]}
    assert check_source_dir(write_pkg(tmp_path, bnd=bnd)) == []


# ── the repaired experimental package, and the live corpus ────────────────────

def test_repaired_experimental_package_is_conformant():
    root = os.path.join(REPO, "canon", "experimental", "book-expansion-qa-v1")
    if not os.path.isdir(root):
        pytest.skip("experimental package not present on this branch")
    from canon.validation.validate_source_artifact_schema import check_package
    errors, n = check_package(root)
    assert n == 17
    assert errors == [], errors


def test_live_canon_scs_provenance_defect_is_recorded_not_silently_fixed():
    """CANON-014 finding F-03.

    Running the corrected validator over ACCEPTED live Canon finds three SourceConceptSystems in
    `sutherland-alchemy-introduction` with no `provenance` field, which SPEC-03 requires. CANON-014
    is not authorised to edit accepted knowledge, and editing it would stale its audit record, so
    the defect is routed to the Controller. This test pins the finding: if someone repairs the
    source WITHOUT re-running the Audit Gate, or if the defect count changes, this fails and forces
    the finding to be revisited.
    """
    root = os.path.join(REPO, "canon", "knowledge", "current")
    if not os.path.isdir(root):
        pytest.skip("live canon not present")
    from canon.validation.validate_source_artifact_schema import check_package
    errors, _ = check_package(root)
    sutherland = [e for e in errors if "sutherland-alchemy-introduction" in e]
    others = [e for e in errors if "sutherland-alchemy-introduction" not in e]
    assert others == [], f"a NEW live-Canon defect appeared: {others}"
    assert len(sutherland) == 3, sutherland
    assert all("provenance" in e for e in sutherland), sutherland
