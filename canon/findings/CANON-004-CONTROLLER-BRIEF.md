# CANON-004 — Controller brief

**Task:** CANON-004, Post-Extraction Audit Gate v0.2
**Date:** 25 Aug 2026 · **Branch:** `work/canon-004` · **Base:** `main` at `dc27616`
**Status:** design and test work complete · **needs_controller_review**
**Severity:** `LOCAL` — one Canon-only spec rule. No architectural conflict, no cross-stream change filed.

---

## Bottom line

The Audit Gate works, and it is cheaper than expected.

All four recurring CANON-003 failures are caught. The gate needs **one** authoritative rule change to
do it — a single addition to SPEC-05's governance section — and nothing else. SPEC-03, SPEC-04 and
SPEC-01 are untouched. No accepted source claim was reinterpreted or rewritten. All 16 books already
have a validated audit record, so **adopting this requires no backfill.**

**Decision needed:** ADOPT, ADOPT WITH REDUCTION, REVISE AND RETEST, or REJECT.
**Recommendation: ADOPT WITH REDUCTION**, cutting the one component that did not earn its place
(details in "The one thing to cut" below).

---

## What was actually built

A second file per book, written after that book's source knowledge is frozen, that asks five
questions and records the answers in a form a machine can read:

1. what did the copy we had hide, distort or destroy?
2. whose evidence is this, and did the source actually supply it?
3. can anything we are building use this — with "no" as a valid answer?
4. are two sources that agree really two sources?
5. is this old technical claim still true?

It reads the frozen record and never writes to it. That separation is the whole point: CANON-003
found that mixing product questions into source extraction distorts the source, so the second look
has to happen in its own layer, after the first is sealed.

Committed on the branch: the candidate schema, 16 records, a validator and 32 tests.

---

## The evidence, in short

**Representation integrity.** CANON-003 recorded one value per book, `visual_completeness`. Sixteen
lanes invented seven different values for it, with no controlled vocabulary in any spec and no
validator check at all. That one field was answering two unrelated questions — how far did we look,
and how much was there to see — and it gave *Creativity, Inc.* and *Building a StoryBrand* the same
value for opposite situations. The candidate splits the axes and records fourteen named loss
patterns, four of which recur across three or more books. It also separates two cases CANON-003
recorded identically: *Ogilvy* was unreachable because of a macOS permission that was later granted,
while *Interaction of Color* opened perfectly and is greyscale for a book about colour. One was a
click. The other is permanent.

**Evidence origin.** This is the strongest recurrence in the corpus. SPEC-03 has one field,
`empirical_within_source`, and four books broke it in four different directions: Hopkins claims tests
and reports almost no result; Heath reports measurement constantly and almost none is his own;
Sutherland does both in one section; Catmull and *Art & Fear* quote named colleagues, which the field
does not address at all. Every extractor did the right thing and wrote the truth into a caveat, where
nothing can count it. The audit records eight origin categories and the validator forces them to
agree with the frozen field rather than drift from it. Nine of sixteen books needed nothing beyond
"the author asserts this", so the cost falls only where the evidence is genuinely mixed.

**Application fit.** Every one of seven consumers must be answered once per source, and
`no current binding` is a full answer that is structurally distinct from "not audited". This restores
the attention the old mandatory-binding rule forced without restoring the rule — which mattered,
because *Creativity, Inc.* and *Art & Fear* produced 44 objects and zero Creative IR bindings, and
that is correct.

**Lineage.** *Grammar of the Shot* and *Grammar of the Edit* are the same two authors, same
publisher, same series, a year apart, each citing the other, sharing four near-identical terms. Under
SPEC-05's current guard — a count of distinct source identifiers — they would pass as two sources
agreeing. They are one position stated twice. The candidate rule rejects that pair and accepts Murch
against *Grammar of the Edit*, which is a real convergence between a different author, publisher and
decade. Both results are asserted by tests against the committed records, not against a fixture.

**Technology contingency.** No new vocabulary. `historical_claim` and `culturally_bounded` already
express it and were applied correctly on *Painting With Light*. What was missing was a step: nothing
forced the extractor to ask. Three sources were assessed as applicable, thirteen marked not
applicable with a stated basis.

---

## What it costs

An audit record averages **154 lines** against an average source-knowledge file of 1,590 — about a
**10 per cent** addition to a book's record, and slightly less than the existing visual-evidence
ledger. Writing all sixteen required **no source book to be re-opened**; every record was built from
committed repository evidence. Three of sixteen carry an element the repository could not settle,
and none escalated to `evidence_insufficient`.

---

## The one thing to cut

`deterministic_composition` as an application consumer fired **once in sixteen books** — on Samara,
where nine of fourteen remedies are layout operations an engine could execute exactly and none is a
generative control. The finding is real. One in sixteen is thin, and fifteen records carry a
`no_current_binding` line that adds nothing. It is the obvious reduction.

By contrast `human_workflow` fired as a candidate in **7 of 16** books — the Braintrust, the
Operating Manual for Not Quitting, Hopkins's keyed-advertisement method — and should stay.

