# CANON-014 — Controller Brief

**Branch:** `claude/canon-014-expansion-admission-ntp0dl` · **Not merged.** Nothing here is live
project knowledge. Paths under `canon/knowledge/current/**` created by this task become live **only
if you merge the branch**.

This brief separates **OBSERVED** (what is mechanically checkable in the repository or was read
directly from a supplied file), **INFERRED** (my reading, which could be wrong), and **RECOMMENDED**
(proposals, which are not decisions). Nothing in RECOMMENDED has been acted on.

---

# OBSERVED

## O-1. Three of the six named books were supplied. Three were not.

Attached to this session: **Parameswaran** (*Nawabs, Nudes, Noodles*), **Desai** (*Mother Pious
Lady*), **Pandey** (*Pandeymonium*). Not attached: **Dwyer & Patel** (*Cinema India*), **Kajri Jain**
(*Gods in the Bazaar*), **Bijapurkar** (*We Are Like That Only*).

The duplicate-upload point in your authorisation did not arise: Mother Pious Lady was supplied once.

**This environment has no external network egress.** Verified rather than assumed — a direct HTTPS
request and the harness fetch tool were both refused by the egress proxy for every external host
tried, including `w3.org` and `gutenberg.org`. Nothing could be fetched to replace a missing book.

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

## O-5. Counts, recomputed mechanically from final files

**The 777 ontology figure in the previous chat report is wrong. The correct figure is 823**, and it
was already correct in that package's own README — the error was in the report, not the artifacts.

CANON-013 package: **822** SourceKnowledge · **70** systems · **184** bindings · **823** ontology
terms · **899** Q&A.

CANON-014 accepted-shape additions: **59** SourceKnowledge · **8** systems · **16** bindings ·
**52** ontology terms (plus 25 relationships, 8 concepts) across the three READY sources.

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
does to a distribution. The three **new** banks, written with no floor at all, come out at 46.2%,
23.8% and 35.3% — and Desai's 23.8% would have failed the old rule, which is the correct outcome for
a collection of interpretive essays.

## O-7. Three sources are READY; twenty are HOLD

**READY — the three supplied books**, each in live shape with all five snapshot files plus
`PROVENANCE.md`, and an Audit Gate v0.2 record written against those exact bytes,
`source_reopened: false`:

| Source | SK | Sys | Bnd | Terms | Visual pass | `claim_resolution` |
|---|---|---|---|---|---|---|
| `parameswaran-nawabs-nudes-noodles` | 32 | 4 | 9 | 22 | **19/19 plates inspected** | `some_underdetermined` |
| `desai-mother-pious-lady` | 17 | 2 | 4 | 18 | completed, null result | `not_applicable` |
| `pandey-pandeymonium` | 10 | 2 | 3 | 12 | completed, evidence never printed | `not_applicable` |

**HOLD — 20:** the 17 CANON-013 candidates (blocker at O-2, plus the five specific representation
defects your authorisation named, none of which is resolved) and the 3 books never supplied.

**Mechanical status:** Audit Gate validator **22 records, 0 errors**. Schema validator **22
directories, 3 errors — all of them F-01**, in a source CANON-014 is not authorised to edit.

## O-8. The visual pass ran on all three supplied books and changed the extractions

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

Verified repository-wide: **zero** concepts with `kind: cross_source_concept` and **zero** with
`asserts_agreement_between_sources: true`. Four apparent agreements are recorded as observations only.

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

## I-8. The gap your authorisation aimed at is partly closed, and the visually demanding half is not

You chose these six books to attack the Indian cultural and Indian visual gap, and made the visual
pass mandatory because *Gods in the Bazaar* and *Cinema India* are the visually demanding ones.
**Those two are exactly the ones not supplied.**

Gained: Indian advertising history, Indian everyday material culture, Indian creative practice, and
19 reproduced Indian advertisements inspected first-hand. Not gained: anything on Hindi-film visual
culture or Indian calendar/bazaar art. The only calendar-art material in the whole corpus is
Parameswaran's **second-hand** paragraph reporting Arvind Rajagopal, explicitly marked as no
substitute for a primary source. **Devanagari and Indic typography remains completely unclosed.**

---

# RECOMMENDED

Proposals. None acted on. None of these is a decision.

## R-1. Merge the branch, treating it as three separable decisions

The branch is one PR but contains three things you could accept independently:

1. **The validator correction and its tests** — the lowest-risk and, I think, the highest-value part.
   It closes a hole that let a defective package report PASS, and it immediately found two defects in
   accepted Canon that nothing else had.
2. **The CANON-013 repair** — mechanical, reversible, and leaves all 17 still HOLD.
3. **The three new accepted sources** — the only part that changes what live Canon contains.

If you want to accept (1) and (2) and defer (3), that is coherent and nothing in the branch prevents
it.

## R-2. Decide F-01 (Sutherland) explicitly rather than letting it sit

Three concept systems in an accepted source have no `provenance`. Repairing it requires opening the
book, which stales the audit, which requires re-running the gate. That is a small task and it needs
your authorisation because it touches accepted knowledge. The test I added will keep failing-visible
until it is dealt with, which is deliberate.

## R-3. Enumerate `target_type` in SPEC-04

A spec whose validation rule cites a "fixed list" it never states is a trap for the next person who
writes a binding. Adding `benchmark` to an explicit list is a small edit and is yours to make.

## R-4. Supply the three missing books, or formally drop them

The two most valuable for the stated gap — *Gods in the Bazaar* and *Cinema India* — are the two
missing. Either they get attached to a future session, or the Indian visual-culture gap should be
recorded as deliberately still open rather than as pending. I would not leave it ambiguous.

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

---

# The one residual mechanical limitation

Everything checkable in this repository was checked and run: both Canon validators, the experimental
validator, all four test suites, all snapshot digests, every count, and the duplicate and injection
scans. Snapshot digests were computed with the repository's **own** `compute_source_snapshot`
function, so the validator recomputes exactly what was written.

**The one thing that could not be done is re-opening any source that was not attached to this
session,** because there is no local library and no network egress. That single limitation is the
whole reason the seventeen CANON-013 candidates are HOLD rather than assessed, and the reason F-03,
F-04 and F-05 are reported as findings from another lane rather than as verified observations. I have
not represented any of them as verified here.
