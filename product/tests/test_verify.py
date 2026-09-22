import glob
import struct
import unittest
from pathlib import Path

import yaml

from product import compose, verify
from product.config import REPO
from product.tests.support import Env
from runtime.compositor import gates as G


class ControlRegister(unittest.TestCase):
    def test_every_recorded_case_defect_is_mapped_to_a_control_and_no_id_is_invented(self):
        known = set()
        for f in glob.glob(str(REPO / "production-learning/cases/*/SYSTEM-DEFECTS.yaml")):
            case = Path(f).parent.name
            for d in yaml.safe_load(open(f)).get("defects") or []:
                known.add(f"{case}:{d['id']}")
        cited = {s for c in verify.controls().values() for s in c["sources"] if not s.startswith("runtime/")}
        self.assertEqual(sorted(known - cited), [])
        self.assertEqual(sorted(cited - known), [])
        self.assertGreaterEqual(len(known), 120)

    def test_every_control_names_a_known_status(self):
        for c in verify.controls().values():
            self.assertIn(c["status"], ("enforced", "by_construction", "reviewer_obligation", "excluded_by_scope", "not_applicable_p1"), c["id"])


class UnrunCheckBlocks(unittest.TestCase):
    """UPWORK-PORTFOLIO-002:PD-06 / QA_COVERAGE_ENFORCEMENT: a check that never ran is not a pass."""

    def setUp(self):
        self.e = Env()
        self.jid = self.e.submit()
        p = self.e.dir / "f.png"
        p.write_bytes(b"one")
        self.aid = self.e.store.add_asset(self.jid, path=p, kind="image", source="composed", content_type="image/png")

    def tearDown(self):
        self.e.close()

    def test_missing_required_check_blocks_and_a_waiver_with_a_name_unblocks(self):
        req = {"ledger_integrity": "X", "hero_visible": "HERO_VISIBLE"}
        self.e.store.record_check(self.jid, self.aid, check_id="ledger_integrity", status="PASS", blocking=True, runner="t", detail="")
        g = verify.gateway(self.e.store, self.jid, self.aid, req)
        self.assertFalse(g["ready"])
        self.assertEqual([b["check_id"] for b in g["blocking"]], ["hero_visible"])
        self.assertEqual(g["blocking"][0]["status"], "NOT_VERIFIED")
        self.e.store.waive(self.jid, self.aid, "hero_visible", "founder", "looked at it: product fully visible")
        self.assertTrue(verify.gateway(self.e.store, self.jid, self.aid, req)["ready"])

    def test_a_result_recorded_for_another_version_of_the_file_does_not_count(self):
        self.e.store.record_check(self.jid, self.aid, check_id="hero_visible", status="PASS", blocking=True, runner="t", detail="")
        with self.e.store.tx() as c:
            c.execute("UPDATE assets SET sha256='0'||substr(sha256,2) WHERE id=?", (self.aid,))
        g = verify.gateway(self.e.store, self.jid, self.aid, {"hero_visible": "HERO_VISIBLE"})
        self.assertFalse(g["ready"])

    def test_a_simulated_review_can_never_pass(self):
        review = {"verdict": "pass", "modalities_evaluated": ["simulated"], "_simulated": True, "_call": {"isolated": True},
                  "mandatory": [{"mandatory_id": "M1", "visible": "yes", "evidence": "x"}], "defects": [],
                  "product_fidelity": "faithful", "continuity": "consistent", "audio": {"speech_or_singing": "no", "notes": ""}}
        rows = verify.review_rows(review, mandatory_ids=["M1"], media_kind="video")
        self.assertTrue(all(r["status"] == "NOT_VERIFIED" for r in rows))

    def test_a_live_review_that_did_not_listen_leaves_audio_unverified(self):
        review = {"verdict": "pass", "modalities_evaluated": ["video_frames"], "_call": {"isolated": True},
                  "mandatory": [], "defects": [], "product_fidelity": "faithful", "continuity": "consistent",
                  "audio": {"speech_or_singing": "cannot_determine", "notes": ""}}
        rows = {r["check_id"]: r["status"] for r in verify.review_rows(review, mandatory_ids=[], media_kind="video")}
        self.assertEqual(rows["audio_reviewed"], "NOT_VERIFIED")
        self.assertEqual(rows["independent_review"], "PASS")


