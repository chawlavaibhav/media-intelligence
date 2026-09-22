"""Regression tests for the deterministic checks promoted from production-learning cases
RENTOK-GAME-A-004 and RENTOK-GAME-B-005 (the RentOK two-lane game film, 2026-09-20/21).

Each test names the defect it closes. Every value used here is the value the independent checker
measured on the job branch (stages/CHECK-STAGE-5.md of each lane), so a test that fails is a test that
would have caught the shipped defect. Nothing here opens a media file or a socket.
"""
from __future__ import annotations

import struct
import unittest
from decimal import Decimal

import _bootstrap as B
from runtime.compositor import gates
from runtime.compositor.gates import LayoutRefused
from runtime.execute.bridge import ExecutionBridge
from runtime.execute.pools import PoolLiquidity
from runtime.loop import container


# ── RENTOK-GAME-B-005 D-1 / D-9, RENTOK-GAME-A-004 D-2: a graphic crossing a text box ────────

class GraphicTextDisjoint(unittest.TestCase):
    def test_b005_d1_phone_rising_over_the_name_tag_is_refused(self):
        # Lane B, 14.9–15.3 s: the phone's top overlapped the `PG OWNER` tag; the text-only check passed.
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_graphic_text_disjoint({"G-phone": (400, 1180, 520, 1320)}, {"C01": (380, 1150, 560, 1200)})
        self.assertEqual(cm.exception.code, "GRAPHIC_OVER_TEXT")
        self.assertEqual(cm.exception.context["pair"], ("G-phone", "C01"))

    def test_a004_d2_text_covering_the_raised_flag_is_refused_symmetrically(self):
        # Lane A, 27.2–27.6 s: the checklist and LEVEL CLEAR! (y 540–666) hid the flag at the top of the pole.
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_graphic_text_disjoint({"G-flag": (700, 540, 780, 700)},
                                              {"CHECKLIST": (200, 540, 760, 666), "LEVEL_CLEAR": (100, 700, 900, 760)})
        self.assertEqual(cm.exception.code, "GRAPHIC_OVER_TEXT")
        self.assertEqual(cm.exception.context["pair"], ("G-flag", "CHECKLIST"))

    def test_b005_d9_a_gap_rule_catches_a_beam_eight_px_under_the_tag(self):
        # Lane B repair round: the beam ran 8 px under the name tag; a 10-px gap rule refuses it, 0 px passes.
        gfx, txt = {"G-beam": (300, 1210, 700, 1230)}, {"C01": (380, 1150, 560, 1202)}
        self.assertEqual(gates.check_graphic_text_disjoint(gfx, txt)["status"], "PASS")
        with self.assertRaises(LayoutRefused):
            gates.check_graphic_text_disjoint(gfx, txt, min_gap_px=10)

    def test_clear_frame_passes_and_reports_every_pair(self):
        r = gates.check_graphic_text_disjoint({"G-phone": (600, 1180, 700, 1320), "G-flag": (900, 300, 960, 500)},
                                              {"C01": (380, 1150, 560, 1200)})
        self.assertEqual(r["status"], "PASS")
        self.assertEqual(r["pairs_checked"], 2)


# ── RENTOK-GAME-B-005 D-3: the announcer 1.2 s ahead of its own words ──────────────────────

class VoTextAlignment(unittest.TestCase):
    FIRST = {"C11": 14.60, "C12": 15.90}          # INSTALLING... / RENTOK MODE: ON, from LAYOUT.json

    def test_b005_d3_v2_at_14_70_before_its_words_at_15_90_is_refused(self):
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_vo_text_alignment([{"id": "V2", "start_s": 14.70, "on_screen_id": "C12"}], self.FIRST)
        self.assertEqual(cm.exception.code, "VO_BEFORE_ITS_TEXT")
        self.assertAlmostEqual(cm.exception.context["lead_s"], 1.2, places=3)

    def test_the_repair_v2_moved_to_15_90_passes(self):
        r = gates.check_vo_text_alignment([{"id": "V2", "start_s": 15.90, "on_screen_id": "C12"}], self.FIRST)
        self.assertEqual(r["status"], "PASS")
        self.assertEqual(r["aligned"][0]["first_on_screen_s"], 15.90)

    def test_a_stated_tolerance_allows_that_much_lead_and_no_more(self):
        line = [{"id": "V2", "start_s": 15.70, "on_screen_id": "C12"}]
        self.assertEqual(gates.check_vo_text_alignment(line, self.FIRST, tolerance_s=0.25)["status"], "PASS")
        with self.assertRaises(LayoutRefused):
            gates.check_vo_text_alignment(line, self.FIRST, tolerance_s=0.1)

    def test_a_paired_string_that_never_appears_is_refused_and_an_unpaired_line_is_listed(self):
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_vo_text_alignment([{"id": "V9", "start_s": 1.0, "on_screen_id": "C99"}], self.FIRST)
        self.assertEqual(cm.exception.code, "VO_BEFORE_ITS_TEXT")
        r = gates.check_vo_text_alignment([{"id": "V0", "start_s": 1.0}], self.FIRST)
        self.assertEqual(r["unpaired"], ["V0"])


