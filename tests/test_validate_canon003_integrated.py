import tempfile
import unittest
from pathlib import Path

import yaml

from canon.validation import validate_canon003_integrated as validator


class Canon003IntegrationValidatorTests(unittest.TestCase):
    def _write_yaml(self, path: Path, data):
        path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")

    def _make_valid_book(self, root: Path) -> Path:
        book = root / "fixture-book"
        book.mkdir(parents=True)
        (book / "PROVENANCE.md").write_text("# Fixture provenance\n\nPrinted page 1.\n", encoding="utf-8")

        self._write_yaml(book / "source-knowledge.yaml", {
            "source_id": "fixture_source",
            "source_knowledge": [{
                "sk_id": "sk_fixture_001",
                "source_id": "fixture_source",
                "source_terms": ["fixture"],
                "concept_label": "fixture_claim",
                "label_origin": "extractor_assigned",
                "claim": "A fixture claim.",
                "claim_type": "explicit_source_claim",
                "interpretation_basis": None,
                "mechanism": {"stated_by_source": False, "text": None},
                "scope": {"domain_discussed_by_source": ["fixture"], "conditions": "fixture"},
                "caveats": [{"text": "fixture caveat", "origin": "extractor_observed"}],
                "source_stated_problems": [],
                "source_stated_remedies": [],
                "examples": {"positive": [], "counter": []},
                "intra_source_relations": [],
                "evidence": {
                    "characteristics": ["explicitly_stated", "mechanism_absent"],
                    "source_uncertainty": "none",
                    "extraction_uncertainty": "none",
                },
                "provenance": {
                    "section": "Fixture",
                    "page_start": 1,
                    "page_end": 1,
                    "figure_refs": [],
                    "source_support": "text",
                    "inspected": {"text": True, "figures": []},
                },
            }],
        })

        self._write_yaml(book / "source-concept-systems.yaml", {
            "source_id": "fixture_source",
            "source_concept_systems": [{
                "scs_id": "scs_fixture_001",
                "source_id": "fixture_source",
                "label": "fixture_sequence",
                "label_origin": "extractor_assigned",
                "system_type": "sequence",
                "system_type_origin": "source_stated",
                "description": "Fixture sequence.",
                "whole_system_claim": {
                    "text": "The fixture is ordered.",
                    "origin": "source_explicit",
                    "interpretation_basis": None,
                    "source_ref": {"page_start": 1},
                },
                "members": [{
                    "sk_ref": "sk_fixture_001",
                    "role_in_system": "step",
                    "order": 1,
                    "membership_origin": "source_stated",
                }],
                "internal_structure": {
                    "ordering": {"scheme": "source_numbered", "origin": "source_stated"},
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
                    "system_level_uncertainty": None,
                },
                "provenance": {"section": "Fixture", "page_start": 1, "page_end": 1, "source_support": "text"},
            }],
        })

        self._write_yaml(book / "ontology-mappings.yaml", {
            "source_id": "fixture_source",
            "extraction_date": "2026-08-24",
            "terms": [{
                "term_id": "t_fixture_001",
                "term": "fixture_problem",
                "origin": "source",
                "origin_ref": "fixture_source",
                "kind": "problem",
                "definition_in_origin_frame": "A fixture problem.",
                "first_seen": "2026-08-24",
                "verbatim": False,
                "source_ref": {"page_start": 1},
                "arising_from": ["sk_fixture_001"],
            }],
            "relationships": [],
            "concepts": [{
                "concept_id": "sc_fixture_001",
                "kind": "source_specific_concept",
                "origin_ref": "fixture_source",
                "children_terms": ["t_fixture_001"],
                "origin": "source_stated",
            }],
        })

        self._write_yaml(book / "operational-bindings.yaml", {
            "source_id": "fixture_source",
            "derived_against": {"schema": "SPEC-01", "version": "v0.1"},
            "operational_bindings": [{
                "binding_id": "bnd_fixture_001",
                "source_knowledge_refs": ["sk_fixture_001"],
                "source_system_refs": [],
                "target_type": "evaluation",
                "target_path": None,
                "role": ["evaluates"],
                "observation_unit": "frame",
                "rationale": "Fixture evaluation.",
                "applicability": {"when": "fixture", "limits": "fixture"},
                "evidence_basis": "derived_from_source",
                "empirical_refs": [],
                "failure_ontology_refs": ["t_fixture_001"],
                "repair_ontology_refs": [],
                "status": "proposed",
                "status_reason": "fixture",
            }],
        })

        self._write_yaml(book / "visual-evidence-ledger.yaml", {
            "source_id": "fixture_source",
            "pass": "independent_visual_evidence",
            "visual_completeness": "verified_page_level",
            "demonstrations": [],
        })
        return book

    def test_valid_minimal_book_has_no_errors(self):
        with tempfile.TemporaryDirectory() as td:
            book = self._make_valid_book(Path(td))
            self.assertEqual([], validator.validate_book_dir(book))

    def test_unresolved_system_member_is_reported(self):
        with tempfile.TemporaryDirectory() as td:
            book = self._make_valid_book(Path(td))
            systems_path = book / "source-concept-systems.yaml"
            data = yaml.safe_load(systems_path.read_text(encoding="utf-8"))
            data["source_concept_systems"][0]["members"][0]["sk_ref"] = "sk_missing"
            self._write_yaml(systems_path, data)
            errors = validator.validate_book_dir(book)
            self.assertTrue(any("unresolved SourceKnowledge ref sk_missing" in e for e in errors), errors)

    def test_invalid_binding_target_and_governance_consumer_are_reported(self):
        with tempfile.TemporaryDirectory() as td:
            book = self._make_valid_book(Path(td))
            bindings_path = book / "operational-bindings.yaml"
            data = yaml.safe_load(bindings_path.read_text(encoding="utf-8"))
            binding = data["operational_bindings"][0]
            binding["target_type"] = "governance"
            binding.pop("observation_unit")
            binding["governance_consumer"] = "misc_junk_drawer"
            self._write_yaml(bindings_path, data)
            errors = validator.validate_book_dir(book)
            self.assertTrue(any("invalid governance_consumer misc_junk_drawer" in e for e in errors), errors)

    def test_invalid_ontology_relation_and_executor_are_reported(self):
        with tempfile.TemporaryDirectory() as td:
            book = self._make_valid_book(Path(td))
            ontology_path = book / "ontology-mappings.yaml"
            data = yaml.safe_load(ontology_path.read_text(encoding="utf-8"))
            data["terms"][0]["kind"] = "remedy"
            data["terms"][0]["executable_by"] = ["magic_prompt"]
            data["relationships"] = [{
                "from": "t_fixture_001", "to": "t_fixture_001",
                "relation": "same_vibes", "confidence_basis": "extractor_judgement"
            }]
            self._write_yaml(ontology_path, data)
            errors = validator.validate_book_dir(book)
            self.assertTrue(any("invalid executable_by magic_prompt" in e for e in errors), errors)
            self.assertTrue(any("invalid ontology relation same_vibes" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
