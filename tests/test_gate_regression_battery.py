"""Regression battery (CANON-GATE-001 Ruling 6 condition 7): one table of phrase → check →
intended outcome, run as a single battery so a checker can diff intended against observed
mechanically.

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

Rows cover the second checker's K-01, K-02, K-03, K-05, K-06 phrases, the first checker's
F-02 (10), F-03 (15 + the existing HITs), F-04 (the two clock-time insertions), F-05 (the
junk VISUAL_SYSTEM, "Soft window light.", "the key is the product itself, shown from the
front", "brighter neutral daylight balance") and F-07 phrases, the K-04 narrowed-term
fixtures, the EVAL-038 defect phrases ("chat bubbles", "notification counter"), and the
third checker's L-01 shapes (the Gemma B02-R1 `"₹9" (massive …)` idiom read in place, the six
tails after a digit-ending closer, the end-of-line closer, an unclosed run), and the fourth
checker's M-01/M-02 shapes (a nested straight-quoted string with a text-bearing tail, the
symbol-initial price strings, a doubt point followed by a symbol-initial or space-led quote).

Each row is (finding, check, phrase, intended). Checks:
  T-scan      textscan.scan_prompt over the phrase              → HIT | CLEAR
  CA-D2       the phrase appended to Sonnet B06's VISUAL_SYSTEM  → PASS | FAIL
  PA-D4       the phrase as a synthetic implied_light_source     → PASS | FAIL
  CA-D5       the phrase as a synthetic VISUAL_SYSTEM            → PASS | FAIL
  CA-D6       the phrase prepended to Sonnet B06's DELIVERABLE,
              with the committed dispatch                        → PASS (4:5 stated,
                                                                   DISPATCH-ASPECT PASS,
                                                                   verdict PASS) | FAIL
  LIMIT-TEXT  the phrase as the only quoted generation prompt of
              a synthetic package                                → PASS | FAIL | ERROR
  LIMIT-TEXT raw  the phrase is the whole GENERATION_PROMPTS
              section of a synthetic video package, verbatim     → PASS | FAIL | ERROR
  LIMIT-TEXT pkg  the phrase names a committed EVAL-038 package
              (relative to eval/experiments/EVAL-038), read in
              place                                              → PASS | FAIL | ERROR

Run: python3 -m unittest tests.test_gate_regression_battery
Table: python3 -m tests.test_gate_regression_battery --table   (prints every row with the
       observed outcome and exits 1 on any mismatch)
"""
import sys
import unittest
from pathlib import Path

from canon.gate import doctrine, findings, predispatch, textscan

REPO_ROOT = Path(__file__).resolve().parents[1]
E38 = REPO_ROOT / "eval/experiments/EVAL-038"
SONNET_B06 = E38 / "baseline/sonnet-no-canon/E037-sonnet-no-canon-B06-R1.txt"
MEDIA = E38 / "media"
S = findings.Status
PLATE = "A matte plate, no text. " * 8   # the synthetic prompt: 192 chars, no hit

JUNK_VISUAL_SYSTEM = ("balance, key light from the side, center, brushed.\n"
                      "1. a\n2. b\n3. c\nglass, highlight.")
PROMPT_LEAD = ("Vertical 9:16, a young man at a desk in a cramped PG office, harsh "
               "tube-light. ")
# L-01 (Ruling 7): a clean prompt, a text-bearing prompt ending in a digit, the six tails
CLEAN = PLATE.strip()
DIRTY = ("Vertical 9:16, a smartphone screen filling with WhatsApp rent-reminder chat bubbles "
         "and a notification counter climbing past 99")
TAILS = (" (8 s)", " — 4 s", " | 4 s |", ". Then the next shot.", " 8 s", " then the next shot")
# M-01 / M-02 (Ruling 8): a nested straight-quoted string with a text-bearing tail (the
# fourth checker's A1/A2/A3), and the symbol-initial price strings
NESTED = ('A model showing the "Aster Meridian" on her wrist, chat bubbles and a notification '
          'counter on screen')
PRICES = 'she holds "₹9" and "₹99" in gold, chat bubbles and a notification counter on screen'
PRICES3 = ('she holds "₹9" and "₹99" and "₹999" in gold, chat bubbles and a notification '
           'counter on screen')
DOUBT_THEN_SPACE_LED = f'{CLEAN} 6" then " chat bubbles and a notification counter past 99'

