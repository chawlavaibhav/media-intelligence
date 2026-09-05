"""Test (k): every deterministic instrument on constructed fixtures (<= 64x64, generated in the temp dir).

Rules proven here: an unparseable input yields absent / parse_failure and never pass; a missing tool yields
absent / instrument_unavailable; while PASS-CRITERIA-v0.yaml says frozen: false the instrument STORES its
measurement but returns absent / other with the note criterion_not_frozen; with a frozen criteria file
(a test-only override, never the committed one) the same measurement becomes pass or fail.
"""
import json
import math
import shutil
import unittest
from pathlib import Path

import yaml

from _support import NoNetworkTestCase, hv2_paths
from instruments import imageio as IO
from instruments import common as C

HAVE_FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


def solid(w, h, rgb):
    return [bytes(rgb) * w for _ in range(h)]


def png_file(path, rows, w, h, channels=3):
    Path(path).write_bytes(IO.encode_png(rows, w, h, channels=channels))
    return Path(path)


def mask_rows(w, h, box):
    """White inside box=(x0,y0,x1,y1) (the changed region), black elsewhere."""
    x0, y0, x1, y1 = box
    return [b"".join((b"\xff\xff\xff" if (x0 <= x < x1 and y0 <= y < y1) else b"\x00\x00\x00") for x in range(w)) for y in range(h)]


class CriteriaFileTest(NoNetworkTestCase):
    """Tester check 7 made mechanical: every instrument has an entry; every entry is frozen: false with a source."""

    def test_every_instrument_has_a_proposed_unfrozen_entry(self):
        crit = C.load_criteria()
        self.assertEqual(crit["status"], "PROPOSED_NOT_FROZEN")
        for iid in ("format_probe", "masked_diff", "brand_colour", "av_offset", "repeat_consistency", "ledger_metrics", "gate_wrapper"):
            with self.subTest(instrument=iid):
                c = C.criterion(iid)
                self.assertFalse(c.frozen)
                self.assertIn(c.status, ("proposed", "observation_only_never_a_row"))
                self.assertTrue(c.source)
                self.assertTrue(c.source.startswith("Planner proposal") or "/" in c.source or "verified: false" in c.source or "task EVAL-039C" in c.source or "coordination/" in c.source)
                self.assertEqual(c.controller_ref, "MD-C1")

    def test_gate_rule_returns_absent_until_frozen_and_pass_fail_after(self):
        c = C.criterion("masked_diff")
        r = C.gate(c, True, {"mae": 1.0})
        self.assertEqual((r["verdict"], r["absence_reason"], r["note"]), ("absent", "other", "criterion_not_frozen"))
        self.assertEqual(r["measurement"]["mae"], 1.0)
        self.assertEqual(r["would_verdict"], "pass")
        frozen = self.freeze("masked_diff")
        c2 = C.criterion("masked_diff", frozen)
        self.assertTrue(c2.frozen)
        self.assertEqual(C.gate(c2, True, {})["verdict"], "pass")
        self.assertEqual(C.gate(c2, False, {}, defects=[{"term": "x"}])["verdict"], "fail")
        self.assertEqual(C.gate(c2, False, {}, defects=[{"term": "x"}])["defects"][0]["observed_by"], "instrument")

    def test_absence_helpers_never_pass(self):
        self.assertEqual(C.parse_failure("bad")["verdict"], "absent")
        self.assertEqual(C.parse_failure("bad")["absence_reason"], "parse_failure")
        self.assertEqual(C.unavailable("no ffmpeg")["absence_reason"], "instrument_unavailable")

    def test_instrument_factory_config_hash_covers_thresholds(self):
        from instruments import masked_diff as MD
        a = MD.instrument()
        b = MD.instrument(criteria_path=self.freeze("masked_diff"))
        self.assertEqual(a.qualification_status, "deterministic")
        self.assertNotEqual(a.config_hash, b.config_hash, "freezing / changing a threshold must change the instrument identity")
        self.assertEqual(a.capabilities, {"edit_preservation"})
        self.assertTrue(a.registry_writable)

    # helper shared by the classes below
    def freeze(self, iid, **overrides):
        return freeze_criteria(self, iid, **overrides)


