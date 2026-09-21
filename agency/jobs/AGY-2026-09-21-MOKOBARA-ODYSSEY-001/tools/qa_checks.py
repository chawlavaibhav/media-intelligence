#!/usr/bin/env python3
"""qa_checks.py — every deterministic (DET) check over the delivered film, as code. ADAPTED from RentOK v2 tools/qa_checks.py
@ ffefe44b (container / duration / faststart / elst atom-walk / loudness logic kept; game-layout checks dropped). Added: copy-deck
byte-exact vs the composed layout, safe-box containment (runtime/compositor/gates.check_text_bounds), claim scan, 2 fps frame
sampling + contact sheet + one keyframe per beat, frame text hygiene by local tesseract OCR (Cloud Vision not authorised),
ledger/attempt consistency vs the cap. usage: qa_checks.py [final.mp4]. Exit 1 on any FAIL."""
import json, re, subprocess, sys
from pathlib import Path
from PIL import Image
HERE = Path(__file__).resolve().parent; JOB = HERE.parent; REPO = JOB.parents[2]; sys.path.insert(0, str(REPO))
from runtime.compositor import gates  # noqa: E402
SAFE = (65, 288, 888, 1248)
FORBIDDEN = ["indestructible", "waterproof", "lifetime", "guarantee", "best-selling", "#1", "odyssey", "%", "sold out", "limited", "airline", "tsa", "warranty"]
R = []
def rec(c, s, e): R.append((c, s, e)); print(f"{s:7s} {c:36s} {e}")
def ffprobe(p): return json.loads(subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(p)], capture_output=True, text=True).stdout)
def count_atoms(data, fourcc):
    containers = {b"moov", b"trak", b"edts", b"mdia", b"minf", b"stbl"}
    def walk(s, e):
        n = 0; pos = s
        while pos + 8 <= e:
            size = int.from_bytes(data[pos:pos + 4], "big"); typ = data[pos + 4:pos + 8]; hdr = 8
            if size == 1: size = int.from_bytes(data[pos + 8:pos + 16], "big"); hdr = 16
            elif size == 0: size = e - pos
            if size < hdr: break
            if typ == fourcc: n += 1
            if typ in containers: n += walk(pos + hdr, min(pos + size, e))
            pos += size
        return n
    return walk(0, len(data))
mp4 = Path(sys.argv[1]) if len(sys.argv) > 1 else JOB / "gen/final/mokobara-odyssey-9x16-30s.mp4"
p = ffprobe(mp4); v = next(s for s in p["streams"] if s["codec_type"] == "video"); a = next((s for s in p["streams"] if s["codec_type"] == "audio"), None)
dur = float(p["format"]["duration"])
rec("DET-A7 duration 29.5-30.5", "PASS" if 29.5 <= dur <= 30.5 else "FAIL", f"{dur:.3f} s")
geom_ok = v["width"] == 1080 and v["height"] == 1920 and v["codec_name"] == "h264" and v.get("profile") == "High" and v["pix_fmt"] == "yuv420p" and v["r_frame_rate"] in ("24/1", "25/1", "30/1")
rec("DET-A8 geometry/codec", "PASS" if geom_ok else "FAIL", f"{v['width']}x{v['height']} {v['codec_name']} {v.get('profile')} {v['pix_fmt']} {v['r_frame_rate']} fps")
size = int(p["format"]["size"]); rec("DET-A8 container/size", "PASS" if p["format"]["format_name"].startswith("mov,mp4") and size < 4e9 else "FAIL", f"{p['format']['format_name']} {size / 1e6:.1f} MB")
data = mp4.read_bytes(); rec("DET-A8 moov first (faststart)", "PASS" if b"moov" in data[:64] else "FAIL", f"moov in first 64 bytes: {b'moov' in data[:64]}")
n_elst = count_atoms(data, b"elst"); rec("DET-A8 no edit lists (elst)", "PASS" if n_elst == 0 else "FAIL", f"{n_elst} elst atoms by walking moov/trak/edts")
a_ok = a and a["codec_name"] == "aac" and a["sample_rate"] == "48000" and a["channels"] == 2 and int(a.get("bit_rate", 0)) >= 128000
rec("DET-A8 audio aac 48k stereo >=128k", "PASS" if a_ok else "FAIL", f"{a and a['codec_name']} {a and a['sample_rate']} ch={a and a['channels']} br={a and a.get('bit_rate')}")
# loudness
r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(mp4), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
summ = r.stderr[r.stderr.rfind("Integrated loudness:"):]; il = float(re.search(r"I:\s+(-?[\d.]+) LUFS", summ).group(1)); tp = float(re.search(r"Peak:\s+(-?[\d.]+) dBFS", summ).group(1))
rec("DET-A9 loudness -14 LUFS +/-1, TP <= -1", "PASS" if -15 <= il <= -13 and tp <= -1 else "FAIL", f"I={il} LUFS TP={tp} dBTP")
# copy deck byte-exact + safe box
deck = json.load(open(JOB / "copy-deck.json"))["strings"]; lay = json.load(open(JOB / "gen/overlays/layout.json"))
exact = all(lay["strings_composed"][k] == deck[k] for k in ("product_line", "tagline", "cta"))
rec("DET-B1 copy deck byte-exact", "PASS" if exact else "FAIL", f"composed {lay['strings_composed']}")
import hashlib
wm_ok = lay["wordmark_sha256"] == hashlib.sha256(open(JOB / deck["wordmark_asset"], "rb").read()).hexdigest()
rec("DET-B2 wordmark = the site's asset", "PASS" if wm_ok else "FAIL", f"sha256 {lay['wordmark_sha256'][:12]}… of {deck['wordmark_asset']}")
bad = []
for it in lay["items"]:
    try: gates.check_text_bounds(tuple(it["box"]), canvas=(0, 0, 1080, 1920), container=SAFE, id_=it["id"])
    except Exception as e: bad.append(f"{it['id']}: {e}")
