#!/usr/bin/env python3
"""
EVAL-003 correction pass · Materialise one crop file per candidate item.

WHY THIS EXISTS
    The reviewer and the checker must judge the SAME region. Previously the reviewer saw a
    CSS-positioned crop rendered in a browser while the checker would have received something
    produced separately — two computations that could silently disagree. A mis-crop is invisible
    in every artifact: the reader transcribes the wrong words, the checker reads the wrong words,
    and the scores look perfectly reasonable.

    Materialising one file per item and pointing BOTH at it replaces "two computations agree"
    with "it is the same file". Equivalence by identity.

HOW GEOMETRY IS VERIFIED
    `sips` crop-offset semantics are not documented in a form we can rely on, so --self-test
    establishes them empirically: it writes a synthetic PNG in which every pixel encodes its own
    (x, y), crops a known rectangle, decodes the result with a dependency-free reader, and checks
    the returned pixels carry the coordinates the requested rectangle should contain.

    Established by that test:  sips -c H W --cropOffset Y X
                               -> a W x H image whose top-left pixel is source (X, Y).

    If the self-test fails, this script refuses to materialise anything.

No network. No model. Source images are opened read-only and never modified.
"""
import argparse, hashlib, json, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _png import write_rgb, read_rgb   # noqa: E402

def _sips(args):
    r = subprocess.run(["sips"] + [str(a) for a in args], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"sips failed: {r.stderr.strip()[:200]}")
    return r

def _image_size(p: Path):
    r = _sips(["-g", "pixelWidth", "-g", "pixelHeight", p])
    w = h = None
    for line in r.stdout.splitlines():
        line = line.strip()
        if line.startswith("pixelWidth:"):  w = int(line.split(":")[1])
        if line.startswith("pixelHeight:"): h = int(line.split(":")[1])
    if w is None or h is None:
        raise RuntimeError(f"could not read dimensions of {p}")
    return w, h

def sips_crop(src: Path, dst: Path, box):
    """
    Crop source rectangle [x0,y0,x1,y1] to dst as PNG (lossless; avoids double-JPEG).

    KNOWN sips DEFECT, found by --self-test and worked around here:
        `--cropOffset 0 0` is treated as "no offset supplied" and silently produces a CENTRE
        crop instead of an origin crop. Every other offset, including a single zero component
        such as (0, 30) or (30, 0), is honoured correctly.

    Workaround for the exact (0,0) case: mirror the image on both axes, crop the mirrored
    rectangle (whose origin is then non-zero), and mirror the result back. --self-test exercises
    this path against the coordinate image, so the workaround is verified, not assumed.
    """
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    if w <= 0 or h <= 0:
        raise ValueError(f"degenerate crop box {box}")

    if (x0, y0) != (0, 0):
        _sips(["-s", "format", "png", "-c", h, w, "--cropOffset", y0, x0, src, "--out", dst])
        return w, h

    # (0,0) path: mirror -> crop -> mirror back
    W, H = _image_size(src)
    if w >= W and h >= H:
        _sips(["-s", "format", "png", src, "--out", dst])   # whole image; no crop needed
        return w, h
    with tempfile.TemporaryDirectory() as T:
        flipped = Path(T) / "flip.png"
        cropped = Path(T) / "crop.png"
        _sips(["-s", "format", "png", "-f", "horizontal", src, "--out", flipped])
        _sips(["-f", "vertical", flipped])
        mx, my = W - w, H - h        # mirrored origin; non-zero because w<W or h<H
        if (mx, my) == (0, 0):
            raise RuntimeError("cannot work around sips (0,0) defect for this box")
        _sips(["-c", h, w, "--cropOffset", my, mx, flipped, "--out", cropped])
        _sips(["-f", "horizontal", cropped])
        _sips(["-f", "vertical", cropped])
        _sips(["-s", "format", "png", cropped, "--out", dst])
    return w, h

