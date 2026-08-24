# CANON-004 — Controller brief

**Task:** CANON-004, Post-Extraction Audit Gate v0.2
**Date:** 25 Aug 2026 · **Branch:** `work/canon-004` · **Base:** `main` at `8e99785`
**Status:** design and test work complete, plus one Controller correction pass · **needs_controller_review**
**Severity:** `LOCAL` — one Canon-only spec rule. No architectural conflict, no cross-stream change filed.

---

## Bottom line

The Audit Gate works, and it is cheaper than expected.

All four recurring CANON-003 failures are caught. The gate needs **one** authoritative rule change to
do it — a single addition to SPEC-05's governance section — and nothing else. SPEC-03, SPEC-04 and
SPEC-01 are untouched. No accepted source claim was reinterpreted or rewritten. All 16 books already
have a validated audit record, so **adopting this requires no backfill.**

**Decision needed:** ADOPT, ADOPT WITH REDUCTION, REVISE AND RETEST, or REJECT.
**Recommendation: ADOPT.** The correction pass closed the one real hole in the design — a stale audit
could previously keep validating after its source had changed — and exposed no further architectural
problem. The earlier recommendation to cut `deterministic_composition` is withdrawn.

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

Committed on the branch: the candidate schema, 16 records, a validator and 46 tests.

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

An audit record now averages **167 lines** against an average source-knowledge file of 1,590 — about
an **11 per cent** addition to a book's record, and slightly more than the existing visual-evidence
ledger at 158. **Fourteen of those lines are the machine-generated snapshot; the human-written part
is unchanged at 154 lines**, so closing the stale-audit hole added no authoring burden. Writing all
sixteen required **no source book to be re-opened**. Three of sixteen carry an element the repository
could not settle, and none escalated to `evidence_insufficient`.

---

## Corrections applied this pass

### 1. `deterministic_composition` retained

The previous brief recommended cutting it for firing once in sixteen books. **That inference does not
hold, and the recommendation is withdrawn.**

Frequency in this corpus measures what these sixteen books happen to teach. It does not measure
whether the product will need the distinction. The project explicitly anticipates deterministic
executors for creative-production tasks where an exact operation beats asking a generative model to
approximate one, and Samara's grid geometry is precisely that class — add a column, hang a character,
set a measure, all operations a layout engine performs exactly. A corpus weighted towards
photography, film and persuasion is the wrong instrument for measuring how much layout knowledge
exists in the world.

Cost of keeping it: one `no_current_binding` line in fifteen records, the same cost every consumer
carries when it does not apply. No binding was created and no SPEC-04 target type was added.

