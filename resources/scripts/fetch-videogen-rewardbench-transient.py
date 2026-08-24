#!/usr/bin/env python3
"""RES-002 :: src_videogen_rewardbench :: bounded member-level acquisition WITHOUT
downloading the 13.42 GB archive.

Official : https://huggingface.co/datasets/KlingTeam/VideoGen-RewardBench
           (KwaiVGI/VideoGen-RewardBench 307-redirects here)
Licence  : dataset card states apache-2.0. Underlying media are outputs of 12 third-party
           generators; the publisher's authority to licence those outputs is NOT verified.
Access   : public, anonymous, ungated. Host answers HTTP 206, so range access is legitimate
           normal client behaviour, not evasion.

METHOD — why this is different from RES-001
  RES-001 marked this source `too_large_for_pilot`: 13.42 GB in a single zip, and taking a
  subset seemed to require downloading all of it. That was wrong. A zip keeps its index at the
  END of the file, so a few range requests read the whole member list, and each member can then
  be fetched by its own byte range. Transfer = index + selected members only.

SELECTION — deterministic, content-blind, diversity-preserving
  The point of this source is that it spans 12 different video generators. Taking "the first N
  files" would over-represent whichever generator sorts first. So: equal count per
  distributor-defined generator folder, files taken in sorted order within each. Nothing is
  chosen for what the video shows or how good it looks.

RETENTION
  Keep the selected members, their hashes, the full remote member list, and the selection rule.
  The archive is never written to disk, so there is deliberately NO full-archive hash — a hash
  of a file we never downloaded would be fabricated. Remote size + URL + this script are the
  reproduction record.
"""
import hashlib, json, os, struct, sys, zipfile, zlib, subprocess
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from remote_zip import HTTPRangeFile, supports_range

URL = "https://huggingface.co/datasets/KlingTeam/VideoGen-RewardBench/resolve/main/videos.zip"
CSV = "https://huggingface.co/datasets/KlingTeam/VideoGen-RewardBench/resolve/main/videogen-rewardbench.csv"
SRC = "src_videogen_rewardbench"
DEST = f"resources/corpus/raw/{SRC}"
PER_GENERATOR = int(os.environ.get("PER_GENERATOR", "24"))
BYTE_BUDGET = int(os.environ.get("BYTE_BUDGET", str(1_100_000_000)))
FREE_FLOOR_GB = 12

def free_gb():
    s = os.statvfs(".")
    return s.f_bavail * s.f_frsize / 1e9

