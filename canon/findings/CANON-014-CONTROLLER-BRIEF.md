# CANON-014 — Controller Brief

**Branch:** `claude/canon-014-expansion-admission-ntp0dl` · **Not merged.** Nothing here is live
project knowledge. Paths under `canon/knowledge/current/**` created by this task become live **only
if you merge the branch**.

> ## Delta pass — read this first
>
> **The three books this brief previously recorded as "never supplied" were found on your machine as
> PDFs, and have been fully processed.** They were missed because the first pass searched for EPUBs.
> A second correction matters as much: the delta brief that authorised this pass named Desai,
> Parameswaran and Pandey as the missed three. **They were not missed** — they were already complete
> on this branch, which was verified by matching their SHA-256 hashes against the values recorded in
> their committed `PROVENANCE.md` files. The genuinely missed three were *Cinema India*, *Gods in the
> Bazaar* and *We Are Like That Only*, and you confirmed that correction before the work proceeded.
>
> **What changed:** READY 3 → **6**. HOLD 20 → **17**. Total candidates unchanged at **23**.
> Everything below is updated in place; sections carrying delta-pass findings are marked **[delta]**.
> Counts everywhere were recomputed mechanically from the final files. **Nothing here is merged, and
> nothing is marked ready for merge.**

This brief separates **OBSERVED** (what is mechanically checkable in the repository or was read
directly from a supplied file), **INFERRED** (my reading, which could be wrong), and **RECOMMENDED**
(proposals, which are not decisions). Nothing in RECOMMENDED has been acted on.

---

# OBSERVED

## O-1. [delta] All six named books have now been processed

**First pass — supplied and processed:** Parameswaran (*Nawabs, Nudes, Noodles*), Desai (*Mother
Pious Lady*), Pandey (*Pandeymonium*).

**Delta pass — found locally and processed:** Dwyer & Patel (*Cinema India*), Kajri Jain (*Gods in
the Bazaar*), Bijapurkar (*We Are Like That Only*). All three were present in `~/Downloads/` as
**PDFs**, which is why the first pass — searching for `*.epub` — did not find them.

| Book | SHA-256 | Bytes | Pages | Image objects |
|---|---|---|---|---|
| *Cinema India* | `d841c2ba964d4c00…36d1583` | 20,007,457 | 244 | 732 |
| *Gods in the Bazaar* | `f019cfe3b7810591…0d34f0883` | 13,108,574 | 449 | 179 |
| *We Are Like That Only* | `8c480391db2f37a9…4a53ca7` | 3,847,876 | 279 | 46 |

**No raw book bytes and no page images are committed anywhere in this repository.** Only derived
Canon artifacts. Confirmed mechanically before commit: no `.pdf`, `.epub`, `.mobi` or `.azw3` is
staged or tracked on this branch.

**The premise of the delta authorisation was wrong and I checked rather than assumed.** It named
Desai, Parameswaran and Pandey as the three missed books. All three were already complete on this
branch, verified by matching the local files' SHA-256 hashes against the values in their committed
`PROVENANCE.md` — Desai `b0a2fb33…` (532,237 B), Parameswaran `a5be652e…` (1,213,464 B), Pandey
`866597a9…` (1,046,663 B), all exact. Had I taken the brief at face value I would have re-processed
three finished sources and left the three real gaps open.

**Access handling.** Per your explicit instruction, acquisition provenance was not adjudicated. All
three filenames carry a `libgen.li` marker; that is recorded as a fact about each artefact in its
`PROVENANCE.md`, was not treated as a reason to exclude the source, and no replacement copy was
sought. Nothing was acquired, purchased, downloaded or redistributed by this worker. Licence status
is recorded as not independently verified.

**The duplicate-upload point in your original authorisation did not arise:** Mother Pious Lady was
supplied once, in one copy.

## O-2. The seventeen CANON-013 candidates cannot be opened here, and that is decisive

That package was produced by reading books from a local library at `~/Downloads/Books/`. This is a
fresh remote container; the library does not exist in it, and O-1 rules out any external route — so
even WCAG 2.2, the Google ABCD pages and the two public-domain Hopkins texts cannot be re-fetched.

**The mechanical consequence:** none of the seventeen has a `visual-evidence-ledger.yaml` — `find`
returns **0** across all seventeen directories. That file is one of the five in the Audit Gate's
`source_snapshot`, and the validator reports a missing covered artifact rather than skipping it. So
**no audit record can be written for any of them**, and the file cannot be authored without the book.

## O-3. The reported schema defect was one member of a class

The previous run reported one object, `scs_sa8_002`, missing `evidence.system_level_uncertainty`.
Comparing the package against the **complete** SPEC-03/04/05 required-field sets rather than against
the old validator found:

| Defect | Reported | Found |
|---|---|---|
| System missing `evidence.system_level_uncertainty` | 1 | **3** |
| `dependencies`/`tradeoffs`/`conflicts` entry missing `origin` (SPEC-03 requires it at every structural level) | — | **84** |
| Artifact file missing the top-level `source_id` that Audit Gate rule 2 resolves against | — | **22** |

All fixed. `origin` failed closed to `extractor_inferred`: an origin never recorded cannot afterwards
be asserted to be the source's.

