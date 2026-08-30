# CANON-014 — Controller Brief (final full-corpus reconciliation)

**Branch:** `work/canon-014-final-full-canon`, cut clean from `main` at `bf02dd1`.
**Not merged. Supersedes PR #66 and PR #67 for integration purposes.**

This brief separates **OBSERVED** (mechanically checkable in the repository), **INFERRED** (my
reading, which could be wrong) and **RECOMMENDED** (proposals, not decisions). Nothing in RECOMMENDED
has been acted on.

The full plain-English account is `CANON-014-FULL-CORPUS-REPORT.md`. This brief is the decision
surface.

---

# OBSERVED

## O-1. One corpus, two states, nothing discarded

42 sources represented. **24 accepted** (19 already live + 5 admitted here), **18 held**. The
23 CANON-014 candidates split 5 accepted / 18 held.

**More than half the knowledge in this repository is held rather than accepted** — 839 of 1,516
source-knowledge objects, and 920 of 1,028 Q&A items. Any total quoted without that split
substantially overstates what the Canon has established.

## O-2. Everything validates, and one thing does not

| Check | Result |
|---|---|
| Audit Gate | **24 records, 0 errors** |
| Schema validator, live | 24 dirs, **3 errors** — all pre-existing in `sutherland-alchemy-introduction` |
| Schema validator, candidates | 18 dirs, **0 errors** |
| Q&A validator | 23 banks, 1,028 items, **0 errors** |
| `pytest tests/ --ignore=tests/test_request_freeze_gates.py` | **179 passed, 113 subtests** |
| Mechanical checklist (13 checks) | all pass |

The checklist proves, among other things: no duplicate object id anywhere across all 42 sources; no
dangling internal reference; **every accepted source has exactly one audit record and no held source
has one**; no source appears in both trees; every accepted snapshot digest matches the exact bytes;
zero `cross_source_concept` and zero agreement assertions in any artifact; no binary added; no
out-of-scope path touched.

## O-3. The five admitted sources were repaired before admission, not admitted as they stood

The three from the laptop lane carried **202 schema violations** against the hardened contract. The
books were not re-extracted; every repair is semantic and decided per object. Three bindings were
**removed** rather than given a stronger role to survive, including one binding *pricing and
packaging strategy* as media production. The knowledge behind every removed binding is untouched.

## O-4. All 18 held sources now pass the same validator the accepted ones do

257 defects repaired from committed evidence, the largest being 216 repair terms carrying
`executable_by` as a string where SPEC-05 wants a list. **A structural pass is not admission** and
this branch never presents it as one.

## O-5. The access blocker on the 17 no longer holds — this is a change of fact

The earlier passes held them partly because the source could not be opened: the extraction had read a
local library absent from the repair container, which also had no network egress. **Neither is true
here. 15 of the 17 books are on this machine, and egress was tested and works.**

What remains is that **no figure-level inspection has ever been run** on any of them, so none has a
visual-evidence ledger and none can complete the Gate. That is now **cost and authorisation, not
access** — a materially better position, and not a pass. This task did not run those inspections;
promoting 17 sources on its own judgement is not a reconciliation's call.

## O-6. Live Canon may be carrying guidance its own source later withdrew

`light-science-magic-beyond-ch3` records that the later chapters **demote a live chapter-3 remedy**
— polarising the source — to "a solution to avoid whenever possible", **reverse** the polariser's
place in the remedy order between chapters 4 and 5, and withdraw the glass-support trick for black
subjects. `light-science-magic-ch3` is accepted live Canon and its record does not know this.

This is one author qualifying himself, **not** two sources disagreeing, and must never be presented
as the latter.

## O-7. No cross-source promotion exists anywhere

Zero `cross_source_concept`, zero `same_failure_family`, zero canonical equivalence, across all 42
sources. Eight apparent convergences are recorded as **refusals with the reason stated**. The
lineage matrix is v3 and covers all 23 candidates plus the live sources they touch, pairwise.

Two constraints on any future promotion are easy to miss and are recorded in the matrix: five of the
17 are the same work read further and carry **zero** independence against a live source; and **none
of the 18 held candidates has an audit record**, so under SPEC-05 no independence is *established*
for any pair involving them, whatever the matrix records about their content.

## O-8. Q&A: 1,028 items, nothing removed, one amended

23 banks at `canon/qa/canon-014/`. 40.7% require application — observed, never required; the old
one-third quota is gone. The screen found no duplicate id, no duplicate question, no malformed item
and no short answer. One item was **amended** because a source correction here made part of its
answer wrong.

**Grounded, ungraded, uncalibrated.** No human and no model has answered a single item. It is not
benchmark ground truth and not evidence that Canon improves anything.

## O-9. Three fingerprints, deliberately separate

