"""The deterministic media engine. System dependencies: ffmpeg/ffprobe (+ rsvg-convert for SVG logos); text is
drawn by Pillow (FreeType + HarfBuzz/raqm shaping) so it never depends on how ffmpeg was built (no drawtext).

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
import unicodedata
from pathlib import Path

FONT_CANDIDATES = {
    "regular": [os.environ.get("MI_FONT_REGULAR", ""), "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/TTF/DejaVuSans.ttf", "/System/Library/Fonts/Supplemental/Arial.ttf"],
    "bold": [os.environ.get("MI_FONT_BOLD", ""), "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
             "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"],
    "devanagari": [os.environ.get("MI_FONT_DEVANAGARI", ""), "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf",
                   "/usr/share/fonts/opentype/noto/NotoSansDevanagari-Regular.ttf", "/System/Library/Fonts/Kohinoor.ttc"],
}
FORMAT_PX = {"1:1": (1080, 1080), "4:5": (1080, 1350), "9:16": (1080, 1920), "16:9": (1920, 1080)}


class MediaError(Exception):
    pass


def have_ffmpeg() -> bool:
    return bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


FALLBACK_FONTS = ["/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                  "/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Kohinoor.ttc"]


import contextvars

# The customer's approved brand fonts (from their shelf), set per job by the sign painter (stations/assembly.py). They are
# tried first, and still only used when they have a real glyph for every character.
BRAND_FONTS: contextvars.ContextVar = contextvars.ContextVar("brand_fonts", default=())


def font(kind: str = "regular", text: str = "") -> str:
    """The first configured font for `kind` that has a real glyph for every character of `text` (₹, Devanagari…).
    Never silently draws tofu: if nothing covers the text, that is a MediaError."""
    if text and re.search(r"[\u0900-\u097F]", text):
        kind = "devanagari"
    seen, tried = set(), []
    for p in list(BRAND_FONTS.get()) + FONT_CANDIDATES.get(kind, []) + FONT_CANDIDATES["regular"] + FALLBACK_FONTS:
        if not p or p in seen or not Path(p).exists():
            continue
        seen.add(p)
        if not text:
            return p
        miss = missing_glyphs(text, p)
        if not miss:
            return p
        tried.append(f"{Path(p).name} lacks {''.join(miss)}")
    raise MediaError("no usable font covers " + repr(text) + (": " + "; ".join(tried) if tried else
                     "; set MI_FONT_REGULAR / MI_FONT_BOLD"))


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
        run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", f"gradients=s={w}x{h}:seed={seed}:speed=0.00001",
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


def _rgba(hex_colour: str) -> tuple:
    h = hex_colour.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + ((int(h[6:8], 16),) if len(h) == 8 else (255,))


def _pil_font(path: str, size: int):
    from PIL import ImageFont
    try:
        return ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)
    except (OSError, ImportError, KeyError):
        return ImageFont.truetype(path, size)


def missing_glyphs(text: str, fontfile: str) -> list:
    """Characters the font draws as its .notdef box (tofu) — an exact-text failure, not a style choice."""
    from PIL import Image, ImageDraw
    f = _pil_font(fontfile, 48)

    def glyph(ch):
        im = Image.new("L", (96, 96)); ImageDraw.Draw(im).text((24, 12), ch, font=f, fill=255)
        return im.tobytes()
    tofu = glyph("\U0010FFFD")
    out = []
    for ch in dict.fromkeys(text):
        if ch.isspace() or unicodedata.category(ch).startswith("M"):   # combining marks shape with their base
            continue
        if glyph(ch) == tofu:
            out.append(ch)
    return out


def text_image(text: str, *, size: int, kind: str = "regular", colour: str = "#ffffff", canvas: tuple, x: int, y: int):
    """RGBA canvas with `text` drawn at origin (x, y) = left edge / ascender line, as measure_text reports it."""
    from PIL import Image, ImageDraw
    ff = font(kind, text)
    miss = missing_glyphs(text, ff)
    if miss:
        raise MediaError(f"font {Path(ff).name} has no glyph for {miss!r} in {text!r}")
    img = Image.new("RGBA", tuple(int(v) for v in canvas), (0, 0, 0, 0))
    ImageDraw.Draw(img).text((int(x), int(y)), text, font=_pil_font(ff, int(size)), fill=_rgba(colour), anchor="la")
    return img


def measure_text(text: str, *, size: int, kind: str = "regular") -> tuple:
    """(dx, dy, w, h): the inked box of `text` drawn at (0,0) with this font and size (read back from real pixels)."""
    ff = font(kind, text)
    cw = int(_pil_font(ff, size).getlength(text)) + size * 3
    img = text_image(text, size=size, kind=kind, canvas=(cw, size * 4), x=size, y=size)
    bb = img.getchannel("A").getbbox()
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
    """The supplied mark at `width` px of VISIBLE ink: transparent margins in the file are trimmed first (a 900x600 file
    carrying a 838x124 wordmark was sized by its padding and shipped at a quarter of the intended size)."""
    from PIL import Image
    raw = out.with_name(out.stem + "-raw.png")
    if src.suffix.lower() == ".svg":
        if not shutil.which("rsvg-convert"):
            raise MediaError("rsvg-convert is required to rasterise an SVG logo")
        run(["rsvg-convert", "-w", str(max(width * 2, 800)), "-o", str(raw), str(src)])
    else:
        Image.open(src).convert("RGBA").save(raw)
    im = Image.open(raw).convert("RGBA")
    bb = im.getchannel("A").getbbox()
    if bb:
        im = im.crop(bb)
    im.resize((width, max(1, round(im.height * width / im.width))), Image.LANCZOS).save(out)
    return out


def compose(*, canvas: tuple, out: Path, plate: Path | None = None, background_hex: str | None = None,
            layers: list = (), transparent: bool = False) -> Path:
    """Render layers over a plate (cover-cropped to the canvas) or a flat background, with real alpha throughout.
    layers: {"type":"image","path":P,"x":int,"y":int} | {"type":"box","x","y","w","h","colour":"#rrggbb[aa]"}
            | {"type":"text","text":s,"size":n,"colour":"#fff","x":int,"y":int,"kind":k}
    Text layers carry the origin they were measured at (x,y = left edge / ascender line)."""
    from PIL import Image, ImageDraw, ImageOps
    cw, ch = (int(v) for v in canvas)
    if plate is not None:
        with Image.open(plate) as im:
            # Alpha on a plate is dropped (as ffmpeg's samplers read it), so the contrast gate measures the very
            # pixels that are delivered — a half-transparent plate once shipped a washed-out ad that "passed".
            base = ImageOps.fit(ImageOps.exif_transpose(im).convert("RGB"), (cw, ch), method=Image.LANCZOS).convert("RGBA")
    else:
        base = Image.new("RGBA", (cw, ch), (0, 0, 0, 0) if transparent else _rgba(background_hex or "#000000"))
    for L in layers:
        if L["type"] == "image":
            with Image.open(L["path"]) as im:
                base.alpha_composite(ImageOps.exif_transpose(im).convert("RGBA"), dest=(int(L["x"]), int(L["y"])))
        elif L["type"] == "box":
            box = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
            ImageDraw.Draw(box).rectangle([int(L["x"]), int(L["y"]), int(L["x"]) + int(L["w"]) - 1, int(L["y"]) + int(L["h"]) - 1],
                                          fill=_rgba(L["colour"]))
            base.alpha_composite(box)
        else:
            base.alpha_composite(text_image(L["text"], size=int(L["size"]), kind=L.get("kind", "regular"),
                                            colour=L.get("colour", "#ffffff"), canvas=(cw, ch), x=int(L["x"]), y=int(L["y"])))
    out.parent.mkdir(parents=True, exist_ok=True)
    (base if transparent else base.convert("RGB")).save(out)
    return out


# ── film ─────────────────────────────────────────────────────────────────────────────────────────
def assemble_film(*, segments: list, endcard: Path, supers: list, music: Path | None, out: Path, size: tuple,
                  card_s: float, workdir: Path, fps: int = 24, xfade: float = 0.6, audio_join: float = 0.06,
                  music_from_s: float = 0.0, voice: Path | None = None) -> dict:
    """segments: [{"clip": path, "in": s, "use": s}]; supers: [{"png": path, "t_in": s, "t_out": s}] (full-frame RGBA)."""
    W, H = size
    workdir.mkdir(parents=True, exist_ok=True)
    n = len(segments)
    total_v = sum(s["use"] for s in segments)
    total = total_v + card_s
    # a line belongs to its shot: it is gone before the dip into the end card starts (live 2026-09-25: the last line hung
    # over the end card)
    supers = [{**sp, "t_out": min(float(sp["t_out"]), total_v - xfade - 0.05)} for sp in supers
              if min(float(sp["t_out"]), total_v - xfade - 0.05) - float(sp["t_in"]) > 0.4]
    inputs, f = [], []
    for s in segments:
        inputs += ["-i", str(s["clip"])]
    inputs += ["-loop", "1", "-t", f"{card_s + xfade:.3f}", "-i", str(endcard)]
    iec = n
    for sp in supers:
        inputs += ["-loop", "1", "-t", f"{sp['t_out'] - sp['t_in'] + 0.1:.3f}", "-i", str(sp["png"])]
    for i, s in enumerate(segments):
        t0, use = float(s["in"]), float(s["use"])
        # out_range=tv: a JPEG-sourced segment is full-range (yuvj420p) and would ship a file some players reject
        f.append(f"[{i}:v]trim={t0}:{t0 + use},setpts=PTS-STARTPTS,scale={W}:{H}:force_original_aspect_ratio=increase:"
                 f"flags=lanczos:out_range=tv,crop={W}:{H},setsar=1,fps={fps},format=yuv420p[v{i}]")
        tail = audio_join if i < n - 1 else 0
        if probe(s["clip"])["has_audio"] and not s.get("mute"):
            f.append(f"[{i}:a]atrim={t0}:{t0 + use + tail},asetpts=PTS-STARTPTS,aresample=48000,"
                     f"aformat=channel_layouts=stereo[a{i}]")
        else:
            f.append(f"anullsrc=r=48000:cl=stereo,atrim=0:{use + tail}[a{i}]")
    f.append("".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0,settb=AVTB[vcat]")
    prev = "a0"
    for i in range(1, n):
        f.append(f"[{prev}][a{i}]acrossfade=d={audio_join}:c1=tri:c2=tri[ax{i}]"); prev = f"ax{i}"
    f.append(f"[{prev}]anull[acat]")
    f.append(f"[{iec}:v]scale={W}:{H}:out_range=tv,setsar=1,fps={fps},format=yuv420p,settb=AVTB[ec]")
    # the scene cross-fades into the end card's OWN BACKGROUND COLOUR, then the words fade in over it (live 2026-09-25: a
    # plain dissolve ghosted the logo over the last scene; a dip to black tripped the no-black-picture check)
    try:
        from PIL import Image
        bg = Image.open(endcard).convert("RGB").getpixel((4, 4))
    except Exception:
        bg = (16, 16, 16)
    bg_hex = "0x%02x%02x%02x" % bg
    f[-1] = f[-1].replace("[ec]", f",fade=t=in:st={xfade:.3f}:d=0.45:color={bg_hex}[ec]") if f[-1].endswith("[ec]") else f[-1]
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
        if voice:                   # kitchen v3: the voice-over leads; the music bed and the scene sound sit under it
            iv = im + 1
            inputs += ["-i", str(voice)]
            f.append(f"[{iv}:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur={total:.3f},atrim=0:{total:.3f}[vo]")
            f.append(f"[bed]volume=-6dB[bedlo];[acat]apad=whole_dur={total:.3f},volume=-10dB[amb];"
                     f"[amb][bedlo][vo]amix=inputs=3:duration=first:normalize=0[amix]")
        else:
            f.append(f"[acat]apad=whole_dur={total:.3f},volume=-4dB[amb];[amb][bed]amix=inputs=2:duration=first:normalize=0[amix]")
    else:
        f.append(f"[acat]apad=whole_dur={total:.3f},volume=-4dB[amix]")
    raw = workdir / "assembled-raw.mov"
    run(["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-filter_complex", ";".join(f), "-map", f"[{cur}]", "-map", "[amix]",
         "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-profile:v", "high", "-pix_fmt", "yuv420p",
         "-color_range", "tv",
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


def frame_rates(path) -> dict | None:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate,avg_frame_rate",
                        "-of", "json", str(path)], capture_output=True, text=True)
    try:
        st = json.loads(r.stdout)["streams"][0]
        return {"r": st["r_frame_rate"], "avg": st["avg_frame_rate"]}
    except (ValueError, KeyError, IndexError):
        return None


def black_spans(path, *, min_s: float = 0.2, pix_th: float = 0.10) -> list:
    """[(start, end)] where the picture is (near) black for ≥ min_s — a dropped or covered picture."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-vf",
                        f"blackdetect=d={min_s}:pic_th=0.98:pix_th={pix_th}", "-an", "-f", "null", "-"], capture_output=True, text=True)
    return [(float(a), float(b)) for a, b in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", r.stderr)]


def frozen_spans(path, *, min_s: float = 1.5, noise: float = 0.001) -> list:
    """[(start, end)] where the picture does not change for ≥ min_s."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-vf", f"freezedetect=n={noise}:d={min_s}",
                        "-an", "-f", "null", "-"], capture_output=True, text=True)
    starts = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", r.stderr)]
    ends = [float(x) for x in re.findall(r"freeze_end: ([\d.]+)", r.stderr)]
    dur = probe(path)["duration_s"]
    return [(a, ends[i] if i < len(ends) else dur) for i, a in enumerate(starts)]


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


# ── product colour match (generated plates drift darker/duller than the real product) ─────────────
_BANDS = {  # hue range (0..1), min saturation, value range — the product's dominant colours, found on the reference photos
    "dark": ((0.55, 0.78), 0.18, (0.08, 0.75)),
    "bright": ((0.08, 0.20), 0.45, (0.50, 1.00)),
}


def _hsv(arr):
    import numpy as np
    r, g, b = (arr[..., i] / 255.0 for i in range(3))
    mx, mn = np.max(arr / 255.0, axis=-1), np.min(arr / 255.0, axis=-1)
    d = mx - mn + 1e-9
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) / 6.0
    s = np.where(mx > 0, (mx - mn) / (mx + 1e-9), 0)
    return h, s, mx


def _band_weight(arr, band, feather=0.03):
    import numpy as np
    (h0, h1), smin, (v0, v1) = _BANDS[band]
    h, s, v = _hsv(arr)
    dh = np.maximum(np.maximum(h0 - h, h - h1), 0)
    w = np.clip(1 - dh / feather, 0, 1) * np.clip((s - smin) / 0.1 + 1, 0, 1) * ((v >= v0) & (v <= v1))
    return w


def colour_match(plate: Path, refs: list, out: Path, *, max_gain: float = 1.35) -> dict:
    """Move the plate's product colours (a dark body band and a bright accent band) to the reference photos' means,
    channel gain within each band, feathered; background untouched. Returns before/after distances per band."""
    import numpy as np
    from PIL import Image
    im = np.asarray(Image.open(plate).convert("RGB"), dtype=np.float64)
    ref_px = []
    for r in refs:
        a = Image.open(r).convert("RGB"); a.thumbnail((600, 600)); ref_px.append(np.asarray(a, dtype=np.float64).reshape(-1, 3))
    ref = np.concatenate(ref_px) if ref_px else np.zeros((0, 3))
    res, outim = {}, im.copy()
    for band in _BANDS:
        rw = _band_weight(ref[None, ...], band)[0] if len(ref) else np.zeros(0)
        pw = _band_weight(im, band)
        if rw.sum() < 0.005 * max(1, len(ref)) or pw.sum() < 0.005 * pw.size:
            res[band] = {"applied": False, "reason": "band not present on both"}
            continue
        ref_mean = (ref * rw[:, None]).sum(0) / rw.sum()
        plate_mean = (im * pw[..., None]).sum((0, 1)) / pw.sum()
        gain = np.clip(ref_mean / np.maximum(plate_mean, 1), 1 / max_gain, max_gain)
        outim = outim * (1 + (gain - 1) * pw[..., None])
        after = (np.clip(outim, 0, 255) * pw[..., None]).sum((0, 1)) / pw.sum()
        res[band] = {"applied": True, "reference_rgb": [round(x) for x in ref_mean], "before_rgb": [round(x) for x in plate_mean],
                     "after_rgb": [round(x) for x in after], "distance_before": round(float(np.linalg.norm(plate_mean - ref_mean)), 1),
                     "distance_after": round(float(np.linalg.norm(after - ref_mean)), 1), "gain": [round(float(x), 3) for x in gain]}
    Image.fromarray(np.clip(outim, 0, 255).astype("uint8")).save(out)
    return res


def calm_extent(plate: Path, *, canvas: tuple, side: str = "top", tol: float = 6.0) -> int:
    """Pixels of uniform background from the top (or bottom) edge of the cover-cropped plate: where the picture's content
    starts. Measured on the image itself — the text zone must end before the product, whatever an inspector says."""
    import numpy as np
    from PIL import Image, ImageOps
    cw, ch = canvas
    with Image.open(plate) as im:
        g = ImageOps.fit(im.convert("L"), (cw, ch), method=Image.LANCZOS).resize((cw // 8, ch // 8), Image.BILINEAR)
    a = np.asarray(g, dtype=np.float64)
    rows = a if side == "top" else a[::-1]
    ref = np.median(rows[:3], axis=0)
    for i, row in enumerate(rows):
        if np.abs(row - ref).max() > tol * 3 or row.std() > tol:
            return i * 8
    return ch


def extend_plate(plate: Path, *, canvas: tuple, extra: int, side: str, out: Path) -> Path:
    """Make room for copy on a uniform-background plate: the picture is scaled down (anchored to the far edge) and the
    freed band is filled with the plate's own edge colour, feathered — no generation, no crop of the product."""
    import numpy as np
    from PIL import Image, ImageOps, ImageFilter
    cw, ch = canvas
    with Image.open(plate) as im:
        base = ImageOps.fit(im.convert("RGB"), (cw, ch), method=Image.LANCZOS)
    a = np.asarray(base, dtype=np.float64)
    edge = np.median(a[:6] if side == "top" else a[-6:], axis=(0, 1))
    f = (ch - extra) / ch
    sw, sh = int(cw * f), int(ch * f)
    small = base.resize((sw, sh), Image.LANCZOS)
    bg = Image.new("RGB", (cw, ch), tuple(int(x) for x in edge))
    x0, y0 = (cw - sw) // 2, (ch - sh if side == "top" else 0)
    feather = max(8, int(min(cw, ch) * 0.06))
    mask = Image.new("L", (sw, sh), 255)
    m = np.asarray(mask, dtype=np.float64)
    ramp = np.clip(np.arange(max(sw, sh)) / feather, 0, 1)
    rows, cols = ramp[:sh][:, None], ramp[:sw][None, :]
    m = m * (rows if side == "top" else rows[::-1]) * np.minimum(cols, cols[:, ::-1])
    if side == "top":
        m[-1:, :] = m[-1:, :]      # far edge stays anchored to the frame
    bg.paste(small, (x0, y0), Image.fromarray(m.astype("uint8")).filter(ImageFilter.GaussianBlur(2)))
    bg.save(out)
    return out


def still_motion(still: Path, out: Path, *, duration_s: float, size: tuple = (720, 1280), fps: int = 24, push: float = 0.06) -> Path:
    """A slow push-in on a still, by code (no generation, USD 0): the honest fallback when a video provider refuses a beat."""
    w, h = size
    frames = max(1, int(round(duration_s * fps)))
    vf = (f"scale={w * 2}:{h * 2}:force_original_aspect_ratio=increase,crop={w * 2}:{h * 2},"
          f"zoompan=z='1+{push}*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={w}x{h}:fps={fps},"
          f"scale=out_range=tv,format=yuv420p")
    run(["ffmpeg", "-y", "-v", "error", "-loop", "1", "-i", str(still), "-vf", vf, "-frames:v", str(frames),
         "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", str(fps), str(out)])
    return out
