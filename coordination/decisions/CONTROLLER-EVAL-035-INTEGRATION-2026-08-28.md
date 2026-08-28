# Controller — EVAL-035 Integration — 2026-08-28

## Status
**ACCEPTED, GOVERNOR-CLEARED, MERGED.**

Evidence:
- Controller acceptance: `CONTROLLER-EVAL-035-FINAL-ACCEPTANCE-2026-08-28.md`
- Governor review: `governance/reviews/GOV-L1-EVAL-035-PILOT-VIDEO-SUBSTRATE.md`
- Governor verdict: **PASS WITH NON-BLOCKING NOTES**
- reviewed worker head: `a4fbf404bdc5ac54f1deebb6ebbfd8d832fa9253`
- merge: PR #61
- squash commit: `39cf38fb2055516aa715850e1e19be0a80e8b98c`

Governor independently reproduced:
- EVAL-035 substrate tests: 103/103;
- decisive RES-007 integration + spend tests: 23/23;
- successful merged Resources writer/validator path: PASS;
- ambiguous/failure merged Resources path: PASS;
- persistent cross-process spend continuity: PASS;
- current paid PILOT-001 authority: CLOSED;
- live provider calls/spend/generations: 0 / USD 0 / 0.

## Integrated T1 substrate
- provider surface: direct Gemini Developer API;
- credential: `GEMINI_API_KEY`;
- temporary T1 model: `veo-3.1-fast-generate-preview`;
- 720p; 9:16 for PILOT-001;
- one generation request = one attempt = one trial;
- polling/download are lifecycle steps, not new trials;
- no automatic retry;
- persistent PILOT-001 spend ledger with stable Resources-resolvable `cost_ref`;
- binary media persistence with SHA-256 / byte count;
- actual merged RES-007 writer + validator integration proven by test.

This does not qualify Veo, populate the Registry, or authorise paid PILOT-001 execution.

## Non-blocking note
One stale docstring still points to `pilot_authorisation.open_pilot_guard`; current live path is
`pilot_spend_ledger.open_pilot_runtime` + `pilot_authorisation.verify_authority`.
Documentation-only; fix opportunistically on a future Eval touch.

## Next gate
Pre-pilot substrate work is complete enough to stop infrastructure preparation.

Proceed to **PILOT-001 freeze**:
1. usable official Aight asset package;
2. freeze unresolved brief choices;
3. freeze the hybrid production recipe;
4. freeze the explicit human acceptance record/criteria;
5. reverify route/model/price at execution time;
6. obtain explicit user approval for a bounded PILOT-001 API-spend cap and record matching machine-verifiable authority.

No generation is authorised by this integration.
