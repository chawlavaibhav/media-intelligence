"""Deterministic layout gates: bounds, contrast, fit, geometry, disjointness. Each refuses by name.

Boxes are (x0, y0, x1, y1) with x1/y1 exclusive, in canvas pixels. Colours are '#RRGGBB'. Luminance
samples are WCAG relative luminances (0.0–1.0) of the pixels behind a text box, read by the caller from
whatever raster it draws on — the gate never opens an image.
"""
from __future__ import annotations

from runtime.errors import Refusal
from runtime.compositor.tokens import DesignTokens

CRITICAL_REGIONS = ("headline", "offer", "code", "cta", "legal")
FITS = ("contain", "native", "cover")


class LayoutRefused(Refusal):
    TEXT_OUT_OF_CANVAS = "TEXT_OUT_OF_CANVAS"
    TEXT_OUT_OF_CONTAINER = "TEXT_OUT_OF_CONTAINER"
    CONTRAST_BELOW_THRESHOLD = "CONTRAST_BELOW_THRESHOLD"
    UNDECLARED_COVER_CROP = "UNDECLARED_COVER_CROP"
    GEOMETRY_OFF_TOKEN = "GEOMETRY_OFF_TOKEN"
    CRITICAL_REGIONS_OVERLAP = "CRITICAL_REGIONS_OVERLAP"
    TOKEN_SOURCE_MISSING = "TOKEN_SOURCE_MISSING"
    # production-learning RENTOK-GAME-A-004 / RENTOK-GAME-B-005 (2026-09-21)
    GRAPHIC_OVER_TEXT = "GRAPHIC_OVER_TEXT"
    VO_BEFORE_ITS_TEXT = "VO_BEFORE_ITS_TEXT"
    BRAND_COLOUR_OFF = "BRAND_COLOUR_OFF"
    # production-learning RENTOK-GAME-V2-006 (2026-09-21)
    HERO_OCCLUDED = "HERO_OCCLUDED"
    FRAMING_BELOW_TARGET = "FRAMING_BELOW_TARGET"
    FRAMING_FRAME_MISSING = "FRAMING_FRAME_MISSING"
    HERO_CLIPPED_BY_FRAME = "HERO_CLIPPED_BY_FRAME"
    WORLD_SMALLER_THAN_FRAME = "WORLD_SMALLER_THAN_FRAME"
    SPRITE_DENSITY_MISMATCH = "SPRITE_DENSITY_MISMATCH"
    VO_LINES_OVERLAP = "VO_LINES_OVERLAP"
    VO_OVERRUNS_END = "VO_OVERRUNS_END"


# ── geometry helpers ─────────────────────────────────────────────────────────

def _box(b) -> tuple:
    x0, y0, x1, y1 = (int(v) for v in b)
    if x1 <= x0 or y1 <= y0:
        raise ValueError(f"degenerate box {b!r}")
    return (x0, y0, x1, y1)


def inside(inner: tuple, outer: tuple) -> bool:
    return inner[0] >= outer[0] and inner[1] >= outer[1] and inner[2] <= outer[2] and inner[3] <= outer[3]


def overlaps(a: tuple, b: tuple, min_gap_px: int = 0) -> bool:
    g = int(min_gap_px)
    return not (a[2] + g <= b[0] or b[2] + g <= a[0] or a[3] + g <= b[1] or b[3] + g <= a[1])


# ── A. text bounds (SD-01) ───────────────────────────────────────────────────

def check_text_bounds(box, *, canvas, container=None, tokens: DesignTokens | None = None, id_: str = "text") -> dict:
    """The measured ink box of a rendered text line must lie inside the canvas and inside its container
    (the card it is drawn on, or the token safe area when no container is given). Overflow is refused,
    never clipped."""
    box, canvas = _box(box), _box(canvas)
    if not inside(box, canvas):
        raise LayoutRefused(LayoutRefused.TEXT_OUT_OF_CANVAS, f"{id_}: text box {box} extends beyond the canvas {canvas}",
                            id=id_, box=box, canvas=canvas)
    label = "container"
    if container is None and tokens is not None:
        container, label = tokens.safe_area(canvas), "safe area"
    if container is not None:
        container = _box(container)
        if not inside(box, container):
            raise LayoutRefused(LayoutRefused.TEXT_OUT_OF_CONTAINER,
                                f"{id_}: text box {box} extends outside its {label} {container}",
                                id=id_, box=box, container=container)
    return {"status": "PASS", "id": id_, "box": box, "canvas": canvas, "container": container}


