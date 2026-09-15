"""Character-metered units are normalised exactly as the harness does.

The harness (`eval/harness-v2/pricing.py`, the price authority) computes
    per_1000_characters  = unit_price x chars / 1000
    per_1M_characters    = unit_price x chars / 1_000_000
The runtime PriceBook wraps that harness for the roster, pins and quantity rules but used to multiply
the per-1000 / per-1M unit price by the RAW character count (Sarvam, 79 chars: USD 2.48 instead of
about USD 0.0025). These tests pin the runtime to the harness figure and prove that a non-character
unit is unchanged. Offline; nothing is sent; no roster file is written.
"""
from __future__ import annotations

import unittest
from decimal import Decimal

import _bootstrap as B

from runtime.route import price as price_mod


class CharacterUnitsMatchTheHarness(unittest.TestCase):
    def setUp(self):
        self.ev = B.evidence_base()
        self.book = B.price_book(self.ev)
        self.harness = self.book.pricing.Pricing()          # the same harness module the book wraps

    def test_sarvam_79_characters_per_1000_characters_matches_the_harness(self):
        facts = {"params": {"chars": 79}}
        q = self.book.quote("sarvam-bulbul-v3", facts)
        self.assertTrue(q.priced, q.reason)
        self.assertEqual(q.unit, "per_1000_characters")
        self.assertEqual(q.quantity, Decimal(79))
        ref = self.harness.evaluate("sarvam-bulbul-v3", facts)
        self.assertTrue(ref.ok, ref.refusal_reason)
        # 3.0 INR per 1000 chars x 79 chars = 0.237 INR = 0.002484 USD at the display rate — NOT 2.48
        self.assertEqual(ref.amount_native, Decimal("0.237000"))
        self.assertEqual(q.expected_cost_usd, ref.amount_usd_equiv)
        self.assertLess(q.expected_cost_usd, Decimal("0.01"))

    def test_per_1M_characters_divides_by_one_million(self):
        # The only per_1M roster route today needs Controller enablement and never reaches the amount
        # step, so the normalisation itself is pinned here, as the harness states it.
        self.assertEqual(price_mod.native_amount(Decimal("15.0"), Decimal(79), "per_1M_characters"),
                         Decimal("15.0") * Decimal(79) / Decimal(1_000_000))
        self.assertEqual(price_mod.native_amount(Decimal("3.0"), Decimal(79), "per_1000_characters"),
                         Decimal("3.0") * Decimal(79) / Decimal(1000))

    def test_a_non_character_unit_is_unchanged(self):
        q = self.book.quote("flux-2-pro", {"params": {}})
        self.assertTrue(q.priced, q.reason)
        self.assertEqual(q.unit, "per_image_first_megapixel")
        self.assertEqual(q.expected_cost_usd, Decimal("0.030000"))
        ref = self.harness.evaluate("flux-2-pro", {"params": {}})
        self.assertEqual(q.expected_cost_usd, ref.amount_usd_equiv)
        self.assertEqual(price_mod.native_amount(Decimal("0.08"), Decimal(10), "per_second"), Decimal("0.80"))

    def test_a_per_second_route_still_multiplies_by_duration(self):
        q = self.book.quote("minimax-h3-max-i2v", {"params": {"duration_s": 10}})
        self.assertTrue(q.priced, q.reason)
        self.assertEqual(q.expected_cost_usd, Decimal("0.800000"))


if __name__ == "__main__":
    unittest.main()
