#!/usr/bin/env python3
"""CANON-V1 / C2 — verify the early-12 selection and render Canon oracle contexts.

THE POINT OF RENDERING RATHER THAN WRITING. Every sentence of Canon in an oracle context is pulled
from the committed extraction by id. Nothing is paraphrased by hand. That means the Oracle arm of the
value gate cannot be accidentally strengthened by a worker writing a better version of what a source
said — a failure mode that would invalidate the whole comparison.

It also fails closed on a reference to an id that does not exist, and on any source whose Audit Gate
record is not `complete`. The gate governs use: unaudited material may not be used for downstream
consumption, and an oracle context IS downstream consumption.

Run: python3 canon/experiments/v1/value-gate/build_oracle_contexts.py
"""
from __future__ import annotations

import collections
import json
import pathlib
import sys

import yaml

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
KNOWLEDGE = ROOT / "canon/knowledge/current"
RECORDS = ROOT / "canon/audit/records"
SEL = HERE / "oracle-selection.yaml"
OUTDIR = HERE / "oracle-contexts"
MANIFEST = HERE / "early-12-manifest.json"
BRIEFS = ROOT / "canon/experiments/v1/brief-bank/briefs.jsonl"
COVERAGE = ROOT / "canon/planning/CANON-V1-LIVE19-COVERAGE.yaml"


def load_corpus():
    systems, objects, owner, audited = {}, {}, {}, {}
    for d in sorted(KNOWLEDGE.iterdir()):
        if not d.is_dir():
            continue
        sk = yaml.safe_load((d / "source-knowledge.yaml").read_text()) or {}
        scs = yaml.safe_load((d / "source-concept-systems.yaml").read_text()) or {}
        for s in (scs.get("source_concept_systems") or []):
            systems[s["scs_id"]] = s
            owner[s["scs_id"]] = d.name
        for o in (sk.get("source_knowledge") or []):
            objects[o["sk_id"]] = o
            owner[o["sk_id"]] = d.name
    for p in RECORDS.glob("*.audit.yaml"):
        r = yaml.safe_load(p.read_text())
        audited[r["knowledge_dir"].rstrip("/").split("/")[-1]] = r.get("audit_status")
    return systems, objects, owner, audited


def words(text: str) -> int:
    return len(text.split())


def render(entry, systems, objects, owner) -> tuple[str, list[dict]]:
    lines = ["# Canon context", ""]
    refs = []
    for sid in entry["oracle"].get("systems", []):
        s = systems[sid]
        lines.append(f"## {s['label'].replace('_', ' ')}")
        lines.append(f"_Source: {owner[sid]} · {sid}_")
        lines.append("")
        lines.append(" ".join((s.get("description") or "").split()))
        wsc = (s.get("whole_system_claim") or {}).get("text")
        if wsc:
            lines.append("")
            lines.append(" ".join(wsc.split()))
        lines.append("")
        refs.append({"ref": sid, "kind": "concept_system", "source_dir": owner[sid],
                     "label": s["label"],
                     "reason": " ".join(entry["oracle"]["inclusion_reasons"][sid].split())})
    for oid in entry["oracle"].get("objects", []):
        o = objects[oid]
        lines.append(f"## {o.get('concept_label', '').replace('_', ' ')}")
        lines.append(f"_Source: {owner[oid]} · {oid}_")
        lines.append("")
        lines.append(" ".join((o.get("claim") or "").split()))
        lines.append("")
        refs.append({"ref": oid, "kind": "source_knowledge", "source_dir": owner[oid],
                     "label": o.get("concept_label"),
                     "reason": " ".join(entry["oracle"]["inclusion_reasons"][oid].split())})
    for ex in entry["oracle"].get("deliberately_excluded", []):
        refs.append({"ref": None, "kind": "deliberate_exclusion",
                     "reason": " ".join(ex["reason"].split())})
    return "\n".join(lines).rstrip() + "\n", refs


