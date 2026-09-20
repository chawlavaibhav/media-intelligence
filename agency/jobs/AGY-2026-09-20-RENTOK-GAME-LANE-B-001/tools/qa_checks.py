#!/usr/bin/env python3
"""Deterministic QA over the delivered file and the composition inputs. USD 0. Every check prints PASS/FAIL with evidence;
the JSON report goes to qa/QA-REPORT.json. Checks: container · safezone · disjoint · copy · claims · prompts · frames ·
loudness · moov."""
from __future__ import annotations

import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
JOB = HERE.parent
REPO = JOB.parents[2]
sys.path.insert(0, str(REPO)); sys.path.insert(0, str(HERE))
from runtime.compositor.gates import check_disjoint, check_text_bounds, LayoutRefused  # noqa: E402
import text_render as T  # noqa: E402
from render_film import DECK, TL  # noqa: E402

FINAL = JOB / "gen/final/rentok-game-lane-b-9x16-30s.mp4"
QA = JOB / "qa"; QA.mkdir(exist_ok=True)
REPORT = {}

FORBIDDEN = ["guarantee", "never", "always", "100%", "zero dues", "zero problems", "no problems", "all problems", "every problem", "no more",
             "can't leave", "cannot leave", "won't leave", "stop tenants", "stops tenants", "prevent", "recover", "insured", "insurance", "claim",
             "instantly verified", "instant verification", "safe tenants", "trusted tenants", "%", "x faster", "eqaro", "mario", "nintendo",
             "luigi", "bowser", "koopa", "goomba", "peach", "nano banana", "gemini", "veo", "lyria", "sarvam", "elevenlabs", "openai", "claude"]
PERMITTED = {"TENANT: VERIFIED": "PC1d", "AUTOPAY: ON": "PC2a", "DUES VISIBLE": "PC3a", "REPORTS: DONE": "PC4a", "TICKETS RESOLVED": "PC5a+PC5c",
             "Get the app": "PC6a", "CHEAT CODE: INSTALL RENTOK": "PC7", "RENTOK MODE: OFF": "brand", "RENTOK MODE: ON": "brand"}


def ffprobe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)], capture_output=True, text=True, check=True)
    return json.loads(r.stdout)


def c_container():
    d = ffprobe(FINAL); v = next(s for s in d["streams"] if s["codec_type"] == "video"); a = next(s for s in d["streams"] if s["codec_type"] == "audio")
    dur = float(d["format"]["duration"])
    checks = {"width_1080": v["width"] == 1080, "height_1920": v["height"] == 1920, "h264": v["codec_name"] == "h264", "profile_high": v.get("profile") == "High",
              "yuv420p": v["pix_fmt"] == "yuv420p", "fps_30": v["r_frame_rate"] == "30/1", "aac": a["codec_name"] == "aac", "aac_48k": a["sample_rate"] == "48000",
              "stereo": a["channels"] == 2, "duration_29.5_30.5": 29.5 <= dur <= 30.5, "size_lt_4GB": int(d["format"]["size"]) < 4 * 1024 ** 3}
    # moov before mdat (faststart)
    data = FINAL.read_bytes()[:4096]
    checks["moov_before_mdat"] = data.find(b"moov") != -1 and (data.find(b"mdat") == -1 or data.find(b"moov") < data.find(b"mdat"))
    ok = all(checks.values())
    REPORT["container"] = {"status": "PASS" if ok else "FAIL", "duration_s": dur, "bit_rate": d["format"].get("bit_rate"), "size_bytes": d["format"]["size"], "checks": checks}
    print("container:", "PASS" if ok else "FAIL", f"dur={dur:.3f}s", f"{v['width']}x{v['height']}", v["codec_name"], v.get("profile"), v["pix_fmt"], v["r_frame_rate"], a["codec_name"], a["sample_rate"], a["channels"], "bitrate", d["format"].get("bit_rate"))