def freeze_criteria(tc, iid, **overrides):
    """Write a TEST-ONLY criteria file with `iid` frozen (never touches the committed file)."""
    d = C.load_criteria()
    d["criteria"][iid]["frozen"] = True
    d["criteria"][iid]["status"] = "frozen_TEST_ONLY"
    for k, v in overrides.items():
        d["criteria"][iid]["thresholds"][k] = v
    p = tc.tmp / f"criteria-{iid}.yaml"
    p.write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False))
    return p


# ------------------------------------------------------------------------------ masked_diff
class MaskedDiffTest(NoNetworkTestCase):
    def setUp(self):
        super().setUp()
        from instruments import masked_diff as MD
        self.MD = MD
        w, h = 32, 24
        self.w, self.h = w, h
        base = [bytes(b"".join(bytes(((x * 7) % 256, (y * 9) % 256, ((x + y) * 3) % 256)) for x in range(w))) for y in range(h)]
        self.inp = png_file(self.tmp / "in.png", base, w, h)
        self.same = png_file(self.tmp / "same.png", base, w, h)
        # change only inside the mask box
        box = (8, 8, 16, 16)
        inside = [bytes(b"".join((b"\xff\x00\x00" if (box[0] <= x < box[2] and box[1] <= y < box[3]) else base[y][3 * x:3 * x + 3]) for x in range(w))) for y in range(h)]
        self.inside = png_file(self.tmp / "inside.png", inside, w, h)
        outside = [bytes(b"".join((b"\x00\x00\x00" if x < 10 else base[y][3 * x:3 * x + 3]) for x in range(w))) for y in range(h)]
        self.outside = png_file(self.tmp / "outside.png", outside, w, h)
        self.mask = png_file(self.tmp / "mask.png", mask_rows(w, h, box), w, h)

    def test_identical_is_zero_and_one(self):
        m = self.MD.measure(self.inp, self.same, self.mask)
        self.assertEqual(m["mae_outside_mask"], 0.0)
        self.assertAlmostEqual(m["ssim_outside_mask"], 1.0, places=6)
        self.assertEqual(m["mask_sha256"], IO.__name__ and __import__("hashlib").sha256(self.mask.read_bytes()).hexdigest())

    def test_change_inside_mask_is_ignored_change_outside_is_measured(self):
        m_in = self.MD.measure(self.inp, self.inside, self.mask)
        self.assertEqual(m_in["mae_outside_mask"], 0.0)
        m_out = self.MD.measure(self.inp, self.outside, self.mask)
        self.assertGreater(m_out["mae_outside_mask"], 8.0)
        self.assertLess(m_out["ssim_outside_mask"], 0.99)

    def test_output_is_resized_to_the_input_size(self):
        big = png_file(self.tmp / "big.png", solid(64, 48, (10, 20, 30)), 64, 48)
        small_in = png_file(self.tmp / "small.png", solid(32, 24, (10, 20, 30)), 32, 24)
        m = self.MD.measure(small_in, big, png_file(self.tmp / "m2.png", mask_rows(32, 24, (0, 0, 1, 1)), 32, 24))
        self.assertEqual(m["mae_outside_mask"], 0.0)
        self.assertEqual(m["resized_output_to"], [32, 24])

    def test_verdicts(self):
        r = self.MD.evaluate(self.inp, self.same, self.mask)
        self.assertEqual((r["verdict"], r["note"]), ("absent", "criterion_not_frozen"))
        self.assertEqual(r["would_verdict"], "pass")
        frozen = freeze_criteria(self, "masked_diff")
        self.assertEqual(self.MD.evaluate(self.inp, self.same, self.mask, criteria_path=frozen)["verdict"], "pass")
        bad = self.MD.evaluate(self.inp, self.outside, self.mask, criteria_path=frozen)
        self.assertEqual(bad["verdict"], "fail")
        self.assertTrue(bad["defects"])

    def test_fail_closed(self):
        corrupt = self.tmp / "c.png"
        corrupt.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 40)
        r = self.MD.evaluate(self.inp, corrupt, self.mask, criteria_path=freeze_criteria(self, "masked_diff"))
        self.assertEqual((r["verdict"], r["absence_reason"]), ("absent", "parse_failure"))
        r2 = self.MD.evaluate(self.inp, self.same, self.tmp / "missing-mask.png", criteria_path=freeze_criteria(self, "masked_diff"))
        self.assertEqual((r2["verdict"], r2["absence_reason"]), ("absent", "parse_failure"))
        wrong_mask = png_file(self.tmp / "wm.png", mask_rows(8, 8, (0, 0, 2, 2)), 8, 8)
        r3 = self.MD.evaluate(self.inp, self.same, wrong_mask)
        self.assertEqual(r3["absence_reason"], "parse_failure")


