#!/usr/bin/env python3
"""Arm C helpers (TEST-FLOWS.md §4): build the librarian prompt, fetch chosen claims, assemble the Canon block.

    python3 canon_context.py librarian <brief_file> <class>      -> prints the C0 librarian prompt
    python3 canon_context.py block <class> <id1,id2,...>          -> prints the Canon block inserted into C2
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


def example_excerpt(cls: str) -> str:
    if not cls.startswith(("F1", "M2")):
        return "(no accepted example for this class yet)"
    t = yaml.safe_load((REPO / "production-learning/cases/MOKOBARA-ODYSSEY-007/ACCEPTED-TEMPLATE.yaml").read_text())
    w = t["what_is_reusable_here"]
    lines = ["Mokobara castaway film v2 — founder: \"excellent. pass\" (accepted).",
             f"Skeleton: {w['skeleton']}", f"Direction layer: {w['direction_layer']}", "Beats:"]
    for b in t["structure"]:
        lines.append(f"- {b['n']}. {b['beat']} ({b['start_s']}–{b['end_s']} s) feeling: {b['feeling']}. {b['content']}")
    return "\n".join(lines)


def gap_card_body() -> str:
    text = (SHAPE / "GAP-CARD.md").read_text()
    return text.split("-->", 1)[1].strip() if "-->" in text else text


def main() -> None:
    cmd = sys.argv[1]
    if cmd == "librarian":
        brief, cls = Path(sys.argv[2]).read_text().strip(), sys.argv[3]
        print(f"""You are the librarian for an ad-making AI. Below is an index of 1,300 short claims from advertising, film, design,
photography and Indian-marketing books (one per line: id | topic).

CUSTOMER REQUEST (verbatim): {brief}
CLASS: {cls}

Pick AT MOST 10 claim ids whose full text would most change a real decision for THIS ad (idea, story, humour, brand
presence, short-form hook, shots/edit, character, showing the product, on-screen text, Indian audience).
Prefer specific over generic; skip anything the writer surely knows. Return JSON {{"ids":[...], "why":{{"id":"<=10 words"}}}}.

INDEX:
{(SHAPE / 'LABEL-INDEX.md').read_text()}""")
    elif cmd == "block":
        cls, ids = sys.argv[2], [i for i in sys.argv[3].split(",") if i][:10]
        cb = claims_by_id()
        pulled = "\n".join(f"[{i}] {cb[i][1]} ({cb[i][0]}) — {cb[i][2]}" for i in ids if i in cb) or "(none)"
        req = yaml.safe_load((SHAPE / "REQUIRED-DECISIONS.yaml").read_text())
        dec = ", ".join(d["id"] for d in req["decisions"])
        scene = ", ".join(d["id"] for d in req["per_scene"])
        print(f"""CRAFT NOTES FROM OUR LIBRARY (use them as a sharp colleague's notes — they never override the customer's words, and
you may depart from any with a one-line reason):

A. WHAT THE MODEL USUALLY DOESN'T KNOW (gap card):
{gap_card_body()}

B. CLAIMS THE LIBRARIAN PULLED FOR THIS BRIEF:
{pulled}

C. WHAT GOOD LOOKED LIKE (one accepted piece; learn the level, do not copy its story, casting, setting or music):
{example_excerpt(cls)}

ADDITIONAL OUTPUT — fill after your treatment:
"decisions": {{{dec}}} — each: {'; '.join(f"{d['id']}: {d['ask']}" for d in req['decisions'])}
and per scene ({scene}): {'; '.join(f"{d['id']}: {d['ask']}" for d in req['per_scene'])}""")
    elif cmd == "checklist":
        q = yaml.safe_load((SHAPE / "AFTER-WRITING-CHECKLIST.yaml").read_text())["questions"]
        print("\n".join(f"{x['id']}. {x['q']}" for x in q))


if __name__ == "__main__":
    main()