def self_test(verbose=True):
    """Prove sips crop geometry against a synthetic coordinate-encoded image."""
    ok = True
    with tempfile.TemporaryDirectory() as T:
        T = Path(T)
        W = H = 220
        src = T / "coord.png"
        write_rgb(src, W, H, [[(x, y, 7) for x in range(W)] for y in range(H)])

        # codec round-trip must hold before it can prove anything about sips
        w, h, rows = read_rgb(src)
        if (w, h) != (W, H) or rows[77][133] != (133, 77, 7):
            print("  FAIL  PNG codec round-trip"); return False
        if verbose: print("  PASS  PNG codec round-trip")

        # Includes the (0,0) origin case and single-zero offsets, because that is exactly where
        # sips misbehaves. A self-test that avoided the awkward cases would prove nothing.
        for (x0, y0, x1, y1) in [(50, 30, 110, 70), (0, 0, 16, 16), (0, 30, 40, 70),
                                 (30, 0, 70, 40), (204, 188, 220, 220), (7, 199, 91, 220),
                                 (0, 0, 219, 219)]:
            dst = T / f"c_{x0}_{y0}.png"
            cw, ch = sips_crop(src, dst, (x0, y0, x1, y1))
            gw, gh, g = read_rgb(dst)
            exp_w, exp_h = x1 - x0, y1 - y0
            size_ok = (gw, gh) == (exp_w, exp_h)
            tl_ok = g[0][0][:2] == (x0, y0)
            br_ok = g[gh-1][gw-1][:2] == (x1-1, y1-1)
            # every pixel must carry the coordinate its position implies
            all_ok = all(g[r][c][:2] == (x0 + c, y0 + r) for r in range(gh) for c in range(gw))
            good = size_ok and tl_ok and br_ok and all_ok
            ok &= good
            if verbose:
                print(f"  {'PASS' if good else 'FAIL'}  rect [{x0},{y0},{x1},{y1}] -> "
                      f"{gw}x{ch} top-left={g[0][0][:2]} bottom-right={g[gh-1][gw-1][:2]} "
                      f"all-pixels-correct={all_ok}")
    return ok

def main():
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--manifest", default=str(here / "candidate-manifest.jsonl"))
    ap.add_argument("--corpus-root", default=None, help="directory containing src_* corpus folders")
    ap.add_argument("--out-dir", default=str(here / "crops"))
    ap.add_argument("--self-test", action="store_true", help="verify sips crop geometry and exit")
    a = ap.parse_args()

    print("Verifying crop geometry against a synthetic coordinate image:")
    if not self_test():
        sys.exit("\nSTOP: sips crop geometry could not be verified. Refusing to materialise crops — "
                 "an unverified crop would have reader and checker judging the wrong region.")
    print("  crop geometry VERIFIED: sips -c H W --cropOffset Y X -> W x H at source (X, Y)\n")
    if a.self_test:
        return

    if not a.corpus_root:
        sys.exit("ERROR: --corpus-root is required (the raw corpus is git-ignored and may live "
                 "in another worktree)")
    corpus, out = Path(a.corpus_root), Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    rows = [json.loads(l) for l in Path(a.manifest).read_text(encoding="utf-8").splitlines() if l.strip()]
    index = []
    for r in rows:
        src = corpus / r["source_image_relpath"]
        dst = out / f'{r["candidate_id"]}.png'
        w, h = sips_crop(src, dst, r["crop_box_xyxy"])
        gw, gh, _ = read_rgb(dst)
        if (gw, gh) != (w, h):
            sys.exit(f"STOP: crop for {r['candidate_id']} is {gw}x{gh}, expected {w}x{h}")
        index.append({
            "item_id": r["candidate_id"],
            "crop_file": dst.name,
            "crop_sha256": hashlib.sha256(dst.read_bytes()).hexdigest(),
            "crop_w": gw, "crop_h": gh,
            "source_image_relpath": r["source_image_relpath"],
            "source_image_sha256": r["source_image_sha256"],
            "crop_box_xyxy": r["crop_box_xyxy"],
        })
    (out / "crop-index.json").write_text(json.dumps({
        "note": "One crop per candidate. The review interface and the checker BOTH read these "
                "files, so the region judged is identical by construction rather than by two "
                "computations agreeing. Derived output: git-ignored, regenerate with this script.",
        "geometry_rule": "sips -c H W --cropOffset y0 x0  ->  (x1-x0) x (y1-y0) at source (x0, y0), "
                         "verified by --self-test against a coordinate-encoded synthetic image",
        "count": len(index), "crops": index,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"materialised {len(index)} crops -> {out}")
    print(f"index -> {out / 'crop-index.json'}")

if __name__ == "__main__":
    main()
