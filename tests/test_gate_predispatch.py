"""Pre-dispatch gate over the four committed EVAL-038 packages (CANON-GATE-001 plan §A, §F,
Rulings 1–3).

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

The expected-status table is plan §F as amended by Ruling 2 (Sonnet B06 passes with a
non-blocking CA-D5 FAIL on record). Mutations flip exactly the intended row. Where the
observed status differs from the plan it is recorded as an expectedFailure with the reason,
never tuned. Run: python3 -m unittest tests.test_gate_predispatch
"""
import json
import unittest
from pathlib import Path

from canon.gate import doctrine, findings, predispatch

REPO_ROOT = Path(__file__).resolve().parents[1]
E38 = REPO_ROOT / "eval/experiments/EVAL-038"
SONNET_B01 = E38 / "baseline/sonnet-no-canon/E037-sonnet-no-canon-B01-R1.txt"
SONNET_B06 = E38 / "baseline/sonnet-no-canon/E037-sonnet-no-canon-B06-R1.txt"
HAIKU_B01 = E38 / "runs/haiku-packs/packages/E038-haiku-packs-B01-R1.txt"
HAIKU_B06 = E38 / "runs/haiku-packs/packages/E038-haiku-packs-B06-R1.txt"
MEDIA = E38 / "media"
S = findings.Status
ALL_IDS = [f"PA-D{i}-check" for i in range(1, 11)] + [f"CA-D{i}-check" for i in range(1, 12)]
NOT_MECH_PRE = ["PA-D2-check", "PA-D3-check", "PA-D5-check", "PA-D6-check", "PA-D7-check",
                "PA-D9-check", "CA-D3-check", "CA-D4-check", "CA-D8-check", "CA-D9-check",
                "CA-D11-check"]


def dispatch(name):
    return json.loads((MEDIA / f"{name}.request.json").read_text())


class _Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reg = doctrine.load_registry()

    def run_gate(self, path, modality, product, text=None, dispatch_doc=None, prompts=None):
        return predispatch.run_predispatch(
            text if text is not None else path.read_text(), prompts, dispatch_doc, modality,
            product, self.reg, label=path.name)

    def status(self, report, check_id):
        return {r.check_id: r for r in report.results}[check_id].status

    def row(self, report, check_id):
        return {r.check_id: r for r in report.results}[check_id]

    def assertInvariants(self, report):
        ids = [r.check_id for r in report.results if r.family == "doctrine"]
        self.assertEqual(ids, ALL_IDS)
        for r in report.results:
            if r.status is not S.PASS:
                self.assertTrue(r.detail.strip(), r.check_id)
            if r.family == "doctrine":
                self.assertEqual(r.source_text, self.reg.checks[r.check_id].text)
                self.assertIn(r.coverage, ("partial", "none"))
            if r.status in (S.PASS, S.FAIL) and r.family == "doctrine":
                self.assertTrue(r.clause, r.check_id)
        text = report.render_text()
        self.assertNotIn("doctrine satisfied", text)
        for cid in ALL_IDS:
            self.assertIn(cid, text)


