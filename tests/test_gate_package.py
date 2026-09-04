"""FINAL_PRODUCTION_PACKAGE parser (CANON-GATE-001 plan §B package.py, §F).

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

Fixtures are the four committed EVAL-038 packages, read in place and never modified. Prompt
extraction must reproduce the four committed media/prompts/*.txt after whitespace
normalisation, consistent with media/prompts/EXTRACTION-RECORD.json.
Run: python3 -m unittest tests.test_gate_package
"""
import re
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
# M-01 / M-02 fixtures (Ruling 8): a text-bearing tail after a legitimately nested straight-
# quoted string (the fourth checker's A1/A2/A3), and the symbol-initial price strings. Each
# lead is clean and >= 120 chars so a truncated extraction would PASS LIMIT-TEXT.
NESTED = ('A model showing the "Aster Meridian" on her wrist, chat bubbles and a notification '
          'counter on screen')
PRICES = 'she holds "₹9" and "₹99" in gold, chat bubbles and a notification counter on screen'
PRICES3 = ('she holds "₹9" and "₹99" and "₹999" in gold, chat bubbles and a notification '
           'counter on screen')
DOUBT_THEN_SPACE_LED = f'{CLEAN} 6" then " chat bubbles and a notification counter past 99'
# N-01 / N-05 fixtures (Ruling 9): a straight-quoted string nested inside a prompt whose
# opener is followed by whitespace (space, `.`-closed, then-next-prompt, inside a K-02 outer,
# newline, NBSP, TAB) — the fifth checker's K11, K11b, K11e, K11f, K12, K12b, K17 — and K16,
# a stand-alone second prompt under the floor. At HEAD e47cf13 the class-3 reading closes
# the prompt at the inner opener, the text-bearing remainder pairs into a sub-floor run
# that `_quoted_runs` drops without trace, and LIMIT-TEXT PASSes.
TAIL = "in gold, chat bubbles and a notification counter on screen"
N01_SHAPES = (
    ("K11 padded inner both", f'"{CLEAN} she holds " Aster " {TAIL}"\n'),
    ("K11b padded opener, .closer", f'"{CLEAN} she holds " Aster." {TAIL}"\n'),
    ("K11e padded both, .\" + next prompt", f'"{CLEAN} she holds " Aster " {TAIL}."\n"{CLEAN}"\n'),
    ("K11f padded both, K-02 outer", f'" {CLEAN} she holds " Aster " {TAIL} "\n'),
    ("K12 inner opener + newline",
     f'"{CLEAN} she reads "\nAster Meridian\n" on her wrist, chat bubbles and a notification '
     f'counter on screen"\n'),
    ("K12b inner opener + NBSP", f'"{CLEAN} she holds "\u00a0Aster\u00a0" {TAIL}"\n'),
    ("K17 inner opener + TAB", f'"{CLEAN} she holds "\tAster\t" {TAIL}"\n'),
)
K16_SHORT_SECOND_PROMPT = f'"{CLEAN}"\n"chat bubbles and a notification counter on screen"\n'

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

    def test_short_quotes_are_an_error_not_ignored(self):
        # Until Ruling 9 this pin read `assertEqual(extract_prompts(pkg), [])`: runs under
        # PROMPT_MIN_CHARS were ignored. Ruling 9 (N-01/N-05) makes a sub-floor quoted run
        # in GENERATION_PROMPTS an extraction error — the floor no longer discards anything.
        pkg = package.parse_package('GENERATION_PROMPTS\nsay "hello there" and "' + "x" * 119 + '"\n')
        with self.assertRaises(package.PromptBelowFloor) as cm:
            package.extract_prompts(pkg)
        self.assertIn("quoted run below the prompt floor — not scanned", str(cm.exception))
        self.assertIn("'hello there'", str(cm.exception))
        # a run exactly at the floor is a prompt
        pkg = package.parse_package('GENERATION_PROMPTS\n"' + "x" * 120 + '"\n')
        self.assertEqual([p.text for p in package.extract_prompts(pkg)], ["x" * 120])


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


