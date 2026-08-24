> ⚠️ **SUPERSEDED, 25 Aug 2026.** The Controller reviewed this proposal and required seven fixes
> before the design could be approved. The authoritative record is now
> [`eval/tasks/EVAL-005.md`](EVAL-005.md) and
> [`eval/tasks/EVAL-005-CONTROLLER-BRIEF.md`](EVAL-005-CONTROLLER-BRIEF.md). This file is retained
> unedited below so the two can be compared; **where it disagrees with those, they govern.**
>
> Specifically superseded here: the item/opportunity counts, the 8.2% and 5.5% bounds, the "85–90
> words" derivation, the claim that the battery is reproducible from `hb-shape` + `pango-view`, and
> the resource-budget figures.

---

# Controller Brief — Devanagari exactness battery design

**COMMUNICATION STANDARD:** `shared/COMMUNICATION-STANDARD.md` applies.

**TASK:** redesign of checker qualification after the EVAL-004 stop.
**Provisional ID: EVAL-005** — the Controller assigns task IDs; this is a worker proposal.
**STATUS:** design complete and tested — **awaiting Controller approval before any run**.

**Spend:** ₹0 API · 0 human specialist hours · 0 generations · 0 Registry entries · BSTD and
Marathi reserve untouched · EVAL-004 not resumed.

---

## HUMAN SUMMARY

The stopped pilot asked "can a model read an easy Hindi sign?" This asks the question that actually
decides whether a checker is safe to use: **when the picture is subtly wrong, does the checker still
say it matches?** That silent yes is what ships a broken asset with a passing grade attached.

The design change that unlocks everything is small: **we draw the images ourselves.** Render a
chosen word, and what the image contains is known by construction — no annotator, no dataset label,
no reader-agreement problem. That is the exact obstacle that stopped EVAL-004, and it disappears.
Human time falls from 3.5–4.5 hours across two readers to **about 1.5 hours, once** — and none of it
establishes the answer key, so a mistake there degrades the battery but cannot corrupt the results.

A hard item renders a *corrupted* word and asks the checker about the *real* word. The model sees
malformed text and is handed a plausible target, so every pull of its language prior says "yes,
that's it". That is precisely where autocorrection hides.

Building it surfaced a trap worth knowing about: **two different Unicode strings can produce
identical pixels.** Precomposed क़ and क+nukta render byte-for-byte the same. An item built on that
pair would have marked a checker wrong for correctly reporting what it saw. Every item is now
screened so that a difference must be both textual and actually on the page.

**One number needs saying before results exist:** the stratum that matters — plausible corruptions
in the hard direction — has only 35 items, giving a weak bound of 8.2%. Getting to ≤5% needs about
85–90 validated words instead of 53. That is a word-list validation, not another transcription
exercise, and it is the highest-value thing you can approve.

---

## OBSERVED

*Measured locally; every figure is reproducible from the committed code.*

1. **Two different Unicode strings can render identically.** क़ (U+0958) and क + nukta both shape to
   `[uni0915093C=0+770]`. 2 of 1,834 candidates were rejected on this basis.
2. **NFC agrees with the pixels.** It collapses precomposed nukta letters onto their decomposed
   forms — the same thing the renderer draws — so the mandated comparison and the image cannot
   disagree.
3. **Conjunct formation is mechanically verifiable.** क्ष shapes to one fused glyph
   `[uni0915094D0937]`; कष shapes to two. Ligature failure is therefore testable and provably visible.
4. **The built battery:** 106 items (53 match / 53 mismatch), 90 distinct images, 53 base words,
   20 failure classes across 5 groups, 35 items in the hard stratum.
5. **Trivial strategies score 50%.** 26 of 53 base words appear in both strata; 27 items are paired
   on one image with opposite expected verdicts.
6. **Determinism:** two builds produce byte-identical manifests; identical text renders
   byte-identically.
7. **Statistical bounds:** zero false passes gives 5.5% (all mismatches, n=53) but **8.2%** on the
   hard stratum (n=35). Per-class rates are **not estimable** at ~2.6 items per class.
8. **All construction tests pass**, including two regressions for defects found while building.

## INFERRED

Constructing images rather than finding them removes the entire ground-truth apparatus that stopped
EVAL-004 — not by cutting a corner, but because there is nothing left for those steps to do. The
`corrupt_image` direction is the only one that reproduces the production failure; the other is a
control. And a checker failing this battery cannot be trusted, because it autocorrects *well-formed*
wrong text, which is the easier case.

## SURPRISES / BELIEF UPDATES

- **The invisible-difference trap was real and I would have shipped it** without the shaping screen.
  It is not exotic: nukta items are exactly the kind of subtle case the battery wants most.
- **My own plausibility rule was wrong.** It flagged `तोड़ा` — an ordinary Hindi word — as malformed
  because it treated a vowel sign after a nukta as illegal. It would have discarded valid hard items.
  Caught by testing against real words, now pinned by a regression.
