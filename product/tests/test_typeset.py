"""Typesetting track (product/typeset): fonts, line breaking, layout, checks, picker, taste. USD 0, no network."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from product.typeset import checks as C
from product.typeset import engine as E
from product.typeset import picker, taste

COPY = [{"id": "C01", "text": "Room for the long way home.", "role": "headline"},
        {"id": "C02", "text": "mokobara.com", "role": "small"}]


def _logo(d: Path) -> Path:
    im = Image.new("RGBA", (600, 200), (0, 0, 0, 0))
    ImageDraw.Draw(im).rectangle((40, 60, 560, 140), fill=(16, 24, 32, 255))
    p = d / "logo.png"
    im.save(p)
    return p


def _plate(d: Path, busy=False) -> Path:
    im = Image.new("RGB", (900, 1125), (240, 236, 228))
    if busy:
        a = (np.random.default_rng(1).random((1125, 900, 3)) * 255).astype("uint8")
        im = Image.fromarray(a)
    ImageDraw.Draw(im).rectangle((200, 250, 700, 1000), fill=(30, 45, 90))
    p = d / ("busy.png" if busy else "plate.png")
    im.save(p)
    return p


class Fonts(unittest.TestCase):
    def test_every_font_file_is_present_licensed_and_unchanged(self):
        src = json.loads((E.FONT_DIR / "SOURCES.json").read_text())
        for rel, meta in src.items():
            p = E.FONT_DIR / rel
            self.assertTrue(p.exists(), rel)
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), meta["sha256"], rel)
        for fid, fam in E.fonts_registry()["families"].items():
            folder = E.font_file(fid, 400).parent
            self.assertTrue((folder / "OFL.txt").exists(), f"{fid} has no licence file")

    def test_weight_axis_is_applied(self):
        light = E.load_font("inter", 300, 80).getlength("Room for the long way home.")
        bold = E.load_font("inter", 800, 80).getlength("Room for the long way home.")
        self.assertGreater(bold, light)

    def test_devanagari_uses_a_devanagari_face_and_draws_no_tofu(self):
        fid, weight, _ = E._face("headline", "घर का लंबा रास्ता", E.system("quiet_premium"), E.BrandKit())
        self.assertIn("devanagari", E._family(fid)["scripts"])
        self.assertEqual(E.missing_glyphs("घर का लंबा रास्ता", fid, weight), [])

    def test_every_system_names_real_families(self):
        fams = E.fonts_registry()["families"]
        for sid, s in E.fonts_registry()["systems"].items():
            for role in ("display", "text"):
                self.assertIn(s[role]["family"], fams, sid)
            self.assertIn(s["devanagari"], fams, sid)


class Breaking(unittest.TestCase):
    def test_no_single_word_left_alone_when_avoidable(self):
        f = E.load_font("inter", 600, 90)
        lines = E.balanced_lines("Room for the long way home.", f, int(f.getlength("Room for the long way")), 3)
        self.assertIsNotNone(lines)
        self.assertGreater(len(lines[-1].split()), 1, lines)

    def test_returns_none_when_it_cannot_fit(self):
        f = E.load_font("inter", 600, 90)
        self.assertIsNone(E.balanced_lines("Supercalifragilistic", f, 100, 3))

    def test_logo_role_is_never_typeset(self):
        deck = [{"id": "C01", "text": "Room for the long way home.", "role": "Headline"},
                {"id": "C02", "text": "mokobara.com", "role": "Website and CTA"},
                {"id": "C03", "text": "Mokobara", "role": "Supplied logo asset used unaltered"}]
        roles = E.roles_from_copy_deck(deck)
        self.assertEqual([r["role"] for r in roles], ["headline", "small"])


class Layouts(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.kit = E.BrandKit(logo=_logo(self.tmp), moods=["premium", "calm"])

    def test_exact_copy_and_checks_on_a_clean_poster(self):
        L = E.layout(template_id="top_center_stack", fmt="4:5", system_id="modern_clean", kit=self.kit, copy=COPY,
                     plate=_plate(self.tmp), product_box_norm=[0.2, 0.2, 0.8, 0.9])
        rows = {r["check_id"]: r for r in C.run(L)}
        self.assertEqual(rows["exact_copy"]["status"], "PASS")
        self.assertEqual(C.blocking_failures(list(rows.values())), [], rows)
        drawn = " ".join(" ".join(e.lines) for e in L["elements"] if e.kind == "text")
        self.assertEqual(drawn, "Room for the long way home. mokobara.com")

    def test_reels_endcard_stays_inside_instagram_safe_area(self):
        for tid in ("endcard_center", "endcard_line_first"):
            L = E.layout(template_id=tid, fmt="9:16", system_id="quiet_premium", kit=self.kit, copy=COPY)
            rows = {r["check_id"]: r for r in C.run(L)}
            self.assertEqual(rows["safe_area"]["status"], "PASS", (tid, rows["safe_area"]))

    def test_text_over_a_busy_picture_is_refused(self):
        L = E.layout(template_id="minimal_corner", fmt="4:5", system_id="quiet_premium", kit=self.kit, copy=COPY,
                     plate=_plate(self.tmp, busy=True), product_box_norm=[0.2, 0.2, 0.8, 0.9])
        rows = {r["check_id"]: r for r in C.run(L)}
        self.assertEqual(rows["calm_ground"]["status"], "FAIL")

    def test_text_over_the_product_is_refused(self):
        L = E.layout(template_id="minimal_corner", fmt="4:5", system_id="quiet_premium", kit=self.kit, copy=COPY,
                     plate=_plate(self.tmp), product_box_norm=[0.0, 0.0, 1.0, 1.0])
        rows = {r["check_id"]: r for r in C.run(L)}
        self.assertEqual(rows["product_clear"]["status"], "FAIL")

    def test_dark_logo_on_dark_panel_is_refused_only_when_the_brand_forbids_reversing(self):
        self.kit.logo_reversible = False
        L = E.layout(template_id="panel_bottom", fmt="4:5", system_id="quiet_premium", kit=self.kit, copy=COPY,
                     plate=_plate(self.tmp), product_box_norm=[0.2, 0.2, 0.8, 0.9])
        self.assertEqual({r["check_id"]: r for r in C.run(L)}["logo"]["status"], "FAIL")
        self.kit.logo_reversible = True
        L = E.layout(template_id="panel_bottom", fmt="4:5", system_id="quiet_premium", kit=self.kit, copy=COPY,
                     plate=_plate(self.tmp), product_box_norm=[0.2, 0.2, 0.8, 0.9])
        self.assertEqual({r["check_id"]: r for r in C.run(L)}["logo"]["status"], "PASS")

    def test_every_headline_minimum_is_phone_legible(self):
        floor = E.MIN_CSS_PX["headline"] / E.PHONE_CSS_WIDTH
        for tid, t in E.templates_registry()["templates"].items():
            self.assertGreaterEqual(t["headline"]["min_size"], floor, tid)

    def test_brand_font_replaces_the_system_face(self):
        kit = E.BrandKit(logo=self.kit.logo, fonts={"display": {"file": str(E.font_file("fraunces", 600)), "weight": 600}})
        L = E.layout(template_id="endcard_center", fmt="9:16", system_id="modern_clean", kit=kit, copy=COPY)
        head = next(e for e in L["elements"] if e.role == "headline")
        self.assertEqual(head.family, "brand_display")


class Additions(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.kit = E.BrandKit(logo=_logo(self.tmp), moods=["premium", "calm"])

    def test_capitals_are_tracked_open_and_mixed_case_is_not(self):
        sys_ = E.system("modern_clean")
        caps = E._text_element({"id": "a", "text": "FREE SHIPPING", "role": "small"}, sys_, self.kit, 40, 1000, 1, "left")
        mixed = E._text_element({"id": "b", "text": "Free shipping", "role": "small"}, sys_, self.kit, 40, 1000, 1, "left")
        self.assertGreater(caps.tracking, 0)
        self.assertEqual(mixed.tracking, 0)

    def test_offer_is_recognised_and_needs_an_offer_layout(self):
        deck = [{"id": "C01", "text": "Room for the long way home.", "role": "Headline"},
                {"id": "C02", "text": "Launch price ₹5,999", "role": "Price"},
                {"id": "C03", "text": "mokobara.com", "role": "Website"}]
        copy = E.roles_from_copy_deck(deck)
        self.assertEqual([c["role"] for c in copy], ["headline", "offer", "small"])
        cands = picker.candidates(kit=self.kit, fmt="4:5", kind="poster", copy=copy, plate=_plate(self.tmp),
                                  product_box_norm=[0.2, 0.2, 0.8, 0.9])
        self.assertEqual({c["template"] for c in cands}, {"offer_stack"})
        best = cands[0]
        self.assertEqual(C.blocking_failures(best["checks"]), [], best["checks"])
        offer = next(e for e in best["layout"]["elements"] if e.role == "offer")
        head = next(e for e in best["layout"]["elements"] if e.role == "headline")
        self.assertGreater(offer.size, head.size)

    def test_product_box_is_detected_on_a_studio_plate(self):
        box = E.detect_product_box(_plate(self.tmp))
        self.assertIsNotNone(box)
        for got, want in zip(box, [200 / 900, 250 / 1125, 700 / 900, 1000 / 1125]):
            self.assertAlmostEqual(got, want, delta=0.02)
        self.assertIsNone(E.detect_product_box(_plate(self.tmp, busy=True)))

    def test_super_gets_a_backing_on_a_busy_shot_and_none_on_a_calm_one(self):
        from product.typeset import supers
        calm = [Image.new("RGB", (1080, 1920), (30, 40, 60))] * 3
        s = supers.make(text="The top stick does all the work.", frames=calm, fmt="9:16", kit=self.kit, system_id="modern_clean")
        self.assertFalse(s.backed)
        self.assertTrue(all(r["status"] == "PASS" for r in s.checks), s.checks)
        busy = [Image.open(_plate(self.tmp, busy=True)).resize((1080, 1920))]
        s = supers.make(text="The top stick does all the work.", frames=busy, fmt="9:16", kit=self.kit, system_id="modern_clean")
        self.assertTrue(s.backed)
        self.assertTrue(all(r["status"] == "PASS" for r in s.checks), s.checks)

    def test_super_reading_time(self):
        from product.typeset import supers
        calm = [Image.new("RGB", (1080, 1920), (30, 40, 60))]
        s = supers.make(text="Pinch. Lift. Eat.", frames=calm, fmt="9:16", kit=self.kit, system_id="modern_clean", duration_s=0.8)
        self.assertEqual({r["check_id"]: r for r in s.checks}["super_reading_time"]["status"], "FAIL")


class PickerAndTaste(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.kit = E.BrandKit(logo=_logo(self.tmp), moods=["premium", "calm"])
        self.saved = picker.TASTE.read_text() if picker.TASTE.exists() else None

    def tearDown(self):
        if self.saved is None:
            picker.TASTE.unlink(missing_ok=True)
        else:
            picker.TASTE.write_text(self.saved)

    def test_a_blocked_layout_never_outranks_a_clean_one(self):
        cands = picker.candidates(kit=self.kit, fmt="4:5", kind="poster", copy=COPY, plate=_plate(self.tmp),
                                  product_box_norm=[0.2, 0.2, 0.8, 0.9])
        seen_blocked = False
        for c in cands:
            blocked = c["layout"] is None or bool(C.blocking_failures(c["checks"]))
            if seen_blocked:
                self.assertTrue(blocked, "a clean layout ranked below a blocked one")
            seen_blocked = seen_blocked or blocked

    def test_taste_choices_move_the_ranking(self):
        from product.typeset import demo
        out = self.tmp / "c"
        demo.run(out=out, fmt="9:16", kind="endcard", copy=COPY, kit=self.kit, plate=None, product_box=None)
        cands = json.loads((out / "candidates.json").read_text())
        a = next(c for c in cands if c["template"] == "endcard_center")
        b = next(c for c in cands if c["template"] == "endcard_line_first")
        res = taste.ingest(out, [{"winner": a["file"], "loser": b["file"]}] * 3)
        self.assertEqual(res["pairs"], 3)
        w = picker.taste_weights()
        self.assertGreater(w["templates"]["endcard_center"], w["templates"]["endcard_line_first"])
        page = taste.page(out)
        self.assertIn("Pick the better ad", page.read_text())

    def test_style_profile_moves_the_ranking_per_brand(self):
        from product.typeset import style
        saved = style.STYLE.read_text() if style.STYLE.exists() else None
        try:
            style.STYLE.write_text("global: {}\nbrands:\n  BrandX: {alignment: {prefer: left-aligned}}\n  BrandY: {alignment: {prefer: centred}}\n")
            kx = E.BrandKit(logo=self.kit.logo, name="BrandX", system="modern_clean")
            ky = E.BrandKit(logo=self.kit.logo, name="BrandY", system="modern_clean")
            best_x = picker.candidates(kit=kx, fmt="4:5", kind="poster", copy=COPY, plate=_plate(self.tmp),
                                       product_box_norm=[0.2, 0.2, 0.8, 0.9])[0]
            best_y = picker.candidates(kit=ky, fmt="4:5", kind="poster", copy=COPY, plate=_plate(self.tmp),
                                       product_box_norm=[0.2, 0.2, 0.8, 0.9])[0]
            self.assertEqual(style.features(best_x["layout"])["alignment"], "left-aligned")
            self.assertEqual(style.features(best_y["layout"])["alignment"], "centred")
        finally:
            if saved is None:
                style.STYLE.unlink(missing_ok=True)
            else:
                style.STYLE.write_text(saved)

    def test_brand_taste_only_moves_that_brand(self):
        from product.typeset import demo
        out = self.tmp / "b"
        demo.run(out=out, fmt="9:16", kind="endcard", copy=COPY, kit=self.kit, plate=None, product_box=None)
        cands = json.loads((out / "candidates.json").read_text())
        a = next(c for c in cands if c["template"] == "endcard_line_first")
        b = next(c for c in cands if c["template"] == "endcard_center")
        taste.ingest(out, [{"winner": a["file"], "loser": b["file"]}] * 4, brand="BrandX")
        w = picker.taste_weights()
        self.assertGreater(w["brands"]["BrandX"]["templates"]["endcard_line_first"], w["templates"]["endcard_line_first"])
        self.assertIn("BrandX", w["brands"])


if __name__ == "__main__":
    unittest.main()
