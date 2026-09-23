"""Typography checks on a typeset layout. Each returns a row {check_id, status, blocking, detail}.

Blocking checks are facts a customer would call a defect (wrong words, unreadable, off the safe area, on top of the
product, on a busy picture). Non-blocking ones are craft flags the picker uses to rank (widows, long lines, small
product). None of them judges taste — that is the picker's judge and the founder's taste test.
"""
from __future__ import annotations

import numpy as np

from product.typeset import engine as E


def _row(cid, ok, detail, blocking=True, flag=False):
    return {"check_id": cid, "status": "PASS" if ok else ("FLAG" if flag else "FAIL"), "blocking": blocking and not ok and not flag,
            "detail": detail}


def _norm(s: str) -> str:
    return " ".join(s.split())


def run(L: dict) -> list:
    W, H = L["canvas"]
    texts = [e for e in L["elements"] if e.kind == "text"]
    logos = [e for e in L["elements"] if e.kind == "logo"]
    rows = []

    # 1. exact copy: every requested line is drawn, word for word, once
    wanted = {c["id"]: _norm(c["text"]) for c in L["copy"]}
    drawn = {e.id: _norm(" ".join(e.lines)) for e in texts}
    bad = [i for i in wanted if drawn.get(i) != wanted[i]]
    rows.append(_row("exact_copy", not bad, "all lines exact" if not bad else f"not drawn exactly: {bad}"))

    # 2. at most two families (a Devanagari companion face does not count)
    fams = {e.family for e in texts if not E.DEVANAGARI.search(e.text)}
    rows.append(_row("typeface_count", len(fams) <= 2, f"{len(fams)} families: {sorted(fams)}"))

    # 3. hierarchy: headline > sub > small, each step at least 1.2x
    sizes = {e.role: e.size for e in texts}
    order = [r for r in ("offer", "headline", "sub", "small") if r in sizes]
    if "offer" in order and sizes["offer"] < sizes.get("headline", 0):
        order = [r for r in ("headline", "offer", "sub", "small") if r in sizes]
    steps = [(a, b, sizes[a] / sizes[b]) for a, b in zip(order, order[1:])]
    weak = [f"{a}/{b}={r:.2f}" for a, b, r in steps if r < 1.2]
    rows.append(_row("hierarchy", not weak, "clear steps " + ", ".join(f"{a}/{b}={r:.2f}" for a, b, r in steps)
                     if not weak else "sizes too close: " + ", ".join(weak), blocking=False, flag=bool(weak)))

    # 4. legible on a phone
    small = [f"{e.role} {e.size * E.PHONE_CSS_WIDTH / W:.1f}px" for e in texts
             if e.size * E.PHONE_CSS_WIDTH / W < E.MIN_CSS_PX.get(e.role, E.MIN_CSS_PX["sub"] if e.role == "offer" else 12)]
    rows.append(_row("phone_legibility", not small, "every line ≥ its minimum on a 390-px phone" if not small
                     else "too small on a phone: " + ", ".join(small)))

    # 5. line length and widows (craft flags)
    long_ = [f"{e.role}: {len(L_)} chars" for e in texts for L_ in e.lines
             if len(L_) > (28 if e.role == "headline" else 45)]
    rows.append(_row("line_length", not long_, "ok" if not long_ else "; ".join(long_), blocking=False, flag=bool(long_)))
    widows = [e.role for e in texts if len(e.lines) > 1 and len(e.lines[-1].split()) == 1 and len(e.text.split()) >= 3]
    rows.append(_row("no_widows", not widows, "ok" if not widows else f"single word alone on the last line: {widows}",
                     blocking=False, flag=bool(widows)))

    # 6. safe area (and the Reels-safe area for 9:16, where Instagram draws its own buttons)
    m = L["margin"]
    safe = (m, m, W - m, H - m)
    if L["fmt"] == "9:16":
        rs = E.templates_registry()["reels_safe"]
        safe = (max(safe[0], int(rs[0] * W)), max(safe[1], int(rs[1] * H)), min(safe[2], int(rs[2] * W)), min(safe[3], int(rs[3] * H)))
    out = [f"{e.id or e.role} {e.box}" for e in L["elements"] if not E._inside(e.box, safe)]
    rows.append(_row("safe_area", not out, f"inside {safe}" if not out else "outside the safe area: " + "; ".join(out)))

    # 7. contrast (measured by the engine on the real pixels, WCAG worst-pixel rule)
    failed = [k for k, v in L["contrast"].items() if (v or {}).get("status") != "PASS"]
    rows.append(_row("contrast", not failed, "every line readable" if not failed else f"unreadable: {failed}"))

    # 8. calm ground: text on a picture must sit on a quiet area (not on a panel or a solid ground)
    busy = []
    g = np.asarray(L["ground"].convert("L"), dtype=np.float32) / 255.0
    for e in texts:
        if e.on_panel:
            continue
        x0, y0, x1, y1 = [int(v) for v in e.box]
        pad = int(e.size * 0.25)
        patch = g[max(0, y0 - pad):min(H, y1 + pad), max(0, x0 - pad):min(W, x1 + pad)]
        if patch.size == 0:
            continue
        gy, gx = np.gradient(patch)
        edges = float(np.mean(np.hypot(gx, gy) > 0.08))
        std = float(patch.std())
        if std > 0.10 or edges > 0.06:
            busy.append(f"{e.role} (spread {std:.2f}, edges {edges:.2f})")
    rows.append(_row("calm_ground", not busy, "text sits on calm ground" if not busy else "text over a busy picture: " + ", ".join(busy)))

    # 9. nothing covers the product
    pb = L.get("product_box")
    if pb:
        from runtime.compositor.gates import LayoutRefused, check_hero_visible
        fg = {(e.id or e.role): e.box for e in L["elements"]}
        try:
            check_hero_visible(pb, fg, max_covered_frac=0.02, id_="product")
            rows.append(_row("product_clear", True, "no text or logo over the product"))
        except LayoutRefused as exc:
            rows.append(_row("product_clear", False, str(exc)[:300]))
        frac = (pb[2] - pb[0]) * (pb[3] - pb[1]) / (W * H)
        rows.append(_row("product_scale", frac >= 0.16, f"product fills {frac:.0%} of the frame", blocking=False, flag=frac < 0.16))
    elif L["kind"] == "poster":
        rows.append({"check_id": "product_clear", "status": "NOT_VERIFIED", "blocking": False,
                     "detail": "no product box was supplied for the plate"})

    # 10. elements do not collide
    from runtime.compositor.gates import LayoutRefused, check_disjoint
    boxes = {(e.id or e.role): e.box for e in L["elements"]}
    try:
        check_disjoint(boxes, critical=tuple(boxes), min_gap_px=int(W * 0.012))
        rows.append(_row("no_collisions", True, "elements keep their distance"))
    except LayoutRefused as exc:
        rows.append(_row("no_collisions", False, str(exc)[:300]))

    # 11. logo: present when supplied, big enough, visible against its ground
    for e in logos:
        w = e.box[2] - e.box[0]
        img = getattr(e, "_drawn", None) or getattr(e, "_img")
        a = np.asarray(img, dtype=np.float32)
        ink = a[a[..., 3] > 128][:, :3]
        from runtime.compositor.gates import contrast_ratio
        ink_l = E._lum(np.median(ink, axis=0)) if len(ink) else 0.0
        ground_l = float(np.median(E.luminance_grid(L["ground"], e.box)))
        ratio = contrast_ratio(ink_l, ground_l)
        rows.append(_row("logo", w >= W * 0.12 and ratio >= 3.0, f"width {w}px, contrast {ratio:.1f}:1"))
    return rows


def blocking_failures(rows: list) -> list:
    return [r for r in rows if r["blocking"]]