# (finding, check, phrase, intended)
ROWS = [
    # ── K-01 / F-07: CA-D2 clause 2 negation window (6 tokens before + disclaimer after) ──
    ("K-01", "CA-D2", "Without clutter, the watch sits on the golden ratio point.", "FAIL"),
    ("K-01", "CA-D2", "No hard shadows, dial placed on the rule of thirds line.", "FAIL"),
    ("K-01", "CA-D2", "Not too tight, the crown sits at the intersection of the thirds.", "FAIL"),
    ("F-07", "CA-D2", "We will not compose this using the rule of thirds.", "PASS"),
    ("F-07", "CA-D2", "Avoid any reliance on the classic rule of thirds.", "PASS"),
    ("F-07", "CA-D2", "The rule of thirds is not used here.", "PASS"),
    ("F-07", "CA-D2", "Not the rule of thirds.", "PASS"),
    ("F-07", "CA-D2", "The golden ratio is deliberately avoided here.", "PASS"),
    ("F-07", "CA-D2", "Placement by zone, not the rule of thirds.", "PASS"),
    ("F-07", "CA-D2", "Rule of thirds, no exceptions.", "FAIL"),
    ("F-07", "CA-D2", "Dial on the rule of thirds line, not centred.", "FAIL"),
    ("F-07", "CA-D2", "Placement follows the golden ratio.", "FAIL"),
    # ── K-03: T3 negation must govern the surface ──
    ("K-03", "T-scan", "Avoid cluttering the dashboard", "HIT"),
    ("K-03", "T-scan", "never crowded, the poster on the wall", "HIT"),
    ("K-03", "T-scan", "A tidy, not busy, receipt on the table", "HIT"),
    ("K-03", "T-scan", "zero clutter around the invoice", "HIT"),
    ("K-03", "T-scan", "no chat bubbles", "CLEAR"),
    ("K-03", "T-scan", "not a dashboard", "CLEAR"),
    ("K-03", "T-scan", "without any visible dashboard", "CLEAR"),
    ("K-03", "T-scan", "a plate free of labels", "CLEAR"),
    ("K-03 recorded over-fire", "T-scan", "no glowing notifications", "HIT"),
    ("K-03 recorded over-fire", "T-scan", "avoid showing the receipt", "HIT"),
    # ── F-02: false FAILs that must clear ──
    ("F-02", "T-scan", "A tidy desk, no secondary messages.", "CLEAR"),
    ("F-02", "T-scan", "Two friends in conversation over chai.", "CLEAR"),
    ("F-02", "T-scan", "A warm banner of cloud over the ridge.", "CLEAR"),
    ("F-02", "T-scan", "A menu of soft greens in the foliage.", "CLEAR"),
    ("F-02", "T-scan", "Hands rest on the counter of the kitchen island.", "CLEAR"),
    ("F-02", "T-scan", "A thumb pressing the crown button.", "CLEAR"),
    ("F-02", "T-scan", "The user interface is not visible; screen off.", "CLEAR"),
    ("F-02", "T-scan", "A model showing the 'Aster Meridian 38' on her wrist, no text anywhere.",
     "CLEAR"),
    ("F-02", "T-scan", "A phone face down, no chat bubbles, no notifications visible.", "CLEAR"),
    ("F-02", "T-scan", "Clean walls, no visible signage.", "CLEAR"),
    ("F-02", "T-scan", "The phone screen shows a notification alert: 'Tenant Complaint Pending'.",
     "HIT"),
    ("F-02", "T-scan", "Cut to him tapping a 'Verify KYC' button on the same app.", "HIT"),
    # ── F-03: false PASSes that must hit ──
    ("F-03", "T-scan", "elegant text on the dial", "HIT"),
    ("F-03", "T-scan", "add text across the top third", "HIT"),
    ("F-03", "T-scan", "the word RENT in bold red letters", "HIT"),
    ("F-03", "T-scan", "the dial shows the model name below 12 o'clock", "HIT"),
    ("F-03", "T-scan", "caseback engraved with the model name", "HIT"),
    ("F-03", "T-scan", "a label that says Aster", "HIT"),
    ("F-03", "T-scan", "a placard with the words Save Time", "HIT"),
    ("F-03", "T-scan", "a wall clock with clear numerals", "HIT"),
    ("F-03", "T-scan", "a calendar with dates circled", "HIT"),
    ("F-03", "T-scan", "license plate clearly visible", "HIT"),
    ("F-03", "T-scan", "a nameplate bearing the manager's name", "HIT"),
    ("F-03", "T-scan", "the phone number 98765 43210 painted across the shutter", "HIT"),
    ("F-03", "T-scan", "a billboard with the URL www.rentok.com", "HIT"),
    ("F-03", "T-scan", "written in Hindi on the wall", "HIT"),
    ("F-03", "T-scan", "a t-shirt with a slogan", "HIT"),
    ("F-03", "T-scan", "a sign reads OPEN", "HIT"),
    ("F-03", "T-scan", "storefront lettering", "HIT"),
    ("F-03", "T-scan", "a tagline underneath", "HIT"),
    ("F-03", "T-scan", "a shop sign in Devanagari script", "HIT"),
    ("F-03", "T-scan", "no text on the dial", "CLEAR"),
    ("F-03", "T-scan", "a plate free of text", "CLEAR"),
    ("F-03", "T-scan", "no numerals, baton markers", "CLEAR"),
    ("F-03", "T-scan", "no license plate in frame", "CLEAR"),
    ("F-03", "T-scan", "a blank label", "CLEAR"),
    ("F-03", "T-scan", "text on the plate is added in post", "CLEAR"),
    ("F-03", "T-scan", "a bag with no slogan", "CLEAR"),
    ("F-03", "T-scan", "signs of wear on the strap", "CLEAR"),
    # ── K-06: the F-03 additions must not fire on watch copy ──
    ("K-06", "T-scan", "Arabic numerals at 12, 3, 6 and 9 on the dial", "CLEAR"),
    ("K-06", "T-scan", "the date digits at 3 o'clock", "CLEAR"),
    ("K-06", "T-scan", "Roman numerals, no other markings", "CLEAR"),
    ("K-06", "T-scan", "a label-free bottle", "CLEAR"),
    ("K-06", "T-scan", "a quiet storefront at dusk, shutters down", "CLEAR"),
    ("K-06", "T-scan", "a storefront sign in Devanagari script", "HIT"),
    ("K-06", "T-scan", "large printed digits on the scoreboard", "HIT"),
    ("K-06 recorded miss", "T-scan", "a wall clock with Roman numerals", "CLEAR"),
    ("K-06 recorded miss", "T-scan", "a busy storefront", "CLEAR"),
    # ── plan §D windows (first-pass fixtures) ──
    ("§D T2 window", "T-scan", "A clean plate, no logo, no watermark.", "CLEAR"),
    ("§D T2 window", "T-scan", "A clean plate without any visible headline.", "CLEAR"),
    ("§D T2 window", "T-scan", "A clean plate with a bold headline.", "HIT"),
    ("§D T2 window", "T-scan", "No clutter, a bright bold tagline.", "HIT"),
    ("§D deferral", "T-scan", "Logo animates in, tagline and CTA text to be added in post.", "CLEAR"),
    # ── EVAL-038 defect phrases (the row that caught 3 of 5 artifacts) ──
    ("EVAL-038", "T-scan", "chat bubbles", "HIT"),
    ("EVAL-038", "T-scan", "notification counter", "HIT"),
    ("EVAL-038", "T-scan", "Extreme close-up of a smartphone screen filling with a rapid stack "
                           "of WhatsApp rent-reminder chat bubbles and a notification counter "
                           "climbing past 99.", "HIT"),
    # ── K-02 / K-05: extraction reaches LIMIT-TEXT ──
    ("K-02", "LIMIT-TEXT", PLATE, "PASS"),
    ("K-02", "LIMIT-TEXT", " " + PLATE.strip(), "PASS"),
    ("K-05", "LIMIT-TEXT",
     PROMPT_LEAD + 'A 6" OLED panel showing chat bubbles and a notification counter.', "FAIL"),
    ("K-05", "LIMIT-TEXT",
     PROMPT_LEAD + 'The panel is 6". It shows chat bubbles and a notification counter.', "FAIL"),
    # ── F-04: a clock time in the deliverable is not an aspect ──
    ("F-04", "CA-D6", "Hands set to 10:10 as convention. ", "PASS"),
    ("F-04", "CA-D6", "The logo holds for the last 0:03. ", "PASS"),
    # ── F-05: bare presence terms narrowed ──
    ("F-05", "CA-D5", JUNK_VISUAL_SYSTEM, "FAIL"),
    ("F-05", "PA-D4", "Soft window light.", "FAIL"),
    ("F-05", "PA-D4", "the key is the product itself, shown from the front", "FAIL"),
    ("F-05", "CA-D5", "brighter neutral daylight balance; brushed case; centre zone.", "FAIL"),
    ("F-05", "CA-D5", "the frame is balanced; brushed case; centre zone.", "PASS"),
    ("F-05", "CA-D5", "compositional balance holds; brushed case; centre zone.", "PASS"),
    ("F-05", "CA-D5", "deliberately unbalanced and restless; brushed case; centre zone.", "PASS"),
    ("F-05", "CA-D5", "an off-balance frame; brushed case; centre zone.", "PASS"),
    # ── K-04: each narrowed bare term, failing direction and narrowed form ──
    ("K-04 fill", "PA-D4", "the fill of the frame is the watch itself, shown from upper left", "FAIL"),
    ("K-04 side", "PA-D4", "key light kept soft, crown on the right side of the case", "FAIL"),
    ("K-04 behind", "PA-D4", "key light kept soft, the strap tucked behind the case", "FAIL"),
    ("K-04 °", "PA-D4", "key light kept soft, dial tilted 5° toward camera", "FAIL"),
    ("K-04 fill", "PA-D4", "gentle fill from the left", "PASS"),
    ("K-04 side", "PA-D4", "key light kept soft, side-lit from camera-left", "PASS"),
    ("K-04 behind", "PA-D4", "key light from behind the watch", "PASS"),
    ("K-04 °", "PA-D4", "key light at 45° above horizontal", "PASS"),
    ("K-04 °", "PA-D4", "key light 45 degrees camera-left", "PASS"),
    ("K-04 window", "PA-D4", "Soft window light from the left", "PASS"),
    ("K-04 key/front", "PA-D4", "soft key from the front", "PASS"),
    # ── L-01 / Ruling 7: a quote run the gate cannot pair fails closed ──
    ("L-01 Gemma B02-R1", "LIMIT-TEXT pkg",
     "runs/gemma-packs/packages/E038-gemma-packs-B02-R1.txt", "ERROR"),
    ("L-01 EOL closer", "LIMIT-TEXT raw", f'"{CLEAN}"\n"{DIRTY}"\n', "FAIL"),
    ("L-01 bracket closer", "LIMIT-TEXT raw", f'"{CLEAN}"\n"{DIRTY}")\n"{CLEAN}"\n', "FAIL"),
    ("L-01 unclosed run", "LIMIT-TEXT raw", f'"{CLEAN}"\n"{CLEAN}\n', "ERROR"),
    *[("L-01 tail, last", "LIMIT-TEXT raw", f'"{CLEAN}"\n"{DIRTY}"{tail}\n', "ERROR")
      for tail in TAILS],
    *[("L-01 tail, then prompt", "LIMIT-TEXT raw", f'"{CLEAN}"\n"{DIRTY}"{tail}\n"{CLEAN}"\n',
       "ERROR") for tail in TAILS],
    # ── M-01 / M-02 / Ruling 8: a nested string never closes the prompt at its inner closer ──
    ("M-01 A1 nested string", "LIMIT-TEXT raw", f'"{CLEAN} {NESTED}"\n', "FAIL"),
    ("M-01 A2 nested, then prompt", "LIMIT-TEXT raw", f'"{CLEAN} {NESTED}."\n"{CLEAN}"\n', "FAIL"),
    ("M-01 A3 nested, last", "LIMIT-TEXT raw", f'"{CLEAN} {NESTED}."\n', "FAIL"),
    ("M-01 symbol-initial", "LIMIT-TEXT raw", f'"{CLEAN} {PRICES}"\n', "ERROR"),
    ("M-02 symbol-initial x3", "LIMIT-TEXT raw", f'"{CLEAN} {PRICES3}"\n', "ERROR"),
    ("M-02 doubt, then symbol", "LIMIT-TEXT raw", f'"{CLEAN} 6" then "₹9" and chat bubbles past 99"\n',
     "ERROR"),
    ("M-02 doubt, then space-led", "LIMIT-TEXT raw", f'"{DOUBT_THEN_SPACE_LED}"\n', "ERROR"),
]


