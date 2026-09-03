"""Gate CLI (CANON-GATE-001 plan §B run_gate.py, §F): exit codes, the final-line idiom,
--json round-trip, detector selection without a paid option.

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

Run: python3 -m unittest tests.test_gate_cli
"""
import contextlib
import hashlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from canon.gate import run_gate

REPO_ROOT = Path(__file__).resolve().parents[1]
E38 = REPO_ROOT / "eval/experiments/EVAL-038"
MEDIA = E38 / "media"
FRAMES = E38 / "judging/media/B01-video"
SONNET_B01 = E38 / "baseline/sonnet-no-canon/E037-sonnet-no-canon-B01-R1.txt"
SONNET_B06 = E38 / "baseline/sonnet-no-canon/E037-sonnet-no-canon-B06-R1.txt"
HAIKU_B06 = E38 / "runs/haiku-packs/packages/E038-haiku-packs-B06-R1.txt"
M01 = MEDIA / "E038-media-B06-haiku-packs.jpg"
M02 = MEDIA / "E038-media-B06-sonnet-no-canon.jpg"
REPLAY = MEDIA / "E038-media-B06-sonnet-replay2.jpg"
V01 = MEDIA / "E038-media-B01-haiku-packs.mp4"


def run(argv):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = run_gate.main(argv)
    return code, out.getvalue()


def scripted_file(tmp, **entries):
    doc = {hashlib.sha256(Path(p).read_bytes()).hexdigest(): v for p, v in entries.items()}
    path = Path(tmp) / "scripted.json"
    path.write_text(json.dumps(doc))
    return str(path)


