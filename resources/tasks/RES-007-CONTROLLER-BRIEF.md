# Controller Brief — RES-007 (corrected)

**TASK:** RES-007
**STATUS:** completed — correction pass under
`coordination/decisions/CONTROLLER-PREPILOT-RETURN-REVIEW-1-2026-08-28.md`; awaiting
Level-1 Governor review before merge.

**HUMAN SUMMARY:** The project now has working, contract-conformant software that can
*record* a real customer production job — every provider call (including failed ones), every
local ffmpeg-style operation, every human review, every file of actual bytes, and every cost
— in the frozen v3 format, and the validators now actually enforce the whole written
contract. That last part is the correction: **the first pass had a real defect, and the
task's own stop condition should have fired.** The v3 rulebook says a provider-call record
inherits the older v2.1 record's required fields (which provider, which model, which
endpoint, hashes of the exact prompt and configuration sent, timestamps, and a benchmark
item id). My first writer accepted any assortment of those fields, my synthetic records
omitted several, and the validator checked none of them — so a record could pass validation
while violating the written contract. My first brief wrongly filed this as a low-priority
observation instead of stopping. The Controller has now ruled on the one genuinely
inapplicable field: `eval_item_id` (the benchmark-item link) stays required for
benchmark/evaluation calls exactly as written, is not required for production-job calls, and
must never be faked there — a production call's context is its chain to the customer brief.
Everything else stays mandatory and is now mechanically enforced by a new validation gate
(G12) in the validator, by the writer itself, and by ten new controls. The corrected
synthetic journey passes end to end and the cost engine still reproduces the hand-computed
total exactly. No money was spent; no real provider was called; HED-1 remains untouched.

**WHAT I DID:** Applied the Controller-approved narrow correction in four places. (1) The
frozen topology document now states the conditional override explicitly (attempt entity
`v3_conditional_override` + gate G12), and states that every other inherited field stays
required. (2) `validate_topology_v3.py` enforces G12 fail-closed: every v3 attempt must
declare `attempt_kind: production | benchmark_eval` (refused, not guessed, when absent) and
carry the full inherited call provenance; `eval_item_id` is required iff benchmark, refused
on production rows. (3) `OutcomeWriter.record_attempt` now takes the provenance as named
required parameters — the unconstrained field bag is gone; unknown extras are refused; the
v2.1 nullable meanings are preserved rather than reinvented (`completed_at` null only for a
call that never completed, and it must be passed explicitly; repeat/retry links null on a
first attempt; `reference_asset_hashes` an empty list, never null). (4) The synthetic
journey, all lineage fixtures, and the control suite were regenerated/extended and re-run.

**OBSERVED:**
- 22/22 writer tests pass; lineage controls **28/28** (2 positives + 26 negatives; was
  18/18 before the correction added ten G12 controls); CpAO controls **13/13 unchanged**.
- Positive controls: the corrected production journey passes all 12 gates with no
  `eval_item_id` anywhere; a benchmark-kind attempt with its `eval_item_id` also passes
  (`v3-valid-benchmark-attempt.yaml`, `benchmark-attempt-journey.yaml`).
- Negative controls (each rejected under G12, by the validator on the durable archive, not
  only by the writer): missing `attempt_kind`; production attempt missing `provider`,
  `model_id`, `prompt_hash`, `config_hash`, `config_location`, or
  `reference_asset_hashes`; benchmark attempt missing `eval_item_id`; production attempt
  *carrying* an `eval_item_id` (fabricated benchmark link).
- Writer-level enforcement observed: null/omitted required provenance, unknown extra
  fields, `eval_item_id` on production rows, and benchmark rows without it are all refused
  at record time with explanatory errors.
