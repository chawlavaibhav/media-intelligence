# Controller Brief — EVAL-001

**TASK:** EVAL-001 — Capability Lab V0 battery design
**STATUS:** **completed — Controller-approved, 24 Aug 2026** (revision 3, substantively approved;
revision 4 was housekeeping only). EVAL-001 is closed.

**Approved:** the V0 battery specification, its seven dimensions including D2 and D5, the calibration
specification and its qualification-gate framing.
**Still unapproved / deferred:** the workflow-model roster, the human-time budget (≈ 11–15.5 hours),
and the Registry's cross-stream field proposals. **No benchmark run is authorised.** Revision history
is in findings §10.

**HUMAN SUMMARY**

Two corrections in this revision change what the battery can honestly claim. First, counting objects
and placing them are now separate measurements — they fail independently and need different detector
settings, so merging them produced one number answering neither question. Second, and more
important: my calibration thresholds were written as if they were error rates, and at V0 sample
sizes they are not. Passing "zero false checks" on the planned set is consistent with a true error
rate as high as **18% for text and 26% for identity**, because a false pass can only occur on a
deliberately-broken item and there are only ten to fifteen of those. The ≤5% identity threshold I
set was not measurable at that size and is withdrawn. The thresholds stay useful as admission
hurdles; they are now labelled as such with their real uncertainty published. I also closed the
open OneIG-Bench question from its released files: its "Multilingualism" set is Chinese, not
multi-script, so our Devanagari claim is unaffected. Nothing runs until you decide on ≈11–15.5 hours
of human time, 2–4 of them a Hindi first-language reader.

**WHAT I DID**

Applied the seven corrections from your review of revision 2, re-checking each against sources
rather than adjusting wording. Merged current Resources policy into the branch. Zero generations,
zero paid API calls, ₹0 spent, no dataset acquired, no historical file altered.

**OBSERVED** *(sources tabulated in findings §7; repository evidence in §5)*

1. **OneIG-Bench, resolved from its released dataset** (findings §1.2). Exactly two configs are
   published: English (1,120 rows, **no Multilingualism category**) and Chinese (1,320 rows,
   including 200 `Multilingualism` rows). Six sampled Multilingualism rows are Simplified Chinese
   prompts about Chinese cultural subjects. **No Devanagari, no Indic script.**
2. **Small-sample arithmetic** (findings §5.9). With zero events in *n* opportunities the 95% upper
   bound on the true rate is `1 − 0.05^(1/n)`. Text: 30 items at 50:50 gives ~15 broken items →
   bound **~18%**. Identity: ~20 items at ~50% drift gives ~10 drifted items → bound **~26%**, and
   the finest observable resolution is 10%, so a ≤5% threshold cannot be tested at all. Supporting
   ≤5% needs 59 opportunities; ≤1% needs ~299.
3. **GenEval uses different detector confidences for the two tasks** — 0.9 for counting, 0.3
   elsewhere — and T2I-CompBench++ likewise separates numeracy from spatial relationships.
4. **Devanagari *recognition* benchmarks exist and are numerous**; **generative** text-rendering
   benchmarks do not cover Devanagari (findings §1.1–§1.2, unchanged from revision 2).
5. **Six provenance problems in our own material** stand unchanged (findings §5).

**INFERRED**

Counting and placement must produce separate Registry results even though they share detector
infrastructure; a merged dimension could not carry one honest `conditions.detector_confidence`.
V0 calibration can qualify an instrument but cannot characterise its error rate, so the first
Registry will be able to say "passed its qualification gate", not "accurate to within X%". Bounding
contact relations ("is the person actually holding it?") is not possible from bounding-box geometry
and stays unrun.

**SURPRISES / BELIEF UPDATES**

- **My thresholds were dressed as error rates and are not.** This is the correction most likely to
  have misled a later reader: a Registry built on revision-2 wording could have been described as
  low-error on evidence that permits an 18–26% true rate.
- **My own findings contradicted my own battery.** Findings §6 already said counting and placement
  were separate capabilities while §6.4 still merged them. Review caught it; I had not.
- **"Multilingualism" did not mean what it sounds like.** In OneIG-Bench it is the Chinese-culture
  prompt set. Reading the released files settled in minutes what the paper prose left ambiguous.

**FAILURES / BLOCKERS**

None blocked EVAL-001. Four block a *run*: no native-speaker ground truth for the Devanagari
instrument; no frozen identity rubric or reference sets; ≈11–15.5 hours of human calibration time
unbudgeted; `check-vlm.mjs` not runnable as committed.

**UNKNOWN / NOT VERIFIED**

- **M1a clearance.** No longer a licence question: under current `resources/CHARTER.md`, licence
  silence alone is not a block for public, ungated, internal-only material. What is unknown is
  whether **Resources will clear it**. **Eval performs no rights assessment.**
