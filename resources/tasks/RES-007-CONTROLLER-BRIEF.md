# Controller Brief — RES-007 (final correction pass)

**TASK:** RES-007
**STATUS:** completed — final bounded correction under
`coordination/decisions/CONTROLLER-RES-007-CORRECTION-REVIEW-2-2026-08-28.md`; returning for
Controller review (then Level-1 Governor review if accepted).

**HUMAN SUMMARY:** The pilot outcome writer is done and, after this third pass, the durable
validator now genuinely enforces every *mechanically explicit* rule the v3 attempt contract
inherits from v2.1. The history matters and is recorded honestly: the **first pass** shipped
a real contract/validator mismatch and failed to fire the task's stop condition. The
**second pass** fixed the substance (the `eval_item_id` production override and required
provenance fields) but its brief **overclaimed** — it said a validator PASS now meant full
written-contract conformance, while the validator still accepted, for example, a lane value
outside the frozen list, a "hash" of 64 letter p's, a boolean repeat counter, or a
made-up timestamp, because it checked that fields were *present*, not that their *values*
were what the contract says. **Review 2 caught exactly that gap; this pass closes it.**
The validator (and the writer, which mirrors it) now checks values: lanes against the
frozen vocabulary, the exact storage class, 0-based integer repeat counters, genuine
SHA-256 hashes, repeat/retry references that resolve to real attempts, and real ISO-8601
UTC timestamps. Thirteen new negative controls prove each rejection individually, and the
control runner now verifies each control fails for its *own* invariant, not by accident.
The `eval_item_id` decision is unchanged. No money was spent; no provider was called;
HED-1 remains untouched.

**WHAT I DID:** Extended gate G12 in `validate_topology_v3.py` with the six value-level
invariant groups Review 2 listed, mirrored the same checks in
`OutcomeWriter.record_attempt`, replaced every placeholder pseudo-hash in fixtures and
tests with genuine SHA-256 digests, added 13 negative controls (each declaring the exact
invariant it must trip via an `# EXPECT-SUBSTRING:` header the runner now verifies against
the failure message), documented the extension in the topology yaml and lineage contract,
and rebased the branch onto current `main` before returning.

**OBSERVED:**
- **Writer tests: 24/24 pass** (was 22; +1 writer-side Review-2 refusal sweep, +1 seeding
  each of the 13 violations into a written archive and proving the frozen validator
  rejects each with a G12 message naming that invariant).
- **Lineage controls: 41/41** — 2 positives (production journey with no `eval_item_id`;
  benchmark attempt with its `eval_item_id`) + 39 negatives (17 original gates G1–G11,
  9 first-correction G12 field-presence controls, 13 new Review-2 value controls:
  missing/unknown lane, wrong storage class, negative/string/boolean repeat_index,
  malformed prompt/config/reference hashes, dangling repeat/retry references, malformed
  `requested_at`, malformed non-null `completed_at`).
- **CpAO controls: 13/13 unchanged; no regression** — the synthetic journey still
  recomputes exactly the hand-computed fully-loaded **42.00 XTS**, shared ledger entry
  counted once, `human_optional` visibly excluded. The full RES-004 check bundle passes.
- **All positive fixtures and journeys now carry genuine SHA-256 values** (hashlib
  hexdigest of named synthetic inputs) — no placeholder pseudo-hashes remain in any
  positive case, including the two hand-typed hex constants the second pass introduced.
