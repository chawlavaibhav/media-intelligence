# Extraction notes — Freeman, *The Photographer's Eye: A Graphic Guide*, Parts 4–10

**EXPERIMENTAL — NOT LIVE CANON.** Lane of `book-expansion-qa-v1`. Nothing here is accepted Canon.
`scope_extension_of: freeman-photographers-eye-graphic-guide` · `independence: none — same work`.

---

## 1. Method

1. Read the whole of converted-PDF pages 71–207 as continuous text, then established the part and
   case structure from the file rather than assuming it. The book's own contents page lists ten
   parts; Parts 1–3 are live Canon and were excluded.
2. Built a page-by-page word-count map first, because the density pattern is itself a hazard here
   (§4.2).
3. **Rendered sixteen pages at 100 dpi with `pdftoppm` and looked at them**, chosen as the pages
   where a claim's substance is carried by a diagram rather than by the caption. Twelve were
   examined closely and are cited in objects; the rest confirmed layout only.
4. Wrote incrementally — source knowledge in six appends of 4–16 objects, the Q&A bank in four
   appends of 13–16 items — and re-parsed the YAML after every append.
5. Ran the self-checks in §6 in code, not by eye.

Rendered and inspected: converted-PDF pages 83, 86, 92, 106, 109, 118, 122, 130, 134, 139, 147,
149, 160, 170, 180, 191.

---

## 2. The page-number hazard — `false_page_affordance` and `converter_pages_not_authored`

This is the governing hazard and it is recorded here under both Canon audit names.

The supplied text file's own header asserts a clean mapping:

```
PAGE MAPPING DETECTED: printed page = PDF page - 0 (folio agreement on 302 pages).
USE THE PRINTED NUMBER IN LOCATORS.
```

**That instruction was not followed, because the mapping is an artefact.** The file is a calibre
3.40.1 conversion into 214 uniform A4 pages; the detector is matching calibre's own injected folios
against calibre's own pagination and finding perfect agreement, as it must. There is no authored
page in this copy — `page_addressability: converter_pages_not_authored`. The affordance is
particularly convincing here, which is exactly what makes it `false_page_affordance`: high support,
zero offset, folios visibly present on the rendered pages.

The live Parts 1–3 audit proved this on five internal cross-references. **This lane found eight
more in Parts 4–10 and checked all of them. Nine for nine point at the wrong case** — the table is
in `PROVENANCE.md` §4. The book's index (converted-PDF pages 208–214) fails identically.

Applied throughout:

- Every citation reads **`converted-PDF page N`**, in exactly that phrasing.
- `provenance.page_start` and `provenance.page_end` are `null` in all 55 objects, verified in code.
- The **case title is the primary locator**; the converted page is secondary. These are the source's
  own headings and they are stable.
- **No cross-reference in the book's text was resolved.** Where an item needs to point at another
  case it points at the title, because the book's title-level references are correct even though
  its page-level ones are not. MID-AIR's reference to the framing case called *Just* is right; only
  the numbers are broken. That asymmetry is itself worth recording: in a converted ebook, an
  author's semantic cross-references survive and their numeric ones do not.

**Where page numbers appear as digits in this directory:** only inside the `PROVENANCE.md` table
that quotes the book's own broken references as evidence, clearly marked "The text says". Those are
quotations of a defect, not locators. A mechanical scan of all seven files found zero locator
violations outside that table.

---

## 3. `figure_semantic_binding_lost` — severe, and worse than an ordinary book

Two things make this the sharpest case of visual loss in the batch.

**The author says the words are insufficient.** His introduction states the premise as *"Words to a
necessary minimum, with visuals carrying the story"*, and says that explaining a point about
composition or colour would often have been simpler by bypassing words entirely. In Parts 4–10 he
says it about a specific case: of TILT he writes that it *"becomes difficult to describe in words,
so I'll let the illustrations tell the story."* That sentence is recorded as its own object
(`sk_pex_0035`) because it documents the hazard from inside the source.

**The conversion destroyed the designed spread.** Rendering confirms it: a single A4 column of
running text with photographs and analytic diagrams dropped in beneath at unrelated sizes, often
with a third of the page blank. The argument in this book *is* the relationship between diagram,
photograph and caption on a facing spread, and that relationship is gone.

