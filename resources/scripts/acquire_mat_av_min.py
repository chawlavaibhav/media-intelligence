#!/usr/bin/env python3
"""RES-005 - bounded acquisition of the MAT-AV-MIN temporal perturbation base.

Reads resources/pre-execution-freeze/mat-av-min/CANDIDATE-SPEC-v1.yaml, retrieves each
source work from its declared retrieval authority, fingerprints what was actually
retrieved, cuts one clip per work, and fingerprints the clip.

It asserts NOTHING about content. Visual tags are measured by
qualify_mat_av_min.py from the extracted clips, never declared here.

Zero paid calls. No account, form, login, terms acceptance or payment.

Exit 0 all candidates retrieved · 1 one or more failed · 2 could not run.
"""
import hashlib, json, os, subprocess, sys, time, urllib.parse, urllib.request, zipfile
from datetime import datetime, timezone

try:
    import yaml
except ImportError:
    print("[FAIL] PyYAML not available", file=sys.stderr); sys.exit(2)

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPEC = os.path.join(REPO, "resources/pre-execution-freeze/mat-av-min/CANDIDATE-SPEC-v1.yaml")
RAW  = os.path.join(REPO, "resources/corpus/raw/mat-av-min")
ORIG = os.path.join(RAW, "originals")
CLIP = os.path.join(RAW, "clips")
OUT  = os.path.join(REPO, "resources/pre-execution-freeze/mat-av-min")
UA   = "media-intelligence-research/1.0 (contact: vaibhav@wherehouse.io) RES-005 bounded evaluation acquisition"
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
RATE_LIMIT_S = 1.0


def now(): return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(chunk), b""):
            h.update(b)
    return h.hexdigest()


def quote_url(u):
    p = urllib.parse.urlsplit(u)
    # safe="/%" so an already-percent-encoded path (as returned by the Commons API)
    # is not double-encoded into a 404.
    return urllib.parse.urlunsplit((p.scheme, p.netloc, urllib.parse.quote(p.path, safe="/%"), p.query, ""))


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)


def commons_imageinfo(title):
    """Resolve a Commons file to its direct URL plus the licence facts the file page states."""
    q = urllib.parse.urlencode({
        "action": "query", "format": "json", "prop": "imageinfo",
        "iiprop": "url|size|mime|sha1|extmetadata|user|timestamp", "titles": title})
    d = fetch_json(f"{COMMONS_API}?{q}")
    page = list(d["query"]["pages"].values())[0]
    if "imageinfo" not in page:
        raise RuntimeError(f"Commons file not found: {title}")
    ii = page["imageinfo"][0]
    em = ii.get("extmetadata", {})
    def g(k):
        import re, html as H
        v = em.get(k, {}).get("value")
        if v is None: return None
        return " ".join(H.unescape(re.sub(r"<[^>]+>", " ", str(v))).split())
    return {
        "direct_url": ii["url"].split("?")[0],
        "file_page": ii["descriptionurl"],
        "remote_bytes": ii["size"], "remote_sha1": ii.get("sha1"),
        "mime": ii.get("mime"), "uploader": ii.get("user"), "upload_timestamp": ii.get("timestamp"),
        "licence_short_name": g("LicenseShortName"), "licence_id": g("License"),
        "usage_terms": g("UsageTerms"), "artist": g("Artist"),
        "credit": (g("Credit") or "")[:400], "restrictions": g("Restrictions"),
        "date_original": g("DateTimeOriginal"),
    }


