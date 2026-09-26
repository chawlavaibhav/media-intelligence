#!/usr/bin/env python3
"""Spend of a bake-off run, read from its ledger only (never mapping.json).

    python3 cost_report.py <run_dir>          → prints the report and writes <run_dir>/COSTS.json

Three views:
- LEDGER TOTAL: the cap's rule. A settled call counts at its settled amount; a call that never settled (stopped
  mid-call) counts at its reserved amount; a failed media call counts at its reserved price (conservative).
- COMPARABLE per exam arm: for each (brief, arm), only the LAST attempt of each generation tag counts. This drops
  takes that were re-made because of the runner's spoken-line defect (E09 B, E12 B, E12 C) and duplicates left by
  stopped attempts, so arms are compared on what they needed to make the ad they showed.
- LIKELY BILL: the ledger total minus Veo generations Google filtered (no video returned, normally not billed) and
  minus reservations that never settled.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path


def main(run_dir: str) -> dict:
    run = Path(run_dir)
    rows = [json.loads(l) for l in (run / "ledger.jsonl").read_text().splitlines() if l.strip()]
    res = {r["id"]: r for r in rows if r["kind"] == "reserve"}
    st = {r["id"]: r for r in rows if r["kind"] == "settle" and r["id"] in res}
    amt = {i: (st[i]["amount"] if i in st else r["amount"]) for i, r in res.items()}
    total = sum(amt.values())
    by_step, by_route = defaultdict(float), defaultdict(float)
    for i, r in res.items():
        by_step[r["step"]] += amt[i]
        by_route[r["route"]] += amt[i]
    filtered = sum(amt[i] for i, s in st.items() if s["status"] == "failed" and res[i]["route"].startswith("veo")
                   and "filtered" in s.get("detail", ""))
    never = sum(r["amount"] for i, r in res.items() if i not in st)

    # comparable: last attempt per (brief, arm, route, tag); OCR checks all count
    last = {}
    extra = defaultdict(float)
    for i, r in sorted(res.items(), key=lambda kv: kv[1]["t"]):
        if r["step"] == "practice":
            continue
        key = (r["brief"], r["arm"], r["route"], r["what"])
        if r["route"] in ("ocr", "claude"):
            last[(key, i)] = amt[i]
            continue
        if key in last:
            extra[(r["brief"], r["arm"])] += last[key]
        last[key] = amt[i]
    # takes set aside for the spoken-line redo (<brief>/<arm>/_superseded-*/S<n>-t<k>.mp4, or recorded as set aside in
    # RUN-LOG when the file was lost): if their last ledger row is older than the set-aside folder, they were not re-made
    # and are not part of the shown ad either — count them as redo overhead, not comparable cost.
    import re
    known_set_aside = {("E12", "B"): {"S1-t1", "S1-t2", "S2-t1"}}      # E12 B's old S1 takes were lost, see RUN-LOG
    for sup in run.glob("E*/*/_superseded-*"):
        b, a = sup.parent.parent.name, sup.parent.name
        tags = {p.stem for p in sup.glob("S*-t*.mp4") if re.fullmatch(r"S\d+-t\d+", p.stem)} | known_set_aside.get((b, a), set())
        cutoff = sup.stat().st_mtime
        for tag in tags:
            for route in ("veo-std", "veo-fast"):
                key = (b, a, route, tag)
                t_last = max((r["t"] for r in res.values() if (r["brief"], r["arm"], r["route"], r["what"]) == key), default=None)
                if key in last and t_last is not None and t_last < cutoff:
                    extra[(b, a)] += last.pop(key)
    comp = defaultdict(float)
    for k, v in last.items():
        b, a = (k[0][0], k[0][1]) if isinstance(k[0], tuple) else (k[0], k[1])
        comp[(b, a)] += v
    per_arm = defaultdict(list)
    for (b, a), v in comp.items():
        per_arm[a].append(v)

    out = {"ledger_total": round(total, 2), "by_step": {k: round(v, 2) for k, v in by_step.items()},
           "by_service": {k: round(v, 2) for k, v in sorted(by_route.items(), key=lambda kv: -kv[1]) if v},
           "veo_filtered_booked": round(filtered, 2), "never_settled": round(never, 2),
           "likely_bill": round(total - filtered - never, 2),
           "comparable_per_brief_arm": {f"{b} {a}": round(v, 2) for (b, a), v in sorted(comp.items())},
           "redo_or_aborted_extra": {f"{b} {a}": round(v, 2) for (b, a), v in sorted(extra.items()) if v},
           "mean_comparable_per_arm": {a: round(sum(v) / len(v), 2) for a, v in sorted(per_arm.items())}}
    (run / "COSTS.json").write_text(json.dumps(out, indent=1))
    print(f"LEDGER TOTAL US${out['ledger_total']:.2f}  (cap rule; failed/stopped calls at full price)")
    print(f"LIKELY BILL  US${out['likely_bill']:.2f}  (minus Veo-filtered US${filtered:.2f}, never-settled US${never:.2f})")
    print("by step      " + ", ".join(f"{k} US${v:.2f}" for k, v in sorted(out["by_step"].items())))
    print("by service   " + ", ".join(f"{k} US${v:.2f}" for k, v in out["by_service"].items()))
    print("mean comparable cost per exam round: " + ", ".join(f"{a} US${v:.2f}" for a, v in out["mean_comparable_per_arm"].items()))
    print("redo / aborted extra (not in comparable): " + ", ".join(f"{k} US${v:.2f}" for k, v in out["redo_or_aborted_extra"].items()))
    return out


if __name__ == "__main__":
    main(sys.argv[1])
