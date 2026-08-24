# CANON-006 — Controller brief

**Task:** CANON-006, adjudicate and integrate the two deferred reserve sources
**Date:** 25 Aug 2026 · **Branch:** `work/canon-006-reserves` · **Task-base:** `main` at `57fccaf`
**Status:** adjudication complete, plus the Controller correction pass applied · **needs_controller_review**
**Severity:** `LOCAL`. The approved lineage relation is applied; nothing further is pending.

---

## Bottom line

**Both reserves in. Live Canon is 18 accepted, with 18 active v0.2 audit records.**

Both recovered extractions were complete and passed every mechanical check unmodified. *Master
Shots* passed the gate directly. *The Conversations* was initially blocked — not by any defect, but
because it is Walter Murch talking, the corpus already held Murch's own book, and none of the seven
lineage relations could say that truthfully. The Controller approved a new dependence relation,
`shared_primary_informant`, which this pass applied. The source now holds an audit record that
states the relationship instead of hiding it.

**No reserve remains blocked merely because the vocabulary was missing a truthful relation.**

**The durable finding stands: different bibliographic authorship does not prove independent
intellectual origin.** The pair still cannot count as independent convergence with each other — and,
because independence is pairwise, each remains a good independent origin against everything else.

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

## 3. Reserve 12 — *The Conversations* · **ACCEPTED**, after the approved lineage relation

Michael Ondaatje, *The Conversations: Walter Murch and the Art of Editing Film*, Knopf, 2002. Third
Conversation, complete.

**Counts:** 27 SourceKnowledge · 3 SourceConceptSystems · 16 terms · 8 relationships · 3 concepts ·
6 OperationalBindings. **Mechanical validation: 0 errors.**

**There is nothing wrong with this extraction.** It is careful work — encoding positively verified
(0 replacement characters across 92,199 words), hedges preserved, speaker register recorded on every
object because SPEC-03 has no speaker field, and contamination disclosed on the object itself.

**Audit record:** `canon/audit/records/ondaatje-conversations-ch3.audit.yaml`,
`audit_record_version: v0.2`, snapshot computed after the source layer was frozen at `d57ac75`.

### The lineage question, and why it needed a new relation

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

Writing any of them would have been a false statement, so none was written and the source was held
pending your decision.

**This is harder than the case the rule already catches.** The Grammar books share authors, publisher
and series — visible on a title page. Here **the author field itself differs**, and no metadata
anywhere records that a book consists largely of another person's words. This pair passes every check
built on author, publisher or source id.

### Resolved — `shared_primary_informant`, approved and applied

The Controller approved the proposed relation and tightened its meaning to:

> The same practitioner's own claims constitute a primary or substantial knowledge source in both
> works despite different bibliographic authorship — for example, one work written by that
> practitioner and another substantially recording them in interview or conversation.

**Incidental quotation of the same person is not sufficient.** *Art & Fear* quotes Joan Didion and
Charles Eames in passing; that would not qualify. The relation applies where the practitioner's
claims are load-bearing in both, which the Egyptian-painting passage and `planarity` demonstrate
here.

The record now states the relationship instead of hiding it, and the record's evidence field explains
why. **Verdict: accepted downstream knowledge**, with the Murch pairing blocked from counting as
independent convergence.

### Other audit areas

**Representation integrity** contributes a loss shape the corpus had not seen. This is a *plate
book*: photographs grouped across facing pages, captions written to address several plates at once by
position. Reflowing destroyed that arrangement. Four caption blocks use "Overleaf:", "Above:",
"Right:", "center", "far right" to say which plate each clause describes, and in an EPUB those words
point at nothing. The worked case: a caption naming three films sits beside an image containing two
of them plus a black rectangle where a third plate was. **Neither the text nor the picture is
missing — the correspondence between them is gone**, and it is unrecoverable in an EPUB by
construction rather than by fault.

**Evidence origin** is the most consequential in the corpus, and it is a *speaker* gap rather than
the measurement gap Lane C found. The source has no single voice: a statement can be Murch asserting;
Ondaatje proposing and Murch assenting; Ondaatje asserting unchallenged; or the producer Rick
Schmidlin recalling in an inset. SPEC-03 has no speaker field, so the frozen extraction named the
speaker in each claim and quoted the source's own `O:`/`M:` markers. The audit records this without
proposing a new field — one source of this shape is not enough evidence to change SPEC-03.

**Application fit:** three consumers bound — `creative_ir` (2), `evaluation` (2), `governance` (2) —
plus a `human_workflow` candidate. Six bindings against 27 objects is correct rather than thin: much
of the chapter is testimony about one film under one set of constraints, true as testimony and never
a claim about films in general. The frozen extraction refused to promote those into principles Murch
did not state, and the audit does not undo that refusal.

**Technology contingency:** not applicable. Two objects carry `historical_claim` and one
`culturally_bounded`, all about past practice rather than surviving equipment.

---

## 4. The authoritative changes, and one thing withdrawn

### Applied — the approved lineage relation

