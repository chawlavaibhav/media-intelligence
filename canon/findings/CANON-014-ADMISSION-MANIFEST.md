# CANON-014 — Admission manifest

**Every candidate is in exactly one of two states. There is no third.** A candidate is READY only if
it sits under `canon/knowledge/current/<dir>/` in the exact live shape with a validating Audit Gate
v0.2 record written against those exact bytes; otherwise it is HOLD with the exact blocker named
below.

The success criterion for this task was **not** the number of admissions. It was leaving every
source in the right epistemic state.

> **Presence on this work branch is a PROPOSED Canon addition and nothing more.** READY means the
> candidate is in live shape and passes the gate. It is not live Canon until the Controller merges
> this branch.

| State | Count |
|---|---|
| **READY** | **6** |
| **HOLD** | **17** (the repaired CANON-013 candidates) |
| **Total candidates** | **23** |

**What changed in the delta pass.** The three books previously recorded as HOLD/never-supplied —
*Cinema India*, *Gods in the Bazaar*, *We Are Like That Only* — were located on the Controller's
machine as PDFs, processed first-hand, and are now READY. **The total candidate count is unchanged
at 23; three candidates moved from HOLD to READY.** No candidate moved the other way.

Mechanical status at the head of this branch, recomputed from the files themselves and not carried
forward from any earlier report:

- `canon/validation/validate_audit_gate_v02.py` → **25 records, 0 errors**
- `canon/validation/validate_source_artifact_schema.py` → **25 source directories, 3 errors**, all
  three pre-existing in the already-accepted `sutherland-alchemy-introduction`, which CANON-014 is
  not authorised to edit (recorded in `CANON-014-LIVE-SOURCE-REAUDIT-FINDINGS.md`). **All six
  CANON-014 READY sources: zero errors.**
- `canon/experimental/book-expansion-qa-v1/validate_experimental.py` → **PASSED**, after a genuine
  defect in its own boundary check was fixed (see "A validator defect was fixed, not worked around")
- `pytest tests/ --ignore=tests/test_request_freeze_gates.py` → **135 passed, 117 subtests passed**.
  **The `--ignore` is load-bearing and is not CANON-014's doing:** that file exits the interpreter at
  import, so without it pytest collects nothing at all. Routed as finding **F-06**.

---

## READY — 6

Each is in live shape with all five snapshot files plus `PROVENANCE.md`, and each has an Audit Gate
v0.2 record written against those exact bytes with `source_reopened: false`.

| Source | SK | Systems | Bindings | Ontology terms | Visual pass | `audit_status` |
|---|---|---|---|---|---|---|
| `parameswaran-nawabs-nudes-noodles` | 32 | 4 | 9 | 22 | 19/19 plates inspected | `complete` |
| `dwyer-patel-cinema-india` | 19 | 3 | 5 | 25 | 11 of ~121 plates; 7 claims checked | `complete` |
| `jain-gods-in-the-bazaar` | 18 | 3 | 6 | 30 | 7 of ~156 figures; 7 claims checked | `complete` |
| `bijapurkar-we-are-like-that-only` | 18 | 3 | 5 | 31 | **30/30 data figures**; 7 claims checked | `complete` |
| `desai-mother-pious-lady` | 17 | 2 | 4 | 18 | completed, null result | `complete` |
| `pandey-pandeymonium` | 10 | 2 | 3 | 12 | completed, evidence never printed | `complete` |
| **Totals** | **114** | **17** | **32** | **138** | 21 claim checks across the three new | — |

Binding distribution across the six, counted mechanically: **governance 16, evaluation 7, creative_ir
3, production_candidate 5, benchmark 1**. Every `production` binding carries `status:
production_candidate` and `target_path: null`, because Production IR does not exist
(PROJECT-CONTRACT separation 2). The single `benchmark` binding, on `jain-gods-in-the-bazaar`,
**adopts no threshold and creates no scorable code** — it records that a discriminating dimension
exists and stops there.

**Why these six and nothing else:** they are the only candidates whose source file was available.
That is not a coverage decision — it is the whole distinction. For these six the extraction, the
visual pass, the provenance hashes and the audit were all done first-hand against real files. For
every HOLD candidate none of that is possible here.

### Each READY record carries its own limits rather than presenting itself as clean

- **Nawabs** — `some_underdetermined`. Four of nineteen plates were opened and still do not settle
  their captions. Body copy is illegible on every plate that has it, and no object rests on any.
- **Cinema India** — `some_underdetermined`, and two bounds that must travel with it. The visual pass
  was **bounded by cost, not blocked**: 11 plates of about 121 were opened, and the ledger says so.
  More important, **the book dates its own subject as ending**: its Conclusion states that the filmi
  style it describes "is a thing of the past". Every convention in it is historical on the authors'
  own instruction. Third, the evidence base is a **survival sample** — hoardings, which the source
  itself calls the most distinctive form of its medium, were destroyed after each film's run.
