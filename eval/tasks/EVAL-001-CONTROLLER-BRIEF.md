# Controller Brief — EVAL-001

**COMMUNICATION STANDARD:** `shared/COMMUNICATION-STANDARD.md` applies. Terms and numbers are
explained where they carry a decision; internal names are given with their plain-English meaning.

**TASK:** EVAL-001 — Capability Lab V0 battery design
**STATUS:** **completed — Controller-approved, 24 Aug 2026.** EVAL-001 is closed.

**Approved:** the V0 battery specification (what we will measure and how), its seven dimensions, and
the calibration specification (how each checker must be proven trustworthy before we believe it).
**Still unapproved / deferred:** the model roster, the human-time budget (≈ 11–15.5 hours), and the
Registry's cross-stream field proposals. **No benchmark run is authorised by this document.**
Revision history: findings §10.

---

## What this task was, in one paragraph

Before we can ever say "model X is good at Hindi text", we need three things: a **test**, a
**checker** that judges the output, and **proof the checker itself is trustworthy**. This task built
the first two and specified the third. It ran nothing. The deliverable is a measuring kit, not a
measurement.

---

## HUMAN SUMMARY

Two corrections in the final revision changed what this battery can honestly claim.

**First: counting and positioning became separate tests.** A model can place a cup correctly beside
a laptop and still draw two laptops — different skills that fail independently. They also need
different sensitivity settings on the same object-detection software (high when counting, so shadows
are not counted as objects; lower when locating). One merged test could only record one setting, so
it would have misdescribed half of what it did.

**Second, and more consequential: my calibration thresholds were written as if they were error
rates, and at these sample sizes they are not.** A checker can only be caught out on an item that is
genuinely broken. A 30-item set that is half broken therefore gives about **15 chances**, not 30.
Scoring zero mistakes on 15 chances is statistically consistent with a checker that is truly wrong
**up to about 18% of the time**. For the identity test, with about 10 chances, up to **26%** — and
the ≤5% target I had set was not even measurable there, because with 10 chances the smallest error
rate observable is 1-in-10. That target is withdrawn. The thresholds remain useful as admission
hurdles and are now labelled as such, with their real uncertainty published.

**Practical consequence:** the first Registry will be able to say *"this checker passed our
screening"*. It will **not** be able to say *"this checker is accurate to within X%"*.

I also closed an open question about a public benchmark whose "Multilingualism" category might have
contradicted our Hindi claim. It did not — see OBSERVED 1.

**Nothing runs** until the model roster and the ≈11–15.5 hours of human time are decided.

---

## WHAT I DID

Reviewed eight published benchmark methodologies and one vendor pricing page; audited this
repository's own evidence against the underlying data files; drafted and then revised the battery
specification, Registry schema and calibration plan through three Controller reviews. Zero
generations, zero paid API calls, ₹0 spent, no dataset acquired, no historical file altered.

---

## OBSERVED

*Directly seen or supported by a named source. Sources tabulated in findings §7; repository evidence
in findings §5.*

**1. A public benchmark's "Multilingualism" category is Chinese, not multi-script.** Checked against
the released dataset rather than the paper's prose. Exactly two versions are published: English
(1,120 rows, **no Multilingualism category at all**) and Chinese (1,320 rows, including 200
Multilingualism rows). Six sampled Multilingualism rows are Chinese prompts about Chinese public
figures. **No Devanagari, no Indic script.** The structural evidence is decisive — only two versions
exist, so there is no third alphabet anywhere. The content evidence is a 6-of-200 sample and is not
extrapolated.

**2. Small-sample arithmetic.** When a test produces zero failures in *n* opportunities, the
standard way to express the residual uncertainty is a **95% upper bound** — the highest true failure
rate that could still plausibly produce a clean sweep. Formula: `1 − 0.05^(1/n)`. In practice:
15 opportunities → **~18%**; 10 opportunities → **~26%**. Put concretely, a checker that genuinely
misses one broken item in ten has roughly a **1-in-5 chance** of scoring perfectly on 15. Supporting
a real "under 5%" claim needs **59** opportunities; "under 1%" needs about **299**.

