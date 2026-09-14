"""Video-frame text hygiene (promoted from UPWORK-INTRO-001, SD-06): a generated video's text verdict comes
ONLY from its sampled frames. A text-clean source still never transfers a PASS to the video; no sampled
frames means NOT_RUN — never PASS. V3's Kling B2 clip is the case: the still passed the scan, the clip
grew letter-shaped signage, and nothing mechanical looked at the clip.
"""
from __future__ import annotations

import hashlib
import tempfile
import unittest

import _bootstrap  # noqa: F401
import test_g_support as G
from test_g_loop import manifest_for
from canon.gate import textscan
from canon.gate.textscan import TextDetection
from runtime.loop import driver, frame_hygiene, memory, package, postdraw, predispatch, synthetic

NOW = "2026-09-14T12:00:00Z"
ROW = "RUNTIME-VIDEO-FRAME-TEXT"


def det(status, transcript=""):
    return TextDetection(status, transcript, "scripted", {})


class Assess(unittest.TestCase):
    def test_text_in_a_sampled_frame_fails_regardless_of_the_source_still(self):
        row = frame_hygiene.assess([det("no_text"), det("text", "BREW"), det("no_text")], source_still_clean=True)
        self.assertEqual(row["check_id"], ROW)
        self.assertEqual(row["status"], "FAIL")
        self.assertTrue(row["blocking"])
        self.assertIn("frame 2", row["detail"])
        self.assertIn("source still", row["detail"])          # says the clean still did not transfer

    def test_clean_still_and_tainted_video_is_a_fail_not_a_pass(self):
        row = frame_hygiene.assess([det("text", "sign")], source_still_clean=True)
        self.assertEqual(row["status"], "FAIL")

    def test_no_frames_is_not_run_never_pass(self):
        row = frame_hygiene.assess([], source_still_clean=True)
        self.assertEqual(row["status"], "NOT-RUN")
        self.assertTrue(row["blocking"])
        self.assertIn("no frames were sampled", row["detail"])

    def test_all_frames_clean_passes_with_the_count(self):
        row = frame_hygiene.assess([det("no_text"), det("no_text")], source_still_clean=None)
        self.assertEqual(row["status"], "PASS")
        self.assertIn("2 sampled frames", row["detail"])

    def test_an_unavailable_frame_is_not_counted_as_clean(self):
        row = frame_hygiene.assess([det("no_text"), det("unavailable")], source_still_clean=None)
        self.assertEqual(row["status"], "NOT-RUN")


class PostDrawVideo(unittest.TestCase):
    def setUp(self):
        self.spec = G.load_spec_dict(G.SPEC_MOTION)
        self.text = package.render_package(self.spec, G.blueprint_motion())
        self.dispatch = predispatch.dispatch_descriptor(self.spec)
        self.mp4 = synthetic.mp4_for_spec(self.spec)
        self.frames = [synthetic.png_for_aspect(self.spec["deliverable"]["aspect"], seed=s) for s in (11, 12, 13)]

    def scripted(self, tainted_index=None):
        doc = {}
        for i, f in enumerate(self.frames):
            doc[hashlib.sha256(f).hexdigest()] = ({"status": "text", "transcript": "CAFE"} if i == tainted_index
                                                  else {"status": "no_text", "transcript": ""})
        return textscan.ScriptedDetector.from_json(doc)

    def test_video_without_sampled_frames_is_not_run_not_pass(self):
        out = postdraw.run(self.spec, self.mp4, self.dispatch, self.text, product_entity=False,
                           detector=self.scripted(), frames=None)
        self.assertEqual(out["verdict"], "NOT_RUN")
        rows = {r["check_id"]: r for r in out["rows"]}
        self.assertEqual(rows[ROW]["status"], "NOT-RUN")
        self.assertEqual(rows["LIMIT-TEXT"]["status"], "NOT-RUN")

    def test_sampled_frame_with_stray_lettering_fails_post_draw(self):
        out = postdraw.run(self.spec, self.mp4, self.dispatch, self.text, product_entity=False,
                           detector=self.scripted(tainted_index=1), frames=self.frames, source_still_clean=True)
        self.assertEqual(out["verdict"], "FAIL")
        self.assertIn("LIMIT-TEXT", out["blocking_failures"])
        self.assertIn(ROW, out["blocking_failures"])

    def test_clean_frames_pass_and_the_row_names_the_frame_count(self):
        out = postdraw.run(self.spec, self.mp4, self.dispatch, self.text, product_entity=False,
                           detector=self.scripted(), frames=self.frames)
        self.assertEqual(out["verdict"], "PASS")
        rows = {r["check_id"]: r for r in out["rows"]}
        self.assertEqual(rows[ROW]["status"], "PASS")
        self.assertIn("3 sampled frames", rows[ROW]["detail"])

    def test_image_modality_is_untouched_by_the_video_row(self):
        spec = G.load_spec_dict(G.SPEC_OVERLAY)
        text = package.render_package(spec, G.blueprint_clean())
        png = synthetic.png_for_aspect(spec["deliverable"]["aspect"], seed=1)
        d = textscan.ScriptedDetector.from_json({hashlib.sha256(png).hexdigest(): {"status": "no_text", "transcript": ""}})
        out = postdraw.run(spec, png, predispatch.dispatch_descriptor(spec), text, product_entity=True, detector=d)
        self.assertEqual(out["verdict"], "PASS")
        self.assertNotIn(ROW, {r["check_id"] for r in out["rows"]})


