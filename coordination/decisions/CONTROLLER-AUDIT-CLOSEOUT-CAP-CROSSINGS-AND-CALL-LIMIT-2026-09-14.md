# Controller — Audit closeout: the two cap crossings, the one call-limit breach, and how caps are enforced from now on — 2026-09-14

**Status:** APPROVED CONTROLLER DECISION.
**Role:** materialised by the governance closeout lane (Agent A) on branch `work/closeout-a-governance`, recording the human Controller's words without reinterpretation.
**Answers:** items **C-1**, **C-5b** and **C-2** of `coordination/audits/AUDIT-2026-09-10-CONTROLLER-DECISIONS.md`.
**Related:** `coordination/audits/AUDIT-2026-09-10-REPORT-B.md` (F-1, F-3, F-4), `coordination/audits/AUDIT-2026-09-10-SPEND-RECONCILIATION.md`, `coordination/audits/README.md`.

## Provenance

The rulings below were delivered by the Controller to the lead implementation agent in the assignment brief of 14 September 2026, which states: *"These are now APPROVED Controller decisions. Materialise them durably under coordination/decisions/ with provenance. Do not reinterpret them."* They answer the items of `coordination/audits/AUDIT-2026-09-10-CONTROLLER-DECISIONS.md`. Each ruling is quoted verbatim below; nothing in this record adds to or narrows the quoted text.

## Authority — the Controller's words

**C-1 (the two cap crossings):**

> "Accept the two historical cap crossings as recorded. Preserve history. Mechanism fixed. Do not annul or rewrite evidence."

**C-5b (the one call limit that was exceeded):**

> "Accept the historical 19-vs-16 call-limit breach as recorded. Do not retroactively enlarge authority."

**C-2 (ledger versus vendor billing):**

> "Future dispatch caps are enforced against conservative ledger consumption at dispatch time. Vendor-billed cost is a separate reconciliation field used for actual CpAO. Do not wait for bills before enforcing a cap. The four historical provider statements still need reconciliation, but lack of statements must not block the USD-0 engineering tranche."

## What was being decided — the facts, in plain English

These figures are OBSERVED from the decision sheet (`AUDIT-2026-09-10-CONTROLLER-DECISIONS.md`, C-1 and C-5b) and the audit reports it summarises:

| Item | What the record authorised | What the ledger shows was consumed | Where |
|---|---|---|---|
| Video piece 1 (`authorization.video1`) | cap **USD 9.96** (₹950) | **USD 10.364** | `CONTROLLER-SPEND-AUTHORISATION-IMAGE-HALF-TWO-AND-VIDEO-PIECE-1-2026-09-09.md`; REPORT-B F-1 |
| Wan 2 contender round (`authorization.wan2`) | final cap **USD 11.53** (₹1,100 after a ₹300 addendum) | **USD 11.840** | `CONTROLLER-SPEND-AUTHORISATION-WAN2-CONTENDER-ROUND-2026-09-10.md` §4; REPORT-B F-1 |
| Stand-in picture run (call count, not money) | **≤ 16** paid calls | **19** paid calls (USD 1.605, inside the money cap) | `CONTROLLER-SPEND-AUTHORISATION-IMAGE-HALF-TWO-AND-VIDEO-PIECE-1-2026-09-09.md:23-28`; REPORT-B F-4 |

Why the crossings happened (OBSERVED, from the decision sheet and `coordination/audits/README.md`): the cap was enforced inside one run folder while each signed authorisation covered three or four runs, so no single run saw the combined total. The "≤ 16 calls" limit was prose only — no code enforced a call count anywhere.

Why C-2 matters: the ledger counts money the moment a request may have left the machine, so it is an **upper bound** on cost, not a bill. About USD 10.11 of recorded spend produced no artifact, and the Wan 2 record itself says at least USD 2.88 of that was "nothing generated, nothing charged". The vendors' actual invoices (fal, Google Cloud, Sarvam, ElevenLabs, 8–10 September) are not in the repository and have never been reconciled.

## Decision

