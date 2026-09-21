#!/usr/bin/env python3
"""render_text.py — every exact string in the film, composed by code (mechanism B) from copy-deck.json.
Writes gen/overlays/super.png (the wordmark super, transparent), gen/overlays/endcard.png (1080x1920), and
gen/overlays/layout.json (every text/logo box, for the safe-box DET check). Wordmark = source/mokobara/wordmark-white.svg
rasterised by rsvg-convert (never redrawn). Font: Avenir Next (system; the brand's face is not verified — Stage 2 (d)).
Safe box (65,288)-(888,1248) from Stage 2; everything is centred on the box's x-centre (476), as Lane A did."""
import json, subprocess, hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
JOB = Path(__file__).resolve().parent.parent
deck = json.load(open(JOB / "copy-deck.json"))["strings"]
OUT = JOB / "gen/overlays"; OUT.mkdir(parents=True, exist_ok=True)
SAFE = (65, 288, 888, 1248); CX = (SAFE[0] + SAFE[2]) // 2
NAVY = (0x24, 0x28, 0x40)      # bag navy sampled from the product photo (#383d5a) darkened ~35% for text contrast
FONT = "/System/Library/Fonts/Avenir Next.ttc"
def font(size, idx): return ImageFont.truetype(FONT, size, index=idx)     # 7 Regular, 5 Medium, 2 Demi Bold
def wordmark(width):
    p = OUT / f"wordmark-{width}.png"
    subprocess.run(["rsvg-convert", "-w", str(width), "-o", str(p), str(JOB / deck["wordmark_asset"])], check=True)
    return Image.open(p).convert("RGBA")
layout = {"safe_box": SAFE, "items": []}
def place(img, im, x, y, id_, kind):
    img.alpha_composite(im, (x, y)); layout["items"].append({"id": id_, "kind": kind, "box": [x, y, x + im.width, y + im.height]})
def text_img(s, f, fill=(255, 255, 255, 255)):
    d = ImageDraw.Draw(Image.new("RGBA", (1, 1))); l, t, r, b = d.textbbox((0, 0), s, font=f)
    im = Image.new("RGBA", (r - l + 4, b - t + 4), (0, 0, 0, 0)); ImageDraw.Draw(im).text((2 - l, 2 - t), s, font=f, fill=fill); return im
# 1. wordmark super (beat 2): small, bottom of the safe box, with a soft dark backing for contrast over pebbles
sup = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); wm = wordmark(300)
bx, by = CX - wm.width // 2, SAFE[1] + 40      # top of the safe box: over the sky, never over the product
back = Image.new("RGBA", (wm.width + 60, wm.height + 36), (0, 0, 0, 110)); sup.alpha_composite(back, (bx - 30, by - 18))
layout["items"].append({"id": "super_backing", "kind": "backing", "box": [bx - 30, by - 18, bx + wm.width + 30, by + wm.height + 18]})
place(sup, wm, bx, by, "wordmark_super", "logo"); sup.save(OUT / "super.png")
# 2. end card
card = Image.new("RGBA", (1080, 1920), NAVY + (255,)); wm2 = wordmark(600)
y = 700; place(card, wm2, CX - wm2.width // 2, y, "wordmark_end", "logo"); y += wm2.height + 48
t = text_img(deck["product_line"], font(40, 5), (255, 255, 255, 215)); place(card, t, CX - t.width // 2, y, "product_line", "text"); y += t.height + 70
t = text_img(deck["tagline"], font(54, 7)); place(card, t, CX - t.width // 2, y, "tagline", "text"); y += t.height + 90
t = text_img(deck["cta"], font(42, 2)); place(card, t, CX - t.width // 2, y, "cta", "text")
card.save(OUT / "endcard.png")
layout["strings_composed"] = {k: v for k, v in deck.items() if k != "wordmark_asset"}
layout["wordmark_sha256"] = hashlib.sha256(open(JOB / deck["wordmark_asset"], "rb").read()).hexdigest()
json.dump(layout, open(OUT / "layout.json", "w"), indent=1)
bad = [i for i in layout["items"] if not (SAFE[0] <= i["box"][0] and SAFE[1] <= i["box"][1] and i["box"][2] <= SAFE[2] and i["box"][3] <= SAFE[3])]
print("items", len(layout["items"]), "outside safe box:", bad)
