#!/usr/bin/env python3
"""Deterministic confidence-marker assigner for the accepted Canon corpus.

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

Reference implementation of canon/context/confidence-marker-v0.yaml. Every marker is a
pure function of committed evidence fields; there is no judgment call in this file —
the authored judgment (keyword lists, seed ids) lives in the committed scheme config.

Usage:
    python3 canon/compilation/assign_markers.py           # write both outputs, print stats
    python3 canon/compilation/assign_markers.py --check   # regenerate to temp, fail on drift

Outputs (byte-identical across runs; no timestamps, sorted iteration everywhere):
    canon/compilation/marker-map-v0.yaml                — per-sk marker map, all 677 objects
    canon/planning/PROPOSED-claim-dating-annex-v1.yaml  — technology-dating + medium-transfer annex

This scheme labels evidence character. It never ranks sources and never scores claims.
Claim-level cross-source consensus is NOT computed (0 cross-source relations exist);
origin counts are decision-level only, read from the LIVE24 coverage map's domains.
"""
from __future__ import annotations

import io
import sys
from collections import Counter
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEME_PATH = REPO_ROOT / "canon/context/confidence-marker-v0.yaml"
CURRENT = REPO_ROOT / "canon/knowledge/current"
RECORDS = REPO_ROOT / "canon/audit/records"
COVERAGE_PATH = REPO_ROOT / "canon/planning/CANON-V1-LIVE24-COVERAGE.yaml"
MARKER_MAP_PATH = REPO_ROOT / "canon/compilation/marker-map-v0.yaml"
ANNEX_PATH = REPO_ROOT / "canon/planning/PROPOSED-claim-dating-annex-v1.yaml"

STATUS_LINE = (
    "PROPOSED — Canon-stream worker output; no Controller decision adopts it; "
    "coordination/CONTROL-STATE.md governs."
)

MEASURED_CHARS = {"controlled_comparison", "empirical_within_source"}
FLAG_ORDER = ["CONTESTED", "QUALIFIED", "DATED", "CULTURE-BOUND", "FIGURE-UNVERIFIED"]
SUFFIX_ORDER = ["-our_reading", "-hedged"]


# ── corpus loading ───────────────────────────────────────────────────────────

def load_corpus(base: Path = CURRENT):
    """Return ({sk_id: object}, {sk_id: source_dir}) over all accepted sources."""
    objs, src_of = {}, {}
    for d in sorted(p.name for p in base.iterdir() if (p / "source-knowledge.yaml").exists()):
        data = yaml.safe_load((base / d / "source-knowledge.yaml").read_text())
        for o in data["source_knowledge"]:
            sk = o["sk_id"]
            if sk in objs:
                raise SystemExit(f"duplicate sk_id across sources: {sk}")
            objs[sk] = o
            src_of[sk] = d
    return objs, src_of


# ── the marker rule (pure function of committed fields) ──────────────────────

def partner_sets(objs: dict):
    """Symmetrise stored relation direction (extractor choice) into flag sets.

    contested: either end of any in-source 'contradicts' edge whose target resolves.
    qualified: the QUALIFIED side only — target of a stored 'qualifies' edge, or
    holder of a stored 'qualified_by' edge. The qualifying exception is not flagged.
    """
    contested, qualified = set(), set()
    for s, o in objs.items():
        for r in o.get("intra_source_relations") or []:
            rel, t = r.get("relation"), r.get("target")
            if t not in objs:
                continue
            if rel == "contradicts":
                contested.add(s)
                contested.add(t)
            elif rel == "qualifies":
                qualified.add(t)
            elif rel == "qualified_by":
                qualified.add(s)
    return contested, qualified


def base_grade(obj: dict) -> str:
    chars = set((obj.get("evidence") or {}).get("characteristics") or [])
    if chars & MEASURED_CHARS:
        return "MEASURED"
    if "mechanism_given" in chars:
        return "REASONED"
    return "ASSERTED"


