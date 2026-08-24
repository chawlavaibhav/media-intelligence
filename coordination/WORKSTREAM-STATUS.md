# Workstream Status

**Snapshot, updated at integration checkpoints. Detail lives in each stream's task brief / handoff.**  
**Updated:** 24 Aug 2026

| Stream | Status | Current approved work | Blocking item / next gate |
|---|---|---|---|
| Canon | **CANON-003 active, parallel extraction with one execution rebalance.** Five usable books complete at the pre-parallel checkpoint. Lane D is Controller-audited complete with Books 16–18 accepted, bringing the currently confirmed count to 8. A has Book 6 worker-complete; B has Book 9 worker-complete; C has Books 13–14 worker-complete. | `CANON-003.md` + `CANON-003-PARALLEL-EXECUTION.md` + `CANON-003-REBALANCE-01.md` | New ownership: A→Book 7; B→Books 10+12; C→Book 15; fresh rebalance branch→Books 8+11. Audit returned books before final integration. Accepted Lane D stays untouched. No schema changes or Canon-consumption experiments during the batch. |
| Eval | **EVAL-003 substantive finalization passed Controller audit; documentation consistency cleanup active.** The Hindi-primary pack and protocol are mechanically in place, but operator-facing files still contain stale pre-finalization instructions, so the branch is not yet merge-ready and no calibration is approved. | `EVAL-003.md` + `EVAL-003-CORRECTION-PASS.md` + `EVAL-003-FINALIZATION-PASS.md` + `EVAL-003-DOC-CONSISTENCY-CLEANUP.md` | Preserve the 173-eligible / 54-Hindi pack, matcher, crop pipeline, two-reader protocol and Resources proposal unchanged. Remove stale 202-item/0-Hindi/browser-crop/pending-composition instructions, fix V0 reproduction commands, sweep current docs, then return. No human/API/model work yet. |
| Resources | **RES-001/002 closed and merged. No active task.** | none | Stay closed unless a Controller-approved cross-stream correction or new sourcing requirement warrants a new task. |

## Canon live-review note

Lane D is accepted and its original branch remains frozen. To reduce idle time without changing the preselected 18-book experiment, Controller approved `CANON-003-REBALANCE-01.md`. At the audit point Books 8 and 11 were explicitly not started, so they were reassigned to a fresh branch `work/canon-003-rebalance-d` created from the original common parallel base. No book was added or dropped and no method/schema rule changed.

The remaining load is now balanced as follows: Lane A finishes Book 7; Lane B finishes Books 10 and 12; Lane C finishes Book 15; the rebalance worker handles Books 8 and 11. Book 12 deliberately remains with B because Lane D had already predicted that an interview-shaped source such as *The Conversations* might expose its claim-attribution issue; moving that source to the same worker after the prediction would weaken freshness.

The rebalance worker must not continue from Lane D's accepted branch and must not read A/B/C fresh findings or use D's issue file as an extraction checklist. It follows the same frozen per-book process and stops after Books 8 and 11.

## Eval live-review note

The finalization return fixed the substantive gates. `work/eval` contains the Controller finalization task; the Hindi-primary selection summary reports **173 eligible Hindi-labelled photographs and 54 selected, all 54 with distinct hashes**; the one-to-one matcher has a committed adversarial self-test where two A regions contend for one B; the run plan and reader guide use **two independent Hindi-competent readers** and allow either reader to perform the later altered-target validity check only after the reference is frozen; the review/checker artifacts reference the same materialised crop hashes; and the Eval→Resources proposal now records the full-scene correction, **375 + 176 locally paired records**, and the denominator-specific **173/176** overlap result.

The branch is still not merge-ready because the Controller Brief's claim that stale contradictions were removed is not true across the active documents. `EVAL-003-calibration-readiness-findings.md` still presents the old **202-item overlap-excluded / 0-Hindi** pool as current, says browser-only crops/no transformed images, and calls crop materialisation unresolved. The README also contains followable old-state instructions, including reproduction without the approved Hindi-primary arguments and stale pool/source-composition prose; `annotator-disagreement.json` still says the shared files are excluded; the retained composition note still contains a later recommendation saying the decision is open. These are documentation/operational consistency defects, not a reason to reopen the method.

Controller therefore opened `eval/tasks/EVAL-003-DOC-CONSISTENCY-CLEANUP.md`. No new research, sample redesign, human review, API/model work, EVAL-004 or Registry work is authorized. After the cleanup returns cleanly, the next Controller decision is whether to merge EVAL-003 readiness and separately authorize the two-reader human pass.

## Cross-stream dependency chain

```text
CANON-003 parallel/rebalanced book extractions
        │
        └──► fresh CANON-003 integration/synthesis
                 │
                 └──► evidence for a later consolidated Canon-method decision

RES-002 closed corpus ──► EVAL-003 Hindi-primary readiness cleanup
                               │
                               └──► Controller merge review
                                      │
                                      ├──► later two-reader human calibration (not yet approved)
                                      └──► later API checker qualification (not yet approved)

Capability Registry / routing remain blocked until empirical measurements exist and the Registry architecture is separately approved.
```

## Current Controller posture

- Preserve the fixed 18-book source set; rebalance only explicitly not-started work under written Controller amendment.
- Keep accepted Lane D untouched until integration.
- Treat source annotations as provenance/evidence, not truth; reference construction remains two-reader and blind.
- Spend the first I1 calibration budget on the Hindi-facing capability actually needed, not a zero-Hindi proxy pack.
- Do not reopen EVAL-003 methodology for documentation cleanup; make current operator instructions match the already-approved Hindi-primary artifacts.
- Do not reopen Resources for ordinary cleanup; use the cross-stream proposal path.
- Do not allow worker-recommended next steps to become automatic tasks.
- Canon-consumption/planning experiments remain paused.
