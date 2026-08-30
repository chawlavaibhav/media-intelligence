# CANON-014 — Canon correction, expansion and admission-preparation pack

**Status:** complete on a work branch, **including the delta-completion pass**. **Not merged. Not
live knowledge. Not marked ready for merge.**
**Authority:** the Controller authorisation issued to this session, reproduced in scope below.
**Branch:** `claude/canon-014-expansion-admission-ntp0dl`.

> **A task file is not an authorisation.** This file records what CANON-014 was authorised to do and
> what it did. It authorises nothing by itself, and it does not make anything under
> `canon/knowledge/current/**` on this branch live. Those paths become live knowledge **only if the
> Controller merges the branch.**

---

## 1. Branch naming — a deviation to record

The authorisation named the branch `work/canon-014-canon-expansion-admission-pack`. This session's
operating constraints designate `claude/canon-014-expansion-admission-ntp0dl` and forbid pushing to
any other branch. **The designated branch was used.** Nothing else about the authorisation is
affected; the branch name is the only deviation and it is recorded here rather than silently
resolved.

## 2. Scope, as authorised

Three connected jobs:

- **A** — repair the CANON-013 experimental Canon expansion (17 sources), fixing the substantive and
  mechanical problems identified after that run rather than regenerating the same package.
- **B** — fully consume six newly supplied books, including visual evidence where the argument is
  visual. **All six are now done**: three in the first pass, three in the delta-completion pass
  authorised afterwards, which found the remaining books locally as PDFs.
- **C** — produce the result in the shape required for addition to live Canon: whatever genuinely
  passes the current Audit Gate ends the branch in accepted-source form; whatever cannot pass is
  explicitly held.

**Explicitly out of scope and untouched:** `coordination/**`, `PROJECT-MEMORY.md`, `eval/**`,
`resources/**`, `governance/**`, the Capability Registry, Production IR, and any programme state. No
merge to `main`. No Controller state updated. No cross-source promotion. Verified mechanically at the
branch head: `git diff --name-only origin/main...HEAD` touches none of those paths.

## 3. What was actually available

**Updated by the delta pass. All six named books have now been processed.**

- **First pass** — Parameswaran, Desai and Pandey were attached to that session and processed.
- **Delta pass** — *Cinema India*, *Gods in the Bazaar* and *We Are Like That Only* were found in
  `~/Downloads/` on the Controller's machine as **PDFs**, which is why an EPUB-shaped search in the
  first pass did not find them. All three were processed first-hand.

**The delta authorisation's own premise was wrong and was checked rather than accepted.** It named
Desai, Parameswaran and Pandey as the missed three; all three were already complete on this branch,
verified by matching the local files' SHA-256 hashes against the values recorded in their committed
`PROVENANCE.md` files. The correction was reported and confirmed before any work proceeded.

The seventeen CANON-013 candidates remain unopenable: they were read from a local library at
`~/Downloads/Books/` which does not exist here, and the first pass verified there is no external
network egress either. That is still what holds them.

## 4. What was produced

### A — repair of the CANON-013 package

Under `canon/experimental/book-expansion-qa-v1/`:

| Defect | Reported | Actually found | Fixed |
|---|---|---|---|
| `SourceConceptSystem` missing `evidence.system_level_uncertainty` | 1 | **3** | 3 |
| `dependencies`/`tradeoffs`/`conflicts` entry missing `origin` | not reported | **84** | 84 |
| Artifact file missing top-level `source_id` (Audit Gate rule 2) | not reported | **22** | 22 |

Values for `system_level_uncertainty` were authored from each object's own recorded origin fields —
a statement about the record, not a new claim about a book — and each says so. `origin` failed closed
to `extractor_inferred`: an origin never recorded cannot afterwards be asserted to be the source's.

**Counts recomputed mechanically from final files**, never copied from a report:
822 SourceKnowledge · 70 concept systems · 184 bindings · **823 ontology terms** · 899 Q&A.
The 777 ontology figure in the previous chat report is wrong; 823 is correct and was already correct
in that package's own README.