---

## Two revisions the corpus forced

Both were caught by running the candidate over all 16 books rather than by reading it, which is the
argument for testing a method design against a whole corpus.

1. **Symmetry only for dependence.** Requiring every lineage relation to be mirrored produced pure
   bookkeeping. A shared publisher is uninformative to mirror and a citation is one-directional. Only
   the four relations that defeat independence must be declared from both sides.
2. **Independence is a property of a pair, not of a source.** A source-level "not independent" flag
   would have blocked *Grammar of the Shot* against Freeman, Murch and Samara in order to catch its
   one real dependence — fifteen usable pairings thrown away to catch one bad one. A test caught it.

---

## A defect found in the inherited corpus

**The committed integration validator was red on `main` before this task changed anything:** 10
errors, all *Made to Stick* remedy terms missing SPEC-05's required `executable_by`.

This does not contradict the integration record, which states plainly that the full validator was
never re-executed on the final head. The mechanism is in the validator: it returns early on a YAML
parse failure. *Made to Stick*'s parse failure was one of the 24 catalogued defects, so that book's
term-level checks never ran in the run that produced the inventory. Repairing the quoting made the
file parseable and unmasked ten checks that had been skipped, and nothing re-ran to see them.

Repaired in its own commit using the repair already Controller-accepted for the same defect class —
`executable_by: [unknown]`, exactly as applied to 16 Hopkins and 7 Sutherland remedies. Additive
only: 10 lines, no id, reference, count, claim, concept, binding or relationship changed, term total
unchanged at 417. **The integration validator now reports 0 errors.**

The lesson is about the instrument, not the data: a validator that aborts a unit on a parse error
under-reports, and the shortfall is invisible in its own output. That is a general engineering point
rather than a Canon finding, so no cross-stream change has been filed — but the Eval harness has
negative fixtures of a similar shape and the Controller may want to forward it.

---

## Exact change requested

**SPEC-05, Governance rule 5.** Append to the existing rule:

> Independence is established from the Audit Gate lineage records, not from a count of distinct
> `origin_ref` values. Two origins may be counted as independent only when neither source's audit
> record declares the other with relation `shared_author`, `same_series`, `companion_volume` or
> `derivative_of`, and neither carries `independence_not_established`. A shared publisher or a
> citation does not by itself defeat independence.

**Extraction procedure**, between the fresh checkpoint and any cross-source or product work:

> After a book's source knowledge, systems and ontology are stable and its fresh checkpoint is
> committed, write its Audit Gate record and validate it. Cross-source promotion and downstream
> product use may not consume an unaudited source.

Nothing else. No new SPEC-03 evidence characteristic, no new SPEC-04 target type, no new ontology
relation or term kind, no Creative IR change, no CI workflow.

---

## Notable rejections

- **New SPEC-03 evidence characteristics** for claimed-measurement and third-party research. Real
  problem, wrong layer — it would mean migrating 16 frozen corpora and re-deciding 505 objects, and
  the audit answers it additively with zero migration.
- **Any numeric visual-risk score.** Three independent findings show count-based proxies fail.
  *Creativity, Inc.* has 33 images and none argues; *StoryBrand* has 36 and two carry content the
  text never states.
- **New SPEC-04 target types** for human workflow and deterministic composition. A target type means
  bindings, and no executor exists for either. Parking the fit is honest; inventing a binding is not.
- **Restoring mandatory Creative IR bindings.** It would have produced 44 distortions across two
  books.

---

## What is still unknown

- The gate has never been exercised on an actual promotion, because no `cross_source_concept` has
  ever been created. The failure it prevents is predicted — but the prediction is now mechanically
  checkable, which is a step short of observed.
- The anti-score guard blocks a field named like a score. It cannot stop a reader counting
  categories and treating the count as a ranking. The corpus contains exactly the trap: *Building a
  StoryBrand* binds best to the product schema and has the weakest support in the corpus. The rule
  that closes this belongs to the consumption layer and is out of scope here.
- Nothing yet checks that an audit was written against the current version of its source record.
  `audited_against_commit` is recorded and not verified.
- These 16 records were written by one worker. Whether a different worker produces the same record
  is untested.

---

## Verification

| Instrument | Result |
|---|---|
| `canon/validation/validate_canon003_integrated.py` | **0 errors** — 16 books, 505 objects, 54 systems, 417 terms, 53 concepts, 111 bindings |
| `canon/validation/validate_audit_gate_v02.py` | **0 errors** — 16 records |
| `tests/` (both suites) | **32 passed** |

Run with a local `.venv` carrying PyYAML and pytest; no PyYAML is installed system-wide on this
machine, which is worth knowing before the next session tries to validate anything.

---

## Recommended next step

Controller decides ADOPT / ADOPT WITH REDUCTION / REVISE AND RETEST / REJECT. On an adopt, open a
small follow-on task that applies the single SPEC-05 rule and the procedure step — CANON-004 does not
apply them. Canon-consumption/RAG work should then consume the audited record rather than the
pre-audit one.