# ------------------------------------------------------------------------------ brand_colour
class BrandColourTest(NoNetworkTestCase):
    def test_lab_conversion_reference_values(self):
        from instruments import brand_colour as BC
        L, a, b = BC.srgb_to_lab((255, 255, 255))
        self.assertAlmostEqual(L, 100.0, places=2)
        self.assertAlmostEqual(a, 0.0, places=1)
        self.assertAlmostEqual(b, 0.0, places=1)
        L, a, b = BC.srgb_to_lab((255, 0, 0))
        self.assertAlmostEqual(L, 53.24, delta=0.1)
        self.assertAlmostEqual(a, 80.09, delta=0.2)
        self.assertAlmostEqual(b, 67.20, delta=0.2)
        self.assertAlmostEqual(BC.delta_e76((50, 0, 0), (50, 3, 4)), 5.0, places=6)

    def test_mean_colour_in_mask_and_delta_e(self):
        from instruments import brand_colour as BC
        w, h = 24, 16
        rows = [bytes(b"".join((b"\x10\x60\xa0" if x < 12 else b"\xf0\xf0\xf0") for x in range(w))) for y in range(h)]
        img = png_file(self.tmp / "pack.png", rows, w, h)
        mask = png_file(self.tmp / "mask.png", mask_rows(w, h, (0, 0, 12, h)), w, h)
        m = BC.measure(img, mask, (0x10, 0x60, 0xA0))
        self.assertEqual(m["mean_srgb_in_mask"], [16, 96, 160])
        self.assertAlmostEqual(m["delta_e_ab"], 0.0, places=6)
        far = BC.measure(img, mask, (0xF0, 0xF0, 0xF0))
        self.assertGreater(far["delta_e_ab"], 30)
        r = BC.evaluate(img, mask, (0x10, 0x60, 0xA0))
        self.assertEqual((r["verdict"], r["note"], r["would_verdict"]), ("absent", "criterion_not_frozen", "pass"))
        frozen = freeze_criteria(self, "brand_colour")
        self.assertEqual(BC.evaluate(img, mask, (0x10, 0x60, 0xA0), criteria_path=frozen)["verdict"], "pass")
        self.assertEqual(BC.evaluate(img, mask, (0xF0, 0xF0, 0xF0), criteria_path=frozen)["verdict"], "fail")
        empty = png_file(self.tmp / "empty.png", mask_rows(w, h, (0, 0, 0, 0)), w, h)
        self.assertEqual(BC.evaluate(img, empty, (1, 2, 3), criteria_path=frozen)["absence_reason"], "parse_failure")
        self.assertEqual(BC.evaluate(self.tmp / "nope.png", mask, (1, 2, 3), criteria_path=frozen)["absence_reason"], "parse_failure")


# ------------------------------------------------------------------------------ av_offset
CLICK_GAPS_S = (0.23, 0.41, 0.17, 0.35, 0.29, 0.19, 0.37)     # APERIODIC on purpose: a periodic train has no unique lag


def click_train(seconds=2.4, rate=16000, offset_s=0.0, click_ms=5, amp=16000):
    n = int(seconds * rate)
    s = [0] * n
    t = offset_s
    for gap in CLICK_GAPS_S * 2:
        if t >= seconds:
            break
        i0 = int(t * rate)
        for i in range(i0, min(n, i0 + int(click_ms * rate / 1000))):
            s[i] = amp if (i - i0) % 2 == 0 else -amp
        t += gap
    return s