`human_workflow` also stays — it fired as a candidate in **7 of 16** books (the Braintrust, the
Operating Manual for Not Quitting, Hopkins's keyed-advertisement method).

### 2. Stale audits now fail, mechanically

**The hole.** An audit describes a source at one moment. The first draft recorded a commit SHA that
nothing checked, so an accepted source could be edited after its audit and the stale audit would keep
validating. For a gate meant to block promotion and product use, that is worse than no gate: a
consumer would be told a source had been audited when the thing audited no longer exists.

**The fix.** Each record carries `source_snapshot` — a SHA-256 content fingerprint of the frozen
artifacts it was written against, computed over lexicographically sorted paths so it depends only on
file bytes, never on filesystem order, clock or git state. The validator recomputes it on every run
and fails if anything moved, naming the file and both digests.

**Why a fingerprint rather than git.** A commit SHA changes on rebase, squash and cherry-pick without
a byte of the source changing, and does not change at all when a file is edited in a dirty tree.
Content addressing asks the question actually needed: *are these still the bytes I audited?*

**What is covered — five files, each justified individually** rather than swept in for completeness:
`source-knowledge.yaml` (sk_refs and the evidence cross-check resolve into it),
`operational-bindings.yaml` (application fit cites its binding ids),
`source-concept-systems.yaml` (bindings resolve system refs into it; audit prose cites its fields),
`ontology-mappings.yaml` (the layer whose promotion the lineage audit governs),
`visual-evidence-ledger.yaml` (representation integrity is derived from it and nothing else would
catch a change to it).

**`PROVENANCE.md` is deliberately excluded** — narrative prose, not a machine-consumed
representation, and the facts the audit takes from it are restated in the audit's own structured
fields. It stays in the informational evidence basis.

**One version mechanism, not two.** `audited_against_commit` is renamed `recorded_at_commit` and is
informational only. The validator does not read it, and a test asserts that changing it has no effect
on validation.

**No refresh tool, deliberately.** A one-command snapshot updater would rubber-stamp the exact
staleness the field exists to catch. A changed source needs a re-run of the Audit Gate, which
produces a new snapshot as a by-product.

**Proven on the real corpus, not only fixtures:** appending one comment line to *The Vignelli
Canon*'s visual ledger turned a clean 16-record run into exactly one error naming the file and both
digests; restoring it returned the run to clean.

### 3. Test fixtures corrected, and a robustness fix they exposed

The independence fixtures constructed `not_independent`, which is not a schema value; they passed
only because the promotion function ignored the unrecognised string. Fixtures now use
`not_independent_of_named_sources`, a test asserts every fixture verdict is in the controlled
vocabulary, and `independent_origins_ok` now **fails closed** on an unrecognised verdict instead of
letting a malformed record through.

### 4. Branch synced with current `main`

`origin/main` advanced to `8e99785` when Resources PR #5 merged. Merged cleanly, no conflicts. The
Resources change touches no file under `canon/` or `tests/`, and none of its semantics were pulled
into Canon.

### 5. Corpus unchanged

CANON-004 remains fixed to the 16-book CANON-003 corpus. *Master Shots* and *The Conversations* are
absent from the repository and were not ingested, audited or integrated.

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
- The snapshot proves the source *representation* has not moved since the audit. It does not prove
  the auditor read it correctly — that remains a review question, not a mechanical one.
- These 16 records were written by one worker. Whether a different worker produces the same record
  is untested.

---

## Verification

Run fresh from the final PR head, after the corrections and after the `main` sync. These are the
actual commands and their actual output, not a carry-over from an earlier run.

| # | Command | Exit | Result |
|---|---|---|---|
| 1 | `python canon/validation/validate_canon003_integrated.py --root .` | **0** | `error_count: 0` · 16 books, 505 SourceKnowledge objects, 54 systems, 417 terms, 53 concepts, 111 bindings |
| 2 | `python canon/validation/validate_audit_gate_v02.py --root .` | **0** | `error_count: 0` · `record_count: 16` |
| 3 | `python -m pytest tests/ -q` | **0** | **46 passed, 5 subtests passed** |

The corpus counts are byte-for-byte identical to the pre-correction run, which is the expected
result: the correction pass added audit metadata and changed no frozen source artifact.

**SPEC files confirmed byte-identical to current `main` (`8e99785`):**
`git diff --stat origin/main -- canon/knowledge/SPEC-01-creative-ir.md
canon/knowledge/SPEC-03-source-knowledge.md canon/knowledge/SPEC-04-operational-bindings.md
canon/knowledge/SPEC-05-knowledge-ontology.md` returns empty.

No GitHub Actions workflow was added.

Run with a local `.venv` carrying PyYAML and pytest; no PyYAML is installed system-wide on this
machine, which is worth knowing before the next session tries to validate anything.

---

## Recommended next step

Controller decides ADOPT / ADOPT WITH REDUCTION / REVISE AND RETEST / REJECT. On an adopt, open a
small follow-on task that applies the single SPEC-05 rule and the procedure step — CANON-004 does not
apply them. Canon-consumption/RAG work should then consume the audited record rather than the
pre-audit one.
