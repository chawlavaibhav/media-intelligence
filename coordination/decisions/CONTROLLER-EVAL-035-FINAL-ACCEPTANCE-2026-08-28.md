# Controller — EVAL-035 Final Acceptance — 2026-08-28

## Status
**CONTROLLER ACCEPTED. LEVEL-1 GOVERNOR REVIEW PENDING.**

Reviewed branch:
- `work/eval-035-video-route`
- head `a4fbf404bdc5ac54f1deebb6ebbfd8d832fa9253`
- current main at review: `745f43c521d9ff1a611589e4ee8f826cf1213009`
- branch status at review: `behind_by: 0`

## Disposition

The third pass satisfies
`coordination/decisions/CONTROLLER-EVAL-035-RETURN-REVIEW-2-2026-08-28.md`.

The Controller specifically rechecked the two defects that caused the earlier correction loop:

1. **Actual Resources integration**
   - EVAL-035 now imports the merged `resources/pilot-writer/outcome_writer.py`.
   - The success path calls the real `add_ledger_entry`, `record_attempt`, and `record_artifact`.
   - The resulting archive is judged by the merged `validate_topology_v3.py`.
   - The ambiguous-failure path is also accepted by the real writer/validator.
   - The earlier copied required-field list is removed.
   - `storage_class` is no longer passed as an unknown attempt-writer kwarg.

2. **Persistent PILOT-001 spend / cost identity**
   - the live pilot path no longer relies on the process-local in-memory `BudgetGuard`;
   - reservations are persisted before dispatch;
   - pending reservations count against the cap;
   - settlement keeps the same stable `cost_ref`;
   - process restart reconstructs committed/pending spend;
   - pre-dispatch release is additive and scoped to the reservation;
   - ambiguous post-dispatch outcomes remain conservatively charged;
   - ledger corruption fails closed;
   - the same `cost_ref` resolves to the Resources immutable cost row.

The branch reports **103/103** EVAL-035 substrate tests passing with zero live network calls,
zero spend and zero real generations.

## Direct Gemini route

The T1 route remains:
- Gemini Developer API, direct Google surface;
- `GEMINI_API_KEY`;
- `veo-3.1-fast-generate-preview`;
- 720p;
- 9:16 for PILOT-001;
- one provider generation request = one attempt = one trial;
- polling/download are lifecycle steps, not extra trials.

This remains a temporary T1 executor, not a model qualification or Capability Registry admission.

Current official Google documentation was rechecked by the Controller on 2026-08-28 and continues to
list the model, portrait 9:16 support, 4/6/8-second generation at the relevant surface, native audio,
long-running-operation flow, and Veo 3.1 Fast 720p pricing of USD 0.10/generated second with audio.

## Non-blocking note

One stale documentation pointer remains in `generate_pilot_video`: its docstring says to see
`pilot_authorisation.open_pilot_guard`, but the current live entry point is the persistent runtime
path through `pilot_spend_ledger.open_pilot_runtime` / `pilot_authorisation.verify_authority`.

This is documentation-only and does not affect the executable path or tests. Route to the Governor
as a Low non-blocking note; do not reopen EVAL-035 implementation solely for this wording.

## Remaining unknowns

Still deliberately unverified until the first authorised PILOT-001 call:
- real Google dispatch;
- operation cadence/error vocabulary;
- blocked-video live response details;
- served content type;
- actual billed amount.

Execution-time route/model/price verification remains required.

## Merge gate

EVAL-035 is Controller-accepted and may proceed to a bounded Level-1 Repository Governor review.

No paid PILOT-001 execution is authorised by this acceptance.