def download(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return {"reused_existing_local_file": True, "http_status": None, "headers": {}}
    req = urllib.request.Request(quote_url(url), headers={"User-Agent": UA})
    tmp = dest + ".part"
    with urllib.request.urlopen(req, timeout=300) as r, open(tmp, "wb") as f:
        hdrs = {k.lower(): v for k, v in r.headers.items()
                if k.lower() in ("content-length", "content-type", "last-modified", "etag")}
        status = r.status
        while True:
            b = r.read(1 << 20)
            if not b: break
            f.write(b)
    os.replace(tmp, dest)
    return {"reused_existing_local_file": False, "http_status": status, "headers": hdrs}


def ffprobe(path):
    p = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path],
        capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {p.stderr.strip()[:300]}")
    d = json.loads(p.stdout)
    v = next((s for s in d["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in d["streams"] if s["codec_type"] == "audio"), None)
    def rate(x):
        try:
            n, dn = x.split("/"); return round(int(n) / int(dn), 6) if int(dn) else None
        except Exception: return None
    return {
        "duration_s": round(float(d["format"]["duration"]), 3) if d["format"].get("duration") else None,
        "bytes": int(d["format"]["size"]),
        "format_name": d["format"].get("format_name"),
        "video_codec": v and v.get("codec_name"),
        "width": v and v.get("width"), "height": v and v.get("height"),
        "avg_fps": v and rate(v.get("avg_frame_rate", "0/0")),
        "r_fps": v and rate(v.get("r_frame_rate", "0/0")),
        "pix_fmt": v and v.get("pix_fmt"),
        "nb_video_frames": v and (int(v["nb_frames"]) if str(v.get("nb_frames", "")).isdigit() else None),
        "audio_present": a is not None,
        "audio_codec": a and a.get("codec_name"),
        "audio_channels": a and a.get("channels"),
        "audio_sample_rate": a and a.get("sample_rate"),
    }



STANDARD_RATES = [23.976, 24.0, 25.0, 29.97, 30.0, 50.0, 59.94, 60.0]


def measured_fps(src, start, seconds):
    """Count real frames inside the clip window instead of trusting the declared rate.

    A container can advertise a nominal rate that is only a timebase. One candidate
    (a VP8 WebM) declared 600 fps while carrying 30 real frames per second; cutting at
    the declared rate produced a clip in which every frame was duplicated twenty times.
    For a FREEZE-detection base that is fatal - the clip would already be nothing but
    freezes - so the rate is measured, not read.
    """
    p = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames",
         "-read_intervals", f"{start}%+{seconds}",
         "-show_entries", "stream=nb_read_frames", "-of", "default=nw=1:nk=1", src],
        capture_output=True, text=True)
    try:
        n = int(p.stdout.strip().splitlines()[0])
    except Exception:
        return None, None
    raw = n / float(seconds)
    snapped = min(STANDARD_RATES, key=lambda r: abs(r - raw))
    if abs(snapped - raw) / max(raw, 1e-9) <= 0.02:
        return snapped, raw
    return round(raw, 6), raw


def unzip_member(zpath, hint, into):
    with zipfile.ZipFile(zpath) as z:
        names = [n for n in z.namelist() if not n.endswith("/")]
        pick = next((n for n in names if os.path.basename(n) == hint), None) \
            or next((n for n in names if n.lower().endswith((".mp4", ".mkv", ".mov", ".avi", ".webm"))), None)
        if pick is None:
            raise RuntimeError(f"no media member in {zpath}: {names[:5]}")
        dest = os.path.join(into, os.path.basename(pick))
        if not (os.path.exists(dest) and os.path.getsize(dest) > 0):
            with z.open(pick) as src, open(dest, "wb") as f:
                while True:
                    b = src.read(1 << 20)
                    if not b: break
                    f.write(b)
        return pick, dest


def cut(src, dest, start, seconds, fps):
    """Frame-accurate re-encode. Stream copy would snap to keyframes, and the
    perturbation plan injects defects at exact frame indices."""
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
           "-ss", start, "-i", src, "-t", str(seconds),
           "-map", "0:v:0", "-c:v", "libx264", "-crf", "12", "-preset", "slow",
           "-pix_fmt", "yuv420p", "-vsync", "cfr", "-r", str(fps),
           "-x264-params", "keyint=1000000:scenecut=0"]
    probe = ffprobe(src)
    if probe["audio_present"]:
        cmd += ["-map", "0:a:0", "-c:a", "aac", "-b:a", "320k", "-ar", "48000"]
    cmd += ["-movflags", "+faststart", dest]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"ffmpeg cut failed: {p.stderr.strip()[:400]}")
    return " ".join(cmd)


