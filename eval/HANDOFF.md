# Eval / Capability Lab — Handoff

**COMMUNICATION STANDARD:** `shared/COMMUNICATION-STANDARD.md` applies. Explain ideas, not just
labels: what a thing is, why it matters, what the numbers mean in practice, what changes, and what
is still uncertain. Do not assume the reader remembers terminology from another document.

---

## PURPOSE — what this stream is for

Decide **what to measure** about image, video and audio generators, **how to measure it**, and then
**measure it**. The output is the **Capability Registry**: a table of what today's models can
actually do, measured rather than assumed — for example, "this model rendered a four-word Hindi
headline correctly 3 times in 20 attempts, judged by this checker, at this cost."

The Registry exists so that later, when a customer job arrives, the system can pick a model based on
measured ability rather than on marketing claims or guesswork.

---

## CURRENT STATE

### The one measurement we have, and why it is not settled

`findings/FINDINGS-01-can-we-check.md` recorded a **checker-calibration study**. *Calibration* here
means: test the checker, not the generator. You hold the images fixed, you already know which are
right and which are wrong, and you see whether the checker agrees. It answers "can we trust this
judge?" — not "is this model any good?"

The study gave 14 images of Hindi (Devanagari) text to three checkers:

| Checker | Result |
|---|---|
| `qwen3-vl-235b` (an AI vision model) | 14 out of 14 correct verdicts |
| `claude-sonnet-4.5` (an AI vision model) | **6 false passes** — called six visibly misspelled signs correct |
| Tesseract (conventional text-recognition software) | reported as 0 out of 14 |

A **false pass** is the dangerous error: the checker looks at broken work and says it is fine, so
the pipeline ships a defect *with a passing grade attached*.

⚠️ **Treat this study as preliminary, not settled.** The finding states its own limits and none has
been resolved:

- **The right answers were never confirmed by a Hindi first-language reader.** The people who
  decided which images were misspelled did not have Hindi as a first language.
- **The sample is smaller than it looks.** 14 images, but only **4 independent sources** — 12 of
  them are frames pulled from 4 short clips, so they are near-copies of each other, not 12
  independent tests.
- **Each image was checked once**, so we do not know whether a checker gives the same answer twice.
- **No file in this repository supports the Tesseract result**, so that number cannot currently be
  reproduced.

Detail: `findings/EVAL-001-battery-design-findings.md` §5.

### EVAL-001 — closed and Controller-approved, 24 Aug 2026

EVAL-001 designed the **battery**: the standard test set we will run against models. Approved are
the battery specification and the calibration specification (how we will prove each checker
trustworthy before we believe it).

**The seven things V0 will measure** — plain-English meaning, then the internal name:

| What it measures | Internal name |
|---|---|
| Does the model draw Hindi (Devanagari) text exactly as specified? | `exact_text_devanagari` |
| Same, in the Latin alphabet — the control, so we can tell "bad at text" from "bad at Hindi" | `exact_text_latin` |
| Does a person's face and wardrobe stay the same across separately generated images? | `person_identity_across_prompts` |
| Does the right *number* of objects appear? | `object_count` |
| Are objects in the right *positions* relative to each other? | `spatial_relationship` |
| Does on-screen text stay the *same* for the whole length of a clip, rather than mutating? | `text_stability_across_frames` |
| Cost, speed, error rate, refusal rate, repeatability | `operational_behaviour` |

"V0" means the first, deliberately narrow version.

### Approved does not mean runnable

Three things are still **unapproved** and each independently blocks a run:

1. **The model roster** — nobody has decided which models we test.
2. **The human time** — roughly **11 to 15.5 hours** of one-off setup, of which **2 to 4 hours must
   be a Hindi first-language reader**. Not budgeted anywhere.
3. **The Registry's cross-stream fields** — proposed additions that would change how the routing
   system reads the table. The Controller has deferred these.

No Capability Registry exists. No model has been benchmarked. **No checker has been calibrated**, so
we currently have no instrument we are entitled to trust.

---

## CURRENT APPROVED DECISIONS

1. **Hard-fidelity and creative-quality checks are separate instruments and must not be merged.**
   "Is the headline spelled correctly" has a right answer; "is this ad any good" does not. One
   evaluator cannot honestly do both.
2. **A checker must be tested against human judgement on the specific task before it is trusted.**
   This is the direct lesson of the study above: an untested checker is worse than none, because it
   attaches false confidence to broken work.
3. **Every capability number must name the checker that produced it and the conditions it ran
   under.** A pass rate is a joint statement about the model *and* the checker; change the checker
   and the number changes without the model changing.

---

## LAST COMPLETED TASK

**EVAL-001 — Capability Battery V0 design.** Completed and Controller-approved 24 Aug 2026.
Full record: `tasks/EVAL-001-CONTROLLER-BRIEF.md`.

## CURRENT TASK / QUEUE

**None.** EVAL-002 has not been opened and must not be started without an approved task file.

---

## IMPORTANT OBSERVATIONS — things the next session should not have to rediscover

**A capability number without its checker is not a measurement.** Covered above; it is the founding
result of this stream.

**A checker has two different accuracies, and they must be stored separately.**
- *Gate* accuracy — does it correctly say pass or fail? This is what routing needs.
- *Diagnosis* accuracy — does it correctly say *what* broke? This is what repair needs.

