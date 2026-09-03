"""Stdlib container probes (CANON-GATE-001 plan §E, §B artifact.py, §F).

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

Real fixtures are the six committed EVAL-038 artifacts, read in place (JPEG SOF -> 928x1152;
MP4 moov/trak/stsd -> avc1 720x1280, mvhd -> 8.0 s, audio track present). Synthetic
PNG/JPEG/MP4 bytes are built here so tkhd v0/v1, a largesize box, `moov` after `mdat`, a
rotated matrix and fragmented input are each exercised. Run: python3 -m unittest
tests.test_gate_artifact
"""
import struct
import unittest
from pathlib import Path

from canon.gate import artifact

REPO_ROOT = Path(__file__).resolve().parents[1]
MEDIA = REPO_ROOT / "eval/experiments/EVAL-038/media"
JPEGS = sorted(MEDIA.glob("E038-media-B06-*.jpg"))
MP4S = sorted(MEDIA.glob("E038-media-B01-*.mp4"))


# ── synthetic byte builders ─────────────────────────────────────────────────

def box(kind, payload, large=False):
    kind = kind.encode("ascii") if isinstance(kind, str) else kind
    if large:
        return struct.pack(">I4sQ", 1, kind, 16 + len(payload)) + payload
    return struct.pack(">I4s", 8 + len(payload), kind) + payload


def full(kind, version, payload):
    return box(kind, bytes([version, 0, 0, 0]) + payload)


IDENTITY = struct.pack(">9i", 0x10000, 0, 0, 0, 0x10000, 0, 0, 0, 0x40000000)
ROT90 = struct.pack(">9i", 0, 0x10000, 0, -0x10000, 0, 0, 0, 0, 0x40000000)


def mvhd(timescale, duration, version=0):
    if version == 1:
        head = struct.pack(">QQIQ", 0, 0, timescale, duration)
    else:
        head = struct.pack(">IIII", 0, 0, timescale, duration)
    return full("mvhd", version, head + struct.pack(">IH", 0x10000, 0x100) + bytes(10)
                + IDENTITY + bytes(24) + struct.pack(">I", 2))


def tkhd(width, height, version=0, matrix=IDENTITY):
    if version == 1:
        head = struct.pack(">QQIIQ", 0, 0, 1, 0, 0)
    else:
        head = struct.pack(">IIIII", 0, 0, 1, 0, 0)
    return full("tkhd", version, head + bytes(8) + struct.pack(">HHHH", 0, 0, 0, 0) + matrix
                + struct.pack(">II", width << 16, height << 16))


def mdhd(timescale, duration):
    return full("mdhd", 0, struct.pack(">IIIIHH", 0, 0, timescale, duration, 0x55C4, 0))


def hdlr(handler):
    return full("hdlr", 0, bytes(4) + handler + bytes(12) + b"\0")


def sample_entry(codec, width, height):
    return box(codec, bytes(6) + struct.pack(">H", 1) + bytes(16) + struct.pack(">HH", width, height)
               + struct.pack(">IIIH", 0x480000, 0x480000, 0, 1) + bytes(32)
               + struct.pack(">Hh", 24, -1))


def stsd(entry):
    return full("stsd", 0, struct.pack(">I", 1) + entry)


def video_trak(width, height, tk_version=0, matrix=IDENTITY, codec=b"avc1", timescale=1000,
               duration=8000):
    stbl = box("stbl", stsd(sample_entry(codec, width, height)))
    minf = box("minf", stbl)
    mdia = box("mdia", mdhd(timescale, duration) + hdlr(b"vide") + minf)
    return box("trak", tkhd(width, height, tk_version, matrix) + mdia)


def audio_trak():
    mdia = box("mdia", mdhd(48000, 384000) + hdlr(b"soun") + box("minf", box("stbl", stsd(box("mp4a", bytes(28))))))
    return box("trak", tkhd(0, 0) + mdia)


def mp4(width=720, height=1280, *, tk_version=0, mv_version=0, matrix=IDENTITY, large=False,
        moov_after_mdat=False, timescale=1000, duration=8000, audio=True, codec=b"avc1",
        extra=b""):
    ftyp = box("ftyp", b"isom" + struct.pack(">I", 512) + b"isomiso2avc1mp41")
    moov = box("moov", mvhd(timescale, duration, mv_version)
               + video_trak(width, height, tk_version, matrix, codec=codec,
                            timescale=timescale, duration=duration)
               + (audio_trak() if audio else b"") + extra, large=large)
    mdat = box("mdat", b"\0" * 32)
    return ftyp + (mdat + moov if moov_after_mdat else moov + mdat)


def png(width, height):
    ihdr = struct.pack(">II", width, height) + bytes([8, 6, 0, 0, 0])
    return (b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR" + ihdr + b"\0\0\0\0"
            + struct.pack(">I", 0) + b"IEND" + b"\0\0\0\0")


def jpeg(width, height, sof=0xC0):
    app0 = b"\xff\xe0" + struct.pack(">H", 16) + b"JFIF\0" + bytes(9)
    sof_seg = b"\xff" + bytes([sof]) + struct.pack(">HBHHB", 17, 8, height, width, 3) + bytes(9)
    # a fill byte, RST0 and TEM (standalone markers, no length) sit between APP0 and SOF
    return (b"\xff\xd8" + app0 + b"\xff\xff\xd0\xff\x01" + sof_seg + b"\xff\xda"
            + struct.pack(">H", 12) + bytes(10))


# ── tests ───────────────────────────────────────────────────────────────────