class HaikuB06Test(_Base):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.rep = cls.run_gate(cls(), HAIKU_B06, "static_image", True,
                               dispatch_doc=dispatch("E038-media-B06-haiku-packs"))

    def test_table_row(self):
        r = self.rep
        self.assertEqual(r.packs_selected, ["composition_and_attention", "product_appearance"])
        self.assertEqual(self.status(r, "LIMIT-TEXT"), S.PASS)
        self.assertIn("no explicit no-text clause", self.row(r, "LIMIT-TEXT").detail)
        self.assertEqual(self.status(r, "PA-D1-check"), S.PASS)
        self.assertIn("matte", self.row(r, "PA-D1-check").detail)
        self.assertEqual(self.status(r, "PA-D4-check"), S.PASS)
        self.assertIn("upper-left", self.row(r, "PA-D4-check").detail)
        self.assertEqual(self.status(r, "PA-D8-check"), S.PASS)
        self.assertEqual(self.status(r, "PA-D10-check"), S.PASS)
        self.assertIn("2 entries", self.row(r, "PA-D10-check").detail)
        self.assertEqual(self.status(r, "CA-D1-check"), S.PASS)
        self.assertEqual(self.status(r, "CA-D2-check"), S.PASS)
        self.assertEqual(self.status(r, "CA-D5-check"), S.PASS)
        self.assertIn("balanced", self.row(r, "CA-D5-check").detail)
        self.assertEqual(self.status(r, "CA-D6-check"), S.PASS)
        self.assertIn("4:5", self.row(r, "CA-D6-check").detail)
        for cid in ("CA-D7-check", "CA-D8-check", "CA-D9-check", "CA-D10-check", "CA-D11-check"):
            self.assertEqual(self.status(r, cid), S.NOT_APPLICABLE)
            self.assertIn("static_image", self.row(r, cid).detail)
        for cid in NOT_MECH_PRE:
            if cid not in ("CA-D8-check", "CA-D9-check", "CA-D11-check"):
                self.assertEqual(self.status(r, cid), S.NOT_MECHANISED, cid)
        self.assertEqual(self.status(r, "DISPATCH-ASPECT"), S.PASS)
        self.assertNotIn("DISPATCH-SHOT-SUM", [x.check_id for x in r.results])
        self.assertEqual(r.verdict(), "PASS")
        self.assertInvariants(r)
        self.assertTrue(r.render_text().splitlines()[-1].startswith("GATE PASS:"))

    def test_typed_subfields_are_the_scope_and_are_named(self):
        self.assertIn("VISUAL_SYSTEM.surface_finish_per_key_object",
                      self.row(self.rep, "PA-D1-check").detail)
        self.assertIn("VISUAL_SYSTEM.implied_light_source", self.row(self.rep, "PA-D4-check").detail)
        self.assertIn("VISUAL_SYSTEM.placement_zone", self.row(self.rep, "CA-D2-check").detail)
        self.assertIn("VISUAL_SYSTEM.attention_order", self.row(self.rep, "CA-D1-check").detail)


class SonnetB06Test(_Base):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.rep = cls.run_gate(cls(), SONNET_B06, "static_image", True,
                               dispatch_doc=dispatch("E038-media-B06-sonnet-no-canon"))

    def test_table_row_under_ruling_2(self):
        r = self.rep
        self.assertEqual(self.status(r, "LIMIT-TEXT"), S.PASS)
        self.assertEqual(self.status(r, "PA-D1-check"), S.PASS)
        self.assertEqual(self.status(r, "PA-D4-check"), S.PASS)
        self.assertEqual(self.status(r, "PA-D8-check"), S.PASS)
        self.assertIn("controlled reflection", self.row(r, "PA-D8-check").detail)
        self.assertEqual(self.status(r, "PA-D10-check"), S.NOT_RUN)
        self.assertIn("no DOCTRINE_DEVIATIONS section", self.row(r, "PA-D10-check").detail)
        self.assertEqual(self.status(r, "CA-D1-check"), S.PASS)
        self.assertEqual(self.status(r, "CA-D2-check"), S.PASS)
        # the true declaration gap: FAIL, non-blocking (Ruling 2), on record
        ca5 = self.row(r, "CA-D5-check")
        self.assertEqual(ca5.status, S.FAIL)
        self.assertFalse(ca5.blocking)
        self.assertIn("no balance/restless declaration", ca5.detail)
        self.assertEqual(self.status(r, "CA-D6-check"), S.PASS)
        self.assertEqual(self.status(r, "DISPATCH-ASPECT"), S.PASS)
        self.assertEqual(r.verdict(), "PASS")
        text = r.render_text()
        self.assertIn("FAIL (non-blocking) CA-D5-check", text)
        self.assertIn("(1 non-blocking FAIL on record)", text.splitlines()[-1])
        self.assertInvariants(r)