# ── B. contrast (SD-02) ──────────────────────────────────────────────────────

def _channel(c: int) -> float:
    c = c / 255.0
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def relative_luminance(hex_colour: str) -> float:
    h = hex_colour.lstrip("#")
    if len(h) != 6:
        raise ValueError(f"colour must be #RRGGBB, got {hex_colour!r}")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _channel(r) + 0.7152 * _channel(g) + 0.0722 * _channel(b)


def contrast_ratio(l1: float, l2: float) -> float:
    a, b = max(l1, l2), min(l1, l2)
    return (a + 0.05) / (b + 0.05)


def check_contrast(text_hex: str, luminance_samples, *, role: str = "body", backing_hex: str | None = None,
                   backing_alpha: float = 1.0, tokens: DesignTokens | None = None, id_: str = "text") -> dict:
    """Wrapper/UI text keeps the readable ratio (WCAG: 4.5 body, 3.0 display) against the WORST pixel
    behind it — the sample whose luminance is nearest the text's, wherever it sits in the range — or it
    sits on a solid opaque backing whose colour is then what the ratio is measured against. A
    translucent backing is not a backing."""
    t = tokens or DesignTokens(card_radius=0, card_border_px=0, card_shadow=(0, 0, 0), safe_x=0, safe_y=0)
    need = t.contrast_display if role == "display" else t.contrast_body
    tl = relative_luminance(text_hex)
    if backing_hex is not None and float(backing_alpha) >= 1.0:
        bl = relative_luminance(backing_hex)
        worst = contrast_ratio(tl, bl)
        against = "backing"
    else:
        samples = [float(s) for s in luminance_samples]
        if not samples:
            raise LayoutRefused(LayoutRefused.CONTRAST_BELOW_THRESHOLD,
                                f"{id_}: no luminance samples behind the box and no opaque backing — unreadable by default",
                                id=id_, worst_ratio=0.0, required=need)
        # The ratio is minimised where the background is CLOSEST to the text luminance — an interior
        # sample, not an endpoint (Controller audit on PR #98, blocker 1) — so every sample is checked.
        worst = min(contrast_ratio(tl, sample) for sample in samples)
        against = "pixels" if backing_hex is None else f"pixels (backing alpha {backing_alpha} is not opaque)"
    if worst < need:
        raise LayoutRefused(LayoutRefused.CONTRAST_BELOW_THRESHOLD,
                            f"{id_}: worst contrast {worst:.2f} < {need} for {role} text ({against}); "
                            "give it an opaque backing surface or change the colour",
                            id=id_, worst_ratio=round(worst, 3), required=need, measured_against=against)
    return {"status": "PASS", "id": id_, "role": role, "required": need, "worst_ratio": round(worst, 3),
            "measured_against": against}


# ── C. crop / fit declaration (SD-03) ────────────────────────────────────────

