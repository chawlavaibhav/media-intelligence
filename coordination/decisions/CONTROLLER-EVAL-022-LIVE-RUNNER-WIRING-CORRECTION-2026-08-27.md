# Controller EVAL-022 Final Live-Runner Wiring Correction — 2026-08-27

## Status

**REQUIRED BEFORE THE ALREADY-AUTHORISED LIVE CLOUD VISION PHASE CAN EXECUTE. NO NEW USER APPROVAL IS NEEDED.**

The pushed OCR branch `eval/eval-022-ocr-family-readiness` at worker-reported head
`6b174b2659584e23fa5704ad48058e0d5c9f35df` passes the scientific/infrastructure taxonomy
correction and zero-spend verification, but Controller inspection found one execution gap:

`eval/empirical-tranche-1/text_qualification/qualify_ocr.py` currently exposes only
`--fake-live` and `--budget-proof`. It does not construct a real Cloud Vision candidate,
does not expose `--live`, and does not open the persistent EMP-001 run/stage budget.

Therefore Phase 4 could not actually execute from the reported tested head even if
`GOOGLE_CLOUD_VISION_API_KEY` were present.

This is a wiring/readiness defect, not a scientific-contract defect.

## Required zero-spend correction

Add the live OCR orchestration path without changing:
- OCR contract thresholds;
- battery;
- normalization;
- provider configuration;
- target-blindness semantics;
- retries 0;
- scientific/infrastructure taxonomy;
- USD 0.0015/image conservative price basis.

### CLI / run controls

Mirror the already accepted persistent EMP-001 qualification discipline used by the VLM runner.

The OCR runner must expose at minimum:
- `--live`;
- `--authorisation`;
- `--run-root`;
- `--run-id`;
- `--out`.

Live execution must:
1. fail closed unless the existing EMP-001 authorisation is valid;
2. open/create the same persistent tranche run;
3. use `TrancheBudget(run).stage("qualification")`, so historical qualification spend is included;
4. construct exactly one candidate:
   - `CloudVisionTextDetection`
   - `CloudVisionHttpTransport`
   - no language hints;
5. read `GOOGLE_CLOUD_VISION_API_KEY` only at dispatch;
6. start Devanagari from call 1;
7. progress to Latin only on `passed is True`;
8. persist a new human-readable OCR live result plus canonical
   `ocr-qualification-result.json` in the EMP-001 evidence directory;
9. preserve all historical evidence files and append only to the persistent spend ledger;
10. stop before A-TEXT even if OCR qualifies both scripts.

### Spend controls

The user's already-recorded combined authorization remains authoritative:
- incremental OCR cap: USD 1.00;
- frozen protocol max reservation: USD 0.864;
- prior qualification spend: USD 0.6712415;
- prospective cumulative: USD 1.5352415 <= USD 6;
- retries 0.

The live path must mechanically refuse any plan/configuration that can exceed the frozen 576 OCR
calls or USD 0.864 OCR reservation. No free-tier assumption.

### Infrastructure semantics

Keep the accepted correction:
- empty successful OCR result = scientific `empty_transcription`;
- provider/API/quota/backend/transport/malformed failures = infrastructure;
- infrastructure failure persists billing/trial evidence, stops, and yields `passed: null` for an
  incomplete script;
- missing key is pre-dispatch, zero calls, zero spend.

### Zero-network tests required before live

Add tests proving:
1. CLI `--live` refuses without authorisation;
2. missing `GOOGLE_CLOUD_VISION_API_KEY` refuses before dispatch;
3. injected fake HTTP through the LIVE orchestration completes 576 calls for a clean candidate;
4. live orchestration writes canonical OCR qualification evidence;
5. canonical evidence fingerprint recomputes;
6. live orchestration uses the persistent qualification stage budget and respects prior spend;
7. infrastructure stop persists the trial and leaves scientific disposition null;
8. retries remain 0;
9. A-TEXT remains blocked;
10. all previous tests/preflight stay green;
11. external calls during verification = 0; spend = USD 0;
12. previous empirical evidence remains byte-identical.

## Branch handling

Bring current `origin/main` into the OCR branch before final verification so the branch contains
all Controller decisions made after its original base. Do not alter historical evidence.

After correction:
- push the new exact HEAD;
- do not merge;
- return the exact pushed/tested HEAD.

If the local Cloud Vision key exists at that point and every zero-spend verification gate is green,
the already-recorded combined authorization permits immediate live execution from that exact
pushed/tested head. No further Controller approval is required.

If the key is still missing, stop pre-dispatch and report only the key blocker.

A-TEXT remains blocked.
Registry remains unchanged.
