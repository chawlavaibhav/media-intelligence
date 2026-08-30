# Experimental Canon expansion + grounded Q&A bank — v1

> ## STATUS: EXPERIMENTAL. NOT LIVE CANON. NOT FOR MERGE.
>
> This directory is **not authorised for merge into live Canon** and nothing in it is accepted
> project knowledge. It was produced on the isolated branch
> `work/canon-parallel-books-qa-experimental` as a parallel-compute exploration.
>
> **Live Canon remains 19 accepted sources and 19 audit records, unchanged.** No file under
> `canon/knowledge/current/**`, `canon/audit/records/**`, `canon/knowledge/SPEC-*`,
> `coordination/**`, `eval/**`, `resources/**` or `governance/**` was created, edited or deleted.
> No Capability Registry row exists or was proposed. No Controller state was touched. No Audit Gate
> record was written — **these sources have not passed the gate and therefore may not be used for
> cross-source promotion, downstream product use, or Canon-consumption/retrieval work**
> (`canon/audit/AUDIT-GATE-v0.2.md`, step 7).
>
> Nothing here is evidence about what any generative model can do.

---

## 1. What this task was for

Two deliverables over legitimately accessible source material the Canon has not consumed:

**A — Experimental Canon extraction.** Run the *current* Canon architecture (SPEC-03 Source
Knowledge, SPEC-03 Source Concept Systems, SPEC-04 Operational Bindings, SPEC-05 ontology) over new
material, to see what the architecture produces on sources of a kind the corpus does not yet hold.

**B — Grounded question–answer banks.** For every source processed, a Q&A bank derived *only* from
that source, so that later work can test retrieval, test retention, compare what a model already
knows against what the Canon explicitly holds, check whether Canon retrieval supplies the right
principle, and eventually test whether a model can *apply* a principle to creative work.

Both are exploratory. Neither is an admission decision.

---

## 2. Source access — how the portfolio was decided

The local library is `~/Downloads/Books/` — 40 files, 37 distinct titles. Its licence status had
never been settled: CANON-003's source inventory
(`canon/findings/CANON-003-source-inventory-and-selection.md` §2) records *"**NOT VERIFIED:** the
licence status of any of these copies. This is a Controller question, not one this extraction can
settle."*

This run began by holding the whole library back on exactly that ground. **The Controller then
explicitly authorised read-only use of the already-present local library for this experimental
task**, answering the question CANON-003 had reserved to them. That decision is what set the
portfolio below.

**What the authorisation does and does not cover.** It authorises reading files already on the
Controller's disk. It does not change any copy's provenance, and it is recorded as an authorisation
rather than as a finding of ownership. Accordingly:

- Nothing was acquired, purchased, downloaded, de-DRM'd, scraped past a paywall, or accessed with
  anyone's credentials. **No book bytes and no page images are committed anywhere in this
  directory.** Extraction output is paraphrase, not reproduction.
- Every processed source's `PROVENANCE.md` states plainly that the licence status of the individual
  copy is **not independently verified**. An inventory that omits provenance defeats its own
  purpose, and this corpus has been caught by that before.

**Six files are excluded despite the authorisation.** Their filenames carry an explicit `libgen.li`
marker — direct evidence of piracy-mirror origin, which contradicts rather than supports an
ownership assertion. A general authorisation over a library does not resolve a specific file that
records where it came from. (The environment's own safety classifier independently refused to read
them, which is consistent.) They are recorded, not processed:

Lupton *Thinking with Type* · Molly Bang *Picture This* · Williams *The Non-Designer's Design Book*
· Albers *Interaction of Color* · Berger *Ways of Seeing* · Graham *Hackers and Painters*

The real cost is narrow: Albers is already live Canon, Berger is an image-only scan and unreadable
anyway, Graham is out of domain, and the remaining three were already processed historically under
the superseded SPEC-02 atom schema. What is lost is a **re-extraction of those three under the
current architecture** — worth doing, and cleanly separable as its own task.

**Four sources needed no authorisation at all**, and it is worth keeping them distinct because their
basis is stronger than anyone's permission:

