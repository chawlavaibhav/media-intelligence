"""Lane G, parts B and C: the pre-dispatch and post-draw wrappers around canon.gate, the dispatch
descriptor built from the spec, and the synthetic artifacts the dry tranche draws."""
from __future__ import annotations

import hashlib
import json
import unittest

import test_g_support as G

from canon.gate import artifact as probes
from canon.gate import textscan
from runtime.errors import Refusal
from runtime.loop import package, postdraw, predispatch, synthetic


def rows_by_id(outcome):
    return {r["check_id"]: r for r in outcome["rows"]}


class DispatchDescriptor(unittest.TestCase):
    def test_image_shape_is_the_committed_request_json_shape(self):
        d = predispatch.dispatch_descriptor(G.load_spec_dict(G.SPEC_OVERLAY))
        self.assertEqual(d, {"generationConfig": {"imageConfig": {"aspectRatio": "4:5"}}})

    def test_video_shape_carries_aspect_and_duration(self):
        d = predispatch.dispatch_descriptor(G.load_spec_dict(G.SPEC_MOTION))
        self.assertEqual(d["parameters"]["aspectRatio"], "9:16")
        self.assertEqual(d["parameters"]["durationSeconds"], 6)
        # the spec names a resolution class, not a pixel resolution; nothing is invented
        self.assertNotIn("resolution", d["parameters"])

    def test_modality_is_read_from_the_binding_yaml(self):
        self.assertEqual(predispatch.modality_of(G.load_spec_dict(G.SPEC_OVERLAY)), "static_image")
        self.assertEqual(predispatch.modality_of(G.load_spec_dict(G.SPEC_MOTION)), "video")
        spec = G.load_spec_dict(G.SPEC_OVERLAY)
        spec["deliverable"]["kind"] = "hologram"
        with self.assertRaises(Refusal):
            predispatch.modality_of(spec)


