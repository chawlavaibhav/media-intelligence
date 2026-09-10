"""Price: the pin has to be live, it has to come through the roster, and the map is not a price list.

Two of these tests edit a COPY of the roster in a temporary directory. Nothing under `eval/` is ever
written to; the copy exists so that "the roster says this route is not callable" can be tested
without waiting for the roster to say it.
"""
from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

import yaml

import _bootstrap as B


class PriceComesFromTheRoster(unittest.TestCase):
    def test_the_decision_records_pin_unit_price_cost_and_pool(self):
        d = B.plan(B.SPEC_MOTION, "alpha_wider_example")
        p = d["primary"]
        self.assertTrue(p["price_pin_ref"].startswith("eval/empirical-planning/price-pins-2026-09/"))
        self.assertEqual(p["unit_price"], "0.08")
        self.assertEqual(p["expected_cost_usd"], "0.480000")     # 0.08/s x 6 s from the spec
        self.assertEqual(p["billing_pool"], "cash")

    def test_the_price_is_not_the_routing_maps_figure_when_the_roster_has_re_pointed(self):
        """nano-banana-pro: the map still says Vertex; the roster says the Gemini Developer API."""
        ev = B.evidence_base()
        map_cell = ev.map["questions"]["IMG-CORE"]["cells"]["nano-banana-pro"]
        d = B.plan(B.SPEC_STATIC_IN_SCENE, "alpha_wider_example")
        self.assertEqual(d["primary"]["route_key"], "nano-banana-pro")
        self.assertEqual(map_cell["surface"], ["vertex"])
        self.assertEqual(d["primary"]["surface"], "gemini_api")
        self.assertNotIn(d["primary"]["price_pin_ref"], map_cell["price_pin_ref"])
        self.assertFalse(d["provenance"]["map_prices_used"])

    def test_a_pin_only_in_a_sub_index_is_still_a_live_pin(self):
        """wan-2.2-a14b has no entry at all in the master PIN-INDEX; its pins live in a sub-index."""
        ev = B.evidence_base()
        pb = B.price_book(ev)
        master = ev.root / ev.binding.sources["price_pin_root"] / "PIN-INDEX.yaml"
        master_files = {p["pin_file"] for p in yaml.safe_load(master.read_text())["pins"]}
        q = pb.quote("wan-2.2-a14b-i2v", {"params": {"duration_s": 6}})
        self.assertTrue(q.priced, q.reason)
        self.assertNotIn(q.price_pin_ref, master_files)
        self.assertTrue(any("wan-2.2-a14b/PIN-INDEX.yaml" in i for i in q.pin_indexes))


class NoLivePinNoAutoRoute(unittest.TestCase):
    def _roster_copy(self, mutate) -> Path:
        ev = B.evidence_base()
        tmp = Path(tempfile.mkdtemp(prefix="route-roster-"))
        src = ev.root / ev.binding.sources["roster"]
        dst = tmp / src.name
        shutil.copy2(src, dst)
        data = yaml.safe_load(dst.read_text(encoding="utf-8"))
        mutate(data)
        dst.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
        self.addCleanup(shutil.rmtree, tmp, True)
        return dst

    def test_a_route_the_roster_cannot_price_is_dropped_at_the_price_stage(self):
        def unpin(data):
            for r in data["routes"]:
                if r["route_key"] == "minimax-h3-max":
                    r["route_status"] = "unpinned"
                    for v in r.get("variants") or []:
                        v["route_status"] = "unpinned"
        roster = self._roster_copy(unpin)
        ev = B.evidence_base()
        d = B.plan(B.SPEC_MOTION, "alpha_wider_example", ev=ev,
                   prices=B.price_book(ev, roster_path=roster))
        by_route = {c["route_key"]: c for c in d["selection_basis"]["candidates_considered"]}
        self.assertEqual(by_route["minimax-h3-max-i2v"]["dropped_at"], "price")
        self.assertIn("never auto-selected", " ".join(by_route["minimax-h3-max-i2v"]["why"]))
        self.assertNotEqual(d["primary"]["route_key"], "minimax-h3-max-i2v")
        self.assertNotEqual(d["fallback"]["route_key"], "minimax-h3-max-i2v")

    def test_a_route_with_no_regular_price_is_dropped_at_the_price_stage(self):
        def strip(data):
            for r in data["routes"]:
                if r["route_key"] == "minimax-h3-max":
                    r["regular_price"] = {"value": None, "currency": "USD", "unit": "per_second"}
                    for v in r.get("variants") or []:
                        v["regular_price"] = {"value": None, "currency": "USD", "unit": "per_second"}
        roster = self._roster_copy(strip)
        ev = B.evidence_base()
        d = B.plan(B.SPEC_MOTION, "alpha_wider_example", ev=ev,
                   prices=B.price_book(ev, roster_path=roster))
        by_route = {c["route_key"]: c for c in d["selection_basis"]["candidates_considered"]}
        self.assertEqual(by_route["minimax-h3-max-i2v"]["dropped_at"], "price")

    def test_a_pin_listed_in_no_index_is_not_a_live_pin(self):
        """Reading only the master index loses the Gemini surface — the supersession, in one test."""
        ev = B.evidence_base()
        tmp = Path(tempfile.mkdtemp(prefix="route-pins-"))
        self.addCleanup(shutil.rmtree, tmp, True)
        shutil.copy2(ev.root / ev.binding.sources["price_pin_root"] / "PIN-INDEX.yaml",
                     tmp / "PIN-INDEX.yaml")
        pb = B.price_book(ev, pin_root=tmp)
        q = pb.quote("nano-banana-pro", {"params": {}})
        self.assertFalse(q.priced)
        self.assertIn("listed in no PIN-INDEX", q.reason)


class QuantityIsNeverEstimated(unittest.TestCase):
    def test_a_per_second_route_without_a_duration_in_the_spec_is_unpriceable(self):
        ev = B.evidence_base()
        pb = B.price_book(ev)
        q = pb.quote("minimax-h3-max-i2v", {"params": {}})
        self.assertFalse(q.priced)
        self.assertIn("refuses to estimate", q.reason)


if __name__ == "__main__":
    unittest.main()
