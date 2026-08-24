# Finding 09 — Aggregate report across six source probes

**Date:** 23 Aug 2026 · **Mode:** unattended exploration. Schemas frozen. Nothing promoted, nothing merged.

## What was run

| Source | Section | Format | Atoms | Operational | Human notes |
|---|---|---|---:|---:|---:|
| Molly Bang, *Picture This* | Principles, pp.42–91 | PDF + 21 rendered figures | 18 | 2 | 0 |
| Robin Williams, *Non-Designer's Design Book* | ch.2 Proximity | PDF | 9 | 0 | 5 |
| Ellen Lupton, *Thinking with Type* | TEXT / Hierarchy | EPUB | 9 | 3 | 2 |
| Thompson & Bowen, *Grammar of the Shot* | ch.4 Continuity | PDF | 10 | 2 | 3 |
| David Ogilvy, *Ogilvy on Advertising* | ch.2 | EPUB | 9 | 1 | 5 |
| Hunter et al., *Light: Science & Magic* | ch.3 Reflection | EPUB | 6 | 1 | 4 |
| **Total** | | | **61** | **9** | **19** |

Each Pass 1 was run in isolation. No source's atoms or vocabulary were visible while extracting
another. Pass 2 was not run for any source.

---

## 1. Headline — zero vocabulary convergence

**42 distinct failure terms. 47 distinct repair terms. Not one term appears in two sources.**

Six sources describing overlapping phenomena produced entirely disjoint vocabularies. This is the
single most important result of the batch, and it settles the question that prompted it: locking
Molly Bang's fourteen terms as the registry would have forced five later sources to either distort
their concepts into her language or fail validation.

It also means the near-synonym problem is **worse than a tidiness issue**. Without a registry,
`no_clear_entry_point`, `no_scan_entry_point` and `competing_focal_points` are three unrelated
strings. Failure counts would never aggregate; repair success rates would never be computable; a
customer failure would never match a Canon prediction.

---

## 2. Suspected near-synonym clusters — NOT merged

Presented as evidence for a human decision. No term has been altered, dropped or unified.

### Cluster A — entry point / focal dominance (3 sources, 6 terms)
```
williams  no_clear_entry_point · competing_entry_points
lupton    no_scan_entry_point
molly     competing_focal_points · wrong_element_dominates · unintended_centre_lock
```
All concern where attention lands first and whether that is contested or correct. Likely one
concept with two states (absent / contested) plus a correctness axis.

### Cluster B — false grouping (3 sources, 4 terms)
```
molly     false_grouping_by_colour
williams  false_grouping_by_proximity · ambiguous_element_association
gos       contradictory_sight_lines
```
Identical failure — *the viewer infers a relationship that was not intended* — differing only in
which cue produced it: colour, proximity, spacing, gaze. **This cluster suggests one parameterised
term rather than four separate ones**, e.g. a single failure with a `cue` field. Worth deciding
before the registry is seeded, because the same choice recurs across the whole taxonomy.

### Cluster C — too many competing signals (3 sources, 3 terms, 3 domains)
```
lupton    signal_overload            (typographic cues on one level)
williams  excessive_separate_elements (ungrouped elements on a page)
ogilvy    objective_overload          (objectives in a brief)
```
The same shape at three different altitudes. Whether these are one concept or three is a genuine
judgment call, not a naming accident.

### Cluster D — things that should match, don't (4 sources, 4 terms)
```
lupton    inconsistent_level_cueing
gos       mismatched_reciprocal_framing
ogilvy    inconsistent_brand_image
lsm       inconsistent_lighting_evidence
```
Consistency failures across four unrelated domains. Note `lsm_005` is an *internal* consistency
check — hard shadows and a pinpoint highlight contradict each other within one image — while
`inconsistent_brand_image` spans assets and months. Possibly the same concept at different scopes.

### Cluster E — repair verb families
```
reduce count:   reduce_element_count · reduce_cue_count · reduce_to_single_signal · reduce_to_single_objective   (4 sources)
adjust spacing: increase_space_between_groups · reduce_space_within_group · increase_surrounding_space
adjust scale:   alter_relative_scale · alter_contrast · strengthen_level_contrast
adjust position:alter_position · alter_vertical_placement · move_off_centre · remove_corner_filling
regroup:        group_related_elements · separate_unrelated_elements · break_colour_association
```

### Collision risk, not synonymy
`molly: flat_depth` and `lsm: glossy_surface_reads_flat` share a word and mean different things
(absent depth cues vs. a material failing to read as glossy). Flagged so they are not merged by
string similarity.

---

## 3. Naming conventions diverge

```
molly     alter_X, break_X, introduce_X, move_X      — verb-first, imperative
williams  group_X, separate_X, remove_X, convert_X   — verb-first, object-second
lupton    normalise_X, reduce_X, align_X             — verb-first
gos       restore_X, match_X, add_X, reframe_X       — verb-first, but domain nouns
ogilvy    state_X, ground_X, promote_X, restate_X    — verb-first, abstract objects
```
Failure terms are less consistent: some are noun phrases (`trapped_white_space`, `jump_cut`),
some are sentences (`glossy_surface_reads_flat`, `advertiser_vocabulary_not_audience_vocabulary`).
**A naming convention should be decided before the registry is seeded**, or the first fifty terms
will set an inconsistent precedent for the next five hundred.

