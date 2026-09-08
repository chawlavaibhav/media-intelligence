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
# P-01 fixtures (Ruling 10): the sixth checker's four curly shapes. At HEAD 8902fb1 the curly
# regex paired each “ with the next ” with none of the fail-closed rules `_straight_runs`
# enforces, so a curly quote nested in a curly prompt (C2), an orphan curly closer (C3) or an
# unclosed second curly prompt (C4, C4b) left the text-bearing remainder outside any run and
# LIMIT-TEXT PASSed. Under Ruling 10 straight quotes alone delimit prompts; a curly quote
# anywhere in GENERATION_PROMPTS is an extraction error.
LQ, RQ = "“", "”"
CURLY_ERROR = "curly quote in GENERATION_PROMPTS — straight quotes delimit prompts; not scanned"
P01_SHAPES = (
    ("C2 curly-in-curly, inner over the floor, dirty tail",
     f'{LQ}{CLEAN} she reads {LQ}{CLEAN}{RQ} on the card, chat bubbles and a notification '
     f'counter on screen{RQ}\n'),
    ("C3 orphan curly closer after a clean curly prompt",
     f'{LQ}{CLEAN}{RQ} chat bubbles and a notification counter on screen{RQ}\n'),
    ("C4 second curly prompt never closes", f'{LQ}{CLEAN}{RQ}\n{LQ}{DIRTY}\n'),
    ("C4b second curly prompt, closer typed as an opener", f'{LQ}{CLEAN}{RQ}\n{LQ}{DIRTY}{LQ}\n'),
)
# Q-01 fixtures (Ruling 11): the seventh checker's five section-parser shapes. At HEAD 0c21d76 a
# bare ALL-CAPS line of four or more characters (or a `###` heading) between two prompts
# matched SECTION_RE, opened a new section, and the second, text-bearing prompt was assigned
# to it — never extracted, never scanned — while LIMIT-TEXT PASSed on the first prompt alone.
# Under Ruling 11 parsing is unchanged (the line still opens a section); a heading outside
# KNOWN_SECTION_HEADINGS after GENERATION_PROMPTS has opened is an extraction error naming it.
UNKNOWN_HEADING_ERROR = ("unrecognised section heading after GENERATION_PROMPTS — prompts may be "
                         "hidden; not scanned")
Q01_SHAPES = (
    ("S6a IMPORTANT between prompts", f'"{CLEAN}"\nIMPORTANT\n"{DIRTY}"\n', "IMPORTANT"),
    ("S6b VIDEO label between prompts", f'"{CLEAN}"\nVIDEO\n"{DIRTY}"\n', "VIDEO"),
    ("S6c NOTE: between prompts", f'"{CLEAN}"\nNOTE:\n"{DIRTY}"\n', "NOTE"),
    ("S6e ### PROMPT_B between prompts", f'"{CLEAN}"\n### PROMPT_B\n"{DIRTY}"\n', "PROMPT_B"),
    ("S6i NOTES, then a dirty blockquote", f'"{CLEAN}"\nNOTES\n> {DIRTY}\n', "NOTES"),
)
# not headings under SECTION_RE (a digit, a space, a colon before the closing `**`): the
# second prompt stays in the section and is scanned (the seventh checker's S6d, S6f, S6j)
Q01_NOT_HEADINGS = (
    ("S6d **SHOT_2**", f'"{CLEAN}"\n**SHOT_2**\n"{DIRTY}"\n'),
    ("S6f SHOT 2", f'"{CLEAN}"\nSHOT 2\n"{DIRTY}"\n'),
    ("S6j **IMAGE_PROMPT:**", f'"{CLEAN}"\n**IMAGE_PROMPT:**\n"{DIRTY}"\n'),
)
# the headings that follow GENERATION_PROMPTS in the four anchors (and Gemma B02-R1), read
# off the files; every one is in the known set, so Ruling 11 leaves the anchors untouched
ANCHOR_HEADINGS_AFTER_PROMPTS = {
    SONNET_B01: ["DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS", "AUDIO_AND_EDIT", "FAILURE_PREVENTION",
                 "HARD_CONSTRAINT_CHECK", "KNOWLEDGE_AND_WEBSITE_USE"],
    SONNET_B06: ["DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS", "AUDIO_AND_EDIT", "FAILURE_PREVENTION",
                 "HARD_CONSTRAINT_CHECK", "KNOWLEDGE_AND_WEBSITE_USE"],
    HAIKU_B01: ["DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS", "AUDIO_AND_EDIT", "FAILURE_PREVENTION",
                "DOCTRINE_DEVIATIONS", "HARD_CONSTRAINT_CHECK", "KNOWLEDGE_AND_WEBSITE_USE"],
    HAIKU_B06: ["DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS", "AUDIO_AND_EDIT", "FAILURE_PREVENTION",
                "DOCTRINE_DEVIATIONS", "HARD_CONSTRAINT_CHECK", "KNOWLEDGE_AND_WEBSITE_USE"],
}
ANCHOR_PROMPT_COUNTS = {SONNET_B01: 4, SONNET_B06: 2, HAIKU_B01: 9, HAIKU_B06: 1}
# R-01 fixtures (Ruling 12, CONTROLLER-CANON-GATE-001-EIGHTH-CHECK-DISPOSITION-2026-09-07.md):
# the eighth checker's known-heading-as-divider shapes, in the checker's wrapper (VISUAL_SYSTEM
# and DELIVERABLE before the prompts, DOCTRINE_DEVIATIONS after). At HEAD dbbe76f every one
# was LIMIT-TEXT PASS with the dirty run unscanned: the Ruling 11 rule checks membership in
# the 15-heading union, not structure, so a known heading reused as a divider after
# GENERATION_PROMPTS opened a section the gate accepted. Under Ruling 12 a heading after the
# prompts that the corpus only ever places before them is an error
# (HeadingNotObservedAfterPrompts, 3a-3, 3d-1, 3d-2, 3d-5) and a heading repeated at or after
# the first GENERATION_PROMPTS line is an error (RepeatedSectionHeading, 3a-1, 3d-3). The rows
# whose only headings after the prompts are in KNOWN_HEADINGS_AFTER_PROMPTS, once each — 3a-2,
# 3a-4, 3a-6, 3a-8, 3d-4 — are the ruled boundary (register R-01 residual): neither refinement
# fires, and they are documented here, not tuned.
AFTER_SET_ERROR = ("section heading not observed after GENERATION_PROMPTS in the committed "
                   "schema — prompts may be hidden; not scanned")
REPEAT_ERROR = "section heading repeated after GENERATION_PROMPTS — prompts may be hidden; not scanned"
R01_PRE = "## VISUAL_SYSTEM\nkey light from upper-left; centre zone\n## DELIVERABLE\none 9:16 video\n"
R01_POST = "## DOCTRINE_DEVIATIONS\nnone\n"


def r01(section, pre=R01_PRE, post=R01_POST):
    """The eighth checker's wrapper: line 5 is GENERATION_PROMPTS, line 6 the first prompt,
    line 7 the divider under test, line 9 the wrapper's DOCTRINE_DEVIATIONS."""
    return pre + "## GENERATION_PROMPTS\n" + section + post


