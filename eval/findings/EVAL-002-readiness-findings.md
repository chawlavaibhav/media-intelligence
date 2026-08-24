# EVAL-002 — Readiness findings

**Date:** 24 Aug 2026 · **Cost:** ₹0 · **Generations:** zero · **Network calls:** zero
**Human specialist time:** zero

What became runnable, what was learned by running it, and what is still only a draft.

---

## 1 · The checker script is portable, and the repair provably did not change its judgement

**What was wrong.** `eval/scripts/check-vlm.mjs` is the only working evaluation script in the
repository — it is the code that produced the FINDINGS-01 checker study. It contained a folder path
that exists only on one machine, so it could not be run anywhere else. That matters more than it
sounds: project rules require a checker to be **re-tested whenever its model version changes**, and
a script nobody else can run cannot be re-tested.

**What changed.** Paths and invocation only. The script now takes `--input`, `--out`, `--model` and
`--target` on the command line, has `--help`, and has a `--dry-run` mode that validates everything
and lists what would be sent **without making a network call and without needing an API key**.

**Why the distinction matters.** A "portability fix" that quietly alters what the checker judges
would make every future result incomparable with the original study — an explicit stop condition in
the autonomy policy. So the judgement code was moved, not rewritten: the prompt, the text
normalisation rule, the edit-distance function and the exact-match verdict are byte-identical.

**How that was proven rather than asserted.** The scoring function is now exported, so it can be run
offline. It was applied to **all 27 transcriptions already stored** in
`eval/runs/finding-01-devanagari-check/` and compared against the stored verdicts:

```
re-scored 27 stored transcriptions; 0 mismatches
```

Every `normalized`, `exact_match` and `edit_distance` value reproduced exactly. **OBSERVED: the
repair preserved judgement.** This is a stronger check than reading the diff, because it exercises
the real Unicode normalisation path on the real recorded data.

**Not fixed, and out of scope:** the script still uses one target string per run. Per-item targets
will be needed when the M1b item set exists. Making the target a command-line value was necessary
for portability; making it per-item is a change to how a run is driven, and belongs with the item
set, not here.

---

## 2 · The harness proves the mechanics, and it found two real defects by being run

`eval/harness/` runs a test item through evaluation end to end using **fabricated data only**. It
makes no network call — `run-fixture.mjs` contains no network primitive of any kind.

**What it demonstrates** (full list in `eval/harness/README.md`): loading an item, identifying its
dimension, attaching a generation reference and a checker result, recording pass/fail with several
defects on one output, separating independent items from repeated attempts, recording the
observation unit, treating a many-frame clip as one observation, carrying cost fields without
inventing values, and emitting both a machine-readable file and a human summary.

**Three counting rules, demonstrated on fixtures:**

| Fixture | Shows |
|---|---|
| `fixture-01` | 1 independent item, 2 attempts (a repeat is not a second item); 2 defects recorded on one output |
| `fixture-02` | 1 generation scored on two dimensions → **2 dimension-results from 1 generation**, explicitly reported as *not* 2 independent trials |
| `fixture-03` | a 6-frame clip → **1 observation**, with correctness and stability reported separately; plus a dimension whose instrument state is *"matters, cannot currently be measured"* |

**The two defects the harness found in itself.** A negative-control fixture was added — deliberately
invalid, counting one generation as two independent trials and using an invalid observation unit —
because **a check that never fails proves nothing**. Running it exposed two real problems:

1. **The run exited successfully despite raising integrity errors.** Any automated use would have
   treated a broken run as a clean one.
2. **A rejected run still reported a Registry-eligible pass rate.** The fixture failed its integrity
   checks and *still* produced `pass_rate: 1` marked as eligible for the Registry, because the
   fixture's instrument state happened to be `deterministic`.

The second is the more serious: it is precisely the "false confidence attached to bad data" pattern
this whole stream exists to prevent, reproduced in our own tooling. **Both were fixed.** A run that
raises any integrity error now quarantines every result in that run regardless of instrument state,
and exits non-zero.

