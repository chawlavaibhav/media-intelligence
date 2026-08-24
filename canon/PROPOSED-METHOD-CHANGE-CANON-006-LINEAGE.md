# Proposed method change — one lineage relation for a recorded practitioner

**From:** Canon worker, CANON-006 · **To:** Controller · **Date:** 25 Aug 2026
**Severity:** `LOCAL` — one Audit Gate vocabulary member and one sentence of SPEC-05.
**Status: CONTROLLER-APPROVED AND APPLIED**, 25 Aug 2026, within PR #9.

> **Decision.** The Controller approved `shared_primary_informant` and tightened its normative
> meaning to: *the same practitioner's own claims constitute a primary or substantial knowledge
> source in both works despite different bibliographic authorship — for example, one work written by
> that practitioner and another substantially recording them in interview or conversation.*
> **Incidental quotation of the same person is not sufficient.** It is a symmetric pairwise
> dependence relation and defeats independent convergence only for that pair.
>
> Applied in `canon/audit/AUDIT-GATE-v0.2.md`, `canon/knowledge/SPEC-05-knowledge-ontology.md`
> Governance rule 5 (four dependence relations to five) and
> `canon/validation/validate_audit_gate_v02.py`. *The Conversations* now holds an active v0.2 audit
> record and is accepted; the live Canon is **18**.

This document is retained as decision history. It records the reasoning as it stood when the block
was raised — the text below is unedited and still speaks of the source as blocked, which is what was
true at the time of writing.

---

## 1. The relationship that cannot be stated

The live corpus contains `murch-blink-p1-25` — *In the Blink of an Eye*, written by Walter Murch.
The recovered reserve is *The Conversations: Walter Murch and the Art of Editing Film*, whose
`dc:creator` is Michael Ondaatje, `opf:role="aut"`, copyright © 2002 Michael Ondaatje, Knopf.

**Both books are Walter Murch talking about editing.** The legacy extraction established this from
the sources themselves, not by inference, and logged it as LB-20:

