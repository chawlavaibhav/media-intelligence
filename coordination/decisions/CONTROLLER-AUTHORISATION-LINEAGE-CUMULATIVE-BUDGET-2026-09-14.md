# Controller — An amendment never creates a fresh budget: immutable authorisation lineage and stable budget identity — 2026-09-14

**Status:** APPROVED CONTROLLER DECISION.
**Role:** materialised by the governance closeout lane (Agent A) on branch `work/closeout-a-governance`, recording the human Controller's words without reinterpretation.
**Answers:** item **C-6a** of `coordination/audits/AUDIT-2026-09-10-CONTROLLER-DECISIONS.md`.
**Related:** `coordination/audits/README.md` ("Discovered while repairing"); `CONTROLLER-AUDIT-CLOSEOUT-CAP-CROSSINGS-AND-CALL-LIMIT-2026-09-14.md` (C-1, C-2, C-5b).

## Provenance

The ruling below was delivered by the Controller to the lead implementation agent in the assignment brief of 14 September 2026, which states: *"These are now APPROVED Controller decisions. Materialise them durably under coordination/decisions/ with provenance. Do not reinterpret them."* It answers an item of `coordination/audits/AUDIT-2026-09-10-CONTROLLER-DECISIONS.md`. The ruling is quoted verbatim.

## Authority — the Controller's words

**C-6a:**

> "An amendment DOES NOT create a fresh economic budget. All amendments remain one cumulative budget. Implement immutable authorisation lineage / stable budget identity so changing a file fingerprint cannot reset consumed spend."

## What was being decided — in plain English

A spend authorisation is a signed file that says how much money a piece of work may consume. When the Controller raises a cap (for example the Wan 2 round's ₹300 addendum), that file has been **edited in place**, so its fingerprint — the hash the ledger uses to recognise "the same authorisation" — changes.

The audit's repaired ledger (OBSERVED, `coordination/audits/README.md`) pools spend across runs by that fingerprint. So an in-place amendment started a **fresh pool**: everything spent under the old fingerprint was forgotten by the new one. Replaying the real ledgers through the repaired code, video piece 1 was caught completely, but Wan 2 was caught only for its first half (8.480 against 8.39, refused) because the later runs sat under the amended file's new fingerprint (`AUDIT-2026-09-10-CONTROLLER-DECISIONS.md`, C-6a). The audit located the one-line change that would close the gap and deliberately did not make it, because "a raised cap re-uses the old spend" is a policy call for the Controller.

## Decision

1. **An amendment does not create a fresh economic budget.** Raising, lowering or otherwise amending an authorisation continues the same budget; consumed spend carries forward.
2. **All amendments of one authorisation remain one cumulative budget.** The cap that is enforced is the latest amended ceiling, checked against the total consumed under every version of that authorisation.
3. **Implement immutable authorisation lineage and a stable budget identity.** An authorisation must carry an identity that does not change when its file bytes change, and each amended version must record what it amends, so that a changed file fingerprint can never reset consumed spend. (This is option B of C-6a on the decision sheet.)

## Consequences / what changes

- **The Wan 2 gap closes prospectively.** Under this rule the second half of the Wan 2 round would have been checked against the spend of the first half, and the crossing recorded under C-1 could not recur in that form. The historical crossing itself stays as recorded (C-1 — "Preserve history").
- **Implementation is on this branch, by a separate lane (the spend lane) — INFERRED, in progress.** This record orders the mechanism; it does not claim it exists yet. The proof that it exists is the ledger code and its tests on this branch, not this file. Until that lane's commit lands, the repaired ledger still pools by file fingerprint and the gap described above is still open.
- **What "stable budget identity" must satisfy, mechanically (follows from the ruling's words, not added to them):** two authorisation versions that belong to one budget must resolve to the same identity; a version must be able to name the version it amends; and the pooled consumption check must sum across every version sharing that identity. How the identity is encoded (a separate id field, a lineage chain, or another form) is an engineering choice for the implementing lane, within those constraints.
- **Interaction with C-2.** The pooled figure this rule protects is the *conservative ledger consumption* that C-2 makes the enforcement number; vendor-billed cost stays a separate reconciliation field and is not what lineage pools.
- **Existing authorisation files are not rewritten.** The historical `*.local.yaml` files (gitignored) and the committed spend records keep their bytes; lineage applies to how the ledger reads them and to every future authorisation. If the implementing lane finds that a historical file must be re-described to fit the lineage model, that is done in a new derivative record, never by editing the original.

## What this does NOT authorise

- No new spend authorisation, no raised cap, no re-issue of any historical authorisation.
- No edit to any historical spend record, ledger row or `*.local.yaml` authorisation file.
- No paid call of any kind to "test" the mechanism — the ledger's tests run on synthetic entries at USD 0.
- No change to the money or call figures recorded under C-1 and C-5b.
- **Adopting the Alpha policy is NOT spend authorisation. No paid dispatch is authorised by any decision above.**
