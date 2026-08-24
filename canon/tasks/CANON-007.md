# CANON-007 — Wave 1 pilot: *Effectiveness in Context*

**Owner:** Canon agent  
**Status:** OPEN — Controller-assigned  
**Scope:** one source only  
**Task type:** first post-CANON-006 expansion ingestion under authoritative Audit Gate v0.2

## Objective

Ingest **one** new Wave-1 source, *Effectiveness in Context*, as the first clean expansion source after the Canon method was stabilized and the two reserve books were resolved.

This is deliberately a **single-source pilot**, not a launch of the whole Wave-1 portfolio. The goal is to add useful advertising-effectiveness knowledge while proving the adopted extraction → freeze → Audit Gate workflow on a visually/data-bearing empirical report.

If accepted, the current live Canon should move from **18 to 19** sources. Historical CANON-003 and CANON-004 remain fixed at 16.

## Source identity and legitimate access

Use the official free Thinkbox route only:

`https://www.thinkbox.tv/research/reports/effectiveness-in-context-free-download`

Work's acquisition-preparation pass identified the source as:

- Les Binet and Peter Field
- *Effectiveness in Context: A Manual for Brand Building*
- Part 2 of *Marketing Effectiveness in the Digital Era*
- EffWeek 2018
- official/authorized PDF distributed by Thinkbox
- 139 pages
- PDF 1.6
- unencrypted
- expected file size from Work's acquired copy: **24,726,437 bytes**
- expected SHA-256 from Work's acquired copy: **`e589a4222f5ce06db52384c5cc002dbd4e96f4156530be60d19bdf73e70ae91e`**

### Acquisition rule

Download only from the official Thinkbox/authorized route into a **git-ignored local workspace**. Do **not** commit the PDF or any copyrighted page/image extract to the public repository.

Before extraction:

1. compute SHA-256 and file size;
2. if both match the Work fingerprint above, record that and proceed;
3. if the official file differs, determine whether Thinkbox has transparently replaced/revised the file;
4. if identity/version cannot be established without guessing, **stop and return to Controller before extraction**.

Do not search for mirrors or substitute copies.

## Required method order

Follow the authoritative Canon method exactly:

1. establish source identity, representation and provenance;
2. perform source-faithful SourceKnowledge extraction under SPEC-03;
3. stabilize source systems / ontology under SPEC-05;
4. stabilize any justified OperationalBindings under SPEC-04 — zero bindings is allowed;
5. commit a **fresh checkpoint** of the frozen source artifacts;
6. write one authoritative Audit Gate v0.2 record against those exact bytes;
7. run the Audit Gate validator;
8. only after the audit passes may the source be described as accepted live Canon knowledge.

Do not weaken or bypass the gate because the PDF is official or because the report appears empirical.

## Extraction requirements specific to this source

This report contains charts, tables, quantitative comparisons and methodological framing. **The figures are evidence, not decoration.** Text-only extraction is insufficient where a claim depends on a chart/table.

### A. Preserve claim origin and empirical scope

For every empirical claim that survives into SourceKnowledge, preserve enough context to distinguish:

- what population/sample/database the result comes from;
- what outcome/metric is being compared;
- relevant time horizon;
- relevant segmentation/context variables;
- whether the report presents a measured result, an interpretation, an extrapolation, a recommendation or a practitioner assertion;
- material caveats or methodological qualifications supplied by the source.

Do not silently upgrade:

- association → causation;
- retrospective effectiveness analysis → universal law;
- average/tendency → deterministic rule;
- a chart's visual pattern → a stronger numeric claim than the source supplies.

If the source relies on earlier IPA/Binet/Field datasets or third-party evidence, distinguish that lineage from measurements performed uniquely within this publication. Do not call everything `source_own_measurement_reported` merely because Binet and Field authored the report.

### B. Inspect claim-bearing charts/tables directly

For every chart/table that materially supports an extracted claim, preserve in the visual-evidence work at minimum where present:

- page number;
- figure/chart/table title;
- axes and scales;
- legend/series labels;
- units;
- categories/segments being compared;
- base/sample/source note;
- adjacent authored interpretation;
- visible methodological caveat or footnote;
- whether the numerical values are explicitly printed or only visually inferable.

Do not infer precise values from bar heights/line positions when the source does not print them. Record the relationship qualitatively if that is all the figure establishes.

Where several charts instantiate one authored mechanism/system, prefer a coherent SourceConceptSystem rather than dozens of near-duplicate isolated terms.

### C. Granularity

Apply the established Canon granularity rule:

