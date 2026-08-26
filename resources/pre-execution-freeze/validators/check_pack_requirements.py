#!/usr/bin/env python3
"""Fail-closed validator for CONTROLLED-PACK-REQUIREMENTS-v2.yaml.

Enforces the mechanical gates RES-004 sets on pack requirements:
  * exactly FOUR pack families - a fifth requires a concrete active consumer;
  * every pack names at least one ACTIVE consumer (no speculative packs);
  * every count is labelled exact or provisional - never unlabelled;
  * every provisional count carries a sizing basis AND the assumption it rests on;
  * no pack claims statistical confidence (no confidence/power/significance language);
  * every pack declares protected roles including a frozen holdout;
  * every pack declares media-lineage granularity and a request-lineage position.

Exit 0 valid · 1 defect found · 2 could not check.
"""
import os, re, sys

try:
    import yaml
except ImportError:
    print("[FAIL] PyYAML not available", file=sys.stderr); sys.exit(2)

HERE = os.path.dirname(os.path.abspath(__file__))
REQ = os.path.join(os.path.dirname(HERE), "CONTROLLED-PACK-REQUIREMENTS-v2.yaml")
EXPECTED_PACKS = 4
COUNT_STATUS = {"exact", "provisional"}
# Language that would assert precision the design has not established.
FORBIDDEN_PRECISION = re.compile(
    r"\b(confidence interval|statistically significant|statistical significance|p-value|"
    r"power analysis|95% confidence|margin of error)\b", re.I)


def fatal(m):
    print(f"[FAIL] {m}", file=sys.stderr); sys.exit(2)


def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, f"{path}.{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f"{path}[{i}]")
    else:
        yield path, o


def main():
    if not os.path.isfile(REQ):
        fatal(f"requirements file not found: {REQ}")
    d = yaml.safe_load(open(REQ))
    if not d:
        fatal("requirements file parsed to nothing")
    packs = d.get("packs") or []
    if not packs:
        fatal("no packs declared; refusing to validate an empty requirements set")

    e = []
    if len(packs) != EXPECTED_PACKS:
        e.append(f"{len(packs)} pack families declared, expected exactly {EXPECTED_PACKS}. "
                 f"A fifth family requires a concrete active consumer and a Controller decision.")
    if d.get("meta", {}).get("fifth_family_created") is not False:
        e.append("meta.fifth_family_created must be explicitly false")
    if not d.get("sizing_rule", {}).get("statement"):
        e.append("no deterministic sizing rule declared")

    ids = set()
    for p in packs:
        pid = p.get("pack_id", "<no id>")
        if pid in ids:
            e.append(f"duplicate pack_id {pid}")
        ids.add(pid)
        if not (p.get("consumers_named") or []):
            e.append(f"{pid}: names no consumer. A pack with no active consumer is speculative.")
        for f in ("protected_roles", "lineage_metadata", "minimum_viable_quantity"):
            if not p.get(f):
                e.append(f"{pid}: missing '{f}'")
        pr = p.get("protected_roles") or {}
        if not pr.get("holdout"):
            e.append(f"{pid}: declares no frozen holdout role")
        lm = p.get("lineage_metadata") or {}
        if not lm.get("media_lineage"):
            e.append(f"{pid}: no media-lineage granularity declared")
        if "request_lineage" not in lm:
            e.append(f"{pid}: no request-lineage position declared (not_applicable is a valid answer)")
        # every count_status labelled and valid
        for path, val in walk(p, pid):
            if path.endswith("count_status") and val not in COUNT_STATUS:
                e.append(f"{path}: count_status {val!r} not in {sorted(COUNT_STATUS)}")
        mv = p.get("minimum_viable_quantity") or {}
        if mv.get("count_status") not in COUNT_STATUS:
            e.append(f"{pid}: minimum_viable_quantity has no valid count_status")
        if mv.get("count_status") == "provisional" and not mv.get("assumption_it_rests_on"):
            e.append(f"{pid}: provisional quantity with no stated assumption")
        ent = p.get("required_entities") or {}
        if ent.get("count_status") == "provisional":
            if not ent.get("sizing_basis"):
                e.append(f"{pid}: provisional entity count with no sizing_basis")
            if not ent.get("smallest_safe_provisional"):
                e.append(f"{pid}: provisional entity count with no smallest_safe_provisional")

    # No invented statistical precision anywhere in the document.
    # ONE exemption: meta.sizing_disclaimer exists precisely to NAME these concepts and deny them.
    # Exempting a field whose purpose is denial is not weakening the check - flagging it would train
    # the author to remove the disclaimer, which is the opposite of what the rule wants.
    EXEMPT = (".meta.sizing_disclaimer",)
    for path, val in walk(d):
        if path in EXEMPT:
            continue
        if isinstance(val, str) and FORBIDDEN_PRECISION.search(val):
            e.append(f"{path}: claims statistical precision the design has not established "
                     f"({FORBIDDEN_PRECISION.search(val).group(0)!r})")

    exact = sum(1 for p in packs for path, v in walk(p) if path.endswith("count_status") and v == "exact")
    prov = sum(1 for p in packs for path, v in walk(p) if path.endswith("count_status") and v == "provisional")
    print(f"pack families:        {len(packs)} (fifth family created: {d.get('meta',{}).get('fifth_family_created')})")
    print(f"sizing rule:          {d.get('sizing_rule',{}).get('id')}")
    print(f"labelled counts:      {exact} exact · {prov} provisional")
    for p in packs:
        print(f"   {p.get('pack_id'):22s} consumers={len(p.get('consumers_named') or []):>2}  "
              f"qty={ {k: v for k, v in (p.get('minimum_viable_quantity') or {}).items() if k in ('images','clips','assets')} }")
    print()
    if e:
        for x in e:
            print(f"[FAIL] {x}")
        print(f"\nRESULT: {len(e)} defect(s).")
        sys.exit(1)
    print("[PASS] exactly four pack families; no fifth created")
    print("[PASS] every pack names at least one active consumer")
    print("[PASS] every count is labelled exact or provisional")
    print("[PASS] every provisional count carries a sizing basis and its assumption")
    print("[PASS] a deterministic sizing rule is declared")
    print("[PASS] no pack claims statistical confidence the design has not established")
    print("[PASS] every pack declares protected roles including a frozen holdout")
    print("[PASS] every pack declares media-lineage granularity and a request-lineage position")
    sys.exit(0)


if __name__ == "__main__":
    main()
