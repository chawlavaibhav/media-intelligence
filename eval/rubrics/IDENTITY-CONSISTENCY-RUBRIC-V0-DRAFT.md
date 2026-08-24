# Identity Consistency Review Rubric — V0 DRAFT

**Task:** EVAL-002 · **Date:** 24 Aug 2026
**Status: DRAFT for Controller review. Not frozen. Not a calibrated instrument. No human has used
it on real media.**

Freezing this rubric requires Controller approval (EVAL-002 human-approval triggers). Until then it
is a proposal about *how* we would judge, not a standard anyone has judged by.

---

## 1 · What this is for, and why it must exist before anyone looks at outputs

The approved battery includes a test called `person_identity_across_prompts`. In plain terms: if we
give a generator a reference photo of a person and then ask it for several different scenes, **does
it stay the same person?**

We already have real failures of this kind, recorded before this rubric existed:

- *"face drift — younger, streak moved"*
- *"blazer color split"*
- *"outfit changed to pants"*

**Why write the rules first.** If reviewers look at the images before the standard is written, the
standard drifts to fit what they saw. Someone who has just looked at forty near-misses starts
accepting near-misses. Writing the rule first is the only way the answer means anything — and
changing it after seeing results is an explicit stop condition in `shared/AUTONOMY-POLICY.md`.

---

## 2 · The two lists every item must declare *before* generation

This rubric is unusable without both. They come from the Creative IR specification
(`canon/knowledge/SPEC-01-creative-ir.md`).

**`invariants`** — the things that ARE the identity. If one changes, identity is broken.
Example fields: face identity, hair marking (e.g. a streak and its position), wardrobe colourway.

**`allowed_variation`** — the things that may change freely and are NOT failures.
Example fields: lighting, viewing angle, pose, expression, background.

**Why the second list is load-bearing, not bookkeeping.** Without it, *"the blazer looks a different
colour"* and *"the lighting changed the apparent shade of the blazer"* are the same observation, and
the reviewer is being asked an undecidable question. A rubric that cannot separate those will
produce noise and call it data.

**Rule:** an item with no declared `allowed_variation` is **not reviewable**. Record it as
`not_reviewable`, do not guess, and send it back for specification.

---

## 3 · What the reviewer is shown

- The reference image(s) that defined the person. **Required** — without them question A in §4
  cannot be answered at all, and an item reviewed without its reference can only ever detect drift,
  never a wrong person.
- The **complete set** of generated images for that item, together.
- The declared `invariants` and `allowed_variation` lists.

**Not shown:** which model produced them, the prompts, other reviewers' scores, or any prior verdict.

**Why the whole set together.** This defect does not exist in any single image — one image of a
person is always "consistent with itself." Drift exists only *across* the set. The battery records
this as observation unit `asset_set_over_time`. Showing images one at a time makes the defect
undetectable no matter how careful the reviewer is.

---

## 4 · How to judge — two questions per invariant

**Corrected 24 Aug 2026 at Controller direction.** An earlier draft asked only whether each
invariant stayed *the same across the generated set*. That was incomplete, and the gap was not
cosmetic: **a set in which the generator produced a completely different person — but produced them
consistently — would have scored every invariant "held" and passed.** Stability is not identity.

For **each declared invariant**, the reviewer answers **two separate questions**:

| | Question | What it detects |
|---|---|---|
| **A · Reference fidelity** | Does this invariant match the **reference set**? | the generator ignored or overrode the reference — wrong person |
| **B · Cross-output consistency** | Is this invariant the same **across every generated image**? | the generator drifted — right person, unstable |

Each is recorded independently as `held`, `broken` or `cannot_tell`.

**Both must hold.** An invariant passes only when A is `held` **and** B is `held`.

### Why they are recorded separately

They fail for different reasons and call for different responses, so collapsing them into one
verdict destroys the information that would tell us what to do:

| A · fidelity | B · consistency | What it means | Implication |
|---|---|---|---|
| held | held | the right person, stably | **invariant passes** |
| held | broken | right person, drifts between images | classic identity drift — the case behind *"face drift — younger, streak moved"* |
| **broken** | **held** | **the same wrong person throughout** | reference conditioning is not taking effect at all. **Must fail.** This is the case the earlier draft would have passed |
| broken | broken | wrong and unstable | reference is being ignored and output is unstable |

**Item verdict:** the item **fails** if any invariant is `broken` on **either** question. It
**passes** only if every invariant is `held` on **both**. If any invariant is `cannot_tell` on either
question and none is `broken`, the verdict is `indeterminate` — not a pass.

### This does not change the approved battery

The approved `person_identity_across_prompts` dimension already defines the property as the declared
invariants holding across images **generated from one reference set** — the reference is part of the
definition. This rubric makes explicit how that is judged. **No dimension, difficulty ladder, pass
criterion or observation unit is changed.**

### Judge one invariant at a time

Do **not** give a single overall similarity impression. Holistic scoring is what makes identity
review unreliable: a set can look broadly right while the one feature that identifies the person has
moved. Per-invariant judging is also what lets repair act on the specific thing that broke.

## 5 · Recording multiple defects

**A single output may break more than one invariant, and all of them must be recorded.**

This is a project rule, not a preference. We have already lost information this way: an image
recorded only as *"rendered hex codes from prompt"* was later found to *also* carry a separate
composition defect. The human wrote down the most obvious problem and the second one vanished.
Under-recording defects makes shared causes invisible.

For each item, record:

