# Controller — Full state-of-record / Governor refresh ordered after the audit-closeout rulings — 2026-09-14

**Status:** APPROVED CONTROLLER DECISION.
**Role:** materialised by the governance closeout lane (Agent A) on branch `work/closeout-a-governance`, recording the human Controller's words without reinterpretation.
**Answers:** item **C-6** of `coordination/audits/AUDIT-2026-09-10-CONTROLLER-DECISIONS.md`.
**Related:** `coordination/audits/AUDIT-2026-09-10-REPORT-B.md` F-5; `coordination/audits/AUDIT-2026-09-10-REPORT-A.md` F-08; `governance/GOVERNOR-CONTRACT.md`.

## Provenance

The ruling below was delivered by the Controller to the lead implementation agent in the assignment brief of 14 September 2026, which states: *"These are now APPROVED Controller decisions. Materialise them durably under coordination/decisions/ with provenance. Do not reinterpret them."* It answers an item of `coordination/audits/AUDIT-2026-09-10-CONTROLLER-DECISIONS.md`. The ruling is quoted verbatim.

## Authority — the Controller's words

**C-6:**

> "Perform a full state-of-record / Governor refresh after the rulings and affected derivative maps are materialised."

## What was being decided — in plain English

`PROJECT-MEMORY.md` is the first file every new session is told to read, and `coordination/CONTROL-STATE.md` is the single current-state surface it points to. Both predate the two-day Capability Lab run of 8–10 September; the audit found `PROJECT-MEMORY.md` saying the Registry was empty when it held 575 rows (REPORT-B F-5), and `CONTROL-STATE.md` carrying stale intermediate numbers (REPORT-A F-08). Three marked factual corrections were applied on 10 September, but neither file has had a full refresh since 7 September. The decision sheet asked whether to order that refresh now or after the rulings C-1…C-5 were made. The Controller chose the sequence below.

## Decision

1. **A full state-of-record / Governor refresh is ordered.** Its scope is the two current-state documents: `PROJECT-MEMORY.md` and `coordination/CONTROL-STATE.md`.
2. **Sequence: after, not before.** The refresh runs after (a) the 14 September rulings are materialised as durable records under `coordination/decisions/` — this record and its five siblings dated 2026-09-14 — and (b) the affected derivative maps have been regenerated (the routing map and taint register under the evidence rulings; see `CONTROLLER-AUDIT-CLOSEOUT-EVIDENCE-RULINGS-2026-09-14.md`). Refreshing earlier would write state that the derivative regeneration then changes.
3. **Who performs it:** per the same 14 September assignment brief, the lead implementation agent on this branch, acting in the Governor role for the two documents in scope (`coordination/PROJECT-CONTRACT.md` "Authority": the Governor may write `PROJECT-MEMORY.md`, `history/**`, `governance/**` and status corrections in `coordination/**` when an approved governance task includes that scope — this order is that scope). The ruling's own words name the action and its timing, not the person.

## Consequences / what changes

- **Documents in scope:** `PROJECT-MEMORY.md` and `coordination/CONTROL-STATE.md`. Nothing else is refreshed under this order; stream-owned handoffs (for example `canon/HANDOFF.md`, `eval/HANDOFF.md`) remain routed to their streams as before.
- **Byte-for-byte snapshots first, per house convention.** Before either file is rewritten, its current text is preserved unchanged under `history/` following the existing naming pattern (`history/PROJECT-MEMORY-PRE-<EVENT>-<DATE>.md`, `history/CONTROL-STATE-PRE-<EVENT>-<DATE>.md`; the most recent are `…-PRE-GATE-001-REFRESH-2026-09-07.md` and `CONTROL-STATE-PRE-CAPABILITY-LAB-2026-09-08.md`). The refreshed files must name their snapshots in their headers, as the current ones do.
- **What the refresh must carry (follows mechanically from the rulings it comes after):** the six 14 September records as governing authority; the Registry at its validator-confirmed row count; the spend figures as corrected on 10 September plus the C-1/C-5b acceptance and the C-2 two-field rule; the C-4 quarantine policy and the C-6b withdrawal of RR-16 as clean routing truth; the C-6c two-mechanism split for exact text; the Alpha 1 product family, human-approval rule and T8 gate (`CONTROLLER-ALPHA-1-PRODUCT-FAMILY-AND-RELEASE-POLICY-2026-09-14.md`); the stop-widening and Canon Injection v1 rulings (`CONTROLLER-CAPABILITY-LAB-STOP-WIDENING-AND-CANON-INJECTION-V1-2026-09-14.md`); and the fact that Group 3 (C-12…C-18) remains unauthorised. The refresh reports state; it decides nothing.
- **Marked corrections stay visible.** The 10 September annotated corrections in both files are history; the refresh may fold their substance into the new text but the snapshots preserve the corrected wording.
- **This record does not perform the refresh** and does not claim it has happened. The proof is the refreshed files, their snapshots under `history/`, and the lead's commit.

## What this does NOT authorise

- No edit to `PROJECT-MEMORY.md` or `coordination/CONTROL-STATE.md` before the derivative maps are regenerated.
- No refresh of any document outside the two named.
- No new decision may be introduced by the refresh — a Governor refresh reports what the durable records say; where it finds a conflict it reports the defect rather than resolving it.
- No spend of any kind. **Adopting the Alpha policy is NOT spend authorisation. No paid dispatch is authorised by any decision above.**
