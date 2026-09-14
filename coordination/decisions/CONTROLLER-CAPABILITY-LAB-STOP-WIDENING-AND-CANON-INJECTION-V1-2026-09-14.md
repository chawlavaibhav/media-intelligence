# Controller — Stop widening the Capability Lab; authorise USD-0 implementation of Canon Injection v1 and template / empirical-memory integration — 2026-09-14

**Status:** APPROVED CONTROLLER DECISION.
**Role:** materialised by the governance closeout lane (Agent A) on branch `work/closeout-a-governance`, recording the human Controller's words without reinterpretation.
**Answers:** items **C-9** and **C-10** of `coordination/audits/AUDIT-2026-09-10-CONTROLLER-DECISIONS.md` (Auditor A's D5 in `AUDIT-2026-09-10-REPORT-A.md` §10).
**Related:** `canon/CANON-SHAPE-v1.md` §7 (the open-work list that names Injection v1 and the template library); `CONTROLLER-CANON-SHAPE-V1-DIRECTION-2026-09-01.md`; `CONTROLLER-CANON-GATE-001-MERGE-2026-09-07.md`; `CONTROLLER-CAPABILITY-LAB-DIRECTION-2026-09-05.md` (the direction this record narrows).

## Provenance

The rulings below were delivered by the Controller to the lead implementation agent in the assignment brief of 14 September 2026, which states: *"These are now APPROVED Controller decisions. Materialise them durably under coordination/decisions/ with provenance. Do not reinterpret them."* They answer the items of `coordination/audits/AUDIT-2026-09-10-CONTROLLER-DECISIONS.md`. Each ruling is quoted verbatim.

## What was being decided — in plain English

The Capability Lab (the empirical model-and-workflow battery) produced 575 deterministic Registry rows and a 61-cell routing map in two days. Both auditors independently reached the same view: continuing to widen it — more premium models, the other eight Canon packs, a better automatic judge, extra draws on every two-draw cell for neatness — now has declining value until the production runtime actually consumes it. On the Canon side, the governing shape document lists two builds after the gate: Injection v1 (packs injected as a cached stable prefix, no consumption receipts) and the template library / empirical memory (accepted blueprints kept as reusable assets). Both are pure code and cost nothing to build. The Controller has ruled on both questions.

## Authority — the Controller's words

**C-9 (stop widening the Lab):**

> "Stop widening the Capability Lab. No generic model battery. No premium-model sweep. No expansion merely to make tables prettier. New evidence work only when the production runtime exposes a launch-critical hole."

**C-10 (Canon):**

> "Authorise USD-0 implementation of: Canon Injection v1; template / empirical-memory integration. Do NOT compile the remaining eight packs unless a real runtime failure later demands one."

## Decision

### C-9 — the Capability Lab stops widening

1. **No generic model battery.** No further round whose purpose is to survey models in general.
2. **No premium-model sweep.** No round whose purpose is to test premium tiers (for example Seedance 2.5 or Wan premium) as a reference; the earlier deferral (`CONTROLLER-WAN2-CONTENDER-PREMIUM-DEFERRED-2026-09-09.md`, "tested only when a production brief calls for them") stands; C-9 adds its own trigger for any new evidence work (item 4 below). The two triggers are not harmonised here.
3. **No expansion merely to make tables prettier.** No extra draws on thin cells for symmetry, completeness or neatness.
4. **New evidence work only when the production runtime exposes a launch-critical hole.** The trigger for any further evidence work is a concrete failure or gap found by building or running the production path for the frozen Alpha 1 family (`CONTROLLER-ALPHA-1-PRODUCT-FAMILY-AND-RELEASE-POLICY-2026-09-14.md`), and even then each piece needs its own written spend record before dispatch.

### C-10 — Canon: two USD-0 builds authorised, eight packs not

5. **Canon Injection v1 is authorised for USD-0 implementation** — packs injected as a cached stable prefix with no forced-consumption receipts, as described in `canon/CANON-SHAPE-v1.md` §7 item 2.
6. **Template / empirical-memory integration is authorised for USD-0 implementation** — accepted blueprints kept and reused as template assets, `canon/CANON-SHAPE-v1.md` §7 item 3.
7. **The remaining eight compiled packs are NOT to be compiled** unless a real runtime failure later demands one. "Real runtime failure" means an observed failure in the production runtime, not an anticipated one; each such pack would need its own Controller decision at that time.

## Consequences / what changes

- **USD 0 means USD 0.** C-10 authorises implementation only: code, fixtures, tests, and integration with the existing gate and runtime contracts. It authorises **no tokens, no model calls and no provider calls** — not to build it, not to test it, and not to "prove" that it works. Any measurement of whether injection or templates improve outcomes (for example the acceptance-rate run the shape document names) is a separate, paid, unauthorised item.
- **Two `CONTROL-STATE.md` "Still blocked" lines change meaning.** The line "injection v1, the template library, or any further pack — the shape document's open-work list is a queue, not an authorisation" is now split: injection v1 and the template / empirical-memory integration **are** authorised at USD 0 by this record; "any further pack" stays blocked. The Governor refresh ordered by `CONTROLLER-GOVERNOR-REFRESH-ORDER-2026-09-14.md` carries this into the state document; until then this record governs over the stale line.
- **The Capability Lab direction of 5/8 September is narrowed, not reversed.** The battery's outputs (Registry, routing map, taint register) stand and are consumed; what stops is *widening* them. The direction decision's remaining unexecuted rounds (`CONTROL-STATE.md` "Next gate": floor round, Seedance on the bottle briefs, judge v2, round two of stills) are not authorised and, under C-9, may only be revisited when the production runtime exposes a launch-critical hole.
- **How this maps onto the audits' "what not to do next" list** (`HANDOFF-TO-CONTROLLER-2026-09-10.md` §8; REPORT-A §9): "do not re-run Stage A" and "do not widen every two-draw cell" are covered by C-9's words; "do not compile the other eight packs" by C-10; "do not chase a better automatic judge yet" is not in C-9's text — judge v2 is simply C-14, unauthorised; "do not build a general planner before the first vertical slice" is not addressed by either ruling and remains audit advice, not a ruling.
- **Group 3 of the decision sheet (C-12 … C-18, the paid items) remains NOT authorised.** No 14 September ruling authorises any of them, and their order has not been stated. Specifically, C-13 (Gemini API smoke), C-14 (judge v2), C-15 (clean re-runs of tainted cells), C-16 (round two of stills), C-17 (Stage B) and C-18 (Stage C) are each unauthorised; C-12 (cheapest-tier floor round) is likewise not authorised by any 14 September ruling; as new evidence work it is also subject to C-9's fourth sentence (only when the production runtime exposes a launch-critical hole). Whether the Controller intends C-12 to be nearer-term than the rest is **not stated** and is not decided here.
- **The reserved verdict is untouched.** Building injection and templates is Canon's *consumption*, not its *evaluation*. Whether Canon works remains reserved to the Controller (`CONTROLLER-EVAL-038-AUTHORISATION-AND-DISPOSITION-2026-09-01.md`); nothing built under C-10 bears on it.

## Context only — not a ruling

C-5 (the supposed judge call-count breach) was withdrawn by the audit itself; no breach occurred. It is mentioned because "do not chase a better automatic judge yet" (C-9's spirit, as both audits phrased it) rests on the judge's *quality* verdict, which the withdrawal does not affect.

## What this does NOT authorise

- **No tokens, no model calls, no provider calls** of any kind under C-10 — implementation is USD 0 in fact, not only in budget.
- No compilation of any of the remaining eight Canon packs.
- No acceptance-rate run, no injection A/B, no measurement of Canon's effect — those are paid and reserved.
- **C-12 through C-18 remain NOT authorised**; no order among them has been stated.
- No new Capability Lab round of any shape: no floor round, no premium sweep, no round two of stills, no judge v2, no widening of thin cells.
- No invocation of the gate's Cloud Vision text detector or any other paid post-draw scan.
- **Adopting the Alpha policy is NOT spend authorisation. No paid dispatch is authorised by any decision above.**
