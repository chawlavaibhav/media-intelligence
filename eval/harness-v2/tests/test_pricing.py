"""Execution-time price check: re-reads the roster, refuses drift, never uses a promo."""
import unittest
from decimal import Decimal
from pathlib import Path

import yaml

from _support import HV2, NoNetworkTestCase, hv2_paths  # noqa: F401
import pricing
from providers import PreDispatchRefusal

ROW_GPT = {"case_id": "IMG-CORE-01", "route_key": "gpt-image-2", "params": {"aspect": "4:5", "refs": 0, "seed": "unset"},
           "quantity": 1, "quantity_unit": "images", "unit_price": 0.053, "price_status": "pinned", "route_status": "pinned"}
ROW_VEO = {"case_id": "VID-T2V-01", "route_key": "veo-3.1-fast", "params": {"aspect": "9:16", "duration_s": 6, "audio": "on"},
           "quantity": 6, "quantity_unit": "seconds", "unit_price": 0.1, "price_status": "pinned", "route_status": "pinned"}
ROW_SARVAM = {"case_id": "AUD-TTS-01", "route_key": "sarvam-bulbul-v3", "params": {"script": "x", "chars": 21},
              "quantity": 21, "quantity_unit": "chars", "unit_price": 3.0, "price_status": "pinned", "route_status": "pinned"}


