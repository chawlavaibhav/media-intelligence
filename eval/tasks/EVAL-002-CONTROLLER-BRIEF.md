# Controller Brief — EVAL-002

**COMMUNICATION STANDARD:** `shared/COMMUNICATION-STANDARD.md` applies. Terms and numbers are
explained where they carry a decision.

**TASK:** EVAL-002 — Calibration & benchmark readiness
**STATUS:** completed — awaiting Controller review

---

## What this task was for

EVAL-001 decided *what* we will measure and *how a checker must earn trust* before we believe it.
But several practical things did not exist yet: the one working evaluation script could only run on
one machine, nothing proved a test item could actually flow through evaluation and come out as a
usable result, there was no written standard for judging whether a generated person stays the same,
and there was no design for the Hindi test prompts.

This task built that plumbing. It ran nothing real: **zero generations, zero network calls, ₹0,
no calibration, no human specialist time, no model roster, no change to the approved battery.**

---

## HUMAN SUMMARY

Three of the four things blocking a first real calibration are now cleared.

**The checker script runs anywhere now** — and, more importantly, I proved the repair did not change
what it judges. Rather than asserting that from the diff, I re-ran the new scoring code over all 27
transcriptions already stored from the original study and confirmed every verdict reproduced exactly
(0 mismatches). That matters because a "portability fix" that silently altered judgement would make
every future result incomparable with the study we already rely on.

**A test item can now be traced end to end through evaluation**, using entirely fabricated data. The
harness demonstrates the counting rules the approved design depends on — that two attempts at one
prompt are not two independent tests, that six frames of one clip are one observation not six, and
that one image scored on two different dimensions is not two independent trials.

**The most useful thing that happened was a failure.** I added a deliberately-broken fixture,
because a check that never fails proves nothing. It exposed two real defects in my own tooling: the
run reported success despite raising integrity errors, and — worse — a run the harness had just
rejected still produced a pass rate marked as eligible for the Registry. That is exactly the
"false confidence attached to bad data" pattern this whole stream exists to prevent, reproduced in
our own code. Both are fixed; a run that fails its integrity checks now quarantines every result in
it and exits non-zero.

**Two documents are drafts, not standards.** The identity review rubric and the Hindi item design
are written and reviewable, but nothing has been calibrated, frozen or populated.

**What still blocks a real calibration** is unchanged and is not something this task could touch:
no Hindi-reader time budgeted, no test material, no identity reference sets, no model roster.

---

## OBSERVED

*Directly run and verified on this machine.*

1. **The script's judgement is unchanged.** The exported scoring function, applied offline to all 27
   stored transcriptions in `eval/runs/finding-01-devanagari-check/`, reproduced every `normalized`,
   `exact_match` and `edit_distance` value: **27 re-scored, 0 mismatches.**
2. **The script is portable.** `--help` and `--dry-run` both run with no API key set and no
   hard-coded path; `--dry-run` correctly enumerated all 14 sample images from an explicit
   `--input` directory and made no network call.
3. **The harness runs and its assertions hold.** All three positive fixtures pass and match their
   stored expected results (`--all --check`, exit 0).
4. **The counting rules hold on fixtures.** One generation scored on two dimensions produced
   2 dimension-results from **1 distinct generation**, explicitly reported as not 2 independent
   trials. A 6-frame clip produced `frames_sampled: 6, observations: 1`. Two attempts at one prompt
   produced `n_items: 1, n_trials: 2`.
5. **The guards fire.** The negative-control fixture was rejected with two error-severity checks
   (`GENERATION_DOUBLE_COUNTED`, `BAD_OBSERVATION_UNIT`) and a non-zero exit.
6. **Two defects existed in the harness and were found by running the negative control:** success
   exit code despite integrity errors, and a Registry-eligible pass rate produced by a rejected run.
7. **No network primitive exists in `run-fixture.mjs`.** The only `fetch` in the repository is in the
   checker's real-run path, which was never taken.

## INFERRED

*Interpretation, not observation.*

Negative controls should be standard for future evaluation tooling. Neither harness defect was
visible from reading the code — both appeared only when something was deliberately broken. A test
suite that only ever confirms correct behaviour cannot distinguish "the guards work" from "the
guards are absent."

The harness's ability to represent all seven approved dimensions without strain is weak evidence
that the EVAL-001 design is implementable. It is not evidence that the design is *right*.

## SURPRISES / BELIEF UPDATES