def object_flags(sk_id: str, obj: dict, contested: set, qualified: set) -> list:
    chars = set((obj.get("evidence") or {}).get("characteristics") or [])
    prov = obj.get("provenance") or {}
    fig_refs = prov.get("figure_refs") or []
    fig_inspected = (prov.get("inspected") or {}).get("figures") or []
    present = {
        "CONTESTED": sk_id in contested,
        "QUALIFIED": sk_id in qualified,
        "DATED": "historical_claim" in chars,
        "CULTURE-BOUND": "culturally_bounded" in chars,
        "FIGURE-UNVERIFIED": bool(fig_refs) and not fig_inspected,
    }
    return [f for f in FLAG_ORDER if present[f]]


def object_suffixes(obj: dict) -> list:
    out = []
    if obj.get("claim_type") == "source_interpretation":
        out.append("-our_reading")
    if any((c or {}).get("origin") == "extractor_observed" for c in obj.get("caveats") or []):
        out.append("-hedged")
    return [s for s in SUFFIX_ORDER if s in out]


def compute_markers(objs: dict) -> dict:
    contested, qualified = partner_sets(objs)
    return {
        sk: {
            "base": base_grade(o),
            "flags": object_flags(sk, o, contested, qualified),
            "suffixes": object_suffixes(o),
        }
        for sk, o in objs.items()
    }


def render_marker(base: str, flags: list, suffixes: list, origin_count: int | None = None) -> str:
    """Render e.g. '[REASONED|CONTESTED|MULTI-ORIGIN(2)]'. Origin is decision-level only."""
    parts = [base + "".join(s for s in SUFFIX_ORDER if s in suffixes)]
    parts += [f for f in FLAG_ORDER if f in flags]
    if origin_count is not None:
        parts.append("SINGLE-ORIGIN" if origin_count == 1 else f"MULTI-ORIGIN({origin_count})")
    return "[" + "|".join(parts) + "]"


def check_entries(objs: dict, entries: dict) -> list:
    """Validate a marker map against the corpus it claims to describe. Fail closed.

    Returns a list of error strings; empty means the entries reproduce the rule exactly.
    Used by tests as the negative-fixture refusal path (e.g. an object carrying
    controlled_comparison mis-marked ASSERTED must be refused here).
    """
    errors = []
    expected = compute_markers(objs)
    for sk in sorted(set(expected) | set(entries)):
        if sk not in entries:
            errors.append(f"{sk}: missing from marker map")
            continue
        if sk not in expected:
            errors.append(f"{sk}: not in corpus")
            continue
        e, g = expected[sk], entries[sk]
        if g.get("base") != e["base"]:
            errors.append(f"{sk}: base {g.get('base')!r} != computed {e['base']!r}")
        if list(g.get("flags") or []) != e["flags"]:
            errors.append(f"{sk}: flags {g.get('flags')!r} != computed {e['flags']!r}")
        if list(g.get("suffixes") or []) != e["suffixes"]:
            errors.append(f"{sk}: suffixes {g.get('suffixes')!r} != computed {e['suffixes']!r}")
        want = render_marker(e["base"], e["flags"], e["suffixes"])
        if g.get("marker") != want:
            errors.append(f"{sk}: marker {g.get('marker')!r} != rendered {want!r}")
    return errors


# ── decision-level origin (from the coverage map; never per claim) ───────────