**The hole is demonstrated, not asserted.** On identical bytes from commit `3c29c8d`, the old
validator's entire `SourceConceptSystem` check reports **0 errors**; the new validator reports
**109**, including all three missing-field cases. The old validator never checked required-field
presence on that object at all, so patching one field would have left the hole open.

## O-4. The corrected validator found two defects in **accepted live Canon**

Neither was previously recorded anywhere. Both are mechanically reproducible.

- **F-01.** All three `SourceConceptSystem`s in `sutherland-alchemy-introduction` — an accepted,
  audited source — have **no `provenance` block**, which SPEC-03 requires. Every other live source is
  clean. **Not edited**, because editing an accepted source stales its audit record and the Audit
  Gate deliberately has no snapshot-refresh tool. Pinned by a test that asserts exactly three errors
  on exactly that source, so it cannot be quietly repaired or quietly grow.
- **F-02.** SPEC-04 says `target_type` comes "from the fixed list" and **never enumerates that list**;
  it shows four worked examples. `benchmark` is used by **13 bindings across accepted live Canon** and
  appears in the Audit Gate's own consumer vocabulary. Accepted live Canon governs, so `benchmark` is
  admitted in the new validator and the spec gap is routed to you.

## O-5. [delta] Counts, recomputed mechanically from final files

**Recomputed from the files as they stand at this branch head. No number below is carried forward
from any earlier report.** The 777 ontology figure in the original chat report was wrong; the
correct figure for that package is 823, and it was already correct in the package's own README.

**CANON-013 repaired package** (17 HOLD candidates, counted by its own validator):
**822** SourceKnowledge · **70** systems · **184** bindings · **823** ontology terms · **899** Q&A
items, **42.8%** application (observed, not required).

**The six READY sources** (per-source, mechanically counted):

| Source | SK | Systems | Bindings | Ontology terms |
|---|---|---|---|---|
| `parameswaran-nawabs-nudes-noodles` | 32 | 4 | 9 | 22 |
| `dwyer-patel-cinema-india` | 19 | 3 | 5 | 25 |
| `jain-gods-in-the-bazaar` | 18 | 3 | 6 | 30 |
| `bijapurkar-we-are-like-that-only` | 18 | 3 | 5 | 31 |
| `desai-mother-pious-lady` | 17 | 2 | 4 | 18 |
| `pandey-pandeymonium` | 10 | 2 | 3 | 12 |
| **Total** | **114** | **17** | **32** | **138** |

The three delta-pass sources alone contribute **55** SourceKnowledge · **9** systems · **16**
bindings · **86** ontology terms.

**Binding distribution across the six:** governance **16**, evaluation **7**, creative_ir **3**,
production_candidate **5**, benchmark **1**. Every `production` binding carries
`status: production_candidate` and `target_path: null` (PROJECT-CONTRACT separation 2). The one
`benchmark` binding **adopts no threshold and creates no scorable code**.

**Q&A across the six banks:** **129** items, **33** requiring application, **25.6%** natural rate.

## O-6. The Q&A floor was distorting the labels, and the distortion is measurable

The one-third `requires_application` floor is removed. A screen over all 899 items found **no**
near-duplicate question, **no** answer under 35 words and **no** item without a support quotation — so
**nothing was deleted and nothing added**. The previous run's items are individually well made; the
defect was in the label.

Reclassified against your own criterion (a new case, not a restatement): 116 false→true, 79
true→false. Natural rate **42.8%**, not 38.7%. Both labels retained.

**The floor's fingerprint:**

| | under the floor | after honest relabelling |
|---|---|---|
| banks in the 7 points immediately above the 33.3% floor | **14 of 17** | **4 of 17** |
| per-source standard deviation | 3.30 | **7.58** |
| range across banks | 13.5 pts | **24.6 pts** |
| banks below the old floor | **0** | **2** |

Clustering just above a threshold, with nothing ever falling below, is what a construction target
does to a distribution. The **six** new banks, written with no floor at all, come out at 46.2%, 35.3%, 23.8%, 17.4%, 14.3%
and 14.3% — total **129 items, 33 application, 25.6%**. **[delta] Four of the six would have failed
the old one-third floor**, and that is the correct outcome rather than a shortfall. The rate tracks
what a source is: Parameswaran's practitioner reflections on campaigns he ran support many transfer
questions; Jain's ethnography of a print trade and Dwyer & Patel's art history support few, because
most of what those books establish is what WAS the case, not a principle to carry to a new case; and
Bijapurkar's is low for a third reason — her material is almost all reasoning discipline, so asking a
reader to restate a named error correctly is a knowledge question, not an application one. Under the
old rule four of six banks would have had to be padded with weak transfer questions to pass. **The
banks are labelled "grounded, ungraded, uncalibrated research Q&A" and are not benchmark ground
truth.**

## O-7. [delta] Six sources are READY; seventeen are HOLD

**READY — all six named books**, each in live shape with all five snapshot files plus
`PROVENANCE.md`, and an Audit Gate v0.2 record written against those exact bytes,
`source_reopened: false`:

| Source | SK | Sys | Bnd | Terms | Visual pass | `claim_resolution` |
|---|---|---|---|---|---|---|
| `parameswaran-nawabs-nudes-noodles` | 32 | 4 | 9 | 22 | **19/19 plates inspected** | `some_underdetermined` |
| `dwyer-patel-cinema-india` | 19 | 3 | 5 | 25 | 11 of ~121 plates; 7 claims checked | `some_underdetermined` |
| `jain-gods-in-the-bazaar` | 18 | 3 | 6 | 30 | 7 of ~156 figures; 7 claims checked | `some_underdetermined` |
| `bijapurkar-we-are-like-that-only` | 18 | 3 | 5 | 31 | **30/30 data figures**; 7 claims checked | `all_resolved` |
| `desai-mother-pious-lady` | 17 | 2 | 4 | 18 | completed, null result | `not_applicable` |
| `pandey-pandeymonium` | 10 | 2 | 3 | 12 | completed, evidence never printed | `not_applicable` |

**HOLD — 17:** the CANON-013 candidates (blocker at O-2, plus the five specific representation
defects your original authorisation named, none of which is resolved). **No source is on HOLD for
lack of supply any more.** No HOLD source appears anywhere under `canon/knowledge/current/**`.

**Mechanical status at this branch head:** Audit Gate validator **25 records, 0 errors**. Schema
validator **25 directories, 3 errors — all of them F-01**, in a source CANON-014 is not authorised to
edit. **All six READY sources: zero errors.**

**Page addressability differs across the six and was established mechanically, never assumed.**
*Cinema India* and *Gods in the Bazaar* have real printed folios — offsets of pdf − 2 and pdf − 13,
each verified at multiple independent points against the book's own contents page and running heads.
*We Are Like That Only* is a calibre conversion with **no authored page at all**, so `page_start` and
`page_end` are `null` throughout and every locator is a chapter and section heading. **No page number
was interpolated anywhere in this task.**

## O-8. The visual pass ran on all six books and changed the extractions

**Nawabs** — all 19 plates in the insert extracted and opened individually. Both directions matter:

- **Six craft mechanisms exist only because the plates were opened.** The book's text describes none
  of them; it supplies one-line captions. Examples: the Coca-Cola plate sets "Thanda matlab" in
  **Devanagari** beside the Latin logotype — the text names the Hindi word and never mentions the
  script; the Amul topical is a fixed form with exactly one variable slot; the Fevicol execution
  carries its whole argument with **no headline and no body copy**; the NDDB frames set the sung word
  "doodh" as the picture rather than as a subtitle.
- **Four captions were found NOT to be settled by their own plates** — Rasna, Naukri, Pepsi, Asian
  Paints — because the artefact reproduced is not the artefact the caption describes. A text-only pass
  would have transcribed all four as established fact. Recorded as
  `figure_inspected_claim_underdetermined`.

**Desai** — completed with a null result: 30 of 33 images are decorative ornaments, the book makes no
visual argument, and a text-only representation loses nothing. `inspected_figure_level` +
`no_visual_argument` records "we looked and there was nothing to see", which the two-axis vocabulary
exists to distinguish from not having looked.

**Pandeymonium** — the campaigns are not in the book **because the publisher put them elsewhere**. The
copyright page states: *"All images and television commercials mentioned in this book are available
for viewing on www.pandeymonium.in"*. That is `source_evidence_never_printed` in its defining form: a
2015 print reader was in exactly our position, so the gap is not ours to fix. The named route was
unreachable here and no claim rests on it.

**[delta] Cinema India** — 11 plates of about 121 opened. **Seven of Patel's own visual claims were
checked against the plates she describes and all seven hold**, which is a real and slightly unusual
result: where an object rests on a described plate, the description can be relied on for those seven
and is unverified for the rest. The checks included the *Deewaar* split-coloured face, the knife-laid
overpainting impasto over a photographic underlay, and a *Pakeezah* caption verified verbatim. The
pass was **bounded by cost, not blocked** — the copy is complete, the page mapping is established and
reproducible, and any plate can be rendered on demand. That distinction is recorded explicitly, and
deliberately NOT as a loss pattern, because nothing is missing from the copy.

**[delta] Gods in the Bazaar** — 7 figures of about 156, and the most productive pass of the three
because Jain's constraints are claims about *what an artefact looks like* and are therefore settleable
by looking. Seven checked, seven hold. Fig. 88 is the valuable one: it photographs a printed Hanuman
beside the original painting it was made from, so the effect of the retouching stage is observed
directly rather than taken from the caption — the print is visibly more saturated and higher in
contrast. Fig. 92 shows the front-looking imperative in a single naturalistically implausible pose: a
woman watching television with her face turned frontally out of frame, watching the screen from the
corner of her eye. Fig. 93 shows Ram and Lakshman drawing bows in battle with half-lidded eyes and
unmuscled bodies.

