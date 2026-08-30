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

## 2. The finding that shaped this run — source access

The single most consequential thing this task established is **not** an extraction result. It is
that most of the local library cannot be cleared for use under this task's source-access rules.

The local library is `~/Downloads/Books/` — 40 files, 37 distinct titles. Its status:

- **Six files carry an explicit `libgen.li` marker in the filename**, indicating a piracy-mirror
  origin. Those are excluded outright.
- **The project's own record already flags the rest as unresolved.** CANON-003's source inventory
  (`canon/findings/CANON-003-source-inventory-and-selection.md` §2) states: *"**NOT VERIFIED:** the
  licence status of any of these copies. This is a Controller question, not one this extraction can
  settle."*
- This task's rules permit only "legitimately owned", "publisher-authorised",
  "institution-authorised", "creator-authorised", "openly licensed" or "other **clearly legitimate**
  access". **"Not verified" is not "clearly legitimate."**

So the in-copyright commercial titles are recorded as `available = false`,
`legitimate_access_basis = not established`, and were not opened. That is **not** an accusation
about any individual file — it is the honest statement that this task could not establish the basis
its own rules require, on a question the project has explicitly reserved to the Controller.

**What survived that filter, and why:**

| Source | Why it clears the bar |
|---|---|
| Hopkins, *My Life in Advertising* (1927) | The **work** is in the public domain (US term for 1927 publications expired 1 Jan 2023; author died 1932). Copyright status of the work governs, independent of which scan is on disk. |
| Hopkins, *Scientific Advertising* ch. 8–21 (1923) | Same: US term for 1923 publications expired 1 Jan 2019. |
| W3C, WCAG 2.2 | Openly published standard under the W3C Document Licence. |
| Google, "ABCDs of effective video ads" | Publisher-authorised, free, unauthenticated, from Google-owned pages. A third-party Scribd reupload of a fuller guide exists and was **deliberately not used**. |

**Nothing was purchased, downloaded from a mirror, de-DRM'd, scraped past a paywall, or accessed
through anyone's credentials.** Two candidates were abandoned rather than routed around: the Dalvi
Devanagari thesis (IIT Bombay SSO — the same wall CANON-008 stopped at) and the Cayla & Elson
article (journal paywall).

---

## 3. Sources discovered, processed, skipped, unavailable

Full row-per-candidate detail: **`SOURCE-STATUS.csv`** (46 rows).

| Disposition | Count |
|---|---|
| Candidate sources inventoried | **46** |
| **Processed** | **4** |
| Skipped — already live Canon | 19 |
| Skipped — already processed historically, not live (and access not established) | 3 |
| Skipped — blocked on source integrity (image-only scan / no extractor) | 4 |
| Skipped — access legitimacy not established | 11 |
| Unavailable — official route failed or identity unresolved | 5 |

### Processed

| # | Source | Kind | Scope | Overlap with live Canon |
|---|---|---|---|---|
| 1 | **Claude C. Hopkins, *My Life in Advertising*** (Harper & Brothers, 1927) | full book, new source | 19 chapters, printed pp. 1–208 | **`shared_author` dependence** with live `hopkins-scientific-advertising-ch1-7`. **Not an independent origin against it.** |
| 2 | **Claude C. Hopkins, *Scientific Advertising*** ch. 8–21 (1923) | **scope extension** of a live source | printed pp. 25–64 | **Same work** as live `hopkins-scientific-advertising-ch1-7`. Zero independence. Ch. 1–7 knowledge deliberately not re-extracted. |
| 3 | **W3C, WCAG 2.2** — Guideline 1.4 contrast / text-presentation criteria | open standard | success criteria + normative glossary + non-normative Understanding notes | None. Independent origin. The corpus's first standards document and its first numeric criteria. |
| 4 | **Google, "ABCDs of effective video ads"** | platform guidance | 3 official Google pages, retrieved 30 Aug 2026 | None. Independent origin. The corpus's first short-form / feed-native source. |

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
2. **Access legitimacy, not source quality, determined the portfolio.** The four sources processed
   are the ones whose access basis could be established — not the four the Canon most needs. Eleven
   genuinely unconsumed, subject-relevant titles sit unopened behind an unresolved licence question
   that only the Controller can settle. This is the single biggest limitation of the run.
3. **Two of the four processed sources are the same author** (Hopkins), and one of those is a scope
   extension of a source already live. In independence terms this run adds **two** independent
   origins (WCAG, Google ABCD), not four.
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