def main():
    """--only MAVM-05,MAVM-09 re-runs just those candidates and merges them back into the
    existing acquisition record, so a revised window does not force a full re-encode."""
    only = None
    if "--only" in sys.argv:
        only = {x.strip() for x in sys.argv[sys.argv.index("--only") + 1].split(",") if x.strip()}
    spec = yaml.safe_load(open(SPEC))
    target = float(spec["meta"]["clip_target_seconds"])
    os.makedirs(ORIG, exist_ok=True); os.makedirs(CLIP, exist_ok=True)
    records, failures = [], []

    previous = {}
    if only and os.path.exists(os.path.join(OUT, "acquisition-record.json")):
        prev = json.load(open(os.path.join(OUT, "acquisition-record.json")))
        previous = {r["id"]: r for r in prev["records"]}

    for c in spec["candidates"]:
        cid = c["id"]
        if only and cid not in only:
            if cid in previous:
                records.append(previous[cid])
                if previous[cid]["status"] != "acquired":
                    failures.append(cid)
            continue
        print(f"[{cid}] {c['work'][:60]}", flush=True)
        rec = {"id": cid, "work": c["work"], "creator_publisher": c["creator"],
               "licence_declared_in_spec": c["licence"],
               "licence_authority_url": c["licence_authority"],
               "retrieval_authority": c["retrieval_authority"],
               "retrieval_date_utc": now(), "status": "pending"}
        for k in ("licence_quote", "attribution_required", "rights_note", "nasa_id",
                  "selection_reason", "commons_title"):
            if c.get(k): rec[k] = c[k]
        try:
            # 1. resolve URL (+ live licence readback for Commons-hosted works)
            if c.get("commons_title"):
                info = commons_imageinfo(c["commons_title"])
                url = info["direct_url"]
                rec["commons_readback"] = info
                rec["licence_verified_at_source"] = info["licence_short_name"]
                rec["source_url"] = info["file_page"]
                rec["direct_media_url"] = url
                time.sleep(RATE_LIMIT_S)
            else:
                url = c["url"]
                rec["source_url"] = url
                rec["direct_media_url"] = url
                rec["licence_verified_at_source"] = c["licence"]

            # 2. retrieve
            fname = os.path.basename(urllib.parse.urlsplit(url).path) or f"{cid}.bin"
            fname = urllib.parse.unquote(fname).replace("/", "_")
            dl = os.path.join(ORIG, f"{cid}__{fname}")
            meta = download(url, dl)
            rec["retrieved_file_name"] = os.path.basename(dl)
            rec["retrieved_file_bytes"] = os.path.getsize(dl)
            rec["retrieved_file_sha256"] = sha256(dl)
            rec["http_response_headers"] = meta["headers"]
            rec["reused_existing_local_file"] = meta["reused_existing_local_file"]
            time.sleep(RATE_LIMIT_S)

            # 3. unwrap container if the publisher ships a zip
            transforms = []
            media = dl
            if c.get("container") == "zip":
                member, media = unzip_member(dl, c.get("member_hint"), ORIG)
                transforms.append(f"extracted member '{member}' from publisher-supplied zip archive")
                rec["zip_member"] = member
                rec["source_media_sha256"] = sha256(media)
                rec["source_media_bytes"] = os.path.getsize(media)
            else:
                rec["source_media_sha256"] = rec["retrieved_file_sha256"]
                rec["source_media_bytes"] = rec["retrieved_file_bytes"]

            # 4. probe the source work
            rec["source_probe"] = ffprobe(media)

            # 5. cut one clip at the MEASURED frame rate
            declared = rec["source_probe"]["r_fps"] or rec["source_probe"]["avg_fps"]
            snapped, raw = measured_fps(media, c["clip_start"], target)
            rec["frame_rate"] = {"declared_by_container": declared,
                                 "measured_raw": round(raw, 6) if raw else None,
                                 "measured_snapped": snapped}
            # The declared rate wins when the measurement CORROBORATES it - counting frames
            # inside a window has boundary effects of a frame or two, and a 24.000 source must
            # not be re-timed to 23.976 on that evidence. The measurement's job is to catch a
            # declared rate that is grossly wrong, not to fine-tune a correct one.
            if raw is None:
                fps = declared or 25
                rec["frame_rate"]["note"] = "measurement failed; fell back to declared rate"
            elif declared and abs(declared - raw) / max(declared, 1e-9) <= 0.05:
                fps = declared
                rec["frame_rate"]["note"] = "measurement corroborates the declared rate"
            else:
                fps = snapped
                rec["frame_rate"]["note"] = (
                    f"container declared {declared} fps but the clip window carries {raw:.3f} real "
                    f"fps; cut at {fps} to avoid fabricated duplicate frames")
            rec["frame_rate"]["used_for_cut"] = fps
            clip = os.path.join(CLIP, f"{cid}.mp4")
            cmdline = cut(media, clip, c["clip_start"], target, fps)
            transforms.append(
                f"cut {target}s from {c['clip_start']}; re-encoded H.264 CRF 12 preset slow "
                f"yuv420p CFR {fps}fps (MEASURED, not the container's declared rate), "
                f"single-keyframe GOP (scenecut disabled) for frame-exact indexing; "
                f"audio to AAC 320k 48kHz where present")
            rec["clip_relative_path"] = os.path.relpath(clip, REPO)
            rec["clip_sha256"] = sha256(clip)
            rec["clip_probe"] = ffprobe(clip)
            rec["transformations_from_original"] = transforms
            rec["ffmpeg_command"] = cmdline
            rec["status"] = "acquired"
            print(f"      -> {rec['clip_probe']['width']}x{rec['clip_probe']['height']} "
                  f"{rec['clip_probe']['duration_s']}s fps={rec['clip_probe']['avg_fps']} "
                  f"audio={rec['clip_probe']['audio_present']}", flush=True)
        except Exception as e:
            rec["status"] = "failed"; rec["failure_reason"] = f"{type(e).__name__}: {e}"
            failures.append(cid); print(f"      !! {rec['failure_reason'][:200]}", flush=True)
        records.append(rec)

    payload = {"generated_utc": now(), "task": "RES-005", "spec_version": spec["meta"]["spec_version"],
               "clip_target_seconds": target,
               "tool_versions": {
                   "ffmpeg": subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
                             .stdout.splitlines()[0],
                   "python": sys.version.split()[0]},
               "acquired": sum(1 for r in records if r["status"] == "acquired"),
               "failed": failures, "records": records}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "acquisition-record.json"), "w") as f:
        json.dump(payload, f, indent=1, ensure_ascii=False)
    print(f"\nacquired {payload['acquired']}/12  failed={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