| Source | Basis |
|---|---|
| Hopkins, *My Life in Advertising* (1927) | The **work** is public domain — US term for 1927 publications expired 1 Jan 2023; author died 1932. Copyright status of the work governs, whichever scan is on disk. |
| Hopkins, *Scientific Advertising* ch. 8–21 (1923) | Same — US term expired 1 Jan 2019. |
| W3C, WCAG 2.2 | Openly published standard, W3C Document Licence. |
| Google, "ABCDs of effective video ads" | Publisher-authorised, free, unauthenticated, Google-owned pages. A third-party Scribd reupload of a fuller guide exists and was **deliberately not used**. |

**Two candidates were abandoned rather than routed around**: the Dalvi Devanagari thesis (IIT Bombay
SSO — the wall CANON-008 already stopped at) and the Cayla & Elson article (journal paywall). No
mirror, reupload, torrent or scraped copy was used for anything in this run.

---

## 3. Sources discovered, processed, skipped, unavailable

Full row-per-candidate detail: **`SOURCE-STATUS.csv`** (46 rows).

| Disposition | Count |
|---|---|
| Candidate sources inventoried | **46** |
| **Processed** | **17** |
| Skipped — already live Canon, scope extension not prioritised this run | 14 |
| Excluded — explicit `libgen.li` piracy-mirror marker | 6 |
| Excluded — unreadable (image-only scan / `.mobi`, no extractor) | 3 |
| Skipped — out of domain | 1 |
| Unavailable — official route failed or identity unresolved | 5 |

### Processed — 17 sources

**Twelve are new independent origins. Five are scope extensions of works already in live Canon** and
carry **zero** independence against their live counterpart — same work, same author.

| # | Source | Kind | Overlap with live Canon |
|---|---|---|---|
| 1 | Hopkins, *My Life in Advertising* (1927) | full book | **`shared_author` dependence** with live `hopkins-scientific-advertising-ch1-7`; its ch.17 is *about* that book. **Not an independent origin against it.** |
| 2 | Hopkins, *Scientific Advertising* ch. 8–21 (1923) | **scope extension** | Same work as live `hopkins-scientific-advertising-ch1-7`. Zero independence. |
| 3 | W3C, **WCAG 2.2** — Guideline 1.4 | open standard | None. Corpus's first standards document and first numeric criteria. |
| 4 | Google, **"ABCDs of effective video ads"** | platform guidance | None. Corpus's first short-form / feed-native source. |
| 5 | Sullivan, ***Hey, Whipple, Squeeze This*** | full book | None. Creative-department tradition; disagrees with the reason-why school held by live Ogilvy and Hopkins. |
| 6 | Connor & Irizarry, ***Discussing Design*** | full book | None. Nearest live neighbour `catmull-creativity-inc-ch5`. The corpus's first source on how judgement itself is conducted. |
| 7 | Hunter/Biver/Fuqua, ***Light: Science & Magic*** beyond ch. 3 | **scope extension** | Same work as live `light-science-magic-ch3`. Zero independence. Targets the open **G4 packshot gap**. |
| 8 | Samara, ***Making and Breaking the Grid*** ch. 2 | **scope extension** | Same work as live `samara-making-breaking-grid-ch1`. Zero independence. Ch.2 is the book's own **counter-argument** to the live material. |
| 9 | Airey, ***Logo Design Love*** | full book | None. Brand-identity marks; nearest live neighbour `vignelli-canon-intangibles`. |
| 10 | Berger, ***Contagious*** | full book | None. Corpus's strongest empirical-social source; adjacent in kind to live `heath-made-to-stick-introduction`. |
| 11 | Ries & Ries, ***The 22 Immutable Laws of Branding*** | full book | None. **Materially disagrees with live `binet-field-effectiveness-in-context-ch1`** — recorded, not resolved. |
| 12 | Kahneman/Sibony/Sunstein, ***Noise*** | full book (judgement material only) | None. No live source covers how human judgement behaves. |
| 13 | Carroll, ***Read This If You Want to Take Great Photographs*** | full book (small) | None. Subject overlap with live `freeman-photographers-eye-graphic-guide`. |
| 14 | Ogilvy, ***Ogilvy on Advertising*** beyond ch. 2 | **scope extension** | Same work as live `ogilvy-ch2-advertising-that-sells`. Zero independence. |
| 15 | Freeman, ***The Photographer's Eye*** beyond Parts 1–3 | **scope extension** | Same work as live `freeman-photographers-eye-graphic-guide`. Zero independence. |
| 16 | Godin, ***This Is Marketing*** | full book | None. Adjacent to live `miller-storybrand-sb7`. |
| 17 | Sontag, ***On Photography*** | full book (transferable material only) | None. Extracted under the project's own standing warning that this is **"critique, not craft"**. |

