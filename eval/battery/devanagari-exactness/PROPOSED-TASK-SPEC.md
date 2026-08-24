> ⚠️ **SUPERSEDED, 25 Aug 2026.** The Controller assigned the real task ID and required seven
> design fixes. The authoritative task file is [`../../tasks/EVAL-005.md`](../../tasks/EVAL-005.md).
> This file is retained unedited below for comparison; where the two disagree, EVAL-005.md governs.
> Superseded here in particular: the item counts, the statistical claim, the human/API budget
> figures, and the "already done" list.

---

# PROPOSED TASK — Devanagari exactness checker qualification

**Provisional ID: EVAL-005.** Per `coordination/RUNBOOK.md` a task is not approved until it exists
as a file with a Controller-set ID. This is a **worker proposal**, not an approved task.

**Proposed by:** Eval / Capability Lab · **Date:** 25 Aug 2026
**Design status:** complete and tested · **Run status:** not started, not authorised

---

## OBJECTIVE

Determine whether a candidate evaluator can faithfully report **exact match** between visible
Devanagari and a requested target string, **without silently autocorrecting plausible-looking
errors** — and do so on constructed items whose ground truth needs no annotator.

## WHY THIS EXISTS

EVAL-004 was stopped because a photographed-signage reading screen was judged too weak a proxy for
the failure that actually matters commercially. This proposal is the redesign the stop decision
called for.

The downstream failure is **not** "can a VLM read Hindi". It is: we ask a generator for a specific
string, it produces something subtly wrong, and the checker says *matches*. That is a false pass,
and it ships a defect with a passing grade attached.

## WHAT IS ALREADY DONE (no approval was required, none was spent)

Design and infrastructure are complete and tested:

- 20-class failure taxonomy implemented as deterministic operators;
- item builder producing a balanced, deterministic, screened battery (**106 items** from 53 words);
- rendering + shaping pipeline giving **ground truth by construction**;
- validity screen rejecting differences that are not visible on the page;
- construction test suite, all passing;
- checker contract, metrics, qualification gates, cost estimate;
- explicit boundary marking what this battery **cannot** test.

## IN SCOPE (for the proposed run)

- validate/expand the base word list with one Hindi-competent reader;
- rebuild the battery deterministically from the validated list;
- run an approved checker roster over both checker shapes;
- score against the constructed ground truth;
- report false-pass and false-fail rates with bounds, split by direction, plausibility and group.

## OUT OF SCOPE

- the Class B generated-glyph stress layer (`GENERATED-GLYPH-STRESS-LAYER.md`) — needs separate
  generation-spend authorisation;
- any Capability Registry entry;
- BSTD or Marathi reserve data — **not consumed, and not to be consumed merely to raise item count**;
- resuming the EVAL-004 two-reader signage protocol;
- promoting the EVAL-004 Reader-A pilot to ground truth;
- qualifying any checker from the EVAL-004 run;
- battery/ladder/threshold/observation-unit changes elsewhere in the approved V0 battery.

## APPROVED-DEPENDENCY NOTE

Base strings are reused from the EVAL-003 Hindi pack transcriptions **as lexical items only**.
Their unreliability in EVAL-003 concerned whether they described a photograph; that is irrelevant
here because the image is rendered from the string. The residual question — "is this a real Hindi
word" — is the reason for the word-list validation below.

## DELIVERABLES (of the run, once approved)

- validated base word list + rebuilt battery manifest;
- checker responses, raw and parsed;
- scored results with bounds, split by every reported axis;
- findings + Controller Brief;
- an explicit statement of what a pass does and does not license.

## AUTONOMY MODE

**Proposed: `interactive`.** Battery design is not worker-autonomous under the Charter; running an
*approved* battery against an *approved* roster may be `autonomous_queue`.

## RESOURCE BUDGET (proposed)

| | |
|---|---|
| Human specialist time | **~1.5 hours, once** — one Hindi-competent reader (`NATIVE-VALIDATION.md`) |
| API/model spend | **₹500–1,500 / $6–17** estimated for a first run across both checker shapes |
| Generation spend | **₹0** — no image or video model is called |
| New data acquisition | **none** |
| Storage | negligible — 90 small PNGs, ~400 KB |

Pricing is an estimate from an old recorded figure and **must be re-verified before any run**.

## STOP CONDITIONS

- the word-list validation leaves too few valid words to build a balanced battery;
- rendering sanity check shows malformed output (we would be testing checkers against a broken font);
- a checker cannot be run without changing the frozen prompt or the comparison predicate;
- results would require changing the battery after seeing them — **EXPERIMENT MUTATION stop**;
- any spend, human time or data acquisition beyond the approved budget becomes necessary;
- any normal `shared/AUTONOMY-POLICY.md` trigger.

## HUMAN APPROVAL TRIGGERS

- the checker roster and API spend;
- the human word-list validation;
- any Class B generated-image work;
- any Capability Registry entry;
- expanding the base word list beyond internal repo-local material.

## CONTROLLER DECISIONS REQUESTED

1. **Approve the design** (or send it back) before any run.
2. **Approve ~1.5 hours** of one Hindi-competent reader, and decide whether to expand the word list
   to ~85–90 — which is what moves the hard-stratum bound from 8.2% to ≤5%.
3. **Approve a checker roster and API budget.** No roster is selected here.
4. **Decide on the Class B layer** separately; it is specified but not built and needs generation
   spend.
5. **Note before results exist** that a pass is a qualification at a stated bound, never an
   accuracy claim, and says nothing about malformed generated glyphs.
