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


class RulingsAppliedToTheRegister(unittest.TestCase):
    """14 Sep 2026: the Controller ruled C-3, C-4, C-6b, C-6c and C-6d, and the register was regenerated
    under them. No cell awaits a ruling any more; the cells that were held are either clean, directional,
    or eliminated on their question. These tests replace the ones that asserted the pre-ruling state."""

    def test_no_cell_awaits_a_controller_ruling_after_regeneration(self):
        ev = B.evidence_base()
        waiting = [k for k, c in ev.cells.items() if c.evidence_status == "awaiting_controller_ruling"]
        self.assertEqual(waiting, [])

    def test_the_static_overlay_ad_now_routes_with_code_composed_text(self):
        """C-6c: the code-overlay cell has its own route identity and is clean; the plate route is an
        IMG-CORE route chosen on evidence then cost; the exact strings are composed by the runtime."""
        d = B.plan(B.SPEC_STATIC_OVERLAY, "alpha_wider_example")
        self.assertFalse(d["manual_route_required"], d["manual_route_reason"])
        self.assertIsNotNone(d["primary"])
        self.assertIsNotNone(d["fallback"])
        composed = [r for r in d["selection_basis"]["self_composed_requirements"]
                    if r["capability"] == "exact_text_composition"]
        self.assertEqual(len(composed), 1)
        self.assertEqual(composed[0]["cell_selected"], "IMG-TEXT/flux-2-pro+code_overlay")
        self.assertEqual(composed[0]["text_mechanism"], "deterministic_text_composition")
        self.assertEqual(composed[0]["evidence_status"], "clean_observed")

    def test_the_bare_plate_cell_is_never_selected_for_code_composed_text(self):
        """The two IMG-TEXT cells share an arm name; only the mechanism tells them apart (C-6c)."""
        ev = B.evidence_base()
        cells = ev.cells_for("IMG-TEXT", None, "deterministic_text_composition")
        self.assertEqual([c.cell_key for c in cells], ["IMG-TEXT/flux-2-pro+code_overlay"])
        bare = ev.cells["IMG-TEXT/flux-2-pro+C_composite_textless_base"]
        self.assertEqual(bare.text_mechanism, "model_draws_text")
        self.assertTrue(bare.eliminated)
        self.assertNotEqual(bare.route_key, ev.cells["IMG-TEXT/flux-2-pro+code_overlay"].route_key)

    def test_an_eliminated_route_is_never_auto_routed_whatever_the_profile_lists(self):
        """C-6b strict: wan-2.2-a14b-i2v is 2/8 with six failures, eliminated E1+E2. Its register status
        is clean (the arithmetic reproduces) but production use is false, and the gate says why."""
        ev = B.evidence_base()
        cell = ev.cells["VID-I2V/wan-2.2-a14b-i2v"]
        self.assertTrue(cell.eliminated)
        self.assertIn("C-6b", cell.rulings_applied)
        gate = ev.gate(cell, ev.status_vocabulary)          # every status the register knows
        self.assertFalse(gate.allowed)
        self.assertIn("eliminated", gate.reason)

    def test_a_profile_cannot_loosen_the_register(self):
        """The invariant does not depend on any real cell being held today: a synthetic cell that is
        awaiting a ruling is refused even by a profile that lists that status as auto-routable."""
        from runtime.route.evidence import Cell
        ev = B.evidence_base()
        held = Cell(cell_key="X/held", question="X", route_key="held", arm=None,
                    evidence_status="awaiting_controller_ruling", production_use_allowed="manual_only",
                    blocking_ruling="C-99", blocking_open_question=None, replacement_needed=False,
                    register_reason="synthetic", accepts=1, trials=2, n_items=1,
                    blinding_commitment_verified=None)
        permissive = ev.status_vocabulary
        self.assertIn("awaiting_controller_ruling", permissive)
        gate = ev.gate(held, permissive)
        self.assertFalse(gate.allowed)
        self.assertIn("C-99", gate.reason)
        self.assertIn("never auto-routed", gate.reason)

    def test_production_use_allowed_false_blocks_even_a_clean_cell(self):
        """After the rulings every production_use_allowed=false cell in the real register is an eliminated
        route (which the gate refuses first, by name). The register's reading still has to be honoured on
        its own, so this uses a synthetic clean, non-eliminated cell the register marks unusable."""
        from runtime.route.evidence import Cell
        ev = B.evidence_base()
        real = ev.cells["IMG-REF/flux-2-pro-edit"]
        self.assertEqual(real.evidence_status, "clean_observed")
        self.assertTrue(real.eliminated)
        self.assertFalse(ev.gate(real, ["clean_observed"]).allowed)
        unusable = Cell(cell_key="X/clean-but-unusable", question="X", route_key="x", arm=None,
                        evidence_status="clean_observed", production_use_allowed=False,
                        blocking_ruling=None, blocking_open_question=None, replacement_needed=False,
                        register_reason="synthetic", accepts=4, trials=4, n_items=2,
                        blinding_commitment_verified=None)
        gate = ev.gate(unusable, ["clean_observed"])
        self.assertFalse(gate.allowed)
        self.assertIn("production_use_allowed=False", gate.reason)


