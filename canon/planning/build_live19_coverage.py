#!/usr/bin/env python3
"""CANON-V1 / C1 — build the live-19 coverage rebaseline.

WHAT THIS DOES, in plain terms. It takes the authored judgement about which accepted sources
contribute to which knowledge domain (`live19_domain_map.yaml`) and joins it to facts computed
directly from committed repository artifacts: how many knowledge objects each source holds, which
product consumers its knowledge is bound to, and — critically — how many INDEPENDENT intellectual
origins actually stand behind each domain.

WHY INDEPENDENCE IS COMPUTED AND NOT AUTHORED. Two books can look independent (different authors,
publishers, years) and still be one intellectual origin. The Canon has learned this twice: Grammar
of the Shot and Grammar of the Edit are companion volumes, and The Conversations is substantially
Walter Murch speaking while the corpus already holds Murch's own book. Counting titles would call
those four sources four origins. They are two. This script therefore never counts titles: it calls
`independent_origins_ok()` from the committed Audit Gate validator, which fails closed.

The greedy maximum-independent-set below is deliberate and stated: it reports the LARGEST set of
mutually independent contributors, and because it is greedy it can only ever UNDER-report, never
over-report. Under-reporting independence is the safe direction.

Run: python3 canon/planning/build_live19_coverage.py
"""
from __future__ import annotations

import collections
import importlib.util
import json
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
KNOWLEDGE = ROOT / "canon/knowledge/current"
RECORDS = ROOT / "canon/audit/records"
PLANNING = ROOT / "canon/planning"

# The ten product-facing knowledge packs required by the runbook, and the diagnostic domains that
# roll up into each. Every one of the 56 domains appears in exactly one pack.
PACKS = {
    "composition_and_attention": ["A01", "A02", "A03", "A04", "A12", "E02"],
    "typography_and_copy": ["A06", "A07", "C12", "A14"],
    "product_appearance": ["A13", "A10", "A09", "A11", "A08"],
    "colour_and_visual_register": ["A05", "B13", "D06"],
    "camera_and_spatial_grammar": ["B01", "B02", "B03", "B08"],
    "editing_pacing_and_short_form": ["B04", "B05", "B06", "B09", "B10", "B11", "B12"],
    "commercial_communication": ["C01", "C02", "C03", "C04", "C05", "C07", "C09", "C11", "C14"],
    "concept_and_distinctiveness": ["B07", "C06", "C08", "C10", "D01", "D02", "D03"],
    "indian_indic_context": ["C13"],
    "critique_and_effectiveness": ["D04", "D05", "D07", "E01", "E03", "E04", "E05", "E06", "E07", "E08"],
}

BINDING_CONSUMERS = ["creative_ir", "evaluation", "benchmark", "production", "governance"]


