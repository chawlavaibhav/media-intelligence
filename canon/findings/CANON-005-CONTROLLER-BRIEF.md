# CANON-005 — Controller brief

**Task:** CANON-005, apply the adopted Audit Gate v0.2
**Date:** 25 Aug 2026 · **Branch:** `work/canon-005` · **Task-base:** `main` at `57395a1`
**Status:** implementation complete · **needs_controller_review**
**Severity:** `LOCAL`

---

## Bottom line

Done, with the change surface the decision authorised and nothing else.

**One authoritative spec changed: SPEC-05.** SPEC-01, SPEC-02, SPEC-03 and SPEC-04 are byte-identical
to the task base. The 16-book source content is byte-identical too — `git diff` against
`canon/knowledge/current/` returns empty, so no source claim, system, binding or ontology entry was
touched by the promotion.

The Audit Gate now has one authoritative home, one active record per accepted source, and no second
editable copy anywhere.

---

## 1. Files promoted and moved

Moved with `git mv`, so `git log --follow` reaches the experimental history from either new path.

| From | To | Git |
|---|---|---|
| `canon/experiments/audit-gate-v0.2/SCHEMA-audit-record-v0.2.md` | `canon/audit/AUDIT-GATE-v0.2.md` | `R090` — moved, then edited to carry the authoritative header and the gate order |
| `canon/experiments/audit-gate-v0.2/records/*.audit.yaml` (16) | `canon/audit/records/*.audit.yaml` (16) | **`R100` on all sixteen — byte-identical** |

`canon/experiments/audit-gate-v0.2/` now contains **only** a README, rewritten as a historical
pointer: it states plainly that nothing there is active, maps each old path to its new one, and
points at `canon/findings/CANON-004-audit-gate-design.md` for the design reasoning, which never lived
in that directory and is unchanged.

**No `SPEC-06` was created**, per the decision. This is a Canon method layer plus one SPEC-05 rule.

---

## 2. Exact SPEC-05 text changed

One insertion into Governance rule 5. Nothing was deleted; the existing rule text is intact and the
amendment follows it. No relation type was added and no concept semantics changed.

> **Independence is established from the active Audit Gate lineage records, never from a count of
> distinct `origin_ref` values.** Two source identifiers can share an author, a publisher, a series
> and a decade — *Grammar of the Shot* and *Grammar of the Edit* are Thompson & Bowen, Focal Press,
> same series, a year apart, each citing the other — so counting ids would report one authorial
> position stated twice as two sources agreeing.
>
> Two origins may be counted as independent only when:
>
> - neither source's audit record declares the other with a **dependence relation**:
>   `shared_author`, `same_series`, `companion_volume` or `derivative_of`; and
> - neither carries `independence_not_established`, which blocks promotion until resolved rather
>   than silently passing.
>
> A shared publisher (`shares_publisher_only`) or a citation (`cites_source`) **does not** by itself
> defeat independence. A source citing an unrelated source is ordinary scholarly behaviour, and
> treating a shared imprint as shared origin would refuse legitimate convergence.
>
> **Independence is pairwise, not a permanent global property of a source.** A source may be
> non-independent of one corpus source and a perfectly good independent origin against every other.
> A record therefore carries `not_independent_of_named_sources`, which points at the pairwise
> entries; it does not block that source everywhere.
>
> The mechanical form of this rule is `independent_origins_ok()` in
> `canon/validation/validate_audit_gate_v02.py`, which fails closed on an unrecognised verdict. The
> audit record schema is `canon/audit/AUDIT-GATE-v0.2.md`. Adopted by
> `canon/decisions/CANON-004-ADOPT-AUDIT-GATE-2026-08-25.md`; applied by CANON-005.

---

## 3. The gate is now documented authoritatively

`canon/audit/AUDIT-GATE-v0.2.md` carries the required order as normative text:

```
1. source extraction stabilises                       SPEC-03
2. source systems / ontology stabilise                SPEC-05
3. OperationalBindings stabilise                      SPEC-04
4. fresh checkpoint is committed
5. Audit Gate record is written against those exact bytes
6. Audit Gate validator passes
   ─────────────────── THE GATE ───────────────────
7. only now: cross-source promotion · downstream product/application use ·
             Canon-consumption / retrieval
```

Two things are stated explicitly so they cannot be misread later:

- **An unaudited or stale source stays in the repository as source evidence.** It is not deleted,
  hidden or devalued — it simply may not pass the three gates in step 7. The gate governs use, not
  worth.
- **Bindings are still not mandatory.** Step 3 stabilises whatever bindings exist, and zero remains
  a normal count. The retired rule is not reintroduced.

---

## 4. Adopted vocabulary and protections preserved

All seven application-fit consumers survive, including `deterministic_composition` and
`human_workflow`. A test asserts the list is exactly seven, contains both, and that every one of the
16 records still covers all seven. **Neither became a SPEC-04 target type or executor** — SPEC-04 is
byte-identical.

