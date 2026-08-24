# Controller Brief — EVAL-002

**COMMUNICATION STANDARD:** `shared/COMMUNICATION-STANDARD.md` applies. Terms and numbers are
explained where they carry a decision.

**TASK:** EVAL-002 — Calibration & benchmark readiness
**STATUS:** **completed and Controller-approved — CLOSED, 24 Aug 2026.**

Three post-approval corrections were applied (see *Correction pass* below and findings §8), followed
by a documentation-only closure pass:

- **Identity rubric frozen at V0** — fixed so it can be tested. **Not validated, not calibrated,
  never used on real media.** The two-question structure (reference fidelity *and* cross-output
  consistency, both required) is part of what is frozen.
- **M1b item structure approved as V0 design** — **not populated, not linguistically validated, not
  ready to score models.** Zero items exist.
- **EVAL-001 findings §1.2 corrected**, dated, with the original wording retained in place and
  marked superseded: our bounded search did not identify a suitable public generative-Devanagari
  benchmark; it did not establish that none exists.

No battery, ladder, threshold, observation-unit or Registry change in any of the above.

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

**The correction pass then found a second, worse hole — in the rubric.** As first written it asked
only whether a person's features stayed *consistent across the generated images*, never whether they
matched the **reference** at all. A generator that ignored the reference and produced a completely
different person — consistently — would have **passed**. That is not an exotic case; it is what
"the reference isn't taking effect" looks like. Fixed: every feature is now judged on two separate
questions, and both must hold.

**What still blocks a real calibration** is unchanged and is not something this task could touch:
no Hindi-reader time budgeted, no test material, no identity reference sets, no model roster.

---

## Correction pass — 24 Aug 2026

Applied after substantive approval. Full detail in findings §8.

**1 · Identity rubric: reference fidelity made explicit.** Each declared identity feature is now
judged on two independent questions — **does it match the reference**, and **is it consistent across
the generated set** — and both must hold. Previously only the second was asked, so **a consistently
wrong person would have passed**. The two are recorded separately because they imply different
responses: *right person drifting* is identity drift, while *the same wrong person throughout* means
reference conditioning is not taking effect at all. An item reviewed without its reference set is now
`not_reviewable` rather than half-judged. **The approved D3 dimension is unchanged** — it already
defines the property against a reference set; the rubric now operationalises that.

**2 · Negative controls verified per fixture.** `--negative` previously passed when any error was
raised anywhere in the run. With two or more negative fixtures that is unsound: one fixture's errors
cover for another that was silently accepted. It now requires **every** fixture to be individually
rejected, with the specific error codes it declares. A second negative fixture makes the multi-fixture
case real, and a new `--selftest` pins the behaviour with four cases — including the exact bug, and
including an empty suite, which previously read as success.

**3 · M1b overclaim corrected.** "No such public benchmark exists" / "nothing public contains this"
became the supported claim: **no suitable public generative-Devanagari benchmark has been identified
in our search so far, therefore our V0 item set still needs to be built.** The practical conclusion
is unchanged; what changes is that the question is now marked as one to revisit if Resources surfaces
a suitable set under RES-002, rather than treated as closed.

**4 · Flagged, not fixed.** The same categorical phrasing survives in the closed, approved EVAL-001
findings §1.2. **I did not edit it** — amending an approved artifact to match a later correction is
a Controller decision. Findings §8.4.

**Unchanged by this pass:** the seven dimensions, their ladders, pass criteria and observation units;
the calibration thresholds and bounds; the Registry architecture.

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
5. **The guards fire, per fixture.** Both negative controls were individually rejected with the
   error codes each declares — `fx-04` with `BAD_OBSERVATION_UNIT` and `GENERATION_DOUBLE_COUNTED`,
   `fx-05` with `BAD_INSTRUMENT_STATE` — each with a non-zero exit. `--selftest` passes 4/4,
   including the case where one fixture is rejected and another silently accepted, which the
   pre-correction aggregate check would have passed.
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

1. **Review the identity rubric**, in particular the corrected two-question structure (reference
   fidelity and cross-output consistency judged separately, both required). Freezing it is a
   Controller decision and it cannot be used until frozen.
2. **Review the Hindi item design**, particularly the coverage categories and the explicit statement
   that the set is a collection of stress cases rather than anything representative of Hindi.
3. **The Resources clearance decision on M1a** remains the gating question for Hindi work — it
   determines both how much must be built and the native-reader hours. **RES-002 is now open on
   Devanagari acquisition**; if it surfaces a suitable public generative-Devanagari set, the M1b
   design says to revisit before items are built.
4. ~~Whether to amend the closed EVAL-001 findings~~ — **RESOLVED 24 Aug 2026: amend.** Applied as
   a dated Controller correction in §1.2, with the original wording retained and marked superseded
   so the reasoning trail stays intact.
5. **Nothing else has changed.** The model roster, the human-time budget (≈ 11–15.5 hours, 2–4 of
   them a Hindi first-language reader) and the Registry cross-stream fields remain unapproved.

## EVIDENCE WORTH HUMAN INSPECTION

- `eval/findings/EVAL-002-readiness-findings.md` **§8.1** — the rubric hole: why a consistently
  wrong person would have passed, and the two-question fix. The most consequential correction.
- `eval/findings/EVAL-002-readiness-findings.md` **§2** — the two defects the negative control found,
  and why the second one matters more than it looks.
- `eval/harness/README.md` — the explicit list of what the harness does and does not prove. Worth
  reading before anyone is tempted to treat a harness output as a result.

## FILES CREATED / MODIFIED

Modified: `eval/scripts/check-vlm.mjs` (portability; judgement unchanged and verified).
Created: `eval/harness/` (README, runner, five fixtures with expected results, two of them negative
controls, plus a `--selftest` regression suite), `eval/rubrics/IDENTITY-CONSISTENCY-RUBRIC-V0-DRAFT.md`,
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
specialist time, no model roster selection, no battery change, no Registry schema promotion. The
correction pass changed no dimension, ladder, threshold or architecture.
**EVAL-003 not started, and will not be started until Controller review after Resources returns
relevant material.**
