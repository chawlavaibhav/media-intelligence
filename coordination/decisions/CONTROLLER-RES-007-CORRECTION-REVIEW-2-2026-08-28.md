# Controller — RES-007 Correction Review 2 — 2026-08-28

## Status
**CORRECTION REQUIRED. WRITER CONTROLLER DISPOSITION.**

Reviewed against current main `8a0be0efe857cff8903f0f67822e237a28d230a0`:
- `work/res-007-pilot-writer`

CANON-012 was also rechecked and has no material change beyond the correction already accepted in
`CONTROLLER-CANON-012-CORRECTION-ACCEPTANCE-2026-08-28.md`; that acceptance stands.

## RES-007 — what is now correct

The second pass correctly implements the Controller-approved `eval_item_id` production override:
- `attempt_kind: production | benchmark_eval` is explicit;
- production attempts must not fabricate `eval_item_id`;
- benchmark/eval attempts still require it;
- writer arguments now name the core inherited provider provenance rather than accepting an unconstrained bag;
- the durable validator now checks the required provenance field set;
- the first-pass stop-condition defect is reported honestly;
- binary/local/human/repair/CpAO behaviours remain intact.

## Remaining defect

The Controller cannot accept the brief's claim that **"passes the validator" now means "conforms to
the written v3 attempt contract"** because G12 still under-checks several mechanically explicit
v2.1 requirements.

At minimum, current `validate_topology_v3.py`:
- does not validate the required `lane` field at all;
- checks `repeat_index` only for presence, not that it is a 0-based integer;
- checks `storage_class` only for non-emptiness, not that it equals
  `C_irreproducible_empirical`;
- treats SHA-256 provenance fields as arbitrary non-empty strings rather than 64-hex hashes;
- does not verify repeat/retry back-references resolve to real attempts;
- does not mechanically validate the recorded timestamps as ISO-8601 UTC.

The writer mirrors some but not all of these constraints. The synthetic tests themselves use
placeholder hash strings in places, so they do not prove the inherited hash semantics.

This is the same class of problem RES-007 is intended to close: a durable archive can still receive
a validator PASS while violating written inherited attempt semantics.

## Bounded correction authority

Resume RES-007 on the same branch. Do not redesign v3 or CpAO.

Extend G12 and the writer only for cheap, explicit, already-written v2.1 attempt invariants:

1. **lane**
   - required on every v3 attempt;
   - must be one of the frozen v2.1 lane values.

2. **storage_class**
   - must equal `C_irreproducible_empirical`.

3. **repeat_index**
   - must be an integer >= 0; booleans are not integers for this purpose.

4. **hash provenance**
   - `prompt_hash` and `config_hash` must be valid SHA-256 hex strings;
   - every value in `reference_asset_hashes` must be a valid SHA-256 hex string;
   - an empty reference list remains valid.

5. **repeat/retry references**
   - non-null `repeat_of_attempt_id` and `retry_of_attempt_id` must resolve to existing attempts;
   - preserve the existing retry-reason requirement;
   - do not invent additional repeat/retry policy beyond the written contract.

6. **timestamps**
   - `requested_at` must be a valid ISO-8601 UTC timestamp;
   - non-null `completed_at` must be a valid ISO-8601 UTC timestamp;
   - null `completed_at` remains valid where the call never completed.

7. **controls**
   - add bounded negative controls proving the validator rejects the above violations;
   - update synthetic fixtures to use genuine SHA-256 strings, not placeholder pseudo-hashes;
   - retain all existing G12 and CpAO controls.

Do not expand this correction into provider-specific validation, URL semantics, model-id vocabularies,
or new topology concepts.

## Branch hygiene

Before returning, update/rebase the RES-007 task branch onto current `main` without importing
unrelated worker-branch commits.

## Merge posture

RES-007 is **not Controller-accepted yet**.

After this bounded correction, it can return directly for Controller review. If accepted, it becomes
eligible for Level-1 Governor review.

CANON-012 remains Controller-accepted and Governor-pending.
