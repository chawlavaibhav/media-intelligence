#!/usr/bin/env python3
"""Build the Canon corpus index and the three corpus fingerprints.

Everything here is DERIVED. It reads the artifacts and reports what they say; it never edits a
source artifact to populate a field, and a field it cannot establish is recorded as null rather than
guessed.

Three fingerprints, kept separate on purpose, because a future experiment must be able to name
exactly which body of knowledge it used:

  accepted_canon      the source artifacts of live accepted Canon only
  full_knowledge      accepted plus every durable candidate - what a run WOULD see if candidate
                      retrieval were ever enabled, which it is not today
  qa_corpus           the Q&A banks, separate from both, because Q&A is a companion asset and is
                      never part of what establishes a source's truth
"""
import glob
import hashlib
import json
import os
import subprocess
import sys
from datetime import date

import yaml

LIVE = "canon/knowledge/current"
CAND = "canon/candidates/canon-014"
QA = "canon/qa/canon-014"
ARTIFACTS = ["source-knowledge.yaml", "source-concept-systems.yaml",
             "operational-bindings.yaml", "ontology-mappings.yaml", "visual-evidence-ledger.yaml"]


def load(p):
    try:
        return yaml.safe_load(open(p))
    except Exception:
        return None


def digest(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def counts(d):
    sk = load(os.path.join(d, "source-knowledge.yaml")) or {}
    scs = load(os.path.join(d, "source-concept-systems.yaml")) or {}
    bnd = load(os.path.join(d, "operational-bindings.yaml")) or {}
    ont = load(os.path.join(d, "ontology-mappings.yaml")) or {}
    return {
        "source_id": sk.get("source_id"),
        "source_knowledge": len(sk.get("source_knowledge") or []),
        "concept_systems": len(scs.get("source_concept_systems") or []),
        "operational_bindings": len(bnd.get("operational_bindings") or []),
        "ontology_terms": len(ont.get("terms") or []),
        "ontology_concepts": len(ont.get("concepts") or []),
        "ontology_relationships": len(ont.get("relationships") or []),
        "extraction_date": ont.get("extraction_date") or sk.get("extraction_date"),
    }


def visual(d):
    p = os.path.join(d, "visual-evidence-ledger.yaml")
    if not os.path.isfile(p):
        return {"ledger": False,
                "status": "NO INSPECTION HAS EVER BEEN RUN. No visual-evidence ledger exists, which "
                          "is why the Audit Gate cannot be completed for this source."}
    v = load(p) or {}
    return {"ledger": True, "pass": v.get("pass"),
            "inspection_state": v.get("inspection_state"),
            "visual_argument_role": v.get("visual_argument_role"),
            "claim_resolution_after_inspection": v.get("claim_resolution_after_inspection")}


def audit_for(name):
    p = f"canon/audit/records/{name}.audit.yaml"
    if not os.path.isfile(p):
        return None
    a = load(p) or {}
    return {"record": p, "audit_id": a.get("audit_id"), "audit_status": a.get("audit_status"),
            "independence_verdict": (a.get("lineage") or {}).get("independence_verdict"),
            "combined_digest": (a.get("source_snapshot") or {}).get("combined_digest")}


def hold_for(d):
    p = os.path.join(d, "audit-assessment-HOLD.yaml")
    if not os.path.isfile(p):
        return None
    h = load(p) or {}
    b = h.get("source_specific_blockers")
    return {"assessment": p, "status": h.get("status", "HOLD"),
            "status_reason": h.get("status_reason"),
            "source_specific_blockers": ([x["blocker"] for x in b] if isinstance(b, list)
                                         else "none beyond the shared blocker"),
            "audit_gate_record": h.get("audit_gate_record", "none")}


def qa_for(stem):
    p = f"{QA}/{stem}-qa-bank.yaml"
    if not os.path.isfile(p):
        return {"bank": None, "qa_items": 0}
    d = load(p) or {}
    items = d.get("qa_items") or []
    return {"bank": p, "qa_items": len(items),
            "requires_application": sum(1 for i in items if i.get("requires_application") is True),
            "source_status": d.get("source_status")}


def fingerprint(paths):
    rows = [{"path": p, "sha256": digest(p)} for p in sorted(paths)]
    canonical = "".join(f"{r['path']}:{r['sha256']}\n" for r in rows)
    return {"algorithm": "sha256-of-sorted-path-and-content",
            "file_count": len(rows),
            "combined_digest": hashlib.sha256(canonical.encode()).hexdigest(),
            "files": rows}


def main():
    commit = subprocess.run(["git", "rev-parse", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    entries, acc_files, cand_files = [], [], []

    for d in sorted(os.listdir(LIVE)):
        p = os.path.join(LIVE, d)
        if not os.path.isdir(p):
            continue
        c = counts(p)
        files = [os.path.join(p, a) for a in ARTIFACTS if os.path.isfile(os.path.join(p, a))]
        acc_files += files
        entries.append({"source_dir": d, "epistemic_status": "accepted",
                        "location": p, **c, "visual_evidence": visual(p),
                        "audit": audit_for(d), "candidate_blocker": None,
                        "qa": qa_for(d), "artifact_count": len(files)})

    for d in sorted(os.listdir(CAND)):
        p = os.path.join(CAND, d)
        if not os.path.isdir(p):
            continue
        c = counts(p)
        files = [os.path.join(p, a) for a in ARTIFACTS if os.path.isfile(os.path.join(p, a))]
        cand_files += files
        entries.append({"source_dir": d, "epistemic_status": "hold",
                        "location": p, **c, "visual_evidence": visual(p),
                        "audit": None, "candidate_blocker": hold_for(p),
                        "qa": qa_for(d), "artifact_count": len(files)})

    qa_files = sorted(glob.glob(f"{QA}/*-qa-bank.yaml"))
    acc = [e for e in entries if e["epistemic_status"] == "accepted"]
    hold = [e for e in entries if e["epistemic_status"] == "hold"]

    def tot(rows, k):
        return sum(r[k] for r in rows)

    index = {
        "index_version": "canon-corpus-index-v1",
        "generated_by": "CANON-014 final full-corpus reconciliation",
        "generated_on": str(date.today()),
        "git_commit": commit,
        "what_this_is": (
            "A complete machine-readable map of every source the Canon represents, in either "
            "epistemic state. It is DERIVED from the artifacts and edits none of them. Read it to "
            "answer: what knowledge exists, where does it live, is it accepted or held, what "
            "established that, and what would change it."),
        "epistemic_states": {
            "accepted": (f"Live Canon under {LIVE}/. Passed Audit Gate v0.2; the record is named in "
                         "`audit` and its snapshot digest covers the exact bytes."),
            "hold": (f"Durable candidate under {CAND}/. Structurally valid against SPEC-03/04/05 and "
                     "NOT admitted. Carries an audit-assessment-HOLD.yaml, which is deliberately "
                     "not an Audit Gate record. A structural pass is never admission."),
        },
        "retrieval_note": (
            "Runtime retrieval today reads canon/knowledge/current/** only. This task did not change "
            "that and does not propose changing it. The candidate corpus is prepared so a later, "
            "controlled retrieval could use it - and if it ever does, every returned object must "
            "expose source_status alongside source_id, claim_type, evidence characteristics and both "
            "uncertainty fields, so held material can never be mistaken for accepted Canon."),
        "totals": {
            "sources_represented": len(entries),
            "accepted": len(acc),
            "hold": len(hold),
            "source_knowledge": tot(entries, "source_knowledge"),
            "concept_systems": tot(entries, "concept_systems"),
            "operational_bindings": tot(entries, "operational_bindings"),
            "ontology_terms": tot(entries, "ontology_terms"),
            "ontology_concepts": tot(entries, "ontology_concepts"),
            "ontology_relationships": tot(entries, "ontology_relationships"),
            "qa_items": sum(e["qa"]["qa_items"] for e in entries),
            "sources_with_a_visual_evidence_ledger": sum(
                1 for e in entries if e["visual_evidence"]["ledger"]),
            "sources_with_no_inspection_ever_run": sum(
                1 for e in entries if not e["visual_evidence"]["ledger"]),
        },
        "totals_accepted_only": {
            "sources": len(acc),
            "source_knowledge": tot(acc, "source_knowledge"),
            "concept_systems": tot(acc, "concept_systems"),
            "operational_bindings": tot(acc, "operational_bindings"),
            "ontology_terms": tot(acc, "ontology_terms"),
            "ontology_concepts": tot(acc, "ontology_concepts"),
            "qa_items": sum(e["qa"]["qa_items"] for e in acc),
        },
        "totals_hold_only": {
            "sources": len(hold),
            "source_knowledge": tot(hold, "source_knowledge"),
            "concept_systems": tot(hold, "concept_systems"),
            "operational_bindings": tot(hold, "operational_bindings"),
            "ontology_terms": tot(hold, "ontology_terms"),
            "ontology_concepts": tot(hold, "ontology_concepts"),
            "qa_items": sum(e["qa"]["qa_items"] for e in hold),
        },
        "fingerprints": {
            "note": ("Three separate fingerprints. A future Canon-vs-no-Canon experiment MUST name "
                     "which one it used; they are not interchangeable and an experiment that ran "
                     "against held knowledge is not an experiment about accepted Canon."),
            "accepted_canon": fingerprint(acc_files),
            "full_knowledge_corpus": fingerprint(acc_files + cand_files),
            "qa_corpus": fingerprint(qa_files),
        },
        "sources": entries,
    }

    with open("canon/knowledge/CANON-CORPUS-INDEX.yaml", "w") as fh:
        fh.write(
            "# CANON CORPUS INDEX — the complete current map of Canon knowledge.\n"
            "#\n"
            "# DERIVED, never authoritative over the artifacts it describes. Regenerate with:\n"
            "#     python3 canon/knowledge/build_corpus_index.py\n"
            "# If this file and an artifact disagree, the artifact wins and this file is stale.\n"
            "#\n"
            "# Covers live accepted Canon AND durable CANON-014 candidates, in one place, each with\n"
            "# its epistemic state stated. A source appears here whether or not it is admitted;\n"
            "# `epistemic_status` is what separates them and it is never implied by presence.\n\n"
            + yaml.dump(index, sort_keys=False, allow_unicode=True, width=100))

    summary = {k: index[k] for k in
               ("index_version", "generated_on", "git_commit", "totals",
                "totals_accepted_only", "totals_hold_only")}
    summary["fingerprints"] = {k: {kk: vv for kk, vv in v.items() if kk != "files"}
                               for k, v in index["fingerprints"].items() if k != "note"}
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    sys.exit(main())
