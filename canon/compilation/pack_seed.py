#!/usr/bin/env python3
"""The builder's reading packet for one pack — everything a compile session needs, by id, with
no whole-file reading.

    python3 canon/compilation/pack_seed.py <pack_id>              # the packet (Markdown)
    python3 canon/compilation/pack_seed.py --claim sk_x_0001 ...  # full text of claims by id
    python3 canon/compilation/pack_seed.py --source <source_dir>  # every claim of one source, one line each
    python3 canon/compilation/pack_seed.py --systems <source_dir> # concept systems (scs_) of one source

Packet contents: the pack's domains (LIVE37), contributor sources, the SEED claims (hand-retrieved
on recorded jobs from those sources — full text, remedies, guard relations that closure must
cover), and a one-line index of every other accepted claim from the contributors.
"""
from __future__ import annotations

import argparse
import re
import sys
import textwrap
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
KNOW = REPO / "canon/knowledge/current"
COV = REPO / "canon/planning/CANON-V1-LIVE37-COVERAGE.yaml"
HAND = REPO / "canon/validation/HAND-RETRIEVED-CLAIMS.yaml"
GUARD = ("contradicts", "qualified_by", "trades_off_with", "depends_on", "qualifies")

_CACHE = {}


def load_source(src: str) -> dict:
    if src in _CACHE:
        return _CACHE[src]
    d = KNOW / src
    sk = yaml.safe_load((d / "source-knowledge.yaml").read_text(encoding="utf-8")) or {}
    objs = sk.get("source_knowledge") or sk.get("objects") or sk.get("items") or (sk if isinstance(sk, list) else [])
    systems = []
    f = d / "source-concept-systems.yaml"
    if f.is_file():
        scs = yaml.safe_load(f.read_text(encoding="utf-8")) or {}
        systems = scs.get("concept_systems") or scs.get("systems") or scs.get("items") or (scs if isinstance(scs, list) else [])
    _CACHE[src] = {"objects": [o for o in objs if isinstance(o, dict) and o.get("sk_id")],
                   "systems": [s for s in systems if isinstance(s, dict)]}
    return _CACHE[src]


def all_sources() -> list:
    return sorted(p.name for p in KNOW.iterdir() if (p / "source-knowledge.yaml").is_file())


def find_claim(cid: str):
    for src in all_sources():
        for o in load_source(src)["objects"]:
            if o.get("sk_id") == cid:
                return src, o
        for s in load_source(src)["systems"]:
            if s.get("scs_id") == cid or s.get("id") == cid:
                return src, s
    return None, None


def one_line(o: dict) -> str:
    claim = " ".join(str(o.get("claim", "")).split())
    return f"{o.get('sk_id')} · {o.get('concept_label', '')} — {textwrap.shorten(claim, 170)}"


def full(o: dict, src: str) -> str:
    out = [f"### {o.get('sk_id')}  ({src})  label: {o.get('concept_label')}",
           f"claim_type: {o.get('claim_type')}  ·  scope: {o.get('scope', {}).get('domain_discussed_by_source')}  ·  conditions: {o.get('scope', {}).get('conditions')}",
           "claim: " + " ".join(str(o.get("claim", "")).split())]
    terms = o.get("source_terms") or []
    if terms:
        out.append("source_terms: " + " | ".join(textwrap.shorten(" ".join(str(t).split()), 160) for t in terms[:4]))
    for key in ("source_stated_problems", "source_stated_remedies"):
        v = o.get(key) or []
        if v:
            out.append(f"{key}: " + " | ".join(str(x) for x in v[:5]))
    cav = o.get("caveats") or []
    if cav:
        out.append("caveats: " + " | ".join(textwrap.shorten(str(c.get("text", c)), 140) for c in cav[:3]))
    rels = [r for r in (o.get("intra_source_relations") or []) if r.get("relation") in GUARD]
    if rels:
        out.append("GUARD relations (closure must cite, conflict-list or waive each partner): " +
                   "; ".join(f"{r['relation']} → {r['target']}" + (f" ({textwrap.shorten(str(r.get('note', '')), 90)})" if r.get("note") else "") for r in rels))
    return "\n".join(out)


def seed_ids_for(contributors: set) -> list:
    text = HAND.read_text(encoding="utf-8")
    rows = re.findall(r"- \{id: (sk_[a-z0-9_]+), source: ([a-z0-9-]+)", text)
    seen, out = set(), []
    for cid, src in rows:
        if src in contributors and cid not in seen:
            seen.add(cid); out.append((cid, src))
    return out


def packet(pack_id: str) -> str:
    cov = yaml.safe_load(COV.read_text(encoding="utf-8"))
    pack = cov["packs"][pack_id]
    domains = [d for d in cov["domains"] if d["id"] in pack["domains"]]
    contributors = list(pack["contributors"])
    lines = [f"# Seed packet — pack `{pack_id}`", "",
             f"LIVE37 state: {pack['pack_state']} · domains {pack['domain_count']} · contributors {pack['contributor_count']} · critical domains {pack.get('critical_domains')}",
             "", "## Domains", ""]
    for d in domains:
        lines.append(f"- {d['id']} {d['name']} — importance {d.get('importance')}; contributors: {', '.join(d.get('contributors', []))}")
    lines += ["", "## Contributor sources (accepted objects / concept systems)", ""]
    for src in contributors:
        s = load_source(src)
        lines.append(f"- {src}: {len(s['objects'])} claims, {len(s['systems'])} concept systems")
    seeds = seed_ids_for(set(contributors))
    lines += ["", f"## SEED claims — {len(seeds)} hand-retrieved on recorded jobs from these sources (every one must be cited by a decision)", ""]
    for cid, src in seeds:
        _, o = find_claim(cid)
        lines.append(full(o, src) if o else f"### {cid} — NOT FOUND")
        lines.append("")
    seed_set = {c for c, _ in seeds}
    lines += ["## Index — every other accepted claim from the contributors (one line each; fetch full text with --claim)", ""]
    for src in contributors:
        s = load_source(src)
        lines.append(f"### {src}")
        for o in s["objects"]:
            if o.get("sk_id") not in seed_set:
                lines.append("- " + one_line(o))
        if s["systems"]:
            lines.append("  concept systems: " + "; ".join(f"{x.get('scs_id') or x.get('id')} · {x.get('label') or x.get('concept_label') or x.get('name', '')}" for x in s["systems"]))
        lines.append("")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pack_id", nargs="?")
    ap.add_argument("--claim", nargs="*", default=None)
    ap.add_argument("--source", default=None)
    ap.add_argument("--systems", default=None)
    a = ap.parse_args(argv)
    if a.claim:
        for cid in a.claim:
            src, o = find_claim(cid)
            print(full(o, src) if o and o.get("sk_id") else (yaml.safe_dump(o, allow_unicode=True) if o else f"{cid}: NOT FOUND"))
            print()
        return 0
    if a.source:
        for o in load_source(a.source)["objects"]:
            print("- " + one_line(o))
        return 0
    if a.systems:
        print(yaml.safe_dump(load_source(a.systems)["systems"], allow_unicode=True, width=110))
        return 0
    if not a.pack_id:
        ap.error("pack_id required")
    print(packet(a.pack_id))
    return 0


if __name__ == "__main__":
    sys.exit(main())
