# RESOURCES–EVAL STORAGE INTEGRATION PASS

**Status:** AUTHORIZED final bounded integration correction on `work/resources-v1-overnight` only.  
**Purpose:** make the Resources v2 persistence contract and the corrected Eval harness wire-compatible before either branch merges.  
**Spend:** ₹0. No acquisition, paid API call, raw-corpus access, Canon/Eval semantic redesign, or merge to `main` is authorized.

## Zoom-out

Resources owns persistent evidence storage and preservation. Eval owns capability/instrument semantics. Both correction passes now agree conceptually on **attempt → artifact → measurement → acceptance**, repeat ≠ retry, canonical observation units, and retention of failed/refused calls. The remaining defect is the exact wire contract: Eval's emitted JSONL does not yet validate against Resources v2.

Do **not** redesign R1–R5/R8 or add another persistence model. Tighten the one canonical contract so Eval can emit it exactly.

## Controller decisions

### RI-C1 — Trial semantics must be one call = one trial

The project definition is: one provider/API generation/transform call is one trial. A deliberate repeat is another trial; a production retry is another trial. Derived frames/crops/transcodes are artifacts of the parent trial and add no trials.

Therefore:
- every `attempt_id` maps to exactly one unique `trial_id`;
- no two provider attempts may share a `trial_id`;
- a retry gets its own `trial_id` and links backward through `retry_of_attempt_id`;
- a repeat gets its own `trial_id` and links through `repeat_of_attempt_id`;
- derived artifacts inherit the producing attempt's `trial_id`.

It is acceptable for `trial_id == attempt_id`; if a distinct id is kept, enforce one-to-one uniqueness. Update schema prose and validator/negative controls. The current phrase that `trial_id` "groups attempts" is too permissive and must be removed.

### RI-C2 — Freeze exact machine vocabularies

Use exact lane ids:
`image | general_video | native_av | lipsync | tts`.

Use exact attempt status ids:
`ok | error | refusal | timeout | cancelled`.

Resources stores these; it does not invent display-name variants.

### RI-C3 — Absence vocabulary belongs to Eval, but attempt failures are not measurement absences

Adopt this canonical measurement `absence_reason` set for V1:
`not_applicable | not_measured | instrument_unavailable | parse_failure | human_adjudication_pending | other`.

Rules:
- provider refusal/error/timeout belongs on the **attempt**, not a fake measurement;
- `instrument_unqualified` is not an absence: an unqualified instrument may still emit an observational result, carrying `instrument_qualification_ref: required_but_no_calibrated_instrument`; it simply cannot create a Registry score;
- exactly one of `result` and `absence_reason` is non-null.

Update the schema, handoff doc and validator/negative controls accordingly.

### RI-C4 — Keep the exact required fields and make cost provenance explicit

The following remain required for a real attempt: `trial_id`, `prompt_hash`, `status`, `cost_ref`, `storage_class`, plus the existing identity/config/reference/timestamp fields.

A paid attempt's `cost_ref` must resolve to an immutable recorded cost ledger entry. Add/clarify the minimal cost-ledger contract needed to validate this reference. Synthetic tests may use clearly synthetic ledger rows, never fabricated real-provider costs.

Artifact records retain required `output_bytes`, `media_kind`, and explicit derivation fields. Measurement records retain flat instrument identity/version/config/qualification provenance.

### RI-C5 — Prove the real cross-branch interface

After updating Resources, fetch the latest `work/eval-v1-overnight` branch into a temporary worktree or otherwise inspect its emitted archive. Do not edit Eval-owned files.

The completion gate is **not** "our Resources validator passes on our own dummy generator." It is:

> a corrected Eval harness dummy archive validates with the Resources validator at exit 0, using the same canonical schema/vocabulary.

If Eval has not yet pushed its integration correction, record `BLOCKED_WAITING_FOR_EVAL_INTERFACE` and provide the exact failing fields from its latest archive rather than weakening the validator.

## Required negative controls

Add/retain tests proving:
1. two attempts sharing one trial id are rejected;
2. a repeat and retry each get their own trial;
3. `refused` is rejected as persistent status while `refusal` is accepted;
4. provider failure cannot be represented only as a measurement absence;
5. `instrument_unqualified` is rejected as an absence reason;
6. a paid/real-shaped attempt with missing/unresolvable `cost_ref` is rejected;
7. the corrected Eval archive validates cleanly once available.

## Completion

Write `resources/findings/RESOURCES-EVAL-STORAGE-INTEGRATION-CONTROLLER-BRIEF.md` with exact commands/results and unresolved items. Commit and push to the existing branch. Do not merge.