### What rendering actually recovered

Six findings that are in the pictures and not in the prose:

1. **SPOT, converted-PDF page 170.** The greyscale comparison is a genuine counterfactual, and it
   is stronger than the caption. The woman does not weaken — she becomes very hard to find at all
   against the weir. Separately, the middle diagram plots progressively less colourful versions of
   the figure at positions progressively nearer the centre, which draws placement latitude as a
   *function* of chromatic strength. The text states only that red allowed a corner placement. The
   scale reading is recorded as ours in `sk_pex_0046`.
2. **CURVES, converted-PDF page 83.** The second illustration reduces the photograph to four flat
   greys, and only the bull's outline and the horn curves survive. That is the corner-detachment
   claim being made visually. Read as a method it is a test for shape claims; the source never
   proposes it as one, and `sk_pex_0008` is the lane's single `source_interpretation` object.
3. **ACTION COINCIDES, converted-PDF page 191.** The marked vectors do not converge on a point;
   they form a closed loop — statue down to cow, cow up, man up, man down. The caption says only
   "the three coinciding actions added to the eyeline." A circuit is a different structure from a
   convergence, and recorded as our reading in `sk_pex_0042`.
4. **TELEPHOTO COOLNESS, converted-PDF page 139.** The diagram explodes the frame into depth planes
   and is *forced to choose* a depth ordering for the mural and the sandwich stall — the very
   relation the caption calls uncertain. The illustration exposes the flattening by having to
   resolve it.
5. **TILT, converted-PDF page 130.** Three coloured lines, parallel un-tilted and converging at one
   lower-right point when tilted. The Scheimpflug relationship is drawn there and nowhere written.
6. **PATTERN & FIELD, converted-PDF page 92.** The frame is drawn as a bright rectangle inside a
   larger pale continuation of the same cell pattern, which makes the mechanism the viewer's
   extrapolation outward. That implies a converse diagnostic the text does not state.

### How much rests on figures I did not verify — reported honestly

| | count | share |
|---|---|---|
| Objects resting on a figure **rendered and inspected** | 19 | 34.5% |
| Objects marked **`extraction_uncertainty: figure_not_inspected`** | 29 | 52.7% |
| Objects that are text-carried argument with no load-bearing figure | 7 | 12.7% |

**So 29 of 55 objects — just over half — cite figures I did not look at.** Every one of them is
marked `figure_not_inspected` and every one of them is written from the running text and captions
alone. **No visual claim in this lane is reconstructed from text.** Where a figure would have been
needed to make a claim, either the page was rendered or the claim was not made.

Given the author's declared method, the honest summary is that **roughly half this extraction is
known to be partial and says so in the object.**

---

## 4. Other hazards

### 4.1 `caption_coverage_uneven`

Confirmed and severe in this span. Case pages carry 142–275 words. The pages immediately following
them carry 4–71 and are almost entirely image. Five pages in the span — converted-PDF pages 78,
112, 127, 137 and 185 — carry a single token, the folio, and nothing else.

**A sparse page was never treated as containing an argument it does not.** Where a following page
carries a real claim it is a caption, and captions are quoted as captions. The alternative failure —
reading a 22-word caption as a case-level principle — was avoided by always going back to the case
page for the claim and using the caption only for the specific detail it states.

Text density is a poor proxy for content here: the book puts its argument on the pages with almost
no text on them.

### 4.2 Text integrity — clean, one real defect

14,177 words across converted-PDF pages 71–207. Twenty-two tokens mix letters and digits and
twenty-one are legitimate — focal lengths, `4x5-inch`, `ƒ/32`, `SR-71`. The twenty-second,
`tw0-dimensional` on converted-PDF page 189, is a **typesetting error in the source itself**, not
conversion damage: it renders that way on the page. No column interleaving, no OCR degradation.
`extraction_uncertainty: ocr_degraded` is used nowhere in this lane.

Drop capitals are split from their words in the extracted text (`N` / `ot to be confused`). This
caused one false negative in the phrase spot-check and is a text-extraction artefact, not a defect.

### 4.3 Physical-production advice was not translated