def check_fit(placement: dict) -> dict:
    """Creative proof defaults to CONTAIN (everything shown). NATIVE needs the exact box size. COVER is a
    destructive crop and needs `declared_crop: {box, reason}` inside the source; then it passes with the
    fraction shown reported for QA. Anything else is refused."""
    id_ = str(placement.get("id") or "placement")
    fit = str(placement.get("fit") or "contain")
    sw, sh = (int(v) for v in placement["source_size"])
    box = _box(placement["box"])
    bw, bh = box[2] - box[0], box[3] - box[1]
    if fit == "contain":
        s = min(bw / sw, bh / sh)
        rendered = (max(1, int(sw * s + 0.5)), max(1, int(sh * s + 0.5)))
        return {"status": "PASS", "id": id_, "fit": "contain", "fraction_shown": 1.0, "rendered_size": rendered}
    if fit == "native":
        if (sw, sh) != (bw, bh):
            raise LayoutRefused(LayoutRefused.UNDECLARED_COVER_CROP,
                                f"{id_}: native placement needs a {bw}x{bh} source, got {sw}x{sh}",
                                id=id_, fit=fit)
        return {"status": "PASS", "id": id_, "fit": "native", "fraction_shown": 1.0, "rendered_size": (sw, sh)}
    if fit == "cover":
        decl = placement.get("declared_crop")
        if not isinstance(decl, dict) or not decl.get("box") or not str(decl.get("reason") or "").strip():
            raise LayoutRefused(LayoutRefused.UNDECLARED_COVER_CROP,
                                f"{id_}: cover crops the source; declare the crop box and its reason or use contain",
                                id=id_, fit=fit)
        crop = _box(decl["box"])
        if not inside(crop, (0, 0, sw, sh)):
            raise LayoutRefused(LayoutRefused.UNDECLARED_COVER_CROP,
                                f"{id_}: declared crop {crop} is not inside the source {sw}x{sh}",
                                id=id_, fit=fit, crop=crop)
        frac = ((crop[2] - crop[0]) * (crop[3] - crop[1])) / (sw * sh)
        return {"status": "PASS", "id": id_, "fit": "cover(declared)", "fraction_shown": round(frac, 4),
                "reason": str(decl["reason"]), "crop": crop, "rendered_size": (bw, bh)}
    raise LayoutRefused(LayoutRefused.UNDECLARED_COVER_CROP, f"{id_}: unknown fit {fit!r}; one of {FITS}", id=id_, fit=fit)


# ── D. geometry tokens (SD-04) ───────────────────────────────────────────────

def card_geometry(tokens: DesignTokens, *, id_: str, kind: str = "card") -> dict:
    """The only way a renderer should obtain a wrapper's geometry."""
    return {"id": id_, "kind": kind, "radius": tokens.card_radius, "border_px": tokens.card_border_px,
            "shadow": tuple(tokens.card_shadow), "token_source": tokens.source}


def check_geometry(cards, tokens: DesignTokens) -> dict:
    """Every wrapper card carries exactly the token radius, border and shadow. A card missing any of them,
    or differing from the tokens, is refused by id."""
    radii = set()
    for c in cards:
        cid = str(c.get("id") or "?")
        for key in ("radius", "border_px", "shadow"):
            if key not in c:
                raise LayoutRefused(LayoutRefused.GEOMETRY_OFF_TOKEN, f"card {cid}: no {key} — not built from the token source",
                                    id=cid, missing=key)
        got = (int(c["radius"]), int(c["border_px"]), tuple(c["shadow"]))
        want = (tokens.card_radius, tokens.card_border_px, tuple(tokens.card_shadow))
        if got != want:
            raise LayoutRefused(LayoutRefused.GEOMETRY_OFF_TOKEN,
                                f"card {cid}: geometry {got} differs from tokens {want}", id=cid, got=got, want=want)
        radii.add(got[0])
    return {"status": "PASS", "cards": len(list(cards)), "radii_used": sorted(radii)}


# ── E. disjointness (SD-07) ──────────────────────────────────────────────────

def check_disjoint(regions: dict, *, critical=CRITICAL_REGIONS, min_gap_px: int = 0) -> dict:
    """Critical regions (offer, code, CTA, legal, headline by default) may not overlap — nor sit closer than
    `min_gap_px` when a gap is required. Pairs are checked in sorted name order; the first collision is
    the refusal."""
    names = sorted(n for n in regions if n in set(critical))
    boxes = {n: _box(regions[n]) for n in names}
    pairs = 0
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            pairs += 1
            if overlaps(boxes[a], boxes[b], min_gap_px):
                raise LayoutRefused(LayoutRefused.CRITICAL_REGIONS_OVERLAP,
                                    f"{a} {boxes[a]} overlaps {b} {boxes[b]}" + (f" (gap < {min_gap_px}px)" if min_gap_px else ""),
                                    pair=(a, b), min_gap_px=min_gap_px)
    return {"status": "PASS", "regions": names, "pairs_checked": pairs, "min_gap_px": min_gap_px}


# ── F. graphic ↔ text disjointness (RENTOK-GAME-B-005 D-1, D-9; RENTOK-GAME-A-004 D-2) ────────

