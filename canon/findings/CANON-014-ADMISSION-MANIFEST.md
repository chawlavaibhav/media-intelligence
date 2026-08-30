# CANON-014 — Admission manifest

**Every candidate is in exactly one of two states. There is no third.** A candidate is READY only if
it sits under `canon/knowledge/current/<dir>/` in the exact live shape with a validating Audit Gate
v0.2 record; otherwise it is HOLD with the exact blocker named below.

The success criterion for this task was **not** the number of admissions. It was leaving every
source in the right epistemic state.

| State | Count |
|---|---|
| **READY** | **3** |
| **HOLD** | **20** (17 repaired CANON-013 candidates + 3 books named for this task that were never supplied) |

Mechanical status at the head SHA of this branch: **22 audit records, 0 errors** from
`canon/validation/validate_audit_gate_v02.py`; **22 source directories, 0 errors** from
`canon/validation/validate_source_artifact_schema.py` other than 3 pre-existing defects in an
already-accepted source that CANON-014 is not authorised to edit (see
`CANON-014-LIVE-SOURCE-REAUDIT-FINDINGS.md`).

---

## READY — 3

Each is in live shape with all five snapshot files plus `PROVENANCE.md`, and each has an Audit Gate
v0.2 record written against those exact bytes with `source_reopened: false`.

| Source | SK | Systems | Bindings | Ontology terms | Visual pass | `audit_status` |
|---|---|---|---|---|---|---|
| `parameswaran-nawabs-nudes-noodles` | 32 | 4 | 9 | 22 | 19/19 plates inspected | `complete` |
| `desai-mother-pious-lady` | 17 | 2 | 4 | 20 | completed, null result | `complete` |
| `pandey-pandeymonium` | 10 | 2 | 3 | 12 | completed, evidence never printed | `complete` |

**Why these three and nothing else:** they are the only candidates whose source was available in
this session. That is not a coincidence or a coverage decision — it is the whole distinction. For
these three the extraction, the visual pass, the provenance hashes and the audit were all done
first-hand against the supplied files. For every HOLD candidate none of that is possible here.

Each READY record carries its own limits rather than presenting itself as clean:

- **Nawabs** — `claim_resolution_after_inspection: some_underdetermined`. Four of nineteen plates
  were opened and still do not settle their captions. Body copy is illegible on every plate that has
  it, and no object rests on any.
- **Desai** — the copy has been modified by a redistributor: publisher metadata overwritten, and one
  non-authorial sentence injected *inside* a paragraph of the Introduction. All 11 injection sites
  were located and excluded. The residual risk is stated as silent and unbounded, which is why no
  object rests on a single verbatim sentence.
- **Pandeymonium** — `source_evidence_never_printed`. The campaigns are not in the book because the
  publisher put them on a companion website; the named route was unreachable in this session. Every
  claim about a campaign is a claim about what Pandey *says* about it.

---

## HOLD — 17 repaired CANON-013 candidates

### The blocker they all share

**`evidence_insufficient` — the source cannot be opened in this session, and the Audit Gate requires
an artifact that cannot be authored without it.**

This is mechanical, not a judgement call, and it has three independent legs:

1. **No candidate has a `visual-evidence-ledger.yaml`.** Verified: `find` returns **0** across all 17
   directories. That file is one of the five in the Audit Gate's `source_snapshot`, and the validator
   reports a missing covered artifact rather than skipping it. Without it no record can be written at
   all, for any of the 17.
2. **It cannot be authored from here.** The previous run read these books from a local library at
   `~/Downloads/Books/`. This is a fresh remote container; that library does not exist in it.
3. **No external route exists either.** Verified rather than assumed: a direct HTTPS request and the
   harness fetch tool were both refused by the egress proxy for every external host tried, including
   `w3.org` and `gutenberg.org`. So even the candidates whose sources are openly published — WCAG 2.2,
   the Google ABCD pages — and the two public-domain Hopkins texts **cannot be re-fetched**. This is
   the one place where a genuinely open source would otherwise have been re-verifiable, and it is not.

**Authoring a ledger anyway would be the failure this task was set against.** A visual-evidence
ledger records what an inspection found. Transcribing the previous run's self-report into a gate
artifact and signing it would be fabricating an inspection, and would convert a prior run's
unverified claims into an admission record. `evidence_insufficient` is a legitimate completed
outcome and this is what it is for.

### What was nonetheless repaired on the branch

The 17 are **not** left as they were. Under `canon/experimental/book-expansion-qa-v1/`:

- 3 `SourceConceptSystem`s missing `evidence.system_level_uncertainty` were fixed — **not 1 as
  previously reported**; the reported omission was one member of a class.
- 84 `dependencies`/`tradeoffs`/`conflicts` entries missing `origin` were fixed, failing closed to
  `extractor_inferred`.
- 22 artifact files missing the top-level `source_id` that Audit Gate rule 2 resolves against were
  fixed.
