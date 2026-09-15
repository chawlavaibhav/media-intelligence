#!/usr/bin/env python3
"""Export portfolio tile media (USD 0): existing accepted V3/V4 media + code-composed missing sizes. usage: export_tiles.py <out>"""
import shutil, subprocess, sys
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent))
import compose_v4 as Cp

V4 = Path(__file__).resolve().parent.parent; V3 = V4.parent / "v3"; G3 = V3 / "gen"; D3 = G3 / "deliverables"
REPO = V4.parents[2]; LAB = REPO / "eval/experiments/EVAL-040/runs"
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
A1 = Image.open(G3 / "stills/a1-accepted.png").convert("RGBA"); A2 = Image.open(G3 / "stills/a2-accepted.png").convert("RGBA")
KORA = Image.open(G3 / "stills/kora-accepted.png").convert("RGBA"); DH = Image.open(G3 / "stills/dhaba-accepted.png").convert("RGBA")
HOOKS = Cp.DECK["aarohi"]["hooks"]; KH = Cp.DECK["kora"]["hooks"]


def save(im, p): p.parent.mkdir(parents=True, exist_ok=True); im.convert("RGB").save(p, quality=95)
def cp(src, dst): dst.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(src, dst)


# tile 01 — Aarohi Skin: master offer in 4 sizes (V3), and the same layout with a SHOP NOW button in 4 sizes (rubric Q3)
t = out / "tile-01-aarohi-skin"
for f in ("4x5", "1x1", "9x16", "wa"):
    cp(D3 / f"aarohi-master-{f}.png", t / f"aarohi-offer-{f}.png")
    save(Cp.aarohi(A1, f, anchor=(0.62, 0.5), cta="SHOP NOW"), t / f"aarohi-offer-cta-{f}.png")
cp(V4 / "gen/deliverables/aarohi-craft-4x5.png", t / "aarohi-hook-night-routine-cta-4x5.png")
cp(V4 / "gen/deliverables/aarohi-offer-in-motion-9x16-11s.mp4", t / "aarohi-offer-in-motion-9x16-11s.mp4")
cp(G3 / "video/a1-accepted.mp4", t / "aarohi-hero-motion-16x9-5s.mp4")
cp(G3 / "stills/a0-accepted.png", t / "aarohi-source-packshot.png")
# tile 02 — six hooks (Aarohi), each in 4x5 + the Hindi version; plus CTA versions
t = out / "tile-02-six-hooks-aarohi"
for j, h in enumerate(HOOKS, 1):
    cp(D3 / f"aarohi-hook-{j}-4x5.png", t / f"hook-{j}-4x5.png")
    save(Cp.aarohi(A1, "4x5", variant=h, anchor=(0.62, 0.5), cta="SHOP NOW"), t / f"hook-{j}-cta-4x5.png")
cp(D3 / "aarohi-hindi-4x5.png", t / "hindi-offer-4x5.png")
for f in ("1x1", "9x16", "wa"):
    save(Cp.aarohi(A1, f, hindi=True, anchor=(0.62, 0.5)), t / f"hindi-offer-{f}.png")
# tile 03 — Kora Threads: six hooks 16:9 (V3) + hook 1 in 4x5, 1x1, 9x16, wa (composed now) + base still
t = out / "tile-03-kora-threads"
for j in range(1, 7):
    save(Cp.kora(KORA, "16x9", KH[j - 1]), t / f"kora-hook-{j}-16x9.png")
for f, anc in (("4x5", (0.30, 0.35)), ("1x1", (0.30, 0.35)), ("9x16", (0.30, 0.35)), ("wa", (0.30, 0.35))):
    save(Cp.kora(KORA, f, KH[0], anchor=anc), t / f"kora-hook-1-{f}.png")
cp(G3 / "stills/kora-accepted.png", t / "kora-base-still-16x9.png")
# tile 05 — Dhaba 47 Hindi: picture over a warm dark panel, Hindi offer + CTA on the panel (v2, 15 Sep), four sizes
t = out / "tile-05-dhaba-47-hindi"
for f, anc, z in (("4x5", (0.60, 0.50), 1.0), ("1x1", (0.60, 0.46), 1.0), ("9x16", (0.66, 0.55), 1.0), ("wa", (0.60, 0.46), 1.0)):
    save(Cp.dhaba_panel(DH, f, anchor=anc, zoom=z), t / f"dhaba47-hindi-{f}.png")
cp(G3 / "stills/dhaba-accepted.png", t / "dhaba47-source-flatlay.png")
# tile 03b — Brewa Kettle: packshot + three accepted scenes + the kitchen motion clip
t = out / "tile-03-brewa-kettle"
cp(G3 / "stills/brewa0-accepted.png", t / "brewa-source-packshot.png")
for k, n in (("b1", "scene-1-kitchen"), ("b2", "scene-2-breakfast-window"), ("b3", "scene-3-evening-counter")):
    cp(G3 / f"stills/{k}-accepted.png", t / f"brewa-{n}-16x9.png")
cp(G3 / "video/b1-accepted.mp4", t / "brewa-scene-1-motion-16x9-4s.mp4")
# tile 09 — presenter: V4 accepted speaker clip, anchor still, bubble frame, V2 takes, the film
t = out / "tile-09-presenter"
cp(V4 / "gen/speaker/veo-r3.mp4", t / "presenter-take-v4-8s.mp4"); cp(V4 / "gen/speaker/still-accepted.png", t / "presenter-anchor-still.png")
cp(V4 / "gen/speaker/speaker-bubble-frame.png", t / "presenter-frame-7.7s.png")
for k in ("t1", "t2", "t3"):
    p = V3.parent / "gen/p1-presenter-takes" / f"{k}-veo-r1.mp4"
    if p.exists(): cp(p, t / f"presenter-v2-take-{k}-8s.mp4")
p = V3.parent / "gen/p2-presenter-chain/chain-1080-r2.mp4"
if p.exists(): cp(p, t / "presenter-v2-chain-22s.mp4")
cp(V4 / "assembly/v4.1/upwork-intro-v4.1.mp4", t / "intro-film-v4.1-57s.mp4")
# tile 10 — two-speaker Hindi paint-can clips (sealed EVAL-040 VID-2SPK-01, all six accepted)
t = out / "tile-10-two-speaker-hindi"
for r in ("veo-3.1-fast__A_native__r1", "veo-3.1-fast__A_native__r2", "gemini-omni-1.1-flash__A_native__r1", "gemini-omni-1.1-flash__A_native__r2", "wan-3.0-prime__A_native__r1", "wan-3.0-prime__A_native__r2"):
    src = LAB / "vid-2spk/artifacts/media" / f"VID-2SPK-01__{r}.mp4"; cp(src, t / f"two-speaker-hindi-{r.split('__')[0]}-{r[-2:]}.mp4")
# tile 07 — real-estate story: the accepted three-shot story clips to choose from (sealed VID-MS-01/02)
t = out / "tile-07-story-clips-to-pick"
for r, n in (("VID-MS-01__kling-v3-pro-15s__core__r1", "story-15s-couple-kling-r1"), ("VID-MS-01__kling-v3-pro-15s__core__r2", "story-15s-couple-kling-r2"),
             ("VID-MS-02__gemini-omni-1.1-flash-10s__core__r1", "story-10s-sleep-omni-r1"), ("VID-MS-02__gemini-omni-1.1-flash-10s__core__r2", "story-10s-sleep-omni-r2")):
    cp(LAB / "vid-ms/artifacts/media" / f"{r}.mp4", t / f"{n}.mp4")
print("exported to", out)