class HistoricalRegressions(unittest.TestCase):
    """Defective historical inputs trigger the check; the documented repair passes it."""

    def test_mokobara_df9_white_wordmark_on_the_light_sky_fails_and_the_black_repair_passes(self):
        sky = [0.72, 0.78, 0.81, 0.69]          # light sky luminances (white measured ~1.3:1 on the real pixels)
        bad = compose.gate("contrast", "CONTRAST_GATE", G.check_contrast, "#ffffff", sky, role="display")
        good = compose.gate("contrast", "CONTRAST_GATE", G.check_contrast, "#000000", sky, role="display")
        self.assertEqual((bad["status"], good["status"]), ("FAIL", "PASS"))

    def test_rentok_a004_d1_edit_lists_fail_and_the_remux_passes(self):
        from runtime.loop.container import assess_edit_lists

        def box(k, p):
            return struct.pack(">I", 8 + len(p)) + k + p

        def mp4(n):
            trak = box(b"trak", box(b"tkhd", b"\0" * 84) + (box(b"edts", b"".join(box(b"elst", b"\0" * 20) for _ in range(n))) if n else b""))
            return box(b"ftyp", b"isom\0\0\2\0isom") + box(b"moov", box(b"mvhd", b"\0" * 100) + trak) + box(b"mdat", b"x")
        self.assertEqual(assess_edit_lists(mp4(2))["status"], "FAIL")
        self.assertEqual(assess_edit_lists(mp4(0))["status"], "PASS")

    def test_an_altered_exact_price_string_fails_the_copy_check(self):
        d = {"copy_deck": [{"id": "c1", "text": "₹186 प्रति लीटर", "source": "customer_exact"}]}
        self.assertEqual(verify.exact_copy_match(["₹185 प्रति लीटर"], d)["status"], "FAIL")
        d["copy_deck"][0]["text"] = "₹185 प्रति लीटर"
        self.assertEqual(verify.exact_copy_match(["₹185 प्रति लीटर"], d)["status"], "PASS")

    def test_rentok_v2_n1_graphic_over_the_hero_fails_and_a_clear_layout_passes(self):
        hero = [0.30, 0.35, 0.70, 0.90]
        over = compose.gate("h", "HERO_VISIBLE", G.check_hero_visible, (300, 350, 700, 900), {"c1": (320, 400, 900, 480)}, max_covered_frac=0.05)
        clear = compose.gate("h", "HERO_VISIBLE", G.check_hero_visible, (300, 350, 700, 900), {"c1": (60, 60, 1000, 200)}, max_covered_frac=0.05)
        self.assertEqual((over["status"], clear["status"]), ("FAIL", "PASS"))

    def test_lane_a_d11_black_end_card_declared_blue_fails(self):
        bad = compose.gate("b", "BRAND_COLOUR_ON_RENDERED_FRAME", G.check_brand_colour, [(0, 0, 0)] * 4, "#0239FF")
        good = compose.gate("b", "BRAND_COLOUR_ON_RENDERED_FRAME", G.check_brand_colour, [(1, 55, 253)] * 4, "#0239FF")
        self.assertEqual((bad["status"], good["status"]), ("FAIL", "PASS"))

    def test_a_previously_rejected_file_cannot_be_presented_again(self):
        e = Env()
        try:
            jid = e.submit()
            p = e.dir / "cut1.png"; p.write_bytes(b"same bytes")
            a1 = e.store.add_asset(jid, path=p, kind="image", source="composed", content_type="image/png")
            e.store.add_feedback(jid, asset_id=a1, target=None, text="no", kind="revision", by_user="c")
            p2 = e.dir / "cut2.png"; p2.write_bytes(b"same bytes")
            a2 = e.store.add_asset(jid, path=p2, kind="image", source="composed", content_type="image/png")
            self.assertEqual(verify.not_previously_rejected(e.store, jid, a2)["status"], "FAIL")
        finally:
            e.close()


if __name__ == "__main__":
    unittest.main()
