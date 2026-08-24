# Audit Gate v0.2 — experiment history (nothing here is active)

**This directory is a historical pointer. It contains no active records, no active schema and no
tooling. Do not edit anything here expecting it to take effect.**

The Post-Extraction Audit Gate was designed and tested here under CANON-004, against the frozen
16-book CANON-003 corpus. The Controller adopted it on 25 Aug 2026 and CANON-005 promoted it out of
experimental status.

## Where everything went

| Was here | Now lives at |
|---|---|
| `SCHEMA-audit-record-v0.2.md` | `canon/audit/AUDIT-GATE-v0.2.md` — the adopted normative procedure and schema |
| `records/*.audit.yaml` (16) | `canon/audit/records/*.audit.yaml` — the one active record per accepted source |

Both were moved with `git mv`, so `git log --follow` on either path reaches the original
experimental history.

There is deliberately **one** active copy of the 16 records. A second editable copy under an
experimental path would let the two drift, and downstream tooling would have no unambiguous source
of truth. The validator reads only `canon/audit/records/`, and a test asserts that no duplicate
copy reappears here.

## Where the experiment's reasoning is recorded

The design evidence was never stored in this directory — it lives in the findings, which are
unchanged and remain the record of why the gate has the shape it has:

- `canon/findings/CANON-004-audit-gate-design.md` — field-by-field rationale tied to CANON-003
  observations, burden assessment, rejected alternatives, and the two revisions the corpus forced
- `canon/findings/CANON-004-CONTROLLER-BRIEF.md` — the decision brief
- `canon/decisions/CANON-004-ADOPT-AUDIT-GATE-2026-08-25.md` — the Controller's adoption decision
  and the exact list of what it did and did not authorise
- `canon/tasks/CANON-004.md`, `canon/tasks/CANON-005.md` — the task definitions

## What the experiment was

Five questions, asked once per book after its source record is frozen, recorded in a form a machine
can read: what the available copy hid, whose evidence a claim is, what the product can use (with
`no_current_binding` a valid answer), whether two agreeing sources are genuinely two, and whether an
old technical claim is still true.

It was tested by writing a record for all 16 accepted books from committed repository evidence,
without re-opening a single source book, and by checking that the resulting rule rejects the
*Grammar of the Shot* / *Grammar of the Edit* companion pair while accepting genuine convergences.
