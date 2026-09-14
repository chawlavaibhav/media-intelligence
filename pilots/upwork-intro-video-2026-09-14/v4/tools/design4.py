#!/usr/bin/env python3
"""V4 design system — ONE token source, measured text boxes that refuse to clip, WCAG contrast measured over the real
pixels, contain-fit placements that refuse to crop. Every rule in the Controller package §16–§20 is a function here, and the
renderer can only draw through these functions."""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).resolve().parent
V4 = HERE.parent
sys.path.insert(0, str(V4.parent / "tools"))
import adcomp as A  # noqa: E402  hb-view glyph rasteriser from the pilot (explicit font files; deterministic)

# ------------------------------------------------------------------ tokens (the only place a size/colour/radius is written)
TOKENS = dict(
    canvas_width=1920, canvas_height=1080, fps=30,
    safe_x=120, safe_y=90,
    card_radius=26, bubble_shape="rounded_square", bubble_radius=26, bubble_size=200,
    card_border=("#111111", 36), card_shadow=dict(blur=28, offset=14, alpha=56),
    wrapper_bg="#F3EFE7", wrapper_fg="#111111", muted_fg="#5F5A54", accent="#FF5A3C", tab_alpha=242,
    h1_size=112, h2_size=64, body_size=40, small_size=32, cta_size=72, giant_size=168,
    spacing_xs=12, spacing_sm=24, spacing_md=48, spacing_lg=96,
    font_h="hn_bold", font_m="hn_medium", font_r="hn", font_mark="didot",
    min_small=32, min_claim=48, contrast_body=4.5, contrast_display=3.0, display_threshold=48,
)
T = TOKENS
W, H = T["canvas_width"], T["canvas_height"]
SAFE = (T["safe_x"], T["safe_y"], W - T["safe_x"], H - T["safe_y"])


class LayoutError(Exception):
    """Raised instead of clipping, overflowing, cropping or drawing unreadable text."""


# ------------------------------------------------------------------ reports (written by the renderer at the end)
REPORT = {"layout": [], "contrast": [], "crop": [], "cards": []}
CHECKED: set = set()


def hex_rgb(h):
    h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rel_lum(rgb):
    def ch(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(x) for x in rgb); return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(l1, l2):
    a, b = max(l1, l2), min(l1, l2); return (a + 0.05) / (b + 0.05)


# ------------------------------------------------------------------ text
@dataclass
class TextBox:
    id: str
    text: str
    font: str
    size: int
    colour: str
    x: int
    y: int
    im: Image.Image
    beat: str = ""
    alpha: int = 255

    @property
    def box(self):
        return (self.x, self.y, self.x + self.im.width, self.y + self.im.height)


def measure(text: str, font: str, size: int) -> tuple[int, int]:
    g = A.text(text, font, size, "#000000"); return g.width, g.height


def wrap(text: str, font: str, size: int, max_w: int, max_lines: int = 3) -> list[str]:
    """Greedy wrap; raises if a single word or the line count cannot fit."""
    words = text.split(); lines = []; cur = ""
    for w_ in words:
        cand = (cur + " " + w_).strip()
        if measure(cand, font, size)[0] <= max_w:
            cur = cand
        else:
            if not cur:
                raise LayoutError(f"word {w_!r} wider than {max_w}px at {size}px")
            lines.append(cur); cur = w_
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        raise LayoutError(f"{text!r} needs {len(lines)} lines > {max_lines} at {size}px in {max_w}px")
    return lines


def fit_size(lines: list[str], font: str, sizes: list[int], max_w: int, floor: int) -> int:
    """Largest size from the ladder at which every line fits max_w; never below the readability floor."""
    for s in sizes:
        if s < floor:
            break
        if all(measure(l, font, s)[0] <= max_w for l in lines):
            return s
    raise LayoutError(f"no size >= {floor}px fits {lines!r} in {max_w}px")


