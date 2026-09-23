"""Typesetting engine: lays the customer's exact copy and supplied logo onto a canvas from a layout template, a type
system and the brand kit, and measures everything it placed.

Division of labour: the TEMPLATE decides where things go and the size limits; the TYPE SYSTEM decides the faces and the
modular scale; the BRAND KIT supplies colours, logo and (optionally) the brand's own fonts; this engine fits the real
copy — balanced line breaks, largest headline that fits, sizes stepped down the scale — and records every box so
`checks.py` can judge real geometry and real pixels. Text is always drawn by code, never by a model.
"""
from __future__ import annotations

import functools
import itertools
import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import yaml
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).parent
DATA, FONT_DIR = HERE / "data", HERE / "fonts"
FORMAT_PX = {"1:1": (1080, 1080), "4:5": (1080, 1350), "9:16": (1080, 1920), "16:9": (1920, 1080)}
DEVANAGARI = re.compile(r"[ऀ-ॿ]")
PHONE_CSS_WIDTH = 390          # a 1080-px-wide post is shown ~390 CSS px wide on a phone
MIN_CSS_PX = {"headline": 20, "sub": 13, "small": 12}


class TypesetError(Exception):
    pass


# ── registry ─────────────────────────────────────────────────────────────────────────────────────────────────────

@functools.lru_cache(maxsize=None)
def fonts_registry() -> dict:
    return yaml.safe_load((DATA / "fonts.yaml").read_text())


@functools.lru_cache(maxsize=None)
def templates_registry() -> dict:
    return yaml.safe_load((DATA / "templates.yaml").read_text())


def template(tid: str) -> dict:
    return templates_registry()["templates"][tid]


def system(sid: str) -> dict:
    return fonts_registry()["systems"][sid]


def _family(fid: str, custom: dict | None = None) -> dict:
    if custom and fid in custom:
        return custom[fid]
    return fonts_registry()["families"][fid]


def font_file(fid: str, weight: int, custom: dict | None = None) -> Path:
    fam = _family(fid, custom)
    if "weights" in fam:
        w = min(fam["weights"], key=lambda k: abs(int(k) - weight))
        return (FONT_DIR / fam["weights"][w]) if not Path(fam["weights"][w]).is_absolute() else Path(fam["weights"][w])
    p = Path(fam["file"])
    return p if p.is_absolute() else FONT_DIR / p


@functools.lru_cache(maxsize=512)
def _load(path: str, weight: int, size: int) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)
    try:
        axes = f.get_variation_axes()
    except (OSError, AttributeError):
        return f
    vals = []
    for ax in axes:
        name = ax["name"].decode() if isinstance(ax["name"], bytes) else str(ax["name"])
        lo, hi, default = ax["minimum"], ax["maximum"], ax["default"]
        if name.lower().startswith("weight"):
            v = weight
        elif name.lower().startswith("optical"):
            v = size * 0.75                          # px → pt, the usual optical-size convention
        else:
            v = default
        vals.append(max(lo, min(hi, v)))
    f.set_variation_by_axes(vals)
    return f


def load_font(fid: str, weight: int, size: int, custom: dict | None = None) -> ImageFont.FreeTypeFont:
    return _load(str(font_file(fid, weight, custom)), int(weight), int(size))


def missing_glyphs(text: str, fid: str, weight: int, custom: dict | None = None) -> list:
    """Characters this face draws as .notdef (tofu)."""
    import unicodedata
    f = load_font(fid, weight, 48, custom)

    def glyph(ch):
        im = Image.new("L", (96, 96))
        ImageDraw.Draw(im).text((24, 12), ch, font=f, fill=255)
        return im.tobytes()
    tofu = glyph("\U0010FFFD")
    return [ch for ch in dict.fromkeys(text)
            if not ch.isspace() and not unicodedata.category(ch).startswith("M") and glyph(ch) == tofu]


# ── brand kit ────────────────────────────────────────────────────────────────────────────────────────────────────