rec("DET-B3 all text/logo boxes inside safe box", "PASS" if not bad else "FAIL", f"{len(lay['items'])} boxes vs {SAFE}; {bad or 'none outside'}")
hits = [w for w in FORBIDDEN for s in (deck["product_line"], deck["tagline"], deck["cta"]) if w in s.lower()]
rec("DET-B4 claim scan on composed strings", "PASS" if not hits else "FAIL", f"forbidden hits: {hits or 'none'}")
# frames 2 fps + contact + keyframes
qd = JOB / "qa/final"; fr = qd / "frames"; fr.mkdir(parents=True, exist_ok=True)
for f in fr.glob("*"): f.unlink()
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf", "fps=2", "-q:v", "3", str(fr / "f%03d.jpg")], check=True)
frames = sorted(fr.glob("*.jpg")); rec("DET-C1 frames sampled at 2 fps", "PASS" if 58 <= len(frames) <= 62 else "FAIL", f"{len(frames)} frames -> {fr}")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(mp4), "-vf", "fps=2,scale=180:-1,tile=10x6", "-frames:v", "1", str(qd / "contact.jpg")], check=True)
board = json.load(open(JOB / "board.json")); kf = []
for b in board["beats"]:
    t = (b["t_in"] + b["t_out"]) / 2; out = qd / f"keyframe-beat{b['n']}-{t:.1f}s.jpg"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t}", "-i", str(mp4), "-frames:v", "1", str(out)], check=True); kf.append(out.name)
rec("DET-C2 one keyframe per beat", "PASS" if len(kf) == len(board["beats"]) else "FAIL", ", ".join(kf))
# text hygiene by local OCR: generated segments (t < 27.4) must carry no readable lettering except the super window (5.0-7.5: 'mokobara')
sup = json.load(open(JOB / "copy-deck.json"))["placements"]["wordmark_super"]; flagged = []
for f in frames:
    t = (int(f.stem[1:]) - 1) / 2.0
    if t >= 27.4: continue
    txt = subprocess.run(["tesseract", str(f), "-", "--psm", "11"], capture_output=True, text=True).stdout
    toks = [w for w in re.findall(r"[A-Za-z]{4,}", txt)]
    if sup["t_in"] <= t < sup["t_out"]: toks = [w for w in toks if w.lower() not in ("mokobara",)]
    if toks: flagged.append((t, toks[:6]))
rec("DET-D1 frame text hygiene (tesseract)", "PASS" if not flagged else "FLAG", f"{len(flagged)} frames with OCR tokens (LJ to confirm by eye): {flagged[:8]}")
# ledger / attempts
att = [json.loads(l) for l in (JOB / "gen/ATTEMPTS.jsonl").read_text().splitlines() if l.strip()]
led = [json.loads(l) for l in (JOB / "gen/LEDGER.jsonl").read_text().splitlines() if l.strip()]
reserved = sum(l.get("reserved_usd", 0) for l in led if l.get("status") == "reserved")
settled = {l["attempt_id"] for l in led if l.get("status") != "reserved"}
rec("DET-E1 every attempt reserved then settled", "PASS" if all(x["attempt_id"] in settled for x in att) else "FAIL", f"{len(att)} attempts, {len(settled)} settled, USD {reserved:.3f} reserved of 12.00")
rec("DET-E2 cap not exceeded", "PASS" if reserved <= 12.0 else "FAIL", f"USD {reserved:.3f} <= 12.00; failed calls counted: {sum(1 for x in att if x['status'] != 'ok')}")
rec("LJ generated speech in native audio", "NOT_RUN", "human ear over the whole file; prompts forbade speech; no speech heard on the producer's listen")
json.dump([{"check": c, "status": s, "evidence": e} for c, s, e in R], open(qd / "qa-results.json", "w"), indent=1)
sys.exit(1 if any(s == "FAIL" for _, s, _ in R) else 0)
