"""Deterministic composition (Mechanism B): exact copy + the customer's logo over generated plates, end cards
and film supers. Every placement is measured and passed through runtime.compositor.gates; each gate result
(PASS or the refusal) is returned as a check row for the exact output file.

The creative director decides the hierarchy and the text zone; this module executes it. It does not impose a
template beyond a safe margin, a type scale and the contrast rule.
"""
from __future__ import annotations

import re
from pathlib import Path

from product import media
from runtime.compositor import gates as G

WHITE, INK = "#ffffff", "#141414"
# "Large text" (WCAG 3:1) is judged at the size a phone shows the ad, not in canvas pixels: a 1080-px-wide ad is
# ~390 CSS px on a phone, so 24 CSS px ≈ 6 % of the canvas width. Below that a line is body text and needs 4.5:1.
DISPLAY_FRAC = 0.06


def _role(size: int, canvas_w: int) -> str:
    return "display" if size >= canvas_w * DISPLAY_FRAC else "body"


def gate(check_id: str, control: str, fn, *args, **kw) -> dict:
    try:
        r = fn(*args, **kw)
        return {"check_id": check_id, "control": control, "status": "PASS", "detail": _short(r), "evidence": r}
    except G.LayoutRefused as e:
        return {"check_id": check_id, "control": control, "status": "FAIL", "detail": str(e)[:600], "evidence": {}}


def _short(r: dict) -> str:
    keys = ("worst_ratio", "required", "box", "container", "pairs_checked", "covered_frac", "worst_channel_delta", "fraction_shown")
    return ", ".join(f"{k}={r[k]}" for k in keys if k in r) or "PASS"


def is_logo_line(c: dict) -> bool:
    """A copy-deck entry the director assigned to the supplied logo: it IS the logo, placed as the image, never typeset
    (live 2026-09-23: 'Supplied logo asset used unaltered, not recreated as typeset' was typeset as 'Mokobara' three times)."""
    return bool(re.search(r"\b(logo|wordmark|brand mark)\b", c.get("role") or "", re.I))


def _lines(direction: dict, ids: list | None = None, logo_present: bool = True) -> list:
    deck = {c["id"]: c for c in direction.get("copy_deck", [])}
    order = ids or [c["id"] for c in direction.get("copy_deck", [])]
    return [deck[i] for i in order if i in deck and not (logo_present and is_logo_line(deck[i]))]


def _ink_for(samples_fn, box, role) -> tuple:
    """Pick white or dark ink by the worst-pixel rule on the real pixels; None if neither passes."""
    samples = samples_fn(box)
    for ink in (WHITE, INK):
        r = gate("contrast", "CONTRAST_GATE", G.check_contrast, ink, samples, role=role)
        if r["status"] == "PASS":
            return ink, r
    return None, gate("contrast", "CONTRAST_GATE", G.check_contrast, WHITE, samples, role=role)


