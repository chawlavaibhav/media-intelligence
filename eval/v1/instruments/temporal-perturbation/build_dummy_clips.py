#!/usr/bin/env python3
"""Constructed stand-in clips, so the perturbation machinery can be proven today.

WHAT THESE ARE, AND WHAT THEY ARE NOT
-------------------------------------
These are simple synthetic clips drawn by this file: a moving figure with a
fixed identity colouring, a static product block, a line of on-screen text, and
a progress bar whose fill only ever increases. Two of the clips cut between
shots.

They exist for ONE reason: to prove that the perturbation, manifest, rebuild,
verification and fail-closed machinery actually works, without waiting for and
without spending anything on real footage.

They are NOT a qualification pack, and running an instrument against them
qualifies nothing. The frozen family-4 conditions are real footage; a checker
that finds a colour block moving on a flat background has been told nothing
about whether it can find identity drift in a real person. Every artifact this
file produces is stamped `material_class: constructed_stand_in` so it can never
be mistaken for the approved 12-clip pack in a later report.

Deterministic: integer arithmetic and a fixed schedule, no RNG, no clock.
"""
from __future__ import annotations

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from clipseq import ClipSequence  # noqa: E402

W, H, FPS, N_FRAMES = 192, 108, 12, 48

# 5x7 glyphs, two hex characters per row, high three bits unused.
FONT = {
    "A": "0E11111F111111", "B": "1E11111E11111E", "C": "0E11101010110E",
    "D": "1E11111111111E", "E": "1F10101E10101F", "F": "1F10101E101010",
    "G": "0E11101711110F", "H": "1111111F111111", "I": "0E04040404040E",
    "J": "0702020202120C", "K": "11121418141211", "L": "1010101010101F",
    "M": "111B1515111111", "N": "11191513111111", "O": "0E11111111110E",
    "P": "1E11111E101010", "Q": "0E11111115120D", "R": "1E11111E141211",
    "S": "0F10100E01011E", "T": "1F040404040404", "U": "1111111111110E",
    "V": "11111111110A04", "W": "11111115151B11", "X": "11110A040A1111",
    "Y": "11110A04040404", "Z": "1F01020408101F",
    "0": "0E11131519110E", "1": "040C040404040E", "2": "0E11010204081F",
    "3": "1F02040201110E", "4": "02060A121F0202", "5": "1F101E0101110E",
    "6": "0608101E11110E", "7": "1F010204080808", "8": "0E11110E11110E",
    "9": "0E11110F01021C",
    " ": "00000000000000", "%": "11120408120100",
    "-": "0000001F000000", ".": "00000000000C0C",
}
GLYPH_SCALE = 2
GLYPH_ADVANCE = (5 + 1) * GLYPH_SCALE

# Region boxes are geometry, not judgements. A bounding box says WHERE to look;
# it never says whether anything is wrong. No human label is involved.
TEXT_BOX = (8, 88, 176, 14)
PRODUCT_BOX = (132, 36, 40, 34)


def _fill(frame, x, y, w, h, rgb):
    r, g, b = rgb
    for yy in range(max(0, y), min(H, y + h)):
        base = yy * W * 3
        for xx in range(max(0, x), min(W, x + w)):
            o = base + xx * 3
            frame[o], frame[o + 1], frame[o + 2] = r, g, b


def _disc(frame, cx, cy, r, rgb):
    rr = r * r
    for yy in range(max(0, cy - r), min(H, cy + r + 1)):
        dy = yy - cy
        for xx in range(max(0, cx - r), min(W, cx + r + 1)):
            dx = xx - cx
            if dx * dx + dy * dy <= rr:
                o = (yy * W + xx) * 3
                frame[o], frame[o + 1], frame[o + 2] = rgb


def render_text(frame, width, box, text, fg=(255, 255, 255), bg=(18, 18, 24)):
    """Draw `text` into `box`, clearing the box first.

    Used by this builder and, for constructed clips only, by the
    text_glyph_substitution perturbation. Real supplied footage cannot use it,
    because we do not own its glyphs.
    """
    x0, y0, w, h = box
    for yy in range(y0, y0 + h):
        base = yy * width * 3
        for xx in range(x0, x0 + w):
            o = base + xx * 3
            frame[o], frame[o + 1], frame[o + 2] = bg
    pen = x0 + 2
    for ch in text.upper():
        rows = FONT.get(ch, FONT[" "])
        for ry in range(7):
            bits = int(rows[ry * 2:ry * 2 + 2], 16)
            for rx in range(5):
                if not (bits >> (4 - rx)) & 1:
                    continue
                for sy in range(GLYPH_SCALE):
                    py = y0 + 1 + ry * GLYPH_SCALE + sy
                    if not (y0 <= py < y0 + h):
                        continue
                    for sx in range(GLYPH_SCALE):
                        px = pen + rx * GLYPH_SCALE + sx
                        if not (x0 <= px < x0 + w):
                            continue
                        o = (py * width + px) * 3
                        frame[o], frame[o + 1], frame[o + 2] = fg
        pen += GLYPH_ADVANCE
        if pen >= x0 + w:
            break