- All counts recomputed mechanically; the Q&A application floor removed and the banks reclassified.
- All 17 now pass the corrected schema validator.

**A structural PASS is not admission.** These are better than they were and still cannot pass the gate.

### Per-candidate blockers, beyond the shared one

The five defects the authorisation named individually are **not** resolved, and each is recorded as
still open rather than converted into a pass:

| Candidate | Additional blocker, unresolved |
|---|---|
| `airey-logo-design-love` | The copy used was an **unattributed degraded Spanish machine translation**, so it cannot establish Airey's English vocabulary. No better English source is attached to this session. No repair was fabricated; the candidate is held. |
| `samara-breaking-the-grid-ch2` | More than half the extraction depended on visual evidence never inspected, in a book whose designed pages are themselves the argument (`source_is_its_own_specimen` on its live counterpart). The caveat stands and is **not** converted into a pass. |
| `freeman-photographers-eye-beyond-parts1-3` | The conversion destroyed designed-spread relationships. The limitation is preserved. |
| `carroll-read-this-photographs` | Roughly half the knowledge depended on photographs unavailable to inspection. Those claims are **not** presented as visually verified. |
| `sullivan-hey-whipple`, `ogilvy-beyond-ch2` | Significant reproduced-advertisement evidence absent. Assessed honestly: insufficient. Sullivan additionally carries `independence_not_established` against the live Ogilvy material (see the lineage matrix), which blocks promotion independently of representation. |

The other 11 are held on the shared blocker alone.

### Five candidates that are worth more as re-audit evidence than as admissions

`light-science-magic-beyond-ch3`, `samara-breaking-the-grid-ch2`,
`freeman-photographers-eye-beyond-parts1-3`, `ogilvy-beyond-ch2` and
`hopkins-scientific-advertising-ch8-21` are same-work scope extensions with **zero independence**
against their live counterparts. Their value is not that they could be admitted — it is what they say
about sources already accepted. Routed to `CANON-014-LIVE-SOURCE-REAUDIT-FINDINGS.md`.

---

## HOLD — 3 books named for this task that were never supplied

| Source | State |
|---|---|
| Rachel Dwyer & Divia Patel — *Cinema India: The Visual Culture of Hindi Film* | **Never attached to this session.** |
| Kajri Jain — *Gods in the Bazaar: The Economies of Indian Calendar Art* | **Never attached to this session.** |
| Rama Bijapurkar — *We Are Like That Only: Understanding the Logic of Consumer India* | **Never attached to this session.** |

Three of the six books named in the authorisation were attached: Parameswaran, Desai and Pandey.
The other three were not, and could not be obtained — there is no external network egress in this
environment.

**Nothing was extracted, inferred or written about these three.** No lineage claim can be made about
a work that was not examined. Two of them already have **inbound forward relations** recorded in the
lineage matrix from Parameswaran's endnotes, which become live the moment either is admitted:

- Parameswaran **cites** Bijapurkar's *We Are Like That Only* directly. If it is admitted, that pair
  carries `cites_source` — not disqualifying, but an auditor must check whether her claims are
  load-bearing in him before treating the two as converging.
- Parameswaran's bazaar-art material is **second-hand**, reporting Arvind Rajagopal. If *Gods in the
  Bazaar* is admitted, Parameswaran must **not** count as independently corroborating it.
- Parameswaran cites Dwyer's *Picture Abhi Baaki Hai*, which is a **different work** from *Cinema
  India*. Citing one book by an author creates no relation to a different, uncited book by the same
  author, so that pair would start at `no_known_relation`.

### The consequence for the gap this task was meant to close

The authorisation's stated reason for choosing these six books was to attack the Canon's Indian
cultural and Indian visual gap, and it made the visual pass mandatory because *Gods in the Bazaar*
and *Cinema India* are the visually demanding ones.

**Those two are exactly the ones not supplied.** So the gap is now *partly* closed rather than
closed: the corpus gains Indian advertising history, Indian everyday material culture and Indian
creative practice, with 19 reproduced Indian advertisements inspected first-hand. It gains **nothing**
on Hindi-film visual culture or on Indian calendar and bazaar art, and the only calendar-art material
anywhere in the corpus is Parameswaran's second-hand paragraph reporting Rajagopal, which is
explicitly marked as no substitute for a primary source.

**Devanagari and Indic typography remains completely unclosed**, as it was after CANON-013.

---

## What would change these states

| To move | Requires |
|---|---|
| Any of the 17 to READY | The source file itself, attached to a session, so a first-hand visual pass can be run and a ledger authored. For WCAG and the Google ABCD pages, network egress alone would suffice. |
| The 3 unsupplied books to any state at all | Attaching the files. Until then no work on them is possible or honest. |
| The Sullivan/Ogilvy pair out of `independence_not_established` | Re-opening Sullivan and testing whether Ogilvy's claims are load-bearing in it — the `shared_primary_informant` test. |
