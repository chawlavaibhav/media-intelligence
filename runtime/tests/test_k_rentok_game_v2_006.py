"""Regression tests for the deterministic checks promoted from production-learning case
RENTOK-GAME-V2-006 (the RentOK game film re-made "the Treatment C way", 2026-09-21).

Each test names the defect it closes. Every box, fraction, scale and pixel height used here is the value
recorded on the job branch at b06deaf7907de9c64d574a5f042a014c2e519ce6 — the layout log
`gen/final-v3-audio-layout.jsonl`, the cut-out records `gen/assets/*_cutout.json`, `board.json` and the
independent checker's `stages/CHECK-STAGE-5.md` — so a test that fails is a test that would have caught
the shipped defect. Nothing here opens a media file or a socket.
"""
from __future__ import annotations

import unittest

import _bootstrap as B  # noqa: F401  (puts the checkout root on sys.path)
from runtime.compositor import gates
from runtime.compositor.gates import LayoutRefused


# ── N1 / N2: a graphic drawn in front of the hero covers him at his best moments ──────────────

class HeroVisible(unittest.TestCase):
    # layout log frame 800 (26.667 s): OWNER cheer [461,980,744,1394]; FLAG [551,1197,739,1310] drawn in front
    OWNER_800 = (461, 980, 744, 1394)
    FLAG_800 = (551, 1197, 739, 1310)

    def test_n1_flag_rising_through_the_cheering_owner_is_refused(self):
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_hero_visible(self.OWNER_800, {"FLAG": self.FLAG_800}, id_="owner@f800")
        self.assertEqual(cm.exception.code, "HERO_OCCLUDED")
        self.assertEqual(cm.exception.context["graphic"], "FLAG")
        # the flag box sits wholly inside his: 188 x 113 of 283 x 414 px ≈ 18 %
        self.assertAlmostEqual(cm.exception.context["covered_frac"], 0.1813, places=3)

    def test_n1_the_c5b_text_gate_could_not_see_it(self):
        # the job's C5b (graphic-vs-text) reported 0 overlaps on the same frame: no text box is involved
        r = gates.check_graphic_text_disjoint({"FLAG": self.FLAG_800, "OWNER": self.OWNER_800},
                                              {"LEVEL_CLEAR": (200, 600, 880, 680)})
        self.assertEqual(r["status"], "PASS")

    def test_n2_phone_over_the_face_at_the_windup_is_refused_but_the_held_phone_is_not(self):
        # frame 546 (18.2 s): OWNER windup [72,1042,431,1561] (519 px tall); head = top fifth → y 1042..1146;
        # PHONE [204,1094,316,1286] crosses the head band. Frame 552 (18.4 s, fire): OWNER [60,1042,522,1561],
        # PHONE [428,1198,540,1390] — in his hand, below the head.
        head_546 = (72, 1042, 431, 1146)
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_hero_visible(head_546, {"PHONE": (204, 1094, 316, 1286)}, id_="owner_face@f546")
        self.assertEqual(cm.exception.code, "HERO_OCCLUDED")
        self.assertGreater(cm.exception.context["covered_frac"], 0.15)
        head_552 = (60, 1042, 522, 1146)
        r = gates.check_hero_visible(head_552, {"PHONE": (428, 1198, 540, 1390)}, id_="owner_face@f552")
        self.assertEqual(r["status"], "PASS")
        self.assertEqual(r["covered_frac"]["PHONE"], 0.0)

    def test_a_stated_tolerance_is_the_callers_and_bounded(self):
        r = gates.check_hero_visible(self.OWNER_800, {"FLAG": self.FLAG_800}, max_covered_frac=0.2)
        self.assertEqual(r["status"], "PASS")
        with self.assertRaises(ValueError):
            gates.check_hero_visible(self.OWNER_800, {}, max_covered_frac=1.0)

    def test_nothing_in_front_passes_with_nothing_checked(self):
        r = gates.check_hero_visible(self.OWNER_800, {})
        self.assertEqual(r["status"], "PASS")
        self.assertEqual(r["foreground"], [])


# ── A-4 / R-1 / N4: the framing target is read at the focus frame, per pose, inside the frame ──