class LoopWithFrameSampler(unittest.TestCase):
    def setUp(self):
        self.spec = G.load_spec_dict(G.SPEC_MOTION)
        self.bp = G.blueprint_motion()
        self.profile = G.profile("alpha_human_release")
        self.tmp = tempfile.mkdtemp(prefix="i-frames-")
        self.aspect = self.spec["deliverable"]["aspect"]

    def provider(self, attempt):
        return synthetic.mp4_for_spec(self.spec, seed=attempt["draw_index"])

    def frames_for(self, attempt, artifact):
        return [synthetic.png_for_aspect(self.aspect, seed=100 * attempt["draw_index"] + k) for k in (1, 2, 3)]

    def scripted(self, taint):
        """taint: set of (draw_index, frame_k) that carry lettering."""
        doc = {}
        for draw in (1, 2):
            for k in (1, 2, 3):
                png = synthetic.png_for_aspect(self.aspect, seed=100 * draw + k)
                doc[hashlib.sha256(png).hexdigest()] = ({"status": "text", "transcript": "40%"} if (draw, k) in taint
                                                        else {"status": "no_text", "transcript": ""})
        return textscan.ScriptedDetector.from_json(doc)

    def run_loop(self, det, sampler, verdicts):
        return driver.run_loop(self.spec, self.bp, manifest_for(self.spec), self.profile,
                               artifact_provider=self.provider, detector=det, human_verdicts=verdicts,
                               product_entity=False, write=False, store=memory.OutcomeStore(self.tmp),
                               now_utc=NOW, frame_sampler=sampler)

    def test_tainted_frame_fails_the_attempt_and_a_clean_redraw_is_accepted(self):
        res = self.run_loop(self.scripted({(1, 2)}), self.frames_for, [G.load_json("human-accept.json")])
        self.assertEqual(res.attempts[0]["gate_post_verdict"], "FAIL")
        self.assertEqual(res.attempts[1]["gate_post_verdict"], "PASS")
        self.assertEqual(res.acceptance_state, "accepted")
        self.assertEqual(res.repairs[0]["failure_category"], "baked_lettering")

    def test_no_sampler_on_video_means_nothing_can_be_accepted(self):
        res = self.run_loop(self.scripted(set()), None, [G.load_json("human-accept.json")])
        self.assertTrue(all(a["gate_post_verdict"] == "NOT_RUN" for a in res.attempts))
        self.assertEqual(res.acceptance_state, "abandoned")


if __name__ == "__main__":
    unittest.main()
