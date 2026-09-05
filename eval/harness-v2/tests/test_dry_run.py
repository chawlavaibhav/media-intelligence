"""Tester checks 4 and 8, mechanised against the committed manifest and the registry.

    counts: conditional false = 288 (192 / 96), conditional true = 32 (Controller between-role note 6);
    every pool reconciles within USD 0.01 or is closed by explained lines; nominal in cap closes on 156.46;
    every would_dispatch: true row is price pinned, route pinned and shape verified; the manifest is
    planning evidence and says so; unpinned / needs_controller_enablement keys never dispatch.
"""
import unittest
from decimal import Decimal
from pathlib import Path

import yaml

from _support import NoNetworkTestCase, hv2_paths
import surfaces

MANIFEST = hv2_paths.HERE / "DRY-RUN-MANIFEST-2026-09.yaml"


class ManifestTest(NoNetworkTestCase):
    @classmethod
    def setUpClass(cls):
        cls.m = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
        cls.h = cls.m["header"]
        cls.rows = cls.m["rows"]

    def test_counts(self):
        c = self.h["counts"]
        self.assertEqual((c["calls_not_conditional"], c["calls_conditional"], c["tranche_1a"], c["tranche_1b"]), (288, 32, 192, 96))
        self.assertTrue(c["counts_match_task"])
        self.assertEqual(c["unpinned_calls"], 20)
        self.assertEqual(sum(1 for r in self.rows if not r["conditional"]), 288)
        self.assertEqual(sum(1 for r in self.rows if r["conditional"]), 32)

    def test_reconciliation_closes(self):
        for t in self.h["reconciliation"]["by_tranche_and_pool"]:
            with self.subTest(pool=(t["tranche"], t["billing_pool"])):
                self.assertEqual(t["manifest_calls"], t["cost_table_calls"])
                self.assertTrue(t["within_0_01"] or t["closed"], t)
        for t in self.h["reconciliation"]["conditional_by_tranche_and_pool"]:
            self.assertTrue(t["within_0_01"], t)
        n = self.h["nominal_in_cap"]
        self.assertEqual(n["cost_table_nominal_usd_in_cap"], "156.46")
        self.assertTrue(n["closed"] and n["all_pools_closed"], n)
        for e in self.h["reconciliation"]["explained_deltas"]:
            self.assertTrue(e["explanation"], e)

    def test_every_dispatchable_row_is_pinned_and_verified(self):
        for r in self.rows:
            if r["would_dispatch"]:
                with self.subTest(row=(r["case_id"], r["route_key"], r["arm"], r["repeat_index"])):
                    self.assertEqual((r["price_status"], r["route_status"], r["shape_status"]), ("pinned", "pinned", "verified"))
                    self.assertFalse(r["conditional"])
                    self.assertIsNotNone(r["computed_amount"])
                    self.assertTrue(r["body_sha256"])
            else:
                self.assertTrue(r["refusal_reason"], r["route_key"])

    def test_no_promo_and_no_key_value(self):
        text = MANIFEST.read_text(encoding="utf-8")
        self.assertNotIn("promo_price_in_use", text)
        self.assertIn("<KEY:FAL_KEY>", text)
        self.assertNotIn("Key fal_", text)
        self.assertEqual(self.h["status"], "PLANNING_EVIDENCE_NOT_A_SPEND_AUTHORISATION")
        self.assertEqual(self.h["inputs"]["roster"]["sha256"], "99cde63c8c668e57457915ee1aae69e7ba7f09ed9c8b2d26bc5a3a0537aa2b46")
        self.assertTrue(self.h["inputs"]["roster"]["roster_last_commit_sha"])

    def test_unpinned_and_enablement_keys_never_dispatch(self):
        never = {"gpt-image-2-edit", "sync-lipsync-v3", "veo-3.1-lite-i2v", "kling-v3-elements",
                 "sd3.5-large", "mai-image-2.6", "sora-2", "chirp-3-hd-hi-in", "azure-neural-tts-hi-in"}
        seen = set()
        for r in self.rows:
            if r["route_key"] in never:
                seen.add(r["route_key"])
                self.assertFalse(r["would_dispatch"], r["route_key"])
        self.assertEqual(seen, never)
        self.assertEqual(sum(1 for r in self.rows if r["route_key"] == "veo-3.1-fast-extend" and r["api_calls_per_trial"] == 2), 2)


class HygieneTest(NoNetworkTestCase):
    """Tester checks 2 and 3 as code: network imports only in transports.py; no key value anywhere.
    The patterns are assembled from fragments so that this file itself never matches the Tester's grep."""

    def test_network_modules_only_in_transports(self):
        import re
        mods = "|".join(("url" + "lib", "http\\." + "client", "sock" + "et", "requ" + "ests"))   # split so this file never matches the Tester grep
        pat = re.compile(r"^\s*(import|from)\s+(" + mods + r")\b", re.M)
        offenders = []
        for p in hv2_paths.HERE.rglob("*.py"):
            if "tests" in p.parts or "__pycache__" in p.parts:
                continue
            if pat.search(p.read_text(encoding="utf-8")) and p.name != "transports.py":
                offenders.append(str(p))
        self.assertEqual(offenders, [])

    def test_no_key_pattern_in_deliverables(self):
        import re
        frags = ("s" + "k-[A-Za-z0-9]{10,}", "AI" + "za[0-9A-Za-z_-]{20,}", "AK" + "IA[0-9A-Z]{12,}", "ke" + "y_[0-9a-f]{20,}",
                 "fa" + "l_[A-Za-z0-9]{20,}", "BEGIN PRIVATE" + " KEY", "api-subscription-" + "key: [A-Za-z0-9]")
        pat = re.compile("(" + "|".join(frags) + ")")
        roots = [hv2_paths.HERE, hv2_paths.EVAL_ROOT / "v1" / "instruments" / "qualification-records"]
        hits = []
        import gzip
        n_files = 0
        for root in roots:
            for p in root.rglob("*"):
                if not p.is_file() or "__pycache__" in p.parts:
                    continue
                n_files += 1
                raw = p.read_bytes()
                if p.suffix == ".gz":                       # compressed files are scanned DECOMPRESSED (Tester D1)
                    raw = gzip.decompress(raw)
                if pat.search(raw.decode("utf-8", errors="ignore")):
                    hits.append(str(p))
        self.assertGreater(n_files, 50)
        self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main()
