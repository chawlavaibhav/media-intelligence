"""The evidence gate: what may be auto-routed, what may not, and who decides.

The register is the authority. The profile may be stricter than the register and may never be
looser: even a profile that listed `awaiting_controller_ruling` as auto-routable would not get such a
cell routed, because that is an invariant of ROUTE-DECISION-v0 rather than a policy choice.
"""
from __future__ import annotations

import unittest

import _bootstrap as B


class CleanCellAutoRoutes(unittest.TestCase):
    def test_a_clean_priced_cell_is_selected_with_a_declared_fallback(self):
        d = B.plan(B.SPEC_MOTION, "alpha_wider_example")
        self.assertFalse(d["manual_route_required"], d["manual_route_reason"])
        self.assertEqual(d["primary"]["route_key"], "minimax-h3-max-i2v")
        self.assertEqual(d["primary"]["evidence_status"], "clean_observed")
        self.assertEqual(d["primary"]["evidence_cells"], ["VID-I2V/minimax-h3-max-i2v"])
        self.assertIsNotNone(d["fallback"])
        self.assertNotEqual(d["fallback"]["route_key"], d["primary"]["route_key"])

    def test_the_fallback_is_declared_before_dispatch_with_named_triggers(self):
        d = B.plan(B.SPEC_MOTION, "alpha_wider_example")
        self.assertEqual(sorted(d["fallback"]["trigger"]),
                         ["capability_unsupported", "gate_fail", "provider_refusal", "timeout"])

    def test_cost_orders_the_survivors_and_never_rescues_a_dropped_route(self):
        d = B.plan(B.SPEC_MOTION, "alpha_wider_example")
        kept = [c for c in d["selection_basis"]["candidates_considered"] if c["kept"]]
        costs = [c["price"]["expected_cost_usd"] for c in kept]
        self.assertEqual(d["primary"]["expected_cost_usd"], min(costs))
        dropped = [c for c in d["selection_basis"]["candidates_considered"] if not c["kept"]]
        self.assertTrue(all(c["dropped_at"] in ("hard_requirements", "evidence_envelope", "price")
                            for c in dropped))


class AwaitingControllerRuling(unittest.TestCase):
    def test_a_blocked_cell_names_its_ruling_and_produces_manual_route_required(self):
        d = B.plan(B.SPEC_STATIC_OVERLAY, "alpha_wider_example")
        self.assertTrue(d["manual_route_required"])
        self.assertIn("C-6c", d["manual_route_reason"])
        blocked = [u for u in d["unsupported_requirements"]
                   if u["capability"] == "exact_text_composition"]
        self.assertEqual(len(blocked), 1)
        self.assertEqual(blocked[0]["blocking"], ["C-6c"])

    def test_dropped_candidates_name_the_ruling_that_blocks_them(self):
        d = B.plan(B.SPEC_STATIC_OVERLAY, "alpha_wider_example")
        by_route = {c["route_key"]: c for c in d["selection_basis"]["candidates_considered"]}
        self.assertEqual(by_route["nano-banana-2"]["dropped_at"], "evidence_envelope")
        self.assertIn("C-4", " ".join(by_route["nano-banana-2"]["why"]))
        self.assertIn("C-6b", " ".join(by_route["qwen-image-3"]["why"]))

    def test_a_profile_cannot_loosen_the_register(self):
        """A profile that DID list awaiting_controller_ruling still would not auto-route such a cell.

        No shipped profile lists it today; the point is that the invariant does not depend on that.
        """
        ev = B.evidence_base()
        blocked = ev.cells["VID-I2V/wan-2.2-a14b-i2v"]
        permissive = ev.status_vocabulary                      # every status the register knows
        self.assertIn("awaiting_controller_ruling", permissive)
        gate = ev.gate(blocked, permissive)
        self.assertFalse(gate.allowed)
        self.assertIn("C-6b", gate.reason)
        self.assertIn("never auto-routed", gate.reason)

    def test_production_use_allowed_false_blocks_even_a_clean_cell(self):
        ev = B.evidence_base()
        cell = ev.cells["IMG-REF/flux-2-pro-edit"]
        self.assertEqual(cell.evidence_status, "clean_observed")
        gate = ev.gate(cell, ["clean_observed"])
        self.assertFalse(gate.allowed)
        self.assertIn("production_use_allowed=False", gate.reason)


class NoInventedStatus(unittest.TestCase):
    def test_launch_eligible_is_not_a_status_the_register_knows(self):
        ev = B.evidence_base()
        self.assertNotIn("launch_eligible", ev.status_vocabulary)

    def test_the_alpha_profile_auto_routes_nothing_and_the_decision_says_so(self):
        d = B.plan(B.SPEC_MOTION, "alpha_human_release")
        self.assertTrue(d["manual_route_required"])
        preflight = " ".join(d["selection_basis"]["preflight"])
        self.assertIn("launch_eligible", preflight)
        self.assertIn("auto-routes NOTHING", preflight)
        self.assertIsNone(d["primary"])


class RouterNeverScores(unittest.TestCase):
    def test_no_score_or_rank_reaches_the_decision(self):
        d = B.plan(B.SPEC_MOTION, "alpha_wider_example")

        def keys(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    yield str(k)
                    yield from keys(v)
            elif isinstance(obj, (list, tuple)):
                for v in obj:
                    yield from keys(v)

        found = [k for k in keys(d)
                 if any(w in k.lower() for w in ("score", "rank", "weight", "leaderboard"))]
        self.assertEqual(found, [])
        self.assertNotIn("rank_in_question", repr(d))

    def test_evidence_n_is_carried_forward_honestly(self):
        d = B.plan(B.SPEC_MOTION, "alpha_wider_example")
        n = d["primary"]["evidence_n"]["image_to_video"]
        self.assertEqual((n["accepts"], n["trials"]), (7, 8))
        self.assertEqual(n["settled_draw_floor"], 4)


if __name__ == "__main__":
    unittest.main()


class HowMuchOfTheMapIsRoutableToday(unittest.TestCase):
    """A regression anchor for the number the Controller actually asked for."""

    def _counts(self, profile_name):
        ev = B.evidence_base()
        r = B.router(ev)
        prof = B.profile(profile_name, ev)
        auto, unpriced = [], []
        for key, cell in sorted(ev.cells.items()):
            gate = ev.gate(cell, prof.auto_routable_evidence_status)
            quote = r.prices.quote(cell.route_key, {"params": {"duration_s": 6}})
            if not quote.priced:
                unpriced.append(key)
            if gate.allowed and quote.priced:
                auto.append(key)
        return ev, auto, unpriced

    def test_sixteen_of_the_sixty_one_cells_are_routable_where_clean_observed_is_allowed(self):
        ev, auto, unpriced = self._counts("alpha_wider_example")
        self.assertEqual(len(ev.cells), 61)
        self.assertEqual(len(auto), 16)
        # The only cells this audit cannot price are the ones whose billing quantity is not a
        # duration: lipsync bills rolled-up input seconds, TTS bills characters. Nothing is blocked
        # on a MISSING pin — today the binding constraint on routing is evidence, not price.
        self.assertEqual(unpriced, ["AUD-LIP/kling-lipsync-a2v+chain",
                                    "AUD-TTS/elevenlabs-v3-direct+native",
                                    "AUD-TTS/sarvam-bulbul-v3+native"])

    def test_none_of_the_sixty_one_are_routable_under_the_shipped_alpha_profile(self):
        _, auto, _ = self._counts("alpha_human_release")
        self.assertEqual(auto, [])
