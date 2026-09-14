"""The acceptance contract's style guard, the same discipline the Stage-A build enforces.

A statement is decidable from the artifact alone. A statement that names a route, a model, an
arm, a cost or a rule id is a build failure, not a warning.
"""
from __future__ import annotations

import unittest

from runtime.canon.normalize import normalize
from runtime.errors import Refusal
from runtime.spec.acceptance import StyleGuard, build
from runtime.tests import support


class GuardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guard = StyleGuard()

    def assertRejected(self, statement, token_hint=None, exempt=()):
        violation = self.guard.inspect(statement, exempt)
        self.assertIsNotNone(violation, f"guard let this through: {statement}")
        if token_hint:
            self.assertIn(token_hint.lower(), violation.token.lower())

    def test_a_statement_naming_a_model_is_rejected(self):
        self.assertRejected(
            "ACCEPT only if the Seedream 5 Pro draw keeps the tin's label unchanged.", "seedream"
        )

    def test_every_provider_in_the_evidence_map_is_guarded(self):
        for token in ("nano", "veo", "kling", "flux", "sarvam", "lyria", "qwen", "recraft", "gemini"):
            self.assertRejected(f"ACCEPT only if the {token} output shows one tin.", token)

    def test_the_model_name_vocabulary_comes_from_the_evidence_map(self):
        self.assertIn("seedream", self.guard.evidence.brand_tokens())
        self.assertIn("nano", self.guard.evidence.brand_tokens())

    def test_a_statement_naming_a_route_arm_cost_or_rule_id_is_rejected(self):
        self.assertRejected("ACCEPT only if the cheapest route produced it.", "route")
        self.assertRejected("ACCEPT only if arm C was used.", "arm C")
        self.assertRejected("REJECT if the picture cost more than USD 0.05.", "USD")
        self.assertRejected("ACCEPT only if RR-1 was followed.", "RR-1")
        self.assertRejected("ACCEPT only if PA-D1 passed.", "PA-D1")
        self.assertRejected("ACCEPT only if the Canon doctrine was applied.", "Canon")
        self.assertRejected("REJECT if the prompt named a second bottle.", "prompt")
        self.assertRejected("ACCEPT only if the text was composited by code.", "composited")

    def test_a_statement_that_does_not_open_with_a_verdict_is_rejected(self):
        self.assertRejected("The tin should look nice.")
        self.assertRejected("")

    def test_a_plain_decidable_statement_passes(self):
        for statement in (
            "ACCEPT only if exactly one oil tin is in frame and no person, hand or second tin appears.",
            "REJECT if any lettering is cut by the frame edge.",
            "ACCEPT only if the model's hand visibly holds the pack — fingers wrap it.",
        ):
            self.assertIsNone(self.guard.inspect(statement), statement)

    def test_the_customers_own_copy_is_not_treated_as_a_leak(self):
        statement = 'ACCEPT only if the lettering reads exactly "Best Price Guaranteed" — every character as given.'
        self.assertIsNotNone(self.guard.inspect(statement))                       # unmasked: 'price' trips it
        self.assertIsNone(self.guard.inspect(statement, ["Best Price Guaranteed"]))  # the customer's string does not


class ContractBuildTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guard = StyleGuard()

    def test_a_bad_statement_from_the_reasoning_pass_fails_the_compile(self):
        job = support.submit("mustard-oil-tin")
        nr = normalize(job)
        with self.assertRaises(Refusal) as caught:
            build(job, nr, ["ACCEPT only if Nano Banana 2 spelled the price correctly."], self.guard)
        self.assertEqual(caught.exception.code, Refusal.ACCEPTANCE_STYLE_VIOLATION)

    def test_a_bad_statement_is_never_silently_dropped(self):
        """It sits past the max, where a trimming implementation would have quietly lost it."""
        job = support.submit("mustard-oil-tin")
        nr = normalize(job)
        good = [
            "ACCEPT only if exactly one oil tin is in frame.",
            "REJECT if the tin is deformed or cut off by the frame edge.",
            "ACCEPT only if the background is a plain warm ground.",
        ]
        with self.assertRaises(Refusal) as caught:
            build(job, nr, good + ["REJECT if the seedream draw shows two tins."], self.guard)
        self.assertEqual(caught.exception.code, Refusal.ACCEPTANCE_STYLE_VIOLATION)

    def test_too_few_statements_is_a_loud_failure(self):
        job = support.submit("showroom-photo-edit")  # no exact strings, so few derived statements
        nr = normalize(job)
        with self.assertRaises(Refusal) as caught:
            build(job, nr, [], self.guard)
        self.assertEqual(caught.exception.code, Refusal.ACCEPTANCE_COUNT_OUT_OF_RANGE)

    def test_the_contract_stays_inside_three_to_six_statements(self):
        for name in ("mustard-oil-tin", "showroom-photo-edit", "lipstick-packshot"):
            spec = support.compiler().compile(support.submit(name), compiled_utc="2026-09-10T12:00:00Z").spec
            statements = spec["acceptance_contract"]
            self.assertGreaterEqual(len(statements), self.guard.min, name)
            self.assertLessEqual(len(statements), self.guard.max, name)

    def test_every_compiled_contract_survives_its_own_guard(self):
        for name in ("mustard-oil-tin", "showroom-photo-edit", "lipstick-packshot"):
            job = support.submit(name)
            spec = support.compiler().compile(job, compiled_utc="2026-09-10T12:00:00Z").spec
            exempt = [s["value"] for s in job.get("exact_text_strings", [])]
            self.guard.check(spec["acceptance_contract"], exempt)

    def test_the_customers_exact_strings_are_always_in_the_contract(self):
        job = support.submit("mustard-oil-tin")
        spec = support.compiler().compile(job, compiled_utc="2026-09-10T12:00:00Z").spec
        contract = " ".join(spec["acceptance_contract"])
        for row in job["exact_text_strings"]:
            self.assertIn(row["value"], contract)


if __name__ == "__main__":
    unittest.main()
