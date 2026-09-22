"""Deterministic composition (Mechanism B): exact copy + the customer's logo over generated plates, end cards
and film supers. Every placement is measured and passed through runtime.compositor.gates; each gate result
(PASS or the refusal) is returned as a check row for the exact output file.

The creative director decides the hierarchy and the text zone; this module executes it. It does not impose a
template beyond a safe margin, a type scale and the contrast rule.
"""
from __future__ import annotations

from pathlib import Path

from product import media
from runtime.compositor import gates as G

WHITE, INK = "#ffffff", "#141414"


def gate(check_id: str, control: str, fn, *args, **kw) -> dict:
    try:
        r = fn(*args, **kw)
        return {"check_id": check_id, "control": control, "status": "PASS", "detail": _short(r), "evidence": r}
    except G.LayoutRefused as e:
        return {"check_id": check_id, "control": control, "status": "FAIL", "detail": str(e)[:600], "evidence": {}}


def _short(r: dict) -> str:
    keys = ("worst_ratio", "required", "box", "container", "pairs_checked", "covered_frac", "worst_channel_delta", "fraction_shown")
    return ", ".join(f"{k}={r[k]}" for k in keys if k in r) or "PASS"


def _lines(direction: dict, ids: list | None = None) -> list:
    deck = {c["id"]: c for c in direction.get("copy_deck", [])}
    order = ids or [c["id"] for c in direction.get("copy_deck", [])]
    return [deck[i] for i in order if i in deck]


def _ink_for(samples_fn, box, role) -> tuple:
    """Pick white or dark ink by the worst-pixel rule on the real pixels; None if neither passes."""
    samples = samples_fn(box)
    for ink in (WHITE, INK):
        r = gate("contrast", "CONTRAST_GATE", G.check_contrast, ink, samples, role=role)
        if r["status"] == "PASS":
            return ink, r
    return None, gate("contrast", "CONTRAST_GATE", G.check_contrast, WHITE, samples, role=role)


