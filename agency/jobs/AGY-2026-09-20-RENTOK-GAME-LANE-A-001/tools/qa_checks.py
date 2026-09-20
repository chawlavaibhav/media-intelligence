#!/usr/bin/env python3
"""qa_checks.py — every deterministic (DET) check of the Stage 4 QA plan, as code, over a rendered film.

usage: python3 qa_checks.py <name> [--final]     (name = the render name: gen/<name>.mp4, gen/<name>-layout.jsonl,
                                                   gen/<name>-events.json, qa/<name>/frames)
Prints one line per check with PASS / FAIL / NOT_RUN and evidence; exits 1 on any FAIL. Uses the repo's own gates
(runtime/compositor/gates.py) — never a weaker one-off — plus ffprobe / ffmpeg ebur128.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
JOB = HERE.parent
REPO = JOB.parents[2]
sys.path.insert(0, str(REPO))
from runtime.compositor import gates  # noqa: E402
from runtime.compositor.gates import LayoutRefused  # noqa: E402

SAFE = (65, 288, 888, 1248)
FORBIDDEN = ["guarantee", "100%", "never", "prevent", "recover", "eliminate", "all problems", "every problem", "always",
             "nintendo", "mario", "luigi", "mushroom kingdom", "%"]
RESULTS: list = []


def rec(check: str, status: str, evidence: str):
    RESULTS.append((check, status, evidence)); print(f"{status:7s} {check:34s} {evidence}")


def ffprobe(path: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)],
                         capture_output=True, text=True).stdout
    return json.loads(out)


def count_atoms(data: bytes, fourcc: bytes) -> int:
    """Walk the MP4 box tree (moov → trak → edts) and count boxes of the given type; a byte grep would also match media payload."""
    containers = {b"moov", b"trak", b"edts", b"mdia", b"minf", b"stbl"}
    def walk(start: int, end: int) -> int:
        n = 0; pos = start
        while pos + 8 <= end:
            size = int.from_bytes(data[pos:pos + 4], "big"); typ = data[pos + 4:pos + 8]; hdr = 8
            if size == 1:
                size = int.from_bytes(data[pos + 8:pos + 16], "big"); hdr = 16
            elif size == 0:
                size = end - pos
            if size < hdr:
                break
            if typ == fourcc:
                n += 1
            if typ in containers:
                n += walk(pos + hdr, min(pos + size, end))
            pos += size
        return n
    return walk(0, len(data))


def lum(rgbv) -> float:
    def ch(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgbv[:3]
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def main():
    name = sys.argv[1]; final = "--final" in sys.argv
    mp4 = JOB / f"gen/{name}.mp4"; layout = JOB / f"gen/{name}-layout.jsonl"; events = JOB / f"gen/{name}-events.json"
    deck = json.load(open(JOB / "copy-deck.json")); strings = deck["strings"]; board = json.load(open(JOB / "board.json"))
    frames_dir = JOB / "qa" / name / "frames"

    # ── DET-A7 / DET-A8 container ────────────────────────────────────────────
    p = ffprobe(mp4); v = next(s for s in p["streams"] if s["codec_type"] == "video")
    a = next((s for s in p["streams"] if s["codec_type"] == "audio"), None)
    dur = float(p["format"]["duration"])
    rec("DET-A7 duration 29.5–30.5", "PASS" if 29.5 <= dur <= 30.5 else "FAIL", f"ffprobe duration {dur:.3f} s")
    geom_ok = v["width"] == 1080 and v["height"] == 1920 and v["codec_name"] == "h264" and v.get("profile") == "High" and v["pix_fmt"] == "yuv420p" and v["r_frame_rate"] == "30/1"
    rec("DET-A8 geometry/codec", "PASS" if geom_ok else "FAIL", f"{v['width']}x{v['height']} {v['codec_name']} {v.get('profile')} {v['pix_fmt']} {v['r_frame_rate']} fps")
    size = int(p["format"]["size"]); rec("DET-A8 container/size", "PASS" if p["format"]["format_name"].startswith("mov,mp4") and size < 4e9 else "FAIL", f"{p['format']['format_name']} {size / 1e6:.1f} MB")
    data = mp4.read_bytes(); head = data[:64]; rec("DET-A8 moov first (faststart)", "PASS" if b"moov" in head else "FAIL", f"first 64 bytes contain moov: {b'moov' in head}")
    n_elst = count_atoms(data, b"elst")
    rec("DET-A8 no edit lists (elst)", "PASS" if n_elst == 0 else "FAIL", f"{n_elst} elst atom(s) found by walking the moov/trak/edts boxes (D-1; Stage 2 §2.1)")
    if final:
        a_ok = a is not None and a["codec_name"] == "aac" and a["sample_rate"] == "48000" and int(a["channels"]) == 2
        rec("DET-A8 audio aac 48k stereo", "PASS" if a_ok else "FAIL", f"{(a or {}).get('codec_name')} {(a or {}).get('sample_rate')} ch={(a or {}).get('channels')} br={(a or {}).get('bit_rate')}")
    else:
        rec("DET-A8 audio aac 48k stereo", "NOT_RUN", "animatic is video-only")

    # ── layout log gates: bounds, disjoint, contrast, exact copy ─────────────
    rows = [json.loads(l) for l in open(layout)]
    n_boxes = 0; bounds_fail = []; disjoint_fail = []; contrast_fail = []; copy_fail = []; contrast_min = 99.0
    sampled = {int(re.search(r"f(\d{4})", f.name).group(1)): f for f in frames_dir.glob("f*.png")}
    for row in rows:
        regions = {}
        for b in row["boxes"]:
            n_boxes += 1
            box = b["backing_box"] if b.get("backing") else b["box"]
            try:
                gates.check_text_bounds(box, canvas=(0, 0, 1080, 1920), container=SAFE, id_=f"{row['frame']}:{b['id']}")
            except LayoutRefused as e:
                bounds_fail.append(str(e)[:120])
            regions[b["id"]] = box
            # exact copy: logged text must equal the deck value for its id (partial typing ids are excluded by name)
            if b["kind"] == "text" and not b["id"].endswith("_partial"):
                if strings.get(b["id"]) != b["text"]:
                    copy_fail.append(f"{row['frame']}:{b['id']}={b['text']!r}")
            # contrast: opaque backing → ratio vs backing; no backing → real pixels of the sampled frame if it exists
            if b["kind"] == "text":
                try:
                    if b.get("backing"):
                        r = gates.check_contrast(b["fg"], [], role="body", backing_hex=b["backing"], id_=b["id"])
                    elif row["frame"] in sampled:
                        im = Image.open(sampled[row["frame"]]).convert("RGB")
                        x0, y0, x1, y1 = b["box"]; samples = []
                        for yy in range(y0, y1, 6):
                            for xx in range(x0, x1, 12):
                                px = im.getpixel((xx, yy))
                                # skip the ink itself (text colour) — sample background-ish pixels only
                                if max(abs(px[i] - int(b["fg"].lstrip('#')[i * 2:i * 2 + 2], 16)) for i in range(3)) > 40:
                                    samples.append(lum(px))
                        r = gates.check_contrast(b["fg"], samples or [lum((0, 56, 255))], role="body", id_=b["id"])
                    else:
                        continue
                    contrast_min = min(contrast_min, r["worst_ratio"])
                except LayoutRefused as e:
                    contrast_fail.append(str(e)[:120])
        try:
            gates.check_disjoint(regions, critical=list(regions.keys()), min_gap_px=0)
        except LayoutRefused as e:
            disjoint_fail.append(f"frame {row['frame']} t={row['t']}: {str(e)[:100]}")
    rec("C1 text bounds in safe box", "PASS" if not bounds_fail else "FAIL", f"{n_boxes} boxes over {len(rows)} frames; failures {len(bounds_fail)} {bounds_fail[:2]}")
    rec("C5 disjoint per frame", "PASS" if not disjoint_fail else "FAIL", f"failures {len(disjoint_fail)} {disjoint_fail[:2]}")
    rec("C2 contrast ≥ 4.5 (body)", "PASS" if not contrast_fail else "FAIL", f"min worst ratio {contrast_min:.2f}; failures {len(contrast_fail)} {contrast_fail[:2]}")
    rec("C6 exact copy byte-check", "PASS" if not copy_fail else "FAIL", f"{len(copy_fail)} mismatches {copy_fail[:3]}")

    # ── DET-A11 forbidden claims over deck + every logged text ───────────────
    texts = set(v for k, v in strings.items()) | {b["text"] for row in rows for b in row["boxes"] if b["kind"] == "text"}
    hits = [(t, w) for t in texts for w in FORBIDDEN if w in t.lower()]
    rec("DET-A11 forbidden-claim scan", "PASS" if not hits else "FAIL", f"{len(texts)} distinct strings; hits {hits}")
    chips = [strings[f"CHIP_{i}"] for i in range(1, 6)]
    perm_src = deck["claims_source_map"]; rec("§D claims sourced", "PASS" if all(f"CHIP_{i}" in perm_src for i in range(1, 6)) else "FAIL", f"{chips}")

    # ── mandatory events from the event log and the layout log ───────────────
    ev = json.load(open(events))
    inst = [e for e in ev if e["event"] == "install"]; bursts = [e for e in ev if e["event"] in ("burst", "tag")]
    chipev = [e for e in ev if e["event"] == "chip"]; flag = [e for e in ev if e["event"] == "flag_reached"]
    rec("DET-A4 install event 10–20 s", "PASS" if inst and 10 <= inst[0]["t"] <= 20 else "FAIL", f"install at {[e['t'] for e in inst]}")
    rec("DET-A6 five clears + flag", "PASS" if len({e['obstacle'] for e in bursts}) == 5 and flag else "FAIL", f"clears {sorted({e['obstacle'] for e in bursts})} chips {len(chipev)} flag {[e['t'] for e in flag]}")
    per_frame = {row["frame"]: row for row in rows}
    def present(key, t0, t1):
        return any(any(b["id"] == key for b in per_frame[i]["boxes"]) for i in range(int(t0 * 30), int(t1 * 30)) if i in per_frame)
    labels_ok = all(present(f"OBST_{k}", f["t0"], f["t1"]) for f in board["frames"] for k in [int(m) for m in re.findall(r"OBST_(\d)", " ".join(f["strings"]))])
    rec("DET-A3 five obstacle labels rendered", "PASS" if labels_ok else "FAIL", "each OBST_k present on its board frames (first and second half)")
    rec("DET-A4 cheat strings at F7", "PASS" if present("CHEAT_1", 15.0, 18.0) and present("CHEAT_2", 15.0, 18.0) else "FAIL", "CHEAT_1/CHEAT_2 full strings logged inside F7")
    rec("DET-A5 powered only after 17.4", "PASS" if all(bool(r.get("powered")) == (r["t"] >= 17.4) for r in rows if r["beat"] != "F11") else "FAIL", "layout-log powered flag vs 17.4 s")
    rec("DET-A2 HUD_NAME on gameplay frames", "PASS" if all(any(b["id"] == "HUD_NAME" for b in r["boxes"]) for r in rows if r["beat"] != "F11") else "FAIL", "HUD name box on every non-end-card frame")
    rec("DET-A6 flag before end card", "PASS" if flag and flag[0]["t"] < 27.6 else "FAIL", f"flag {flag[0]['t'] if flag else None} < 27.6")
    end_ok = present("CTA_1", 27.6, 30.0) and present("CTA_2", 27.6, 30.0) and present("URL", 27.6, 30.0) and any(any(b["id"] == "WORDMARK" for b in per_frame[i]["boxes"]) for i in range(int(27.6 * 30), 900) if i in per_frame)
    rec("brand end card strings", "PASS" if end_ok else "FAIL", "CTA_1, CTA_2, URL, WORDMARK logged in F11")

    # ── loudness (final only) ────────────────────────────────────────────────
    if final:
        out = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(mp4), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
        out = out[out.rfind("Integrated loudness:"):]
        il = re.search(r"I:\s+(-?[\d.]+) LUFS", out); tp = re.search(r"Peak:\s+(-?[\d.]+) dBFS", out)
        okl = il and tp and -15.5 <= float(il.group(1)) <= -12.5 and float(tp.group(1)) <= -1.0
        rec("5.5 loudness −14 LUFS ±1.5, TP ≤ −1", "PASS" if okl else "FAIL", f"I={il.group(1) if il else '?'} LUFS, TP={tp.group(1) if tp else '?'} dBTP")
    else:
        rec("5.5 loudness", "NOT_RUN", "animatic has no audio")

    # ── frame sampling artefacts exist ───────────────────────────────────────
    rec("D13 contact sheet + keyframes", "PASS" if (JOB / "qa" / name / "CONTACT-SHEET.png").exists() and (JOB / "qa" / name / "KEYFRAMES.png").exists() else "FAIL", f"{len(sampled)} sampled frames at 2 fps under qa/{name}/frames")
    rec("D1 frame text hygiene", "NOT_RUN", "human-eye pass over the sampled frames (Cloud Vision not authorised); recorded in 05-EXECUTION")

    fails = [r for r in RESULTS if r[1] == "FAIL"]
    json.dump([{"check": c, "status": s, "evidence": e} for c, s, e in RESULTS], open(JOB / "qa" / name / "DET-RESULTS.json", "w"), indent=1, ensure_ascii=False)
    print(f"\n{len(RESULTS)} checks: {len(fails)} FAIL, {sum(1 for r in RESULTS if r[1]=='NOT_RUN')} NOT_RUN")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
