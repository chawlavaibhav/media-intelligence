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

**EVAL-003 — Devanagari checker calibration pack readiness.** Completed 24 Aug 2026, **awaiting
Controller review**. Full record: `tasks/EVAL-003-CONTROLLER-BRIEF.md`.

Readiness only: ₹0 API, 0 hours human specialist time, no external call, no generator, no capability
result. What it produced, in `eval/calibration/devanagari-v0/`:

- **A 54-item candidate pool** of real photographed Devanagari signage, built deterministically from
  the CVIT lineage. The same repository state always produces a byte-identical manifest.
- **A blinded reviewer pack** — readers see crop and item ID only. Verified mechanically: no
  Devanagari character appears anywhere in the generated pack. **The protocol uses two independent
  readers** (≈ 3.5–4.5 h total); a single reader's transcription would silently have become the
  answer key.
- **Materialised crops with proven geometry.** Reviewer and checker read the **same files**, verified
  by hash. A self-test on a coordinate-encoded synthetic image proves crop geometry and found that
  `sips --cropOffset 0 0` silently centre-crops; a verified workaround handles it.
- **A calibration run plan** with staged blinding, costs, and what a clean result would and would not
  license.
- **`check-vlm.mjs` per-item targets** — each item can carry its own reference transcription.
  Judgement provably unchanged: all 27 stored historical cases re-scored through both code paths,
  0 mismatches.

**⚠ Two dataset releases from the same source lineage disagree about one time in three.** On 1,082
strictly one-to-one matched regions they agree 725 times (67%).

**What that supports:** source annotations are demonstrably unsafe to promote directly to project
ground truth — which is why the protocol establishes its own reference with **two independent
readers** rather than adopting a dataset label.

**What it does NOT support** *(corrected 24 Aug 2026 after Controller review — an earlier version of
this handoff claimed otherwise)*: it is **not** human inter-annotator agreement, **not** a measure of
human reading ability, and **not** a ceiling. No evaluator threshold may be derived from it. The
repository holds no provenance showing the two annotation sets were made independently.

**⚠ The pool currently contains no Hindi at all** — 53 Marathi, 1 unlabelled. All 173 Hindi-labelled
records sit inside the excluded cross-dataset overlap, because the smaller dataset's Devanagari
folder *is* the larger one's Hindi folder. Since the failure we hunt is a language-prior failure and
our production failure is Hindi, this is a validity gap. Options are in
`eval/calibration/devanagari-v0/PROPOSED-V0-COMPOSITION.md`; **awaiting a Controller decision.**

Earlier: **EVAL-002** (completed, Controller-approved, closed) and **EVAL-001** (completed,
Controller-approved).

It built plumbing only — no generation, no network call, no calibration, no spend. What it produced:

- **`scripts/check-vlm.mjs` now runs anywhere.** It previously contained a folder path that existed
  on one machine only. Paths and invocation changed; **what the checker judges did not** — the new
  code was run offline over all 27 stored transcriptions from the original study and reproduced
  every verdict exactly (0 mismatches).
- **`harness/` — a local evaluation harness using fabricated data only.** It proves a test item can
  flow through evaluation and come out as a countable result obeying the battery's rules. It proves
  **nothing** about any model. Its outputs are labelled synthetic and are git-ignored.
- **`rubrics/IDENTITY-CONSISTENCY-RUBRIC-V0-DRAFT.md`** — how a reviewer would judge whether a
  generated person is the right person and stays that person. Each declared identity feature is
  judged on **two** questions: does it match the reference, and is it consistent across the
  generated set. **Both must hold** — a consistently-produced *wrong* person is a failure, not a
  pass. **V0 FROZEN 24 Aug 2026 — but not validated and not calibrated, and never used on real
  media.** Frozen means the standard is fixed so it can be tested; it does not mean it works.
  It may not be edited during or after calibration — a case it cannot decide is logged as
  `not_reviewable` and raised as a V1. *(The filename keeps `-DRAFT` because the approved task file
  names that exact path; the status inside the document governs.)*
- **`battery/M1B-DEVANAGARI-GENERATION-ITEM-DESIGN-V0.md`** — the structure and coverage plan for
  the Hindi generation-test prompts. **Controller-approved V0 design, 24 Aug 2026 — but not
  populated, not linguistically validated, and not ready to score models.** Zero items exist; no
  Hindi phrase has been selected or authored; no first-language reader has checked anything. The
  fields, ladder and coverage categories are fixed at V0.

