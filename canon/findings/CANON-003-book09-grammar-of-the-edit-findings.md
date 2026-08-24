# CANON-003 book 9 — *Grammar of the Edit*, chapters 3–5

**Lane B** · branch `work/canon-003-b` · fresh checkpoint `ddef98d`, pushed before any comparison
material was opened.

**Source:** Roy Thompson & Christopher J. Bowen, *Grammar of the Edit*, 2nd ed., Focal Press, 2009.
**Section:** Chapters Three, Four and Five, complete — printed pp.55–109 (PDF 68–122).
**Output:** 60 SourceKnowledge objects · 5 SourceConceptSystems · 48 ontology terms ·
15 relationships · 6 concepts · 11 operational bindings. All validate.

---

## 1. What this book turned out to be

An introductory teaching text that argues almost entirely about **relations between shots**. Nothing
it teaches can be checked by looking at one image, and that single fact shaped every binding the
extraction produced.

Its evidence profile is narrow and consistent: claims are asserted from professional experience,
taught by enumeration, usually given a worked scenario and a demonstration figure, and given a
mechanism about half the time. **There is no measurement anywhere in 55 pages.** No study, no
controlled test of a viewer response, no number that came from counting something. The one numeric
threshold in the section — 30 degrees — arrives as received craft convention with no derivation.

That is worth stating plainly because the batch has now seen two opposite profiles at this
granularity: *Light: Science & Magic* explaining physical causes, and this book asserting practice.
The schema absorbed both without strain.

## 2. Historical comparison

**No historical *Grammar of the Edit* extraction exists in this repository.** Verified by filename
search, and by content search for the title, the authors, and a `gote` identifier prefix. The only
two hits outside this lane's own files are planning documents — `CANON-COVERAGE-MAP-V0.md` and
`CANON-CURRICULUM-V0.md` — which name the book as a *planned* source and contain no extracted claim.

Recorded as **`no historical comparator`**, per CANON-003, rather than manufacturing one. This is the
third such book in the batch, after Albers and Vignelli.

## 3. The companion-volume question — answered, and it is not what the inventory expected

The source inventory selected this book to test "whether two books by the same authors produce
near-duplicate knowledge". *Grammar of the Shot* ch.4 is book 1 of this same batch: same authors,
same publisher, same series, adjacent subject.

**They do not.** The overlap is about 13%, and it is systematically transformed.

*Grammar of the Shot* ch.4 produced 17 objects. Of this book's 60, **eight** cover conceptually
shared ground:

| Shared concept | *Grammar of the Shot* (production side) | *Grammar of the Edit* (editorial side) |
|---|---|---|
| The action line | established by the talent's sight line | established by sight lines **or** an object's direction of movement — broader |
| Screen direction | must be maintained across a cut | same, plus a remedy when the coverage contradicts it |
| The 180° arc | keep all camera setups within it | select only from shots taken within it |
| The 30° rule | **"move the camera at least 30 degrees"** | **"place shots of differing horizontal angles more than 30 degrees apart"** |
| Jump cut | the result of insufficient camera movement | the result of insufficient angle difference **or** compositional similarity |
| Eye-line match | pay off a look with a correspondingly angled reveal | the viewer's gaze crosses the look room and is rewarded |
| Reciprocal coverage | shoot the matching reverse | both singles must come from one side of the line |
| Rules are defeasible | "very few absolutes ... a creative reason is sufficient warrant" | "effective creativity overrules grammar" |

**The pattern in that table is the finding.** Where the two books share a concept, the shooting book
states it as a *camera action* and the editing book states it as a *selection constraint on footage
that already exists*. The 30-degree rule is the cleanest case: one says move the camera, the other
says choose shots. Same geometry, different executor, different remedy, and — importantly for the
product — different applicability to generated material, since "choose among alternatives" assumes a
pool of coverage that a single generated take does not have.

The remaining 52 objects have no counterpart in book 1 at all. This book adds the four transitions
and their meanings, the five edit categories, the six-element decision framework, the whole of sound
(sound bridge, ambience and room tone, split edits, sound leading picture), continuity of content and
of sound, two methods for timing a shot, the invisibility standard, and the claim that a bad edit
damages comprehension downstream. Book 1 in turn has material this book lacks: coverage as a shooting
requirement, how shots compose into scenes and acts, the wider-to-tighter convention, and specific
staging remedies.

### The hazard this exposes

Four terms now appear in two source files with near-identical meaning: `action_line` /
`axis_of_action`, `screen_direction`, `jump_cut`, `eye_line_match`. An aggregation pass looking for
agreement would find them in "two sources" and could promote them to a `cross_source_concept`, which
SPEC-05 defines as requiring **two or more independent origins**.

**These are not independent origins.** Same two authors, same publisher, same series, published
within a year of each other, each cross-referencing the other. Agreement between them is evidence of
one position stated twice, not of two practitioners converging.

SPEC-05 says `origin_ref` is the source, and nothing in the schema records that two `origin_ref`s
share an author. Recorded as **LB-09** in the lane issue file. This is a real finding and it was
produced by the batch's own selection policy — deliberately choosing a companion volume for source
diversity surfaced a defect in how independence is counted.

**It also validates the operator's instruction.** Not merging these two books during fresh extraction
is what makes the comparison meaningful. Had the extraction consulted book 1, the overlap figure
would measure my reading rather than the sources.

## 4. What the fresh pass may have missed

No comparator exists, so the usual check — did the old pass catch something this one walked past —
cannot run for this book. Stated rather than left implied: **the miss rate for book 9 is unknown, not
zero.**

One known gap of a different kind. CANON-002 recorded that the older extractions kept noticing
Creative IR fit that the fresh ones missed, with the inferred cause being that the old rule forced
the question every time. This book cannot test that hypothesis, and neither could Albers or Vignelli.
Three of the batch's books are now silent on the batch's strongest recurring signal.

## 5. Issues added to the lane file

`LB-01` through `LB-08` were written before the checkpoint. `LB-09` follows from the comparison above
and is added after it, marked as such.

The one worth reading first is **LB-01**: SPEC-03's intra-source relation vocabulary could not
express thirteen connections in this book, and the most consequential loss is that the five edit
categories and the four transitions are two orthogonal classifications of the same event — a fact the
source states in its own review and which now survives only as prose in two `caveats` fields.

## 6. Evidence for the current design

Worth recording alongside the problems:

- **The V0 granularity rule held with no invented exception** across a source far more enumerative
  than anything the batch had seen — 60 objects from 55 pages. Ambiguous cases were recorded, not
  resolved by new policy.
- **`VideoCreativeExtension.continuity_requirements`** existed in SPEC-01 as an empty reservation,
  with a note predicting "the filmmaking and editing books will land almost entirely here". That
  prediction came true; this book fills it with a four-way division.
- **Mechanical validation caught a fidelity error that reading did not.** Thirteen relations drafted
  with an out-of-layer vocabulary read perfectly naturally and were caught only by the fixed
  vocabulary check.
- **The layer separation held.** Zero product vocabulary reached the source layer; 11 bindings
  against 60 objects left most of the book unbound, which SPEC-04 says is normal.