def main():
    os.makedirs(DEST, exist_ok=True)
    assert supports_range(URL), "host does not honour Range; STOP per RES-002 priority order"

    f = HTTPRangeFile(URL)
    z = zipfile.ZipFile(f)
    infos = [i for i in z.infolist() if not i.is_dir()]
    index_cost = f.bytes_fetched
    print(f"[{SRC}] remote archive {f.size:,} bytes; {len(infos):,} members")
    print(f"[{SRC}] index read via {f.requests} range requests, {index_cost/1e6:.1f} MB "
          f"({100*index_cost/f.size:.4f}% of archive)")

    bygen = {}
    for i in sorted(infos, key=lambda x: x.filename):
        gen = i.filename.split("/")[1] if len(i.filename.split("/")) > 2 else "_root"
        bygen.setdefault(gen, []).append(i)

    selected, total = [], 0
    for gen in sorted(bygen):
        for i in bygen[gen][:PER_GENERATOR]:
            if total + i.file_size > BYTE_BUDGET:
                continue
            selected.append(i); total += i.file_size
    print(f"[{SRC}] selection: {PER_GENERATOR}/generator across {len(bygen)} generators "
          f"-> {len(selected)} files, {total/1e9:.2f} GB")

    if free_gb() - total/1e9 < FREE_FLOOR_GB:
        sys.exit(f"STOP: would breach the {FREE_FLOOR_GB} GB free-disk floor")

    subprocess.run(["curl", "-sS", "-L", "--retry", "3", "-o", f"{DEST}/videogen-rewardbench.csv", CSV], check=True)

    # ---- one range request per member ----------------------------------------
    # A zip member is stored as: local header (30 bytes + name + extra) then the
    # compressed bytes. Reading the central directory already told us where each
    # member starts and how many compressed bytes it has, so we can pull the whole
    # member in a SINGLE range request and inflate it locally. Letting zipfile do
    # the reading instead issues dozens of tiny requests per member, which is
    # roughly two orders of magnitude slower over the network.
    LOCAL_HDR_MAX = 30 + 65535 + 65535
    stats = {"bytes": 0, "requests": 0}

    def fetch_member(i):
        out = os.path.join(DEST, os.path.basename(i.filename))
        if os.path.exists(out) and os.path.getsize(out) == i.file_size:
            return out, i, 0
        span = 30 + len(i.filename.encode()) + 4096 + i.compress_size
        start = i.header_offset
        end = min(start + span, f.size) - 1
        r = subprocess.run(["curl", "-sS", "-L", "--max-time", "900", "--retry", "3",
                            "-r", f"{start}-{end}", URL], capture_output=True)
        if r.returncode != 0:
            raise IOError(f"range fetch failed for {i.filename}: {r.stderr.decode()[:160]}")
        buf = r.stdout
        if buf[:4] != b"PK\x03\x04":
            raise IOError(f"bad local header for {i.filename}")
        n_len, e_len = struct.unpack("<HH", buf[26:30])
        off = 30 + n_len + e_len
        comp = buf[off:off + i.compress_size]
        if len(comp) < i.compress_size:
            raise IOError(f"short read for {i.filename}: {len(comp)}/{i.compress_size}")
        data = comp if i.compress_type == zipfile.ZIP_STORED else zlib.decompressobj(-15).decompress(comp)
        if len(data) != i.file_size:
            raise IOError(f"size mismatch for {i.filename}: {len(data)}/{i.file_size}")
        with open(out, "wb") as fh:
            fh.write(data)
        return out, i, len(buf)

    manifest = []
    done = 0
    with ThreadPoolExecutor(max_workers=4) as ex:
        for out, i, got in ex.map(fetch_member, selected):
            stats["bytes"] += got; stats["requests"] += 1 if got else 0
            h = hashlib.sha256(open(out, "rb").read()).hexdigest()
            manifest.append({"member": i.filename, "bytes": i.file_size, "sha256": h,
                             "generator": i.filename.split("/")[1]})
            done += 1
            if done % 50 == 0:
                print(f"  ...{done}/{len(selected)}  transferred {(index_cost+stats['bytes'])/1e9:.2f} GB", flush=True)

    json.dump({
        "source_id": SRC, "official_url": URL,
        "remote_archive_bytes": f.size,
        "remote_member_count": len(infos),
        "full_archive_downloaded": False,
        "full_archive_sha256": None,
        "full_archive_sha256_note": "deliberately absent - the archive was never downloaded, so any hash would be fabricated",
        "selection_rule": f"equal count per distributor-defined generator folder ({PER_GENERATOR} each), files in sorted order within each folder; content-blind",
        "byte_budget": BYTE_BUDGET,
        "generators": sorted(bygen),
        "selected_count": len(selected),
        "selected_bytes": total,
        "bytes_transferred_total": index_cost + stats["bytes"],
        "index_bytes": index_cost,
        "range_requests": f.requests + stats["requests"],
        "items": manifest,
    }, open(f"{DEST}/_transient_acquisition.json", "w"), indent=1)

    with open(f"{DEST}/_all_members.txt", "w") as fh:
        fh.write("\n".join(sorted(i.filename for i in infos)) + "\n")

    moved = index_cost + stats["bytes"]
    print(f"[{SRC}] done. transferred {moved/1e9:.2f} GB of a "
          f"{f.size/1e9:.2f} GB archive ({100*moved/f.size:.1f}%)")
    print(f"[{SRC}] free disk now {free_gb():.1f} GB")

if __name__ == "__main__":
    main()
