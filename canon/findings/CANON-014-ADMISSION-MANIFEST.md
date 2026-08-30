# CANON-014 — Admission manifest (final)

**Branch:** `work/canon-014-final-full-canon`. **Not merged.** Paths under
`canon/knowledge/current/**` become live knowledge only when the Controller merges.

Every one of the 23 CANON-014 source candidates is in exactly one of two states. There is no third,
and **presence in this repository is never admission**.

| State | Count | Where |
|---|---|---|
| **ACCEPTED** | **5** | `canon/knowledge/current/<source>/` + an Audit Gate v0.2 record |
| **HELD** | **18** | `canon/candidates/canon-014/<source>/` + an `audit-assessment-HOLD.yaml` |

With the 19 sources already live, **live Canon becomes 24 accepted sources**.

Mechanical status at this branch head, every number read from the files:

| Check | Result |
|---|---|
| `validate_audit_gate_v02.py` | **24 records, 0 errors** |
| `validate_source_artifact_schema.py canon/knowledge/current` | 24 dirs, **3 errors**, all pre-existing in `sutherland-alchemy-introduction` |
| `validate_source_artifact_schema.py canon/candidates/canon-014` | 18 dirs, **0 errors** |
| `validate_qa_corpus.py` | 23 banks, 1,028 items, **0 errors** |
| `pytest tests/` (see the note on `--ignore` below) | **179 passed, 113 subtests** |

---

## ACCEPTED — 5

Each is in live shape with all five snapshot files plus `PROVENANCE.md`, and an Audit Gate v0.2
record written against those exact bytes with `source_reopened: false`.

| Source | SK | Systems | Bindings | Terms | Visual pass |
|---|---|---|---|---|---|
| `parameswaran-nawabs-nudes-noodles` | 32 | 4 | 9 | 22 | **19/19 plates**, complete |
| `dwyer-patel-cinema-india` | 19 | 3 | 4 | 25 | 11 of ~121 plates; 7 claims checked, all held |
| `jain-gods-in-the-bazaar` | 18 | 3 | 5 | 30 | 7 of ~156 figures; 7 claims checked, all held |
| `bijapurkar-we-are-like-that-only` | 18 | 3 | 4 | 30 | **30/30 data figures**, complete |
| `pandey-pandeymonium` | 10 | 2 | 3 | 12 | completed; evidence never printed in the book |
| **Total** | **97** | **15** | **25** | **119** | |

### Three of these were repaired before admission, not admitted as they stood

Cinema India, Gods in the Bazaar and We Are Like That Only were extracted against an older validator
and carried **202 schema violations** between them. The books were **not** re-extracted; every repair
is semantic and was decided per object. Full detail is in the commit for
`canon-014: admit five Indian-context sources`. In summary:

- **60 intra-source relations** used `supports`/`supported_by`, which SPEC-03 does not define. 39
  were mapped where a permitted relation genuinely matches; **21 were removed** where none does, each
  keeping its note as a caveat.
- **51 uncertainty fields** carried free prose where SPEC-03 wants a controlled value. Most of that
  prose was the extractor's assessment of evidential strength rather than a statement that the source
  hedges, so the value became `none` and the prose moved to a caveat. **72 caveats added; nothing
  lost.**
- **86 ontology terms** used invented kinds, reclassified by reading each definition.
- **3 bindings were removed and 1 recast.** The removals matter: `bnd_rbwl_0005` bound *pricing and
  packaging strategy* as media production, which puts commercial strategy inside a media production
  contract; `bnd_jgb_0006`'s own rationale said it informed "and for no other purpose", which is an
  honest description of something that is not a binding. **The knowledge behind every removed binding
  is untouched.** Zero bindings is a normal SPEC-04 state and is a fact about our product, not about
  the source.

### Each accepted record carries its own limits

- **Cinema India** — the book **dates its own subject as ending** in the 1990s, in its own
  Conclusion. Its evidence base is also a survival sample: hoardings, which the source itself calls
  the most distinctive form of its medium, were destroyed after each film's run.
- **Gods in the Bazaar** — the author states what her interview evidence can bear, and that statement
  is grouped with every object depending on it. The strongest-attested constraint in the book, the
  injunction against divine musculature, **was breached from the late 1980s**, which the source
  itself documents; the two must be cited together.
- **We Are Like That Only** — the data is **2008 and earlier** and the author says so twice. Every
  numerical object is grouped with her own vintage statement, and **no binding from this source
  carries a number**.
- **Parameswaran** — four of nineteen plates were opened and still do not settle their captions.
- **Pandey** — the campaigns are not in the book; the publisher put them on a website.

---

## HELD — 18

**17 earlier expansion sources + Desai.** All 18 pass the hardened structural validator with zero
errors and **none is admitted**. Each carries an `audit-assessment-HOLD.yaml` which is deliberately
**not** an Audit Gate record.

### The blocker 17 of them share