def check_graphic_text_disjoint(graphics: dict, texts: dict, *, min_gap_px: int = 0) -> dict:
    """A declared critical graphic (the product, a phone, a flag, a projectile) may not cross a critical
    text box, and a text box may not cover a critical graphic. `check_disjoint` sees only the regions it
    is handed, and both RentOK lanes handed it text alone: Lane B shipped a phone rising over the
    `PG OWNER` tag (D-1) and later a beam 8 px under it (D-9); Lane A shipped the raised flag — the
    customer's "gets the flag" payoff — hidden behind the checklist and `LEVEL CLEAR!` (D-2). Every
    graphic is checked against every text box; the first collision (sorted names) is the refusal."""
    g_names, t_names = sorted(graphics), sorted(texts)
    g_boxes = {n: _box(graphics[n]) for n in g_names}
    t_boxes = {n: _box(texts[n]) for n in t_names}
    pairs = 0
    for g in g_names:
        for t in t_names:
            pairs += 1
            if overlaps(g_boxes[g], t_boxes[t], min_gap_px):
                raise LayoutRefused(LayoutRefused.GRAPHIC_OVER_TEXT,
                                    f"graphic {g} {g_boxes[g]} crosses text {t} {t_boxes[t]}"
                                    + (f" (gap < {min_gap_px}px)" if min_gap_px else ""),
                                    pair=(g, t), min_gap_px=min_gap_px)
    return {"status": "PASS", "graphics": g_names, "texts": t_names, "pairs_checked": pairs, "min_gap_px": min_gap_px}


# ── G. a voice line may not run ahead of its own on-screen words (RENTOK-GAME-B-005 D-3) ───────

def check_vo_text_alignment(lines, text_first_on_screen: dict, *, tolerance_s: float = 0.0) -> dict:
    """When a spoken line and an on-screen string are meant to be the same words, the line may not
    begin before the string first appears (a `tolerance_s` of lead is allowed when the caller states
    one). Lane B's announcer said "RentOk mode: on" at 14.70 s while the screen still read
    `INSTALLING...`; the words appeared at 15.90 s. The lane's VO gate checked overlap and film end,
    not this. Each line is {"id", "start_s", "on_screen_id"}; `text_first_on_screen` maps a string id
    to the first second it is on screen (from the layout log). A line without `on_screen_id` has
    nothing to align to and is listed as unpaired; a paired string that never appears is refused."""
    tol = float(tolerance_s)
    if tol < 0:
        raise ValueError("tolerance_s must be >= 0")
    aligned, unpaired = [], []
    for ln in lines:
        lid, start = str(ln.get("id")), float(ln["start_s"])
        sid = ln.get("on_screen_id")
        if sid is None:
            unpaired.append(lid)
            continue
        sid = str(sid)
        if sid not in text_first_on_screen:
            raise LayoutRefused(LayoutRefused.VO_BEFORE_ITS_TEXT,
                                f"vo line {lid} is paired with {sid}, which never appears on screen",
                                id=lid, on_screen_id=sid)
        first = float(text_first_on_screen[sid])
        if start + tol < first:
            raise LayoutRefused(LayoutRefused.VO_BEFORE_ITS_TEXT,
                                f"vo line {lid} starts at {start:.2f}s but its words {sid} first appear at {first:.2f}s "
                                f"({first - start:.2f}s early; tolerance {tol:.2f}s)",
                                id=lid, on_screen_id=sid, start_s=start, first_on_screen_s=first,
                                lead_s=round(first - start, 3))
        aligned.append({"id": lid, "on_screen_id": sid, "start_s": start, "first_on_screen_s": first})
    return {"status": "PASS", "aligned": aligned, "unpaired": unpaired, "tolerance_s": tol}


# ── H. a declared brand colour is measured on the rendered frame (RENTOK-GAME-A-004 D-11) ──────