R01_AFTER_SET_SHAPES = (   # (name, package text, heading, its line)
    ("3a-3 DELIVERABLE repeated after the prompts as a divider",
     r01(f'"{CLEAN}"\n## DELIVERABLE\n"{DIRTY}"\n'), "DELIVERABLE", 7),
    ("3d-1 FINAL_PRODUCTION_PACKAGE bare divider",
     r01(f'"{CLEAN}"\nFINAL_PRODUCTION_PACKAGE\n"{DIRTY}"\n'), "FINAL_PRODUCTION_PACKAGE", 7),
    ("3d-2 ## FINAL_PRODUCTION_PACKAGE, then a dirty blockquote",
     r01(f'"{CLEAN}"\n## FINAL_PRODUCTION_PACKAGE\n> {DIRTY}\n'), "FINAL_PRODUCTION_PACKAGE", 7),
    ("3d-5 CORE_CREATIVE_IDEA after the prompts",
     r01(f'"{CLEAN}"\n## CORE_CREATIVE_IDEA\n"{DIRTY}"\n'), "CORE_CREATIVE_IDEA", 7),
)
R01_REPEAT_SHAPES = (      # (name, package text, heading, first line, second line)
    ("3a-1 FAILURE_PREVENTION divider, then the real FAILURE_PREVENTION",
     r01(f'"{CLEAN}"\n## FAILURE_PREVENTION\n"{DIRTY}"\n## FAILURE_PREVENTION\nreal notes\n'),
     "FAILURE_PREVENTION", 7, 9),
    ("3d-3 DOCTRINE_DEVIATIONS divider, then the wrapper's DOCTRINE_DEVIATIONS",
     r01(f'"{CLEAN}"\n## DOCTRINE_DEVIATIONS\n"{DIRTY}"\n'), "DOCTRINE_DEVIATIONS", 7, 9),
)
R01_BOUNDARY_SHAPES = (    # (name, package text): extracts CLEAN alone — register R-01 residual
    ("3a-2 FAILURE_PREVENTION divider, no repeat", r01(f'"{CLEAN}"\n## FAILURE_PREVENTION\n"{DIRTY}"\n')),
    ("3a-4 FAILURE_PREVENTION divider, then a dirty blockquote",
     r01(f'"{CLEAN}"\n## FAILURE_PREVENTION\n> {DIRTY}\n')),
    ("3a-6 AUDIO_AND_EDIT bare divider", r01(f'"{CLEAN}"\nAUDIO_AND_EDIT\n"{DIRTY}"\n')),
    ("3a-8 FAILURE_PREVENTION divider, dirty, the ordinary tail",
     r01(f'"{CLEAN}"\n## FAILURE_PREVENTION\n"{DIRTY}"\n## HARD_CONSTRAINT_CHECK\nok\n')),
    ("3d-4 DOCTRINE_DEVIATIONS divider, v1 package (no other DOCTRINE_DEVIATIONS)",
     r01(f'"{CLEAN}"\n## DOCTRINE_DEVIATIONS\n"{DIRTY}"\n', post="")),
)
# the seven after-prompts headings in the order the corpus places them (read off
# E038-haiku-packs-B03-R1.txt, the one committed package that carries all seven); asserted
# equal to the frozen set as a set in KnownHeadingsTest
AFTER_PROMPTS_SCHEMA_ORDER = ["DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS", "AUDIO_AND_EDIT",
                              "FAILURE_PREVENTION", "DOCTRINE_DEVIATIONS", "HARD_CONSTRAINT_CHECK",
                              "KNOWLEDGE_AND_WEBSITE_USE", "CREATIVE_BRIEF_TO_EXECUTION_NARRATIVE"]

V1_SECTIONS = ["DELIVERABLE", "OBJECTIVE_INTERPRETATION", "CORE_CREATIVE_IDEA",
               "MESSAGE_AND_INFORMATION_HIERARCHY", "VISUAL_SYSTEM", "PRODUCTION_RECIPE",
               "GENERATION_PROMPTS", "DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS", "AUDIO_AND_EDIT",
               "FAILURE_PREVENTION", "HARD_CONSTRAINT_CHECK", "KNOWLEDGE_AND_WEBSITE_USE"]


def norm(s):
    return " ".join(s.split())


def committed_packages():
    """The 84 committed EVAL-038 packages (baseline/, runs/*/packages/, judging/packages/**),
    read in place — the corpus Ruling 11's known heading set is derived from."""
    return sorted(p for p in list((E38 / "baseline").rglob("*.txt"))
                  + list((E38 / "runs").rglob("packages/*.txt"))
                  + list((E38 / "judging/packages").rglob("*.txt"))
                  if p.name != "FREEZE-COMMIT.txt")


def headings_in_order(text):
    """Every section heading of `text` in order of appearance, repeats kept, from SECTION_RE
    alone (the regex is parity-pinned to strip_blind.py) — independent of the helper the
    implementation uses."""
    matches = (package.SECTION_RE.match(line.strip()) for line in text.splitlines())
    return [m.group(1) for m in matches if m]


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

    def test_n01_a_short_curly_run_is_a_curly_error_now(self):
        # "curly short": flipped PromptBelowFloor→CurlyQuotes ERROR under Ruling 10 (curly quotes
        # are not delimiters); the curly long twin flipped extract [CLEAN, CLEAN]→ERROR likewise
        with self.assertRaises(package.CurlyQuotes) as cm:
            self.prompts(f'"{CLEAN}"\n“chat bubbles on screen”\n')
        self.assertIn(f"offset {len(CLEAN) + 3}", str(cm.exception))
        with self.assertRaises(package.CurlyQuotes):
            self.prompts(f'"{CLEAN}"\n“{CLEAN}”\n')

    def test_n01_a_run_nested_in_the_other_quote_style_is_a_curly_error_now(self):
        # A5 (a curly-quoted name inside a straight prompt), "straight-in-curly", "long curly
        # inner in straight" and the sub-floor curly label: each flipped extract-whole or
        # PromptBelowFloor→CurlyQuotes ERROR under Ruling 10 (curly quotes are not delimiters).
        # Containment now applies among straight runs only; a straight string nested in a
        # straight prompt is still covered by the depth rule (M01NestedQuotesTest).
        inner_curly = (f'{CLEAN} the “Aster Meridian” on her wrist, chat bubbles and a '
                       f'notification counter')
        with self.assertRaises(package.CurlyQuotes):
            self.prompts(f'"{inner_curly}"\n')
        inner_straight = (f'{CLEAN} the "Aster Meridian" on her wrist, chat bubbles and a '
                          f'notification counter')
        with self.assertRaises(package.CurlyQuotes):
            self.prompts(f'“{inner_straight}”\n')
        long_inner = f'{CLEAN} she reads “{CLEAN}” on the card, chat bubbles on screen'
        with self.assertRaises(package.CurlyQuotes):
            self.prompts(f'"{long_inner}"\n')
        with self.assertRaises(package.CurlyQuotes):
            self.prompts(f'"{inner_curly}"\n“Aster”\n')

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


