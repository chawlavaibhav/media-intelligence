#!/usr/bin/env python3
"""preview.py — USD-0 look tool: renders the frames at the given times (full pipeline, no encode) and tiles them into one
strip so a beat can be judged frame by frame. usage: preview.py <out.png> <poses> t1 t2 ...  (times in seconds)
Because particles / hit-stop are stateful, the renderer walks every frame from the earliest time to the latest and keeps
only the requested ones."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_v2 as R
import pixfont as PF

out = Path(sys.argv[1]); poses = sys.argv[2]; times = [float(x) for x in sys.argv[3:]]
want = {int(round(t * R.FPS)) for t in times}
i0, i1 = min(want), max(want) + 1
S = R.V2Sprites(R.JOB / "gen/assets", poses); plate = S.plate(); st = R.State()
last_world = last_wt = None; last_boxes = []; frames = []
for i in range(i0, i1):
    t = i / R.FPS; f = R.beat_at(t); n = f["n"]; log = []
    if n == "F11":
        cv = R.end_card(t, S, log); sb = []
    else:
        wt = R.world_time(t)
        if last_world is not None and abs(wt - last_wt) < 1e-6:
            world = last_world; boxes = last_boxes
        else:
            boxes = []; world = R.draw_world(t, wt, S, plate, st, boxes)
            mul, vig, lift, cyan = R.grade_for(t)
            if mul != (1, 1, 1) or vig or lift or cyan:
                world = R.grade(world, mul, vig, lift, cyan)
            last_world, last_wt, last_boxes = world, wt, boxes
        s, cx, cy = R.camera(t); dx, dy = R.shake_offset(t)
        cv, view = R.apply_camera(world, s, cx, cy, dx, dy); cv = cv.copy()
        st.view = view
        R.draw_ui(cv, t, log, S, st)
        sb = [{**b, "screen_box": R.to_screen(b["box"], view)} for b in boxes]
    if i in want:
        im = cv.convert("RGB"); d = ImageDraw.Draw(im)
        for b in sb:   # thin outlines of the logged sprite boxes (screen space) so overlaps with text are visible
            d.rectangle(b["screen_box"], outline=(255, 0, 255), width=2)
        for b in log:
            d.rectangle(b.get("backing_box") or b["box"], outline=(0, 255, 0), width=2)
        frames.append((t, im, s if n != "F11" else 1.0))
cols = min(6, len(frames)); th = 640; tw = int(th * R.W / R.H); rows = (len(frames) + cols - 1) // cols
sheet = Image.new("RGB", (cols * tw, rows * (th + 26)), (20, 20, 24))
for j, (t, im, s) in enumerate(frames):
    x, y = (j % cols) * tw, (j // cols) * (th + 26)
    sheet.paste(im.resize((tw, th), Image.LANCZOS), (x, y))
    lab = PF.render(f"{t:05.2f} X{s:.2f}", 2, fg=(255, 255, 255)); sheet.paste(lab, (x + 6, y + th + 4), lab)
sheet.save(out); print("wrote", out, len(frames), "frames")