def check_brand_colour(samples_rgb, declared_hex: str, *, max_channel_delta: int = 8, id_: str = "brand_fill") -> dict:
    """Pixels the caller reads from the RENDERED, ENCODED frame where a brand colour was declared must
    each sit within `max_channel_delta` of the declared #RRGGBB on every channel. Lane A's repair
    statement said the end card was filled "#0239FF"; the file was black — the renderer had sampled a
    transparent corner of the logo raster, and no check measured the output. A colour claim is
    verified against the output, never the intent. No samples → refused: an unmeasured colour is not
    a matching colour. The default delta leaves room for H.264 4:2:0 chroma drift (Lane A measured
    (2,57,255) → (1,55,253) on the accepted file); the caller may tighten or widen it with a reason."""
    h = declared_hex.lstrip("#")
    if len(h) != 6:
        raise ValueError(f"colour must be #RRGGBB, got {declared_hex!r}")
    want = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    limit = int(max_channel_delta)
    samples = [tuple(int(c) for c in s[:3]) for s in samples_rgb]
    if not samples:
        raise LayoutRefused(LayoutRefused.BRAND_COLOUR_OFF,
                            f"{id_}: no pixels sampled from the rendered frame; the declared {declared_hex} is unverified",
                            id=id_, declared=declared_hex, samples=0)
    worst, worst_sample = -1, None
    for s in samples:
        d = max(abs(s[i] - want[i]) for i in range(3))
        if d > worst:
            worst, worst_sample = d, s
    if worst > limit:
        raise LayoutRefused(LayoutRefused.BRAND_COLOUR_OFF,
                            f"{id_}: rendered pixel {worst_sample} is {worst} per channel from the declared "
                            f"{declared_hex} {want} (limit {limit}); the file does not carry the colour the record claims",
                            id=id_, declared=declared_hex, worst_sample=worst_sample, worst_delta=worst, limit=limit)
    return {"status": "PASS", "id": id_, "declared": declared_hex, "samples": len(samples),
            "worst_channel_delta": worst, "worst_sample": worst_sample, "limit": limit}


# ── I. a hero graphic may not be covered by another graphic (RENTOK-GAME-V2-006 N1, N2) ───────

def _overlap_area(a: tuple, b: tuple) -> int:
    w = min(a[2], b[2]) - max(a[0], b[0])
    h = min(a[3], b[3]) - max(a[1], b[1])
    return w * h if (w > 0 and h > 0) else 0


def check_hero_visible(region, foreground: dict, *, max_covered_frac: float = 0.0, id_: str = "hero") -> dict:
    """A declared region of the hero (his whole box at a triumph beat; his face while he holds the phone)
    may not be covered by any graphic drawn IN FRONT of him beyond `max_covered_frac` of the region's
    area. `check_graphic_text_disjoint` sees graphic-versus-text only: the V2 job's C5b gate reported 0
    overlaps while the flag rose through the cheering owner for 26 frames (26.53–27.37 s, N1) and the
    raised phone sat over his face for 6 frames at the wind-up (18.20–18.37 s, N2). The caller hands the
    region to protect and the graphics layered over it (not the ones he holds behind or beside it — a
    held phone is inside his box by design, which is why the region, not the whole box, is the unit).
    Refuses on the first graphic (sorted names) whose overlap exceeds the fraction; an empty foreground
    is a pass with nothing checked."""
    frac = float(max_covered_frac)
    if not (0.0 <= frac < 1.0):
        raise ValueError("max_covered_frac must be in [0, 1)")
    reg = _box(region)
    area = (reg[2] - reg[0]) * (reg[3] - reg[1])
    names = sorted(foreground)
    covered = {}
    for g in names:
        gb = _box(foreground[g])
        c = _overlap_area(reg, gb) / area
        covered[g] = round(c, 4)
        if c > frac:
            raise LayoutRefused(LayoutRefused.HERO_OCCLUDED,
                                f"{id_}: graphic {g} {gb} covers {c:.1%} of the protected region {reg} (limit {frac:.0%})",
                                id=id_, graphic=g, graphic_box=gb, region=reg, covered_frac=round(c, 4), limit=frac)
    return {"status": "PASS", "id": id_, "region": reg, "foreground": names, "covered_frac": covered, "limit": frac}


# ── J. the framing target is measured at the beat's focus frame (RENTOK-GAME-V2-006 A-4, R-1, N4) ──

