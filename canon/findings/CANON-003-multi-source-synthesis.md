# CANON-003 — Multi-source synthesis

**Date:** 24 Aug 2026  
**Integration branch:** `work/canon-003-integration-16`  
**Batch status:** extraction closed at **16 Controller-accepted books**. Books 11 (*Master Shots*) and 12 (*The Conversations*) were deliberately deferred after the batch exceeded its 15-book minimum. *Thinking with Type* remained blocked by structural column interleaving and is not counted.

## Executive conclusion

The frozen Canon architecture survived the batch better than the extraction *method* did.

Across 16 accepted books, the three-layer separation — **SourceKnowledge → source systems/ontology → OperationalBindings** — repeatedly prevented source claims from being distorted into whatever the current product could execute. It accepted technical, visual, procedural, persuasive, editorial and organisational knowledge without requiring a schema rewrite during the batch. Legitimate zero-Creative-IR-binding outcomes occurred, and highly executable physical or deterministic knowledge could remain useful without being falsely translated into prompt controls.

The strongest recurring weakness is therefore **not a need to collapse or replace the current model**. It is that, once source truth was cleanly separated from product use, several questions that the old forced-binding workflow accidentally made people ask stopped being mandatory: what the source format hid, where the evidence came from, whether an old technical claim is still durable, how a source relates to the current product, and whether two apparently agreeing sources are actually independent.

**Recommendation:** keep SPEC-03/04/05's core separation and make the next revision one consolidated **post-extraction Audit Gate**. The Audit Gate should run only after the source record is frozen and before cross-source promotion or product use. It should force four checks: source/visual integrity, evidence origin, product/application fit, and source lineage/independence. Exact field additions belong in the follow-on revision task; CANON-003 does not change the frozen specs.

---

## 1. Integrated batch

Accepted books:

1. *Grammar of the Shot*
2. *Ogilvy on Advertising*
3. *Light: Science & Magic*
4. *Interaction of Color*
5. *The Vignelli Canon*
6. *Making and Breaking the Grid*
7. *The Photographer's Eye: A Graphic Guide*
8. *Painting With Light*
9. *Grammar of the Edit*
10. *In the Blink of an Eye*
13. *Scientific Advertising*
14. *Made to Stick*
15. *Alchemy*
16. *Creativity, Inc.*
17. *Art & Fear*
18. *Building a StoryBrand*

The last complete strict integration run, before the narrowly-scoped mechanical repairs described below, saw the full 16-book set and counted:

- **505 SourceKnowledge objects**
- **54 SourceConceptSystems**
- **417 ontology terms**
- **53 concepts**
- **111 operational bindings**

Raw object counts are retained as inventory, **not as a measure of source quality or knowledge density**. Lane A demonstrated directly that representative sections of similar page length can yield very different object counts because the unit of argument differs by source shape.

### Historical-comparison coverage

Only books 1–3 had genuine prior extraction comparators. The other 13 accepted books had no historical extraction to compare against. Therefore historical-comparison findings are diagnostically useful but **not representative of the full 16-book batch**.

---

## 2. What the frozen design got right

### 2.1 Source truth and product use should remain separate

This was the most consistently validated architectural choice.

The old extraction pattern forced nearly every atom toward a Creative IR field. That made product-fit questions hard to forget, but it also over-bound knowledge. The fresh method produced far fewer bindings and allowed unbound knowledge to remain first-class.

The strongest positive control came from Lane D. *Creativity, Inc.* and *Art & Fear* produced 44 SourceKnowledge objects and **zero Creative IR bindings**. That is not a failure: their processed sections concern critique culture and the maker's behaviour, not the contents of one generated asset. *Building a StoryBrand*, by contrast, produced Creative IR bindings while carrying weaker evidence in the processed section. **Bindability and evidence quality are different dimensions.**

A similar boundary appeared in technical sources. Physical lighting repairs belong to `physical_production`; deterministic layout operations belong to their own executable class. Neither becomes a generative-control instruction merely because the current product uses generative models.

**Decision:** do not restore the old mandatory-binding rule. Recover its useful attentional effect as a separate post-source application audit.

### 2.2 The systems layer earned its complexity

The SourceConceptSystem layer handled materially different structures without a batch-time vocabulary change: ordered shot/edit relationships, design systems, checklists that explicitly are not formulas, priority structures, interacting persuasion principles, creative-process systems and internally qualified rules.

There are representation gaps — e.g. Murch's explicit priority *weights* do not fit a rank-only `priority_order`, and a traversal-with-return pattern strains current hierarchy representation — but these are bounded gaps, not evidence that the system layer is wrong.

