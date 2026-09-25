#!/usr/bin/env python3
"""Canon Q&A knowledge test (2026-09-25): what does a strong model already know WITHOUT the Canon?

A blind Claude model answered 345 Canon Q&A items (15 per book x 23 books, stratified by application vs knowledge)
from its own knowledge; separate blind graders scored each answer against the book's reference answer
(2 = key points right, 1 = partial / generic, 0 = wrong or filler). This script joins sample.json with
answers-*.json and grades-*.json and writes RESULT-TABLES.md + by_item.json.

    python3 eval/canon-qa-knowledge-2026-09-25/analyse.py
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    sample = {s["qa_id"]: s for s in json.loads((HERE / "sample.json").read_text())}
    ans, grd = {}, {}
    for b in range(1, 5):
        for a in json.loads((HERE / f"answers-{b}.json").read_text()):
            ans[a["qa_id"]] = a["answer"]
        for g in json.loads((HERE / f"grades-{b}.json").read_text()):
            grd[g["qa_id"]] = g
    rows = []
    for q, s in sample.items():
        g = grd.get(q)
        if not g:
            continue
        rows.append({**s, "model_answer": ans.get(q, ""), "score": int(g["score"]), "generic": bool(g.get("generic")),
                     "missed": g.get("missed", ""), "unsure": "[unsure]" in ans.get(q, "")})
    (HERE / "by_item.json").write_text(json.dumps(rows, indent=1))

    def summ(rs):
        n = len(rs)
        full = sum(r["score"] == 2 for r in rs) / n
        part = sum(r["score"] == 1 for r in rs) / n
        wrong = sum(r["score"] == 0 for r in rs) / n
        return n, full, part, wrong, sum(r["score"] for r in rs) / (2 * n), sum(r["generic"] for r in rs) / n

    out = ["# Canon Q&A knowledge test — tables", ""]
    n, f, p, w, m, gen = summ(rows)
    out += [f"**All items:** n={n} · knows it (2) **{f:.0%}** · partial (1) {p:.0%} · wrong (0) {w:.0%} · "
            f"score {m:.0%} · answers graded generic {gen:.0%} · self-flagged unsure {sum(r['unsure'] for r in rows)/n:.0%}", ""]

    def table(title, key):
        groups = defaultdict(list)
        for r in rows:
            groups[key(r)].append(r)
        t = [f"## {title}", "", "| group | n | knows (2) | partial (1) | wrong (0) | score |", "|---|---|---|---|---|---|"]
        for k, rs in sorted(groups.items(), key=lambda kv: summ(kv[1])[4]):
            n, f, p, w, m, _ = summ(rs)
            t.append(f"| {k} | {n} | {f:.0%} | {p:.0%} | {w:.0%} | {m:.0%} |")
        return t + [""]

    out += table("By question kind", lambda r: "application (new case)" if r["requires_application"] else "knowledge of the book")
    out += table("By answer type", lambda r: r["answer_type"] or "?")
    out += table("By source status", lambda r: r["source_status"] or "?")
    out += table("By book (lowest score first = biggest gap)", lambda r: r["source_id"])
    (HERE / "RESULT-TABLES.md").write_text("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    main()
