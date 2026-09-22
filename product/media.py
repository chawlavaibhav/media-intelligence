"""The deterministic media engine. One system dependency: ffmpeg/ffprobe (+ rsvg-convert for SVG logos).

Exact text, logos and brand colours are rendered here, by code (Mechanism B), never by a model. Text
boxes are MEASURED by rendering each line alone and reading back its alpha, so the compositor gates
(runtime.compositor.gates) judge real geometry and real pixels, as they did on Mokobara's overlays.

Film assembly is the Mokobara v2 `assemble.py` generalised: EDL segments → upscale → hard cuts with
60-ms audio acrossfades (DF-10) → crossfade into the code end card → supers → music bed → two-pass
loudnorm I=-14 TP=-4 + limiter → mux with no edit lists and +faststart.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

FONT_CANDIDATES = {
    "regular": [os.environ.get("MI_FONT_REGULAR", ""), "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/TTF/DejaVuSans.ttf", "/System/Library/Fonts/Supplemental/Arial.ttf"],
    "bold": [os.environ.get("MI_FONT_BOLD", ""), "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
             "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"],
    "devanagari": [os.environ.get("MI_FONT_DEVANAGARI", ""), "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf",
                   "/usr/share/fonts/opentype/noto/NotoSansDevanagari-Regular.ttf"],
}
FORMAT_PX = {"1:1": (1080, 1080), "4:5": (1080, 1350), "9:16": (1080, 1920), "16:9": (1920, 1080)}


class MediaError(Exception):
    pass


def have_ffmpeg() -> bool:
    return bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


def font(kind: str = "regular", text: str = "") -> str:
    if text and re.search(r"[\u0900-\u097F]", text):
        kind = "devanagari"
    for p in FONT_CANDIDATES.get(kind, []) + FONT_CANDIDATES["regular"]:
        if p and Path(p).exists():
            return p
    raise MediaError("no usable font file found; set MI_FONT_REGULAR / MI_FONT_BOLD")


def run(cmd: list, *, capture=True) -> subprocess.CompletedProcess:
    r = subprocess.run(cmd, capture_output=capture, text=False)
    if r.returncode:
        raise MediaError(f"{cmd[0]} failed ({r.returncode}): {(r.stderr or b'')[-1500:].decode('utf-8', 'replace')}")
    return r


def sha256_file(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def probe(path) -> dict:
    r = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)])
    d = json.loads(r.stdout)
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), None)
    a = next((s for s in d.get("streams", []) if s.get("codec_type") == "audio"), None)
    return {"duration_s": float(d.get("format", {}).get("duration") or 0), "width": int(v["width"]) if v else None,
            "height": int(v["height"]) if v else None, "has_audio": a is not None,
            "video_codec": v.get("codec_name") if v else None, "audio_codec": a.get("codec_name") if a else None,
            "pix_fmt": v.get("pix_fmt") if v else None, "fps": v.get("r_frame_rate") if v else None}


def hex_to_ffmpeg(hex_colour: str, alpha: float = 1.0) -> str:
    h = hex_colour.lstrip("#")
    return f"0x{h}@{alpha:.3f}"


# ── simulated media (no network): real, playable files when ffmpeg exists ──────────────────────
def sim_image(w: int, h: int, *, seed: int, label: str = "") -> bytes | None:
    if not have_ffmpeg():
        return None
    hue = (seed * 67) % 360
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "s.png"
        run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"gradients=s={w}x{h}:seed={seed}:speed=0",
             "-vf", f"hue=h={hue}", "-frames:v", "1", str(out)])
        return out.read_bytes()


def sim_video(duration_s: int, aspect: str, *, seed: int) -> bytes | None:
    if not have_ffmpeg():
        return None
    w, h = {"9:16": (720, 1280), "16:9": (1280, 720)}.get(aspect, (720, 1280))
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "s.mp4"
        run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"testsrc2=s={w}x{h}:r=24:d={duration_s}",
             "-f", "lavfi", "-i", f"anoisesrc=d={duration_s}:c=pink:a=0.02:seed={seed}",
             "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest", str(out)])
        return out.read_bytes()


# ── pixels ──────────────────────────────────────────────────────────────────────────────────────
def raw_rgba(src, *, w: int, h: int, t: float | None = None, vf_extra: str = "") -> bytes:
    cmd = ["ffmpeg", "-v", "error"] + (["-ss", f"{t:.3f}"] if t is not None else []) + ["-i", str(src), "-frames:v", "1",
           "-vf", (vf_extra + "," if vf_extra else "") + f"scale={w}:{h},format=rgba", "-f", "rawvideo", "-"]
    return run(cmd).stdout


def luminance_samples(src, box, *, canvas: tuple, t: float | None = None, grid: int = 24) -> list:
    """Relative luminance of a grid of pixels behind `box` (canvas coordinates) — for check_contrast."""
    from runtime.compositor.gates import relative_luminance
    x0, y0, x1, y1 = [int(v) for v in box]
    cw, ch = canvas
    vf = f"scale={cw}:{ch}:force_original_aspect_ratio=increase,crop={cw}:{ch},crop={max(1, x1 - x0)}:{max(1, y1 - y0)}:{x0}:{y0}"
    raw = raw_rgba(src, w=grid, h=grid, t=t, vf_extra=vf)
    out = []
    for i in range(0, len(raw), 4):
        r, g, b = raw[i], raw[i + 1], raw[i + 2]
        out.append(relative_luminance(f"#{r:02x}{g:02x}{b:02x}"))
    return out


def mean_rgb(src, box, *, canvas: tuple) -> list:
    x0, y0, x1, y1 = [int(v) for v in box]
    cw, ch = canvas
    vf = f"scale={cw}:{ch},crop={max(1, x1 - x0)}:{max(1, y1 - y0)}:{x0}:{y0}"
    raw = raw_rgba(src, w=8, h=8, vf_extra=vf)
    return [(raw[i], raw[i + 1], raw[i + 2]) for i in range(0, len(raw), 4)]


def _alpha_bbox(raw: bytes, w: int, h: int):
    alpha = raw[3::4]
    rows = [y for y in range(h) if alpha[y * w:(y + 1) * w].strip(b"\x00")]
    if not rows:
        return None
    y0, y1 = rows[0], rows[-1] + 1
    xs0, xs1 = w, 0
    for y in range(y0, y1):
        line = alpha[y * w:(y + 1) * w]
        s = line.lstrip(b"\x00"); e = line.rstrip(b"\x00")
        if s:
            xs0 = min(xs0, w - len(s)); xs1 = max(xs1, len(e))
    return xs0, y0, xs1, y1


def _drawtext(text_file: str, fontfile: str, size: int, colour: str, x, y) -> str:
    esc = lambda p: p.replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
    return (f"drawtext=fontfile='{esc(fontfile)}':textfile='{esc(text_file)}':fontsize={size}:"
            f"fontcolor={colour}:x={x}:y={y}:text_shaping=1")


def measure_text(text: str, *, size: int, kind: str = "regular") -> tuple:
    """(dx, dy, w, h): the inked box of `text` drawn at (0,0) with this font and size."""
    ff = font(kind, text)
    cw, ch = max(64, int(len(text) * size * 0.9) + size * 2), size * 3
    with tempfile.TemporaryDirectory() as d:
        tf = Path(d) / "t.txt"; tf.write_text(text, encoding="utf-8")
        vf = f"color=c=0x00000000:s={cw}x{ch},format=rgba,{_drawtext(str(tf), ff, size, 'white', size, size)}"
        raw = run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", vf, "-frames:v", "1", "-f", "rawvideo", "-pix_fmt", "rgba", "-"]).stdout
    bb = _alpha_bbox(raw, cw, ch)
    if bb is None:
        raise MediaError(f"text rendered no pixels: {text!r} (font {ff} may lack these glyphs)")
    return bb[0] - size, bb[1] - size, bb[2] - bb[0], bb[3] - bb[1]


def fit_text(text: str, *, max_w: int, start_size: int, min_size: int, kind: str = "regular") -> tuple:
    size = start_size
    while size >= min_size:
        m = measure_text(text, size=size, kind=kind)
        if m[2] <= max_w:
            return size, m
        size = int(size * 0.92)
    return min_size, measure_text(text, size=min_size, kind=kind)


def logo_png(src: Path, width: int, out: Path) -> Path:
    if src.suffix.lower() == ".svg":
        if not shutil.which("rsvg-convert"):
            raise MediaError("rsvg-convert is required to rasterise an SVG logo")
        run(["rsvg-convert", "-w", str(width), "-o", str(out), str(src)])
    else:
        run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vf", f"scale={width}:-1:flags=lanczos,format=rgba", str(out)])
    return out


def compose(*, canvas: tuple, out: Path, plate: Path | None = None, background_hex: str | None = None,
            layers: list = (), transparent: bool = False) -> Path:
    """Render layers over a plate (cover-cropped to the canvas) or a flat background.
    layers: {"type":"image","path":P,"x":int,"y":int} | {"type":"text","text":s,"size":n,"colour":"#fff","x":int,"y":int,"kind":k}
    Text layers carry the origin they were measured at (x,y = drawtext origin)."""
    cw, ch = canvas
    inputs, chain = [], []
    if plate is not None:
        inputs += ["-i", str(plate)]
        chain.append(f"[0:v]scale={cw}:{ch}:force_original_aspect_ratio=increase:flags=lanczos,crop={cw}:{ch},setsar=1,format=rgba[b0]")
    else:
        col = "0x00000000" if transparent else hex_to_ffmpeg(background_hex or "#000000")
        inputs += ["-f", "lavfi", "-i", f"color=c={col}:s={cw}x{ch}"]
        chain.append("[0:v]format=rgba[b0]")
    cur, n_in = "b0", 1
    tmp = Path(tempfile.mkdtemp(prefix="mi-compose-"))
    try:
        for i, L in enumerate(layers):
            if L["type"] == "image":
                inputs += ["-i", str(L["path"])]
                chain.append(f"[{cur}][{n_in}:v]overlay={int(L['x'])}:{int(L['y'])}:format=auto[b{i + 1}]")
                n_in += 1
            elif L["type"] == "box":
                chain.append(f"[{cur}]drawbox=x={int(L['x'])}:y={int(L['y'])}:w={int(L['w'])}:h={int(L['h'])}:"
                             f"color={hex_to_ffmpeg(L['colour'])}:t=fill[b{i + 1}]")
            else:
                tf = tmp / f"t{i}.txt"; tf.write_text(L["text"], encoding="utf-8")
                chain.append(f"[{cur}]" + _drawtext(str(tf), font(L.get("kind", "regular"), L["text"]), int(L["size"]),
                                                    hex_to_ffmpeg(L.get("colour", "#ffffff")), int(L["x"]), int(L["y"])) + f"[b{i + 1}]")
            cur = f"b{i + 1}"
        out.parent.mkdir(parents=True, exist_ok=True)
        run(["ffmpeg", "-y", "-v", "error"] + inputs + ["-filter_complex", ";".join(chain), "-map", f"[{cur}]",
             "-frames:v", "1", str(out)])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return out


# ── film ─────────────────────────────────────────────────────────────────────────────────────────
def assemble_film(*, segments: list, endcard: Path, supers: list, music: Path | None, out: Path, size: tuple,
                  card_s: float, workdir: Path, fps: int = 24, xfade: float = 0.6, audio_join: float = 0.06,
                  music_from_s: float = 0.0) -> dict:
    """segments: [{"clip": path, "in": s, "use": s}]; supers: [{"png": path, "t_in": s, "t_out": s}] (full-frame RGBA)."""
    W, H = size
    workdir.mkdir(parents=True, exist_ok=True)
    n = len(segments)
    total_v = sum(s["use"] for s in segments)
    total = total_v + card_s
    inputs, f = [], []
    for s in segments:
        inputs += ["-i", str(s["clip"])]
    inputs += ["-loop", "1", "-t", f"{card_s + xfade:.3f}", "-i", str(endcard)]
    iec = n
    for sp in supers:
        inputs += ["-loop", "1", "-t", f"{sp['t_out'] - sp['t_in'] + 0.1:.3f}", "-i", str(sp["png"])]
    for i, s in enumerate(segments):
        t0, use = float(s["in"]), float(s["use"])
        f.append(f"[{i}:v]trim={t0}:{t0 + use},setpts=PTS-STARTPTS,scale={W}:{H}:force_original_aspect_ratio=increase:"
                 f"flags=lanczos,crop={W}:{H},setsar=1,fps={fps},format=yuv420p[v{i}]")
        tail = audio_join if i < n - 1 else 0
        if probe(s["clip"])["has_audio"]:
            f.append(f"[{i}:a]atrim={t0}:{t0 + use + tail},asetpts=PTS-STARTPTS,aresample=48000,"
                     f"aformat=channel_layouts=stereo[a{i}]")
        else:
            f.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{use + tail}[a{i}]")
    f.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,settb=AVTB[vcat]")
    prev = "a0"
    for i in range(1, n):
        f.append(f"[{prev}][a{i}]acrossfade=d={audio_join}:c1=tri:c2=tri[ax{i}]"); prev = f"ax{i}"
    f.append(f"[{prev}]anull[acat]")
    f.append(f"[{iec}:v]scale={W}:{H},setsar=1,fps={fps},format=yuv420p,settb=AVTB[ec]")
    f.append(f"[vcat][ec]xfade=transition=fade:duration={xfade}:offset={total_v - xfade:.3f}[vx]")
    cur = "vx"
    for j, sp in enumerate(supers):
        k = iec + 1 + j
        d = sp["t_out"] - sp["t_in"]
        f.append(f"[{k}:v]format=rgba,fade=t=in:st=0:d=0.3:alpha=1,fade=t=out:st={max(0.0, d - 0.3):.2f}:d=0.3:alpha=1,"
                 f"setpts=PTS+{sp['t_in']}/TB[sp{j}]")
        f.append(f"[{cur}][sp{j}]overlay=0:0:eof_action=pass:enable='between(t,{sp['t_in']},{sp['t_out']})'[vs{j}]")
        cur = f"vs{j}"
    if music:
        im = iec + 1 + len(supers)
        inputs += ["-i", str(music)]
        span = total - music_from_s
        f.append(f"[{im}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{span:.3f},asetpts=PTS-STARTPTS,"
                 f"afade=t=in:d=1.5,afade=t=out:st={max(0.0, span - 1.8):.2f}:d=1.8,adelay={int(music_from_s * 1000)}|{int(music_from_s * 1000)},"
                 f"volume=-9dB[bed]")
        f.append(f"[acat]apad=whole_dur={total:.3f},volume=-4dB[amb];[amb][bed]amix=inputs=2:duration=first:normalize=0[amix]")
    else:
        f.append(f"[acat]apad=whole_dur={total:.3f},volume=-4dB[amix]")
    raw = workdir / "assembled-raw.mov"
    run(["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(f), "-map", f"[{cur}]", "-map", "[amix]",
         "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p",
         "-r", str(fps), "-c:a", "pcm_s16le", str(raw)])
    wav, norm, vid = workdir / "audio-raw.wav", workdir / "audio-mix.wav", workdir / "video-only.mp4"
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-map", "0:a", "-c:a", "pcm_s16le", str(wav)])
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-map", "0:v", "-c:v", "copy", str(vid)])
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(wav), "-af",
                        "loudnorm=I=-14:TP=-4:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
    blob = r.stderr[r.stderr.rfind("{"):]; blob = blob[: blob.find("}") + 1]
    m = json.loads(blob)
    af = (f"loudnorm=I=-14:TP=-4:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
          f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:print_format=json,"
          f"alimiter=limit=0.5:attack=3:release=40:level=false,volume=1.5dB")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(wav), "-af", af, "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", str(norm)])
    out.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(vid), "-i", str(norm), "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-shortest", "-movflags", "+faststart+negative_cts_offsets",
         "-use_editlist", "0", str(out)])
    cuts, t = [], 0.0
    for s in segments[:-1]:
        t += s["use"]; cuts.append(round(t, 3))
    return {"out": str(out), "duration_s": total, "cuts_s": cuts, "card_in_s": round(total_v - xfade, 3), "loudnorm_pass1": m}


def loudness(path) -> dict:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    summ = r.stderr[r.stderr.rfind("Integrated loudness:"):]
    il = re.search(r"I:\s+(-?[\d.]+) LUFS", summ); tp = re.search(r"Peak:\s+(-?[\d.]+) dBFS", summ)
    return {"integrated_lufs": float(il.group(1)) if il else None, "true_peak_dbtp": float(tp.group(1)) if tp else None}


def rms_db(path, start: float, dur: float) -> float | None:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-ss", f"{max(0.0, start):.3f}", "-t", f"{dur:.3f}", "-i", str(path),
                        "-af", "astats=metadata=0:reset=0", "-f", "null", "-"], capture_output=True, text=True)
    vals = re.findall(r"RMS level dB:\s+(-?[\d.]+|-inf)", r.stderr)
    if not vals:
        return None
    v = vals[-1]
    return -120.0 if v == "-inf" else float(v)


def scene_cuts(path, threshold: float = 0.4) -> list:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-vf", f"select='gt(scene,{threshold})',showinfo",
                        "-f", "null", "-"], capture_output=True, text=True)
    return [float(x) for x in re.findall(r"pts_time:([\d.]+)", r.stderr)]


def frame_png(path, t: float, out: Path, width: int = 540) -> Path:
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", str(path), "-frames:v", "1", "-vf", f"scale={width}:-2", str(out)])
    return out


def contact_sheet(path, out: Path, *, fps: float = 2.0, cols: int = 6, width: int = 240) -> Path:
    d = probe(path)["duration_s"] or 1
    rows = max(1, int((d * fps + cols - 1) // cols))
    run(["ffmpeg", "-y", "-v", "error", "-i", str(path), "-vf", f"fps={fps},scale={width}:-2,tile={cols}x{rows}:padding=4",
         "-frames:v", "1", str(out)])
    return out


def resize_for_review(path, out: Path, width: int = 1024) -> Path:
    run(["ffmpeg", "-y", "-v", "error", "-i", str(path), "-vf", f"scale={width}:-2", "-frames:v", "1", str(out)])
    return out


def reencode_small(path, out: Path, *, height: int = 720) -> Path:
    """A review copy (<~15 MB) of a film for a multimodal reviewer; picture + sound preserved."""
    run(["ffmpeg", "-y", "-v", "error", "-i", str(path), "-vf", f"scale=-2:{height}", "-c:v", "libx264", "-crf", "28",
         "-preset", "veryfast", "-c:a", "aac", "-b:a", "96k", str(out)])
    return out


def export_format(master: Path, out: Path, size: tuple) -> Path:
    run(["ffmpeg", "-y", "-v", "error", "-i", str(master), "-vf", f"scale={size[0]}:{size[1]}:force_original_aspect_ratio=increase,"
         f"crop={size[0]}:{size[1]}", "-frames:v", "1", str(out)])
    return out