def decision_level_origin(coverage_path: Path = COVERAGE_PATH) -> dict:
    cov = yaml.safe_load(coverage_path.read_text())
    domains = {
        d["id"]: {"pack": d.get("pack"), "independent_origin_count": d["independent_origin_count"]}
        for d in cov["domains"]
    }
    packs = {
        name: {
            "independent_origin_count": p["independent_origin_count"],
            "method": p.get("independent_origin_count_method"),
        }
        for name, p in cov["packs"].items()
    }
    return {
        "level": "decision_only",
        "source": str(coverage_path.relative_to(REPO_ROOT)),
        "note": (
            "SINGLE-ORIGIN/MULTI-ORIGIN(n) attaches to a compiled DECISION via its domain's "
            "independent_origin_count. Claim-level cross-source consensus is uncomputable "
            "today (0 cross-source relations committed) and is not claimed."
        ),
        "domains": {k: domains[k] for k in sorted(domains)},
        "packs": {k: packs[k] for k in sorted(packs)},
    }


# ── technology-dating annex (mechanical join over audit records) ─────────────

def technology_dating_rows(objs: dict, src_of: dict, records: Path = RECORDS):
    """One row per (sk_id, class) listed under technology_contingency in any
    applicable=true audit record. Fully mechanical; classes copied verbatim."""
    rows, applicable = [], []
    for f in sorted(records.glob("*.audit.yaml")):
        d = yaml.safe_load(f.read_text())
        tc = d.get("technology_contingency") or {}
        if not tc.get("applicable"):
            continue
        rel = str(f.relative_to(REPO_ROOT))
        applicable.append(rel)
        for c in tc.get("classes") or []:
            for sk in c.get("sk_refs") or []:
                if sk not in objs:
                    raise SystemExit(f"{rel}: technology_contingency sk_ref {sk} unresolved")
                rows.append(
                    {
                        "sk_id": sk,
                        "source_dir": src_of[sk],
                        "audit_record": rel,
                        "class": c["class"],
                    }
                )
    rows.sort(key=lambda r: (r["sk_id"], r["class"], r["audit_record"]))
    return applicable, rows


# ── medium-transfer sweep (committed config + committed evidence fields) ─────

def _keyword_probes(kw: str) -> list:
    probes, out = [kw, kw.replace(" ", "_"), kw.replace("_", " ")], []
    for p in probes:
        if p not in out:
            out.append(p)
    return out


def _object_text(obj: dict) -> str:
    return (obj.get("concept_label") or "") + " " + (obj.get("claim") or "")


def _first_keyword_hit(text: str, keywords: list):
    low = text.lower()
    for kw in keywords:
        for probe in _keyword_probes(kw):
            i = low.find(probe)
            if i >= 0:
                return kw, text[i : i + len(probe)]
    return None, None


def medium_transfer_rows(objs: dict, src_of: dict, cfg: dict):
    """Deterministic sweep per medium_transfer_config in the scheme file.

    A row exists iff the sk_id is seeded, or the object sits in a swept source and its
    concept_label+claim contains a listed keyword. Every row records the verbatim
    substring that triggered it (seed phrase, or the matched keyword slice).
    """
    seeds = cfg["seeds"]
    scopes = [
        (set(cfg["swept_sources_editing"]), list(cfg["keywords_editing"]), "editing_pack"),
        (set(cfg["swept_sources_commercial"]), list(cfg["keywords_commercial"]), "commercial_hooks"),
    ]
    rows = {}
    for sk in sorted(objs):
        obj, d, text = objs[sk], src_of[sk], _object_text(objs[sk])
        keyword, slice_ = None, None
        scope_name = None
        for dirs, kws, name in scopes:
            if d in dirs:
                keyword, slice_ = _first_keyword_hit(text, kws)
                scope_name = name
                break
        seeded = sk in seeds
        if not seeded and keyword is None:
            continue
        if seeded:
            phrase = seeds[sk]
            if phrase not in text:
                raise SystemExit(f"seed phrase for {sk} not found verbatim: {phrase!r}")
            origin = "seeded_and_keyword" if keyword else "seeded"
            trigger = phrase
        else:
            origin = "keyword_sweep"
            trigger = slice_
        rows[sk] = {
            "sk_id": sk,
            "source_dir": d,
            "sweep_scope": scope_name,
            "origin": origin,
            "matched_keyword": keyword,
            "trigger_substring": trigger,
        }
    return [rows[sk] for sk in sorted(rows)]