- All first-pass properties re-verified after the correction: binary artifacts (bytes not
  valid UTF-8; SHA-256/byte counts recomputed from disk and matching), provider/local/human
  step distinction, failed refusal+timeout attempts preserved individually with no faked
  artifacts (the timed-out call records `completed_at: null` — the v2.1 meaning of "never
  completed"), ordered multi-parent lineage, repair step, deterministic byte-for-byte
  output, and CpAO recomputed at fully-loaded **42.00 XTS** matching the independent
  hand-computed expectation; the `human_optional` entry remains visibly excluded.
- The pre-existing 17 negative lineage fixtures were updated only by adding the
  now-required provenance to their attempts; each still fails for **its own declared
  gate** (verified by the control suite's gate-matching check).
- Historical v2.1 archives: untouched. G12 applies only to `schema_era: v3` records; the
  v2.1 validator and archives are unchanged, and G9 still blocks context backfill.

**INFERRED:** With inheritance now mechanically enforced, "passes the validator" and
"conforms to the written v3 contract" mean the same thing for attempt provenance. I base
this on the validator rejecting each seeded violation on the durable archive itself,
independently of the writer.

**SURPRISES / BELIEF UPDATES:** The first pass's "all gates green" was weaker evidence than
it appeared: a validator can only prove the rules it implements. The belief to carry
forward: when a contract says "inherits X", conformance is not established until something
mechanically checks X.

**FAILURES / BLOCKERS (including corrected history):**
- **First pass: a stop-condition defect, not a low-risk footnote.** RES-007's stop condition
  ("the accepted v3 schema cannot represent the pilot journey without a contract change")
  fired in substance: v2.1-required `eval_item_id` has no truthful value for a production
  attempt, and the only ways through were fabricating one, silently dropping inherited
  requirements (what actually happened), or a contract change. I should have stopped with
  `STOP — CONTEXT_INSUFFICIENT`/`needs_controller_review` instead of noting it under
  "unknown". The first validator pass therefore did **not** prove full contract
  conformance — the validator simply never checked inheritance.
- The earlier workspace incident (parallel workers sharing one checkout; commit re-parented
  onto clean main) remains as reported previously; this correction pass ran in an isolated
  worktree and did not touch the shared checkout.

**UNKNOWN / NOT VERIFIED:** Real provider payloads may still surface fields or shapes the
synthetic journey does not exercise; the writer now fails closed on anything outside the
contract, so the failure mode is a loud refusal, not silent acceptance — but this remains
unverified until PILOT-001. `V21-V3-COMPATIBILITY.md` still carries its historical
"18/18 controls" execution statement about the original R4-C run; it describes that run
truthfully, and the current count lives in `LINEAGE-CONTRACT-v3.md`'s correction note.

**ASSUMPTIONS CHALLENGED:** none in `coordination/ASSUMPTIONS.md`.

**LOCAL IMPLICATIONS:** Resources' persistence path for PILOT-001 is now both usable and
honest: recording a real journey forces capture of the exact prompt/config hashes, provider
identity and timestamps for every call — precisely the evidence CpAO and later routing
decisions depend on.

**CROSS-STREAM IMPLICATIONS:** CROSS_STREAM (propose only): EVAL-035's route substrate will
need to surface the full call provenance (endpoint, hashes, timestamps) for each real call
so the writer can record it; its fake-transport tests could reuse
`benchmark-attempt-journey.yaml` / the G12 fixtures as reference shapes. Measurement
semantics remain Eval-owned and untouched.

**ARCHITECTURAL IMPLICATIONS:** ARCHITECTURAL (resolved): the v3 attempt-inheritance
mismatch is closed by the Controller's conditional override; no further topology change is
proposed.

**DECISIONS NEEDED FROM CONTROLLER:**
- **HED-1 remains open, deliberately** — unchanged from the first pass: both
  `human_required` and `human_optional` classes are representable and compute correctly;
  synthetic labels imply nothing about real pilot review time.
- None new from this correction; the `eval_item_id` question is settled by
  `CONTROLLER-PREPILOT-RETURN-REVIEW-1-2026-08-28.md`.

**EVIDENCE WORTH HUMAN INSPECTION:**
- `resources/pre-execution-freeze/fixtures/lineage/nc-G12i-production-with-eval-item-id.yaml`
  — the subtle one: a production attempt *with* a benchmark id is rejected, because a
  plausible-looking extra link is fabricated provenance.
- `resources/pilot-writer/synthetic-journey/pilot-journey-synthetic.yaml` — each attempt
  row now reads as a complete call record: who was called, at which endpoint, with which
  exact prompt/config (by hash), when, at what cost, and what happened.

**FILES CREATED / MODIFIED (this correction):**
- `resources/pre-execution-freeze/OUTCOME-PRODUCTION-TOPOLOGY-v3.yaml` (conditional
  override + G12, correction header)
- `resources/pre-execution-freeze/validators/validate_topology_v3.py` (G12, fail-closed)
- `resources/pre-execution-freeze/validators/run_lineage_controls.sh` (dynamic counts,
  multiple positives)
- `resources/pre-execution-freeze/LINEAGE-CONTRACT-v3.md` (correction note, twelfth gate)
- `resources/pre-execution-freeze/fixtures/lineage/` (17 fixtures gain required
  provenance; 9 new `nc-G12*` negatives; 1 new positive)
- `resources/pilot-writer/outcome_writer.py` (mechanical provenance enforcement)
- `resources/pilot-writer/tests/test_pilot_journey.py` (22 tests)
- `resources/pilot-writer/synthetic-journey/` (regenerated; + `benchmark-attempt-journey.yaml`)
- this brief
CpAO logic, CpAO fixtures, and all historical v2.1 material: untouched.

**RECOMMENDED NEXT STEP:** Level-1 Governor review of this branch (per the return-review
decision), alongside EVAL-035 when it returns, then the PILOT-001 freeze gate.

**EPISTEMIC CHECK:** Facts are from committed code and validator/control output;
interpretations are labeled INFERRED; the first pass's defect is stated as a defect, not
minimized; unknowns are stated, not filled; no unapproved decision is presented as fact.

**CONFIRMATION:** No unapproved next strategic step was started. USD 0 spent, 0 generations,
0 external provider calls. HED-1 not decided. CpAO semantics unchanged. The only contract
change made is the one the Controller explicitly authorised.
