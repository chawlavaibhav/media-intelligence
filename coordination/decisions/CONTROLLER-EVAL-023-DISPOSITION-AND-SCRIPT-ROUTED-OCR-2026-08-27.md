# Controller EVAL-023 Disposition and Script-Routed Literal OCR Follow-Up — 2026-08-27

## Status

**EVAL-023 ACCEPTED AND INTEGRATED. TESSERACT `hin+eng` LITERAL CONFIGURATION IS DISQUALIFIED. ONE FINAL ZERO-API-COST TESSERACT FOLLOW-UP IS AUTHORISED: SCRIPT-ROUTED `hin` AND `eng` LEGS.**

Integration:
- PR #46
- merge commit `0ecbf5f19cd6a3a14a15e85e1a1f6ae8fa690431`

Tested EVAL-023 head:
- `4783a3a5a560fe171031d08a7e279449bbaf446a`

## Accepted Devanagari result

Frozen candidate:
- Tesseract 5.5.3
- tessdata_best tag 4.1.0 / commit `e2aad9b983032bb1beff9133104a67cdbb87ca4d`
- `hin+eng`
- OEM 1
- PSM 13
- all six DAWG lexical aids disabled
- fresh process per trial
- retries 0
- API spend USD 0

Devanagari:
- 288/288 complete;
- false passes: **3** across **1 unique item**;
- match false-fail rate: **0.6667**;
- empty transcriptions: 0;
- repeat consistency: 1.0;
- failed gates: `mismatch_false_pass`, `match_false_fail_rate`.

Disposition:
- candidate is scientifically **DISQUALIFIED**.

## Mechanism finding

Removing lexical/dictionary priors reduced false passes dramatically relative to Sonnet, Gemini and
Cloud Vision. The remaining Devanagari false pass was a direct glyph confusion rather than broad
word repair.

This supports the mechanism claim:
- lexical/language priors are a major driver of silent correction;
- removing them improves safety;
- but the `hin+eng` literal configuration becomes too inaccurate on valid text.

The trade-off is now empirically demonstrated rather than hypothetical.

## Latin diagnostic

At the user's request, the worker ran the same frozen configuration on Latin after Devanagari had
already failed.

Controller classification:
- **useful diagnostic evidence; not qualification evidence**;
- do not alter `qualified_scope`;
- do not rewrite the canonical progressive qualification record;
- do not use this post-hoc Latin run to claim the candidate qualified or completed the frozen
  progressive protocol.

Diagnostic Latin result:
- 288/288 executions;
- false passes: 12 / 4 unique;
- match false-fail rate: 0.1875;
- repeat consistency: 1.0;
- all false passes were confusable substitutions such as O/0, 5/S and Z/2;
- no API spend.

Interpretation:
- Latin failure mechanism is more optical/glyph-confusability driven than the Devanagari lexical
  repair problem;
- loosening normalization is NOT authorised because it would break cross-candidate comparability.

## Final Tesseract follow-up: script-routed literal OCR

The mixed `hin+eng` configuration produced many wrong-script reads. The customer's requested text
script is already known upstream, so selecting a script-specific OCR leg is not leakage and is not
a production trick learned from the answer. It is a legitimate evaluator workflow.

Authorise one final zero-cost probe with the configuration frozen before results:

### Devanagari leg
- alias: `tesseract5-hin-literal-psm13-v1`
- languages: `hin`
- same Tesseract build
- same pinned `hin.traineddata`
- OEM 1
- PSM 13
- all six DAWG flags 0
- no preprocessing
- retries 0
- full 96 × 3 = 288 Devanagari executions

### Latin leg
- alias: `tesseract5-eng-literal-psm13-v1`
- languages: `eng`
- same Tesseract build
- same pinned `eng.traineddata`
- OEM 1
- PSM 13
- all six DAWG flags 0
- no preprocessing
- retries 0
- full 96 × 3 = 288 Latin executions

Both legs may run in the same task because they are local and zero-cost.

Do not make either leg contingent on the other's result. The purpose is to measure whether
script-routing removes wrong-script errors on each script.

## Qualification interpretation

Each leg is evaluated under the existing OCR scientific gates:
- mismatch false-pass max 0;
- match false-fail rate max 0.10;
- empty-transcription rate max 0.05;
- repeat consistency min 0.95.

If BOTH script-specific legs pass:
- do not automatically open A-TEXT;
- return to Controller to define a fingerprinted composite script-routed OCR evaluator identity and
  handoff.

If either leg fails mismatch false-pass:
- stop Tesseract tuning after this task;
- do not try further PSM/preprocessing/config sweeps without a new mechanistic rationale.

If false-pass clears but false-fail remains above threshold:
- report the gap;
- Controller may consider a complementary evaluator/ensemble design, not ad-hoc normalization changes.

## Spend / boundaries

- API spend: USD 0;
- no Gemini, Cloud Vision, Anthropic or fal calls in this task;
- no Registry population;
- A-TEXT evaluation remains blocked;
- current cumulative paid qualification spend remains USD 1.3037905.