# ── RENTOK-GAME-A-004 D-11: the end card the record called #0239FF was black ───────────────

class BrandColourOnTheRenderedFrame(unittest.TestCase):
    def test_a004_d11_black_pixels_against_the_declared_brand_blue_are_refused(self):
        # five sampled pixels of the 29.90-s frame (four corners + centre) were (0,0,0); the record said #0239FF
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_brand_colour([(0, 0, 0)] * 5, "#0239FF", id_="end_card")
        self.assertEqual(cm.exception.code, "BRAND_COLOUR_OFF")
        self.assertEqual(cm.exception.context["worst_delta"], 255)

    def test_the_repaired_frame_after_h264_chroma_drift_passes(self):
        # round 1b: hard-coded (2,57,255); measured on the encoded 29.9-s frame at (540,1500): (1,55,253)
        r = gates.check_brand_colour([(1, 55, 253), (2, 57, 255), (1, 56, 254)], "#0239FF", id_="end_card")
        self.assertEqual(r["status"], "PASS")
        self.assertLessEqual(r["worst_channel_delta"], 2)

    def test_no_samples_is_a_refusal_not_a_pass(self):
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_brand_colour([], "#0239FF")
        self.assertEqual(cm.exception.code, "BRAND_COLOUR_OFF")

    def test_the_limit_is_the_callers_and_the_faint_seam_colour_is_caught_when_tightened(self):
        # Lane A D-8: the logo card's own slightly lighter blue on #0038FF read as a faint rectangle
        seam = [(2, 57, 255)]
        self.assertEqual(gates.check_brand_colour(seam, "#0038FF", max_channel_delta=8)["status"], "PASS")
        with self.assertRaises(LayoutRefused):
            gates.check_brand_colour(seam, "#0038FF", max_channel_delta=0)


# ── RENTOK-GAME-A-004 D-1: two edit lists in a container whose spec said none ───────────────

def _box(fourcc: bytes, payload: bytes = b"") -> bytes:
    return struct.pack(">I", 8 + len(payload)) + fourcc + payload


def _mp4(edit_lists_per_track: tuple) -> bytes:
    """A minimal MP4 box tree: ftyp, moov with one trak per entry, each trak carrying that many elst boxes
    inside edts, then mdat whose payload deliberately contains the letters 'elst' (a byte grep would count it)."""
    traks = b""
    for n in edit_lists_per_track:
        edts = _box(b"edts", b"".join(_box(b"elst", b"\x00" * 20) for _ in range(n)))
        traks += _box(b"trak", _box(b"tkhd", b"\x00" * 84) + (edts if n else b"") + _box(b"mdia", b""))
    moov = _box(b"moov", _box(b"mvhd", b"\x00" * 100) + traks)
    return _box(b"ftyp", b"isom\x00\x00\x02\x00isomiso2avc1mp41") + moov + _box(b"mdat", b"payload elst elst elst")


