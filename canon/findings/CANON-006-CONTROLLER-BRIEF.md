# CANON-006 — Controller brief

**Task:** CANON-006, adjudicate and integrate the two deferred reserve sources
**Date:** 25 Aug 2026 · **Branch:** `work/canon-006-reserves` · **Task-base:** `main` at `57fccaf`
**Status:** adjudication complete · **needs_controller_review**
**Severity:** `LOCAL`, with one method-change proposal returned for decision.

---

## Bottom line

**One reserve in, one reserve blocked. Live Canon is 17 accepted, not 18.**

*Master Shots* passed the authoritative Audit Gate and is accepted downstream knowledge.

*The Conversations* is **blocked** — and it is blocked by a limit in our method, not by any defect in
the extraction. Its recovered record is complete and passes every mechanical check with zero errors.
The problem is that it is Walter Murch talking, the live corpus already contains Murch's own book,
and **none of Audit Gate v0.2's seven lineage relations can say that truthfully.** Rather than pick
the least-wrong label, I wrote no audit record, held the source as source evidence, and returned the
exact minimum method change for your decision.

A live Canon of 17 is better than a dishonest 18.

**Historical numbers are untouched.** CANON-003 accepted 16. CANON-004 tested 16. The historical
validator is byte-identical to `main` and still reports 16 books / 505 objects / 111 bindings.

---

## 1. Recovery — what was imported and how

No legacy branch was merged and no legacy commit was cherry-picked. Each artifact was taken by path
with `git checkout <legacy-ref> -- <exact paths>`.

| Reserve | Legacy branch | Imported |
|---|---|---|
| *Master Shots* | `work/canon-003-rebalance-d` | `canon/knowledge/current/kenworthy-master-shots-ch8/` (6 files) · `canon/findings/CANON-003-book11-master-shots-findings.md` |
| *The Conversations* | `work/canon-003-b` | `canon/knowledge/current/ondaatje-conversations-ch3/` (6 files) · `canon/findings/CANON-003-book12-conversations-findings.md` |

Both findings files are new; neither overwrites anything on `main`. **The lane checkpoint files on
`main` were deliberately not overwritten** with their legacy tip versions — those are historical
CANON-003 records, and their completion evidence is quoted here instead.

### Frozen-extraction check

Required before importing, and it passed cleanly for both. Each source directory was diffed between
its stated fresh pre-history checkpoint and its legacy branch tip:

| Source | Range checked | Files changed | Commits touching the directory |
|---|---|---|---|
| `kenworthy-master-shots-ch8` | `2d3da5d` → `work/canon-003-rebalance-d` | **0** | **none** |
| `ondaatje-conversations-ch3` | `9e6f716` → `work/canon-003-b` | **0** | **none** |

Later lane work did not silently reinterpret either frozen extraction. The sealed-until-checkpoint
discipline held.

### Were the source files changed?

**No.** Neither directory was edited — not to fit modern expectations, not to resolve anything. All
original ids were preserved, and they do not collide with anything in the live corpus.

---

## 2. Reserve 11 — *Master Shots* · **ACCEPTED**

Christopher Kenworthy, *Master Shots* vol. 1, 2nd ed., Michael Wiese Productions, 2011. Frame
material plus chapter 8 "Directing Attention", complete.

**Counts, matching the legacy record exactly:** 20 SourceKnowledge · 3 SourceConceptSystems ·
17 ontology terms · 8 relationships · 3 concepts · 6 OperationalBindings.

**Mechanical validation:** 0 errors against current SPEC-03/04/05, unmodified.

**Audit record:** `canon/audit/records/kenworthy-master-shots-ch8.audit.yaml`,
`audit_record_version: v0.2`, snapshot computed after the source layer was frozen at `d57ac75`.

### Representation integrity

`publisher_epub` · `no_pages_reflowable` · `inspected_figure_level` · `figure_carries_content`.

The important finding is the one the task flagged, and I recorded it as **two competing patterns
rather than one**, because the evidence does not settle which applies:

- **`required_visual_dimension_destroyed`** — technique 8.6 "Color Guides" claims a character in an
  orange jacket stays identifiable against a blue-graded frame. Colour saturation was measured across
  all 124 images at ~2,000 samples each: **zero coloured pixels in any of them.** The illustration
  shows a grey smudge on a grey beach — the outcome the technique says colour prevents. The
  demonstration does not merely fail to support the claim, it shows the opposite. Detectability
  `silent`: nothing in the text, file or image is anomalous, and no mechanical check would find it.