class PreDispatch(unittest.TestCase):
    def setUp(self):
        self.spec = G.load_spec_dict(G.SPEC_OVERLAY)
        self.text = package.render_package(self.spec, G.blueprint_clean())
        self.dispatch = predispatch.dispatch_descriptor(self.spec)

    def test_outcome_shape_and_pass(self):
        out = predispatch.run(self.spec, self.text, self.dispatch, product_entity=True)
        self.assertEqual(out["gate"], "pre_dispatch")
        self.assertEqual(out["verdict"], "PASS", out["rows"])
        self.assertEqual(out["blocking_failures"], [])
        self.assertEqual(set(out) >= {"gate", "verdict", "blocking_failures", "rows", "report_sha256",
                                      "packs_selected"}, True)
        self.assertEqual(out["packs_selected"], ["composition_and_attention", "product_appearance"])
        self.assertEqual(len(out["report_sha256"]), 64)
        rows = rows_by_id(out)
        self.assertEqual(rows["LIMIT-TEXT"]["status"], "PASS")
        self.assertTrue(rows["LIMIT-TEXT"]["blocking"])
        self.assertEqual(rows["RUNTIME-PLATE-NO-LETTERING-INSTRUCTION"]["status"], "PASS")

    def test_report_sha_is_over_the_rendered_report_text(self):
        out = predispatch.run(self.spec, self.text, self.dispatch, product_entity=True)
        self.assertEqual(out["report_sha256"], hashlib.sha256(out["report_text"].encode("utf-8")).hexdigest())

    def test_empty_packs_selected_hands_selection_to_the_trigger_table(self):
        # the fixture names no compiled pack; LIMIT-TEXT must still run, never be switched off
        self.assertEqual(self.spec["canon"]["packs_selected"], [])
        out = predispatch.run(self.spec, self.text, self.dispatch, product_entity=False)
        self.assertEqual(out["packs_selected"], ["composition_and_attention"])
        self.assertEqual(rows_by_id(out)["LIMIT-TEXT"]["status"], "PASS")

    def test_compiled_packs_from_spec_are_passed_through(self):
        spec = G.load_spec_dict(G.SPEC_OVERLAY)
        spec["canon"]["packs_selected"] = [
            {"pack_id": "composition_and_attention", "trigger": "base:static_image", "compiled": True},
            {"pack_id": "typography_and_copy", "trigger": "R08", "compiled": False},
        ]
        out = predispatch.run(spec, self.text, self.dispatch, product_entity=True)
        self.assertEqual(out["packs_selected"], ["composition_and_attention"])

    def test_aspect_mismatch_blocks(self):
        out = predispatch.run(self.spec, self.text,
                              {"generationConfig": {"imageConfig": {"aspectRatio": "1:1"}}},
                              product_entity=True)
        self.assertEqual(out["verdict"], "FAIL")
        self.assertIn("DISPATCH-ASPECT", out["blocking_failures"])

    def test_img_text_01_plate_blocks_on_limit_text(self):
        text = package.render_package(self.spec, G.blueprint_overlay())
        out = predispatch.run(self.spec, text, self.dispatch, product_entity=True)
        self.assertEqual(out["verdict"], "FAIL")
        self.assertEqual(out["blocking_failures"], ["LIMIT-TEXT"])

    def test_plate_without_no_lettering_instruction_is_a_runtime_fail_row(self):
        bp = G.blueprint_clean()
        plate = bp["generation_prompts"]["textless_plate"]
        bp["generation_prompts"]["textless_plate"] = plate.replace(
            " No text, no lettering, no numerals, no symbols anywhere in the image.",
            " The lower band stays empty maroon, ready for the composited copy later.")
        text = package.render_package(self.spec, bp)
        out = predispatch.run(self.spec, text, self.dispatch, product_entity=True)
        row = rows_by_id(out)["RUNTIME-PLATE-NO-LETTERING-INSTRUCTION"]
        self.assertEqual(row["status"], "FAIL")
        self.assertTrue(row["blocking"])
        self.assertEqual(row["family"], "runtime")
        self.assertIn("RUNTIME-PLATE-NO-LETTERING-INSTRUCTION", out["blocking_failures"])
        self.assertEqual(out["verdict"], "FAIL")

    def test_runtime_row_not_run_when_mechanism_is_not_a_plate(self):
        spec = G.load_spec_dict(G.SPEC_MOTION)
        text = package.render_package(spec, G.blueprint_motion())
        out = predispatch.run(spec, text, predispatch.dispatch_descriptor(spec), product_entity=False)
        self.assertEqual(rows_by_id(out)["RUNTIME-PLATE-NO-LETTERING-INSTRUCTION"]["status"], "NOT-APPLICABLE")
        self.assertEqual(out["verdict"], "PASS", out["report_text"])


class Synthetic(unittest.TestCase):
    def test_png_probes_to_declared_size(self):
        data = synthetic.make_png(64, 80)
        info = probes.probe(data)
        self.assertEqual((info.kind, info.container, info.width, info.height), ("image", "png", 64, 80))
        # a real PNG: zlib-compressed rows, CRC-checked chunks
        self.assertTrue(synthetic.png_crc_ok(data))

    def test_png_for_aspect(self):
        data = synthetic.png_for_aspect("4:5")
        info = probes.probe(data)
        ok, _, _ = probes.aspect_matches(info.width, info.height, "4:5")
        self.assertTrue(ok)
        # the same aspect + seed give the same bytes (the scripted detector keys on sha256)
        self.assertEqual(data, synthetic.png_for_aspect("4:5"))
        self.assertNotEqual(data, synthetic.png_for_aspect("4:5", seed=2))

    def test_mp4_stub_probes(self):
        data = synthetic.make_mp4_stub(72, 128, duration_s=6.0)
        info = probes.probe(data)
        self.assertEqual(info.kind, "video")
        self.assertEqual((info.width, info.height), (72, 128))
        self.assertAlmostEqual(info.duration_s, 6.0)
        self.assertTrue(info.has_video_track)
        self.assertFalse(info.has_audio_track)


