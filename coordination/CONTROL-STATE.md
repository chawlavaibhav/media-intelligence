# Controller State

**Updated:** 25 Aug 2026 by Repository Governor, task GOV-001, against `main` at
`00ea9b067229cd992b77b7d6e0958df35178b01b`.

**Read `PROJECT-MEMORY.md` first.** This file is the Controller's operational snapshot;
`PROJECT-MEMORY.md` is the canonical narrative and the authority map.

> **Correction notice.** Before GOV-001 this file described CANON-003 as an in-flight extraction
> batch with 13 of 18 books accepted, and EVAL-004 as unopened. Both were badly out of date — the
> repository had moved through CANON-004 to CANON-008 and EVAL-005 in the meantime. The stale text is
> preserved in Git history; the substantive history it described is preserved in
> `coordination/CANON-003-LANE-A-C-AUDIT.md`, `coordination/CANON-003-BOOKS-08-10-AUDIT.md`,
> `canon/decisions/` and `canon/findings/`. This correction was requested by the Canon stream in
> `canon/PROPOSED-INTEGRATION-CHANGE-CANON-005-COORDINATION.md`, which had not been actioned.

## Global posture — audit freeze

**All new domain work is frozen.** No Canon, Eval, Resources, acquisition, Capability Registry or
Production IR task may be opened or self-assigned. **No task is currently open in any stream.**

**The freeze remains in force until the Controller explicitly lifts or re-scopes it.** It does not
expire when a governance task completes or merges.

## Architecture state

- Source Knowledge: **SPEC-03 v0**. Operational Bindings: **SPEC-04 v0**. Knowledge Ontology:
  **SPEC-05 v0** — Governance rule 5 amended twice under Controller-approved Canon tasks (CANON-005
  independence-by-lineage; CANON-006 fifth dependence relation).
- SPEC-01 Creative IR v0.1 locked. SPEC-02 superseded conceptually by SPEC-03/04/05 and retained as
  evidence.
- Capability Battery V0: approved as **measurement design**, not empirical capability data.
- Identity rubric V0: frozen for later calibration. **Frozen does not mean calibrated or validated.**
- M1b Devanagari generation-item design V0: approved **design only**. Zero items exist.
- **Capability Registry does not exist.** Its cross-stream schema remains proposed/deferred.
- **Production IR does not exist.** Neither does the Production Planner or any routing system.

## Canon status — 19 live sources; no open task

**CANON-003 is closed.** It stopped at **16 Controller-accepted usable books** on 24 Aug 2026 — above
its minimum of 15, below its 18 target, by deliberate Controller decision
(`canon/decisions/CANON-003-STOP-AT-16-2026-08-24.md`). It was integrated and merged via PR #4.

**Two counts exist and must not be confused:**

| Number | Value | Meaning |
|---|---|---|
| Historical CANON-003 / CANON-004 method-test corpus | **16** | Frozen forever. |
| **Live accepted Canon** | **19** | Current, verified below. |

Mechanically verified by GOV-001 at the baseline SHA: `canon/knowledge/current/` holds 19 source
directories; `canon/audit/records/` holds 19 audit records; the sets match one-for-one.
`canon/validation/validate_audit_gate_v02.py` → 19 records, 0 errors.
`canon/validation/validate_canon003_integrated.py` → 16 books, 0 errors, unchanged.

**Audit Gate v0.2 is the authoritative admission method** (adopted CANON-004, applied CANON-005).
It governs downstream *use*, not storage: an unaudited or stale-audited source stays as evidence but
may not be used for cross-source promotion, product use or Canon-consumption.
`evidence_insufficient` is a legitimate completed outcome.

Since CANON-003 closed:

- **CANON-006** admitted both former deferred reserves — *Master Shots* and *The Conversations*.
  16 → 18. Added the pairwise, symmetric lineage relation `shared_primary_informant`.
  **The "deferred reserve" status of Books 11–12 is therefore obsolete.**
- **CANON-007** admitted *Effectiveness in Context*. 18 → 19. Added the representation-loss category
  `figure_semantic_binding_lost`.