class HaikuB01Test(_Base):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.rep = cls.run_gate(cls(), HAIKU_B01, "video", False,
                               dispatch_doc=dispatch("E038-media-B01-haiku-packs"))

    def test_table_row(self):
        r = self.rep
        self.assertEqual(r.packs_selected, ["composition_and_attention"])
        lt = self.row(r, "LIMIT-TEXT")
        self.assertEqual(lt.status, S.FAIL)
        hit_prompts = {e.split(",")[0] for e in lt.evidence}
        self.assertTrue({"prompt 1", "prompt 2", "prompt 9"} <= hit_prompts, hit_prompts)
        for cid in [f"PA-D{i}-check" for i in range(1, 11)]:
            self.assertEqual(self.status(r, cid), S.NOT_APPLICABLE, cid)
            self.assertIn("product_appearance not selected", self.row(r, cid).detail)
        self.assertEqual(self.status(r, "CA-D1-check"), S.PASS)
        self.assertEqual(self.status(r, "CA-D2-check"), S.PASS)
        self.assertEqual(self.status(r, "CA-D5-check"), S.PASS)
        self.assertIn("restless", self.row(r, "CA-D5-check").detail)
        self.assertEqual(self.status(r, "CA-D6-check"), S.PASS)
        self.assertEqual(self.status(r, "CA-D7-check"), S.PASS)
        self.assertIn("6 shot", self.row(r, "CA-D7-check").detail)
        self.assertEqual(self.status(r, "CA-D10-check"), S.PASS)
        for cid in ("CA-D8-check", "CA-D9-check", "CA-D11-check"):
            self.assertEqual(self.status(r, cid), S.NOT_MECHANISED, cid)
        ss = self.row(r, "DISPATCH-SHOT-SUM")
        self.assertEqual(ss.status, S.FAIL)
        self.assertTrue(ss.blocking)
        self.assertIn("17.5", ss.detail)
        self.assertIn("30", ss.detail)
        self.assertEqual(self.status(r, "DISPATCH-ASPECT"), S.PASS)
        self.assertEqual(r.verdict(), "FAIL")
        self.assertInvariants(r)
        self.assertTrue(r.render_text().splitlines()[-1].startswith("GATE FAIL ("))


class SonnetB01Test(_Base):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.rep = cls.run_gate(cls(), SONNET_B01, "video", False,
                               dispatch_doc=dispatch("E038-media-B01-sonnet-no-canon"))

    def test_table_row(self):
        r = self.rep
        lt = self.row(r, "LIMIT-TEXT")
        self.assertEqual(lt.status, S.FAIL)
        self.assertTrue(lt.detail.startswith("prompt 1, sentence 2"))
        hit_prompts = {e.split(",")[0] for e in lt.evidence}
        self.assertTrue({"prompt 1", "prompt 3"} <= hit_prompts, hit_prompts)
        self.assertNotIn("prompt 4", hit_prompts)   # "to be added in post" defers
        self.assertEqual(self.status(r, "CA-D1-check"), S.PASS)
        self.assertEqual(self.status(r, "CA-D2-check"), S.PASS)
        self.assertEqual(self.status(r, "CA-D6-check"), S.PASS)
        self.assertEqual(self.status(r, "CA-D7-check"), S.PASS)
        self.assertIn("11 shot", self.row(r, "CA-D7-check").detail)
        self.assertEqual(self.status(r, "CA-D10-check"), S.PASS)
        ss = self.row(r, "DISPATCH-SHOT-SUM")
        self.assertEqual(ss.status, S.PASS)
        self.assertIn("26", ss.detail)
        self.assertEqual(r.verdict(), "FAIL")
        self.assertInvariants(r)

    @unittest.expectedFailure
    def test_ca_d5_fails_as_the_plan_states(self):
        # DISCREPANCY recorded for the checker. Plan §F expects CA-D5 FAIL ("no declaration")
        # on Sonnet B01. Its VISUAL_SYSTEM says "brighter neutral daylight balance" and the
        # plan's BALANCE_TERMS carry bare "balance", so the presence clause is met by a
        # white-balance phrase — a false pass the plan did not foresee. Not tuned.
        self.assertEqual(self.status(self.rep, "CA-D5-check"), S.FAIL)

    def test_ca_d5_observed(self):
        row = self.row(self.rep, "CA-D5-check")
        self.assertEqual(row.status, S.PASS)
        self.assertIn("balance", row.detail)


