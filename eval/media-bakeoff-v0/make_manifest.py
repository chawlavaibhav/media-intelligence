#!/usr/bin/env python3
"""Hash-pin a bake-off run's media so the media can live outside git.

    python3 make_manifest.py <run_dir>                  # writes <run_dir>/MANIFEST.sha256
    python3 make_manifest.py <run_dir> --out <file>     # writes the manifest somewhere else (e.g. the repo's run folder)
    python3 make_manifest.py <run_dir> --check [<file>] # re-hashes and reports anything missing, changed or new

Format: one line per media file, "<sha256>  <path relative to run_dir>", sorted by path, the same format as
`shasum -a 256`, so it can also be checked with:   cd <run_dir> && shasum -a 256 -c MANIFEST.sha256

Media = .png .jpg .jpeg .mp4 .mp3 .wav (case-insensitive), anywhere under run_dir, including assets/ and every
take, not only the *-final files. Nothing is opened except the media files and each brief's results.json
(to tell whether the run is still going). mapping.json is never read.

It refuses to write while the run looks unfinished (an exam/practice brief folder with no results.json, or a
CAP-REACHED.txt), unless --force is given, because a manifest taken mid-run would miss files.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import sys
from pathlib import Path

MEDIA = {".png", ".jpg", ".jpeg", ".mp4", ".mp3", ".wav"}
NAME = "MANIFEST.sha256"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):   # 1 MB chunks: films never load whole into memory
            h.update(chunk)
    return h.hexdigest()


def media_files(run: Path) -> list[Path]:
    out = []
    for root, dirs, files in os.walk(run):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for name in files:
            p = Path(root) / name
            if p.suffix.lower() in MEDIA and not name.startswith("."):
                out.append(p)
    return sorted(out, key=lambda p: p.relative_to(run).as_posix())


def unfinished(run: Path) -> list[str]:
    notes = []
    for d in sorted(run.iterdir()):
        if d.is_dir() and d.name[:1] in ("E", "T") and d.name[1:].isdigit() and not (d / "results.json").exists():
            notes.append(f"{d.name} has no results.json (still running?)")
    if (run / "CAP-REACHED.txt").exists():
        notes.append("CAP-REACHED.txt present (run stopped at a cap)")
    return notes


def build(run: Path) -> list[tuple[str, str, int]]:
    rows = []
    for p in media_files(run):
        rows.append((sha256(p), p.relative_to(run).as_posix(), p.stat().st_size))
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run_dir")
    ap.add_argument("--out", help=f"manifest path (default <run_dir>/{NAME})")
    ap.add_argument("--check", nargs="?", const="", metavar="MANIFEST",
                    help="verify instead of write (default manifest: <run_dir>/MANIFEST.sha256)")
    ap.add_argument("--force", action="store_true", help="write even if the run looks unfinished")
    a = ap.parse_args()

    run = Path(a.run_dir).expanduser().resolve()
    if not run.is_dir():
        print(f"not a directory: {run}", file=sys.stderr)
        return 2

    if a.check is not None:
        mf = Path(a.check).expanduser() if a.check else run / NAME
        want = {}
        for line in mf.read_text().splitlines():
            if line.strip():
                digest, rel = line.split("  ", 1)
                want[rel] = digest
        have = {rel: d for d, rel, _ in build(run)}
        missing = sorted(set(want) - set(have))
        changed = sorted(r for r in set(want) & set(have) if want[r] != have[r])
        new = sorted(set(have) - set(want))
        for label, items in (("MISSING", missing), ("CHANGED", changed), ("NOT IN MANIFEST", new)):
            for r in items:
                print(f"{label}: {r}")
        ok = not (missing or changed)
        print(f"{'OK' if ok else 'FAILED'}: {len(want)} in manifest, {len(missing)} missing, {len(changed)} changed, "
              f"{len(new)} new media files not in the manifest")
        return 0 if ok else 1

    notes = unfinished(run)
    if notes and not a.force:
        print("Run looks unfinished; manifest NOT written (use --force to write anyway):", file=sys.stderr)
        for n in notes:
            print("  - " + n, file=sys.stderr)
        return 3

    rows = build(run)
    out = Path(a.out).expanduser() if a.out else run / NAME
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(f"{d}  {rel}\n" for d, rel, _ in rows))
    total = sum(s for _, _, s in rows)
    finals = sum(1 for _, rel, _ in rows if "-final." in rel.rsplit("/", 1)[-1])
    by_ext: dict[str, int] = {}
    for _, rel, _ in rows:
        ext = Path(rel).suffix.lower()
        by_ext[ext] = by_ext.get(ext, 0) + 1
    print(f"wrote {out}: {len(rows)} media files ({finals} *-final), {total / 1e6:.1f} MB, "
          + ", ".join(f"{k} {v}" for k, v in sorted(by_ext.items())))
    for n in notes:
        print("  note: " + n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