**3. Counting and positioning use different detector settings.** The published method (GenEval) uses
a high confidence threshold for counting and a lower one elsewhere; a second benchmark
(T2I-CompBench++) likewise treats numeracy and spatial relationships as separate categories.

**4. Hindi: reading benchmarks exist and are numerous; drawing benchmarks do not.** Public
benchmarks for recognising Devanagari in a photo are plentiful. Public benchmarks for *generating*
Devanagari do not cover it — the generative text-rendering benchmarks are English and Chinese.
(Findings §1.1–§1.2.)

**5. Six provenance problems in our own material** stand unchanged and are itemised in findings §5 —
including that the Hindi ground-truth labels were never confirmed by a first-language reader, and
that the one working script in this repository points at a folder path that does not exist.

---

## INFERRED

*Reasoned interpretation of the above, not directly observed.*

Counting and positioning must produce separate Registry results even though they share detection
software, because a single result could not carry one honest record of the settings used.

V0-sized calibration can **qualify** a checker but cannot **characterise** its error rate. That is
not a flaw to be fixed by wording — it is a property of the sample size, and it caps what the first
Registry can claim.

Whether an object is being *held* is not decidable from the boxes that detection software draws.
Boxes can overlap without contact, so contact relationships stay untested rather than being
approximated.

---

## SURPRISES / BELIEF UPDATES

**My thresholds were dressed as error rates and were not.** This is the correction most likely to
have caused real harm: on the earlier wording, a future Registry could have been described as
low-error on evidence permitting an 18–26% true failure rate.

**My own findings contradicted my own battery.** The findings document already said counting and
positioning were separate capabilities while the battery specification still merged them. Controller
review caught it; I had not.

**"Multilingualism" did not mean what it sounds like.** Downloading the released files settled in
minutes a question the paper's prose left ambiguous. Worth remembering as a method: read the
artifact, not the description of the artifact.

---

## FAILURES / BLOCKERS

None blocked EVAL-001 itself. Four block an actual *run*: no first-language ground truth for the
Hindi checker; no frozen rubric or reference images for the identity checker; ≈11–15.5 hours of
human calibration time unbudgeted; and the one working script not runnable as committed.

---

## UNKNOWN / NOT VERIFIED

*Gaps that remain. None is filled by assumption.*

- **Whether Resources will clear the reusable Hindi material.** This is no longer a licence question
  — under current policy, a missing licence alone does not block public, ungated material used only
  internally. What is unknown is the clearance decision itself. **Eval performs no rights
  assessment.**
- **The checkers' true error rates.** V0 bounds them only loosely (~18% text, ~26% identity).
  Narrowing them is a sample-size decision, not something to assume away.
- **Whether checker rankings measured on scanned documents transfer to generated images.** These are
  different regimes: generated text is often clean-looking but semantically wrong.
- **Whether conventional text-recognition software genuinely fails on Devanagari.** Our 0/14 record
  has no supporting file, and published data on a comparable engine makes the blanket claim
  doubtful. Should be re-tested, not written off.
- Hindi ground-truth labels; checker repeat-run consistency; the exact price of one model variant.
- **Whether these seven dimensions are the right seven.** They are the traceable, affordable ones.
  Coverage is not claimed.

---

## ASSUMPTIONS CHALLENGED

None promoted or demoted — no experiment was run. Three register entries are *informed*
(findings §8): entry 12 on cost-per-accepted-outcome gains external support for its shape and
confirmation of its stated weakness; entry 4 on book-knowledge-to-failure links gains a second
instance of the observation-unit channel; entry 15 on Canon-informed routing stays blocked and
remains untestable after this battery, which measures only hard-fidelity properties.

---

## LOCAL IMPLICATIONS

Seven dimensions after the split: Hindi exact text, Latin exact text (the control), person identity
across separately generated images, object count, spatial relationship, on-screen text stability
within a clip, and operational behaviour (cost, speed, reliability).

Run size for image models rises from 12 test cells to 15 — **360 attempts per model** at 12 items ×
2 repeats. Video is unchanged at 144.

