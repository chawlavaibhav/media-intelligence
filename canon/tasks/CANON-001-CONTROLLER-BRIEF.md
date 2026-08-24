# Controller Brief — CANON-001

**TASK:** CANON-001
**STATUS:** completed — **APPROVED by Controller, 24 Aug 2026**

**HUMAN SUMMARY:**
The first clean extraction under the new schema worked, and it produced a result worth acting on:
one of the frozen rulebooks, SPEC-03, is factually wrong about this book. Its teaching example says
Molly Bang never states her big claim in general terms, so it credits that claim to us. She states
it plainly on page 58 and again over pages 58–60. The example that teaches "who said this" gets this
source backwards, in the direction of under-crediting the author. Separately, the new
knowledge/bindings split behaved as designed for the first time — more than half the extracted
knowledge carries no product use at all, where the old migrated version had roughly one binding per
object. Two things went wrong on my side: I missed a claim the old audit found in a figure, and I
deliberately did not back-fill it, because patching it would hide a real limitation in how I read
figures. Five decisions are waiting on you; the granularity one matters most, because two defensible
conventions produced 19 objects and 55 objects from the same fifty pages, and that gap multiplies
across every future book.

---

## Controller decisions — 24 Aug 2026

All five questions raised in this brief are answered. Recorded verbatim in substance; none required
a change to the extraction, and none was made.

| # | Decision | Effect on Canon |
|---|---|---|
| 1 | SPEC-03's Molly Bang worked example is **confirmed incorrect** and will be corrected by the Controller. | Canon does not edit it. Finding stands as filed. |
| 2 | **Do not back-fill** the missed page-87 figure-only claim. Preserve CANON-001 as evidence of the miss. A later visual-completeness task will handle it explicitly. | The gap stays open on purpose. Do not treat it as an outstanding defect. |
| 3 | `distinct_from` **is permitted** in the SPEC-05 ontology layer, being already part of that relation vocabulary. **Not** permission to use it inside SPEC-03 `intra_source_relations`. | Grants the authority this brief asked for, and closes the door I was worried about. |
| 4 | **V0 granularity rule:** split into a separate SourceKnowledge object when a claim can meaningfully be **retrieved, supported, contradicted or qualified independently**. Do not split merely because there is another example, explanation or restatement. Test the rule on the next source rather than targeting an object count. | Standing rule for the next extraction. |
| 5 | Bang's visual minimal-pair candidates **may** be passed to Eval's deferred creative-evaluation list, clearly marked as source-asserted expected readings rather than validated human ground truth. | `PROPOSED-INTEGRATION-CHANGE-CANON-001.md` moved to APPROVED with the marking requirement recorded. |

### What was deliberately not done in response

**Decision 3 was not applied retroactively.** It makes the two negative findings in
`findings/CANON-001-current-schema-extraction-findings.md` §8 writable —
`space_reads_as_flat` vs `reads_as_floating` (both depth failures, unrelated mechanisms) and
`monotony_of_relentless_repetition` vs `boring_and_heavy` (currently recorded as `related_to`).
Neither was written. CANON-001 is approved, and adding ontology content to an approved artifact was
not part of the instruction. Both remain available as a small follow-up if wanted.

**Decision 4 was not applied retroactively either, and compliance is NOT VERIFIED.** The rule was
issued after this extraction was frozen. The convention actually used was "one object per distinct
claim", which is close to the rule but not identical, and the 55 objects have **not** been re-audited
against the rule's four-part test. The Controller directed that the rule be tested on the next
source, so no re-audit was performed. Do not read this brief as claiming the 55 objects satisfy it.

---

**WHAT I DID:** Extracted Molly Bang, *Picture This* pp.42–91 directly under SPEC-03/04/05 without
consulting the historical audit or the superseded atom files. Inspected all 21 rendered figures
before writing any claim, validated the four output files by script against SPEC-03 rules 1–7,
SPEC-04 rules 1–9 and the SPEC-05 layer constraints, committed the frozen pre-audit checkpoint
(`1383abe`), and only then opened `AUDIT-molly-bang.md` to compare.

