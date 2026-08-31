#!/usr/bin/env python3
"""Validate the compiled pilot doctrine packs and the NR->pack trigger table. FAIL CLOSED.

STATUS: PROPOSED — Canon-stream worker output; no Controller decision adopts it;
coordination/CONTROL-STATE.md governs.

Extends the canon/validation/validate_canon_context.py check family (accepted-only linkage,
audit-complete sources, budgets, stated conflicts/limits) with the compiled-pack checks of
canon/compilation/COMPILED-DOCTRINE-SPEC-v0.md and the REP-05 acceptance list:

  (1) every cited sk_/scs_/t_ id resolves under canon/knowledge/current/; zero ids resolve
      under canon/candidates/ (collision is a hard fail); every cited source has a complete
      Audit Gate record;
  (2) closure — for every cited sk id, each direction-normalized guard partner (contradicts
      symmetric / qualified_by incl. reversed qualifies / trades_off_with symmetric /
      depends_on directed) is cited in the same pack, named in a conflicts entry with a
      resolution_rule, or listed in closure_waivers with a reason; regression: a pack citing
      sk_gos_c003_0012 must also carry sk_gos_c003_0007, sk_gos_c003_0010, sk_gos_c003_0013;
  (3) every decision's confidence marker recomputes from the REP-04 assigner
      (canon/compilation/assign_markers.py) under the spec §4 aggregation rule — this file
      re-implements the rule independently of the compiler so drift in either fails;
      PA-D9's marker must contain ASSERTED, DATED and SINGLE-ORIGIN;
  (4) the terse rendering of each pack is <= 2,500 tokens at 4 chars/token and matches the
      stamped counts; the largest legal pack combination in the trigger table is <= 45,000
      tokens; the injection contract's system-prompt block fits its declared 300 tokens;
  (5) the stamped corpus digest equals the digest recomputed from
      canon/knowledge/CANON-CORPUS-INDEX.yaml accepted entries (and the entries match disk);
  (6) the trigger table is total over all 28 (modality x operation) cells of the frozen
      grammar; every referenced pack id is one of the 10 in the coverage map; every audio
      cell carries the coverage-gap notice;
  (7) reproducibility — the compiler, run twice in-process, yields bytes identical to each
      other and to the committed pack files;
  (8) both packs contain the Devanagari limit line and product_appearance contains the LSM
      later-chapters caveat, by exact-string match;
  (9) zero occurrences of any sk_abcd_/HOLD-lane id in any REP-05 deliverable (every
      sk_/scs_-shaped token in every deliverable must resolve in accepted Canon).

A PASS establishes structure over committed bytes. It does NOT establish relevance, doctrine
quality, outcome improvement, or adoption.

Run: python3 canon/validation/validate_compiled_pack.py
"""
from __future__ import annotations

import hashlib
import importlib.util
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from canon.compilation import assign_markers  # noqa: E402

KNOWLEDGE = ROOT / "canon/knowledge/current"
CANDIDATES = ROOT / "canon/candidates"
RECORDS = ROOT / "canon/audit/records"
INDEX = ROOT / "canon/knowledge/CANON-CORPUS-INDEX.yaml"
ANNEX = ROOT / "canon/planning/PROPOSED-claim-dating-annex-v1.yaml"
COVERAGE = ROOT / "canon/planning/CANON-V1-LIVE24-COVERAGE.yaml"
GRAMMAR = ROOT / "canon/experiments/pre-execution-freeze/MEDIA-REQUEST-GRAMMAR-v1.yaml"
AUDIT_GATE = ROOT / "canon/validation/validate_audit_gate_v02.py"
CONTRACT = ROOT / "canon/compilation/INJECTION-CONTRACT-v0.md"

PACK_PATHS = [
    ROOT / "canon/compilation/PACK-product_appearance-v0.yaml",
    ROOT / "canon/compilation/PACK-composition_and_attention-v0.yaml",
]
TRIGGERS = ROOT / "canon/packs/pack-triggers-v0.yaml"
DELIVERABLES = PACK_PATHS + [
    TRIGGERS,
    CONTRACT,
    ROOT / "canon/compilation/COMPILED-DOCTRINE-SPEC-v0.md",
    ROOT / "canon/compilation/compile_pilot_packs.py",
    ROOT / "canon/validation/validate_compiled_pack.py",
]