- **True instrument error rates.** V0 gates bound them only loosely. Not a gap to fill by
  assumption — a V1 sample-size decision.
- Whether checker rankings from printed-scan benchmarks transfer to generated-image text.
- Whether Tesseract genuinely fails on Devanagari — should be re-tested, not written off.
- Devanagari ground-truth labels; checker run-to-run consistency; Nano Banana **Pro** pricing.
- Whether the seven V0 dimensions are the *right* seven. Coverage is not claimed.

**ASSUMPTIONS CHALLENGED**

None promoted or demoted — no experiment was run. Three informed (findings §8): **§12** gains
external support for CpAO's shape and confirmation of its stated weakness; **§4**'s observation-unit
channel gains a second instance; **§15** stays blocked and untestable after V0, which is A-side only.

**LOCAL IMPLICATIONS**

Seven V0 dimensions after the split: D1 Devanagari text, D2 Latin text, D3 person identity,
**D4 `object_count`**, **D4b `spatial_relationship`**, D5 text stability across frames, D6
operational. Image run-shape rises from 12 cells to 15 — **360 trials per image workflow** at
N=12, R=2; video unchanged at 144. D4/D4b restricted to COCO-representable objects; brand marks and
contact relations deferred as `required_but_no_calibrated_instrument`.

**CROSS-STREAM IMPLICATIONS** — proposed, not acted on. Nothing filed pending your direction.

- **→ Canon.** SPEC-01 open question 1 (element-reference naming) unresolved, so the battery cannot
  cite IR paths mechanically. Nine path mismatches in battery §7.2, including one substantive error.
- **→ Empirical Memory / Planner.** Four Registry fields touch routing or memory semantics. Marked
  `PROPOSED · CROSS_STREAM`; **deferred per your direction**, not assumed.
- **→ Resources.** **M1a clearance under `resources/CHARTER.md` is the gating question** — it
  decides how much of M1 must be built and which end of the 11–15.5 hour range applies.

**ARCHITECTURAL IMPLICATIONS**

None requiring a stop. Schema gaps were representable as proposed fields.

**DECISIONS NEEDED FROM CONTROLLER**

1. **The workflow roster.** Costing cannot be finalised without it; battery §8.3 is illustrative.
2. **Human calibration budget: ≈ 11–15.5 hours**, of which 2–4 must be a Hindi first-language
   reader. Gates every Devanagari Registry entry.
3. **M1 ownership.** **M1a** — ask Resources to *clear* published Devanagari recognition material
   for bounded internal evaluation (not a licence hunt). **M1b** — assign an owner for the
   capability item set; its target strings may be sourced from existing permissible Hindi text
   rather than authored. Nobody owns either.
4. **Whether to buy narrower error bounds.** A genuine ≤5% claim needs ~59 opportunities per
   instrument — about six times the identity sample, with proportional annotator time.
   **Recommend not for V0**; flagged because it limits what the first Registry can say.
5. **Which cross-stream items to formalise**, given Registry architecture is deferred.

**EVIDENCE WORTH HUMAN INSPECTION**

- `INSTRUMENT-CALIBRATION-PLAN-V0.md` **§2b** — what a V0-sized calibration can and cannot
  establish, with the bound table. The section most likely to prevent a later over-claim.
- `EVAL-001-battery-design-findings.md` **§1.2** — the OneIG-Bench resolution, showing what the
  released files establish and what remains a sample.

**FILES CREATED / MODIFIED**

All under `eval/`: battery draft, Registry schema, calibration plan, findings, this brief, and
`HANDOFF.md`. Per-revision section lists are in findings §10. **No historical finding, script or
result file has been altered at any point** (clarification 12).

**RECOMMENDED NEXT STEP** *(recommendation, not an action taken)*

Get the M1a clearance decision from Resources first — it sets both the human-hour figure and how
much must be built. Then open a separate task to assemble M1b and run the I1/I2 calibrations, before
any capability run. Per §2b, the first Registry will be able to say an instrument *passed its
qualification gate*, not that it is accurate to within a stated percentage.

**EPISTEMIC CHECK**

Every figure is read from a named published source, a released dataset, or a file in this
repository, attributable via findings §7 or §5. Interpretations are confined to INFERRED, unknowns
are listed rather than filled, and nothing is presented as approved beyond D2 and D5.

Revision 3 specifically: thresholds are relabelled as qualification gates and published with their
95% bounds, and the ≤5% identity threshold is **withdrawn as not estimable** rather than quietly
retained; the OneIG-Bench conclusion separates decisive structural evidence from a 6-of-200 content
sample and extrapolates neither; external reuse is conditioned on a Resources *clearance decision*
matching current charter policy, with no rights assessment by Eval; and human-hour figures are now
identical across the calibration plan, battery, Handoff and this brief.

**CONFIRMATION**

No unapproved next strategic step was started. No model benchmarked, no generation call made, no
money spent, no dataset acquired. EVAL-002 not started.