class P01CurlyQuoteTest(unittest.TestCase):
    """Ruling 10 (P-01): a curly double quote anywhere in GENERATION_PROMPTS is an extraction
    error naming its offset — CurlyQuotes, "curly quote in GENERATION_PROMPTS — straight quotes
    delimit prompts; not scanned". Curly runs are no longer prompts; the check runs before the
    straight pairer so the outcome does not depend on the straight-quote state."""

    def prompts(self, section):
        return [p.text for p in package.extract_prompts(
            package.parse_package("GENERATION_PROMPTS\n" + section))]

    def assertCurlyError(self, section, name):
        with self.assertRaises(package.CurlyQuotes, msg=name) as cm:
            self.prompts(section)
        msg = str(cm.exception)
        self.assertIn(CURLY_ERROR, msg, name)
        first = min(i for i, ch in enumerate(section) if ch in (LQ, RQ))
        self.assertIn(f"offset {first}", msg, name)
        self.assertIsInstance(cm.exception, package.ExtractionError, name)
        return msg

    def test_p01_the_four_shapes_are_errors(self):
        # at HEAD 8902fb1 each extracted one clean prompt and PASSed with the dirty text unscanned
        for name, section in P01_SHAPES:
            with self.subTest(name):
                self.assertCurlyError(section, name)

    def test_p01_a_lone_curly_quote_of_either_kind_is_an_error(self):
        for name, section in (("lone opener", f'"{CLEAN}"\nsee {LQ}below\n'),
                              ("lone closer", f'"{CLEAN}"\nas above{RQ}\n'),
                              ("opener only, no straight run", f'{LQ}{CLEAN}\n'),
                              ("closer only, no straight run", f'{CLEAN}{RQ}\n')):
            with self.subTest(name):
                self.assertCurlyError(section, name)

    def test_p01_the_error_names_the_offset_and_the_quote(self):
        msg = self.assertCurlyError(f'"{CLEAN}"\n{LQ}{DIRTY}\n', "C4")
        self.assertIn(f"offset {len(CLEAN) + 3}", msg)
        self.assertIn(LQ, msg)
        msg = self.assertCurlyError(f'"{CLEAN}"\n{DIRTY}{RQ}\n', "closer")
        self.assertIn(f"offset {len(CLEAN) + 3 + len(DIRTY)}", msg)
        self.assertIn(RQ, msg)

    def test_p01_the_curly_check_comes_before_pairing(self):
        # a section that both carries a curly quote and fails to pair, or carries a sub-floor
        # straight run, reports the curly error whichever comes first in the text
        for name, section in (
                ("curly before an unclosed straight run", f'{LQ}{CLEAN}{RQ}\n"{CLEAN}\n'),
                ("unclosed straight run before curly", f'"{CLEAN}\n{LQ}{CLEAN}{RQ}\n'),
                ("orphan straight closer, then curly", f'"{CLEAN}"\nbubbles" {LQ}x{RQ}\n'),
                ("symbol-initial (M-01), then curly", f'"{CLEAN} {PRICES}"\n{LQ}{CLEAN}{RQ}\n'),
                ("sub-floor straight run, then curly", f'{K16_SHORT_SECOND_PROMPT}{LQ}{CLEAN}{RQ}\n'),
                ("curly, then sub-floor straight run", f'{LQ}{CLEAN}{RQ}\n{K16_SHORT_SECOND_PROMPT}')):
            with self.subTest(name):
                self.assertCurlyError(section, name)

    def test_p01_a_straight_only_section_is_untouched(self):
        self.assertEqual(self.prompts(f'"{CLEAN}"\n"{CLEAN} {NESTED}."\n'),
                         [CLEAN, f"{CLEAN} {NESTED}."])
        with self.assertRaises(package.UnbalancedQuotes):
            self.prompts(f'"{CLEAN}"\n"{CLEAN}\n')
        with self.assertRaises(package.PromptBelowFloor):
            self.prompts(K16_SHORT_SECOND_PROMPT)

    def test_p01_a_curly_quote_outside_generation_prompts_is_not_an_error(self):
        pkg = package.parse_package(
            f'DELIVERABLE\nthe {LQ}Aster{RQ} poster, 4:5\nGENERATION_PROMPTS\n"{CLEAN}"\n')
        self.assertEqual([p.text for p in package.extract_prompts(pkg)], [CLEAN])

    def test_p01_declared_aspect_survives_the_curly_error(self):
        pkg = package.parse_package(
            f'DELIVERABLE\none 4:5 poster\nGENERATION_PROMPTS\n{P01_SHAPES[0][1]}')
        self.assertEqual(package.declared_aspect(pkg), "4:5")
        pkg = package.parse_package(f'GENERATION_PROMPTS\n{P01_SHAPES[0][1]}')
        self.assertIsNone(package.declared_aspect(pkg))


class KnownHeadingsTest(unittest.TestCase):
    """Ruling 11: KNOWN_SECTION_HEADINGS is the frozen union of every section heading
    `parse_package` yields over the 84 committed EVAL-038 packages, recomputed here in place
    so the constant cannot drift — a heading added to or removed from the corpus, or the
    constant edited by hand, fails this test. Zero corpus change under the rule follows by
    construction, and the second test states it directly."""

    def test_the_frozen_set_equals_the_recomputed_union(self):
        files = committed_packages()
        self.assertEqual(len(files), 84)
        union = set()
        for path in files:
            union.update(package.parse_package(path.read_text(encoding="utf-8")).sections)
        self.assertEqual(package.KNOWN_SECTION_HEADINGS, tuple(sorted(union)))
        self.assertEqual(len(package.KNOWN_SECTION_HEADINGS), 15)
        self.assertIn("GENERATION_PROMPTS", package.KNOWN_SECTION_HEADINGS)
        self.assertIsInstance(package.KNOWN_SECTION_HEADINGS, tuple)

    def test_the_frozen_after_prompts_set_equals_the_recomputed_union(self):
        # Ruling 12: the union of every heading that follows the first GENERATION_PROMPTS
        # heading in at least one committed package, recomputed from SECTION_RE over the raw
        # text (repeats kept, so a repeat would count — none exists), a strict subset of the
        # full union: the seven pre-prompt schema sections and GENERATION_PROMPTS itself never
        # follow the prompts in any file
        files = committed_packages()
        self.assertEqual(len(files), 84)
        after = set()
        for path in files:
            headings = headings_in_order(path.read_text(encoding="utf-8"))
            after.update(headings[headings.index("GENERATION_PROMPTS") + 1:])
        self.assertEqual(package.KNOWN_HEADINGS_AFTER_PROMPTS, tuple(sorted(after)))
        self.assertEqual(len(package.KNOWN_HEADINGS_AFTER_PROMPTS), 7)
        self.assertIsInstance(package.KNOWN_HEADINGS_AFTER_PROMPTS, tuple)
        self.assertTrue(set(package.KNOWN_HEADINGS_AFTER_PROMPTS) < set(package.KNOWN_SECTION_HEADINGS))
        self.assertNotIn("GENERATION_PROMPTS", package.KNOWN_HEADINGS_AFTER_PROMPTS)
        self.assertEqual(set(AFTER_PROMPTS_SCHEMA_ORDER), set(package.KNOWN_HEADINGS_AFTER_PROMPTS))
        before_only = set(package.KNOWN_SECTION_HEADINGS) - set(package.KNOWN_HEADINGS_AFTER_PROMPTS)
        self.assertEqual(len(before_only), 8)
        self.assertIn("GENERATION_PROMPTS", before_only)

    def test_no_committed_package_carries_an_unknown_heading_after_the_prompts(self):
        # zero corpus change: every heading after GENERATION_PROMPTS in every committed
        # package is in the frozen after-prompts set (so in the full set), no heading repeats
        # anywhere in the file, so neither the Ruling 11 rule nor the Ruling 12 refinements
        # ever fire on it; `section_headings` (numbered or not) agrees with the walk here
        for path in committed_packages():
            text = path.read_text(encoding="utf-8")
            headings = headings_in_order(text)
            self.assertIn("GENERATION_PROMPTS", headings, path.name)
            after = headings[headings.index("GENERATION_PROMPTS") + 1:]
            self.assertTrue(after, path.name)
            self.assertTrue(set(after) <= set(package.KNOWN_HEADINGS_AFTER_PROMPTS), (path.name, after))
            self.assertTrue(set(after) <= set(package.KNOWN_SECTION_HEADINGS), (path.name, after))
            self.assertEqual(len(headings), len(set(headings)), path.name)
            self.assertEqual(package.section_headings(text), headings, path.name)
            numbered = package.section_headings(text, numbered=True)
            self.assertEqual([h for _, h in numbered], headings, path.name)
            lines = text.splitlines()
            for line_no, heading in numbered:
                self.assertEqual(package.SECTION_RE.match(lines[line_no - 1].strip()).group(1),
                                 heading, (path.name, line_no))
            self.assertEqual(headings, list(package.parse_package(text).sections), path.name)


