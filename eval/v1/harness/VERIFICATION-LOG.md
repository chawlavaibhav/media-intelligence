# E5 harness verification log

**Executed:** 26 Aug 2026 in the cloud session · **Runner:** Python 3.11.15
**Status:** `implementation_written_AND_executed_in_cloud`
**Covers:** E-C4–E-C7 corrections and EI-C1–EI-C8 storage integration

All fixtures are dummy/synthetic. No network call, no model call, no paid API call,
no empirical Registry row.

```
python3 eval/v1/harness/run_selftest.py
```

```text
==========================================================================
E5 HARNESS VERIFICATION — dummy/synthetic fixtures only, zero spend
==========================================================================

DEMO 1 — one generated asset scored by several evaluators, no regeneration
  [PASS] one generation call only
         attempts=1, assets=1
  [PASS] >=3 distinct evaluators scored the SAME asset
         12 measurements from 4 instruments (dummy-ocr, dummy-temporal, dummy-vlm, file-probe) on 1 asset
  [PASS] all measurements point at that one asset
  [PASS] still exactly one trial asset
         measurements_per_trial_asset = 12.0x
  [PASS] multiple defects recorded on one output
         co-occurrence: ['face_drift + text_mutates_mid_clip']

DEMO 2 — an experimental REPEAT creates a new attempt, never a replacement
  [PASS] new attempt id
         att-d58327e0143c -> att-d8f477d94aa3
  [PASS] new asset id (original NOT overwritten)
  [PASS] original asset still on disk with its original hash
  [PASS] repeat linkage recorded as a REPEAT
  [PASS] a repeat is NOT a retry
  [PASS] each asset has exactly one provenance record

DEMO 2b — E-C4: repeat and retry are structurally separate
  [PASS] a repeat is counted as a repeat, NOT a retry
         experimental_repeats=1
  [PASS] a retry is counted as a retry, NOT a repeat
         production_retries=1
  [PASS] the two counters are reported separately and never summed
  [PASS] EI-C2: a repeat gets its OWN trial id, never the original's
  [PASS] EI-C2: a retry gets its OWN trial id, never the original's
  [PASS] the CpAO retry chain contains the retry and EXCLUDES the repeat
         chain=['att-d58327e0143c', 'att-25144b2d0a1f']
  [PASS] retry-attempt cost and repeat cost are separate, accurately named lines
         retry_attempts=1.0 repeats=1.0
  [PASS] a COMPLETE chain cost includes the originator, unlike the retry-only line
         complete chain=2.0 vs retry-only=1.0 - the old key summed only retries and could never have been a chain cost
  [PASS] an attempt that is BOTH repeat and retry is REFUSED
         raised: An attempt cannot be BOTH an experimental repeat and a production retry. A repeat is decided before the run to measure r
  [PASS] a retry with no reason is REFUSED
         raised: A production retry requires retry_reason. An unexplained retry is indistinguishable from an experimental repeat.
  [PASS] a repeat with repeat_index 0 is REFUSED
         raised: An experimental repeat requires a repeat_index >= 1. repeat_index 0 is the first attempt of a repeat set, not a repeat o

DEMO 3 — frames sampled from a clip keep the parent trial id
  [PASS] 4 child assets created
  [PASS] every frame names its parent
  [PASS] every frame inherits the parent's TRIAL id (EI-C2)
  [PASS] every frame inherits the parent's ATTEMPT id
  [PASS] 4 frames added 0 new trials
         assets=6 but trials=2 (2 calls, 4 derived frames). The trial is the CALL.
  [PASS] trial_id == attempt_id, one-to-one by construction (EI-C2)
  [PASS] frame extraction cost nothing

DEMO 4 — the duplicate-regeneration guard fires
  [PASS] regenerating the same item+config is REFUSED
         raised: DUPLICATE GENERATION REFUSED for item compound-024 config 9ee2cda49772: asset ast-c0475d53d85e already exists. Evaluatin
  [PASS] guard did not create a stray attempt
         attempts still 2
  [PASS] but re-measuring the SAME asset is allowed and free
         evaluating another capability needs no new generation - the point of fan-out

DEMO 5 — an unqualified instrument cannot write a Registry row
  [PASS] unqualified instrument REFUSED at the Registry boundary
         raised: REGISTRY WRITE REFUSED: instrument dummy-vlm has qualification status 'screened_not_qualified'. Only ('qualified', 'dete
  [PASS] dummy-vlm is correctly marked not-writable
         status=screened_not_qualified
  [PASS] file-probe IS writable (deterministic needs no calibration)
  [PASS] even a QUALIFIED instrument is refused on synthetic data
         raised: REGISTRY WRITE REFUSED: synthetic/dummy measurements may never become empirical Registry rows. There is no override.
  [PASS] empty measurement set is REFUSED
         raised: REGISTRY WRITE REFUSED: no measurements. An empty check is not a passing check.
  [PASS] registry still empty

DEMO 5d — E-C6: there is NO synthetic promotion bypass
  [PASS] write_registry_row exposes NO override parameter
         parameters: ['capability', 'instrument_id', 'measurements', 'conditions', 'difficulty_level', 'repeats_per_item']
  [PASS] no allow_synthetic anywhere in the harness source
  [PASS] no call shape promotes synthetic measurements
         2/2 call shapes refused
  [PASS] registry STILL empty after bypass attempts

DEMO 5e — E-C5: a Registry row must be ONE coherent cell
  [PASS] mixing TWO MODELS in one cell is REFUSED
         raised: REGISTRY WRITE REFUSED: mixed cell. Trials disagree on 'model': ['model-A', 'model-B']. Two providers, models, versions,
  [PASS] mixing TWO CAPABILITIES in one cell is REFUSED
         raised: REGISTRY WRITE REFUSED: mixed cell. Measurements disagree on 'capability': ['action_adherence', 'text_logo_stability_in_
  [PASS] mixing TWO INSTRUMENTS in one cell is REFUSED
         raised: REGISTRY WRITE REFUSED: mixed cell. Measurements disagree on 'capability': ['action_adherence', 'text_logo_stability_in_
  [PASS] a capability that is not the requested one is REFUSED
         raised: REGISTRY WRITE REFUSED: requested capability 'text_logo_stability_in_clip' but measurements are for 'action_adherence'.
  [PASS] an instrument that is not the requested one is REFUSED
         raised: REGISTRY WRITE REFUSED: requested instrument 'dummy-ocr' but measurements came from 'dummy-temporal'.
  [PASS] a declared condition contradicting the trials is REFUSED
         raised: REGISTRY WRITE REFUSED: declared condition model='model-Z' contradicts the trials, which carry 'model-A'.
  [PASS] an over-declared repeats_per_item is not trusted
         raised: REGISTRY WRITE REFUSED: repeats_per_item must be >= 1.
  [PASS] pooling a production RETRY into a pass-rate cell is REFUSED
         raised: REGISTRY WRITE REFUSED: 1 trial(s) in this cell are production RETRIES. A retry exists because something failed; pooling
  [PASS] no Registry row was created by any mixed-cell attempt

DEMO 5b — absence reasons and harness negative controls
  [PASS] 'absent' carries a machine-readable reason
         reason=not_applicable
  [PASS] 'absent' with NO reason is REFUSED
         raised: absent verdict needs a reason from ('not_applicable', 'not_measured', 'instrument_unavailable', 'parse_failure', 'human_
  [PASS] verdict outside the vocabulary is REFUSED
         raised: instrument returned unknown verdict probably_fine
  [PASS] found a capability owned by the instrument but outside the fan-out
         using 'anatomy_hands'
  [PASS] scoring a capability outside the item's fan-out is REFUSED
         raised: capability anatomy_hands is not in item compound-006's measurement fan-out. The bank decides what an asset may validly e
  [PASS] using an instrument outside its judgement family is REFUSED
         raised: instrument dummy-ocr is not specified for capability object_count. Qualification NEVER generalises across judgement fami

DEMO 5c — EI-C5: a provider failure lives on the ATTEMPT, not a measurement
  [PASS] refusal recorded as a refusal, not a failed capability
         refusals=1, error_classes={'moderation_block': 1}
  [PASS] canonical persistent status is 'refusal', not 'refused'
  [PASS] a refused attempt still has a trial id and a cost_ref
  [PASS] measuring a failed attempt is REFUSED (no double-counting)
         raised: unknown asset x

DEMO 5f — EI-C6: cost is summed over ATTEMPTS, not over artifacts
  [PASS] a refused attempt with non-zero cost SURVIVES the total
         total=2.25 (1.00 ok + 0.75 refusal + 0.50 error). Summing produced artifacts only would give 1.00.
  [PASS] the dropped portion is surfaced explicitly
         failed/refused cost=1.25
  [PASS] every attempt has a resolvable cost_ref
         3 ledger lines
  [PASS] the misleading cost_in_retry_chains key is GONE
  [PASS] no complete CpAO chain cost is claimed without an acceptance
         status=not_computed_no_acceptance_exists

DEMO 6 — the Registry schema validates and starts EMPTY
  [PASS] registry file exists
  [PASS] registry contains ZERO empirical rows
         0 data rows
  [PASS] registry schema file exists
  [PASS] schema parses and declares zero entries
         status=PROPOSED_NOT_IN_FORCE

DEMO 6b — EI-C7: repeat structure is DERIVED from provenance
  [PASS] a BALANCED cell is built from real provenance (2 items x 2 repeats)
         4 measurements over 4 distinct trials
  [PASS] EI-C7: declaring 2 repeats while only 1 was observed is REFUSED
         raised: REGISTRY WRITE REFUSED: declared repeats_per_item=2 but the observed trial structure is {'compound-026': 1}. Items ['com
  [PASS] EI-C7: two measurements of ONE trial is REFUSED
         raised: REGISTRY WRITE REFUSED: 1 trial(s) contribute more than one scoreable measurement to this cell (e.g. att-027f9e6ce927). 
  [PASS] EI-C7: one item with fewer repeats than another is REFUSED
         raised: REGISTRY WRITE REFUSED: declared repeats_per_item=2 but the observed trial structure is {'compound-028': 1, 'compound-02
  [PASS] EI-C7: a retry masquerading inside the repeat cell is REFUSED
         raised: REGISTRY WRITE REFUSED: 1 trial(s) in this cell are production RETRIES. A retry exists because something failed; pooling
  [PASS] EI-C7: a mis-shaped cell (3 trials over 2 items) is REFUSED
         raised: REGISTRY WRITE REFUSED: declared repeats_per_item=2 but the observed trial structure is {'compound-024': 2, 'compound-02
  [PASS] the balance invariant trials == n_items x repeats is enforced in code
  [PASS] no Registry row was created by any EI-C7 attempt

DEMO 7 — E-C7: canonical Resources storage handoff
  [PASS] canonical record file emitted: attempts.jsonl
  [PASS] canonical record file emitted: artifacts.jsonl
  [PASS] canonical record file emitted: measurements.jsonl
  [PASS] canonical record file emitted: acceptances.jsonl
  [PASS] no competing Eval-specific persistent manifest is emitted
         the old single manifest is gone; Resources owns the persistent model
  [PASS] every failed/refused call survives as an ATTEMPT record
         2 non-ok attempts, none with a direct artifact, all carrying error_detail; statuses=['error', 'refusal']
  [PASS] attempts without an artifact are NOT dropped from the handoff
         attempts_without_artifact=2
  [PASS] attempt records carry every contract field
         5 rows, 23 required, missing=none
  [PASS] artifact records carry every contract field
         7 rows, 11 required, missing=none
  [PASS] measurement records carry every contract field
         14 rows, 13 required, missing=none
  [PASS] observation units are the CANONICAL vocabulary only
         used: ['frame']
  [PASS] derived artifacts point to a parent and add no trial
         7 artifacts, 4 derived, 5 trials
  [PASS] acceptance is EMPTY - Eval does not decide it
  [PASS] artifact locations are RELATIVE, not machine-specific
         7 artifacts, absolute paths: none
  [PASS] the handoff emission is deterministic across calls
  [PASS] no routing score or weight was computed
  [PASS] generation and evaluator costs are separate lines
         gen=5.0 eval=0.121

==========================================================================
RESULT: 95/95 checks passed
Registry rows created: 0  (must be 0)
Paid API calls made:   0
==========================================================================
```