**INFERRED:** negative controls should be standard for any future evaluation tooling. Neither defect
was visible from reading the code; both appeared only when something was deliberately broken.

**What the harness does NOT prove:** anything about a model, a checker's accuracy, or cost. The
fixtures are hand-written mock data, labelled `SYNTHETIC_FIXTURE` and producing results labelled
`SYNTHETIC_RESULT` with a warning against ever copying them into the Registry.

**Registry schema not promoted.** The harness writes a local JSON shape because it needs something
to aggregate. That shape is implementation-scoped and reversible, and is stated as such in the
README. The proposed Registry schema and its deferred cross-stream fields are untouched.

---

## 3 · Devanagari content: reused, never authored

The fixtures needed some Devanagari to exercise the Unicode normalisation path — the part of the
checker most likely to break silently, since it handles zero-width joiners and combining marks.

**No Hindi was written for this task.** The two strings used are *already recorded* in
`eval/runs/finding-01-devanagari-check/`: the original target and the corrupted reading observed in
the Wan clip, including the within-clip drift. Each fixture field carries a
`*_provenance` note saying so.

**Why this is not a linguistic judgement.** The assertion being made is that two strings the
repository already records as different normalise to different values. That is a string-processing
check, not a claim about Hindi. **Every judgement about whether a Hindi string is correct remains
outstanding and belongs to a native reader.**

---

## 4 · Two drafts that must not be mistaken for standards

**The identity rubric** (`eval/rubrics/IDENTITY-CONSISTENCY-RUBRIC-V0-DRAFT.md`) sets out how a
reviewer would judge whether a generated person stays the same across images: judge each declared
identity feature separately rather than forming an overall impression, show the reviewer the whole
set at once because the defect does not exist in any single image, count `cannot_tell` as
indeterminate rather than a pass, and record every defect rather than only the most obvious one.

Its examples are **fabricated text descriptions** — no image exists for any of them.

**The M1b design** (`eval/battery/M1B-DEVANAGARI-GENERATION-ITEM-DESIGN-V0.md`) specifies the fields
and coverage plan for the Hindi generation-test items: conjuncts, vowel marks, nukta, and the ब→व
and य→थ confusions we have actually observed, with matched Latin controls so a Hindi failure can be
distinguished from a general text failure.

**No item was created and no phrase was selected.** The design also records what it does *not*
claim: it is a set of deliberately chosen stress cases, not a representative model of Hindi.

**Neither draft is calibrated, frozen or approved.** Both say so at the top.

---

## 5 · What this changes for the first real calibration

Before EVAL-002, four things stood between an approved design and a first calibration run: an
unrunnable script, no proof an item could flow through evaluation at all, no written identity
standard, and no design for the Hindi items.

**Three are now removed.** The script runs anywhere; the mechanics are demonstrated and
regression-guarded; the two documents exist as reviewable drafts.

**What still blocks a real calibration, unchanged by this task:**

1. **No Hindi first-language reader time is budgeted.** Approximately 2–4 hours, and without it no
   Hindi target string is established ground truth.
2. **No material.** M1a needs a Resources clearance decision; M1b items do not exist.
3. **No identity reference sets**, and no frozen rubric.
4. **No model roster**, and no human-time budget.

**An expectation worth setting now.** When calibration does run, at the approved sample size a clean
result is a *qualification gate* — it justifies choosing a checker. It is **not** an accuracy
measurement: a clean sweep there is statistically consistent with a true error rate around 18% for
text and 26% for identity. The harness enforces the corresponding rule mechanically — an instrument
that is not `calibrated` or `deterministic` cannot produce a Registry-eligible number.

---

## 6 · What remains uncertain

- **Whether the harness's local result shape survives contact with the real Registry format.** The
  Registry schema is still a proposal with deferred cross-stream fields. Deliberately reversible.
- **Whether the identity rubric produces agreement between two reviewers.** Never used. That is a
  calibration question and calibration was out of scope.