@unittest.skipUnless(HAVE_FFMPEG, "ffmpeg/ffprobe genuinely absent on this machine")
class AvOffsetTest(NoNetworkTestCase):
    def test_shifted_click_train_gives_the_shift(self):
        from instruments import av_offset as AV
        drive = IO.write_wav(self.tmp / "drive.wav", click_train(offset_s=0.10), 16000)
        late = IO.write_wav(self.tmp / "late.wav", click_train(offset_s=0.22), 16000)     # artifact audio lags by 120 ms
        m = AV.measure(drive, late)
        self.assertAlmostEqual(m["lag_ms"], 120, delta=10)
        self.assertGreater(m["peak_correlation"], 0.5)
        self.assertEqual(m["rate_hz"], 16000)
        self.assertEqual(m["envelope_step_ms"], 10)
        m0 = AV.measure(drive, drive)
        self.assertAlmostEqual(m0["lag_ms"], 0, delta=10)
        early = IO.write_wav(self.tmp / "early.wav", click_train(offset_s=0.04), 16000)
        self.assertAlmostEqual(AV.measure(drive, early)["lag_ms"], -60, delta=10)

    def test_video_container_audio_track_is_decoded(self):
        from instruments import av_offset as AV
        drive = IO.write_wav(self.tmp / "drive.wav", click_train(offset_s=0.10), 16000)
        late = IO.write_wav(self.tmp / "late.wav", click_train(offset_s=0.22), 16000)
        clip = self.tmp / "clip.mov"
        IO.make_test_video(clip, width=32, height=32, seconds=2.4, fps=5, audio_path=late, audio_codec="pcm_s16le")
        m = AV.measure(drive, clip)
        self.assertAlmostEqual(m["lag_ms"], 120, delta=15)

    def test_verdicts_and_fail_closed(self):
        from instruments import av_offset as AV
        drive = IO.write_wav(self.tmp / "drive.wav", click_train(offset_s=0.10), 16000)
        late = IO.write_wav(self.tmp / "late.wav", click_train(offset_s=0.22), 16000)
        near = IO.write_wav(self.tmp / "near.wav", click_train(offset_s=0.13), 16000)
        r = AV.evaluate(drive, near)
        self.assertEqual((r["verdict"], r["note"], r["would_verdict"]), ("absent", "criterion_not_frozen", "pass"))
        self.assertEqual(r["claim"], "partial: audio_track_offset_vs_drive")
        frozen = freeze_criteria(self, "av_offset")
        self.assertEqual(AV.evaluate(drive, near, criteria_path=frozen)["verdict"], "pass")
        self.assertEqual(AV.evaluate(drive, late, criteria_path=frozen)["verdict"], "fail")
        garbage = self.tmp / "g.wav"
        garbage.write_bytes(b"RIFF....WAVEjunk" * 10)
        self.assertEqual(AV.evaluate(drive, garbage, criteria_path=frozen)["absence_reason"], "parse_failure")
        silence = IO.write_wav(self.tmp / "s.wav", [0] * 38400, 16000)
        r2 = AV.evaluate(drive, silence, criteria_path=frozen)
        self.assertEqual(r2["verdict"], "absent")
        self.assertIn("no alignment", r2["note"])

    def test_missing_ffmpeg_is_instrument_unavailable(self):
        from instruments import av_offset as AV
        drive = IO.write_wav(self.tmp / "d.wav", click_train(), 16000)
        saved = IO.FFMPEG_BIN, IO.FFPROBE_BIN
        try:
            IO.FFMPEG_BIN = IO.FFPROBE_BIN = "ffmpeg-definitely-not-installed"
            r = AV.evaluate(drive, drive, criteria_path=freeze_criteria(self, "av_offset"))
            self.assertEqual((r["verdict"], r["absence_reason"]), ("absent", "instrument_unavailable"))
        finally:
            IO.FFMPEG_BIN, IO.FFPROBE_BIN = saved