def lockup_ad(*, plate: Path, out: Path, aspect: str, direction: dict, logo: Path | None, workdir: Path,
              product_box_norm: list | None, zone: str) -> tuple:
    """Top/bottom copy zone as ONE brand lockup: the logo leads (the largest element), then the headline, then the rest.
    The block keeps a measured clearance from the product; if the plate's empty band is too small, the picture is scaled
    down and the background extended (founder, 2026-09-23: "text is overlapping the image; brand name/logo is smaller
    than the tag line")."""
    W, H = media.FORMAT_PX[aspect]
    m = int(min(W, H) * 0.06)
    safe = (m, m, W - m, H - m)
    lines = _lines(direction, logo_present=logo is not None)
    gap, clear = int(H * 0.022), int(H * 0.05)
    items = []                                    # (id, kind, payload, w, h, meta)
    if logo is not None:
        lp = media.logo_png(logo, int(W * 0.40), workdir / f"lockup-logo-{W}x{H}-{Path(out).stem}.png")
        lw, lh = _png_size(lp)
        if lh > H * 0.09:                         # a tall mark is capped by height, not width
            lp = media.logo_png(logo, int(lw * H * 0.09 / lh), workdir / f"lockup-logo-{W}x{H}-{Path(out).stem}-h.png")
            lw, lh = _png_size(lp)
        items.append(("logo", "image", lp, lw, lh, None))
    for i, c in enumerate(lines):
        start = int(W * (0.058 if i == 0 else 0.034))
        if logo is not None and i == 0:
            start = min(start, int(items[0][4] * 0.8))   # the headline never outweighs the brand
        size, (dx, dy, tw, th) = media.fit_text(c["text"], max_w=W - 2 * m, start_size=start, min_size=max(22, int(start * 0.5)),
                                                kind="bold" if i == 0 else "regular")
        items.append((c["id"], "text", c, tw, th, (size, dx, dy, i)))
    gaps = [int(gap * 1.6) if it[0] == "logo" else gap for it in items[:-1]]   # the brand mark gets air below it
    block = sum(it[4] for it in items) + sum(gaps)
    need = m + block + clear
    free = media.calm_extent(plate, canvas=(W, H), side=zone)
    src, extended = plate, 0
    base_free = free
    for _ in range(3):                  # re-measure after each extension (8-px sampling + the feathered edge)
        if free >= need:
            break
        # shrinking the picture by f also moves its content: extra + free·(H − extra)/H ≥ need
        extended += int((need - free) / max(0.2, 1 - base_free / H)) + 8
        src = media.extend_plate(plate, canvas=(W, H), extra=extended, side=zone, out=workdir / f"{Path(plate).stem}-{zone}-ext-{W}x{H}.png")
        free = media.calm_extent(src, canvas=(W, H), side=zone)
    y = m if zone == "top" else H - m - block
    sample = lambda box: media.luminance_samples(src, box, canvas=(W, H))
    checks, layers, boxes = [], [], {}
    for name, kind, payload, w, h, meta in items:
        x = (W - w) // 2
        box = (x, y, x + w, y + h)
        boxes[name] = box
        if kind == "image":
            layers.append({"type": "image", "path": payload, "x": x, "y": y})
        else:
            size, dx, dy, i = meta
            role = _role(size, W)
            ink, cres = _ink_for(sample, box, role)
            if ink is None:
                pad = int(size * 0.3)
                layers.append({"type": "box", "x": box[0] - pad, "y": box[1] - pad, "w": w + 2 * pad, "h": h + 2 * pad, "colour": INK})
                ink = WHITE
                cres = gate("contrast", "CONTRAST_GATE", G.check_contrast, ink, [], role=role, backing_hex=INK)
            cres["check_id"] = f"contrast:{name}"
            checks.append(cres)
            layers.append({"type": "text", "text": payload["text"], "size": size, "colour": ink, "x": x - dx, "y": y - dy,
                           "kind": "bold" if i == 0 else "regular"})
            checks.append(gate(f"fit:{name}", "CROP_FIT_DECLARATION", G.check_fit, {"id": name, "fit": "contain", "source_size": (w, h), "box": box}))
        checks.append(gate(f"bounds:{name}", "TEXT_BOUNDS_GATE", G.check_text_bounds, box, canvas=(0, 0, W, H), container=safe, id_=name))
        y += h + (int(gap * 1.6) if name == "logo" else gap)
    checks.append(gate("disjoint", "ELEMENT_DISJOINTNESS", G.check_disjoint, boxes, critical=tuple(boxes), min_gap_px=8))
    # measured clearance: the lockup ends before the picture's content starts, with room to breathe
    block_edge = max(b[3] for b in boxes.values()) if zone == "top" else H - min(b[1] for b in boxes.values())
    ok = block_edge + clear <= free + 1
    checks.append({"check_id": "clear_of_product", "control": "HERO_VISIBLE", "status": "PASS" if ok else "FAIL",
                   "detail": f"copy ends {block_edge}px from the {zone} edge; picture content starts at {free}px; clearance needed {clear}px"
                             + (f"; background extended by {extended}px" if extended else ""),
                   "evidence": {"block_edge": block_edge, "content_start": free, "clearance": clear, "extended_px": extended}})
    if product_box_norm and len(product_box_norm) == 4:
        pb = (int(product_box_norm[0] * W), int(product_box_norm[1] * H), int(product_box_norm[2] * W), int(product_box_norm[3] * H))
        checks.append(gate("hero_visible", "HERO_VISIBLE", G.check_hero_visible, pb, boxes, max_covered_frac=0.05, id_="product"))
    else:
        checks.append({**checks[-1], "check_id": "hero_visible", "detail": "measured on the picture: " + checks[-1]["detail"]})
    media.compose(canvas=(W, H), out=out, plate=src, layers=layers)
    return out, checks, {"canvas": [W, H], "safe": safe, "zone": zone, "boxes": boxes, "extended_px": extended,
                         "rendered_text": [L["text"] for L in layers if L["type"] == "text"]}


