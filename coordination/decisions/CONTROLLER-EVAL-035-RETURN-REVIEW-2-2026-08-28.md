# Controller — EVAL-035 Return Review 2 — Cost / RES Integration Correction — 2026-08-28

## Status
**CORRECTION REQUIRED. DIRECT GEMINI/VEO ROUTE REMAINS ACCEPTED.**

Reviewed branch `work/eval-035-video-route` at
`d7525bbf716f78cd1c30133effc53d14cde76f4e`.

The direct Gemini Developer API route itself remains the intended T1 substrate:
- credential: `GEMINI_API_KEY`;
- model: `veo-3.1-fast-generate-preview`;
- 720p, 9:16 for the Aight pilot;
- one generation request = one attempt = one trial;
- long-running-operation polling is lifecycle, not extra trials;
- no real call or spend in EVAL-035.

## What is now correct
The fal execution path is gone. The implementation has:
- direct Gemini request / poll / binary-download handling;
- request/config hashes and recoverable config;
- binary SHA-256 and byte count;
- conservative ambiguous-dispatch handling;
- current committed state fail-closed for spend authority;
- a production-attempt shape that satisfies the value-level final RES-007 G12 rules
  (hashes, UTC timestamps, lane, repeat index, no eval_item_id).

## Remaining integration defects

### 1. `storage_class` is incorrectly passed as a writer argument
The final RES-007 `OutcomeWriter.record_attempt()` does **not** accept `storage_class` from the
caller. Resources sets the frozen storage class internally and rejects unknown extra fields.

Current `res007_production_attempt()` includes `storage_class` in `writer_fields`.
A direct `record_attempt(..., **writer_fields)` therefore fails.

Correction:
- remove `storage_class` from the attempt writer kwargs;
- retain it only where artifact/provider evidence legitimately needs it;
- add an integration test that actually imports/calls the final RES-007 writer interface rather
  than comparing a hand-maintained field list.

### 2. Live spend guard cannot produce a valid `cost_ref`
`open_pilot_guard()` currently returns EMP-001's in-memory `BudgetGuard`.
That guard's `record()` returns no cost reference.

Therefore a real Gemini attempt settles with `cost_ref: null`, while RES-007 requires an attempt
cost_ref resolving to an immutable cost-ledger entry.

This also reintroduces an older failure mode already learned in EMP-001: an in-memory ceiling resets
across processes and is not a durable tranche-level spend history.

Correction:
- PILOT-001 must use an append-only, persistent runtime spend ledger keyed to the pilot tranche/run;
- reservation must be persisted before dispatch and count against the authorised ceiling;
- spend/release must settle that reservation additively;
- the settled provider call must return a stable `cost_ref`;
- process restart must reconstruct consumed + pending spend rather than start from zero;
- corruption must fail closed;
- keep the existing machine-verifiable Controller-authority + matching local-authorisation gate.

Reuse the accepted EMP-001 durable-ledger semantics as the design precedent, but do not mutate
EMP-001's frozen tranche/stage constants or history.

### 3. RES-007 cost-ledger handoff must be complete
The EVAL result must provide enough data for the pilot integration layer to call
`OutcomeWriter.add_ledger_entry()` with the same cost identity before recording the attempt.

At minimum expose a writer-ready cost record containing:
- `ledger_entry_id` matching the attempt `cost_ref`;
- amount;
- currency = USD;
- cost_class = `api_tool`;
- recorded_at;
- basis (e.g. provisional published rate / conservative provisional where applicable);
- immutable = true.

Do not mislabel a published-rate estimate as invoice evidence. The contract permits modelled cost
when its basis is explicit.

### 4. Branch freshness
The branch's Controller Brief says it rebased onto current main, but the returned branch is still
behind current main. After the correction, update it onto the then-current `main` and run the
actual RES-007 interface integration test.

## Required controls
Add tests proving:
1. `record_attempt(..., **handoff_writer_fields)` succeeds against the final RES-007 writer
   after the caller adds the returned cost-ledger row and step;
2. no unknown `storage_class` kwarg is passed;
3. the real pilot guard path yields a non-null stable `cost_ref`;
4. a second process/run opening the same pilot run sees prior committed and pending spend;
5. a pending reservation blocks spend beyond the cap;
6. pre-dispatch release restores only that reservation;
7. ambiguous post-dispatch settlement does not manufacture headroom;
8. corrupted/missing spend history fails closed;
9. local authorisation alone still cannot create spend authority;
10. no network is used in tests.

## Scope
USD 0. No real Gemini call. No Registry write. No second provider. No Planner/Production IR.
Do not change Resources contracts or CpAO semantics.

After this correction EVAL-035 returns for Controller review, then Level-1 Governor review.
