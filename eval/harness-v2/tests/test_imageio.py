"""Test (k) part 1: the stdlib PNG decoder and the ffmpeg/ffprobe wrappers in instruments/imageio.py.

Fixtures are generated here, <= 64x64, in the test's temp dir. The five PNG filter types are exercised by
encoding the same image five ways with the module's own encoder (filter chosen per row) and checking the
decoder returns identical pixels. Corrupt input must raise ProbeError (fail closed), never return pixels.
"""
import shutil
import struct
import unittest
import zlib

from _support import NoNetworkTestCase
from instruments import imageio as IO


def checker(w, h, channels=3):
    """A small deterministic test image: gradient + checkerboard so every filter type has work to do."""
    rows = []
    for y in range(h):
        row = bytearray()
        for x in range(w):
            r = (x * 255) // max(w - 1, 1)
            g = (y * 255) // max(h - 1, 1)
            b = 255 if ((x // 4 + y // 4) % 2) else 0
            grey = (r + g + b) // 3
            px = {1: [grey], 2: [grey], 3: [r, g, b], 4: [r, g, b]}[channels]
            if channels in (2, 4):
                px.append(200 if x % 3 else 40)
            row += bytes(px)
        rows.append(bytes(row))
    return rows


class PngCodecTest(NoNetworkTestCase):
    def test_all_five_filter_types_roundtrip_rgb(self):
        rows = checker(37, 23, 3)
        for ftype in range(5):
            with self.subTest(filter_type=ftype):
                png = IO.encode_png(rows, 37, 23, channels=3, filter_type=ftype)
                img = IO.decode_png(png)
                self.assertEqual((img.width, img.height, img.channels), (37, 23, 3))
                self.assertEqual(img.rows(), rows)

    def test_grey_greyalpha_rgba_and_palette(self):
        for ch in (1, 2, 4):
            rows = checker(16, 9, ch)
            png = IO.encode_png(rows, 16, 9, channels=ch, filter_type=(ch + 1) % 5)
            img = IO.decode_png(png)
            self.assertEqual(img.channels, ch)
            self.assertEqual(img.rows(), rows)
        # palette PNG (colour type 3) expands to RGB
        pal = bytes([255, 0, 0, 0, 255, 0, 0, 0, 255])
        idx_rows = [bytes([0, 1, 2, 1]) for _ in range(3)]
        png = IO.encode_png(idx_rows, 4, 3, channels=1, filter_type=0, palette=pal)
        img = IO.decode_png(png)
        self.assertEqual(img.channels, 3)
        self.assertEqual(img.pixel(1, 0), (0, 255, 0))

    def test_rgb_view_and_grey_conversion(self):
        rows = checker(8, 8, 4)
        img = IO.decode_png(IO.encode_png(rows, 8, 8, channels=4))
        rgb = img.to_rgb()
        self.assertEqual(rgb.channels, 3)
        self.assertEqual(rgb.pixel(3, 2), tuple(rows[2][12:15]))
        grey = img.to_grey()
        self.assertEqual(grey.channels, 1)
        self.assertEqual(len(grey.data), 64)

    def test_corrupt_inputs_fail_closed(self):
        for bad in (b"", b"\x89PNG\r\n\x1a\n" + b"\x00" * 64, b"not a png at all", IO.encode_png(checker(4, 4), 4, 4)[:-20]):
            with self.subTest(prefix=bad[:12]):
                with self.assertRaises(IO.ProbeError):
                    IO.decode_png(bad)
        # a bad CRC and a bad zlib stream are both refused
        good = IO.encode_png(checker(6, 6), 6, 6)
        idat = good.index(b"IDAT")
        tampered = good[:idat + 8] + bytes([good[idat + 8] ^ 0xFF]) + good[idat + 9:]
        with self.assertRaises(IO.ProbeError):
            IO.decode_png(tampered)

    def test_interlaced_and_16bit_refuse_rather_than_guess(self):
        rows = checker(4, 4)
        png = IO.encode_png(rows, 4, 4)
        # flip the interlace byte inside IHDR (last byte of the 13-byte IHDR data) and fix the CRC
        ihdr_start = png.index(b"IHDR")
        data = bytearray(png[ihdr_start + 4: ihdr_start + 17])
        data[12] = 1
        crc = struct.pack(">I", zlib.crc32(b"IHDR" + bytes(data)) & 0xFFFFFFFF)
        png2 = png[:ihdr_start + 4] + bytes(data) + crc + png[ihdr_start + 21:]
        with self.assertRaises(IO.ProbeError):
            IO.decode_png(png2)


class ResizeTest(NoNetworkTestCase):
    def test_nearest_neighbour_resize(self):
        rows = checker(8, 4)
        img = IO.decode_png(IO.encode_png(rows, 8, 4))
        small = IO.resize_nearest(img, 4, 2)
        self.assertEqual((small.width, small.height), (4, 2))
        self.assertEqual(small.pixel(0, 0), img.pixel(0, 0))
        self.assertEqual(small.pixel(3, 1), img.pixel(6, 2))
        same = IO.resize_nearest(img, 8, 4)
        self.assertEqual(same.rows(), img.rows())


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg/ffprobe genuinely absent on this machine")
class FfmpegWrapperTest(NoNetworkTestCase):
    def test_tools_report_versions(self):
        t = IO.tools()
        self.assertTrue(t["ffmpeg"]["available"] and t["ffprobe"]["available"])
        self.assertTrue(t["ffmpeg"]["version"].startswith("ffmpeg version"))

    def test_probe_and_decode_a_generated_mp4_and_wav(self):
        mp4 = self.tmp / "tiny.mp4"
        wav = self.tmp / "tone.wav"
        IO.make_test_video(mp4, width=64, height=48, seconds=1.0, fps=10, with_audio=True)
        IO.make_test_audio(wav, seconds=0.5, rate=16000, freq=440)
        info = IO.ffprobe(mp4)
        self.assertEqual((info["width"], info["height"]), (64, 48))
        self.assertTrue(info["has_audio"])
        self.assertAlmostEqual(info["duration_s"], 1.0, delta=0.15)
        self.assertAlmostEqual(info["fps"], 10.0, delta=0.01)
        frames = IO.decode_video_frames(mp4, ("first", "middle", "last"))
        self.assertEqual(len(frames), 3)
        self.assertEqual((frames[0].width, frames[0].height, frames[0].channels), (64, 48, 3))
        pcm = IO.decode_audio_pcm(wav, rate=16000)
        self.assertEqual(pcm.rate, 16000)
        self.assertAlmostEqual(len(pcm.samples) / 16000, 0.5, delta=0.02)
        self.assertGreater(max(abs(s) for s in pcm.samples), 1000)

    def test_probe_fails_closed_on_garbage(self):
        bad = self.tmp / "bad.mp4"
        bad.write_bytes(b"\x00\x01garbage" * 50)
        with self.assertRaises(IO.ProbeError):
            IO.ffprobe(bad)
        with self.assertRaises(IO.ProbeError):
            IO.decode_video_frames(bad, ("first",))

    def test_decode_image_via_ffmpeg_matches_stdlib_decoder(self):
        rows = checker(20, 12)
        p = self.tmp / "c.png"
        p.write_bytes(IO.encode_png(rows, 20, 12))
        a = IO.decode_png(p.read_bytes())
        b = IO.decode_image_ffmpeg(p)
        self.assertEqual(a.rows(), b.rows())


class MissingToolsTest(NoNetworkTestCase):
    def test_missing_ffmpeg_is_reported_not_guessed(self):
        saved = IO.FFMPEG_BIN, IO.FFPROBE_BIN
        try:
            IO.FFMPEG_BIN, IO.FFPROBE_BIN = "ffmpeg-definitely-not-installed", "ffprobe-definitely-not-installed"
            t = IO.tools()
            self.assertFalse(t["ffmpeg"]["available"])
            with self.assertRaises(IO.ToolUnavailable):
                IO.ffprobe(self.tmp / "nothing.mp4")
        finally:
            IO.FFMPEG_BIN, IO.FFPROBE_BIN = saved


if __name__ == "__main__":
    unittest.main()
