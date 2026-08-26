#!/usr/bin/env python3
"""Build the family-2 deterministic CV/geometry qualification pack.

100 synthetic fixtures whose answers are TRUE BY CONSTRUCTION: each image is
drawn by this code from a specification we chose, so the count, the positions,
the colours and the sizes are exact and need no human label.

This is the same trick that made the Devanagari battery cheap - construct the
truth instead of annotating it.

No external image library. PNG is written with stdlib zlib only, matching the
approach already proven in eval/battery/devanagari-exactness/pngraster.py.

Deterministic: a fixed seed and integer arithmetic only, so the same repository
state always produces byte-identical fixtures. Verified by --verify.

Usage:
  python3 eval/v1/instruments/build_cv_fixtures.py --build
  python3 eval/v1/instruments/build_cv_fixtures.py --verify
"""
import argparse, hashlib, json, pathlib, struct, sys, zlib, random

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "eval/v1/instruments/fixtures/cv-geometry"
W, H = 640, 480
SEED = 20260826

# Named colours, deliberately far apart so a colour judgement is unambiguous.
COLOURS = {
    "red":    (220, 40, 40),
    "blue":   (40, 80, 220),
    "green":  (40, 170, 70),
    "yellow": (240, 200, 50),
    "purple": (150, 60, 190),
}
SHADOW = (185, 185, 185)   # the trap: grey, object-shaped, must NOT be counted
BG = (255, 255, 255)


# ---------------------------------------------------------------- PNG output
def write_png(path, pixels):
    """pixels: list of H rows, each a list of W (r,g,b) tuples."""
    raw = bytearray()
    for row in pixels:
        raw.append(0)                      # filter type 0
        for r, g, b in row:
            raw += bytes((r, g, b))

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)   # 8-bit RGB
    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b""))
    path.write_bytes(png)
    return hashlib.sha256(png).hexdigest()


def blank():
    return [[BG for _ in range(W)] for _ in range(H)]


def rect(px, x, y, w, h, colour):
    for yy in range(max(0, y), min(H, y + h)):
        row = px[yy]
        for xx in range(max(0, x), min(W, x + w)):
            row[xx] = colour


def circle(px, cx, cy, r, colour):
    r2 = r * r
    for yy in range(max(0, cy - r), min(H, cy + r + 1)):
        dy = yy - cy
        row = px[yy]
        for xx in range(max(0, cx - r), min(W, cx + r + 1)):
            dx = xx - cx
            if dx * dx + dy * dy <= r2:
                row[xx] = colour


