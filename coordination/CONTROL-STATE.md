# Controller State

**Updated:** 25 Aug 2026 by Controller after GOV-001, against the post-audit decisions recorded in
`coordination/decisions/CONTROLLER-POST-AUDIT-UNBLOCK-2026-08-25.md`.

**Read `PROJECT-MEMORY.md` first.** This file is the Controller's operational snapshot;
`PROJECT-MEMORY.md` is the canonical narrative and authority map. Until the Governor performs the
next coherence refresh, the newer Controller decision and this file supersede any stale memory text
that still says the audit freeze is global or that no task is open.

> **Historical correction notice.** Before GOV-001 this file described CANON-003 as an in-flight
> extraction batch with 13 of 18 books accepted, and EVAL-004 as unopened. Both were badly out of
> date. GOV-001 corrected that state; Git history preserves the prior text.

## Global posture — audit freeze re-scoped

The GOV-001 audit freeze is **not fully lifted**. It is explicitly re-scoped by the Controller.

**OPEN:** `EVAL-006` only — checker qualification and a bounded first Capability Registry bootstrap,
under `eval/tasks/EVAL-006.md` and its stated budgets/stop conditions.

**HOLD:** new Canon expansion, Resources expansion/acquisition, Production IR, Production Planner or
routing implementation, Canon-consumption/RAG/training, and any Eval model/dimension outside EVAL-006.

Completion of EVAL-006 does not automatically authorize another task.

## Architecture state

- Source Knowledge: **SPEC-03 v0**. Operational Bindings: **SPEC-04 v0**. Knowledge Ontology:
  **SPEC-05 v0**.
- SPEC-01 Creative IR v0.1 locked. SPEC-02 superseded conceptually by SPEC-03/04/05 and retained as
  evidence.
- Capability Battery V0: approved as **measurement design**, not empirical capability data.
- Identity rubric V0: frozen for later calibration. **Frozen does not mean calibrated or validated.**
- M1b Devanagari generation-item design V0: approved **design only**.
- `eval/battery/CAPABILITY-REGISTRY-SCHEMA-V0-DRAFT.yaml` is now **approved as the basis for Eval
  measurement storage** under the post-audit Controller decision. Its cross-stream fields may store
  evidence but carry **no approved Planner/routing semantics yet**.
- **Capability Registry still has no empirical entries yet.** EVAL-006 is the task authorised to
  create the first evidence-backed entries.
- **Production IR does not exist.** Neither does the Production Planner or any routing system.

## Canon status — 19 live sources; CANON-008 closed; no open Canon task

**CANON-003 is closed.** It stopped at **16 Controller-accepted usable books** on 24 Aug 2026 and was
integrated and merged via PR #4.

Two counts remain intentionally distinct:

| Number | Value | Meaning |
|---|---|---|
| Historical CANON-003 / CANON-004 method-test corpus | **16** | Frozen forever. |
| **Live accepted Canon** | **19** | Current live Canon. |

Audit Gate v0.2 remains the authoritative admission method.

Since CANON-003 closed:

- **CANON-006** admitted *Master Shots* and *The Conversations*: 16 → 18.
- **CANON-007** admitted *Effectiveness in Context*: 18 → 19.
- **CANON-008** stopped correctly at its acquisition gate because the official Dalvi archive exposes
  only a 3-page abstract while the full thesis is behind IIT Bombay authentication.

**Controller disposition on CANON-008:** close the task as a legitimate blocked-source adjudication
and leave the Devanagari-structure gap open. No mirror, bypass, substitute identity or replacement
source is authorised by that decision. A future legitimate full thesis or replacement requires a new
Canon task.

**The Canon therefore remains at 19 live accepted sources and still has no accepted
Devanagari-structure source.** There is no open Canon task.

## Eval status — EVAL-006 is the only open domain task

No generator has yet been benchmarked and the Capability Registry has no empirical entry **as of the
opening of EVAL-006**.

Completed prior state:

- EVAL-001/002/003 closed and merged.
- EVAL-004 stopped by Controller; Reader A remains exploratory only.
- EVAL-005 human validation complete and frozen. Authoritative battery: **96 items — 48 match / 48
  mismatch, 48 accepted base words, 33 hard opportunities, 20 failure classes across 5 groups**.

**Checker qualification gates approved provisionally for EVAL-006:**

- zero false passes;
- false-fail rate <= 10%;
- refusal rate <= 5%;
- repeat consistency >= 0.95 across at least 3 full passes in both checker shapes.

The 10%, 5% and 0.95 values are provisional usability thresholds, not empirical truths. They may be
revised only by later Controller decision using completed-run evidence. The iid reference figure
remains a sizing calculation only.

**Approved first checker roster:** GPT-5.6 Luna, Gemini 3.7 Flash, Claude Sonnet 5,
Qwen3-VL-32B-Instruct. Exact API IDs, availability and pricing must be verified from official
provider documentation before spend. Checker budget cap: **₹4,000**.

**EVAL-006 then bootstraps the first Registry measurements**, only if at least one checker qualifies.
Its approved first generator/workflow roster and item rules are in `eval/tasks/EVAL-006.md`. Total
external API cap for the task is **₹16,000**, with a maximum of 260 generated images/clips including
retries.

EVAL-006 explicitly preserves the broader production-capability mission — product/person identity,
reference conditioning, human-object interaction, motion/physics, logo fidelity and
**speech/lip-sync including Hindi and two-speaker cases** remain visible future work rather than being
dropped because the first empirical Registry cells are narrower.

## Resources status — correction accepted; closed/on-demand

RES-001/002 are closed and merged. The EVAL-003 correction pass is merged.

**Corpus: 34,786 items / 5.70 GB across 8 acquired sources; 4 blocked.** Existing rights posture
remains internal research and evaluation only unless separately cleared.

The Controller accepts the correction and reply in
`resources/PROPOSED-INTEGRATION-CHANGE-RES-003-EVAL.md` as the disposition of
`eval/PROPOSED-INTEGRATION-CHANGE-EVAL-003-RESOURCES.md`:

- IndicSTR12 and IIIT-ILST are treated as **one source lineage** for holdout/independence purposes;
- crop-level transcription recoverability is recorded without promoting source labels to ground truth;
- BSTD remains the genuine cross-lineage reserve.

**Resources has no unresolved blocker and no open task.** It should source again only against a
concrete approved Eval requirement; no speculative accumulation is authorised.

## Current integration gates

1. **Eval:** execute EVAL-006. First gate is checker qualification. If no checker qualifies, stop.
   If one does, create the first evidence-backed Registry entries under the frozen task scope.
2. **Canon:** no open task. Devanagari-structure gap remains explicit; no replacement work is
   authorised now.
3. **Resources:** closed/on-demand; no acquisition until Eval produces a concrete approved need.
4. **Architecture:** Production IR and Planner/routing remain unapproved and unimplemented. Registry
   storage is approved; operational routing from Registry data is not.
5. **Governance:** `PROJECT-MEMORY.md` should be refreshed by the Repository Governor after these
   Controller changes so the canonical entry point reflects the new re-scoped freeze and EVAL-006.
