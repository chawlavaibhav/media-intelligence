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

from canon.gate import doctrine, findings, package, predispatch, textscan

REPO_ROOT = Path(__file__).resolve().parents[1]
E38 = REPO_ROOT / "eval/experiments/EVAL-038"
SONNET_B01 = E38 / "baseline/sonnet-no-canon/E037-sonnet-no-canon-B01-R1.txt"
SONNET_B06 = E38 / "baseline/sonnet-no-canon/E037-sonnet-no-canon-B06-R1.txt"
HAIKU_B01 = E38 / "runs/haiku-packs/packages/E038-haiku-packs-B01-R1.txt"
HAIKU_B06 = E38 / "runs/haiku-packs/packages/E038-haiku-packs-B06-R1.txt"
MEDIA = E38 / "media"
GEMMA_B02 = E38 / "runs/gemma-packs/packages/E038-gemma-packs-B02-R1.txt"
# L-01 fixtures (Ruling 7): a clean 144-char prompt, a text-bearing prompt ending in a digit,
# and the six tail shapes the third checker listed after a digit-ending closer.
CLEAN = ("A matte plate, no text. " * 6).strip()
DIRTY = ("Vertical 9:16, a smartphone screen filling with WhatsApp rent-reminder chat bubbles "
         "and a notification counter climbing past 99")
TAILS = (" (8 s)", " — 4 s", " | 4 s |", ". Then the next shot.", " 8 s", " then the next shot")
# M-01 / M-02 fixtures (Ruling 8): a nested straight-quoted string with a text-bearing tail,
# and the symbol-initial price strings; the clean 143-char lead would PASS on its own.
NESTED = ('A model showing the "Aster Meridian" on her wrist, chat bubbles and a notification '
          'counter on screen')
PRICES = 'she holds "₹9" and "₹99" in gold, chat bubbles and a notification counter on screen'
PRICES3 = ('she holds "₹9" and "₹99" and "₹999" in gold, chat bubbles and a notification '
           'counter on screen')
DOUBT_THEN_SPACE_LED = f'{CLEAN} 6" then " chat bubbles and a notification counter past 99'
# N-01 / N-05 fixtures (Ruling 9): the fifth checker's seven class-3 shapes — a nested
# straight-quoted string whose opener is followed by whitespace — and K16, a stand-alone
# second prompt under the floor. At HEAD e47cf13 each PASSed with its tail unscanned.
TAIL = "in gold, chat bubbles and a notification counter on screen"
N01_SHAPES = (
    ("K11", f'"{CLEAN} she holds " Aster " {TAIL}"\n'),
    ("K11b", f'"{CLEAN} she holds " Aster." {TAIL}"\n'),
    ("K11e", f'"{CLEAN} she holds " Aster " {TAIL}."\n"{CLEAN}"\n'),
    ("K11f", f'" {CLEAN} she holds " Aster " {TAIL} "\n'),
    ("K12", f'"{CLEAN} she reads "\nAster Meridian\n" on her wrist, chat bubbles and a '
            f'notification counter on screen"\n'),
    ("K12b", f'"{CLEAN} she holds "\u00a0Aster\u00a0" {TAIL}"\n'),
    ("K17", f'"{CLEAN} she holds "\tAster\t" {TAIL}"\n'),
)
K16_SHORT_SECOND_PROMPT = f'"{CLEAN}"\n"chat bubbles and a notification counter on screen"\n'
S = findings.Status
ALL_IDS = [f"PA-D{i}-check" for i in range(1, 11)] + [f"CA-D{i}-check" for i in range(1, 12)]
NOT_MECH_PRE = ["PA-D2-check", "PA-D3-check", "PA-D5-check", "PA-D6-check", "PA-D7-check",
                "PA-D9-check", "CA-D3-check", "CA-D4-check", "CA-D8-check", "CA-D9-check",
                "CA-D11-check"]