def still_ad(*, plate: Path, out: Path, aspect: str, direction: dict, logo: Path | None, workdir: Path,
             product_box_norm: list | None) -> tuple:
    """Compose one format. Returns (out_path, checks, layout)."""
    W, H = media.FORMAT_PX[aspect]
    m = int(min(W, H) * 0.06)
    safe = (m, m, W - m, H - m)
    zone = (direction.get("composition") or {}).get("text_zone", "top")
    zone = "bottom" if zone == "none" else zone
    lines = _lines(direction)
    checks, layers, boxes = [], [], {}
    # zone box inside the safe area
    if zone in ("top", "bottom"):
        zh = int((H - 2 * m) * 0.30)
        zbox = (m, m, W - m, m + zh) if zone == "top" else (m, H - m - zh, W - m, H - m)
    else:
        zw = int((W - 2 * m) * 0.42)
        zbox = (m, m, m + zw, H - m) if zone == "left" else (W - m - zw, m, W - m, H - m)
    max_w = zbox[2] - zbox[0]
    y = zbox[1]
    base = int(W * 0.075)
    placed = []
    for i, c in enumerate(lines):
        start = base if i == 0 else int(base * 0.55)
        size, (dx, dy, tw, th) = media.fit_text(c["text"], max_w=max_w, start_size=start, min_size=max(22, int(start * 0.45)),
                                                kind="bold" if i == 0 else "regular")
        placed.append((c, size, dx, dy, tw, th))
    gap = int(base * 0.35)
    total_h = sum(p[5] for p in placed) + gap * max(0, len(placed) - 1)
    y = zbox[1] + max(0, ((zbox[3] - zbox[1]) - total_h) // 2)
    sample = lambda box: media.luminance_samples(plate, box, canvas=(W, H))
    for c, size, dx, dy, tw, th in placed:
        x_ink = zbox[0] + (max_w - tw) // 2
        box = (x_ink, y, x_ink + tw, y + th)
        role = "display" if size >= 40 else "body"
        ink, cres = _ink_for(sample, box, role)
        if ink is None:     # neither ink reads: an opaque backing panel behind the zone, recorded as such
            pad = int(size * 0.35)
            panel = (max(0, box[0] - pad), max(0, box[1] - pad), min(W, box[2] + pad), min(H, box[3] + pad))
            layers.append({"type": "box", "x": panel[0], "y": panel[1], "w": panel[2] - panel[0], "h": panel[3] - panel[1],
                           "colour": INK})
            ink = WHITE
            cres = gate(f"contrast:{c['id']}", "CONTRAST_GATE", G.check_contrast, ink, [], role=role, backing_hex=INK)
        else:
            cres["check_id"] = f"contrast:{c['id']}"
        checks.append(cres)
        layers.append({"type": "text", "text": c["text"], "size": size, "colour": ink, "x": box[0] - dx, "y": box[1] - dy,
                       "kind": "bold" if c is placed[0][0] else "regular"})
        checks.append(gate(f"bounds:{c['id']}", "TEXT_BOUNDS_GATE", G.check_text_bounds, box, canvas=(0, 0, W, H), container=safe,
                           id_=c["id"]))
        checks.append(gate(f"fit:{c['id']}", "CROP_FIT_DECLARATION", G.check_fit,
                           {"id": c["id"], "fit": "contain", "source_size": (tw, th), "box": box}))
        boxes[c["id"]] = box
        y += th + gap
    if logo is not None:
        lw = int(W * 0.22)
        lp = media.logo_png(logo, lw, workdir / f"logo-{lw}.png")
        lwp, lhp = _png_size(lp)
        corner_y = H - m - lhp if zone == "top" else m
        lx = W - m - lwp
        lbox = (lx, corner_y, lx + lwp, corner_y + lhp)
        layers.append({"type": "image", "path": lp, "x": lx, "y": corner_y})
        boxes["logo"] = lbox
        checks.append(gate("bounds:logo", "TEXT_BOUNDS_GATE", G.check_text_bounds, lbox, canvas=(0, 0, W, H), container=safe, id_="logo"))
    crit = tuple(boxes)
    checks.append(gate("disjoint", "ELEMENT_DISJOINTNESS", G.check_disjoint, boxes, critical=crit, min_gap_px=8))
    if product_box_norm and len(product_box_norm) == 4:
        pb = (int(product_box_norm[0] * W), int(product_box_norm[1] * H), int(product_box_norm[2] * W), int(product_box_norm[3] * H))
        checks.append(gate("hero_visible", "HERO_VISIBLE", G.check_hero_visible, pb, boxes, max_covered_frac=0.05, id_="product"))
    else:
        checks.append({"check_id": "hero_visible", "control": "HERO_VISIBLE", "status": "NOT_VERIFIED",
                       "detail": "the product was not located on the plate by an independent inspection", "evidence": {}})
    media.compose(canvas=(W, H), out=out, plate=plate, layers=layers)
    return out, checks, {"canvas": [W, H], "safe": safe, "zone": zone, "boxes": boxes}


def _png_size(p: Path) -> tuple:
    import struct
    b = Path(p).read_bytes()[:24]
    return struct.unpack(">II", b[16:24])


def end_card(*, out: Path, size: tuple, direction: dict, logo: Path | None, workdir: Path) -> tuple:
    W, H = size
    bg = (direction.get("end_card") or {}).get("background_hex") or "#101010"
    m = int(min(W, H) * 0.08)
    safe = (m, m, W - m, H - m)
    lines = _lines(direction, (direction.get("end_card") or {}).get("copy_ids"))
    ink = WHITE if G.contrast_ratio(G.relative_luminance(WHITE), G.relative_luminance(bg)) >= 4.5 else INK
    items, checks, boxes = [], [], {}
    if logo is not None:
        lp = media.logo_png(logo, int(W * 0.5), workdir / "endcard-logo.png")
        lw, lh = _png_size(lp)
        items.append(("logo", lp, lw, lh, None))
    for i, c in enumerate(lines):
        start = int(W * (0.06 if i == 0 else 0.04))
        size, (dx, dy, tw, th) = media.fit_text(c["text"], max_w=W - 2 * m, start_size=start, min_size=24, kind="bold" if i == 0 else "regular")
        items.append((c["id"], c["text"], tw, th, (size, dx, dy, i)))
    gap = int(W * 0.04)
    total = sum(it[3] for it in items) + gap * max(0, len(items) - 1)
    y = (H - total) // 2
    layers = []
    for it in items:
        name, payload, w, h, meta = it
        x = (W - w) // 2
        box = (x, y, x + w, y + h)
        boxes[name] = box
        if meta is None:
            layers.append({"type": "image", "path": payload, "x": x, "y": y})
        else:
            size, dx, dy, i = meta
            layers.append({"type": "text", "text": payload, "size": size, "colour": ink, "x": x - dx, "y": y - dy,
                           "kind": "bold" if i == 0 else "regular"})
            checks.append(gate(f"contrast:{name}", "CONTRAST_GATE", G.check_contrast, ink, [], role="body", backing_hex=bg))
        checks.append(gate(f"bounds:{name}", "TEXT_BOUNDS_GATE", G.check_text_bounds, box, canvas=(0, 0, W, H), container=safe, id_=name))
        y += h + gap
    checks.append(gate("disjoint", "ELEMENT_DISJOINTNESS", G.check_disjoint, boxes, critical=tuple(boxes), min_gap_px=16))
    media.compose(canvas=(W, H), out=out, background_hex=bg, layers=layers)
    corner = media.mean_rgb(out, (0, 0, max(8, m // 2), max(8, m // 2)), canvas=(W, H))
    checks.append(gate("brand_colour:end_card", "BRAND_COLOUR_ON_RENDERED_FRAME", G.check_brand_colour, corner, bg,
                       id_="end_card_background"))
    return out, checks, {"boxes": boxes, "background_hex": bg}


def super_overlay(*, out: Path, size: tuple, text: str, clip: Path, clip_in: float, use: float, clip_size: tuple) -> tuple:
    """A full-frame transparent PNG carrying one line in the lower third; contrast sampled from the clip frames it sits on."""
    W, H = size
    m = int(min(W, H) * 0.07)
    s, (dx, dy, tw, th) = media.fit_text(text, max_w=W - 2 * m, start_size=int(W * 0.06), min_size=28, kind="bold")
    x, y = (W - tw) // 2, int(H * 0.74)
    box = (x, y, x + tw, y + th)
    samples = []
    for k in range(4):
        t = clip_in + use * (k + 0.5) / 4
        samples += media.luminance_samples(clip, box, canvas=(W, H), t=t, grid=12)
    ink, cres = _ink_for(lambda _b: samples, box, "display")
    layers = []
    checks = []
    if ink is None:
        pad = int(s * 0.4)
        layers.append({"type": "box", "x": box[0] - pad, "y": box[1] - pad, "w": tw + 2 * pad, "h": th + 2 * pad, "colour": INK})
        ink = WHITE
        cres = gate("contrast:super", "CONTRAST_GATE", G.check_contrast, ink, [], role="display", backing_hex=INK)
    cres["check_id"] = "contrast:super"
    checks.append(cres)
    layers.append({"type": "text", "text": text, "size": s, "colour": ink, "x": x - dx, "y": y - dy, "kind": "bold"})
    checks.append(gate("bounds:super", "TEXT_BOUNDS_GATE", G.check_text_bounds, box, canvas=(0, 0, W, H),
                       container=(m, m, W - m, H - m), id_="super"))
    media.compose(canvas=(W, H), out=out, layers=layers, transparent=True)
    return out, checks