**Decision:** keep the systems layer. Do not redesign it from isolated edge cases yet.

### 2.3 Refusal and negative relations are useful knowledge

`distinct_from`, explicit uncertainty, zero bindings, `unknown` executability, and no-historical-comparator outcomes all prevented false certainty. The batch repeatedly found pairs that looked mergeable on the surface but behaved differently in mechanism or context.

**Decision:** preserve refusal as a valid outcome; do not reward extraction volume or forced convergence.

### 2.4 The frozen granularity rule was robust

Across the diverse accepted source shapes, no lane had to invent a new granularity policy during extraction. Ambiguity could be recorded rather than patched with a new rule.

**Decision:** no granularity-method change is justified by this batch.

---

## 3. Strongest recurring problems

### 3.1 Visual/source-format risk is structural, not proportional to image count

The batch found several different failure mechanisms that should not be compressed into one generic `visual risk` concept:

- a real printed page can be unavailable because an EPUB has no page at all;
- a converted PDF can expose a **false page** that looks page-addressable but is not the authored layout;
- headings or labels can exist only as raster/SVG artwork and silently flatten the text structure;
- text inside figures can disappear while the prose extraction looks perfectly complete;
- a greyscale digitisation of a colour argument can survive a visual pass while still destroying the evidence;
- a figure can be inspected successfully yet remain insufficient to resolve which image carries which verdict;
- conversely, a diagram-led source can survive perfectly well without page layout if the diagram itself is self-contained.

Lane D added an important counterexample to any image-count proxy: books with similar raw image counts had radically different visual dependence. What matters is **what the source uses images/page structure to teach**, not how many images it contains.

**Implication:** the method needs a source/visual-integrity audit based on representation shape and argumentative role, not figure count.

### 3.2 Evidence-origin metadata is the clearest schema pressure

The exact `empirical_within_source` distinction failed in all three Lane C books, in three different ways:

- *Scientific Advertising* repeatedly claims tests/measurement while often omitting enough result or attribution detail to know what was actually measured;
- *Made to Stick* reports empirical studies, but most are third-party studies;
- *Alchemy* mixes the author's own experiment with cited external work.

The current extraction can preserve the truth in caveats, but that truth is not aggregatable. Lane D independently found an adjacent attribution problem: the schema does not cleanly distinguish an author's own claim from a third-party claim quoted approvingly.

**Implication:** the next revision should distinguish evidence/claim *origin* without turning evidence characteristics into a credibility score. At minimum it must make own measurement, reported third-party evidence, claimed measurement without supplied result, and mixed provenance machine-readable.

### 3.3 Source identity is not source independence

*Grammar of the Shot* and *Grammar of the Edit* are separate source ids but companion books by the same authors. Agreement between them is useful, but it is not the same evidential event as independent convergence.

SPEC-05 currently guards cross-source concepts at the source-id level and has no durable lineage structure for shared authorship/series/source ancestry.

**Implication:** cross-source promotion needs lineage metadata before it can count independent origins honestly. Same-author companion agreement should be recorded without being counted as independent convergence.

### 3.4 Removing forced product fit removed a useful question

Historical comparisons showed a consistent trade-off: earlier extraction work, because it forced a Creative IR connection, repeatedly noticed product-schema implications that the cleaner source-first pass could walk past. The old method's answer was often wrong — it over-bound — but the *question* was useful.

Lane D then showed why putting the requirement back into SourceKnowledge would be a mistake: valuable knowledge can legitimately have no Creative IR binding, and the most bindable source can be the weakest-evidenced one.

**Implication:** add a mandatory **application audit after source freeze**, not mandatory bindings during source extraction. The audit may conclude `no current binding`.

### 3.5 Older technical sources need an explicit durability question

*Painting With Light* interleaved durable optical geometry, technology-contingent film practice, and period-specific studio convention. Existing characteristics such as `historical_claim` can express this, but nothing in the frozen procedure forces the extractor to ask the question.

**Implication:** the Audit Gate should explicitly ask whether claims in older technical sources depend on obsolete technology or historical convention. This is a procedural addition; the batch does not justify a new vocabulary merely to restate fields that already exist.

---

## 4. Important bounded gaps that should NOT drive the next revision

The batch surfaced real but currently narrow representation issues:

- rank order cannot express Murch's explicit numerical weights;
- `creative.hierarchy` is weak for traversal followed by return;
- some source-local relations wanted richer relation types than lane governance allowed;
- human/organisational remedies do not fit naturally into an asset-execution vocabulary;
- one source's long-form structure suggests local sections may defer their governing question far away.

