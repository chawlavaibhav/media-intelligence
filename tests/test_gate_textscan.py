"""Baked-text scan and detector adapters (CANON-GATE-001 plan §D, §B textscan.py, §F).

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

LIMIT-TEXT is sourced from the verbatim pack limit line (Ruling 1). Fixtures are the four
committed dispatched prompts under eval/experiments/EVAL-038/media/prompts/, read in place.
The Cloud Vision adapter is wired and never invoked: the default transport refuses before
any socket and this file asserts it. Run: python3 -m unittest tests.test_gate_textscan
"""
import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

from canon.gate import doctrine, findings, predispatch, textscan

REPO_ROOT = Path(__file__).resolve().parents[1]
E38 = REPO_ROOT / "eval/experiments/EVAL-038"
PROMPTS = E38 / "media/prompts"
GATE_DIR = REPO_ROOT / "canon/gate"
FIXED_IMAGE = b"\xff\xd8\xff\xe0" + bytes(range(64)) + b"\xff\xd9"


def prompt(name):
    return (PROMPTS / f"{name}.txt").read_text()


def subchecks(scan):
    return sorted({h.subcheck for h in scan.hits})


class DevanagariTest(unittest.TestCase):
    def test_t1_devanagari_codepoints(self):
        self.assertEqual(textscan.devanagari_spans("किराया reminder"), ["किराया"])
        self.assertEqual(textscan.devanagari_spans("plain latin, 9:16"), [])
        self.assertEqual(textscan.devanagari_spans("꣠x"), ["꣠"])   # Devanagari Extended
        scan = textscan.scan_prompt("A poster reading किराया due.")
        self.assertIn("T1", subchecks(scan))


class PromptGuardTest(unittest.TestCase):
    # ── the four committed prompts ──────────────────────────────────────
    def test_sonnet_b06_prompt_passes_with_an_explicit_no_text_clause(self):
        scan = textscan.scan_prompt(prompt("B06-sonnet-no-canon"))
        self.assertEqual(scan.hits, [])
        self.assertTrue(scan.no_text_clause)

    def test_haiku_b06_prompt_passes_without_a_no_text_clause(self):
        scan = textscan.scan_prompt(prompt("B06-haiku-packs"))
        self.assertEqual(scan.hits, [])
        self.assertFalse(scan.no_text_clause)

    def test_sonnet_b01_prompt_1_fails_on_text_bearing_surfaces(self):
        scan = textscan.scan_prompt(prompt("B01-sonnet-no-canon"))
        self.assertIn("T3", subchecks(scan))
        sentences = {h.sentence_index for h in scan.hits}
        self.assertIn(2, sentences)   # "chat bubbles ... notification counter climbing past 99"
        s2 = [h for h in scan.hits if h.sentence_index == 2][0]
        self.assertTrue({"chat bubbles", "notification", "counter"} & set(s2.terms), s2.terms)
        # the closing "no text overlays baked into video (captions added in post)" sentence
        # is negated + deferred and must not be a hit
        last = scan.sentences[-1]
        self.assertIn("captions added in post", last)
        self.assertNotIn(len(scan.sentences), sentences)

    def test_sonnet_b01_prompt_3_fails_on_requested_text(self):
        text = ("Vertical 9:16, same man, same PG office now tidy and brightly lit, calm steady "
                "camera. Close-up of his phone screen showing a clean mobile app dashboard UI "
                "with a green checkmark and text 'Rent Collected' and 'Autopay Active', modern "
                "minimal Indian fintech-app UI design in a blue/teal brand color.")
        scan = textscan.scan_prompt(text)
        self.assertIn("T2", subchecks(scan))
        self.assertIn("T3", subchecks(scan))

    def test_haiku_b01_shot_1_fails_on_surfaces(self):
        scan = textscan.scan_prompt(prompt("B01-haiku-packs"))
        self.assertEqual(subchecks(scan), ["T3"])
        self.assertEqual([h.sentence_index for h in scan.hits][0], 2)

    def test_haiku_b01_shot_2_and_6_fail_on_requested_text(self):
        shot2 = ("Extreme close-up macro shot of a male hand holding a smartphone. The phone "
                 "screen shows a notification alert: 'Tenant Complaint Pending' and '3 Rents "
                 "Due' with red badge numbers.")
        self.assertIn("T2", subchecks(textscan.scan_prompt(shot2)))
        shot6 = ("Clean, minimal title card. Bold, modern sans-serif headline text (white or dark "
                 "gray on the light background), reading one of the following (verbatim from "
                 "RentOK website): 'Join 15,000+ Property Owners' OR 'Save Time. Work Less.'")
        self.assertIn("T2", subchecks(textscan.scan_prompt(shot6)))

    # ── windows ─────────────────────────────────────────────────────────
    def test_negation_window_clears_a_text_request(self):
        self.assertEqual(textscan.scan_prompt("A clean plate, no logo, no watermark.").hits, [])
        self.assertEqual(textscan.scan_prompt("A clean plate without any visible headline.").hits, [])
        hits = textscan.scan_prompt("A clean plate with a bold headline.").hits
        self.assertEqual([h.subcheck for h in hits], ["T2"])
        # five tokens between the negator and the term: outside the 4-token window
        hits = textscan.scan_prompt("No clutter, a bright bold tagline.").hits
        self.assertEqual([h.subcheck for h in hits], ["T2"])

    def test_deferral_clears_a_text_request_in_the_same_sentence(self):
        hits = textscan.scan_prompt("Logo animates in, tagline and CTA text to be added in post.").hits
        self.assertEqual(hits, [])
        hits = textscan.scan_prompt("Logo animates in. The tagline follows.").hits
        self.assertEqual([h.subcheck for h in hits], ["T2", "T2"])

    def test_illegibility_clears_a_text_surface(self):
        original = ("Extreme close-up of a smartphone screen filling with a rapid stack of "
                    "WhatsApp rent-reminder chat bubbles and a notification counter climbing "
                    "past 99.")
        self.assertTrue(textscan.scan_prompt(original).hits)
        rewritten = original.replace("climbing past 99.", "climbing, screens dark and illegible.")
        self.assertEqual(textscan.scan_prompt(rewritten).hits, [])

    def test_quoted_string_needs_two_word_characters_and_a_text_verb(self):
        self.assertEqual(textscan.scan_prompt("the 'Aster Meridian 38', shot as a still life").hits, [])
        self.assertEqual(textscan.scan_prompt("a sign saying 'x'").hits[0].subcheck, "T3")
        self.assertEqual([h.subcheck for h in textscan.scan_prompt("a dial reading 'ab'").hits],
                         ["T2"])
        # apostrophes are not quote openers
        self.assertEqual(textscan.scan_prompt("a man's hands showing the crown at 3 o'clock").hits,
                         [])

    def test_sonnet_b06_prompt_with_no_deleted_before_text(self):
        # Plan §F negative fixture: "B06 Sonnet prompt with 'no ' deleted before 'text' -> FAIL".
        # DISCREPANCY recorded for the checker: under the plan's own T2 vocabulary a bare
        # "text" is a TEXT_VERB (rule a, which also needs a quoted string) and not a
        # TEXT_REQUEST term (rule b), so "…, text, no logos, no watermark" yields no hit.
        # The vocabulary is not widened here (that is a Controller-visible change).
        mutated = prompt("B06-sonnet-no-canon").replace("no text, no logos", "text, no logos")
        self.assertNotEqual(mutated, prompt("B06-sonnet-no-canon"))
        self.assertEqual(textscan.scan_prompt(mutated).hits, [],
                         "if this now fails, the vocabulary changed — see plan §F fixture")


class LimitTextCheckTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reg = doctrine.load_registry()

    def check(self, *texts):
        return predispatch.check_limit_text(list(texts), self.reg)

    def test_sonnet_b06_passes_and_cites_the_limit_line(self):
        r = self.check(prompt("B06-sonnet-no-canon"))
        self.assertEqual(r.check_id, "LIMIT-TEXT")
        self.assertEqual(r.status, findings.Status.PASS)
        self.assertEqual(r.family, "limit")
        self.assertTrue(r.blocking)
        self.assertEqual(r.coverage, "full")
        self.assertEqual(r.source_text, self.reg.limit_text)
        self.assertIn("explicit no-text clause", r.detail)

    def test_haiku_b06_passes_with_a_note(self):
        r = self.check(prompt("B06-haiku-packs"))
        self.assertEqual(r.status, findings.Status.PASS)
        self.assertIn("no explicit no-text clause", r.detail)

    def test_sonnet_b01_fails_quoting_the_sentence_and_the_source(self):
        r = self.check(prompt("B01-sonnet-no-canon"))
        self.assertEqual(r.status, findings.Status.FAIL)
        self.assertTrue(r.detail.startswith("prompt 1, sentence 2"))
        self.assertIn("composite text deterministically", r.detail)
        self.assertTrue(r.evidence)

    def test_no_prompts_is_an_error(self):
        r = self.check()
        self.assertEqual(r.status, findings.Status.ERROR)
        self.assertIn("no generation prompt", r.detail)

    def test_devanagari_fails_in_full(self):
        r = self.check("A plain plate with किराया on it.")
        self.assertEqual(r.status, findings.Status.FAIL)
        self.assertIn("Devanagari", r.detail)


