"""runtime/compositor — deterministic layout gates promoted from production-learning case UPWORK-INTRO-001.

Every gate is a pure function over geometry and colour; pixel reading stays with the caller. Each test names
the V3/V4 defect it encodes (SYSTEM-DEFECTS.yaml SD-01..SD-04, SD-07). Nothing here draws anything.
"""
from __future__ import annotations

import unittest

import _bootstrap  # noqa: F401
from runtime.compositor import gates
from runtime.compositor.gates import LayoutRefused
from runtime.compositor.tokens import DesignTokens

CANVAS = (0, 0, 1920, 1080)
TOKENS = DesignTokens(card_radius=26, card_border_px=1, card_shadow=(28, 14, 56), safe_x=120, safe_y=90)


class TextBounds(unittest.TestCase):                       # SD-01: text cut off
    def test_text_that_would_extend_beyond_the_canvas_is_refused(self):
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_text_bounds((1700, 900, 2100, 980), canvas=CANVAS)
        self.assertEqual(cm.exception.code, "TEXT_OUT_OF_CANVAS")

    def test_text_that_would_extend_outside_its_card_is_refused(self):
        card = (200, 200, 800, 500)
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_text_bounds((600, 300, 900, 360), container=card, canvas=CANVAS)
        self.assertEqual(cm.exception.code, "TEXT_OUT_OF_CONTAINER")

    def test_text_inside_both_passes_and_reports_the_boxes(self):
        r = gates.check_text_bounds((220, 220, 700, 280), container=(200, 200, 800, 500), canvas=CANVAS)
        self.assertEqual(r["status"], "PASS")
        self.assertEqual(r["box"], (220, 220, 700, 280))

    def test_safe_area_from_tokens_is_the_container_when_none_is_given(self):
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_text_bounds((10, 10, 300, 60), canvas=CANVAS, tokens=TOKENS)
        self.assertEqual(cm.exception.code, "TEXT_OUT_OF_CONTAINER")
        self.assertIn("safe area", str(cm.exception))


class Contrast(unittest.TestCase):                          # SD-02: text colour lost on backgrounds
    # relative luminance samples of the pixels behind a box: a bright photo (0.8–0.95) and a mid tone (0.4)
    BRIGHT_PHOTO = [0.80, 0.92, 0.95, 0.88]

    def test_wrapper_text_below_threshold_is_refused(self):
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_contrast("#F3EFE7", self.BRIGHT_PHOTO, role="body")   # cream on a bright photo
        self.assertEqual(cm.exception.code, "CONTRAST_BELOW_THRESHOLD")
        self.assertLess(cm.exception.context["worst_ratio"], 4.5)

    def test_same_text_with_an_opaque_backing_passes(self):
        r = gates.check_contrast("#F3EFE7", self.BRIGHT_PHOTO, role="body", backing_hex="#111111")
        self.assertEqual(r["status"], "PASS")
        self.assertGreaterEqual(r["worst_ratio"], 4.5)
        self.assertEqual(r["measured_against"], "backing")

    def test_a_translucent_backing_does_not_count_as_opaque(self):
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_contrast("#F3EFE7", self.BRIGHT_PHOTO, role="body", backing_hex="#111111",
                                 backing_alpha=0.6)
        self.assertEqual(cm.exception.code, "CONTRAST_BELOW_THRESHOLD")

    def test_display_size_uses_the_display_threshold(self):
        # ink (#111111, L≈0.0056) on a dark grey (L 0.13–0.15): worst ratio ≈ 3.2 — fails body (4.5), passes display (3.0)
        samples = [0.13, 0.15, 0.14]
        with self.assertRaises(LayoutRefused):
            gates.check_contrast("#111111", samples, role="body")
        r = gates.check_contrast("#111111", samples, role="display")
        self.assertEqual(r["status"], "PASS")

    def test_an_interior_sample_near_the_text_luminance_is_the_worst_case(self):
        # Controller audit on PR #98, blocker 1: contrast is minimised where the background is CLOSEST to
        # the text luminance, which can be an interior sample. #808080 has L≈0.216; the endpoints 0.0 and
        # 1.0 give 5.3:1 and 3.95:1 (display passes at 3.0), but the 0.21 pixel is ≈1.0:1 — unreadable.
        samples = [0.0, 0.21, 1.0]
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_contrast("#808080", samples, role="display")
        self.assertLess(cm.exception.context["worst_ratio"], 1.2)
        r = gates.check_contrast("#808080", [0.0, 1.0], role="display")   # the same endpoints alone pass
        self.assertEqual(r["status"], "PASS")

    def test_worst_case_is_the_ratio_reported(self):
        r = gates.check_contrast("#111111", [0.05, 0.9], role="body", backing_hex="#FFFFFF")
        self.assertEqual(r["measured_against"], "backing")
        self.assertAlmostEqual(r["worst_ratio"], gates.contrast_ratio(gates.relative_luminance("#111111"), 1.0), places=3)