Most of this book is about what a person does with a camera before the exposure. That block is
bound exactly once, in `bnd_pex_010`, as `target_type: production` with
`status: production_candidate` and `target_path: null`, and it is **explicitly not rewritten as
generative control**. Fourteen remedy terms whose only route is a person operating a camera carry
`executable_by: [physical_production]`. Nothing in this lane is evidence about what any generative
system can do.

Three remedies carry a different value honestly: `crop_tightly_to_exclude_what_competes`,
`process_for_contrast_rather_than_balance_the_tones` and `turn_the_vignetting_correction_off` are
`human_edit`; `convert_to_greyscale_to_test_whether_the_colour_is_load_bearing` and
`reduce_the_frame_to_flat_tonal_masses` are `deterministic_composite`, because they are mechanical
transforms used as checks.

### 4.4 Practitioner assertion dominates — the count

`empirical_within_source` appears **zero times** in this lane, and that is the correct number.

| characteristic | count (of 55) |
|---|---|
| `practitioner_assertion` | 54 |
| `explicitly_stated` | 54 |
| `visually_demonstrated` | 44 |
| `mechanism_given` | 36 |
| `argued` | 31 |
| `mechanism_absent` | 18 |
| `controlled_comparison` | 8 |
| `historical_claim` | 7 |
| `culturally_bounded` | 5 |
| `repeated_within_source` | 4 |
| `anecdotal` | 4 |
| `outcome_claimed` | 1 |
| `empirical_within_source` | **0** |

Mechanism is stated by the source in 36 of 55 objects; 18 carry `mechanism_absent`. Source
uncertainty: 46 `none`, 5 `source_concedes_difficulty`, 3 `source_hedges`, 1
`source_asks_open_question`.

The eight `controlled_comparison` marks are generous and are qualified in the objects. They are the
source's own before/after pairs, and several are not controlled at all — the rhythm comparison is
two photographs taken on different mornings in different weather, and the freezing comparison is
one frame with an element digitally removed rather than a second exposure.

---

## 5. What was deliberately not extracted

**Part 10 is the one part not fully mined, and deliberately.** Four of its seven cases spend most of
their words on Photoshop layer operations — Multiply and Lighten blend modes, eraser-brush
blending, cloning, exploded layer stacks, focus stacking. Those are software procedure and were
refused. What was taken is the transferable material: what holds a collage together, the declared-
versus-undeclared position, the mountain-water vertical form, the set-level argument for treatment
variety, and the overlap precondition for merging a sequence into one frame. Part 10 yielded
2 objects against 16 for Part 4.

Also refused across the span:

- **Camera-settings recipes with no stated reason.** ƒ-stops and shutter speeds were kept only where
  Freeman argues for them and names what they cost — ƒ/32 in HORIZONTAL LINES and in STACKING, both
  of which he pays for.
- **Gear notes** — the "across-the-street" 180mm lens, the Panavision body, the ILM shoot's kit.
- **Pure image description and travel anecdote** — the Stonehenge overflight permission, the Dinka's
  attachment to their cattle, the Burmese festival calendar, the Millennium Bridge's nickname.
- **The index** (converted-PDF pages 208–214), which is apparatus and whose page numbers are
  unusable in this copy.

### Where I was tempted to over-claim and did not

1. **The colour-contrast afterimage.** CONTRAST invites the reader to stare at orange against white
   and then look at the white to see blue, and Freeman offers this as showing the claim is "not just
   a matter of opinion." It is the one place in the span that looks like evidence. It is an
   invitation to a perceptual demonstration, not data collected within the source, so
   `empirical_within_source` was **not** used. `argued` and `mechanism_given` were.
2. **The spot-colour latitude scale.** The diagram plots placement against chromatic strength and it
   would have been easy to write "Freeman says placement latitude scales with hue strength." He does
   not. He says red allowed a corner placement. The scale is recorded as an extractor observation
   inside a caveat.
3. **The tonal-reduction test.** Reading Freeman's illustration technique as a diagnostic is
   genuinely useful and genuinely not his. It is the lane's only `source_interpretation` object,
   with a non-null `interpretation_basis` that says so, and the Q&A item built on it
   (`qa_pex_0030`) states in the answer that attributing the test to him would be wrong.
4. **The closed-circuit reading of ACTION COINCIDES.** The loop is visible in the rendered diagram.
   The caption is not making that claim, so it is a caveat, not the claim.
