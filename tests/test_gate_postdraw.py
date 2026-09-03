"""Post-draw gate end-to-end over the six committed EVAL-038 artifacts (CANON-GATE-001
plan §D post-draw, §E, §F).

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

The scripted detector results below encode HUMAN-OBSERVED truth — plan §0.2 (direct
inspection of the committed artifacts), the reviewer notes under judging/, and the RESULTS.md
replay note — keyed by sha256. They are not a detector measurement and prove plumbing only;
frames not named there stay `unavailable`. The paid detector is never invoked.
Run: python3 -m unittest tests.test_gate_postdraw
"""
import hashlib
import json
import unittest
from pathlib import Path

from canon.gate import doctrine, findings, postdraw, textscan
from tests.test_gate_artifact import audio_trak, box, jpeg, mp4, mvhd

REPO_ROOT = Path(__file__).resolve().parents[1]
E38 = REPO_ROOT / "eval/experiments/EVAL-038"
MEDIA = E38 / "media"
FRAMES = E38 / "judging/media/B01-video"
SONNET_B06 = E38 / "baseline/sonnet-no-canon/E037-sonnet-no-canon-B06-R1.txt"
HAIKU_B06 = E38 / "runs/haiku-packs/packages/E038-haiku-packs-B06-R1.txt"
S = findings.Status
ALL_IDS = [f"PA-D{i}-check" for i in range(1, 11)] + [f"CA-D{i}-check" for i in range(1, 12)]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def td(status, transcript=""):
    return textscan.TextDetection(status, transcript, "scripted", {"human_observed": True})


# Human-observed truth (plan §0.2): M01 (haiku) and M02 (sonnet no-canon) carry no dial text;
# the B06 replay bakes "ASTER / MERIDIAN 38 / MECHANICAL"; V01 frame 2 bakes garbled
# "Whatsapp" chips; V02 frame 1 bakes "Rent reminurders" bubbles and a "99" badge.
SCRIPTED = {
    sha(MEDIA / "E038-media-B06-haiku-packs.jpg"): td("no_text"),
    sha(MEDIA / "E038-media-B06-sonnet-no-canon.jpg"): td("no_text"),
    sha(MEDIA / "E038-media-B06-sonnet-replay2.jpg"): td("text", "ASTER MERIDIAN 38 MECHANICAL"),
    sha(FRAMES / "V01-frame-2.jpg"): td("text", "Whatsapp"),
    sha(FRAMES / "V02-frame-1.jpg"): td("text", "Rent reminurders 99"),
}


def dispatch(name):
    return json.loads((MEDIA / f"{name}.request.json").read_text())


def record(name):
    return json.loads((MEDIA / f"{name}.record.json").read_text())


