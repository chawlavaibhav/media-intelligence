#!/usr/bin/env python3
"""RES-005 - measure the MAT-AV-MIN clips against what the temporal plan needs.

Nothing here is declared. Every tag is MEASURED from the extracted clip:

  cuts            ffmpeg scene-change detection      -> multi_shot
  on_screen_text  Tesseract over evenly-spaced frames -> on_screen_text (SCREEN ONLY,
                  confirmed by human/agent frame inspection; EVAL-022/023 established
                  that Tesseract is not a reliable exact-text judge, so it is used here
                  only to answer "is there rendered text at all", never what it says)
  motion          mean absolute inter-frame luma difference -> motion
  audio           ffprobe stream presence            -> audio

Cleanliness screens, because a perturbation base must carry no defect except the
injected one:

  freezedetect    pre-existing frozen runs would contaminate freeze-injection recall
  blackdetect     black frames / fades to black
  idet            interlacing, which reads as comb artefacts between frames

Writes qualification-measurements.json and a contact sheet per clip for visual
confirmation of person / product-object tags, which no local tool can assert honestly.

Exit 0 measured · 2 could not run.
"""
import json, os, re, subprocess, sys
from datetime import datetime, timezone

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CLIP = os.path.join(REPO, "resources/corpus/raw/mat-av-min/clips")
SHEET = os.path.join(REPO, "resources/corpus/raw/mat-av-min/contact-sheets")
OUT = os.path.join(REPO, "resources/pre-execution-freeze/mat-av-min")
SCENE_THRESHOLD = 0.30
TEXT_SAMPLES = 20
TEXT_MIN_CONF = 70
TEXT_MIN_CHARS = 3


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(path):
    p = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path])
    d = json.loads(p.stdout)
    v = next(s for s in d["streams"] if s["codec_type"] == "video")
    a = next((s for s in d["streams"] if s["codec_type"] == "audio"), None)
    n, dn = v["avg_frame_rate"].split("/")
    return {"duration_s": round(float(d["format"]["duration"]), 3),
            "width": v["width"], "height": v["height"],
            "fps": round(int(n) / int(dn), 6),
            "nb_frames": int(v["nb_frames"]) if str(v.get("nb_frames", "")).isdigit() else None,
            "audio_present": a is not None,
            "bit_rate_kbps": round(int(d["format"]["bit_rate"]) / 1000) if d["format"].get("bit_rate") else None}


def cuts(path):
    p = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path,
             "-filter_complex", f"select='gt(scene,{SCENE_THRESHOLD})',showinfo", "-f", "null", "-"])
    ts = [round(float(m), 3) for m in re.findall(r"pts_time:([0-9.]+)", p.stderr)]
    return ts


def motion(path):
    """Mean absolute inter-frame luma difference, 0-255. Higher = more movement."""
    p = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path,
             "-filter_complex", "[0:v]tblend=all_mode=difference,signalstats,metadata=print:key=lavfi.signalstats.YAVG",
             "-f", "null", "-"])
    vals = [float(m) for m in re.findall(r"lavfi\.signalstats\.YAVG=([0-9.]+)", p.stderr)]
    if not vals: return None
    vals = vals[1:] or vals
    return {"mean_abs_frame_diff": round(sum(vals) / len(vals), 4),
            "max_abs_frame_diff": round(max(vals), 4),
            "frames_measured": len(vals)}


def freezes(path):
    p = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path,
             "-vf", "freezedetect=n=0.001:d=0.5", "-map", "0:v:0", "-f", "null", "-"])
    return [round(float(m), 3) for m in re.findall(r"freeze_start: ([0-9.]+)", p.stderr)]


def blacks(path):
    p = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path,
             "-vf", "blackdetect=d=0.1:pix_th=0.10", "-map", "0:v:0", "-f", "null", "-"])
    return re.findall(r"black_start:([0-9.]+) black_end:([0-9.]+)", p.stderr)