- **Gods in the Bazaar** — `some_underdetermined`. The cleanest copy of the three (a publisher's
  typeset PDF, no OCR error class at all), and the pass was bounded at 7 figures of about 156.
  The author states what her interview evidence can bear, and that statement is grouped with every
  object that depends on it. The strongest-attested constraint in the book — the injunction against
  divine musculature — **was breached from the late 1980s**, which the source itself documents; the
  two must be cited together.
- **We Are Like That Only** — `all_resolved`, and the only complete visual pass in the batch. It was
  also the most necessary: **every table and figure exists only as a raster image**, their content is
  absent from the text stream, and the prose reasons from them without restating them. A text-only
  extraction would have kept the assertions and silently lost the evidence. All 30 data figures were
  opened; at least 9 tables carry content found nowhere in the text. The data is **2008 and earlier**
  and the author says so twice; every numerical object is grouped with her own vintage statement, and
  **no binding from this source carries a number**.
- **Desai** — the copy has been modified by a redistributor: publisher metadata overwritten, and one
  non-authorial sentence injected *inside* a paragraph of the Introduction. All 11 injection sites
  were located and excluded. Residual risk stated as silent and unbounded, which is why no object
  rests on a single verbatim sentence.
- **Pandeymonium** — `source_evidence_never_printed`. The campaigns are not in the book because the
  publisher put them on a companion website; the named route was unreachable in that session.

### Page addressability differs across the six and was established, never assumed

| Source | Addressability | How established |
|---|---|---|
| `dwyer-patel-cinema-india` | `authored_pages` | Real folios; printed = pdf − 2, verified at six points against the book's own contents page and a running folio |
| `jain-gods-in-the-bazaar` | `authored_pages` | Real folios; printed = pdf − 13, verified at three independent points |
| `bijapurkar-we-are-like-that-only` | `converter_pages_not_authored` | calibre-produced, US-Letter default, no folios anywhere. **`page_start`/`page_end` are `null` throughout**; every locator is chapter + section |
| `parameswaran`, `desai`, `pandey` | `no_pages_reflowable` | As recorded in the first pass |

**No page number was interpolated anywhere in this task.**

---

## HOLD — 17 repaired CANON-013 candidates

### The blocker they all share

**`evidence_insufficient` — the source cannot be opened, and the Audit Gate requires an artifact that
cannot be authored without it.**

This is mechanical, not a judgement call, and it has three independent legs:

1. **No candidate has a `visual-evidence-ledger.yaml`.** Verified: `find` returns **0** across all 17
   directories. That file is one of the five in the Audit Gate's `source_snapshot`, and the validator
   reports a missing covered artifact rather than skipping it. Without it no record can be written at
   all, for any of the 17.
2. **It cannot be authored from the environment the repair ran in.** That run read these books from a
   local library at `~/Downloads/Books/` which did not exist in the container.
3. **No external route existed either** — direct HTTPS and the harness fetch tool were both refused
   by the egress proxy for every host tried, including `w3.org` and `gutenberg.org`, so even the
   openly published sources could not be re-fetched.

**Authoring a ledger anyway would be the failure this task was set against.** A visual-evidence
ledger records what an inspection found. Transcribing a prior run's self-report into a gate artifact
and signing it would be fabricating an inspection. `evidence_insufficient` is a legitimate completed
outcome and this is what it is for.

> **A note the delta pass adds, because it now has evidence for it.** Three books were held in the
> previous pass for exactly this reason and have now been processed first-hand — and the processing
> found things no self-report would have surfaced: nine tables that exist only as images, a
> constraint breached within the period its own source covers, and a book that dates its own content
> as expired. **That is the argument for the HOLD state, not against it.** The 17 remain held.

### What was nonetheless repaired

Under `canon/experimental/book-expansion-qa-v1/`: 3 `SourceConceptSystem`s missing
`evidence.system_level_uncertainty` fixed (**not 1 as previously reported** — the reported omission
was one member of a class); 84 `dependencies`/`tradeoffs`/`conflicts` entries missing `origin` fixed,
failing closed to `extractor_inferred`; 22 artifact files missing the top-level `source_id` that
Audit Gate rule 2 resolves against fixed; all counts recomputed mechanically; the Q&A application
floor removed and the banks reclassified. All 17 pass the corrected schema validator.
Package totals, recomputed by its own validator at the head of this branch: **822 SourceKnowledge ·
70 ConceptSystems · 184 bindings · 899 Q&A items (42.8% application, observed not required)**.

**A structural PASS is not admission.** These are better than they were and still cannot pass the gate.

### Per-candidate blockers, beyond the shared one

| Candidate | Additional blocker, unresolved |
|---|---|
| `airey-logo-design-love` | The copy used was an **unattributed degraded Spanish machine translation**, so it cannot establish Airey's English vocabulary. |
| `samara-breaking-the-grid-ch2` | More than half the extraction depended on visual evidence never inspected, in a book whose designed pages are themselves the argument. |
| `freeman-photographers-eye-beyond-parts1-3` | The conversion destroyed designed-spread relationships. |
| `carroll-read-this-photographs` | Roughly half the knowledge depended on photographs unavailable to inspection. |
| `sullivan-hey-whipple`, `ogilvy-beyond-ch2` | Significant reproduced-advertisement evidence absent. Sullivan additionally carries `independence_not_established` against the live Ogilvy material, which blocks promotion independently of representation. |