5. **The depth-cue system.** `scs_pex_005` groups six claims from four different parts into an
   account of how a flat frame reads as three-dimensional, and it surfaces a real conflict — aerial
   perspective supplies distance in DISTANT and removes description in STACKING. **The source has no
   chapter on depth, never groups these, and never notices the conflict.** The system's
   `system_level_uncertainty` says the structure is ours in full.
6. **The silhouette's general principle.** "Sometimes you need to hold things back from the viewer"
   is broader than the one case offered for it. A caveat says so rather than letting the principle
   stand on the evidence given.
7. **Freeman's taxonomy admission.** He says once, about one case, that he could have put it in
   another chapter. Generalising that to all ten parts is our extrapolation and `bnd_pex_012` says
   so, even though the straddling cases support it.

---

## 6. Self-check results

All run in code.

### 6.1 Every YAML parses

`source-knowledge.yaml`, `source-concept-systems.yaml`, `operational-bindings.yaml`,
`ontology-mappings.yaml`, `qa-bank.yaml` — all parse under `yaml.safe_load`. **Pass.**

### 6.2 No locator presents a converter page as an authored page — the exhaustive check

Scanned all seven files with two patterns: `(printed )?pp?\. \d+`, and `page[s] \d+` not preceded by
`converted-PDF`.

- **YAML files: 0 violations.**
- `PROVENANCE.md`: 9 hits, **all of them inside the table quoting the book's own broken
  cross-references as evidence**, marked "The text says". Deliberate; they are quotations of a
  defect, not locators.

`provenance.page_start` and `provenance.page_end` are `null` in **55 of 55** objects and in all 5
concept systems. **Pass.**

### 6.3 Cited case/page supports the answer — spot-check

**40 Q&A items spot-checked** (69% of the bank), against 47 verbatim phrases pulled from the
answers and matched against the actual text of the cited converted-PDF pages.

- **46 of 47 phrases found. 1 apparent failure, investigated and dismissed:** `qa_pex_0002`'s "not
  to be confused with close-up" is present on converted-PDF page 110 but split by a drop capital in
  the extracted text (`N` / `ot to be confused…`). Text-extraction artefact, not a citation error.
- **Every cited converted-PDF page also appears in that item's `source_locator` or `support`.**
- **0 corrections were required.** No item was rewritten as a result of this check.

### 6.4 No Parts 1–3 duplication

Diffed all 55 concept labels in this lane against the 34 in the live
`freeman-photographers-eye-graphic-guide/source-knowledge.yaml`, by exact match, by token Jaccard
and by sequence ratio.

- **0 exact collisions.**
- 4 lexical candidates above threshold, **all rejected on inspection as coincidences of function
  words** (`is_not_the_same_as`, `direction`, `eye`) with no conceptual overlap. Example:
  `showing_distance_is_not_the_same_as_being_far_away` against
  `a_vertical_frame_is_not_the_same_as_a_sense_of_tallness`.

Four **substantive** near-duplicates that a token diff would not catch were checked by hand and
**kept, with reasons**:

| This lane | Live Parts 1–3 | Kept because |
|---|---|---|
| `sk_pex_0005` diagonals are a camera product, energy from counter-diagonals | `diagonals_divide_cleanly_only_against_strict_horizontals_and_verticals` | The live claim is about diagonals as **dividers** needing an orthogonal reference. This one is about diagonals being **created by camera rotation**, and about opposition between two diagonal sets. Different mechanism, different part. |
| `sk_pex_0042` gaze and gesture vectors recruit attention | `eyes_attract_attention_more_strongly_than_any_other_subject` | The live claim is about **salience** — eyes as the most attention-getting subject. This one is about **direction** — a gaze as a vector the viewer follows. Recorded as `related_to` in the ontology, explicitly as one author's vocabulary across his own chapters. |
| `sk_pex_0048` near-far requires a compared relationship | `a_figure_supplies_scale_but_only_above_a_size_that_depends_on_the_print` | Both put a small near element against a large setting. The live one is about whether a scale reference **registers at all**; this one requires both elements sharp and demands they **compare**. Recorded as `distinct_from`. |
| `sk_pex_0053` a squared-up tableau imports an association | `the_square_frame_reads_as_strict_and_formal` | The live claim is about the **square format's** character. This one is about a **frontal arrangement importing a specific cultural reference** the photographer did not intend. |