class _Base(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reg = doctrine.load_registry()
        cls.det = textscan.ScriptedDetector(SCRIPTED)

    def run_post(self, name, modality, product, *, package=None, frames=None, detector=None,
                 artifact_bytes=None, dispatch_doc=None, rec=None):
        path = MEDIA / (f"{name}.jpg" if modality == "static_image" else f"{name}.mp4")
        return postdraw.run_postdraw(
            artifact_bytes if artifact_bytes is not None else path.read_bytes(),
            dispatch_doc if dispatch_doc is not None else dispatch(name),
            package.read_text() if package else None,
            detector if detector is not None else self.det,
            frames, modality, product, self.reg, label=path.name, record=rec)

    def row(self, report, check_id):
        return {r.check_id: r for r in report.results}[check_id]

    def status(self, report, check_id):
        return self.row(report, check_id).status

    def assertInvariants(self, report):
        self.assertEqual([r.check_id for r in report.results if r.family == "doctrine"], ALL_IDS)
        for r in report.results:
            if r.status is not S.PASS:
                self.assertTrue(r.detail.strip(), r.check_id)
            if r.family == "doctrine":
                self.assertEqual(r.source_text, self.reg.checks[r.check_id].text)
        text = report.render_text()
        self.assertNotIn("doctrine satisfied", text)
        self.assertEqual(report.gate, "post_draw")
        self.assertTrue(text.startswith("CANON GATE v0 — post-draw — artifact "))


class ImageTest(_Base):
    def test_m01_haiku_passes(self):
        r = self.run_post("E038-media-B06-haiku-packs", "static_image", True, package=HAIKU_B06,
                          rec=record("E038-media-B06-haiku-packs"))
        lt = self.row(r, "LIMIT-TEXT")
        self.assertEqual(lt.status, S.PASS)
        self.assertIn("per scripted", lt.detail)
        self.assertIn("benchmark qualification never certifies an individual output (EVAL-029)",
                      lt.detail)
        self.assertEqual(self.status(r, "CA-D6-check"), S.PASS)
        self.assertIn("928", self.row(r, "CA-D6-check").detail)
        self.assertEqual(self.status(r, "DISPATCH-ASPECT"), S.PASS)
        dims = self.row(r, "DISPATCH-DIMENSIONS")
        self.assertEqual(dims.status, S.NOT_RUN)
        self.assertIn("declares no minimum", dims.detail)
        self.assertNotIn("DISPATCH-DURATION", [x.check_id for x in r.results])
        self.assertEqual(self.status(r, "INFRA-CONTAINER"), S.PASS)
        self.assertEqual(self.status(r, "INFRA-RECORD-SHA"), S.PASS)
        self.assertEqual(r.verdict(), "PASS")
        self.assertInvariants(r)
        for cid in ALL_IDS:
            if cid != "CA-D6-check":
                self.assertIn(self.status(r, cid), (S.NOT_MECHANISED, S.NOT_APPLICABLE), cid)

    def test_m02_sonnet_fails_the_declared_minimum_dimensions(self):
        r = self.run_post("E038-media-B06-sonnet-no-canon", "static_image", True,
                          package=SONNET_B06)
        self.assertEqual(self.status(r, "LIMIT-TEXT"), S.PASS)
        self.assertEqual(self.status(r, "CA-D6-check"), S.PASS)
        dims = self.row(r, "DISPATCH-DIMENSIONS")
        self.assertEqual(dims.status, S.FAIL)
        self.assertTrue(dims.blocking)
        self.assertIn("1600", dims.detail)
        self.assertIn("928", dims.detail)
        self.assertEqual(r.verdict(), "FAIL")
        self.assertInvariants(r)

    def test_replay_image_fails_on_baked_text(self):
        r = self.run_post("E038-media-B06-sonnet-replay2", "static_image", True,
                          package=SONNET_B06)
        lt = self.row(r, "LIMIT-TEXT")
        self.assertEqual(lt.status, S.FAIL)
        self.assertTrue(lt.blocking)
        self.assertIn("ASTER MERIDIAN 38 MECHANICAL", lt.detail)
        self.assertIn("composite text deterministically", lt.detail)
        self.assertEqual(r.verdict(), "FAIL")

    def test_no_detector_is_not_run_never_pass(self):
        r = self.run_post("E038-media-B06-haiku-packs", "static_image", True,
                          detector=textscan.NoDetector())
        lt = self.row(r, "LIMIT-TEXT")
        self.assertEqual(lt.status, S.NOT_RUN)
        self.assertIn("no text detector configured", lt.detail)
        self.assertIn("separate spend authorisation", lt.detail)
        self.assertEqual(r.verdict(), "PASS")
        # the plan's j counts doctrine lines; a blocking-family row not run is named too so a
        # verdict PASS cannot read as a clean report (Ruling 2's rationale)
        last = r.render_text().splitlines()[-1]
        self.assertIn("not run: LIMIT-TEXT", last)
        self.assertIn("0 not run — none counted as satisfied", last)

    def test_record_sha_mismatch_is_reported(self):
        rec = record("E038-media-B06-haiku-packs")
        rec["sha256"] = "0" * 64
        r = self.run_post("E038-media-B06-haiku-packs", "static_image", True, rec=rec)
        row = self.row(r, "INFRA-RECORD-SHA")
        self.assertEqual(row.status, S.FAIL)
        self.assertIn("record.json", row.detail)
        self.assertTrue(row.blocking)
        self.assertEqual(r.verdict(), "FAIL")


class VideoTest(_Base):
    def frames(self, prefix):
        return [p.read_bytes() for p in sorted(FRAMES.glob(f"{prefix}-frame-*.jpg"))]

    def test_v01_with_frames_fails_on_baked_text(self):
        r = self.run_post("E038-media-B01-haiku-packs", "video", False, frames=self.frames("V01"))
        lt = self.row(r, "LIMIT-TEXT")
        self.assertEqual(lt.status, S.FAIL)
        self.assertIn("frame 2", lt.detail)
        self.assertIn("Whatsapp", lt.detail)
        self.assertEqual(r.verdict(), "FAIL")
        self.assertInvariants(r)

    def test_v02_with_frames_fails_on_baked_text(self):
        r = self.run_post("E038-media-B01-sonnet-no-canon", "video", False,
                          frames=self.frames("V02"))
        lt = self.row(r, "LIMIT-TEXT")
        self.assertEqual(lt.status, S.FAIL)
        self.assertIn("frame 1", lt.detail)
        self.assertEqual(r.verdict(), "FAIL")

    def test_v01_without_frames_passes_geometry_with_text_not_run(self):
        r = self.run_post("E038-media-B01-haiku-packs", "video", False,
                          rec=record("E038-media-B01-haiku-packs"))
        lt = self.row(r, "LIMIT-TEXT")
        self.assertEqual(lt.status, S.NOT_RUN)
        self.assertIn("frame extraction not available in stdlib", lt.detail)
        self.assertEqual(self.status(r, "CA-D6-check"), S.PASS)
        self.assertEqual(self.status(r, "DISPATCH-ASPECT"), S.PASS)
        dur = self.row(r, "DISPATCH-DURATION")
        self.assertEqual(dur.status, S.PASS)
        self.assertIn("8", dur.detail)
        self.assertEqual(self.status(r, "INFRA-VIDEO-TRACK"), S.PASS)
        self.assertEqual(self.status(r, "INFRA-RECORD-SHA"), S.PASS)
        self.assertEqual(self.status(r, "DISPATCH-DIMENSIONS"), S.NOT_RUN)
        for cid in [f"PA-D{i}-check" for i in range(1, 11)]:
            self.assertEqual(self.status(r, cid), S.NOT_APPLICABLE)
        self.assertEqual(r.verdict(), "PASS")

    def test_frames_all_unavailable_is_not_run(self):
        r = self.run_post("E038-media-B01-sonnet-replay2", "video", False,
                          frames=[b"\xff\xd8\xff\xd9"])
        self.assertEqual(self.status(r, "LIMIT-TEXT"), S.NOT_RUN)

    def test_duration_mismatch_blocks(self):
        d = dispatch("E038-media-B01-haiku-packs")
        d["parameters"]["durationSeconds"] = 6
        r = self.run_post("E038-media-B01-haiku-packs", "video", False, dispatch_doc=d)
        row = self.row(r, "DISPATCH-DURATION")
        self.assertEqual(row.status, S.FAIL)
        self.assertTrue(row.blocking)
        self.assertEqual(r.verdict(), "FAIL")


class InfraVerdictTest(_Base):
    """Ruling 4 / condition 7: every INFRA row is blocking, and each one, failing alone,
    turns the verdict — not only its own status (checker F-01)."""

    def failing_ids(self, report):
        return [r.check_id for r in report.results if r.failing]

    def test_every_infra_row_is_blocking(self):
        r = self.run_post("E038-media-B01-haiku-packs", "video", False,
                          rec=record("E038-media-B01-haiku-packs"))
        infra = [x for x in r.results if x.family == "infra"]
        self.assertEqual([x.check_id for x in infra],
                         ["INFRA-CONTAINER", "INFRA-VIDEO-TRACK", "INFRA-RECORD-SHA"])
        for x in infra:
            self.assertTrue(x.blocking, x.check_id)

    def test_record_sha_mismatch_alone_flips_the_verdict(self):
        # M01 passes in full with its committed record; the zeroed sha is the only change
        rec = record("E038-media-B06-haiku-packs")
        rec["sha256"] = "0" * 64
        r = self.run_post("E038-media-B06-haiku-packs", "static_image", True, package=HAIKU_B06,
                          rec=rec)
        self.assertEqual(self.failing_ids(r), ["INFRA-RECORD-SHA"])
        self.assertEqual(r.verdict(), "FAIL")
        self.assertTrue(r.render_text().splitlines()[-1].startswith("GATE FAIL ("))
        self.assertIn("FAIL            INFRA-RECORD-SHA", r.render_text())

    def test_image_under_a_video_dispatch_alone_flips_the_verdict(self):
        # a 9:16 JPEG satisfies DISPATCH-ASPECT against the committed B01 dispatch, so the
        # missing video track is the only failing row
        r = self.run_post("E038-media-B01-haiku-packs", "video", False,
                          artifact_bytes=jpeg(720, 1280))
        self.assertEqual(self.status(r, "DISPATCH-ASPECT"), S.PASS)
        self.assertEqual(self.failing_ids(r), ["INFRA-VIDEO-TRACK"])
        self.assertEqual(r.verdict(), "FAIL")

    def test_audio_only_mp4_under_a_video_dispatch_flips_the_verdict(self):
        ftyp = box("ftyp", b"isom" + bytes(4) + b"isomiso2avc1mp41")
        data = ftyp + box("moov", mvhd(1000, 8000) + audio_trak()) + box("mdat", bytes(32))
        r = self.run_post("E038-media-B01-haiku-packs", "video", False, artifact_bytes=data)
        track = self.row(r, "INFRA-VIDEO-TRACK")
        self.assertEqual(track.status, S.FAIL)
        self.assertIn("no video track", track.detail)
        self.assertIn("INFRA-VIDEO-TRACK", self.failing_ids(r))
        self.assertEqual(r.verdict(), "FAIL")

    def test_unparsable_container_alone_flips_the_verdict(self):
        r = self.run_post("E038-media-B06-haiku-packs", "static_image", True,
                          artifact_bytes=b"\xff\xd8\xff\xe0\x00\x10JFIF")
        row = self.row(r, "INFRA-CONTAINER")
        self.assertEqual(row.status, S.ERROR)
        self.assertTrue(row.blocking)
        self.assertEqual(self.failing_ids(r), ["INFRA-CONTAINER"])
        self.assertEqual(r.verdict(), "FAIL")


class SyntheticTest(_Base):
    PNG_1000 = (b"\x89PNG\r\n\x1a\n\x00\x00\x00\x0dIHDR\x00\x00\x03\xe8\x00\x00\x03\xe8"
                b"\x08\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00IEND\x00\x00\x00\x00")

    def test_square_png_against_4_5_fails_aspect(self):
        r = self.run_post("E038-media-B06-haiku-packs", "static_image", True,
                          artifact_bytes=self.PNG_1000)
        ca6 = self.row(r, "CA-D6-check")
        self.assertEqual(ca6.status, S.FAIL)
        self.assertFalse(ca6.blocking)
        self.assertIn("1000", ca6.detail)
        da = self.row(r, "DISPATCH-ASPECT")
        self.assertEqual(da.status, S.FAIL)
        self.assertTrue(da.blocking)
        self.assertEqual(r.verdict(), "FAIL")

    def test_truncated_jpeg_is_an_error_and_fails_closed(self):
        r = self.run_post("E038-media-B06-haiku-packs", "static_image", True,
                          artifact_bytes=b"\xff\xd8\xff\xe0\x00\x10JFIF")
        self.assertEqual(self.status(r, "INFRA-CONTAINER"), S.ERROR)
        self.assertEqual(self.status(r, "CA-D6-check"), S.NOT_RUN)
        self.assertEqual(self.status(r, "DISPATCH-ASPECT"), S.NOT_RUN)
        self.assertEqual(r.verdict(), "FAIL")
        self.assertInvariants(r)

    def test_gif_is_not_run_unsupported(self):
        r = self.run_post("E038-media-B06-haiku-packs", "static_image", True,
                          artifact_bytes=b"GIF89a" + bytes(30))
        row = self.row(r, "INFRA-CONTAINER")
        self.assertEqual(row.status, S.NOT_RUN)
        self.assertIn("unsupported container", row.detail)
        self.assertEqual(self.status(r, "CA-D6-check"), S.NOT_RUN)
        self.assertEqual(r.verdict(), "PASS")

    def test_video_dispatch_over_an_image_fails_the_track_check(self):
        r = self.run_post("E038-media-B06-haiku-packs", "video", False,
                          artifact_bytes=(MEDIA / "E038-media-B06-haiku-packs.jpg").read_bytes(),
                          dispatch_doc=dispatch("E038-media-B01-haiku-packs"))
        row = self.row(r, "INFRA-VIDEO-TRACK")
        self.assertEqual(row.status, S.FAIL)
        self.assertTrue(row.blocking)
        self.assertEqual(self.status(r, "DISPATCH-DURATION"), S.NOT_RUN)
        self.assertEqual(r.verdict(), "FAIL")

    def test_json_carries_every_row(self):
        r = self.run_post("E038-media-B06-haiku-packs", "static_image", True)
        js = r.to_json()
        self.assertEqual(js["gate"], "post_draw")
        self.assertEqual(len([x for x in js["results"] if x["family"] == "doctrine"]), 21)
        self.assertIn("E038-media-B06-haiku-packs.jpg", js["inputs"])


if __name__ == "__main__":
    unittest.main()
