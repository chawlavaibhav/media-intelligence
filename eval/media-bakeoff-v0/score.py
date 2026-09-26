#!/usr/bin/env python3
"""Score the bake-off against the pre-registered rules in HANDOFF.md.

    python3 score.py <run_dir>          (needs verdicts.json exported from viewer.html, mapping.json, outputs.json)
Writes <run_dir>/SCORECARD.md.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from math import comb
from pathlib import Path

PAYS = {"Yes as-is": 1, "Yes after one small fix": 1, "No": 0}


def sign_p(wins: int, n: int) -> float:
    """One-sided sign-test p-value: P(X >= wins | n, 0.5)."""
    return sum(comb(n, k) for k in range(wins, n + 1)) / 2 ** n if n else 1.0


def main(run_dir: str) -> None:
    run = Path(run_dir)
    mapping = json.loads((run / "mapping.json").read_text())
    verdicts = {v["pair_id"]: v for v in json.loads((run / "verdicts.json").read_text())}
    outputs = json.loads((run / "outputs.json").read_text())

    comp = defaultdict(lambda: {"w": 0, "l": 0, "t": 0, "by_class": defaultdict(lambda: [0, 0, 0])})
    pay = defaultdict(lambda: [0, 0])
    reasons = defaultdict(lambda: defaultdict(int))
    repeats = []
    for pid, m in mapping.items():
        v = verdicts.get(pid)
        if not v or not v.get("pref"):
            continue
        first = m["comparison"].split(" vs ")[0]
        pref = v["pref"]
        winner_side = "left" if pref.startswith("A") and "choose" not in pref else "right" if pref.startswith("B") else None
        winner = m[winner_side] if winner_side else None
        if "repeat_of" in m:
            repeats.append((m["repeat_of"], winner))
            continue
        c = comp[m["comparison"]]
        k = "t" if winner is None else ("w" if winner == first else "l")
        c[k] += 1
        c["by_class"][m["class"]][{"w": 0, "l": 1, "t": 2}[k]] += 1
        for side, key in (("left", "payA"), ("right", "payB")):
            arm = m[side]
            if v.get(key) in PAYS:
                pay[arm][0] += PAYS[v[key]]
                pay[arm][1] += 1
            why = v.get("whyA" if side == "left" else "whyB")
            if why and not why.startswith("("):
                reasons[arm][why] += 1
    agree = None
    if repeats:
        orig = {}
        for pid, m in mapping.items():
            v = verdicts.get(pid)
            if v and v.get("pref") and "repeat_of" not in m:
                pr = v["pref"]
                ws = "left" if pr.startswith("A") and "choose" not in pr else "right" if pr.startswith("B") else None
                orig[pid] = m[ws] if ws else None
        agree = sum(orig.get(o) == w for o, w in repeats) / len(repeats)

    cost = defaultdict(list)
    secs = defaultdict(list)
    for o in outputs:
        cost[o["arm"]].append(o.get("cost_usd") or 0)
        secs[o["arm"]].append(o.get("seconds") or 0)

    L = ["# Bake-off scorecard", ""]
    L += ["| comparison | wins | losses | ties | win rate (non-tie) | sign-test p |", "|---|---|---|---|---|---|"]
    for name, c in comp.items():
        n = c["w"] + c["l"]
        L.append(f"| {name} | {c['w']} | {c['l']} | {c['t']} | {c['w']/n:.0%} | {sign_p(c['w'], n):.3f} |" if n else f"| {name} | 0 | 0 | {c['t']} | – | – |")
    L += ["", "| arm | would pay | mean cost/round US$ | mean machine time s | top 'no' reasons |", "|---|---|---|---|---|"]
    for arm in sorted(set(pay) | set(cost)):
        pr = f"{pay[arm][0]}/{pay[arm][1]} ({pay[arm][0]/pay[arm][1]:.0%})" if pay[arm][1] else "–"
        mc = sum(cost[arm]) / len(cost[arm]) if cost[arm] else 0
        ms = sum(secs[arm]) / len(secs[arm]) if secs[arm] else 0
        top = ", ".join(f"{k} ×{n}" for k, n in sorted(reasons[arm].items(), key=lambda kv: -kv[1])[:3])
        L.append(f"| {arm} | {pr} | {mc:.2f} | {ms:.0f} | {top} |")
    L += ["", f"Founder consistency on swapped repeats: {agree:.0%}" if agree is not None else "No repeats judged.", ""]
    L += ["## By class (wins / losses / ties)", ""]
    for name, c in comp.items():
        L.append(f"- **{name}:** " + "; ".join(f"{k} {w}/{l}/{t}" for k, (w, l, t) in sorted(c["by_class"].items())))
    L += ["", "## Pre-registered decisions (HANDOFF.md)", ""]

    def rate(name):
        c = comp.get(name)
        n = (c["w"] + c["l"]) if c else 0
        return (c["w"] / n if n else None), c

    _, c = rate("B vs A")
    if c:
        for k, (w, l, t) in sorted(c["by_class"].items()):
            ok = (w + l) and w / (w + l) >= 2 / 3
            L.append(f"- {k}: B vs A {w}/{l} (ties {t}) -> {'ship the pipeline' if ok else 'ship A + our finishing'}")
    pr = lambda arm: (pay[arm][0] / pay[arm][1]) if pay[arm][1] else 0
    for arm, name in (("B", "B vs A"), ("C", "C vs A")):
        _, c = rate(name)
        if c:
            ok = c["w"] >= 8 and pr(arm) - pr("A") >= 0.20
            L.append(f"- Golden benchmark via {arm}: {name} {c['w']}/{c['l']} (ties {c['t']}), would-pay {arm} {pr(arm):.0%} vs A {pr('A'):.0%} -> {'BEATS LLM+model' if ok else 'does not clearly beat LLM+model'}")
    _, c = rate("C vs B")
    if c:
        ok = c["w"] > c["l"] and c["w"] >= 7
        L.append(f"- Canon: C vs B {c['w']}/{c['l']} (ties {c['t']}) -> {'KEEP in writer context (confirm on 30 briefs)' if ok else 'NOT in writer context'}")
    _, c = rate("A_MAI vs A")
    if c:
        L.append(f"- Side check, image model: MAI-Image-2.6 vs Nano Banana 2 (same prompts) {c['w']}/{c['l']} (ties {c['t']}) -> "
                 f"{'MAI preferred' if c['w'] > c['l'] else 'Nano Banana 2 preferred' if c['l'] > c['w'] else 'no difference'} (directional, n small)")
    (run / "SCORECARD.md").write_text("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main(sys.argv[1])
