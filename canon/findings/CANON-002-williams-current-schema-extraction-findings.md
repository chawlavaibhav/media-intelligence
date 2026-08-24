# CANON-002 — Williams proximity: second current-schema extraction, findings

**Date:** 24 Aug 2026 · **Task:** `canon/tasks/CANON-002.md` · **Branch:** `work/canon`
**Source:** Robin Williams, *The Non-Designer's Design Book*, 3rd ed., ch.2 Proximity, printed pp.15–32
**Pre-history checkpoint:** `3b933ef`

---

## 1. Phase 0 — provenance gate: PASSED

| Check | Result |
|---|---|
| Text source readable | Yes, 29,134 bytes, UTF-8 |
| Matching visual source available locally | Yes — a Non-Designer's Design Book PDF already on the local disk |
| Edition match | PDF `/Title` is `0321563077.pdf`; that ISBN is the 3rd edition (Peachpit, 2008). 217 pages, InDesign CS3, created Feb 2008 |
| Page offset established | PDF page = printed page + 1 |
| Chapter boundary confirmed | Printed 15–32 = PDF 16–33; printed 33 (PDF 34) begins ch.3 Alignment |
| Text↔visual match | Normalised character counts identical (28,597 both sides); 152 of 152 sentences over 60 characters found verbatim in the PDF |
| Rendering permitted and non-committing | Rendered to session scratchpad at 110 dpi; nothing committed |

**Provenance disclosure.** The local PDF's filename carries a `libgen.li` marker, indicating where
that copy originated. It was already present on the local disk; CANON-002 permits read-only use of
already-available local material and forbids acquiring anything new, and nothing was acquired,
redistributed or committed. Recording it because Phase 0 is a provenance gate and omitting the
observation would defeat its purpose. **NOT VERIFIED:** whether that copy is licensed. That is a
question for the Controller, not for this extraction.

---

## 2. The headline result: plain text destroys this chapter's central evidence

This is the finding CANON-002's mandatory visual pass was designed to surface, and it overturns a
recorded historical verdict.

**OBSERVED.** The chapter's opening demonstration is two flower lists side by side. On the page,
they are identical in words, word order, typeface, colour, box tint and box size, and differ by
exactly one thing: the right-hand list has a blank line after its sixth item. In
`canon/sources/williams-proximity-p15-32.txt` the two lists appear consecutively and are
**character-for-character identical**. The separating blank line is gone.

The same holds for the Correspondences list on printed p.19, the chapter's second grouping
demonstration: both columns are identical in the text file.

**Consequence.** Williams's prose says the reader knows the last four flowers are different
"because they are physically separated from the rest of the list." Read from the text file alone,
that sentence describes evidence the file does not contain. A text-only extractor must take the
claim on trust or record it as unsupported.

**This directly contradicts the historical pass.** `FINDINGS-04-williams-proximity-pass1.md`,
under "Visual-context status", records:

> "No unresolved items. The before/after pairs survive text extraction well enough to judge, with
> one exception: the dance-postcard example…"

The before/after pairs do **not** survive text extraction. The two that carry the chapter's core
claim are wholly destroyed by it. The disagreement is not interpretive: it is checkable in thirty
seconds by opening the text file and looking at the two lists.

**INFERRED.** A text-only extractor cannot reliably assess its own visual completeness, because the
missing evidence leaves no trace. The historical pass reported no unresolved visual items while
working from a file in which the chapter's central demonstration had been flattened. That is a
strong argument for the visual pass being a precondition rather than an enhancement — at least for
sources whose subject is spatial.

**Scope limit.** One chapter of one source. This says nothing about how other sources survive text
extraction, and CANON-001's source largely did survive it.

*(Minor: FINDINGS-04 cites the dance postcard as p24; it is printed p23.)*

---

## 3. Did the method travel from Bang to Williams?

| | CANON-001 (Bang) | CANON-002 (Williams) |
|---|---|---|
| SourceKnowledge objects | 55 | 31 |
| Pages | 50 | 18 |
| Objects per page | 1.10 | 1.72 |
| Systems | 6 | 4 |
| Ontology terms | 26 | 23 |
| — of which problems | 6 | **10** |
| — of which remedies | 10 | **9** |
| Objects with source-stated problems | 6 of 55 (11%) | **9 of 31 (29%)** |
| Objects with source-stated remedies | 9 of 55 (16%) | **20 of 31 (65%)** |
| Bindings | 13 | 8 |
| Objects resting on text alone | 28 of 55 (51%) | 8 of 31 (26%) |
| `mechanism.stated_by_source` true | 27 of 55 (49%) | 6 of 31 (19%) |

**Yes, with two clear differences.**

**Williams yields far richer source-authored problem and remedy vocabulary.** Two-thirds of her
claims arrive with a remedy she wrote herself, against one in six for Bang. The reason is
structural: every principle chapter closes with sections headed *The basic purpose*, *How to get
it* and *What to avoid*. The last is a failure list; the middle is a diagnostic plus repairs. The
CANON-001 finding that "the ontology layer is aimed at a different kind of source than this one"
is supported: it is aimed at sources shaped like Williams.

