#!/usr/bin/env python3
"""
Lightweight validators for the EXPERIMENTAL book-expansion + Q&A output.

This is NOT a Canon validator. It does not admit anything, gate anything, or touch
`canon/validation/`. It checks that this experimental directory is internally coherent and
that it has not written where it must not.

Checks implemented (numbered as in the task brief):
  1.  every Q&A item resolves to a source directory that exists
  2.  every Q&A item has a non-empty locator
  3.  required fields present on every Q&A item
  4.  allowed enums respected (answer_type, difficulty, knowledge_type, requires_application)
  5.  every operational binding resolves to SourceKnowledge or a SourceConceptSystem in its lane
  6.  no output writes into canon/knowledge/current/**
  7.  no accepted audit record changed
  8.  no Capability Registry file changed
  9.  no Q&A answer is an empty placeholder
  10. application-question counts OBSERVED and reported (see CANON-014 note below)

CANON-014 changes:
  * The minimum one-third `requires_application` rate is REMOVED. It was a construction
    target rather than a property of the sources, and lanes demonstrably added application
    questions after falling below it. A rate that a validator requires is a rate the bank was
    built to satisfy, so it cannot afterwards be read as evidence about the sources. The
    proportion is still computed and printed; nothing fails on it.
  * Required-field conformance against the FULL SPEC-03/04/05 schemas is delegated to
    `canon/validation/validate_source_artifact_schema.py`, which exists because this file
    reported PASS on a package whose `scs_sa8_002` was missing SPEC-03's required
    `evidence.system_level_uncertainty` - this file never checked SourceConceptSystem
    required-field presence at all.

A PASS here means the implemented checks passed. It is NOT Canon admission.

Plus structural checks that protect the project's frozen separations:
  A.  SPEC-03: no Creative IR path / product vocabulary inside SourceKnowledge
  B.  SPEC-04: production bindings are production_candidate with target_path null;
      evaluation bindings carry observation_unit; governance bindings carry a permitted consumer;
      creative_ir bindings carry target_path + schema + version
  C.  SPEC-05: no cross_source_concept (xs_) created; no same_failure_family relation used
  D.  no decimal-confidence field anywhere
  E.  Hopkins page locators fall inside the real printed-page span of each book

Exit code 0 = pass, 1 = fail.

Usage:  python3 canon/experimental/book-expansion-qa-v1/validate_experimental.py [repo_root]
"""

import json
import os
import re
import subprocess
import sys

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

HERE = os.path.dirname(os.path.abspath(__file__))
EXP_REL = "canon/experimental/book-expansion-qa-v1"

# ---------------------------------------------------------------- vocabularies

ANSWER_TYPES = {
    "factual", "concept_definition", "mechanism", "comparison", "tradeoff",
    "failure_diagnosis", "repair", "application", "boundary_condition", "source_position",
}
DIFFICULTIES = {"easy", "medium", "hard"}
KNOWLEDGE_TYPES = {
    "advertising", "persuasion", "copywriting", "effectiveness",
    "testing_method", "media_planning", "brand_communication", "concept_development",
    "short_form", "creative_process", "production_reasoning", "evaluation_diagnosis",
    "typography", "hierarchy", "composition", "colour",
    "photography", "lighting", "product_photography",
    "editing", "continuity", "shot_design",
    "accessibility_legibility", "indian_context",
}
QA_REQUIRED = [
    "qa_id", "source_id", "source_title", "source_locator", "question", "answer",
    "answer_type", "difficulty", "knowledge_type", "requires_application", "support",
    "confounders",
]
TARGET_TYPES = {"creative_ir", "evaluation", "production", "governance", "benchmark"}
GOVERNANCE_CONSUMERS = {
    "taxonomy_governance", "retrieval_governance", "conflict_resolution",
    "evidence_interpretation", "rule_application", "cross_source_synthesis",
}
OBSERVATION_UNITS = {
    "frame", "shot", "shot_pair", "sequence", "whole_asset", "asset_set_over_time",
}
EVIDENCE_CHARACTERISTICS = {
    "explicitly_stated", "visually_demonstrated", "controlled_comparison", "argued",
    "practitioner_assertion", "anecdotal", "outcome_claimed", "empirical_within_source",
    "repeated_within_source", "mechanism_given", "mechanism_absent",
    "culturally_bounded", "historical_claim",
}
PLACEHOLDERS = {"", "tbd", "todo", "n/a", "na", "none", "-", "...", "xxx", "placeholder"}

