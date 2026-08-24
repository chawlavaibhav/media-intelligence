#!/usr/bin/env python3
"""RES-001 :: deterministic integrity validation + item manifest builder.

For every media file under resources/corpus/raw/<source_id>/:
  - SHA256, byte size, extension, media type
  - ffprobe: image dimensions, or video dimensions/duration/fps/codec
  - validation_status: ok | undecodable | zero_bytes

No model is involved. Nothing is deleted. Corrupt files are recorded, not removed.
Usage: validate_and_manifest.py <source_id> [<source_id> ...]
"""
import hashlib, json, os, subprocess, sys, csv
from concurrent.futures import ThreadPoolExecutor

RAW = "resources/corpus/raw"
OUT_JSONL = "resources/manifests/corpus-pilot-v0.jsonl"
OUT_CSV = "resources/manifests/corpus-pilot-v0.csv"

VIDEO_EXT = {".mp4", ".webm", ".mkv", ".mov", ".avi"}
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"}

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def probe(p):
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-print_format", "json",
             "-show_streams", "-show_format", p],
            capture_output=True, text=True, timeout=60)
        if r.returncode != 0:
            return None
        return json.loads(r.stdout)
    except Exception:
        return None

def fps_of(stream):
    raw = stream.get("avg_frame_rate") or stream.get("r_frame_rate") or ""
    if "/" in raw:
        n, d = raw.split("/")
        try:
            n, d = float(n), float(d)
            return round(n / d, 4) if d else None
        except ValueError:
            return None
    return None

def build(source_id, path, rel):
    ext = os.path.splitext(path)[1].lower()
    size = os.path.getsize(path)
    mtype = "video" if ext in VIDEO_EXT else "image" if ext in IMAGE_EXT else "other"
    rec = {
        "item_id": f"{source_id}::{rel}",
        "source_id": source_id,
        "original_id": os.path.splitext(os.path.basename(path))[0],
        "relative_path": os.path.join(RAW, source_id, rel),
        "media_type": mtype,
        "extension": ext,
        "bytes": size,
        "sha256": None,
        "width": None, "height": None,
        "duration_s": None, "fps": None, "codec": None,
        "source_split": "source_default",
        "source_labels_ref": None,
        "download_status": "downloaded",
        "validation_status": "unknown",
    }
    if size == 0:
        rec["validation_status"] = "zero_bytes"
        return rec
    rec["sha256"] = sha256(path)
    info = probe(path)
    if not info or not info.get("streams"):
        rec["validation_status"] = "undecodable"
        return rec
    st = next((s for s in info["streams"] if s.get("codec_type") == "video"), info["streams"][0])
    rec["width"] = st.get("width")
    rec["height"] = st.get("height")
    rec["codec"] = st.get("codec_name")
    if mtype == "video":
        dur = info.get("format", {}).get("duration")
        rec["duration_s"] = round(float(dur), 3) if dur else None
        rec["fps"] = fps_of(st)
    rec["validation_status"] = "ok" if rec["width"] else "undecodable"
    return rec

def main(source_ids):
    existing = []
    if os.path.exists(OUT_JSONL):
        with open(OUT_JSONL) as f:
            existing = [json.loads(l) for l in f if l.strip()]
        existing = [r for r in existing if r["source_id"] not in source_ids]

    records = list(existing)
    for sid in source_ids:
        root = os.path.join(RAW, sid)
        files = []
        for dirpath, _, names in os.walk(root):
            for n in names:
                if n.startswith("_") or n.startswith("."):
                    continue
                ext = os.path.splitext(n)[1].lower()
                if ext in VIDEO_EXT or ext in IMAGE_EXT:
                    p = os.path.join(dirpath, n)
                    files.append((p, os.path.relpath(p, root)))
        print(f"[{sid}] validating {len(files)} media files...")
        with ThreadPoolExecutor(max_workers=8) as ex:
            new = list(ex.map(lambda t: build(sid, t[0], t[1]), files))
        ok = sum(1 for r in new if r["validation_status"] == "ok")
        print(f"[{sid}] ok={ok}  problems={len(new)-ok}  bytes={sum(r['bytes'] for r in new):,}")
        records.extend(new)

    records.sort(key=lambda r: (r["source_id"], r["relative_path"]))
    os.makedirs("resources/manifests", exist_ok=True)
    with open(OUT_JSONL, "w") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        w.writeheader()
        w.writerows(records)
    print(f"manifest: {len(records)} items -> {OUT_JSONL} / {OUT_CSV}")

if __name__ == "__main__":
    main(sys.argv[1:])
