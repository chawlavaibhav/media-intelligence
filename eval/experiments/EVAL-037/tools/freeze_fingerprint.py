#!/usr/bin/env python3
"""EVAL-037 — compute the freeze fingerprint over the whole substrate.

One digest covering every file under eval/experiments/EVAL-037/, using the same
algorithm the Canon corpus index uses (sha256 over sorted "path:sha256\\n" lines), so
the two kinds of fingerprint in this experiment are directly comparable.

FREEZE-FINGERPRINT.yaml itself is excluded — a digest cannot cover the file that
stores it. Also excluded: runs/ (per-lane evidence written after the freeze),
__pycache__/, and dotfiles.

  python3 tools/freeze_fingerprint.py            # write FREEZE-FINGERPRINT.yaml
  python3 tools/freeze_fingerprint.py --check    # verify, exit 1 on drift
"""
import argparse
import hashlib
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
PKG = HERE.parent
OUT = PKG / "FREEZE-FINGERPRINT.yaml"
EXCLUDE_DIRS = {"runs", "__pycache__"}
EXCLUDE_FILES = {"FREEZE-FINGERPRINT.yaml"}


def files():
    out = []
    for p in sorted(PKG.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(PKG)
        if set(rel.parts) & EXCLUDE_DIRS or rel.name in EXCLUDE_FILES:
            continue
        if rel.name.startswith("."):
            continue
        out.append(rel)
    return sorted(out, key=str)


def compute():
    rows = [(str(r), hashlib.sha256((PKG / r).read_bytes()).hexdigest()) for r in files()]
    canonical = "".join(f"{p}:{h}\n" for p, h in rows)
    return hashlib.sha256(canonical.encode()).hexdigest(), rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    digest, rows = compute()

    if a.check:
        if not OUT.exists():
            print("FREEZE-FINGERPRINT.yaml is missing", file=sys.stderr)
            return 1
        recorded = None
        for line in OUT.read_text().splitlines():
            if line.startswith("combined_digest:"):
                recorded = line.split(":", 1)[1].strip()
        if recorded != digest:
            print(f"FREEZE DRIFT\n  recorded: {recorded}\n  computed: {digest}", file=sys.stderr)
            return 1
        print(f"freeze fingerprint intact: {digest}")
        return 0

    lines = [
        "# EVAL-037 — freeze fingerprint over the whole common substrate.",
        "#",
        "# Regenerate:  python3 tools/freeze_fingerprint.py",
        "# Verify:      python3 tools/freeze_fingerprint.py --check",
        "#",
        "# Excludes this file (self-reference), runs/ (post-freeze lane evidence),",
        "# __pycache__/, and dotfiles (.gitignore is hygiene, not experimental design).",
        "",
        "experiment: EVAL-037",
        "scope: eval/experiments/EVAL-037/**",
        "base_commit: c6f8d910f7a3cdaaeafa2280313abfb9b898cddd",
        "algorithm: sha256-of-sorted-path-and-content",
        f"file_count: {len(rows)}",
        f"combined_digest: {digest}",
        "files:",
    ]
    for p, h in rows:
        lines += [f"  - path: {p}", f"    sha256: {h}"]
    OUT.write_text("\n".join(lines) + "\n")
    print(f"{len(rows)} files\nfreeze fingerprint: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