**[delta] We Are Like That Only — this is the finding of the delta pass.** The calibre conversion
preserved the prose as text and **every table and figure as a raster image**, so their content is
absent from the extracted text stream entirely, while the running prose names them and reasons from
them without restating them: *"Table 5.1 gives a stratification scheme…"*, *"as can be seen in Table
9.2"*. **A text-only extraction of this book would have met every assertion, never met the evidence,
and shown no sign of the loss.** All 46 image objects were enumerated and all 30 data figures opened.
**At least nine tables carry content found nowhere in the text**, including the full urban and rural
SEC classification grids, the eight-layer consumption-intensity scheme, the GDP distribution that is
the source of the text's US$367 billion bottom-of-pyramid figure, and the youth-segment profile that
substantiates the book's own sampling argument. Four objects rest partly on tables that could not
have been read from the text. Six quantitative claims were checked against their tables and all six
hold — one, the rural shampoo penetration, only after separating the confirmed measurement (13.3% in
2000 to 68.7% in 2008) from the causal attribution to packaging innovation, which is the author's own
footnote to her own table and is not evidence. A seventh, Figure 4.2, was opened and found to carry
**no data at all**: it is a schematic that illustrates its argument and is not evidence for it.

**Across the three delta sources: 21 authorial visual claims checked — 19 confirmed, 1 partially
confirmed, 1 confirmed as schematic only.**

## O-9. Two representation defects in the supplied copies, both found mechanically

- **Desai's copy has been modified by a redistributor.** `dc:publisher` reads `GAPPAA.ORG` instead of
  HarperCollins, and the string appears at 11 positions. Ten are obviously non-authorial front
  matter. **One is a complete non-authorial sentence inside an authorial paragraph of the
  Introduction**, with no distinguishing markup: *"My effort in this book has been to examine Middle
  India from within. **This book has been downloaded from gappaa dot org.** I have grown up in a
  middle class family…"*. All 11 located and excluded.
- **Pandeymonium's copy flattens pull-quotes into the body text.** A duplicate-sentence scan returned
  exactly **10 sentences, each occurring exactly twice**. A naive pass could read the standalone
  pull-quote as a second claim and double-count it.

## O-10. A first reading I got wrong, and the check that corrected it

Pandeymonium's EPUB folders are named `GoogleDoc/`, which I initially read as evidence of a
re-typeset non-publisher copy — which would have been a serious provenance problem and would have
pushed it to HOLD. **That reading was wrong.** The file carries Penguin's complete copyright page:
the Portfolio imprint, "First published in Portfolio by Penguin Books India 2015", the cover-design
credit, the print ISBN, and a digital-edition page whose **e-ISBN matches the ISBN in the OPF
metadata**. A re-typeset copy would not reproduce a matching e-ISBN.

I record this because the corrected conclusion is load-bearing for admission and you should be able
to re-run the check. It also corrects the supplied filename, which says 2016; the book is 2015.

## O-11. No cross-source promotion exists anywhere

Verified repository-wide **after the delta pass**: **zero** concepts with `kind:
cross_source_concept` and **zero** with `asserts_agreement_between_sources: true`. No
`same_failure_family` was created. **Eight** apparent agreements are now recorded as observations
only — the original four plus four from the delta pass — each with the reason it was refused.

## O-12. [delta] Three real lineage relations were found, and none defeats independence

Independence is pairwise throughout; there is no global count in the matrix and none can be derived
from it.

1. **Dwyer & Patel cite Kajri Jain** — ch. 2 note 9, *"Kajri Jain, 'Gods in the Bazaar', South Asia,
   XXI/1 (1998)"*, the journal article her book grew out of five years later. **Directional and
   inbound to the earlier work**; Jain's book cites Dwyer & Patel nowhere. `cites_source`, verdict
   `independent_origin`. **What it required, and what was done:** both books use *frontality* and
   *iconicity* and do not mean the same thing by them — Dwyer reports Geeta Kapur's formal
   art-historical categories applied to cinema, Jain treats frontality as a functional requirement of
   ritual use with a stated devotional mechanism. Both terms are held **source-local with each
   author's own gloss**. No concept was merged.
2. **Bijapurkar cites Santosh Desai** — repeatedly, and thanks him in her Acknowledgements: he *"has
   been quoted quite a bit in this book"*. Desai is another CANON-014 candidate. **The date order
   settles what the relation is**: Bijapurkar is 2007/2009 and *Mother Pious Lady* is a 2010
   collection of columns, so she cites his columns and conversations and cannot be citing the book.
   `cites_source`, verdict `independent_origin`. The specific attributions are enumerated in her
   `ontology-mappings.yaml` under `t_rbwl_0060` **as an attribution record and not as a concept**,
   precisely because the party attributed is another candidate. **Practical consequence: agreement
   between these two on a cultural observation is not two independent observations.**
3. **Parameswaran cites Bijapurkar** — *We Are Like That Only* by name in his endnotes. **This row
   was recorded FORWARD in v1 of the lineage matrix**, as a relation that would become live the
   moment a Bijapurkar source was admitted, with the specific warning that his account of Indian
   youth partly rests on her work. It is now live and the warning was correct.

Two further predictions from v1 also resolved: the forward row warning that Parameswaran's bazaar-art
material is **second-hand** (reporting Arvind Rajagopal) became operative the moment *Gods in the
Bazaar* was admitted — where the two appear to agree about calendar art, one is a first-hand
ethnography and the other a practitioner relaying a scholar, so the corroboration value is nil. And
the forward row for Dwyer correctly **stayed** forward: Parameswaran cites *Picture Abhi Baaki Hai*,
a different work by one of *Cinema India*'s two authors, twelve years later, so that pair starts and
stays at `no_known_relation`. **Three forward rows, three correct outcomes.**