class Q01UnknownHeadingTest(unittest.TestCase):
    """Ruling 11 (Q-01): a section heading outside KNOWN_SECTION_HEADINGS after
    GENERATION_PROMPTS has opened is an extraction error — UnknownSectionHeading,
    "unrecognised section heading after GENERATION_PROMPTS — prompts may be hidden; not
    scanned" — naming the heading. Parsing is untouched: the line still opens a section and
    SECTION_RE is the blinding tool's; extraction refuses the package instead of reading the
    first section alone. The check is section-level and runs before any quote is read."""

    def prompts(self, text):
        return [p.text for p in package.extract_prompts(package.parse_package(text))]

    def assertHeadingError(self, text, heading, name):
        with self.assertRaises(package.UnknownSectionHeading, msg=name) as cm:
            self.prompts(text)
        msg = str(cm.exception)
        self.assertIn(UNKNOWN_HEADING_ERROR, msg, name)
        self.assertIn(f"heading {heading!r}", msg, name)
        self.assertIsInstance(cm.exception, package.ExtractionError, name)
        return msg

    def test_q01_the_five_shapes_are_errors(self):
        # at HEAD 0c21d76 each parsed the ALL-CAPS line as a heading, extracted the clean
        # prompt alone and PASSed with the dirty text sitting in the new section, unscanned
        for name, section, heading in Q01_SHAPES:
            with self.subTest(name):
                pkg = package.parse_package("GENERATION_PROMPTS\n" + section)
                self.assertIn(heading, pkg.sections, name)   # parsing unchanged
                self.assertNotIn("chat bubbles", pkg.sections["GENERATION_PROMPTS"], name)
                self.assertIn("chat bubbles", pkg.sections[heading], name)
                self.assertHeadingError("GENERATION_PROMPTS\n" + section, heading, name)

    def test_q01_the_error_names_the_heading_and_its_line(self):
        head = f'## DELIVERABLE\none 4:5 poster\n## GENERATION_PROMPTS\n"{CLEAN}"\n'
        msg = self.assertHeadingError(head + f'IMPORTANT\n"{DIRTY}"\n', "IMPORTANT", "bare")
        self.assertIn("line 5", msg)
        msg = self.assertHeadingError(head + f'### PROMPT_B\n"{DIRTY}"\n', "PROMPT_B", "###")
        self.assertIn("line 5", msg)
        msg = self.assertHeadingError(head + f'"{CLEAN}"\nNOTE:\n"{DIRTY}"\n', "NOTE", "colon")
        self.assertIn("line 6", msg)

    def test_q01_the_heading_check_comes_before_quotes(self):
        # a section that also carries a curly quote, an unclosed run, an orphan closer or a
        # sub-floor run reports the heading: a section-level property, decided before the
        # quotes are read, so the outcome does not depend on the quote state
        for name, section in (
                ("curly prompt, then heading", f'{LQ}{CLEAN}{RQ}\nIMPORTANT\n"{DIRTY}"\n'),
                ("unclosed run, then heading", f'"{CLEAN}\nIMPORTANT\n"{DIRTY}"\n'),
                ("orphan closer, then heading", f'"{CLEAN}"\nbubbles" here\nIMPORTANT\n"{DIRTY}"\n'),
                ("sub-floor run, then heading", f'"x"\nIMPORTANT\n"{DIRTY}"\n'),
                ("heading, then curly in the new section", f'"{CLEAN}"\nIMPORTANT\n{LQ}{DIRTY}{RQ}\n'),
                ("heading, then nothing", f'"{CLEAN}"\nIMPORTANT\n')):
            with self.subTest(name):
                self.assertHeadingError("GENERATION_PROMPTS\n" + section, "IMPORTANT", name)

    def test_q01_every_after_prompts_heading_after_the_prompts_is_not_an_error(self):
        # counter-pin: each of the 7 after-prompts headings, in each heading style the parser
        # accepts, may follow the prompts section without tripping the rule. Under Ruling 11
        # this ran over the 14 other known headings; Ruling 12 narrowed the post-prompts set
        # to KNOWN_HEADINGS_AFTER_PROMPTS, and the 7 before-only headings are now the
        # after-set error (R01HeadingStructureTest)
        for heading in package.KNOWN_HEADINGS_AFTER_PROMPTS:
            self.assertNotEqual(heading, "GENERATION_PROMPTS")
            for style in ("{h}", "## {h}", "**{h}**", "{h}:", "### **{h}**:"):
                text = f'## GENERATION_PROMPTS\n"{CLEAN}"\n{style.format(h=heading)}\nprose\n'
                with self.subTest(heading=heading, style=style):
                    pkg = package.parse_package(text)
                    self.assertEqual(list(pkg.sections), ["GENERATION_PROMPTS", heading])
                    self.assertEqual(self.prompts(text), [CLEAN])

    def test_q01_a_known_heading_after_the_prompts_opens_a_genuine_section(self):
        # the ruled boundary, recorded: a known heading is schema, and what follows it belongs
        # to that section — it is not a prompt and is not scanned as one (a quoted run under
        # FAILURE_PREVENTION is that section's prose). Ruling 11 refuses unknown headings
        # only; Ruling 12 refuses headings the corpus never places after the prompts, and
        # repeats; a heading in KNOWN_HEADINGS_AFTER_PROMPTS, once, stays a genuine section
        # (the eighth checker's 3a-2; CANON-GATE-002 register, R-01 residual: closable only
        # by the production blueprint schema, Ruling 3). Documented, not tuned.
        text = f'## GENERATION_PROMPTS\n"{CLEAN}"\n## FAILURE_PREVENTION\n"{DIRTY}"\n'
        self.assertIn("FAILURE_PREVENTION", package.KNOWN_HEADINGS_AFTER_PROMPTS)
        self.assertEqual(self.prompts(text), [CLEAN])

    def test_q01_the_four_anchors_carry_known_headings_after_the_prompts_and_extract(self):
        for path, expected in ANCHOR_HEADINGS_AFTER_PROMPTS.items():
            with self.subTest(path.name):
                text = path.read_text()
                headings = headings_in_order(text)
                after = headings[headings.index("GENERATION_PROMPTS") + 1:]
                self.assertEqual(after, expected)
                self.assertTrue(set(after) <= set(package.KNOWN_SECTION_HEADINGS))
                self.assertTrue(set(after) <= set(package.KNOWN_HEADINGS_AFTER_PROMPTS))
                prompts = package.extract_prompts(package.parse_package(text))
                self.assertEqual(len(prompts), ANCHOR_PROMPT_COUNTS[path])
        # Gemma B02-R1 keeps its Ruling 7 outcome: the heading rule finds nothing, pairing raises
        with self.assertRaises(package.UnbalancedQuotes):
            package.extract_prompts(package.parse_package(GEMMA_B02.read_text()))

    def test_q01_an_unknown_heading_before_the_prompts_still_extracts(self):
        text = (f'## IMPORTANT\nread this first\n## DELIVERABLE\none 4:5 poster\n'
                f'## GENERATION_PROMPTS\n"{CLEAN}"\n## DOCTRINE_DEVIATIONS\nnone\n')
        pkg = package.parse_package(text)
        self.assertIn("IMPORTANT", pkg.sections)
        self.assertEqual(self.prompts(text), [CLEAN])
        # the same heading once more after the section has opened is the error, even though
        # `Package.sections` (keyed by name, first appearance) lists it before the prompts
        pkg = package.parse_package(text + f'## IMPORTANT\n"{DIRTY}"\n')
        self.assertEqual(list(pkg.sections)[0], "IMPORTANT")
        self.assertHeadingError(text + f'## IMPORTANT\n"{DIRTY}"\n', "IMPORTANT", "repeat")

    def test_q01_a_bare_heading_before_the_first_prompt_is_the_heading_error_now(self):
        # S6h: at HEAD 0c21d76 `VIDEO` right after the section opened moved the only prompt
        # into VIDEO and extraction returned no prompt (LIMIT-TEXT ERROR, "no generation
        # prompt"); still an ERROR, now naming the heading — nothing moved toward PASS
        self.assertHeadingError(f'GENERATION_PROMPTS\nVIDEO\n"{DIRTY}"\n', "VIDEO", "S6h")

    def test_q01_a_second_generation_prompts_heading_merges_as_today(self):
        # observed at HEAD 0c21d76 and left as it is by Ruling 11 condition 2 (the seventh
        # checker's S1): parse_package keys sections by name, so a second GENERATION_PROMPTS
        # heading appends its lines to the first section — both prompts extract and are
        # scanned. GENERATION_PROMPTS is in the known set, so the rule does not fire.
        text = (f'## GENERATION_PROMPTS\n"{CLEAN}"\n## DOCTRINE_DEVIATIONS\nnone\n'
                f'## GENERATION_PROMPTS\n"{DIRTY}"\n')
        pkg = package.parse_package(text)
        self.assertEqual(headings_in_order(text),
                         ["GENERATION_PROMPTS", "DOCTRINE_DEVIATIONS", "GENERATION_PROMPTS"])
        self.assertEqual(list(pkg.sections), ["GENERATION_PROMPTS", "DOCTRINE_DEVIATIONS"])
        self.assertEqual(pkg.sections["GENERATION_PROMPTS"], f'"{CLEAN}"\n"{DIRTY}"')
        self.assertEqual(self.prompts(text), [CLEAN, DIRTY])

    def test_q01_lines_that_are_not_headings_stay_in_the_section(self):
        for name, section in Q01_NOT_HEADINGS:
            with self.subTest(name):
                pkg = package.parse_package("GENERATION_PROMPTS\n" + section)
                self.assertEqual(list(pkg.sections), ["GENERATION_PROMPTS"])
                self.assertEqual(self.prompts("GENERATION_PROMPTS\n" + section), [CLEAN, DIRTY])

    def test_q01_no_prompts_section_still_yields_no_prompts(self):
        pkg = package.parse_package(f'DELIVERABLE\none\nIMPORTANT\n"{DIRTY}"\n')
        self.assertEqual(package.extract_prompts(pkg), [])

    def test_q01_section_headings_lists_every_heading_in_order_with_repeats(self):
        text = "## A_BC\nx\nVISUAL_SYSTEM:\n**DELIVERABLE**\n> NOT_ONE\n  ## A_BC\nabc\n"
        self.assertEqual(package.section_headings(text), ["A_BC", "VISUAL_SYSTEM", "DELIVERABLE", "A_BC"])
        self.assertEqual(package.section_headings(text), headings_in_order(text))
        self.assertEqual(package.section_headings(""), [])

    def test_q01_declared_aspect_survives_the_heading_error(self):
        pkg = package.parse_package(
            f'DELIVERABLE\none 4:5 poster\nGENERATION_PROMPTS\n{Q01_SHAPES[0][1]}')
        self.assertEqual(package.declared_aspect(pkg), "4:5")
        pkg = package.parse_package(f'GENERATION_PROMPTS\n{Q01_SHAPES[0][1]}')
        self.assertIsNone(package.declared_aspect(pkg))