def check_framing_target(owner_frac_by_frame: dict, *, focus_frame: int, target: float, beat: str,
                         hero_box=None, canvas=None) -> dict:
    """The hero's screen height ÷ frame height, read from the layout log at the beat's declared focus
    frame, must reach the board's target for that beat. Two lessons are fixed here: the value is read at
    ONE named frame (the hold — the V2 job first measured mid-ease and failed for the wrong reason, A-4),
    and a focus frame missing from the log is a refusal, never a pass. The target is the caller's, set
    per POSE — a crouched or lying pose is inherently short (F5 cover 0.16 vs F2 hurt 0.25 in the job).
    When `hero_box` and `canvas` are given, the hero must also lie inside the frame at that focus: the
    dazed owner was drawn 52 px off the left edge for 0.46 s (N4)."""
    tgt = float(target)
    if tgt < 0:
        raise ValueError("target must be >= 0")
    f = int(focus_frame)
    if f not in owner_frac_by_frame or owner_frac_by_frame[f] is None:
        raise LayoutRefused(LayoutRefused.FRAMING_FRAME_MISSING,
                            f"{beat}: focus frame {f} has no hero measurement in the layout log; the framing target {tgt} is unverified",
                            beat=beat, focus_frame=f, target=tgt)
    got = float(owner_frac_by_frame[f])
    if got + 1e-6 < tgt:
        raise LayoutRefused(LayoutRefused.FRAMING_BELOW_TARGET,
                            f"{beat}: hero is {got:.3f} of the frame at focus frame {f}; the board asks for {tgt:.3f}",
                            beat=beat, focus_frame=f, measured=got, target=tgt)
    out = {"status": "PASS", "beat": beat, "focus_frame": f, "measured": got, "target": tgt}
    if hero_box is not None and canvas is not None:
        hb, cv = _box(hero_box), _box(canvas)
        if not inside(hb, cv):
            raise LayoutRefused(LayoutRefused.HERO_CLIPPED_BY_FRAME,
                                f"{beat}: hero box {hb} is clipped by the frame {cv} at focus frame {f}",
                                beat=beat, focus_frame=f, hero_box=hb, canvas=cv)
        out["hero_box"] = hb
    return out


# ── K. the world fills the frame at every zoom (RENTOK-GAME-V2-006, LJ-15 / DET 'world fills the frame') ──

def check_world_fills_frame(camera_scales, *, min_scale: float = 1.0) -> dict:
    """Every logged camera scale must be >= `min_scale` (1.0 = the world exactly fills the frame; a
    pull-out below it shows the frame's own background beside the world — a black band or letterbox).
    The V2 job's camera moved 1.0–1.6 across 900 frames and its checker confirmed no band on any of 61
    frames (LJ-15); this gate makes that a refusal instead of an eye check. No scales logged → refused:
    an unlogged camera is not a verified one. `camera_scales` is an iterable of (frame, scale) or of
    bare scales."""
    lo = float(min_scale)
    rows = []
    for i, item in enumerate(camera_scales):
        if isinstance(item, (tuple, list)):
            frame, scale = int(item[0]), float(item[1])
        else:
            frame, scale = i, float(item)
        rows.append((frame, scale))
    if not rows:
        raise LayoutRefused(LayoutRefused.WORLD_SMALLER_THAN_FRAME,
                            "no camera scales logged; whether the world fills the frame is unverified", frames=0)
    for frame, scale in rows:
        if scale + 1e-9 < lo:
            raise LayoutRefused(LayoutRefused.WORLD_SMALLER_THAN_FRAME,
                                f"frame {frame}: camera scale {scale:.3f} < {lo:.3f} — the world is smaller than the frame",
                                frame=frame, scale=scale, min_scale=lo)
    scales = [s for _, s in rows]
    return {"status": "PASS", "frames": len(rows), "min_scale": min(scales), "max_scale": max(scales), "limit": lo}


# ── L. one character, several sheets, one pixel density (RENTOK-GAME-V2-006 N5 / LJ-11) ──────────

