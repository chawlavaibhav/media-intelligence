# Provenance record — Jonah Berger, *Contagious: Why Things Catch On*

**EXPERIMENTAL — NOT LIVE CANON.** `book-expansion-qa-v1`, non-merge, exploratory lane. Nothing in
this directory is accepted Canon and nothing here may be described as accepted.

`source_id: berger-contagious` · ID prefix `ctg`

---

## 1. Source identity

| Field | Value |
|---|---|
| Author | Jonah Berger (Wharton School, University of Pennsylvania) |
| Title | *Contagious: Why Things Catch On* |
| Publisher / date | Simon & Schuster; jacket copyright notice **© 2013 Simon & Schuster** |
| Local form | EPUB (reflowable), `Contagious_ Why Things Catch On.epub` |
| Local path | `/Users/vaibhavchawla/Downloads/Books/Contagious_ Why Things Catch On.epub` |
| File size | 592,807 bytes |
| MD5 | `625aba06ceed728ba573dad60a52b3ed` |
| Extracted text | `scratchpad/src/EPUB-Contagious__Why_Things_Catch_On..txt` — 417,081 characters of body text across 17 spine documents with text |

## 2. Span processed

**The whole book was read and is in scope**: Introduction ("Why Things Catch On"), chapters 1–6
(Social Currency, Triggers, Emotion, Public, Practical Value, Stories), the Epilogue, and the two
long author footnotes attached to the Introduction and chapter 1. The Notes section (spine 17) was
read **as an attribution source only** — it is what establishes, study by study, whose research each
finding actually is, and that distinction is the disciplinary point of this lane.

