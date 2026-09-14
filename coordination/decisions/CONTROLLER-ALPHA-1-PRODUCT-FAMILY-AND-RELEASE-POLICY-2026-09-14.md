# Controller — Alpha 1 product family frozen; human approval before every external delivery; the twelve-condition public-release gate — 2026-09-14

**Status:** APPROVED CONTROLLER DECISION.
**Role:** materialised by the governance closeout lane (Agent A) on branch `work/closeout-a-governance`, recording the human Controller's words without reinterpretation.
**Answers:** items **C-7**, **C-8** and **C-11** of `coordination/audits/AUDIT-2026-09-10-CONTROLLER-DECISIONS.md` (Auditor A's D2, D3 and D8 in `AUDIT-2026-09-10-REPORT-A.md` §10).
**Related:** `coordination/audits/AUDIT-2026-09-10-REPORT-A.md` §7 (T7 private alpha, T8 public beta gate); `coordination/audits/HANDOFF-TO-CONTROLLER-2026-09-10.md` §6; `CONTROLLER-AUDIT-CLOSEOUT-EVIDENCE-RULINGS-2026-09-14.md` (C-6c — the exact-text mechanism split this product family relies on).

## Provenance

The rulings below were delivered by the Controller to the lead implementation agent in the assignment brief of 14 September 2026, which states: *"These are now APPROVED Controller decisions. Materialise them durably under coordination/decisions/ with provenance. Do not reinterpret them."* They answer the items of `coordination/audits/AUDIT-2026-09-10-CONTROLLER-DECISIONS.md`. Each ruling is quoted verbatim. The twelve T8 conditions are copied verbatim from `AUDIT-2026-09-10-REPORT-A.md` §7 "T8 — Public beta gate".

## What was being decided — in plain English

Both audits said the same thing: without a frozen first job family, "more testing" has no stopping rule, and every evidence question becomes "does this matter for launch?" with no answer. The Controller has now named that family (C-7), fixed the release rule for it (C-8 — a human approves every output before it goes out, because the automatic judge agreed with the Controller only about two-thirds of the time and wrongly accepted 22 % of what the Controller rejected), and adopted the bar that must be met before anything is delivered to the public automatically (C-11).

## Authority — the Controller's words

**C-7 (ALPHA 1 PRODUCT FAMILY):**

> "Freeze Alpha 1 to: one STATIC COMMERCIAL AD WITH EXACT OVERLAY COPY, optionally followed by: one SHORT MOTION VERSION DERIVED ONLY FROM THE ACCEPTED STILL. Supplied-photo work is conditional behind the identifiable-person / consent gate. Exclude from Alpha 1: talking heads; lip-sync; native speech; multi-shot stories; generated in-scene exact text."

**C-8 (human release policy):**

> "Every Alpha-1 output requires human approval before external delivery. No autonomous external delivery."

**C-11 (the public-release bar):**

> "Adopt Auditor A's twelve-condition T8 public-release gate."

## Decision

### C-7 — the Alpha 1 product family is frozen to:

1. **One static commercial ad with exact overlay copy.** A single still image for commercial use, carrying exact text (prices, legal lines, brand names, offer copy) as an **overlay** — text composed onto the picture, not drawn by the image model into the scene. Read together with C-6c and with the exclusion in item 4 below, this is exact-text **mechanism B** (textless plate + deterministic code composition) — INFERRED from the pairing "exact overlay copy" (included) versus "generated in-scene exact text" (excluded); the ruling does not use the letters A/B itself.
2. **Optionally followed by one short motion version derived only from the accepted still.** A short video whose only source is the still the human has already accepted. It is not a fresh generation from a text prompt, and it does not introduce new content, new text or new shots.
3. **Supplied-photo work is conditional** — it sits behind the identifiable-person / consent gate. Work on a customer-supplied photograph is inside the family only when that gate is passed; the gate itself (what counts as identifiable, what consent evidence is required) is not defined by this record.
4. **Excluded from Alpha 1:** talking heads; lip-sync; native speech; multi-shot stories; generated in-scene exact text (which is C-6c's exact-text **mechanism A** — the model drawing the copy; same INFERRED mapping as item 1).

### C-8 — release policy for Alpha 1:

5. **Every Alpha-1 output requires human approval before external delivery.** No output leaves the project to a customer or the public without a human having approved that specific output.
6. **No autonomous external delivery.** No automatic path may deliver externally, whatever any judge, gate or score says.

### C-11 — the public-release gate:

7. **Auditor A's twelve-condition T8 gate is adopted as the formal bar for public delivery.** Copied verbatim from `AUDIT-2026-09-10-REPORT-A.md` §7, "T8 — Public beta gate", "Required conditions":

> 1. audit closed;
> 2. HEAD reproducible;
> 3. route evidence clean;
> 4. Stage-B envelopes exist for public routes;
> 5. Stage-C accepted-outcome evidence exists;
> 6. CpAO measured;
> 7. fallback/repair bounded;
> 8. spend ceilings and kill switch live;
> 9. customer privacy/retention policy live;
> 10. provider commercial/terms review complete;
> 11. observability/incident handling live;
> 12. human override remains available.

The same section describes the gate's purpose in its closing line — *"Only after this gate should automatic customer delivery be enabled"* — and its end condition as the Controller signing a public-release decision. Read with C-8 (no autonomous external delivery), it follows that automatic customer delivery stays off until the twelve conditions are met and the Controller signs; that consequence is stated here as following from the two rulings together, not as extra text adopted.

## Consequences / what changes

- **A stopping rule now exists.** Evidence work is launch-critical only if it bears on the two Alpha 1 deliverables (static ad with overlay copy; optional motion version from the accepted still) or the conditional supplied-photo path. Anything about talking heads, lip-sync, native speech, multi-shot stories or model-drawn in-scene text is outside Alpha 1 and is not a launch blocker.
- **The exact-text wedge is mechanism B by definition.** The C-6c re-keying (`CONTROLLER-AUDIT-CLOSEOUT-EVIDENCE-RULINGS-2026-09-14.md`) is what lets a router select "textless plate + code-set overlay" as a distinct route without colliding with the eliminated "model draws the text" cell.
- **A human approval step is a hard requirement of the Alpha 1 runtime.** Any runtime, policy profile or delivery path built for Alpha 1 must stop before external delivery and wait for a human decision on that output. **Relation to an older statement — INFERRED, not ruled:** `PROJECT-MEMORY.md` §7 trap 8 and `CONTROL-STATE.md` "Still blocked" say no mandatory human-in-the-loop step exists in the production API architecture (the withdrawn exact-text review of 28 Aug 2026). C-8's words do not mention that statement. The reading recorded here is that C-8 is an *external-delivery* approval for the Alpha 1 product, while the older line was about a text-checking step inside the pipeline; whether the Governor refresh should amend the older line to say "except the Alpha 1 external-delivery approval (C-8)" is for the refresh to surface and the Controller to confirm. This record does not resolve it.
- **The automatic judge stays out of the release decision.** Its "not qualified" verdict (kappa 0.33, false-accept 22 %) stands; C-8 makes the human the release authority regardless of any future judge version. Whether a judge v2 is ever attempted is C-14, a paid item, and remains unauthorised.
- **T8 conditions are a checklist, not a status.** As of this record none of the twelve is asserted to be met; the record adopts the bar and says nothing about how far along any condition is. Several conditions (Stage-B envelopes, Stage-C accepted-outcome evidence, CpAO measured) depend on paid work that is not authorised.
- **What the identifiable-person / consent gate is, mechanically, is open.** The Controller placed supplied-photo work behind it; defining it (criteria, evidence, who decides) is work for the alpha lane and, where it touches policy, for the Controller. This record does not define it.

## Context only — not a ruling

C-5 (the supposed judge call-count breach) was withdrawn by the audit itself; no breach occurred. The judge's *quality* verdict — not qualified — is unaffected by that withdrawal and is the reason C-8 was recommended by both auditors.

## What this does NOT authorise

- **Adopting the Alpha policy is NOT spend authorisation. No paid dispatch is authorised by any decision above.**
- No customer intake, no external delivery, no terms of service, no output-rights position, no provider resale review and no refund policy — the handoff (§6) lists these as missing and this record does not supply them.
- No private alpha start, no public beta, no automatic customer delivery. T8 is the bar; passing it is a separate Controller signature.
- No definition of the identifiable-person / consent gate; no supplied-photo work until that gate exists and is passed.
- No re-admission of any excluded capability (talking heads, lip-sync, native speech, multi-shot stories, generated in-scene exact text) into Alpha 1 without a newer Controller decision.
- No Registry row, no change to any evidence number, and no verdict on whether Canon works.