class R01HeadingStructureTest(unittest.TestCase):
    """Ruling 12 (R-01, CONTROLLER-CANON-GATE-001-EIGHTH-CHECK-DISPOSITION-2026-09-07.md): two
    refinements of the Ruling 11 rule. A heading after the first GENERATION_PROMPTS that is in
    KNOWN_SECTION_HEADINGS but not in KNOWN_HEADINGS_AFTER_PROMPTS raises
    HeadingNotObservedAfterPrompts naming it and its line; a heading appearing more than once
    at or after the first GENERATION_PROMPTS line raises RepeatedSectionHeading naming it and
    both lines — except a second GENERATION_PROMPTS, exempt from both, which merges as
    recorded under Ruling 11. Precedence when more than one could fire: unrecognised (Ruling
    11) first, then not in the after-prompts set, then repeated — each rule over the whole
    heading list, naming its first offender in line order. Parsing is untouched."""

    def prompts(self, text):
        return [p.text for p in package.extract_prompts(package.parse_package(text))]

    def assertAfterSetError(self, text, heading, line, name):
        with self.assertRaises(package.HeadingNotObservedAfterPrompts, msg=name) as cm:
            self.prompts(text)
        msg = str(cm.exception)
        self.assertIn(AFTER_SET_ERROR, msg, name)
        self.assertIn(f"heading {heading!r} at line {line}", msg, name)
        self.assertIsInstance(cm.exception, package.ExtractionError, name)
        self.assertNotIsInstance(cm.exception, package.UnknownSectionHeading, name)
        return msg

    def assertRepeatError(self, text, heading, first, second, name):
        with self.assertRaises(package.RepeatedSectionHeading, msg=name) as cm:
            self.prompts(text)
        msg = str(cm.exception)
        self.assertIn(REPEAT_ERROR, msg, name)
        self.assertIn(f"heading {heading!r} at lines {first} and {second}", msg, name)
        self.assertIsInstance(cm.exception, package.ExtractionError, name)
        self.assertNotIsInstance(cm.exception, package.UnknownSectionHeading, name)
        return msg

    def test_r01_the_after_set_rows_are_errors(self):
        # at HEAD dbbe76f each extracted CLEAN alone and PASSed, the dirty run sitting in a
        # section the corpus never places after the prompts
        for name, text, heading, line in R01_AFTER_SET_SHAPES:
            with self.subTest(name):
                pkg = package.parse_package(text)
                self.assertNotIn("chat bubbles", pkg.sections["GENERATION_PROMPTS"], name)   # parsing unchanged
                self.assertIn(heading, package.KNOWN_SECTION_HEADINGS)
                self.assertNotIn(heading, package.KNOWN_HEADINGS_AFTER_PROMPTS)
                self.assertAfterSetError(text, heading, line, name)

    def test_r01_the_repeat_rows_are_errors(self):
        # at HEAD dbbe76f each extracted CLEAN alone and PASSed, the dirty run sitting between
        # two occurrences of a heading no committed package repeats
        for name, text, heading, first, second in R01_REPEAT_SHAPES:
            with self.subTest(name):
                pkg = package.parse_package(text)
                self.assertNotIn("chat bubbles", pkg.sections["GENERATION_PROMPTS"], name)
                self.assertIn(heading, package.KNOWN_HEADINGS_AFTER_PROMPTS)
                self.assertRepeatError(text, heading, first, second, name)

    def test_r01_every_before_only_heading_after_the_prompts_is_an_error(self):
        before_only = sorted(set(package.KNOWN_SECTION_HEADINGS)
                             - set(package.KNOWN_HEADINGS_AFTER_PROMPTS) - {"GENERATION_PROMPTS"})
        self.assertEqual(len(before_only), 7)
        for heading in before_only:
            for style in ("{h}", "## {h}", "**{h}**", "{h}:", "### **{h}**:"):
                text = f'## GENERATION_PROMPTS\n"{CLEAN}"\n{style.format(h=heading)}\n"{DIRTY}"\n'
                with self.subTest(heading=heading, style=style):
                    self.assertEqual(list(package.parse_package(text).sections),
                                     ["GENERATION_PROMPTS", heading])
                    self.assertAfterSetError(text, heading, 3, f"{heading} {style}")

    def test_r01_every_after_prompts_heading_once_in_schema_order_extracts(self):
        # counter-pin: all seven after-prompts headings, once each, in the corpus's order —
        # and each on its own
        text = f'## GENERATION_PROMPTS\n"{CLEAN}"\n' + "".join(
            f"## {h}\nprose\n" for h in AFTER_PROMPTS_SCHEMA_ORDER)
        self.assertEqual(headings_in_order(text)[1:], AFTER_PROMPTS_SCHEMA_ORDER)
        self.assertEqual(self.prompts(text), [CLEAN])
        for heading in package.KNOWN_HEADINGS_AFTER_PROMPTS:
            with self.subTest(heading):
                self.assertEqual(
                    self.prompts(f'## GENERATION_PROMPTS\n"{CLEAN}"\n## {heading}\nprose\n'), [CLEAN])

    def test_r01_the_four_anchors_after_prompts_headings_are_all_in_the_after_set(self):
        for path, expected in ANCHOR_HEADINGS_AFTER_PROMPTS.items():
            with self.subTest(path.name):
                text = path.read_text()
                headings = headings_in_order(text)
                after = headings[headings.index("GENERATION_PROMPTS") + 1:]
                self.assertEqual(after, expected)
                self.assertTrue(set(after) <= set(package.KNOWN_HEADINGS_AFTER_PROMPTS), after)
                self.assertEqual(len(headings), len(set(headings)))
                self.assertEqual(len(package.extract_prompts(package.parse_package(text))),
                                 ANCHOR_PROMPT_COUNTS[path])

    def test_r01_a_heading_once_before_and_never_after_still_extracts(self):
        # the wrapper itself carries VISUAL_SYSTEM and DELIVERABLE, both before-only, before
        # the prompts; so may CORE_CREATIVE_IDEA and PRODUCTION_RECIPE
        self.assertEqual(self.prompts(r01(f'"{CLEAN}"\n')), [CLEAN])
        text = "## CORE_CREATIVE_IDEA\nidea\n## PRODUCTION_RECIPE\nsteps\n" + r01(f'"{DIRTY}"\n')
        self.assertEqual(self.prompts(text), [DIRTY])

    def test_r01_a_second_generation_prompts_heading_still_merges(self):
        # the one exempt repeat: Ruling 11 condition 2 recorded the merge, Ruling 12 keeps it —
        # both prompts extract and are scanned, also after a known divider (the eighth
        # checker's 3a-5) and inside a run (3c-2); a third GENERATION_PROMPTS is exempt too
        text = r01(f'"{CLEAN}"\n## GENERATION_PROMPTS\n"{DIRTY}"\n')
        self.assertEqual(self.prompts(text), [CLEAN, DIRTY])
        text = r01(f'"{CLEAN}"\n## FAILURE_PREVENTION\nx\n## GENERATION_PROMPTS\n"{DIRTY}"\n')
        self.assertEqual(self.prompts(text), [CLEAN, DIRTY])
        text = r01(f'"{CLEAN}"\n"{DIRTY[:40]}\nGENERATION_PROMPTS\n{DIRTY[40:]}"\n')
        self.assertEqual(len(self.prompts(text)), 2)
        text = r01(f'"{CLEAN}"\n## GENERATION_PROMPTS\n"{DIRTY}"\n## GENERATION_PROMPTS\n"{CLEAN}"\n')
        self.assertEqual(self.prompts(text), [CLEAN, DIRTY, CLEAN])

    def test_r01_the_boundary_rows_extract_the_first_prompt_alone(self):
        # documented, not tuned — CANON-GATE-002 register, R-01 (residual), EIGHTH-CHECK-
        # DISPOSITION: a known post-prompts heading, once, with a quoted run or a blockquote
        # under it is content of that section by Ruling 11's own text; only the production
        # blueprint schema closes it. Each of these is the 3a-2 shape: every heading after
        # the prompts is in KNOWN_HEADINGS_AFTER_PROMPTS and appears once, so neither
        # refinement fires and the dirty text is that section's prose, not a prompt.
        for name, text in R01_BOUNDARY_SHAPES:
            with self.subTest(name):
                headings = headings_in_order(text)
                after = headings[headings.index("GENERATION_PROMPTS") + 1:]
                self.assertTrue(set(after) <= set(package.KNOWN_HEADINGS_AFTER_PROMPTS), after)
                self.assertEqual(len(after), len(set(after)), after)
                self.assertNotIn("chat bubbles", package.parse_package(text).sections["GENERATION_PROMPTS"])
                self.assertEqual(self.prompts(text), [CLEAN])

    def test_r01_precedence_unrecognised_then_after_set_then_repeat(self):
        gp = f'## GENERATION_PROMPTS\n"{CLEAN}"\n'
        # a before-only heading, then an unknown one: unrecognised wins although it comes later
        with self.assertRaises(package.UnknownSectionHeading) as cm:
            self.prompts(gp + f'## DELIVERABLE\nx\nIMPORTANT\n"{DIRTY}"\n')
        self.assertIn("heading 'IMPORTANT' at line 5", str(cm.exception))
        # a repeated after-set heading, then an unknown one: unrecognised wins
        with self.assertRaises(package.UnknownSectionHeading):
            self.prompts(gp + f'## FAILURE_PREVENTION\nx\n## FAILURE_PREVENTION\ny\nIMPORTANT\n"{DIRTY}"\n')
        # a repeated after-set heading, then a before-only one: the after-set message wins
        self.assertAfterSetError(
            gp + f'## FAILURE_PREVENTION\nx\n## FAILURE_PREVENTION\ny\n## DELIVERABLE\n"{DIRTY}"\n',
            "DELIVERABLE", 7, "repeat, then before-only")
        # a before-only heading repeated after the prompts: the after-set message, first line
        self.assertAfterSetError(gp + f'## DELIVERABLE\nx\n## DELIVERABLE\n"{DIRTY}"\n',
                                 "DELIVERABLE", 3, "before-only twice")
        # an unknown heading repeated after the prompts: unrecognised, first line (Ruling 11)
        with self.assertRaises(package.UnknownSectionHeading) as cm:
            self.prompts(gp + f'IMPORTANT\nx\nIMPORTANT\n"{DIRTY}"\n')
        self.assertIn("heading 'IMPORTANT' at line 3", str(cm.exception))
        # two after-set headings each repeated: the first second-occurrence in line order
        self.assertRepeatError(
            gp + f'## AUDIO_AND_EDIT\nx\n## FAILURE_PREVENTION\ny\n## AUDIO_AND_EDIT\nz\n'
                 f'## FAILURE_PREVENTION\n"{DIRTY}"\n', "AUDIO_AND_EDIT", 3, 7, "two repeats")
        # a heading three times names its first two lines
        self.assertRepeatError(
            gp + f'## AUDIO_AND_EDIT\nx\n## AUDIO_AND_EDIT\ny\n## AUDIO_AND_EDIT\n"{DIRTY}"\n',
            "AUDIO_AND_EDIT", 3, 5, "three")

    def test_r01_a_heading_before_the_prompts_does_not_count_as_a_repeat(self):
        # "at or after the first GENERATION_PROMPTS line": DELIVERABLE before the prompts and
        # once after is the after-set error, not a repeat; an after-set heading before the
        # prompts and once after is neither — nothing before the section opens is counted
        self.assertAfterSetError(r01(f'"{CLEAN}"\n## DELIVERABLE\n"{DIRTY}"\n'),
                                 "DELIVERABLE", 7, "before and after")
        text = "## FAILURE_PREVENTION\nearly\n" + r01(f'"{CLEAN}"\n## FAILURE_PREVENTION\nlate\n')
        self.assertEqual(self.prompts(text), [CLEAN])

    def test_r01_the_heading_checks_come_before_quotes(self):
        # section-level, decided before any quote is read: the outcome does not depend on
        # the quote state (a curly prompt, an unclosed run, a sub-floor run)
        for name, section in (
                ("curly prompt, then before-only heading", f'{LQ}{CLEAN}{RQ}\n## DELIVERABLE\n"{DIRTY}"\n'),
                ("unclosed run, then before-only heading", f'"{CLEAN}\n## DELIVERABLE\n"{DIRTY}"\n'),
                ("sub-floor run, then before-only heading", f'"x"\n## DELIVERABLE\n"{DIRTY}"\n')):
            with self.subTest(name):
                self.assertAfterSetError(r01(section), "DELIVERABLE", 7, name)
        for name, section in (
                ("curly prompt, then repeat",
                 f'{LQ}{CLEAN}{RQ}\n## FAILURE_PREVENTION\n"{DIRTY}"\n## FAILURE_PREVENTION\nx\n'),
                ("unclosed run, then repeat",
                 f'"{CLEAN}\n## FAILURE_PREVENTION\n"{DIRTY}"\n## FAILURE_PREVENTION\nx\n'),
                ("sub-floor run, then repeat",
                 f'"x"\n## FAILURE_PREVENTION\n"{DIRTY}"\n## FAILURE_PREVENTION\nx\n')):
            with self.subTest(name):
                self.assertRepeatError(r01(section), "FAILURE_PREVENTION", 7, 9, name)

    def test_r01_section_headings_numbered_is_the_same_walk(self):
        # R-02: `section_headings` is the production path's one line-walk; numbered, it
        # yields (line, heading) pairs over the same lines
        text = "## A_BC\nx\nVISUAL_SYSTEM:\n**DELIVERABLE**\n> NOT_ONE\n  ## A_BC\nabc\n"
        self.assertEqual(package.section_headings(text, numbered=True),
                         [(1, "A_BC"), (3, "VISUAL_SYSTEM"), (4, "DELIVERABLE"), (6, "A_BC")])
        self.assertEqual([h for _, h in package.section_headings(text, numbered=True)],
                         package.section_headings(text))
        self.assertEqual(package.section_headings("", numbered=True), [])

    def test_r01_declared_aspect_survives_the_new_errors(self):
        for name, text, *_ in (*R01_AFTER_SET_SHAPES, *R01_REPEAT_SHAPES):
            with self.subTest(name):
                self.assertEqual(package.declared_aspect(package.parse_package(text)), "9:16")