Also read and used, but marked as such wherever cited: **"A Conversation with Jonah Berger"** (spine
14), part of the Simon & Schuster Readers Group Guide back matter. It contains one statement about
the framework that appears nowhere else in the same words ("No one of the STEPPS is most important,
but certain ones are definitely easier to apply in certain situations"), so it is used, always with
the back-matter status stated in the object.

Not extracted: the dedication, acknowledgments, About the Author, the Questions for Discussion, and
the Index.

## 3. Locators — **Case 3, EPUB, no authored page exists**

The supplied text file's own header states: `FORMAT: EPUB (reflowable). THERE ARE NO AUTHORED PAGE
NUMBERS IN THIS FORMAT.` Markers are `<<<SPINE n | FILE index_split_00n.html | TITLE ...>>>`.

Accordingly, per `SCHEMA-CONTRACT-ADDENDUM-LOCATORS.md` Case 3:

- Every locator is **chapter plus named section**, e.g.
  `Ch. 2 "Triggers", section "What Makes for an Effective Trigger?" (spine 7)`.
- The spine number is carried as a secondary aid only. **It is a file position, not a page.**
- `provenance.page_start` and `provenance.page_end` are `null` in **every** object, and
  `provenance.locator` carries the chapter/section string.
- **Audit pattern recorded: `no_authored_page`.** This is a property of the format, not a defect in
  the extraction, and it is unfixable in this copy.

**The endnotes are a page-number trap and were treated as one.** The Notes section is dense with
page numbers — `Journal of Marketing Research 49, no. 2, 192–205`, `Marketing Science 29, no. 5,
815–27`, and so on. **Every one of those numbers is a page range inside a different work** (a
journal article, another book). None of them is a locator into *Contagious*. No number from the
Notes has been used as a locator anywhere in this extraction.

The book's own body text contains no internal "see page N" cross-references, so no unresolvable
internal cross-reference had to be recorded.

## 4. Access basis and rights

The Controller authorised **read-only use of an already-present local copy**. Use here is local,
read-only and internal to this research task. No render, image or extract of the book is committed;
the extraction files contain paraphrase and short terminology quotations only.

**NOT VERIFIED: the licence status of the local file.** This lane did not and could not establish
it, and states it unresolved rather than assuming it, exactly as the live `heath-made-to-stick-introduction`
record does for its own EPUB.

## 5. Overlap with live Canon

**No overlap. Independent origin.** *Contagious* is not in `canon/knowledge/current/` in any span,
and this is not a scope extension of any live source. `scope_extension_of: null`.

## 6. Observations for cross-source review (NOT promotions)

**These are observations only. No cross-source concept, no `xs_` identifier and no cross-source
claim has been created anywhere in this lane, and nothing below may be read as corroboration.**
Every SourceKnowledge object here records only what *Contagious* says.

The live extraction `canon/knowledge/current/heath-made-to-stick-introduction` was read in full
before drafting, precisely so that convergence could be told apart from restatement. Six things are
worth a reviewer's attention:

1. **Adjacent in kind, different in target.** Both sources are named six-part frameworks by
   academics writing for a trade audience. But Berger states the difference himself, in the text,
   and names the Heaths while doing it: their book is about getting an idea **remembered**; his is
   about getting a product or idea **passed on**. Berger also discloses that Chip Heath was his
   graduate mentor. A reviewer should treat the two frameworks as addressing **different dependent
   variables**, on the source's own testimony, not as two versions of one theory.

2. **The frameworks are structurally different in a way that matters.** The Heath extraction records
   `sk_hea_mts_0019 the_six_traits_are_a_common_set_not_a_formula`. Berger's footnote goes further
   and more specifically: he says the six are **relatively independent**, that **not all six are
   required**, and that a product weak on one will not fail for that reason. Whether these are the
   same claim is a reviewer question, not an extractor conclusion, and it is not resolved here.

3. **Berger cites the Heaths inside his own text** — the "Three Whys" technique in the Emotion
   chapter is credited to *Made to Stick* by name. That is a real citation relationship between two
   works in the corpus, and it is recorded in the relevant object's caveats as the source's own
   attribution. It is **not** evidence that the two agree about anything else.

4. **One apparent overlap that is NOT the same claim.** Heath's "unexpectedness" and Berger's
   "remarkability" look alike and are not. Heath's is about **holding attention** on an idea being
   communicated; Berger's is about a property that makes the **teller** look good and so buys them
   social currency. Berger's mechanism runs through the sharer's self-presentation; Heath's does
   not. This is recorded in `ontology-mappings.yaml` as an explicit `distinct_from` relationship
   between this lane's own terms and stated in prose here, and it is **not** written as a
   cross-lane relationship because the Heath term ids are not resolvable from this lane.

5. **The two sources have opposite evidence profiles, and this is the most useful observation.**
   The live Heath record states plainly that its source "reports measurement constantly, almost none
   of it their own", and that the vocabulary gap makes the book read weaker than it is. *Contagious*
   is the inverse case: a large fraction of its central findings are **Berger's own published
   studies, with figures**. If the corpus has been looking for a source that can carry
   `empirical_within_source` honestly, this is it — and that is exactly why the own-versus-third-party
   split had to be done carefully rather than generously. See §7.

6. **A shared hazard, differently shaped.** Both books are trade-press compressions of journal work.
   Heath's compression hides third-party provenance; Berger's compression hides **statistical
   qualification** — correlational field studies are narrated with the confidence of experiments.
   That is recorded per-object in caveats, not resolved.

## 7. Evidence stance — read this before reading any `evidence` field

SPEC-03 defines `empirical_within_source` as "the source reports its own measurement", and the fixed
characteristic list contains **no value for research by a third party**. This lane therefore did
what the live Heath extraction did, and for the same reason:

- **`empirical_within_source` is applied only where the measurement is Berger's own** — a study he
  conducted or co-authored, or a demonstration he himself ran, and where he says what it found.
- **Every third-party study is recorded in a caveat marked `origin: extractor_observed`, naming
  whose study it was**, with its design and figures. It never contributes an evidence characteristic.
- Where a claim is Berger's own but rests on a **single** study, or on **correlational field data**
  narrated as if causal, that is said in an `extractor_observed` caveat. His confidence is reported;
  it is not adopted.

Counts and the full own-versus-third-party ledger are in `EXTRACTION-NOTES.md` §4.

## 8. Replication status

**NOT VERIFIED and out of scope.** This extraction records only what the book claims. It asserts
nothing about whether any finding in it has since replicated, been revised, or failed. Several of
the cited works are 2011–2012 working papers at the time of writing, which is recorded as a fact
about the source, not as a judgement.

## 9. Period-bounding

The book is of 2013 and its platform environment is of 2011–2012: Foursquare mayorships, Rue La La,
the pre-algorithmic Twitter timeline, the *New York Times* Most E-Mailed list as a scarce ranking
surface. Every object whose support depends on that environment carries `historical_claim`, and
several carry `culturally_bounded` where the examples are specifically American.

## 10. Scope limit on translation

*Contagious* is about **transmission between people**. Nothing in this extraction translates any of
it into a model instruction, and nothing in it is evidence about what any generative system can do.
Where the project might apply a claim, that leap lives only in `operational-bindings.yaml`, marked
as ours.

## 11. What was produced

54 SourceKnowledge objects · 5 SourceConceptSystems · 14 operational bindings (6 evaluation,
4 benchmark, 4 governance; no `creative_ir` and no `production`) · SPEC-05 ontology (66 terms —
22 problems, 23 remedies, 17 properties, 4 entities — 15 relationships including 6 `distinct_from`,
7 source-specific concepts) · 60 Q&A pairs, 23 of them `requires_application: true` (38.3%).

Self-check results are in `EXTRACTION-NOTES.md` §7. Headline: all YAML parses; all 119 locator-bearing
objects verified to carry null pages and no page-style locator, with zero failures; 19 objects carry
`empirical_within_source` and every one was checked back against the attribution ledger; the
application fraction is 23/60 = 0.3833 against a threshold of 0.3333.