- **Whether sourced Hindi text can fill the coverage categories**, or whether items must be
  constructed — which would increase native-reader time.
- **Whether the per-run target string is sufficient** once items have individual targets. Flagged in
  §1, not resolved.
- **Whether the fixtures cover the mechanics that will actually matter.** They cover what the
  approved design specifies today. Real items will probably surface cases nobody anticipated.

---

## 7 · Stop conditions — none fired

No stop condition in EVAL-002 or `shared/AUTONOMY-POLICY.md` was triggered. Specifically: the
portability repair did **not** require changing checker judgement (§1, proven); the approved battery
was representable without altering any dimension, ladder, pass criterion or observation unit; no new
instrument was needed; no cross-stream schema decision became necessary; no Hindi content had to be
invented or judged (§3); and no real media, API access, dataset acquisition, spend or specialist time
was required.

The two harness defects in §2 were **implementation bugs in tooling written during this task**, not
contradictions in the approved EVAL-001 design.

---

## 8 · Correction pass — 24 Aug 2026, after Controller review

Three corrections were applied after EVAL-002 was substantively approved. The first closed a real
logical hole; the second closed a real hole in a test; the third corrected an overclaim.

### 8.1 · The identity rubric could have passed the wrong person

**The hole.** The rubric as first written asked, for each declared identity feature, only whether it
stayed *the same across the generated set*. It never asked whether it matched the **reference** in
the first place.

**Why that is serious.** A generator that ignores the reference entirely and produces a completely
different person — but produces them **consistently** — would have scored every feature "held" and
**passed**. Stability is not identity. The rubric would have certified the wrong person as correct,
provided the model was wrong in a stable way. And a stably-wrong model is a *likely* failure mode,
not an exotic one: it is what "the reference conditioning is not taking effect" looks like.

**The fix.** Each declared feature is now judged on **two independent questions**:
**A · reference fidelity** — does it match the reference? and **B · cross-output consistency** — is
it the same across the set? Both must hold; either being broken fails the item.

**They are kept separately diagnosable because they imply different responses:**

| Fidelity | Consistency | Meaning |
|---|---|---|
| held | broken | right person, drifts — classic identity drift |
| **broken** | **held** | **the same wrong person throughout** — reference is being ignored |
| broken | broken | wrong and unstable |

**No battery change.** The approved `person_identity_across_prompts` dimension already defines the
property against a reference set; the rubric now operationalises what the dimension already implies.
No dimension, ladder, pass criterion or observation unit was touched.

**Consequence for later work:** an item reviewed **without its reference set** can detect drift only,
never a wrong person. Such items are now `not_reviewable` rather than silently half-judged.

### 8.2 · The negative-control check was unsound with more than one fixture

**The hole.** `--negative` passed when *any* error was raised anywhere in the run
(`totalErrors > 0`). With one negative fixture that is adequate. **With two or more it is unsound:**
one fixture's errors cover for another that was silently *accepted*, so a broken guard passes
unnoticed — precisely the failure negative controls exist to catch.

This is the same class of error as §2's: a check that looks like it verifies something and does not.

**The fix.** `--negative` now requires **every** negative fixture to be individually rejected, and
where a fixture declares `expected_error_codes`, those specific codes must appear — so a fixture
rejected *for the wrong reason* also fails.

**Regression coverage added.** A second negative fixture (`fx-05`, violating a different rule) makes
the multi-fixture case real rather than hypothetical, and `--selftest` pins the corrected behaviour
with four cases, including the exact bug:

```
PASS  all fixtures rejected with their declared codes -> PASS
PASS  one fixture NOT rejected while another is -> FAIL (the bug being guarded against)
      note: aggregate totalErrors would be 2 > 0 here, so the OLD check passed this. It must now fail.
PASS  fixture rejected but for the wrong reason -> FAIL
PASS  no negative fixtures at all -> FAIL (an empty suite must not read as success)
```

The last case matters too: an empty negative suite previously reported success, so deleting the
fixtures would have looked like everything passing.

