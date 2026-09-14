#!/usr/bin/env python3
"""Exact text onto video, by code, per frame. USD 0. Local only (hb-view + ffmpeg).

PROVENANCE
  Text raster: the hb-view invocation is copied from eval/battery/devanagari-exactness/devtext.py render() (font FILE +
  face INDEX, --unicodes, transparent background) - the renderer behind RR-1 (4/4) and RR-6 arm C (2/2).
  Compositing: written fresh. The Lab's eval/harness-v2/composite.py --video blends the RGBA glyph layer onto every
  decoded frame in pure Python (proven, slow: ~minutes per clip). This recipe reaches the same result through ffmpeg's
  `overlay` filter, which also gives motion (fade / slide / hold windows) for the text-in-motion unit (U4). This ffmpeg
  build (8.1.2, Homebrew) has NO drawtext, subtitles or ass filter (no libfreetype / libass), so PNG overlay is the
  only text path; `overlay`, `fade`, `format=rgba`, `drawbox`, `color` are present (checked 2026-09-14).

FONTS ON THIS MAC (fc-query, 2026-09-14)
  /System/Library/Fonts/Kohinoor.ttc      faces 0 Regular, 1 Medium, 2 Semibold, 3 Bold, 4 Light   (Devanagari; the Lab's arm C used face 3)
  /System/Library/Fonts/HelveticaNeue.ttc faces 0 Regular, 1 Bold, 2 Italic, 3 Bold Italic, 4 Condensed Bold, 5 UltraLight, 7 Light, 9 Condensed Black, 10 Medium, 12 Thin
  Also present: Avenir / Avenir Next, Gill Sans, Futura, Mukta Mahee, ITF Devanagari, Devanagari Sangam MN, Shree Devanagari 714, ~/Library/Fonts/D-DIN.ttf
  Kohinoor Devanagari shapes Latin digits/percent too; mixed English + Devanagari lines should be split per script and set as
  two layers (Kohinoor has Latin glyphs but they are not Helvetica Neue).

USAGE
  # 1. render a string to a transparent PNG (deterministic)
  python3 overlay_text_video.py render --text "FLAT 30% OFF" --font latin-bold --size 96 --colour F5E9D3 --out t_offer.png
  python3 overlay_text_video.py render --text "सभी मिठाइयों पर 20% छूट" --font dev-bold --size 72 --colour D4A017 --out t_hindi.png
  # 2. static overlay onto every frame (RR-6 arm C, the accepted mechanism), audio copied
  python3 overlay_text_video.py static --clip plate_i2v.mp4 --layer t_offer.png:center:0.12 --layer t_hindi.png:center:0.22 --out b3_text.mp4
  # 3. animated: each layer gets in/out times and a motion (fade | slide-up | slide-left | hold)
  python3 overlay_text_video.py animate --clip plate_i2v.mp4 --layer "t_offer.png:center:0.40:in=0.5:out=4.0:motion=fade" \
        --layer "t_hindi.png:center:0.55:in=1.2:out=4.0:motion=slide-up" --panel "0.30:0.70:1F4B3F:0.85" --out u4_text_in_motion.mp4
  Layer spec: <png>:<anchor center|left|right>:<y_frac of frame height for the layer's vertical centre>[:x_frac=..][:in=s][:out=s][:motion=..]
  --panel  y0_frac:y1_frac:hex:alpha  draws a solid full-width band (design direction: panel touches two frame edges; no floating scrim)
  --check  prints the layer boxes so a reviewer can confirm nothing sits inside the 9:16 / 1:1 safe reserves if a crop is planned.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

FONTS = {
    "dev-regular": ("/System/Library/Fonts/Kohinoor.ttc", 0), "dev-medium": ("/System/Library/Fonts/Kohinoor.ttc", 1),
    "dev-semibold": ("/System/Library/Fonts/Kohinoor.ttc", 2), "dev-bold": ("/System/Library/Fonts/Kohinoor.ttc", 3),
    "latin-regular": ("/System/Library/Fonts/HelveticaNeue.ttc", 0), "latin-bold": ("/System/Library/Fonts/HelveticaNeue.ttc", 1),
    "latin-medium": ("/System/Library/Fonts/HelveticaNeue.ttc", 10), "latin-light": ("/System/Library/Fonts/HelveticaNeue.ttc", 7),
    "latin-condensed-bold": ("/System/Library/Fonts/HelveticaNeue.ttc", 4),
}


def need(*tools):
    missing = [t for t in tools if shutil.which(t) is None]
    if missing:
        sys.exit(f"missing local tools: {missing} (brew install harfbuzz ffmpeg)")


def unicodes(text: str) -> str:
    return ",".join(f"U+{ord(c):04X}" for c in text)


def render(text: str, font: str, size: int, colour: str, out: Path, margin: int = 8) -> Path:
    """hb-view -> RGBA PNG on a transparent ground. Copied from devtext.render()."""
    need("hb-view")
    file, face = FONTS[font]
    if not Path(file).exists():
        sys.exit(f"font file missing: {file} (no fallback by design)")
    out.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["hb-view", file, f"--face-index={face}", f"--unicodes={unicodes(text)}", f"--font-size={size}",
                        f"--margin={margin}", "--background=00000000", f"--foreground={colour.upper()}FF", "-O", "png", "-o", str(out)],
                       capture_output=True, text=True)
    if r.returncode != 0 or not out.exists():
        sys.exit(f"hb-view failed: {r.stderr[:200]}")
    return out


def probe(path: str) -> dict:
    need("ffprobe")
    r = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path], capture_output=True, text=True, check=True)
    d = json.loads(r.stdout)
    v = next(s for s in d["streams"] if s["codec_type"] == "video")
    num, den = v["r_frame_rate"].split("/")
    return {"w": int(v["width"]), "h": int(v["height"]), "fps": v["r_frame_rate"], "fps_f": float(num) / float(den),
            "dur": float(d["format"]["duration"]), "audio": any(s["codec_type"] == "audio" for s in d["streams"])}


def png_size(path: str) -> tuple[int, int]:
    import struct
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        sys.exit(f"{path} is not a PNG")
    w, h = struct.unpack(">II", head[16:24]); return w, h


def parse_layer(spec: str) -> dict:
    parts = spec.split(":")
    d = {"png": parts[0], "anchor": parts[1] if len(parts) > 1 else "center", "y_frac": float(parts[2]) if len(parts) > 2 else 0.5,
         "x_frac": None, "in": None, "out": None, "motion": "hold"}
    for p in parts[3:]:
        k, _, v = p.partition("=")
        if k == "x_frac": d["x_frac"] = float(v)
        elif k == "in": d["in"] = float(v)
        elif k == "out": d["out"] = float(v)
        elif k == "motion": d["motion"] = v
    return d


def place(layer: dict, W: int, H: int) -> tuple[int, int, int, int]:
    lw, lh = png_size(layer["png"])
    y0 = int(round(layer["y_frac"] * H - lh / 2))
    if layer["anchor"] == "center":
        x0 = (W - lw) // 2
    elif layer["anchor"] == "left":
        x0 = int(round((layer["x_frac"] or 0.06) * W))
    else:
        x0 = int(round(W - (layer["x_frac"] or 0.06) * W - lw))
    return x0, y0, lw, lh


def build_graph(layers: list[dict], W: int, H: int, fps_f: float, panel: str | None, animate: bool) -> tuple[list[str], str, list[dict]]:
    """Returns (extra ffmpeg inputs, filter_complex, placed boxes)."""
    inputs, chain, boxes = [], [], []
    cur = "[0:v]"
    step = 0
    if panel:
        y0f, y1f, hexc, alpha = panel.split(":")
        y0, y1 = int(float(y0f) * H), int(float(y1f) * H)
        chain.append(f"{cur}drawbox=x=0:y={y0}:w={W}:h={y1 - y0}:color=0x{hexc}@{alpha}:t=fill[v{step}]"); cur = f"[v{step}]"; step += 1
    for i, L in enumerate(layers):
        x0, y0, lw, lh = place(L, W, H); boxes.append({"png": L["png"], "box": [x0, y0, lw, lh], **{k: L[k] for k in ("in", "out", "motion")}})
        idx = i + 1                                   # input 0 is the clip; each layer PNG is the next input
        inputs += ["-loop", "1", "-framerate", f"{fps_f:.6f}", "-i", L["png"]]
        lbl = f"[{idx}:v]"
        pre = f"{lbl}format=rgba"
        if animate and L["motion"] in ("fade", "slide-up", "slide-left") and L["in"] is not None:
            tin, tout = L["in"], L["out"] if L["out"] is not None else 10 ** 6
            pre += f",fade=t=in:st={tin}:d=0.4:alpha=1"
            if L["out"] is not None:
                pre += f",fade=t=out:st={max(tout - 0.4, tin)}:d=0.4:alpha=1"
        pre += f"[l{i}]"; chain.append(pre)
        x_expr, y_expr = str(x0), str(y0)
        if animate and L["in"] is not None and L["motion"] == "slide-up":
            y_expr = f"'{y0}+40*max(0\\,1-(t-{L['in']})/0.5)'"
        if animate and L["in"] is not None and L["motion"] == "slide-left":
            x_expr = f"'{x0}+60*max(0\\,1-(t-{L['in']})/0.5)'"
        en = ""
        if animate and (L["in"] is not None or L["out"] is not None):
            en = f":enable='between(t,{L['in'] or 0},{L['out'] if L['out'] is not None else 10 ** 6})'"
        chain.append(f"{cur}[l{i}]overlay=x={x_expr}:y={y_expr}:shortest=1{en}[v{step}]"); cur = f"[v{step}]"; step += 1
    chain[-1] = chain[-1].replace(cur, "[vout]")
    return inputs, ";".join(chain), boxes


def composite(args, animate: bool):
    need("ffmpeg", "ffprobe")
    info = probe(args.clip); W, H = info["w"], info["h"]
    layers = [parse_layer(s) for s in args.layer]
    inputs, graph, boxes = build_graph(layers, W, H, info["fps_f"], args.panel, animate)
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", args.clip, *inputs, "-filter_complex", graph, "-map", "[vout]"]
    if info["audio"]:
        cmd += ["-map", "0:a:0", "-c:a", "copy"]
    cmd += ["-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p", "-r", info["fps"], "-movflags", "+faststart", args.out]
    print(json.dumps({"frame": [W, H], "fps": info["fps"], "duration_s": info["dur"], "layers": boxes}, indent=1, ensure_ascii=False))
    if args.check:
        return
    print(" ".join(cmd))
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ffmpeg failed: {r.stderr[:500]}")
    print("wrote", args.out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("render"); r.add_argument("--text", required=True); r.add_argument("--font", choices=list(FONTS), default="latin-bold")
    r.add_argument("--size", type=int, default=72); r.add_argument("--colour", default="FFFFFF"); r.add_argument("--out", required=True)
    for name in ("static", "animate"):
        s = sub.add_parser(name); s.add_argument("--clip", required=True); s.add_argument("--layer", action="append", required=True)
        s.add_argument("--panel"); s.add_argument("--out", required=True); s.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    if a.cmd == "render":
        print(render(a.text, a.font, a.size, a.colour, Path(a.out)))
    else:
        composite(a, animate=(a.cmd == "animate"))


if __name__ == "__main__":
    main()
