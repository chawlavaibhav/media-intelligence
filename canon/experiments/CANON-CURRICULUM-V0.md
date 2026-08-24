# Canon V0 Curriculum

**Date:** 23 Aug 2026 · **Selected from:** [CANON-COVERAGE-MAP-V0](CANON-COVERAGE-MAP-V0.md)
**Not to be started until reviewed.**

**Principle:** breadth across disciplines, not volume. Eleven sources, sections chosen for
coverage, with deliberate overlaps so cross-source synthesis has something to work with.

Six sources have one section processed already (marked ✓). Those sections stay; further sections
are listed where the Coverage Map shows a gap.

---

## The eleven

### Already begun

**1 · Molly Bang, *Picture This*** ✓ *The Principles* (pp.42–91) — done
Adds: visual weight, attention, emotional register of structure, depth, grouping.
Overlaps: Photographer's Eye (composition), Albers (colour).
Does not cover: typography, commercial objective, anything time-based, any non-Latin script.

**2 · Robin Williams, *Non-Designer's Design Book*** ✓ ch.2 Proximity — done
**Add:** ch.5 Contrast, and ch.3 Alignment.
Adds: grouping, spacing as signal, contrast as a design tool, information hierarchy. Authors its
own failure and repair lists, which extract unusually cleanly.
Overlaps: Lupton (typographic hierarchy), Bang (contrast).
Does not cover: colour theory, imagery, anything commercial.

**3 · Ellen Lupton, *Thinking with Type*** ✓ Hierarchy — done
**Add:** *Alignment*, *Line Spacing*, and the GRID part.
Adds: typographic hierarchy, cue economy, layout systems.
⚠ **Extraction hazard.** The EPUB interleaves two print columns. Every claim needs de-interleaving
and the nine existing objects are flagged. **Re-extract from a page-image render instead.**
Does not cover: Devanagari, imagery, motion.

**4 · Thompson & Bowen, *Grammar of the Shot*** ✓ ch.4 Continuity — done
**Add:** ch.1 shot types, ch.2 composition for human subjects, ch.5 dynamic shots.
Adds: shot grammar, framing of people, camera movement, continuity geometry, temporal structure.
Overlaps: Master Shots, Blink.
Does not cover: cut logic, pacing, commercial intent, sound.

**5 · David Ogilvy, *Ogilvy on Advertising*** ✓ ch.2 — done
**Add:** ch.7 print advertising, ch.8 TV commercials.
Adds: objective, positioning, proposition, brand image, product-as-hero, campaign discipline.
Overlaps: Whipple (concepting), Scientific Advertising (response).
Does not cover: modern formats, digital, non-Western markets. **1983 — treat as period evidence.**

**6 · Hunter et al., *Light: Science & Magic*** ✓ ch.3 Reflection — done
**Add:** ch.4 Surface Appearances, ch.5 Revealing Shape and Contour.
Adds: material appearance, reflection families, how surface reads as substance, depth via light.
**The single most relevant source for product photography**, the Coverage Map's weakest critical
static domain.
Does not cover: composition, commercial framing. Most of it is production knowledge and will bind
as production candidates — correctly.

### New for V0

**7 · Josef Albers, *Interaction of Color***
Why: colour is `critical` and only `medium`. Albers is the canonical treatment of colour as
**relational** — a colour's appearance depends entirely on its neighbours.
Adds: colour interaction, simultaneous contrast, value/intensity relationships.
Overlaps: Bang (colour association, value against ground), Light: S&M (surface and light).
Does not cover: colour semantics or cultural meaning — a real gap, and Indian colour codes are
absent from the whole library.
Note: heavily plate-based. Expect `source_support: visual` and require rendered figures.

**8 · Michael Freeman, *The Photographer's Eye***
Why: composition applied to **photographic and commercial framing**, where Bang is illustration.
The cross-source overlap is deliberate — if Bang and Freeman agree on visual weight from different
media, that is our first real `cross_source_concept`.
Adds: framing, balance, dynamic tension, depth cues, subject placement, cropping.
Does not cover: typography, motion, commercial objective.

