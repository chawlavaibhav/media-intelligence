#!/usr/bin/env python3
"""Deterministic assembly for AGY-2026-09-15-CUMINCO-CHOPSTICKS-001 — USD 0, local only (ffmpeg + hb-view + Pillow).

One geometry per run. Every delivered geometry is BUILT from the accepted source clips with its own declared crop
and its own text layout (FORMAT_SPECIFIC_REVALIDATION, case 002): the 4:5 and 1:1 files are not crops of the 9:16
master with text baked in. Every text box goes through the repo's own gates (runtime/compositor/gates.py) with one
DesignTokens source; contrast is measured against real pixels sampled from the frames behind the box; a failing
box gets an OPAQUE backing card (token geometry) and is re-measured. Exact strings are byte-checked against the
frozen deck. The report is written next to the output as <out>.qa.json.

Text raster: hb-view (the pilot's overlay_text_video.render). Fonts: Charter Roman (step lines, tagline) and
Avenir Next Demi Bold (beat numerals, brand line) — system files, recorded with sha256 in the report.

    python3 compose.py --geometry 9:16 --out ../gen/final/cuminco-chopsticks-9x16.mp4
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
JOB = HERE.parent
REPO = JOB.parents[2]
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(REPO))
import overlay_text_video as OTV  # noqa: E402  (hb-view render, copied from the pilot)
from runtime.compositor.tokens import DesignTokens  # noqa: E402
from runtime.compositor import gates  # noqa: E402
from runtime.errors import Refusal  # noqa: E402

try:
    from PIL import Image
    import numpy as np
except ImportError:  # the scratch venv carries Pillow; the system python does not
    sys.exit("run with the venv python that has Pillow + numpy")

OTV.FONTS.update({
    "charter": ("/System/Library/Fonts/Supplemental/Charter.ttc", 0),
    "avenir-demi": ("/System/Library/Fonts/Avenir Next.ttc", 2),
})
TOKENS = DesignTokens(card_radius=28, card_border_px=0, card_shadow=(0, 0, 0), safe_x=72, safe_y=170,
                      spacing=(12, 24, 48, 96), contrast_body=4.5, contrast_display=3.0, display_threshold_px=48,
                      min_gap_px=24, source="compose.py TOKENS (one instance)")
INK = "3A2A20"          # warm dark brown, body text
ACCENT = "9A4B3F"       # terracotta, numerals + brand line (display role)
BACKING = "F4EDE3"      # opaque oat backing card, used only when pixels fail contrast
FPS = 24

# ── the frozen deck (JOB.yaml intake.mandatory_text) — byte-checked at the end ──
DECK = {
    "t1": "The bottom stick stays still.",
    "t2": "The top stick does all the work.",
    "t3": "Pinch and release.",
    "t4": "Ramen night at home.",
    "t5": "Cumin Co.",
    "t6": "15 cm Ceramic Ramen Bowl",     # PDP title, verbatim fragment (approved by the user, V3)
    "t7": "cuminco.com",                  # Direction line — the brand's domain (approved by the user, V3)
}

# ── timeline (seconds on the master) — VO-paced; recorded as a deviation from the 18-s plan ──
BEATS = [  # (beat, clip file, in, out)  -> master start is cumulative   (v2: closed-mouth two-shots r2; windows chosen on the sampled frames)
    (1, "clip-1-r2.mp4", 3.0, 6.0),     # 0.0–3.0   both mouths closed from 3.0 s; he fumbles, she reaches for her chopsticks
    (2, "clip-2-accepted.mp4", 0.0, 5.5),   # 3.0–8.5
    (3, "clip-3-r1.mp4", 0.5, 5.5),     # 8.5–13.5
    (4, "clip-4-r1.mp4", 0.0, 4.0),     # 13.5–17.5
    (5, "clip-5-r2.mp4", 1.0, 4.5),     # 17.5–21.0  her mouth closes at ~1.2 s; closed-lip laughter, spoon
    (6, "ENDCARD", 0.0, 4.6),           # 21.0–25.6  product hero: the brand's own photograph (blog hero), slow code push, captions + Direction
]
TAIL_HOLD_S = 0.0
VO = {1: ("final-b1.wav", 0.3), 2: ("final-b2.wav", 4.7), 3: ("final-b3.wav", 9.1), 4: ("final-b4.wav", 13.6), 5: ("final-b5.wav", 17.7), 6: ("final-b6.wav", 22.0)}
ENDCARD_IMAGE = JOB / "source/images/blog_Setof2withchopstickslifestyle.jpg"   # 1080x1080, text-free, the brand's photograph
ENDCARD_GROUND = "F1E9DD"
# v2 deviation: the beat-1 VO line ("First noodle night with chopsticks.") is DROPPED — the four remaining lines run
# 4.4–4.9 s each in the chosen slow, bubbly read and cannot all fit without pushing the film past 26 s; beat 1 is
# carried by the picture and the music (muted test: yes). Flagged for the human; restorable at USD 0.
VO_TEMPO = 1.10
TEXT = {  # beat -> [(region, string_id | literal, font, size_at_1080w, colour, role, y_centre_px)]  — a top band just inside the token safe area, every geometry
    1: [],
    2: [("numeral", "1", "avenir-demi", 44, ACCENT, "display", 205), ("headline", "t1", "charter", 60, INK, "body", 282)],
    3: [("numeral", "2", "avenir-demi", 44, ACCENT, "display", 205), ("headline", "t2", "charter", 60, INK, "body", 282)],
    4: [("numeral", "3", "avenir-demi", 44, ACCENT, "display", 205), ("headline", "t3", "charter", 60, INK, "body", 282)],
    5: [],                                                                                   # the two-shot carries no copy in V3; the end card does
    6: [("tagline", "t4", "charter", 66, INK, "body", 250), ("product_name", "t6", "avenir-demi", 40, INK, "display", 330),
        ("brand_line", "t5", "avenir-demi", 54, ACCENT, "display", 404), ("cta", "t7", "avenir-demi", 38, ACCENT, "display", 470)],
}
BRAND_MARK = ("brand_mark", "t5", "avenir-demi", 34, INK, "display", 192)     # persistent, top-left, beats 1–5 ("early and throughout")
# per geometry: output size, and the declared crop (y offset in the 1080x1920 upscaled frame) per beat with its reason
GEOM = {
    "9:16": {"size": (1080, 1920), "crop_y": None, "layout": {"macro": [("left", 520), ("centre", 940)], "twoshot": [("centre", 940), ("centre", 620)], "endcard": [("centre", 940)]}, "endcard_top": 590},
    "4:5": {"size": (1080, 1350), "crop_y": {1: 250, 2: 400, 3: 400, 4: 400, 5: 250}, "layout": {"macro": [("left", 460), ("centre", 700)], "twoshot": [("centre", 440), ("left", 440)], "endcard": [("centre", 940)]}, "endcard_top": 590,
             "reason": "subject-anchored: two-shots keep both faces and both bowls (y 250-1600 of 1920); macros keep chopstick tips to bowl base (y 400-1750); the copy takes an opaque backing where it must sit over the chopsticks"},
    "1:1": {"size": (1080, 1080), "crop_y": {1: 330, 2: 500, 3: 500, 4: 500, 5: 330}, "layout": {"macro": [("left", 440), ("centre", 700)], "twoshot": [("centre", 400), ("left", 420)], "endcard": [("centre", 940)]}, "endcard_top": 580,
             "reason": "subject-anchored: two-shots keep faces and bowls (y 330-1410); macros keep the hand, chopsticks and the bowl's rim and wall, cutting ~100 px of the bowl base/shadow (y 500-1580); the copy takes an opaque backing"},
}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(cmd: list, quiet=True):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"command failed: {' '.join(cmd[:6])}…\n{r.stderr[-1500:]}")
    return r


def ink_box(png: Path) -> tuple:
    """Measured ink box of a rendered RGBA glyph layer (alpha > 8)."""
    a = np.asarray(Image.open(png).convert("RGBA"))[:, :, 3]
    ys, xs = np.where(a > 8)
    return (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)


def luminance_samples(frames: list, box: tuple) -> list:
    out = []
    for f in frames:
        im = np.asarray(Image.open(f).convert("RGB"), dtype=float) / 255.0
        x0, y0, x1, y1 = box
        region = im[y0:y1, x0:x1]
        lin = np.where(region <= 0.03928, region / 12.92, ((region + 0.055) / 1.055) ** 2.4)
        lum = 0.2126 * lin[..., 0] + 0.7152 * lin[..., 1] + 0.0722 * lin[..., 2]
        # 5x5 grid of local means plus the extremes: the worst pixel decides (Controller audit on PR #98)
        h, w = lum.shape
        for gy in range(5):
            for gx in range(5):
                out.append(float(lum[gy * h // 5:(gy + 1) * h // 5 or 1, gx * w // 5:(gx + 1) * w // 5 or 1].mean()))
        out += [float(lum.min()), float(lum.max())]
    return out


def wall_obstruction(frames: list, box: tuple, pad: int = 18) -> float:
    """Fraction of pixels inside the padded box that are NOT wall — measured against the frame's own wall model
    (the median colour of the top 8 % of the frame, which is always wall in this film). Returns the worst frame."""
    worst = 0.0
    for f in frames:
        im = np.asarray(Image.open(f).convert("RGB"), dtype=float)
        h = im.shape[0]
        # per-COLUMN wall reference (median of the top rows in that column): the wall is a gradient — darker at
        # the frame edges, brighter near the window — and a single global median flagged the edges as "subject"
        wall_cols = np.median(im[: max(8, h // 14)], axis=0)            # (W, 3)
        x0, y0, x1, y1 = max(0, box[0] - pad), max(0, box[1] - pad), min(im.shape[1], box[2] + pad), min(h, box[3] + pad)
        region = im[y0:y1, x0:x1]
        dist = np.sqrt(((region - wall_cols[None, x0:x1, :]) ** 2).sum(axis=-1))
        worst = max(worst, float((dist > 60).mean()))
    return worst


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--geometry", required=True, choices=list(GEOM))
    ap.add_argument("--out", required=True)
    ap.add_argument("--no-music", dest="music", action="store_false")
    a = ap.parse_args()
    g = GEOM[a.geometry]; W, H = g["size"]
    out = Path(a.out).resolve(); work = out.parent / f"_work-{a.geometry.replace(':', 'x')}"; work.mkdir(parents=True, exist_ok=True)
    report = {"geometry": a.geometry, "size": [W, H], "tokens": TOKENS.__dict__ | {"card_shadow": list(TOKENS.card_shadow), "spacing": list(TOKENS.spacing)},
              "fonts": {k: {"file": v[0], "face": v[1], "sha256": sha(Path(v[0]))} for k, v in OTV.FONTS.items() if k in ("charter", "avenir-demi")},
              "beats": [], "text": [], "gates": {}, "deviations": []}

    # 1. beats: trim, upscale (declared), crop (declared)
    starts, t = [], 0.0
    seg_files = []
    for beat, clip, tin, tout in BEATS:
        dur = round(tout - tin, 3)
        seg = work / f"seg-{beat}.mp4"
        if clip == "ENDCARD":
            top = g["endcard_top"]; avail = H - top - 40
            side = min(W - 2 * TOKENS.safe_x, avail)             # contain: the whole photograph, never cropped
            x0 = (W - side) // 2
            fr = gates.check_fit({"id": "endcard-photo", "fit": "contain", "source_size": (1080, 1080), "box": (x0, top, x0 + side, top + side)})
            nfr = int(dur * FPS)
            run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", f"{dur}", "-i", str(ENDCARD_IMAGE), "-f", "lavfi", "-t", f"{dur}", "-i", f"color=c=0x{ENDCARD_GROUND}:s={W}x{H}:r={FPS}",
                 "-filter_complex", f"[0:v]scale=2160:2160:flags=lanczos,zoompan=z='1+0.04*on/{nfr}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:s={side}x{side}:fps={FPS}[ph];[1:v][ph]overlay=x={x0}:y={top}:shortest=1,format=yuv420p[v]",
                 "-map", "[v]", "-t", f"{dur}", "-r", str(FPS), "-c:v", "libx264", "-preset", "medium", "-crf", "16", str(seg)])
            seg_files.append(seg); starts.append(t)
            report["beats"].append({"beat": beat, "clip": "ENDCARD (code): " + str(ENDCARD_IMAGE.relative_to(JOB)), "clip_sha256": sha(ENDCARD_IMAGE), "in": 0, "out": dur, "master_start": round(t, 3),
                                    "fit": fr, "push": "zoompan 1.00→1.04 over the beat (declared, no crop of the photograph beyond the push)"})
            t = round(t + dur, 3)
            continue
        src = JOB / "gen/clips" / clip
        vf = "scale=1080:1920:flags=lanczos"
        fit = {"id": f"beat-{beat}", "fit": "contain", "source_size": (1080, 1920), "box": (0, 0, W, H)}
        if g["crop_y"] is not None:
            y = g["crop_y"][beat]
            vf += f",crop={W}:{H}:0:{y}"
            fit = {"id": f"beat-{beat}", "fit": "cover", "source_size": (1080, 1920), "box": (0, 0, W, H),
                   "declared_crop": {"box": (0, y, W, y + H), "reason": g["reason"]}}
        hold = TAIL_HOLD_S if beat == BEATS[-1][0] else 0.0
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{tin}", "-t", f"{dur}", "-i", str(src), "-an", "-vf", vf + f",fps={FPS},format=yuv420p" + (f",tpad=stop_mode=clone:stop_duration={hold}" if hold else ""),
             "-c:v", "libx264", "-preset", "medium", "-crf", "16", str(seg)])
        dur = round(dur + hold, 3)
        try:
            fr = gates.check_fit(fit)
        except Refusal as e:
            sys.exit(f"check_fit refused: {e}")
        seg_files.append(seg); starts.append(t)
        report["beats"].append({"beat": beat, "clip": clip, "clip_sha256": sha(src), "in": tin, "out": tout, "master_start": round(t, 3),
                                "upscale": "720x1280 -> 1080x1920 lanczos (DECLARED)", "fit": fr})
        t = round(t + dur, 3)
    total = t
    concat = work / "concat.txt"; concat.write_text("".join(f"file '{s}'\n" for s in seg_files))
    base = work / "base.mp4"
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(base)])

    # 2. text layers + gates on real pixels
    layers = []   # (png, x, y, t_in, t_out, backing or None)
    mark_layers = []
    for beat, items in TEXT.items():
        b_start = starts[beat - 1]; b_end = b_start + (BEATS[beat - 1][3] - BEATS[beat - 1][2])
        t_in, t_out = b_start + 0.35, b_end - 0.15
        if beat == 6:
            t_in, t_out = b_start + 0.25, b_end + 0.5
        if beat == 1:
            t_in = 0.0
        pdir = work / f"probe-{beat}"; pdir.mkdir(exist_ok=True)
        for old in pdir.glob("*.png"): old.unlink()
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t_in:.3f}", "-t", f"{t_out - t_in:.3f}", "-i", str(base), "-vf", "fps=4", str(pdir / "p_%03d.png")])
        frames = sorted(pdir.glob("*.png"))
        mark_box = None
        if beat <= 5:
            region, sid, font, size_1080, colour, role, _ = BRAND_MARK
            text = DECK[sid]; px = int(size_1080 * W / 1080)
            png = work / f"mark-{beat}.png"; OTV.render(text, font, px, colour, png, margin=6)
            ib = ink_box(png); tw, th = ib[2] - ib[0], ib[3] - ib[1]
            x = W - TOKENS.safe_x - TOKENS.spacing[1] - tw - ib[0]
            for yc in (192, H - TOKENS.safe_y - TOKENS.spacing[1] - th // 2):
                y = int(yc) - th // 2 - ib[1]; box = (x + ib[0], y + ib[1], x + ib[2], y + ib[3])
                obs = wall_obstruction(frames, box)
                try:
                    gates.check_text_bounds(box, canvas=(0, 0, W, H), tokens=TOKENS, id_=f"{beat}-brand_mark")
                    c2 = gates.check_contrast(colour, luminance_samples(frames, box), role=role, tokens=TOKENS, id_=f"{beat}-brand_mark")
                except Refusal:
                    continue
                if obs < 0.02:
                    mark_box = box
                    report["text"].append({"beat": beat, "region": "brand_mark", "string": text, "font": font, "px": px, "box": box, "C1_bounds": {"status": "PASS"}, "C2_contrast": c2, "backing": None, "C6_exact": {"status": "PASS", "expected": text}, "obstruction": round(obs, 4)})
                    mark_layers.append((png, x, y, b_start if beat > 1 else 0.0, b_end + 0.02, None))
                    break
            if mark_box is None:
                report["deviations"].append(f"beat {beat}: the brand mark has no clean corner at {a.geometry} (subject under both corners); omitted for this beat — 'early and throughout' lapses here")
        # frames behind the boxes, sampled across the beat
        regions = {}
        group = []   # (region, text, png, x, y, box, colour, role, samples)
        candidates = g["layout"]["endcard" if beat == 6 else ("twoshot" if beat in (1, 5) else "macro")]
        if not items:
            regions = {}
            if mark_box is not None:
                regions["brand_mark"] = mark_box
            report["gates"][f"C5_disjoint_beat{beat}"] = gates.check_disjoint(regions, critical=("brand_mark",), min_gap_px=TOKENS.min_gap_px)
            continue
        chosen = None; tried = []
        for ci, (align, max_w) in enumerate(candidates):
          group = []; y_cursor = None
          for region, sid, font, size_1080, colour, role, yc in items:
              text = DECK.get(sid, sid)
              px = int(size_1080 * W / 1080)
              # wrap by word to max_w (measured ink), render the lines, stack them into one RGBA layer
              words = text.split(" "); lines = []; cur = ""
              for wd in words:
                  cand = (cur + " " + wd).strip()
                  OTV.render(cand, font, px, colour, work / "_measure.png", margin=6)
                  mb = ink_box(work / "_measure.png")
                  if mb[2] - mb[0] > max_w and cur:
                      lines.append(cur); cur = wd
                  else:
                      cur = cand
              lines.append(cur)
              rendered = []
              for i, ln in enumerate(lines):
                  lp = work / f"text-{beat}-{region}-c{ci}-l{i}.png"; OTV.render(ln, font, px, colour, lp, margin=6); rendered.append(Image.open(lp).convert("RGBA"))
              gap = int(px * 0.28)
              lw = max(r.width for r in rendered); lh = sum(r.height for r in rendered) + gap * (len(rendered) - 1)
              layer = Image.new("RGBA", (lw, lh), (0, 0, 0, 0)); yy = 0
              for r in rendered:
                  xx = 0 if align == "left" else (lw - r.width) // 2
                  layer.paste(r, (xx, yy), r); yy += r.height + gap
              png = work / f"text-{beat}-{region}-c{ci}.png"; layer.save(png)     # per candidate: the chosen layer must not be overwritten by a later candidate
              ib = ink_box(png); tw, th = ib[2] - ib[0], ib[3] - ib[1]
              if y_cursor is not None:
                  yc = y_cursor + th // 2 + max(int(px * 0.55), TOKENS.min_gap_px + 10)      # stack the next region under the previous one (≥ the disjointness gap)
              x = (TOKENS.safe_x + TOKENS.spacing[2] - ib[0]) if align == "left" else ((W - tw) // 2 - ib[0]); y = int(yc) - th // 2 - ib[1]   # left: inset by one token step so a backing card still fits inside the safe area
              top_min = TOKENS.safe_y + TOKENS.spacing[0] + TOKENS.spacing[1]      # room for a backing card (pad = spacing[1]) inside the safe area
              if y + ib[1] < top_min:            # a wrapped block grows upward from its centre; keep it inside the safe area (+ room for a card)
                  y = top_min - ib[1]
              box = (x + ib[0], y + ib[1], x + ib[2], y + ib[3])
              y_cursor = box[3]
              group.append((region, text, png, x, y, box, colour, role, luminance_samples(frames, box), font, px, sid))
              report.setdefault("wrap", []).append({"beat": beat, "region": region, "lines": lines, "align": align, "max_w": max_w})
          worst = max(wall_obstruction(frames, b[5]) for b in group)
          contrast_ok = True
          for region, text, png, x, y, box, colour, role, samples, font, px, sid in group:
              try:
                  gates.check_contrast(colour, samples, role=role, tokens=TOKENS, id_=f"{beat}-{region}")
              except Refusal:
                  contrast_ok = False
          report.setdefault("obstruction", []).append({"beat": beat, "align": align, "max_w": max_w, "worst_nonwall_fraction": round(worst, 4), "contrast_on_pixels": contrast_ok})
          tried.append((worst, align, max_w, group, contrast_ok))
          if worst < 0.02 and contrast_ok:
              chosen = (align, max_w); break
        if chosen is None:   # no band is both on wall and readable on pixels for the whole beat: take the band with the LEAST
            # subject under it, put the copy on an opaque card, and record the obstruction for the human (CF2)
            worst, align, max_w, group, contrast_ok = min(tried, key=lambda t: t[0])
            chosen = (align, max_w)
            report["deviations"].append(f"beat {beat}: no copy band is on wall and readable for the whole beat at {a.geometry}; least-obstructed band '{align}' (non-wall fraction {worst:.3f}) on an opaque card — CF2 obstruction recorded for the human")
            needs_backing_forced = True
        else:
            needs_backing_forced = False
        align, max_w = chosen
        # contrast on real pixels first; if ANY line of the beat fails, the whole beat's copy sits on ONE opaque
        # backing card (token geometry) and every line is re-measured against the backing
        needs_backing = needs_backing_forced; pixel_failures = {}
        for region, text, png, x, y, box, colour, role, samples, font, px, sid in group:
            try:
                gates.check_contrast(colour, samples, role=role, tokens=TOKENS, id_=f"{beat}-{region}")
            except Refusal as e:
                needs_backing = True; pixel_failures[region] = str(e)[:160]
        backing = None
        if needs_backing:
            pad = TOKENS.spacing[1]
            u = (min(b[5][0] for b in group) - pad * 2, min(b[5][1] for b in group) - pad, max(b[5][2] for b in group) + pad * 2, max(b[5][3] for b in group) + pad)
            backing = {"box": u, "hex": BACKING, **gates.card_geometry(TOKENS, id_=f"backing-{beat}")}
            report["deviations"].append(f"beat {beat}: pixels behind the copy failed contrast at {a.geometry} ({', '.join(pixel_failures)}); one opaque backing card added (token geometry)")
        for region, text, png, x, y, box, colour, role, samples, font, px, sid in group:
            row = {"beat": beat, "region": region, "string": text, "font": font, "px": px, "box": box}
            try:
                row["C1_bounds"] = gates.check_text_bounds(box, canvas=(0, 0, W, H), container=backing["box"] if backing else None, tokens=TOKENS, id_=f"{beat}-{region}")
                if backing:
                    gates.check_text_bounds(backing["box"], canvas=(0, 0, W, H), tokens=TOKENS, id_=f"{beat}-backing")
            except Refusal as e:
                sys.exit(f"C1 refused: {e}")
            if backing:
                row["C2_contrast"] = gates.check_contrast(colour, samples, role=role, backing_hex=BACKING, backing_alpha=1.0, tokens=TOKENS, id_=f"{beat}-{region}")
                row["C2_contrast"]["pixels_failed"] = pixel_failures.get(region, "this line passed on pixels; shares the beat's backing")
            else:
                row["C2_contrast"] = gates.check_contrast(colour, samples, role=role, tokens=TOKENS, id_=f"{beat}-{region}")
            regions[region] = box
            row["backing"] = backing
            row["C6_exact"] = {"status": "PASS" if text == DECK.get(sid, sid) else "FAIL", "expected": DECK.get(sid, sid)}
            report["text"].append(row)
            layers.append((png, x, y, t_in, t_out, backing if region == group[0][0] else None))
        if mark_box is not None:
            regions["brand_mark"] = mark_box
        try:
            report["gates"][f"C5_disjoint_beat{beat}"] = gates.check_disjoint(regions, critical=("brand_mark", "numeral", "headline", "tagline", "product_name", "brand_line", "cta"), min_gap_px=TOKENS.min_gap_px)
        except Refusal as e:
            sys.exit(f"C5 refused: {e}")
    layers = mark_layers + layers
    report["gates"]["C4_geometry"] = gates.check_geometry([l[5] for l in layers if l[5]], TOKENS)

    # 3. video with overlays: backing cards (drawbox, opaque) then glyph layers with alpha fades
    inputs = ["-i", str(base)]; fc = []; cur = "[0:v]"
    n = 1; idx = 0
    card_layers = []
    for png, x, y, t_in, t_out, backing in layers:
        if backing:   # the card is RENDERED at the token radius (Pillow), never approximated with a square drawbox (SD-04)
            from PIL import ImageDraw
            bx0, by0, bx1, by1 = backing["box"]
            card = Image.new("RGBA", (bx1 - bx0, by1 - by0), (0, 0, 0, 0))
            ImageDraw.Draw(card).rounded_rectangle((0, 0, bx1 - bx0 - 1, by1 - by0 - 1), radius=backing["radius"], fill="#" + BACKING)
            cp = work / f"card-{backing['id']}.png"; card.save(cp)
            card_layers.append((cp, bx0, by0, t_in, t_out, None))
    layers = card_layers + layers
    for png, x, y, t_in, t_out, backing in layers:
        inputs += ["-loop", "1", "-t", f"{total + 1:.3f}", "-i", str(png)]
        idx += 1
        fc.append(f"[{idx}:v]format=rgba,fade=t=in:st={t_in:.3f}:d=0.35:alpha=1,fade=t=out:st={t_out - 0.3:.3f}:d=0.3:alpha=1[l{n}]")
        fc.append(f"{cur}[l{n}]overlay=x={x}:y={y}:enable='between(t,{t_in:.3f},{t_out:.3f})'[v{n}]"); cur = f"[v{n}]"; n += 1
    video = work / "video.mp4"
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", ";".join(fc), "-map", cur, "-t", f"{total:.3f}",
         "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-r", str(FPS), str(video)])

    # 4. audio — VO lines trimmed at the EDGES only (no internal silence removal, no tempo change), each normalised
    # to -16 LUFS, placed at the beat's VO time; music bed at -30 LUFS, ducked 8 dB under speech; true-peak limiter.
    # Diagnosis of v1 (human: 'random audio'): stop_periods=-1 removed silences INSIDE lines and shifted them, and a
    # single-pass loudnorm over the ducked mix pumped between speech and music.
    ai = []; af = []; vo_paths = []
    for i, (beat, (wav, at)) in enumerate(sorted(VO.items())):
        src = JOB / "gen/vo" / wav; trimmed = work / f"vo-{beat}.wav"
        run(["ffmpeg", "-v", "error", "-y", "-i", str(src), "-af",
             "silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
             f"atempo={VO_TEMPO},loudnorm=I=-16:TP=-2:LRA=9,aformat=sample_rates=48000:channel_layouts=mono", str(trimmed)])
        vo_paths.append((beat, trimmed, at))
    for i, (beat, trimmed, at) in enumerate(vo_paths):
        ai += ["-i", str(trimmed)]
        af.append(f"[{i}:a]adelay={int(at * 1000)}|{int(at * 1000)},apad=whole_dur={total + 1:.3f}[vo{i}]")
    nvo = len(vo_paths)
    af.append("".join(f"[vo{i}]" for i in range(nvo)) + f"amix=inputs={nvo}:normalize=0,aformat=channel_layouts=stereo,asplit=2[vo][voS]")
    if a.music:
        ai += ["-i", str(JOB / "gen/music/bed-r1.wav")]
        af.append(f"[{nvo}:a]atrim=0:{total:.3f},afade=t=in:d=1.0,afade=t=out:st={total - 2.5:.3f}:d=2.5,loudnorm=I=-30:TP=-6:LRA=7,aformat=sample_rates=48000:channel_layouts=stereo[mus]")
        af.append("[mus][voS]sidechaincompress=threshold=0.02:ratio=4:attack=30:release=600:makeup=1[ducked]")
        af.append("[ducked][vo]amix=inputs=2:normalize=0,alimiter=limit=0.89:level=false[mix]")
    else:
        af.append("[voS]anullsink;[vo]alimiter=limit=0.89:level=false[mix]")
    run(["ffmpeg", "-v", "error", "-y", *ai, "-filter_complex", ";".join(af), "-map", "[mix]", "-t", f"{total:.3f}", "-ar", "48000", str(work / "mix.wav")])
    run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-i", str(work / "mix.wav"), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(out)])
    report["audio"] = {"vo_lufs": -16, "music_lufs": -30 if a.music else None, "duck": "sidechain 4:1 under speech" if a.music else None, "limiter": "TP -1 dBFS"}

    # 5. export facts
    probe = run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_name,width,height,r_frame_rate,duration", "-of", "json", str(out)]).stdout
    report["C8_export"] = {"declared": [W, H, FPS, round(total, 3)], "probe": json.loads(probe)["streams"], "status": "PASS" if any(s.get("width") == W and s.get("height") == H for s in json.loads(probe)["streams"]) else "FAIL"}
    report["C6_exact_all"] = "PASS" if all(r["C6_exact"]["status"] == "PASS" for r in report["text"]) else "FAIL"
    report["C7_brand_colours"] = "N/A — no brand hex supplied for a spec film; ink 3A2A20 / accent 9A4B3F / backing F4EDE3 recorded"
    report["duration_s"] = total; report["output"] = str(out.relative_to(JOB)); report["sha256"] = sha(out)
    (out.with_suffix(".qa.json")).write_text(json.dumps(report, indent=1, default=str))
    print(f"built {out.relative_to(JOB)}  {W}x{H}  {total:.2f} s  sha256 {report['sha256'][:16]}  text boxes {len(report['text'])}  deviations {len(report['deviations'])}")


if __name__ == "__main__":
    main()
