# CANON-008 — Wave 1: Devanagari typeface structure

**Owner:** Canon agent  
**Status:** OPEN — Controller-assigned  
**Scope:** one source only  
**Task type:** post-CANON-007 expansion ingestion under authoritative Audit Gate v0.2

## Objective

Add the first India-script / Devanagari-specific source to the live Canon using a legitimate, institution-hosted source.

The discovery workbook's prior C08 identity ("Devanagari Type Design — Fiona Ross") is **superseded and must not be used**. Controller review could not verify that bibliographic identity. CANON-008 repairs that portfolio slot with the stronger institution-hosted source below; it is a replacement for C08, not an additional 23rd expansion source.

If accepted, live Canon should move from **19 to 20** sources. Historical CANON-003 / CANON-004 remain fixed at 16.

## Source identity and legitimate route

Target source:

- **Girish Dalvi**
- **Conceptual Model for Devanagari Typefaces**
- PhD thesis, Industrial Design Centre (IDC), IIT Bombay
- 2010
- official D'source / IDC archive record

Official archive route:

`https://dsource.in/dcontent/idc-archive/collection/collection-details2.php?id=1275`

D'source identifies this as a thesis from IDC IIT Bombay and exposes the archive's own PDF/download route. Use only the official D'source / IDC-hosted material linked from that record.

Do **not** use mirrors, scraped copies, Google Books, Internet Archive copies, reuploads, or the old Fiona Ross metadata.

### Acquisition gate

Before extraction:

1. resolve the official archive's actual downloadable artifact;
2. record title page / author / institution / year from the artifact itself;
3. record file size, page count, PDF version/encryption state and SHA-256;
4. confirm the artifact is the thesis itself rather than only an abstract/preview;
5. if the archive exposes only an abstract, incomplete preview, or an identity-ambiguous file, **STOP and return to Controller before extraction**.

Download into a git-ignored workspace only. Do not commit the thesis PDF, page images or screenshots.

## Bounded processed scope

This is **not** authorization to ingest an entire PhD thesis indiscriminately.

After opening the verified thesis, use its authored table of contents and choose **one coherent contiguous scope** that most directly establishes the structure/terminology/classification of Devanagari typefaces relevant to visual exactness and type design.

Prefer a scope containing, where present:

- structural anatomy / reference lines / parts of Devanagari glyphs;
- relationships among visual features;
- terminology and classification dimensions;
- the conceptual model itself and the evidence used to derive it;
- explicit limits, disagreements, ambiguity or non-standardized terminology.

Avoid background/history chapters unless they are necessary to interpret the selected model. Avoid implementation details of the old web/Flex/PHP search tool unless they contain enduring type-design knowledge.

Record the exact selected chapter/section/page span in `PROVENANCE.md` and explicitly name all unprocessed thesis material.

If the table of contents does not permit a clean bounded scope without guessing, stop and return a scope proposal before extraction.

## Why this source matters

The current Canon has general typography/design sources but no accepted source whose primary subject is the internal structure of Devanagari typefaces. The source is potentially useful for:

- understanding what visual features must remain correct in generated Hindi/Devanagari text;
- separating token/string correctness from glyph-form / typography correctness;
- giving future evaluation work a source-grounded vocabulary for Devanagari visual structure;
- avoiding Latin-centric typography assumptions.

Do not turn those potential uses into bindings before source truth is frozen.

## Required method order

Follow the authoritative sequence exactly:

1. establish source identity, representation and provenance;
2. SourceKnowledge extraction under SPEC-03;
3. source systems / ontology under SPEC-05;
4. justified OperationalBindings under SPEC-04 — zero is valid;
5. fresh checkpoint of frozen source artifacts;
6. one Audit Gate v0.2 record against those exact bytes;
7. run validator/tests;
8. only then describe the source as accepted live Canon.

## Source-specific extraction requirements

### A. Visual argument is first-class

A typeface thesis is likely to make claims through letterform diagrams, labelled glyphs, reference-line illustrations, classification examples, comparison plates and tables.

Where a claim depends on a figure, inspect the figure itself. Text-only extraction is not sufficient.

For claim-bearing figures preserve where present:

- authored page and figure number/title;
- exact Devanagari glyph/sample shown;
- labels / reference lines / feature names;
- spatial relation among labels and glyph features;
- category/classification relation the figure demonstrates;
- whether distinctions depend on stroke shape, proportion, position, terminal, join, headline/shirorekha relation, counters, vertical metrics or another visible property;
- whether the thesis states the distinction or the extractor is inferring it from the visual;
- any ambiguity caused by PDF linearisation.