# ── emission (deterministic bytes) ───────────────────────────────────────────

def _dump(doc, header_lines) -> str:
    buf = io.StringIO()
    for line in header_lines:
        buf.write(f"# {line}\n" if line else "#\n")
    buf.write(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100))
    return buf.getvalue()


def build_marker_map_text(objs, src_of, markers) -> str:
    dist_base = Counter(m["base"] for m in markers.values())
    dist_flags = Counter(f for m in markers.values() for f in m["flags"])
    dist_suffix = Counter(s for m in markers.values() for s in m["suffixes"])
    doc = {
        "artifact": "marker-map-v0",
        "status": STATUS_LINE,
        "scheme": "canon/context/confidence-marker-v0.yaml",
        "generated_by": "canon/compilation/assign_markers.py (deterministic; rerun to verify)",
        "objects": len(markers),
        "distribution": {
            "base": {k: dist_base[k] for k in ["MEASURED", "REASONED", "ASSERTED"]},
            "flags": {k: dist_flags.get(k, 0) for k in FLAG_ORDER},
            "suffixes": {k: dist_suffix.get(k, 0) for k in SUFFIX_ORDER},
        },
        "decision_level_origin": decision_level_origin(),
        "markers": {
            sk: {
                "source_dir": src_of[sk],
                "base": m["base"],
                "flags": m["flags"],
                "suffixes": m["suffixes"],
                "marker": render_marker(m["base"], m["flags"], m["suffixes"]),
            }
            for sk, m in sorted(markers.items())
        },
    }
    return _dump(
        doc,
        [
            "marker-map-v0.yaml — GENERATED by canon/compilation/assign_markers.py; do not hand-edit.",
            f"STATUS: {STATUS_LINE}",
            "Per-sk confidence markers for all accepted objects; pure function of committed fields.",
            "Markers label evidence character; they never rank sources (anti-score rule G6 in spirit).",
        ],
    )


def build_annex_text(objs, src_of, scheme) -> str:
    cfg = scheme["medium_transfer_config"]
    applicable, tech_rows = technology_dating_rows(objs, src_of)
    mt_rows = medium_transfer_rows(objs, src_of, cfg)
    tech_counts = Counter(r["class"] for r in tech_rows)
    mt_counts = Counter(r["origin"] for r in mt_rows)
    doc = {
        "artifact": "PROPOSED-claim-dating-annex-v1",
        "status": STATUS_LINE,
        "generated_by": "canon/compilation/assign_markers.py (deterministic; rerun to verify)",
        "scheme": "canon/context/confidence-marker-v0.yaml",
        "method": {
            "technology_dating": (
                "Mechanical join: for every canon/audit/records/*.audit.yaml with "
                "technology_contingency.applicable == true, each class's sk_refs become one row "
                "per (sk_id, class), classes copied verbatim, sk_ids resolved against "
                "canon/knowledge/current/. No judgment in code."
            ),
            "medium_transfer_untested": (
                "Deterministic sweep per medium_transfer_config in the scheme file: seeded ids "
                "plus keyword matches over concept_label+claim in the swept sources. Every row "
                "cites the verbatim substring that triggered it. The flag means transfer to "
                "6-20s vertical feed video is UNTESTED per GAP-LEDGER G2/G5 — it must not be "
                "assumed either way; flagged claims compile as defaults-with-questions, not doctrine."
            ),
        },
        "technology_dating": {
            "records_applicable_true": applicable,
            "records_applicable_count": len(applicable),
            "row_count": len(tech_rows),
            "counts_by_class": {k: tech_counts[k] for k in sorted(tech_counts)},
            "rows": tech_rows,
        },
        "medium_transfer_untested": {
            "row_count": len(mt_rows),
            "counts_by_origin": {k: mt_counts[k] for k in sorted(mt_counts)},
            "swept_sources_editing": list(cfg["swept_sources_editing"]),
            "swept_sources_commercial": list(cfg["swept_sources_commercial"]),
            "rows": mt_rows,
        },
        "notes": [
            "Claim-level cross-source consensus is uncomputable today (0 cross-source relations "
            "committed); nothing in this annex claims two sources agree on a claim.",
            "Admission-context update (DN-06, 2026-09-01): google-abcd-video-ads entered "
            "accepted Canon carrying the platform_contingent admission condition, so its "
            "sound-off warning (sk_abcd_0014 — YouTube is largely sound-on, sound-off design is "
            "platform-contingent) now resolves in canon/knowledge/current and is consumable "
            "subject to that marker. It bears on how medium-transfer flags scope for audio "
            "claims; compiled artifacts must surface the platform_contingent condition with it.",
        ],
    }
    return _dump(
        doc,
        [
            "PROPOSED-claim-dating-annex-v1.yaml — GENERATED by canon/compilation/assign_markers.py;",
            "do not hand-edit.",
            f"STATUS: {STATUS_LINE}",
            "Technology-dating join (audit records -> sk ids) + medium_transfer_untested sweep.",
        ],
    )


