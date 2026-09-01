#!/usr/bin/env python3
"""REP-07 / DN-06 consequence 5 — validator for the live-37 coverage layer.

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

Adapts canon/validation/validate_live24_coverage.py (retained frozen with its corpus) to the
live-37 coverage layer. Checks, all mechanical, all over committed files (no network, no model
calls):

  1. build_live37_coverage.py runs cleanly TWICE and both runs produce byte-identical
     CANON-V1-LIVE37-COVERAGE.yaml and .md (determinism).
  2. Regenerated summary records accepted_sources == 37 and total_objects == 1300.
  3. Every directory under canon/knowledge/current that holds a source-knowledge.yaml appears
     in at least one pack's contributors (no orphan sources).
  4. packs.indian_indic_context keeps its live24 state: contributors == the five CANON-014
     India sources and pack_state equal to the committed CANON-V1-LIVE24-COVERAGE.yaml value
     (DN-06 changed none of its sources).
  5. DN-06 ruling (c) markers are visible: summary.admission_markers carries
     platform_contingent == [google-abcd-video-ads] and critique_context ==
     [sontag-on-photography]; each marked source's committed audit record carries a matching
     admission_conditions entry; and every domain row and pack row that lists a marked source
     as contributor carries the marker in its contributor_markers.
  6. DN-06 ruling (d) scoped extensions: summary.scoped_extensions is exactly the three
     same-work pairs; each pair is dependence-blocked by the committed
     independent_origins_ok(); and no domain's or pack's independent_origin_set contains an
     extension together with its parent (an extension is never counted as an independent
     origin of its parent).
  7. Every sk_/scs_ id cited anywhere in live37_domain_map.yaml (justification comments
     included) resolves in the committed corpus.
  8. B11 reflects the google-abcd admission: google-abcd-video-ads is a contributor, the
     domain is no longer `absent`, and the row no longer claims the 2011 newest-moving-image
     floor.
  9. The live37 artifacts carry the PROPOSED status line.

Exit 0 iff every check passes. Run: python3 canon/validation/validate_live37_coverage.py
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
RECORDS = ROOT / "canon/audit/records"

MAP_YAML = PLANNING / "live37_domain_map.yaml"
COVERAGE_YAML = PLANNING / "CANON-V1-LIVE37-COVERAGE.yaml"
COVERAGE_MD = PLANNING / "CANON-V1-LIVE37-COVERAGE.md"
LIVE24_COVERAGE_YAML = PLANNING / "CANON-V1-LIVE24-COVERAGE.yaml"

INDIA_FIVE = [
    "bijapurkar-we-are-like-that-only",
    "dwyer-patel-cinema-india",
    "jain-gods-in-the-bazaar",
    "pandey-pandeymonium",
    "parameswaran-nawabs-nudes-noodles",
]

EXPECTED_MARKERS = {
    "platform_contingent": ["google-abcd-video-ads"],
    "critique_context": ["sontag-on-photography"],
}

EXPECTED_SCOPED_EXTENSIONS = {
    "hopkins-scientific-advertising-ch8-21": "hopkins-scientific-advertising-ch1-7",
    "light-science-magic-beyond-ch3": "light-science-magic-ch3",
    "ogilvy-beyond-ch2": "ogilvy-ch2-advertising-that-sells",
}

errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def load_audit_gate():
    path = ROOT / "canon/validation/validate_audit_gate_v02.py"
    spec = importlib.util.spec_from_file_location("audit_gate_v02_live37", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def corpus_ids():
    """(source_dir -> set(sk_id), source_dir -> set(scs_id), source_dir -> source_id)."""
    sk_by_src, scs_by_src, sid_by_src = {}, {}, {}
    for d in sorted(KNOWLEDGE.iterdir()):
        if not d.is_dir() or not (d / "source-knowledge.yaml").exists():
            continue
        sk_doc = yaml.safe_load((d / "source-knowledge.yaml").read_text()) or {}
        sk = sk_doc.get("source_knowledge") or []
        scs = (yaml.safe_load((d / "source-concept-systems.yaml").read_text()) or {}).get(
            "source_concept_systems") or []
        sk_by_src[d.name] = {o["sk_id"] for o in sk}
        scs_by_src[d.name] = {s["scs_id"] for s in scs}
        sid_by_src[d.name] = sk_doc.get("source_id")
    return sk_by_src, scs_by_src, sid_by_src


def load_records():
    return {p.name: yaml.safe_load(p.read_text()) for p in sorted(RECORDS.glob("*.audit.yaml"))}


def check_build_deterministic() -> dict | None:
    """Checks 1-2: run the generator twice; byte-identical outputs; summary facts."""
    outputs = []
    for run in (1, 2):
        proc = subprocess.run(
            [sys.executable, str(PLANNING / "build_live37_coverage.py")],
            capture_output=True, text=True)
        if proc.returncode != 0:
            err(f"build_live37_coverage.py run {run} exited {proc.returncode}: "
                f"{proc.stdout[-500:]}{proc.stderr[-500:]}")
            return None
        outputs.append((COVERAGE_YAML.read_bytes(), COVERAGE_MD.read_bytes()))
    if outputs[0][0] != outputs[1][0]:
        err("CANON-V1-LIVE37-COVERAGE.yaml differs between two consecutive builds")
    if outputs[0][1] != outputs[1][1]:
        err("CANON-V1-LIVE37-COVERAGE.md differs between two consecutive builds")
    cov = yaml.safe_load(COVERAGE_YAML.read_text())
    s = cov["summary"]
    if s["accepted_sources"] != 37:
        err(f"summary.accepted_sources == {s['accepted_sources']}, expected 37")
    if s["total_objects"] != 1300:
        err(f"summary.total_objects == {s['total_objects']}, expected 1300")
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
    live24_iic = (yaml.safe_load(LIVE24_COVERAGE_YAML.read_text())["packs"]
                  .get("indian_indic_context") or {})
    if iic.get("pack_state") != live24_iic.get("pack_state"):
        err(f"indian_indic_context pack_state == {iic.get('pack_state')!r}; DN-06 changed "
            f"none of its sources, so it must keep the live24 state "
            f"{live24_iic.get('pack_state')!r}")


def check_admission_markers(cov: dict, sid_by_src: dict, records: dict) -> None:
    """Check 5."""
    s = cov["summary"]
    got = {cond: sorted(srcs) for cond, srcs in (s.get("admission_markers") or {}).items()}
    if got != EXPECTED_MARKERS:
        err(f"summary.admission_markers == {got}, expected {EXPECTED_MARKERS}")
    by_sid = {r.get("source_id"): r for r in records.values() if r.get("source_id")}
    marked = {src: cond for cond, srcs in EXPECTED_MARKERS.items() for src in srcs}
    for src, cond in sorted(marked.items()):
        rec = by_sid.get(sid_by_src.get(src))
        if rec is None:
            err(f"no committed audit record found for marked source {src}")
            continue
        conds = {c.get("condition") for c in (rec.get("admission_conditions") or [])}
        if cond not in conds:
            err(f"audit record for {src} carries admission_conditions {sorted(conds)}, "
                f"missing required condition {cond!r}")
    for d in cov["domains"]:
        for src, cond in sorted(marked.items()):
            if src in d["contributors"] and (d.get("contributor_markers") or {}).get(src) != cond:
                err(f"domain {d['id']} lists {src} but does not carry its {cond!r} marker")
    for name, p in cov["packs"].items():
        for src, cond in sorted(marked.items()):
            if src in p["contributors"] and (p.get("contributor_markers") or {}).get(src) != cond:
                err(f"pack {name} lists {src} but does not carry its {cond!r} marker")


def check_scoped_extensions(cov: dict, sid_by_src: dict, records: dict) -> None:
    """Check 6."""
    got = dict(cov["summary"].get("scoped_extensions") or {})
    if got != EXPECTED_SCOPED_EXTENSIONS:
        err(f"summary.scoped_extensions == {got}, expected {EXPECTED_SCOPED_EXTENSIONS}")
    vmod = load_audit_gate()
    for ext, parent in sorted(EXPECTED_SCOPED_EXTENSIONS.items()):
        ext_sid, parent_sid = sid_by_src.get(ext), sid_by_src.get(parent)
        if not ext_sid or not parent_sid:
            err(f"scoped extension pair ({ext}, {parent}) not resolvable in the corpus")
            continue
        ok, _ = vmod.independent_origins_ok(ext_sid, parent_sid, records)
        if ok:
            err(f"scoped extension {ext} is NOT dependence-blocked against {parent} — it "
                "would count as an independent origin of its parent")
        for d in cov["domains"]:
            chosen = set(d.get("independent_origin_set") or [])
            if ext_sid in chosen and parent_sid in chosen:
                err(f"domain {d['id']} counts {ext} and {parent} together in its "
                    "independent_origin_set — a scoped extension counted as independent")


def check_cited_ids_resolve(sk_by_src: dict, scs_by_src: dict) -> None:
    """Check 7: every sk_/scs_ id cited anywhere in the map (comments included) resolves."""
    all_sk = {i for ids in sk_by_src.values() for i in ids}
    all_scs = {i for ids in scs_by_src.values() for i in ids}
    text = MAP_YAML.read_text()
    for ref in sorted(set(re.findall(r"\bsk_[a-z0-9]+_[0-9]{4}\b", text))):
        if ref not in all_sk:
            err(f"live37 map cites unresolvable knowledge id {ref!r}")
    for ref in sorted(set(re.findall(r"\bscs_[a-z0-9]+_[0-9]{3}\b", text))):
        if ref not in all_scs:
            err(f"live37 map cites unresolvable concept-system id {ref!r}")


def check_b11(cov: dict) -> None:
    """Check 8."""
    b11 = next((d for d in cov["domains"] if d["id"] == "B11"), None)
    if b11 is None:
        err("coverage yaml has no B11 row")
        return
    if "google-abcd-video-ads" not in b11["contributors"]:
        err("B11 does not list google-abcd-video-ads as a contributor")
    if b11["coverage_state"] == "absent":
        err("B11 coverage_state is still 'absent' despite the google-abcd admission")
    if "2011" in b11["gap"]:
        err("B11 gap prose still cites the 2011 newest-moving-image floor; google-abcd is "
            "2026 material")


def check_status_lines() -> None:
    """Check 9."""
    for path in [MAP_YAML, COVERAGE_YAML, COVERAGE_MD,
                 PLANNING / "build_live37_coverage.py"]:
        head = path.read_text()[:2000]
        if "STATUS: PROPOSED" not in head:
            err(f"{path.relative_to(ROOT)} lacks the PROPOSED status line in its header")


def main() -> int:
    sk_by_src, scs_by_src, sid_by_src = corpus_ids()
    records = load_records()
    cov = check_build_deterministic()
    if cov is not None:
        check_pack_membership(cov, sk_by_src)
        check_admission_markers(cov, sid_by_src, records)
        check_scoped_extensions(cov, sid_by_src, records)
        check_b11(cov)
    check_cited_ids_resolve(sk_by_src, scs_by_src)
    check_status_lines()
    if errors:
        print(json.dumps({"ok": False, "error_count": len(errors), "errors": errors}, indent=2))
        return 1
    print(json.dumps({"ok": True, "checks": [
        "build deterministic (2 runs byte-identical, yaml+md)",
        "summary: 37 accepted sources / 1300 objects",
        "every accepted source in >=1 pack; indian_indic_context == the 5 CANON-014 sources "
        "and keeps its live24 pack_state",
        "DN-06 ruling (c) markers: platform_contingent(google-abcd) + critique_context(sontag) "
        "in the summary, matched against the records' admission_conditions, and carried on "
        "every domain and pack row that lists a marked source",
        "DN-06 ruling (d) scoped extensions: exactly the three same-work pairs, each "
        "dependence-blocked, never counted independent of its parent in any origin set",
        "every sk_/scs_ id cited in live37_domain_map.yaml resolves in the committed corpus",
        "B11 carries the google-abcd contribution, is not absent, and no longer claims the "
        "2011 newest-moving-image floor",
        "PROPOSED status line on every live37 artifact",
    ]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