**Williams almost never gives a mechanism.** Only 19% of her claims explain why, against 49% for
Bang. Bang argues from gravity, association and physiology; Williams asserts and demonstrates. She
is richer in what to do and much poorer in why it works.

**Caution.** Two sources. This is a contrast between two books, not a taxonomy of sources. It
becomes a claim about kinds of source only if a third and fourth behave consistently.

---

## 4. Did the V0 granularity rule work?

**Yes, and it was decidable without inventing exceptions.** The rule — split when a claim can be
retrieved, supported, contradicted or qualified independently; do not split for a further example,
explanation or restatement — resolved every case encountered. The ambiguous ones, recorded as
CANON-002 requires:

1. **Perceptual fusing versus inferred relationship** (`0003` / `0004`). Williams states both in one
   sentence pair. Split, because one can be contradicted without the other: elements could merge
   visually while the viewer infers no semantic relationship. That distinction is the one that
   matters for detecting unintended relationships, so collapsing it would lose the useful part.
2. **Equal gaps versus an enlarged gap** (`0011` / `0013`). Same variable, opposite settings, stated
   eleven pages apart with different demonstrations. Split, and they are recorded as contradicting
   each other.
3. **The What-to-avoid list.** Five imperatives closing the chapter. Most are the prescriptive form
   of a claim already stated, so under the rule they are restatements. They were folded into their
   parent objects as `source_stated_remedies` rather than becoming objects. The one exception is
   "avoid too many separate elements", which carries the three-to-five threshold and is the only
   numeric decision rule in the chapter; that became `0027`.
4. **All capitals** (`0020`). Williams makes two claims in one passage: all caps are hard to read
   (legibility) and all caps consume the white space needed for rest (spatial). The chapter argues
   only the second. The spatial claim became the object; the legibility assertion is recorded as a
   `source_stated` caveat. The historical pass made the opposite choice — see §6.

**No new policy was invented and no case forced a rule change.**

---

## 5. Comparison with the sealed historical work

Opened only after checkpoint `3b933ef`. **No fresh object, system, term, relation or binding was
altered, added or removed afterwards.**

**Found by both — 11 of the historical 14.** `proximity_implies_relationship`, `eye_stop_count_threshold`,
`reading_path_requires_definite_start_and_end`, `competing_emphasis_destroys_entry_point`,
`trapped_white_space_separates_related_elements`, `equal_spacing_signals_equal_relationship`,
`do_not_fill_space_for_its_own_sake`, `all_caps_reduces_legibility` (differently framed, §6),
`clarity_outranks_thematic_expression`, `organisation_increases_readership_and_recall`,
`group_information_before_designing`.

**Found only by the fresh pass — 20 objects.** Concentrated in three areas:
- **Gap magnitude as structure.** `0012` (greater distance signals subordinate status) and `0013`
  (an enlarged gap marks one item as different in kind) have no historical counterpart. The
  historical pass has `equal_spacing_signals_equal_relationship` only. The p.21/p.22 near-minimal
  pair, which is where the graded reading is demonstrated, appears not to have been used.
- **The pre-attentive claim** (`0005`) — that grouping is read instantly and stays legible when
  content cannot be read clearly. This is the chapter's strongest testable claim and has no
  historical counterpart.
- **Method and scope claims** — indentation as a substitute for space (`0019`), grouping requiring
  size/weight/placement changes (`0017`), subsidiary type at 7–8 point (`0018`), proximity applied
  first among four principles (`0023`), web application (`0024`), uniform arrangement misstating
  importance (`0025`).

**Found only historically — 3 objects, and they share one cause.**
`overlap_graphic_past_the_edge`, `straight_corners_read_stronger_than_rounded` and
`reversed_type_needs_a_robust_face` all come from the same passage: the four "other things I did
along the way" Williams lists on printed p.18 after fixing the newsletter flag.

**My visual pass classified that whole list as confounds** — evidence that the before/after
comparison is not isolated — and recorded it in the ledger as `author_flagged_confounds: true`. It
did not occur to me that the confounds were also claims. They are: "straight corners give a
cleaner, stronger look" and "reversed type needs a robust face so it won't fall apart when printed"
are things Williams teaches, and SPEC-03 has no usefulness test that would exclude them.

**Not back-filled, deliberately.** This mirrors CANON-001's page-87 miss and the Controller's
decision 2 of 24 Aug 2026 to preserve that miss as evidence rather than patch it. The same logic
applies more strongly here, because this is a *systematic* failure mode rather than a single
oversight: **a claim that also functions as a methodological confound gets filed as method
metadata and drops out of the knowledge.** Patching three objects would hide a rule that will
recur on every source with a self-narrating author. Controller direction requested.

---