1. **C-1 — both cap crossings stand as recorded.** Video piece 1 at USD 10.364 against USD 9.96 and Wan 2 at USD 11.840 against USD 11.53 are accepted as historical fact. They are neither annulled nor re-issued at the true amounts. The ledgers, spend records and audit reports that document them are not rewritten. (This is option A of C-1 on the decision sheet.)
2. **C-5b — the 19-vs-16 call-limit breach stands as recorded.** The authority is not enlarged after the fact to make the 19 calls compliant; the record continues to say "≤ 16" and the ledger continues to say 19.
3. **C-2 — from now on, a cap is enforced against the ledger, at dispatch time.** The conservative ledger figure (money counted when a request may have left the machine) is the number a cap is checked against, before each paid call. Nothing waits for a vendor bill.
4. **C-2 — vendor-billed cost is a separate field.** It exists for reconciliation and for computing *actual* cost per accepted outcome (CpAO). It is never the number a cap is enforced against.
5. **C-2 — the four provider statements still need reconciliation**, but their absence must not block the USD-0 engineering tranche (the work authorised elsewhere on this branch that spends no money).

## Consequences / what changes

- **History is preserved.** No ledger row, spend record, audit report or `CONTROL-STATE.md` spend paragraph is edited to hide or reverse either crossing or the call overrun. Future readers will see the crossings and, beside them, this ruling accepting them.
- **The mechanism repair is already on this branch — OBSERVED from `coordination/audits/README.md` ("What was repaired")**: `eval/harness-v2/ledger.py` now pools every run that records the same signed authorisation and checks the ceiling, tranche caps and currency sub-caps against the combined total, refusing a new run under a spent authorisation before its folder exists and failing closed on an unreadable sibling; and `max_paid_calls` is an optional authorisation field enforced at reservation time across the same pooled runs (absent means no limit, and the status output says so). The README records that replaying the real ledgers through this code prevents the video-piece-1 overrun outright.
- **Not yet complete, and not claimed here — INFERRED, in progress:** the README also records that the repaired ledger pools spend by the authorisation file's fingerprint, and that a cap raised by editing the file in place therefore starts a fresh pool, which is why the Wan 2 overrun is caught only for its first half. The Controller's ruling C-6a (one cumulative budget across amendments; stable budget identity) closes that gap. It is recorded separately in `CONTROLLER-AUTHORISATION-LINEAGE-CUMULATIVE-BUDGET-2026-09-14.md` and is being implemented on this branch by a separate lane. This record does not state that implementation is done.
- **Two cost numbers now exist by design.** Every future spend surface must show *ledger-consumed* (the cap number) and *vendor-billed* (the reconciliation number) as different fields, never merged into one figure. The four-column table produced by `python3 coordination/audits/tools/reconcile_spend.py` already carries a deliberately empty vendor-billed column; C-2 confirms that shape.
- **CpAO figures remain provisional until reconciled.** Any cost-per-accepted-outcome quoted from the ledger alone is an upper bound. Reconciling the 8–10 September statements from fal, Google Cloud, Sarvam and ElevenLabs remains open work; the Controller has ruled that this open work does not gate the USD-0 tranche. Who reads the statements, and when, is **not settled by this record** (the decision sheet asked; the ruling did not name a person).

## Context only — not a ruling

**C-5 was withdrawn by the audit itself.** Both auditors had reported the vision judge as making 206 calls against a 200-call authority; both were wrong — `calls: 206` was a row count from an offline rebuild, and at most 190 calls were sent. There was no judge breach and nothing to rule (`AUDIT-2026-09-10-CONTROLLER-DECISIONS.md`, C-5). It is noted here only so that a reader does not look for a missing ruling.

## What this does NOT authorise

- No annulment, re-issue or rewriting of any historical spend record, ledger or audit figure.
- No retroactive enlargement of the "≤ 16 calls" authority or of either money cap.
- No new paid dispatch of any kind. **Adopting the Alpha policy is NOT spend authorisation. No paid dispatch is authorised by any decision above.**
- No provider account access, no billing-portal login and no network call is authorised by this record; reconciling the four statements is open work that needs its own assignment.
- Nothing here changes any evidence number, Registry row, routing-map cell or elimination verdict — those are the subject of `CONTROLLER-AUDIT-CLOSEOUT-EVIDENCE-RULINGS-2026-09-14.md`.