# K-04: the pre-F-05 PA-D4 vocabularies, verbatim from `git show 3baa673:canon/gate/vocab.py`,
# so the narrowing is pinned against the terms that produced the false PASS.
OLD_LIGHT_TERMS_3BAA673 = (
    r"key\s+light", "key", r"light\s+source", "softbox", r"soft\s+box", r"window\s+light",
    "daylight", "sunlight", "tube-light", "tubelight", "lamp", "practical", "backlight",
    r"rim\s+light", "kicker", "fill", "spotlight", r"overhead\s+light", r"lit\s+from",
    r"light\s+from",
)
OLD_DIRECTION_TERMS_3BAA673 = (
    "upper-left", r"upper\s+left", "top-left", r"top\s+left", "upper-right", r"upper\s+right",
    "top-right", r"from\s+the\s+left", r"from\s+the\s+right", r"from\s+above", r"from\s+behind",
    r"from\s+the\s+side", "camera-left", "camera-right", "overhead", "behind", "side", "front",
    r"\d+\s*°", r"\d+\s*degrees", "window",
)


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
            if r.family == "doctrine" and r.clause:
                # condition 5: every clause fragment is a verbatim substring of the pack line
                for fragment in r.clause.split(" … "):
                    self.assertIn(fragment, r.source_text, f"{r.check_id}: {fragment!r}")
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
        self.assertIn('[partial: "Placement is stated as a zone" … "no placement is justified '
                      'by a named ratio or grid line"]', r.render_text())
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
        self.assertIn("; 1 non-blocking FAIL on record)", text.splitlines()[-1])
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

    def test_ca_d5_fails_as_the_plan_states(self):
        # Plan §F: CA-D5 FAIL ("no declaration") on Sonnet B01. Its VISUAL_SYSTEM says
        # "brighter neutral daylight balance" — a white-balance phrase; bare "balance" was
        # narrowed out of BALANCE_TERMS (F-05, condition 2) and the plan's value is restored.
        row = self.row(self.rep, "CA-D5-check")
        self.assertEqual(row.status, S.FAIL)
        self.assertFalse(row.blocking)
        self.assertIn("no balance/restless declaration", row.detail)
        self.assertIn("1 non-blocking FAIL on record", self.rep.render_text().splitlines()[-1])


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

    def ca_d2_with(self, sentence):
        text = SONNET_B06.read_text().replace(
            "Aspect ratio: 4:5, vertical.", f"Aspect ratio: 4:5, vertical. {sentence}")
        return self.row(self.run_gate(SONNET_B06, "static_image", True, text=text), "CA-D2-check")

    def test_f07_negated_named_ratio_outside_a_four_token_window_still_passes(self):
        # checker F-07: the negator sits more than 4 tokens before the term (within the
        # 6-token CA-D2 window of Ruling 6 condition 1), or after it as a disclaimer
        for sentence in ("We will not compose this using the rule of thirds.",
                         "Avoid any reliance on the classic rule of thirds.",
                         "The rule of thirds is not used here.",
                         "Not the rule of thirds.",
                         "The golden ratio is deliberately avoided here."):
            row = self.ca_d2_with(sentence)
            self.assertEqual(row.status, S.PASS, sentence)

    def test_k01_an_unrelated_negator_earlier_in_the_sentence_does_not_clear_a_named_ratio(self):
        # checker K-01: sentence-wide negation is withdrawn (Ruling 6 condition 1). A negator
        # seven or more tokens before the term governs something else; the placement is
        # still justified by the named ratio and the row FAILs, blocking.
        for sentence in ("Without clutter, the watch sits on the golden ratio point.",
                         "No hard shadows, dial placed on the rule of thirds line.",
                         "Not too tight, the crown sits at the intersection of the thirds."):
            row = self.ca_d2_with(sentence)
            self.assertEqual(row.status, S.FAIL, sentence)
            self.assertTrue(row.blocking, sentence)
            self.assertEqual(self.run_gate(SONNET_B06, "static_image", True,
                                           text=SONNET_B06.read_text().replace(
                                               "Aspect ratio: 4:5, vertical.",
                                               f"Aspect ratio: 4:5, vertical. {sentence}")).verdict(),
                             "FAIL", sentence)

    def test_f07_named_ratio_with_an_unrelated_negator_still_fails(self):
        # the negator does not govern the term: still a justification by a named ratio
        for sentence in ("Placement follows the golden ratio.",
                         "Dial on the rule of thirds line, not centred.",
                         "Rule of thirds, no exceptions."):
            row = self.ca_d2_with(sentence)
            self.assertEqual(row.status, S.FAIL, sentence)
            self.assertTrue(row.blocking, sentence)

    def test_f04_a_clock_time_in_the_deliverable_is_not_an_aspect(self):
        # checker F-04: watch briefs conventionally state 10:10; a timestamp is not an aspect
        for lead in ("Hands set to 10:10 as convention. ", "The logo holds for the last 0:03. "):
            text = SONNET_B06.read_text().replace(
                "One premium, commercially usable", lead + "One premium, commercially usable")
            r = self.run_gate(SONNET_B06, "static_image", True, text=text,
                              dispatch_doc=dispatch("E038-media-B06-sonnet-no-canon"))
            self.assertIn("aspect stated: 4:5", self.row(r, "CA-D6-check").detail, lead)
            self.assertEqual(self.status(r, "DISPATCH-ASPECT"), S.PASS, lead)
            self.assertEqual(r.verdict(), "PASS", lead)

    def test_f12_an_inch_mark_before_the_prompts_does_not_shift_extraction(self):
        # checker F-12: one unbalanced straight quote in product copy above the prompts
        text = SONNET_B01.read_text().replace(
            "**Shot 1–5 (Chaos block)", 'Note: the 5" screen is the hero.\n\n**Shot 1–5 (Chaos block)')
        self.assertNotEqual(text, SONNET_B01.read_text())
        r = self.run_gate(SONNET_B01, "video", False, text=text)
        lt = self.row(r, "LIMIT-TEXT")
        self.assertEqual(lt.status, S.FAIL)
        self.assertTrue(lt.detail.startswith("prompt 1, sentence 2"))
        hit_prompts = {e.split(",")[0] for e in lt.evidence}
        self.assertTrue({"prompt 1", "prompt 3"} <= hit_prompts, hit_prompts)

    def test_f11_a_prose_lead_in_before_the_deviation_entries_is_not_an_entry(self):
        text = HAIKU_B06.read_text().replace(
            "## DOCTRINE_DEVIATIONS\n",
            "## DOCTRINE_DEVIATIONS\n\nThe following deviations were forced by the brief:\n")
        r = self.run_gate(HAIKU_B06, "static_image", True, text=text)
        row = self.row(r, "PA-D10-check")
        self.assertEqual(row.status, S.PASS, row.detail)
        self.assertIn("2 entries", row.detail)

    def test_f11_prose_after_an_entry_is_its_continuation(self):
        pkg = ("## VISUAL_SYSTEM\nkey light from upper-left; brushed case; centre zone; balanced\n"
               "## DELIVERABLE\none 4:5 image\n## GENERATION_PROMPTS\n\""
               + "A matte plate, no text. " * 8 + "\"\n## DOCTRINE_DEVIATIONS\n"
               "Deviations forced by the brief:\n\n"
               "- PA-D4 (single source)\n"
               "  Overridden because the brief fixes a two-window room.\n")
        r = self.run_gate(Path("synthetic.txt"), "static_image", True, text=pkg)
        row = self.row(r, "PA-D10-check")
        self.assertEqual(row.status, S.PASS, row.detail)
        self.assertIn("1 entries", row.detail)

    # ── F-05: bare terms narrowed (condition 2) ──────────────────────────
    def synthetic(self, visual_system, deviations="none"):
        pkg = ("## VISUAL_SYSTEM\n" + visual_system + "\n## DELIVERABLE\none 4:5 image\n"
               "## GENERATION_PROMPTS\n\"" + "A matte plate, no text. " * 8 + "\"\n"
               "## DOCTRINE_DEVIATIONS\n" + deviations + "\n")
        return self.run_gate(Path("synthetic.txt"), "static_image", True, text=pkg)

    def test_k02_the_synthetic_prompt_is_extracted_not_limit_text_error(self):
        # checker K-02: the fixture prompt above ends "no text. " + '"' — whitespace before
        # the closing quote — and must be one extracted prompt, never LIMIT-TEXT ERROR
        r = self.synthetic("key light from upper-left; brushed case; centre zone; balanced")
        row = self.row(r, "LIMIT-TEXT")
        self.assertNotEqual(row.status, S.ERROR, row.detail)
        self.assertEqual(row.status, S.PASS, row.detail)
        self.assertIn("1 prompt(s)", row.detail)
        r = self.synthetic("key light from upper-left; brushed case; centre zone; balanced",
                           deviations="- PA-D4 because the brief fixes a two-window room")
        self.assertNotEqual(self.status(r, "LIMIT-TEXT"), S.ERROR)

    def test_k05_an_inch_mark_inside_a_prompt_still_reaches_limit_text(self):
        # checker K-05 / Ruling 6 condition 5: the remainder after the inch mark is scanned
        lead = "Vertical 9:16, a young man at a desk in a cramped PG office, harsh tube-light. "
        for tail in ('A 6" OLED panel showing chat bubbles and a notification counter.',
                     'The panel is 6". It shows chat bubbles and a notification counter.'):
            pkg = ("## VISUAL_SYSTEM\nkey light from upper-left; centre zone\n"
                   "## DELIVERABLE\none 9:16 video\n## GENERATION_PROMPTS\n\"" + lead + tail + "\"\n")
            r = self.run_gate(Path("synthetic.txt"), "video", False, text=pkg)
            row = self.row(r, "LIMIT-TEXT")
            self.assertEqual(row.status, S.FAIL, tail)
            self.assertIn("chat bubbles", row.detail, tail)
            self.assertEqual(r.verdict(), "FAIL", tail)

    def test_f05_checkers_junk_visual_system(self):
        # checker F-05: the junk VISUAL_SYSTEM that satisfied seven presence partials. After
        # narrowing, bare "balance" no longer declares balance (CA-D5 FAIL). The rows that
        # still PASS do so on the plan's necessary-condition clauses, lexically met: a
        # LIGHT term with a DIRECTION term ("key light from the side"), a FINISH term
        # ("brushed"), a PLACEMENT term ("center") and an ordered 1/2/3 list. The plan says
        # these are presence checks. PA-D8's committed feeds_sections do not include
        # VISUAL_SYSTEM, so "glass, highlight" there is out of scope: NOT_RUN, not PASS.
        r = self.synthetic("balance, key light from the side, center, brushed.\n"
                           "1. a\n2. b\n3. c\nglass, highlight.")
        ca5 = self.row(r, "CA-D5-check")
        self.assertEqual(ca5.status, S.FAIL)
        self.assertIn("no balance/restless declaration", ca5.detail)
        for cid in ("PA-D1-check", "PA-D4-check", "CA-D1-check", "CA-D2-check"):
            self.assertEqual(self.status(r, cid), S.PASS, cid)
        self.assertEqual(self.status(r, "PA-D8-check"), S.NOT_RUN)
        self.assertNotIn("VISUAL_SYSTEM", self.reg.checks["PA-D8-check"].feeds_sections)

    def test_f05_soft_window_light_is_not_a_direction(self):
        r = self.synthetic("**implied_light_source:**\nSoft window light.\n")
        row = self.row(r, "PA-D4-check")
        self.assertEqual(row.status, S.FAIL, row.detail)
        r = self.synthetic("**implied_light_source:**\nSoft window light from the left.\n")
        self.assertEqual(self.status(r, "PA-D4-check"), S.PASS)
        r = self.synthetic("**implied_light_source:**\nNatural daylight from the office window.\n")
        self.assertEqual(self.status(r, "PA-D4-check"), S.PASS)

    def test_f05_bare_key_and_front_are_not_a_light_and_a_direction(self):
        r = self.synthetic("**implied_light_source:**\n"
                           "the key is the product itself, shown from the front\n")
        self.assertEqual(self.status(r, "PA-D4-check"), S.FAIL)
        r = self.synthetic("**implied_light_source:**\nsoft key from the front\n")
        self.assertEqual(self.status(r, "PA-D4-check"), S.PASS)
        r = self.synthetic("**implied_light_source:**\nkey light, fill from the left\n")
        self.assertEqual(self.status(r, "PA-D4-check"), S.PASS)

    # ── K-04: every narrowed bare term pinned in the failing direction ─────
    # Each fixture is one sentence with no splitter boundary (`. `, `; `, newline) between
    # the light term and the direction term. OLD_* are the F-05-era tuples transcribed
    # verbatim from `git show 3baa673:canon/gate/vocab.py`; the test asserts PA-D4 would
    # PASS on them (the false PASS the checker reported) and FAILs on the narrowed vocabulary.
    K04_FIXTURES = (
        ("fill", "the fill of the frame is the watch itself, shown from upper left"),
        ("side", "key light kept soft, crown on the right side of the case"),
        ("behind", "key light kept soft, the strap tucked behind the case"),
        ("°", "key light kept soft, dial tilted 5° toward camera"),
        ("key/front", "the key is the product itself, shown from the front"),
        ("window", "Soft window light"),
    )
    K04_NARROWED_PASS = (
        ("fill", "gentle fill from the left"),
        ("side", "key light kept soft, side-lit from camera-left"),
        ("behind", "key light from behind the watch"),
        ("°", "key light at 45° above horizontal"),
        ("°", "key light 45 degrees camera-left"),
        ("key/front", "soft key from the front"),
        ("window", "Soft window light from the left"),
    )

    def _old_pa_d4(self, sentence):
        lights = predispatch._found(textscan.compile_terms(OLD_LIGHT_TERMS_3BAA673), sentence)
        directions = predispatch._found(textscan.compile_terms(OLD_DIRECTION_TERMS_3BAA673),
                                        sentence)
        return S.PASS if lights and directions else S.FAIL

    def test_k04_each_narrowed_bare_term_fails_where_the_old_term_passed(self):
        for term, sentence in self.K04_FIXTURES:
            self.assertEqual(len(package.split_sentences(sentence)), 1, sentence)
            self.assertEqual(self._old_pa_d4(sentence), S.PASS, f"{term}: {sentence}")
            r = self.synthetic("**implied_light_source:**\n" + sentence + "\n")
            row = self.row(r, "PA-D4-check")
            self.assertEqual(row.status, S.FAIL, f"{term}: {sentence} — {row.detail}")

    def test_k04_the_narrowed_forms_still_declare_a_source_with_a_direction(self):
        for term, sentence in self.K04_NARROWED_PASS:
            r = self.synthetic("**implied_light_source:**\n" + sentence + "\n")
            self.assertEqual(self.status(r, "PA-D4-check"), S.PASS, f"{term}: {sentence}")

    def test_f05_white_balance_is_not_a_balance_declaration(self):
        r = self.synthetic("brighter neutral daylight balance; brushed case; centre zone.")
        self.assertEqual(self.status(r, "CA-D5-check"), S.FAIL)
        for phrase in ("the frame is balanced", "compositional balance holds",
                       "deliberately unbalanced and restless", "an off-balance frame"):
            r = self.synthetic(phrase + "; brushed case; centre zone.")
            self.assertEqual(self.status(r, "CA-D5-check"), S.PASS, phrase)

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