class M01NestedQuotesTest(unittest.TestCase):
    """Ruling 8 (M-01, M-02): a straight-quoted string nested inside a prompt never closes the
    prompt at the inner closer. Either the whole prompt is extracted (the inner string is
    provably nested) or extraction raises UnbalancedQuotes — never a truncated prompt whose
    text-bearing tail goes unscanned."""

    def prompts(self, section):
        return [p.text for p in package.extract_prompts(
            package.parse_package("GENERATION_PROMPTS\n" + section))]

    def assertWhole(self, section, expected):
        got = self.prompts(section)
        self.assertEqual(got, expected)
        for text in got:
            if "Aster" in text:
                self.assertIn("chat bubbles", text,
                              "the inner closer was allowed to close the outer run")

    def test_m01_a1_a_nested_string_does_not_close_the_prompt(self):
        # A1: the prompt ends in a letter; at HEAD d19cb3a the run closed at `Meridian"` and
        # the clean 160-char head PASSed while the text-bearing tail was never scanned
        self.assertWhole(f'"{CLEAN} {NESTED}"\n', [f"{CLEAN} {NESTED}"])

    def test_m01_a2_the_tail_is_kept_when_another_prompt_follows(self):
        # A2: `."` then a second prompt; at HEAD the `."` opened a phantom run that swallowed
        # the second prompt, and the first prompt's tail was lost
        self.assertWhole(f'"{CLEAN} {NESTED}."\n"{CLEAN}"\n', [f"{CLEAN} {NESTED}.", CLEAN])

    def test_m01_a3_the_tail_is_kept_when_the_prompt_is_last(self):
        # A3: the only shape that already failed closed (ERROR); now the prompt is whole
        self.assertWhole(f'"{CLEAN} {NESTED}."\n', [f"{CLEAN} {NESTED}."])

    def test_m01_a_nested_string_closed_by_a_bracket_is_still_nested(self):
        body = f'{CLEAN} the watch ("Aster Meridian") on her wrist, chat bubbles on screen'
        self.assertWhole(f'"{body}"\n', [body])

    def test_m01_a_symbol_initial_string_inside_a_prompt_is_an_error_not_a_close(self):
        # `"₹9`: prev is a space, next is a symbol — a nested opener or a closer with K-02
        # trailing whitespace; two pairings, so neither is chosen. At HEAD the run closed here.
        with self.assertRaises(package.UnbalancedQuotes) as cm:
            self.prompts(f'"{CLEAN} {PRICES}"\n')
        self.assertIn("unbalanced quotes", str(cm.exception))

    def test_m02_a_symbol_initial_string_after_a_doubt_point_is_an_error(self):
        # the fourth checker's M-02 shape: HEAD ERROR only through the second raise
        with self.assertRaises(package.UnbalancedQuotes):
            self.prompts(f'"{CLEAN} {PRICES3}"\n')
        # a doubt point (`6"` + prose) followed by a symbol-initial string
        with self.assertRaises(package.UnbalancedQuotes):
            self.prompts(f'"{CLEAN} 6" then "₹9" and chat bubbles past 99"\n')

    def test_m02_a_space_led_quote_after_a_doubt_point_is_an_error(self):
        # isolates the second raise: with it disabled the `" ` closes the run after `then`,
        # the clean head PASSes and `past 99"` is skipped as an inch mark — PASS over the
        # unscanned "chat bubbles"
        with self.assertRaises(package.UnbalancedQuotes) as cm:
            self.prompts(f'"{DOUBT_THEN_SPACE_LED}"\n')
        self.assertIn("inch mark under one pairing", str(cm.exception))

    def test_m01_a_letter_preceded_quote_outside_any_run_is_an_error(self):
        # the orphan closer (HEAD :198) is no longer skipped: it is the trace every early
        # close leaves behind. A digit-preceded one is still the F-12 inch mark.
        with self.assertRaises(package.UnbalancedQuotes) as cm:
            self.prompts(f'"{CLEAN}"\nchat bubbles on screen" then\n')
        self.assertIn("closes no open run", str(cm.exception))
        self.assertEqual(self.prompts(f'"{CLEAN}"\nthe 5" screen\n"{CLEAN}"\n'), [CLEAN, CLEAN])

    def test_m01_declared_aspect_survives_the_new_errors(self):
        pkg = package.parse_package(f'DELIVERABLE\none 4:5 poster\nGENERATION_PROMPTS\n"{CLEAN} {PRICES}"\n')
        self.assertEqual(package.declared_aspect(pkg), "4:5")
        pkg = package.parse_package(f'GENERATION_PROMPTS\n"{CLEAN} {PRICES}"\n')
        self.assertIsNone(package.declared_aspect(pkg))