| Fingerprint | Files | SHA-256 |
|---|---|---|
| Accepted Canon | 120 | `a9cee40fb433adc08ac98ba7c87e1ead790f60aa71d184327cc5e97f59ed7eb9` |
| Full knowledge corpus | 193 | `cbd321aa3be7464e785a0d42de1764cdccc8bdd33bc023a376740f8f196bde60` |
| Q&A corpus | 23 | `1313c0babe2194a7bc71c1628f9fbec5fa4f35ca5ff5edc7f594662101dc62bd` |

A future Canon-vs-no-Canon experiment **must name which one it used**. They are not interchangeable.

## O-10. An unrelated test defect blocks the whole suite

`tests/test_request_freeze_gates.py` (CANON-010) hardcodes an absolute container path and runs its
runner at module scope, so importing it calls `sys.exit(0)` and pytest **aborts collection of the
entire suite**. Every green suite figure in this repository — including the 179 above — is an
`--ignore`d subset. Recorded as **F-06** with a verified two-line patch. **Not fixed here:**
CANON-014 does not own that file.

---

# INFERRED

## I-1. The held corpus is the most valuable unfinished asset in the repository

839 source-knowledge objects and 920 Q&A items are sitting one authorised visual pass away from an
admission decision, and the pass is no longer blocked. The cost of finishing is small relative to the
cost of the extraction already paid for.

## I-2. Two of the 17 are worth finishing before the rest

**`light-science-magic-beyond-ch3`**, because live Canon may be giving consumers withdrawn guidance
and this is the source that would establish it. And the **`kahneman-sibony-sunstein-noise` /
`connor-irizarry-discussing-design` pair**, because it is the corpus's only material on how human
judgement of the same artefact varies, and evaluator design is live work now.

## I-3. What the Indian expansion actually bought

Not "Indian context" as a checkbox. Four specific things Canon did not have: a **documented case of a
production convention outliving its cause**; a structural account of why a **purchase signal is not a
preference signal** when the purchaser is not the viewer; a distinction between an **enabling
condition and a grading criterion** that our evaluation work had no name for; and a set of **named
reasoning errors with worked cases**, stripped of every number.

All of it is bounded historical material — *Cinema India* dates its own subject as past, Bijapurkar's
data is 2008, Jain's fieldwork ends around 2006. **It is not a current picture of India** and
presenting it as one would contradict all three sources.

## I-4. The Bijapurkar representation finding generalises beyond that book

A conversion preserved the prose as text and the entire evidence base as images, so a text-only
extraction would have kept every assertion and silently lost everything under it. That failure mode
is **invisible from the text** and applies to any converted source with tables or figures. It is the
strongest argument in the corpus for running the visual pass at all.

## I-5. Where I judged the corpus weakest

Airey's copy inverts a case study's outcome and should probably be replaced rather than inspected.
The Ries/Binet contradiction is a genuine problem: a source asserting "immutable laws" without
measurement against an accepted source built on measured data, and admitting both without deciding
would put opposed advice in one Canon. And Google's ABCD material is platform-contingent almost
throughout — legitimate knowledge about a platform, not knowledge about how images and video work.

---

# RECOMMENDED

Proposals. None acted on. None is a decision.

## R-1. Merge this branch as one decision, and retire PR #66 and #67

The two donor branches are superseded for integration. This branch is cut clean from `main` and
contains what both produced, reconciled, plus the 17-source migration neither did.

## R-2. Authorise a visual-pass programme for the held corpus, in priority order

`light-science-magic-beyond-ch3` first (it may correct live Canon), then the *Noise* /
*Discussing Design* pair (evaluator design), then the remaining scope extensions, then the rest.
**Not** Airey, which needs a different copy first.

## R-3. Decide the Ries versus Binet & Field contradiction explicitly

Five recorded contradictions between a held candidate and an accepted live source. Leaving it
undecided is fine while Ries is held and becomes a real problem the moment anyone proposes admitting
it. This is a Controller judgement and I have not made it.

## R-4. Fix F-06 under a task that owns `tests/**`

Two lines, no assertion changed. Until it lands the repository has no runnable full test suite, and
every green figure is a subset. Higher priority than its size suggests.

## R-5. Decide the three Sutherland defects rather than letting them sit

Three concept systems in an accepted source have no `provenance`. Repairing requires reopening the
book, which stales the audit and needs your authorisation.

## R-6. Do not enable candidate retrieval without a status-carrying interface

This task prepared the candidate corpus and **did not change runtime retrieval**, which still reads
`canon/knowledge/current/**` only. If candidate retrieval is ever enabled, every returned object must
expose `source_status` alongside `source_id`, `claim_type`, the evidence characteristics and both
uncertainty fields. Without that, held material can reach a consumer indistinguishable from audited
Canon, which is the one failure this whole two-state architecture exists to prevent.

## R-7. Two gaps remain closed to us, and both are access rather than effort

**Devanagari and Indic typography is completely unclosed** and unchanged since CANON-013 — the Dalvi
paper's publisher route returned HTTP 503 throughout and the thesis is behind institutional
authentication, which must not be bypassed. The Cayla & Elson article on Indian consumers is
paywalled. Neither is a work-scheduling question; both need a decision about acquisition.
