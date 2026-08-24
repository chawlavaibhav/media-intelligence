# Controller Brief — CANON-001

**TASK:** CANON-001
**STATUS:** completed

**WHAT I DID:** Produced the first Canon source representation created directly under SPEC-03/04/05,
from Molly Bang's *Picture This* pp.42–91, without consulting the historical audit or the superseded
atom files. Inspected all 21 rendered figures before writing any claim, wrote the four
representation files, validated them by script against SPEC-03 rules 1–7, SPEC-04 rules 1–9 and the
SPEC-05 layer constraints, committed the frozen pre-audit checkpoint (`1383abe`), and only then
opened `AUDIT-molly-bang.md` for comparison.

**OBSERVED:**
- 55 SourceKnowledge objects, 6 SourceConceptSystems, 26 ontology terms (6 problems, 10 remedies,
  7 properties, 3 entities), 9 Layer-2 relations, 2 `source_specific_concept`s, 13 bindings
  (5 creative_ir, 4 evaluation, 1 benchmark, 2 governance, 1 production candidate).
- 30 of 55 objects (55%) carry no direct binding; 13 appear in neither a binding nor a bound system.
- 28 of 55 objects rest on text alone. Ten pages carrying claims have no rendered figure: 53, 61, 72,
  73, 82, 83, 85, 88, 89, 90. Principle 8 ("the larger an object is, the stronger it feels") has no
  inspectable figure at all.
- `claim_type` is `explicit_source_claim` for all 55 objects. Zero `source_interpretation`.
- `mechanism.stated_by_source` splits 27 true / 28 false. Caveats split 44 source-stated /
  51 extractor-observed.
- SPEC-03's worked example states of `scs_mb_001`'s whole-system claim that *"the source never
  states this as a general claim."* The source states it on page 58 and again across pages 58–60.
- All 18 historical atoms have a counterpart here. 37 fresh objects have no counterpart, concentrated
  in pp.81–91 (3 historical → 10 fresh) and in the unnumbered interludes and worked examples.
- The historical audit's one recovered object, `sk_mb_0019 depth_from_frame_exceeding_element`, has
  no counterpart in the fresh extraction.
- Historical audit: 21 Creative IR bindings against 19 objects, 0 governance, 0 production.
- 13 drafted intra-source relations were rejected by validation as outside SPEC-03's listed
  vocabulary and were removed rather than retyped. Four objects now carry an empty relation list.
- No object, system, term, relation or binding changed after the audit was opened. Checkpoint
  `1383abe` and the final file state are identical.

**INFERRED:**
- The SPEC-03/04 split is behaving as designed for the first time. The fresh pass independently
  avoided all four distortions the migration audit catalogued, without sight of it, and produced the
  unbound-majority profile SPEC-04 predicts. The historical 21-bindings-for-19-objects ratio looks
  like SPEC-02's coupled rule surviving the migration.
- The numbered principles are roughly a third of what this source teaches. A
  one-object-per-numbered-principle convention would miss the combination rule, the association
  mechanism, the whole closing section on space, and the author's own refusal to name a principle.
- The ontology layer is aimed at a different kind of source than this one. It indexes problems and
  remedies; this source is principles, and its real vocabulary sits in `property` and `entity` terms
  outside the failure/repair spine the join depends on.
- Missing the recovered figure-only object suggests this pass used figures to verify text-derived
  claims rather than as independent evidence. That is a method property worth knowing before the
  same method runs over ten more books.

**SURPRISES:**
- A frozen spec contains a factual error about this source, in the example that teaches the
  origin-marking convention — and the error runs in the under-crediting direction, attributing to the
  extractor something the author stated plainly.
- Bang states her own system-level claim explicitly. The extraction records it as `source_explicit`
  where SPEC-03 assumed synthesis.
- Two governance bindings and one benchmark binding came out of a picture-book craft text that the
  historical pass read as producing neither.

**FAILURES / BLOCKERS:** None. No stop gate fired.

**ASSUMPTIONS CHALLENGED:** Entry **3** — its review trigger ("after five systems exist") has fired;
six systems now exist from one source, and finding B in the findings bears on its falsifier. Entry
**2** further weakened (`sk_mb_c001_0003`). Entry **1b** weakly supported in shape, though its stated
falsifier remains untouched — no binding has yet been revised. Entry **14** untouched.

**LOCAL IMPLICATIONS:** A granularity convention should be settled before a second source: two
defensible conventions produced 19 and 55 objects from the same 50 pages. The ten missing figure
pages should be rendered before this source is called complete.

**CROSS-STREAM IMPLICATIONS:** Tagged **CROSS_STREAM** — `bnd_mb_c001_0010`. The source constructs
four near-minimal pairs with stated expected readings (p55/p57, p63/p65, p70/p71, p75/p77), which is
the shape a creative-fitness benchmark item needs, and EVAL-001 is designing a Capability Battery V0
now. Two of the four are not strictly isolated and the binding records which. The expected readings
are the author's judgements, not measurements, so they are candidate expected answers requiring
independent validation — never ground truth. Proposed, not acted on. No
`PROPOSED-INTEGRATION-CHANGE` filed, because this proposes an input to another stream's approved
task rather than a change to shared truth; say the word if you want one filed.

**ARCHITECTURAL IMPLICATIONS:** None that triggered a stop. The schema represented everything this
source produced, including its uncertainties. Two representational gaps are reported as findings
rather than stops, because SPEC-03 could record the material honestly in both cases: no relation type
for claims that are adjacent but not logically related, and no Layer-1 term kind for a principle.

**DECISIONS NEEDED FROM CONTROLLER:**
1. Correct SPEC-03's `scs_mb_001` worked example. I may not edit a frozen spec.
2. Add or omit the missed `source_interpretation` object (findings §6). I did not back-fill it
   deliberately; the correction is cheap either way.
3. Is `distinct_from` a local decision? Two negative findings are sitting unwritten.
4. Granularity convention before the next source.
5. Whether to route the benchmark binding to EVAL-001.

**FILES CREATED / MODIFIED:**
- `canon/knowledge/current/molly-bang/source-knowledge.yaml`
- `canon/knowledge/current/molly-bang/source-concept-systems.yaml`
- `canon/knowledge/current/molly-bang/ontology-mappings.yaml`
- `canon/knowledge/current/molly-bang/operational-bindings.yaml`
- `canon/findings/CANON-001-current-schema-extraction-findings.md`
- `canon/tasks/CANON-001-CONTROLLER-BRIEF.md`

Nothing outside `canon/` was touched. No historical atom or audit file was modified. The four
inconsistencies found in files I do not own (SPEC-03's `member_of_system`, SPEC-04's `fo_`/`ro_`
identifiers, the curriculum's stale ✓, the decision log's broken link) are recorded in the findings
and left unrepaired.

**RECOMMENDED NEXT STEP:** A recommendation, not a next action taken. Before scaling ingestion,
settle the granularity convention and correct the SPEC-03 example, since both compound across every
future source. A second extraction under the settled convention — Williams is the cheapest test,
being short and authoring its own failure and repair lists — would show whether the thin ontology
yield here is a property of this source or of the layer.

**CONFIRMATION:** No unapproved next strategic step was started. CANON-002 was not begun, no second
source was touched, no experiment was run or extended, no schema was edited, and no file outside
Canon's ownership was modified. Disclosed for completeness: SPEC-01's opening section and field names
were read during the Phase 0 governance review, before extraction began, so the intended "bindings
last" isolation was partial rather than complete for this run.