The other 11 are held on the shared blocker alone.

### Five candidates worth more as re-audit evidence than as admissions

`light-science-magic-beyond-ch3`, `samara-breaking-the-grid-ch2`,
`freeman-photographers-eye-beyond-parts1-3`, `ogilvy-beyond-ch2` and
`hopkins-scientific-advertising-ch8-21` are same-work scope extensions with **zero independence**
against their live counterparts. Routed to `CANON-014-LIVE-SOURCE-REAUDIT-FINDINGS.md`.

---

## The gap this task was meant to close

The authorisation chose these six books to attack the Canon's Indian cultural and Indian visual gap,
and made the visual pass mandatory because *Gods in the Bazaar* and *Cinema India* are the visually
demanding ones. **After the first pass those two were exactly the ones missing. They are now in.**

What the corpus gains, with the bounds attached:

- **Hindi-film visual culture** — the poster and publicity conventions of a period the source itself
  dates as ending in the 1990s, with 11 plates inspected first-hand and 7 authorial visual claims
  checked and confirmed.
- **Indian calendar and bazaar art** — first-hand ethnography of a print trade, 1994-2001, with named
  informants: production constraints, a documented convention outliving its cause, and a structural
  account of why a gifting catalogue is not a demand signal. This **replaces** the corpus's only
  previous calendar-art material, which was Parameswaran's second-hand paragraph reporting Rajagopal
  — and the lineage matrix records that Parameswaran must **not** count as corroborating it.
- **Indian consumer market reasoning** — a set of named reasoning errors with worked cases, deliberately
  stripped of every number.

**Still unclosed: Devanagari and Indic typography.** Nothing in these six sources addresses it, and
the position is unchanged from CANON-013.

---

## A validator defect was fixed, not worked around

`canon/experimental/book-expansion-qa-v1/validate_experimental.py` reported
`[BOUNDARY] check 6: live Canon knowledge ... was modified — forbidden` for every file in the three
new source directories. **The finding was false and the validator was wrong.**

- **Root cause 1.** The check used `git diff --name-only`, which reports *that* a path changed and
  not *how*. Checks 6 and 7 exist to stop an accepted source or audit record being **modified**;
  CANON-014's authorised job is to **add** new candidate directories under exactly those prefixes.
  Every addition therefore tripped a check written to catch edits — and the same allowlist two lines
  below explicitly permits those prefixes. Verified mechanically: `git diff --name-status
  origin/main...HEAD -- canon/knowledge/current/ canon/audit/records/ | grep -v "^A"` returns
  **nothing**. Every path is an addition; **zero modifications**.
- **Root cause 2.** The whole block was wrapped so that any failure became a **warning**. A boundary
  check that cannot run has verified nothing. That is how a run in an environment without
  `origin/main` fetched can report PASS while checking nothing at all.
- **Root cause 3.** `canon/experimental/canon-014-qa/` — where this task's own Q&A banks live — was
  missing from the allowlist.

**The fix strengthens the check rather than relaxing it.** Additions and modifications are now
distinguished; a modification or deletion under `canon/knowledge/current/` or
`canon/audit/records/` is still an error; a set of prefixes where nothing may be written **at all**
(`coordination/`, `PROJECT-MEMORY.md`, the frozen SPECs, `governance/`, the Capability Registry) now
errors on **additions too**, which the old code would have missed if a path had been created rather
than edited; and inability to run the check is now an error instead of a warning.

---

## Raw source files

**No book bytes are committed by this task.** Verified over the committed diff and the pending
working tree: this branch adds no `.pdf`, `.epub`, `.mobi`, `.azw3` or image file of any kind. The
three PDFs consumed in the delta pass stayed on the Controller's machine and are recorded only by
SHA-256, byte count, page count and bibliographic detail in each source's `PROVENANCE.md`.

Separately, and **not introduced by CANON-014**: `canon/sources/` on `main` already holds 21
page-image JPGs and six extracted book text files, committed by `2cf4988`. This branch does not touch
them. Flagged to the Controller in the brief at O-14 as an observation, not adjudicated here.

## What would change the remaining states

| To move | Requires |
|---|---|
| Any of the 17 to READY | The source file itself, attached to a session, so a first-hand visual pass can be run and a ledger authored. For WCAG and the Google ABCD pages, network egress alone would suffice. |
| The Sullivan/Ogilvy pair out of `independence_not_established` | Re-opening Sullivan and testing whether Ogilvy's claims are load-bearing in it — the `shared_primary_informant` test. |
| Cinema India or Gods in the Bazaar to a complete visual pass | Nothing but cost. Both copies are intact, both page mappings are established and reproducible, and any plate or figure can be rendered on demand. Neither is blocked. |