**Q&A one-third application floor removed.** A screen over all 899 items found no near-duplicate
question, no answer under 35 words and no item without a support quotation — so nothing was deleted
and nothing added. The defect was in the label. Reclassified against the authorisation's own
criterion: 116 false→true, 79 true→false, natural rate **42.8%**. Both labels retained
(`requires_application_canon013`). Bank marked GROUNDED, UNGRADED, UNCALIBRATED.

### B — the six named books, in accepted shape

| Source | SK | Systems | Bindings | Terms | Visual pass |
|---|---|---|---|---|---|
| `parameswaran-nawabs-nudes-noodles` | 32 | 4 | 9 | 22 | **19/19 plates inspected first-hand** |
| `dwyer-patel-cinema-india` | 19 | 3 | 5 | 25 | 11 of ~121 plates; 7 claims checked, all confirmed |
| `jain-gods-in-the-bazaar` | 18 | 3 | 6 | 30 | 7 of ~156 figures; 7 claims checked, all confirmed |
| `bijapurkar-we-are-like-that-only` | 18 | 3 | 5 | 31 | **30/30 data figures**; 7 claims checked |
| `desai-mother-pious-lady` | 17 | 2 | 4 | 18 | completed, null result |
| `pandey-pandeymonium` | 10 | 2 | 3 | 12 | completed, evidence never printed |
| **total** | **114** | **17** | **32** | **138** | 21 claim checks across the three delta sources |

Each has all five snapshot files plus `PROVENANCE.md`, and an Audit Gate v0.2 record written against
those exact bytes with `source_reopened: false`. Binding distribution: governance 16, evaluation 7,
creative_ir 3, production_candidate 5, benchmark 1.

### C — admission preparation

- **6 READY, 17 HOLD**, 23 candidates in total — unchanged in total; three moved HOLD → READY.
  `canon/findings/CANON-014-ADMISSION-MANIFEST.md`.
- Pairwise lineage matrix (**v2**) correcting the previous run's global independence count and
  recording the three real relations found in the delta pass. Two forward rows recorded in v1 became
  live exactly as predicted; a third correctly stayed forward.
- Live-source re-audit findings, including two CANON-014 found itself.
- Corrected schema validator + tests; **a boundary-check defect in `validate_experimental.py` fixed
  at the root**; **two portability defects in `tests/test_request_freeze_gates.py` fixed** so the
  whole suite collects and runs.
- **129-item grounded, ungraded, uncalibrated research Q&A** across six banks, kept outside the Canon
  source snapshot. **Not a benchmark and not benchmark ground truth.** Natural application rate
  **25.6%**; the one-third floor is removed and four of the six banks fall below it, which is the
  correct outcome rather than a shortfall.

## 5. Rules held to

- **No `cross_source_concept` anywhere.** Mechanically verified across the whole repository: zero
  concepts with `kind: cross_source_concept` and zero with `asserts_agreement_between_sources: true`.
  Apparent agreements are recorded as observations in the lineage matrix.
- **No model capability inferred from any book.** Both production bindings carry
  `status: production_candidate` with `target_path: null`.
- **No accepted live knowledge edited.** No pre-existing file under `canon/knowledge/current/**` or
  `canon/audit/records/**` was changed. Defects found in accepted Canon are routed as findings.
- **No page number interpolated anywhere.** Addressability was established per source, not assumed:
  *Cinema India* and *Gods in the Bazaar* have real printed folios (offsets pdf − 2 and pdf − 13,
  each verified at multiple independent points against the book's own contents page and running
  heads), so their locators cite printed pages. The other four have no authored page in the copies
  used, so `page_start`/`page_end` are `null` and every locator is a chapter and section heading.
- **No raw book bytes committed.** No `.pdf`, `.epub`, `.mobi`, `.azw3` or image file is added by
  this branch, verified over both the committed diff and the working tree. Only derived Canon
  artifacts.
- **Acquisition provenance not adjudicated**, per the Controller's explicit instruction. Filename
  source markers are recorded as bibliographic facts and were not treated as grounds for exclusion.
- **Source terminology preserved**, including Hindi terms, recorded in the source's own form with the
  source's gloss.
- **A structural validator PASS is never described as Canon admission.**

## 6. Deliverables