**Independence accounting, stated plainly:** this run adds **12** independent origins, not 17. The
five scope extensions deepen origins the Canon already had. Hopkins's *My Life in Advertising* is a
new work but **not** a new origin against the Hopkins already in Canon.

### Unavailable — recorded, not routed around

| Source | Why |
|---|---|
| Dalvi, *Anatomy of Devanagari Typefaces* (Design Thoughts, 2009) | Identity and the publisher's own link both confirmed. The IDC IIT Bombay asset route returns **HTTP 503 on every attempt**; the https path 404s. No authorised alternative. Mirrors not used. |
| Dalvi, *Conceptual Model for Devanagari Typefaces* (2010 thesis) | Behind IIT Bombay SSO. CANON-008 already stopped here; not re-attempted. |
| Cayla & Elson, *Indian Consumer Kaun Hai?* (2012) | Journal paywall. No purchase authorised. |
| Meta official creative guidance | No citable official artifact identified. Agency blogs restating it are not a substitute. |
| TikTok Creative Center best practices | Same — identity unresolved. |

**Consequence worth stating plainly:** the Canon's two largest acknowledged gaps — **Devanagari /
Indic typography** and **Indian cultural context** — remain completely unclosed, and this run did
not close them. `indian_indic_context` still has zero contributors.

---

## 4. Volume produced

<!-- COUNTS:BEGIN -->
*(filled mechanically by `build_manifest.py` — see `QA-MANIFEST.json`)*
<!-- COUNTS:END -->

---

## 5. How to read what is here

Each source directory contains:

| File | What it is |
|---|---|
| `PROVENANCE.md` | Source identity, edition, exact material available, span, local path/URL, fingerprint, access basis, overlap with live Canon |
| `source-knowledge.yaml` | SPEC-03 SourceKnowledge — **what the source teaches**, in the source's frame |
| `source-concept-systems.yaml` | SPEC-03 SourceConceptSystem — knowledge that only exists in relationships between principles |
| `operational-bindings.yaml` | SPEC-04 — **our** revisable interpretation of what today's system could do with it. Never part of the source's claim |
| `ontology-mappings.yaml` | SPEC-05 terms / relationships / concepts. Source terminology preserved verbatim, mapped rather than normalised |
| `qa-bank.yaml` | The grounded Q&A bank |
| `EXTRACTION-NOTES.md` | Method, hazards, what was deliberately not extracted, self-check results |

Repository-level files:

| File | What it is |
|---|---|
| `SCHEMA-CONTRACT.md` | The binding schema and controlled vocabulary all four lanes followed |
| `SOURCE-STATUS.csv` | One row per candidate source |
| `QA-MANIFEST.json` | Every Q&A item plus counts by source, answer type, difficulty, knowledge type, application |
| `CROSS-SOURCE-OBSERVATIONS.md` | **Observations only** — potential agreements, contradictions, relationships. Explicitly *not* promoted to accepted cross-source concepts |
| `validate_experimental.py` | The validators |
| `build_manifest.py` | Mechanical consolidation |

---

## 6. Rules the extraction was held to

- Source claims remain source claims; practitioner opinion did not become universal truth.
- Physical-production advice was **not** rewritten as generative-media instruction. Production
  bindings carry `status: production_candidate` and `target_path: null`, because Production IR does
  not exist.
- Applicability and limits recorded on every binding.
- **Disagreement between sources preserved, not resolved.** No cross-source agreement was
  manufactured.