# ------------------------------------------------------------------------------ format_probe
@unittest.skipUnless(HAVE_FFMPEG, "ffmpeg/ffprobe genuinely absent on this machine")
class FormatProbeTest(NoNetworkTestCase):
    def setUp(self):
        super().setUp()
        from instruments import format_probe as FP
        self.FP = FP
        self.clip = IO.make_test_video(self.tmp / "clip.mp4", width=64, height=48, seconds=1.0, fps=10, with_audio=True)
        self.silent = IO.make_test_video(self.tmp / "silent.mp4", width=64, height=48, seconds=1.0, fps=10, with_audio=False)
        self.case = {"conditions": {"COND-DELIVERY": {"aspect_ratio": "4:3", "resolution": "48p-class (test)", "duration_s": 1, "fps": 10}},
                     "params": {"aspect": "4:3", "duration_s": 1, "audio": "on", "resolution": "48p"}}

    def test_measurement_and_comparison(self):
        m = self.FP.measure(self.clip, self.case)
        self.assertEqual((m["probe"]["width"], m["probe"]["height"], m["probe"]["aspect"]), (64, 48, "4:3"))
        self.assertTrue(m["probe"]["has_audio"])
        self.assertTrue(m["checks"]["aspect_ok"])
        self.assertTrue(m["checks"]["duration_ok"])
        self.assertTrue(m["checks"]["audio_ok"])
        r = self.FP.evaluate(self.clip, self.case)
        self.assertEqual((r["verdict"], r["note"], r["would_verdict"]), ("absent", "criterion_not_frozen", "pass"))
        frozen = freeze_criteria(self, "format_probe")
        self.assertEqual(self.FP.evaluate(self.clip, self.case, criteria_path=frozen)["verdict"], "pass")
        bad = self.FP.evaluate(self.silent, self.case, criteria_path=frozen)
        self.assertEqual(bad["verdict"], "fail")
        self.assertIn("audio", " ".join(d["term"] for d in bad["defects"]))
        wrong = {**self.case, "params": {**self.case["params"], "aspect": "9:16"}}
        self.assertEqual(self.FP.evaluate(self.clip, wrong, criteria_path=frozen)["verdict"], "fail")

    def test_image_probe_and_fail_closed(self):
        img = png_file(self.tmp / "i.png", solid(40, 50, (1, 2, 3)), 40, 50)
        case = {"conditions": {"COND-DELIVERY": {"aspect_ratio": "4:5", "duration_s": "not_applicable", "fps": "not_applicable"}},
                "params": {"aspect": "4:5", "audio": "not_applicable", "resolution": "~1 MP (1024-class)"}}
        m = self.FP.measure(img, case)
        self.assertEqual(m["probe"]["aspect"], "4:5")
        self.assertTrue(m["checks"]["aspect_ok"] and m["checks"]["audio_ok"] and m["checks"]["duration_ok"])
        self.assertFalse(m["checks"]["resolution_class_ok"])          # 40x50 is not 1024-class
        frozen = freeze_criteria(self, "format_probe")
        self.assertEqual(self.FP.evaluate(img, case, criteria_path=frozen)["verdict"], "fail")
        junk = self.tmp / "junk.mp4"
        junk.write_bytes(b"\x00" * 100)
        self.assertEqual(self.FP.evaluate(junk, case, criteria_path=frozen)["absence_reason"], "parse_failure")
        saved = IO.FFMPEG_BIN, IO.FFPROBE_BIN
        try:
            IO.FFMPEG_BIN = IO.FFPROBE_BIN = "ffprobe-definitely-not-installed"
            self.assertEqual(self.FP.evaluate(img, case, criteria_path=frozen)["absence_reason"], "instrument_unavailable")
        finally:
            IO.FFMPEG_BIN, IO.FFPROBE_BIN = saved