class L01UnbalancedQuotesTest(_Base):
    """Ruling 7 (L-01): a quote run the gate cannot pair is an extraction ERROR on LIMIT-TEXT
    (reason "unbalanced quotes", verdict FAIL) — never a dropped or manufactured prompt."""

    @staticmethod
    def synthetic(section):
        return ("## VISUAL_SYSTEM\nkey light from upper-left; centre zone\n## DELIVERABLE\n"
                "one 9:16 video\n## GENERATION_PROMPTS\n" + section
                + "## DOCTRINE_DEVIATIONS\nnone\n")

    def test_gemma_b02_r1_read_in_place_does_not_exit_pass(self):
        # condition 3(a): the committed poster package requesting rendered prices
        for product in (False, True):
            r = self.run_gate(GEMMA_B02, "static_image", product)
            lt = self.row(r, "LIMIT-TEXT")
            self.assertIn(lt.status, (S.ERROR, S.FAIL), lt.detail)
            self.assertEqual(lt.status, S.ERROR, lt.detail)
            self.assertIn("unbalanced quotes", lt.detail)
            self.assertTrue(lt.blocking)
            self.assertEqual(r.verdict(), "FAIL", product)
            self.assertTrue(r.render_text().splitlines()[-1].startswith("GATE FAIL"))
            self.assertInvariants(r)

    def test_six_tails_after_a_digit_ending_closer_never_pass(self):
        # condition 3(b): PASS is the only forbidden outcome; this build leaves the run in
        # doubt and errors, so the observed status is ERROR with the reason named
        for tail in TAILS:
            for follow in ("", f'"{CLEAN}"\n'):
                section = f'"{CLEAN}"\n"{DIRTY}"{tail}\n{follow}'
                r = self.run_gate(Path("synthetic.txt"), "video", False,
                                  text=self.synthetic(section))
                lt = self.row(r, "LIMIT-TEXT")
                self.assertIn(lt.status, (S.ERROR, S.FAIL), (tail, follow, lt.detail))
                if lt.status is S.ERROR:
                    self.assertIn("unbalanced quotes", lt.detail)
                else:
                    self.assertIn("prompt 2", lt.detail)
                self.assertEqual(r.verdict(), "FAIL", (tail, follow))

    def test_a_digit_ending_closer_at_end_of_line_still_closes_and_is_scanned(self):
        # condition 3(c)
        r = self.run_gate(Path("synthetic.txt"), "video", False,
                          text=self.synthetic(f'"{CLEAN}"\n"{DIRTY}"\n'))
        lt = self.row(r, "LIMIT-TEXT")
        self.assertEqual(lt.status, S.FAIL, lt.detail)
        self.assertTrue(lt.detail.startswith("prompt 2, sentence"), lt.detail)
        self.assertEqual(r.verdict(), "FAIL")

    def test_an_unclosed_run_is_an_error_and_a_supplied_prompt_bypasses_extraction(self):
        # condition 1, plain shape: a prompt whose closing quote is missing
        text = self.synthetic(f'"{CLEAN}"\n"{CLEAN}\n')
        r = self.run_gate(Path("synthetic.txt"), "video", False, text=text)
        lt = self.row(r, "LIMIT-TEXT")
        self.assertEqual(lt.status, S.ERROR, lt.detail)
        self.assertIn("unbalanced quotes", lt.detail)
        self.assertEqual(r.verdict(), "FAIL")
        # --prompt-file supplies the prompts; extraction is not consulted
        r = self.run_gate(Path("synthetic.txt"), "video", False, text=text, prompts=[CLEAN])
        self.assertEqual(self.status(r, "LIMIT-TEXT"), S.PASS)

    def test_check_limit_text_names_the_extraction_error(self):
        row = predispatch.check_limit_text([], self.reg, extraction_error="unbalanced quotes in "
                                           "GENERATION_PROMPTS: run opened at offset 3 never closes")
        self.assertEqual(row.status, S.ERROR)
        self.assertTrue(row.blocking)
        self.assertIn("unbalanced quotes", row.detail)
        self.assertIn("offset 3", row.detail)
        # without an extraction error the empty-prompt row reads as before
        row = predispatch.check_limit_text([], self.reg)
        self.assertEqual(row.status, S.ERROR)
        self.assertIn("no generation prompt could be extracted", row.detail)


