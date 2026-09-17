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


# ── F. voice-over schedule (CUMINCO-CHOPSTICKS-003, DF-08) ───────────────────

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