class N01NoSilentDiscardInvariantTest(unittest.TestCase):
    """Ruling 9 condition 1 as amended by Ruling 10 condition 2, Ruling 11 condition 5 and
    Ruling 12 condition 5, as a property over a set of sections: for any package with a
    GENERATION_PROMPTS section, if a heading outside KNOWN_SECTION_HEADINGS follows the
    section's opening `extract_prompts` raises UnknownSectionHeading naming it (a
    section-level property, checked before any quote); otherwise if a known heading outside
    KNOWN_HEADINGS_AFTER_PROMPTS (other than GENERATION_PROMPTS) follows it, extraction raises
    HeadingNotObservedAfterPrompts naming it; otherwise if any heading but GENERATION_PROMPTS
    recurs at or after the section's opening, extraction raises RepeatedSectionHeading naming
    it; otherwise if the section contains a curly double quote
    `extract_prompts` raises CurlyQuotes; otherwise either `_straight_runs` cannot pair it and
    extraction raises UnbalancedQuotes, or an outermost straight run is under the floor and
    extraction raises PromptBelowFloor naming it, or extraction succeeds and every outermost
    straight run is a prompt exactly, every nested run inside one. There is no eighth
    outcome: nothing quoted is ever silently discarded, and nothing after the section opens
    is read as a section the gate does not know, does not expect there, or has already seen.
    The straight spans are computed here from `_straight_runs` alone, independently of
    `_quoted_runs`; the headings from SECTION_RE alone (`headings_in_order`, its own line
    walk), independently of `section_headings` and of the production helper."""

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
            # the curly fixtures: each flipped FAIL / extract / PromptBelowFloor→CurlyQuotes
            # ERROR under Ruling 10 (curly quotes are not delimiters)
            ("curly short", f'"{CLEAN}"\n\u201cchat bubbles on screen\u201d\n'),
            ("A5 curly inner in straight", f'"{CLEAN} the \u201cAster Meridian\u201d on her wrist, '
                                           f'chat bubbles and a notification counter"\n'),
            ("straight inner in curly", f'\u201c{CLEAN} the "Aster Meridian" on her wrist, chat '
                                        f'bubbles and a notification counter\u201d\n'),
            ("long curly inner in straight",
             f'"{CLEAN} she reads \u201c{CLEAN}\u201d on the card, chat bubbles on screen"\n'),
            ("A4 curly outer, inch mark inside",
             f'\u201c{CLEAN} a 6" OLED panel showing chat bubbles and a notification counter\u201d\n'),
            *P01_SHAPES,
            ("curly, then unclosed straight run", f'{LQ}{CLEAN}{RQ}\n"{CLEAN}\n'),
            ("unclosed straight run, then curly", f'"{CLEAN}\n{LQ}{CLEAN}{RQ}\n'),
            # Ruling 11: the five Q-01 shapes, S6h, and unknown headings paired with each
            # quote state — every one the heading error; then the counter-shapes
            *[(name, section) for name, section, _ in Q01_SHAPES],
            ("S6h VIDEO before the first prompt", f'VIDEO\n"{DIRTY}"\n'),
            ("unknown heading after a curly prompt", f'{LQ}{CLEAN}{RQ}\nIMPORTANT\n"{DIRTY}"\n'),
            ("unknown heading after an unclosed run", f'"{CLEAN}\nIMPORTANT\n"{DIRTY}"\n'),
            ("unknown heading after a sub-floor run", f'"x"\nIMPORTANT\n"{DIRTY}"\n'),
            ("unknown heading, then curly", f'"{CLEAN}"\nIMPORTANT\n{LQ}{DIRTY}{RQ}\n'),
            ("known heading after the prompts", f'"{CLEAN}"\n## FAILURE_PREVENTION\nnone\n'),
            ("second GENERATION_PROMPTS heading", f'"{CLEAN}"\n## GENERATION_PROMPTS\n"{DIRTY}"\n'),
            *Q01_NOT_HEADINGS,
            # Ruling 12: the eighth checker's R-01 shapes — a before-only heading after the
            # prompts, a repeat — paired with each quote state, the precedence pairs, then
            # the boundary shapes and the counter-shapes
            ("3a-3 DELIVERABLE after the prompts", f'"{CLEAN}"\n## DELIVERABLE\n"{DIRTY}"\n'),
            ("3d-1 FINAL_PRODUCTION_PACKAGE bare divider",
             f'"{CLEAN}"\nFINAL_PRODUCTION_PACKAGE\n"{DIRTY}"\n'),
            ("3d-2 FINAL_PRODUCTION_PACKAGE, dirty blockquote",
             f'"{CLEAN}"\n## FINAL_PRODUCTION_PACKAGE\n> {DIRTY}\n'),
            ("3d-5 CORE_CREATIVE_IDEA after the prompts", f'"{CLEAN}"\n## CORE_CREATIVE_IDEA\n"{DIRTY}"\n'),
            ("before-only heading after a curly prompt", f'{LQ}{CLEAN}{RQ}\n## DELIVERABLE\n"{DIRTY}"\n'),
            ("before-only heading after an unclosed run", f'"{CLEAN}\n## DELIVERABLE\n"{DIRTY}"\n'),
            ("before-only heading after a sub-floor run", f'"x"\n## DELIVERABLE\n"{DIRTY}"\n'),
            ("before-only heading, then curly", f'"{CLEAN}"\n## DELIVERABLE\n{LQ}{DIRTY}{RQ}\n'),
            ("3a-1 FAILURE_PREVENTION repeated",
             f'"{CLEAN}"\n## FAILURE_PREVENTION\n"{DIRTY}"\n## FAILURE_PREVENTION\nreal\n'),
            ("3d-3 DOCTRINE_DEVIATIONS repeated",
             f'"{CLEAN}"\n## DOCTRINE_DEVIATIONS\n"{DIRTY}"\n## DOCTRINE_DEVIATIONS\nnone\n'),
            ("repeat after a curly prompt",
             f'{LQ}{CLEAN}{RQ}\n## FAILURE_PREVENTION\n"{DIRTY}"\n## FAILURE_PREVENTION\nx\n'),
            ("repeat after an unclosed run",
             f'"{CLEAN}\n## FAILURE_PREVENTION\n"{DIRTY}"\n## FAILURE_PREVENTION\nx\n'),
            ("repeat after a sub-floor run",
             f'"x"\n## FAILURE_PREVENTION\n"{DIRTY}"\n## FAILURE_PREVENTION\nx\n'),
            ("repeat, then curly", f'"{CLEAN}"\n## FAILURE_PREVENTION\nx\n## FAILURE_PREVENTION\n{LQ}{DIRTY}{RQ}\n'),
            ("before-only, then unknown", f'"{CLEAN}"\n## DELIVERABLE\nx\nIMPORTANT\n"{DIRTY}"\n'),
            ("repeat, then unknown",
             f'"{CLEAN}"\n## FAILURE_PREVENTION\nx\n## FAILURE_PREVENTION\ny\nIMPORTANT\n"{DIRTY}"\n'),
            ("repeat, then before-only",
             f'"{CLEAN}"\n## FAILURE_PREVENTION\nx\n## FAILURE_PREVENTION\ny\n## DELIVERABLE\n"{DIRTY}"\n'),
            ("before-only repeated", f'"{CLEAN}"\n## DELIVERABLE\nx\n## DELIVERABLE\n"{DIRTY}"\n'),
            ("3a-2 known divider (boundary)", f'"{CLEAN}"\n## FAILURE_PREVENTION\n"{DIRTY}"\n'),
            ("3a-4 known divider, dirty blockquote (boundary)", f'"{CLEAN}"\n## FAILURE_PREVENTION\n> {DIRTY}\n'),
            ("3a-6 AUDIO_AND_EDIT bare divider (boundary)", f'"{CLEAN}"\nAUDIO_AND_EDIT\n"{DIRTY}"\n'),
            ("3a-8 known divider, ordinary tail (boundary)",
             f'"{CLEAN}"\n## FAILURE_PREVENTION\n"{DIRTY}"\n## HARD_CONSTRAINT_CHECK\nok\n'),
            ("3a-5 known divider, second GENERATION_PROMPTS",
             f'"{CLEAN}"\n## FAILURE_PREVENTION\nx\n## GENERATION_PROMPTS\n"{DIRTY}"\n'),
            ("all seven after-prompts headings in schema order",
             f'"{CLEAN}"\n' + "".join(f"## {h}\nprose\n" for h in AFTER_PROMPTS_SCHEMA_ORDER)),
        ]
        for name, section in synthetic:
            out.append((name, package.parse_package("GENERATION_PROMPTS\n" + section)))
        return out

    @staticmethod
    def spans(section):
        """Every straight-quoted run of the section as (start, end, body), from
        `_straight_runs` alone (raises UnbalancedQuotes); `end` is the offset of the closing
        quote. Curly quotes are not runs (Ruling 10) and are handled before this is called."""
        runs = list(package._straight_runs(section))
        return sorted((s, s + 1 + len(b), b) for s, b in runs)

    def test_every_quoted_run_is_extracted_or_the_section_errors(self):
        cases = self.sections()
        self.assertGreaterEqual(len(cases), 60)
        outcomes = {"heading": 0, "after_set": 0, "repeat": 0, "curly": 0, "unbalanced": 0,
                    "floor": 0, "extracted": 0}
        for name, pkg in cases:
            with self.subTest(name):
                headings = headings_in_order(pkg.text)
                after = headings[headings.index("GENERATION_PROMPTS") + 1:]
                unknown = [h for h in after if h not in package.KNOWN_SECTION_HEADINGS]
                if unknown:
                    # exactly one admitted outcome: the heading error, naming the first
                    # unknown heading, whatever the section's quotes would do — the check
                    # is section-level and precedes every quote rule
                    with self.assertRaises(package.UnknownSectionHeading) as cm:
                        package.extract_prompts(pkg)
                    self.assertIn(UNKNOWN_HEADING_ERROR, str(cm.exception), name)
                    self.assertIn(f"heading {unknown[0]!r}", str(cm.exception), name)
                    outcomes["heading"] += 1
                    continue
                not_after = [h for h in after if h != "GENERATION_PROMPTS"
                             and h not in package.KNOWN_HEADINGS_AFTER_PROMPTS]
                if not_after:
                    # Ruling 12 refinement 1 — exactly one admitted outcome: the after-set
                    # error, naming the first known heading the corpus never places after
                    # the prompts, whatever the section's quotes would do
                    with self.assertRaises(package.HeadingNotObservedAfterPrompts) as cm:
                        package.extract_prompts(pkg)
                    self.assertIn(AFTER_SET_ERROR, str(cm.exception), name)
                    self.assertIn(f"heading {not_after[0]!r}", str(cm.exception), name)
                    outcomes["after_set"] += 1
                    continue
                at_or_after = headings[headings.index("GENERATION_PROMPTS"):]
                repeated = [h for i, h in enumerate(at_or_after)
                            if h != "GENERATION_PROMPTS" and h in at_or_after[:i]]
                if repeated:
                    # Ruling 12 refinement 2 — exactly one admitted outcome: the repeat
                    # error, naming the first heading seen a second time (a second
                    # GENERATION_PROMPTS is exempt and merges)
                    with self.assertRaises(package.RepeatedSectionHeading) as cm:
                        package.extract_prompts(pkg)
                    self.assertIn(REPEAT_ERROR, str(cm.exception), name)
                    self.assertIn(f"heading {repeated[0]!r}", str(cm.exception), name)
                    outcomes["repeat"] += 1
                    continue
                section = pkg.sections["GENERATION_PROMPTS"]
                curly = [i for i, ch in enumerate(section) if ch in (LQ, RQ)]
                if curly:
                    # exactly one admitted outcome: the curly error, naming the first curly
                    # quote's offset, whatever the straight quotes around it would do
                    with self.assertRaises(package.CurlyQuotes) as cm:
                        package.extract_prompts(pkg)
                    self.assertIn(CURLY_ERROR, str(cm.exception), name)
                    self.assertIn(f"offset {curly[0]}", str(cm.exception), name)
                    outcomes["curly"] += 1
                    continue
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
        # the set exercises all seven admitted outcomes at least once
        self.assertTrue(all(outcomes.values()), outcomes)
        self.assertGreaterEqual(outcomes["heading"], 10, outcomes)
        self.assertGreaterEqual(outcomes["after_set"], 8, outcomes)
        self.assertGreaterEqual(outcomes["repeat"], 6, outcomes)


if __name__ == "__main__":
    unittest.main()