class M01NestedQuotesTest(_Base):
    """Ruling 8 (M-01, M-02): a straight-quoted string nested inside a prompt is either kept
    inside a whole prompt (LIMIT-TEXT FAIL on the tail) or is an extraction ERROR — PASS over
    the unscanned tail is the one forbidden outcome."""

    @staticmethod
    def synthetic(section):
        return ("## VISUAL_SYSTEM\nkey light from upper-left; centre zone\n## DELIVERABLE\n"
                "one 9:16 video\n## GENERATION_PROMPTS\n" + section
                + "## DOCTRINE_DEVIATIONS\nnone\n")

    def limit_text(self, section):
        r = self.run_gate(Path("synthetic.txt"), "video", False, text=self.synthetic(section))
        lt = self.row(r, "LIMIT-TEXT")
        self.assertIn(lt.status, (S.ERROR, S.FAIL), (section, lt.detail))
        self.assertTrue(lt.blocking)
        self.assertEqual(r.verdict(), "FAIL", section)
        self.assertInvariants(r)
        return lt

    def test_m01_a1_a2_a3_extract_whole_and_fail_on_the_tail(self):
        for name, section in (("A1", f'"{CLEAN} {NESTED}"\n'),
                              ("A2", f'"{CLEAN} {NESTED}."\n"{CLEAN}"\n'),
                              ("A3", f'"{CLEAN} {NESTED}."\n')):
            lt = self.limit_text(section)
            self.assertEqual(lt.status, S.FAIL, (name, lt.detail))
            self.assertTrue(lt.detail.startswith("prompt 1, sentence"), (name, lt.detail))

    def test_m01_symbol_initial_string_is_an_error(self):
        lt = self.limit_text(f'"{CLEAN} {PRICES}"\n')
        self.assertEqual(lt.status, S.ERROR, lt.detail)
        self.assertIn("unbalanced quotes", lt.detail)

    def test_m02_symbol_initial_string_after_a_doubt_point_is_an_error(self):
        for section in (f'"{CLEAN} {PRICES3}"\n', f'"{DOUBT_THEN_SPACE_LED}"\n',
                        f'"{CLEAN} 6" then "₹9" and chat bubbles past 99"\n'):
            lt = self.limit_text(section)
            self.assertEqual(lt.status, S.ERROR, (section, lt.detail))
            self.assertIn("unbalanced quotes", lt.detail)


