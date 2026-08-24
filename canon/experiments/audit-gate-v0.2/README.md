# Audit Gate v0.2 — experimental, NOT authoritative

**Task:** CANON-004 · **Status:** candidate design under test · **Do not consume downstream.**

Everything in this directory is an experiment. Nothing here changes SPEC-03, SPEC-04 or SPEC-05,
and nothing here has been approved by the Controller.

## What this is

CANON-003 concluded that the three-layer Canon architecture (SourceKnowledge → source
systems/ontology → OperationalBindings) should be kept, but that the extraction *procedure* stopped
forcing five useful questions once source truth was cleanly separated from product use:

1. what the available copy of the source hid, distorted or destroyed;
2. where each claim's evidence actually came from;
3. whether anything in today's product can use the knowledge;
4. whether two sources that appear to agree are actually independent;
5. whether an old technical claim is still true.

This directory holds a candidate **post-extraction Audit Gate**: a separate record, written after a
book's source knowledge is frozen, that asks those five questions and records the answers in a form
a machine can read.

## Layout

| Path | What it is |
|---|---|
| `SCHEMA-audit-record-v0.2.md` | the candidate data model and its controlled vocabularies |
| `records/*.audit.yaml` | one experimental audit record per accepted CANON-003 book (16) |
| `../../validation/validate_audit_gate_v02.py` | the mechanical validator for these records |
| `../../../tests/test_validate_audit_gate_v02.py` | its regression tests |

The findings and the Controller decision brief live in `canon/findings/`:
`CANON-004-audit-gate-design.md` and `CANON-004-CONTROLLER-BRIEF.md`.

## Rules that held while these records were written

- **No source book was re-opened.** Every record is built from committed repository evidence —
  `source-knowledge.yaml`, `visual-evidence-ledger.yaml`, `operational-bindings.yaml`,
  `ontology-mappings.yaml`, `PROVENANCE.md`, and the CANON-003 lane issue files. Where the
  repository record could not settle a question, the record says so rather than guessing.
- **No accepted source claim was reinterpreted or rewritten.** The audit sits beside the frozen
  source record and points at it by `sk_id`. It never edits it.
- **The audit is not a quality score.** There is no rank, rating, grade or confidence number
  anywhere in the model, and the validator refuses a record that introduces one.
