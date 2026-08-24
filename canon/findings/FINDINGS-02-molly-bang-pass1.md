# Finding 02 — Molly Bang, "The Principles" (pp. 42–91), Pass 1

**Date:** 23 Aug 2026 · **Cost:** ~₹0 (text extraction only) · **Schema:** SPEC-02 v0
**Scope:** one chapter. Not the book.

---

## Headline counts

```
60  candidate ideas identified
──
 2  operational
16  pending_vocabulary        ← own atom, blocked only on vocabulary
18  folded into a parent atom ← same idea, recorded as mechanism or exception
24  human_notes
──
18  distinct atoms written
```

**18 atoms from 60 candidates (30%).** That is neither the shoehorn failure (34→33) nor the
majority-notes outcome predicted before the run.

---

## Finding 1 — On book one, `pending_vocabulary` is the default, not the exception

Only **two** atoms reached `operational` (mb_004 size-as-strength, mb_005 contrast-enables-
perception). Both did so purely because they happened to use the three failure/repair terms
already registered in SPEC-02's worked example.

Every other qualifying atom is `pending_vocabulary` — not because the knowledge is weak, but
because the registry is empty and rule 3 requires registered terms.

**This is structural, not a result.** The distribution you sketched (8 operational / 6 pending /
20 notes) is unreachable on the first book by construction: the first source has to bootstrap
the vocabulary it is then validated against.

**Recommendation:** add an explicit registry-seeding step between Pass 1 and Pass 2. Pass 1
proposes terms, a human promotes them, and the atoms are re-validated. Without it, "operational"
just measures how early a book was processed.

## Finding 2 — Coverage is extremely narrow, and that is useful

Where the 18 atoms landed:

| IR path | Atoms |
|---|---|
| `static.composition` | 9 |
| `creative.visual_language` | 8 |
| `creative.hierarchy` | 7 |
| `static.spatial_hierarchy` | 1 |
| `relationships` | 2 |
| `message.emotional_target` | 1 |
| `entities.role` | 1 |

**Zero** atoms landed on `intent`, `audience`, `copy`, `brand`, `delivery`, `assets`,
`entities.invariants`, or **any field in the video extension.**

Molly Bang informs three field groups out of roughly twenty. That is not a deficiency in the
book — it is a precise statement of what this book is for, and it should drive the choice of
book two. `Grammar of the Shot` / `In the Blink of an Eye` for the video extension, `Ogilvy` /
`Hopkins` for `intent`, `Thinking with Type` for `copy` and `typography_layout`.

## Finding 3 — The most important idea in the chapter informs nothing

Bang states twice (pp. 58, 60) that the principles are never used one at a time, always operate
in combination, and are **subservient to context and content**. She then demonstrates it: one
composition reads as a general surveying territory, a triumphant climber, or a suicide,
depending on content alone.

This has no `informs` path. It is not a fact about pictures — it is a rule about how a Canon
may be applied. Under SPEC-02 it becomes `human_notes`, which is mechanically correct and
feels wrong.

It is also direct source support for the `exceptions_status` discipline and for advisories
never overriding user intent. **Open question:** does the Canon need a `governance` class for
knowledge that constrains the Canon's own use?

## Finding 4 — Group B may be one atom, not six

mb_007 to mb_012 all have the form *form X produces feeling Y* — horizontal/calm,
vertical/energy, diagonal/tension, upper-lower/register, point-curve/safety, light-dark/safety.
Same `informs`, same role, same diagnostic, same proposed failure mode.

Arguments for six: each has different exceptions, different repairs, and independent confidence.
Arguments for one: retrieval will always want them together, and six near-identical atoms is
how a Canon becomes bloated at book forty.

**Recommendation:** keep six for now, revisit after Robin Williams. If that book produces
another dozen of the same shape, the case for a table-valued atom becomes strong.

## Finding 5 — I have not seen the figures

`visual_context_required: true` on **15 of 18** atoms. This pass read the OCR text layer only.
For a book that argues through cut-paper images, that is a material limitation: the atoms are
derived from Bang's prose *about* her pictures, not from the pictures.

`source_support: text_and_visual` is therefore currently an assertion about where the argument
lives, not a record of what was inspected. A vision pass over the referenced figures could
revise confidence, add atoms, or contradict some. It is cheap and it should happen before these
atoms are trusted.

---

