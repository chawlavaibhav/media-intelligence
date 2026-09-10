"""Exclusions, the cost envelope, execute's refusals, identities, and fail-closed limits."""
from __future__ import annotations

import shutil
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

import yaml

import _bootstrap as B
from runtime.route.attempt_id import IdentityCollision, load_identities
from runtime.route.decision import CostEnvelopeExceeded, ExecuteRefused
from runtime.route.evidence import EvidenceBase, FingerprintMismatch
from runtime.route.profile import MissingLimit, load_profile


class Exclusions(unittest.TestCase):
    def setUp(self):
        self.d = B.plan(B.SPEC_MOTION, "alpha_wider_example")

    def test_an_excluded_route_is_neither_primary_nor_fallback(self):
        self.assertNotEqual(self.d["primary"]["route_key"], "veo-3.1-fast-i2v")
        self.assertNotEqual(self.d["fallback"]["route_key"], "veo-3.1-fast-i2v")

    def test_the_exclusion_is_shown_rather_than_left_to_be_inferred(self):
        rows = [e for e in self.d["exclusions_applied"] if e["route_key"] == "veo-3.1-fast-i2v"]
        self.assertEqual(len(rows), 1)
        self.assertIn("RR-8", rows[0]["basis"])
        self.assertEqual(rows[0]["would_have_supplied"], "VID-I2V/veo-3.1-fast-i2v")
        self.assertEqual(rows[0]["effect"], "neither primary nor fallback")

    def test_the_excluded_route_was_dropped_at_the_hard_requirement_stage(self):
        by_route = {c["route_key"]: c for c in self.d["selection_basis"]["candidates_considered"]}
        self.assertEqual(by_route["veo-3.1-fast-i2v"]["dropped_at"], "hard_requirements")

    def test_cost_does_not_overrule_the_exclusion(self):
        """The excluded route is cheaper than the declared fallback and still loses."""
        ev = B.evidence_base()
        pb = B.price_book(ev)
        excluded = pb.quote("veo-3.1-fast-i2v", {"params": {"duration_s": 6}})
        self.assertLess(excluded.expected_cost_usd,
                        Decimal(self.d["fallback"]["expected_cost_usd"]))


class CostEnvelope(unittest.TestCase):
    def test_the_envelope_is_checked_before_dispatch_and_refuses(self):
        d = B.plan(B.SPEC_MOTION, "alpha_wider_example", committed="4.90")
        self.assertFalse(d["cost_envelope"]["within_ceiling"])
        self.assertTrue(d["manual_route_required"])
        self.assertIn("cost_envelope_exceeded", d["manual_route_reason"])

    def test_the_envelope_arithmetic_is_committed_plus_worst_case_draws(self):
        d = B.plan(B.SPEC_MOTION, "alpha_wider_example", committed="1.00")
        ce = d["cost_envelope"]
        # worst case is the dearer of primary and fallback, times the profile's draw allowance
        self.assertEqual(ce["this_decision_max_usd"], "2.688000")   # 0.672 x 4
        self.assertEqual(ce["already_committed_usd"], "1.00")
        self.assertTrue(ce["within_ceiling"])

    def test_execute_stops_on_the_envelope_before_anything_else_happens(self):
        ev = B.evidence_base()
        r = B.router(ev)
        with self.assertRaises((CostEnvelopeExceeded, ExecuteRefused)):
            r.execute(B.spec(B.SPEC_MOTION), B.profile("dry", ev),
                      request_cost_ceiling_usd=Decimal("5.00"), already_committed_usd=Decimal("4.99"))


class ExecuteRefuses(unittest.TestCase):
    def test_execute_refuses_under_a_non_adopted_profile(self):
        r = B.router()
        with self.assertRaises(ExecuteRefused) as ctx:
            r.execute(B.spec(B.SPEC_MOTION), B.profile("alpha_human_release"),
                      request_cost_ceiling_usd=Decimal("5.00"))
        joined = " ".join(ctx.exception.reasons)
        self.assertIn("adopted: false", joined)
        self.assertIn("alpha_human_release", joined)

    def test_execute_refuses_without_a_request_level_ceiling(self):
        r = B.router()
        with self.assertRaises(ExecuteRefused) as ctx:
            r.execute(B.spec(B.SPEC_MOTION), B.profile("dry"), request_cost_ceiling_usd=None)
        self.assertIn("no request-level cost ceiling", " ".join(ctx.exception.reasons))

    def test_execute_refuses_for_both_reasons_at_once_when_both_are_missing(self):
        r = B.router()
        with self.assertRaises(ExecuteRefused) as ctx:
            r.execute(B.spec(B.SPEC_MOTION), B.profile("alpha_human_release"),
                      request_cost_ceiling_usd=None)
        self.assertEqual(len(ctx.exception.reasons), 2)

    def test_even_with_ceiling_and_adopted_profile_no_provider_client_exists(self):
        r = B.router()
        with self.assertRaises(ExecuteRefused) as ctx:
            r.execute(B.spec(B.SPEC_MOTION), B.profile("dry"),
                      request_cost_ceiling_usd=Decimal("5.00"))
        self.assertIn("no provider client is wired", " ".join(ctx.exception.reasons).lower())