- Conventions preserved, not invented: hashes are 64 **lowercase** hex (the project's
  hexdigest convention — uppercase hex is refused, proven by test); timestamps are
  ISO-8601 UTC `...Z` (or explicit `+00:00`); `completed_at: null` remains valid exactly
  for a call that never completed (the journey's timeout attempt exercises this);
  `reference_asset_hashes: []` remains valid; booleans do not count as integers for
  `repeat_index`.
- All previously verified behaviour re-verified after the extension and rebase: one call =
  one attempt = one trial; local/human steps create no fake attempts; binary artifact
  hashing/byte counts; ordered multi-parent lineage; failed/refused/timed-out attempts
  kept individually; immutable cost references; repair representation; acceptance only at
  outcome level; deterministic output. Historical v2.1 archives untouched (G12 applies to
  `schema_era: v3` only).

**INFERRED:** For the attempt entity, a validator PASS and the *mechanically explicit*
written v2.1/v3 provenance invariants are now aligned: every field-presence and
field-value rule that the contract states in checkable form is enforced on the durable
archive independently of the writer. This claim is deliberately narrower than the second
pass's — see the next section for what it excludes.

**Intentionally outside mechanical validation (unchanged by design, per the bounded
authority):** whether a `provider`/`model_id`/`endpoint` actually exists or is spelled
canonically; URL/URI semantics of `endpoint`, `config_location`, `output_location`;
whether a recorded hash matches bytes the archive does not hold (prompt/config text is
recoverable via `config_location`, not stored); repeat/retry *policy* (when a repeat or
retry was strategically justified — only structural provenance is checked);
`transform_recipe.params_hash` and artifact `output_hash` formats (owned by gates G8/G6 as
originally written, not part of the Review-2 attempt scope); and all measurement
semantics (Eval-owned). These are recorded so no future brief mistakes "validator PASS"
for proof of them.

**SURPRISES / BELIEF UPDATES:** none new; Review 2 confirmed the first-pass lesson —
"enforced" means value-checked, not merely present.

**FAILURES / BLOCKERS:** none in this pass. The prior history (first-pass stop-condition
defect; second-pass overclaim; the shared-checkout workspace incident, since resolved by
isolated worktrees) stands recorded above and in the decision records.

**UNKNOWN / NOT VERIFIED:** real provider payload shapes remain unverified until
PILOT-001; the writer and validator now fail closed on anything outside the contract, so
the expected failure mode is a loud refusal, not silent acceptance.

**ASSUMPTIONS CHALLENGED:** none in `coordination/ASSUMPTIONS.md`.

**LOCAL IMPLICATIONS:** Recording a real pilot journey now forces genuine call identity —
real hashes, real timestamps, frozen lane values — at write time *and* at validation time,
so PILOT-001's archive will be verifiable evidence even if the writer is bypassed.

**CROSS-STREAM IMPLICATIONS:** CROSS_STREAM (propose only): EVAL-035's route substrate
must surface per-call `lane`, prompt/config hashes and UTC timestamps in exactly these
formats for the writer to record; the G12 fixtures are reference shapes.

**ARCHITECTURAL IMPLICATIONS:** none new; the conditional override from Review 1 is
unchanged and this pass adds no topology concepts.

**DECISIONS NEEDED FROM CONTROLLER:** none new. **The `eval_item_id` decision is not
reopened or changed** — production attempts carry none (fabrication refused), benchmark
attempts require it. HED-1 remains open, deliberately.

**EVIDENCE WORTH HUMAN INSPECTION:**
- `resources/pre-execution-freeze/fixtures/lineage/nc-G12p-malformed-prompt-hash.yaml` —
  the emblematic Review-2 case: 64 p's is non-empty, looks hash-length, and is now
  refused; before this pass it validated.
- The `41/41` runner output — each G12 rejection now names the exact invariant it tripped.

**FILES CREATED / MODIFIED (this pass):**
- `resources/pre-execution-freeze/validators/validate_topology_v3.py` (G12 value checks)
- `resources/pilot-writer/outcome_writer.py` (mirrored value checks)
- `resources/pre-execution-freeze/validators/run_lineage_controls.sh` (EXPECT-SUBSTRING
  verification)
- `resources/pre-execution-freeze/fixtures/lineage/` (13 new `nc-G12j…v`; genuine SHA-256
  values everywhere; invariant headers on all G12 controls)
- `resources/pre-execution-freeze/OUTCOME-PRODUCTION-TOPOLOGY-v3.yaml`,
  `LINEAGE-CONTRACT-v3.md` (Review-2 extension documented, counts corrected)
- `resources/pilot-writer/tests/test_pilot_journey.py` (24 tests)
- `resources/pilot-writer/synthetic-journey/` (regenerated, all-genuine hashes)
- this brief
CpAO logic and fixtures, historical v2.1 material: untouched.

**RECOMMENDED NEXT STEP:** Controller review of this branch; if accepted, Level-1 Governor
review, then the PILOT-001 freeze gate alongside EVAL-035.

**EPISTEMIC CHECK:** Facts are from committed code and control-suite output; the
conformance claim is explicitly scoped to mechanically explicit invariants with the
exclusions listed; prior defects are described as defects; unknowns are stated, not
filled; no unapproved decision is presented as fact.

**CONFIRMATION:** No unapproved next strategic step was started. USD 0 spent, 0 provider
calls, 0 generations. HED-1 not decided. CpAO semantics unchanged. Only the
Controller-authorised Review-2 extension was made.