**9 · Walter Murch, *In the Blink of an Eye***
Why: editing and pacing are `critical` and only `medium`, and *Grammar of the Shot* covers shot
craft rather than **why and when to cut**. Murch's Rule of Six is an explicit weighted priority
order — a `priority_order` SourceConceptSystem, the type we have never yet tested.
Adds: cut logic, pacing, rhythm, emotional continuity, attention across time.
Overlaps: Grammar of the Shot (continuity), Conversations.
Does not cover: commercial format, short-form, sound design in depth.

**10 · Sullivan, *Hey Whipple, Squeeze This***
Why: `hooks & openings` is `critical` and `weak`; concept development is `medium`. Whipple is the
modern working counterweight to Ogilvy — concepting, headlines, what makes an idea rather than a
layout.
Adds: concept generation, hooks, headline craft, distinctiveness, common advertising failures.
Overlaps: Ogilvy (strategy — with a **useful disagreement**, since Whipple is often directly
opposed to Ogilvy's research-led method, which gives the ontology a real `distinct_from` to record).
Does not cover: production craft, non-Western markets.

**11 · Heath & Heath, *Made to Stick***
Why: memorability is high-importance and the SUCCESs framework is unusually operational — six
named attributes with diagnostics, which maps almost directly onto evaluation dimensions.
Adds: memorability, concreteness, unexpectedness, emotional resonance, story.
Overlaps: Contagious (held in reserve), Alchemy, Ogilvy.
Does not cover: visual craft entirely.

---

## What this curriculum deliberately excludes

**Berger, Sontag, Thinking Fast and Slow, Noise, Superforecasting, Creativity Inc, Art & Fear.**
Valuable, but either criticism rather than craft, or aimed at *our own judgement* rather than at
creative output. *Noise* and *Thinking Fast and Slow* belong to evaluator design and should be
processed when the evaluator is built, not now.

**Grid Systems, Making & Breaking the Grid, Vignelli.** Layout is already `strong`; adding them
now buys redundancy rather than breadth.

**Scientific Advertising, My Life in Advertising, 22 Immutable Laws, StoryBrand, This Is
Marketing, Contagious, Alchemy.** Commercial communication is the best-covered area in the
library. Ogilvy plus Whipple plus Made to Stick is enough for V0.

**Everything for the four critical absent domains** — short-form feed grammar, Devanagari
typography, Indian cultural context, modern effectiveness evidence. **No book in the library
supplies these and no book we could buy would fully supply three of them.** They need experts,
platform data and empirical work, and they are the largest known hole in Canon V0. Recorded, not
papered over.

---

## Coverage after V0

| Area | Before | After V0 |
|---|---|---|
| Static visual craft | 6 of 14 domains touched | **12 of 14** |
| Moving image | 4 of 13 | **9 of 13** |
| Commercial communication | 5 of 14 | **11 of 14** |
| Creative thinking | 2 of 7 | **6 of 7** |
| Evaluation | 3 of 8 | **6 of 8** |

Still absent after V0: short-form feed grammar, Devanagari, Indian cultural context, motion design,
semiotics, modern effectiveness evidence, colour semantics.

---

## Stopping criterion

**Not atom count.** Volume was never the constraint and optimising for it is how the first probe
went wrong.

Canon V0 is complete when **all four hold**:

1. **Dimensional coverage.** Every judging dimension in
   [CANON-EXPERIMENT-V0](CANON-EXPERIMENT-V0.md) — concept quality, hierarchy reasoning,
   proposition clarity, objective fit, audience fit, visual strategy, trade-off awareness,
   contradiction detection, appropriate specificity, intent preservation — has **at least two
   independent sources** able to inform it.

2. **Cross-source structure exists.** At least one `cross_source_concept` in each of static craft,
   moving image, and commercial communication. Fewer than three means the sources are not yet
   speaking to each other and the Canon is still a pile of books.

3. **At least one recorded disagreement.** Sources must contradict somewhere — Whipple against
   Ogilvy on method is the expected one. A Canon with no disagreements has been flattened.

4. **Both experiments are runnable.** Enough coverage to retrieve relevant knowledge for every
   brief in the planning set and every asset in the evaluation set, without a domain being empty.

Then stop and run the experiments. **Do not extend V0 to close the four absent domains** — they
need non-book work and would delay the only tests that matter.
