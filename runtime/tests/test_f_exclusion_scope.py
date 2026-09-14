"""A scoped route exclusion bites only what it names (lane F, 14 Sep 2026; lead-found defect).

THE DEFECT. RR-3 forbids certain routes from DRAWING Devanagari text. PRODUCTION-SPEC-v1 gave
route_exclusions a `scope` for exactly this reason (`generated_text_only` versus `whole_route`), but
the router's Exclusion had no scope field and stage 1 dropped the whole route. On the overlay job -
where the model draws no text at all, code composes it onto a textless plate - that deleted flux-2-pro,
the cheapest plate route the project has (USD 0.03), although nothing is drawn.

THE RULE NOW. An exclusion with scope generated_text_only bites a dispatching candidate only when the
spec's exact_text.text_mechanism is model_draws_text, or when the spec carries no text_mechanism and a
text requirement exists (fail closed: if we cannot tell whether the model draws the text, assume it
does). Otherwise it is recorded as `scoped_out`, with the reason, in exclusions_applied - seen, not
silently ignored. scope whole_route (and an absent scope) keeps the old behaviour.
"""
from __future__ import annotations

import copy
import unittest
from pathlib import Path

import _bootstrap as B
from runtime.route.spec import Spec, load_spec


def _spec_with(path: Path, mutate) -> Spec:
    data = copy.deepcopy(load_spec(path).data)
    mutate(data)
    return Spec(path=path, data=data)


class OverlayKeepsThePlateRoute(unittest.TestCase):
    def setUp(self):
        self.d = B.plan(B.SPEC_STATIC_OVERLAY, "alpha_human_release")
        self.by_route = {c["route_key"]: c for c in self.d["selection_basis"]["candidates_considered"]}

    def test_flux_2_pro_is_a_kept_candidate_for_the_textless_plate(self):
        self.assertIn("flux-2-pro", self.by_route)
        self.assertTrue(self.by_route["flux-2-pro"]["kept"], self.by_route["flux-2-pro"]["why"])

    def test_the_cheapest_plate_route_becomes_primary(self):
        self.assertFalse(self.d["manual_route_required"], self.d["manual_route_reason"])
        self.assertEqual(self.d["primary"]["route_key"], "flux-2-pro")
        self.assertEqual(self.d["primary"]["expected_cost_usd"], "0.030000")

    def test_the_scoped_out_exclusion_is_shown_not_hidden(self):
        rows = [e for e in self.d["exclusions_applied"] if e["route_key"] == "flux-2-pro"]
        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row["scope"], "generated_text_only")
            self.assertEqual(row["effect"], "scoped_out")
            self.assertIn("deterministic_text_composition", row["scope_reason"])
            self.assertIn("IMG-CORE/flux-2-pro", row["would_have_supplied"])

    def test_the_same_scoped_exclusion_still_bites_a_route_that_would_draw_text(self):
        """The in-scene fixture carries the same three RR-3 exclusions with the same scope; there the
        model draws the price line, so the scope bites. flux-2-pro is out of that job before the
        exclusion is even reached (its only model-draws-text cell is not an in-scene arm), so the route
        the exclusion visibly removes is seedream-5-pro, which does cover both requirements."""
        d = B.plan(B.SPEC_STATIC_IN_SCENE, "alpha_wider_example")
        by_route = {c["route_key"]: c for c in d["selection_basis"]["candidates_considered"]}
        self.assertFalse(by_route["flux-2-pro"]["kept"])
        self.assertEqual(by_route["flux-2-pro"]["dropped_at"], "hard_requirements")
        self.assertFalse(by_route["seedream-5-pro"]["kept"])
        bit = [e for e in d["exclusions_applied"] if e["route_key"] == "seedream-5-pro"]
        self.assertTrue(bit)
        self.assertTrue(all(e["effect"] == "neither primary nor fallback" for e in bit))
        self.assertTrue(all(e["scope"] == "generated_text_only" for e in bit))
        self.assertTrue(all("model_draws_text" in e["scope_reason"] for e in bit))
        for slot in (d["primary"], d["fallback"]):
            if slot:
                self.assertNotIn(slot["route_key"], ("flux-2-pro", "seedream-5-pro", "recraft-v4"))


class FailClosed(unittest.TestCase):
    def test_no_text_mechanism_on_the_spec_means_the_exclusion_bites(self):
        """A spec with exact strings but no text_mechanism cannot prove the model draws nothing, so a
        generated_text_only exclusion is applied to the whole route."""
        def strip(data):
            data["exact_text"].pop("text_mechanism", None)
        d = B.router().plan(_spec_with(B.SPEC_STATIC_OVERLAY, strip), B.profile("alpha_human_release"))
        by_route = {c["route_key"]: c for c in d["selection_basis"]["candidates_considered"]}
        self.assertFalse(by_route["flux-2-pro"]["kept"])
        rows = [e for e in d["exclusions_applied"] if e["route_key"] == "flux-2-pro"]
        self.assertTrue(rows)
        self.assertTrue(all(e["effect"] == "neither primary nor fallback" for e in rows))
        self.assertTrue(any("fail closed" in (e.get("scope_reason") or "") for e in rows))

    def test_an_exclusion_with_no_scope_is_whole_route(self):
        def unscope(data):
            for e in data["route_exclusions"]:
                e.pop("scope", None)
        spec = _spec_with(B.SPEC_STATIC_OVERLAY, unscope)
        self.assertTrue(all(e.scope == "whole_route" for e in spec.exclusions()))
        d = B.router().plan(spec, B.profile("alpha_human_release"))
        by_route = {c["route_key"]: c for c in d["selection_basis"]["candidates_considered"]}
        self.assertFalse(by_route["flux-2-pro"]["kept"])

    def test_an_unknown_scope_is_treated_as_whole_route_and_reported(self):
        def weird(data):
            data["route_exclusions"][2]["scope"] = "only_on_tuesdays"
        d = B.router().plan(_spec_with(B.SPEC_STATIC_OVERLAY, weird), B.profile("alpha_human_release"))
        by_route = {c["route_key"]: c for c in d["selection_basis"]["candidates_considered"]}
        self.assertFalse(by_route["flux-2-pro"]["kept"])
        rows = [e for e in d["exclusions_applied"] if e["route_key"] == "flux-2-pro"]
        self.assertTrue(any("not a scope the router knows" in (e.get("scope_reason") or "") for e in rows))

    def test_a_whole_route_exclusion_still_bites_whatever_the_mechanism(self):
        """The motion fixture excludes veo-3.1-fast-i2v for camera movement, scope whole_route."""
        d = B.plan(B.SPEC_MOTION, "alpha_human_release")
        by_route = {c["route_key"]: c for c in d["selection_basis"]["candidates_considered"]}
        self.assertFalse(by_route["veo-3.1-fast-i2v"]["kept"])
        rows = [e for e in d["exclusions_applied"] if e["route_key"] == "veo-3.1-fast-i2v"]
        self.assertTrue(all(e["scope"] == "whole_route" for e in rows))


if __name__ == "__main__":
    unittest.main()