Qwen's "14 out of 14" is a **gate** score. The same finding records that it caught one misspelling
and silently corrected another — so its diagnosis was incomplete. **Never cite a bare "14/14" as
general accuracy.**

**Some defects are invisible unless you look at the right unit.** A misspelling that *changes*
partway through a clip does not exist in any single frame — it only exists *between* frames. Look at
one frame and you cannot see it, however good your checker is. Every test therefore declares its
**observation unit** (frame, shot, pair of shots, sequence, whole asset, or a set of assets over
time). That vocabulary already exists in `canon/knowledge/SPEC-04-operational-bindings.md` and must
be adopted, not reinvented.

**Frames from one clip are one test, not many.** Near-identical samples inflate apparent confidence.
Always report the number of *independent items* alongside the number of attempts.

**Hindi text: reading benchmarks exist; drawing benchmarks do not.** There are many public
benchmarks for *reading* Devanagari out of a photo (text recognition). As far as the EVAL-001 review
could establish on 24 Aug 2026, there is **no public benchmark measuring whether a generative model
correctly draws Devanagari it was told to produce**. Reading and drawing are different capabilities.
**Do not cite a text-recognition benchmark as evidence about a generator.**

Those recognition datasets are still useful — for calibrating our *reading* checker, not for scoring
generators. Using them is conditional on Resources clearing the material for bounded internal
evaluation under the current Resources policy.

**A calibration set of clean, tidy Hindi renders would be useless.** In one published study all ten
systems tested scored within a narrow band on clean text (chrF++ 91–98 — chrF++ is a
character-overlap score where higher is better). If every candidate looks equally good, the test has
not separated anything. **Any calibration set must include degraded and real-world material**, where
the same study found nine of ten systems collapsing.

**Human checking, not API spend, is likely to dominate cost — and must be in the cost model.** Our
original cost model left it out entirely. ⚠️ The specific ratio quoted in battery §8.3 is an
*illustrative scenario* built on assumptions nobody has approved or measured, not a finding.

**V0 calibration thresholds are admission hurdles, not accuracy measurements.** A checker can only
be caught out on an item that is genuinely broken, so a 30-item set that is half broken gives about
**15 chances**, not 30. Scoring zero mistakes on 15 chances is statistically consistent with a
checker that is truly wrong **up to about 18% of the time**; for the identity test, with about 10
chances, up to **26%**. Passing is a fair reason to *choose* a checker. **It is never evidence the
checker is accurate, and no Registry entry may describe it as low-error on this evidence.**
Full reasoning: `battery/INSTRUMENT-CALIBRATION-PLAN-V0.md` §2b.

**Counting objects and positioning them are separate capabilities.** A model can place a cup
correctly beside a laptop and still draw two laptops. They also need different sensitivity settings
on the same object-detection software — high when counting, so shadows are not counted as extra
objects; lower when locating. Shared software, **separate results**.

**Published benchmarks are method inputs, never our scores.** They did not test our conditions, our
scripts or our brand constraints.

**`scripts/check-vlm.mjs` cannot be run as committed** — it points at a folder path that does not
exist on this machine. Fixing it is a prerequisite for any re-calibration, because the rules require
re-testing a checker whenever its version changes.

---

## OPEN QUESTIONS

- Which additional checkers could be calibrated cheaply enough to be worth adding to V0.
- How a Registry entry should lose confidence as it ages. Deliberately **no formula was invented** —
  inventing one now would encode a guess about how fast models drift as though it were a finding.
  A rule can be proposed later from drift we have actually observed.

---

## DEPENDENCIES — what this stream is waiting on

**Material needed from Resources.** The Hindi test material splits in two, and the two cannot
substitute for each other:

- **M1a — the checker-calibration material.** Existing published Devanagari images that already come
  with human transcriptions. This tests whether our checker can *read* Hindi. **Reusable if
  Resources clears it** for bounded internal evaluation under the current Resources policy — note
  that a missing licence alone is no longer an automatic block for public, ungated material used
  internally.
- **M1b — the capability test items.** Prompt-and-target pairs to feed generators. These test
  whether a model can *draw* Hindi, and nothing public contains them, so the item set must be built.
  The **target phrases themselves may be sourced** from existing permissible Hindi text rather than
  written from scratch; what must be deliberately constructed is coverage of the hard cases —
  joined-letter forms, vowel marks, and the specific letter pairs we have watched models confuse.

**Neither has an owner.** Runs also wait on Controller approval of the model roster and on the
human-time budget (**≈ 11–15.5 hours, of which 2–4 must be a Hindi first-language reader**).

---

## PROPOSED CROSS-STREAM CHANGES

Three were identified in the EVAL-001 brief — one to Canon (about field naming), one to the routing
and memory systems (about Registry fields), one to Resources (about material). **None has been
filed** as a formal `PROPOSED-INTEGRATION-CHANGE` document; all await Controller direction on which
to formalise. The Registry field proposals are explicitly deferred.

---

## NEXT APPROVED TASK

**None.** Do not benchmark and do not spend on generation without a new approved task.

When the Controller opens one, the likely first step is the Resources clearance decision on M1a,
then assembling M1b and calibrating the two text checkers — because calibration is a gate that comes
*before* measurement. **That is a recommendation recorded in the EVAL-001 brief, not an approved
next action.**
