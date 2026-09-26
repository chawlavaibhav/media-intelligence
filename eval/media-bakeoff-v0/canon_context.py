#!/usr/bin/env python3
"""Arm C helpers (TEST-FLOWS.md §4): build the librarian prompt, fetch chosen claims, assemble the Canon block.

    python3 canon_context.py librarian <brief_file> <class>      -> prints the C0 librarian prompt
    python3 canon_context.py block <class> <id1,id2,...> [<g1,g2,...>] -> the Canon block inserted into C2 (claims + chosen gap rules; no example)
    python3 canon_context.py checklist                           -> prints the C2b checklist questions

Deterministic: the same inputs give the same text. It reads canon/shape-v1/ and canon/knowledge/current/ only.
"""
from __future__ import annotations

import glob
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
SHAPE = REPO / "canon" / "shape-v1"


def claims_by_id() -> dict:
    out = {}
    for f in glob.glob(str(REPO / "canon/knowledge/current/*/source-knowledge.yaml")):
        src = Path(f).parent.name
        for c in yaml.safe_load(open(f, encoding="utf-8"))["source_knowledge"]:
            out[c["sk_id"]] = (src, c["concept_label"].replace("_", " "), " ".join(c["claim"].split()))
    return out


def gap_rules() -> dict:
    """{n: (heading, text)} parsed from GAP-CARD.md (numbered rules under ## headings)."""
    import re
    text = (SHAPE / "GAP-CARD.md").read_text()
    text = text.split("-->", 1)[1] if "-->" in text else text
    rules, heading, cur = {}, "", None
    for line in text.splitlines():
        if line.startswith("## "):
            heading, cur = line[3:].strip(), None
            continue
        m = re.match(r"^(\d+)\.\s+(.*)", line)
        if m:
            cur = int(m.group(1))
            rules[cur] = [heading, m.group(2).strip()]
        elif cur and line.strip() and not line.startswith("#"):
            rules[cur][1] += " " + line.strip()
    return {k: (h, " ".join(t.split())) for k, (h, t) in rules.items()}


def main() -> None:
    cmd = sys.argv[1]
    if cmd == "librarian":
        brief, cls = Path(sys.argv[2]).read_text().strip(), sys.argv[3]
        gr = gap_rules()
        gap_list = "\n".join(f"G{n}. [{h}] {t}" for n, (h, t) in sorted(gr.items()))
        print(f"""You are the librarian for an ad-making AI. You prepare its reading for ONE ad.

CUSTOMER REQUEST (verbatim): {brief}
CLASS: {cls}

TASK 1 — From the GAP RULES below (things the writer model does not know by default), pick ONLY the ones that apply to
THIS ad (at most 8; zero is fine). Skip any rule about a subject this ad does not involve.
TASK 2 — From the INDEX below (1,300 short claims from advertising, film, design, photography and Indian-marketing books;
one per line: id | topic), pick AT MOST 10 claim ids whose full text would most change a real decision for THIS ad
(idea, story, humour, brand presence, short-form hook, shots/edit, character, showing the product, on-screen text,
Indian audience). Prefer specific over generic; skip anything the writer surely knows.

Return JSON only: {{"gap_rules":[numbers], "ids":[...], "why":{{"id or G#":"<=10 words"}}}}

GAP RULES:
{gap_list}

INDEX:
{(SHAPE / 'LABEL-INDEX.md').read_text()}""")
    elif cmd == "block":
        cls, ids = sys.argv[2], [i for i in sys.argv[3].split(",") if i][:10]
        gsel = [int(x) for x in (sys.argv[4].split(",") if len(sys.argv) > 4 else []) if x.strip()][:8]
        cb, gr = claims_by_id(), gap_rules()
        pulled = "\n".join(f"[{i}] {cb[i][1]} ({cb[i][0]}) — {cb[i][2]}" for i in ids if i in cb) or "(none)"
        gaps = "\n".join(f"- {gr[n][1]}" for n in gsel if n in gr) or "(none apply to this ad)"
        req = yaml.safe_load((SHAPE / "REQUIRED-DECISIONS.yaml").read_text())
        dec = ", ".join(d["id"] for d in req["decisions"])
        scene = ", ".join(d["id"] for d in req["per_scene"])
        print(f"""CRAFT NOTES FROM OUR LIBRARY (use them as a sharp colleague's notes — they never override the customer's words, and
you may depart from any with a one-line reason):

A. WHAT YOU PROBABLY DON'T KNOW THAT MATTERS FOR THIS AD:
{gaps}

B. CLAIMS FROM OUR BOOKS PULLED FOR THIS AD:
{pulled}

ADDITIONAL OUTPUT — fill after your treatment:
"decisions": {{{dec}}} — each: {'; '.join(f"{d['id']}: {d['ask']}" for d in req['decisions'])}
and per scene ({scene}): {'; '.join(f"{d['id']}: {d['ask']}" for d in req['per_scene'])}""")
    elif cmd == "checklist":
        q = yaml.safe_load((SHAPE / "AFTER-WRITING-CHECKLIST.yaml").read_text())["questions"]
        print("\n".join(f"{x['id']}. {x['q']}" for x in q))


if __name__ == "__main__":
    main()
