#!/usr/bin/env python3
"""verify_sealed_evidence.py -- prove the sealed experimental evidence is byte-intact.

Two independent checks, both read-only, no network:

  1. HASH CHECK. Every `*.record.json` under eval/experiments/EVAL-040/runs/*/artifacts/ names the
     media file it seals (`relative_path`), its byte count (`bytes`) and its sha256. The media bytes
     on disk are re-hashed and re-counted against the record. Report B (10 Sep 2026) did this by hand
     and found 311 of 311 intact; this tool makes that check re-runnable by anyone.

  2. DIFF CHECK (optional, `--against <git ref>`). The sealed trees must not differ from the named
     ref. The sealed trees are:
        eval/experiments/          eval/registry/          eval/empirical-planning/STAGE-A-FREEZE-2026-09/
     A non-empty diff is reported file by file and the exit code is non-zero. This is the mechanical
     form of the rule "sealed evidence is never edited; derivative maps are regenerated instead".

Exit 0 only when every record re-hashes AND (if asked) the diff is empty.

    python3 coordination/audits/tools/verify_sealed_evidence.py
    python3 coordination/audits/tools/verify_sealed_evidence.py --against origin/main
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import subprocess
import sys

RUNS_GLOB = os.path.join("eval", "experiments", "EVAL-040", "runs", "*", "artifacts", "*.record.json")
SEALED_TREES = ("eval/experiments", "eval/registry", "eval/empirical-planning/STAGE-A-FREEZE-2026-09")


def repo_root() -> str:
    here = os.path.dirname(os.path.abspath(__file__))
    cur = here
    while cur != os.path.dirname(cur):
        if os.path.isdir(os.path.join(cur, "eval")) and os.path.isdir(os.path.join(cur, "coordination")):
            return cur
        cur = os.path.dirname(cur)
    sys.stderr.write("could not find the repository root above %s\n" % here)
    raise SystemExit(2)


def hash_check(root: str) -> tuple[int, int, list, list]:
    records = sorted(glob.glob(os.path.join(root, RUNS_GLOB)))
    checked, ok, bad, missing = 0, 0, [], []
    for rec_path in records:
        with open(rec_path, "r", encoding="utf-8") as fh:
            rec = json.load(fh)
        sha, rel, size = rec.get("sha256"), rec.get("relative_path"), rec.get("bytes")
        if not sha or not rel:
            continue
        run_dir = os.path.dirname(os.path.dirname(rec_path))
        media = os.path.join(run_dir, rel)
        if not os.path.exists(media):
            alt = os.path.join(os.path.dirname(rec_path), rel)
            if os.path.exists(alt):
                media = alt
            else:
                missing.append(os.path.relpath(rec_path, root))
                continue
        checked += 1
        with open(media, "rb") as fh:
            data = fh.read()
        if hashlib.sha256(data).hexdigest() == sha and (size is None or len(data) == size):
            ok += 1
        else:
            bad.append(os.path.relpath(media, root))
    return checked, ok, bad, missing


def diff_check(root: str, ref: str) -> list:
    out = subprocess.run(["git", "diff", "--name-only", ref, "--", *SEALED_TREES],
                         cwd=root, capture_output=True, text=True, check=True)
    return [line for line in out.stdout.splitlines() if line.strip()]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--against", metavar="REF", default=None,
                    help="also require `git diff REF -- <sealed trees>` to be empty")
    args = ap.parse_args()
    root = repo_root()

    checked, ok, bad, missing = hash_check(root)
    print("sealed media records checked : %d" % checked)
    print("re-hash + byte count match   : %d" % ok)
    print("mismatched                   : %d" % len(bad))
    print("record without media on disk : %d" % len(missing))
    for p in bad:
        print("  MISMATCH %s" % p)
    for p in missing:
        print("  MISSING  %s" % p)
    failed = bool(bad or missing) or checked == 0

    if args.against:
        changed = diff_check(root, args.against)
        print("sealed trees vs %s        : %s" % (args.against, "UNCHANGED" if not changed else "%d file(s) differ" % len(changed)))
        for p in changed:
            print("  CHANGED  %s" % p)
        failed = failed or bool(changed)

    print("RESULT: %s" % ("PASS" if not failed else "FAIL"))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