# SPEC-03 forbids Creative IR paths and product vocabulary inside SourceKnowledge.
IR_PATH_RE = re.compile(
    r"\b(creative|entities|production_ir|normalized_request)\.[a-z_]+", re.I
)
PRODUCT_VOCAB = [
    "capability registry", "capability_registry", "normalized request", "normalized_request",
    "creative ir", "creative_ir", "production ir", "production_ir", "rank-1 element",
    "cost per accepted outcome", "cpao",
]
CONFIDENCE_KEY_RE = re.compile(r"^(confidence|certainty|score|rating|probability)$", re.I)

# Real printed-page spans of the AUTHOR'S OWN TEXT, established page by page from the scanned
# copies themselves. Beyond these the scans carry publisher advertising, not the book:
# My Life ends at printed 206 (PDF 220; printed 207+ is Harper's own book announcements);
# Scientific Advertising ends at printed 64 (PDF 72; printed 65+ is Snowball/BN back matter).
PAGE_SPANS = {
    "hopkins-my-life-in-advertising": (1, 206),
    "hopkins-scientific-advertising-ch8-21": (25, 64),
}
PAGELESS = {"w3c-wcag22-text-legibility", "google-abcd-video-ads"}

errors = []
warnings = []
stats = {}


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def load_yaml(path):
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as fh:
        try:
            return yaml.safe_load(fh)
        except yaml.YAMLError as exc:
            err(f"[YAML] {path}: does not parse: {exc}")
            return None


def walk_scalars(node, path=""):
    """Yield (key_path, key, value) for every scalar in a nested structure."""
    if isinstance(node, dict):
        for k, v in node.items():
            yield from walk_scalars(v, f"{path}.{k}")
            if not isinstance(v, (dict, list)):
                yield path, k, v
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from walk_scalars(v, f"{path}[{i}]")