---

## 4. IR-field coverage

| Field | Atoms | Sources |
|---|---:|---|
| `static.composition` | 19 | molly, williams, gos |
| `creative.hierarchy` | 17 | molly, williams, lupton, ogilvy |
| `creative.visual_language` | 17 | molly, williams, ogilvy, lsm |
| `static.typography_layout` | 10 | williams, lupton |
| `video.continuity_requirements` | 9 | gos |
| `entities` | 6 | ogilvy, lsm |
| `video.temporal_structure` | 5 | gos |
| `message.proposition` | 5 | ogilvy |
| `relationships` | 4 | molly, gos |
| `intent.objective` | 3 | ogilvy |
| `creative.concept` | 2 | williams, ogilvy |
| `audience.who` | 2 | ogilvy |
| `static.spatial_hierarchy`, `entities.role`, `message.emotional_target`, `copy.headline`, `copy.body`, `video.temporal_hierarchy`, `message.support`, `audience.context`, `brand.palette`, `brand.type` | 1 each | — |

### Fields never touched by any of six sources

```
intent.desired_action        intent.success_criteria
audience.language            message (beyond proposition/support/emotional_target)
entities.invariants          entities.allowed_variation   (implied by lsm_004, never named)
creative.hook
copy.cta                     copy.script_system
brand.logo                   brand.mandatories            brand.prohibitions
delivery.platform            delivery.aspect_ratios       delivery.duration    delivery.resolution
acceptance.*                 (entire section)
video.dialogue_intent
```

### The structural observation this produces

`delivery` and `acceptance` received **nothing**, and probably never will from books. Delivery
specs come from the customer and the platform. Acceptance criteria are generated from the
completed spec. Brand mandatories and prohibitions come from the customer's brand policy. These
fields are not gaps in the Canon — **they are fields the Canon is not the source for.**

That divides the IR into two territories, which is worth naming before more books are processed:
fields that book knowledge fills, and fields that only the customer, the platform, or Empirical
Memory can fill. `creative.hook` receiving zero — including from Ogilvy — is the one genuine
surprise and may indicate a concept that postdates these sources.

---

## 5. Granularity is not consistent

```
molly     18 atoms · 0 human_notes   ← see §6
lsm        6 atoms · 4 human_notes   ← densest chapter, fewest atoms
ogilvy     9 atoms · 5 human_notes
```

Molly's atoms are fine-grained — roughly one per numbered principle. Ogilvy's are coarse —
roughly one per section heading. Lupton's sit between. No convention was applied because none
exists yet, and the six probes do not resolve it. What they do show is that **granularity
currently tracks how the source is organised**, not any decision of ours.

---

## 6. Molly Bang produced zero human_notes — the shoehorn signal

Every other source produced between two and five rejected candidates. **Molly Bang produced none:
18 candidates, 18 atoms, nothing held out.**

That is close to the `34 ideas → 33 operational` pattern flagged in SPEC-02 as the result that
should worry us. It was invisible until five later probes established a baseline of 2–5 rejects
each. It does not prove the extraction was wrong — a book of numbered principles about picture
construction may genuinely be almost entirely operational for this product — but it is the single
most likely place in this batch for over-fitting to have occurred, and the visual pass already
weakened two of those atoms on inspection.

**Recommendation for review: re-examine the Molly Bang extraction for candidates that should have
been human_notes**, now that there is a baseline to compare against.

---

## 7. A defect in SPEC-02's promotion rule

Nine atoms reached `operational`. They did so because they proposed **no new vocabulary** — not
because their knowledge was better.