class N01SubFloorRunTest(_Base):
    """Ruling 9 (N-01, N-05): a quoted run under the prompt floor inside GENERATION_PROMPTS is
    a LIMIT-TEXT ERROR naming the reason ("quoted run below the prompt floor — not scanned"),
    verdict FAIL — never a silent drop that lets the clean head PASS."""

    @staticmethod
    def synthetic(section):
        return ("## VISUAL_SYSTEM\nkey light from upper-left; centre zone\n## DELIVERABLE\n"
                "one 9:16 video\n## GENERATION_PROMPTS\n" + section
                + "## DOCTRINE_DEVIATIONS\nnone\n")

    def assertFloorError(self, section, name):
        r = self.run_gate(Path("synthetic.txt"), "video", False, text=self.synthetic(section))
        lt = self.row(r, "LIMIT-TEXT")
        self.assertNotEqual(lt.status, S.PASS, (name, lt.detail))
        self.assertEqual(lt.status, S.ERROR, (name, lt.detail))
        self.assertIn("quoted run below the prompt floor — not scanned", lt.detail, name)
        self.assertIn("fails closed", lt.detail, name)
        self.assertTrue(lt.blocking)
        self.assertEqual(r.verdict(), "FAIL", name)
        self.assertTrue(r.render_text().splitlines()[-1].startswith("GATE FAIL"))
        self.assertInvariants(r)

    def test_n01_the_seven_class_3_shapes_are_errors(self):
        for name, section in N01_SHAPES:
            with self.subTest(name):
                self.assertFloorError(section, name)

    def test_n05_k16_a_short_second_prompt_is_an_error(self):
        self.assertFloorError(K16_SHORT_SECOND_PROMPT, "K16")

    def test_n01_a_supplied_prompt_file_still_bypasses_extraction(self):
        r = self.run_gate(Path("synthetic.txt"), "video", False,
                          text=self.synthetic(K16_SHORT_SECOND_PROMPT), prompts=[CLEAN])
        self.assertEqual(self.status(r, "LIMIT-TEXT"), S.PASS)

    def test_check_limit_text_names_the_floor_error(self):
        row = predispatch.check_limit_text(
            [], self.reg, extraction_error="quoted run below the prompt floor — not scanned — "
                                           "the run at offset 146 is 49 chars")
        self.assertEqual(row.status, S.ERROR)
        self.assertTrue(row.blocking)
        self.assertIn("below the prompt floor", row.detail)
        self.assertIn("offset 146", row.detail)


if __name__ == "__main__":
    unittest.main()