def still_ad(*, plate: Path, out: Path, aspect: str, direction: dict, logo: Path | None, workdir: Path,
             product_box_norm: list | None) -> tuple:
    """Compose one format. Returns (out_path, checks, layout)."""
    zone0 = (direction.get("composition") or {}).get("text_zone", "top")
    if zone0 in ("top", "bottom", "none"):
        return lockup_ad(plate=plate, out=out, aspect=aspect, direction=direction, logo=logo, workdir=workdir,
                         product_box_norm=product_box_norm, zone="bottom" if zone0 == "none" else zone0)
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
        # the zone ends where the picture's content begins (measured), so copy never sits on the product
        free = media.calm_extent(plate, canvas=(W, H), side=zone) - int(m * 0.5)
        if product_box_norm and len(product_box_norm) == 4:
            free = min(free, int((product_box_norm[1] if zone == "top" else 1 - product_box_norm[3]) * H) - int(m * 0.5))
        zh = max(int(H * 0.10), min(zh, free - m))
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
    rows = []
    for c, size, dx, dy, tw, th in placed:
        x_ink = zbox[0] + (max_w - tw) // 2
        box = (x_ink, y, x_ink + tw, y + th)
        role = _role(size, W)
        ink, cres = _ink_for(sample, box, role)
        rows.append([c, size, dx, dy, box, role, ink, cres])
        y += th + gap
    if any(r[6] is None for r in rows):
        # Some line reads in neither ink on these pixels: one opaque panel behind the whole text block, every line
        # white on it (one panel, not per-line boxes that crowd the next line). Recorded as a backed contrast check.
        pad = int(base * 0.35)
        x0 = min(r[4][0] for r in rows) - pad; y0 = rows[0][4][1] - pad
        x1 = max(r[4][2] for r in rows) + pad; y1 = rows[-1][4][3] + pad
        panel = (max(0, x0), max(0, y0), min(W, x1), min(H, y1))
        layers.append({"type": "box", "x": panel[0], "y": panel[1], "w": panel[2] - panel[0], "h": panel[3] - panel[1], "colour": INK})
        for r in rows:
            r[6] = WHITE
            r[7] = gate("contrast", "CONTRAST_GATE", G.check_contrast, WHITE, [], role=r[5], backing_hex=INK)
    for c, size, dx, dy, box, role, ink, cres in rows:
        cres["check_id"] = f"contrast:{c['id']}"
        checks.append(cres)
        layers.append({"type": "text", "text": c["text"], "size": size, "colour": ink, "x": box[0] - dx, "y": box[1] - dy,
                       "kind": "bold" if c is placed[0][0] else "regular"})
        checks.append(gate(f"bounds:{c['id']}", "TEXT_BOUNDS_GATE", G.check_text_bounds, box, canvas=(0, 0, W, H), container=safe,
                           id_=c["id"]))
        checks.append(gate(f"fit:{c['id']}", "CROP_FIT_DECLARATION", G.check_fit,
                           {"id": c["id"], "fit": "contain", "source_size": (box[2] - box[0], box[3] - box[1]), "box": box}))
        boxes[c["id"]] = box
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
    return out, checks, {"canvas": [W, H], "safe": safe, "zone": zone, "boxes": boxes,
                         "rendered_text": [L["text"] for L in layers if L["type"] == "text"]}


def _png_size(p: Path) -> tuple:
    import struct
    b = Path(p).read_bytes()[:24]
    return struct.unpack(">II", b[16:24])


