#!/usr/bin/env python3
"""Canon shape v1 — piece 4 of 5: build LABEL-INDEX.md, one line per accepted claim, grouped by source.

    python3 canon/shape-v1/build_label_index.py

The index is what a lookup step (an LLM) scans to pick <=10 brief-specific claims, then fetches their full
text by id. In the 2026-09-25 retrieval test (eval/retrieval-canon-2026-09-25/RESULT.md) an LLM scanning
exactly this kind of index was the best retriever; keyword/embedding search on the brief was near random.
Regenerate whenever canon/knowledge/current changes; never edit by hand.
"""
from __future__ import annotations

import glob
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def main() -> None:
    lines = ["# Canon label index (generated — do not edit)", "",
             "One line per accepted claim: `sk_id | what it is about`. Scan, pick at most 10 ids that matter for THIS brief,",
             "then read those claims in full from `canon/knowledge/current/<source>/source-knowledge.yaml`.", ""]
    n = 0
    for f in sorted(glob.glob(str(REPO / "canon/knowledge/current/*/source-knowledge.yaml"))):
        src = Path(f).parent.name
        claims = yaml.safe_load(open(f, encoding="utf-8"))["source_knowledge"]
        lines.append(f"## {src} ({len(claims)})")
        for c in claims:
            lines.append(f"{c['sk_id']} | {c['concept_label'].replace('_', ' ')}")
            n += 1
        lines.append("")
    (HERE / "LABEL-INDEX.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"LABEL-INDEX.md: {n} claims, {sum(len(l) for l in lines)} chars")


if __name__ == "__main__":
    main()
