#!/usr/bin/env python3
"""
Consolidate every lane's Q&A bank into QA-MANIFEST.json, and refresh the counts row of
SOURCE-STATUS.csv.

Mechanical only. It aggregates what the lanes wrote; it decides nothing.

Usage: python3 canon/experimental/book-expansion-qa-v1/build_manifest.py [repo_root]
"""

import csv
import json
import os
import sys
from collections import Counter, OrderedDict

import yaml

EXP_REL = "canon/experimental/book-expansion-qa-v1"

# Stated rather than computed: the spans actually read, established from the copies themselves.
MATERIAL_EXAMINED = (
    "~248 printed pages of Hopkins (208 + 40), plus WCAG 2.2 Guideline 1.4 "
    "with its glossary and 7 Understanding notes, plus 3 Google ABCD pages"
)


def unwrap(obj, *keys):
    if isinstance(obj, dict):
        for k in keys:
            if k in obj and obj[k] is not None:
                return obj[k]
        return []
    return obj or []


def load(path, *keys):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return unwrap(yaml.safe_load(fh), *keys)


def main(root):
    exp = os.path.join(root, EXP_REL)
    dirs = sorted(
        d for d in os.listdir(exp)
        if os.path.isdir(os.path.join(exp, d)) and not d.startswith(".")
    )

    items = []
    per_source = OrderedDict()
    for sd in dirs:
        base = os.path.join(exp, sd)
        qa = load(os.path.join(base, "qa-bank.yaml"), "qa_items", "items", "qa_bank")
        sk = load(os.path.join(base, "source-knowledge.yaml"), "source_knowledge", "objects", "items")
        scs = load(os.path.join(base, "source-concept-systems.yaml"), "source_concept_systems", "systems", "items")
        bnd = load(os.path.join(base, "operational-bindings.yaml"), "operational_bindings", "bindings", "items")
        ontp = os.path.join(base, "ontology-mappings.yaml")
        ont = {}
        if os.path.exists(ontp):
            with open(ontp, encoding="utf-8") as fh:
                ont = yaml.safe_load(fh) or {}
        items.extend(qa)
        per_source[sd] = {
            "source_knowledge_objects": len(sk),
            "source_concept_systems": len(scs),
            "operational_bindings": len(bnd),
            "ontology_terms": len(ont.get("terms") or []) if isinstance(ont, dict) else 0,
            "ontology_relationships": len(ont.get("relationships") or []) if isinstance(ont, dict) else 0,
            "ontology_concepts": len(ont.get("concepts") or []) if isinstance(ont, dict) else 0,
            "qa_count": len(qa),
            "requires_application": sum(1 for i in qa if i.get("requires_application") is True),
        }

    def tally(field):
        return OrderedDict(sorted(Counter(str(i.get(field)) for i in items).items()))

    manifest = OrderedDict()
    manifest["manifest_version"] = "experimental-v1"
    manifest["status"] = (
        "EXPERIMENTAL — NOT LIVE CANON. Not merged, not accepted, not project knowledge. "
        "Produced on branch work/canon-parallel-books-qa-experimental."
    )
    manifest["generated_from"] = EXP_REL
    manifest["totals"] = {
        "sources_processed": len(dirs),
        "qa_items": len(items),
        "requires_application": sum(1 for i in items if i.get("requires_application") is True),
        "source_knowledge_objects": sum(v["source_knowledge_objects"] for v in per_source.values()),
        "source_concept_systems": sum(v["source_concept_systems"] for v in per_source.values()),
        "operational_bindings": sum(v["operational_bindings"] for v in per_source.values()),
        "ontology_terms": sum(v["ontology_terms"] for v in per_source.values()),
    }
    manifest["counts_by_source"] = per_source
    manifest["counts_by_answer_type"] = tally("answer_type")
    manifest["counts_by_difficulty"] = tally("difficulty")
    manifest["counts_by_knowledge_type"] = tally("knowledge_type")
    manifest["counts_by_requires_application"] = tally("requires_application")

    # per-source cross-tabs, so a reader can see each bank's own shape
    cross = OrderedDict()
    for sd in dirs:
        sub = [i for i in items if i.get("source_id") == sd]
        cross[sd] = {
            "answer_type": OrderedDict(sorted(Counter(str(i.get("answer_type")) for i in sub).items())),
            "difficulty": OrderedDict(sorted(Counter(str(i.get("difficulty")) for i in sub).items())),
            "knowledge_type": OrderedDict(sorted(Counter(str(i.get("knowledge_type")) for i in sub).items())),
        }
    manifest["counts_by_source_and_dimension"] = cross
    manifest["qa_items"] = items

    out = os.path.join(exp, "QA-MANIFEST.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    print(f"wrote {out}")
    print(f"  sources: {len(dirs)}   qa_items: {len(items)}   "
          f"requires_application: {manifest['totals']['requires_application']}")
    for sd, v in per_source.items():
        print(f"  {sd:<42} qa={v['qa_count']:<4} sk={v['source_knowledge_objects']:<4} "
              f"bnd={v['operational_bindings']:<3} app={v['requires_application']}")

    # refresh the counts block in README.md
    readme = os.path.join(exp, "README.md")
    if os.path.exists(readme):
        t = manifest["totals"]
        lines = [
            "| Measure | Count |",
            "|---|---|",
            f"| Sources processed | **{t['sources_processed']}** |",
            f"| Material examined | **{MATERIAL_EXAMINED}** |",
            f"| Source Knowledge objects | **{t['source_knowledge_objects']}** |",
            f"| Source Concept Systems | **{t['source_concept_systems']}** |",
            f"| Proposed operational bindings | **{t['operational_bindings']}** |",
            f"| Ontology terms | **{t['ontology_terms']}** |",
            f"| **Q&A pairs** | **{t['qa_items']}** |",
            "| — of which require application | **{}** ({}) |".format(
                t["requires_application"],
                f"{t['requires_application'] / t['qa_items'] * 100:.0f}%" if t["qa_items"] else "n/a",
            ),
            "",
            "Per source:",
            "",
            "| Source | Source Knowledge | Concept Systems | Bindings | Q&A | Application |",
            "|---|---|---|---|---|---|",
        ]
        for sd, v in per_source.items():
            pct = (v["requires_application"] / v["qa_count"] * 100) if v["qa_count"] else 0
            lines.append(
                f"| `{sd}` | {v['source_knowledge_objects']} | {v['source_concept_systems']} | "
                f"{v['operational_bindings']} | **{v['qa_count']}** | "
                f"{v['requires_application']} ({pct:.0f}%) |"
            )
        lines += [
            "",
            "Breakdowns by answer type, difficulty and knowledge type are in `QA-MANIFEST.json` "
            "(`counts_by_answer_type`, `counts_by_difficulty`, `counts_by_knowledge_type`, "
            "`counts_by_source_and_dimension`).",
        ]
        block = "\n".join(lines)
        with open(readme, encoding="utf-8") as fh:
            body = fh.read()
        start, end = "<!-- COUNTS:BEGIN -->", "<!-- COUNTS:END -->"
        if start in body and end in body:
            pre = body.split(start)[0]
            post = body.split(end)[1]
            with open(readme, "w", encoding="utf-8") as fh:
                fh.write(pre + start + "\n" + block + "\n" + end + post)
            print("  refreshed counts block in README.md")

    # refresh qa_count in SOURCE-STATUS.csv if it exists
    csv_path = os.path.join(exp, "SOURCE-STATUS.csv")
    if os.path.exists(csv_path):
        with open(csv_path, newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        fields = list(rows[0].keys()) if rows else []
        changed = 0
        for r in rows:
            sid = r.get("source", "")
            if sid in per_source:
                new = str(per_source[sid]["qa_count"])
                if r.get("qa_count") != new:
                    r["qa_count"] = new
                    changed += 1
        if changed:
            with open(csv_path, "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=fields)
                w.writeheader()
                w.writerows(rows)
            print(f"  refreshed qa_count for {changed} row(s) in SOURCE-STATUS.csv")
    return 0


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else
                  os.path.abspath(os.path.join(here, "..", "..", ".."))))