- **`source_evidence_never_printed`** — the original worker's *inferred, explicitly unverified*
  reading that the greyscale is the printed book's own condition. Three things point that way: the
  arrow notation distinguishes camera from actor by white-against-black, a choice only a monochrome
  book needs; "About the Images" discusses printing clarity and never mentions colour; and the
  greyscale is uniform across all 124 images. If that is right, the evidence was never printed and no
  better copy exists.

Collapsing those into one would have asserted a cause nobody established. Settling it needs a
physical copy, which the task forbids acquiring.

Also recorded: `no_authored_page` (no page numbers anywhere, none invented) and one
`display_type_ocr_damage` instance ("REST pOINT"). **Nineteen of twenty objects are unaffected**, and
the mirror finding is evidence *for* the source: its arrow notation is tonal rather than chromatic
and survives greyscale, low resolution and colour-blind readers.

### Evidence origin

The most uniform profile in the live corpus: all 20 objects carry `explicitly_stated` and
`practitioner_assertion`; none carries `empirical_within_source`, `outcome_claimed`, `anecdotal` or
`controlled_comparison`. Single category, `source_author_assertion`.

One pattern named so it is not mistaken for an origin category: each technique is warranted by naming
a released film that used it. That is an **example type**, not a claim origin — the claim stays
Kenworthy's — and it is already carried by `visually_demonstrated`. No category was invented for it.

### Application fit

Bound: `creative_ir` (2), `production_ir` (1, parked), `evaluation` (2), `governance` (1).
No binding: `benchmark`, `deterministic_composition`. Candidate: **`human_workflow`** — four objects
are about how the reader should practise rather than about an asset, including that the source ranks
the reader's own test above its own recommendations.

### Lineage · `independent_origin`

Michael Wiese Productions appears nowhere else in the corpus, so not even `shares_publisher_only`
applies. Three domain-adjacent sources were checked individually and recorded as `no_known_relation`
so a later promotion can see the question was examined: both Grammar books and Alton. **Shared domain
and conventional Hollywood shot grammar are not dependence** — if they were, no two sources in a craft
could ever corroborate each other.

### Technology contingency · not applicable

A 2011 second edition. It is one of only two sources in the corpus with **no** `historical_claim` and
**no** `culturally_bounded` object, and the source states the point itself: the techniques are stated
independently of the equipment that executes them.

**Verdict: accepted downstream knowledge.**

---

## 3. Reserve 12 — *The Conversations* · **BLOCKED — source evidence only**

Michael Ondaatje, *The Conversations: Walter Murch and the Art of Editing Film*, Knopf, 2002. Third
Conversation, complete.

**Counts:** 27 SourceKnowledge · 3 SourceConceptSystems · 16 terms · 8 relationships · 3 concepts ·
6 OperationalBindings. **Mechanical validation: 0 errors.**

**There is nothing wrong with this extraction.** It is careful work — encoding positively verified
(0 replacement characters across 92,199 words), hedges preserved, speaker register recorded on every
object because SPEC-03 has no speaker field, and contamination disclosed on the object itself.

### Why it is blocked

The live corpus contains `murch-blink-p1-25`, written by Walter Murch. *The Conversations* is
substantially Murch speaking, under Ondaatje's authorship. The legacy extraction established two
concrete overlaps from the sources themselves:

- the **Egyptian-painting argument** — a footnote in *Blink*, a full passage here;
- **`planarity`** — a Rule of Six criterion in *Blink*, `planarity_of_the_face` here.

They are not two origins agreeing. **One practitioner, recorded twice, by two different authors.**

I tested all seven relations against the evidence. None is truthful:

| Relation | Verdict |
|---|---|
| `shared_author` | **false** — Ondaatje is the author; Murch is the interviewee |
| `same_series` | **false** — Knopf 2002 vs Silman-James Press 2001 |
| `companion_volume` | **false** — different publishers, four years apart |
| `derivative_of` | **false** — neither derives from the other |
| `cites_source` | **insufficient and dangerous** — not established, and under the adopted rule it does not defeat independence, so it would let the pair pass |
| `shares_publisher_only` | **false** |
| `no_known_relation` | **false** — the relationship is documented and concrete |

Writing any of them into an authoritative record would be a false statement. So I wrote none.

**This is harder than the case the rule already catches.** The Grammar books share authors, publisher
and series — visible on a title page. Here **the author field itself differs**, and no metadata
anywhere records that a book consists largely of another person's words. This pair passes every check
built on author, publisher or source id.

**Verdict: source evidence only.** Present, valid, documented, and blocked from cross-source
promotion, downstream product use and Canon-consumption/retrieval. No audit record was written, which
is what makes the block real rather than advisory.

