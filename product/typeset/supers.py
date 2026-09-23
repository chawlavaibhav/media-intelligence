"""Film supers (on-screen captions) through the same type system as posters and end cards.

A super sits over MOVING pictures, so it is judged against several frames of the shot, not one: it must be readable
and on calm ground in every sampled frame, or it gets an opaque backing (a pill in the brand colour). It must also stay
on screen long enough to read. Output: a transparent RGBA overlay the size of the film + check rows.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from PIL import Image, ImageDraw

from product.typeset import engine as E

READ_WPS = 3.0          # words per second a viewer reads on a phone; plus a fixed 0.6 s to find the line
POSITIONS = {"lower": 0.84, "upper": 0.12, "middle": 0.52}   # centre line as a fraction of the Reels-safe frame height


@dataclass
class Super:
    image: Image.Image
    box: tuple
    lines: list
    size: int
    backed: bool
    checks: list


def min_seconds(text: str) -> float:
    return round(0.6 + len(text.split()) / READ_WPS, 2)


def make(*, text: str, frames: list, fmt: str, kit: E.BrandKit, system_id: str, position: str | None = None,
         duration_s: float | None = None, allow_backing: bool = True, subject_box: list | None = None) -> Super:
    """`position` None = choose: the first of lower / upper / middle that keeps clear of `subject_box` (fractions of the
    frame: the product and the hands acting on it) and needs no backing; failing that, the first clear one, backed."""
    if position is not None:
        return _make(text, frames, fmt, kit, system_id, position, duration_s, allow_backing, subject_box)
    tries = [_make(text, frames, fmt, kit, system_id, p, duration_s, allow_backing, subject_box) for p in ("lower", "upper", "middle")]
    clear = [t for t in tries if not any(r["check_id"] == "super_clear_of_subject" and r["status"] != "PASS" for r in t.checks)]
    for t in clear:
        if not t.backed:
            return t
    return (clear or tries)[0]


def _make(text, frames, fmt, kit, system_id, position, duration_s, allow_backing, subject_box) -> Super:
    W, H = E.FORMAT_PX[fmt]
    frames = [f.convert("RGB").resize((W, H)) for f in frames] or [Image.new("RGB", (W, H), E._hex(kit.background))]
    frame = E.content_frame(fmt, W, H) or (int(W * 0.06), int(H * 0.06), int(W * 0.94), int(H * 0.94))
    sys_ = kit.resolve_system(system_id)
    c = {"id": "super", "text": text, "role": "sub"}
    size = max(int(W * 0.052), int(W * 0.036))            # 20 CSS px on a phone: a super is read in motion
    max_w = int((frame[2] - frame[0]) * 0.86)
    el = None
    while size >= int(W * 0.04):
        el = E._text_element(c, sys_, kit, size, max_w, 2, "center")
        if el is not None:
            break
        size = int(size * 0.94)
    if el is None:
        raise E.TypesetError(f"super does not fit two lines: {text!r}")
    w, h, asc = E._measure(el, kit)
    cy = frame[1] + int((frame[3] - frame[1]) * POSITIONS[position])
    x0 = (W - w) // 2
    y0 = cy - h // 2
    box = (x0, y0, x0 + w, y0 + h)
    pad = int(size * 0.45)
    pill = (x0 - pad, y0 - pad, x0 + w + pad, y0 + h + pad)
    # judge every frame: contrast (worst pixel) and calm ground, for dark and light ink
    from runtime.compositor.gates import LayoutRefused, check_contrast
    role = "display" if size * E.PHONE_CSS_WIDTH / W >= 24 else "body"
    ink, backed = None, False
    for cand in (kit.on_primary, kit.ink):
        ok = True
        for fr in frames:
            try:
                check_contrast(cand, E.luminance_grid(fr, box), role=role, id_="super")
            except LayoutRefused:
                ok = False
                break
        if ok:
            ink = cand
            break
    calm = all(_calm(fr, pill) for fr in frames)
    if ink is None or not calm:
        if not allow_backing:
            ink = ink or kit.on_primary
        else:
            backed, ink = True, kit.on_primary
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    if backed:
        d.rounded_rectangle(pill, radius=int(size * 0.5), fill=E._hex(kit.primary) + (255,))
    f = E.load_font(el.family, el.weight, el.size, kit.custom_families())
    yb, boxes = y0 + asc, []
    for L in el.lines:
        lw = E.tracked_length(f, L, el.tracking)
        boxes.append(E.draw_line(d, ((W - lw) / 2, yb), L, f, E._hex(ink) + (255,), el.tracking))
        yb += el.size * el.leading
    inked = (min(b[0] for b in boxes), min(b[1] for b in boxes), max(b[2] for b in boxes), max(b[3] for b in boxes))
    rows = []
    rows.append(_row("super_exact", " ".join(el.lines) == " ".join(text.split()), f"drawn: {el.lines}"))
    rows.append(_row("super_legible", size * E.PHONE_CSS_WIDTH / W >= 14, f"{size * E.PHONE_CSS_WIDTH / W:.1f} CSS px on a phone"))
    rows.append(_row("super_safe_area", E._inside(pill if backed else inked, frame), f"inside {frame}"))
    if backed:
        from runtime.compositor.gates import check_contrast as cc
        try:
            cc(ink, [], role=role, backing_hex=kit.primary, id_="super")
            rows.append(_row("super_contrast", True, f"{ink} on an opaque {kit.primary} pill"))
        except LayoutRefused as exc:
            rows.append(_row("super_contrast", False, str(exc)[:200]))
    else:
        rows.append(_row("super_contrast", True, f"{ink} readable in all {len(frames)} sampled frames"))
        rows.append(_row("super_calm_ground", calm, f"calm in all {len(frames)} sampled frames" if calm else "busy picture under the line"))
    if subject_box:
        sb = (int(subject_box[0] * W), int(subject_box[1] * H), int(subject_box[2] * W), int(subject_box[3] * H))
        from runtime.compositor.gates import overlaps
        rows.append(_row("super_clear_of_subject", not overlaps(pill if backed else inked, sb),
                         "clear of the product and hands" if not overlaps(pill if backed else inked, sb) else f"covers the subject {sb}"))
    if duration_s is not None:
        need = min_seconds(text)
        rows.append(_row("super_reading_time", duration_s >= need, f"on screen {duration_s:.1f} s, needs ≥ {need} s"))
    return Super(image=overlay, box=pill if backed else inked, lines=el.lines, size=size, backed=backed, checks=rows)


def _calm(img: Image.Image, box) -> bool:
    g = np.asarray(img.convert("L").crop(tuple(int(v) for v in box)), dtype=np.float32) / 255.0
    if g.size == 0:
        return True
    gy, gx = np.gradient(g)
    return float(g.std()) <= 0.10 and float(np.mean(np.hypot(gx, gy) > 0.08)) <= 0.06


def _row(cid, ok, detail):
    return {"check_id": cid, "status": "PASS" if ok else "FAIL", "blocking": not ok, "detail": detail}


def frames_from_video(path, times: list, fmt: str) -> list:
    """Sample frames at `times` (seconds) with ffmpeg; used by the pipeline to judge a super over its whole shot."""
    import subprocess
    import tempfile
    from pathlib import Path
    W, H = E.FORMAT_PX[fmt]
    out = []
    with tempfile.TemporaryDirectory() as d:
        for i, t in enumerate(times):
            p = Path(d) / f"f{i}.png"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(path), "-frames:v", "1",
                            "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}", str(p)], check=True)
            out.append(Image.open(p).convert("RGB"))
    return out