# Twelve stand-ins, mirroring the shape RESOURCE-REQUESTS asks of the real pack:
# every clip carries a person, a product and on-screen text, and at least two
# clips cut between shots.
SPECS = [
    ("dummy-01", (214, 176, 140), (40, 90, 200), (60, 62, 78), "SAVE 20%", 1),
    ("dummy-02", (150, 110, 80), (200, 70, 60), (30, 70, 60), "NEW ARRIVAL", 1),
    ("dummy-03", (232, 200, 170), (90, 60, 170), (70, 70, 40), "AAJ KI DEAL", 1),
    ("dummy-04", (120, 84, 60), (30, 120, 110), (110, 40, 50), "FREE SHIP", 1),
    ("dummy-05", (198, 158, 120), (170, 120, 40), (40, 40, 90), "BUY 1 GET 1", 1),
    ("dummy-06", (176, 130, 96), (60, 140, 60), (120, 60, 120), "ORDER NOW", 1),
    ("dummy-07", (240, 210, 190), (50, 50, 140), (140, 90, 30), "LIMITED", 1),
    ("dummy-08", (130, 95, 70), (120, 30, 90), (30, 100, 130), "20 PERCENT", 1),
    ("dummy-09", (206, 168, 132), (35, 105, 95), (95, 45, 105), "SHOP TODAY", 1),
    ("dummy-10", (162, 118, 88), (145, 95, 45), (45, 85, 145), "BEST PRICE", 1),
    ("dummy-11", (222, 190, 158), (55, 75, 165), (165, 75, 55), "TWO SHOT AD", 2),
    ("dummy-12", (142, 102, 76), (75, 145, 75), (145, 55, 95), "CUT TEST", 2),
]


def build_clip(spec) -> ClipSequence:
    clip_id, identity, bg1, bg2, text, n_shots = spec
    skin = identity
    shirt = (255 - identity[0], identity[1] // 2 + 60, identity[2] // 2 + 40)
    hair = (identity[0] // 3, identity[1] // 3, identity[2] // 3)
    product = ((identity[2] + 90) % 256, (identity[0] + 40) % 256, (identity[1] + 120) % 256)

    shots = ([(0, N_FRAMES)] if n_shots == 1
             else [(0, N_FRAMES // 2), (N_FRAMES // 2, N_FRAMES)])
    frames = []
    for i in range(N_FRAMES):
        shot = 0 if i < shots[0][1] else 1
        bg = bg1 if shot == 0 else bg2
        f = bytearray()
        row = bytes(bg) * W
        for _ in range(H):
            f += row

        # Person: walks left to right within the shot, always facing the way
        # they travel. A horizontal flip therefore reverses screen direction.
        local = i - shots[shot][0]
        span = max(1, shots[shot][1] - shots[shot][0] - 1)
        cx = 24 + (local * 96) // span
        cy = 54
        _fill(f, cx - 9, cy - 2, 18, 30, shirt)          # torso
        _disc(f, cx, cy - 10, 9, skin)                   # head
        _fill(f, cx - 9, cy - 20, 18, 5, hair)           # hair
        _fill(f, cx + 6, cy - 12, 4, 4, (20, 20, 20))    # facing marker (right)

        # Product: fixed block with a border, static in frame.
        px, py, pw, ph = PRODUCT_BOX
        _fill(f, px, py, pw, ph, product)
        _fill(f, px, py, pw, 3, (250, 250, 250))
        _fill(f, px, py + ph - 3, pw, 3, (250, 250, 250))

        # Visible monotone state: a bar that only ever fills further. Reorder
        # the frames and the state provably runs backwards.
        _fill(f, 8, 8, 176, 8, (25, 25, 30))
        _fill(f, 8, 8, 8 + (168 * i) // (N_FRAMES - 1), 8, (245, 205, 60))

        render_text(f, W, TEXT_BOX, text)
        frames.append(f)

    provenance = {
        "material_class": "constructed_stand_in",
        "built_by": "eval/v1/instruments/temporal-perturbation/build_dummy_clips.py",
        "not_a_qualification_pack": True,
        "regions": {"text": list(TEXT_BOX), "product": list(PRODUCT_BOX)},
        "region_source": "declared_by_constructor",
        "shots": [list(s) for s in shots],
        "text_string": text,
        "identity_colours": {"skin": list(skin), "shirt": list(shirt), "hair": list(hair)},
    }
    return ClipSequence(clip_id, W, H, FPS, frames, provenance)


def build_all() -> list:
    return [build_clip(s) for s in SPECS]


def main() -> int:
    ap = argparse.ArgumentParser(description="Build constructed stand-in base clips.")
    ap.add_argument("--out-dir", default=None)
    args = ap.parse_args()
    root = pathlib.Path(__file__).resolve().parents[4]
    out = (pathlib.Path(args.out_dir) if args.out_dir else
           root / "eval/v1/instruments/temporal-perturbation/fixtures/base-standin")
    out.mkdir(parents=True, exist_ok=True)
    for clip in build_all():
        side = clip.write(out / clip.clip_id)
        print(f"{clip.clip_id}  {side['n_frames']} frames  "
              f"motion_load={side['motion_load']:.6f}  {side['content_hash'][:16]}")
    print(f"\n{len(SPECS)} constructed stand-in clips written to {out}")
    print("These prove the machinery. They qualify nothing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