## Full candidate ledger

Every idea found in the chapter, including discarded. `HN` = human_notes, `PV` = pending_vocabulary, `OP` = operational.

| # | p | Idea | Status | informs |
|---|---|---|---|---|
| 1 | 42 | Horizontal shapes → stability and calm | PV | visual_language, composition |
| 2 | 42 | Small horizontal shapes = local islands of calm | PV | (folded into mb_007) |
| 3 | 44 | Vertical shapes → excitement, energy, aspiration | PV | visual_language, composition |
| 4 | 45 | Horizontal capping verticals restores stability | PV | (folded into mb_008) |
| 5 | 46 | Diagonals → motion or tension | PV | visual_language, composition |
| 6 | 46 | Diagonals create depth, lead eye into frame | PV | (folded into mb_009) |
| 7 | 47 | Diagonal strut stabilises vertical + horizontal | PV | (exception in mb_009) |
| 8 | 48 | Flying buttress as tension example | HN | — |
| 9 | 49 | Diagonals read left to right | HN | — culturally contingent, source does not qualify it |
| 10 | 49 | Mountains/waves/slides as diagonals in tension | HN | — illustration |
| 11 | 50 | Triangle on flat base = stable | HN | — demonstration of mb_007 |
| 12 | 51 | Same triangle on diagonal = movement | HN | — demonstration of mb_009 |
| 13 | 51 | No baseline → floating | HN | — candidate; no IR field for groundedness |
| 14 | 52 | Progressive size decrease along diagonal increases motion | HN | — subsumed by mb_015 |
| 15 | 52 | Same-size parallel repetition reads boring and heavy | HN | — no field; see Finding 3 |
| 16 | 52 | Art-history anecdote, "dynamic of the diagonal" | HN | — |
| 17 | 54 | Invisible emotional horizon divides frame | PV | (mechanism for mb_010) |
| 18 | 54 | Upper half → freedom, happiness, triumph, spiritual | PV | visual_language, composition |
| 19 | 56 | Lower half → heavier, sadder, constrained, grounded | PV | (folded into mb_010) |
| 20 | 56 | **Higher placement = greater pictorial weight** | PV | hierarchy, spatial_hierarchy |
| 21 | 54–56 | Verbal idiom evidence ("top dog", "down in the dumps") | HN | — supporting evidence |
| 22 | 58 | **Principles combine; subservient to context and content** | HN | — see Finding 3 |
| 23 | 58–60 | Same composition reads three ways by content alone | HN | — demonstration of #22 |
| 24 | 60 | Circular frames read as floating | HN | — no aspect-ratio field consumes it |
| 25 | 62 | Frame creates a picture-world; edges radiate inward | PV | (mechanism for mb_002) |
| 26 | 62 | **Centre = strongest attractor** | PV | hierarchy, composition |
| 27 | 62 | **Keep emphasis off-centre if picture is to be explored** | PV | composition, hierarchy |
| 28 | 62 | Square/round frames intensify centre lock | PV | (exception in mb_002) |
| 29 | 64 | Off-centre focus makes the picture dynamic | PV | (folded into mb_003) |
| 30 | 64 | White area running to edge implies space beyond | PV | (folded into mb_018) |
| 31 | 66 | **Proximity to edge or centre raises tension** | PV | composition, visual_language |
| 32 | 66 | Edge/corner verbal idioms ("cornered", "on edge") | HN | — supporting evidence |
| 33 | 66 | Golf-ball-near-hole analogy | HN | — |
| 34 | 67 | Centre reserved for objects of meditation | PV | (exception in mb_003) |
| 35 | 67 | Viewers grant living elements wills of their own | HN | — no consumer |
| 36 | 68 | Light ground = day, dark ground = night/storm | PV | (folded into mb_012) |
| 37 | 68 | **Light grounds feel safer than dark** | PV | visual_language |
| 38 | 68 | Exceptions: cover of darkness; limitless ice | PV | (exception in mb_012) |
| 39 | 69 | Black and white both signify death; culturally inverted | PV | (exception in mb_014) |
| 40 | 69 | **Bright colour glows on dark, washes out on light** | PV | hierarchy, visual_language, composition |
| 41 | 70 | **Points → fear; curves → security** | PV | visual_language |
| 42 | 72 | **Larger = stronger; small = vulnerable** | **OP** | hierarchy, entities.role |
| 43 | 73 | Association is the mechanism behind all of it | HN | — meta-mechanism, no consumer |
| 44 | 73 | Viewers suspend disbelief; the picture becomes "real" | HN | — |
| 45 | 74 | **Colour affects viewers more than other elements** | PV | visual_language, emotional_target |
| 46 | 74 | Colour meanings borrow from "natural constants" | PV | (folded into mb_014) |
| 47 | 74 | Secondary colour associations are false but universal | PV | (folded into mb_014) |
| 48 | 74 | Colour symbolism is used in advertising and propaganda | HN | — source's own aside; Pass 2 territory |
| 49 | 76 | **Colour grouping beats shape grouping** | PV | hierarchy, composition, relationships |
| 50 | 76 | Young children group by shape instead | PV | (exception in mb_013) |
| 51 | 78 | Repetition/confusion — source declines to call it a principle | HN | — explicitly unnamed by author |
| 52 | 78 | Perfect regularity more horrifying than chaos | HN | — |
| 53 | 80 | **Contrast enables perception** | **OP** | hierarchy, composition |
| 54 | 84 | **Surrounding space isolates and elevates a figure** | PV | composition, hierarchy |
| 55 | 85 | Movement set as much by gaps as by shapes | HN | — subsumed by mb_017 |
| 56 | 86 | **Overlap takes space and binds two into one unit** | PV | composition, relationships |
| 57 | 87 | **Depth via size + base height + geometric spacing** | PV | composition |
| 58 | 88–89 | Space implies time; distance between threat and victim | HN | — narrative, no static field |
| 59 | 90 | Both wide space and slivers create tension | HN | — subsumed by mb_018 |
| 60 | 91 | Sue Jensen illustration analysis | PV | (evidence for mb_006, mb_013) |