def check_sprite_density(standing_heights: dict, *, min_ratio: float = 0.8) -> dict:
    """When one character is drawn from more than one sprite sheet, the sheets' standing-cell heights
    (source pixels for the same standing figure) must agree within `min_ratio` (smallest ÷ largest).
    Sheets that differ are scaled to the same screen height, so their pixel grain differs on screen:
    the V2 job's base sheet stood 561 px, its two expression sheets 344 and 342 px (ratio 0.61), and every
    swap between a base run pose and a sheet pose popped in grain and proportion — some 150 times in the
    film (checker N5). The producer had recorded the 60 % figure and accepted it as 'not visible at phone
    size' (INFERRED); the checker found the pop visible. The threshold is the caller's; the default 0.8
    is a starting point, not a measured perceptual limit. One sheet is nothing to compare: PASS."""
    ratio_min = float(min_ratio)
    if not (0.0 < ratio_min <= 1.0):
        raise ValueError("min_ratio must be in (0, 1]")
    heights = {}
    for name in sorted(standing_heights):
        h = float(standing_heights[name])
        if h <= 0:
            raise ValueError(f"sheet {name}: standing height must be > 0, got {h}")
        heights[name] = h
    if len(heights) < 2:
        return {"status": "PASS", "sheets": list(heights), "ratio": 1.0, "limit": ratio_min, "note": "one sheet; nothing to compare"}
    lo_name = min(heights, key=heights.get)
    hi_name = max(heights, key=heights.get)
    ratio = heights[lo_name] / heights[hi_name]
    if ratio < ratio_min:
        raise LayoutRefused(LayoutRefused.SPRITE_DENSITY_MISMATCH,
                            f"sheet {lo_name} stands {heights[lo_name]:.0f} px against {hi_name} at {heights[hi_name]:.0f} px "
                            f"(ratio {ratio:.2f} < {ratio_min:.2f}); the character will change grain at every pose swap",
                            smallest=lo_name, largest=hi_name, ratio=round(ratio, 4), limit=ratio_min, heights=heights)
    return {"status": "PASS", "sheets": list(heights), "ratio": round(ratio, 4), "limit": ratio_min}
# ── M. voice-over schedule (CUMINCO-CHOPSTICKS-003, DF-08) ───────────────────

def check_vo_schedule(lines, *, film_end_s: float, min_gap_s: float = 0.0) -> dict:
    """Voice-over lines are placed from their MEASURED durations, never from a plan: two lines may not
    overlap (nor sit closer than `min_gap_s`), and no line may run past the end of the film. Case 003:
    six lines were placed at hand-set start times from an 18-s plan; measured afterwards, line 1 overlapped
    line 2 by 0.92 s and the closing line overran the film by 0.94 s — the human heard "voices overlapping".
    Text overflow already failed closed (check_text_bounds); audio overflow did not. Each line is
    {"id", "start_s", "duration_s"}; durations are what the trimmed file actually measures."""
    rows = []
    for ln in lines:
        start, dur = float(ln["start_s"]), float(ln["duration_s"])
        if dur <= 0:
            raise ValueError(f"vo line {ln.get('id')!r}: duration must be measured and positive")
        rows.append((start, start + dur, str(ln.get("id"))))
    rows.sort()
    end = float(film_end_s)
    for i in range(1, len(rows)):
        prev, cur = rows[i - 1], rows[i]
        if cur[0] < prev[1] + float(min_gap_s):
            raise LayoutRefused(LayoutRefused.VO_LINES_OVERLAP,
                                f"vo line {cur[2]} starts at {cur[0]:.2f}s but {prev[2]} ends at {prev[1]:.2f}s"
                                + (f" (gap < {min_gap_s}s)" if min_gap_s else ""),
                                pair=(prev[2], cur[2]), overlap_s=round(prev[1] + float(min_gap_s) - cur[0], 3))
    for start, stop, lid in rows:
        if stop > end + 1e-6:
            raise LayoutRefused(LayoutRefused.VO_OVERRUNS_END,
                                f"vo line {lid} ends at {stop:.2f}s, after the film ends at {end:.2f}s",
                                id=lid, overrun_s=round(stop - end, 3))
    return {"status": "PASS", "lines": [r[2] for r in rows], "film_end_s": end, "min_gap_s": float(min_gap_s),
            "last_line_ends_s": round(rows[-1][1], 3) if rows else None}