```
item_id
verdict:            pass | fail | indeterminate | not_reviewable
invariant_results:                                    # one entry per DECLARED invariant
  - invariant:            <name>
    reference_fidelity:   held | broken | cannot_tell   # question A — matches the reference?
    cross_output_consistency: held | broken | cannot_tell   # question B — same across the set?
    images_affected:      [...]
    note:                 <free text>
defects:            [ { term, invariant, failure_mode, images_affected[], observer } ]
allowed_variation_notes: free text — differences that were noticed and correctly NOT counted
```

`failure_mode` on a defect is `reference_fidelity`, `cross_output_consistency`, or `both`, so the
distinction survives into the record rather than being flattened at capture time.

**`defects` may contain several entries.** The `allowed_variation_notes` field exists so a reviewer
can say "I noticed the lighting changed and did not count it" — which makes correct non-counting
visible instead of indistinguishable from not looking.

**Terms are recorded in the observer's own words.** Do not translate a description into a
predefined vocabulary at capture time; mapping happens later, and the original wording is evidence.

---

## 6 · Worked examples — fabricated descriptions, no media

⚠️ **These are invented text descriptions written to illustrate the rule. No image exists for any of
them. They are not evidence and must never be cited as observations.**

**Example A — passes.** Invariants: `face_identity`, `hair_streak_position`, `jacket_colourway`.
Allowed variation: `lighting`, `pose`, `background`.
Across four fabricated images the face and streak match the reference and are consistent with each
other; the jacket reads darker in one because the scene is dimmer. → all three invariants `held` on
**both** questions; the jacket note goes in `allowed_variation_notes`; **verdict: pass**.

**Example B — fails on consistency.** Same lists. In one fabricated image the hair streak sits on
the opposite side. Lighting is identical throughout, so shading cannot explain it.
→ `hair_streak_position`: `reference_fidelity: held`, `cross_output_consistency: broken`; defect
*"streak moved to other side"*, `failure_mode: cross_output_consistency`; **verdict: fail**.

**Example B2 — fails on fidelity, the case the earlier draft would have passed.** Same lists. Across
all four fabricated images the person is described identically to themselves — completely stable —
but the face does not match the reference person at all, and the hair streak the reference has is
absent throughout.
→ `face_identity`: `reference_fidelity: broken`, `cross_output_consistency: held`.
   `hair_streak_position`: `reference_fidelity: broken`, `cross_output_consistency: held`.
→ two defects, each `failure_mode: reference_fidelity`; **verdict: fail**.
**A perfectly consistent set of the wrong person is a failure, not a pass.**

**Example C — fails, two simultaneous defects.** In one fabricated image the face reads noticeably
younger **and** the jacket has become a different garment.
→ two invariants `broken`, **two defect entries recorded**; **verdict: fail**. Recording only the
more striking of the two would repeat the known under-counting error.

**Example D — indeterminate.** In one fabricated image the person is turned away and the streak is
not visible. Nothing is broken; one invariant cannot be checked.
→ `hair_streak_position: cannot_tell`; **verdict: indeterminate**, not pass. A pass would claim
evidence we do not have.

---

## 7 · Ambiguity and adjudication

1. **Two reviewers judge independently.** Neither sees the other's verdicts.
2. **Disagreement on any invariant goes to a third reviewer**, who sees the same material and the
   two conflicting per-invariant verdicts — not the reasons, to avoid anchoring.
3. **A reviewer who is unsure must use `cannot_tell`.** Guessing to avoid an awkward answer is the
   single most damaging thing a reviewer can do here, because it converts missing evidence into
   apparent evidence.
4. **Inter-reviewer agreement is reported alongside any result computed from these verdicts.** An
   automated judge can never be held to a higher standard than the humans defining truth for it.
5. **The rubric may not be edited mid-review.** If a case arises the rubric cannot decide, log it,
   mark the item `not_reviewable`, finish the batch, and revise the rubric as a new version
   afterwards.

---

## 8 · What this rubric cannot decide reliably

Stated so these limits are visible before use rather than discovered during it.

- **Whether a person is "the same person" in an absolute sense.** It only judges the invariants that
  were declared. If the declaration missed something that matters, the rubric will pass an image a
  customer would reject. **This is a specification risk, not a reviewer error.**
- **Anything at all about reference fidelity when the reference set is missing.** Without it,
  question A cannot be answered and the item is `not_reviewable`. An item reviewed without its
  reference detects drift only — which is precisely the blind spot this correction closed.
- **Degree of drift.** Verdicts are held/broken, not "20% different." Nothing here supports a claim
  like "this model drifts slightly."
- **Cause.** It records *what* changed, never *why* — not whether the reference was weak, the prompt
  ambiguous, or the model incapable.
- **Anything about low-resolution or heavily occluded material.** Those become `cannot_tell`, and a
  set with many `cannot_tell` results is a material-quality problem, not a model result.
- **Its own reliability.** This rubric has never been used. Whether two reviewers using it actually
  agree is unmeasured, and that measurement is part of calibration — which is **not** part of
  EVAL-002.

---

## 9 · Status and what would have to happen next

**Draft.** Not frozen, not calibrated, never used on real media.

Before it can produce a number anyone may rely on:

1. Controller approval to freeze it.
2. Reference image sets with declared invariants and allowed-variation lists — these do not exist,
   and acquiring them is Resources' work.
3. A calibration exercise measuring whether two reviewers using it agree, and whether an automated
   judge tracks them.
4. **A clear-eyed reading of what that calibration can support.** At the sample size the approved
   calibration plan proposes, a clean result is a *qualification gate*, not an accuracy figure — it
   would be consistent with a true error rate around 26%. See
   `eval/battery/INSTRUMENT-CALIBRATION-PLAN-V0.md` §2b.

None of steps 1–4 was performed in EVAL-002, and none may be started without a new approved task.