@dataclass
class BrandKit:
    """What the customer shelf holds for typesetting. Colours are #RRGGBB."""
    primary: str = "#101820"             # brand colour: panels, accents
    ink: str = "#101820"                 # dark text colour
    on_primary: str = "#FFFFFF"          # text colour on the brand colour
    background: str = "#F4F1EA"          # light ground for end cards
    logo: Path | None = None             # the supplied mark, for light grounds
    logo_on_dark: Path | None = None     # optional variant for dark grounds
    system: str | None = None            # a fixed type system id, or None to let the picker choose by mood
    moods: list = field(default_factory=list)
    fonts: dict = field(default_factory=dict)   # brand's own faces: {"display": {"file": path, "weight": 700}, "text": {...}}
    preferred_templates: list = field(default_factory=list)
    logo_reversible: bool = False        # brand allows its single-colour mark to be shown in `on_primary` on dark grounds

    @classmethod
    def from_shelf(cls, d: dict) -> "BrandKit":
        k = cls(**{key: d[key] for key in ("primary", "ink", "on_primary", "background", "system", "moods",
                                             "fonts", "preferred_templates", "logo_reversible") if key in d})
        k.logo = Path(d["logo"]) if d.get("logo") else None
        k.logo_on_dark = Path(d["logo_on_dark"]) if d.get("logo_on_dark") else None
        return k

    def custom_families(self) -> dict:
        """The brand's own font files as registry-shaped families named 'brand_display' / 'brand_text'."""
        out = {}
        for role, spec in (self.fonts or {}).items():
            out[f"brand_{role}"] = {"name": f"brand {role}", "class": "brand", "scripts": spec.get("scripts", ["latin"]),
                                   "weights": {int(spec.get("weight", 400)): str(Path(spec["file"]).resolve())}}
        return out

    def resolve_system(self, sid: str) -> dict:
        """The type system with any brand faces substituted in."""
        s = dict(system(sid))
        for role in ("display", "text"):
            if role in (self.fonts or {}):
                s[role] = {"family": f"brand_{role}", "weight": int(self.fonts[role].get("weight", 400))}
        return s


def systems_for(moods: list, limit: int = 3) -> list:
    """Type systems ranked by how many of the moods they carry (ties keep registry order)."""
    systems = fonts_registry()["systems"]
    ranked = sorted(systems, key=lambda s: -len(set(moods or []) & set(systems[s]["moods"])))
    return ranked[:limit]


# ── copy ─────────────────────────────────────────────────────────────────────────────────────────────────────────

URLISH = re.compile(r"(\.[a-z]{2,}(/|\b))|(^www\.)|(@)", re.I)


def roles_from_copy_deck(deck: list) -> list:
    """Copy-deck entries → [{id, text, role}] with roles headline / sub / small. Entries that ARE the logo are dropped:
    the supplied mark is placed as an image, never typeset (live 2026-09-23: 'Mokobara' was typeset beside the logo)."""
    out, headline_taken = [], False
    for c in deck:
        role_txt = (c.get("role") or "").lower()
        if re.search(r"\b(logo|wordmark|brand mark)\b", role_txt):
            continue
        if URLISH.search(c["text"]) or re.search(r"\b(website|url|cta|call to action|legal)\b", role_txt):
            role = "small"
        elif not headline_taken:
            role, headline_taken = "headline", True
        else:
            role = "sub"
        out.append({"id": c["id"], "text": c["text"], "role": role})
    return out


# ── line breaking ────────────────────────────────────────────────────────────────────────────────────────────────

def balanced_lines(text: str, font: ImageFont.FreeTypeFont, max_w: int, max_lines: int) -> list | None:
    """Break `text` into ≤ max_lines lines that each fit max_w, choosing the most even set of line widths and never
    leaving a single short word alone on the last line when that can be avoided. None if it cannot fit."""
    words = text.split()
    if not words:
        return []
    best, best_cost = None, None
    for n in range(1, min(max_lines, len(words)) + 1):
        for cuts in itertools.combinations(range(1, len(words)), n - 1):
            idx = (0,) + cuts + (len(words),)
            lines = [" ".join(words[idx[i]:idx[i + 1]]) for i in range(n)]
            widths = [font.getlength(L) for L in lines]
            if max(widths) > max_w:
                continue
            cost = (max(widths) - min(widths)) ** 2 if n > 1 else 0.0
            if n > 1 and len(lines[-1].split()) == 1 and len(words) >= 3:
                cost += (max_w * 2) ** 2            # widow
            cost += (n - 1) * (max_w * 0.15) ** 2   # prefer fewer lines when the evenness is similar
            if best_cost is None or cost < best_cost:
                best, best_cost = lines, cost
        if best is not None and n >= 2:
            break
    return best


# ── layout ───────────────────────────────────────────────────────────────────────────────────────────────────────