- one SourceKnowledge object per useful, source-faithful claim/mechanism/constraint;
- do not create an object for every sentence, slide-like heading or chart merely to raise counts;
- preserve caveats with the claim they constrain;
- preserve explicit refusal/conditionality when the report warns against universal application;
- do not collapse materially different contexts into a generic advertising rule.

### D. Application fit only after source truth is frozen

Only after the source record is stable, assess application fit across the seven Audit Gate consumers.

Potential relevance may exist to planning, evaluation, benchmark/governance or human workflow, but **do not force bindings because the report sounds useful**. `no_current_binding` and `candidate_no_binding_made` remain valid outcomes.

Do not create a new SPEC-04 target type or executor in this task.

### E. Technology/context contingency

The report is from 2018 and discusses marketing effectiveness in a particular media/measurement era. Audit this explicitly.

Distinguish durable mechanisms from claims that depend on:

- then-current channel mix;
- media costs/availability;
- measurement conventions;
- platform behaviour;
- historical market structure.

Do not modernize or rewrite an older claim. Record the contingency.

## Lineage / independence

Perform the normal pairwise lineage audit against relevant existing Canon sources.

Do not infer independence from source ids or different authors alone. CANON-006 established that bibliographic authorship is not sufficient.

Use the current controlled vocabulary, including `shared_primary_informant`, only when its exact definition is met. Incidental quotation is not enough.

If this source has a relationship that the current controlled vocabulary cannot state truthfully, **stop and return a minimum method-change proposal instead of inventing or stretching a relation**.

## Representation integrity

The Work pass reported a complete, unencrypted 139-page official PDF with intact figures/tables. Verify that in the actual acquired copy.

Record any observed issues such as:

- text extraction / reading-order damage;
- figure labels absent from text layer;
- rasterized chart text;
- missing pages/images;
- inaccessible footnotes/source notes;
- ambiguity caused by figure reproduction.

Do not mark representation integrity as clean merely because the PDF opens.

## Repository outputs

Create one new source directory under:

`canon/knowledge/current/<stable-source-slug>/`

with the same authoritative source-artifact set used by the current Canon:

- `PROVENANCE.md`
- `source-knowledge.yaml`
- `source-concept-systems.yaml`
- `ontology-mappings.yaml`
- `operational-bindings.yaml`
- `visual-evidence-ledger.yaml`

Create:

- one Audit Gate record under `canon/audit/records/`;
- a bounded CANON-007 findings / Controller Brief record;
- `canon/HANDOFF.md` update.

Do not commit the copyrighted PDF, page renders, screenshots or extracted source images.

## Frozen non-goals

Do **not** in CANON-007:

- ingest any other Wave-1 source;
- start Product Photography, Thinking with Type, Brand New, Animation Bootcamp, Advertising Concept Book or the Devanagari replacement;
- reopen CANON-003 accepted sources except as needed to read their committed audit/lineage metadata;
- rewrite CANON-003 or CANON-004 historical counts/synthesis;
- create cross-source promoted concepts;
- start RAG/retrieval/Canon-consumption experiments;
- start Production IR;
- add a GitHub Actions workflow;
- spend on any model/API or paid source;
- modify SPEC-01, SPEC-03 or SPEC-04;
- modify SPEC-05 unless a genuine stop condition fires and Controller explicitly approves the minimum proposed change.

## Verification required from final branch head

Run fresh:

1. `python canon/validation/validate_canon003_integrated.py --root .`
   - must retain its historical 16-source meaning and output.
2. `python canon/validation/validate_audit_gate_v02.py --root .`
   - if this source is accepted, expect **19 active records over 19 current source directories**.
3. `python -m pytest tests/ -q`
4. mechanically verify the new source's five snapshot-covered artifacts match its Audit Gate snapshot;
5. verify no id collision across the enlarged live corpus;
6. verify SPEC-01/03/04 are unchanged from task-base `main`;
7. verify no historical CANON-003/004 decision or synthesis was rewritten;
8. verify no source PDF/image/page render was committed;
9. verify no `.github` workflow was added.

If any validator or test fails, fix only defects within CANON-007 scope; do not weaken existing tests to obtain a pass.

## Delivery

Use branch:

`work/canon-007-effectiveness-context`

Open **one PR** against current `main` and return a Controller Brief containing:

- exact acquired source identity + SHA-256/bytes;
- source slug/id;
- SourceKnowledge / systems / ontology / binding counts;
- most consequential extracted systems/claims (summary only, not copied source prose);
- representation-integrity findings;
- evidence-origin findings;
- lineage verdict;
- technology-contingency findings;
- Audit Gate verdict;
- exact fresh verification commands/results;
- any stop condition or unresolved issue.

Then **stop for Controller review**. Do not self-assign the next Wave-1 source.