### 8.3 · An overclaim about public benchmarks, corrected

**What was wrong.** The M1b design said no public generative-Devanagari benchmark **"does not
exist"** and that **"nothing public contains this."**

**Why that is more than the evidence supports.** What we actually have is a **bounded search
conducted during EVAL-001 that did not find one.** That is not an exhaustive survey of everything
published, and absence of evidence in a search is not evidence of absence.

**The supported claim, now used consistently:** *no suitable public generative-Devanagari benchmark
has been identified in our search so far, therefore our V0 item set still needs to be built.*

**The practical conclusion is unchanged** — we build the set either way. What changes is that the
design now says the claim should be **revisited if a suitable public set is later identified**,
including anything Resources surfaces under RES-002, rather than treating the question as closed.

### 8.4 · Flagged, not fixed: the same phrasing survives in EVAL-001

`eval/findings/EVAL-001-battery-design-findings.md` §1.2 still carries the categorical form
("no public benchmark measures whether a generative image or video model correctly renders
Devanagari…"), though it is dated and scoped in context.

**I did not edit it.** EVAL-001 is closed and Controller-approved, and correction 3 was scoped to
the M1b wording. Editing an approved, closed artifact to match a later correction is a Controller
decision, not a worker one. **Flagged here for that decision.**

### 8.5 · What the correction pass did not change

The seven approved dimensions, their difficulty ladders, pass criteria and observation units; the
calibration thresholds and their published bounds; and the Registry architecture, which remains a
proposal with deferred cross-stream fields. No generation, network call, calibration, spend or
specialist time.

---

## 9 · Closure pass — 24 Aug 2026, documentation only

Applied after Controller approval of the correction pass. **No code, no design, no threshold and no
architecture changed** — status statements only.

**9.1 · The identity rubric is frozen at V0.** Frozen means the standard is now fixed so a
calibration exercise can be run *against* it, and it may not be edited during or after that exercise
— amending a rubric after seeing its results converts a measurement into a description of what we
hoped to find. A case it cannot decide is logged, the item marked `not_reviewable`, and a **V1**
raised afterwards.

**Frozen is not validated.** No human has used it on real media; whether two reviewers applying it
agree is unmeasured. The two-question structure — reference fidelity *and* cross-output consistency,
recorded separately, both required — is explicitly part of what is frozen, because collapsing them
would restore the hole §8.1 closed.

**9.2 · The M1b item structure is Controller-approved as a V0 design.** Approved: the item fields,
the inherited difficulty ladder, and the coverage categories. Not approved and not done: **zero items
exist**, nothing has been linguistically validated by a Hindi first-language reader, and it is
therefore **not ready to score any model** — a generator's output cannot be judged against a target
nobody has confirmed is correct.

**9.3 · EVAL-001 findings §1.2 corrected, with traceability preserved.** §8.4 flagged that the
categorical phrasing survived in the closed, approved EVAL-001 findings and left the decision to the
Controller. The decision was to amend. Applied as a **dated Controller correction**: the original
wording is **retained in place and marked superseded** rather than deleted, with the supported
statement — *our bounded search did not identify a suitable public generative-Devanagari benchmark;
it did not establish that none exists* — recorded beneath it along with what changed, what did not,
and what follows. The correction is also listed in that file's revision history so it is discoverable
from either end.

**Why retained rather than replaced.** Anyone who cited the original line needs to be able to see
exactly what it said and why it changed. Silently rewriting history would leave a citation pointing
at text that no longer exists.

**9.4 · One cosmetic mismatch, deliberately not fixed.** The frozen rubric's filename still ends
`-DRAFT`, because `eval/tasks/EVAL-002.md` — a Controller-authored task file — names that exact path
as the deliverable. Renaming would either invalidate that reference or require editing an approved
task file. The status block inside the document governs and says FROZEN unambiguously. **Renaming is
a Controller decision.**

**EVAL-002 is closed.** EVAL-003 is not open; Resources is being finalised and becomes its input.