## O-13. [delta] A validator defect was found and fixed at the root

`validate_experimental.py` reported `[BOUNDARY] check 6: live Canon knowledge … was modified —
forbidden` for every file in the three new source directories. **The finding was false and the
validator was wrong**, in three separate ways:

- It used `git diff --name-only`, which reports *that* a path changed and not *how*. Checks 6 and 7
  exist to stop an accepted source being **modified**; this task's authorised job is to **add** new
  candidate directories under exactly those prefixes, which its own allowlist two lines below
  permits. Verified mechanically: `git diff --name-status origin/main...HEAD --
  canon/knowledge/current/ canon/audit/records/ | grep -v "^A"` returns **nothing**. Every path is an
  addition; **zero modifications**.
- The whole block was wrapped so any failure became a **warning**. A boundary check that cannot run
  has verified nothing — that is how a run without `origin/main` fetched can report PASS while
  checking nothing.
- `canon/experimental/canon-014-qa/`, where this task's own Q&A banks live, was missing from the
  allowlist.

**The fix strengthens the check.** Additions and modifications are now distinguished; a modification
or deletion under the two candidate prefixes is still an error; the prefixes where nothing may be
written at all (`coordination/`, `PROJECT-MEMORY.md`, the frozen SPECs, `governance/`, the Capability
Registry) now error on **additions too**, which the old code would have missed; and inability to run
the check is now an error. The validator passes on this branch with no false positives.

**Then it immediately caught me, and I let it win.** I had fixed two real defects in
`tests/test_request_freeze_gates.py` (F-06 — see O-15) and the strengthened check reported that file
as outside CANON-014's allowlist. **The finding was correct**: that is a CANON-010 file and this
task's allowlist covers its own new test, not another task's. The available move was to add the path
to the allowlist — and adding a path to an allowlist in order to authorise one's own edit is exactly
the failure this branch was set against. **The fix was reverted and the defect routed to you as a
finding instead**, which is the same handling F-01 got. I record it because a boundary check that
only ever fires on other people's work has not been tested.

## O-15. [delta] `pytest tests/` currently collects nothing, and every green suite figure is a subset

Found while running the full suite. `tests/test_request_freeze_gates.py`, from CANON-010 commit
`3cf2979`, has two defects:

- **`ROOT` is hardcoded** to `pathlib.Path('/home/user/media-intelligence')`, the absolute path of
  the container it was written in, so every path derived from it fails in any other checkout.
- **Its runner block runs at module scope** with no `if __name__ == "__main__"` guard, so importing
  the file calls `sys.exit(0)` — and pytest aborts collection of the **entire suite** with an
  INTERNALERROR. **No test in the run executes**, not this file's and not any other file's.

**The consequence for how you read numbers in this repository:** the only way to get a green suite is
`--ignore=tests/test_request_freeze_gates.py`, and **that is where the "135 passed" figure comes
from** — everywhere it appears, on this branch and the last. It is the suite minus this file. A
reader could reasonably take it for the whole thing.

I fixed both (two lines, no assertion or fixture touched) and verified: the full suite then collects
and reports **136 passed, 117 subtests**, all seven CANON-010 gates fire standalone, and nothing under
`canon/experiments/**` is left mutated afterwards. **Then I reverted it**, for the reason in O-13. The
verified patch is recorded in full as **F-06** in
`canon/findings/CANON-014-LIVE-SOURCE-REAUDIT-FINDINGS.md`, and it needs a task that owns `tests/**`.
I would treat it as higher priority than two lines suggests: until it lands, the repository has no
runnable full test suite.

## O-14. [delta] No book bytes were committed — and a pre-existing condition you should see

**CANON-014 adds no binary file of any kind.** Verified mechanically over both the committed diff and
the pending working tree: no `.pdf`, `.epub`, `.mobi`, `.azw3`, or image file is added by this
branch. Only derived Canon artifacts are committed, per your instruction. All three book PDFs stayed
in `~/Downloads/` and are recorded only by SHA-256, byte count and bibliographic detail.