- **Our own tooling reproduced the exact failure mode the stream exists to prevent** — attaching a
  confident-looking result to data that had already been flagged as invalid. Worth remembering: the
  discipline has to be enforced mechanically, not just documented.
- **The offline re-scoring check turned out to be far stronger evidence than a code diff**, because
  it exercises the real Unicode normalisation path on real recorded data. Cheap, and worth repeating
  any time evaluation code is touched.

## FAILURES / BLOCKERS

No stop condition fired. The two harness defects were implementation bugs in code written during
this task, **not** contradictions in the approved design.

## UNKNOWN / NOT VERIFIED

- **Whether the harness's local result shape survives the real Registry format.** The Registry schema
  is still a proposal with deferred cross-stream fields; the harness format is deliberately
  reversible and is stated as implementation-scoped in its README.
- **Whether the identity rubric produces agreement between two reviewers.** It has never been used.
  That is a calibration question, and calibration was out of scope.
- **Whether sourced Hindi text can fill the coverage categories**, or whether items must be
  constructed — which would increase native-reader time.
- **Whether one target string per run is sufficient** once items have individual targets. Flagged in
  findings §1, deliberately not fixed here.
- **Everything about actual model capability.** Nothing was generated or measured.

## ASSUMPTIONS CHALLENGED

None. No experiment was run and no register entry is affected.

## LOCAL IMPLICATIONS

The stream now has runnable plumbing. Three of the four practical prerequisites for a first
calibration are cleared; the fourth (material and human time) is outside this task's authority.

## CROSS-STREAM IMPLICATIONS

**None new.** The three raised in EVAL-001 stand and remain unfiled pending Controller direction.
Explicitly **not** done here: the proposed Registry schema was not promoted, and no cross-stream
schema decision was made or needed.

## ARCHITECTURAL IMPLICATIONS

None. Every approved dimension, ladder, pass criterion and observation unit was representable
without change.

---

## DECISIONS NEEDED FROM CONTROLLER

1. **Review the identity rubric.** Freezing it is a Controller decision. It cannot be used until
   frozen, and it should not be frozen without someone judging whether its per-feature approach is
   what you want reviewers held to.
2. **Review the Hindi item design**, particularly the coverage categories and the explicit statement
   that the set is a collection of stress cases rather than anything representative of Hindi.
3. **The Resources clearance decision on M1a** remains the gating question for Hindi work — it
   determines both how much must be built and the native-reader hours.
4. **Nothing else has changed.** The model roster, the human-time budget (≈ 11–15.5 hours, 2–4 of
   them a Hindi first-language reader) and the Registry cross-stream fields remain unapproved.

## EVIDENCE WORTH HUMAN INSPECTION

- `eval/findings/EVAL-002-readiness-findings.md` **§2** — the two defects the negative control found,
  and why the second one matters more than it looks.
- `eval/harness/README.md` — the explicit list of what the harness does and does not prove. Worth
  reading before anyone is tempted to treat a harness output as a result.

## FILES CREATED / MODIFIED

Modified: `eval/scripts/check-vlm.mjs` (portability; judgement unchanged and verified).
Created: `eval/harness/` (README, runner, four fixtures with expected results, one of them a
negative control), `eval/rubrics/IDENTITY-CONSISTENCY-RUBRIC-V0-DRAFT.md`,
`eval/battery/M1B-DEVANAGARI-GENERATION-ITEM-DESIGN-V0.md`,
`eval/findings/EVAL-002-readiness-findings.md`, this brief.

**No approved EVAL-001 artifact was altered.** No historical finding or result file was altered.
Generated harness output is git-ignored so mock results cannot become committed evidence.

## RECOMMENDED NEXT STEP

*A recommendation, not an action taken.*

Review the two drafts, then get the Resources clearance decision, since it gates both the Hindi
material and the hours. Calibration should still come before any capability run — a score from an
uncalibrated checker is not a weak measurement, it is a false one.

## EPISTEMIC CHECK

Every claim above was produced by a command run on this machine and is reproducible from the
repository. Fabricated data is labelled fabricated in every file that contains it. The two drafts are
marked as drafts and were not used to produce any number. No result here is evidence about any
model, and nothing was promoted from proposal to decision.

## CONFIRMATION

No unapproved step was started. No generation, no network call, no spend, no calibration, no human
specialist time, no model roster selection, no battery change, no Registry schema promotion.
**EVAL-003 not started.**