class N01SubFloorRunTest(unittest.TestCase):
    """Ruling 9 (N-01, N-05): a quoted run inside GENERATION_PROMPTS that falls under the
    prompt floor is an extraction error, never a silent drop. The class-3 whitespace reading
    (a could-open quote followed by whitespace closes the run) stays; its worst case is now
    PromptBelowFloor, not a PASS over the unscanned remainder."""

    def prompts(self, section):
        return [p.text for p in package.extract_prompts(
            package.parse_package("GENERATION_PROMPTS\n" + section))]

    def assertFloorError(self, section, name):
        with self.assertRaises(package.PromptBelowFloor, msg=name) as cm:
            self.prompts(section)
        self.assertIn("quoted run below the prompt floor — not scanned", str(cm.exception), name)
        self.assertIsInstance(cm.exception, package.ExtractionError)

    def test_n01_the_seven_class_3_shapes_are_errors(self):
        for name, section in N01_SHAPES:
            with self.subTest(name):
                self.assertFloorError(section, name)

    def test_n05_k16_a_short_second_prompt_is_an_error(self):
        self.assertFloorError(K16_SHORT_SECOND_PROMPT, "K16")

    def test_n01_the_error_names_the_run_and_the_floor(self):
        with self.assertRaises(package.PromptBelowFloor) as cm:
            self.prompts(K16_SHORT_SECOND_PROMPT)
        msg = str(cm.exception)
        self.assertIn("GENERATION_PROMPTS", msg)
        self.assertIn("'chat bubbles and a notification counter on screen'", msg)
        self.assertIn(f"{package.PROMPT_MIN_CHARS}-char floor", msg)
        self.assertIn(f"offset {len(CLEAN) + 3}", msg)

    def test_n01_a_short_curly_run_is_an_error_too(self):
        # the floor applied to both quote styles; it discards neither now
        with self.assertRaises(package.PromptBelowFloor):
            self.prompts(f'"{CLEAN}"\n\u201cchat bubbles on screen\u201d\n')
        self.assertEqual(self.prompts(f'"{CLEAN}"\n\u201c{CLEAN}\u201d\n'), [CLEAN, CLEAN])

    def test_n01_a_run_nested_inside_another_is_covered_not_an_error(self):
        # the fourth checker's A5 (a curly-quoted name inside a straight prompt) and its
        # mirror: the inner run's bytes are scanned as part of the outer prompt, so the floor
        # does not apply to it — only to runs that no other run contains. This is the same
        # fact `_straight_runs` already applies to a straight string nested in a straight
        # prompt (M-01); it is not a guess about what the inner run "looks like".
        inner_curly = (f'{CLEAN} the \u201cAster Meridian\u201d on her wrist, chat bubbles and a '
                       f'notification counter')
        self.assertEqual(self.prompts(f'"{inner_curly}"\n'), [inner_curly])
        inner_straight = (f'{CLEAN} the "Aster Meridian" on her wrist, chat bubbles and a '
                          f'notification counter')
        self.assertEqual(self.prompts(f'\u201c{inner_straight}\u201d\n'), [inner_straight])
        # a nested run over the floor is not a second prompt either: it is scanned once, as
        # part of the prompt that contains it
        long_inner = f'{CLEAN} she reads \u201c{CLEAN}\u201d on the card, chat bubbles on screen'
        self.assertEqual(self.prompts(f'"{long_inner}"\n'), [long_inner])
        # but a sub-floor run that is not contained by any other still errors
        with self.assertRaises(package.PromptBelowFloor):
            self.prompts(f'"{inner_curly}"\n\u201cAster\u201d\n')

    def test_n01_pairing_errors_still_come_first(self):
        # a section that both fails to pair and carries a short run reports the pairing error
        with self.assertRaises(package.UnbalancedQuotes):
            self.prompts(f'"{CLEAN} {PRICES}"\n')

    def test_n01_declared_aspect_survives_the_floor_error(self):
        pkg = package.parse_package(
            f'DELIVERABLE\none 4:5 poster\nGENERATION_PROMPTS\n{K16_SHORT_SECOND_PROMPT}')
        self.assertEqual(package.declared_aspect(pkg), "4:5")
        pkg = package.parse_package(f'GENERATION_PROMPTS\n{K16_SHORT_SECOND_PROMPT}')
        self.assertIsNone(package.declared_aspect(pkg))