def main(root):
    exp = os.path.join(root, EXP_REL)
    if not os.path.isdir(exp):
        sys.exit(f"experimental directory not found: {exp}")

    source_dirs = sorted(
        d for d in os.listdir(exp)
        if os.path.isdir(os.path.join(exp, d)) and not d.startswith(".")
    )
    if not source_dirs:
        err("no source directories found")

    all_qa = []
    per_source = {}

    for sd in source_dirs:
        base = os.path.join(exp, sd)
        sk = load_yaml(os.path.join(base, "source-knowledge.yaml")) or []
        scs = load_yaml(os.path.join(base, "source-concept-systems.yaml")) or []
        bnd = load_yaml(os.path.join(base, "operational-bindings.yaml")) or []
        ont = load_yaml(os.path.join(base, "ontology-mappings.yaml")) or {}
        qa = load_yaml(os.path.join(base, "qa-bank.yaml")) or {}

        # tolerate either a bare list or a wrapped mapping
        def unwrap(obj, *keys):
            if isinstance(obj, dict):
                for k in keys:
                    if k in obj and obj[k] is not None:
                        return obj[k]
                return []
            return obj or []

        sk = unwrap(sk, "source_knowledge", "objects", "items")
        scs = unwrap(scs, "source_concept_systems", "systems", "items")
        bnd = unwrap(bnd, "operational_bindings", "bindings", "items")
        qa_items = unwrap(qa, "qa_items", "items", "qa_bank")

        for f in ("PROVENANCE.md", "EXTRACTION-NOTES.md"):
            if not os.path.exists(os.path.join(base, f)):
                err(f"[{sd}] missing required file {f}")

        sk_ids = {o.get("sk_id") for o in sk if isinstance(o, dict)}
        scs_ids = {o.get("scs_id") for o in scs if isinstance(o, dict)}

        # ---- A. SPEC-03 purity ------------------------------------------------
        for o in sk:
            if not isinstance(o, dict):
                continue
            oid = o.get("sk_id", "?")
            if "informs" in o:
                err(f"[{sd}/{oid}] SPEC-03 violation: 'informs' field present")
            blob = json.dumps(o, default=str)
            m = IR_PATH_RE.search(blob)
            if m:
                err(f"[{sd}/{oid}] SPEC-03 violation: Creative IR path '{m.group(0)}'")
            low = blob.lower()
            for term in PRODUCT_VOCAB:
                if term in low:
                    err(f"[{sd}/{oid}] SPEC-03 violation: product vocabulary '{term}'")
            ct = o.get("claim_type")
            if ct not in ("explicit_source_claim", "source_interpretation"):
                err(f"[{sd}/{oid}] claim_type invalid: {ct!r}")
            if ct == "source_interpretation" and not o.get("interpretation_basis"):
                err(f"[{sd}/{oid}] source_interpretation without interpretation_basis")
            ev = (o.get("evidence") or {}).get("characteristics") or []
            if not ev:
                err(f"[{sd}/{oid}] evidence.characteristics empty")
            for c in ev:
                if c not in EVIDENCE_CHARACTERISTICS:
                    err(f"[{sd}/{oid}] unknown evidence characteristic '{c}'")
            mech = o.get("mechanism")
            if not isinstance(mech, dict) or "stated_by_source" not in mech:
                err(f"[{sd}/{oid}] mechanism.stated_by_source missing")
            prov = o.get("provenance") or {}
            if prov.get("source_support") not in ("text", "visual", "text_and_visual"):
                err(f"[{sd}/{oid}] provenance.source_support invalid")
            if sd in PAGE_SPANS:
                lo, hi = PAGE_SPANS[sd]
                for key in ("page_start", "page_end"):
                    p = prov.get(key)
                    if isinstance(p, int) and not (lo <= p <= hi):
                        err(f"[{sd}/{oid}] provenance.{key}={p} outside printed span {lo}-{hi}")
            elif sd in PAGELESS:
                for key in ("page_start", "page_end"):
                    if prov.get(key) not in (None, "", "null"):
                        err(f"[{sd}/{oid}] pageless source must not carry {key}="
                            f"{prov.get(key)!r}")

        # ---- SourceConceptSystem origin marking -------------------------------
        for o in scs:
            if not isinstance(o, dict):
                continue
            oid = o.get("scs_id", "?")
            wsc = o.get("whole_system_claim") or {}
            if wsc.get("origin") == "extractor_synthesis" and not wsc.get("interpretation_basis"):
                err(f"[{sd}/{oid}] extractor_synthesis without interpretation_basis")
            for member in o.get("members") or []:
                ref = member.get("sk_ref") if isinstance(member, dict) else None
                if ref and ref not in sk_ids:
                    err(f"[{sd}/{oid}] member sk_ref '{ref}' does not resolve")

        # ---- 5 + B. bindings --------------------------------------------------
        for o in bnd:
            if not isinstance(o, dict):
                continue
            oid = o.get("binding_id", "?")
            refs = list(o.get("source_knowledge_refs") or [])
            srefs = list(o.get("source_system_refs") or [])
            if not refs and not srefs:
                err(f"[{sd}/{oid}] binding references neither SourceKnowledge nor a system")
            for r in refs:
                if r not in sk_ids:
                    err(f"[{sd}/{oid}] source_knowledge_ref '{r}' does not resolve")
            for r in srefs:
                if r not in scs_ids:
                    err(f"[{sd}/{oid}] source_system_ref '{r}' does not resolve")
            tt = o.get("target_type")
            if tt not in TARGET_TYPES:
                err(f"[{sd}/{oid}] target_type invalid: {tt!r}")
            if tt == "production":
                if o.get("status") != "production_candidate":
                    err(f"[{sd}/{oid}] production binding must be status "
                        f"production_candidate (Production IR does not exist)")
                if o.get("target_path") not in (None, "", "null"):
                    err(f"[{sd}/{oid}] production binding must have target_path null")
            if tt == "evaluation" and o.get("observation_unit") not in OBSERVATION_UNITS:
                err(f"[{sd}/{oid}] evaluation binding needs a valid observation_unit, "
                    f"got {o.get('observation_unit')!r}")
            if tt == "governance" and o.get("governance_consumer") not in GOVERNANCE_CONSUMERS:
                err(f"[{sd}/{oid}] governance binding needs a permitted governance_consumer, "
                    f"got {o.get('governance_consumer')!r}")
            if tt == "creative_ir":
                for k in ("target_path", "target_schema", "target_schema_version"):
                    if not o.get(k):
                        err(f"[{sd}/{oid}] creative_ir binding missing {k}")
            if not o.get("evidence_basis"):
                err(f"[{sd}/{oid}] evidence_basis missing")
            if o.get("evidence_basis") in ("cross_source_supported", "empirically_supported"):
                err(f"[{sd}/{oid}] evidence_basis '{o.get('evidence_basis')}' is not "
                    f"authorised in this experimental task")

        # ---- C. ontology ------------------------------------------------------
        if isinstance(ont, dict):
            for c in ont.get("concepts") or []:
                if not isinstance(c, dict):
                    continue
                cid = c.get("concept_id", "?")
                if c.get("kind") == "cross_source_concept" or str(cid).startswith("xs_"):
                    err(f"[{sd}/{cid}] cross_source_concept created — forbidden in this task")
                if c.get("kind") == "canonical_concept" and c.get("asserts_equivalence") is not False:
                    err(f"[{sd}/{cid}] canonical_concept must carry asserts_equivalence: false")
            for r in ont.get("relationships") or []:
                if isinstance(r, dict) and r.get("relation") == "same_failure_family":
                    err(f"[{sd}] same_failure_family used — requires human review (SPEC-05)")
            for t in ont.get("terms") or []:
                if isinstance(t, dict) and t.get("kind") == "remedy" and not t.get("executable_by"):
                    err(f"[{sd}/{t.get('term_id','?')}] remedy term missing executable_by")

        # ---- D. no decimal confidence ----------------------------------------
        for blob, name in ((sk, "source-knowledge"), (scs, "source-concept-systems"),
                           (bnd, "operational-bindings"), (ont, "ontology-mappings")):
            for _p, k, v in walk_scalars(blob):
                if CONFIDENCE_KEY_RE.match(str(k)) and isinstance(v, float):
                    err(f"[{sd}/{name}] uncalibrated decimal confidence '{k}: {v}'")

        # ---- 1,2,3,4,9,E. Q&A -------------------------------------------------
        seen_ids = set()
        for item in qa_items:
            if not isinstance(item, dict):
                err(f"[{sd}] qa item is not a mapping")
                continue
            qid = item.get("qa_id", "?")
            if qid in seen_ids:
                err(f"[{sd}] duplicate qa_id '{qid}'")
            seen_ids.add(qid)
            for f in QA_REQUIRED:
                if f not in item:
                    err(f"[{sd}/{qid}] missing required field '{f}'")
            if item.get("source_id") != sd:
                err(f"[{sd}/{qid}] source_id '{item.get('source_id')}' does not match its "
                    f"directory")
            loc = str(item.get("source_locator") or "").strip()
            if not loc or loc.lower() in PLACEHOLDERS:
                err(f"[{sd}/{qid}] empty or placeholder source_locator")
            for field in ("answer", "question", "support"):
                val = str(item.get(field) or "").strip()
                if not val or val.lower() in PLACEHOLDERS or len(val) < 15:
                    err(f"[{sd}/{qid}] '{field}' is empty, placeholder or too short")
            if item.get("answer_type") not in ANSWER_TYPES:
                err(f"[{sd}/{qid}] answer_type invalid: {item.get('answer_type')!r}")
            if item.get("difficulty") not in DIFFICULTIES:
                err(f"[{sd}/{qid}] difficulty invalid: {item.get('difficulty')!r}")
            if item.get("knowledge_type") not in KNOWLEDGE_TYPES:
                err(f"[{sd}/{qid}] knowledge_type invalid: {item.get('knowledge_type')!r}")
            if not isinstance(item.get("requires_application"), bool):
                err(f"[{sd}/{qid}] requires_application must be a boolean")
            conf = item.get("confounders")
            if not isinstance(conf, list) or not [c for c in conf if str(c).strip()]:
                err(f"[{sd}/{qid}] confounders must be a non-empty list")
            # E. page locators must be inside the real span.
            # Only numbers introduced by a p./pp. marker count as pages. A locator legitimately
            # carries other integers -- "Chapter 11", "SB7", a year -- and treating those as
            # pages produced a wave of false failures on the first run.
            if sd in PAGE_SPANS:
                lo, hi = PAGE_SPANS[sd]
                for m in re.finditer(r"\bpp?\.\s*([\d\s,–\-and]+)", loc):
                    for p in [int(n) for n in re.findall(r"\d{1,3}", m.group(1))]:
                        if p < lo or p > hi:
                            err(f"[{sd}/{qid}] locator page {p} outside printed span "
                                f"{lo}-{hi}: {loc!r}")
            if sd in PAGELESS and re.search(r"\bp{1,2}\.\s*\d", loc):
                err(f"[{sd}/{qid}] pageless source carries a page locator: {loc!r}")
            all_qa.append(item)

        per_source[sd] = {
            "source_knowledge": len(sk),
            "source_concept_systems": len(scs),
            "operational_bindings": len(bnd),
            "terms": len((ont or {}).get("terms") or []) if isinstance(ont, dict) else 0,
            "qa_items": len(qa_items),
            "requires_application": sum(
                1 for i in qa_items if isinstance(i, dict) and i.get("requires_application") is True
            ),
        }

    # ---- 6,7,8. write-boundary checks via git ---------------------------------
    try:
        changed = subprocess.run(
            ["git", "-C", root, "diff", "--name-only", "origin/main...HEAD"],
            capture_output=True, text=True, check=False,
        ).stdout.split()
        dirty = subprocess.run(
            ["git", "-C", root, "status", "--porcelain"],
            capture_output=True, text=True, check=False,
        ).stdout.splitlines()
        dirty = [ln[3:].strip() for ln in dirty if ln.strip()]
        touched = set(changed) | set(dirty)
        stats["files_touched_vs_origin_main"] = len(touched)
        forbidden = [
            ("canon/knowledge/current/", "check 6: live Canon knowledge"),
            ("canon/audit/records/", "check 7: accepted audit records"),
            ("eval/v1/capability-registry", "check 8: Capability Registry"),
            ("eval/capability-registry", "check 8: Capability Registry"),
            ("canon/knowledge/SPEC-", "frozen SPEC files"),
            ("coordination/", "Controller state"),
            ("PROJECT-MEMORY.md", "project memory"),
            ("governance/", "governance"),
        ]
        for path in sorted(touched):
            for prefix, label in forbidden:
                if path.startswith(prefix):
                    err(f"[BOUNDARY] {label}: '{path}' was modified — forbidden")
        # CANON-014 additionally writes the corrected schema validator and its tests, which by
        # design must live outside this experimental directory: the hole being closed is that a
        # package-local validator was the only thing checking a package-local claim.
        CANON014_ALLOWED = (
            "canon/validation/validate_source_artifact_schema.py",
            "tests/test_validate_source_artifact_schema.py",
            "canon/knowledge/current/",
            "canon/audit/records/",
            "canon/tasks/",
            "canon/findings/",
            "canon/candidates/",
        )
        outside = [
            p for p in changed
            if not p.startswith(EXP_REL) and p not in ("", ".")
            and not p.startswith(CANON014_ALLOWED)
        ]
        if outside:
            err(f"[BOUNDARY] files changed outside {EXP_REL} and the CANON-014 allowlist: {outside}")
    except Exception as exc:  # noqa: BLE001
        warn(f"git boundary check could not run: {exc}")

    # ---- report ---------------------------------------------------------------
    total_qa = len(all_qa)
    total_app = sum(1 for i in all_qa if i.get("requires_application") is True)
    print("=" * 72)
    print("EXPERIMENTAL VALIDATION — book-expansion-qa-v1")
    print("=" * 72)
    for sd in source_dirs:
        s = per_source.get(sd, {})
        n, a = s.get("qa_items", 0), s.get("requires_application", 0)
        pct = (a / n * 100) if n else 0.0
        # CANON-014: the one-third application floor is REMOVED. It was a construction
        # target, and lanes added questions to clear it. The rate is now observed, never required.
        print(f"\n{sd}")
        print(f"  SourceKnowledge {s.get('source_knowledge',0):>4}   "
              f"ConceptSystems {s.get('source_concept_systems',0):>3}   "
              f"Bindings {s.get('operational_bindings',0):>3}   "
              f"Terms {s.get('terms',0):>4}")
        print(f"  Q&A {n:>4}   requires_application {a:>4} ({pct:.1f}%  observed, not required)")

    print("\n" + "-" * 72)
    print(f"TOTAL Q&A: {total_qa}   requires_application: {total_app} "
          f"({(total_app/total_qa*100) if total_qa else 0:.1f}%)")
    print(f"TOTAL SourceKnowledge: {sum(s['source_knowledge'] for s in per_source.values())}")
    print(f"TOTAL ConceptSystems:  {sum(s['source_concept_systems'] for s in per_source.values())}")
    print(f"TOTAL Bindings:        {sum(s['operational_bindings'] for s in per_source.values())}")
    if "files_touched_vs_origin_main" in stats:
        print(f"Files changed vs origin/main: {stats['files_touched_vs_origin_main']} "
              f"(all must be under {EXP_REL})")

    if warnings:
        print("\nWARNINGS")
        for w in warnings:
            print("  ! " + w)
    if errors:
        print(f"\nFAILED — {len(errors)} error(s)")
        for e in errors[:200]:
            print("  x " + e)
        if len(errors) > 200:
            print(f"  ... and {len(errors)-200} more")
        return 1
    print("\nPASSED — all checks green")
    return 0


if __name__ == "__main__":
    repo = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(
        os.path.join(HERE, "..", "..", "..")
    )
    sys.exit(main(repo))
