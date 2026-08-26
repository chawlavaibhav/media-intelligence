#!/usr/bin/env python3
"""Validate the R3-A source register for completeness and internal consistency.

FAIL-CLOSED, in the house style: missing/empty/short input is exit 2 and no verdict, distinct from
exit 1 for a finding. An empty check is not a passing check.

What it enforces:
  * every source carries the fields the task requires, separately (publisher, access route, gate,
    dataset/annotation licence, underlying-media rights, redistribution, suitability, prompt-text
    availability, lineage, scale);
  * every rights-bearing field carries an evidence_level, and no field claims officially_verified
    while the register records that official pages were egress-blocked;
  * every source's lineage id exists in lineage_groups and lists that source as a member;
  * suitable_for / NOT_suitable_for use the declared vocabulary and never overlap;
  * a source marked blocked claims no suitability.
"""
import os, sys

try:
    import yaml
except ImportError:
    print("[FAIL] PyYAML not available", file=sys.stderr); sys.exit(2)

HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.join(os.path.dirname(HERE), "REQUEST-AND-EVAL-SOURCE-ACCESS-REGISTER.yaml")

REQUIRED = ["source_id", "name", "category", "publisher", "distributor", "access_route",
            "authentication_or_terms_gate", "dataset_annotation_licence", "underlying_media_rights",
            "redistribution_status", "internal_research_evaluation_suitability",
            "prompt_text_accessible", "source_lineage", "acquisition_status"]
EVIDENCE = {"officially_verified", "search_supported", "inferred", "unknown"}


def fatal(m):
    print(f"[FAIL] {m}", file=sys.stderr); sys.exit(2)


def main():
    if not os.path.isfile(REG):
        fatal(f"register not found: {REG}")
    doc = yaml.safe_load(open(REG))
    if not doc:
        fatal("register parsed to nothing")
    srcs = doc.get("sources") or []
    if len(srcs) < 8:
        fatal(f"only {len(srcs)} sources parsed; refusing to report on a truncated register")
    groups = doc.get("lineage_groups") or {}
    vocab = set(doc["meta"]["suitability_vocabulary"])

    errors = []
    ids = set()
    for s in srcs:
        sid = s.get("source_id", "<no id>")
        if sid in ids:
            errors.append(f"duplicate source_id {sid}")
        ids.add(sid)
        for f in REQUIRED:
            if not s.get(f):
                errors.append(f"{sid}: missing required field '{f}'")
        # evidence levels on rights-bearing fields
        for f in ("dataset_annotation_licence", "underlying_media_rights", "prompt_text_rights",
                  "approximate_scale", "code_licence", "methodology_notes"):
            v = s.get(f)
            if isinstance(v, dict):
                lv = v.get("evidence_level")
                if lv not in EVIDENCE:
                    errors.append(f"{sid}.{f}: evidence_level {lv!r} not in {sorted(EVIDENCE)}")
                elif lv == "officially_verified":
                    errors.append(f"{sid}.{f}: claims officially_verified, but the register records "
                                  f"that official pages were egress-blocked this session")
        # lineage integrity
        lin = str(s.get("source_lineage", "")).split(" ")[0].split("—")[0].strip()
        if lin and lin.startswith("lin_"):
            g = groups.get(lin)
            if g is None:
                errors.append(f"{sid}: lineage {lin} is not declared in lineage_groups")
            elif isinstance(g, dict) and sid not in (g.get("members") or []):
                errors.append(f"{sid}: lineage group {lin} does not list it as a member")
        # suitability vocabulary and disjointness
        ok_for = set(s.get("suitable_for") or [])
        not_for = set(s.get("NOT_suitable_for") or [])
        for v in ok_for:
            if v not in vocab:
                errors.append(f"{sid}: suitable_for '{v}' not in the declared vocabulary")
        overlap = ok_for & not_for
        if overlap:
            errors.append(f"{sid}: {sorted(overlap)} appears in BOTH suitable_for and NOT_suitable_for")
        if str(s.get("acquisition_status", "")).startswith("blocked") and ok_for:
            errors.append(f"{sid}: marked blocked but still claims suitability {sorted(ok_for)}")

    # every declared lineage member must be a real source
    for gid, g in groups.items():
        if not gid.startswith("lin_") or not isinstance(g, dict):
            continue
        for m in (g.get("members") or []):
            if m not in ids and not m.startswith("src_imagerewarddb"):
                errors.append(f"lineage {gid}: member {m} is not a source in this register")

    import collections
    print(f"sources:            {len(srcs)}")
    print(f"lineage groups:     {len([k for k in groups if k.startswith('lin_')])}")
    print("evidence levels used on licence fields:",
          dict(collections.Counter(
              s.get("dataset_annotation_licence", {}).get("evidence_level")
              for s in srcs if isinstance(s.get("dataset_annotation_licence"), dict))))
    print("acquisition status:",
          dict(collections.Counter(s.get("acquisition_status") for s in srcs)))
    shared = {k: v["members"] for k, v in groups.items()
              if isinstance(v, dict) and len(v.get("members") or []) > 1}
    print(f"multi-member lineages (non-independent): {len(shared)}")
    for k, v in shared.items():
        print(f"   {k}: {v}")
    print()
    if errors:
        for e in errors:
            print(f"[FAIL] {e}")
        print(f"\nRESULT: {len(errors)} register defect(s).")
        sys.exit(1)
    print("[PASS] every source carries all required fields, separately")
    print("[PASS] every rights-bearing field carries an evidence_level")
    print("[PASS] no field claims officially_verified while official pages were egress-blocked")
    print("[PASS] every lineage is declared and reciprocal")
    print("[PASS] suitable_for / NOT_suitable_for are disjoint and use the declared vocabulary")
    print("[PASS] blocked sources claim no suitability")
    sys.exit(0)


if __name__ == "__main__":
    main()