| # | Deliverable | Path |
|---|---|---|
| 1 | This task file | `canon/tasks/CANON-014-CANON-EXPANSION-ADMISSION-PACK.md` |
| 2 | Repaired CANON-013 material | `canon/experimental/book-expansion-qa-v1/**` |
| 3 | Extractions for all six books | `canon/knowledge/current/{parameswaran-…,desai-…,pandey-…,dwyer-patel-cinema-india,jain-gods-in-the-bazaar,bijapurkar-we-are-like-that-only}/` |
| 4 | Live-form directories for READY candidates | same as 3 |
| 5 | Audit Gate v0.2 records | `canon/audit/records/<source-dir>.audit.yaml` — one per READY source, six in total |
| 6 | Candidate lineage matrix | `canon/findings/CANON-014-CANDIDATE-LINEAGE-MATRIX.yaml` |
| 7 | READY/HOLD admission manifest | `canon/findings/CANON-014-ADMISSION-MANIFEST.md` |
| 8 | Corrected consolidated counts | in this file, the manifest and the brief |
| 9 | Grounded Q&A + manifest | `canon/experimental/canon-014-qa/` |
| 10 | Validator correction + tests | `canon/validation/validate_source_artifact_schema.py`, `tests/test_validate_source_artifact_schema.py` |
| 10b | Boundary-check defect fix | `canon/experimental/book-expansion-qa-v1/validate_experimental.py` |
| 10c | Test-suite portability fix | `tests/test_request_freeze_gates.py` |
| 11 | Live-source re-audit findings | `canon/findings/CANON-014-LIVE-SOURCE-REAUDIT-FINDINGS.md` |
| 12 | Controller Brief | `canon/findings/CANON-014-CONTROLLER-BRIEF.md` |

## 7. Mechanical status at the branch head

Recomputed at the end of the delta pass. Every number is read from the files, not carried forward.

```
canon/validation/validate_audit_gate_v02.py            25 records, 0 errors
canon/validation/validate_source_artifact_schema.py    25 dirs, 3 errors (all pre-existing, F-01,
                                                       in sutherland-alchemy-introduction; all six
                                                       CANON-014 READY sources: 0 errors)
canon/experimental/.../validate_experimental.py        PASSED (after its own boundary-check defect
                                                       was fixed at the root — see the manifest)
pytest tests/                                          136 passed, 117 subtests passed
tests/test_request_freeze_gates.py (standalone)        all 7 gates fire; exit 0
```

**Two defects in `tests/test_request_freeze_gates.py` were fixed, and neither weakens it.** `ROOT`
was hardcoded to `/home/user/media-intelligence`, the absolute path of the container the test was
written in, so it could not run in any other checkout; and its runner block ran at module scope, so
importing the file called `sys.exit(0)` and pytest aborted collection of the **entire suite** with an
INTERNALERROR before a single test ran. `ROOT` is now derived from the file's own location and the
runner block is guarded by `if __name__ == "__main__"`. No assertion, gate or fixture is changed, and
the standalone entry point behaves exactly as before. The suite previously reported 135 passed only
because that file was explicitly ignored; it now collects and passes with everything else.

**Mechanical checklist, all passing:** every YAML and JSON in `canon/` parses; IDs unique across the
six sources; every internal reference resolves; every SourceConceptSystem carries
`system_level_uncertainty`, `whole_system_claim.origin` and `ordering.origin`; no Creative IR or
Production IR vocabulary appears in any SourceKnowledge; every `production` binding is a
`production_candidate` with `target_path: null`; zero `cross_source_concept` and zero
`asserts_agreement_between_sources: true` anywhere in `canon/knowledge` or `canon/audit`; every Q&A
item has a unique id, a non-empty locator, a support quotation and a matching `source_id`; every live
source directory has exactly one audit record; no HOLD candidate appears under
`canon/knowledge/current/**`; every audit snapshot digest matches the bytes on disk, recomputed
independently of the validator; no binary file added by this branch; and the no-authored-page source
carries `null` pages throughout.

## 8. Stop condition

Branch complete; draft PR opened to `main`; **not merged**. Controller state not updated. No T2B, no
media generation, no other programme task started.