CANON-007 added `figure_semantic_binding_lost` for cases where tokens survive but their figure topology does not. Use it only if that exact failure is observed; do not apply it automatically.

### B. Terminology must stay source-faithful

Devanagari anatomy terminology is not universally standardized. Preserve:

- the source's own term;
- transliteration/English label only if the source provides it or the mapping is explicitly extractor-assigned;
- competing or ambiguous terminology where the thesis reports it;
- relationships among features rather than flattening everything into isolated dictionary terms.

Do not normalize multiple source terms into one canonical term unless the source itself establishes equivalence. Any cross-source promotion remains out of scope.

### C. Separate descriptive structure from normative design rule

Do not convert:

- observed/common structure → mandatory rule;
- classification feature → quality criterion;
- historical convention → universal contemporary requirement;
- expert preference → script invariant.

Preserve whether each claim is descriptive, classificatory, empirical, historical, practitioner assertion, or extractor synthesis.

### D. Empirical / participant evidence

If the selected scope reports expert/non-expert classification exercises, studies or observations, preserve:

- participant/sample description;
- task;
- measured/observed outcome;
- whether it is the thesis author's own study or cited prior work;
- limitations supplied by the source.

Do not turn a classification experiment into a universal perceptual law.

### E. Technology contingency

The thesis is from 2010 and may discuss then-current font technologies/tools. Audit technology contingency explicitly.

Separate durable script/typeface structure from:

- obsolete software/toolchain assumptions;
- then-current font formats/rendering environments;
- historical production constraints;
- classifications tied to a particular font corpus.

## Application fit

Assess only after freeze across all seven Audit Gate consumers.

Potential relevance may exist to evaluation, benchmark, deterministic composition or human workflow, but do not invent fields or force bindings.

In particular, **do not edit EVAL-005 or use this task to redefine the Devanagari battery**. Any future Eval use must be a separate Controller task after this source is accepted.

## Lineage / independence

Perform normal pairwise lineage checks against the live 19-source corpus.

Also record if this thesis materially depends on earlier Devanagari sources that could later be ingested. A citation alone is not dependence; use only the controlled lineage definitions.

Do not infer independence merely because this is the first Devanagari-specific accepted source.

## Repository outputs

Create one new source directory under:

`canon/knowledge/current/<stable-source-slug>/`

with:

- `PROVENANCE.md`
- `source-knowledge.yaml`
- `source-concept-systems.yaml`
- `ontology-mappings.yaml`
- `operational-bindings.yaml`
- `visual-evidence-ledger.yaml`

Create:

- one active v0.2 Audit Gate record;
- bounded CANON-008 findings / Controller Brief;
- `canon/HANDOFF.md` update.

Do not commit copyrighted source files or page/figure renders.

## Frozen non-goals

Do not in CANON-008:

- ingest a second Devanagari source;
- ingest the Snehal Patil project as an additional source;
- ingest Thinking with Type, Brand New, Product Photography, Animation Bootcamp or Advertising Concept Book;
- change EVAL-005 or any Eval battery;
- promote cross-source concepts;
- start RAG/retrieval or Production IR;
- change SPEC-01/03/04/05 unless a genuine stop condition requires a minimum proposal and Controller approval;
- expand Audit Gate vocabulary unless a genuinely unrepresentable observed failure forces a stop;
- add GitHub Actions;
- spend on any model/API or paid source.

## Verification from final branch head

Run fresh:

1. `python canon/validation/validate_canon003_integrated.py --root .` — historical 16 unchanged;
2. `python canon/validation/validate_audit_gate_v02.py --root .` — if accepted, expect **20 active records over 20 current source directories**;
3. `python -m pytest tests/ -q`;
4. verify the new source's five snapshot-covered artifacts against its audit snapshot;
5. verify no ID collision across the live corpus;
6. verify no source PDF/page render/image was committed;
7. verify SPEC-01/03/04/05 and historical CANON-003/004 decisions/synthesis remain unchanged unless an approved stop-condition change occurred;
8. verify no other Wave-1 source or Eval file was touched.

## Delivery

Use branch:

`work/canon-008-dalvi-devanagari`

Open one PR against current `main` and return a Controller Brief with:

- exact official artifact identity + SHA-256/bytes/pages;
- selected bounded thesis scope and why;
- source slug/id;
- SourceKnowledge / systems / ontology / binding counts;
- most consequential structural/typeface concepts in summary;
- representation-integrity findings;
- evidence-origin findings;
- lineage verdict;
- technology-contingency findings;
- Audit Gate verdict;
- exact fresh verification outputs;
- any stop condition or unresolved issue.

Then stop. Do not self-assign CANON-009.
