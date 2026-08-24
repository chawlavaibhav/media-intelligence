#!/usr/bin/env python3
"""RES-002 :: src_indicstr12_devanagari :: IndicSTR12 Devanagari subset, member-level.

Official : https://cvit.iiit.ac.in/research/projects/cvit-projects/indicstr  (CVIT, IIIT Hyderabad)
Archive  : https://cvit.iiit.ac.in/images/datasets/IndicSTR12/real.zip  (1,382,967,649 bytes)
Access   : public direct link, no login/form. Host answers HTTP 206 so member-level range
           access works. robots.txt disallows Joomla system paths (/media/, /templates/, ...)
           but NOT /images/datasets/.
Licence  : NOT STATED anywhere on the project page -> recorded not_stated / not_verified.
           Acquired for internal research/evaluation only under Resources charter policy.
Selection: the two Devanagari-script languages the distributor separates - hindi and marathi -
           plus their *_gt.txt ground-truth files. Content-blind: chosen by script, never by
           what a sign says or how legible it looks.
Note     : the synthetic companion (synthetic.tar.gz, 62,692,393,572 bytes) is deliberately NOT
           acquired. RES-002 states clean synthetic text alone is insufficient for calibration,
           and it is 62 GB.
Retention: only the selected members are kept. The 1.38 GB archive is never written to disk,
           so there is deliberately no full-archive hash.
"""
import hashlib, json, os, struct, subprocess, sys, time, zipfile, zlib
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from remote_zip import HTTPRangeFile, supports_range

URL = "https://cvit.iiit.ac.in/images/datasets/IndicSTR12/real.zip"
SRC = "src_indicstr12_devanagari"
DEST = f"resources/corpus/raw/{SRC}"
DEVANAGARI_LANGS = ("hindi", "marathi")
FREE_FLOOR_GB = 12

def free_gb():
    s = os.statvfs("."); return s.f_bavail * s.f_frsize / 1e9

def main():
    os.makedirs(DEST, exist_ok=True)
    assert supports_range(URL), "host does not honour Range; STOP per RES-002 priority order"
    f = HTTPRangeFile(URL); z = zipfile.ZipFile(f)
    infos = [i for i in z.infolist() if not i.is_dir() and "__MACOSX" not in i.filename
             and not i.filename.split("/")[-1].startswith("._")]
    index_cost = f.bytes_fetched
    sel = [i for i in sorted(infos, key=lambda x: x.filename)
           if len(i.filename.split("/")) > 2 and i.filename.split("/")[1] in DEVANAGARI_LANGS]
    total = sum(i.file_size for i in sel)
    print(f"[{SRC}] remote {f.size:,} bytes, {len(infos):,} real members; "
          f"index cost {index_cost/1e6:.1f} MB in {f.requests} requests")
    print(f"[{SRC}] selected {len(sel)} Devanagari members ({total/1e6:.1f} MB)")
    if free_gb() - total/1e9 < FREE_FLOOR_GB:
        sys.exit(f"STOP: would breach the {FREE_FLOOR_GB} GB free-disk floor")

    stats = {"bytes": 0}
    def fetch(i):
        out = os.path.join(DEST, i.filename.replace("/", "__"))
        if os.path.exists(out) and os.path.getsize(out) == i.file_size:
            return out, i, 0
        span = 30 + len(i.filename.encode()) + 4096 + i.compress_size
        # --http1.1: this host intermittently returns "HTTP2 framing layer" errors under
        # concurrent range requests. Forcing HTTP/1.1 and keeping concurrency low is the
        # polite fix - we retry rather than hammer.
        for attempt in range(4):
            r = subprocess.run(["curl", "-sS", "-L", "--http1.1", "--max-time", "600",
                                "--retry", "3", "--retry-delay", "2",
                                "-r", f"{i.header_offset}-{min(i.header_offset+span, f.size)-1}", URL],
                               capture_output=True)
            if r.returncode == 0 and r.stdout[:4] == b"PK\x03\x04":
                break
            time.sleep(1 + attempt)
        else:
            raise IOError(f"range fetch failed for {i.filename}: {r.stderr.decode()[:160]}")
        buf = r.stdout
        if buf[:4] != b"PK\x03\x04": raise IOError(f"bad local header {i.filename}")
        n_len, e_len = struct.unpack("<HH", buf[26:30])
        comp = buf[30+n_len+e_len : 30+n_len+e_len+i.compress_size]
        data = comp if i.compress_type == zipfile.ZIP_STORED else zlib.decompressobj(-15).decompress(comp)
        if len(data) != i.file_size: raise IOError(f"size mismatch {i.filename}")
        open(out, "wb").write(data)
        return out, i, len(buf)

    man, done = [], 0
    with ThreadPoolExecutor(max_workers=2) as ex:
        for out, i, got in ex.map(fetch, sel):
            stats["bytes"] += got
            man.append({"member": i.filename, "bytes": i.file_size,
                        "sha256": hashlib.sha256(open(out,"rb").read()).hexdigest(),
                        "language": i.filename.split("/")[1]})
            done += 1
            if done % 500 == 0: print(f"  ...{done}/{len(sel)}", flush=True)

    json.dump({"source_id": SRC, "official_url": URL,
               "remote_archive_bytes": f.size, "remote_member_count": len(infos),
               "full_archive_downloaded": False, "full_archive_sha256": None,
               "full_archive_sha256_note": "deliberately absent - archive never downloaded",
               "selection_rule": "all members under the distributor's hindi/ and marathi/ folders (the two Devanagari-script languages), images and *_gt.txt; content-blind",
               "selected_count": len(sel), "selected_bytes": total,
               "index_bytes": index_cost,
               "bytes_transferred_total": index_cost + stats["bytes"],
               "items": man}, open(f"{DEST}/_transient_acquisition.json","w"), indent=1)
    open(f"{DEST}/_all_members.txt","w").write("\n".join(sorted(i.filename for i in infos))+"\n")
    moved = index_cost + stats["bytes"]
    print(f"[{SRC}] done. transferred {moved/1e6:.0f} MB of a {f.size/1e9:.2f} GB archive "
          f"({100*moved/f.size:.1f}%)  free now {free_gb():.1f} GB")

if __name__ == "__main__":
    main()