**OBSERVED:**
- Produced 55 SourceKnowledge objects, 6 SourceConceptSystems, 26 ontology terms (6 problems,
  10 remedies, 7 properties, 3 entities), 9 Layer-2 relations, 2 `source_specific_concept`s,
  13 bindings (5 creative_ir, 4 evaluation, 1 benchmark, 2 governance, 1 production candidate).
- 30 of 55 objects (55%) carry no direct binding. 13 appear in neither a binding nor a bound system.
- 28 of 55 objects rest on text alone. Ten pages carrying claims have no rendered figure: 53, 61, 72,
  73, 82, 83, 85, 88, 89, 90. Principle 8 ("the larger an object is, the stronger it feels") has no
  inspectable figure at all.
- `claim_type` is `explicit_source_claim` for all 55 objects. Zero `source_interpretation`.
- SPEC-03's worked example states of `scs_mb_001`'s whole-system claim: *"The source never states
  this as a general claim."* The source states it on page 58 and again across pages 58–60.
- All 18 historical atoms have a counterpart here. 37 fresh objects have none, concentrated in
  pp.81–91 (3 historical → 10 fresh) and in the unnumbered interludes and worked examples.
- The audit's one recovered object, `sk_mb_0019 depth_from_frame_exceeding_element`, has no
  counterpart here.
- Historical audit: 21 Creative IR bindings against 19 objects, 0 governance, 0 production.
- 13 drafted intra-source relations were rejected by my validator as outside SPEC-03's listed
  vocabulary and were removed rather than retyped. Four objects now carry an empty relation list.
- No object, system, term, relation or binding changed after the audit was opened. Checkpoint
  `1383abe` and the final file state are identical.

**INFERRED:**
- The SPEC-03/04 split is behaving as designed for the first time. The fresh pass independently
  avoided all four distortions the migration audit catalogued, without sight of it, and produced the
  unbound-majority profile SPEC-04 predicts. The historical 21-for-19 ratio looks like SPEC-02's
  coupled rule surviving the migration rather than a property of the source.
- The numbered principles are roughly a third of what this source teaches. A
  one-object-per-numbered-principle convention misses the combination rule, the association
  mechanism, the whole closing section on space, and the author's own refusal to name a principle.
- The ontology layer is aimed at a different kind of source than this one. It indexes problems and
  remedies; this source is principles, and its real vocabulary sits in `property` and `entity` terms
  outside the failure/repair spine the book-to-failure join depends on.
- Missing the figure-only object suggests this pass used figures to verify text-derived claims rather
  than as independent evidence — a method property, not a one-off slip.

**SURPRISES / BELIEF UPDATES:**
- A frozen spec contains a factual error about this source, inside the example that teaches the
  origin-marking convention. Do not take SPEC-03's worked examples as verified against their sources.
- Bang states her own system-level claim explicitly, so it is recorded `source_explicit` where
  SPEC-03 assumed extractor synthesis. The next worker should check this per source rather than
  assuming synthesis is the default.
- Two governance bindings and one benchmark binding came out of a picture-book craft text the
  historical pass read as producing neither. "This source yields no governance material" was a
  property of the old extraction rule, not of the source.

**FAILURES / BLOCKERS:** None. No stop gate fired. One self-caught error during the run: I used
`related_to`, a SPEC-05 term-layer relation, inside SPEC-03's `intra_source_relations`, which has a
different closed vocabulary. My validator caught it; 7 were re-expressed correctly and 13 removed.

**UNKNOWN / NOT VERIFIED:**
- Whether the missed object `depth_from_frame_exceeding_element` should exist. Re-inspecting p87
  after the comparison, the audit's observation looks defensible from the figure, but I did not add
  it and have not verified it as a claim.
- Whether the thin ontology yield (6 problems, 10 remedies from 55 claims) is a property of this
  source or of the ontology layer. One source cannot tell them apart.
- Whether any of this holds beyond picture-book illustration. The source's stated domain is
  picture books; nothing here was tested at feed-creative crop, scale or viewing duration.
- Whether the four benchmark pairs predict real viewer response. The expected readings are the
  author's judgements. No human response data exists.

