# CANON-014 — Findings about sources already in live Canon

**Nothing in this document has been acted on.** No file under `canon/knowledge/current/**` that
existed before CANON-014 has been edited, and no existing `canon/audit/records/*.audit.yaml` has been
touched. Editing an accepted source would make its audit record stale, and the Audit Gate has
**deliberately no snapshot-refresh tool** — "refreshing a snapshot against changed content without
re-examining the source would rubber-stamp exactly the staleness this field exists to catch." The
correct response to a legitimate change is to re-run the gate for that book, which requires the book.

Each finding below therefore states what was observed, what it would change, and what re-audit it
would need.

---

## F-01 — `sutherland-alchemy-introduction`: three concept systems have no `provenance`

**Status: found by CANON-014, not previously recorded anywhere. Mechanically verified.**

### Observed

Running the corrected schema validator over live accepted Canon returns exactly three errors:

```
ERROR [sutherland-alchemy-introduction] scs_sut_alc_001: missing required SourceConceptSystem field 'provenance'
ERROR [sutherland-alchemy-introduction] scs_sut_alc_002: missing required SourceConceptSystem field 'provenance'
ERROR [sutherland-alchemy-introduction] scs_sut_alc_003: missing required SourceConceptSystem field 'provenance'
```

All three `SourceConceptSystem`s in an **accepted, audited** source lack the `provenance` block that
SPEC-03's schema requires. Every other live source is clean; 22 directories were checked.

### Why it was not caught before

The same reason `scs_sa8_002` was not caught: no validator in the repository checked required-field
*presence* on `SourceConceptSystem`. `validate_canon003_integrated.py` does not, and the experimental
validator did not. The defect has been sitting in accepted Canon since the source was admitted.

### What it would change

`provenance` on a system carries `section`, page range and `source_support`. Without it, a consumer
retrieving one of these systems cannot locate it in Sutherland's text at all. That is a real loss for
a system, whose whole claim is that a structure exists *across* several places in a source.

### What it does NOT change

The source's audit record remains valid as written: the Audit Gate does not check SPEC-03 field
presence, and the record's own `source_snapshot` still matches the bytes on disk. This is a defect in
the source representation, not in its audit.

### Required path

Repairing it means opening Sutherland's *Alchemy* introduction to establish where each system sits.
That changes `source-concept-systems.yaml`, which is one of the five snapshot files, which stales
`sutherland-alchemy-introduction.audit.yaml`. So the path is: re-open the source → repair → re-run the
Audit Gate for that book → new record with a new snapshot. **Not** a hash refresh.

**Pinned by a test.** `tests/test_validate_source_artifact_schema.py::
test_live_canon_scs_provenance_defect_is_recorded_not_silently_fixed` asserts exactly three errors,
all on this source. If someone repairs the source without re-running the gate, or if a new live defect
appears, the test fails and forces this finding to be revisited.

---

## F-02 — SPEC-04's `target_type` "fixed list" is never enumerated, and live Canon uses a fifth value

### Observed

SPEC-04 validation rule 2 says `target_type` comes "from the fixed list". **SPEC-04 never enumerates
that list.** It shows four worked examples — `creative_ir`, `governance`, `production`, `evaluation`.

Live accepted Canon uses a fifth: `target_type: benchmark` appears in **13 bindings** across accepted
sources. The Audit Gate's own `application_fit` consumer vocabulary also lists `benchmark` explicitly.

### What CANON-014 did

Admitted `benchmark` in the new validator, and recorded the gap rather than "fixing" it. Accepted live
Canon governs over an unenumerated list; the alternative would have been a validator that invalidates
13 bindings in audited sources on the strength of a spec section that does not say what it claims to.

### What it would change

Nothing today. It matters the next time someone writes a binding and needs to know what the permitted
values are, because the authoritative document does not tell them.

### Recommended

Enumerate the list in SPEC-04, including `benchmark`. That is a spec edit, which is Controller
territory, not a worker's.

---

## F-03 — `light-science-magic-ch3`: the later chapters qualify and in one case reverse the live guidance

**Source: the CANON-013 `light-science-magic-beyond-ch3` lane. Not re-verified by CANON-014 — the
source is not available in this session.**

### Observed, as that lane recorded it

Four cases, all of them **one author team revising its own earlier statement within a stated scope**.
The lane recorded this correctly and it must be preserved: **none of this is cross-source
disagreement and none of it may be presented as two sources conflicting.** The extension has *zero*
independence against the live chapter (see the lineage matrix).

1. **Polarizing the light source is demoted from a remedy to a last resort.** Live `sk_lsm_c003_0019`
   states that a polarizing filter over the light turns direct reflection into polarized reflection a
   lens polarizer can then manage. The later material attaches the price the live object does not
   carry: *"Polarizing the light source has serious drawbacks and is a solution to avoid whenever
   possible"* — four to six stops in practice rather than the theoretical two, depth-of-field and
   movement consequences, heat damage to the filters, and a colour-balance shift. `origin:
   source_stated`.