Three of these four are recorded as explicit `distinct_from` / `related_to` relationships in
`ontology-mappings.yaml`, so the negative findings survive as data rather than only as prose.

### 6.5 Application fraction — computed in code

```
items 58 · requires_application: true → 25 · fraction 0.431
```

**43.1%, against a floor of 33.3%. Pass.**

Answer-type mix: mechanism 11 · application 11 · source_position 10 · comparison 6 ·
boundary_condition 6 · concept_definition 4 · tradeoff 3 · repair 3 · factual 2 ·
failure_diagnosis 2. Difficulty: 40 medium, 13 hard, 5 easy.

`source_position` is over-represented against the contract's suggested mix (10 of 58 rather than a
handful), and that is deliberate: an unusual amount of this span is Freeman stating a position
rather than a fact — that four-square objectivity is a delusion, that muted and drab differ only in
the viewer's mood, that juxtaposition being open to abuse is good, that he will not settle the
manipulation debate. Those items are typed honestly rather than dressed as mechanisms.

### 6.6 Structural checks

- All 55 `sk_id` unique; all **121** `intra_source_relations` targets resolve inside the lane.
- All 5 concept systems: every `sk_ref` resolves; both `extractor_synthesis` whole-system claims
  carry non-null `interpretation_basis`; all five carry a `system_level_uncertainty` statement.
- All 12 bindings: refs resolve; every `evaluation` binding has an `observation_unit`; the single
  `production` binding has `status: production_candidate` and `target_path: null`; both `governance`
  bindings use a permitted `governance_consumer`; **no `creative_ir` binding exists**; **no
  `cross_source_supported` or `empirically_supported` evidence basis anywhere**.
- Ontology: 70 terms, 16 relationships, 6 concepts. Every `remedy` term carries `executable_by`.
  Every concept's `children_terms` resolve. **No `xs_` concept created. `same_failure_family` not
  used.** Four relationships point at live Parts 1–3 term ids and are labelled in their notes as
  the same book, observation only, no promotion.
- All 58 Q&A items carry all twelve required fields, a controlled `answer_type`, `difficulty` and
  `knowledge_type`, a boolean `requires_application`, and a non-empty `confounders` list.
- The lane's shared `validate_experimental.py` was run over the whole run and reports **zero errors
  for this directory**, with `SourceKnowledge 55 · ConceptSystems 5 · Bindings 12 · Terms 70 ·
  Q&A 58 · requires_application 25 (43.1%)`. The errors it does report all belong to other lanes'
  directories and nothing outside this directory was touched.

---

## 7. What the source is best at, and where the value sits

Freeman is at his strongest exactly where the brief predicted — boundary conditions and interactions
— and this span contains several that would be worth having even without the rest:

- **A rule and its stated exception, one case apart.** MOVING IN gives a placement rule with a
  perceptual reason; MOVING OUT reverses it and names the condition (a scene-level direction that
  the departing figure completes). MOMENT then overrides both where the setting is strongly graphic.
  Three cases, one quantity.
- **Sharpness as a distribution, not a quantity.** He argues for ƒ/32 in one case and refuses a
  smaller aperture in another because it would spoil the merged overlaps — and there is no
  contradiction once you see that the question is always *where* the viewer is permitted to see
  clearly.
- **Depth produced by deleting information.** STACKING needs haze to remove the modelling inside
  each land form so that each reads as a flat cut-out. That is the opposite of the usual account,
  and it sits in the same book as DISTANT, where haze supplies distance. He does not notice.
- **A named quality with no image-side definition.** Muted versus drab is settled by the viewer's
  mood, not by the picture. He says it plainly, and it undercuts the coordinate system he spent the
  chapter building.
- **The look of objectivity as a compositional effect.** Four-square looks unmediated, which is why
  it became the documentary default, and Freeman calls believing it therefore *is* unmediated a
  delusion.
- **An association you cannot switch off.** A squared-up long table evokes the Last Supper whether or
  not the photographer intends it — meaning arriving from outside the frame.

The one genuinely portable diagnostic in the span is the greyscale test in SPOT, and it is bound as
`bnd_pex_001`.
