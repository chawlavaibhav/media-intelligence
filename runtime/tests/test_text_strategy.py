"""The exact-text strategy is chosen BY RULE, and the rules live in the evidence map."""
from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

import yaml

from runtime import paths
from runtime.canon.normalize import NormalizedRequest, normalize
from runtime.errors import Refusal
from runtime.evidence import EvidenceMap
from runtime.spec import text_strategy
from runtime.tests import support


def request(**facets) -> NormalizedRequest:
    base = {
        "exact_text_present": True,
        "exactness_contractual": True,
        "text_in_scene": False,
        "script_beyond_latin": True,
        "scripts": ["devanagari"],
        "text_must_move": False,
        "product_entity_present": True,
        "supplied_asset_present": True,
        "identity_bound_roles": ["product"],
        "market": "IN",
    }
    base.update(facets)
    return NormalizedRequest(
        requested_operation="generate",
        supplied_assets=[],
        deliverable_set={},
        modality=facets.pop("modality", "static_image"),
        entities=[],
        text_requirements=[{"id": "t1", "content": "₹185 प्रति लीटर"}] if base["exact_text_present"] else [],
        language_topology=None,
        temporal_structure=None,
        delivery={},
        specification_provenance={},
        ambiguity_markers=[],
        acceptance_intent=None,
        market="IN",
        facets=base,
    )


class StrategyChoiceTest(unittest.TestCase):
    def test_a_contractual_devanagari_price_line_gets_code_set_text(self):
        chosen = text_strategy.choose(request())
        self.assertEqual(chosen.strategy, "code_set_on_textless_plate")
        self.assertEqual(chosen.rule_id, "RR-1")
        self.assertIn("RR-1", chosen.strategy_basis)
        self.assertIn("IMG-TEXT/", chosen.strategy_basis)  # the map cell is named, as the contract asks

    def test_the_real_mustard_oil_brief_gets_code_set_text(self):
        job = support.submit("mustard-oil-tin")
        chosen = text_strategy.choose(normalize(job))
        self.assertEqual(chosen.strategy, "code_set_on_textless_plate")
        self.assertIn("exactness_contractual", chosen.facets_active)
        self.assertIn("script_devanagari", chosen.facets_active)

    def test_the_rr3_routes_are_refused_for_devanagari_the_maker_would_draw(self):
        chosen = text_strategy.choose(request(text_in_scene=True, exactness_contractual=False))
        self.assertEqual(chosen.strategy, "generated_in_scene")
        self.assertEqual(chosen.prohibited_routes, ("flux-2-pro", "recraft-v4", "seedream-5-pro"))
        for route in chosen.prohibited_routes:
            self.assertFalse(any(route in cell for cell in chosen.map_cells), cell_msg(chosen, route))
        self.assertTrue(chosen.map_cells)  # something is still allowed to make it

    def test_a_route_prohibition_about_lettering_does_not_bite_when_code_sets_the_lettering(self):
        chosen = text_strategy.choose(request())
        self.assertEqual(chosen.prohibited_routes, ())
        self.assertIn(("RR-3", ("flux-2-pro", "recraft-v4", "seedream-5-pro"), True), chosen.prohibitions)

    def test_text_that_must_move_is_never_drawn_by_the_maker(self):
        chosen = text_strategy.choose(request(text_must_move=True))
        self.assertEqual(chosen.strategy, "code_set_on_textless_plate")
        self.assertEqual(chosen.rule_id, "RR-6")

    def test_no_exact_string_means_no_lettering_strategy_at_all(self):
        chosen = text_strategy.choose(request(exact_text_present=False, exactness_contractual=False,
                                              script_beyond_latin=False, scripts=[]))
        self.assertEqual(chosen.strategy, "no_exact_text")
        self.assertEqual(chosen.map_cells, ())

    def test_the_same_request_chooses_the_same_strategy_every_time(self):
        first = text_strategy.choose(request())
        second = text_strategy.choose(request())
        self.assertEqual(first.strategy, second.strategy)
        self.assertEqual(first.strategy_basis, second.strategy_basis)


class RulesLiveInTheMapTest(unittest.TestCase):
    """The rules will change. The code must not have to."""

    def test_rewriting_rr3_in_the_map_changes_the_outcome_with_no_code_edit(self):
        doc = yaml.safe_load(Path(paths.EVIDENCE_MAP).read_text(encoding="utf-8"))
        for rule in doc["routing_rules"]:
            if rule["id"] == "RR-3":
                rule["rule"] = "Avoid Qwen Image 3 for Devanagari text."
        edited = Path(tempfile.mkdtemp(prefix="runtime-map-")) / "ROUTING-EVIDENCE-MAP-v0.yaml"
        edited.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False), encoding="utf-8")

        evidence = EvidenceMap(map_path=edited)
        chosen = text_strategy.choose(request(text_in_scene=True, exactness_contractual=False), evidence)
        self.assertEqual(chosen.prohibited_routes, ("qwen-image-3",))
        cells = " ".join(chosen.map_cells)
        self.assertIn("seedream", cells)        # no longer excluded by the rewritten rule
        self.assertNotIn("qwen", cells)         # excluded by it instead

    def test_a_rule_out_of_scope_is_not_applied(self):
        """RR-3 is about Devanagari. A Latin-only job must not inherit its prohibition."""
        chosen = text_strategy.choose(
            request(text_in_scene=True, exactness_contractual=False, script_beyond_latin=False, scripts=["latin"])
        )
        self.assertEqual(chosen.strategy, "generated_in_scene")
        self.assertEqual(chosen.prohibited_routes, ())


def cell_msg(chosen, route) -> str:
    return f"{route} survived in {chosen.map_cells}"


if __name__ == "__main__":
    unittest.main()
