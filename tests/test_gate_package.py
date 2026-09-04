"""FINAL_PRODUCTION_PACKAGE parser (CANON-GATE-001 plan §B package.py, §F).

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

Fixtures are the four committed EVAL-038 packages, read in place and never modified. Prompt
extraction must reproduce the four committed media/prompts/*.txt after whitespace
normalisation, consistent with media/prompts/EXTRACTION-RECORD.json.
Run: python3 -m unittest tests.test_gate_package
"""
import unittest
from pathlib import Path

from canon.gate import package

REPO_ROOT = Path(__file__).resolve().parents[1]
E38 = REPO_ROOT / "eval/experiments/EVAL-038"
SONNET_B01 = E38 / "baseline/sonnet-no-canon/E037-sonnet-no-canon-B01-R1.txt"
SONNET_B06 = E38 / "baseline/sonnet-no-canon/E037-sonnet-no-canon-B06-R1.txt"
HAIKU_B01 = E38 / "runs/haiku-packs/packages/E038-haiku-packs-B01-R1.txt"
HAIKU_B06 = E38 / "runs/haiku-packs/packages/E038-haiku-packs-B06-R1.txt"
PROMPTS = E38 / "media/prompts"
GEMMA_B02 = E38 / "runs/gemma-packs/packages/E038-gemma-packs-B02-R1.txt"
# L-01 fixtures: a clean 144-char prompt, a text-bearing prompt that ends in a digit, and the
# six tail shapes the third checker listed after a digit-ending closer.
CLEAN = ("A matte plate, no text. " * 6).strip()
DIRTY = ("Vertical 9:16, a smartphone screen filling with WhatsApp rent-reminder chat bubbles "
         "and a notification counter climbing past 99")
TAILS = (" (8 s)", " — 4 s", " | 4 s |", ". Then the next shot.", " 8 s", " then the next shot")

V1_SECTIONS = ["DELIVERABLE", "OBJECTIVE_INTERPRETATION", "CORE_CREATIVE_IDEA",
               "MESSAGE_AND_INFORMATION_HIERARCHY", "VISUAL_SYSTEM", "PRODUCTION_RECIPE",
               "GENERATION_PROMPTS", "DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS", "AUDIO_AND_EDIT",
               "FAILURE_PREVENTION", "HARD_CONSTRAINT_CHECK", "KNOWLEDGE_AND_WEBSITE_USE"]


def norm(s):
    return " ".join(s.split())


class ParseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s01 = package.parse_package(SONNET_B01.read_text())
        cls.s06 = package.parse_package(SONNET_B06.read_text())
        cls.h01 = package.parse_package(HAIKU_B01.read_text())
        cls.h06 = package.parse_package(HAIKU_B06.read_text())

    def test_section_regex_is_strip_blinds(self):
        src = (E38 / "tools/strip_blind.py").read_text()
        self.assertIn(package.SECTION_RE.pattern, src)

    def test_v1_packages(self):
        # Sonnet B01 uses `##` headings and Sonnet B06 bare ones; both are v1 by content
        # (no typed VISUAL_SYSTEM subfields, no DOCTRINE_DEVIATIONS) — schema is decided by
        # the v2 contract's fields, not by heading style.
        for pkg in (self.s01, self.s06):
            self.assertEqual(pkg.schema, "v1")
            for name in V1_SECTIONS:
                self.assertIn(name, pkg.sections, name)
            self.assertNotIn("DOCTRINE_DEVIATIONS", pkg.sections)
            self.assertEqual(pkg.subfields, {})
        self.assertTrue(self.s06.sections["DELIVERABLE"].startswith("One premium"))
        self.assertIn("Aspect ratio: 4:5, vertical.", self.s06.sections["VISUAL_SYSTEM"])

    def test_v2_hash_headings_and_typed_subfields(self):
        for pkg in (self.h01, self.h06):
            self.assertEqual(pkg.schema, "v2")
            self.assertIn("DOCTRINE_DEVIATIONS", pkg.sections)
            self.assertEqual(sorted(pkg.subfields),
                             sorted(package.TYPED_SUBFIELDS) if pkg is self.h06
                             else ["attention_order", "implied_light_source", "placement_zone",
                                   "surface_finish_per_key_object"])
        self.assertTrue(self.h06.subfields["placement_zone"].startswith("Watch dial positioned"))
        self.assertIn("45° above horizontal", self.h06.subfields["implied_light_source"])
        self.assertTrue(self.h01.subfields["attention_order"].startswith("- **1st read"))
        # a subfield's text stops at the next subfield
        self.assertNotIn("implied_light_source", self.h06.subfields["surface_finish_per_key_object"])

    def test_bold_headings_and_trailing_colon_parse(self):
        # strip_blind's SECTION_RE accepts `**NAME**` and `NAME:` (not `**NAME:**`)
        pkg = package.parse_package("**DELIVERABLE**\none image\n\nVISUAL_SYSTEM:\nkey light\n")
        self.assertEqual(pkg.sections["DELIVERABLE"].strip(), "one image")
        self.assertEqual(pkg.sections["VISUAL_SYSTEM"].strip(), "key light")

    def test_empty_typed_subfield_is_recorded_as_empty(self):
        pkg = package.parse_package("## VISUAL_SYSTEM\n**placement_zone:**\n\n**attention_order:**\n"
                                    "1st read: dial\n")
        self.assertEqual(pkg.subfields["placement_zone"], "")
        self.assertEqual(pkg.subfields["attention_order"].strip(), "1st read: dial")

    def test_scope_text_reads_typed_subfield_first_then_prose(self):
        # v2: the typed subfield; v1: falls back to the VISUAL_SYSTEM prose
        got = package.scope_text(self.h06, ["VISUAL_SYSTEM.placement_zone"])
        self.assertEqual(got.sources, ["VISUAL_SYSTEM.placement_zone"])
        self.assertTrue(got.text.startswith("Watch dial positioned"))
        got = package.scope_text(self.s06, ["VISUAL_SYSTEM.placement_zone", "GENERATION_PROMPTS"])
        self.assertEqual(got.sources, ["VISUAL_SYSTEM", "GENERATION_PROMPTS"])
        self.assertIn("Aspect ratio: 4:5", got.text)
        self.assertEqual(got.empty_subfields, [])
        pkg = package.parse_package("## VISUAL_SYSTEM\n**placement_zone:**\n\n## FAILURE_PREVENTION\nx\n")
        got = package.scope_text(pkg, ["VISUAL_SYSTEM.placement_zone", "FAILURE_PREVENTION"])
        self.assertEqual(got.empty_subfields, ["VISUAL_SYSTEM.placement_zone"])
        self.assertEqual(got.sources, ["FAILURE_PREVENTION"])
        got = package.scope_text(pkg, ["AUDIO_AND_EDIT"])
        self.assertEqual(got.sources, [])
        self.assertEqual(got.text, "")


class PromptExtractionTest(unittest.TestCase):
    def committed(self, name):
        return norm((PROMPTS / f"{name}.txt").read_text())

    def test_sonnet_b01_first_quoted_prompt_is_the_dispatched_one(self):
        prompts = package.extract_prompts(package.parse_package(SONNET_B01.read_text()))
        self.assertEqual(len(prompts), 4)
        self.assertEqual([p.index for p in prompts], [1, 2, 3, 4])
        self.assertEqual(norm(prompts[0].text), self.committed("B01-sonnet-no-canon"))
        self.assertEqual(prompts[0].origin, "quoted")
        self.assertTrue(prompts[3].text.endswith("to be added in post."))

    def test_sonnet_b06_first_quoted_prompt_is_the_dispatched_one(self):
        prompts = package.extract_prompts(package.parse_package(SONNET_B06.read_text()))
        self.assertEqual(norm(prompts[0].text), self.committed("B06-sonnet-no-canon"))
        # the negative/exclusion guidance is a second double-quoted run >= 120 chars
        self.assertEqual(len(prompts), 2)
        self.assertTrue(prompts[1].text.startswith("no date window"))

    def test_haiku_b06_blockquote_prompt_matches_committed(self):
        prompts = package.extract_prompts(package.parse_package(HAIKU_B06.read_text()))
        self.assertEqual(len(prompts), 1)
        self.assertEqual(prompts[0].origin, "blockquote")
        self.assertEqual(norm(prompts[0].text), self.committed("B06-haiku-packs"))
        self.assertNotIn("**", prompts[0].text)

    def test_haiku_b01_shot_1_prompt_matches_committed(self):
        prompts = package.extract_prompts(package.parse_package(HAIKU_B01.read_text()))
        self.assertEqual(norm(prompts[0].text), self.committed("B01-haiku-packs"))
        # shots 1, 2, 3, 4a-4d, 5, 6 — nine quoted visual prompts, in package order
        self.assertEqual(len(prompts), 9)
        self.assertTrue(prompts[1].text.startswith("Extreme close-up macro shot"))
        self.assertTrue(prompts[8].text.startswith("Clean, minimal title card"))

    def test_missing_generation_prompts_yields_no_prompts(self):
        pkg = package.parse_package("DELIVERABLE\none image\n")
        self.assertEqual(package.extract_prompts(pkg), [])

    def test_short_quotes_are_not_prompts(self):
        pkg = package.parse_package('GENERATION_PROMPTS\nsay "hello there" and "' + "x" * 119 + '"\n')
        self.assertEqual(package.extract_prompts(pkg), [])


class ShotAndDeclarationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s01 = package.parse_package(SONNET_B01.read_text())
        cls.s06 = package.parse_package(SONNET_B06.read_text())
        cls.h01 = package.parse_package(HAIKU_B01.read_text())
        cls.h06 = package.parse_package(HAIKU_B06.read_text())

    def test_sonnet_b01_shot_table_11_rows_26_seconds(self):
        shots = package.extract_shots(self.s01)
        self.assertEqual(len(shots), 11)
        self.assertEqual([s.label for s in shots], [str(i) for i in range(1, 12)])
        self.assertEqual(package.shot_sum_s(shots), 26.0)
        self.assertEqual((shots[2].duration_s_min, shots[2].duration_s_max), (1.5, 1.5))

    def test_haiku_b01_six_shot_headings(self):
        shots = package.extract_shots(self.h01)
        self.assertEqual(len(shots), 6)
        self.assertEqual([s.label for s in shots], ["1", "2", "3", "4", "5", "6"])
        self.assertEqual([(s.duration_s_min, s.duration_s_max) for s in shots],
                         [(3.0, 4.0), (2.0, 2.0), (1.5, 1.5), (4.0, 5.0), (2.0, 2.0), (2.0, 3.0)])

    @unittest.expectedFailure
    def test_haiku_b01_shot_sum_is_16_5_as_the_plan_states(self):
        # DISCREPANCY recorded for the checker. Plan §F states "Haiku B01 -> 6 shots summing
        # to 16.5 s (max of ranges)". The six Shot headings in GENERATION_PROMPTS carry
        # 3-4 / 2 / 1.5 / 4-5 / 2 / 2-3 seconds, whose maxima sum to 17.5 s. 16.5 s is the
        # sum of the AUDIO_AND_EDIT edit-table column (3.5 / 2 / 1.5 / 4.5 / 2 / 2.5-3),
        # whose rows ("| 1 (Chaos setup) |") match none of the plan's SHOT_PATTERNS. Built
        # to the plan's patterns; the number is not tuned. Verdict unaffected (17.5 vs 30 s
        # is outside +/-20 % exactly as 16.5 is).
        self.assertEqual(package.shot_sum_s(package.extract_shots(self.h01)), 16.5)

    def test_haiku_b01_shot_sum_observed(self):
        self.assertEqual(package.shot_sum_s(package.extract_shots(self.h01)), 17.5)

    def test_shot_list_comes_from_the_single_richest_section(self):
        # Sonnet B01 GENERATION_PROMPTS also carries four "**Shot 1-5 ..." headings; the
        # 11-row PRODUCTION_RECIPE table is the shot list, not the union (15).
        shots = package.extract_shots(self.s01)
        self.assertTrue(all(s.section == "PRODUCTION_RECIPE" for s in shots))

    def test_declared_aspect(self):
        self.assertEqual(package.declared_aspect(self.s01), "9:16")
        self.assertEqual(package.declared_aspect(self.h01), "9:16")
        self.assertEqual(package.declared_aspect(self.s06), "4:5")
        self.assertEqual(package.declared_aspect(self.h06), "4:5")
        self.assertIsNone(package.declared_aspect(package.parse_package("DELIVERABLE\nan image\n")))

    def test_declared_duration(self):
        self.assertEqual(package.declared_duration_s(self.s01), 30.0)
        self.assertEqual(package.declared_duration_s(self.h01), 30.0)
        self.assertIsNone(package.declared_duration_s(self.s06))
        self.assertIsNone(package.declared_duration_s(self.h06))

    def test_declared_min_dimensions(self):
        self.assertEqual(package.declared_min_dimensions(self.s06), (1600, 2000))
        self.assertIsNone(package.declared_min_dimensions(self.h06))
        self.assertIsNone(package.declared_min_dimensions(self.s01))

    def test_f04_find_aspect_ignores_clock_times(self):
        fa = package.find_aspect
        self.assertEqual(fa("Vertical 9:16 handheld video"), "9:16")
        self.assertEqual(fa("4:5 aspect ratio (e.g., 1600×2000 px minimum"), "4:5")
        self.assertEqual(fa("One vertical (9:16) commercial video"), "9:16")
        self.assertEqual(fa("Deliverable: 3:4."), "3:4")            # no context: an aspect
        self.assertEqual(fa("Hands set to 10:10 as convention. 4:5 aspect"), "4:5")
        self.assertIsNone(fa("Hands set to 10:10 as convention."))
        self.assertIsNone(fa("Time must read ~10:10."))
        self.assertIsNone(fa("the logo holds for the last 0:03"))
        self.assertIsNone(fa("shot runs 0:05–0:12"))
        self.assertIsNone(fa("at 10:10 sharp"))
        self.assertEqual(fa("at 16:9 aspect"), "16:9")               # aspect context wins

    def test_f14_exclamation_inside_a_clause_does_not_split(self):
        split = package.split_sentences
        self.assertEqual(split("a spreadsheet with a visible #REF! error as a cursor clicks. Next."),
                         ["a spreadsheet with a visible #REF! error as a cursor clicks", "Next."])
        # the delimiter is consumed, as `.` and `;` already are
        self.assertEqual(split("Really! The next shot"), ["Really", "The next shot"])
        self.assertEqual(split("Why? Because."), ["Why", "Because."])
        self.assertEqual(split("go! 9:16 frame"), ["go", "9:16 frame"])
        self.assertEqual(split("Cut; then hold. Done"), ["Cut", "then hold", "Done"])

    def test_f12_inch_mark_before_the_prompts_does_not_shift_pairing(self):
        body = "x" * 130
        pkg = package.parse_package(
            'GENERATION_PROMPTS\nNote: the 5" screen is the hero.\n\n"' + body + '"\n')
        prompts = package.extract_prompts(pkg)
        self.assertEqual([p.text for p in prompts], [body])
        # and between prompts, and a genuine closing quote after a digit still closes
        pkg = package.parse_package(
            'GENERATION_PROMPTS\n"' + body + '"\nthe 5" screen\n"' + body + ' 99"\n')
        self.assertEqual([p.text for p in package.extract_prompts(pkg)], [body, body + " 99"])

    def test_k02_whitespace_inside_the_quotes_still_pairs(self):
        # checker K-02 / Ruling 6 condition 2: a closing quote preceded by whitespace and an
        # opening quote followed by whitespace pair normally
        body = "A matte plate, no text. " * 8            # 192 chars, trailing space
        pkg = package.parse_package('GENERATION_PROMPTS\n"' + body + '"\n')
        self.assertEqual([p.text for p in package.extract_prompts(pkg)], [body.strip()])
        pkg = package.parse_package('GENERATION_PROMPTS\n" ' + body.strip() + '"\n')
        self.assertEqual([p.text for p in package.extract_prompts(pkg)], [body.strip()])
        pkg = package.parse_package('GENERATION_PROMPTS\n" ' + body + '"\n')
        self.assertEqual([p.text for p in package.extract_prompts(pkg)], [body.strip()])

    def test_k05_an_inch_mark_inside_a_prompt_does_not_truncate_it(self):
        # checker K-05 / Ruling 6 condition 5: a digit-preceded quote mid-line inside an open
        # run is a measurement; the run closes at the end-of-line quote
        lead = "Vertical 9:16, a young man at a desk in a cramped PG office, harsh tube-light. "
        for tail in ('A 6" OLED panel showing chat bubbles and a notification counter.',
                     'The panel is 6". It shows chat bubbles and a notification counter.'):
            pkg = package.parse_package('GENERATION_PROMPTS\n"' + lead + tail + '"\n')
            prompts = package.extract_prompts(pkg)
            self.assertEqual([p.text for p in prompts], [lead + tail], tail)
        # a digit-preceded quote followed by a bracket or end-of-line still closes
        body = "x" * 130
        pkg = package.parse_package('GENERATION_PROMPTS\n(see "' + body + ' 38") then\n"' + body + ' 99"\n')
        self.assertEqual([p.text for p in package.extract_prompts(pkg)], [body + " 38", body + " 99"])

    def test_f12_sonnet_b01_prompts_survive_an_inch_mark_above_them(self):
        text = SONNET_B01.read_text().replace(
            "**Shot 1–5 (Chaos block)", 'Note: the 5" screen is the hero.\n\n**Shot 1–5 (Chaos block)')
        before = [p.text for p in package.extract_prompts(package.parse_package(SONNET_B01.read_text()))]
        after = [p.text for p in package.extract_prompts(package.parse_package(text))]
        self.assertEqual(len(before), 4)
        self.assertEqual(after, before)

    def test_l01_a_run_still_open_at_the_end_of_the_section_is_an_error(self):
        # Ruling 7 condition 1: a run still open at the end of GENERATION_PROMPTS is an
        # extraction error — the gate never guesses a closer
        pkg = package.parse_package(f'GENERATION_PROMPTS\n"{CLEAN}"\n"{DIRTY}" (8 s)\n')
        with self.assertRaises(package.UnbalancedQuotes) as cm:
            package.extract_prompts(pkg)
        self.assertIn("unbalanced quotes", str(cm.exception))
        pkg = package.parse_package(f'GENERATION_PROMPTS\n"{CLEAN}"\n"{CLEAN}\n')
        with self.assertRaises(package.UnbalancedQuotes):
            package.extract_prompts(pkg)

    def test_l01_the_gemma_price_idiom_is_an_error_not_a_phantom_prompt(self):
        # Ruling 7 condition 3(a): `"₹9" (massive …)` — a digit-preceded quote followed by
        # prose, then a quote that opens a new string; two pairings are possible, so neither
        # is chosen. The committed package is read in place.
        with self.assertRaises(package.UnbalancedQuotes) as cm:
            package.extract_prompts(package.parse_package(GEMMA_B02.read_text()))
        self.assertIn("unbalanced quotes", str(cm.exception))
        idiom = ('The text "IMAGE" (small) is paired with "₹9" (massive, bold, gold). Below it, '
                 '"VIDEO" (small) is paired with "₹99" (massive, bold, gold). ' + "x" * 200
                 + ' No "sale" badges.')
        with self.assertRaises(package.UnbalancedQuotes):
            package.extract_prompts(package.parse_package("GENERATION_PROMPTS\n" + idiom + "\n"))

    def test_l01_six_tails_after_a_digit_ending_closer_are_errors_not_drops(self):
        # Ruling 7 condition 3(b): after `…99"` + tail the run is in doubt; with nothing after
        # it the run never closes, with another prompt after it the next quote could open or
        # close — both are errors. The dirty prompt is never silently dropped or merged.
        for tail in TAILS:
            for follow in ("", f'"{CLEAN}"\n'):
                section = f'"{CLEAN}"\n"{DIRTY}"{tail}\n{follow}'
                pkg = package.parse_package("GENERATION_PROMPTS\n" + section)
                with self.assertRaises(package.UnbalancedQuotes, msg=(tail, follow)):
                    package.extract_prompts(pkg)

    def test_l01_a_digit_ending_closer_at_end_of_line_or_before_a_bracket_still_closes(self):
        # Ruling 7 condition 3(c)
        pkg = package.parse_package(f'GENERATION_PROMPTS\n"{CLEAN}"\n"{DIRTY}"\n')
        self.assertEqual([p.text for p in package.extract_prompts(pkg)], [CLEAN, DIRTY])
        pkg = package.parse_package(f'GENERATION_PROMPTS\n"{CLEAN}"\n"{DIRTY}")\n"{CLEAN}"\n')
        self.assertEqual([p.text for p in package.extract_prompts(pkg)], [CLEAN, DIRTY, CLEAN])
        # the K-05 shapes: an inch mark inside a run that closes at end of line
        pkg = package.parse_package(f'GENERATION_PROMPTS\n"{CLEAN} A 6" OLED panel, then {CLEAN}"\n')
        self.assertEqual([p.text for p in package.extract_prompts(pkg)],
                         [f'{CLEAN} A 6" OLED panel, then {CLEAN}'])

    def test_l01_declared_aspect_does_not_raise_on_an_unbalanced_prompt_section(self):
        pkg = package.parse_package(f'GENERATION_PROMPTS\n"{DIRTY}" (8 s)\n')
        self.assertIsNone(package.declared_aspect(pkg))
        pkg = package.parse_package(f'DELIVERABLE\none 4:5 poster\nGENERATION_PROMPTS\n"{DIRTY}" (8 s)\n')
        self.assertEqual(package.declared_aspect(pkg), "4:5")

    def test_duration_pattern_forms(self):
        self.assertEqual(package.parse_duration("2s"), (2.0, 2.0))
        self.assertEqual(package.parse_duration("~30 seconds"), (30.0, 30.0))
        self.assertEqual(package.parse_duration("(3–4 seconds)"), (3.0, 4.0))
        self.assertEqual(package.parse_duration("2.5-3 sec"), (2.5, 3.0))
        self.assertIsNone(package.parse_duration("shot 4"))
        self.assertIsNone(package.parse_duration("3 screens"))


if __name__ == "__main__":
    unittest.main()
