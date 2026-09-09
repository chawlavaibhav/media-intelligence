"""stack_audio.py: a music track laid under a clip for stacked judging - synthetic media only, ffmpeg local."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _support import NoNetworkTestCase  # noqa: E402

import stack_audio as SA  # noqa: E402
from instruments import imageio as IO  # noqa: E402


class StackAudioTest(NoNetworkTestCase):
    def test_track_is_trimmed_to_the_clip_and_ambience_is_kept(self):
        clip = IO.make_test_video(self.tmp / "clip.mp4", seconds=2.0, fps=10, with_audio=True)
        track = IO.make_test_audio(self.tmp / "track.wav", seconds=6.0, freq=220.0)
        out = self.tmp / "stacked.mp4"
        info = SA.stack(clip, track, out)
        p = SA.probe(out)
        self.assertTrue(p["has_audio"])
        self.assertAlmostEqual(p["duration_s"], 2.0, delta=0.25, msg="the stacked view is the clip's length, not the track's")
        self.assertTrue(info["clip_had_audio"] and info["judging_view_only"])

    def test_a_silent_clip_gets_the_music_alone(self):
        clip = IO.make_test_video(self.tmp / "clip.mp4", seconds=1.5, fps=10, with_audio=False)
        track = IO.make_test_audio(self.tmp / "track.wav", seconds=4.0)
        info = SA.stack(clip, track, self.tmp / "s.mp4")
        self.assertFalse(info["clip_had_audio"])
        self.assertTrue(SA.probe(self.tmp / "s.mp4")["has_audio"])


if __name__ == "__main__":
    unittest.main()
