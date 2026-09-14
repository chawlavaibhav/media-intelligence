#!/usr/bin/env python3
"""Reconcile a pilot's append-only JSONL ledgers into the figures a production-learning case records.

Ledger semantics (the pilots' own): a `reserved` line is written BEFORE every request with its pinned
`est_usd`; the returning line carries `status: ok` or an error status. Conservative accounting counts every
reserved line — including calls that failed at the provider — because whether a failed call billed is
unknown until a vendor statement is reconciled. That is the same rule the spend records used
(`SPEND-AMENDMENT-V4.md`: "every `reserved` line ... failed calls included").

Usage:
    python3 production-learning/tools/reconcile_pilot_ledgers.py --ref work/pilot-upwork-intro-video-v4 \
        --pilot-dir pilots/upwork-intro-video-2026-09-14
Reads the ledgers through `git show <ref>:<path>` so it works whether or not the pilot tree is checked out.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from collections import OrderedDict
from decimal import Decimal
from pathlib import Path

LEDGERS = OrderedDict([
    ("v1_v2", "gen/LEDGER.jsonl"),
    ("v3", "v3/gen/LEDGER.jsonl"),
    ("v4", "v4/gen/LEDGER.jsonl"),
])


def totals(lines: list[dict]) -> dict:
    reserved = [r for r in lines if r.get("status") == "reserved"]
    returned = [r for r in lines if r.get("status") != "reserved"]
    by_route: dict = {}
    for r in reserved:
        slot = by_route.setdefault(r.get("route", "?"), {"calls": 0, "usd": Decimal("0")})
        slot["calls"] += 1
        slot["usd"] += Decimal(str(r.get("est_usd", "0")))
    stamps = [r["utc"] for r in lines if r.get("utc")]
    return {
        "reserved_usd": sum((Decimal(str(r.get("est_usd", "0"))) for r in reserved), Decimal("0")),
        "dispatches": len(reserved),
        "returned_ok": sum(1 for r in returned if r.get("status") == "ok"),
        "failed": sum(1 for r in returned if r.get("status") != "ok"),
        "first_utc": min(stamps) if stamps else None,
        "last_utc": max(stamps) if stamps else None,
        "by_route": by_route,
    }


def read_ledger(root: Path, ref: str, path: str) -> list[dict]:
    out = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=root, capture_output=True, text=True, check=True)
    return [json.loads(line) for line in out.stdout.splitlines() if line.strip()]


def pilot_totals(root: Path, ref: str, pilot_dir: str) -> dict:
    figures: dict = {}
    combined: list[dict] = []
    for key, rel in LEDGERS.items():
        lines = read_ledger(root, ref, f"{pilot_dir}/{rel}")
        figures[key] = totals(lines)
        combined.extend(lines)
    figures["all"] = totals(combined)
    return figures


def _plain(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    if isinstance(obj, dict):
        return {k: _plain(v) for k, v in obj.items()}
    return obj


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ref", default="work/pilot-upwork-intro-video-v4")
    ap.add_argument("--pilot-dir", default="pilots/upwork-intro-video-2026-09-14")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parents[2]))
    a = ap.parse_args()
    print(json.dumps(_plain(pilot_totals(Path(a.root), a.ref, a.pilot_dir)), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