**ASSUMPTIONS CHALLENGED:** Entry **3** — its review trigger ("after five systems exist") has fired;
six systems now exist from one source, and the missing relation vocabulary bears on its falsifier.
Entry **2** further weakened (`sk_mb_c001_0003` is a relationship that had to become its own object).
Entry **1b** weakly supported in shape only — its stated falsifier is untouched, since no binding has
yet been revised. Entry **14** untouched.

**LOCAL IMPLICATIONS:** A granularity convention should be settled before a second source. The ten
missing figure pages should be rendered before this source is called complete.

**CROSS-STREAM IMPLICATIONS:** Tagged **CROSS_STREAM**. Filed as
`canon/PROPOSED-INTEGRATION-CHANGE-CANON-001.md`. Bang builds four near-minimal pairs with stated
expected readings (p55/p57, p63/p65, p70/p71, p75/p77). Having read EVAL-001's Controller
clarification §2, which places creative-judgement evaluation outside Capability Battery V0, this is
proposed **only** for EVAL's deferred-creative-dimensions list, not for V0. Two of the four pairs are
not strictly isolated and the proposal records which.

**ARCHITECTURAL IMPLICATIONS:** None that triggered a stop. The schema represented everything this
source produced, including its uncertainties. Two representational gaps are reported as findings, not
stops, because SPEC-03 could record the material honestly in both cases: no relation type for claims
that are adjacent but not logically related, and no Layer-1 term kind for a principle.

**DECISIONS NEEDED FROM CONTROLLER:** None outstanding. All five were answered on 24 Aug 2026 — see
the Controller decisions table above. One optional follow-up remains open, not blocking: whether to
write the two `distinct_from` relations that decision 3 now permits.

**EVIDENCE WORTH HUMAN INSPECTION:**
- `canon/knowledge/SPEC-03-source-knowledge.md` lines 189–201 against page 58 of
  `canon/sources/molly-bang-principles-p42-91.txt`. This is decision 1 and takes two minutes.
- `canon/sources/figures/p55-55.jpg` and `p57-57.jpg` side by side — the cleanest of the four
  benchmark pairs, and the fastest way to judge whether that material is worth anything to Eval.

**FILES CREATED / MODIFIED:**
- `canon/knowledge/current/molly-bang/source-knowledge.yaml`
- `canon/knowledge/current/molly-bang/source-concept-systems.yaml`
- `canon/knowledge/current/molly-bang/ontology-mappings.yaml`
- `canon/knowledge/current/molly-bang/operational-bindings.yaml`
- `canon/findings/CANON-001-current-schema-extraction-findings.md`
- `canon/PROPOSED-INTEGRATION-CHANGE-CANON-001.md`
- `canon/HANDOFF.md`
- `canon/tasks/CANON-001-CONTROLLER-BRIEF.md`

Nothing outside `canon/` was modified. No historical atom or audit file was touched. Four
inconsistencies in files I do not own are recorded in the findings and left unrepaired: SPEC-03's
`member_of_system`, SPEC-04's `fo_`/`ro_` identifier examples, the curriculum's stale ✓ on this
source, and a broken link in `coordination/DECISION-LOG.md`.

**RECOMMENDED NEXT STEP:** A recommendation, not an action taken. Settle the granularity convention
and correct the SPEC-03 example before scaling ingestion, since both compound across every future
source. Then a second extraction under the settled convention — Williams is the cheapest test, being
short and authoring its own failure and repair lists — would show whether the thin ontology yield
here is a property of this source or of the layer.

**EPISTEMIC CHECK:** Counts, page numbers and file states in OBSERVED were produced by script or by
direct inspection and are reproducible from the named files. Interpretations are confined to
INFERRED. Gaps are listed under UNKNOWN / NOT VERIFIED rather than filled. No recommendation in this
brief is presented as a decision, and the cross-stream item is filed as a proposal. One disclosure:
SPEC-01's opening section and field names were read during the Phase 0 governance review, before
extraction began, so the intended "bindings last" isolation was partial rather than complete.

**CONFIRMATION:** No unapproved next strategic step was started. CANON-002 was not begun, no second
source was touched, no experiment was run or extended, no schema was edited, and no file outside
Canon's ownership was modified.