- **CANON-008 STOPPED at its acquisition gate; nothing was ingested.** The official archive route for
  Girish Dalvi's Devanagari thesis publishes only a 3-page abstract. Live Canon stays 19. The task is
  `needs_controller_review`; four options are in `canon/findings/CANON-008-CONTROLLER-BRIEF.md`.

**The Canon still has no accepted Devanagari-structure source.** *Thinking with Type* remains blocked
on structural column interleaving.

## Eval status — battery human-validated; no checker ever run

**No checker is qualified. No model has been benchmarked. No Registry entry exists. ₹0 API and
generation spend.**

- **EVAL-001/002/003 closed and merged.** EVAL-003's 54-item Hindi-primary photographed-signage pack
  (173 eligible → 54 selected → 54 distinct hashes) is untouched and still available.
- **EVAL-004 STOPPED by Controller, 24 Aug 2026** after one 54-item Reader-A pilot. There is no
  Reader B and no two-reader reference. Reader A is exploratory evidence only; no checker may be
  qualified, ranked or entered in the Registry from it, and it must not be resumed.
- **EVAL-005 human validation is COMPLETE and frozen.** One Hindi-competent reviewer answered 98 of
  98; 5 of 53 base words were rejected, excluding 10 items. Controller decision: **PRUNE, DO NOT
  REBUILD** — excluded items are not replaced.

**Authoritative battery: the 96-item validated view** — 48 match / 48 mismatch, 48 accepted base
words, 33 hard opportunities on 33 distinct base words, 20 failure classes across 5 groups. The
original **106-item build is historical source material and is unchanged**.

GOV-001 verified the human-validation record mechanically: `human-validation-v1.json` is status
`FROZEN`, lists the 10 excluded item IDs and the expected validated state, and both raw response
artifacts match their recorded SHA-256 hashes.

**One reader is not independent-reader ground truth**, and the record says so. The 8.68% figure is an
iid *reference* calculation for sizing under an assumption the battery explicitly does not establish.
The actual qualification gate is deterministic: **zero false passes**.

**Next Eval gate:** Controller approval of a checker roster and API budget (order ₹600–2,100 on an
old price needing re-verification), plus the proposed thresholds. That is the only thing blocking the
project's first real measurement.

## Resources status — closed; no open task

RES-001/002 closed and merged. The EVAL-003 correction pass **is merged** (PR #5).

**Corpus: 34,786 items / 5.70 GB across 8 acquired sources; 4 blocked.** GOV-001 recomputed this
directly from `resources/manifests/corpus-pilot-v0.jsonl`: 34,786 records, all `validation_status:
ok`, 34,586 distinct hashes, 200 duplicates (27 within a source, 173 across two). Every per-source
count matches.

The corpus is **internal research and evaluation material only** unless separately cleared.

**IndicSTR12 and IIIT-ILST are one source lineage, not two independent sources** — 173 byte-identical
files, 98.3% of IIIT-ILST's scene photographs. **BSTD is the only genuine cross-lineage reserve and
stays untouched.**

Pending optional Controller action: `eval/PROPOSED-INTEGRATION-CHANGE-EVAL-003-RESOURCES.md` and
`resources/PROPOSED-INTEGRATION-CHANGE-RES-003-EVAL.md`.

## Current integration gates

1. **Governance:** the Governor control layer is established (`PROJECT-MEMORY.md`,
   `governance/GOVERNOR-CONTRACT.md`, `governance/audits/`). **The audit freeze remains in force
   until the Controller explicitly lifts or re-scopes it.**
2. **Canon:** decide CANON-008 — the Devanagari slot is empty and the task is stopped at the
   acquisition gate. No other Canon work is authorized.
3. **Eval:** approve a checker roster and API budget, and the proposed thresholds. Optionally decide
   whether to ask Resources to check held material for ~36–42 more Hindi words.
4. **Resources:** closed unless the Controller actions a pending proposal or opens a new task.
5. **Architecture:** Capability Registry, Production IR, routing and Canon-consumption experiments
   remain unapproved and not implemented.