def c_safezone_disjoint():
    lay = json.load(open(JOB / "gen/render/LAYOUT.json"))
    fails = []; n = 0
    byframe = defaultdict(dict)
    crit = {"C01", "C02", "C03", "C04", "C05", "C06", "C07", "C08", "C09", "C10", "C11", "C12", "C13", "C14", "C15", "C16", "C17", "C18", "C19", "C20", "C21", "C22", "C10-typing", "HUD-heart"}
    for it in lay:
        if it["id"] not in crit: continue
        n += 1
        try:
            check_text_bounds(tuple(it["box"]), canvas=(0, 0, 1080, 1920), container=T.SAFE, tokens=T.TOKENS, id_=it["id"])
        except LayoutRefused as e:
            fails.append({"id": it["id"], "t": it["t"], "box": it["box"], "err": str(e)[:120]})
        # right-edge rule: no critical text with x>950 in y>960 (Stage 2 decision)
        x0, y0, x1, y1 = it["box"]
        if x1 > 950 and y1 > 960: fails.append({"id": it["id"], "t": it["t"], "box": it["box"], "err": "right-edge rule (x>950 & y>960)"})
        if it["id"] in byframe[it["t"]] and byframe[it["t"]][it["id"]] == tuple(it["box"]):
            continue                                   # identical duplicate record of the same placement (not two regions)
        byframe[it["t"]][it["id"] + ("" if it["id"] not in byframe[it["t"]] else "_b")] = tuple(it["box"])
    dis_fails = []
    for t, regions in byframe.items():
        try:
            check_disjoint(regions, critical=tuple(regions.keys()), min_gap_px=T.TOKENS.min_gap_px)
        except LayoutRefused as e:
            dis_fails.append({"t": t, "err": str(e)[:160]})
    REPORT["safezone"] = {"status": "PASS" if not fails else "FAIL", "placements_checked": n, "failures": fails[:20], "safe_box": T.SAFE}
    REPORT["disjoint"] = {"status": "PASS" if not dis_fails else "FAIL", "frames_checked": len(byframe), "failures": dis_fails[:20], "min_gap_px": T.TOKENS.min_gap_px}
    print("safezone:", REPORT["safezone"]["status"], n, "placements;", len(fails), "failures")
    print("disjoint:", REPORT["disjoint"]["status"], len(byframe), "frames;", len(dis_fails), "failures")


def c_copy_claims():
    pg = json.load(open(JOB / "gen/render/PLATE_GATES.json"))
    rendered = defaultdict(set)
    for k, rep in pg.items():
        cid = k.split("|")[0]
        rendered[cid].add(" ".join(rep["lines"]).replace("_", "").strip())
    mism = []
    for cid, val in DECK.items():
        got = rendered.get(cid, set())
        if val not in got: mism.append({"id": cid, "expected": val, "rendered": sorted(got)})
    # contrast + geometry statuses from the gate reports
    bad = [k for k, rep in pg.items() if rep["contrast"]["status"] != "PASS" or rep["geometry"] != "PASS"]
    worst = min(rep["contrast"]["worst_ratio"] for rep in pg.values())
    REPORT["copy"] = {"status": "PASS" if not mism else "FAIL", "deck_strings": len(DECK), "mismatches": mism, "contrast_min_ratio": worst, "gate_failures": bad}
    print("copy byte-exact:", REPORT["copy"]["status"], f"{len(DECK)} strings; worst contrast {worst}")
    # forbidden scan over deck + VO transcripts + VO lines
    texts = {f"deck:{k}": v for k, v in DECK.items()}
    for p in sorted(QA.glob("transcript_*.txt")): texts[f"transcript:{p.name}"] = p.read_text()
    for vid, line in {"V1": "Cheat code: install RentOk.", "V2": "RentOk mode: on.", "V3": "Level complete. Get the app."}.items(): texts[f"vo:{vid}"] = line
    hits = [(k, w) for k, v in texts.items() for w in FORBIDDEN if w.lower() in v.lower()]
    # claim strings: every product-state card must be in the permitted list
    cards = {DECK[c] for c in ("C13", "C14", "C15", "C16", "C17", "C20", "C10", "C03", "C12")}
    unpermitted = [c for c in cards if c not in PERMITTED]
    REPORT["claims"] = {"status": "PASS" if not hits and not unpermitted else "FAIL", "forbidden_hits": hits, "unpermitted_product_strings": unpermitted,
                        "permitted_used": {c: PERMITTED[c] for c in cards if c in PERMITTED}}
    print("claims/forbidden:", REPORT["claims"]["status"], hits, unpermitted)


def c_prompts():
    hits = []
    for p in sorted((JOB / "gen/prompts").glob("*.txt")):
        txt = p.read_text().lower()
        for w in ("mario", "nintendo", "luigi", "bowser", "koopa", "goomba", "mushroom kingdom", "peach"):
            if w in txt: hits.append((p.name, w))
        for cid, val in DECK.items():
            if val.lower() in txt and len(val) > 6: hits.append((p.name, f"deck string {cid}"))
    REPORT["prompts"] = {"status": "PASS" if not hits else "FAIL", "hits": hits, "files": [p.name for p in (JOB / "gen/prompts").glob("*.txt")]}
    print("prompts:", REPORT["prompts"]["status"], hits)