**No figure-level inspection has ever been run**, so none has a `visual-evidence-ledger.yaml`. That
file is one of the five the Audit Gate fingerprints, and the Gate reports a missing covered artifact
rather than skipping it — so no record can be written at all. It cannot be authored from the
committed extraction either, because a ledger records what an inspection found.

> **A change of fact the Controller should see.** The earlier passes recorded these as blocked partly
> because *the source could not be opened*: the extraction had read a local library absent from the
> repair container, which also had no network egress. Both were true there. **Neither is true here —
> 15 of the 17 books are on this machine and egress was tested and works.** What remains unresolved
> is therefore not access; it is that the inspection has not been done. That is cost and
> authorisation. It is a materially better position and **it is not a pass**.

### Desai's blocker is different and survives having the file

The supplied EPUB has been **modified by a redistributor**, including one complete non-authorial
sentence sitting *inside* an authorial paragraph of the Introduction with no distinguishing markup.
Eleven injection sites were found and excluded, and the residual risk is **silent and unbounded**:
nothing establishes that all modifications were found, because there is no independent clean copy to
compare against. None was found here either, so the HOLD stands.

### Source-specific blockers that survive a visual pass

| Source | Blocker |
|---|---|
| `airey-logo-design-love` | **The strongest blocker on any of the 18.** The only copy is an unattributed, degraded Spanish machine translation; Airey's own wording is unrecoverable, and on printed p.64 it calls the **failed** Tropicana redesign the "successfully renamed identity", contradicting its own body text. A copy that inverts one case study cannot be trusted for the others. |
| `sullivan-hey-whipple` | `independence_not_established` against live Ogilvy — which **blocks promotion** until resolved. Also a partial extraction recorded as whole: chapters 10, 13, 14 and 17 were never read. |
| `samara-breaking-the-grid-ch2` | The live counterpart carries `source_is_its_own_specimen`: the designed pages **are** the argument, so a text-only reading cannot see it. |
| `freeman-photographers-eye-beyond-parts1-3` | The conversion destroyed the designed-spread relationships, and in this book a facing pair is a unit of meaning. A different copy fixes it, not a better extraction. |
| `ries-22-immutable-laws-branding` | Materially disagrees with live `binet-field-effectiveness-in-context-ch1` on five points. Recorded, unresolved, and a Controller judgement. |
| `w3c-wcag22-text-legibility`, `google-abcd-video-ads` | Living web artifacts read without a fingerprint of the bytes; both can change under their own URLs. Google's is additionally platform-contingent throughout. |
| `carroll-read-this-photographs` | Roughly half the knowledge rests on photographs never inspected. |
| Five scope extensions | Hopkins ch8-21, LSM beyond ch3, Samara ch2, Ogilvy beyond ch2, Freeman beyond parts 1-3 — **zero independence** against their live counterparts. Never a separate book. |
| `hopkins-my-life-in-advertising` | `shared_author` with the live Hopkins source, whose chapter 17 is *about* it. Never corroboration. |
| `kahneman-sibony-sunstein-noise`, `sontag-on-photography` | Partial extractions by topic, scoped by the extractor. |

### Held knowledge is retained in full

**839 source-knowledge objects, 72 concept systems, 188 bindings, 841 ontology terms and 920 Q&A
items** — more raw knowledge than the accepted corpus holds. Every Q&A item carries
`source_status: hold`, and the Q&A validator refuses any bank that claims `accepted` for a source
sitting in the candidate tree.

---

## Raw sources and clean diff

**No book bytes are committed.** No `.pdf`, `.epub`, `.mobi`, `.azw3` or image file is added by this
branch, verified over the diff and the working tree. `canon/experimental/**` is not on this branch at
all; its derived knowledge is preserved under `canon/candidates/canon-014/` and `canon/qa/canon-014/`.
No `coordination/**`, `PROJECT-MEMORY.md`, `eval/**`, `resources/**`, `governance/**`, `shared/**` or
SPEC file is touched.

## The one unrelated test failure

`pytest tests/` requires `--ignore=tests/test_request_freeze_gates.py`. That CANON-010 file hardcodes
an absolute container path and runs its runner block at module scope, so importing it calls
`sys.exit(0)` and pytest **aborts collection of the entire suite**. The **179 passed** figure above is
the suite with that file excluded. The defect is recorded as **F-06** in
`CANON-014-LIVE-SOURCE-REAUDIT-FINDINGS.md` with a verified two-line patch. It is not fixed here:
CANON-014 does not own that file, and editing another task's test to get a green run is exactly the
move this branch exists to avoid.

## What would change the remaining states

| To move | Requires |
|---|---|
| Most of the 17 to ACCEPTED | One authorised figure-level inspection each, then an Audit Gate record. **The books are present; this is cost, not access.** |
| Airey | A different copy. No amount of inspection fixes a bad translation. |
| Sullivan | Re-opening it and testing whether Ogilvy's claims are load-bearing — the `shared_primary_informant` test. |
| Desai | An independently clean copy to establish that all redistributor modifications were found. |
| The three Sutherland defects in live Canon | Controller authorisation to reopen an accepted source, which stales its audit and requires re-running the Gate. |