def generate() -> dict:
    scheme = yaml.safe_load(SCHEME_PATH.read_text())
    objs, src_of = load_corpus()
    markers = compute_markers(objs)
    return {
        MARKER_MAP_PATH: build_marker_map_text(objs, src_of, markers),
        ANNEX_PATH: build_annex_text(objs, src_of, scheme),
    }


def print_stats(markers):
    base = Counter(m["base"] for m in markers.values())
    flags = Counter(f for m in markers.values() for f in m["flags"])
    suff = Counter(s for m in markers.values() for s in m["suffixes"])
    print(f"objects: {len(markers)}")
    print("base:   ", {k: base[k] for k in ["MEASURED", "REASONED", "ASSERTED"]})
    print("flags:  ", {k: flags.get(k, 0) for k in FLAG_ORDER})
    print("suffixes:", {k: suff.get(k, 0) for k in SUFFIX_ORDER})


def main(argv):
    outputs = generate()
    objs, _ = load_corpus()
    if "--check" in argv:
        drift = []
        for path, text in outputs.items():
            if not path.exists():
                drift.append(f"{path}: missing")
            elif path.read_text() != text:
                drift.append(f"{path}: committed bytes differ from recomputation")
        scheme = yaml.safe_load(SCHEME_PATH.read_text())
        markers = compute_markers(objs)
        base = Counter(m["base"] for m in markers.values())
        flags = Counter(f for m in markers.values() for f in m["flags"])
        suff = Counter(s for m in markers.values() for s in m["suffixes"])
        for rule in scheme["decision_table"]["base_grade"]["rules"]:
            if base.get(rule["grade"], 0) != rule["expected_count"]:
                drift.append(f"base {rule['grade']}: {base.get(rule['grade'], 0)} != {rule['expected_count']}")
        for rule in scheme["decision_table"]["flags"]["rules"]:
            if flags.get(rule["flag"], 0) != rule["expected_count"]:
                drift.append(f"flag {rule['flag']}: {flags.get(rule['flag'], 0)} != {rule['expected_count']}")
        for rule in scheme["decision_table"]["suffixes"]["rules"]:
            if suff.get(rule["suffix"], 0) != rule["expected_count"]:
                drift.append(f"suffix {rule['suffix']}: {suff.get(rule['suffix'], 0)} != {rule['expected_count']}")
        if drift:
            print("DRIFT:", *drift, sep="\n  ")
            return 1
        print("check OK: outputs reproduce byte-identically; all expected counts hold")
        print_stats(compute_markers(objs))
        return 0
    for path, text in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        print(f"wrote {path.relative_to(REPO_ROOT)} ({len(text)} bytes)")
    print_stats(compute_markers(objs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