Counting and positioning are restricted to generic objects the detection software actually knows
(its 80 standard categories). **Brand marks and contact relationships are deferred** and recorded as
*"matters, but we have no trustworthy way to measure it"* — a deliberate, visible state, so that a
gap is never mistaken for a decision that it did not matter.

---

## CROSS-STREAM IMPLICATIONS

*Proposed, not acted on. Nothing filed pending Controller direction.*

- **→ Canon.** The Creative IR specification has not settled how its own fields are referenced, so
  the battery cannot cite them mechanically. Nine naming mismatches are tabulated in battery §7.2,
  including one substantive error where on-screen Hindi was justified against the wrong field.
- **→ Empirical Memory / Planner.** Four proposed Registry fields would change how routing and
  memory read the table. Marked as cross-stream proposals; **deferred by Controller direction**, not
  assumed.
- **→ Resources.** Material requirements in battery §9. The clearance decision on the reusable Hindi
  material is the gating question — it determines how much we must build and which end of the
  11–15.5 hour range applies.

## ARCHITECTURAL IMPLICATIONS

None requiring a stop. Every gap found was representable as a proposed field rather than an
inability of the architecture to hold the evidence.

---

## DECISIONS NEEDED FROM CONTROLLER

1. **Which models to test.** The costing in battery §8.3 is a worked example only and cannot be
   finalised without a roster.
2. **The human calibration budget: ≈ 11–15.5 hours**, of which **2–4 must be a Hindi first-language
   reader**. This is one-off setup, not per-run, and it gates every Hindi Registry entry.
3. **Ownership of the Hindi material.** Two separate asks: request that Resources *clear* the
   published recognition material for internal use, and assign an owner for the test-item set that
   must be built.
4. **Whether to buy narrower error bounds.** Moving from "passed our screening" to a genuine
   "under 5%" claim needs about 59 opportunities per checker — roughly six times the identity sample
   and proportionally more annotator time. **Recommend not for V0**, but it is the ceiling on what
   the first Registry can say, so it should be a conscious choice.
5. **Which cross-stream items to formalise**, given the Registry field proposals are deferred.

---

## EVIDENCE WORTH HUMAN INSPECTION

- `battery/INSTRUMENT-CALIBRATION-PLAN-V0.md` **§2b** — what a small calibration can and cannot
  establish, with the bound table. The section most likely to prevent a future over-claim.
- `findings/EVAL-001-battery-design-findings.md` **§1.2** — how the benchmark question was settled
  from the released files, and the line drawn between what that proves and what it samples.

## FILES CREATED / MODIFIED

All under `eval/`: the battery specification, the Registry schema, the calibration plan, the
findings, this brief, and `HANDOFF.md`. Per-revision section lists are in findings §10. **No
historical finding, script or result file has been altered at any point.**

---

## RECOMMENDED NEXT STEP

*A recommendation, not an action taken.*

Get the clearance decision on the reusable Hindi material first — it sets both the human-hour figure
and how much we must build ourselves. Then open a separate task to assemble the test items and
calibrate the two text checkers, **before** any capability run. Calibration is a gate that precedes
measurement: a score produced by an uncalibrated checker is not a weak measurement, it is a false
one.

## EPISTEMIC CHECK

Every figure here is read from a named published source, a released dataset, or a file in this
repository, traceable via findings §7 or §5. Interpretations are confined to INFERRED, unknowns are
listed rather than filled, and nothing is presented as approved beyond what the Controller approved.

Across revisions: the over-broad "no Devanagari benchmark" claim was withdrawn and marked as
withdrawn in place rather than deleted; the cost ratio was demoted from a finding to an illustrative
scenario with its assumptions named; all figures from one video benchmark are pinned to its single
published version; calibration thresholds were relabelled as qualification gates with their bounds
published, and the unmeasurable ≤5% identity target withdrawn rather than quietly retained; and
external material reuse is conditioned on a Resources clearance decision, with no rights assessment
performed by Eval.

## CONFIRMATION

No unapproved next strategic step was started. No model benchmarked, no generation call made, no
money spent, no dataset acquired. EVAL-002 not started.
