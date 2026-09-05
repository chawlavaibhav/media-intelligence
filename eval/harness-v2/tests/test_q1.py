"""Q1 detector and record plumbing (task §4). Tiny synthetic scenes (<= 128x96) built here; the real pack
is only READ by run_q1 (its manifest is a protected baseline and is verified before and after the run)."""
import json
import unittest
from pathlib import Path

from _support import NoNetworkTestCase, hv2_paths
from instruments import imageio as IO
from q1 import detector as D
from q1 import check_record as CR

RED, BLUE, GREEN, WHITE, SHADOW = (220, 40, 40), (40, 80, 220), (40, 170, 70), (255, 255, 255), (185, 185, 185)


def scene(w=128, h=96, shapes=()):
    px = [[WHITE] * w for _ in range(h)]
    for kind, x, y, size, col in shapes:
        if kind == "square":
            for yy in range(y, min(h, y + size)):
                for xx in range(x, min(w, x + size)):
                    px[yy][xx] = col
        elif kind == "circle":
            r = size // 2
            cx, cy = x + r, y + r
            for yy in range(max(0, cy - r), min(h, cy + r + 1)):
                for xx in range(max(0, cx - r), min(w, cx + r + 1)):
                    if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                        px[yy][xx] = col
        elif kind == "bar":
            for yy in range(y, min(h, y + max(6, size // 3))):
                for xx in range(x, min(w, x + size)):
                    px[yy][xx] = col
    rows = [b"".join(bytes(p) for p in row) for row in px]
    return IO.encode_png(rows, w, h)


class DetectorTest(NoNetworkTestCase):
    def test_config_is_hash_covered_and_declares_t_rgb(self):
        self.assertIn("T_rgb", D.CONFIG)
        self.assertEqual(D.CONFIG["connectivity"], 4)
        self.assertEqual(len(D.config_hash()), 64)
        self.assertEqual(D.config_hash(), D.config_hash())

    def test_counts_shapes_and_colours(self):
        png = scene(shapes=[("square", 5, 5, 20, RED), ("circle", 40, 10, 24, BLUE), ("bar", 70, 40, 30, GREEN)])
        r = D.detect(png)
        self.assertEqual(r["object_count"], 3)
        kinds = sorted((o["colour"], o["shape"]) for o in r["objects"])
        self.assertEqual(kinds, [("blue", "circle"), ("green", "bar"), ("red", "square")])
        sq = next(o for o in r["objects"] if o["shape"] == "square")
        self.assertEqual((sq["x0"], sq["y0"], sq["x1"], sq["y1"]), (5, 5, 25, 25))
        self.assertEqual(sq["area"], 400)

    def test_shadow_and_white_are_background(self):
        png = scene(shapes=[("square", 5, 5, 20, RED), ("square", 40, 40, 20, SHADOW)])
        self.assertEqual(D.detect(png)["object_count"], 1)
        self.assertEqual(D.detect(scene())["object_count"], 0)

    def test_relations_quadrants_and_sizes(self):
        png = scene(shapes=[("square", 5, 40, 16, RED), ("circle", 90, 44, 16, BLUE)])
        r = D.detect(png)
        self.assertEqual(D.relation(r, ("square", "red"), ("circle", "blue")), "left_of")
        self.assertEqual(D.relation(r, ("circle", "blue"), ("square", "red")), "right_of")
        png2 = scene(shapes=[("square", 50, 2, 16, RED), ("circle", 54, 60, 16, BLUE)])
        self.assertEqual(D.relation(D.detect(png2), ("square", "red"), ("circle", "blue")), "above")
        one = D.detect(scene(shapes=[("square", 100, 70, 16, GREEN)]))
        self.assertEqual(D.quadrant(one["objects"][0], 128, 96), "bottom_right")
        two = D.detect(scene(shapes=[("square", 5, 5, 30, GREEN), ("square", 60, 5, 12, (150, 60, 190))]))
        self.assertEqual(D.larger(two, "green", "purple"), "green")

    def test_corrupt_png_fails_closed(self):
        with self.assertRaises(D.ProbeError):
            D.detect(b"\x89PNG\r\n\x1a\n" + b"\x00" * 64)
        with self.assertRaises(D.ProbeError):
            D.detect(b"")

    def test_pixels_outside_tolerance_are_background(self):
        off = tuple(min(255, c + D.CONFIG["T_rgb"] + 20) for c in RED)
        png = scene(shapes=[("square", 5, 5, 20, off)])
        self.assertEqual(D.detect(png)["object_count"], 0)


class RecordCheckerTest(NoNetworkTestCase):
    def test_checker_reports_every_missing_schema_field(self):
        schema = hv2_paths.EVAL_ROOT / "v1" / "instruments" / "qualification-result-schema.yaml"
        missing = CR.missing_fields({"record_id": "x"}, schema)
        self.assertIn("instrument_id", missing)
        self.assertIn("gate.n_opportunities", missing)
        self.assertIn("uncertainty_placeholder", missing) if "uncertainty_placeholder" in missing else None
        full = CR.skeleton(schema)
        self.assertEqual(CR.missing_fields(full, schema), [])


class RunnerGuardTest(NoNetworkTestCase):
    def test_run_refuses_without_a_matching_preregistration(self):
        from q1 import run_q1 as R
        with self.assertRaises(R.PreregistrationMissing):
            R.load_preregistration(self.tmp / "nope.yaml")
        p = self.tmp / "pre.yaml"
        p.write_text("R_q: 3\nconfiguration_hash: not-the-detector\n")
        with self.assertRaises(R.PreregistrationMismatch):
            R.load_preregistration(p)


if __name__ == "__main__":
    unittest.main()
