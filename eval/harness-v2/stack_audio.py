#!/usr/bin/env python3
"""stack_audio: lay a generated music track under an accepted clip, for STACKED judging (Controller, 2026-09-09:
"combine one of the video tests with music one so collapsing 2 test classes into one").

    python3 eval/harness-v2/stack_audio.py --clip <accepted clip> --track <sealed music artifact> --out <mp4> [--music-gain 1.0] [--ambience-gain 0.35]

The stacked file is a JUDGING VIEW, never a sealed artifact and never a Registry input: the music contract is judged on
the raw track (duration, vocals, instrument colour, build), the stacked view answers "does it fit the cut". The track is
trimmed to the clip's length with a one-second fade-out; the clip's own audio (ambience), when present, is kept
underneath at `ambience_gain`. Video is stream-copied (no re-encode); audio is AAC. ffmpeg only, via instruments.imageio.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from instruments import imageio as IO


def probe(path: Path | str) -> dict:
    r = subprocess.run([IO.FFPROBE_BIN, "-v", "error", "-show_entries", "format=duration", "-show_streams", "-of", "json", str(path)],
                       capture_output=True, text=True, check=True)
    d = json.loads(r.stdout)
    return {"duration_s": float(d["format"]["duration"]), "has_audio": any(s.get("codec_type") == "audio" for s in d.get("streams", []))}


def stack(clip: Path | str, track: Path | str, out: Path | str, music_gain: float = 1.0, ambience_gain: float = 0.35, fade_s: float = 1.0) -> dict:
    IO._require(IO.FFMPEG_BIN, "ffmpeg")
    clip, track, out = Path(clip), Path(track), Path(out)
    info = probe(clip)
    d = info["duration_s"]
    fade_start = max(d - fade_s, 0.0)
    music = f"[1:a]atrim=0:{d:.3f},asetpts=PTS-STARTPTS,afade=t=out:st={fade_start:.3f}:d={fade_s},volume={music_gain}[m]"
    if info["has_audio"]:
        graph = f"{music};[0:a]volume={ambience_gain}[amb];[amb][m]amix=inputs=2:duration=first:dropout_transition=0[a]"
    else:
        graph = f"{music};[m]anull[a]"
    cmd = [IO.FFMPEG_BIN, "-y", "-v", "error", "-i", str(clip), "-i", str(track), "-filter_complex", graph,
           "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(out)]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0 or not out.exists():
        raise RuntimeError(f"stack failed: {(r.stderr or b'').decode('utf-8', 'replace')[:300]}")
    return {"clip": str(clip), "track": str(track), "out": str(out), "clip_duration_s": d, "clip_had_audio": info["has_audio"],
            "music_gain": music_gain, "ambience_gain": ambience_gain, "fade_out_s": fade_s, "judging_view_only": True}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--clip", required=True); ap.add_argument("--track", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--music-gain", type=float, default=1.0); ap.add_argument("--ambience-gain", type=float, default=0.35)
    a = ap.parse_args(argv)
    print(json.dumps(stack(a.clip, a.track, a.out, a.music_gain, a.ambience_gain), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