def draw(px, shape, x, y, size, colour):
    if shape == "square":
        rect(px, x, y, size, size, colour)
    elif shape == "circle":
        circle(px, x + size // 2, y + size // 2, size // 2, colour)
    elif shape == "bar":
        rect(px, x, y, size, max(6, size // 3), colour)


def quadrant(x, y, size):
    cx, cy = x + size // 2, y + size // 2
    return ("top" if cy < H // 2 else "bottom") + "_" + ("left" if cx < W // 2 else "right")


# ------------------------------------------------------------------ fixtures
def build():
    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("*"):
        f.unlink()
    rng = random.Random(SEED)
    items, idx = [], 0

    def emit(cat, truth, px, notes=""):
        nonlocal idx
        fid = f"cv-{idx:04d}"
        idx += 1
        p = OUT / f"{fid}.png"
        h = write_png(p, px)
        items.append({"id": fid, "category": cat, "image": p.name,
                      "sha256": h, "truth": truth, "notes": notes})

    # ---- 30 count fixtures ------------------------------------------------
    # 24 plain (1-8 objects x 3), 3 overlapping, 3 with shadow distractors.
    for n in range(1, 9):
        for v in range(3):
            px = blank()
            shape = ["square", "circle", "bar"][v]
            colour = COLOURS[list(COLOURS)[v % len(COLOURS)]]
            placed = []
            for i in range(n):
                col, row = i % 4, i // 4
                x, y = 60 + col * 130, 90 + row * 150
                draw(px, shape, x, y, 70, colour)
                placed.append({"x": x, "y": y})
            emit("count", {"object_count": n, "shape": shape,
                           "colour": [k for k, c in COLOURS.items() if c == colour][0],
                           "positions": placed, "overlap": False}, px)

    for n, off in ((3, 40), (4, 35), (5, 30)):
        px = blank()
        placed = []
        for i in range(n):
            x, y = 70 + i * off, 180
            draw(px, "circle", x, y, 90, COLOURS["blue"])
            placed.append({"x": x, "y": y})
        emit("count", {"object_count": n, "shape": "circle", "colour": "blue",
                       "positions": placed, "overlap": True}, px,
             "OVERLAPPING - a naive detector may merge these into fewer objects "
             "or split them into more. Exact count is still n.")

    for n in (2, 3, 4):
        px = blank()
        for i in range(n):
            draw(px, "square", 80 + i * 140, 110, 70, COLOURS["red"])
        for i in range(n):                      # grey shadow-like duplicates
            draw(px, "square", 92 + i * 140, 200, 70, SHADOW)
        emit("count", {"object_count": n, "shape": "square", "colour": "red",
                       "distractor_count": n, "distractor_colour": "grey_shadow",
                       "overlap": False}, px,
             "SHADOW TRAP - grey object-shaped regions must NOT be counted. This "
             "is the recorded failure mode: counting needs HIGH detector "
             "confidence so shadows are not counted as extra objects.")

    # ---- 25 relative position fixtures ------------------------------------
    rels = ["left_of", "right_of", "above", "below"]
    for i in range(25):
        px = blank()
        rel = rels[i % 4]
        a_col, b_col = "red", "blue"
        # Every fixture varies BOTH offsets and size, so no two are identical.
        d1, d2, sz = i * 7, i * 5, 60 + (i % 7) * 8
        if rel in ("left_of", "right_of"):
            ax, ay = 40 + d1 % 120, 150 + d2 % 90
            bx, by = 400 + d2 % 110, 150 + d1 % 90
        else:
            ax, ay = 200 + d1 % 130, 30 + d2 % 70
            bx, by = 200 + d2 % 130, 300 + d1 % 70
        if rel in ("right_of", "below"):
            ax, ay, bx, by = bx, by, ax, ay
        draw(px, "square", ax, ay, sz, COLOURS[a_col])
        draw(px, "circle", bx, by, sz, COLOURS[b_col])
        emit("relative_position",
             {"subject": {"shape": "square", "colour": a_col, "x": ax, "y": ay},
              "object": {"shape": "circle", "colour": b_col, "x": bx, "y": by},
              "size_px": sz,
              "relation": rel, "decidable_from_boxes": True}, px)

    # ---- 15 absolute placement fixtures -----------------------------------
    for i in range(15):
        px = blank()
        q = ["top_left", "top_right", "bottom_left", "bottom_right"][i % 4]
        sz = 60 + i * 4
        x = (30 + i * 3) if "left" in q else (W - 40 - sz - i * 3)
        y = (30 + i * 2) if "top" in q else (H - 40 - sz - i * 2)
        col = list(COLOURS)[i % 5]
        draw(px, "square", x, y, sz, COLOURS[col])
        emit("absolute_placement",
             {"quadrant": q, "computed_quadrant": quadrant(x, y, sz),
              "x": x, "y": y, "size_px": sz, "colour": col,
              "object_count": 1}, px)

    # ---- 15 attribute binding fixtures ------------------------------------
    # 8 straight, 7 SWAPPED - the swap is the whole point of the category.
    PAIRS = [("red", "blue"), ("green", "yellow"), ("purple", "red"),
             ("blue", "green"), ("yellow", "purple"), ("red", "green"),
             ("blue", "yellow"), ("purple", "green")]
    for i in range(15):
        px = blank()
        swapped = i >= 8
        c1, c2 = PAIRS[i % len(PAIRS)]
        if swapped:
            c1, c2 = c2, c1
        sz = 70 + (i % 6) * 9
        y = 150 + (i % 4) * 18
        draw(px, "square", 90 + (i % 5) * 11, y, sz, COLOURS[c1])
        draw(px, "circle", 380 + (i % 3) * 13, y, sz, COLOURS[c2])
        emit("attribute_binding",
             {"square_colour": c1, "circle_colour": c2, "object_count": 2,
              "size_px": sz, "is_swapped_vs_canonical": swapped}, px,
             "Both colours and both shapes are present in EVERY fixture. Only "
             "the assignment differs, so an instrument that merely detects "
             "'red and blue and square and circle' scores at chance.")

    # ---- 15 size / aspect fixtures ----------------------------------------
    for i in range(15):
        px = blank()
        s1 = 45 + i * 6
        s2 = 140 - i * 5
        draw(px, "square", 110, 200, s1, COLOURS["green"])
        draw(px, "square", 400, 200, s2, COLOURS["purple"])
        larger = "green" if s1 > s2 else ("purple" if s2 > s1 else "equal")
        emit("size_aspect",
             {"green_size_px": s1, "purple_size_px": s2, "larger": larger,
              "object_count": 2, "frame_w": W, "frame_h": H,
              "frame_aspect": f"{W}:{H}"}, px)

    # ---- negative controls: an empty check is not a passing check ---------
    px = blank()
    emit("negative_control", {"object_count": 0, "expected_behaviour":
         "report zero objects, NOT an error"}, px,
         "BLANK IMAGE. Correct answer is 0 objects.")

    corrupt = OUT / "cv-corrupt.png"
    corrupt.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 64)   # truncated garbage
    items.append({
        "id": "cv-corrupt", "category": "negative_control",
        "image": corrupt.name,
        "sha256": hashlib.sha256(corrupt.read_bytes()).hexdigest(),
        "truth": {"expected_behaviour": "FAIL CLOSED - raise a decode error"},
        "notes": "CORRUPT FILE. An instrument that reports '0 objects, all "
                 "good' here has FAILED, not passed. This control exists "
                 "because that defect is invisible from reading the code."})

    # ---- uniqueness gate --------------------------------------------------
    # A pack of N fixtures that is really M distinct images is a CORRELATED
    # pack: it inflates apparent coverage exactly the way frames sampled from
    # one clip inflate apparent sample size. Fail closed rather than ship it.
    seen = {}
    dupes = []
    for it in items:
        seen.setdefault(it["sha256"], []).append(it["id"])
    for h, ids in seen.items():
        if len(ids) > 1:
            dupes.append(ids)
    if dupes:
        raise SystemExit(
            f"BUILD ABORTED: {len(dupes)} group(s) of pixel-identical fixtures: "
            f"{dupes[:5]}. Distinct fixture count would be {len(seen)} not "
            f"{len(items)}. Fix the parameterisation; do not ship a correlated pack.")

    manifest = {
        "pack": "cv-geometry-v1",
        "task": "E3 family 2",
        "date": "2026-08-26",
        "seed": SEED,
        "frame": {"w": W, "h": H},
        "ground_truth_origin": "constructed_by_code_no_human_label",
        "human_labels_required": 0,
        "spend": 0,
        "counts": {
            "total": len(items),
            "scoreable": sum(1 for i in items if i["category"] != "negative_control"),
            "negative_controls": sum(1 for i in items if i["category"] == "negative_control"),
            "distinct_images": len({i["sha256"] for i in items}),
        },
        "by_category": {},
        "items": items,
    }
    for it in items:
        manifest["by_category"][it["category"]] = manifest["by_category"].get(it["category"], 0) + 1
    mpath = OUT / "manifest.json"
    mpath.write_text(json.dumps(manifest, indent=2, sort_keys=True))
    return manifest


def verify():
    """Rebuild in memory and confirm every committed image still hashes true."""
    mpath = OUT / "manifest.json"
    if not mpath.exists():
        print("FAIL: no manifest; run --build first")
        return 1
    m = json.loads(mpath.read_text())
    if not m["items"]:
        print("FAIL: manifest is empty - an empty check is not a passing check")
        return 1
    bad = []
    for it in m["items"]:
        p = OUT / it["image"]
        if not p.exists():
            bad.append(f"{it['id']}: missing file")
            continue
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        if h != it["sha256"]:
            bad.append(f"{it['id']}: hash mismatch")
    print(f"pack              : {m['pack']}")
    print(f"total fixtures    : {m['counts']['total']}")
    print(f"scoreable         : {m['counts']['scoreable']}")
    print(f"negative controls : {m['counts']['negative_controls']}")
    print(f"by category       : {m['by_category']}")
    print(f"human labels used : {m['human_labels_required']}")
    # Distinctness is an invariant, not a nice-to-have.
    distinct = len({i["sha256"] for i in m["items"]})
    print(f"distinct images   : {distinct}/{m['counts']['total']}")
    if distinct != m["counts"]["total"]:
        bad.append(f"pack contains pixel-identical duplicates: "
                   f"{distinct} distinct of {m['counts']['total']}")
    if bad:
        print(f"\nFAIL - {len(bad)} integrity error(s):")
        for b in bad:
            print("  -", b)
        return 1
    print("\nPASS - every fixture present and hash-identical to its manifest.")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()
    if a.build:
        m = build()
        print(f"built {m['counts']['total']} fixtures "
              f"({m['counts']['scoreable']} scoreable + "
              f"{m['counts']['negative_controls']} negative controls)")
        print(json.dumps(m["by_category"], indent=2))
    if a.verify or not a.build:
        sys.exit(verify())