def c_frames():
    """Sample first, last, every 0.5 s (2 fps) and ±0.2 s around the three cuts -> contact sheet + keyframes."""
    ts = sorted(set([0.0, 29.9] + [round(i * 0.5, 3) for i in range(60)] + [round(TL[c][0] + d, 3) for c in ("F7", "F9", "F17") for d in (-0.2, 0.2)]))
    d = QA / "frames"; d.mkdir(exist_ok=True)
    files = []
    for t in ts:
        f = d / f"t{t:06.2f}.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", str(FINAL), "-frames:v", "1", str(f)], check=True); files.append((t, f))
    # contact sheet with the safe box drawn
    th = 216; cols = 10; rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (th + 6), rows * (th * 16 // 9 + 26)), (18, 18, 22))
    dr = ImageDraw.Draw(sheet)
    for i, (t, f) in enumerate(files):
        im = Image.open(f).resize((th, th * 16 // 9)); x, y = (i % cols) * (th + 6), (i // cols) * (th * 16 // 9 + 26)
        sheet.paste(im, (x, y))
        s = th / 1080
        dr.rectangle([x + 65 * s, y + 269 * s, x + 1015 * s, y + 1248 * s], outline=(255, 230, 0), width=1)
        dr.text((x + 4, y + th * 16 // 9 + 6), f"{t:.2f}s", fill=(255, 255, 255))
    sheet.save(JOB / "gen/final/CONTACT-SHEET.png")
    # keyframes: one per beat (midpoint), labelled
    kf = []
    for b, (a, e) in TL.items():
        t = round((a + e) / 2, 3); f = d / f"beat_{b}.png"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", str(FINAL), "-frames:v", "1", str(f)], check=True); kf.append((b, t, f))
    th = 300; cols = 6; rows = (len(kf) + cols - 1) // cols
    ks = Image.new("RGB", (cols * (th + 8), rows * (th * 16 // 9 + 30)), (18, 18, 22)); dr = ImageDraw.Draw(ks)
    for i, (b, t, f) in enumerate(kf):
        im = Image.open(f).resize((th, th * 16 // 9)); x, y = (i % cols) * (th + 8), (i // cols) * (th * 16 // 9 + 30)
        ks.paste(im, (x, y)); dr.text((x + 4, y + th * 16 // 9 + 8), f"{b}  {TL[b][0]:.2f}-{TL[b][1]:.2f}s (shown {t:.2f}s)", fill=(255, 255, 255))
    ks.save(JOB / "gen/final/KEYFRAMES.png")
    REPORT["frames"] = {"status": "SAMPLED", "sampled_timestamps": [t for t, _ in files], "count": len(files), "contact_sheet": "gen/final/CONTACT-SHEET.png", "keyframes": "gen/final/KEYFRAMES.png",
                        "text_hygiene_detector": "NOT_RUN (Cloud Vision not authorised); human-eye pass by the independent inspector over qa/frames/*"}
    print("frames:", len(files), "sampled; contact sheet + keyframes written")


def c_loudness():
    r = subprocess.run(["ffmpeg", "-v", "info", "-i", str(FINAL), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    tail = r.stderr[r.stderr.rfind("Summary:"):]
    I = float(re.search(r"I:\s+(-?[\d.]+) LUFS", tail).group(1)); tp = float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", tail).group(1)); lra = float(re.search(r"LRA:\s+(-?[\d.]+) LU", tail).group(1))
    ok = (-15.0 <= I <= -13.0) and tp <= -1.0
    REPORT["loudness"] = {"status": "PASS" if ok else "FAIL", "integrated_lufs": I, "true_peak_dbtp": tp, "lra_lu": lra, "target": "I -14 ±1, TP ≤ -1 (our own target, Stage 2 §2.6)"}
    print("loudness:", REPORT["loudness"]["status"], f"I={I} LUFS TP={tp} dBTP LRA={lra}")


def c_vo():
    m = json.load(open(JOB / "gen/audio/MIX_REPORT.json"))
    REPORT["vo_schedule"] = {"status": m["vo_gate"]["status"], "lines": m["vo_lines"], "gate": m["vo_gate"]}
    print("vo schedule:", m["vo_gate"]["status"], m["vo_lines"])


if __name__ == "__main__":
    c_container(); c_safezone_disjoint(); c_copy_claims(); c_prompts(); c_vo(); c_loudness(); c_frames()
    json.dump(REPORT, open(QA / "QA-REPORT.json", "w"), indent=1, default=str)
    print("report:", QA / "QA-REPORT.json")
