#!/usr/bin/env python3
"""Recompute the EVAL-037 retrieval figures cited in CANON-CONTEXT-SPEC-v0.1.md §1.

COMPUTE FIRST, LOAD SECOND (shared/CONTEXT-SUFFICIENCY-POLICY.md). The spec argues from a handful
of numbers about how the unbounded Canon interface actually behaved. Those numbers are derived
here from the committed EVAL-037 repair-run artifacts rather than restated from prose, so a reader
can check them without loading multi-megabyte transcripts into context.

This reads committed evidence and asserts nothing new. It is not a certification of EVAL-037.

Run: python3 canon/validation/recount_eval037_retrieval.py
"""
from __future__ import annotations

import collections
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
RUN = ROOT / "eval/experiments/EVAL-037/runs/sonnet-full-canon-repair-001"
ORACLE = ROOT / "canon/experiments/v1/value-gate/oracle-contexts"


def main() -> int:
    if not RUN.exists():
        print(f"MISSING: {RUN.relative_to(ROOT)} — cannot recount", file=sys.stderr)
        return 2

    result = json.loads((RUN / "result.json").read_text())
    statuses = collections.Counter(t["status"] for t in result["trials"])

    calls = searches = reads = 0
    total_bytes = max_bytes = 0
    items = collections.Counter()
    transcripts = sorted((RUN / "transcripts").glob("*.jsonl"))
    for path in transcripts:
        for line in path.read_text().splitlines():
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            call = record.get("call") or {}
            if call.get("tool_family") != "canon":
                continue
            calls += 1
            name = call.get("name", "")
            searches += "search" in name
            reads += "read" in name
            nbytes = call.get("result_bytes") or 0
            total_bytes += nbytes
            max_bytes = max(max_bytes, nbytes)
            for key in ("accepted_items", "hold_items", "qa_items"):
                items[key] += call.get(key) or 0

    usage = result.get("lane_usage_totals") or {}

    print("EVAL-037 — sonnet-full-canon-repair-001 (committed evidence)")
    print(f"  trials:                {result.get('trial_count')} "
          f"({', '.join(f'{v} {k}' for k, v in sorted(statuses.items()))})")
    print(f"  committed transcripts: {len(transcripts)}  (failed trials produced none)")
    print(f"  canon tool calls:      {calls}  ({searches} search, {reads} read)")
    print(f"  search result bytes:   {total_bytes:,} total, {max_bytes:,} largest single call")
    print(f"  items returned:        {items['accepted_items']} accepted, "
          f"{items['hold_items']} HOLD, {items['qa_items']} QA")
    print(f"  lane input tokens:     {usage.get('input_tokens'):,} over "
          f"{usage.get('provider_turns')} provider turns")
    print(f"  lane calculated cost:  USD {result.get('lane_calculated_cost_usd')}")

    if ORACLE.exists():
        sizes = sorted(p.stat().st_size for p in ORACLE.glob("*.md"))
        entries = sorted(
            sum(1 for line in p.read_text().splitlines() if line.startswith("## "))
            for p in ORACLE.glob("*.md")
        )
        print("\nvalue-gate oracle contexts (the hand-built size precedent)")
        print(f"  contexts:              {len(sizes)}")
        print(f"  bytes:                 {sizes[0]:,}–{sizes[-1]:,}")
        print(f"  entries per context:   {entries[0]}–{entries[-1]}")
        if max_bytes and sizes:
            median = sizes[len(sizes) // 2]
            print(f"  largest search / median oracle context: {max_bytes / median:.0f}x")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