class NoInventedStatus(unittest.TestCase):
    def test_launch_eligible_is_not_a_status_the_register_knows(self):
        ev = B.evidence_base()
        self.assertNotIn("launch_eligible", ev.status_vocabulary)

    def test_every_status_a_profile_names_is_one_the_register_actually_has(self):
        """The defect this replaces: `alpha_human_release` named `launch_eligible`, a status the
        register does not have and says in writing it never will. The effect was total - the profile
        auto-routed 0 of 61 cells. A profile naming a status that does not exist is now a test
        failure rather than a silent shutdown."""
        ev = B.evidence_base()
        for name in ("alpha_human_release", "alpha_wider_example", "dry"):
            prof = B.profile(name)
            for status in prof.auto_routable_evidence_status:
                self.assertIn(status, ev.status_vocabulary,
                              f"profile {name} names status {status!r}, which the taint register does not have")

    def test_the_alpha_profile_now_routes_the_motion_job_and_still_refuses_a_blocked_cell(self):
        """Corrected behaviour. The shipped alpha profile allows `clean_observed` only, so the motion
        job routes; a cell held by a Controller ruling is still refused by name."""
        d = B.plan(B.SPEC_MOTION, "alpha_human_release")
        self.assertFalse(d["manual_route_required"])
        self.assertIsNotNone(d["primary"])
        self.assertEqual(d["primary"]["evidence_status"], "clean_observed")
        ev = B.evidence_base()
        gate = ev.gate(ev.cells["VID-I2V/wan-2.2-a14b-i2v"],
                       B.profile("alpha_human_release").auto_routable_evidence_status)
        self.assertFalse(gate.allowed)
        self.assertIn("eliminated", gate.reason)          # C-6b strict, applied 14 Sep 2026


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

    def test_twenty_six_of_the_sixty_one_cells_are_routable_where_clean_observed_is_allowed(self):
        """Was 16 before the 14 Sep 2026 rulings; the recomputed register (C-3/C-4/C-6b/C-6c/C-6d) frees
        the cells that were held by paperwork and drops the ones eliminated under the frozen rule."""
        ev, auto, unpriced = self._counts("alpha_wider_example")
        self.assertEqual(len(ev.cells), 61)
        self.assertEqual(len(auto), 26)
        # The cells this audit cannot price: lipsync bills rolled-up input seconds, TTS bills
        # characters, and the code-overlay cell is composed by the runtime (no provider call, so no
        # price pin applies to it - the plate it sits on is priced as an IMG-CORE route). Nothing is
        # blocked on a MISSING pin - the binding constraint on routing is evidence, not price.
        self.assertEqual(unpriced, ["AUD-LIP/kling-lipsync-a2v+chain",
                                    "AUD-TTS/elevenlabs-v3-direct+native",
                                    "AUD-TTS/sarvam-bulbul-v3+native",
                                    "IMG-TEXT/flux-2-pro+code_overlay"])

    def test_the_shipped_alpha_profile_routes_the_same_twenty_six(self):
        """Was: asserted zero, because the profile named a status that did not exist. The alpha
        profile allows `clean_observed` only, so it reaches exactly the cells that are clean AND
        marked usable - no more, never a cell awaiting a ruling, never an eliminated route."""
        ev, auto, _ = self._counts("alpha_human_release")
        self.assertEqual(len(auto), 26)
        for key in auto:
            cell = ev.cells[key]
            self.assertEqual(cell.evidence_status, "clean_observed")
            self.assertTrue(cell.production_use_allowed)
        self.assertNotIn("VID-I2V/wan-2.2-a14b-i2v", auto)