The clearest case: `og_009` (Ogilvy's five-question big-idea test) is `operational` despite being
`evidence_class: hypothesis`, confidence 0.55, mechanism not stated, and the source itself
conceding the judgment is "horribly difficult." Meanwhile `og_001` (positioning, `established`,
0.85) and `lsm_001` (surface identity, `established`, 0.95) sit at `pending_vocabulary` because
each proposed a single term.

**Status currently measures vocabulary novelty and is being read as a quality gate.** SPEC-02
rule 3 was written to protect the taxonomy; it is doing something else as a side effect. Not
fixed — schemas frozen.

---

## 8. Evidence quality varies enormously, and nothing consumes it

```
design / craft sources   established        confidence 0.7 – 0.95
Ogilvy                   supported_extrapolation / hypothesis   0.55 – 0.85
```

Ogilvy's support is practitioner assertion, anecdote and uncontrolled sales figures. Four of his
atoms record `mechanism: "Not stated."` The design and photography sources demonstrate mechanisms;
Molly Bang demonstrates hers with controlled minimal pairs.

SPEC-02 records `evidence_class` and `confidence` on every atom. **Nothing in the architecture
reads either field.** Retrieval as specified would hand a 0.55 hypothesis to the planner with
exactly the authority of a demonstrated principle. This is a live gap between the schema and the
runtime that does not yet exist.

---

## 9. Human_notes that may be governance or meta-knowledge

Nineteen human_notes were produced. These are the ones that are not simply out of scope:

**Vocabulary governance — the most useful thing found**
`lsm: source_refuses_an_ambiguous_term`. *Light: Science & Magic* declines to use the word
"specular" anywhere in the book, because practitioners use it to mean at least three different
things and because "specular light" drifted to describe the source rather than the reflection.
Its resolution: **refuse the ambiguous term and name the two concepts separately.** That is
exactly the problem §2 of this report describes, solved and documented by a technical field that
had it first.

**Statements about our own pipeline**
- `williams: group_information_before_designing` — write out what belongs together *before*
  attempting layout. That is producing a specification before execution.
- `ogilvy: committees_cannot_create` — campaigns reflecting many stakeholders' objectives achieve
  nothing; average gestation 117 days. An argument for automating the specification step.

**Production IR candidates, accumulating**
- `williams: reversed_type_needs_a_robust_face` — render-method-dependent constraint
- `gos: shoot_coverage_to_give_the_editor_choices` — generate N variants for a downstream chooser
- `gos: minimise_take_count_for_cost` — cost modelling
- `lsm: the_family_of_angles` — where to place a physical light

That last one is the book's central concept. **Four of six sources produced content that belongs
to an object that does not exist yet.** Production IR is now the most-requested missing piece.

**Possible promotion**
`ogilvy: style_as_added_value_for_parity_products` — where products are undifferentiated, the
style of the advertising *is* the differentiation. Plausibly informs `creative.visual_language`.

---

## 10. Repairs do not transfer from photography

*Light: Science & Magic* proposed **one** repair term against six atoms. Every repair it actually
implies is a physical camera action — enlarge the source, move the light outside the family of
angles, raise the camera, add a polariser.

None is executable against a generative model, where the only repair is to respecify and
regenerate. **Its failure modes transfer; its repairs do not.** The terms were deliberately left
untranslated — converting them is a `generative_media_hypothesis` and belongs to Pass 2.

Expect the same for every technique-heavy source: cinematography, lighting, photography.

---

## 11. Extraction quality by format

| Format | Result |
|---|---|
| PDF, single column (Williams, GoS) | Clean. Before/after pairs and prose survive intact. |
| PDF, image-led (Molly Bang) | Text extracts; **figures required rendering and inspection.** Four atoms revised as a result. |
| EPUB, single column (Ogilvy, LSM) | Clean. |
| EPUB, multi-column print (Lupton) | **Columns interleave sentence-by-sentence.** Every atom required de-interleaving — an inference step. Confidence capped at 0.8; needs checking against the printed page. |

Lupton is the warning case: the extraction looked like prose and was not.

---

## 12. Recommended vocabulary candidates for human review

Not promotions. Ranked by cross-source evidence.

**Strongest — attested from three or more sources under different names**
1. A single **false-grouping** concept, parameterised by cue (colour / proximity / spacing / gaze) — Cluster B
2. A single **entry-point** concept with absent and contested states — Cluster A
3. A **too-many-signals** concept, if the three altitudes in Cluster C are judged to be one thing
4. A **consistency-failure** concept, scoped to within-asset vs across-asset — Cluster D
5. A **reduce-count** repair, parameterised by what is being counted — Cluster E

**Decide before seeding, not after**
6. Naming convention for failure terms (noun phrase vs sentence) and repairs (verb-first confirmed)
7. Whether parameterised terms are permitted at all, or whether every variant gets its own string

**Structural questions this batch raised**
8. Whether `status` should reflect evidence quality rather than vocabulary novelty (§7)
9. Whether retrieval weights by `evidence_class` and `confidence` (§8)
10. Whether the IR should be formally divided into Canon-fillable and non-Canon-fillable fields (§4)

---

## What was deliberately not done

No vocabulary promoted. No terms merged, renamed or deduplicated. No schema edited. No IR fields
added. No Pass 2 or generative-media hypotheses generated. No cross-source synthesis into
canonical concepts. No human_notes item reclassified. No conclusion drawn that the IR is missing
a field.

Every cluster in §2 is presented as evidence, with all original terms intact in their source
files.

## Files

```
canon/molly-bang-principles-atoms.yaml     18 atoms   (4 revised by visual pass)
canon/williams-proximity-atoms.yaml         9 atoms +  5 human_notes
canon/lupton-hierarchy-atoms.yaml           9 atoms +  2 human_notes
canon/gos-continuity-atoms.yaml            10 atoms +  3 human_notes
canon/ogilvy-selling-atoms.yaml             9 atoms +  5 human_notes
canon/lsm-reflection-atoms.yaml             6 atoms +  4 human_notes

FINDINGS-03  Molly Bang visual pass
FINDINGS-04  Williams        FINDINGS-05  Lupton      FINDINGS-06  Grammar of the Shot
FINDINGS-07  Ogilvy          FINDINGS-08  Light: Science & Magic
FINDINGS-09  this report

source/  extracted chapter text for all six · 21 rendered Molly Bang figure pages
```