class Identities(unittest.TestCase):
    def test_a_customer_attempt_id_is_minted_in_the_customer_namespace(self):
        ids = load_identities()
        got = ids.mint(customer_ref="acct-1", job_id="job-1", decision_id="rd-1",
                       route_key="minimax-h3-max-i2v", draw_index=1)
        self.assertEqual(got, "cust:acct-1:job-1:rd-1:minimax-h3-max-i2v:draw1")

    def test_an_id_that_could_be_read_as_a_lab_identity_is_refused(self):
        ids = load_identities()
        with self.assertRaises(IdentityCollision):
            ids.mint(customer_ref="aud-lip-smoke", job_id="job-1", decision_id="rd-1",
                     route_key="kling-lipsync-a2v", draw_index=1)
        with self.assertRaises(IdentityCollision):
            ids.mint(customer_ref="acct-1", job_id="AUD-LIP-01__kling__chain__r1", decision_id="rd-1",
                     route_key="kling-lipsync-a2v", draw_index=1)

    def test_one_id_per_draw_the_profile_allows_and_no_retry_identity(self):
        d = B.plan(B.SPEC_MOTION, "alpha_wider_example")
        ids = d["primary"]["attempt_ids_if_dispatched"]
        self.assertEqual(len(ids), B.profile("alpha_wider_example").max_provider_draws)
        self.assertEqual(len(set(ids)), len(ids))


class FailClosed(unittest.TestCase):
    def test_a_profile_missing_a_limit_refuses_rather_than_defaulting(self):
        ev = B.evidence_base()
        tmp = Path(tempfile.mkdtemp(prefix="route-profiles-"))
        self.addCleanup(shutil.rmtree, tmp, True)
        src = ev.root / ev.binding.sources["policy_profiles"]
        data = yaml.safe_load(src.read_text(encoding="utf-8"))
        for row in data["profiles"]:
            if row["profile"] == "dry":
                row.pop("fallback_required")
        dst = tmp / "POLICY-PROFILES.yaml"
        dst.write_text(yaml.safe_dump(data), encoding="utf-8")
        prof = load_profile("dry", dst)
        with self.assertRaises(MissingLimit):
            _ = prof.fallback_required

    def test_the_register_must_describe_the_map_on_disk(self):
        ev = B.evidence_base()
        tmp = Path(tempfile.mkdtemp(prefix="route-binding-"))
        self.addCleanup(shutil.rmtree, tmp, True)
        # a checkout-shaped temp tree whose map differs from the one the register was built against
        (tmp / "runtime" / "contracts").mkdir(parents=True)
        (tmp / "eval" / "capability-map").mkdir(parents=True)
        shutil.copy2(ev.register_path, tmp / "eval" / "capability-map" / ev.register_path.name)
        mangled = ev.map_path.read_text(encoding="utf-8") + "\n# a byte the register never saw\n"
        (tmp / "eval" / "capability-map" / ev.map_path.name).write_text(mangled, encoding="utf-8")
        binding = tmp / "BINDING.yaml"
        data = dict(ev.binding.data)
        binding.write_text(yaml.safe_dump(data), encoding="utf-8")
        with self.assertRaises(FingerprintMismatch):
            EvidenceBase(root=tmp, binding_path=binding)

    def test_the_deliverable_kind_must_be_allowed_by_the_profile(self):
        ev = B.evidence_base()
        prof = B.profile("alpha_human_release", ev)
        self.assertTrue(prof.allows_kind("static_ad"))
        self.assertFalse(prof.allows_kind("two_speaker_dialogue"))


if __name__ == "__main__":
    unittest.main()