# ------------------------------------------------------------------------------ repeat_consistency
class RepeatConsistencyTest(NoNetworkTestCase):
    def _img(self, name, rows, w=32, h=24):
        return png_file(self.tmp / name, rows, w, h)

    def test_dhash_and_ssim_between_repeats(self):
        from instruments import repeat_consistency as RC
        base = [bytes(b"".join(bytes(((x * 8) % 256, (y * 10) % 256, 128)) for x in range(32))) for y in range(24)]
        a = self._img("a.png", base)
        b = self._img("b.png", base)
        pert = [bytes(b"".join(bytes((min(255, base[y][3 * x] + 3), base[y][3 * x + 1], base[y][3 * x + 2])) for x in range(32))) for y in range(24)]
        c = self._img("c.png", pert)
        d = self._img("d.png", [bytes(b"".join(bytes((255 - base[y][3 * x], 30, (x * y) % 256)) for x in range(32))) for y in range(24)])
        self.assertEqual(RC.dhash(IO.decode_png(a.read_bytes())), RC.dhash(IO.decode_png(b.read_bytes())))
        m = RC.measure(a, b, seed_policy="unset")
        self.assertEqual(m["dhash_hamming_max"], 0)
        self.assertAlmostEqual(m["ssim_min"], 1.0, places=6)
        self.assertEqual(m["group"], "unseeded")
        self.assertTrue(m["same_probed_format"])
        m2 = RC.measure(a, c, seed_policy="unset")
        self.assertLessEqual(m2["dhash_hamming_max"], 4)
        m3 = RC.measure(a, d, seed_policy="unset")
        self.assertGreater(m3["dhash_hamming_max"], 10)
        self.assertLess(m3["ssim_min"], 0.9)

    def test_groups_are_never_pooled_and_verdicts_follow_the_group(self):
        from instruments import repeat_consistency as RC
        horiz = [bytes(b"".join(bytes(((x * 16) % 256,) * 3) for x in range(16))) for y in range(16)]
        vert = [bytes(b"".join(bytes(((y * 16) % 256,) * 3) for x in range(16))) for y in range(16)]
        a = self._img("a.png", horiz, 16, 16)
        b = self._img("b.png", vert, 16, 16)
        r = RC.evaluate(a, b, seed_policy="unset")
        self.assertEqual((r["verdict"], r["note"]), ("absent", "criterion_not_frozen"))
        self.assertEqual(r["measurement"]["group"], "unseeded")
        self.assertEqual(r["would_verdict"], "pass")                      # structural reproducibility: both valid PNGs
        frozen = freeze_criteria(self, "repeat_consistency")
        self.assertEqual(RC.evaluate(a, b, seed_policy="unset", criteria_path=frozen)["verdict"], "pass")
        held = RC.evaluate(a, b, seed_policy="held", criteria_path=frozen)
        self.assertEqual(held["measurement"]["group"], "held_seed")
        self.assertEqual(held["verdict"], "fail")
        with self.assertRaises(ValueError):
            RC.measure(a, b, seed_policy="mixed")

    def test_fail_closed(self):
        from instruments import repeat_consistency as RC
        a = self._img("a.png", solid(8, 8, (1, 1, 1)), 8, 8)
        bad = self.tmp / "bad.png"
        bad.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 30)
        r = RC.evaluate(a, bad, seed_policy="unset", criteria_path=freeze_criteria(self, "repeat_consistency"))
        self.assertEqual((r["verdict"], r["absence_reason"]), ("absent", "parse_failure"))

    @unittest.skipUnless(HAVE_FFMPEG, "ffmpeg/ffprobe genuinely absent on this machine")
    def test_video_uses_first_middle_last_frames(self):
        from instruments import repeat_consistency as RC
        v1 = IO.make_test_video(self.tmp / "v1.mp4", width=32, height=32, seconds=1.0, fps=5, with_audio=False)
        v2 = IO.make_test_video(self.tmp / "v2.mp4", width=32, height=32, seconds=1.0, fps=5, with_audio=False)
        m = RC.measure(v1, v2, seed_policy="unset")
        self.assertEqual(m["frames_compared"], ["first", "middle", "last"])
        self.assertEqual(len(m["per_frame"]), 3)
        self.assertLessEqual(m["dhash_hamming_max"], 2)


