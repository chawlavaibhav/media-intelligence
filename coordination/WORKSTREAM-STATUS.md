# Workstream Status

**Snapshot, updated at integration checkpoints.**
**Updated:** 25 Aug 2026 by Repository Governor, task GOV-001, against `main` at
`00ea9b067229cd992b77b7d6e0958df35178b01b`.

**Read `PROJECT-MEMORY.md` first.**

> **Correction notice.** Before GOV-001 this file's live sections stopped at the CANON-003 close and
> the EVAL-004 stop, and still described Books 11–12 as deferred reserves outside the synthesis set.
> CANON-004 through CANON-008 and EVAL-005 have happened since, and CANON-006 admitted both reserves.
> The superseded text is preserved in Git history. The historical CANON-003 record below is retained
> because it remains true of CANON-003.

## Global posture

**Audit freeze — all new domain work is frozen** pending completion of the governance reset.
**No task is open in any stream.** Next work in every stream is Controller-assigned only.

| Stream | Status | Current approved work | Blocking item / next gate |
|---|---|---|---|
| Canon | **19 live accepted sources.** CANON-003 closed at 16; CANON-004/005 established the Audit Gate; CANON-006/007 took live Canon to 19; **CANON-008 stopped at its acquisition gate**. | none | Controller decision on CANON-008 — the Devanagari-structure slot is still empty. `canon/findings/CANON-008-CONTROLLER-BRIEF.md`. |
| Eval | **EVAL-005 human validation complete and frozen; authoritative battery is the 96-item validated view.** No checker qualified, no model benchmarked, no Registry entry, ₹0 spend. EVAL-004 remains stopped. | none | Approve a checker roster and API budget (order ₹600–2,100, price needs re-verification) and the proposed thresholds. This blocks the project's first empirical measurement. |
| Resources | **RES-001/002 closed and merged; EVAL-003 correction merged (PR #5).** | none | Optional Controller action on `eval/PROPOSED-INTEGRATION-CHANGE-EVAL-003-RESOURCES.md` and `resources/PROPOSED-INTEGRATION-CHANGE-RES-003-EVAL.md`; otherwise remain closed. |

## Canon

**Live accepted Canon: 19 sources.** Verified mechanically by GOV-001 — 19 directories under
`canon/knowledge/current/`, 19 records under `canon/audit/records/`, matching one-for-one;
`validate_audit_gate_v02.py` reports 19 records and 0 errors.

**Historical CANON-003 baseline: 16 — fixed forever.** `validate_canon003_integrated.py` still
reports 16 books / 505 source-knowledge objects / 54 concept systems / 417 terms / 53 concepts /
111 bindings, 0 errors. **That instrument is historical and its meaning must never change.**

**Admission method: Audit Gate v0.2**, authoritative since CANON-005
(`canon/audit/AUDIT-GATE-v0.2.md`). The live invariant needs no registry: **every source directory
holds exactly one active Audit Gate record.** A source whose audit cannot be completed records
`audit_status: evidence_insufficient`, which is a legitimate completed outcome.

### How CANON-003's historical 16 became today's live 19

- **CANON-006** admitted both former deferred reserves: Book 11 *Master Shots* (Kenworthy) and
  Book 12 *The Conversations* (Ondaatje). 16 → 18. **Books 11–12 are no longer deferred.** It added
  the lineage relation `shared_primary_informant`, applied **pairwise and symmetrically**, because
  *The Conversations* is substantially Walter Murch speaking and the corpus already held Murch's own
  *In the Blink of an Eye*. Incidental quotation of the same person does not qualify.
- **CANON-007** admitted *Effectiveness in Context* (Binet & Field). 18 → 19. Added the
  representation-loss category `figure_semantic_binding_lost` — for material where a chart's text and
  numbers survive extraction but which number belongs to which category does not.
- **CANON-008 stopped at its acquisition gate and ingested nothing.** Live Canon stays 19.

### Historical CANON-003 record — retained, still true of CANON-003

Controller-accepted usable books totalled **16**, exceeding the task's minimum of 15. On 24 Aug 2026
the Controller stopped extraction above the minimum but below the 18-book target rather than spend
further time on diminishing-return sources (`canon/decisions/CANON-003-STOP-AT-16-2026-08-24.md`).

Accepted lanes: Lane A Books 6–7; rebalance lane Book 8; Lane B Books 9–10; Lane C Books 13–15;
original Lane D Books 16–18; plus the five usable pre-parallel books.

Controller audits are recorded at `coordination/CANON-003-LANE-A-C-AUDIT.md` and
`coordination/CANON-003-BOOKS-08-10-AUDIT.md`. Worker validators were ephemeral and were therefore
not treated as independently rerun evidence; final integration mechanically revalidated every
accepted book.

Book 7 identity correction remains durable: the preselected Freeman artifact is *The Photographer's
Eye: A Graphic Guide* (2013), not the 2007 *The Photographer's Eye*.

*Thinking with Type* was blocked by structural column interleaving and is in neither the historical
16 nor the live 19.

## Eval

**No checker has been qualified and no capability has ever been measured.** ₹0 API, ₹0 generation,
0 Registry entries. BSTD and the Marathi reserve are untouched.

**EVAL-005 is the live artifact.** It asks whether a checker reports "matches" when the picture is
subtly wrong, and it removes the annotator by rendering its own images from strings we chose, so what
each image contains is known by construction.

| View | Contents | Status |
|---|---|---|
| Original build | 106 items — 53 match / 53 mismatch, 53 base words | **Historical source material.** What the reviewer saw. Unchanged. |
| **Validated view** | **96 items — 48/48, 48 accepted base words, 33 hard opportunities on 33 distinct base words, 20 classes / 5 groups** | **Authoritative for any checker run.** |

**Human validation complete and frozen.** One Hindi-competent reviewer, 98 of 98 answered, 0
unanswered, 0 unsure. 5 of 53 base words rejected → 10 items excluded and **not replaced**.
Controller decision: **PRUNE, DO NOT REBUILD** — preserving already-reviewed item identities rather
than opening a new human-validation surface.
Record: `eval/battery/devanagari-exactness/human-validation/HUMAN-VALIDATION-RECORD.md`.

**One reader is provenance, not ground truth.** The record states this itself; no threshold, rate or
checker claim may be derived from it. Two words flagged in both the word and rendering questions are
*within-reader* consistency, not a second reader.

**The qualification gate is deterministic — zero false passes — and needs no probability model.**
The 8.68% figure attached to the validated view is an `iid_reference_upper_bound_…` sizing
calculation under an independence assumption the battery explicitly does **not** establish. It is
never a checker's real-world error rate.

**EVAL-004 remains stopped** (`eval/decisions/EVAL-004-STOP-2026-08-24.md`). One 54-item Reader-A
pass exists; a second person looked informally but did not perform the frozen blind pass, so there is
no Reader B and no two-reader reference. Its design lesson stands: ordinary photographed signage is
too weak a proxy for the failure that costs money — a checker silently normalising subtly malformed
*generated* Hindi.

**EVAL-003 remains closed and merged.** Its 54-item Hindi-primary pack (173 eligible → 54 selected →
54 distinct hashes) is untouched and available if that screen is ever wanted. Its enduring finding:
two dataset releases from the same source lineage disagree on about one region in three (725 of
1,082 matched regions agree). That shows source labels are unsafe as ground truth. It is **not**
human inter-annotator agreement and yields **no** evaluator threshold.

## Cross-stream dependency chain

```text
CANON-003 CLOSED at 16 accepted books  ──►  integrated and merged (PR #4)
        │
        ├──► CANON-004 Audit Gate v0.2 designed and tested against the frozen 16
        ├──► CANON-005 gate made authoritative
        ├──► CANON-006 both reserves admitted          → live Canon 18
        ├──► CANON-007 Effectiveness in Context        → live Canon 19
        └──► CANON-008 STOPPED at acquisition gate     → live Canon stays 19
                 │
                 └──► next: Controller decision on the empty Devanagari slot

RES-001/002 corpus ──► EVAL-003 readiness MERGED
                         │
                         ├──► EVAL-004 single-reader pilot STOPPED
                         └──► EVAL-005 battery built, human-validated, frozen at 96 items
                                  │
                                  └──► next: Controller approves checker roster + API budget

Capability Registry / Production IR / routing remain blocked until empirical measurements exist
and the architecture is separately approved.
```

## Current Controller posture

- **Audit freeze holds.** Do not open or self-assign any domain task.
- Keep the historical **16** and the live **19** visibly distinct. Never rewrite one into the other.
- Treat the **96-item validated view** as the authoritative battery; keep the 106-item build as
  historical source material.
- Do not promote Reader A to ground truth, and do not resume EVAL-004.
- Treat one-reader validation as provenance, not independent ground truth.
- Treat source dataset labels as observations, not truth.
- Keep BSTD untouched until a deliberate cross-lineage validation task.
- CANON-008 is a legitimate stop, not a problem to work around with unauthorized access.
- Do not authorize checker/API/model runs, Registry, Production IR or routing work implicitly.
