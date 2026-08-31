#!/usr/bin/env python3
"""Canon repair / REP-01 — build the live-24 coverage rebaseline.

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

SUPERSEDES canon/planning/build_live19_coverage.py, which is retained untouched together with its
outputs (frozen decision: supersede, never mutate). This script is that generator re-based on the
live-24 corpus: it reads the authored judgement in `live24_domain_map.yaml` (the live19 map plus
authored entries for the five CANON-014 India-context sources) and joins it to facts computed
directly from committed repository artifacts. Run it twice and the outputs are byte-identical:
nothing here depends on time, environment or ordering beyond the committed files.

Differences from the live19 generator, in full:
  1. Input map is live24_domain_map.yaml; outputs are CANON-V1-LIVE24-COVERAGE.yaml/.md.
  2. The authored state_override value `present_but_operationally_limited` (used by C13) is
     counted in `critical_limited` at both domain and pack level, so a pack holding only such
     domains reads `critical_limited`, never `covered`. Counting it as covered would overstate
     the Canon — the exact error the live19 map's C09 note warns against.
  3. A deterministic Markdown summary is emitted next to the YAML so human review does not
     require parsing the YAML.

WHY INDEPENDENCE IS COMPUTED AND NOT AUTHORED — unchanged from the live19 generator. Two books can
look independent and still be one intellectual origin (companion volumes; a shared primary
informant). Independence between any two sources is decided ONLY by `independent_origins_ok()`
from the committed Audit Gate validator, which fails closed.

INDEPENDENT-ORIGIN COUNTING. Exact exhaustive maximisation up to EXACT_MAX_NODES nodes, greedy
lower bound above that, labelled as such. NOTE for the live-24 corpus: 24 accepted sources exceed
EXACT_MAX_NODES, so the CORPUS-level count is reported with method `greedy_lower_bound` — an
honest under-report, never a false maximum. Per-domain and per-pack counts stay exact wherever
their contributor sets are small enough, which is everywhere today.

Run: python3 canon/planning/build_live24_coverage.py
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

STATUS_LINE = (
    "# STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;\n"
    "# coordination/CONTROL-STATE.md governs.\n"
)

# The ten product-facing knowledge packs required by the runbook, and the diagnostic domains that
# roll up into each. Every one of the 56 domains appears in exactly one pack. Unchanged from the
# live19 generator: the pack taxonomy is a Controller artifact and is not this worker's to edit.
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

# Authored override states that mean "present but not usable as-is". A domain in one of these
# states makes its pack `critical_limited` when the domain is critical.
LIMITED_STATES = (
    "present_but_application_unbound",
    "representation_or_evidence_limited",
    "present_but_operationally_limited",
)


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


EXACT_MAX_NODES = 22  # 2**22 subsets is still tractable; above this, refuse and say so.


def independent_origin_count(source_ids: list[str], records: dict, vmod):
    """Maximum set of mutually independent origins, plus the dependence blocks found.

    Identical in rule to the live19 generator: pairwise independence comes ONLY from
    `independent_origins_ok()`; this function only decides how many can be held at once.
    `method` is "exact_exhaustive" for a proven maximum, "greedy_lower_bound" otherwise.
    """
    blocked = []
    pair_ok: dict[tuple[str, str], bool] = {}
    for i, a in enumerate(source_ids):
        for b in source_ids[i + 1:]:
            ok, reason = vmod.independent_origins_ok(a, b, records)
            pair_ok[(a, b)] = pair_ok[(b, a)] = ok
            if not ok:
                blocked.append(reason)

    def is_independent_set(members: list[str]) -> bool:
        for i, a in enumerate(members):
            for b in members[i + 1:]:
                if not pair_ok[(a, b)]:
                    return False
        return True

    greedy: list[str] = []
    for sid in source_ids:
        if all(pair_ok[(sid, c)] for c in greedy):
            greedy.append(sid)

    n = len(source_ids)
    if n > EXACT_MAX_NODES:
        return greedy, blocked, "greedy_lower_bound"

    best = greedy
    for mask in range(1 << n):
        if bin(mask).count("1") <= len(best):
            continue
        subset = [source_ids[i] for i in range(n) if mask >> i & 1]
        if is_independent_set(subset):
            best = subset
    assert len(greedy) <= len(best), "greedy exceeded the exhaustive maximum"
    return best, blocked, "exact_exhaustive"


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


def render_markdown(payload: dict) -> str:
    """Deterministic human-readable summary of the coverage yaml."""
    s = payload["summary"]
    lines = [
        "<!-- GENERATED by canon/planning/build_live24_coverage.py — do not hand-edit. -->",
        "<!-- STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;",
        "     coordination/CONTROL-STATE.md governs. -->",
        "",
        "# CANON-V1 LIVE-24 coverage — generated summary",
        "",
        "Supersedes `CANON-V1-LIVE19-COVERAGE.md` (frozen, untouched). Authored input:",
        "`canon/planning/live24_domain_map.yaml`. Mechanical inputs: `canon/knowledge/current`,",
        "`canon/audit/records`, `canon/validation/validate_audit_gate_v02.py` (independence rule).",
        "",
        "## Corpus",
        "",
        f"- accepted sources: **{s['accepted_sources']}** · audit records: {s['audit_records']}"
        f" ({s['audit_status_complete']} complete)",
        f"- knowledge objects: **{s['total_objects']}** · concept systems: {s['total_systems']}"
        f" · ontology terms: {s['total_terms']} · bindings: {s['total_bindings']}",
        f"- corpus independent origins: {s['corpus_independent_origins']}"
        f" (method: {s['corpus_independent_origins_method']})",
        "",
        "## Packs",
        "",
        "| pack | state | contributors | independent origins | critical absent | critical limited |",
        "|---|---|---|---|---|---|",
    ]
    for name, p in payload["packs"].items():
        lines.append(
            f"| {name} | {p['pack_state']} | {p['contributor_count']} |"
            f" {p['independent_origin_count']} ({p['independent_origin_count_method']}) |"
            f" {', '.join(p['critical_absent']) or '—'} | {', '.join(p['critical_limited']) or '—'} |"
        )
    lines += [
        "",
        "## Domain states",
        "",
        "| state | domains |",
        "|---|---|",
    ]
    by_state = collections.defaultdict(list)
    for d in payload["domains"]:
        by_state[d["coverage_state"]].append(d["id"])
    for state in sorted(by_state):
        lines.append(f"| {state} | {', '.join(by_state[state])} |")
    lines += [
        "",
        f"Critical absent: {', '.join(s['critical_absent']) or '—'}.",
        f"Critical limited: {', '.join(s['critical_limited']) or '—'}.",
        "",
        "The authored assignments in the domain map are Canon judgements, validated for",
        "completeness only; they are not machine-discovered facts and must not be cited as such.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    vmod = load_validator()
    sources = load_sources()
    records = load_records()
    dirmap = {d: v["source_id"] for d, v in sources.items()}

    doc = yaml.safe_load((PLANNING / "live24_domain_map.yaml").read_text())
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
        chosen, blocked, method = independent_origin_count(sids, records, vmod)
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
            "independent_origin_count_method": method,
            "independent_origin_set": chosen,
            "dependence_blocks": sorted(set(blocked)),
            "concept_systems_exist": any(sources[c]["systems"] > 0 for c in contributors),
            # Upper bound only: the TOTAL objects held by every contributing source, not a count of
            # objects on this topic. A source contributes to several domains, so these do not sum
            # to 677. Use it to tell a thin contribution from a deep one, never as a coverage score.
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
        chosen, _, pack_method = independent_origin_count(
            [dirmap[c] for c in contribs], records, vmod)
        crit = [r for r in rows if r["importance"] == "critical"]
        crit_absent = [r["id"] for r in crit if r["coverage_state"] == "absent"]
        crit_limited = [r["id"] for r in crit if r["coverage_state"] in LIMITED_STATES]
        packs_out[pack] = {
            "domains": ids,
            "domain_count": len(ids),
            "contributors": contribs,
            "contributor_count": len(contribs),
            "independent_origin_count": len(chosen),
            "independent_origin_count_method": pack_method,
            "critical_domains": [r["id"] for r in crit],
            "critical_absent": crit_absent,
            "critical_limited": crit_limited,
            "pack_state": ("absent" if not contribs
                           else "critical_hole" if crit_absent
                           else "critical_limited" if crit_limited
                           else "covered"),
        }

    live_ids = [v["source_id"] for v in sources.values()]
    all_chosen, _, corpus_method = independent_origin_count(live_ids, records, vmod)
    summary = {
        "accepted_sources": len(sources),
        "audit_records": len(records),
        "audit_status_complete": sum(1 for r in records.values() if r.get("audit_status") == "complete"),
        "total_objects": sum(v["objects"] for v in sources.values()),
        "total_systems": sum(v["systems"] for v in sources.values()),
        "total_terms": sum(v["terms"] for v in sources.values()),
        "total_bindings": sum(v["bindings"] for v in sources.values()),
        "corpus_independent_origins": len(all_chosen),
        "corpus_independent_origins_method": corpus_method,
        "evidence_class": {
            "mechanical": [
                "accepted source count and audit record count",
                "per-source object/system/term/binding counts",
                "audit_status of every record",
                "the dependence relation between any two sources, via the committed "
                "independent_origins_ok()",
                "independent-origin counts (exact where the set fits under EXACT_MAX_NODES, "
                "greedy lower bound above it, labelled per count)",
            ],
            "authored_then_validated": [
                "which sources contribute to which domain (live24_domain_map.yaml)",
                "each domain's first-product importance",
                "gap statements and every coverage_state override",
            ],
            "note": "The authored assignments are Canon judgements, made by reading the committed "
                    "extraction. The generator checks them for completeness and for naming only "
                    "real accepted sources; it cannot check whether a judgement is correct. They "
                    "are not machine-discovered facts and must not be cited as such. The live24 "
                    "additions are PROPOSED pending a Controller decision.",
        },
        "domains_total": len(out_domains),
        "packs_total": len(packs_out),
        "by_state": dict(collections.Counter(d["coverage_state"] for d in out_domains)),
        "by_importance": dict(collections.Counter(d["importance"] for d in out_domains)),
        "critical_absent": [d["id"] for d in out_domains
                            if d["importance"] == "critical" and d["coverage_state"] == "absent"],
        "critical_limited": [d["id"] for d in out_domains
                             if d["importance"] == "critical"
                             and d["coverage_state"] in LIMITED_STATES],
        "sources_contributing_to_no_domain": sorted(
            d for d in sources if not any(d in x["contributors"] for x in out_domains)),
    }

    payload = {"summary": summary, "sources": sources, "packs": packs_out, "domains": out_domains}
    (PLANNING / "CANON-V1-LIVE24-COVERAGE.yaml").write_text(
        "# GENERATED by canon/planning/build_live24_coverage.py — do not hand-edit.\n"
        + STATUS_LINE
        + "# Supersedes CANON-V1-LIVE19-COVERAGE.yaml (frozen, untouched).\n"
        "# Authored input: canon/planning/live24_domain_map.yaml\n"
        "# Mechanical input: canon/knowledge/current, canon/audit/records,\n"
        "#                   canon/validation/validate_audit_gate_v02.py (independence rule)\n"
        + yaml.dump(payload, sort_keys=False, width=100, allow_unicode=True)
    )
    (PLANNING / "CANON-V1-LIVE24-COVERAGE.md").write_text(render_markdown(payload))
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