class PostDraw(unittest.TestCase):
    def setUp(self):
        self.spec = G.with_aspect(G.load_spec_dict(G.SPEC_OVERLAY), "1:1")
        self.text = package.render_package(self.spec, G.blueprint_clean())
        self.dispatch = predispatch.dispatch_descriptor(self.spec)
        self.png = synthetic.png_for_aspect("1:1")

    def detector(self, name):
        return textscan.ScriptedDetector.from_json(G.load_json(name))

    def test_no_artifact_is_not_run_never_pass(self):
        out = postdraw.run(self.spec, None, self.dispatch, self.text, product_entity=True)
        self.assertEqual(out["verdict"], "NOT_RUN")
        self.assertEqual(out["blocking_failures"], [])
        self.assertTrue(out["rows"])
        for row in out["rows"]:
            self.assertEqual(row["status"], "NOT-RUN")
            self.assertIn("no artifact; dry attempt", row["detail"])

    def test_clean_png_passes_aspect_rows(self):
        out = postdraw.run(self.spec, self.png, self.dispatch, self.text, product_entity=True,
                           detector=self.detector("detector-no-text.json"))
        rows = rows_by_id(out)
        self.assertEqual(rows["DISPATCH-ASPECT"]["status"], "PASS", rows["DISPATCH-ASPECT"]["detail"])
        self.assertEqual(rows["INFRA-CONTAINER"]["status"], "PASS")
        self.assertEqual(rows["LIMIT-TEXT"]["status"], "PASS", rows["LIMIT-TEXT"]["detail"])
        self.assertEqual(rows["CA-D6-check"]["status"], "PASS")
        self.assertEqual(out["verdict"], "PASS", out["report_text"])

    def test_four_by_five_png_against_one_by_one_dispatch_fails_delivered_vs_declared(self):
        out = postdraw.run(self.spec, synthetic.png_for_aspect("4:5"), self.dispatch, self.text,
                           product_entity=True, detector=self.detector("detector-no-text.json"))
        self.assertEqual(out["verdict"], "FAIL")
        self.assertIn("DISPATCH-ASPECT", out["blocking_failures"])

    def test_lettering_fixture_fails_limit_text_blocking(self):
        out = postdraw.run(self.spec, self.png, self.dispatch, self.text, product_entity=True,
                           detector=self.detector("detector-lettering.json"))
        rows = rows_by_id(out)
        self.assertEqual(rows["LIMIT-TEXT"]["status"], "FAIL")
        self.assertTrue(rows["LIMIT-TEXT"]["blocking"])
        self.assertIn("40% 40%", rows["LIMIT-TEXT"]["detail"])
        self.assertEqual(out["blocking_failures"], ["LIMIT-TEXT"])
        self.assertEqual(out["verdict"], "FAIL")

    def test_no_detector_means_limit_text_not_run_never_pass(self):
        out = postdraw.run(self.spec, self.png, self.dispatch, self.text, product_entity=True)
        self.assertEqual(rows_by_id(out)["LIMIT-TEXT"]["status"], "NOT-RUN")

    def test_video_stub_against_video_dispatch(self):
        spec = G.load_spec_dict(G.SPEC_MOTION)
        text = package.render_package(spec, G.blueprint_motion())
        dispatch = predispatch.dispatch_descriptor(spec)
        out = postdraw.run(spec, synthetic.mp4_for_spec(spec), dispatch, text, product_entity=False)
        rows = rows_by_id(out)
        self.assertEqual(rows["DISPATCH-ASPECT"]["status"], "PASS", rows["DISPATCH-ASPECT"]["detail"])
        self.assertEqual(rows["DISPATCH-DURATION"]["status"], "PASS", rows["DISPATCH-DURATION"]["detail"])
        self.assertEqual(rows["INFRA-VIDEO-TRACK"]["status"], "PASS")
        # stdlib cannot decode frames: the video text scan is honestly NOT-RUN
        self.assertEqual(rows["LIMIT-TEXT"]["status"], "NOT-RUN")

    def test_detector_fixtures_key_on_the_synthetic_sha(self):
        digest = hashlib.sha256(self.png).hexdigest()
        self.assertIn(digest, G.load_json("detector-no-text.json"))
        self.assertIn(digest, G.load_json("detector-lettering.json"))


if __name__ == "__main__":
    unittest.main()
