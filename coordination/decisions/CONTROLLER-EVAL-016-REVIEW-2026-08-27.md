# Controller EVAL-016 Review — 2026-08-27

## Verdict

**ACCEPTED AND INTEGRATED — ZERO-SPEND PRE-EXECUTION VERIFICATION GREEN.**

EVAL-016 corrects the transition from an unperformed Latin human review to a completed real review.

Integration:
- PR #39
- merged to `main`
- merge commit `ff0e4bb379acd69a23909a57a2da50bf5ceaace3`

## Why the correction was required

After the real human review was completed and committed, the preparation renderer still:
1. rewrote `perceptibility-review.csv` back to an empty template during a rebuild; and
2. the A-TEXT validator required a visible-difference answer on match rows, even though the frozen review contract requires that field only for mismatch rows.

Those behaviours conflicted with the frozen Task-2 review rule and could erase valid human evidence.

## Accepted corrected semantics

- the human review is durable evidence and a routine render rebuild must preserve it;
- all 96 Latin items require `usable_surface=yes`;
- only the 48 controlled mismatch rows require `visible_difference=yes`;
- the completed review is bound to the frozen Latin pack SHA-256;
- if the pack changes, the old review becomes stale and the gate closes;
- Latin qualification fails closed before any Latin evaluator call when the human review is missing, incomplete, rejected or stale;
- A-TEXT uses the same canonical human-review validator;
- the cross-process rehearsal retains a negative control proving an unresolved review still blocks.

## Fresh macOS verification evidence

Execution worker reported a clean detached worktree at EVAL-016 head `c84c069`.

### Latin material

Renderer:
- exact font file: `/System/Library/Fonts/Supplemental/Arial.ttf`
- font SHA-256: `525979822591a3447cfc49d943d6f7683508e25543407871c0ed8fed05fd2bd9`
- point size: 64
- tool: `hb-view`
- 96 rendered PNGs

Completed review survived the rebuild byte-identically:
- review CSV SHA-256 before/after: `4953037022e19afc97d72e4ed621434ff9f00d0aba756c4c50d82c527829b18a`

Canonical validator:
- status: `COMPLETE_HUMAN_REVIEW`
- resolved: true
- usable: **96/96**
- mismatch-visible: **48/48**
- bound rows: 96
- rejected items: 0
- pack SHA-256: `320323ff84dd9c0d3ea3e9110eead1a3b789516de43c5f31c4f414fa022f1fcb`

Mechanical gate:
- mismatches checked: 48
- visible: 48
- invisible: 0

### Devanagari material

Rebuilt battery identity:
- `items.jsonl` SHA-256: `9c69cac28c3123713652a26548eb09aabdd36966a44a433a9069b787fea6d09d`
- exactly matches frozen human-validation battery identity
- validated execution view: 96 items = 48 match + 48 mismatch
- frozen battery was read, not modified

### Verification suite

- EMP-001 tests: **366 passed**
- failures: 0
- skips: 0
- errors: 0
- preflight: **PREFLIGHT_GREEN**
- all 8 preflight checks PASS

A local isolated Python venv was used because the host had no pytest installation. It installed `pytest` and `pyyaml` from PyPI. This was ordinary package-index network traffic, not provider/model/evaluator execution and incurred no API spend.

## Spend / external-provider state

- provider/model/evaluator API calls: **0**
- paid services used: none
- consumed API spend: **USD 0**
- no EMP-001 run ledger created
- no local authorisation file created
- provider keys were unset during verification

## Controller disposition

The zero-spend code/material verification gate is now complete.

The remaining execution prerequisites are operational:
1. runtime availability of `OPENAI_API_KEY`, `GOOGLE_API_KEY`, and `FAL_KEY`, without requiring prefunding above the approved ceiling;
2. explicit user approval of the bounded EMP-001 spend.

No paid call is authorised by this review.