class Observer:
    """Runs one row against the gate and returns the observed outcome as a string."""

    def __init__(self):
        self.reg = doctrine.load_registry()
        self.sonnet_b06 = SONNET_B06.read_text()
        import json
        self.b06_dispatch = json.loads(
            (MEDIA / "E038-media-B06-sonnet-no-canon.request.json").read_text())

    def _run(self, text, modality="static_image", product=True, dispatch=None):
        return predispatch.run_predispatch(text, None, dispatch, modality, product, self.reg,
                                           label="battery")

    @staticmethod
    def _row(report, check_id):
        return {r.check_id: r for r in report.results}[check_id]

    @staticmethod
    def _name(status):
        return getattr(status, "name", str(status))

    def _synthetic(self, visual_system, prompt=PLATE, deliverable="one 4:5 image",
                   modality="static_image", product=True):
        pkg = ("## VISUAL_SYSTEM\n" + visual_system + "\n## DELIVERABLE\n" + deliverable
               + "\n## GENERATION_PROMPTS\n\"" + prompt + "\"\n## DOCTRINE_DEVIATIONS\nnone\n")
        return self._run(pkg, modality, product)

    def observe(self, check, phrase):
        if check == "T-scan":
            return "HIT" if textscan.scan_prompt(phrase).hits else "CLEAR"
        if check == "CA-D2":
            text = self.sonnet_b06.replace("Aspect ratio: 4:5, vertical.",
                                           f"Aspect ratio: 4:5, vertical. {phrase}")
            assert text != self.sonnet_b06
            return self._name(self._row(self._run(text), "CA-D2-check").status)
        if check == "PA-D4":
            r = self._synthetic("**implied_light_source:**\n" + phrase + "\n")
            return self._name(self._row(r, "PA-D4-check").status)
        if check == "CA-D5":
            r = self._synthetic(phrase)
            return self._name(self._row(r, "CA-D5-check").status)
        if check == "CA-D6":
            text = self.sonnet_b06.replace("One premium, commercially usable",
                                           phrase + "One premium, commercially usable")
            assert text != self.sonnet_b06
            r = self._run(text, dispatch=self.b06_dispatch)
            ok = ("aspect stated: 4:5" in self._row(r, "CA-D6-check").detail
                  and self._row(r, "DISPATCH-ASPECT").status is S.PASS
                  and r.verdict() == "PASS")
            return "PASS" if ok else "FAIL"
        if check == "LIMIT-TEXT":
            r = self._synthetic("key light from upper-left; centre zone", prompt=phrase,
                                deliverable="one 9:16 video", modality="video", product=False)
            return self._name(self._row(r, "LIMIT-TEXT").status)
        if check == "LIMIT-TEXT raw":
            pkg = ("## VISUAL_SYSTEM\nkey light from upper-left; centre zone\n## DELIVERABLE\n"
                   "one 9:16 video\n## GENERATION_PROMPTS\n" + phrase
                   + "## DOCTRINE_DEVIATIONS\nnone\n")
            return self._name(self._row(self._run(pkg, "video", False), "LIMIT-TEXT").status)
        if check == "LIMIT-TEXT pkg":
            r = self._run((E38 / phrase).read_text())
            return self._name(self._row(r, "LIMIT-TEXT").status)
        raise ValueError(check)