- **The Egyptian-painting argument** appears in both — a footnote in *Blink* ("each part of the body
  drawn from its most characteristic angle… in some remote future, our films will look just as comic
  and twisted"), and a full passage in *The Conversations* ("five hundred years from now, when people
  see films from our era, they'll seem 'Egyptian' in a strange way").
- **`planarity`** appears in both — a named criterion of the Rule of Six in *Blink*, and
  `planarity_of_the_face` applied to lens choice in *The Conversations*.

They are not two origins agreeing. They are **one practitioner recorded twice, by two different
authors.**

The extractor also disclosed contamination on the object itself: `sk_conv_c003_0027` carries a
caveat recording that the Egyptian argument was recognised on sight, because the same lane had
extracted it from *Blink* earlier. Nothing was imported, and the recognition is on the record.

## 2. Why none of the seven current relations is truthful

| Relation | Verdict | Why |
|---|---|---|
| `shared_author` | **false** | Ondaatje is the bibliographic author. Murch is the interviewee. CANON-006 explicitly forbids calling him an author the source does not support. |
| `same_series` | **false** | Knopf 2002 against Silman-James Press 2001. No series relationship. |
| `companion_volume` | **false** | Different publishers, four years apart, not published or marketed as companions. |
| `derivative_of` | **false** | Neither derives from the other. The shared material appears in both because Murch holds the view, not because one book copies the other. |
| `cites_source` | **insufficient, and dangerous** | Not established from committed evidence. And under the adopted SPEC-05 rule `cites_source` explicitly does **not** defeat independence — so recording it would let the pair pass as independent convergence, which is the precise error the rule exists to prevent. |
| `shares_publisher_only` | **false** | Knopf and Silman-James Press. |
| `no_known_relation` | **false** | The relationship is documented and concrete. |

Writing any of them into an authoritative record would be a false statement. So the record was not
written.

**Why this is harder than the case the rule already catches.** *Grammar of the Shot* and *Grammar of
the Edit* share authors, publisher and series — a reviewer could catch that from a title page. Here
**the author field itself differs**, and no metadata anywhere records that a book consists largely of
another person's words. This pair passes every check built on author, publisher or source id.

## 3. The proposed minimum change

**One new lineage relation**, and nothing else:

```
shared_primary_informant
```

> The same practitioner's own claims are recorded in both sources, under different bibliographic
> authorship — for example one book written by that practitioner and another recording them in
> interview. Agreement between such sources is one position stated twice, not convergence between
> independent origins.

It joins the **dependence** set alongside `shared_author`, `same_series`, `companion_volume` and
`derivative_of`, so it defeats independence for that pair and must be declared from both sides.

### Rejected alternatives, and why

- **Reuse `shared_author` with an explanatory note.** Rejected: the note is prose a machine does not
  read, and the field would assert something bibliographically false.
- **`same_speaking_voice`.** Rejected as vague — it invites reading as register or style.
- **`shared_subject`.** Rejected as far too broad. Two independent biographies of one director are
  genuinely independent origins; the dependence here is that the *claims* are the subject's own.
- **A generic `dependent_other` escape hatch.** Rejected: it would turn a controlled vocabulary into
  a free-text field and hide the next distinct relationship rather than surfacing it.
- **Accept the source and record the risk in prose only.** Rejected: that is exactly the failure
  CANON-004 was built to remove — a truth living in a caveat that nothing can count.

## 4. Exact consequences if approved

| Artifact | Change |
|---|---|
| `canon/audit/AUDIT-GATE-v0.2.md` | add `shared_primary_informant` to the relation list and to the dependence set; one table row and one line in the promotion rule |
| `canon/knowledge/SPEC-05-knowledge-ontology.md`, Governance rule 5 | the dependence list names four relations; it would name five. **One sentence. Authoritative — Controller approval required.** |
| `canon/validation/validate_audit_gate_v02.py` | one member added to `LINEAGE_RELATIONS` and one to `DEPENDENT_RELATIONS`. No new logic: symmetry enforcement, fail-closed verdicts and `independent_origins_ok()` all work unchanged, because the relation is symmetric like the existing four. |
| `tests/test_validate_audit_gate_v02.py` | one real-corpus test asserting the Murch ↔ Conversations pair is refused, mirroring the existing Grammar-pair test |
| `canon/audit/records/murch-blink-p1-25.audit.yaml` | gains one reciprocal `related_sources_in_corpus` entry and its verdict becomes `not_independent_of_named_sources`. Because independence is pairwise, *Blink* stays a good independent origin against all 16 other sources. |
| `canon/audit/records/ondaatje-conversations-ch3.audit.yaml` | written for the first time, with the dependence declared |
| `canon/audit/LIVE-CORPUS.yaml` | `ondaatje-conversations-ch3` moves from `source_evidence_only` to `accepted` |

**Migration surface is exactly one pair.** The other 16 accepted sources are authored works with no
recorded-practitioner relationship to each other, so none of their records changes. No source
knowledge, system, ontology entry or binding changes anywhere.

**Snapshots are unaffected.** They fingerprint the frozen source artifacts, not the audit records, so
editing *Blink*'s audit record cannot invalidate its snapshot.

## 5. What would have happened if the Controller had declined

Nothing breaks. *The Conversations* stays `source_evidence_only`: present, mechanically valid, fully
documented, and blocked from cross-source promotion, downstream product use and Canon-consumption.
The live Canon stays at **17 accepted**.

That is a legitimate outcome and, on the current vocabulary, the honest one. A live Canon of 17 is
better than a dishonest 18.

## 6. What this is not

Not a request to change SPEC-01, SPEC-03 or SPEC-04. Not a new Audit Gate version. Not a new evidence
characteristic, term kind, concept kind or ontology relation type — SPEC-05's `maps_to` /
`same_mechanism` / `distinct_from` family is untouched. Not a change to the anti-score rule, the
seven application-fit consumers, or snapshot semantics.

One relation, one sentence, one pair.