- SPEC-05 independence rules respected: **no `cross_source_concept` was created anywhere in this
  task.** Hopkins × Hopkins is one authorial position stated twice and is recorded as a dependence,
  not a convergence.
- Technology-contingent and historical-convention knowledge labelled as such.
- **No model capability inferred from any book.**

---

## 7. Known limitations

1. **Nothing here has passed the Audit Gate.** No `*.audit.yaml` record exists for any of these four
   sources, so under `canon/audit/AUDIT-GATE-v0.2.md` none of them may be used for cross-source
   promotion, downstream product use, or retrieval work. They are source evidence, not accepted
   knowledge.
2. **The run adds 12 independent origins, not 17.** Five of the seventeen are scope extensions of
   works already live, with zero independence against their counterpart, and *My Life in
   Advertising* is a new work by an author already in Canon. Any later cross-source promotion must
   use the pairwise dependence rules, not a count of directory names — the failure SPEC-05
   governance rule 5 exists to prevent.
3. **Six files were excluded despite the Controller's authorisation** because their filenames record
   a piracy-mirror origin. Three of those (Lupton, Bang, Williams) were processed historically under
   the superseded SPEC-02 atom schema, so a re-extraction under the current architecture — which the
   portfolio noted might close gap **G9** at zero acquisition cost — did **not** happen and remains
   open.
4. **Hopkins is heavily era-bound.** Mail order, coupon keying, door-to-door sampling, 1920s
   American consumer culture. Objects are labelled `historical_claim` / `culturally_bounded`, and
   they were **not** modernised. Some passages reflect 1927 attitudes to gender and class, and one
   whole class of his work (patent medicine) the author himself later disavowed; that material is
   recorded as source position, not as guidance.
5. ***My Life in Advertising* is an OCR'd older scan** with running heads interleaving into body
   text and damaged display type. Affected objects carry `extraction_uncertainty: ocr_degraded`.
   Long verbatim quotation was avoided for this reason as well as for copyright.
6. **Retrospective self-report.** Hopkins is a successful man explaining his own success at the end
   of his career. Survivorship and self-attribution are unmanaged by the source and are not
   corrected by this extraction — they are recorded.
7. **WCAG's thresholds are web-accessibility conformance criteria, not commercial-creative
   legibility rules.** Any application to feed creative, thumbnails or packshots is *our*
   extrapolation and lives only in bindings marked `extractor_inference`, never in a source claim.
8. **Google's ABCD guidance is platform-contingent and the publisher has a declared interest** — it
   sells advertising on the platform whose effectiveness its research validates. Third-party review
   involvement moderates this; it does not remove it. Every effectiveness object carries both
   cautions.
9. **The Q&A banks are ungraded.** No one has answered them, no model has been run against them, and
   no difficulty calibration has been empirically checked. `difficulty` is an extractor judgement.
10. **Figures.** WCAG and the Google pages carry diagrams and example imagery that were not
    inspected as images; the Hopkins books argue in prose and reproduce no advertisements at all
    (a known audit pattern for *Scientific Advertising* — a 1923 reader was in the same position we
    are). Where a figure would have been needed, lanes recorded
    `figure_semantic_binding_lost` in their extraction notes.
11. **Cross-source observations are unadjudicated.** `CROSS-SOURCE-OBSERVATIONS.md` records
    apparent agreements and contradictions without resolving any of them. Several would be
    disqualified from promotion anyway by the Hopkins–Hopkins dependence.

---

## 8. Reproducing the checks

```bash
python3 canon/experimental/book-expansion-qa-v1/validate_experimental.py
python3 canon/experimental/book-expansion-qa-v1/build_manifest.py
```

The validator checks that every Q&A item resolves to a source and carries a non-empty locator, that
required fields and controlled enums are respected, that every binding resolves to Source Knowledge
or a Source Concept System, that no answer is a placeholder, that Hopkins page locators fall inside
each book's real printed-page span, that the SPEC-03/04/05 structural rules hold, and — via git —
that **nothing outside this directory was modified**. It reports application-question counts per
source and fails if any bank falls below one third.