TERSE_MAX_TOKENS = 2500
COMBO_MAX_TOKENS = 45000
GRADE_ORDER = ["ASSERTED", "REASONED", "MEASURED"]
FLAG_ORDER = list(assign_markers.FLAG_ORDER) + ["MEDIUM-UNTESTED"]

DEVANAGARI_LIMIT = (
    "Devanagari correctness criteria do not exist in Canon — never generate Devanagari "
    "glyphs; composite text deterministically."
)
LSM_LATER_CHAPTERS_CAVEAT = (
    "Coverage caveat (GAP-16): light-science-magic ch3 is the only admitted chapter of its "
    "source; the source's later chapters are HOLD (not admitted) and are recorded as "
    "qualifying and in places reversing ch3 guidance. This pack cites that caveat's "
    "existence only and consumes no HOLD content."
)
GOS_REGRESSION = {
    "sk_gos_c003_0012": ["sk_gos_c003_0007", "sk_gos_c003_0010", "sk_gos_c003_0013"],
}


# ── environment (loaded once) ────────────────────────────────────────────────

def load_audit_gate():
    spec = importlib.util.spec_from_file_location("audit_gate_v02_v", AUDIT_GATE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def load_environment() -> dict:
    objs, src_of = assign_markers.load_corpus()
    owner, source_id_of, systems, terms = {}, {}, {}, {}
    for d in sorted(p.name for p in KNOWLEDGE.iterdir() if p.is_dir()):
        scs = yaml.safe_load((KNOWLEDGE / d / "source-concept-systems.yaml").read_text()) or {}
        ont = yaml.safe_load((KNOWLEDGE / d / "ontology-mappings.yaml").read_text()) or {}
        for s in scs.get("source_concept_systems") or []:
            systems[s["scs_id"]] = s
            owner[s["scs_id"]] = d
            source_id_of[s["scs_id"]] = scs.get("source_id")
        for t in ont.get("terms") or []:
            terms[t["term_id"]] = t
            owner[t["term_id"]] = d
    for sk, o in objs.items():
        owner[sk] = src_of[sk]
        source_id_of[sk] = o.get("source_id")

    audited, records = {}, {}
    for p in sorted(RECORDS.glob("*.audit.yaml")):
        r = yaml.safe_load(p.read_text()) or {}
        records[p.name] = r
        audited[str(r.get("knowledge_dir", "")).rstrip("/").split("/")[-1]] = r.get("audit_status")

    candidate_ids = set()
    for p in CANDIDATES.rglob("source-knowledge.yaml"):
        for o in (yaml.safe_load(p.read_text()) or {}).get("source_knowledge") or []:
            candidate_ids.add(o.get("sk_id"))
    for p in CANDIDATES.rglob("source-concept-systems.yaml"):
        for s in (yaml.safe_load(p.read_text()) or {}).get("source_concept_systems") or []:
            candidate_ids.add(s.get("scs_id"))

    annex = yaml.safe_load(ANNEX.read_text())
    dating_by_id: dict = {}
    for row in annex["technology_dating"]["rows"]:
        dating_by_id.setdefault(row["sk_id"], set()).add(row["class"])
    medium_untested = {row["sk_id"] for row in annex["medium_transfer_untested"]["rows"]}

    tc_applicable_dirs = set()
    for r in records.values():
        if (r.get("technology_contingency") or {}).get("applicable"):
            tc_applicable_dirs.add(str(r.get("knowledge_dir", "")).rstrip("/").split("/")[-1])

    return {
        "objs": objs, "src_of": src_of, "systems": systems, "terms": terms,
        "owner": owner, "source_id_of": source_id_of, "audited": audited, "records": records,
        "candidate_ids": candidate_ids, "dating_by_id": dating_by_id,
        "medium_untested": medium_untested, "tc_applicable_dirs": tc_applicable_dirs,
        "markers": assign_markers.compute_markers(objs),
        "audit_gate": load_audit_gate(),
        "pack_ids": sorted((yaml.safe_load(COVERAGE.read_text()) or {}).get("packs", {})),
    }


def recompute_corpus_digest(errors: list) -> str | None:
    acc = (yaml.safe_load(INDEX.read_text()) or {}).get("fingerprints", {}).get("accepted_canon")
    if not acc:
        errors.append("corpus index: fingerprints.accepted_canon missing")
        return None
    for row in acc["files"]:
        actual = hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest()
        if actual != row["sha256"]:
            errors.append(f"corpus index stale: {row['path']} differs from recorded sha256")
    canonical = "".join(
        f"{r['path']}:{r['sha256']}\n" for r in sorted(acc["files"], key=lambda x: x["path"])
    )
    combined = hashlib.sha256(canonical.encode()).hexdigest()
    if combined != acc["combined_digest"]:
        errors.append("corpus index inconsistent: recombined digest != combined_digest")
    return combined


# ── check (3): independent marker aggregation (spec §4, re-implemented) ──────

def guard_partners(env: dict) -> dict:
    part: dict = {}

    def add(a, rel, b):
        part.setdefault(a, {}).setdefault(rel, set()).add(b)

    for s, o in env["objs"].items():
        for r in o.get("intra_source_relations") or []:
            rel, t = r.get("relation"), r.get("target")
            if t not in env["objs"]:
                continue
            if rel == "contradicts":
                add(s, "contradicts", t)
                add(t, "contradicts", s)
            elif rel == "qualifies":
                add(t, "qualified_by", s)
            elif rel == "qualified_by":
                add(s, "qualified_by", t)
            elif rel == "trades_off_with":
                add(s, "trades_off_with", t)
                add(t, "trades_off_with", s)
            elif rel == "depends_on":
                add(s, "depends_on", t)
    return part


def independent_origin_count(source_ids: list, env: dict) -> int:
    n = len(source_ids)
    if n <= 1:
        return n
    ok = {}
    for i, a in enumerate(source_ids):
        for b in source_ids[i + 1:]:
            good, _ = env["audit_gate"].independent_origins_ok(a, b, env["records"])
            ok[(a, b)] = ok[(b, a)] = good
    best = 1
    for mask in range(1, 1 << n):
        members = [source_ids[i] for i in range(n) if mask >> i & 1]
        if all(ok[(x, y)] for i, x in enumerate(members) for y in members[i + 1:]):
            best = max(best, len(members))
    return best


def expected_decision_marker(ids: list, env: dict) -> str:
    sk_ids = [i for i in ids if i in env["objs"]]
    ms = [env["markers"][i] for i in sk_ids]
    base = GRADE_ORDER[min(GRADE_ORDER.index(m["base"]) for m in ms)]
    if len(sk_ids) == 1:
        base = GRADE_ORDER[max(0, GRADE_ORDER.index(base) - 1)]
    suffixes = [s for s in assign_markers.SUFFIX_ORDER if any(s in m["suffixes"] for m in ms)]
    flags = {f for m in ms for f in m["flags"]}
    for i in sk_ids:
        if (env["owner"][i] in env["tc_applicable_dirs"]
                and "durable_mechanism" not in env["dating_by_id"].get(i, set())):
            flags.add("DATED")
    if any(i in env["medium_untested"] for i in sk_ids):
        flags.add("MEDIUM-UNTESTED")
    sources = sorted({env["source_id_of"][i] for i in ids if env["source_id_of"].get(i)})
    n = independent_origin_count(sources, env)
    origin = "SINGLE-ORIGIN" if n == 1 else f"MULTI-ORIGIN({n})"
    parts = [base + "".join(suffixes)] + [f for f in FLAG_ORDER if f in flags] + [origin]
    return "[" + "|".join(parts) + "]"


# ── pack validation (checks 1, 2, 3, 4a, 5, 8, 9) ────────────────────────────

def validate_pack(path: pathlib.Path, env: dict, digest: str | None) -> list:
    errors: list = []

    def err(msg):
        errors.append(f"{path.name}: {msg}")

    raw = path.read_text()
    pack = yaml.safe_load(raw) or {}
    pack_id = pack.get("pack_id")

    # (9) every id-shaped token anywhere in the file must resolve in accepted Canon,
    # and sk_abcd_* (the HOLD lane's id space) must not appear at all.
    if re.search(r"sk_abcd_\d+", raw):
        err("contains an sk_abcd_ (HOLD) id — forbidden in any deliverable")
    for token in sorted(set(re.findall(r"\b(?:sk|scs)_[a-z0-9_]+\b", raw))):
        if token in env["candidate_ids"]:
            err(f"{token}: resolves under canon/candidates/ (HOLD lane) — fail closed")
        elif token not in env["owner"]:
            err(f"{token}: does not resolve in canon/knowledge/current/")

    decisions = pack.get("decisions") or []
    if not decisions:
        err("no decisions")
        return errors

    cited: set = set()
    for d in decisions:
        did = d.get("decision_id")
        refs = [r.get("ref") for r in d.get("compiled_from") or []]
        if not refs:
            err(f"{did}: compiled_from is empty — every compiled decision lists its ids")
        for field in ("question", "default", "check"):
            if not str(d.get(field) or "").strip():
                err(f"{did}: `{field}` is empty")
        if d.get("check_id") != f"{did}-check":
            err(f"{did}: check_id is {d.get('check_id')!r}, expected '{did}-check'")
        for ref in refs:
            cited.add(ref)
            # (1) resolution, candidate collision, audit status
            if ref in env["candidate_ids"]:
                err(f"{did}: {ref} collides with canon/candidates/ — fail closed")
                continue
            if ref not in env["owner"]:
                err(f"{did}: {ref} does not resolve in canon/knowledge/current/")
                continue
            src = env["owner"][ref]
            if env["audited"].get(src) != "complete":
                err(f"{did}: {ref} — Audit Gate status for {src} is "
                    f"{env['audited'].get(src)!r}, not 'complete'")
            row = next(r for r in d["compiled_from"] if r.get("ref") == ref)
            if row.get("source_dir") != src:
                err(f"{did}: {ref} — compiled_from says source_dir="
                    f"{row.get('source_dir')!r}, corpus owner is {src!r}")
        # (3) marker recomputation
        sk_refs = [r for r in refs if r in env["objs"]]
        if sk_refs:
            want = expected_decision_marker(refs, env)
            if d.get("confidence_marker") != want:
                err(f"{did}: confidence_marker {d.get('confidence_marker')!r} != "
                    f"recomputed {want!r}")
        else:
            err(f"{did}: cites no sk objects — a decision must compile from claims")

    # (3) PA-D9 marker tokens
    if pack_id == "product_appearance":
        d9 = next((d for d in decisions if d.get("decision_id") == "PA-D9"), None)
        if d9 is None:
            err("PA-D9 missing")
        else:
            marker = str(d9.get("confidence_marker") or "")
            for needle in ("ASSERTED", "DATED", "SINGLE-ORIGIN"):
                if needle not in marker:
                    err(f"PA-D9: marker {marker!r} lacks {needle}")
            limits_text = " ".join(d9.get("limits") or [])
            if "application_unbound" not in limits_text:
                err("PA-D9: missing the A13 application_unbound packshot limit")

    # (2) closure over the pack's cited set
    part = guard_partners(env)
    conflict_named: set = set()
    for c in pack.get("conflicts") or []:
        cid = c.get("conflict_id")
        between = c.get("between") or []
        if len(set(between)) < 2:
            err(f"{cid}: `between` needs two distinct refs")
        conflict_named.update(between)
        if not str(c.get("resolution_rule") or "").strip():
            err(f"{cid}: conflicts entry has no resolution_rule — R7 forbids "
                "shipping an unarbitrated pair to a weak model")
    waived = {(w.get("ref"), w.get("relation"), w.get("partner"))
              for w in pack.get("closure_waivers") or []}
    for w in pack.get("closure_waivers") or []:
        if not str(w.get("reason") or "").strip():
            err(f"closure_waivers[{w.get('ref')}]: no reason stated")
    for sk in sorted(r for r in cited if r in env["objs"]):
        for rel in ("contradicts", "qualified_by", "trades_off_with", "depends_on"):
            for partner in sorted(part.get(sk, {}).get(rel, ())):
                if partner in cited or partner in conflict_named:
                    continue
                if (sk, rel, partner) in waived:
                    continue
                err(f"closure hole: {sk} {rel} {partner} is neither cited, in conflicts, "
                    "nor waived (GAP-11)")
    for trigger_id, required in GOS_REGRESSION.items():
        if trigger_id in cited:
            for req in required:
                if req not in cited:
                    err(f"regression: pack cites {trigger_id} without {req}")

    # (4a) terse budget and stamped counts
    terse = pack.get("terse_injection_text") or ""
    tokens = (len(terse) + 3) // 4
    if not terse:
        err("terse_injection_text is empty")
    if tokens > TERSE_MAX_TOKENS:
        err(f"terse rendering {tokens} tokens > {TERSE_MAX_TOKENS}")
    counts = pack.get("counts") or {}
    if counts.get("terse_chars") != len(terse) or counts.get("terse_tokens") != tokens:
        err(f"stamped terse counts ({counts.get('terse_chars')}, {counts.get('terse_tokens')}) "
            f"!= measured ({len(terse)}, {tokens}) — size reported must equal size delivered")
    if counts.get("decisions") != len(decisions):
        err("stamped decision count != actual")
    sk_cited = sorted(r for r in cited if r in env["objs"])
    claim_bytes = sum(len(env["objs"][r].get("claim") or "") for r in sk_cited)
    if counts.get("cited_sk_objects") != len(sk_cited):
        err("stamped cited_sk_objects != recount")
    if counts.get("cited_claim_bytes") != claim_bytes:
        err("stamped cited_claim_bytes != recount")

    # (5) corpus digest stamp
    if digest is not None and pack.get("corpus_digest") != digest:
        err(f"stamped corpus_digest {str(pack.get('corpus_digest'))[:12]}... != recomputed "
            f"{digest[:12]}... — stale stamp")

    # (8) verbatim limit lines
    pack_limits = pack.get("pack_limits") or []
    if DEVANAGARI_LIMIT not in pack_limits or DEVANAGARI_LIMIT not in terse:
        err("Devanagari limit line missing or not verbatim (GAP-09)")
    if pack_id == "product_appearance":
        if LSM_LATER_CHAPTERS_CAVEAT not in pack_limits or LSM_LATER_CHAPTERS_CAVEAT not in terse:
            err("LSM later-chapters coverage caveat missing or not verbatim (GAP-16)")

    return errors


# ── trigger table validation (checks 4b, 6) ──────────────────────────────────

def validate_triggers(path: pathlib.Path, env: dict) -> list:
    errors: list = []

    def err(msg):
        errors.append(f"{path.name}: {msg}")

    doc = yaml.safe_load(path.read_text()) or {}
    grammar = yaml.safe_load(GRAMMAR.read_text()) or {}
    fields = {f.get("id"): f for f in grammar.get("fields") or []}
    modalities = list((fields.get("R05") or {}).get("domain") or [])
    vocab = (grammar.get("vocabularies") or {}).get("requested_operation")
    operations = list(vocab if isinstance(vocab, list) else (vocab or {}).get("values") or [])
    if not modalities or not operations:
        err("cannot read modality/operation enums from the frozen grammar")
        return errors

    closed = set(env["pack_ids"])
    declared = set(doc.get("pack_ids_closed_set") or [])
    if declared != closed:
        err(f"pack_ids_closed_set != the coverage map's 10 packs "
            f"(missing {sorted(closed - declared)}, extra {sorted(declared - closed)})")

    budgets = doc.get("token_budgets") or {}
    for pid in closed:
        if not isinstance(budgets.get(pid), int) or budgets.get(pid, 0) < 1:
            err(f"token_budgets[{pid}] missing or not a positive integer")

    universal = doc.get("universal_packs") or []
    bases = doc.get("modality_base_packs") or {}
    conditionals = [c.get("pack") for c in doc.get("conditional_packs") or []]
    for name in universal + conditionals + [p for b in bases.values() for p in b]:
        if name not in closed:
            err(f"pack id {name!r} is not in the closed set of 10")

    # (6) totality over 28 cells
    cells = {(c.get("modality"), c.get("requested_operation")): c
             for c in doc.get("cells") or []}
    expected = {(m, o) for m in modalities for o in operations}
    if len(expected) != 28:
        err(f"grammar enums give {len(expected)} cells, expected 28")
    for cell in sorted(expected - set(cells)):
        err(f"missing cell {cell}")
    for cell in sorted(set(cells) - expected):
        err(f"unknown cell {cell} (outside the grammar enums)")
    for (m, o), c in sorted(cells.items()):
        if c.get("base_packs") not in bases:
            err(f"cell ({m}, {o}): base_packs {c.get('base_packs')!r} names no modality base set")
        if m == "audio" and c.get("coverage_gap_notice") != "mandatory":
            err(f"cell ({m}, {o}): audio cell lacks the mandatory coverage-gap notice")
    if not str(doc.get("coverage_gap_notice") or "").strip():
        err("coverage_gap_notice text is empty")

    # (4b) largest legal combination
    if all(isinstance(budgets.get(p), int) for p in closed):
        block = doc.get("system_prompt_block_tokens") or 0
        notice = doc.get("coverage_gap_notice_tokens") or 0
        limit = doc.get("per_request_max_tokens")
        if limit != COMBO_MAX_TOKENS:
            err(f"per_request_max_tokens is {limit}, the contract envelope is {COMBO_MAX_TOKENS}")
        worst = 0
        base_names = list(bases)
        for combo_bases in [[b] for b in base_names] + [["static_image", "video"]]:
            packs = set(universal) | {p for b in combo_bases for p in bases.get(b, [])} | set(conditionals)
            total = sum(budgets.get(p, 0) for p in packs) + block + notice
            worst = max(worst, total)
        if worst > COMBO_MAX_TOKENS:
            err(f"largest legal combination {worst} tokens > {COMBO_MAX_TOKENS}")

    # system-prompt block within its declared budget (INJECTION-CONTRACT §2)
    contract = CONTRACT.read_text()
    m = re.search(r"```\n(.*?)```", contract, re.S)
    if not m:
        err("INJECTION-CONTRACT-v0.md: no fenced system-prompt block found")
    else:
        block_tokens = (len(m.group(1)) + 3) // 4
        declared_block = doc.get("system_prompt_block_tokens") or 0
        if block_tokens > declared_block:
            err(f"system-prompt block is {block_tokens} tokens > declared {declared_block}")
    return errors


# ── reproducibility (check 7) ────────────────────────────────────────────────

def validate_reproducibility() -> list:
    errors: list = []
    spec = importlib.util.spec_from_file_location(
        "compile_pilot_packs_v", ROOT / "canon/compilation/compile_pilot_packs.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    try:
        first = mod.generate()
        second = mod.generate()
    except SystemExit as exc:
        return [f"compiler refused to generate: {exc}"]
    for path, text in first.items():
        if second[path] != text:
            errors.append(f"{path.name}: two compiles differ — non-determinism")
        if not path.exists():
            errors.append(f"{path.name}: committed file missing")
        elif path.read_text() != text:
            errors.append(f"{path.name}: committed bytes differ from recompilation")
    return errors


# ── deliverable-wide HOLD scan (check 9) ─────────────────────────────────────

def validate_no_hold_ids(env: dict) -> list:
    errors: list = []
    for path in DELIVERABLES:
        if not path.exists():
            errors.append(f"{path.name}: deliverable missing")
            continue
        raw = path.read_text()
        if re.search(r"sk_abcd_\d+", raw):
            errors.append(f"{path.name}: contains an sk_abcd_ (HOLD) id")
        for token in sorted(set(re.findall(r"\b(?:sk|scs)_[a-z0-9_]*\d\b", raw))):
            if token in env["candidate_ids"] or token not in env["owner"]:
                errors.append(f"{path.name}: id-shaped token {token} does not resolve in "
                              "accepted Canon (HOLD/unknown)")
    return errors


def main(argv=None) -> int:
    env = load_environment()
    all_errors: list = []
    digest_errors: list = []
    digest = recompute_corpus_digest(digest_errors)
    all_errors += digest_errors

    for path in PACK_PATHS:
        if not path.exists():
            all_errors.append(f"{path.name}: missing")
            continue
        errors = validate_pack(path, env, digest)
        all_errors += errors
        if not errors:
            pack = yaml.safe_load(path.read_text())
            print(f"PASS {path.name} ({pack['counts']['decisions']} decisions, "
                  f"{pack['counts']['cited_sk_objects']} sk objects, "
                  f"{pack['counts']['terse_tokens']}/{TERSE_MAX_TOKENS} terse tokens)")

    trig_errors = validate_triggers(TRIGGERS, env)
    all_errors += trig_errors
    if not trig_errors:
        print(f"PASS {TRIGGERS.name} (28 cells total, closed pack set, combination budget holds)")

    repro = validate_reproducibility()
    all_errors += repro
    if not repro:
        print("PASS reproducibility (double compile byte-identical with committed packs)")

    hold = validate_no_hold_ids(env)
    all_errors += hold
    if not hold:
        print(f"PASS HOLD-id scan over {len(DELIVERABLES)} deliverables")

    if all_errors:
        print(f"FAIL ({len(all_errors)} error{'s' if len(all_errors) != 1 else ''})")
        for e in all_errors:
            print(f"  - {e}")
        return 1
    print("PASS: all compiled-pack checks hold. This establishes structure over committed "
          "bytes — not relevance, quality, outcomes, or adoption.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
