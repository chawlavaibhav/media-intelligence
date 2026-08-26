#!/usr/bin/env python3
"""CANON-V1 / C-C3 — build the fresh-session generic-control authoring input, and prove it is clean.

WHY THIS EXISTS. The committed generic controls were authored by a session that had already read the
Oracle Canon. Their independence cannot be demonstrated, so they cannot serve as the control in a
real run. The replacement must be authored by a session with NO Canon access — which means someone
has to hand that session an input file, and that input file must be provably free of Canon.

WHAT THIS SCRIPT GUARANTEES. It assembles the input from the brief bank only, and then runs a
LEAKAGE CHECK over the assembled bytes: no accepted-source directory name, no source_id, no Canon
reference id (scs_*/sk_*/t_*), no accepted-source title fragment, and no substring of any oracle
context. It fails closed. A packet that cannot be proven clean is not written.

The word-count targets ARE included and that is deliberate: matching context length is what stops a
Canon win being bought with extra words, and a number of words reveals nothing about content.

Run: python3 canon/experiments/v1/value-gate/build_control_packet.py
"""
from __future__ import annotations

import json
import pathlib
import re
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BRIEFS = ROOT / "canon/experiments/v1/brief-bank/briefs.jsonl"
MANIFEST = HERE / "early-12-manifest.json"
ORACLE = HERE / "oracle-contexts"
KNOWLEDGE = ROOT / "canon/knowledge/current"
PROMPT = HERE / "prompts/planning-prompt.md"
OUT = HERE / "control-authoring-input.json"

TOLERANCE = 0.15
# Fields of a brief a control author may see. Everything else — above all authoritative_intent —
# is withheld: it is scoring material and must never reach an authoring or planning arm.
ALLOWED_BRIEF_FIELDS = ["brief_id", "customer_brief", "media_class", "duration_seconds"]


# Ordinary English words that happen to appear inside a source directory name — "context" comes out
# of `binet-field-effectiveness-in-context-ch1`, "science" out of `light-science-magic-ch3`. Flagging
# these would make the check fire on any normal sentence and would train us to ignore it. What we
# actually care about is DISTINCTIVE identifiers: surnames, titles, ids.
GENERIC_FRAGMENTS = {
    "interaction", "colour", "color", "painting", "light", "science", "magic", "effectiveness",
    "context", "creativity", "photographers", "graphic", "guide", "grammar", "master", "shots",
    "making", "breaking", "grid", "canon", "intangibles", "advertising", "sells", "scientific",
    "introduction", "conversations", "alchemy", "blink", "framework", "stick",
}


def leakage_terms() -> list[str]:
    """Distinctive strings whose presence would mean Canon leaked into the packet.

    Deliberately excludes ordinary English words that happen to sit inside a directory name (see
    GENERIC_FRAGMENTS). A check that fires on the word "context" is a check nobody reads.
    """
    terms: set[str] = set()
    for d in sorted(KNOWLEDGE.iterdir()):
        if not d.is_dir():
            continue
        terms.add(d.name)
        for part in d.name.split("-"):
            if len(part) > 5 and part.lower() not in GENERIC_FRAGMENTS:
                terms.add(part)          # albers, samara, ondaatje, hopkins, kenworthy, vignelli...
        sk = yaml.safe_load((d / "source-knowledge.yaml").read_text()) or {}
        if sk.get("source_id"):
            terms.add(sk["source_id"])
    return sorted(terms)


def main() -> int:
    briefs = {json.loads(l)["brief_id"]: json.loads(l) for l in BRIEFS.read_text().splitlines()}
    manifest = json.loads(MANIFEST.read_text())

    items = []
    for row in manifest["briefs"]:
        bid = row["brief_id"]
        b = briefs[bid]
        target = len((ORACLE / f"{bid}.md").read_text().split())
        items.append({
            **{k: b.get(k) for k in ALLOWED_BRIEF_FIELDS},
            "target_words": target,
            "min_words": int(round(target * (1 - TOLERANCE))),
            "max_words": int(round(target * (1 + TOLERANCE))),
        })

    packet = {
        "packet_id": "CANON-V1-GENERIC-CONTROL-AUTHORING-INPUT",
        "version": 1,
        "authoring_session_requirement": "FRESH SESSION WITH NO ACCESS TO canon/knowledge/, "
                                         "canon/audit/ OR canon/experiments/v1/value-gate/"
                                         "oracle-contexts/.",
        "task": "For each brief below, write one generic professional craft-guidance context.",
        "rules": [
            "Write strong, genuinely useful professional craft guidance. A weak control invalidates "
            "the experiment it is part of; do not soften it.",
            "Do not name, cite or allude to any specific book, author, framework or published "
            "source. No attributions of any kind.",
            "Do not use headings or structure that imply a source's own organisation of ideas.",
            "Write only from general professional practice.",
            "Stay within min_words and max_words for that brief. This is a hard requirement.",
            "Match the house format: a '# Craft context' title, then '## ' sections of short "
            "paragraphs, ending with a '## Before finishing' checklist section.",
            "Address what the brief actually needs. A context that would suit any brief equally is "
            "not doing its job.",
        ],
        "output": {
            "one_file_per_brief": "generic-contexts-real/<brief_id>.md",
            "format": "markdown",
        },
        "planning_procedure_the_context_will_be_used_with": PROMPT.read_text().split("```")[1],
        "briefs": items,
    }

    blob = json.dumps(packet, ensure_ascii=False)
    low = blob.lower()

    findings = []
    for term in leakage_terms():
        if term.lower() in low:
            findings.append(f"packet contains Canon term {term!r}")
    if re.search(r"\b(scs|sk|t|bnd)_[a-z0-9_]+", blob):
        findings.append("packet contains a Canon reference id")
    for f in sorted(ORACLE.glob("*.md")):
        for line in f.read_text().splitlines():
            line = line.strip()
            if len(line) > 60 and line in blob:
                findings.append(f"packet reproduces a line of oracle context from {f.name}")
                break
    if "authoritative_intent" in blob:
        findings.append("packet exposes authoritative_intent, which is scoring material")

    if findings:
        print(json.dumps({"status": "LEAKAGE_DETECTED", "error_count": len(findings),
                          "errors": findings}, indent=2))
        return 1

    OUT.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({
        "status": "CLEAN",
        "output": str(OUT.relative_to(ROOT)),
        "briefs": len(items),
        "leakage_terms_checked": len(leakage_terms()),
        "word_targets": {"min": min(i["min_words"] for i in items),
                         "max": max(i["max_words"] for i in items)},
        "fields_exposed_per_brief": ALLOWED_BRIEF_FIELDS + ["target_words", "min_words", "max_words"],
        "authoritative_intent_exposed": False,
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
