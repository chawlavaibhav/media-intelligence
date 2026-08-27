#!/usr/bin/env python3
"""Turn supplied video files into ClipSequences, locally and fail-closed.

This is the ONLY place that touches a real delivered clip, and it is the only
place that shells out to anything. It uses ffmpeg/ffprobe, which run entirely on
this machine: no account, no API, no upload, no spend.

WHY A NORMALISATION STEP EXISTS
-------------------------------
Real footage arrives at whatever frame rate the camera or encoder chose -
23.976, 29.97, variable. Fractional and variable rates make "the defect is at
frame 41" ambiguous, and ambiguity is exactly what a truth-by-construction pack
cannot afford. So ingest resamples each clip to one declared integer frame rate
before anything is injected. That step is deterministic, is recorded with the
exact command and the ffmpeg version, and becomes a stated CONDITION of any
qualification earned on this pack.

Two hashes are therefore recorded for every clip and they mean different things:
  source_file_sha256          - the delivered file exactly as Resources gave it
  source_sequence_content_hash - the normalised frames the perturbation acts on

FAIL-CLOSED
-----------
Missing ffmpeg, a non-zero exit, a truncated frame buffer, a zero-frame decode
or a clip shorter than the declared minimum all raise ClipError. Nothing is
guessed, nothing is skipped silently.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from clipseq import ClipError, ClipSequence  # noqa: E402

DEFAULT_TARGET_FPS = 24
DEFAULT_MIN_SECONDS = 6      # RESOURCE-REQUESTS.yaml: clean base clips are 6-20s
DEFAULT_MAX_SECONDS = 20
CUT_DETECT_THRESHOLD = 0.08  # mean absolute inter-frame change, 0.0-1.0


def _tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise ClipError(
            f"{name} is not installed. Real-clip ingest cannot run without it. "
            "This is a hard stop, not a fallback: guessing frames would invent material.")
    return path


def tool_versions() -> dict:
    out = {}
    for name in ("ffmpeg", "ffprobe"):
        path = shutil.which(name)
        if not path:
            out[name] = None
            continue
        res = subprocess.run([path, "-version"], capture_output=True, text=True, check=False)
        out[name] = res.stdout.splitlines()[0].strip() if res.stdout else None
    return out


def probe(path: pathlib.Path) -> dict:
    ffprobe = _tool("ffprobe")
    cmd = [ffprobe, "-v", "error", "-select_streams", "v:0",
           "-show_entries", "stream=width,height,avg_frame_rate,codec_name,nb_frames",
           "-show_entries", "format=duration",
           "-of", "json", str(path)]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode != 0:
        raise ClipError(f"ffprobe failed on {path.name}: {res.stderr.strip()[:400]}")
    try:
        info = json.loads(res.stdout)
        stream = info["streams"][0]
    except (json.JSONDecodeError, KeyError, IndexError) as exc:
        raise ClipError(f"ffprobe returned no usable video stream for {path.name}") from exc
    return {
        "width": int(stream["width"]),
        "height": int(stream["height"]),
        "codec_name": stream.get("codec_name"),
        "avg_frame_rate": stream.get("avg_frame_rate"),
        "duration_s": float(info.get("format", {}).get("duration") or 0.0),
        "probe_command": cmd[1:],
    }


def decode(path: pathlib.Path, target_fps: int, width: int, height: int) -> tuple:
    ffmpeg = _tool("ffmpeg")
    cmd = [ffmpeg, "-nostdin", "-v", "error", "-i", str(path),
           "-vf", f"fps={target_fps}", "-pix_fmt", "rgb24",
           "-f", "rawvideo", "-"]
    res = subprocess.run(cmd, capture_output=True, check=False)
    if res.returncode != 0:
        raise ClipError(f"ffmpeg decode failed on {path.name}: "
                        f"{res.stderr.decode('utf-8', 'replace').strip()[:400]}")
    fsize = width * height * 3
    buf = res.stdout
    if not buf:
        raise ClipError(f"ffmpeg decoded zero bytes from {path.name}")
    if len(buf) % fsize != 0:
        raise ClipError(f"ffmpeg output for {path.name} is not a whole number of "
                        f"{width}x{height} rgb24 frames")
    return [bytearray(buf[i:i + fsize]) for i in range(0, len(buf), fsize)], cmd[1:]


def detect_cuts(clip: ClipSequence, threshold: float = CUT_DETECT_THRESHOLD) -> list:
    """Propose shot boundaries from inter-frame change alone.

    Deterministic and label-free: it measures how much the picture changed, it
    does not judge anything. Its output is a PROPOSAL. The pack builder uses it
    only when a clip's config asks for `"shots": "auto"`, and the threshold used
    is recorded so the proposal can be reproduced or disputed.
    """
    if clip.n_frames < 2:
        return [[0, clip.n_frames]]
    n = len(clip.frames[0]) * 255
    cuts = []
    for i in range(1, clip.n_frames):
        d = sum(abs(x - y) for x, y in zip(clip.frames[i - 1], clip.frames[i])) / n
        if d >= threshold:
            cuts.append(i)
    bounds, prev = [], 0
    for c in cuts:
        bounds.append([prev, c])
        prev = c
    bounds.append([prev, clip.n_frames])
    return bounds


def ingest_file(path: pathlib.Path, clip_id: str, config: dict,
                target_fps: int = DEFAULT_TARGET_FPS,
                min_seconds: float = DEFAULT_MIN_SECONDS,
                max_seconds: float = DEFAULT_MAX_SECONDS) -> ClipSequence:
    if not path.is_file():
        raise ClipError(f"ingest: {path} does not exist")
    raw = path.read_bytes()
    if not raw:
        raise ClipError(f"ingest: {path.name} is empty")
    file_sha = hashlib.sha256(raw).hexdigest()
    info = probe(path)
    frames, decode_cmd = decode(path, target_fps, info["width"], info["height"])
    if not frames:
        raise ClipError(f"ingest: no frames decoded from {path.name}")
    duration = len(frames) / target_fps
    if duration < min_seconds:
        raise ClipError(f"ingest: {path.name} is {duration:.2f}s, below the declared "
                        f"minimum of {min_seconds}s for a perturbation base clip")
    if duration > max_seconds:
        raise ClipError(f"ingest: {path.name} is {duration:.2f}s, above the declared "
                        f"maximum of {max_seconds}s for a perturbation base clip")

    regions = dict(config.get("regions") or {})
    region_source = "declared" if regions else "geometric_default"
    if not regions:
        # Geometry, not judgement. A default box says where to look; it never
        # asserts that a product or a caption is actually there. Any fixture
        # built on a default box records region_source=geometric_default so the
        # weaker basis is visible in the manifest.
        w, h = info["width"], info["height"]
        regions = {
            "text": [w // 8, h - h // 5, w - w // 4, h // 8],
            "product": [w // 2, h // 3, w // 4, h // 4],
        }

    provenance = {
        "material_class": config.get("material_class", "supplied_real_clip"),
        "source_file_name": path.name,
        "source_file_sha256": file_sha,
        "source_file_bytes": len(raw),
        "probe": info,
        "ingest_target_fps": target_fps,
        "ingest_decode_command": decode_cmd,
        "tool_versions": tool_versions(),
        "regions": regions,
        "region_source": region_source,
        "text_string": config.get("text_string"),
        "rights_ref": config.get("rights_ref"),
        "pack_ref": config.get("pack_ref"),
    }
    clip = ClipSequence(clip_id, info["width"], info["height"], target_fps, frames, provenance)

    shots_cfg = config.get("shots")
    if shots_cfg == "auto":
        clip.provenance["shots"] = detect_cuts(clip)
        clip.provenance["shot_source"] = "auto_detected"
        clip.provenance["shot_detect_threshold"] = CUT_DETECT_THRESHOLD
    elif isinstance(shots_cfg, list) and shots_cfg:
        clip.provenance["shots"] = [list(s) for s in shots_cfg]
        clip.provenance["shot_source"] = "declared"
    else:
        clip.provenance["shots"] = [[0, clip.n_frames]]
        clip.provenance["shot_source"] = "single_shot_assumed"
    return clip


def ingest_manifest(manifest_path: pathlib.Path, out_dir: pathlib.Path) -> list:
    """Ingest every clip named in a JSON config. Stops at the first failure."""
    cfg = json.loads(manifest_path.read_text())
    clips_cfg = cfg.get("clips") or []
    if not clips_cfg:
        raise ClipError("ingest: config lists no clips - an empty ingest is a failure, "
                        "not a success")
    base = manifest_path.parent
    target_fps = int(cfg.get("target_fps", DEFAULT_TARGET_FPS))
    out = []
    for entry in clips_cfg:
        clip = ingest_file(base / entry["file"], entry["clip_id"], entry,
                           target_fps=target_fps,
                           min_seconds=float(cfg.get("min_seconds", DEFAULT_MIN_SECONDS)),
                           max_seconds=float(cfg.get("max_seconds", DEFAULT_MAX_SECONDS)))
        clip.write(pathlib.Path(out_dir) / clip.clip_id)
        out.append(clip)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Ingest supplied clips into ClipSequences.")
    ap.add_argument("--config", required=True, help="JSON config listing the clips")
    ap.add_argument("--out-dir", required=True)
    args = ap.parse_args()
    clips = ingest_manifest(pathlib.Path(args.config), pathlib.Path(args.out_dir))
    for c in clips:
        print(f"{c.clip_id}  {c.n_frames} frames @ {c.fps}fps  "
              f"{c.duration_s}s  motion_load={c.motion_load():.6f}  "
              f"shots={len(c.provenance['shots'])} ({c.provenance['shot_source']})")
    print(f"\n{len(clips)} clips ingested.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