class FramingTarget(unittest.TestCase):
    # board.json F4: focus_t 8.55 s → frame 256 (30 fps); target 0.21 (reach pose). Layout log owner_frac:
    # 8.40 s 0.156 (camera still easing), 8.55 s 0.216 (the hold, delivered file). final-v1 measured 0.202 (R-1).
    LOG = {252: 0.156, 253: 0.19, 254: 0.197, 255: 0.209, 256: 0.216, 257: 0.218}

    def test_r1_final_v1_reach_pose_at_0_202_against_0_21_is_refused(self):
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_framing_target({256: 0.202}, focus_frame=256, target=0.21, beat="F4")
        self.assertEqual(cm.exception.code, "FRAMING_BELOW_TARGET")
        self.assertEqual(cm.exception.context["measured"], 0.202)

    def test_the_delivered_file_at_the_hold_passes(self):
        r = gates.check_framing_target(self.LOG, focus_frame=256, target=0.21, beat="F4")
        self.assertEqual(r["status"], "PASS")
        self.assertEqual(r["measured"], 0.216)

    def test_a4_measuring_mid_ease_fails_for_the_wrong_reason_and_is_visible_as_such(self):
        # focus placed at the camera keyframe start (8.40 s, frame 252) instead of the hold: 0.156 < 0.21
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_framing_target(self.LOG, focus_frame=252, target=0.21, beat="F4")
        self.assertEqual(cm.exception.context["focus_frame"], 252)
        self.assertEqual(cm.exception.context["measured"], 0.156)

    def test_a_focus_frame_missing_from_the_log_is_a_refusal_not_a_pass(self):
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_framing_target(self.LOG, focus_frame=870, target=0.0, beat="F11")
        self.assertEqual(cm.exception.code, "FRAMING_FRAME_MISSING")
        with self.assertRaises(LayoutRefused):
            gates.check_framing_target({256: None}, focus_frame=256, target=0.21, beat="F4")

    def test_per_pose_targets_a_crouched_pose_is_short_by_design(self):
        # F5 cover pose: target 0.16 (board), measured 0.206 at frame 357 — a per-pose target, not F2's 0.25
        self.assertEqual(gates.check_framing_target({357: 0.206}, focus_frame=357, target=0.16, beat="F5")["status"], "PASS")
        with self.assertRaises(LayoutRefused):
            gates.check_framing_target({357: 0.206}, focus_frame=357, target=0.25, beat="F5")

    def test_n4_dazed_owner_52_px_off_the_left_edge_is_refused_when_the_canvas_is_given(self):
        # frame 113 (3.767 s): OWNER dazed screen box [-52,1062,205,1542] on a 1080x1920 canvas; owner_frac 0.25
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_framing_target({113: 0.25}, focus_frame=113, target=0.2, beat="F2",
                                       hero_box=(-52, 1062, 205, 1542), canvas=(0, 0, 1080, 1920))
        self.assertEqual(cm.exception.code, "HERO_CLIPPED_BY_FRAME")
        r = gates.check_framing_target({113: 0.25}, focus_frame=113, target=0.2, beat="F2",
                                       hero_box=(8, 1062, 265, 1542), canvas=(0, 0, 1080, 1920))
        self.assertEqual(r["status"], "PASS")


# ── LJ-15 / DET 'world fills the frame': every camera scale >= 1.0 ──────────────────────────

class WorldFillsFrame(unittest.TestCase):
    def test_the_delivered_films_camera_range_1_0_to_1_6_passes(self):
        r = gates.check_world_fills_frame([(0, 1.0), (99, 1.5), (546, 1.6), (899, 1.0)])
        self.assertEqual(r["status"], "PASS")
        self.assertEqual((r["min_scale"], r["max_scale"]), (1.0, 1.6))

    def test_a_pull_out_below_1_0_is_refused_at_its_frame(self):
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_world_fills_frame([1.0, 1.2, 0.9, 1.0])
        self.assertEqual(cm.exception.code, "WORLD_SMALLER_THAN_FRAME")
        self.assertEqual(cm.exception.context["frame"], 2)

    def test_no_logged_camera_is_a_refusal_not_a_pass(self):
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_world_fills_frame([])
        self.assertEqual(cm.exception.code, "WORLD_SMALLER_THAN_FRAME")


# ── N5 / LJ-11: one character drawn from sheets of different pixel density ────────────────────

class SpriteDensity(unittest.TestCase):
    # owner_cutout.json idle h 561; c_cutout.json brace/windup/fire h 344; v2_cutout.json standing_cell_h 342
    SHEETS = {"base_A1": 561, "C-A1": 344, "V2-S1": 342}

    def test_n5_the_two_expression_sheets_at_61_pct_of_the_base_sheet_are_refused(self):
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_sprite_density(self.SHEETS)
        self.assertEqual(cm.exception.code, "SPRITE_DENSITY_MISMATCH")
        self.assertEqual((cm.exception.context["smallest"], cm.exception.context["largest"]), ("V2-S1", "base_A1"))
        self.assertAlmostEqual(cm.exception.context["ratio"], 0.6096, places=3)

    def test_the_two_expression_sheets_agree_with_each_other(self):
        r = gates.check_sprite_density({"C-A1": 344, "V2-S1": 342})
        self.assertEqual(r["status"], "PASS")
        self.assertAlmostEqual(r["ratio"], 0.9942, places=3)

    def test_the_threshold_is_the_callers_and_one_sheet_is_nothing_to_compare(self):
        self.assertEqual(gates.check_sprite_density(self.SHEETS, min_ratio=0.6)["status"], "PASS")
        self.assertEqual(gates.check_sprite_density({"base_A1": 561})["status"], "PASS")
        with self.assertRaises(ValueError):
            gates.check_sprite_density({"x": 0, "y": 10})


if __name__ == "__main__":
    unittest.main()