class MutationTest(_Base):
    def test_rule_of_thirds_fails_ca_d2_and_blocks(self):
        text = SONNET_B06.read_text().replace(
            "Aspect ratio: 4:5, vertical.",
            "Aspect ratio: 4:5, vertical. Dial placed on the rule of thirds intersection.")
        r = self.run_gate(SONNET_B06, "static_image", True, text=text)
        row = self.row(r, "CA-D2-check")
        self.assertEqual(row.status, S.FAIL)
        self.assertTrue(row.blocking)
        self.assertIn("rule of thirds", row.detail)
        self.assertEqual(r.verdict(), "FAIL")

    def test_negated_rule_of_thirds_still_passes(self):
        text = SONNET_B06.read_text().replace(
            "Aspect ratio: 4:5, vertical.",
            "Aspect ratio: 4:5, vertical. Placement by zone, not the rule of thirds.")
        r = self.run_gate(SONNET_B06, "static_image", True, text=text)
        self.assertEqual(self.status(r, "CA-D2-check"), S.PASS)

    def test_deleting_finish_words_fails_pa_d1_non_blocking(self):
        text = SONNET_B06.read_text()
        for w in ("brushed", "polished", "Brushed", "Polished", "glossy", "gloss", "matte",
                  "specular", "reflective", "reflection", "sheen", "metallic", "mirror", "satin",
                  "frosted", "lacquer", "glare", "diffuse", "direct"):
            text = text.replace(w, "plain")
        r = self.run_gate(SONNET_B06, "static_image", True, text=text)
        row = self.row(r, "PA-D1-check")
        self.assertEqual(row.status, S.FAIL)
        self.assertFalse(row.blocking)
        self.assertEqual(r.verdict(), "PASS")

    def test_deleting_light_direction_fails_pa_d4(self):
        text = (SONNET_B06.read_text()
                .replace("from upper left", "").replace("~45° top-left", "soft")
                .replace("from the right", "gently").replace("from camera-right", "gently"))
        r = self.run_gate(SONNET_B06, "static_image", True, text=text)
        self.assertEqual(self.status(r, "PA-D4-check"), S.FAIL)

    def test_deviation_entry_without_id_or_clause_fails_pa_d10(self):
        text = HAIKU_B06.read_text().replace(
            "## DOCTRINE_DEVIATIONS\n", "## DOCTRINE_DEVIATIONS\n\nWe softened the key light.\n")
        r = self.run_gate(HAIKU_B06, "static_image", True, text=text)
        row = self.row(r, "PA-D10-check")
        self.assertEqual(row.status, S.FAIL)
        self.assertFalse(row.blocking)
        self.assertIn("softened", row.detail)

    def test_literal_none_deviation_passes(self):
        pkg = ("## VISUAL_SYSTEM\n**surface_finish_per_key_object:**\ncase: brushed\n"
               "**implied_light_source:**\nkey light from upper-left\n"
               "**placement_zone:**\noff-centre left zone because the scene points outward\n"
               "**attention_order:**\n1st read: dial\n2nd read: case\n3rd read: strap\n"
               "## DELIVERABLE\none 4:5 image\n## GENERATION_PROMPTS\n\"" + "A matte plate, no text. " * 8
               + "\"\n## DOCTRINE_DEVIATIONS\nnone\n")
        r = self.run_gate(Path("synthetic.txt"), "static_image", True, text=pkg)
        self.assertEqual(self.status(r, "PA-D10-check"), S.PASS)
        self.assertEqual(self.status(r, "CA-D1-check"), S.PASS)

    def test_empty_typed_subfield_is_a_non_blocking_fail_not_not_run(self):
        text = HAIKU_B06.read_text()
        start = text.index("**placement_zone:**")
        end = text.index("## PRODUCTION_RECIPE")
        text = text[:start] + "**placement_zone:**\n\n" + text[end:]
        r = self.run_gate(HAIKU_B06, "static_image", True, text=text)
        row = self.row(r, "CA-D2-check")
        self.assertEqual(row.status, S.FAIL)
        self.assertFalse(row.blocking)
        self.assertIn("present but empty", row.detail)

    def test_missing_prompts_is_an_error_and_fails_closed(self):
        text = SONNET_B06.read_text().replace("GENERATION_PROMPTS", "GENERATION_NOTES")
        r = self.run_gate(SONNET_B06, "static_image", True, text=text)
        self.assertEqual(self.status(r, "LIMIT-TEXT"), S.ERROR)
        self.assertEqual(r.verdict(), "FAIL")
        self.assertIn("ERROR", r.render_text())

    def test_supplied_prompts_replace_extraction(self):
        r = self.run_gate(SONNET_B01, "video", False, prompts=["A dark, empty room. No text."])
        self.assertEqual(self.status(r, "LIMIT-TEXT"), S.PASS)

    def test_dispatch_aspect_mismatch_blocks(self):
        d = dispatch("E038-media-B06-haiku-packs")
        d["generationConfig"]["imageConfig"]["aspectRatio"] = "1:1"
        r = self.run_gate(HAIKU_B06, "static_image", True, dispatch_doc=d)
        row = self.row(r, "DISPATCH-ASPECT")
        self.assertEqual(row.status, S.FAIL)
        self.assertIn("4:5", row.detail)
        self.assertIn("1:1", row.detail)
        self.assertEqual(r.verdict(), "FAIL")

    def test_no_dispatch_leaves_dispatch_aspect_not_run(self):
        r = self.run_gate(HAIKU_B06, "static_image", True)
        self.assertEqual(self.status(r, "DISPATCH-ASPECT"), S.NOT_RUN)
        self.assertEqual(r.verdict(), "PASS")

    def test_audio_request_selects_no_pack(self):
        r = self.run_gate(SONNET_B06, "audio", True)
        self.assertEqual(r.packs_selected, [])
        for cid in ALL_IDS:
            self.assertEqual(self.status(r, cid), S.NOT_APPLICABLE)
        self.assertEqual(self.status(r, "LIMIT-TEXT"), S.NOT_APPLICABLE)
        self.assertInvariants(r)

    def test_pa_d8_condition_not_detected_is_not_run(self):
        pkg = ("VISUAL_SYSTEM\nkey light from upper-left; brushed case\n"
               "PRODUCTION_RECIPE\nshoot the matte fabric swatch\n"
               "GENERATION_PROMPTS\n\"" + "A matte fabric swatch on plain paper. " * 5 + "\"\n")
        r = self.run_gate(Path("synthetic.txt"), "static_image", True, text=pkg)
        row = self.row(r, "PA-D8-check")
        self.assertEqual(row.status, S.NOT_RUN)
        self.assertIn("condition not detected", row.detail)

    def test_inputs_carry_sha256(self):
        r = self.run_gate(HAIKU_B06, "static_image", True)
        self.assertEqual(list(r.inputs), [HAIKU_B06.name])
        self.assertEqual(len(r.inputs[HAIKU_B06.name]), 64)


if __name__ == "__main__":
    unittest.main()