@dataclass
class Element:
    role: str
    kind: str                      # text | logo
    id: str = ""
    text: str = ""
    lines: list = field(default_factory=list)
    family: str = ""
    weight: int = 400
    size: int = 0
    leading: float = 1.2
    colour: str = ""
    align: str = "left"
    box: tuple = (0, 0, 0, 0)      # inked union box, canvas px
    line_boxes: list = field(default_factory=list)
    on_panel: bool = False
    logo_path: str = ""


def _px(frac_box, W, H, frame=None):
    """Template fractions → canvas px. With `frame` (the Reels-safe area on 9:16), fractions are taken inside it, so
    one template design works on a Reel/Story without landing under Instagram's own buttons."""
    if frame is None:
        return (int(frac_box[0] * W), int(frac_box[1] * H), int(frac_box[2] * W), int(frac_box[3] * H))
    fx0, fy0, fx1, fy1 = frame
    fw, fh = fx1 - fx0, fy1 - fy0
    return (int(fx0 + frac_box[0] * fw), int(fy0 + frac_box[1] * fh), int(fx0 + frac_box[2] * fw), int(fy0 + frac_box[3] * fh))


def content_frame(fmt: str, W: int, H: int):
    if fmt != "9:16":
        return None
    rs = templates_registry()["reels_safe"]
    return (int(rs[0] * W) + 1, int(rs[1] * H) + 1, int(rs[2] * W) - 1, int(rs[3] * H) - 1)


def _face(role: str, text: str, sys_: dict, kit: BrandKit):
    spec = sys_["display"] if role == "headline" else sys_["text"]
    fid, weight = spec["family"], int(spec["weight"])
    custom = kit.custom_families()
    if DEVANAGARI.search(text) and "devanagari" not in _family(fid, custom).get("scripts", []):
        fid = sys_.get("devanagari", "notosansdevanagari")
    miss = missing_glyphs(text, fid, weight, custom)
    if miss:
        raise TypesetError(f"face {fid} has no glyph for {miss!r} in {text!r}")
    return fid, weight, custom


def _text_element(c: dict, sys_: dict, kit: BrandKit, size: int, max_w: int, max_lines: int, align: str):
    fid, weight, custom = _face(c["role"], c["text"], sys_, kit)
    f = load_font(fid, weight, size, custom)
    lines = balanced_lines(c["text"], f, max_w, max_lines)
    if lines is None:
        return None
    serif = _family(fid, custom).get("class") == "serif"
    leading = (1.06 if serif else 1.1) if c["role"] == "headline" else 1.32
    return Element(role=c["role"], kind="text", id=c["id"], text=c["text"], lines=lines, family=fid, weight=weight,
                   size=size, leading=leading, align=align)


def _measure(el: Element, kit: BrandKit):
    """(width, height, ascent) of a text element at its size, from font metrics (baseline-to-baseline leading)."""
    f = load_font(el.family, el.weight, el.size, kit.custom_families())
    asc, desc = f.getmetrics()
    w = max(f.getlength(L) for L in el.lines)
    h = int(asc + desc + (len(el.lines) - 1) * el.size * el.leading)
    return int(w), h, asc


def _logo_image(path: Path, width: int) -> Image.Image:
    im = Image.open(path).convert("RGBA")
    bb = im.getchannel("A").getbbox()
    if bb:
        im = im.crop(bb)
    return im.resize((width, max(1, round(im.height * width / im.width))), Image.LANCZOS)