class PricingTest(NoNetworkTestCase):
    def setUp(self):
        super().setUp()
        self.p = pricing.Pricing()

    def test_pinned_row_passes_and_prices_from_the_roster(self):
        pc = self.p.check("gpt-image-2", ROW_GPT)
        self.assertTrue(pc.ok)
        self.assertEqual(pc.unit_price, Decimal("0.053"))
        self.assertEqual(pc.amount_usd_equiv, Decimal("0.053000"))
        self.assertEqual(pc.currency, "USD")
        self.assertEqual(pc.quantity_rule, "per_image")

    def test_per_second_quantity(self):
        pc = self.p.check("veo-3.1-fast", ROW_VEO)
        self.assertEqual(pc.quantity, Decimal(6))
        self.assertEqual(pc.amount_usd_equiv, Decimal("0.600000"))

    def test_inr_row_keeps_inr_and_carries_a_usd_equivalent(self):
        pc = self.p.check("sarvam-bulbul-v3", ROW_SARVAM)
        self.assertEqual(pc.currency, "INR")
        self.assertEqual(pc.amount_native, Decimal("0.063000"))          # 3.0 x 21 / 1000
        self.assertEqual(pc.fx_rate, pricing.INR_USD_DISPLAY_RATE)
        self.assertEqual(pc.amount_usd_equiv, (Decimal("0.063") / pricing.INR_USD_DISPLAY_RATE).quantize(Decimal("0.000001")))

    def test_price_mismatch_refuses_before_anything_is_reserved(self):
        row = {**ROW_GPT, "unit_price": 0.211}
        with self.assertRaises(PreDispatchRefusal) as cm:
            self.p.check("gpt-image-2", row)
        self.assertIn("price_mismatch", str(cm.exception))

    def test_unpinned_route_refuses(self):
        row = {"case_id": "IMG-EDIT-01", "route_key": "gpt-image-2-edit", "params": {"refs": 1}, "quantity": 1,
               "quantity_unit": "images", "unit_price": None, "price_status": "unpinned", "route_status": "pinned"}
        pc = self.p.evaluate("gpt-image-2-edit", row)
        self.assertFalse(pc.ok)
        self.assertIn("price_unpinned", pc.refusal_reason)
        with self.assertRaises(PreDispatchRefusal):
            self.p.check("gpt-image-2-edit", row)

    def test_needs_enablement_route_refuses(self):
        row = {"case_id": "IMG-CORE-01", "route_key": "sd3.5-large", "params": {}, "quantity": 1, "quantity_unit": "images",
               "unit_price": 0.08, "price_status": "pinned", "route_status": "needs_controller_enablement"}
        pc = self.p.evaluate("sd3.5-large", row)
        self.assertFalse(pc.ok)
        self.assertIn("route_status_not_pinned", pc.refusal_reason)

    def test_quantity_rules(self):
        lip = {"case_id": "AUD-LIP-01", "route_key": "kling-lipsync-a2v", "params": {"billed_input_seconds": "10 (6-s plate rolled up to the 5-s increment)"},
               "quantity": 10, "quantity_unit": "seconds", "unit_price": 0.014, "price_status": "pinned", "route_status": "pinned"}
        self.assertEqual(self.p.check("kling-lipsync-a2v", lip).quantity, Decimal(10))
        music = {"case_id": "MUS-01", "route_key": "elevenlabs-music", "params": {"duration_s": 30}, "quantity": 1,
                 "quantity_unit": "minutes", "unit_price": 0.6, "price_status": "pinned", "route_status": "pinned"}
        self.assertEqual(self.p.check("elevenlabs-music", music).amount_usd_equiv, Decimal("0.600000"))
        ext = {"case_id": "VID-MS-01", "route_key": "veo-3.1-fast-extend", "params": {"duration_s": 15}, "quantity": 15,
               "quantity_unit": "seconds", "unit_price": 0.1, "price_status": "pinned", "route_status": "pinned"}
        pc = self.p.check("veo-3.1-fast-extend", ext)
        self.assertEqual(pc.quantity_rule, "veo_extend_15s")
        self.assertEqual(pc.amount_usd_equiv, Decimal("1.500000"))

    def test_quantity_mismatch_refuses(self):
        row = {**ROW_VEO, "quantity": 8}
        with self.assertRaises(PreDispatchRefusal) as cm:
            self.p.check("veo-3.1-fast", row)
        self.assertIn("quantity_rule_mismatch", str(cm.exception))

    def test_roster_is_re_read_at_every_check(self):
        """A roster edited on disk between two checks changes the second answer."""
        roster_copy = self.tmp / "roster.yaml"
        roster_copy.write_bytes(Path(hv2_paths.ROSTER).read_bytes())
        p = pricing.Pricing(roster_copy)
        self.assertTrue(p.check("gpt-image-2", ROW_GPT).ok)
        data = yaml.safe_load(roster_copy.read_text())
        for r in data["routes"]:
            if r["route_key"] == "gpt-image-2":
                r["fallback"]["regular_price"]["value"] = 0.999
        roster_copy.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))
        with self.assertRaises(PreDispatchRefusal):
            p.check("gpt-image-2", ROW_GPT)

    def test_promo_flagged_as_used_refuses(self):
        roster_copy = self.tmp / "roster.yaml"
        data = yaml.safe_load(Path(hv2_paths.ROSTER).read_text())
        for r in data["routes"]:
            if r["route_key"] == "minimax-h3-max":
                r["promo_price"]["used_in_totals"] = True
        roster_copy.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))
        p = pricing.Pricing(roster_copy)
        row = {"case_id": "VID-T2V-01", "route_key": "minimax-h3-max", "params": {"duration_s": 6}, "quantity": 6,
               "quantity_unit": "seconds", "unit_price": 0.08, "price_status": "pinned", "route_status": "pinned"}
        pc = p.evaluate("minimax-h3-max", row)
        self.assertIn("promo_price_in_use", pc.refusal_reason)

    def test_expected_sha_drift_refuses(self):
        p = pricing.Pricing(expected_roster_sha256="0" * 64)
        pc = p.evaluate("gpt-image-2", ROW_GPT)
        self.assertIn("roster_sha256_drift", pc.refusal_reason)

    def test_af1_roster_sha_is_bound_by_default_to_the_cost_table_basis(self):
        """AF-1: the sha check is mandatory - the default expectation is COST-TABLE.priced_against_roster.sha256."""
        self.assertEqual(self.p.expected_roster_sha256, pricing.CostTable().priced_against_roster["sha256"])
        roster_copy = self.tmp / "roster.yaml"
        data = yaml.safe_load(Path(hv2_paths.ROSTER).read_text())
        data["meta"]["route_count"] = 999
        roster_copy.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))
        pc = pricing.Pricing(roster_copy).evaluate("gpt-image-2", ROW_GPT)
        self.assertIn("roster_sha256_drift", pc.refusal_reason)
        with self.assertRaises(ValueError):
            pricing.Pricing(expected_roster_sha256=None, bind_roster_sha=False, catalogue={})   # opting out is not offered

    def test_af9_character_quantity_comes_from_the_rendered_text(self):
        pc = self.p.check("sarvam-bulbul-v3", ROW_SARVAM, rendered_chars=21)
        self.assertEqual(pc.quantity, Decimal(21))
        with self.assertRaises(PreDispatchRefusal) as cm:
            self.p.check("sarvam-bulbul-v3", ROW_SARVAM, rendered_chars=25)
        self.assertIn("quantity_rule_mismatch", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
