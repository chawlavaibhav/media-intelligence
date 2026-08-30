# CANON-014 — Canon correction, expansion and admission-preparation pack

**Status:** complete on a work branch. **Not merged. Not live knowledge.**
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
  visual.
- **C** — produce the result in the shape required for addition to live Canon: whatever genuinely
  passes the current Audit Gate ends the branch in accepted-source form; whatever cannot pass is
  explicitly held.

**Explicitly out of scope and untouched:** `coordination/**`, `PROJECT-MEMORY.md`, `eval/**`,
`resources/**`, `governance/**`, the Capability Registry, Production IR, and any programme state. No
merge to `main`. No Controller state updated. No cross-source promotion.

## 3. What was actually available

**Three of the six named books were attached to this session**: Parameswaran, Desai, Pandey.
*Cinema India*, *Gods in the Bazaar* and *We Are Like That Only* were not, and this environment has
**no external network egress** — verified, not assumed: a direct HTTPS request and the harness fetch
tool were both refused by the egress proxy for every external host tried.

That same absence is what makes the seventeen CANON-013 candidates unopenable here: they were read
from a local library on the Controller's machine, and this is a fresh remote container. It also means
the two openly published candidates (WCAG 2.2, the Google ABCD pages) and the two public-domain
Hopkins texts could not be re-fetched either.

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

### B — the three supplied books, in accepted shape

| Source | SK | Systems | Bindings | Terms | Visual pass |
|---|---|---|---|---|---|
| `parameswaran-nawabs-nudes-noodles` | 32 | 4 | 9 | 22 | **19/19 plates inspected first-hand** |
| `desai-mother-pious-lady` | 17 | 2 | 4 | 18 | completed, null result |
| `pandey-pandeymonium` | 10 | 2 | 3 | 12 | completed, evidence never printed |
| **total** | **59** | **8** | **16** | **52** | |

Each has all five snapshot files plus `PROVENANCE.md`, and an Audit Gate v0.2 record written against
those exact bytes.

### C — admission preparation

- 3 READY, 20 HOLD. `canon/findings/CANON-014-ADMISSION-MANIFEST.md`.
- Pairwise lineage matrix correcting the previous run's global independence count.
- Live-source re-audit findings, including two CANON-014 found itself.
- Corrected schema validator + 44 tests.
- 64-item grounded Q&A for the new sources, kept outside the Canon source snapshot.

## 5. Rules held to

- **No `cross_source_concept` anywhere.** Mechanically verified across the whole repository: zero
  concepts with `kind: cross_source_concept` and zero with `asserts_agreement_between_sources: true`.
  Apparent agreements are recorded as observations in the lineage matrix.
- **No model capability inferred from any book.** Both production bindings carry
  `status: production_candidate` with `target_path: null`.
- **No accepted live knowledge edited.** No pre-existing file under `canon/knowledge/current/**` or
  `canon/audit/records/**` was changed. Defects found in accepted Canon are routed as findings.
- **No page number interpolated.** All three sources are reflowable with no authored page; every
  locator is a chapter or essay title.
- **Source terminology preserved**, including Hindi terms, recorded in the source's own form with the
  source's gloss.
- **A structural validator PASS is never described as Canon admission.**

## 6. Deliverables

| # | Deliverable | Path |
|---|---|---|
| 1 | This task file | `canon/tasks/CANON-014-CANON-EXPANSION-ADMISSION-PACK.md` |
| 2 | Repaired CANON-013 material | `canon/experimental/book-expansion-qa-v1/**` |
| 3 | Extractions for the supplied books | `canon/knowledge/current/{parameswaran-…,desai-…,pandey-…}/` |
| 4 | Live-form directories for READY candidates | same as 3 |
| 5 | Audit Gate v0.2 records | `canon/audit/records/{parameswaran-…,desai-…,pandey-…}.audit.yaml` |
| 6 | Candidate lineage matrix | `canon/findings/CANON-014-CANDIDATE-LINEAGE-MATRIX.yaml` |
| 7 | READY/HOLD admission manifest | `canon/findings/CANON-014-ADMISSION-MANIFEST.md` |
| 8 | Corrected consolidated counts | in this file, the manifest and the brief |
| 9 | Grounded Q&A + manifest | `canon/experimental/canon-014-qa/` |
| 10 | Validator correction + tests | `canon/validation/validate_source_artifact_schema.py`, `tests/test_validate_source_artifact_schema.py` |
| 11 | Live-source re-audit findings | `canon/findings/CANON-014-LIVE-SOURCE-REAUDIT-FINDINGS.md` |
| 12 | Controller Brief | `canon/findings/CANON-014-CONTROLLER-BRIEF.md` |

## 7. Mechanical status at the branch head

```
canon/validation/validate_audit_gate_v02.py            22 records, 0 errors
canon/validation/validate_source_artifact_schema.py    22 dirs, 3 errors (all pre-existing, F-01)
canon/experimental/.../validate_experimental.py        PASSED
tests/test_validate_audit_gate_v02.py                  60 passed, 105 subtests
tests/test_validate_source_artifact_schema.py          44 passed
tests/test_validate_canon003_integrated.py              5 passed
tests/test_value_gate_corrections.py                   26 passed
tests/test_request_freeze_gates.py                     passes as a script (pre-existing: it calls
                                                       sys.exit() at import, so pytest cannot
                                                       collect it; unmodified by CANON-014)
```

## 8. Stop condition

Branch complete; draft PR opened to `main`; **not merged**. Controller state not updated. No T2B, no
media generation, no other programme task started.