class DetectorTest(unittest.TestCase):
    def test_no_detector_is_unavailable(self):
        d = textscan.NoDetector()
        res = d.detect(FIXED_IMAGE)
        self.assertEqual(res.status, "unavailable")
        self.assertEqual(res.detector_id, d.detector_id)

    def test_scripted_detector_by_sha256(self):
        digest = hashlib.sha256(FIXED_IMAGE).hexdigest()
        d = textscan.ScriptedDetector({digest: textscan.TextDetection(
            "text", "ASTER MERIDIAN 38", "scripted", {})})
        self.assertEqual(d.detect(FIXED_IMAGE).transcript, "ASTER MERIDIAN 38")
        self.assertEqual(d.detect(b"other").status, "unavailable")

    def test_scripted_detector_loads_a_json_file(self):
        digest = hashlib.sha256(FIXED_IMAGE).hexdigest()
        d = textscan.ScriptedDetector.from_json(
            {digest: {"status": "no_text", "transcript": ""}})
        self.assertEqual(d.detect(FIXED_IMAGE).status, "no_text")


class CloudVisionAdapterTest(unittest.TestCase):
    def test_build_request_equals_the_emp001_shape_byte_for_byte(self):
        sys.path.insert(0, str(REPO_ROOT / "eval/empirical-tranche-1"))
        try:
            import ocr_providers
        finally:
            sys.path.pop(0)
        theirs = ocr_providers.CloudVisionTextDetection().build_request(FIXED_IMAGE)
        ours = textscan.CloudVisionTextDetection().build_request(FIXED_IMAGE)
        self.assertEqual(json.dumps(ours, sort_keys=True), json.dumps(theirs, sort_keys=True))
        self.assertNotIn("languageHints", json.dumps(ours))
        self.assertEqual(ours["requests"][0]["features"], [{"type": "TEXT_DETECTION",
                                                             "maxResults": 1}])

    def test_parse_documented_shapes(self):
        p = textscan.CloudVisionTextDetection().parse
        self.assertEqual(p({"responses": [{"textAnnotations": [{"description": "ASTER\nMERIDIAN"}]}]}).status,
                         "text")
        self.assertEqual(p({"responses": [{"textAnnotations": [{"description": "ASTER\nMERIDIAN"}]}]}).transcript,
                         "ASTER\nMERIDIAN")
        self.assertEqual(p({"responses": [{"fullTextAnnotation": {"text": "99+"}}]}).status, "text")
        self.assertEqual(p({"responses": [{"fullTextAnnotation": {"text": "  "}}]}).status, "no_text")
        self.assertEqual(p({"responses": [{"textAnnotations": []}]}).status, "no_text")
        self.assertEqual(p({"responses": [{}]}).status, "no_text")
        self.assertEqual(p({"responses": [{"error": {"code": 3, "message": "bad image"}}]}).status,
                         "unavailable")
        self.assertEqual(p({"error": {"code": 429}}).status, "unavailable")
        self.assertEqual(p({}).status, "unavailable")
        self.assertEqual(p({"responses": []}).status, "unavailable")
        self.assertEqual(p({"responses": [{"labelAnnotations": []}]}).status, "unavailable")

    def test_default_transport_refuses_before_any_network_activity(self):
        det = textscan.CloudVisionTextDetection()
        self.assertIsInstance(det.transport, textscan.RefusingTransport)
        with self.assertRaises(textscan.SpendNotAuthorised) as ctx:
            det.detect(FIXED_IMAGE)
        self.assertEqual(str(ctx.exception),
                         "CANON-GATE-001 authorises zero provider calls; invoking Cloud Vision "
                         "TEXT_DETECTION needs a separate spend authorisation")
        self.assertEqual(det.transport.calls, 0)

    def test_a_scripted_transport_is_the_only_way_to_exercise_parse_end_to_end(self):
        calls = []

        def transport(request):
            calls.append(request)
            return {"responses": [{"textAnnotations": [{"description": "MECHANICAL"}]}]}

        det = textscan.CloudVisionTextDetection(transport=transport)
        self.assertEqual(det.detect(FIXED_IMAGE).transcript, "MECHANICAL")
        self.assertEqual(len(calls), 1)


class BoundaryTest(unittest.TestCase):
    def test_no_secrets_network_or_env_reads_under_the_gate(self):
        files = sorted(GATE_DIR.glob("*.py"))
        self.assertTrue(files)
        for path in files:
            for n, line in enumerate(path.read_text().splitlines(), 1):
                self.assertNotIn("environ", line, f"{path.name}:{n}")
                self.assertNotIn("urlopen", line, f"{path.name}:{n}")
                self.assertNotRegex(line, r"^\s*(?:import|from)\s+(?:urllib|socket|http\b|requests)",
                                    f"{path.name}:{n}")
                if "vision.googleapis" in line:
                    self.assertEqual(path.name, "textscan.py", f"{path.name}:{n}")
                    self.assertRegex(line, r"^CLOUD_VISION_ENDPOINT\s*=", f"{path.name}:{n}")
        self.assertEqual(sum(1 for l in (GATE_DIR / "textscan.py").read_text().splitlines()
                             if "vision.googleapis" in l), 1)

    def test_doctrine_satisfied_never_appears_in_gate_sources(self):
        for path in sorted(GATE_DIR.glob("*.py")):
            self.assertNotIn("doctrine satisfied", path.read_text().lower(), path.name)


if __name__ == "__main__":
    unittest.main()
