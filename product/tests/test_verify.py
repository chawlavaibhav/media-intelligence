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
        cited = {s for c in verify.controls().values() for s in c["sources"] if not s.startswith(("runtime/", "product/", "atlas:"))}
        self.assertEqual(sorted(known - cited), [])
        self.assertEqual(sorted(cited - known), [])
        self.assertGreaterEqual(len(known), 120)

    def test_the_recovered_atlas_is_reconciled_row_for_row_with_its_own_identifiers(self):
        atlas = yaml.safe_load(open(REPO / "production-learning/atlas/2026-09-22/FAILURE-ATLAS-CLASSIFIED.yaml"))["defects"]
        reg = yaml.safe_load(open(verify.CONTROLS_FILE))
        modes = reg["atlas_reconciliation"]["modes"]
        ids = {r["id"] for r in atlas}
        self.assertEqual((len(atlas), len({r["failure_mode"] for r in atlas})), (225, 104))
        self.assertEqual({m["mode"] for m in modes}, {r["failure_mode"] for r in atlas})
        listed = [rid for m in modes for rid in m["rows"]]
        self.assertEqual(sorted(listed), sorted(ids))                       # every row once, no invented row
        by_row = {r["id"]: r for r in atlas}
        for m in modes:
            self.assertTrue(all(by_row[r]["failure_mode"] == m["mode"] and by_row[r]["bucket"] == m["bucket"] for r in m["rows"]), m["mode"])
            self.assertIn(m["p1"], ("enforced", "reviewer_obligation", "by_construction", "excluded_by_scope", "not_applicable_p1",
                                    "human_judgement", "operator_process", "deferred"))
            for c in m["controls"]:
                self.assertIn(c, verify.controls(), m["mode"])
            if m["beta_critical"]:
                # a beta-critical mechanism needs a machine or a named person behind it — never prose, never "later"
                self.assertIn(m["p1"], ("enforced", "reviewer_obligation", "by_construction"), m["mode"])
                self.assertTrue(any(verify.controls()[c]["status"] in ("enforced", "reviewer_obligation", "by_construction")
                                    for c in m["controls"]), m["mode"])
        cited = [s[6:] for c in verify.controls().values() for s in c["sources"] if s.startswith("atlas:")]
        self.assertTrue(cited and set(cited) <= ids)

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
                  "product_fidelity": {"verdict": "faithful", "evidence": "x"}, "continuity": {"verdict": "consistent", "evidence": "x"},
                  "model_lettering": {"present": "no", "evidence": "x"}, "audio": {"speech_or_singing": "no", "notes": ""}}
        rows = verify.review_rows(review, mandatory_ids=["M1"], media_kind="video")
        self.assertTrue(all(r["status"] == "NOT_VERIFIED" for r in rows))

    def test_a_live_review_that_did_not_listen_leaves_audio_unverified(self):
        review = {"verdict": "pass", "modalities_evaluated": ["video_frames"], "_call": {"isolated": True},
                  "mandatory": [], "defects": [], "product_fidelity": {"verdict": "faithful", "evidence": "x"},
                  "continuity": {"verdict": "consistent", "evidence": "x"}, "model_lettering": {"present": "no", "evidence": "x"},
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
        drawn = [c["text"] for c in d["copy_deck"]]
        self.assertEqual(verify.exact_copy_match(["₹185 प्रति लीटर"], d, drawn)["status"], "FAIL")
        d["copy_deck"][0]["text"] = "₹185 प्रति लीटर"
        drawn = [c["text"] for c in d["copy_deck"]]
        self.assertEqual(verify.exact_copy_match(["₹185 प्रति लीटर"], d, drawn)["status"], "PASS")

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


class FilmPictureChecks(unittest.TestCase):
    """Defects found the first time the engine ran on real ffmpeg (2026-09-23): each is caught; the repair passes."""

    @classmethod
    def setUpClass(cls):
        import tempfile
        from product import media
        from product.providers import _wav
        from PIL import Image
        cls.media = media
        cls.d = Path(tempfile.mkdtemp(prefix="mi-film-"))
        cls.clips = []
        for i in range(2):
            p = cls.d / f"c{i}.mp4"; p.write_bytes(media.sim_video(3, "9:16", seed=i + 1)); cls.clips.append(p)
        cls.card = cls.d / "card.png"; Image.new("RGB", (1080, 1920), (31, 42, 68)).save(cls.card)
        cls.bed = cls.d / "bed.wav"; cls.bed.write_bytes(_wav(10.0))
        cls.good_super, _ = compose.super_overlay(out=cls.d / "super.png", size=(1080, 1920), text="Pack less. Go further.",
                                                  clip=cls.clips[1], clip_in=0.0, use=2.5, clip_size=(1080, 1920))
        # the defect as it shipped: a "transparent" super that was really an opaque black canvas
        cls.black_super = cls.d / "super-black.png"
        im = Image.new("RGBA", (1080, 1920), (0, 0, 0, 255)); im.alpha_composite(Image.open(cls.good_super).convert("RGBA")); im.save(cls.black_super)

    def _film(self, super_png, name):
        rep = self.media.assemble_film(segments=[{"clip": c, "in": 0.0, "use": 2.5} for c in self.clips], endcard=self.card,
                                       supers=[{"png": super_png, "t_in": 2.7, "t_out": 4.9}], music=self.bed, out=self.d / name,
                                       size=(1080, 1920), card_s=2.0, workdir=self.d / ("w-" + name))
        rows = verify.film_checks(self.d / name, cuts=rep["cuts_s"], source_sizes=[[720, 1280]], delivered=(1080, 1920),
                                  planned_s=rep["duration_s"], card_in_s=rep["card_in_s"])
        return {r["check_id"]: r for r in rows}

    def test_a_super_on_an_opaque_canvas_blacks_out_the_beat_and_fails(self):
        self.assertEqual(Image_mode(self.good_super), "RGBA")
        bad = self._film(self.black_super, "bad.mp4")
        self.assertEqual(bad["no_black_frames"]["status"], "FAIL", bad["no_black_frames"])
        good = self._film(self.good_super, "good.mp4")
        self.assertEqual(good["no_black_frames"]["status"], "PASS", good["no_black_frames"])
        self.assertEqual(good["delivery_conformance"]["status"], "PASS", good["delivery_conformance"])

    def test_a_film_of_the_wrong_size_or_length_fails_conformance(self):
        rep = self._film(self.good_super, "good2.mp4")
        rows = {r["check_id"]: r for r in verify.film_checks(self.d / "good2.mp4", cuts=[], source_sizes=[[720, 1280]],
                                                              delivered=(1080, 1350), planned_s=30.0)}
        self.assertEqual(rows["delivery_conformance"]["status"], "FAIL")
        self.assertIn("duration", rows["delivery_conformance"]["detail"])


def Image_mode(p):
    from PIL import Image
    return Image.open(p).mode


class DeliveredPixelsAreMeasuredPixels(unittest.TestCase):
    def test_a_half_transparent_plate_is_delivered_opaque_so_contrast_judges_what_ships(self):
        import tempfile
        from PIL import Image
        from product import media
        d = Path(tempfile.mkdtemp(prefix="mi-still-"))
        Image.new("RGBA", (1080, 1080), (110, 67, 161, 140)).save(d / "plate.png")
        deck = {"copy_deck": [{"id": "c1", "text": "Pack less. Go further."}, {"id": "c2", "text": "₹2,499 · acme.in"}],
                "composition": {"text_zone": "top"}}
        out, checks, lay = compose.still_ad(plate=d / "plate.png", out=d / "ad.png", aspect="1:1", direction=deck, logo=None,
                                            workdir=d, product_box_norm=None)
        im = Image.open(out)
        self.assertEqual(im.mode, "RGB")
        self.assertEqual(im.getpixel((540, 700)), (110, 67, 161))
        self.assertEqual(sorted(lay["rendered_text"]), sorted(c["text"] for c in deck["copy_deck"]))

    def test_small_lines_are_body_text_at_phone_size(self):
        self.assertEqual(compose._role(41, 1080), "body")
        self.assertEqual(compose._role(81, 1080), "display")


class GlyphCoverage(unittest.TestCase):
    def test_the_chosen_font_draws_the_rupee_sign_and_uncovered_text_is_refused(self):
        from product import media
        f = media.font("bold", "₹1,299")
        self.assertEqual(media.missing_glyphs("₹1,299", f), [])
        with self.assertRaises(media.MediaError):
            media.font("regular", "\U0001F600\u4e2d")


class EvidenceBackedPass(unittest.TestCase):
    def test_exact_copy_is_judged_on_what_was_drawn_on_the_file(self):
        d = {"copy_deck": [{"id": "c1", "text": "Pack less. Go further."}, {"id": "c2", "text": "₹2,499"}]}
        self.assertEqual(verify.exact_copy_match(["₹2,499"], d, ["Pack less. Go further."])["status"], "FAIL")
        self.assertEqual(verify.exact_copy_match(["₹2,499"], d, None)["status"], "NOT_VERIFIED")
        self.assertEqual(verify.exact_copy_match(["₹2,499"], d, ["₹2,499"])["status"], "FAIL")   # approved line c1 dropped
        self.assertEqual(verify.exact_copy_match(["₹2,499"], d, ["₹2,499", "Pack less. Go further."])["status"], "PASS")

    def test_a_reviewer_that_says_nothing_about_a_property_does_not_pass_it(self):
        review = {"verdict": "pass", "modalities_evaluated": ["video_frames", "audio"], "_call": {"isolated": True},
                  "mandatory": [], "defects": [], "audio": {"speech_or_singing": "no", "notes": ""}}
        rows = {r["check_id"]: r["status"] for r in verify.review_rows(review, mandatory_ids=["M1"], media_kind="video")}
        for cid in ("product_fidelity", "no_model_lettering", "character_continuity", "mandatory:M1"):
            self.assertEqual(rows[cid], "NOT_VERIFIED", cid)
        self.assertEqual(rows["audio_reviewed"], "PASS")

    def test_a_review_of_another_file_proves_nothing_about_this_one(self):
        review = {"verdict": "pass", "modalities_evaluated": ["image"], "_call": {"isolated": True}, "_reviewed_sha256": ["aaa"],
                  "mandatory": [], "defects": [], "product_fidelity": {"verdict": "faithful", "evidence": "x"},
                  "model_lettering": {"present": "no", "evidence": "x"}}
        rows = verify.review_rows(review, mandatory_ids=[], media_kind="image", asset_sha256="bbb")
        self.assertTrue(all(r["status"] == "NOT_VERIFIED" for r in rows), rows)


import os
_MOKO_REL = "media-intelligence-mokobara/agency/jobs/AGY-2026-09-21-MOKOBARA-ODYSSEY-001/gen/final"
MOKOBARA = next((p for p in [Path(os.environ.get("MI_HISTORICAL_MOKOBARA", "/nonexistent"))] + [b / _MOKO_REL for b in (REPO.parent, REPO.parent.parent)]
                 if (p / "v1/mokobara-odyssey-9x16-30s.mp4").exists()), Path("/nonexistent"))


@unittest.skipUnless((MOKOBARA / "v1/mokobara-odyssey-9x16-30s.mp4").exists(), "historical Mokobara films not on this host")
class HistoricalRealMedia(unittest.TestCase):
    """The delivered-film checks on real historical media: the defective v1 fails where the record says, the repaired v2 passes."""

    def test_mokobara_df10_audio_holes_fail_v1_and_the_crossfaded_v2_passes(self):
        v1 = verify.film_checks(MOKOBARA / "v1/mokobara-odyssey-9x16-30s.mp4", cuts=[1.54, 3.5, 7.5, 12.5, 20.5, 24.5],
                                source_sizes=[[720, 1280]], delivered=(1080, 1920), planned_s=30.0, card_in_s=26.0)
        v2 = verify.film_checks(MOKOBARA / "mokobara-odyssey-9x16-30s.mp4", cuts=[1.5, 3.5, 7.5, 13.0, 21.0, 24.21],
                                source_sizes=[[720, 1280]], delivered=(1080, 1920), planned_s=30.0, card_in_s=26.0)
        j1 = next(r for r in v1 if r["check_id"] == "audio_joins")
        j2 = next(r for r in v2 if r["check_id"] == "audio_joins")
        self.assertEqual(j1["status"], "FAIL")
        self.assertIn("3.50s", j1["detail"]); self.assertIn("7.50s", j1["detail"])
        self.assertEqual(j2["status"], "PASS", j2["detail"])
        for rows in (v1, v2):
            st = {r["check_id"]: r["status"] for r in rows}
            self.assertEqual((st["delivery_conformance"], st["no_black_frames"], st["loudness_true_peak"], st["container_edit_lists"]),
                             ("PASS", "PASS", "PASS", "PASS"))


class PersonChecksCannotBeWaived(unittest.TestCase):
    def test_a_waiver_does_not_discharge_the_listen_but_a_recorded_listen_does(self):
        e = Env()
        try:
            jid = e.submit()
            p = e.dir / "f.mp4"; p.write_bytes(b"film")
            aid = e.store.add_asset(jid, path=p, kind="video", source="composed", content_type="video/mp4")
            req = {"audio_heard_by_person": "AUDIO_REVIEWED_BY_EAR"}
            e.store.waive(jid, aid, "audio_heard_by_person", "operator:x", "no time to listen, customer is waiting")
            self.assertFalse(verify.gateway(e.store, jid, aid, req)["ready"])
            with self.assertRaises(ValueError):
                verify.attest(e.store, jid, aid, "audio_heard_by_person", by="operator:x", note="ok")
            verify.attest(e.store, jid, aid, "audio_heard_by_person", by="operator:x",
                          note="full listen on headphones: surf, wind and the music bed only")
            g = verify.gateway(e.store, jid, aid, req)
            self.assertTrue(g["ready"])
            self.assertEqual(g["table"][0]["runner"], "person:operator:x")
        finally:
            e.close()


_MDR8 = next((b / "media-intelligence-mokobara-v3/agency/jobs/AGY-2026-09-22-MOKOBARA-DEEPREAD-001/gen/final/mokobara-deepread-9x16-30s.mp4"
              for b in (REPO.parent, REPO.parent.parent)
              if (b / "media-intelligence-mokobara-v3/agency/jobs/AGY-2026-09-22-MOKOBARA-DEEPREAD-001/gen/final/mokobara-deepread-9x16-30s.mp4").exists()),
             None)


@unittest.skipUnless(_MDR8, "the rejected MDR8 film is not on this host")
class HistoricalRejectedFilm(unittest.TestCase):
    def test_the_rejected_mdr8_film_fails_true_peak_which_the_atlas_never_recorded(self):
        # codec_true_peak_overshoot, 5th occurrence (atlas rows: 4, none on MDR8). Found 2026-09-23 by running the P1 checks.
        rows = {r["check_id"]: r for r in verify.film_checks(_MDR8, cuts=[3.58, 8.08, 12.58, 19.08, 23.58], source_sizes=[[720, 1280]],
                                                              delivered=(1080, 1920), planned_s=30.0, card_in_s=26.2)}
        self.assertEqual(rows["loudness_true_peak"]["status"], "FAIL", rows["loudness_true_peak"]["detail"])
        self.assertEqual(rows["no_black_frames"]["status"], "PASS")