class N01NoSilentDiscardInvariantTest(unittest.TestCase):
    """Ruling 9 condition 1, as a property over a set of sections: for any GENERATION_PROMPTS
    section, either `extract_prompts` returns prompts whose texts cover every run
    `_straight_runs` (and the curly pairing) yields, or extraction raises an ExtractionError
    (UnbalancedQuotes from pairing, PromptBelowFloor from the floor) that is justified by a
    run the section actually contains. There is no third outcome: nothing quoted is ever
    silently discarded."""

    @classmethod
    def sections(cls):
        out = []
        for path in (SONNET_B01, SONNET_B06, HAIKU_B01, HAIKU_B06, GEMMA_B02):
            out.append((path.name, package.parse_package(path.read_text())))
        synthetic = [
            *N01_SHAPES,
            ("K16 short second prompt", K16_SHORT_SECOND_PROMPT),
            ("K-05 OLED", '"Vertical 9:16, a young man at a desk in a cramped PG office, harsh '
                          'tube-light. A 6" OLED panel showing chat bubbles and a notification '
                          'counter."\n'),
            ("K-05 is 6\".", '"Vertical 9:16, a young man at a desk in a cramped PG office, harsh '
                             'tube-light. The panel is 6". It shows chat bubbles and a notification '
                             'counter."\n'),
            ("F-12 inch mark before", 'Note: the 5" screen is the hero.\n\n"' + "x" * 130 + '"\n'),
            ("F-12 inch mark between", '"' + "x" * 130 + '"\nthe 5" screen\n"' + "x" * 130 + ' 99"\n'),
            ("K-02 trailing space", '"' + "A matte plate, no text. " * 8 + '"\n'),
            ("K-02 leading space", '" ' + CLEAN + '"\n'),
            ("L-01 EOL closer", f'"{CLEAN}"\n"{DIRTY}"\n'),
            ("L-01 unclosed run", f'"{CLEAN}"\n"{CLEAN}\n'),
            *[(f"L-01 tail{tail!r}, last", f'"{CLEAN}"\n"{DIRTY}"{tail}\n') for tail in TAILS],
            *[(f"L-01 tail{tail!r}, then prompt", f'"{CLEAN}"\n"{DIRTY}"{tail}\n"{CLEAN}"\n')
              for tail in TAILS],
            ("L-01 Gemma idiom",
             'The text "IMAGE" (small) is paired with "₹9" (massive, bold, gold). Below it, '
             '"VIDEO" (small) is paired with "₹99" (massive, bold, gold). ' + "x" * 200
             + ' No "sale" badges.\n'),
            ("M-01 A1", f'"{CLEAN} {NESTED}"\n'),
            ("M-01 A2", f'"{CLEAN} {NESTED}."\n"{CLEAN}"\n'),
            ("M-01 A3", f'"{CLEAN} {NESTED}."\n'),
            ("M-01 symbol-initial", f'"{CLEAN} {PRICES}"\n'),
            ("M-02 symbol-initial x3", f'"{CLEAN} {PRICES3}"\n'),
            ("M-02 doubt, then space-led", f'"{DOUBT_THEN_SPACE_LED}"\n'),
            ("M-01 orphan closer", f'"{CLEAN}"\nchat bubbles on screen" then\n'),
            ("short label in prose", 'say "hello there" and "' + "x" * 119 + '"\n'),
            ("curly short", f'"{CLEAN}"\n\u201cchat bubbles on screen\u201d\n'),
            ("A5 curly inner in straight", f'"{CLEAN} the \u201cAster Meridian\u201d on her wrist, '
                                           f'chat bubbles and a notification counter"\n'),
            ("straight inner in curly", f'\u201c{CLEAN} the "Aster Meridian" on her wrist, chat '
                                        f'bubbles and a notification counter\u201d\n'),
            ("long curly inner in straight",
             f'"{CLEAN} she reads \u201c{CLEAN}\u201d on the card, chat bubbles on screen"\n'),
            ("A4 curly outer, inch mark inside",
             f'\u201c{CLEAN} a 6" OLED panel showing chat bubbles and a notification counter\u201d\n'),
        ]
        for name, section in synthetic:
            out.append((name, package.parse_package("GENERATION_PROMPTS\n" + section)))
        return out

    @staticmethod
    def spans(section):
        """Every quoted run of the section as (start, end, body): straight runs from
        `_straight_runs` (raises UnbalancedQuotes), curly runs from the same regex
        `_quoted_runs` uses. `end` is the offset of the closing quote."""
        runs = list(package._straight_runs(section))
        runs += [(m.start(), m.group(1))
                 for m in re.finditer(r"\u201c([^\u201c\u201d]*)\u201d", section, re.S)]
        return sorted((s, s + 1 + len(b), b) for s, b in runs)

    def test_every_quoted_run_is_extracted_or_the_section_errors(self):
        cases = self.sections()
        self.assertGreaterEqual(len(cases), 40)
        outcomes = {"extracted": 0, "unbalanced": 0, "floor": 0}
        for name, pkg in cases:
            with self.subTest(name):
                section = pkg.sections["GENERATION_PROMPTS"]
                try:
                    runs = self.spans(section)
                except package.UnbalancedQuotes:
                    with self.assertRaises(package.UnbalancedQuotes):
                        package.extract_prompts(pkg)
                    outcomes["unbalanced"] += 1
                    continue
                # a run strictly inside another run's span is nested: its bytes are scanned
                # as part of the run that contains it (computed here, independently of
                # `_quoted_runs`, from the spans alone)
                outer = [(s, e, b) for s, e, b in runs
                         if not any(s2 < s and e < e2 for s2, e2, _ in runs)]
                nested = [r for r in runs if r not in outer]
                short_outer = [b for _, _, b in outer if len(b) < package.PROMPT_MIN_CHARS]
                if short_outer:
                    # exactly one admitted outcome: the floor error, and it must name a run
                    # the section really contains
                    with self.assertRaises(package.PromptBelowFloor) as cm:
                        package.extract_prompts(pkg)
                    self.assertTrue(any(" ".join(b.split()) in str(cm.exception)
                                        for b in short_outer), (name, str(cm.exception)))
                    outcomes["floor"] += 1
                    continue
                # otherwise extraction must succeed and cover every outermost run exactly,
                # and every nested run through the outermost run that contains it
                prompts = package.extract_prompts(pkg)
                texts = [p.text for p in prompts]
                for start, _, body in outer:
                    self.assertIn(body.strip(), texts, (name, start))
                for s, e, body in nested:
                    holder = [b for s2, e2, b in outer if s2 < s and e < e2]
                    self.assertTrue(holder, (name, s))
                    self.assertTrue(any(body in b for b in holder), (name, s))
                    self.assertNotIn(body.strip(), texts, (name, s, "nested run extracted twice"))
                outcomes["extracted"] += 1
        # the set exercises all three admitted outcomes
        self.assertTrue(all(outcomes.values()), outcomes)


if __name__ == "__main__":
    unittest.main()
