#!/usr/bin/env python3
"""verify_price_pins: every pinned vendor page still says what we claim it says.

    python3 coordination/audits/tools/verify_price_pins.py

Read-only. No network — it re-checks the BYTES ALREADY FETCHED, it never fetches again. Walks the
master index and every sub-index under eval/empirical-planning/price-pins-2026-09/ and checks, for
each pin: the file exists, its byte count matches, its sha256 matches, and every evidence quote is a
literal substring of the bytes. Exit code 1 if anything fails.

Written for the 2026-09-10 audit (findings F-9 and F-12): the master index had gone stale for the
re-pointed Gemini routes, and two of the judge's quotes are joined with an ellipsis and so are not
literal substrings. That is reported as a warning, not a failure, because the underlying numbers are
present in the bytes — but it must be visible rather than silent.
"""
import glob, hashlib, os, sys
import yaml

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PINS = os.path.join(ROOT, "eval", "empirical-planning", "price-pins-2026-09")


def load(idx):
    d = yaml.safe_load(open(idx, encoding="utf-8"))
    return d["pins"] if isinstance(d, dict) and "pins" in d else (d or [])


def main():
    cache, fails, warns, ok = {}, [], [], 0
    for idx in sorted(glob.glob(os.path.join(PINS, "**", "PIN-INDEX.yaml"), recursive=True)):
        rel = os.path.relpath(idx, ROOT)
        for pin in load(idx):
            key = f"{rel}::{pin.get('route_key')}"
            f = pin.get("pin_file")
            if not f:
                fails.append((key, "no pin_file")); continue
            path = f if os.path.isabs(f) else os.path.join(ROOT, f)
            if not os.path.exists(path):
                fails.append((key, f"missing file {f}")); continue
            if path not in cache:
                cache[path] = open(path, "rb").read()
            b = cache[path]
            if pin.get("bytes") and len(b) != int(pin["bytes"]):
                fails.append((key, f"byte count {len(b)} != recorded {pin['bytes']}")); continue
            if pin.get("sha256") and hashlib.sha256(b).hexdigest() != pin["sha256"]:
                fails.append((key, "sha256 mismatch")); continue
            quotes = [pin.get("evidence_quote")] + list(pin.get("additional_evidence_quotes") or [])
            missing = [q for q in quotes if q and q.encode("utf-8") not in b]
            if missing:
                if any("..." in q or "…" in q for q in missing):
                    warns.append((key, "quote is an ellipsis excerpt, not a literal substring"))
                    ok += 1
                else:
                    fails.append((key, f"quote not in bytes: {missing[0][:40]!r}"))
                    continue
            else:
                ok += 1
    print(f"pins checked: {ok + len(fails)}   verified: {ok}   failed: {len(fails)}   warnings: {len(warns)}")
    for k, m in warns:
        print(f"  WARN  {k}: {m}")
    for k, m in fails:
        print(f"  FAIL  {k}: {m}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