def end_card(*, out: Path, size: tuple, direction: dict, logo: Path | None, workdir: Path) -> tuple:
    W, H = size
    bg = (direction.get("end_card") or {}).get("background_hex") or "#101010"
    m = int(min(W, H) * 0.08)
    safe = (m, m, W - m, H - m)
    lines = _lines(direction, (direction.get("end_card") or {}).get("copy_ids"), logo_present=logo is not None)
    ink = WHITE if G.contrast_ratio(G.relative_luminance(WHITE), G.relative_luminance(bg)) >= 4.5 else INK
    items, checks, boxes = [], [], {}
    if logo is not None:
        lp = media.logo_png(logo, int(W * 0.5), workdir / "endcard-logo.png")
        lw, lh = _png_size(lp)
        items.append(("logo", lp, lw, lh, None))
    for i, c in enumerate(lines):
        start = int(min(W, H) * (0.13 if i == 0 else 0.08))          # the name big, the line after it readable at a glance
        size, (dx, dy, tw, th) = media.fit_text(c["text"], max_w=W - 2 * m, start_size=start, min_size=40, kind="bold" if i == 0 else "regular")
        items.append((c["id"], c["text"], tw, th, (size, dx, dy, i)))
    gap = int(min(W, H) * 0.045)
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
        if meta is not None:
            checks.append(gate(f"fit:{name}", "CROP_FIT_DECLARATION", G.check_fit, {"id": name, "fit": "contain", "source_size": (w, h), "box": box}))
        y += h + gap
    checks.append(gate("disjoint", "ELEMENT_DISJOINTNESS", G.check_disjoint, boxes, critical=tuple(boxes), min_gap_px=16))
    media.compose(canvas=(W, H), out=out, background_hex=bg, layers=layers)
    corner = media.mean_rgb(out, (0, 0, max(8, m // 2), max(8, m // 2)), canvas=(W, H))
    checks.append(gate("brand_colour:end_card", "BRAND_COLOUR_ON_RENDERED_FRAME", G.check_brand_colour, corner, bg,
                       id_="end_card_background"))
    return out, checks, {"boxes": boxes, "background_hex": bg, "rendered_text": [L["text"] for L in layers if L["type"] == "text"]}


def super_overlay(*, out: Path, size: tuple, text: str, clip: Path, clip_in: float, use: float, clip_size: tuple) -> tuple:
    """A full-frame transparent PNG carrying one line in the lower third; contrast sampled from the clip frames it sits on."""
    W, H = size
    m = int(min(W, H) * 0.07)
    # sized by the frame's SHORT side (a vertical film's words were ~3% of its height — too small for 50+ eyes, 2026-09-25)
    s, (dx, dy, tw, th) = media.fit_text(text, max_w=W - 2 * m, start_size=int(min(W, H) * 0.085), min_size=36, kind="bold")
    x, y = (W - tw) // 2, int(H * (0.76 if H > W else 0.78))
    box = (x, y, x + tw, y + th)
    samples = []
    for k in range(4):
        t = clip_in + use * (k + 0.5) / 4
        samples += media.luminance_samples(clip, box, canvas=(W, H), t=t, grid=12)
    ink, cres = _ink_for(lambda _b: samples, box, _role(s, W))
    layers = []
    checks = []
    if ink is None:
        # a soft darkening of the lower frame (a film's grade, not a subtitle box); contrast is checked against the frame
        # as it will be seen under it (black at up to 70 %: linear luminance x 0.3)
        peak, steps = 0.75, 12
        solid = max(0, y - int(th * 0.5))                 # behind and below the words: black at `peak`
        top = max(0, solid - int(th * 2.0))               # above them: a ramp from clear to `peak`, in bands that never overlap
        for i in range(steps):
            y0, y1 = top + (solid - top) * i // steps, top + (solid - top) * (i + 1) // steps
            if y1 > y0:
                layers.append({"type": "box", "x": 0, "y": y0, "w": W, "h": y1 - y0, "colour": f"#000000{int(255 * peak * (i + 1) / (steps + 1)):02x}"})
        layers.append({"type": "box", "x": 0, "y": solid, "w": W, "h": H - solid, "colour": f"#000000{int(255 * peak):02x}"})
        ink = WHITE
        cres = gate("contrast:super", "CONTRAST_GATE", G.check_contrast, ink, [v * (1 - peak) for v in samples], role=_role(s, W))
    cres["check_id"] = "contrast:super"
    checks.append(cres)
    layers.append({"type": "text", "text": text, "size": s, "colour": ink, "x": x - dx, "y": y - dy, "kind": "bold"})
    checks.append(gate("bounds:super", "TEXT_BOUNDS_GATE", G.check_text_bounds, box, canvas=(0, 0, W, H),
                       container=(m, m, W - m, H - m), id_="super"))
    checks.append(gate("fit:super", "CROP_FIT_DECLARATION", G.check_fit, {"id": "super", "fit": "contain", "source_size": (tw, th), "box": box}))
    media.compose(canvas=(W, H), out=out, layers=layers, transparent=True)
    return out, checks