class CropFit(unittest.TestCase):                           # SD-03: creatives cropped
    def test_undeclared_destructive_crop_is_refused(self):
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_fit({"id": "proof-1", "fit": "cover", "source_size": (1280, 1600), "box": (0, 0, 1920, 1080)})
        self.assertEqual(cm.exception.code, "UNDECLARED_COVER_CROP")

    def test_declared_validated_cover_crop_passes_and_reports_the_fraction(self):
        r = gates.check_fit({"id": "bubble", "fit": "cover", "source_size": (1920, 1080), "box": (0, 0, 200, 200),
                             "declared_crop": {"box": (860, 240, 1060, 440), "reason": "speaker face for the trust bubble"}})
        self.assertEqual(r["status"], "PASS")
        self.assertEqual(r["fit"], "cover(declared)")
        self.assertAlmostEqual(r["fraction_shown"], (200 * 200) / (1920 * 1080), places=4)

    def test_declared_crop_without_a_reason_is_refused(self):
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_fit({"id": "x", "fit": "cover", "source_size": (1920, 1080), "box": (0, 0, 200, 200),
                             "declared_crop": {"box": (0, 0, 200, 200)}})
        self.assertEqual(cm.exception.code, "UNDECLARED_COVER_CROP")

    def test_declared_crop_box_outside_the_source_is_refused(self):
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_fit({"id": "x", "fit": "cover", "source_size": (1920, 1080), "box": (0, 0, 200, 200),
                             "declared_crop": {"box": (1800, 1000, 2000, 1200), "reason": "r"}})
        self.assertEqual(cm.exception.code, "UNDECLARED_COVER_CROP")

    def test_contain_is_the_default_and_shows_everything(self):
        r = gates.check_fit({"id": "proof-1", "source_size": (1280, 1600), "box": (0, 0, 1920, 1080)})
        self.assertEqual(r["fit"], "contain")
        self.assertEqual(r["fraction_shown"], 1.0)
        self.assertEqual(r["rendered_size"], (864, 1080))

    def test_native_needs_the_exact_box_size(self):
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_fit({"id": "kora", "fit": "native", "source_size": (1600, 900), "box": (0, 0, 1920, 1080)})
        self.assertEqual(cm.exception.code, "UNDECLARED_COVER_CROP")


class GeometryTokens(unittest.TestCase):                    # SD-04: square + rounded cards
    def test_tokens_are_immutable(self):
        with self.assertRaises(Exception):
            TOKENS.card_radius = 0                                     # type: ignore[misc]

    def test_a_card_off_the_token_radius_is_refused(self):
        cards = [{"id": "brief", "radius": 26, "border_px": 1, "shadow": (28, 14, 56)},
                 {"id": "intake", "radius": 0, "border_px": 1, "shadow": (28, 14, 56)}]
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_geometry(cards, TOKENS)
        self.assertEqual(cm.exception.code, "GEOMETRY_OFF_TOKEN")
        self.assertIn("intake", str(cm.exception))

    def test_cards_built_from_the_tokens_pass_and_report_one_radius(self):
        cards = [gates.card_geometry(TOKENS, id_="a"), gates.card_geometry(TOKENS, id_="b")]
        r = gates.check_geometry(cards, TOKENS)
        self.assertEqual(r["status"], "PASS")
        self.assertEqual(r["radii_used"], [26])

    def test_a_card_with_no_token_source_is_refused(self):
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_geometry([{"id": "x", "radius": 26}], TOKENS)
        self.assertEqual(cm.exception.code, "GEOMETRY_OFF_TOKEN")


class Disjointness(unittest.TestCase):                      # SD-07: offer / code collision
    def test_offer_and_cta_collision_is_refused(self):
        regions = {"headline": (100, 100, 900, 220), "offer": (100, 300, 520, 380), "cta": (500, 340, 900, 420),
                   "code": (100, 460, 500, 510), "legal": (100, 560, 900, 590)}
        with self.assertRaises(LayoutRefused) as cm:
            gates.check_disjoint(regions)
        self.assertEqual(cm.exception.code, "CRITICAL_REGIONS_OVERLAP")
        self.assertEqual(cm.exception.context["pair"], ("cta", "offer"))

    def test_disjoint_regions_pass_and_list_every_pair_checked(self):
        regions = {"headline": (100, 100, 900, 220), "offer": (100, 300, 520, 380), "cta": (100, 400, 900, 480),
                   "code": (100, 500, 500, 550), "legal": (100, 600, 900, 630)}
        r = gates.check_disjoint(regions)
        self.assertEqual(r["status"], "PASS")
        self.assertEqual(r["pairs_checked"], 10)

    def test_edge_touching_counts_as_overlap_when_a_gap_is_required(self):
        regions = {"offer": (100, 300, 520, 380), "code": (520, 300, 900, 380)}
        self.assertEqual(gates.check_disjoint(regions)["status"], "PASS")
        with self.assertRaises(LayoutRefused):
            gates.check_disjoint(regions, min_gap_px=12)

    def test_non_critical_regions_are_ignored_unless_named(self):
        regions = {"offer": (100, 300, 520, 380), "decor": (100, 300, 520, 380)}
        self.assertEqual(gates.check_disjoint(regions)["status"], "PASS")
        with self.assertRaises(LayoutRefused):
            gates.check_disjoint(regions, critical=("offer", "decor"))


if __name__ == "__main__":
    unittest.main()