- **The headline statistical number flatters the design.** 5.5% across all mismatches sounds
  reasonable; the stratum that matters is 8.2%. Quoting the former would have been misleading.

## FAILURES / BLOCKERS

None blocked the design. Three defects found and fixed during construction (findings §5): duplicate
images, implausible corruptions diluting the hard stratum, and the plausibility-rule bug.

## UNKNOWN / NOT VERIFIED

- **Whether all 53 base words are real, well-formed Hindi.** The most important open question and
  the reason for the word-list validation.
- **Whether every mechanically-visible difference is perceptible to a person** at the rendered size.
- **Whether font choice changes results** — one font is used; unmeasured.
- **Whether transcribe-shape or verdict-shape is more exposed to autocorrection** — a hypothesis,
  both will be reported separately.
- **Whether passing predicts anything about malformed generated glyphs** — untestable here by
  construction.
- **Real per-call pricing** — the estimate rests on an old recorded figure needing re-verification.

## ASSUMPTIONS CHALLENGED

None promoted or demoted; no experiment was run. The design is consistent with ASSUMPTIONS §12 —
the cost model separates evaluation cost from human time, and human time again dominates.

## LOCAL IMPLICATIONS

Eval now has a checker-qualification design that does not depend on human transcription for ground
truth. The EVAL-003 calibration pack, its crops and its two-reader protocol are untouched and
remain available if the Controller ever wants the photographed-signage screen completed.

## CROSS-STREAM IMPLICATIONS

**None.** No Canon or Resources artifact is touched, no BSTD or Marathi data is used, and no
Registry field is proposed. Base strings are reused from the EVAL-003 Hindi pack **as lexical items
only** — a use unaffected by the annotation-reliability finding, since the image is rendered from
the string rather than described by it.

## ARCHITECTURAL IMPLICATIONS

None. No battery dimension, ladder, pass criterion, observation unit or Registry field is changed.

---

## DECISIONS NEEDED FROM CONTROLLER

1. **Approve or reject the design** before any run.
2. **Approve ~1.5 hours of one Hindi-competent reader** — and decide whether to expand the word list
   to ~85–90. That single choice moves the hard-stratum bound from 8.2% to ≤5% and costs almost
   nothing extra. **This is the highest-value decision here.**
3. **Approve a checker roster and API budget** — estimated ₹500–1,500 / $6–17 for a first run across
   both checker shapes. No roster is selected; that is deliberately yours.
4. **Decide separately on the Class B generated-glyph layer.** Specified, not built, needs
   generation spend.
5. **Note before results exist** that a pass is a qualification at a stated bound — never an accuracy
   claim — and says nothing about malformed generated glyphs.

## EVIDENCE WORTH HUMAN INSPECTION

- `eval/battery/devanagari-exactness/build/images/` — the rendered items. Worth looking at a few;
  it is the whole design in one glance.
- `eval/battery/devanagari-exactness/GENERATED-GLYPH-STRESS-LAYER.md` — what this battery
  deliberately **cannot** test, and why that boundary is stated rather than blurred.
- `NATIVE-VALIDATION.md` — the argument that one reader now suffices, and why that is structural
  rather than a shortcut.

## FILES CREATED

All under `eval/battery/devanagari-exactness/` unless noted: `devtext.py`, `perturb.py`,
`build_items.py`, `test_devanagari_exactness.py`, `README.md`, `FAILURE-TAXONOMY.md`,
`GENERATED-GLYPH-STRESS-LAYER.md`, `CHECKER-CONTRACT.md`, `METRICS-AND-QUALIFICATION.md`,
`NATIVE-VALIDATION.md`, `PROPOSED-TASK-SPEC.md`; plus
`eval/findings/devanagari-exactness-design-findings.md` and this brief.

**Nothing existing was modified.** No approved EVAL-001/002/003 artifact, no Resources or Canon
file, no historical evidence.

## RECOMMENDED NEXT STEP

*A recommendation, not an action taken.*

Approve the word-list validation first and expand the list while a reader is looking at it. It is
about an hour, it costs nothing else, and it is what moves the battery from "suggestive" to "a bound
worth quoting". Roster and API spend can follow; they are cheap and not the constraint.

## EPISTEMIC CHECK

Every figure is produced by committed code and reproducible by re-running it. Interpretations are
confined to INFERRED. Unknowns are listed rather than filled. Nothing is presented as approved: the
task ID is provisional, the battery is a proposal, and no checker has been run, qualified or ranked.

## CONFIRMATION

No paid checker call. No image or video model spend. No network call to any model. No human time
consumed. No Capability Registry entry. No BSTD or Marathi reserve use. EVAL-004 not resumed, its
Reader-A pilot not promoted to ground truth, and no checker qualified from it.
