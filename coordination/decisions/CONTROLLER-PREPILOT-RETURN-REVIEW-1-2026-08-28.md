# Controller — Pre-Pilot Return Review 1 — 2026-08-28

## Status
**WRITER CONTROLLER DISPOSITION.**

Reviewed against current main `2995b442dc1307532e8629243068181a32441da6`:
- `work/canon-012-aight-ir-seed`
- `work/canon-013-marketplace-triage`
- `work/res-007-pilot-writer`

No branch is merged by this decision. EVAL-035 remains outstanding.

## CANON-012 — CORRECTION REQUIRED, then Level-1 Governor review

The substantive work is useful and in scope. The Aight Normalized Request / Creative IR seed exposed genuine schema friction and correctly preserved customer-vs-fixture distinctions.

Four corrections are required before merge:

1. **Creative-IR conformance must be stated honestly.**
   SPEC-01 says derived/system-decided fields carry numeric `confidence: 0.0–1.0`, while PROJECT-CONTRACT forbids invented decimal confidence. The instance uses `confidence: not_assigned`. That is a valuable discovered contract conflict, but it means the object is **not strictly conformant to SPEC-01 as written**. Do not say both schemas represented the brief without qualification. Mark the instance/brief as a real seed with a known F5 conformance deviation.

2. **F4 is overstated.**
   SPEC-01 does have first-class exact-copy machinery under `copy` (`headline/body/cta` + `exactness`) and explicitly permits price under `brand.mandatories[]`. The narrower observed gap is that the current IR has no clean general representation for **multiple independently required exact commercial strings / arbitrary exact text elements with their own roles**, beyond fitting them into headline/body/cta or mandatories. Correct the finding; do not claim exact price copy has no first-class IR support at all.

3. **Remove the false pilot-blinding attribution.**
   Current CONTROL-STATE requires an explicit human acceptance record for PILOT-001; it does **not** require pilot review to be blinded. Blinding is required later for the architecture outcome experiment. The pilot may use a pre-frozen acceptance contract and explicit human inspection without claiming blindness.

4. **Instance-local workarounds remain instance-local.**
   `fixture: true`, `required_external_assets`, and `confidence: not_assigned` are observations/workarounds, not schema precedent. Do not mutate the frozen grammar or SPEC-01 in this correction.

Controller disposition on the broader friction:
- F1/F2/F3/F5 are real architecture/spec seams to retain for later schema revision.
- Do **not** revise the schemas before PILOT-001 merely to make this instance prettier.
- Official Aight wordmark/master remains a PILOT-001 input gate.

After the corrections, CANON-012 is eligible for bounded Level-1 Governor review.

## CANON-013 — ACCEPT TASK RESULT; SPLIT REMAINS UNFROZEN

The triage satisfies the task:
- all 16 runnable cases were assessed;
- the worker distinguished constructible fixtures from operational burden;
- no media/model evidence contaminated selection;
- an auditable 8-development / 8-holdout proposal exists.

The triage and proposed split may proceed to bounded Level-1 Governor review.

**The proposed 8/8 split is NOT frozen by this decision.**

Reason: MKT-003 and MKT-004 make the holdout materially dependent on long-form segmentation/assembly and human subject-matter judgement. Before freezing the final split, the Controller will decide the architecture experiment's representative-deliverable policy and the v0 production envelope. Freezing before that would turn an implementation assumption into a holdout constraint.

No new CANON-013 execution is authorised.

## RES-007 — BLOCK; RESUME SAME TASK WITH CONTROLLER-APPROVED CORRECTION

The implementation demonstrates useful writer mechanics, but the task's first STOP CONDITION fired.

### Observed contract defect

Outcome topology v3 says `attempt` inherits v2.1 attempt semantics. v2.1 requires, among other fields:
- `eval_item_id`
- `provider`
- `model_id`
- `model_version`
- `endpoint`
- `workflow`
- `prompt_hash`
- `config_hash`
- `config_location`
- `reference_asset_hashes`
- `requested_at`
- `completed_at`
- `status`
- `cost_ref`
- `storage_class`
- repeat/retry fields.

The RES-007 writer accepts arbitrary `provider_fields` and does not mechanically require that inherited set. The synthetic production attempts also omit several required inherited fields. The current v3 validator does not catch this.

Therefore an archive can pass the current validator while violating the written v3 inheritance contract.

The worker noticed `eval_item_id` but treated it as low priority. It is not: RES-007 explicitly said to STOP if the accepted v3 schema could not represent the pilot journey without a contract change.

### Controller-approved narrow v3 correction

RES-007 may resume on the same branch with this exact correction authority:

1. **Production semantics for `eval_item_id`:**
   - for benchmark/evaluation attempts, `eval_item_id` remains required exactly as v2.1;
   - for v3 production-job attempts, `eval_item_id` is not required and must not be fabricated; the attempt is already linked through step → unit → set → outcome → job → `brief_ref`;
   - document this as an explicit v3 conditional override, preserving all historical v2.1 archives unchanged.

2. **All other inherited required attempt provenance stays required.**
   The v3 validator must fail closed when a v3 provider attempt omits required call identity/provenance fields.

3. **Writer enforcement.**
   `OutcomeWriter.record_attempt` must require the applicable production-attempt field set instead of accepting an unconstrained provider-fields bag as sufficient.

4. **Controls.**
   Add negative controls proving missing required provenance is rejected, while a valid production attempt with no `eval_item_id` passes.

5. **Synthetic archive.**
   Regenerate the synthetic journey so every production provider attempt is contract-valid under the corrected v3 rules.

6. **Controller Brief.**
   Correct status/history: the original run exposed a stop-condition defect; the resumed pass resolves it under this Controller authority. Do not describe the original validator pass as proof the uncorrected schema was fully satisfied.

This is a bounded correction to make v3 usable for its declared production purpose, not permission to redesign CpAO/topology generally. HED-1 remains untouched.

After correction, RES-007 requires Level-1 Governor review before merge.

## Merge posture

No returned branch may merge yet:
- CANON-012: correction first;
- CANON-013: ready for Governor review, split still proposal only;
- RES-007: correction first;
- EVAL-035: still outstanding.

