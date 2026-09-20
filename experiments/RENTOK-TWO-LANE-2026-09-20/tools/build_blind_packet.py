#!/usr/bin/env python3
"""Build the anonymised blind packet: copy the two lane finals as video-X / video-Y with a random mapping,
seal the mapping (sha256 published, mapping file kept out of the packet the customer sees), and write the packet README.
Run from experiments/RENTOK-TWO-LANE-2026-09-20/. USD 0."""
import hashlib, json, secrets, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
P = Path("/Users/vaibhavchawla/Vaibhav_Personal_Projects")
LANES = {
    "A": P / "media-intelligence-rentok-lane-a/agency/jobs/AGY-2026-09-20-RENTOK-GAME-LANE-A-001/gen/final/rentok-game-lane-a-9x16-30s.mp4",
    "B": P / "media-intelligence-rentok-lane-b/agency/jobs/AGY-2026-09-20-RENTOK-GAME-LANE-B-001/gen/final/rentok-game-lane-b-9x16-30s.mp4",
}
OUT = HERE / "05-BLIND-PACKET"
SEALED = HERE / "05-BLIND-PACKET-SEALED"   # not shown to the customer until verdicts are recorded

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def probe(p):
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration:stream=codec_name,width,height","-of","json",str(p)],capture_output=True,text=True)
    return json.loads(r.stdout)

OUT.mkdir(exist_ok=True); SEALED.mkdir(exist_ok=True)
flip = secrets.randbelow(2)
mapping = {"X": "A", "Y": "B"} if flip == 0 else {"X": "B", "Y": "A"}
now = datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
rec = {"sealed_utc": now, "mapping": mapping, "sources": {}}
for label, lane in mapping.items():
    src = LANES[lane]
    if not src.exists(): sys.exit(f"missing {src}")
    dst = OUT / f"video-{label}.mp4"
    shutil.copyfile(src, dst)
    # strip container metadata that could hint at the lane (title tags etc.), keep streams as-is
    tmp = OUT / f"video-{label}.tmp.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-i",str(dst),"-map_metadata","-1","-c","copy","-movflags","+faststart",str(tmp)],check=True)
    tmp.replace(dst)
    rec["sources"][label] = {"lane": lane, "source_path": str(src), "source_sha256": sha(src), "packet_sha256": sha(dst), "probe": probe(dst)}
(SEALED / "MAPPING.json").write_text(json.dumps(rec, indent=2))
seal = sha(SEALED / "MAPPING.json")
(OUT / "SEAL.txt").write_text(f"mapping sealed {now}\nsha256(MAPPING.json) = {seal}\nThe mapping file is held outside this folder until both verdicts are recorded verbatim.\n")
(OUT / "SHA256SUMS.txt").write_text("".join(f"{sha(OUT/f)}  {f}\n" for f in ("video-X.mp4","video-Y.mp4")))
print("packet built; mapping sealed", seal[:16])
for label in ("X","Y"):
    print(label, rec["sources"][label]["packet_sha256"][:16], rec["sources"][label]["probe"]["format"]["duration"])
