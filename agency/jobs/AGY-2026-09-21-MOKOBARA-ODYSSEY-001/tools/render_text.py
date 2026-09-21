#!/usr/bin/env python3
"""render_text.py (v2, repair round 1) — every exact string in the film, composed by code (mechanism B) from copy-deck.json.
Writes gen/overlays/super.png (the wordmark super, transparent), gen/overlays/endcard.png (1080x1920) and
gen/overlays/layout.json (every text/logo box + gate results).

Brand assets, never redrawn: the wordmark super uses the site's own BLACK logo PNG (source/mokobara/logo-png.png, fetched
from mokobara.com, FETCH-LOG.txt) because the beat-2 sky is light (white measured 1.3:1 on real pixels); the end card uses
the site's WHITE SVG (source/mokobara/wordmark-white.svg) on the bag navy. Both hashes are recorded in layout.json.
Typography: the site's own face is 'NeurialGrotesk' (@font-face in home.html, a commercial font not on this machine, not
downloaded); its Shopify body font is Karla (not present either). Closest face available here: Helvetica Neue (system
.ttc), a neo-grotesque of the same family as Neurial Grotesk. Weights: Medium (face 10) for the product line and CTA,
Light (face 7) for the tagline. The product line is set as the site sets its small labels — uppercase, letter-spacing
.08em (home.html: 'letter-spacing: .08em; text-transform: uppercase'); the tagline carries the site's heading tracking
(-0.02em). Shaping: hb-view (HarfBuzz 14) renders every line; tracking is applied per glyph run by code.
Safe box (65,288)-(888,1248) from Stage 2; everything is centred on the box's x-centre (476). No lockup rule (clear space,
mono-colour) was found in the fetched html; clear space used = the wordmark's own x-height on every side."""
import json, subprocess, hashlib, os, sys, tempfile
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from runtime.compositor.gates import check_text_bounds, check_contrast, check_disjoint, relative_luminance, LayoutRefused
JOB = Path(__file__).resolve().parent.parent
deck = json.load(open(JOB / "copy-deck.json"))["strings"]
OUT = JOB / "gen/overlays"; OUT.mkdir(parents=True, exist_ok=True)
SAFE = (65, 288, 888, 1248); CX = (SAFE[0] + SAFE[2]) // 2; CANVAS = (0, 0, 1080, 1920)
NAVY = "#242840"                      # bag navy sampled from the product photo (#383d5a) darkened ~35% for text contrast
FONT = "/System/Library/Fonts/HelveticaNeue.ttc"; MEDIUM, LIGHT = 10, 7
LOGO_BLACK = JOB / "source/mokobara/logo-png.png"; LOGO_WHITE = JOB / deck["wordmark_asset"]
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
ENV = dict(os.environ, LANG="en_US.UTF-8", LC_ALL="en_US.UTF-8")

def hb(s: str, size: int, face: int, colour="ffffff") -> Image.Image:
    with tempfile.TemporaryDirectory() as d:
        t = Path(d) / "t.txt"; t.write_text(s, encoding="utf-8"); o = Path(d) / "o.png"
        subprocess.run(["hb-view", FONT, "-y", str(face), f"--font-size={size}", "--background=none", f"--foreground={colour}",
                        "--margin=0", "-o", str(o), f"--text-file={t}"], check=True, env=ENV)
        return Image.open(o).convert("RGBA")

def run(s: str, size: int, face: int, track_em: float = 0.0, colour="ffffff") -> Image.Image:
    """One shaped line; tracking (em) applied between glyph runs by code (hb-view has no letter-spacing)."""
    if not track_em:
        im = hb(s, size, face, colour); return im.crop(im.getbbox())
    parts = [hb(c, size, face, colour) if c != " " else None for c in s]
    gap = int(round(track_em * size)); space = int(round(0.28 * size))
    w = sum((p.width if p else space) + gap for p in parts) - gap; h = max(p.height for p in parts if p)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); x = 0
    for p in parts:
        if p: im.alpha_composite(p, (x, 0)); x += p.width + gap
        else: x += space + gap
    return im.crop(im.getbbox())

def logo_black(width: int) -> Image.Image:
    im = Image.open(LOGO_BLACK).convert("RGBA"); im = im.crop(im.getbbox())
    return im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)

def logo_white(width: int) -> Image.Image:
    p = OUT / f"wordmark-{width}.png"
    subprocess.run(["rsvg-convert", "-w", str(width), "-o", str(p), str(LOGO_WHITE)], check=True)
    im = Image.open(p).convert("RGBA"); return im.crop(im.getbbox())

