#!/usr/bin/env python3
"""Generic Ledge composer for the portfolio brands (IronLeaf, GyaanBox) + a text-in-motion builder. Deterministic; copy from COPY-PF.yaml."""
from __future__ import annotations
import subprocess, sys
from pathlib import Path
import yaml
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, str(Path(__file__).resolve().parent))
import compose_v4 as Cp
from compose_v4 import A, FORMATS, cover, wrap2

V4 = Path(__file__).resolve().parent.parent
PF = yaml.safe_load((V4 / "plan/COPY-PF.yaml").read_text())


def ledge(plate, fmt, brand: dict, copy: dict, build: float = 1.0, anchor=(0.5, 0.5), fit: str = "cover"):
    for k in range(12):
        im, ok = _ledge(plate, fmt, brand, copy, build, anchor, 1.0 - 0.07 * k, fit)
        if ok:
            return im
    raise RuntimeError(f"ledge {fmt}: stack does not fit")


def plate_contain(plate, W, plate_h):
    """Packshot plates: the whole product stays visible. Backdrop = the plate itself cover-scaled and heavily blurred (same tone,
    no colour seam); the contained plate is pasted with feathered edges so no rectangle shows."""
    w, h = plate.size
    px = plate.convert("RGB"); band = px.crop((int(w * 0.3), 4, int(w * 0.7), int(h * 0.06))).resize((1, 1), Image.BOX).getpixel((0, 0))
    back = Image.new("RGBA", (W, plate_h), band + (255,))
    s_ = min(W / w, (plate_h - int(plate_h * 0.05)) / h); nw, nh = int(w * s_), int(h * s_)
    im = plate.resize((nw, nh), Image.LANCZOS).convert("RGBA")
    fe = max(24, int(min(nw, nh) * 0.22)); mask = Image.new("L", (nw, nh), 255); d = ImageDraw.Draw(mask)
    for i in range(fe):
        a = int(255 * (i / fe)); d.rectangle([i, i, nw - 1 - i, nh - 1 - i], outline=a)
    im.putalpha(mask)
    back.alpha_composite(im, ((W - nw) // 2, plate_h - nh - int(plate_h * 0.015)))
    return back


def _ledge(plate, fmt, B, C, build, anchor, shrink, fit="cover"):
    W, H = FORMATS[fmt]; is_wa = fmt == "wa"
    seam = {"4x5": 0.58, "1x1": 0.52, "9x16": 0.58, "wa": 0.52}[fmt]; ui_bot = int(H * 0.10) if fmt == "9x16" else 0
    plate_h = int(H * seam); m = int(W * 0.07)
    canvas = Image.new("RGBA", (W, H), A._hex_to_rgba(B["primary"]))
    A.paste(canvas, plate_contain(plate, W, plate_h) if fit == "contain" else cover(plate, W, plate_h, *anchor), 0, 0)
    sh = Image.new("RGBA", (W, 40), (0, 0, 0, 0)); ImageDraw.Draw(sh).rectangle([0, 0, W, 12], fill=(0, 0, 0, 60))
    A.paste(canvas, sh.filter(ImageFilter.GaussianBlur(10)), 0, plate_h - 24)
    if build < 0.15:
        return canvas, True
    A.paste(canvas, Image.new("RGBA", (W, H - plate_h), A._hex_to_rgba(B["primary"])), 0, plate_h)
    disp, txt, bold = B.get("display", "didot"), "hn", "hn_medium"
    hl = int(W * (0.078 if not is_wa else 0.088) * (1.35 if fmt == "9x16" else 1.0) * shrink)
    pill = A.pill(C["pill"], bold, int(W * 0.033), B["accent"], B["primary"])
    if build >= 0.30:
        A.paste(canvas, pill, m, plate_h - pill.height // 2)
    y = plate_h + pill.height // 2 + int(W * 0.045 * shrink)
    maxw = W - 2 * m - int(W * 0.05)
    lines = wrap2(C["headline"], disp, hl, maxw)
    while any(A.text_width(l, disp, hl) > maxw for l in lines) and hl > 30:
        hl -= 2; lines = wrap2(C["headline"], disp, hl, maxw)
    if build >= 0.45:
        for l in lines:
            g = A.text(l, disp, hl, B["cream"]); A.paste(canvas, g, m, y); y += int(hl * 1.08)
    else:
        y += int(hl * 1.08) * len(lines)
    y += int(W * 0.03 * shrink)
    if build >= 0.60:
        g = A.text(C["support"], bold, int(W * 0.040), B["accent"]); A.paste(canvas, g, m, y); y += g.height + int(W * 0.035 * shrink)
    else:
        y += int(W * 0.040) + int(W * 0.035 * shrink)
    if C.get("cta") and build >= 0.75:
        btn = A.button(C["cta"], bold, int(W * 0.034), B["accent"], B["primary"], min_w=int(W * 0.30)); A.paste(canvas, btn, m, y); y += btn.height
    elif C.get("cta"):
        y += int(W * 0.034 * 2.5)
    leg = A.text(C["legal"], txt, max(18, int(W * 0.022)), B["cream"], alpha=165)
    mark = A.text(B["name"], B.get("markface", "hn_medium"), int(W * 0.036), B["cream"])
    ly = H - ui_bot - int(W * 0.06); ok = y + int(W * 0.03) <= ly - leg.height
    if build >= 0.85:
        A.paste(canvas, leg, m, ly - leg.height); A.paste(canvas, mark, W - m - mark.width, ly - mark.height)
    return canvas, ok


def text_in_motion(clip: Path, out: Path, brand, copy, total_s=12.0, anchor=(0.5, 0.35), fps=30):
    """9:16 Ledge whose plate is the moving clip; elements build on in hierarchy order over 3 s; last frame held to total_s."""
    Wv, Hv = 1080, 1920; plate_h = int(Hv * 0.58)
    vf = f"fps={fps},scale={Wv}:{plate_h}:force_original_aspect_ratio=increase,crop={Wv}:{plate_h}:(iw-{Wv})*{anchor[0]}:(ih-{plate_h})*{anchor[1]}"
    dec = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", str(clip), "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    out.parent.mkdir(parents=True, exist_ok=True)
    enc = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{Wv}x{Hv}", "-r", str(fps), "-i", "-", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    last = None
    def ease(t): t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3
    for i in range(int(total_s * fps)):
        t = i / fps; buf = dec.stdout.read(Wv * plate_h * 3)
        fr = Image.frombytes("RGB", (Wv, plate_h), buf).convert("RGBA") if len(buf) == Wv * plate_h * 3 else last
        last = fr
        b = 0.15 + 0.85 * ease((t - 0.5) / 2.5)
        f = ledge(fr, "9x16", brand, copy, build=min(b, 1.0))   # the moving frame IS the plate; no seam artefacts
        enc.stdin.write(f.convert("RGB").tobytes())
    enc.stdin.close(); enc.wait(); dec.stdout.close(); dec.kill(); dec.wait()


if __name__ == "__main__":
    out = Path(sys.argv[1])
    for key, plate_path, anchor, fit in (("ironleaf", V4 / "gen/portfolio/ironleaf-packshot-accepted.png", (0.5, 0.5), "contain"), ("gyaanbox", V4 / "gen/portfolio/gyaan-plate-accepted.png", (0.5, 0.35), "cover")):
        spec = PF[key]; plate = Image.open(plate_path).convert("RGBA"); d = out / spec["tile"]; d.mkdir(parents=True, exist_ok=True)
        for f in ("4x5", "1x1", "9x16", "wa"):
            ledge(plate, f, spec["brand"], spec["copy"], anchor=anchor, fit=fit).convert("RGB").save(d / f"{key}-offer-{f}.png", quality=95)
        if key == "ironleaf":
            (d / "ironleaf-source-packshot.png").write_bytes(plate_path.read_bytes())
    spec = PF["gyaanbox"]
    text_in_motion(V4 / "gen/portfolio/gyaan-motion-accepted.mp4", out / spec["tile"] / "gyaanbox-offer-in-motion-9x16-12s.mp4", spec["brand"], spec["copy"])
    print("ok")