def interlace(path):
    p = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-vf", "idet", "-f", "null", "-"])
    m = re.search(r"Multi frame detection: TFF:\s*(\d+)\s*BFF:\s*(\d+)\s*Progressive:\s*(\d+)\s*Undetermined:\s*(\d+)", p.stderr)
    if not m: return None
    tff, bff, prog, und = (int(x) for x in m.groups())
    tot = tff + bff + prog + und
    return {"tff": tff, "bff": bff, "progressive": prog, "undetermined": und,
            "interlaced_fraction": round((tff + bff) / tot, 4) if tot else None}


def text_screen(path, dur, workdir):
    os.makedirs(workdir, exist_ok=True)
    hits, per_frame = 0, []
    for i in range(TEXT_SAMPLES):
        t = dur * (i + 0.5) / TEXT_SAMPLES
        png = os.path.join(workdir, f"t{i:02d}.png")
        # Cap the OCR frame at 1920 wide. Tesseract on a 3840x2160 frame took minutes per
        # frame and answers the same presence question; the cap changes runtime, not the answer.
        run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{t:.3f}",
             "-i", path, "-frames:v", "1",
             "-vf", "scale='min(1920,iw)':-2", png])
        if not os.path.exists(png): continue
        p = run(["tesseract", png, "stdout", "--psm", "11", "-l", "eng", "tsv"])
        toks = []
        for line in p.stdout.splitlines()[1:]:
            f = line.split("\t")
            if len(f) < 12: continue
            try: conf = float(f[10])
            except ValueError: continue
            word = f[11].strip()
            if conf >= TEXT_MIN_CONF and len(re.sub(r"[^A-Za-z0-9]", "", word)) >= TEXT_MIN_CHARS:
                toks.append(word)
        per_frame.append({"t": round(t, 3), "confident_tokens": len(toks), "sample": toks[:6]})
        if toks: hits += 1
    return {"frames_sampled": len(per_frame), "frames_with_confident_text": hits,
            "min_confidence": TEXT_MIN_CONF, "min_alnum_chars": TEXT_MIN_CHARS,
            "detail": per_frame}


def contact_sheet(path, dur, dest):
    n = 12
    fps_expr = f"fps=1/{max(dur / n, 0.01):.4f}"
    run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", path,
         "-vf", f"{fps_expr},scale=480:-1,tile=4x3", "-frames:v", "1", dest])


def main():
    if not os.path.isdir(CLIP):
        print("[FAIL] no clips directory", file=sys.stderr); return 2
    os.makedirs(SHEET, exist_ok=True)
    tmp = os.path.join(SHEET, ".frames")
    out = {"generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "task": "RES-005", "scene_threshold": SCENE_THRESHOLD, "clips": {}}
    for f in sorted(os.listdir(CLIP)):
        if not f.endswith(".mp4"): continue
        cid = f[:-4]; p = os.path.join(CLIP, f)
        pr = probe(p)
        c = cuts(p)
        m = {"probe": pr,
             "cut_timestamps_s": c,
             "shot_count_estimate": len(c) + 1,
             "multi_shot_measured": len(c) >= 1,
             "motion": motion(p),
             "pre_existing_freeze_starts_s": freezes(p),
             "black_intervals": blacks(p),
             "interlace": interlace(p),
             "audio_present": pr["audio_present"],
             "on_screen_text_screen": text_screen(p, pr["duration_s"], os.path.join(tmp, cid))}
        contact_sheet(p, pr["duration_s"], os.path.join(SHEET, f"{cid}.jpg"))
        out["clips"][cid] = m
        print(f"{cid}: shots~{m['shot_count_estimate']} motion={m['motion']['mean_abs_frame_diff'] if m['motion'] else '?'} "
              f"text_frames={m['on_screen_text_screen']['frames_with_confident_text']}/{TEXT_SAMPLES} "
              f"freezes={len(m['pre_existing_freeze_starts_s'])} audio={m['audio_present']}", flush=True)
    with open(os.path.join(OUT, "qualification-measurements.json"), "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
    print(f"\nmeasured {len(out['clips'])} clips")
    return 0


if __name__ == "__main__":
    sys.exit(main())