def _edge_colour(plate: Image.Image, side: str) -> tuple:
    a = np.asarray(plate.convert("RGB"), dtype=np.float32)
    band = max(2, a.shape[0] // 40)
    strip = {"top": a[:band], "bottom": a[-band:]}.get(side, np.concatenate([a[:band], a[-band:]]))
    return tuple(int(v) for v in np.median(strip.reshape(-1, 3), axis=0))


def _feathered(img: Image.Image, frac: float = 0.04) -> Image.Image:
    """Alpha mask that fades the outer `frac` of the picture, so a fitted plate melts into its own edge colour."""
    w, h = img.size
    m = Image.new("L", (w, h), 255)
    d = int(min(w, h) * frac)
    if d > 0:
        m = Image.new("L", (w - 2 * d, h - 2 * d), 255)
        big = Image.new("L", (w, h), 0)
        big.paste(m, (d, d))
        m = big.filter(ImageFilter.GaussianBlur(d / 2))
    return m


def _place_plate(canvas: Image.Image, plate: Image.Image, region: tuple, mode: str, product_box_norm):
    W, H = canvas.size
    x0, y0, x1, y1 = region
    if mode == "cover":
        s = max(W / plate.width, H / plate.height)
        pw, ph = int(plate.width * s), int(plate.height * s)
        ox, oy = (W - pw) // 2, (H - ph) // 2
        canvas.paste(plate.resize((pw, ph), Image.LANCZOS).convert("RGB"), (ox, oy))
    elif product_box_norm:
        # Keep the PRODUCT as large as possible: the picture spans the canvas width, anchored to the region's far edge;
        # it shrinks only as much as needed for the product (not the whole picture) to clear the text region. The
        # picture's own empty background may run under the text — calm_ground then judges those real pixels.
        pb = product_box_norm
        s = W / plate.width
        if mode == "fit_below":
            s = min(s, (y1 - y0) / max(1e-6, (1 - pb[1]) * plate.height))
        else:
            s = min(s, (y1 - y0) / max(1e-6, pb[3] * plate.height))
        pw, ph = int(plate.width * s), int(plate.height * s)
        oy = y1 - ph if mode == "fit_below" else y0
        ox = int(W / 2 - (pb[0] + pb[2]) / 2 * pw)
        if pw >= W:
            ox = max(W - pw, min(0, ox))
        pr = plate.resize((pw, ph), Image.LANCZOS).convert("RGB")
        canvas.paste(pr, (ox, oy), _feathered(pr))
    else:
        rw, rh = x1 - x0, y1 - y0
        s = min(rw / plate.width, rh / plate.height)
        pw, ph = int(plate.width * s), int(plate.height * s)
        ox = x0 + (rw - pw) // 2
        oy = y1 - ph if mode in ("fit_below",) else y0 + (rh - ph) // 2
        pr = plate.resize((pw, ph), Image.LANCZOS).convert("RGB")
        canvas.paste(pr, (ox, oy), _feathered(pr))
    if product_box_norm:
        bx = product_box_norm
        return (ox + int(bx[0] * pw), oy + int(bx[1] * ph), ox + int(bx[2] * pw), oy + int(bx[3] * ph)), (ox, oy, ox + pw, oy + ph)
    return None, (ox, oy, ox + pw, oy + ph)


def _lum(rgb) -> float:
    from runtime.compositor.gates import relative_luminance
    return relative_luminance("#%02x%02x%02x" % tuple(int(v) for v in rgb[:3]))


def luminance_grid(img: Image.Image, box: tuple, grid: int = 24) -> list:
    x0, y0, x1, y1 = [int(v) for v in box]
    crop = img.convert("RGB").crop((max(0, x0), max(0, y0), max(x0 + 1, x1), max(y0 + 1, y1))).resize((grid, grid))
    a = np.asarray(crop, dtype=np.float64) / 255.0
    lin = np.where(a <= 0.03928, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    return (0.2126 * lin[..., 0] + 0.7152 * lin[..., 1] + 0.0722 * lin[..., 2]).ravel().tolist()


def layout(*, template_id: str, fmt: str, system_id: str, kit: BrandKit, copy: list, plate: Path | None = None,
           product_box_norm: list | None = None) -> dict:
    """Typeset one candidate. Returns {'image': PIL image, 'ground': image before text, 'elements': [...], meta...}.
    Raises TypesetError when the copy cannot be fitted within the template's limits."""
    T = template(template_id)
    if fmt not in T["formats"]:
        raise TypesetError(f"template {template_id} does not support {fmt}")
    W, H = FORMAT_PX[fmt]
    sys_ = kit.resolve_system(system_id)
    scale = float(sys_["scale"])
    margin = int(min(W, H) * 0.06)
    frame = content_frame(fmt, W, H)
    block = _px(T["block"]["box"], W, H, frame)
    block = (max(block[0], margin), max(block[1], margin), min(block[2], W - margin), min(block[3], H - margin))
    align, valign = T["block"]["align"], T["block"]["valign"]
    bw = block[2] - block[0]
    corners = T.get("corners", {})
    by_role = {c["role"]: c for c in copy}
    # headline sizing: largest size in [min, max] (step 4 %) at which every role fits the block
    hl = T["headline"]
    size = int(hl["max_size"] * W)
    min_size = int(hl["min_size"] * W)
    chosen = None
    while size >= min_size:
        els = []
        ok = True
        for role in T["block"]["order"]:
            if role == "logo" or role not in by_role or role in corners:
                continue
            if role == "headline":
                s, ml = size, hl["max_lines"]
            elif role == "sub":
                s, ml = max(int(size / scale), int(W * 0.036)), 3
            else:
                s, ml = max(int(size / scale / scale), int(W * 0.032)), 2
            e = _text_element(by_role[role], sys_, kit, s, bw, ml, align)
            if e is None:
                ok = False
                break
            els.append(e)
        if ok:
            chosen = els
            logo_h = 0
            if "logo" in T["block"]["order"] and kit.logo and "logo" not in corners:
                logo_h = _logo_image(kit.logo, int(T["logo_width"] * W)).height
            total = logo_h + sum(_measure(e, kit)[1] for e in els) + int(size * 0.55) * (len(els) + (1 if logo_h else 0) - 1)
            if total <= block[3] - block[1]:
                break
            chosen = None
        size = int(size * 0.96)
    if chosen is None:
        raise TypesetError(f"copy does not fit template {template_id} ({fmt}) at ≥ {hl['min_size']} of width")
    # stack the block
    items = []
    if "logo" in T["block"]["order"] and kit.logo and "logo" not in corners:
        items.append(("logo", _logo_image(kit.logo, int(T["logo_width"] * W))))
    order = [r for r in T["block"]["order"] if r != "logo"]
    for r in order:
        for e in chosen:
            if e.role == r:
                items.append(("text", e))
    gaps = []
    heights = []
    for i, (k, obj) in enumerate(items):
        heights.append(obj.height if k == "logo" else _measure(obj, kit)[1])
        if i:
            prev = items[i - 1][1]
            nxt = obj
            ps = prev.size if items[i - 1][0] == "text" else size
            ns = nxt.size if k == "text" else size
            gaps.append(int(max(ps * 0.45, ns * 0.55)))
    total = sum(heights) + sum(gaps)
    y = {"top": block[1], "center": block[1] + (block[3] - block[1] - total) // 2, "bottom": block[3] - total}[valign]
    placed = []
    for i, ((k, obj), h) in enumerate(zip(items, heights)):
        if i:
            y += gaps[i - 1]
        if k == "logo":
            x = {"left": block[0], "center": block[0] + (bw - obj.width) // 2, "right": block[2] - obj.width}[align]
            placed.append(Element(role="logo", kind="logo", box=(x, y, x + obj.width, y + obj.height), logo_path=str(kit.logo),
                                  align=align))
            placed[-1]._img = obj  # type: ignore[attr-defined]
        else:
            obj.box = (block[0], y, block[2], y + h)
            placed.append(obj)
        y += h
    used = (block[0], min(e.box[1] for e in placed), block[2], max(e.box[3] for e in placed))
    # corner elements
    for role, corner in corners.items():
        if role == "logo":
            if not kit.logo:
                continue
            img = _logo_image(kit.logo, int(T["logo_width"] * W))
            el = Element(role="logo", kind="logo", logo_path=str(kit.logo))
            el._img = img  # type: ignore[attr-defined]
            w, h = img.size
        else:
            if role not in by_role:
                continue
            s = min(max(int(chosen[0].size / scale / scale), int(W * 0.032)), int(W * 0.042))
            el = _text_element(by_role[role], sys_, kit, s, int(W * 0.45), 1, "left")
            if el is None:
                raise TypesetError(f"{role} does not fit its corner")
            w, h, _ = _measure(el, kit)
        top, bottom, left, right = margin, H - margin, margin, W - margin
        if frame is not None or corner.endswith("_safe"):
            rs = templates_registry()["reels_safe"]
            top, bottom = int(rs[1] * H) + 1, int(rs[3] * H) - 1
            left, right = max(left, int(rs[0] * W) + 1), min(right, int(rs[2] * W) - 1)
        if corner.endswith("_panel") and "panel" in T:
            pb = _panel_px(T, W, H, frame)
            cy = (pb[1] + min(pb[3], bottom)) // 2
            x = right - w
            yy = cy - h // 2
            el.on_panel = True
        else:
            x = left if corner.startswith(("tl", "bl")) else right - w
            yy = top if corner.startswith(("tl", "tr")) else bottom - h
        el.box = (x, yy, x + w, yy + h)
        if el.kind == "text":
            el.align = "right" if corner.startswith(("tr", "br")) else "left"
        placed.append(el)
    # ground: background, panel, plate
    bg_name = T.get("background")
    ground = Image.new("RGB", (W, H), _hex(getattr(kit, bg_name)) if bg_name else (255, 255, 255))
    panel_box = None
    if "panel" in T:
        panel_box = _panel_px(T, W, H, frame)
    product_px, plate_px = None, None
    if plate is not None and T["plate"] != "none":
        pimg = Image.open(plate)
        mode = T["plate"]
        gap = int(H * 0.025)
        foot = [e.box[1] for e in placed if e not in chosen and e.box[1] > H * 0.6]
        head = [e.box[3] for e in placed if e not in chosen and e.box[3] < H * 0.4]
        if mode == "cover":
            region = (0, 0, W, H)
        elif mode == "fit_below":
            region = (0, used[3] + gap, W, (min(foot) - gap) if foot else H)
            ground.paste(_edge_colour(pimg, "top"), (0, 0, W, H))
        elif mode == "fit_above":
            region = (0, (max(head) + gap) if head else 0, W, used[1] - gap)
            ground.paste(_edge_colour(pimg, "bottom"), (0, 0, W, H))
        elif mode == "fit_above_panel":
            region = (0, 0, W, panel_box[1])
            ground.paste(_edge_colour(pimg, "bottom"), (0, 0, W, H))
        else:
            raise TypesetError(f"unknown plate mode {mode}")
        product_px, plate_px = _place_plate(ground, pimg, region, "cover" if mode == "cover" else
                                            ("fit_below" if mode == "fit_below" else "fit_above"), product_box_norm)
    if panel_box:
        ImageDraw.Draw(ground).rectangle(panel_box, fill=_hex(getattr(kit, T["panel"]["colour"])))
        for e in placed:
            if _inside(e.box, panel_box):
                e.on_panel = True
    # colours, then draw
    from runtime.compositor.gates import LayoutRefused, check_contrast
    img = ground.copy()
    draw = ImageDraw.Draw(img)
    contrast = {}
    for e in placed:
        if e.kind == "logo":
            logo = e._img  # type: ignore[attr-defined]
            if np.mean(luminance_grid(ground, e.box)) < 0.25:
                if kit.logo_on_dark:
                    logo = _logo_image(kit.logo_on_dark, logo.width)
                    e.logo_path = str(kit.logo_on_dark)
                elif kit.logo_reversible:
                    solid = Image.new("RGBA", logo.size, _hex(kit.on_primary) + (255,))
                    solid.putalpha(logo.getchannel("A"))
                    logo = solid
                    e.logo_path = ""
            e._drawn = logo  # type: ignore[attr-defined]
            img.paste(logo, (e.box[0], e.box[1]), logo)
            continue
        f = load_font(e.family, e.weight, e.size, kit.custom_families())
        asc, _ = f.getmetrics()
        role = "display" if e.size * PHONE_CSS_WIDTH / W >= 24 else "body"
        candidates = [kit.on_primary, kit.ink] if e.on_panel else [kit.ink, "#FFFFFF", kit.on_primary]
        samples = luminance_grid(ground, e.box)
        e.colour, res = "", None
        for ink in dict.fromkeys(candidates):
            try:
                res = check_contrast(ink, samples, role=role, id_=e.id or e.role)
                e.colour = ink
                break
            except LayoutRefused as exc:
                res = {"status": "FAIL", "detail": str(exc)[:300]}
        contrast[e.id or e.role] = res
        colour = e.colour or kit.ink
        boxes, yb = [], e.box[1] + asc
        for L in e.lines:
            lw = f.getlength(L)
            x = {"left": e.box[0], "center": e.box[0] + ((e.box[2] - e.box[0]) - lw) / 2, "right": e.box[2] - lw}[e.align]
            draw.text((x, yb), L, font=f, fill=_hex(colour), anchor="ls")
            bb = draw.textbbox((x, yb), L, font=f, anchor="ls")
            boxes.append(tuple(int(v) for v in bb))
            yb += e.size * e.leading
        e.line_boxes = boxes
        e.box = (min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes))
    return {"image": img, "ground": ground, "elements": placed, "template": template_id, "system": system_id, "fmt": fmt,
            "canvas": (W, H), "margin": margin, "panel": panel_box, "product_box": product_px, "plate_box": plate_px,
            "contrast": contrast, "copy": copy, "kind": T["kind"]}


def _panel_px(T, W, H, frame):
    """A panel starts where the template says (inside the frame) and bleeds to the canvas edge it touches."""
    pb = T["panel"]["box"]
    x0, y0, x1, y1 = _px(pb, W, H, frame)
    return (0 if pb[0] <= 0 else x0, 0 if pb[1] <= 0 else y0, W if pb[2] >= 1 else x1, H if pb[3] >= 1 else y1)


def _inside(a, b) -> bool:
    return a[0] >= b[0] and a[1] >= b[1] and a[2] <= b[2] and a[3] <= b[3]


def _hex(h: str) -> tuple:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