def observe_all(observer=None):
    """[(finding, check, phrase, intended, observed)] for every row, in table order."""
    observer = observer or Observer()
    return [(f, c, p, i, observer.observe(c, p)) for f, c, p, i in ROWS]


def render(results) -> str:
    lines = [f"{'ok':2} | {'finding':24} | {'check':14} | {'intended':8} | {'observed':8} | phrase"]
    for f, c, p, i, o in results:
        shown = p.replace("\n", "⏎")
        shown = shown if len(shown) <= 72 else shown[:69] + "…"
        lines.append(f"{'ok' if i == o else 'XX':2} | {f:24} | {c:14} | {i:8} | {o:8} | {shown}")
    return "\n".join(lines)


class RegressionBatteryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = observe_all()

    def test_table_is_well_formed(self):
        self.assertGreaterEqual(len(ROWS), 100)
        self.assertEqual(len({(c, p) for _, c, p, _ in ROWS}), len(ROWS), "duplicate row")
        for f, c, p, i in ROWS:
            self.assertIn(c, ("T-scan", "CA-D2", "PA-D4", "CA-D5", "CA-D6", "LIMIT-TEXT",
                              "LIMIT-TEXT raw", "LIMIT-TEXT pkg"), f)
            self.assertIn(i, ("HIT", "CLEAR", "PASS", "FAIL", "ERROR"), f)

    def test_every_row_individually(self):
        for f, c, p, i, o in self.results:
            with self.subTest(finding=f, check=c, phrase=p):
                self.assertEqual(o, i)

    def test_intended_equals_observed_for_the_whole_battery(self):
        mismatches = [r for r in self.results if r[3] != r[4]]
        self.assertEqual(mismatches, [], "\n" + render(mismatches))


if __name__ == "__main__":
    if "--table" in sys.argv:
        results = observe_all()
        print(render(results))
        bad = sum(1 for r in results if r[3] != r[4])
        print(f"\n{len(results)} rows, {bad} mismatch(es)")
        sys.exit(1 if bad else 0)
    unittest.main()
