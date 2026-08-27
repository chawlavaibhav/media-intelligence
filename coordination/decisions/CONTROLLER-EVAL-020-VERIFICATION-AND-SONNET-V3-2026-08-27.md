# Controller EVAL-020 Verification Acceptance and Sonnet v3 Run — 2026-08-27

## Status

**EVAL-020 ACCEPTED AND INTEGRATED. FRESH SONNET 5 CONTRACT-V2 QUALIFICATION IS AUTHORISED UNDER THE EXISTING EMP-001 SPEND CEILING.**

Integration:
- PR #43
- merge commit `45dbcdebd4326e42cef0ee72f999cf6665e60ac1`

## Verification evidence accepted

Worker verification was performed at branch head `0e051e4764aeec4a84d79cf7ccfd68b25c264c0b`
before the final stale-test correction.

Observed:
- five focused test files: 138 passed, 1 stale assertion failed;
- targeted EVAL-020 semantic tests: 9 passed, 0 failed;
- preflight: PREFLIGHT_GREEN, 8/8;
- all provider keys explicitly unset during zero-spend checks;
- external calls: 0;
- spend: USD 0;
- prior live evidence byte-identical;
- deterministic Devanagari and Latin build products reproduced with frozen identities.

The single failed assertion expected the old pooled-v1 refusal count (576) at the top level. Under
contract v2 top-level metrics intentionally represent only the primary transcribe shape (288 calls).
All 576 dispatches still occurred. The assertion was corrected to the v2 semantics in commit
`94bda012442bc02bfdc4076643cdd8e8eca65c4e`; no production/instrument logic changed in that commit.

Controller disposition: **verification accepted**. A second paid rerun is not blocked by that stale test.

## Contract-v2 semantics now authoritative for NEW qualification evidence

- blind `transcribe` is the only qualifying shape;
- target-aware `verdict` remains mandatory diagnostic coverage and cannot fail qualification;
- numerical thresholds remain unchanged:
  - mismatch false pass max = 0;
  - match false-fail rate max = 0.10;
  - refusal rate max = 0.05;
  - repeat consistency min = 0.95;
- per-call outcomes are persisted;
- candidate outcomes, call records and contract hash are fingerprint-bound;
- A-TEXT rejects old/different-contract evidence;
- live qualification persists canonical `qualification-result.json`.

## Historical evidence disposition

Existing v1 evidence is preserved but is not final contract-v2 qualification evidence:
- Haiku 4.5: failed pooled provisional v1 gate;
- Sonnet 5 v2: failed pooled provisional v1 gate;
- Gemini: unresolved after 429 halt.

Do not reinterpret or rewrite these artifacts.

## Authorised Sonnet v3 run

Run only Anthropic `claude-sonnet-5` from Devanagari call 1 under qualification contract v2.

Frozen execution:
- `thinking: {"type":"disabled"}`;
- 96 Devanagari items;
- transcribe + verdict;
- 3 repeats;
- Latin only if the PRIMARY Devanagari transcribe gate passes;
- same frozen material, prompts and numerical thresholds;
- retries 0;
- preserve prior evidence;
- use the same persistent EMP-001 ledger;
- write a new human-readable result artifact and canonical `qualification-result.json`.

Spend before Sonnet v3:
- cumulative qualification spend: USD 0.3112678.

Conservative maximum reservation if Sonnet v3 reaches and completes both scripts:
- USD 5.345280.

Cumulative worst case:
- **USD 5.6565478**, below the existing USD 6 qualification sub-cap.

This falls within the user's existing bounded EMP-001 approval; no new spend approval is required.

## Stop conditions

- true ambiguous post-dispatch failure: count/persist, no retry, stop;
- contract-v2 primary Devanagari gate fails: stop before Latin;
- primary Devanagari gate passes: run Latin automatically;
- both script gates pass: stop before A-TEXT and return to Controller;
- no Gemini, Haiku or fal calls during this run.

A-TEXT remains blocked until a contract-v2 judge qualifies on both scripts.