def place_text(frame: Image.Image, id_: str, text: str, font: str, size: int, colour: str, x: int, y: int, beat: str,
               alpha: float = 1.0, check: bool = True, role: str = "auto") -> TextBox:
    """Draw one text line. Asserts: inside the safe area (else LayoutError), readable size, and — when `check` — measured
    WCAG contrast against the pixels actually behind the box."""
    floor = T["min_small"]
    if size < floor:
        raise LayoutError(f"{id_}: {size}px < min {floor}px")
    g = A.text(text, font, size, colour)
    box = (x, y, x + g.width, y + g.height)
    inside = box[0] >= SAFE[0] and box[1] >= SAFE[1] and box[2] <= SAFE[2] and box[3] <= SAFE[3]
    entry = {"id": id_, "beat": beat, "text": text, "size": size, "box": box, "inside_safe": inside}
    if not inside:
        REPORT["layout"].append({**entry, "FAIL": True}); raise LayoutError(f"{id_} {text!r} box {box} outside safe area {SAFE}")
    if check and alpha >= 0.999 and (id_, beat) not in CHECKED:
        CHECKED.add((id_, beat))
        region = np.asarray(frame.convert("RGB").crop(box)).reshape(-1, 3)
        lum = np.array([rel_lum(tuple(p)) for p in region[:: max(1, len(region) // 4000)]])
        tl = rel_lum(hex_rgb(colour))
        worst = min(contrast_ratio(tl, float(lum.max())), contrast_ratio(tl, float(lum.min())))
        mean = contrast_ratio(tl, float(lum.mean()))
        need = T["contrast_display"] if (role == "display" or (role == "auto" and size >= T["display_threshold"])) else T["contrast_body"]
        ok = worst >= need
        REPORT["contrast"].append({"id": id_, "beat": beat, "text": text, "size": size, "colour": colour, "worst_ratio": round(worst, 2), "mean_ratio": round(mean, 2), "required": need, "pass": ok})
        if not ok:
            raise LayoutError(f"{id_} {text!r}: worst contrast {worst:.2f} < {need} (mean {mean:.2f})")
    if not any(e["id"] == id_ and e["beat"] == beat for e in REPORT["layout"]):
        REPORT["layout"].append(entry)
    if alpha < 1:
        g = g.copy(); g.putalpha(g.getchannel("A").point(lambda v: int(v * max(0.0, alpha))))
    frame.alpha_composite(g, (x, y))
    return TextBox(id_, text, font, size, colour, x, y, g, beat)


def tab(frame: Image.Image, id_: str, lines: list[tuple[str, str, int, str]], x: int, y: int, beat: str, alpha: float = 1.0, pad=None):
    """Solid wrapper_bg tab behind wrapper text placed over imagery (§18 B). Returns the tab box."""
    pad = pad or T["spacing_sm"]
    glyphs = [A.text(t, f, s, c) for (t, f, s, c) in lines]
    w = max(g.width for g in glyphs) + 2 * pad; h = sum(g.height for g in glyphs) + T["spacing_xs"] * (len(glyphs) - 1) + 2 * pad
    box = (x, y, x + w, y + h)
    if not (box[0] >= SAFE[0] and box[1] >= SAFE[1] and box[2] <= SAFE[2] and box[3] <= SAFE[3]):
        raise LayoutError(f"tab {id_} {box} outside safe area")
    panel = rounded((w, h), T["card_radius"], T["wrapper_bg"], T["tab_alpha"])
    if alpha < 1:
        panel.putalpha(panel.getchannel("A").point(lambda v: int(v * alpha)))
    frame.alpha_composite(panel, (x, y))
    yy = y + pad
    for (t, f, s, c), g in zip(lines, glyphs):
        place_text(frame, f"{id_}/{t[:18]}", t, f, s, c, x + pad, yy, beat, alpha=alpha, check=alpha >= 0.999)
        yy += g.height + T["spacing_xs"]
    REPORT["cards"].append({"id": id_, "beat": beat, "kind": "tab", "radius": T["card_radius"], "box": box})
    return box


# ------------------------------------------------------------------ shapes
def rounded(size, radius, colour, alpha=255):
    im = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=A._hex_to_rgba(colour, alpha))
    return im


def mask_rounded(im: Image.Image, radius: int) -> Image.Image:
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=radius, fill=255)
    out = im.copy(); out.putalpha(Image.fromarray(np.minimum(np.asarray(out.getchannel("A")), np.asarray(m)))); return out


def card(im: Image.Image, id_: str, beat: str, radius=None, border=True, shadow=True) -> tuple[Image.Image, int]:
    """Wrapper card: one radius, one border, one shadow (tokens). Returns (canvas with padding, pad)."""
    radius = T["card_radius"] if radius is None else radius
    sh = T["card_shadow"]; pad = sh["blur"] * 2 + sh["offset"]
    canvas = Image.new("RGBA", (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
    if shadow:
        s = rounded(im.size, radius, "#000000", sh["alpha"]); canvas.alpha_composite(s, (pad, pad + sh["offset"]))
        canvas = canvas.filter(ImageFilter.GaussianBlur(sh["blur"]))
    body = mask_rounded(im.convert("RGBA"), radius)
    if border:
        b = Image.new("RGBA", im.size, (0, 0, 0, 0))
        ImageDraw.Draw(b).rounded_rectangle([0, 0, im.width - 1, im.height - 1], radius=radius, outline=A._hex_to_rgba(*T["card_border"]), width=1)
        body.alpha_composite(b)
    canvas.alpha_composite(body, (pad, pad))
    REPORT["cards"].append({"id": id_, "beat": beat, "kind": "card", "radius": radius, "size": im.size})
    return canvas, pad


# ------------------------------------------------------------------ image fit (contain by default; cover only when declared)
def contain(im: Image.Image, box_w: int, box_h: int, id_: str, beat: str, source: str) -> Image.Image:
    s = min(box_w / im.width, box_h / im.height)
    out = im.resize((max(1, int(im.width * s + 0.5)), max(1, int(im.height * s + 0.5))), Image.LANCZOS)
    REPORT["crop"].append({"id": id_, "beat": beat, "source": source, "fit": "contain", "fraction_shown": 1.0, "rendered": out.size})
    return out


def native(im: Image.Image, id_: str, beat: str, source: str) -> Image.Image:
    if im.size != (W, H):
        raise LayoutError(f"{id_}: native placement needs {W}x{H}, got {im.size}")
    REPORT["crop"].append({"id": id_, "beat": beat, "source": source, "fit": "native", "fraction_shown": 1.0, "rendered": im.size})
    return im


def declared_cover(im: Image.Image, box: tuple, id_: str, beat: str, source: str, reason: str) -> Image.Image:
    """An intentional crop (e.g. the speaker face for the bubble). Recorded with its reason and the fraction shown."""
    out = im.crop(box); frac = (out.width * out.height) / (im.width * im.height)
    REPORT["crop"].append({"id": id_, "beat": beat, "source": source, "fit": "cover(declared)", "reason": reason, "box": box, "fraction_shown": round(frac, 3)})
    return out


def write_reports(qa_dir: Path):
    qa_dir.mkdir(parents=True, exist_ok=True)
    seen = set(); layout = []
    for e in REPORT["layout"]:
        k = (e["id"], e["beat"])
        if k not in seen:
            seen.add(k); layout.append(e)
    (qa_dir / "layout-report.json").write_text(json.dumps({"safe_area": SAFE, "tokens": {k: v for k, v in T.items() if k != "card_border"}, "text_boxes": layout,
                                                           "cards": REPORT["cards"], "all_inside_safe": all(e["inside_safe"] for e in layout),
                                                           "radii_used": sorted({c["radius"] for c in REPORT["cards"]})}, indent=1))
    seen = set(); con = []
    for e in REPORT["contrast"]:
        k = (e["id"], e["beat"])
        if k not in seen:
            seen.add(k); con.append(e)
    (qa_dir / "contrast-report.json").write_text(json.dumps({"method": "WCAG 2.x relative-luminance ratio of the text colour vs the min/max/mean luminance of the pixels behind each box (worst reported)",
                                                             "thresholds": {"body": T["contrast_body"], "display": T["contrast_display"]}, "boxes": con, "all_pass": all(e["pass"] for e in con)}, indent=1))
    seen = set(); crop = []
    for e in REPORT["crop"]:
        k = (e["id"], e["beat"])
        if k not in seen:
            seen.add(k); crop.append(e)
    (qa_dir / "crop-report.json").write_text(json.dumps({"placements": crop, "unintended_crops": [e for e in crop if e["fit"] not in ("contain", "native", "cover(declared)")]}, indent=1))
