#!/usr/bin/env python3
"""composite_d.py — Treatment D: code HUD/text over the generated clip (05 §3f).

The generated 720x1280 24-fps clip is the WORLD layer; the UI layer (PG OWNER + health, wordmark chip, obstacle labels,
GAME OVER?, the cheat panel with its typed lines, POWER UP!, the chip flight, the HUD phone icon) is drawn by code at the
baseline's positions/scales with the frozen put_text, so the layout-log gates apply. UI timing follows the CLIP's own
events (read off the 10-fps contact sheet by the producer — the one manual pass 05 predicted), not the board.
Output: 1080x1920 30 fps video (LANCZOS upscale of each nearest source frame), native audio of the clip kept.
usage: composite_d.py <take.mp4> <events.json> <out_video_only.mp4> <name>
"""
import json, subprocess, sys, tempfile, shutil
from pathlib import Path
from PIL import Image, ImageDraw
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "C-creative-direction/job/tools"))
import render_game as G  # noqa: E402  (frozen copy; JOB there holds board/deck/logo)
T = G.T; W, H = G.W, G.H; FPS = 30; hx = G.hx

take, events_path, out, name = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
E = json.load(open(events_path))          # clip-relative seconds
board, deck, frames = G.load()
S = G.Sprites("final", HERE.parent / "A-baseline/frozen-inputs/gen/assets")
DUR = E["out_s"]


def health(t):
    if t < E["hit"]: return 1
    if t < E["refill_start"]: return 0
    return min(5, int((t - E["refill_start"]) / 0.08) + 1)


