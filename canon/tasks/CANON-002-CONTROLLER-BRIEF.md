# Controller Brief — CANON-002

**TASK:** CANON-002
**STATUS:** completed

**HUMAN SUMMARY:**
The Phase-0 gate passed and the extraction ran to completion, but the mandatory visual pass produced
a result that matters more than the extraction itself: for this chapter, the plain-text file destroys
the evidence the chapter is built on. Williams's opening demonstration is two flower lists that differ
only by one blank line; in our text file they are character-for-character identical, so her
explanation describes something the file does not contain. That directly contradicts the historical
Williams pass, which recorded "no unresolved items" for visual completeness. A text-only extractor
cannot see what it is missing, because the missing evidence leaves no trace. The method otherwise
travelled well from Bang to Williams and the new granularity rule held without exceptions. I missed
three claims the historical pass caught, all from one passage, and the cause is systematic rather
than careless: I classified Williams's own list of "other things I changed" as methodological
confounds and never tested them as claims. I have not back-filled them, following your CANON-001
precedent, because the pattern is worth more than the three objects.

**WHAT I DID:** Verified provenance of a locally available Non-Designer's Design Book PDF against the
repository text, ran an independent visual pass over all 18 pages before writing any object, produced
the five fresh files under SPEC-03/04/05 using the V0 granularity rule, validated them by script,
committed the pre-history checkpoint `3b933ef`, and only then opened the sealed historical material.

**OBSERVED:**
- Provenance verified: PDF `/Title` = `0321563077` (3rd edition ISBN), 217 pages; printed page = PDF
  page − 1; printed 15–32 = PDF 16–33; printed 33 begins ch.3. Normalised text identical in length
  (28,597 chars) and 152 of 152 sentences over 60 characters matched verbatim.
- The two flower lists on printed p.15 are identical in the repository text file. The Correspondences
  lists on p.19 are also identical. On the page each pair differs by inserted blank lines.
- `FINDINGS-04-williams-proximity-pass1.md` records under Visual-context status: "No unresolved items.
  The before/after pairs survive text extraction well enough to judge."
- Produced 31 SourceKnowledge objects, 4 SourceConceptSystems, 23 ontology terms (10 problems,
  9 remedies, 4 properties), 8 relations including 2 `distinct_from`, 2 `source_specific_concept`s,
  8 bindings. All validate against SPEC-03 rules 1–7, SPEC-04 rules 1–9, SPEC-05 constraints.
- Williams: 65% of objects carry a source-written remedy and 29% a source-named problem. Bang: 16%
  and 11%. Williams states a mechanism in 19% of objects; Bang in 49%.
- 11 of the historical 14 objects have a fresh counterpart. 20 fresh objects have no historical
  counterpart. 3 historical objects have no fresh counterpart, all from printed p.18.
- Historical: 12 Creative IR bindings against 14 objects. Fresh: 2 against 31.
- The historical audit records that `creative.hierarchy` is a rank-ordered list and cannot express
  "the viewer knows when they are finished". The fresh pass extracted the same claim and bound it to
  that field without noticing the limitation.
- No fresh object, system, term, relation or binding changed after the checkpoint.

**INFERRED:**
- A text-only extractor cannot audit its own visual completeness for a spatially-argued source. The
  historical pass reported full visual coverage while working from a file with the chapter's central
  demonstration flattened out of it.
- The method travels, with the profile shifting by source shape rather than breaking. Williams's
  chapter-closing sections — *The basic purpose*, *How to get it*, *What to avoid* — are why her
  problem and remedy yield is roughly four times Bang's. This supports CANON-001's inference that the
  ontology layer suits sources shaped like Williams and sits awkwardly on sources shaped like Bang.
- My three misses share one cause worth naming: when a claim also functions as a confound in a
  before/after comparison, the visual pass files it as method metadata and it never reaches the
  extraction. That will recur on any self-narrating author.

**SURPRISES / BELIEF UPDATES:**
- I expected the visual pass to add coverage. It instead invalidated a historical completeness
  verdict. Do not treat prior "visual status: no unresolved items" statements as checked.
- Williams gives remedies but almost never mechanisms — nearly the inverse of Bang. Before this I
  would have assumed a practical design manual would explain itself more, not less.
- The historical pass beat the fresh pass on one thing: it noticed an architectural limitation in
  `creative.hierarchy` that I extracted the evidence for and walked straight past.

**FAILURES / BLOCKERS:** None; no stop gate fired. Two self-caught errors during the run: I used
`depended_on_by` and, in CANON-001, `related_to` inside SPEC-03 `intra_source_relations`, where
neither belongs. Both were caught by the validator before the checkpoint.

**UNKNOWN / NOT VERIFIED:**
- Whether the three missed p.18 claims should exist. The source supports them; the omission was a
  classification decision, not a factual error.
- Whether the Bang/Williams contrast is a property of source kinds or of two particular books. Two
  data points.
- Whether the local PDF copy is licensed. Its filename carries a `libgen.li` marker. It was already
  on the disk, was used read-only, and nothing was acquired or committed. Flagged, not adjudicated.