class ContainerEditLists(unittest.TestCase):
    def test_a004_d1_the_ffmpeg_default_two_elst_boxes_fail(self):
        row = container.assess_edit_lists(_mp4((1, 1)))     # video B-frame delay + AAC priming, one per track
        self.assertEqual(row["status"], "FAIL")
        self.assertTrue(row["blocking"])
        self.assertIn("2 elst", row["detail"])

    def test_the_re_muxed_file_with_no_edit_lists_passes_and_names_the_tracks(self):
        row = container.assess_edit_lists(_mp4((0, 0)))
        self.assertEqual(row["status"], "PASS")
        self.assertIn("0 elst boxes across 2 track(s)", row["detail"])

    def test_the_walk_is_a_box_walk_not_a_byte_grep(self):
        data = _mp4((0,))
        self.assertGreaterEqual(data.count(b"elst"), 3)          # the payload carries the letters
        self.assertEqual(container.count_boxes(data, b"elst"), 0)

    def test_no_bytes_or_no_moov_is_not_run_never_pass(self):
        self.assertEqual(container.assess_edit_lists(b"")["status"], "NOT-RUN")
        row = container.assess_edit_lists(_box(b"ftyp", b"isom") + _box(b"free", b"\x00" * 8))
        self.assertEqual(row["status"], "NOT-RUN")
        self.assertIn("no moov", row["detail"])

    def test_a_largesize_box_is_walked(self):
        elst = _box(b"elst", b"\x00" * 20)
        edts_payload = elst
        edts_large = struct.pack(">I", 1) + b"edts" + struct.pack(">Q", 16 + len(edts_payload)) + edts_payload
        trak = _box(b"trak", edts_large)
        data = _box(b"ftyp", b"isom") + _box(b"moov", trak)
        self.assertEqual(container.count_boxes(data, b"elst"), 1)


# ── RENTOK-GAME-B-005 att-016 / T1: a reservation written before the input was checked ─────

class HarnessRefusedAttemptsReserveNothing(unittest.TestCase):
    """Lane B's dispatcher reserved a transcription and then found the input file did not exist; the
    reservation stayed on the ledger by rule. The bridge had the same ordering fault: an attempt the
    harness refused (unresolved input) still added its cost to the running ceiling and drew the pool
    down, so a later sendable attempt could be blocked_by_pool by money set aside for a call that
    could never leave."""

    @classmethod
    def setUpClass(cls):
        ev = B.evidence_base()
        pb = B.price_book(ev)
        r = B.router(ev, pb)
        cls.bridge = ExecutionBridge(evidence=ev, prices=pb, identities=r.identities)
        cls.spec = B.spec(B.SPEC_MOTION)                       # needs plate_accepted_draw; unresolved → refused
        cls.prof = B.profile("dry", ev)
        cls.decision = r.plan(cls.spec, cls.prof, customer_ref="cust-004-005")
        cls.pool = cls.decision["primary"]["billing_pool"]

    def _pools(self, balance: str) -> PoolLiquidity:
        return PoolLiquidity.from_readings([{"pool": self.pool, "balance_usd": balance,
                                             "read_utc": "2026-09-21T00:00:00Z", "source": "test reading"}])

    def test_b005_att016_a_harness_refused_attempt_reserves_neither_ceiling_nor_pool(self):
        pools = self._pools("1.00")                            # funds any ONE attempt, not the four together (2.304)
        m = self.bridge.build(self.spec, self.decision, self.prof, prompt_text="p", customer_ref="cust-004-005",
                              pools=pools)
        self.assertEqual(m["ceiling"]["reserved_total_usd"], "0")
        self.assertEqual(Decimal(pools.reading(self.pool)["remaining_usd"]), Decimal("1.00"))
        for a in m["attempts"]:
            self.assertIn("harness: input_unresolved", a["refusal_reason"])
            self.assertIn("not_reserved", a["refusal_reason"])
            self.assertEqual(a["ceiling"]["reserved_before_this_usd"], "0")
            self.assertFalse(a["blocked_by_ceiling"])
            self.assertFalse(a["blocked_by_pool"], a["pool_liquidity"])   # the pool was never drawn down by a refusal
            self.assertFalse(a["would_dispatch"])

    def test_a_resolvable_attempt_still_reserves_in_order(self):
        still = {"image_url": "sealed://accepted-still/job-fixture-A/sha256/0000"}
        pools = self._pools("1.00")
        m = self.bridge.build(self.spec, self.decision, self.prof, prompt_text="p", customer_ref="cust-004-005",
                              inputs=still, pools=pools)
        primary = [a for a in m["attempts"] if a["slot"] == "primary"]
        self.assertTrue(primary[0]["would_dispatch"], primary[0]["refusal_reason"])
        self.assertLess(Decimal(pools.reading(self.pool)["remaining_usd"]), Decimal("1.00"))
        self.assertGreater(Decimal(m["ceiling"]["reserved_total_usd"]), Decimal("0"))


if __name__ == "__main__":
    unittest.main()
