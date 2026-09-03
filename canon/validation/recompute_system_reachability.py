#!/usr/bin/env python3
"""Canon repair / REP-01 — recompute system-seeded reachability over the accepted corpus.

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

WHAT THIS MEASURES. A pack compiler that seeds from SourceConceptSystem members (every sk_ref in
canon/knowledge/current/*/source-concept-systems.yaml) and closes over intra_source_relations
(treated as UNDIRECTED edges; any sk_-prefixed value in a relation row is an endpoint) reaches
some fraction of the corpus. Objects outside that closure are silently dropped by any
system-seeded compilation. This script computes the closure per source and reports every
unreached sk_id, so the drop is visible instead of silent.

The relation graph is intra-source by construction (0 cross-source edges in the committed
corpus), so the closure is computed per source directory; results are exact and deterministic.

Run: python3 canon/validation/recompute_system_reachability.py
Prints JSON: {"reached": R, "total": T, "unreached": {source_dir: [sk_id, ...]}}.
Against the live-24 corpus (24 sources, 677 objects) the expected result is 641/677 reached with
36 unreached. Library use: compute(extra_memberships=..., extra_edges=...) simulates adopting
backfill proposals (see canon/planning/PROPOSED-orphan-backfill-v0.yaml).
"""
from __future__ import annotations

import collections
import json
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
KNOWLEDGE = ROOT / "canon/knowledge/current"


def compute(extra_memberships: dict | None = None, extra_edges: list | None = None) -> dict:
    """Closure per source.

    extra_memberships: {sk_id: scs_id} — proposed member_of_system additions (each sk_id becomes
    a seed; the scs_id is not otherwise used here, but must belong to the same source).
    extra_edges: [(sk_id, sk_id)] — proposed relation edges, undirected.
    """
    extra_memberships = extra_memberships or {}
    extra_edges = extra_edges or []
    reached_total = 0
    total = 0
    unreached: dict[str, list[str]] = {}
    for d in sorted(KNOWLEDGE.iterdir()):
        if not d.is_dir() or not (d / "source-knowledge.yaml").exists():
            continue
        sk = (yaml.safe_load((d / "source-knowledge.yaml").read_text()) or {}).get(
            "source_knowledge") or []
        scs = (yaml.safe_load((d / "source-concept-systems.yaml").read_text()) or {}).get(
            "source_concept_systems") or []
        ids = {o["sk_id"] for o in sk}
        adj: dict[str, set] = collections.defaultdict(set)
        for o in sk:
            for r in o.get("intra_source_relations") or []:
                for v in r.values():
                    if isinstance(v, str) and v.startswith("sk_") and v in ids:
                        adj[o["sk_id"]].add(v)
                        adj[v].add(o["sk_id"])
        for a, b in extra_edges:
            if a in ids and b in ids:
                adj[a].add(b)
                adj[b].add(a)
        seeds = set()
        for s in scs:
            for m in s.get("members") or []:
                ref = m.get("sk_ref") if isinstance(m, dict) else m
                if isinstance(ref, str) and ref in ids:
                    seeds.add(ref)
        for sk_id in extra_memberships:
            if sk_id in ids:
                seeds.add(sk_id)
        seen = set(seeds)
        stack = list(seeds)
        while stack:
            x = stack.pop()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        missing = sorted(ids - seen)
        total += len(ids)
        reached_total += len(seen)
        if missing:
            unreached[d.name] = missing
    return {"reached": reached_total, "total": total, "unreached": unreached}


def main() -> int:
    print(json.dumps(compute(), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