def lum_samples(rgb: Image.Image, box):
    px = rgb.crop(box).resize((min(64, box[2] - box[0]), min(64, box[3] - box[1]))).getdata()
    return [relative_luminance("#%02x%02x%02x" % p[:3]) for p in px]

layout = {"safe_box": SAFE, "font": {"family": "Helvetica Neue (system)", "file": FONT, "faces": {"medium": MEDIUM, "light": LIGHT},
          "site_faces_seen": ["NeurialGrotesk (commercial, @font-face in home.html)", "Karla (Shopify font picker)", "Montserrat", "HammersmithOne"],
          "why": "closest neo-grotesque available on this machine; no font downloaded"},
          "logo_black_sha256": sha(LOGO_BLACK), "wordmark_sha256": sha(LOGO_WHITE), "items": [], "gates": []}
def place(img, im, x, y, id_, kind):
    img.alpha_composite(im, (x, y)); box = [x, y, x + im.width, y + im.height]
    layout["items"].append({"id": id_, "kind": kind, "box": box}); return tuple(box)

# ── 1. wordmark super (beat 2, 5.0–7.5 s): the site's black logo, 420 px, top-left of the safe box, on the sky ──
sup = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); wm = logo_black(420)
xh = round(wm.height * 0.62)                                       # x-height of the wordmark ≈ clear space
sb = place(sup, wm, SAFE[0], SAFE[1] + xh, "wordmark_super", "logo"); sup.save(OUT / "super.png")
layout["gates"].append(check_text_bounds(sb, canvas=CANVAS, container=SAFE, id_="wordmark_super"))
# contrast on the real pixels behind the box for every sampled beat-2 frame under the super (assemble upscales b2 to 1080x1920)
frames_dir = Path(tempfile.mkdtemp())
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1.5", "-i", str(JOB / "gen/clips/b2.mp4"), "-t", "2.5", "-vf", "fps=4,scale=1080:1920", str(frames_dir / "f%02d.png")], check=True)
samples = []
for f in sorted(frames_dir.glob("*.png")): samples += lum_samples(Image.open(f).convert("RGB"), sb)
layout["gates"].append(check_contrast("#000000", samples, role="display", id_="wordmark_super (black logo on sky, 10 frames)"))
for f in frames_dir.glob("*.png"): f.unlink()

# ── 2. end card: wordmark first and largest, then product line, tagline, CTA — one centred column ──
card = Image.new("RGBA", (1080, 1920), NAVY + "ff" and (0x24, 0x28, 0x40, 255)); wm2 = logo_white(700)
pl = run(deck["product_line"].upper(), 34, MEDIUM, track_em=0.08, colour="ffffffd9")
tg = run(deck["tagline"], 62, LIGHT, track_em=-0.02)
ct = run(deck["cta"], 40, MEDIUM)
gap_wm, gap_pl, gap_tg = 56, 88, 120
total = wm2.height + gap_wm + pl.height + gap_pl + tg.height + gap_tg + ct.height
y = (SAFE[1] + SAFE[3]) // 2 - total // 2 - 20
boxes = {}
boxes["wordmark_end"] = place(card, wm2, CX - wm2.width // 2, y, "wordmark_end", "logo"); y += wm2.height + gap_wm
boxes["headline"] = place(card, pl, CX - pl.width // 2, y, "product_line", "text"); y += pl.height + gap_pl
boxes["tagline"] = place(card, tg, CX - tg.width // 2, y, "tagline", "text"); y += tg.height + gap_tg
boxes["cta"] = place(card, ct, CX - ct.width // 2, y, "cta", "text")
card.save(OUT / "endcard.png")
for k, b in boxes.items(): layout["gates"].append(check_text_bounds(b, canvas=CANVAS, container=SAFE, id_=k))
for k, role in [("headline", "body"), ("tagline", "display"), ("cta", "body")]:
    layout["gates"].append(check_contrast("#ffffff", [], role=role, backing_hex=NAVY, id_=f"{k} on navy"))
layout["gates"].append(check_disjoint({"wordmark_end": boxes["wordmark_end"], "headline": boxes["headline"], "tagline": boxes["tagline"], "cta": boxes["cta"]},
                                      critical=("wordmark_end", "headline", "tagline", "cta"), min_gap_px=24))
layout["strings_composed"] = {k: v for k, v in deck.items() if k != "wordmark_asset"}
layout["strings_rendered"] = {"product_line": deck["product_line"].upper() + "  (uppercase, .08em, as the site's labels)", "tagline": deck["tagline"], "cta": deck["cta"]}
json.dump(layout, open(OUT / "layout.json", "w"), indent=1)
print("items", len(layout["items"]), "| gates:", [(g.get("id") or "disjoint", g["status"], g.get("worst_ratio")) for g in layout["gates"]])