## 6. Substantive disagreements with the historical record

Preserved, not resolved.

**A. Visual completeness.** §2. The historical "no unresolved items" verdict is contradicted by
direct inspection. Fresh evidence is stronger: it rests on looking at the pages.

**B. All capitals — legibility or space.** Historical `rw_008` is `all_caps_reduces_legibility` with
`mechanism_absent`. Fresh `0020` is `all_caps_consumes_the_space_grouping_needs` with
`mechanism_given`. Williams states both in the same passage; the chapter argues only the spatial
one, and it is the one that connects to the rest of her material. Both readings are defensible and
each demotes the other to a caveat. **UNKNOWN** which is the better convention when a source states
two claims in one passage and argues one.

**C. Governance — a rejection re-opened on different evidence.** The historical audit records a
governance binding *considered and rejected*, on the grounds that
`group_information_before_designing` has no named consumer from SPEC-04's permitted list. The fresh
pass creates one (`bnd_rw_c002_0006`, `governance_consumer: rule_application`).

This is not a contradiction of the audit's reasoning. It rests on material the historical pass did
not extract: `0023`, Williams's statement that the principles must be taken one at a time starting
with proximity because the others achieve nothing until the spacing is right. That is directly a
statement about whether a principle may be applied in isolation, which is what `rule_application`
governs. The audit rejected a weaker candidate; the fresh pass had a stronger one available.

**Precision defect in the fresh file, recorded not fixed.** `bnd_rw_c002_0006`'s rationale leans on
the ordering constraint, but its `source_knowledge_refs` list only `0021` and `0022`. `0023` is
reachable only through `source_system_refs: [scs_rw_c002_003]`. The binding resolves, but a reader
checking its direct references will not find the claim the rationale rests on.

**D. An architectural observation the historical pass caught and the fresh pass missed.** The audit
records that `reading_path_requires_definite_start_and_end` needs a composition to have a definite
**end** — the viewer must know when they are finished — and that SPEC-01's `creative.hierarchy` is a
rank-ordered list which can express "noticed first" but not "finished". It notes Lupton
independently describes hierarchy as a traversal rather than a ranking.

The fresh pass extracted the same claim (`0007`, including "from a definite beginning to a definite
end") and bound it to `creative.hierarchy` — **without noticing that the field cannot represent the
second half of it.** That is a genuine miss of an architectural implication, and the historical work
is better here. It is recorded, not acted on: the Charter forbids schema changes and CANON-002 lists
schema inadequacy as a stop condition, but this was found *after* the checkpoint, in comparison,
and does not block the completed extraction.

**E. Structure of the systems.** Historical: one system plus one explicit stub. Fresh: four systems,
no stub. The historical `scs_wil_001` (members: proximity, trapped white space, equal spacing, don't
fill space) is split across three fresh systems. The historical stub for "the four principles"
records that only proximity was processed; the fresh pass instead carries that incompleteness as a
caveat on `0023`. Both make the gap visible; the stub is the more findable device.

---

## 7. Bearing on the assumptions register

Evidence, not resolution.

- **Entry 3 — SourceConceptSystems are required.** Its falsifier is that every system proves
  reconstructible from its members' `intra_source_relations`. `scs_rw_c002_002` (gap magnitude) is a
  candidate falsifier: its content is largely carried by contradicts/qualifies relations already on
  `0011`, `0012` and `0013`. `scs_rw_c002_003` (the working procedure) is not — procedural order and
  the conflict about invented taxonomy have nowhere to live on a member. **Mixed evidence.**
- **Entry 1b — the Source/Binding split.** Second source, same profile: 8 bindings against 31
  objects, most objects unbound. The stated falsifier (fifty bindings, none revised) remains
  untouched — 21 bindings now exist across both extractions and none has been revised.
- **Entry 2 — atoms are sufficient.** Unchanged by this source.
- **Entry 14 — corpus representativeness.** Untouched. Two chapters say nothing about forty books.

---

## 8. Open items for the Controller

1. **The three missed p.18 claims** — add under a follow-up task, or preserve the miss as CANON-001's
   was? The failure mode is systematic, not incidental.
2. **The confound/claim collision** — should the visual-pass method be amended so that author-flagged
   confounds are also tested as candidate claims? That is a change to the visual-pass method, which
   CANON-002 lists as a human approval trigger, so it is not made here.
3. **The `creative.hierarchy` traversal limitation** (§6D) — now independently observed by the
   historical Williams pass, the Lupton pass, and this extraction's source. Three sightings.
4. **All-caps convention** (§6B) — which claim wins when a source states two in one passage and
   argues one.
5. **The benchmark stimulus** (`bnd_rw_c002_0007`) — the flower pair is the most strictly isolated
   comparison found in either extraction. Same labelling requirement as the CANON-001 pairs.
6. **Provenance of the local PDF** (§1) — not a blocker for this task; the Controller may want a
   position before further chapters are rendered from it.