- Whether `scs_rw_c002_002` earns its place, or is fully reconstructible from its members' relations —
  a live candidate falsifier for assumptions-register entry 3.

**ASSUMPTIONS CHALLENGED:** Entry **3** — mixed evidence; one of four systems looks reconstructible
from member relations, one clearly is not. Entry **1b** — second source, same unbound-majority
profile; the stated falsifier remains untouched, as no binding has yet been revised across either
extraction.

**LOCAL IMPLICATIONS:** The V0 granularity rule worked without exceptions and needs no amendment.
The visual-pass method does need review, for the confound/claim collision described above — which is
a human approval trigger under CANON-002, so it is proposed, not done.

**CROSS-STREAM IMPLICATIONS:** Tagged **CROSS_STREAM**. `bnd_rw_c002_0007` — the flower pair is the
most strictly isolated comparison found in either extraction to date: two lists identical in words,
order, typeface, colour and container, differing by one blank line, with the author's stated expected
reading. Offered to Eval's deferred creative-evaluation list under exactly the labelling the
Controller set on 24 Aug 2026: a candidate stimulus, not an instrument, not usable as-is, and the
expected reading is source-asserted rather than validated human ground truth. Filed as
`canon/PROPOSED-INTEGRATION-CHANGE-CANON-002.md`.

**ARCHITECTURAL IMPLICATIONS:** Tagged **ARCHITECTURAL — for review, no stop triggered.** SPEC-01's
`creative.hierarchy` is a rank-ordered list. Williams requires a composition to have a definite end,
so the viewer knows when they are finished. Ranking can express "noticed first" and cannot express
"finished". This is now independently observed by the historical Williams pass, the historical Lupton
pass, and this source. Three sightings. No stop was triggered because the finding arrived after the
checkpoint during comparison and does not block the completed extraction, and because the Charter
forbids a worker changing a schema. Recorded for Controller decision.

**DECISIONS NEEDED FROM CONTROLLER:**
1. **The three missed p.18 claims** — back-fill under a follow-up task, or preserve as evidence like
   CANON-001's page-87 miss? The failure mode is systematic and will recur.
2. **Amend the visual-pass method** so author-flagged confounds are also tested as candidate claims?
   Changing the visual-pass method is a human approval trigger, so I have not.
3. **The `creative.hierarchy` traversal limitation** — three independent sightings. Whether that
   crosses the threshold for a schema review is yours.
4. **All-caps convention** — when a source states two claims in one passage and argues only one,
   which becomes the object? The historical and fresh passes chose opposite ways.
5. **Provenance position on the local PDF** — not blocking, but worth settling before more chapters
   are rendered from it.

**EVIDENCE WORTH HUMAN INSPECTION:**
- Open `canon/sources/williams-proximity-p15-32.txt` and look at the two "My Flowers" lists near the
  top. They are identical. Then note that the surrounding prose explains why they differ. That is the
  whole of finding §2 and takes under a minute.
- `canon/findings/CANON-002-...md` §3, the Bang-versus-Williams table — the clearest evidence so far
  that source shape, not source quality, determines how well the schema fits.

**FILES CREATED / MODIFIED:**
- `canon/knowledge/current/robin-williams-proximity/visual-evidence-ledger.yaml`
- `canon/knowledge/current/robin-williams-proximity/source-knowledge.yaml`
- `canon/knowledge/current/robin-williams-proximity/source-concept-systems.yaml`
- `canon/knowledge/current/robin-williams-proximity/ontology-mappings.yaml`
- `canon/knowledge/current/robin-williams-proximity/operational-bindings.yaml`
- `canon/findings/CANON-002-williams-current-schema-extraction-findings.md`
- `canon/PROPOSED-INTEGRATION-CHANGE-CANON-002.md`
- `canon/HANDOFF.md`
- `canon/tasks/CANON-002-CONTROLLER-BRIEF.md`

Nothing outside `canon/` modified. No historical Williams file altered. No page renders committed.

**RECOMMENDED NEXT STEP:** A recommendation, not an action taken. Settle decisions 1 and 2 before a
third source, since both concern the extraction method and compound. Then a third source chosen to
test the Bang/Williams contrast rather than to add coverage — a source that, like Williams, authors
its own failure lists, to see whether the problem/remedy yield tracks source shape as inferred. Do
not treat two sources as having established that.

**EPISTEMIC CHECK:** Counts, page numbers, character counts and match percentages under OBSERVED were
produced by script and are reproducible from the named files. Interpretations are confined to
INFERRED. The provenance question, the source-kind question and the status of the missed claims are
listed as unknown rather than resolved. The cross-stream item is a proposal and the architectural
item is recorded for review, not acted on. No recommendation is presented as a decision.

**CONFIRMATION:** No unapproved next strategic step was started. CANON-003 was not begun, no third
source was touched, no schema was edited, no new source was acquired, no page renders were committed,
and no historical Williams file was modified.