class PreDispatchCliTest(unittest.TestCase):
    def test_haiku_b06_exits_zero_with_the_pass_idiom(self):
        code, out = run(["pre", "--package", str(HAIKU_B06), "--modality", "static_image",
                         "--product", "--dispatch", str(MEDIA / "E038-media-B06-haiku-packs.request.json")])
        self.assertEqual(code, 0)
        lines = out.strip().splitlines()
        self.assertTrue(lines[0].startswith("CANON GATE v0 — pre-dispatch — package "
                                            "E038-haiku-packs-B06-R1.txt (sha256 "))
        self.assertTrue(lines[-1].startswith("GATE PASS: "))
        self.assertTrue(lines[-1].endswith(
            "— none counted as satisfied. This establishes structure over the prompt/artifact "
            "bytes — not doctrine satisfaction, quality, outcomes, or adoption."))
        self.assertNotIn("doctrine satisfied", out)
        for i in range(1, 11):
            self.assertIn(f"PA-D{i}-check", out)
        for i in range(1, 12):
            self.assertIn(f"CA-D{i}-check", out)

    def test_sonnet_b01_exits_one_with_the_fail_idiom(self):
        code, out = run(["pre", "--package", str(SONNET_B01), "--modality", "video"])
        self.assertEqual(code, 1)
        last = out.strip().splitlines()[-1]
        self.assertTrue(last.startswith("GATE FAIL ("))
        self.assertIn("over 21 doctrine check lines", last)
        self.assertIn("never counted as satisfied", last)
        self.assertIn("FAIL            LIMIT-TEXT", out)

    def test_json_round_trips_every_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.json"
            code, out = run(["pre", "--package", str(SONNET_B06), "--modality", "static_image",
                             "--product", "--json", str(path)])
            js = json.loads(path.read_text())
        self.assertEqual(code, 0)
        self.assertEqual(js["verdict"], "PASS")
        self.assertEqual(len([r for r in js["results"] if r["family"] == "doctrine"]), 21)
        self.assertEqual(js["report_text"].strip(), out.strip())
        ca5 = next(r for r in js["results"] if r["check_id"] == "CA-D5-check")
        self.assertEqual((ca5["status"], ca5["blocking"]), ("FAIL", False))

    def test_prompt_files_replace_extraction(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "prompt.txt"
            p.write_text("A dark empty room, no text, no logos.")
            code, out = run(["pre", "--package", str(SONNET_B01), "--modality", "video",
                             "--prompt-file", str(p)])
        self.assertIn("PASS            LIMIT-TEXT", out)

    def test_packs_override_restricts_selection(self):
        code, out = run(["pre", "--package", str(HAIKU_B06), "--modality", "static_image",
                         "--product", "--packs", "composition_and_attention"])
        self.assertIn("packs: composition_and_attention\n", out)
        self.assertIn("NOT-APPLICABLE  PA-D1-check", out)

    def test_unknown_pack_is_refused(self):
        with self.assertRaises(SystemExit):
            run(["pre", "--package", str(HAIKU_B06), "--modality", "static_image",
                 "--packs", "typography_and_copy"])

    def test_invalid_modality_is_refused(self):
        with self.assertRaises(SystemExit):
            run(["pre", "--package", str(HAIKU_B06), "--modality", "hologram"])

    def test_validate_packs_runs_the_full_validator(self):
        code, out = run(["pre", "--package", str(HAIKU_B06), "--modality", "static_image",
                         "--product", "--validate-packs"])
        self.assertEqual(code, 0)
        self.assertIn("PASS pack validation", out)


class PostDrawCliTest(unittest.TestCase):
    def test_m01_with_no_detector_exits_zero_and_reports_not_run(self):
        code, out = run(["post", "--artifact", str(M01),
                         "--dispatch", str(MEDIA / "E038-media-B06-haiku-packs.request.json"),
                         "--modality", "static_image", "--product", "--detector", "none",
                         "--record", str(MEDIA / "E038-media-B06-haiku-packs.record.json")])
        self.assertEqual(code, 0)
        self.assertTrue(out.startswith("CANON GATE v0 — post-draw — artifact "
                                       "E038-media-B06-haiku-packs.jpg (sha256 "))
        self.assertIn("NOT-RUN         LIMIT-TEXT      no text detector configured", out)
        self.assertIn("PASS            INFRA-RECORD-SHA", out)
        self.assertIn("not run: LIMIT-TEXT", out.strip().splitlines()[-1])

    def test_replay_with_a_scripted_detector_exits_one(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = scripted_file(tmp, **{str(REPLAY): {"status": "text",
                                                         "transcript": "ASTER MERIDIAN 38"}})
            code, out = run(["post", "--artifact", str(REPLAY),
                             "--dispatch", str(MEDIA / "E038-media-B06-sonnet-replay2.request.json"),
                             "--package", str(SONNET_B06), "--modality", "static_image",
                             "--product", "--detector", f"scripted:{spec}"])
        self.assertEqual(code, 1)
        self.assertIn("FAIL            LIMIT-TEXT      text detected ('ASTER MERIDIAN 38')", out)
        self.assertIn("FAIL            DISPATCH-DIMENSIONS", out)

    def test_m02_with_package_fails_on_declared_dimensions_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = scripted_file(tmp, **{str(M02): {"status": "no_text"}})
            code, out = run(["post", "--artifact", str(M02),
                             "--dispatch", str(MEDIA / "E038-media-B06-sonnet-no-canon.request.json"),
                             "--package", str(SONNET_B06), "--modality", "static_image",
                             "--product", "--detector", f"scripted:{spec}"])
        self.assertEqual(code, 1)
        self.assertIn("PASS            LIMIT-TEXT", out)
        self.assertIn("FAIL            DISPATCH-DIMENSIONS", out)

    def test_video_with_frames_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            spec = scripted_file(tmp, **{str(FRAMES / "V01-frame-2.jpg"): {"status": "text",
                                                                          "transcript": "Whatsapp"}})
            code, out = run(["post", "--artifact", str(V01),
                             "--dispatch", str(MEDIA / "E038-media-B01-haiku-packs.request.json"),
                             "--modality", "video", "--frames", str(FRAMES),
                             "--detector", f"scripted:{spec}"])
        self.assertEqual(code, 1)
        self.assertIn("frame 2: text detected ('Whatsapp')", out)
        # the dir's eight JPEGs are scanned in sorted order; V01-frame-2.jpg is the second
        self.assertIn("PASS            DISPATCH-DURATION", out)

    def test_video_without_frames_passes_geometry(self):
        code, out = run(["post", "--artifact", str(V01),
                         "--dispatch", str(MEDIA / "E038-media-B01-haiku-packs.request.json"),
                         "--modality", "video"])
        self.assertEqual(code, 0)
        self.assertIn("NOT-RUN         LIMIT-TEXT      frame extraction not available in stdlib", out)
        self.assertIn("PASS            DISPATCH-ASPECT", out)
        self.assertIn("PASS            INFRA-VIDEO-TRACK", out)

    def test_there_is_no_paid_detector_flag(self):
        with self.assertRaises(SystemExit):
            run(["post", "--artifact", str(M01),
                 "--dispatch", str(MEDIA / "E038-media-B06-haiku-packs.request.json"),
                 "--modality", "static_image", "--detector", "cloud-vision"])

    def test_json_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "post.json"
            code, out = run(["post", "--artifact", str(M01),
                             "--dispatch", str(MEDIA / "E038-media-B06-haiku-packs.request.json"),
                             "--modality", "static_image", "--product", "--json", str(path)])
            js = json.loads(path.read_text())
        self.assertEqual(js["gate"], "post_draw")
        self.assertEqual(js["report_text"].strip(), out.strip())


class ScriptInvocationTest(unittest.TestCase):
    def test_runs_as_a_script_from_the_repo_root(self):
        proc = subprocess.run(
            [sys.executable, "canon/gate/run_gate.py", "pre", "--package", str(HAIKU_B06),
             "--modality", "static_image", "--product"],
            cwd=REPO_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(proc.stdout.strip().splitlines()[-1].startswith("GATE PASS: "))

    def test_help_names_both_gates(self):
        proc = subprocess.run([sys.executable, "canon/gate/run_gate.py", "--help"],
                              cwd=REPO_ROOT, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("pre", proc.stdout)
        self.assertIn("post", proc.stdout)


if __name__ == "__main__":
    unittest.main()