Earlier: **EVAL-001 — Capability Battery V0 design**, completed and Controller-approved 24 Aug 2026
(`tasks/EVAL-001-CONTROLLER-BRIEF.md`).

## CURRENT TASK / QUEUE

**None.** The EVAL-003 correction pass is complete and awaiting Controller review. **Do not start the
human calibration** — it needs a composition decision, reader approval and a checker roster first.
EVAL-004 has not been opened and must not be started without an approved task file.

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

**Devanagari calibration material now exists, and its labels disagree with each other.** Resources
supplied 29,722 real photographed Devanagari images with transcriptions. Two dataset releases from
the **same source lineage** assign different transcriptions to ~33% of the same regions (EVAL-003
findings §2). Treat every source transcription as one observation, never as project ground truth.
This is cross-dataset annotation disagreement — **not** human inter-annotator agreement, and no
evaluator threshold may be derived from it.

**The CVIT lineage is effectively one dataset.** 173 files are byte-identical across IndicSTR12 and
IIIT-ILST — and those are 98% of everything IIIT-ILST has labelled, leaving only 3 unique images.
**BSTD is therefore the only genuine cross-source check we have, and it is held untouched.**

**Hindi text: reading benchmarks are plentiful; a drawing benchmark has not been found.** There are
many public benchmarks for *reading* Devanagari out of a photo (text recognition). **No suitable
public benchmark for generative Devanagari rendering was identified in the EVAL-001 search (24 Aug
2026)** — a bounded review, not an exhaustive survey, so treat this as "not found", not "does not
exist". Reading and drawing are different capabilities either way: **do not cite a text-recognition
benchmark as evidence about a generator.**

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

**`scripts/check-vlm.mjs` is portable and supports per-item targets** (EVAL-002, EVAL-003). Two
mutually exclusive modes: `--input` + `--target` for one target across a run, or `--items` for a file
where each record carries its own `{id, image, target}`. `--dry-run` validates either with no API key
and no network call. **Judgement is unchanged across both**, verified against all 27 stored historical
cases with 0 mismatches, and that check runs in `node eval/harness/run-fixture.mjs --selftest`.

**Test evaluation tooling with deliberately-broken inputs, not only correct ones.** EVAL-002 added
negative-control fixtures and they immediately exposed three real defects: a run that raised
integrity errors still exited successfully; a run the harness had *already rejected* still reported a
result marked eligible for the Registry; and the negative check itself passed on an aggregate
"some error was raised somewhere", which with two or more fixtures would pass even when one was
silently accepted. All fixed, with `--selftest` pinning the last one. **None was visible from reading
the code** — each appeared only when something was deliberately broken.

**Stability is not identity.** A checker or rubric that only asks "did this stay the same?" will
certify a consistently *wrong* result. Any consistency test needs a fidelity test beside it.

---

## OPEN QUESTIONS

- Which additional checkers could be calibrated cheaply enough to be worth adding to V0.
- How a Registry entry should lose confidence as it ages. Deliberately **no formula was invented** —
  inventing one now would encode a guess about how fast models drift as though it were a finding.
  A rule can be proposed later from drift we have actually observed.

---

## DEPENDENCIES — what this stream is waiting on

**M1a is now satisfied.** Resources delivered the Devanagari reading material and EVAL-003 built a
calibration pack from it. What blocks the first real calibration is **human time and a roster**:
~1.5–2 hours of a Hindi first-language reader for the blind transcription pass, 20–30 minutes to
confirm altered targets afterwards, then a checker roster and API spend. **None is approved.**


**Material needed from Resources.** The Hindi test material splits in two, and the two cannot
substitute for each other:

- **M1a — the checker-calibration material.** Existing published Devanagari images that already come
  with human transcriptions. This tests whether our checker can *read* Hindi. **Reusable if
  Resources clears it** for bounded internal evaluation under the current Resources policy — note
  that a missing licence alone is no longer an automatic block for public, ungated material used
  internally.
- **M1b — the capability test items.** Prompt-and-target pairs to feed generators. These test
  whether a model can *draw* Hindi. **No suitable public set has been identified in our search so
  far**, so the V0 item set must be built — that is a statement about our search, not proof that
  none exists, and it should be revisited if Resources surfaces one.
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
