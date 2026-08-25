# CANON-008 — Controller brief

**Task:** CANON-008, Wave 1 — Devanagari typeface structure (Girish Dalvi, *Conceptual Model for
Devanagari Typefaces*, IDC IIT Bombay, 2010)
**Date:** 25 Aug 2026 · **Branch:** `work/canon-008-dalvi-devanagari` · **Task-base:** `main` at `f8abfe8`
**Status:** **STOPPED AT THE ACQUISITION GATE — no extraction performed** · **needs_controller_review**
**Severity:** `LOCAL`. No SPEC or Audit Gate change. No source ingested.

---

## Bottom line

**The official archive route exposes only a 3-page abstract, not the thesis. The task's own gate
condition 5 fires, so I stopped before extraction.**

Live Canon stays at **19 sources / 19 audit records**. Historical CANON-003/004 remain 16.

This is the gate working as designed, not a failure to find the file. The record's full-text access
sits behind IITB SSO, which I neither hold nor attempted to work around.

---

## 1. What the official route actually resolves to

Route used, exactly as the task names it, with no mirror, reupload, Google Books, Internet Archive
copy or the superseded Fiona Ross metadata:

`https://dsource.in/dcontent/idc-archive/collection/collection-details2.php?id=1275`

The record loads (HTTP 200) and is unambiguously the right project — its heading reads **"Conceptual
Model for Devanagari Typefaces"** under *Home / Projects / Thesis / Detail*.

**It exposes exactly one downloadable artifact**, referenced three times in the page — once by the
inline PDF viewer, once by its fallback, and once by the "Click here to download" link:

```
doc/idc-girish-pdh-abstract.pdf
```

Two access paths exist for it. The direct asset path returns **403**; the archive's own
`view-pdf.php` wrapper returns the file. I used the wrapper — the route the record itself links.

## 2. Artifact identity, recorded before any extraction

| Check | Value |
|---|---|
| File | `idc-girish-pdh-abstract.pdf` via `view-pdf.php?file=doc%2Fidc-girish-pdh-abstract.pdf` |
| HTTP | 200, `application/pdf` |
| **Bytes** | **50,197** |
| **SHA-256** | **`e9baa76ca7b8338842f9bf35bce098f4a7cff8e7765fa2f44ff53481d92d2cf7`** |
| **Pages** | **3** |
| PDF version | 1.6 |
| Encrypted | no |
| Page size | 612 × 792 pt (US Letter) |
| **PDF `Title` metadata** | **`Abstract.xps`** |
| Creator / Producer | Adobe Acrobat 9.3.2 / Acrobat 9.3.2 XPS Conversion Plug-in |
| Created / Modified | 18 Jan 2011 / 17 Mar 2023 |

**Identity from the artifact itself** (gate condition 2): its first line reads *"Conceptual Model for
Devanagari Typefaces (2010)"* followed by *"Girish Dalvi"*. Author, title and year are confirmed
from the document, not from the web page. The institution is established by the hosting archive
rather than by the artifact — the abstract carries no title page, no institutional imprint and no
supervisor statement.

## 3. Why this is an abstract and not the thesis — four independent signals

1. **Its own heading is "Research Abstract."** That is the document's first section title.
2. **Three pages, 841 words.** A PhD thesis it is not.
3. **The PDF's title metadata is literally `Abstract.xps`.**
4. **It contains a section called "Organization of the thesis" that *describes* six chapters it does
   not contain.** It says chapter two surveys "differences in the methods and nomenclature proposed
   by earlier authors to describe the anatomy of Devanagari letters", chapter three details the
   expert/non-expert classification experiment and cluster analysis, and chapter four presents the
   conceptual model with "the underlying concepts, terms of Devanagari fonts and the relations that
   exist between them".

**That fourth point is the decisive one.** Everything CANON-008 asks me to extract — anatomy and
reference-line structure, competing non-standardized terminology, classification dimensions, the
conceptual model, the participant study — is *named* in this artifact and *present* in none of it.

## 4. The archive distinguishes abstracts from theses, and for this record holds only the abstract

This is not a naming coincidence. The two neighbouring IDC thesis records linked from the same
listing expose full documents under a different convention:

| Record | Title | Exposed artifact |
|---|---|---|
| id=1274 | *Knowledge Representation of Grids in Graphic Design…* (Bokil) | `idc-prasad-bokil-**thesis**.pdf` |
| id=1690 | *Visual framework of color analysis of shop signs…* (Nanki) | `idc-nanki-phd-**report**.pdf` |
| **id=1275** | **Conceptual Model for Devanagari Typefaces (Dalvi)** | **`idc-girish-pdh-**abstract**.pdf`** |

So the archive does publish full theses for other students, and for this one it publishes an
abstract. I searched the archive's own Thesis listing and **id=1275 is the only record for this
thesis** — 1274 and 1690 are different projects whose card text merely sits adjacent to Dalvi's in
the listing HTML.

*Recorded precisely:* I did **not** measure the neighbouring files' sizes. `HEAD` requests through
the PHP wrapper returned no `Content-Length`, and I did not download theses outside this task's
scope to find out. The evidence above is the naming convention and the record structure, both
directly observed; the size comparison is not claimed.

## 5. What I did not do, and why

**The record page carries a "Classified Archive Access" panel requiring IITB SSO credentials.** The
full thesis is behind institutional authentication.

- I did not attempt that login. I hold no such credentials, and attempting one would be an
  access-control bypass.
- I did not probe for an unlinked direct URL such as a guessed `idc-girish-pdh-thesis.pdf`. The
  archive has deliberately gated full access; guessing at an unlinked path to get round that gate is
  the same bypass by another name, and the task's instruction is to use material *linked from that
  record*.
- I did not go to any mirror, scraped copy, reupload, Google Books or Internet Archive copy — all
  explicitly forbidden.

## 6. Why I did not ingest the abstract instead

It would have produced a source *about* a thesis rather than the thesis's knowledge. The abstract
contains no anatomy term, no reference-line structure, no classification dimension, no figure, no
participant count and no model — only sentences saying those things exist in chapters I cannot read.

Extracting it would yield objects whose claims are second-hand descriptions of unread content, and
the Audit Gate's evidence-origin audit would have to record almost every one as
`origin_unresolved`. That is precisely the identity-ambiguous outcome gate condition 5 exists to
prevent. **A blocked source is a valid adjudication result; a thin one dressed as a real ingestion
is not.**

## 7. State of the repository

Nothing was extracted and no source directory was created.

| | |
|---|---|
| CANON-003 accepted / CANON-004 method-test | **16 — unchanged** |
| Live accepted Canon | **19 — unchanged** |
| Active v0.2 audit records | **19 — unchanged** |
| SPEC-01/02/03/04/05 | unchanged |
| Audit Gate vocabulary | unchanged |
| EVAL-005 / any Eval file | untouched |
| Files added by this task | this brief and a HANDOFF note — no PDF, no render, no image |

The 3-page abstract lives only in a workspace outside the repository and is not committed.

## 8. Options for the Controller — none self-assigned

1. **Supply the full thesis through an authorised route.** Someone with IITB SSO can retrieve it
   from the Classified Archive Access panel and provide a fingerprint — file size and SHA-256 —
   exactly as Work did for CANON-007. That worked cleanly there and would let CANON-008 resume
   unchanged.
2. **Approve a different bibliographic identity.** Dalvi published peer-reviewed work derived from
   this thesis. Any such paper is a *different* source identity with its own scope and would need
   Controller approval; I have not gone looking, since selecting a replacement source is your call
   and the task forbids ingesting another Devanagari source.
3. **Repair the portfolio slot again**, as CANON-008 already did once for the unverifiable Fiona
   Ross identity.
4. **Accept the Canon at 19** and leave the Devanagari-structure gap open, recorded rather than
   filled.

I recommend **option 1** if the credential is obtainable — the source is the right one and only its
delivery is blocked. **I am not self-assigning any of these, and I am not starting CANON-009.**

## 9. One thing worth noting for whoever resumes this

The abstract, though unusable as a source, tells us the thesis's own framing: it states that
Devanagari type design has "largely been an intuitive activity" because "there exists no single,
unanimously accepted body of work which formalizes the structure and display of Devanagari
typefaces", and that existing accounts are "based on antiquated technologies".

If that holds in the full text, two CANON-008 requirements will matter more than usual: **terminology
must stay source-faithful** because the thesis itself reports the terminology as contested, and the
**technology-contingency audit** is load-bearing because the thesis explicitly positions itself
against earlier technology-bound accounts while itself being written in 2010.