`source_snapshot` behaviour is unchanged and required no path-only update: the fingerprint covers
files under `canon/knowledge/current/<book>/`, which did not move. All 16 snapshots validate against
current source bytes after the promotion. `recorded_at_commit` remains informational; there is still
no snapshot-refresh shortcut.

Everything the validator protected before, it still protects: reference resolution, controlled
vocabularies, the anti-score rule, evidence-origin consistency against the frozen
`empirical_within_source`, complete application-fit coverage, pairwise lineage, fail-closed
independence verdicts, stale-audit snapshot checks, and the 16-source coverage check.

**Tests were added, not weakened** — 46 → 52, plus 37 subtests. The six new ones guard the promotion
itself: the authoritative path is where the validator looks; no duplicate records remain under the
retired path; a duplicate that reappears is reported as an error; the adopted method document exists
and declares itself authoritative; every record still carries a snapshot over the adopted artifact
set; all seven consumers survive in the vocabulary and in every record.

The validator also gained a repository-level check: if any `*.audit.yaml` reappears under
`canon/experiments/audit-gate-v0.2/records/`, the run fails with `duplicate active records`.

---

## 5. Verification — fresh from the final branch head

Re-run from the final branch head with a clean working tree. Two SHAs are involved and the
distinction is stated rather than glossed: `6cb1999` carries every substantive change, and the head
commit edits **only this brief** — no code, spec, record or test differs between them.

Final head: `07e5850`.

| # | Command | Exit | Result |
|---|---|---|---|
| 1 | `python canon/validation/validate_canon003_integrated.py --root .` | **0** | `error_count = 0` · 16 books, 505 SourceKnowledge objects, 54 systems, 417 terms, 53 concepts, 111 bindings |
| 2 | `python canon/validation/validate_audit_gate_v02.py --root .` | **0** | `error_count = 0` · `record_count = 16` · `records_path = canon/audit/records` |
| 3 | `python -m pytest tests/ -q` | **0** | **52 passed, 37 subtests passed** |

Corpus counts are identical to the task-base baseline, which is the expected result for a promotion
that moved files and changed no content.

### Mechanical confirmations

| Check | Result |
|---|---|
| exactly 16 active audit records | ✅ `canon/audit/records/` contains 16 |
| no active duplicate under an experimental path | ✅ `canon/experiments/audit-gate-v0.2/` contains only `README.md` |
| all 16 snapshots validate against current source bytes | ✅ validator `error_count = 0` |
| only authoritative spec changed is SPEC-05 | ✅ `git diff --name-only` over SPEC-01…SPEC-05 returns SPEC-05 alone |
| SPEC-01, SPEC-03, SPEC-04 byte-identical to task base | ✅ `git diff --stat` empty (SPEC-02 also unchanged) |
| no source-knowledge / system / binding meaning changed | ✅ `git diff --stat 57395a1 -- canon/knowledge/current/` empty |
| record files unchanged apart from the move | ✅ all 16 renames are `R100` |
| no GitHub Actions workflow added | ✅ no `.github` directory exists |
| no new source ingested | ✅ no *Master Shots*, *The Conversations* or any other new material |

Run with a local `.venv` carrying PyYAML and pytest; neither is installed system-wide on this
machine.

---

## 6. Migration and path consequences

- **Anything referencing the old paths must be repointed.** Inside the repository that was the
  validator's two header comments, its `RECORDS_SUBPATH`, and the experiment README — all updated.
  A repo-wide grep finds no remaining stale reference except in `canon/tasks/CANON-004.md` and
  `canon/tasks/CANON-005.md`, which correctly cite the paths as they stood when those tasks were
  written and should not be rewritten.
- **Snapshots did not need regenerating**, because the fingerprint covers the source artifacts, not
  the audit's own location.
- **A future source must be audited before downstream use.** That is a new obligation created by the
  gate, and it applies to the two deferred reserve books whenever they are integrated.

---

## 7. Not done, deliberately

No new source ingested. No cross-source concept created. No RAG, retrieval, Canon-consumption or
Production IR work. No new Audit Gate version designed. No CI workflow. No model or API spend.

`coordination/CONTROL-STATE.md` and `coordination/WORKSTREAM-STATUS.md` are **stale** — both still
describe CANON-003 as an active batch with lanes in flight. Those files are Controller-owned and the
runbook forbids a stream editing them, so the discrepancies and the replacement facts are filed as a
proposal at `canon/PROPOSED-INTEGRATION-CHANGE-CANON-005-COORDINATION.md` rather than edited.
`canon/HANDOFF.md` has been updated and is current for the Canon stream in the meantime.

---

## 8. Recommended next step

Controller review and merge. After that, the natural next tasks — none of which CANON-005 has
started or self-assigned — are integrating the two deferred reserve books under the adopted method
(each needing its own fresh Audit Gate record), refreshing the coordination files from the proposal
above, and reopening Canon-consumption work so it consumes the audited record.