Rows folded into a parent atom are counted once in the headline totals.

---

## Proposed vocabulary

Every new term, with the atom proposing it. None are registered yet.

**Failure modes**

| Term | Proposed by |
|---|---|
| `unintended_centre_lock` | mb_002, mb_003 |
| `unintended_emotional_register` | mb_007–mb_012, mb_014, mb_018 |
| `salience_lost_to_background` | mb_005, mb_006 |
| `false_grouping_by_colour` | mb_013 |
| `flat_depth` | mb_015 |

**Repairs**

| Term | Proposed by |
|---|---|
| `alter_vertical_placement` | mb_001, mb_010 |
| `move_off_centre` | mb_002, mb_003 |
| `alter_structural_direction` | mb_007, mb_008, mb_009 |
| `alter_shape_language` | mb_011 |
| `alter_background_value` | mb_006, mb_012 |
| `break_colour_association` | mb_013 |
| `alter_size_progression` | mb_015 |
| `introduce_overlap` / `remove_overlap` | mb_016 |
| `increase_surrounding_space` | mb_017 |

9 failure/repair terms proposed against 5 registered. **Registry seeding is now the blocking step.**

---

## Where the extractor was uncertain

1. **Figures unseen** (Finding 5). 15 of 18 atoms claim `source_support: text_and_visual` on the
   basis of what the prose says about the images, not inspection of them.
2. **Group B granularity** (Finding 4) — six atoms or one.
3. **Space-section confidence.** mb_015 to mb_017 come from a section the author explicitly says
   is *not* principles. Recorded as `supported_extrapolation` at 0.75 rather than `established`.
   That may be too generous or too harsh; it is a judgment call with no source basis.
4. **`message.emotional_target` as an `informs` target.** mb_014 claims it. Arguably the Canon
   informs the *translation* from emotional_target into visual_language, and never writes
   emotional_target itself — which the user or the brief supplies. If that reading is right,
   mb_014's path list is wrong.
5. **Item 9 (diagonals read left to right)** discarded as culturally contingent. The source
   states it without qualification. Discarding it is the extractor overriding the source —
   flagged rather than done silently.
6. **Item 13 (no baseline → floating)** has no IR field, but "does the subject read as grounded"
   is a plausible missing field. Possible IR gap rather than a discard.

---

## Next

1. **Registry seeding pass** — promote or reject the 14 proposed terms. Blocking for everything else.
2. **Vision pass** over the 15 figure-dependent atoms. Cheap; should happen before these are trusted.
3. **Then Pass 2** — implications for generated media, from approved atoms only, never from the chapter.