# ------------------------------------------------------------------------------ ledger_metrics
class LedgerMetricsTest(NoNetworkTestCase):
    def _attempt(self, tid, status, t0, t1, reserved="0.100000", error_class=None, spent=None):
        return {"trial_id": tid, "attempt_id": tid, "case_id": "C", "route_key": "r", "arm": "a", "status": status,
                "error_class": error_class, "requested_at": t0, "completed_at": t1, "reserved_amount_usd_equiv": reserved,
                "cost_ref": f"cost-res-{tid}", "reservation_id": f"res-{tid}", "billing_state": "reported"}

    def _ledger(self, tid, amount):
        return [{"type": "reservation", "reservation_id": f"res-{tid}", "amount_usd": "0.100000", "cost_ref": f"cost-res-{tid}", "trial_id": tid},
                {"type": "spend", "reservation_id": f"res-{tid}", "amount_usd": amount, "cost_ref": f"cost-res-{tid}", "trial_id": tid}]

    def test_cell_metrics(self):
        from instruments import ledger_metrics as LM
        attempts = [self._attempt("t1", "ok", "2026-09-05T00:00:00Z", "2026-09-05T00:00:04Z"),
                    self._attempt("t2", "ok", "2026-09-05T00:00:00Z", "2026-09-05T00:00:10Z"),
                    self._attempt("t3", "refusal", "2026-09-05T00:00:00Z", "2026-09-05T00:00:01Z", error_class="moderation_block"),
                    self._attempt("t4", "timeout", "2026-09-05T00:00:00Z", None, error_class="poll_budget_exhausted")]
        ledger = sum((self._ledger(t, a) for t, a in (("t1", "0.100000"), ("t2", "0.100000"), ("t3", "0.100000"), ("t4", "0.100000"))), [])
        m = LM.cell_metrics(attempts, ledger)
        self.assertEqual(m["n_attempts"], 4)
        self.assertEqual(m["status_counts"], {"ok": 2, "refusal": 1, "timeout": 1})
        self.assertEqual(m["error_class_counts"], {"moderation_block": 1, "poll_budget_exhausted": 1})
        self.assertEqual(m["refusal_rate"], 0.25)
        self.assertEqual(m["latency_s"]["p50"], 4.0)
        self.assertEqual(m["latency_s"]["p95"], 10.0)
        self.assertEqual(m["latency_s"]["n"], 3)
        self.assertEqual(m["settled_total_usd_equiv"], "0.400000")

    def test_per_trial_verdicts(self):
        from instruments import ledger_metrics as LM
        ok = self._attempt("t1", "ok", "2026-09-05T00:00:00Z", "2026-09-05T00:00:04Z")
        ledger = self._ledger("t1", "0.100000")
        r = LM.evaluate(ok, ledger, "latency_errors_refusals")
        self.assertEqual((r["verdict"], r["note"], r["would_verdict"]), ("absent", "criterion_not_frozen", "pass"))
        self.assertEqual(r["measurement"]["latency_s"], 4.0)
        frozen = freeze_criteria(self, "ledger_metrics")
        self.assertEqual(LM.evaluate(ok, ledger, "latency_errors_refusals", criteria_path=frozen)["verdict"], "pass")
        bad = self._attempt("t2", "error", "2026-09-05T00:00:00Z", "2026-09-05T00:00:04Z", error_class="http_500")
        self.assertEqual(LM.evaluate(bad, self._ledger("t2", "0.100000"), "latency_errors_refusals", criteria_path=frozen)["verdict"], "fail")
        c = LM.evaluate(ok, ledger, "cost_and_cpao", criteria_path=frozen)
        self.assertEqual(c["verdict"], "pass")
        self.assertEqual(c["measurement"]["settled_usd_equiv"], "0.100000")
        self.assertEqual(c["measurement"]["cpao"], {"verdict": "absent", "absence_reason": "not_applicable"})
        over = LM.evaluate(ok, self._ledger("t1", "0.250000"), "cost_and_cpao", criteria_path=frozen)
        self.assertEqual(over["verdict"], "fail")
        missing = LM.evaluate(ok, [], "cost_and_cpao", criteria_path=frozen)
        self.assertEqual((missing["verdict"], missing["absence_reason"]), ("absent", "parse_failure"))
        with self.assertRaises(ValueError):
            LM.evaluate(ok, ledger, "edit_preservation", criteria_path=frozen)


# ------------------------------------------------------------------------------ gate_wrapper
class GateWrapperTest(NoNetworkTestCase):
    def test_not_available_on_this_base(self):
        from instruments import gate_wrapper as GW
        self.assertFalse((hv2_paths.REPO_ROOT / "canon" / "gate" / "run_gate.py").exists(), "this branch must not carry the gate")
        r = GW.run_post(self.tmp / "a.png", self.tmp / "a.request.json", "static_image")
        self.assertEqual(r["status"], "not_available_on_base")
        self.assertTrue(r["base"])
        inst = GW.instrument()
        self.assertEqual(inst.qualification_status, "provisional")
        self.assertFalse(inst.registry_writable)
        self.assertEqual(inst.capabilities, set())
        out = inst.fn(self.tmp / "a.png", {"item_id": "x"}, "delivery_format_compliance")
        self.assertEqual((out["verdict"], out["absence_reason"]), ("absent", "instrument_unavailable"))
        self.assertEqual(out["observation"]["status"], "not_available_on_base")

    def test_scripted_gate_is_run_via_subprocess_and_parsed(self):
        from instruments import gate_wrapper as GW
        fake = self.tmp / "run_gate.py"
        fake.write_text("import json,sys\nargs=sys.argv[1:]\nout=args[args.index('--json')+1]\n"
                        "json.dump({'verdict':'PASS','findings':[],'argv':args}, open(out,'w'))\nprint('PASS')\n")
        art = self.tmp / "a.png"
        art.write_bytes(b"x")
        req = self.tmp / "a.request.json"
        req.write_text("{}")
        r = GW.run_post(art, req, "static_image", gate_script=fake)
        self.assertEqual(r["status"], "ran")
        self.assertEqual(r["report"]["verdict"], "PASS")
        self.assertIn("--modality", r["report"]["argv"])
        self.assertEqual(r["exit_code"], 0)


if __name__ == "__main__":
    unittest.main()
