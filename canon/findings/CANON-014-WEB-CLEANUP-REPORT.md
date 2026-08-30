# CANON-014 web-cleanup lane — report

**Branch:** `work/canon-014-web-cleanup`, cut from current `main` (`bf02dd1`).
**Donor:** PR #66 (`claude/canon-014-expansion-admission-ntp0dl`) — used as a reference, not merged.
**Not for merge** until reconciled with the laptop agent's completion branch.

A parallel lane. The laptop agent is processing the three missing PDF sources (*Cinema India*,
*Gods in the Bazaar*, *We Are Like That Only*); **this lane did not touch them.** Its job was to
repair and rigorously re-review the material already produced for the three EPUB sources, and to
harden the validator that was supposed to have caught the defects in the first place.

---

## 1. What this branch contains, and deliberately does not

**Contains:** the hardened validator and its tests; corrected Parameswaran and Pandey candidates in
live shape with regenerated Audit Gate records; the Desai extraction relocated to a non-live
candidate area as HOLD; this report.

**Deliberately excluded:** the 17-source `canon/experimental/book-expansion-qa-v1/**` package (those
remain experimental/HOLD and are not this lane's business); the three missing PDFs; the Q&A banks;
the CANON-014 task file, lineage matrix, admission manifest and Controller Brief; any
Controller-state or programme-state edit; any raw source book.

---

## 2. Validator defects found

The donor validator closed one serious hole — it checked required-field **presence**, which the
CANON-013 validator did not. It still checked almost none of the specs' controlled **vocabularies**.
That is why free prose, invented relation names and an out-of-vocabulary `label_origin` all passed.

| # | Defect in the donor validator | Consequence |
|---|---|---|
| V-1 | `label_origin` never checked | `source_stated`, not a SPEC-03 value, passed on 4 objects |
| V-2 | `evidence.characteristics` membership never checked | any string would have passed |
| V-3 | `evidence.source_uncertainty` never checked | free prose passed on 29 objects |
| V-4 | `evidence.extraction_uncertainty` never checked | free prose passed on 5 objects |
| V-5 | `intra_source_relations` never checked at all | 8 invented relation names passed on 23 relations |
| V-6 | relation targets never resolved | a dangling `target` would have passed |
| V-7 | `caveats[].origin` presence checked, value not | any string would have passed |
| V-8 | SCS `system_type`, `system_type_origin`, `label_origin` never checked | out-of-vocabulary values passed |
| V-9 | `whole_system_claim.origin` never checked | ditto |
| V-10 | `ordering.scheme` never checked | ditto |
| V-11 | `membership_origin` presence checked, value not | ditto |
| V-12 | structural `origin` presence checked, value not; `between` refs never resolved | ditto |
| V-13 | binding `role` never checked (vocabulary or non-empty) | any string, or `[]`, would have passed |
| V-14 | binding `evidence_basis` and `status` never checked | ditto |
| V-15 | `governance_consumer` never checked | ditto |
| V-16 | `observation_unit` presence checked, value not | ditto |
| V-17 | SPEC-04 rule 8 (ontology refs are SPEC-05 identifiers) never checked | raw strings would have passed |
| V-18 | **SPEC-05 essentially unvalidated** — no term fields, `origin`, `kind`, relation vocabulary, relation endpoints, concept kinds, `children_terms` resolution | 20 mis-kinded terms passed |
| V-19 | SPEC-05 repair `executable_by` never checked | 9 repair terms had none; the generative gap SPEC-05 exists to keep visible was invisible |
| V-20 | concept invariants never checked | a `canonical_concept` without `asserts_equivalence: false`, a `source_specific_concept` asserting agreement, or a `cross_source_concept` with one origin would all have passed |

### A defect this lane introduced and caught

Writing V-17 strictly — ontology refs must resolve to a `term_id` — produced **5 errors against
accepted live Canon**, in `freeman`, `grammar-of-the-edit` and `samara`. Those sources bind
canonical **concepts** (`cc_perceived_break_at_a_transition` and similar), which are SPEC-05
identifiers just as terms are. The validator was wrong, not the audited sources. Fixed to resolve
against both, with a test pinning that a `concept_id` is accepted.

This is recorded because it is the useful kind of near-miss: a stricter validator run against
accepted Canon is how an over-strict rule gets caught before it invalidates audited work.

## 3. Validator defects fixed

All twenty, plus the self-inflicted one. The validator now checks every controlled vocabulary in
SPEC-03, SPEC-04 and SPEC-05, plus reference resolution in five directions (relation targets,
member `sk_ref`s, structural `between` refs, binding source/system refs, ontology refs, relationship
endpoints, `children_terms`).

**88 tests**, including a malformed fixture for every vocabulary. Each asserts the invalid value
actually **fails** — a validator that passes malformed examples is not done. The battery covers all
eight invented relation names found in the candidates, `source_stated` as a `label_origin`, prose in
both uncertainty fields, `source_specific_concept` used as a term kind, an invalid repair executor,
and every concept invariant.

---

## 4. Source dispositions

### Parameswaran — *Nawabs, Nudes, Noodles* → **READY**

Structurally clean and substantively reviewed. What was preserved, as instructed: 19/19 plates
inspected; six mechanisms discovered only through visual inspection; four caption/plate pairs
correctly left underdetermined; the historical, platform and cultural boundaries; the
evidence-origin distinctions.

**32 SourceKnowledge · 4 systems · 9 bindings · 22 ontology terms.**
`audit_status: complete`, snapshot regenerated against the corrected bytes,
`source_reopened: false` — every correction was made from committed bytes, not by reopening the book.

### Pandey — *Pandeymonium* → **READY**

Structurally clean and substantively reviewed. Preserved: the survivorship caveats, the
hindsight/counterfactual cautions, the practitioner-assertion classification, and the fact that the
campaign media was intentionally external to the printed book (`source_evidence_never_printed`,
established from the copyright page). **No visual verification was manufactured** — the book
contains no argument-bearing figure and the record says so.

**10 SourceKnowledge · 2 systems · 3 bindings · 12 ontology terms.**

### Desai — *Mother Pious Lady* → **HOLD / evidence_insufficient**

Moved to `canon/candidates/canon-014/desai-mother-pious-lady/`. It is **not** under
`canon/knowledge/current/**` and has **no record in `canon/audit/records/`**, because a record there
would imply it passed the gate. Its assessment is retained in the candidate directory as
`audit-assessment-HOLD.yaml`.

The reasoning, which the donor record itself established and then failed to act on: this copy has
redistributor-overwritten publisher metadata, 11 injected strings, and one complete non-authorial
sentence inside an authorial paragraph of the Introduction. **Excluding the marked injections does
not bound the risk.** A redistributor demonstrably willing to insert a sentence into an author's
prose may have made further unmarked changes, and that risk is silent and unbounded. Settling it
needs comparison against an independent clean representation; none is available in this environment
and there is no network egress. `evidence_insufficient` is the Audit Gate's designed outcome for
exactly this.

**The extraction is not discarded.** 17 SourceKnowledge objects, 2 systems, 4 bindings and 18
ontology terms are retained as source evidence, and were corrected to the same structural standard
as the two READY sources — HOLD is an evidence judgement, not a structural excuse. A test asserts the
held material still validates clean.

**Consequence handled:** holding Desai removed it from the accepted corpus, which made the two READY
records' `related_sources_in_corpus` entries for it invalid — the Audit Gate validator caught this.
The relation was **not** dropped: it moved into `independence_basis` as a forward relation, live
again the moment Desai is admitted.

---

## 5. Knowledge-quality review

Beyond structure. Every SourceKnowledge object in the two READY candidates was reviewed for the six
failure shapes named in the lane brief.

**Found and corrected: seven mechanisms attributed to the source that were the extractor's own
generalisation.** The test applied was strict — did the source *explain why*, or only *describe what
happened*?

| Object | What the source actually does | Action |
|---|---|---|
| `sk_nnn_0001` | supplies the premise by quoting Barthes; never draws the evidential conclusion from it | `stated_by_source: false` |
| `sk_nnn_0011` | narrates the *gori*→*nikhri* substitution and its outcome; never explains why the transfer works | `false` |
| `sk_nnn_0012` | reports the 2007 Cable TV amendment and the non-member compliance gap as separate facts; never connects them | `false` |
| `sk_nnn_0031` | reports three influence bands as findings from unnamed researchers; explains none | `false` |
| `sk_nnn_0050` | states the problem, the yield and the practice; the probabilistic reasoning is not in the source | `false` |
| `sk_nnn_0051` | states the consequence; the licensing vocabulary was the extractor's | text corrected |
| `sk_ppm_0021` | states the review-conditions point; offers nothing on why conviction predicts being right | text corrected |

Where a mechanism became the extractor's, `mechanism_given` was replaced by `mechanism_absent` in
the evidence characteristics, so the object no longer claims the source supplied a mechanism. Each
carries a new caveat recording precisely what the source does and does not say.

`sk_nnn_0050` matters most: it is the one carrying a **production** binding, and a mechanism about
why redundant casting works is exactly the kind of thing that could later be lifted as a rule.

**Checked and clean:**

- **No interpolated page numbers** — 0 across all three sources; all are reflowable with no authored page.
- **Model capability from production practice** — the only model-capability language in any
  source-knowledge file is a prohibition; both production bindings are `production_candidate` with
  `target_path: null`.
- **Indian examples universalised** — every object carries a non-trivial `scope.conditions`;
  `culturally_bounded` is on 30/32 Parameswaran and 8/10 Pandey objects. The four without it are
  method statements and representation findings, correctly.
- **Extractor synthesis presented as source statement** — after the corrections above, 22 of 32
  Parameswaran and 5 of 10 Pandey mechanisms are explicitly the extractor's, each labelled in its
  own text.
- **Criticism as production advice** — no binding was written from the interpretive material.
- **Zero `cross_source_concept`** anywhere in the repository.

**Bindings removed: none.** Each of the twelve was re-examined against the corrected objects and
each still follows. Where a mechanism was re-attributed, the affected binding's rationale describes
a constraint or a hazard rather than the mechanism itself, so it survives the change.

---

## 6. Governance findings preserved, not acted on

Per the lane brief these remain Controller findings and **no accepted live Canon was modified**:

- **F-01** — three `SourceConceptSystem`s in the accepted `sutherland-alchemy-introduction` have no
  `provenance`, which SPEC-03 requires. Still unfixed; still the only live-Canon defect the hardened
  validator reports. Pinned by a test that asserts exactly three errors on exactly that source, so
  it cannot be quietly repaired without re-running the gate, nor quietly grow.
- **F-02** — SPEC-04 cites a "fixed list" of `target_type` it never enumerates, while `benchmark` is
  used by 13 bindings across accepted Canon. `benchmark` is admitted in the validator with the
  reasoning recorded in the code; the spec gap is the Controller's to close.
- **F-03** — `light-science-magic-ch3` later-chapter qualification and re-audit need. Untouched.

---

## 7. Mechanical status at the branch head

```
canon/validation/validate_audit_gate_v02.py          21 records, 0 errors
canon/validation/validate_source_artifact_schema.py  21 dirs, 3 errors  (all F-01, pre-existing)
  same, over the held Desai candidate                 1 dir,  0 errors
tests/test_validate_source_artifact_schema.py        88 passed
tests/test_validate_audit_gate_v02.py                60 passed, 101 subtests
tests/test_validate_canon003_integrated.py            5 passed
tests/test_value_gate_corrections.py                 26 passed
```

`tests/test_request_freeze_gates.py` calls `sys.exit()` at import so pytest cannot collect it. That
is pre-existing and untouched by this lane; it passes when run as the script it is.

---

## 8. For the Controller

1. **This is a donor/cleanup PR and must not be merged until reconciled with the laptop agent's
   completion branch.** Both lanes touch `canon/validation/validate_source_artifact_schema.py` and
   `tests/`, and both may touch the Parameswaran and Pandey directories. This lane's validator is
   strictly stronger than the donor's and should win any conflict on those two files.
2. **Desai's disposition changed** from READY to HOLD. If the laptop agent's branch still carries
   Desai under `canon/knowledge/current/`, that is the reconciliation's first decision.
3. **The seven re-attributed mechanisms are the substantive change to the knowledge**, not the
   vocabulary fixes. They are worth a read before merge: each moved a generalisation out of the
   source's mouth and into the extractor's.
4. **F-01 and F-02 still need your decision** and neither is a worker's to make.