2. **A polarizer's place in the remedy order is reversed between chapters 4 and 5.** Chapter 4 offers
   it among the first remedies; chapter 5's glossy-box ladder demotes it to next-to-last, with the
   optical reason stated: a box carries polarized reflection on more than one face in mutually
   perpendicular planes, so removing one effectively increases another.
3. **The glass-support-plus-polarizer trick is explicitly withdrawn for black subjects**, on the
   stated ground that much of a black subject's direct reflection is likely polarized too, so the
   filter that clears the support would probably blacken the subject.
4. Weaker: chapter 6 states its glossy-box theory is *identical* to chapters 4 and 5 while the
   material difference makes practitioners apply it the opposite way — an inversion of prescription
   rather than a qualification of a claim.

### Why this matters more than most re-audit findings

The live chapter-3 material is among the most operationally specific in the corpus. A consumer
retrieving `sk_lsm_c003_0019` today gets a remedy with **no cost attached**, when the same authors
later say it is to be avoided whenever possible. That is the shape of error the Canon exists to
prevent.

### Required path

The live source cannot be edited without staling its audit, and the qualifying material is not
admitted. Two honest options, both Controller decisions:

- **(a)** Admit the extension as a separate source, recording `derivative_of` against the live
  chapter, and let the qualification live there. Requires the book.
- **(b)** Re-run the Audit Gate for `light-science-magic-ch3` with the later material in scope, which
  produces a new snapshot as a by-product. Also requires the book.

**Neither is possible in this session.** Recorded so the choice is available when the source is.

---

## F-04 — `light-science-magic-ch3`: its visual block was environmental and is now known to be liftable

### Observed

The live ledger records `pass: attempted_and_blocked` and `visual_completeness:
blocked_visual_validation` for all fourteen of chapter 3's figures, diagnosed at the time as a macOS
privacy protection on the local library, not a source-integrity problem.

The CANON-013 extension lane reports that **the block was gone** — the file opened, and that lane
inspected **54 distinct figures**, recording 53 of them in `provenance.inspected.figures` across 28
objects with `source_support: text_and_visual`.

### What it changes

The live chapter-3 record's `inspection_state` is `not_inspected_access_blocked`, and the Audit Gate
draws a sharp distinction between that and permanent damage inside an artifact: Ogilvy's file "was
simply unreachable" and "was fixed by a macOS permission", while Albers's greyscale digitisation is
irrecoverable. Chapter 3 is in the first class. Its fourteen figures — which include matched
photographic pairs that are the chapter's proof, such as 3.13/3.14's polarising-filter comparison
with its internal validity check — are **recoverable, not lost**.

### Required path

Open the source, inspect figures 3.1–3.14, rewrite the ledger, re-run the gate. Requires the book.
**Not** a hash refresh: the current record is honest about what it saw, and the new one would say
something different.

---

## F-05 — `freeman-photographers-eye-graphic-guide`: more evidence for `false_page_affordance`

**Source: the CANON-013 `freeman-photographers-eye-beyond-parts1-3` lane. Not re-verified here.**

### Observed

The live Parts 1–3 audit established `false_page_affordance` on **five** internal cross-references
that point to the wrong place in a converter-paginated PDF. The extension lane reports finding
**eight more**, and reports resolving **no** cross-reference in the book's text — recording that the
author's semantic cross-references survive while the numeric ones do not.

### What it changes

Only the strength of a finding already accepted and correctly recorded. `false_page_affordance` and
`converter_pages_not_authored` are already on the live record; thirteen instances rather than five
does not change the classification.

### Recommended

**Do nothing.** Recording it here is sufficient. Re-running the gate to raise a count would stale a
correct audit for no gain, which is precisely what the no-refresh rule exists to prevent. Noted
because the authorisation asked for it and because the count is now known.

---

## Summary

| ID | Source | Newly found by CANON-014 | Verified here | Recommended action |
|---|---|---|---|---|
| F-01 | `sutherland-alchemy-introduction` | **Yes** | **Yes, mechanically** | Re-audit when the source is available. Pinned by a test. |
| F-02 | SPEC-04 | **Yes** | **Yes, mechanically** | Controller edits the spec to enumerate the list. |
| F-03 | `light-science-magic-ch3` | No (CANON-013 lane) | No — source unavailable | Controller chooses (a) or (b); both need the book. |
| F-04 | `light-science-magic-ch3` | No (CANON-013 lane) | No — source unavailable | Re-inspect and re-run the gate when the book is available. |
| F-05 | `freeman-photographers-eye-graphic-guide` | No (CANON-013 lane) | No — source unavailable | None. Already correctly classified. |

**F-01 and F-02 are the two CANON-014 found itself, and both were found by the corrected validator
that this task was asked to build** — which is the clearest evidence that the schema hole it closed
was worth closing.