**Reported because I found it while checking that, and it is not mine to fix:** `canon/sources/` on
`main` already contains **21 page-image JPGs** (`canon/sources/figures/p43-43.jpg` and siblings) and
**six extracted book text files** — Molly Bang, Lupton, Ogilvy ch. 2, Williams, Grammar of the Shot
ch. 4 and Light: Science & Magic ch. 3. They were committed by `2cf4988` ("Set up three-workstream
operating structure"), long before this task, and this branch does not touch them.

I am not adjudicating it and I have not changed anything. I am flagging it because it is the same
class of artifact this task was explicitly instructed not to commit, it concerns in-copyright works,
and the instruction I was given suggests it may not be intentional. Your call entirely.

---

# INFERRED

Everything below is my judgement and could be wrong.

## I-1. The previous summary's error was of kind, not arithmetic

"12 new independent origins + 5 scope extensions" reports independence as a **per-source property**.
The Audit Gate is explicit that independence is a property of a **pair**. No single number can express
that *Grammar of the Shot* is not an independent origin against its companion volume and is a
perfectly good one against everything else. The lineage matrix therefore records pairs and contains
no global count, and one cannot be derived from it by counting rows.

Two pairs the old summary specifically mishandled: Hopkins's *My Life in Advertising* is a distinct
**work** that shares author and position with the live Hopkins (`shared_author`, zero independence
against it — a different title is not a different origin); and Sullivan/Ogilvy is
`independence_not_established`, which **blocks** promotion rather than quietly passing as independent.

## I-2. The Parameswaran/Pandey pair is independent, and I tested it before saying so

The candidate relation was `shared_primary_informant`: Parameswaran names Piyush Pandey, and both
books discuss Fevicol, Cadbury Dairy Milk and Asian Paints. I rejected it. The Audit Gate requires a
practitioner's claims to be **load-bearing in both works**; Pandey appears in one passage, in a list
of four writers, illustrating a point about language, and **no claim extracted from Parameswaran
rests on his account of anything**. The shared campaigns are common property of the industry both
worked in. Shared subject matter is not shared origin.

## I-3. The most important new knowledge is the plate section, not the prose

The prose of these three books is valuable context. What is *new to this corpus in kind* is nineteen
reproduced Indian advertisements read first-hand — the corpus's first Indian visual material of any
sort. Six mechanisms came out of it that no text-only pass could have produced (O-8).

The single most useful individual finding, for this project specifically, is **O-8's four
unsettled captions**. It is direct evidence that a caption-plus-figure pair is not self-verifying,
which bears on every retrieval and every evaluation this system will build.

## I-4. The most important contradiction of existing Canon is F-03, and it is not a contradiction between sources

The later *Light: Science & Magic* chapters **qualify and in one case reverse** live chapter-3
guidance. Live `sk_lsm_c003_0019` offers polarizing the light source as a remedy **with no cost
attached**; the same authors later write *"Polarizing the light source has serious drawbacks and is a
solution to avoid whenever possible"* — four to six stops in practice, depth-of-field and movement
consequences, heat damage, a colour shift. A polarizer's place in the remedy order is also reversed
between chapters 4 and 5, and a glass-support trick is explicitly withdrawn for black subjects.

**This is one author team revising itself within a stated scope, not two sources disagreeing.** The
CANON-013 lane recorded that correctly and I have preserved it. It matters because a consumer
retrieving that live object today gets a remedy the authors themselves later warn against — the exact
shape of error the Canon exists to prevent. I could not verify it: the source is unavailable here.

## I-5. A second contradiction, inside the new material, that I deliberately did not resolve

Parameswaran and Pandey both bear on advertising pre-testing and **pull in different directions**.
Parameswaran reports it as established practice with a distorting side-effect (celebrities raise
scores, so celebrities get cast) and does not say it should stop. Pandey rejects the procedures
outright. One is a practitioner reporting an industry incentive; the other is a practitioner
defending his own work with counterfactual claims about tests that were never run. Recorded as OBS-02,
unresolved. Both bear on evaluator design, which is live work here — which makes it **more** important
not to merge them, not less.

## I-6. The pair I most expected to be asked to merge, and refused

Parameswaran's censored-word substitution (*gori* → *nikhri*) and Desai's descriptor inflation
("fair" → "VV Fair") look alike to any keyword pass. **The mechanisms run in opposite directions.**
One is a word *acquiring* a meaning it did not have, under an external prohibition, driven by one
advertiser's sustained investment. The other is a word *losing* force it did have, with no prohibition,
driven by universal adoption across many writers. They share only the surface feature that a word's
meaning changed with use. Recorded as OBS-03, refused, with the caveat on both objects.

## I-7. Where I judged the sources weakest

- **Parameswaran** invokes "a frame-by-frame content analysis of consumer product television
  advertising in India, released over the last fifty years" and reports two findings from it with no
  numbers, sample, method or attribution — and the chapter's endnotes cite nothing resembling a
  content analysis. He also reports his **own agency's consulting arm** as a source of findings
  (ManMood, Youth Mood, the 2002 celebrity study), always without method or effect size. The 2002
  study's decisive dimension, "Aura", is **never defined**.
- **Desai's** one measurement — a thirty-year content analysis of matrimonial advertisements — has no
  sample, frame, coding scheme, date range or single number. Its most valuable result is a **null**
  (caste mention did not change), which is the least likely to be selectively reported.
- **Pandey's** book is structurally survivorship: every case is one that succeeded, no campaign
  outcome is evidenced anywhere, and his central argument rests on counterfactuals about pre-tests
  that were never run. He counts the other branch exactly once, noting he would have been "history"
  had the Tata Cement pitch been lost.

## I-8. [delta] The gap your authorisation aimed at is now closed on five of six fronts

You chose these six books to attack the Indian cultural and Indian visual gap, and made the visual
pass mandatory because *Gods in the Bazaar* and *Cinema India* are the visually demanding ones.
**Those two were exactly the ones missing after the first pass. They are now in, and both had their
visual passes run first-hand.**

**Gained:** Indian advertising history; Indian everyday material culture; Indian creative practice;
Hindi-film poster and publicity convention for a dated period; first-hand ethnography of the Indian
calendar-print trade, 1994-2001, with named informants; and a set of named reasoning errors about the
Indian consumer market, deliberately stripped of every number. Across the six, **48 reproduced Indian
images inspected first-hand** (19 advertising plates, 11 film-publicity plates, 7 calendar-art
figures, 30 data figures — of which 30 and 19 are complete passes) and **21 authorial visual claims
checked**.

**The calendar-art position has changed materially.** Before the delta pass the only calendar-art
material anywhere in the corpus was Parameswaran's second-hand paragraph reporting Rajagopal. There
is now a primary source, and the lineage matrix records that Parameswaran must **not** count as
independently corroborating it.

**Still unclosed: Devanagari and Indic typography.** Nothing in these six sources addresses it. The
one Devanagari observation in the whole corpus remains the Coca-Cola "Thanda matlab" plate in
Parameswaran, which shows a script decision and analyses none. The position is unchanged from
CANON-013 and I would record it as deliberately open.

**A second bound worth stating plainly.** *Cinema India* dates its own subject as ending in the 1990s,
in its own Conclusion. *We Are Like That Only* states twice that its data expires. Jain's material
runs to roughly 2006. **What the corpus has gained is historical Indian visual and market culture,
carefully bounded — not a current picture of India.** Treating any of it as current would contradict
all three sources.
## I-9. [delta] What the three new sources materially add, and where they are weakest

**Cinema India** adds a documented account of how a poster carries a plot without text — a
compression code the *viewer* holds, built from character types the casting convention taught them —
and a distinct design problem this project has no name for: **re-release publicity targets what the
audience RETAINS, not what the film was originally sold on**, which is why *Aan*'s redesign acquired a
sword fight that was not on the original poster. **Weakest:** everything in it is dated by its own
authors, the evidence base is a survival sample of what happened to be collectable, and nothing in it
is measured — no attendance, sales or recognition figure appears anywhere.

**Gods in the Bazaar** adds the most operationally useful material in the batch and is therefore the
one most at risk of being turned into a rule set. Four things: a **fully documented case of a
production convention outliving its cause** (manual colour retouching, begun because filters and film
were inadequate, migrating into software after digital scanning made it unnecessary); a structural
account of **why a purchase signal is not a preference signal when the purchaser is not the viewer**;
a distinction between an **enabling condition and a grading criterion** that this project's
evaluation work lacks a name for; and two idiom constraints, confirmed against the plates, that a
generator working from naturalist priors would violate by default. **Weakest:** the reasons given for
the constraints are practitioner testimony, the author states herself what that testimony can bear,
and no audience-level claim in the book is measured. There is no sample size anywhere in it.

**We Are Like That Only** adds a set of **named reasoning errors with worked cases**: reading a
supply-side change as a consumer character trait; planning on a segment label with no stated
definition or population base; extrapolating a stock release as though it were a flow; and treating a
threshold derived by holding prices fixed as a fact about buyers rather than about supply.
**Weakest, and it must be said plainly:** two of its most quoted arguments rest on nothing. The
no-frills failure argument **names no failed product at all** — not one firm, product, date or
figure. The change-confluence framework is illustrated by undated, unattributed consulting cases with
no outcomes. The mechanisms are clear and useful; the outcome claims are not evidenced, and every
binding drawn from the source binds the reasoning and never the outcome.

## I-10. [delta] The agreements I most expected to be asked to promote, and refused

Four, recorded as observations in the lineage matrix with the reason on each:

- **OBS-05** — Jain documents a convention **surviving** the loss of its justification; Dwyer & Patel
  document one being **displaced**. These are opposite outcomes of the same transition type, and
  merging them would erase the only interesting thing about the pair.
- **OBS-06** — the front-facing figure. **The strongest-looking convergence in the batch and the one
  most clearly to be refused.** Jain records a production rule practitioners say they follow in a
  print trade; Dwyer reports an analytic category two film scholars apply to a medium, and bounds her
  own agreement with it. The pair also carries a `cites_source` relation, so even the appearance of
  independent arrival is weakened.
- **OBS-07** — a misread demand signal. Jain's case is about **who the signal comes from**;
  Bijapurkar's is about **what caused it to move**. A single concept would be a keyword merge of two
  structurally different errors. Both bear on evaluation work that is live here, which makes
  premature merging more costly, not less.
- **OBS-08** — three sources in one batch that state their own limits. That is an observation about
  the audit, worth your attention when weighing these against sources that do not, and it is not a
  claim any two of them share.

## I-11. [delta] What these books qualify in existing Canon

Nothing in accepted live Canon is contradicted by the three new sources. Two qualifications are worth
recording:

- **Parameswaran's calendar-art paragraph is now superseded rather than merely flagged.** His own
  audit record predicted this. Where his second-hand report and Jain's first-hand ethnography agree,
  that is one observation, not two.
- **Bijapurkar's cultural-observation material in her chapters 8 and 9 partly derives from Desai.**
  Both are CANON-014 candidates. On that subset, agreement between them is one voice reported twice.

Neither is a contradiction and neither requires a Controller decision now. Both would matter the
moment anyone tried to build a cross-source concept from Indian cultural material, which is why they
are recorded pairwise before anyone tries.

---

# RECOMMENDED

Proposals. None acted on. None of these is a decision.

## R-1. Merge the branch, treating it as three separable decisions

The branch is one PR but contains three things you could accept independently:

1. **The validator correction and its tests** — the lowest-risk and, I think, the highest-value part.
   It closes a hole that let a defective package report PASS, and it immediately found two defects in
   accepted Canon that nothing else had.
2. **The CANON-013 repair** — mechanical, reversible, and leaves all 17 still HOLD.
3. **The six new accepted sources** — the only part that changes what live Canon contains. **[delta]**
   These are now six rather than three, and they split further if you want them to: the three from
   the first pass are practitioner and interpretive material, and the three from the delta pass are
   two academic studies and one market-analysis book. Nothing couples them.

If you want to accept (1) and (2) and defer (3), that is coherent and nothing in the branch prevents
it. **[delta] The validator fix at O-13 is now part of (1)** and is the piece I would take first: it
found and corrected a check that was reporting a false boundary violation while a second defect in
the same block could have let a real one pass silently.

## R-2. Decide F-01 (Sutherland) explicitly rather than letting it sit

Three concept systems in an accepted source have no `provenance`. Repairing it requires opening the
book, which stales the audit, which requires re-running the gate. That is a small task and it needs
your authorisation because it touches accepted knowledge. The test I added will keep failing-visible
until it is dealt with, which is deliberate.

## R-3. Enumerate `target_type` in SPEC-04

A spec whose validation rule cites a "fixed list" it never states is a trap for the next person who
writes a binding. Adding `benchmark` to an explicit list is a small edit and is yours to make.

## R-4. [delta] Resolved — and one thing to decide in its place

**This recommendation is closed.** All three books were found locally and processed; the Indian
visual-culture gap is closed on the two fronts this recommendation named.

**What replaces it is a decision about completeness of inspection.** The visual passes for *Cinema
India* (11 of ~121 plates) and *Gods in the Bazaar* (7 of ~156 figures) are **bounded by cost, not
blocked**: both copies are intact, both page mappings are established and reproducible, and any plate
or figure can be rendered on demand. The ledgers say so explicitly, and the bound is recorded as a
coverage statement rather than as a loss pattern, because nothing is missing from either copy.

I would not treat this as urgent. No object in either record rests on an uninspected plate, and every
object resting on an inspected one names it. But it is a real difference from *We Are Like That
Only*, whose pass is complete — and the Bijapurkar case is the argument for finishing the other two,
because its complete pass is precisely what surfaced nine tables whose content exists nowhere in the
text. **A bounded pass cannot tell you what it did not look at.**

## R-5. Do not resolve OBS-02 by picking a side

The Parameswaran/Pandey disagreement about pre-testing is real and both are self-interested
practitioners. It bears directly on evaluator design here. My recommendation is to keep it recorded
as a live disagreement and let the project's own empirical work settle it, rather than promoting
either into Canon as the position on pre-testing.

## R-6. Treat `light-science-magic-ch3` as the priority re-audit when a source library is next available

F-03 and F-04 both attach to it: its guidance is qualified by the authors' own later chapters, and its
visual block was environmental and is now known to be liftable (that lane inspected 54 figures where
the live record has 14 unseen). Of everything in this brief, this is the finding most likely to be
actively misleading a consumer today.

## R-7. Consider whether the Audit Gate needs a category for insider institutional recollection

Five Parameswaran objects are an industry participant recounting institutional facts decades later
without a contemporaneous record — his own censorship rejection, ASCI's constitution, a lost internal
argument. These are neither disinterested third-party reports nor measurements, and no
`evidence_origin` category fits. I placed them at `origin_unresolved`, which is honest but loses the
distinction. Adding a category is a Controller decision of the same kind as CANON-006's
`shared_primary_informant` and CANON-007's `figure_semantic_binding_lost`, and I have not made it.

There is a second, smaller vocabulary gap: **no loss pattern covers third-party text injected into an
authorial paragraph** (O-9). I used `text_layer_order_damage`, which is the closest fit and is not
quite right — nothing was reordered, something was inserted.

## R-8. [delta] Decide whether "no authored page" needs a stronger convention than a null

*We Are Like That Only* is the fourth source in this corpus with no authored page in the copy used,
and the handling is by now consistent — `page_start` and `page_end` null, locators by chapter and
section heading. It works because that book's headings are numbered, distinctive and non-repeating.
**It would not work for a book with repeated or generic section headings**, and nothing in the specs
says what to do then. That is a Controller decision of the same kind as the other vocabulary gaps in
R-7, and I have not made it.

---

# The one residual mechanical limitation

Everything checkable in this repository was checked and run: both Canon validators, the experimental
validator, all four test suites, all snapshot digests, every count, and the duplicate and injection
scans. Snapshot digests were computed with the repository's **own** `compute_source_snapshot`
function, so the validator recomputes exactly what was written.

**[delta] The three books previously reported as unobtainable were found on the local machine and
processed, so that limitation no longer applies to them.** What remains is unchanged in kind:

**The one thing that could not be done is re-opening any source that is not present on this machine,** because there is no local library and no network egress. That single limitation is the
whole reason the seventeen CANON-013 candidates are HOLD rather than assessed, and the reason F-03,
F-04 and F-05 are reported as findings from another lane rather than as verified observations. I have
not represented any of them as verified here.