| Artifact | Change |
|---|---|
| `canon/audit/AUDIT-GATE-v0.2.md` | `shared_primary_informant` added to the relation vocabulary and the dependence set, with the tightened definition and the explicit statement that incidental quotation does not qualify |
| `canon/knowledge/SPEC-05-knowledge-ontology.md` | Governance rule 5's dependence list goes from four relations to five. **The only authoritative spec change.** No other SPEC-05 semantics touched |
| `canon/validation/validate_audit_gate_v02.py` | one member added to `LINEAGE_RELATIONS`, one to `DEPENDENT_RELATIONS`. **No special code path** — symmetry enforcement, fail-closed verdicts and `independent_origins_ok()` all work unchanged, because the relation is symmetric like the existing four |
| `canon/audit/records/ondaatje-conversations-ch3.audit.yaml` | written, declaring the dependence |
| `canon/audit/records/murch-blink-p1-25.audit.yaml` | reciprocal entry added; verdict becomes `not_independent_of_named_sources`. **Its frozen source artifacts and snapshot are untouched** — the snapshot fingerprints source files, not the audit record |

SPEC-01, SPEC-03 and SPEC-04 are unchanged.

### Withdrawn — the live-corpus register

An earlier version of this branch added `canon/audit/LIVE-CORPUS.yaml`, a matching validator and its
tests, so a source could be recorded as present-but-not-cleared. **The Controller rejected it and it
has been removed**, together with the change that made audit coverage depend on it.

The objection is correct and worth recording: Audit Gate v0.2 already defines
`audit_status: evidence_insufficient` as a legitimate *written* audit outcome. A general rule that a
non-cleared source must have **no** record would contradict that existing contract — two mechanisms
for the same idea, disagreeing. And once the lineage relation existed, both reserves satisfied the
simple invariant anyway, so the registry solved a problem that had stopped existing.

Restored invariant: **every source directory holds exactly one active Audit Gate record.** No
replacement registry was designed. If a future task genuinely needs persistent source-evidence-only
state beyond the existing audit statuses, that is a separate design job.

### The historical validator was not touched

`validate_canon003_integrated.py` is byte-identical to `main`, its `ACCEPTED_BOOK_DIRS` still holds
exactly 16 entries, neither reserve appears in it, and its output is unchanged.

Two existing tests hard-coded `16` for the live record count. They now derive the invariant from the
source directories actually present, and no test asserts a floor on the live count. That is a
correction: those tests conflated the historical method-test corpus with the live corpus, which is
the exact distinction this task exists to draw. **The historical 16 belongs only to the historical
CANON-003/004 instrumentation.**

---

## 5. Verification — fresh from the final branch head

| # | Command | Exit | Result |
|---|---|---|---|
| 1 | `python canon/validation/validate_canon003_integrated.py --root .` | **0** | `error_count = 0` · **16 books**, 505 objects, 54 systems, 417 terms, 53 concepts, 111 bindings — *unchanged from `main`* |
| 2 | `python canon/validation/validate_audit_gate_v02.py --root .` | **0** | `error_count = 0` · **`record_count = 18`**, covering all 18 source directories |
| 3 | `python -m pytest tests/ -q` | **0** | **63 passed, 85 subtests passed** |

Live corpus totals across all 18 directories: 552 SourceKnowledge · 60 systems · 450 terms ·
59 concepts · 123 bindings.

### Mechanical confirmations

| Check | Result |
|---|---|
| both imported reserve directories tree-identical to their legacy source outputs | ✅ `git diff` against **both** the lane tip and the fresh checkpoint returns empty, for both directories |
| no legacy branch merged | ✅ no merge commit on the branch; every artifact taken by path |
| no unrelated legacy source imported | ✅ only the two named directories and their two findings files |
| no source book, page or image committed | ✅ every changed path is `.md`, `.yaml` or `.py`; no binary |
| no source re-opened | ✅ every adjudication made from committed evidence; the re-opening stop condition never fired |
| no source snapshot stale | ✅ all 18 recompute clean; Murch's snapshot untouched because only its audit record changed |
| no id collisions across the 18-source live corpus | ✅ 0 over 552 / 60 / 450 / 59 / 123 |
| SPEC-01, SPEC-02, SPEC-03, SPEC-04 unchanged | ✅ `git diff --stat` empty; SPEC-05 is the only spec changed |
| historical CANON-003/004 decisions and synthesis unchanged | ✅ no decision, synthesis, controller-brief or lane-checkpoint file touched |
| historical validator meaning preserved | ✅ byte-identical; 16 entries; neither reserve present; output unchanged |
| every source directory has exactly one active v0.2 record | ✅ 18 directories, 18 records, all `v0.2` |
| no GitHub Actions workflow | ✅ no `.github` directory |
| no model/API/generation spend | ✅ none |

---

## 6. Counts, stated precisely

| Number | Value | Fixed? |
|---|---|---|
| CANON-003 accepted books | **16** | forever |
| CANON-004 method-test corpus | **16** | forever |
| Source directories in the repository | **18** | current |
| **Live accepted Canon after CANON-006** | **18** | current |
| Active authoritative v0.2 audit records | **18** | current |
| Reserves still blocked for want of a truthful relation | **0** | — |

---

## 7. For review

The approved lineage relation is applied and nothing is pending a decision. What is worth your
attention on merge:

1. **The tightened definition of `shared_primary_informant`** as written into
   `canon/audit/AUDIT-GATE-v0.2.md` and SPEC-05, including the explicit statement that incidental
   quotation does not qualify.
2. **The withdrawal of the live-corpus register** (§4), and the reasoning that the existing
   `audit_status: evidence_insufficient` already covers the case a registry would have duplicated.
3. **The finding this task exists to preserve:** different bibliographic authorship does not prove
   independent intellectual origin. Both sources are accepted; only the pairing is blocked.

Not started and not self-assigned: Wave 1, any Work-discovered source, RAG/retrieval, cross-source
concepts, Production IR.