def ui(cv, t, log):
    d = ImageDraw.Draw(cv); cxs = (T.safe[0] + T.safe[2]) // 2; put = G.put_text
    powered = t >= E["install"]
    if E["label5_0"] <= t < E["label5_1"]:
        put(cv, log, "OBST_5", deck["OBST_5"], T.label_scale, T.yellow, cx=cxs, y=T.label_y)
    if E["label1_0"] <= t < E["label1_1"]:
        put(cv, log, "OBST_1", deck["OBST_1"], T.label_scale, T.yellow, cx=cxs, y=T.label_y)
    if t >= E["chip_0"]:
        k2 = 1 - (1 - min(1.0, (t - E["chip_0"]) / 0.35)) ** 3
        cw = G.text_img(deck["CHIP_1"], T.checklist_scale, T.green).width
        x_start = max(T.safe[0] + T.chip_pad, min(T.safe[2] - cw - T.chip_pad, 700 - cw // 2))
        x = int(x_start + (T.checklist_x - x_start) * k2); y = int(880 + (T.checklist_y0 - 880) * k2)
        put(cv, log, "CHIP_1", deck["CHIP_1"], T.checklist_scale, T.green, x=x, y=y, pad=T.chip_pad)
    hp = health(t); hkey = f"HUD_HEALTH_{hp}"
    put(cv, log, "HUD_NAME", deck["HUD_NAME"], T.hud_scale, T.white, x=T.safe[0] + 12, y=T.hud_y + 6)
    hfg = T.cyan if powered else (T.white if hp > 1 else T.yellow)
    hx0 = T.safe[0] + 12 + G.text_img(deck["HUD_NAME"], T.hud_scale, T.white).width + 40
    put(cv, log, hkey, deck[hkey], T.hud_scale, hfg, x=hx0, y=T.hud_y + 6)
    if powered and t >= E["refill_start"] + 0.4:
        pxx = hx0 + G.text_img(deck[hkey], T.hud_scale, hfg).width + 36
        d.rectangle((pxx, T.hud_y - 2, pxx + 30, T.hud_y + 52), fill=hx(T.brand_blue), outline=hx(T.ink), width=3)
        d.rectangle((pxx + 6, T.hud_y + 6, pxx + 24, T.hud_y + 40), fill=hx(T.cyan))
    chip = S.wordmark.resize((T.chip_box[2] - T.chip_box[0], T.chip_box[3] - T.chip_box[1]), Image.LANCZOS)
    cv.alpha_composite(chip, (T.chip_box[0], T.chip_box[1]))
    log.append({"id": "WORDMARK_CHIP", "text": "RentOk (raster)", "kind": "logo", "box": list(T.chip_box), "fg": None, "backing": None})
    blink = int(t * 4) % 2 == 0
    if E["gameover_0"] <= t < E["gameover_1"] and blink:
        put(cv, log, "GAMEOVER", deck["GAMEOVER"], T.flash_scale, T.yellow, cx=cxs, y=T.flash_y)
    if E["powerup_0"] <= t < E["powerup_1"] and blink:
        put(cv, log, "POWERUP", deck["POWERUP"], T.flash_scale, T.cyan, cx=cxs, y=T.flash_y)
    # cheat panel: slide over panel_slide_s, type over type_s, fade over 0.3 s after panel_off
    p0, ps, ty0, tys, poff = E["panel_0"], E["panel_slide_s"], E["type_0"], E["type_s"], E["panel_off"]
    if p0 <= t < poff + 0.3:
        slide = min(1.0, (t - p0) / ps); py = int(520 + (1 - slide) * 500); panel = (105, py, 848, py + 400)
        if t < poff:
            d.rectangle(panel, fill=hx(T.panel), outline=hx(T.cyan), width=6)
        else:
            fade = max(0.0, 1 - (t - poff) / 0.3)
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(ov).rectangle(panel, fill=hx(T.panel, int(255 * fade)), outline=hx(T.cyan, int(255 * fade)), width=6); cv.alpha_composite(ov)
        if slide >= 1.0 and t < poff:
            put(cv, log, "CHEAT_HDR", deck["CHEAT_HDR"], 7, T.white, cx=cxs, y=py + 36, backing=T.panel)
            full1, full2 = deck["CHEAT_1"], deck["CHEAT_2"]
            nchars = int(max(0.0, (t - ty0)) / tys * (len(full1) + len(full2)))
            s1 = full1[:min(nchars, len(full1))]; s2 = full2[:max(0, nchars - len(full1))]
            if s1: put(cv, log, "CHEAT_1" if s1 == full1 else "CHEAT_1_partial", s1, T.cheat_scale, T.cyan, cx=cxs, y=py + 130, backing=T.panel)
            if s2: put(cv, log, "CHEAT_2" if s2 == full2 else "CHEAT_2_partial", s2, T.cheat_scale, T.cyan, cx=cxs, y=py + 240, backing=T.panel)


tmp = tempfile.mkdtemp()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(take), f"{tmp}/f%04d.png"], check=True)
src = sorted(Path(tmp).glob("f*.png")); n_src = len(src); src_fps = 24.0
n_out = int(round(DUR * FPS)); log_all = []
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
       "-c:v", "libx264", "-profile:v", "high", "-pix_fmt", "yuv420p", "-b:v", "9M", "-maxrate", "12M", "-bufsize", "18M", "-g", "15", "-bf", "2", "-r", str(FPS), "-movflags", "+faststart", "-an", str(out)]
proc = subprocess.Popen(cmd, stdin=subprocess.PIPE); cache = {}
for i in range(n_out):
    t = i / FPS; j = min(n_src - 1, int(round(t * src_fps)))
    if j not in cache:
        cache = {j: Image.open(src[j]).convert("RGB").resize((W, H), Image.LANCZOS).convert("RGBA")}
    cv = cache[j].copy(); log = []; ui(cv, t, log)
    log_all.append({"frame": i, "t": round(t, 3), "src_frame": j, "boxes": log})
    proc.stdin.write(cv.convert("RGB").tobytes())
proc.stdin.close(); proc.wait(); shutil.rmtree(tmp)
with open(HERE / f"gen/{name}-layout.jsonl", "w") as fh:
    for row in log_all: fh.write(json.dumps(row, ensure_ascii=False) + "\n")
print("wrote", out, "frames", n_out)