def load_validator():
    """Import the committed Audit Gate validator so independence uses the authoritative rule."""
    path = ROOT / "canon/validation/validate_audit_gate_v02.py"
    spec = importlib.util.spec_from_file_location("audit_gate_v02", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_sources() -> dict:
    """Per-source object/system/term/binding counts, read from the committed extraction."""
    out = {}
    for d in sorted(KNOWLEDGE.iterdir()):
        if not d.is_dir():
            continue
        sk = yaml.safe_load((d / "source-knowledge.yaml").read_text()) or {}
        scs = yaml.safe_load((d / "source-concept-systems.yaml").read_text()) or {}
        ont = yaml.safe_load((d / "ontology-mappings.yaml").read_text()) or {}
        bind = yaml.safe_load((d / "operational-bindings.yaml").read_text()) or {}
        targets = collections.Counter(
            b.get("target_type") for b in (bind.get("operational_bindings") or [])
        )
        out[d.name] = {
            "source_id": sk.get("source_id"),
            "objects": len(sk.get("source_knowledge") or []),
            "systems": len(scs.get("source_concept_systems") or []),
            "terms": len(ont.get("terms") or []),
            "bindings": sum(targets.values()),
            "binding_targets": dict(targets),
        }
    return out


def load_records() -> dict:
    return {p.name: yaml.safe_load(p.read_text()) for p in sorted(RECORDS.glob("*.audit.yaml"))}


def max_independent_set(source_ids: list[str], records: dict, vmod) -> tuple[list[str], list[str]]:
    """Greedy largest set of mutually independent origins, plus the blocked pairs found.

    Greedy, so it can under-report and never over-report. Independence is decided ONLY by
    `independent_origins_ok()` from the committed validator.
    """
    blocked = []
    for i, a in enumerate(source_ids):
        for b in source_ids[i + 1:]:
            ok, reason = vmod.independent_origins_ok(a, b, records)
            if not ok:
                blocked.append(reason)
    chosen: list[str] = []
    for sid in source_ids:
        if all(vmod.independent_origins_ok(sid, c, records)[0] for c in chosen):
            chosen.append(sid)
    return chosen, blocked


def coverage_state(entry: dict, contributors: list[str], independent: int) -> tuple[str, str]:
    """Compute the inventory state. Authored overrides win and must carry a reason."""
    override = entry.get("state_override")
    if override:
        return override["state"], override["reason"].strip()
    if not contributors:
        return "absent", "no accepted source contributes knowledge to this domain"
    if independent >= 2:
        return "present_multi_origin", f"{independent} independent origins among {len(contributors)} contributors"
    return "present_single_origin", f"1 independent origin among {len(contributors)} contributors"


def main() -> int:
    vmod = load_validator()
    sources = load_sources()
    records = load_records()
    dirmap = {d: v["source_id"] for d, v in sources.items()}

    doc = yaml.safe_load((PLANNING / "live19_domain_map.yaml").read_text())
    domains = doc["domains"]

    errors = []
    seen_ids = set()
    for e in domains:
        if e["id"] in seen_ids:
            errors.append(f"duplicate domain id {e['id']}")
        seen_ids.add(e["id"])
        for c in e.get("contributors", []) + e.get("incidental_only", []):
            if c not in dirmap:
                errors.append(f"{e['id']} names unknown source directory {c!r}")

    packed = {d for ds in PACKS.values() for d in ds}
    for e in domains:
        if e["id"] not in packed:
            errors.append(f"domain {e['id']} belongs to no product pack")
    for d in packed:
        if d not in seen_ids:
            errors.append(f"pack references unknown domain {d}")
    dupe_packed = [d for d, n in collections.Counter(
        x for ds in PACKS.values() for x in ds).items() if n > 1]
    for d in dupe_packed:
        errors.append(f"domain {d} appears in more than one pack")

    if errors:
        print(json.dumps({"error_count": len(errors), "errors": errors}, indent=2))
        return 1

    out_domains = []
    for e in domains:
        contributors = e.get("contributors", [])
        sids = [dirmap[c] for c in contributors]
        chosen, blocked = max_independent_set(sids, records, vmod)
        state, basis = coverage_state(e, contributors, len(chosen))
        consumers = collections.Counter()
        objects = 0
        for c in contributors:
            objects += sources[c]["objects"]
            for t, n in sources[c]["binding_targets"].items():
                consumers[t] += n
        out_domains.append({
            "id": e["id"],
            "name": e["name"],
            "section": e["section"],
            "importance": e["importance"],
            "pack": next(p for p, ds in PACKS.items() if e["id"] in ds),
            "contributors": contributors,
            "contributor_count": len(contributors),
            "independent_origin_count": len(chosen),
            "independent_origin_set": chosen,
            "dependence_blocks": sorted(set(blocked)),
            "concept_systems_exist": any(sources[c]["systems"] > 0 for c in contributors),
            # Upper bound only: the TOTAL objects held by every contributing source, not a count of
            # objects on this topic. A source contributes to several domains, so these do not sum to
            # 580. Use it to tell a thin contribution from a deep one, never as a coverage score.
            "contributing_source_objects_upper_bound": objects,
            "binding_state": ([t for t in BINDING_CONSUMERS if consumers.get(t)] or ["none"]),
            "coverage_state": state,
            "coverage_state_basis": basis,
            "incidental_only": e.get("incidental_only", []),
            "cross_stream_relevance": e.get("cross_stream_relevance"),
            "gap": " ".join(e["gap"].split()),
        })

    packs_out = {}
    for pack, ids in PACKS.items():
        rows = [d for d in out_domains if d["id"] in ids]
        contribs = sorted({c for r in rows for c in r["contributors"]})
        chosen, _ = max_independent_set([dirmap[c] for c in contribs], records, vmod)
        crit = [r for r in rows if r["importance"] == "critical"]
        crit_absent = [r["id"] for r in crit if r["coverage_state"] == "absent"]
        crit_limited = [r["id"] for r in crit
                        if r["coverage_state"] in ("present_but_application_unbound",
                                                   "representation_or_evidence_limited")]
        packs_out[pack] = {
            "domains": ids,
            "domain_count": len(ids),
            "contributors": contribs,
            "contributor_count": len(contribs),
            "independent_origin_count": len(chosen),
            "critical_domains": [r["id"] for r in crit],
            "critical_absent": crit_absent,
            "critical_limited": crit_limited,
            "pack_state": ("absent" if not contribs
                           else "critical_hole" if crit_absent
                           else "critical_limited" if crit_limited
                           else "covered"),
        }

    live_ids = [v["source_id"] for v in sources.values()]
    all_chosen, _ = max_independent_set(live_ids, records, vmod)
    summary = {
        "accepted_sources": len(sources),
        "audit_records": len(records),
        "audit_status_complete": sum(1 for r in records.values() if r.get("audit_status") == "complete"),
        "total_objects": sum(v["objects"] for v in sources.values()),
        "total_systems": sum(v["systems"] for v in sources.values()),
        "total_terms": sum(v["terms"] for v in sources.values()),
        "total_bindings": sum(v["bindings"] for v in sources.values()),
        "corpus_independent_origins": len(all_chosen),
        "domains_total": len(out_domains),
        "packs_total": len(packs_out),
        "by_state": dict(collections.Counter(d["coverage_state"] for d in out_domains)),
        "by_importance": dict(collections.Counter(d["importance"] for d in out_domains)),
        "critical_absent": [d["id"] for d in out_domains
                            if d["importance"] == "critical" and d["coverage_state"] == "absent"],
        "critical_limited": [d["id"] for d in out_domains
                             if d["importance"] == "critical"
                             and d["coverage_state"] in ("present_but_application_unbound",
                                                         "representation_or_evidence_limited")],
        "sources_contributing_to_no_domain": sorted(
            d for d in sources if not any(d in x["contributors"] for x in out_domains)),
    }

    payload = {"summary": summary, "sources": sources, "packs": packs_out, "domains": out_domains}
    (PLANNING / "CANON-V1-LIVE19-COVERAGE.yaml").write_text(
        "# GENERATED by canon/planning/build_live19_coverage.py — do not hand-edit.\n"
        "# Authored input: canon/planning/live19_domain_map.yaml\n"
        "# Mechanical input: canon/knowledge/current, canon/audit/records,\n"
        "#                   canon/validation/validate_audit_gate_v02.py (independence rule)\n"
        + yaml.dump(payload, sort_keys=False, width=100, allow_unicode=True)
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
