#!/usr/bin/env python3
"""Score every ranking in runs.json (+ agentic-results.json, llm-rerank.json, baselines) against the hand-cited claims.

    python3 eval/retrieval-canon-2026-09-25/score_runs.py      (needs pyyaml; seconds, US$0)

Metrics per brief and k: P@k (share of the top k a producer actually cited), R@k (share of the cited set found),
and R@k/max (recall divided by the best possible at that k, min(1, k/|truth|)) so briefs with 82 vs 22 cited claims
are comparable. Writes SCORES.md and scores.json.
"""
from __future__ import annotations

import glob
import json
import random
import re
from collections import Counter
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
KS = (5, 10, 20, 50)
SK = re.compile(r"\bsk_[a-z0-9]+(?:_[a-z0-9]+)*_[0-9]{3,4}\b")


def main():
    corpus = []
    for f in sorted(glob.glob(str(REPO / "canon/knowledge/current/*/source-knowledge.yaml"))):
        corpus += [c["sk_id"] for c in yaml.safe_load(open(f, encoding="utf-8"))["source_knowledge"]]
    cset = set(corpus)
    y = yaml.safe_load(open(REPO / "canon/validation/HAND-RETRIEVED-CLAIMS.yaml"))
    jobs = {j: [c["id"] for c in (v.get("claims") or [])] for j, v in y["jobs"].items()}
    rj = ["RENTOK-GAME-A-004", "RENTOK-GAME-B-005", "RENTOK-CREATIVE-QUALITY-001", "RENTOK-GAME-V2-006"]
    truth = {"rentok": set().union(*(set(jobs[j]) for j in rj)), "mokobara": set(jobs["MOKOBARA-ODYSSEY-007"])}

    runs = json.loads((HERE / "runs.json").read_text())
    for extra, label in (("agentic-results.json", "agentic (blind LLM agent over a label index, 7 tool calls)"),
                         ("llm-rerank.json", "LLM re-rank of hybrid(LLM sub-queries) top-60 (blind)")):
        p = HERE / extra
        if p.exists():
            d = json.loads(p.read_text())
            for b in truth:
                runs[b][label] = [i for i in d[b] if i in cset]

    # Baseline: no retrieval at all, a fixed "most-cited claims" list learned from the OTHER brief's jobs.
    # For Mokobara: rank by how many of the 4 RentOK jobs cited each claim. For RentOK: by Mokobara (weak, 22 ids).
    pop_r = Counter(i for j in rj for i in jobs[j])
    runs["mokobara"]["fixed popular list (learned from RentOK jobs, no query)"] = [i for i, _ in pop_r.most_common()]
    runs["rentok"]["fixed popular list (learned from Mokobara job, no query)"] = list(jobs["MOKOBARA-ODYSSEY-007"])

    # Random baseline (mean of 200 shuffles)
    rng = random.Random(0)

    def metrics(r, t):
        out = {}
        for k in KS:
            hit = len(set(r[:k]) & t)
            out[k] = {"P": hit / k, "R": hit / len(t), "Rmax": (hit / len(t)) / min(1, k / len(t)), "n": len(r[:k])}
        return out

    table = {b: {name: metrics(r, truth[b]) for name, r in runs[b].items()} for b in truth}
    for b in truth:
        acc = {k: {"P": 0, "R": 0, "Rmax": 0} for k in KS}
        for _ in range(200):
            sh = corpus[:]
            rng.shuffle(sh)
            m = metrics(sh, truth[b])
            for k in KS:
                for x in ("P", "R", "Rmax"):
                    acc[k][x] += m[k][x] / 200
        table[b]["random"] = {k: {**acc[k], "n": k} for k in KS}

    overlap = truth["rentok"] & truth["mokobara"]
    lines = ["# Canon retrieval — scores", "",
             f"Corpus {len(corpus)} claims. Cited (truth): RentOK {len(truth['rentok'])} (union of 4 jobs on one brief), "
             f"Mokobara {len(truth['mokobara'])}. Overlap between the two briefs: {len(overlap)} claims "
             f"({len(overlap)/len(truth['mokobara']):.0%} of Mokobara's).", ""]
    for b in truth:
        lines += [f"## {b} (|truth| = {len(truth[b])})", "",
                  "| method | P@10 | P@20 | P@50 | R@20 | R@50 | R@20 / max |", "|---|---|---|---|---|---|---|"]
        order = sorted(table[b], key=lambda n: -table[b][n][20]["P"])
        for name in order:
            m = table[b][name]
            f = lambda k, x: (f"{m[k][x]:.2f}" if m[k]["n"] >= k else "–")
            lines.append(f"| {name} | {f(10,'P')} | {f(20,'P')} | {f(50,'P')} | {f(20,'R')} | {f(50,'R')} | {f(20,'Rmax')} |")
        lines.append("")
    (HERE / "SCORES.md").write_text("\n".join(lines))
    (HERE / "scores.json").write_text(json.dumps(table, indent=1, default=str))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
