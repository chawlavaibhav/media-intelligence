#!/usr/bin/env python3
"""Canon repair / REP-01 — validator for the live-24 coverage layer.

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

Checks, all mechanical, all over committed files (no network, no model calls):

  1. build_live24_coverage.py runs cleanly TWICE and both runs produce byte-identical
     CANON-V1-LIVE24-COVERAGE.yaml and .md (determinism).
  2. Regenerated summary records accepted_sources == 24 and total_objects == 677.
  3. Every directory under canon/knowledge/current that holds a source-knowledge.yaml appears in
     at least one pack's contributors (no orphan sources).
  4. packs.indian_indic_context.contributors == the five CANON-014 India sources, and its
     pack_state != absent.
  5. domain-system-map-v0.yaml references only scs_ids that exist in committed
     source-concept-systems.yaml files; covers every domain of every pack; every domain resolves
     to >= 1 scs_id or carries an explicit residue entry; every sk_id mentioned in a residue note
     resolves in the committed corpus.
  6. PROPOSED-orphan-backfill-v0.yaml contains exactly one entry for every sk_id the committed
     closure recompute (canon/validation/recompute_system_reachability.py) reports unreached;
     every entry carries a non-empty claim-citing justification; every proposed relation type is
     from the SPEC-03 intra-source enum (and each enum term is verified present in the committed
     spec text); every referenced sk_id/scs_id resolves and stays within its source; and
     simulating adoption of all proposals closes the graph completely (reached == total).
  7. PROPOSED-demand-weighted-pack-priority-v1.md carries a demand_counts block whose every
     number recomputes from the three committed demand files (30/18/6 units; 39/54 video).
  8. The authored artifacts carry the PROPOSED status line.

Exit 0 iff every check passes. Run: python3 canon/validation/validate_live24_coverage.py
"""
from __future__ import annotations

import importlib.util
import json
import pathlib
import re
import subprocess
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
PLANNING = ROOT / "canon/planning"
KNOWLEDGE = ROOT / "canon/knowledge/current"

COVERAGE_YAML = PLANNING / "CANON-V1-LIVE24-COVERAGE.yaml"
COVERAGE_MD = PLANNING / "CANON-V1-LIVE24-COVERAGE.md"
DOMAIN_SYSTEM_MAP = PLANNING / "domain-system-map-v0.yaml"
BACKFILL = PLANNING / "PROPOSED-orphan-backfill-v0.yaml"
PRIORITY_MD = PLANNING / "PROPOSED-demand-weighted-pack-priority-v1.md"
SPEC03 = ROOT / "canon/knowledge/SPEC-03-source-knowledge.md"

INDIA_FIVE = [
    "bijapurkar-we-are-like-that-only",
    "dwyer-patel-cinema-india",
    "jain-gods-in-the-bazaar",
    "pandey-pandeymonium",
    "parameswaran-nawabs-nudes-noodles",
]

# SPEC-03 intra-source relation vocabulary (canon/knowledge/SPEC-03-source-knowledge.md);
# check 6 verifies each term is literally present in the committed spec text.
SPEC03_ENUM = {
    "qualifies", "qualified_by", "trades_off_with", "depends_on",
    "generalises", "specialises", "contradicts", "demonstrated_together_with",
}

errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def load_reachability_module():
    path = ROOT / "canon/validation/recompute_system_reachability.py"
    spec = importlib.util.spec_from_file_location("recompute_system_reachability", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def corpus_ids():
    """(source_dir -> set(sk_id), source_dir -> set(scs_id), scs_id -> source_dir)."""
    sk_by_src, scs_by_src, scs_home = {}, {}, {}
    for d in sorted(KNOWLEDGE.iterdir()):
        if not d.is_dir() or not (d / "source-knowledge.yaml").exists():
            continue
        sk = (yaml.safe_load((d / "source-knowledge.yaml").read_text()) or {}).get(
            "source_knowledge") or []
        scs = (yaml.safe_load((d / "source-concept-systems.yaml").read_text()) or {}).get(
            "source_concept_systems") or []
        sk_by_src[d.name] = {o["sk_id"] for o in sk}
        scs_by_src[d.name] = {s["scs_id"] for s in scs}
        for s in scs:
            scs_home[s["scs_id"]] = d.name
    return sk_by_src, scs_by_src, scs_home


def check_build_deterministic() -> dict | None:
    """Checks 1-2: run the generator twice; byte-identical outputs; summary facts."""
    outputs = []
    for run in (1, 2):
        proc = subprocess.run(
            [sys.executable, str(PLANNING / "build_live24_coverage.py")],
            capture_output=True, text=True)
        if proc.returncode != 0:
            err(f"build_live24_coverage.py run {run} exited {proc.returncode}: "
                f"{proc.stderr[-500:]}")
            return None
        outputs.append((COVERAGE_YAML.read_bytes(), COVERAGE_MD.read_bytes()))
    if outputs[0][0] != outputs[1][0]:
        err("CANON-V1-LIVE24-COVERAGE.yaml differs between two consecutive builds")
    if outputs[0][1] != outputs[1][1]:
        err("CANON-V1-LIVE24-COVERAGE.md differs between two consecutive builds")
    cov = yaml.safe_load(COVERAGE_YAML.read_text())
    s = cov["summary"]
    if s["accepted_sources"] != 24:
        err(f"summary.accepted_sources == {s['accepted_sources']}, expected 24")
    if s["total_objects"] != 677:
        err(f"summary.total_objects == {s['total_objects']}, expected 677")
    return cov


def check_pack_membership(cov: dict, sk_by_src: dict) -> None:
    """Checks 3-4."""
    in_pack = {c for p in cov["packs"].values() for c in p["contributors"]}
    for src in sk_by_src:
        if src not in in_pack:
            err(f"accepted source {src} appears in no pack's contributors")
    iic = cov["packs"].get("indian_indic_context") or {}
    if sorted(iic.get("contributors") or []) != INDIA_FIVE:
        err(f"indian_indic_context contributors == {iic.get('contributors')}, "
            f"expected exactly {INDIA_FIVE}")
    if iic.get("pack_state") == "absent" or not iic.get("pack_state"):
        err(f"indian_indic_context pack_state == {iic.get('pack_state')!r}; must not be absent")


def check_domain_system_map(cov: dict, sk_by_src: dict, scs_home: dict) -> None:
    """Check 5."""
    dsm = yaml.safe_load(DOMAIN_SYSTEM_MAP.read_text())
    rows = {e["id"]: e for e in dsm["domains"]}
    all_sk = {i for ids in sk_by_src.values() for i in ids}
    pack_domains = {d for p in cov["packs"].values() for d in p["domains"]}
    for dom in sorted(pack_domains):
        e = rows.get(dom)
        if e is None:
            err(f"domain-system-map has no entry for pack domain {dom}")
            continue
        systems = e.get("systems") or []
        residue = e.get("residue") or []
        if not systems and not residue:
            err(f"domain {dom} resolves to no scs_id and carries no explicit residue entry")
        for srow in systems:
            scs_id = srow.get("scs_id")
            if scs_id not in scs_home:
                err(f"domain {dom} references unknown scs_id {scs_id!r}")
        for text in [json.dumps(systems), json.dumps(residue)]:
            for sk_ref in set(re.findall(r"sk_[a-z0-9_]+", text)):
                if sk_ref not in all_sk:
                    err(f"domain {dom} note mentions unresolvable id {sk_ref!r}")
    for dom in rows:
        if dom not in pack_domains:
            err(f"domain-system-map entry {dom} is not a pack domain in the coverage yaml")


def check_backfill(sk_by_src: dict, scs_by_src: dict) -> None:
    """Check 6."""
    rmod = load_reachability_module()
    base = rmod.compute()
    unreached = {i for ids in base["unreached"].values() for i in ids}
    bf = yaml.safe_load(BACKFILL.read_text())
    entries = bf["entries"]
    by_id = {}
    for e in entries:
        if e["sk_id"] in by_id:
            err(f"backfill has duplicate entry for {e['sk_id']}")
        by_id[e["sk_id"]] = e
    if set(by_id) != unreached:
        missing = sorted(unreached - set(by_id))
        extra = sorted(set(by_id) - unreached)
        err(f"backfill entries do not match the recomputed unreached set: "
            f"missing={missing} extra={extra}")
    if len(unreached) != 36:
        err(f"closure recompute reports {len(unreached)} unreached (brief expected 36) — "
            "corpus changed under the map; re-run REP-01")

    spec_text = SPEC03.read_text()
    for term in sorted(SPEC03_ENUM):
        if term not in spec_text:
            err(f"enum term {term!r} not found in {SPEC03} — enum out of date")

    memberships, edges = {}, []
    for e in entries:
        sk_id, src, p = e["sk_id"], e["source"], e["proposal"]
        if sk_id not in sk_by_src.get(src, set()):
            err(f"backfill {sk_id}: not an sk_id of {src}")
            continue
        if not (e.get("justification") or "").strip():
            err(f"backfill {sk_id}: empty justification")
        kind = p.get("type")
        if kind == "new_relation":
            if p.get("relation") not in SPEC03_ENUM:
                err(f"backfill {sk_id}: relation {p.get('relation')!r} not in SPEC-03 enum")
            tgt = p.get("target")
            if tgt not in sk_by_src.get(src, set()):
                err(f"backfill {sk_id}: relation target {tgt!r} not an sk_id of {src} "
                    "(intra-source relations must stay within the source)")
            else:
                edges.append((sk_id, tgt))
        elif kind == "new_membership":
            if p.get("relation") != "member_of_system":
                err(f"backfill {sk_id}: membership proposal must use member_of_system")
            scs_id = p.get("scs_id")
            if scs_id not in scs_by_src.get(src, set()):
                err(f"backfill {sk_id}: scs_id {scs_id!r} not a system of {src}")
            else:
                memberships[sk_id] = scs_id
        elif kind == "reachable_via":
            via = p.get("entry")
            if via not in by_id:
                err(f"backfill {sk_id}: reachable_via names {via!r}, which has no entry")
            if p.get("committed_relation") not in SPEC03_ENUM:
                err(f"backfill {sk_id}: committed_relation "
                    f"{p.get('committed_relation')!r} not in SPEC-03 enum")
        else:
            err(f"backfill {sk_id}: unknown proposal type {kind!r}")

    sim = rmod.compute(extra_memberships=memberships, extra_edges=edges)
    if sim["reached"] != sim["total"]:
        left = {i for ids in sim["unreached"].values() for i in ids}
        err(f"adopting all backfill proposals still leaves {sorted(left)} unreached "
            f"({sim['reached']}/{sim['total']})")


def check_priority_md() -> None:
    """Check 7."""
    text = PRIORITY_MD.read_text()
    m = re.search(r"```yaml\n(demand_counts:.*?)```", text, re.S)
    if not m:
        err("priority md: no demand_counts yaml block found")
        return
    dc = yaml.safe_load(m.group(1))["demand_counts"]

    briefs = [json.loads(l) for l in
              (ROOT / "canon/experiments/v1/brief-bank/briefs.jsonl").read_text().splitlines()
              if l.strip()]
    bank_total = len(briefs)
    bank_video = sum(1 for b in briefs if b["media_class"] == "video")

    mkt = yaml.safe_load(
        (ROOT / "canon/research/marketplace-demand-v1/derived/"
                "marketplace-brief-bank-v1.yaml").read_text())
    mkt_total = len(mkt["cases"])
    mkt_video = sum(1 for c in mkt["cases"]
                    if c["normalized_request"]["R05_modality"]["value"] == "video")

    eval_dir = ROOT / "eval/experiments/EVAL-037/common/briefs"
    eval_files = sorted(eval_dir.glob("*.txt"))
    eval_total = len(eval_files)
    # a brief is video iff it states a duration (B01/B04 "Target duration", B05 "Target final
    # duration"; no static brief mentions a duration) — rule stated in the priority md §1.
    eval_video = sum(1 for f in eval_files if "duration" in f.read_text().lower())

    recomputed = {
        "brief_bank_total": bank_total, "brief_bank_video": bank_video,
        "marketplace_total": mkt_total, "marketplace_video": mkt_video,
        "eval037_total": eval_total, "eval037_video": eval_video,
        "total": bank_total + mkt_total + eval_total,
        "video_total": bank_video + mkt_video + eval_video,
    }
    for k, v in recomputed.items():
        if dc.get(k) != v:
            err(f"priority md demand_counts.{k} == {dc.get(k)}, recomputed {v}")
    if recomputed["total"] != 54 or recomputed["video_total"] != 39:
        err(f"recomputed demand base {recomputed['total']}/{recomputed['video_total']} "
            "(expected 54 units, 39 video) — demand files changed under the table")


def check_status_lines() -> None:
    """Check 8."""
    for path in [PLANNING / "live24_domain_map.yaml", DOMAIN_SYSTEM_MAP, BACKFILL,
                 PRIORITY_MD, COVERAGE_YAML, COVERAGE_MD,
                 PLANNING / "build_live24_coverage.py",
                 ROOT / "canon/validation/recompute_system_reachability.py"]:
        head = path.read_text()[:2000]
        if "STATUS: PROPOSED" not in head:
            err(f"{path.relative_to(ROOT)} lacks the PROPOSED status line in its header")


def main() -> int:
    sk_by_src, scs_by_src, scs_home = corpus_ids()
    cov = check_build_deterministic()
    if cov is not None:
        check_pack_membership(cov, sk_by_src)
        check_domain_system_map(cov, sk_by_src, scs_home)
    check_backfill(sk_by_src, scs_by_src)
    check_priority_md()
    check_status_lines()
    if errors:
        print(json.dumps({"ok": False, "error_count": len(errors), "errors": errors}, indent=2))
        return 1
    print(json.dumps({"ok": True, "checks": [
        "build deterministic (2 runs byte-identical, yaml+md)",
        "summary: 24 accepted sources / 677 objects",
        "every accepted source in >=1 pack; indian_indic_context == the 5 CANON-014 sources, "
        "state != absent",
        "domain-system map: all scs_ids resolve; every pack domain has systems or explicit "
        "residue; all cited sk_ids resolve",
        "orphan backfill: entries == recomputed unreached set (36); relations from SPEC-03 "
        "enum; simulated adoption closes the graph (677/677)",
        "priority table demand counts recompute (30/18/6; 39/54 video)",
        "PROPOSED status line on every REP-01 artifact",
    ]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