class RealArtifactTest(unittest.TestCase):
    def test_committed_jpegs_are_928_by_1152(self):
        self.assertEqual(len(JPEGS), 3)
        for path in JPEGS:
            info = artifact.probe(path.read_bytes())
            self.assertEqual((info.kind, info.container), ("image", "jpeg"), path.name)
            self.assertEqual((info.width, info.height), (928, 1152), path.name)
            self.assertIsNone(info.duration_s)

    def test_committed_mp4s_are_avc1_720_by_1280_8s_with_audio(self):
        self.assertEqual(len(MP4S), 3)
        for path in MP4S:
            info = artifact.probe(path.read_bytes())
            self.assertEqual((info.kind, info.container), ("video", "mp4"), path.name)
            self.assertEqual((info.width, info.height), (720, 1280), path.name)
            self.assertEqual(info.codec, "avc1", path.name)
            self.assertAlmostEqual(info.duration_s, 8.0, places=2, msg=path.name)
            self.assertTrue(info.has_video_track, path.name)
            self.assertTrue(info.has_audio_track, path.name)


class SyntheticTest(unittest.TestCase):
    def test_png_ihdr(self):
        info = artifact.probe(png(1000, 1000))
        self.assertEqual((info.kind, info.container, info.width, info.height),
                         ("image", "png", 1000, 1000))

    def test_jpeg_sof_variants_and_standalone_markers(self):
        for sof in (0xC0, 0xC1, 0xC2):
            info = artifact.probe(jpeg(640, 480, sof))
            self.assertEqual((info.width, info.height), (640, 480), hex(sof))

    def test_mp4_tkhd_v0_and_v1_and_mvhd_v1(self):
        for tk, mv in ((0, 0), (1, 0), (0, 1), (1, 1)):
            info = artifact.probe(mp4(tk_version=tk, mv_version=mv))
            self.assertEqual((info.width, info.height), (720, 1280), (tk, mv))
            self.assertEqual(info.duration_s, 8.0, (tk, mv))
            self.assertTrue(info.has_audio_track)

    def test_mp4_largesize_box_and_moov_after_mdat(self):
        info = artifact.probe(mp4(large=True, moov_after_mdat=True))
        self.assertEqual((info.width, info.height, info.duration_s), (720, 1280, 8.0))

    def test_mp4_rotated_matrix_swaps_dimensions(self):
        info = artifact.probe(mp4(1280, 720, matrix=ROT90))
        self.assertEqual((info.width, info.height), (720, 1280))
        self.assertIn("rotat", " ".join(info.notes))

    def test_mp4_other_codecs_and_no_audio(self):
        info = artifact.probe(mp4(codec=b"hvc1", audio=False))
        self.assertEqual(info.codec, "hvc1")
        self.assertFalse(info.has_audio_track)

    def test_fragmented_mp4_has_no_duration(self):
        data = mp4(duration=0) + box("moof", b"")
        info = artifact.probe(data)
        self.assertEqual((info.width, info.height), (720, 1280))
        self.assertIsNone(info.duration_s)
        self.assertIn("fragmented", " ".join(info.notes))

    def test_mdhd_cross_checks_mvhd(self):
        info = artifact.probe(mp4(timescale=1000, duration=8000))
        self.assertEqual(info.duration_s, 8.0)

    # ── refusals ────────────────────────────────────────────────────────
    def test_truncated_jpeg_without_sof_is_a_probe_error(self):
        with self.assertRaises(artifact.ProbeError):
            artifact.probe(b"\xff\xd8\xff\xe0\x00\x10JFIF\0" + bytes(9) + b"\xff\xda\x00\x0c")
        with self.assertRaises(artifact.ProbeError):
            artifact.probe(b"\xff\xd8\xff\xe0\x00\x10JFIF")

    def test_mp4_without_moov_is_a_probe_error(self):
        with self.assertRaises(artifact.ProbeError):
            artifact.probe(box("ftyp", b"isom" + bytes(4)) + box("mdat", bytes(8)))

    def test_truncated_png_is_a_probe_error(self):
        with self.assertRaises(artifact.ProbeError):
            artifact.probe(b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR")

    def test_unrecognised_bytes_are_a_probe_error(self):
        with self.assertRaises(artifact.ProbeError):
            artifact.probe(b"not an artifact at all" * 4)

    def test_gif_and_webp_are_unsupported_not_errors(self):
        info = artifact.probe(b"GIF89a" + bytes(20))
        self.assertEqual((info.kind, info.container), ("unknown", "gif"))
        self.assertIsNone(info.width)
        info = artifact.probe(b"RIFF" + bytes(4) + b"WEBPVP8 " + bytes(20))
        self.assertEqual((info.kind, info.container), ("unknown", "webp"))
        info = artifact.probe(box("ftyp", b"heic" + bytes(4) + b"mif1heic"))
        self.assertEqual((info.kind, info.container), ("unknown", "heic"))


class AspectTest(unittest.TestCase):
    def test_tolerance_boundary(self):
        self.assertTrue(artifact.aspect_matches(928, 1152, "4:5")[0])    # delta 0.0056
        self.assertTrue(artifact.aspect_matches(720, 1280, "9:16")[0])   # exact
        self.assertFalse(artifact.aspect_matches(1000, 1000, "4:5")[0])
        self.assertTrue(artifact.aspect_matches(810, 1000, "4:5")[0])    # delta 0.010 (<=)
        self.assertFalse(artifact.aspect_matches(812, 1000, "4:5")[0])   # delta 0.012
        ok, ratio, target = artifact.aspect_matches(928, 1152, "4:5")
        self.assertAlmostEqual(ratio, 0.8056, places=4)
        self.assertAlmostEqual(target, 0.8, places=4)

    def test_malformed_aspect_is_refused(self):
        with self.assertRaises(ValueError):
            artifact.aspect_matches(10, 10, "square")


if __name__ == "__main__":
    unittest.main()