def main() -> int:
    systems, objects, owner, audited = load_corpus()
    sel = yaml.safe_load(SEL.read_text())
    entries = sel["early_12"]
    briefs = {json.loads(l)["brief_id"]: json.loads(l) for l in BRIEFS.read_text().splitlines()}
    cov = yaml.safe_load(COVERAGE.read_text())
    all_packs = set(cov["packs"])

    errors = []
    if len(entries) != 12:
        errors.append(f"expected 12 early-gate briefs, found {len(entries)}")

    for e in entries:
        bid = e["brief_id"]
        if bid not in briefs:
            errors.append(f"{bid}: not present in the 30-brief bank")
            continue
        used = e["oracle"].get("systems", []) + e["oracle"].get("objects", [])
        if not used:
            errors.append(f"{bid}: oracle context is empty")
        for r in used:
            if r not in systems and r not in objects:
                errors.append(f"{bid}: reference {r!r} does not exist in the accepted corpus")
                continue
            src = owner[r]
            if audited.get(src) != "complete":
                errors.append(f"{bid}: {r} comes from {src}, whose audit_status is "
                              f"{audited.get(src)!r}; only audited sources may be used")
            if r not in e["oracle"]["inclusion_reasons"]:
                errors.append(f"{bid}: reference {r} has no logged inclusion reason")
        for r in e["oracle"]["inclusion_reasons"]:
            if r not in used:
                errors.append(f"{bid}: inclusion reason logged for unused reference {r}")

    chosen = [briefs[e["brief_id"]] for e in entries if e["brief_id"] in briefs]
    n_static = sum(1 for b in chosen if b["media_class"] == "static")
    n_video = sum(1 for b in chosen if b["media_class"] == "video")
    n_hi = sum(1 for b in chosen if b["language_condition"] == "hindi_devanagari_primary")
    n_hg = sum(1 for b in chosen if b["language_condition"] == "hinglish_mixed")
    roles = collections.Counter(e["gate_role"] for e in entries)
    packs_hit = {p for b in chosen for p in b["tags"]["knowledge_packs_required"]}

    for label, got, need in (("static", n_static, 3), ("video", n_video, 5),
                             ("hindi/devanagari", n_hi, 3), ("hinglish/mixed", n_hg, 3),
                             ("gap_probe", roles.get("gap_probe", 0), 2),
                             ("coverage_probe", roles.get("coverage_probe", 0), 4)):
        if got < need:
            errors.append(f"early-12 has {got} {label} briefs, runbook requires >= {need}")
    missing_packs = sorted(all_packs - packs_hit)
    if missing_packs:
        errors.append(f"early-12 does not exercise these packs at all: {missing_packs}")
    if sel["meta"].get("planning_outputs_generated_so_far") != 0:
        errors.append("selection must be made before any planning output exists")

    if errors:
        print(json.dumps({"error_count": len(errors), "errors": errors}, indent=2))
        return 1

    OUTDIR.mkdir(parents=True, exist_ok=True)
    manifest = {"task": "CANON-V1 / C2", "selected_before_any_generation": True,
                "planning_outputs_generated": 0, "briefs": []}
    for e in entries:
        bid = e["brief_id"]
        body, refs = render(e, systems, objects, owner)
        (OUTDIR / f"{bid}.md").write_text(body)
        manifest["briefs"].append({
            "brief_id": bid,
            "scenario_family": briefs[bid]["scenario_family"],
            "media_class": briefs[bid]["media_class"],
            "language_condition": briefs[bid]["language_condition"],
            "specification_quality": briefs[bid]["tags"]["specification_quality"],
            "knowledge_packs_required": briefs[bid]["tags"]["knowledge_packs_required"],
            "gate_role": e["gate_role"],
            "probes_gaps": e.get("probes_gaps", []),
            "why_selected": " ".join(e["why_selected"].split()),
            "oracle_context_file": f"oracle-contexts/{bid}.md",
            "oracle_context_words": words(body),
            "canon_refs": refs,
            "lineage_note": " ".join(e["lineage_note"].split()) if e.get("lineage_note") else None,
            "scoring_note": " ".join(e["scoring_note"].split()) if e.get("scoring_note") else None,
        })
    wc = [b["oracle_context_words"] for b in manifest["briefs"]]
    manifest["oracle_word_count"] = {
        "min": min(wc), "max": max(wc), "mean": round(sum(wc) / len(wc), 1), "total": sum(wc)}
    manifest["balance"] = {
        "static": n_static, "video": n_video,
        "english_primary": sum(1 for b in chosen if b["language_condition"] == "english_primary"),
        "hindi_devanagari_primary": n_hi, "hinglish_mixed": n_hg,
        "gap_probe": roles.get("gap_probe", 0), "coverage_probe": roles.get("coverage_probe", 0),
        "distinct_families": len({b["scenario_family"] for b in chosen}),
        "packs_exercised": sorted(packs_hit),
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"briefs": len(manifest["briefs"]),
                      "balance": manifest["balance"],
                      "oracle_word_count": manifest["oracle_word_count"],
                      "distinct_canon_refs": len({r["ref"] for b in manifest["briefs"]
                                                  for r in b["canon_refs"] if r["ref"]}),
                      "sources_drawn_on": len({r["source_dir"] for b in manifest["briefs"]
                                               for r in b["canon_refs"] if r.get("source_dir")})},
                     indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