These should stay logged. None has enough independent recurrence to justify making it the centre of the next method revision.

---

## 5. Method/governance lessons

### 5.1 Isolation is procedural, not magical

The fresh-before-history checkpoint rule worked and should remain. It gave the repository an auditable boundary between fresh extraction and comparison.

But the batch also showed that a spec can itself contain examples from a book being extracted. An extractor who has read the spec may already know the old finding. Apparent convergence in that case is not independent.

**Implication:** lineage/contamination metadata belongs in synthesis and promotion decisions, not only in extractor memory.

### 5.2 Governance ambiguity can reduce fidelity without a schema defect

Lane C found a disagreement between governing documents about which ontology relation types a worker may set locally. The conservative interpretation avoided overreach but forced source-stated relationships into weaker generic links.

**Implication:** resolve authority/order of governing documents before adding relation types. This is a governance clarification, not evidence for schema expansion.

### 5.3 Committed validation is necessary

Most lanes reported successful validation using ephemeral scratchpad scripts. The independent integration validator nevertheless found 24 mechanical defects across three accepted directories: one YAML serialization error and 23 remedy terms missing SPEC-05's required `executable_by` field.

The strict integration run also found an over-strict assumption in the new validator itself; a regression test proved and corrected it before data changes were made. After that correction the remaining defects were narrow and data-specific.

Integration repairs made no semantic reinterpretation:

- the Made to Stick visual ledger's malformed flow-scalar quoting was repaired;
- 16 Hopkins remedy terms received `executable_by: [unknown]`;
- 7 Sutherland remedy terms received `executable_by: [unknown]`.

`unknown` is intentionally conservative: the batch does not justify inventing a generative or deterministic executor for those strategy/process remedies.

**Implication:** keep the reproducible validator and its tests in the repository. A validation claim should come from a committed instrument, not a session scratchpad.

---

## 6. One consolidated revision recommendation

### CANON Method v0.2 proposal: the Post-Extraction Audit Gate

Do **not** rewrite SPEC-03/04/05 piecemeal from this batch. Create one follow-on revision that adds a formal Audit Gate between stable source extraction and downstream promotion/use.

The Audit Gate should have four mandatory outputs:

1. **Source/visual integrity audit** — classify the actual representation available (authored page, reflow/no-page, converted/false-page, image-carried headings/text, figure self-containment) and state what argumentative evidence could be missing.
2. **Evidence-origin audit** — make author-owned measurement, third-party reported evidence, claimed measurement without supplied result, mixed evidence, and quoted third-party claims distinguishable without converting them into a credibility score.
3. **Application audit** — explicitly revisit Creative IR / Production IR / evaluation / governance relevance *after* source truth is frozen; `no current binding` remains a successful outcome.
4. **Lineage/independence audit** — record authorship/source lineage sufficient to prevent same-author or derivative sources from being counted as independent convergence.

Two supporting procedural rules belong in the same revision:

- ask an explicit technology-contingency question for older technical sources;
- use the committed validator as the mechanical acceptance gate.

This is one coordinated method revision because all six changes solve the same observed failure: **the source-first method is good at preserving truth but currently lacks a mandatory, structured second look at the conditions under which that truth was represented, evidenced, applied and promoted.**

The revision should preserve the present layer boundaries. It should not create automatic cross-source merges, force product bindings, translate physical remedies into prompts, or treat source quantity as evidence strength.

---

## 7. Batch limitations

- 16 books exceed the task minimum but are not a random or exhaustive sample of creative-production knowledge.
- Books 11–12 were deferred by Controller choice, so interview/transcript and *Master Shots* source shapes remain less stressed than originally planned.
- Only 3/16 accepted books had historical extraction comparators.
- Representative sections differ in length and argumentative density; raw object counts are not comparable performance metrics.
- Parallel-lane cognitive isolation is procedural; shared model/agent identity cannot guarantee erasure of prior exposure.
- Same-author companion books must not be counted as independent evidence.
- Rights status of local source copies remains outside this extraction experiment and unresolved where previously noted.
- CANON-003 tests extraction/representation, not whether downstream RAG/planning actually improves generated media. That consumption experiment remains a separate stage.

---

## 8. Controller decision from CANON-003

**The frozen Canon architecture is retained.**

CANON-003 is evidence for a **method hardening revision**, not a conceptual reset. The next Canon task should specify and test the Post-Extraction Audit Gate, including the minimum schema additions for evidence origin and source lineage, while leaving the successful source/system/binding separation intact.