**Proposal returned:** `canon/PROPOSED-METHOD-CHANGE-CANON-006-LINEAGE.md` — one new lineage relation
`shared_primary_informant`, one sentence of SPEC-05 Governance rule 5, two validator constants, one
test, and reciprocal entries on exactly one pair of records. Migration surface is that one pair;
nothing else changes. Rejected alternatives are listed with reasons.

---

## 4. New infrastructure — the live-corpus register

The Audit Gate created a state the repository could not express: a source that is real, valid and
worth keeping, but not cleared for downstream use. Before CANON-006 the audit validator assumed every
source directory must hold a record, so a deliberately-blocked source was indistinguishable from an
oversight.

Added, as the smallest thing that closes it:

- **`canon/audit/LIVE-CORPUS.yaml`** — declares every live source as `accepted` or
  `source_evidence_only`, the latter requiring a `blocked_reason`. It also pins
  `historical_method_test_corpus: 16` so that number cannot drift with the live one.
- **`canon/validation/validate_live_corpus.py`** — validates the current corpus: every source on disk
  is declared, every `accepted` has exactly one active v0.2 audit record, every
  `source_evidence_only` has none and states why, every source is mechanically valid whether accepted
  or not, and ids are unique across everything present.
- The audit validator's coverage check now consults the register instead of assuming. **An undeclared
  source is still an error** — a decision must be recorded, not merely implied by absence.

**The historical validator was not touched.** `validate_canon003_integrated.py` is byte-identical to
`main`, its `ACCEPTED_BOOK_DIRS` still holds exactly 16 entries, neither reserve appears in it, and
its output is unchanged.

Two existing tests hard-coded `16` for the live record count. They now count from the register and
additionally assert the live corpus never *loses* accepted sources. That is a correction, not a
weakening: those tests conflated the historical method-test corpus with the live corpus, which is the
exact distinction this task exists to draw.

---

## 5. Verification — fresh from the final branch head

| # | Command | Exit | Result |
|---|---|---|---|
| 1 | `python canon/validation/validate_canon003_integrated.py --root .` | **0** | `error_count = 0` · **16 books**, 505 objects, 54 systems, 417 terms, 53 concepts, 111 bindings — *unchanged from `main`* |
| 2 | `python canon/validation/validate_audit_gate_v02.py --root .` | **0** | `error_count = 0` · `record_count = 17` · `records_path = canon/audit/records` |
| 3 | `python -m pytest tests/ -q` | **0** | **73 passed, 78 subtests passed** |
| 4 | `python canon/validation/validate_live_corpus.py --root .` | **0** | `error_count = 0` · 18 on disk · **17 accepted** · 1 source-evidence-only |

Live corpus totals across all 18 directories: 552 SourceKnowledge · 60 systems · 450 terms ·
59 concepts · 123 bindings.

### Mechanical confirmations

| Check | Result |
|---|---|
| no whole legacy lane branch merged | ✅ no merge commit; every artifact taken by path |
| no unrelated legacy source directory imported | ✅ only the two named directories and their two findings files |
| no historical 16-source decision or synthesis rewritten | ✅ `git diff` vs `main` touches no CANON-003/004 synthesis, decision or lane-checkpoint file |
| historical validator meaning preserved | ✅ byte-identical; 16 entries; output unchanged |
| every accepted live source has exactly one active v0.2 record | ✅ 17 accepted, 17 records, all `v0.2` |
| no accepted audit is stale | ✅ all 17 snapshots recompute clean |
| ids unique across the live corpus | ✅ 0 collisions over 552 / 60 / 450 / 59 / 123 |
| no source book, page or image committed | ✅ only `.md` and `.yaml`; no binary added |
| no GitHub Actions workflow | ✅ no `.github` directory |
| no model/API/generation spend | ✅ none; no source was re-opened |

**No source was re-opened.** Every adjudication was made from committed repository evidence, so the
task's re-opening stop condition never fired.

---

## 6. Counts, stated precisely

| Number | Value | Fixed? |
|---|---|---|
| CANON-003 accepted books | **16** | forever |
| CANON-004 method-test corpus | **16** | forever |
| Source directories in the repository | **18** | current |
| **Live accepted Canon after CANON-006** | **17** | current |
| Held as source evidence, blocked downstream | **1** | pending your decision |

---

## 7. Decision needed

1. **Approve or decline** `shared_primary_informant` (the proposal document). If approved, a small
   follow-on task writes *The Conversations*' audit record and takes the live Canon to 18. If
   declined, nothing breaks and it stays at 17.
2. **Review the live-corpus register and validator** as the new home for gate status.

Not started and not self-assigned: Wave 1, any Work-discovered source, RAG/retrieval, cross-source
concepts, Production IR.
