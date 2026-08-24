# Finding 11 — Empirical / knowledge join

**Date:** 23 Aug 2026 · **Cost:** ₹0 — all material already existed
**Tests:** assumption 4 — *a shared ontology improves joins between books and empirical failures*
**Not tested:** A/B/C. No books ingested. No Pass 2.

## Material

All failures below were **observed and recorded before this experiment**, by a human, for other
reasons. Nothing was generated or invented for it.

| Source | What it is | Failures used |
|---|---|---:|
| `media-factory/spike/out/scores.json` | 64 human-scored generations, nano-banana-pro + seedream, pass/fail with a free-text note | 10 |
| `FINDINGS-01` | Devanagari checker study, 14 samples | 4 |
| `media-factory/HANDOFF.md` | post-mortem of the live WhatsApp product | 6 |

Three of the ten scored images were re-inspected directly to describe the observable defect
precisely. **Raw observer descriptions are preserved verbatim throughout.**

The scored set's own headline: **84% pass rate, 10 failures in 64** — nano 7/32, seedream 3/32.

---

## The twenty records

Abbreviations: **SK** source knowledge · **req** Creative IR requirement · **cons** consequence

### Group 1 — Direct creative-knowledge relationship (4)

**E-01 · `nano_arms-crossed_t0` — raw: "logo floating mid-air"**
- *Observable:* the wordmark and tagline sit in the reception space with no visible plaque,
  mounting or wall contact. Tagline strokes are also degraded.
- *Suspected cause:* generator placed a 2D asset into a 3D scene without resolving contact geometry.
- *Requirement violated:* `brand.logo` placement; physical plausibility (no IR field).
- *Consequence:* reads as a compositing error; undermines the premium register.
- *Relations:*
  `same_mechanism` → `mb_009` (Bang, p51: *"notice how it feels as though it is floating, because
  there isn't any defined ground or baseline attached to it"*). The book states the mechanism
  exactly — absence of a baseline produces the floating read.
  `related_to` → `mb_015` (depth via base height).
- **The strongest join in the set.** A 2000 picture-book about cut paper explains a 2026 diffusion
  artefact at mechanism level, and the mechanism implies the repair: give it a surface.

**E-02 · `nano_sign_t1` — raw: "board occludes body oddly"**
- *Observable:* held board overlaps the subject's torso at an angle that reads as interpenetration
  rather than holding.
- *Cause:* unresolved occlusion ordering / contact.
- *Req:* `relationships` (person *holding* board); `static.composition`.
- *Cons:* subject reads as behind their own prop.
- *Relations:* `same_observed_effect` → `mb_016` (overlap takes the covered element's space and
  binds the two into one unit). **Mechanism matches; intent inverts** — Bang describes overlap as a
  deliberate binding tool; here it is a defect. See §Expressiveness.

**E-03 · `seedream_sign_t0` — raw: "text collides with head"**
- *Observable:* the subject's head sits inside the headline, occluding a character.
- *Cause:* independent placement of text and subject with no z-order or keep-out reasoning.
- *Req:* `copy.headline` exactness; `creative.hierarchy`.
- *Cons:* headline unreadable — the asset's primary message fails.
- *Relations:* `same_observed_effect` → `mb_016`; `violates_requirement` → `rw_003` (a reading path
  needs a definite start and end); `related_to` → `rw_009` (clarity outranks thematic expression).

**E-04 · HANDOFF §5 — raw: "a photo with a banner stamped on it"**
- *Observable:* every output is a photograph with a flat headline bar composited over it.
- *Cause:* architectural — `CLAUDE.md`'s never-render-text rule forced compositing.
- *Req:* `creative.hierarchy`, `static.composition`.
- *Cons:* named in the post-mortem as *"the main reason output looks amateur."*
- *Relations:* `same_mechanism` → `rw_005` (trapped white space separates related elements);
  `same_observed_effect` → `lu_007` (three-cue ceiling / signal overload);
  `related_to` → `mb_005`, `mb_006` (contrast and value against ground).
- Richest set of book relations in the batch, and the only failure that is a **design decision**
  rather than a generation artefact.

### Group 2 — Family-level relationship only, mechanism differs (4)

**E-05 · Wan `chai-sign` — raw: "सुवह की (frames 1–4) → सुवह के (frames 5–6)"**
- *Observable:* the rendered sign's misspelling **changes within a single 5-second clip**.
- *Cause:* no cross-frame text conditioning.
- *Req:* `copy.script_system`, exactness; `video.continuity_requirements`.
- *Cons:* an in-world sign that mutates while on screen.
- *Relations:* `same_observed_effect` → `gos_010` (continuity of action across takes) **at family
  level only**. Both are "a property that must be invariant across time is not." Mechanisms are
  unrelated — a performer repeating a gesture differently versus a diffusion model resampling
  glyphs. `distinct_from` at mechanism level, recorded explicitly.

**E-06 · `nano_chai_t3` — raw: "face drift — younger, streak moved"**
**E-07 · `nano_server-room_t2` — raw: "blazer color split"**
**E-08 · `nano_server-room_t3` — raw: "outfit changed to pants"**
- *Observable:* the same character's face, hair marking and wardrobe change between generations in
  one set.
- *Cause:* reference conditioning insufficient to hold identity across prompts.
- *Req:* `entities.invariants`, `entities.allowed_variation`.
- *Cons:* the cast does not read as one person — the exact capability `HANDOFF.md` §7 calls the
  unproven, load-bearing one.
- *Relations:* `same_observed_effect` → `gos_007` (reciprocating imagery: shots covering the same
  subject must match on size, placement, height, angle) at family level. GoS is about framing
  geometry; this is generative identity instability. `no_known_connection` at mechanism level.
- One partial mechanism link worth noting: `lsm_004` says appearance variation across viewing
  angle is **a property of the surface, not a free choice**. E-07's blazer changes colour with no
  lighting justification, which is that constraint violated — but LSM never discusses identity.

### Group 3 — Connected only through requirement or consequence (5)

No creative-knowledge relation. They connect to the architecture, not to the books.

**E-09 · `nano_desk_t3` — raw: "two laptops"** — count violation. Both bear the logo; the marks
differ from each other. `violates_requirement` → entity count. `no_known_connection` to any SK.

**E-10 · `seedream_poster_t2` — raw: "wordmark missing"** — mandatory omitted.
`violates_requirement` → `brand.mandatories`. `related_to` → `og_004` (every asset contributes to
one brand image) at **consequence** level only — Ogilvy explains why it matters, not why it happened.

**E-11 · `nano_server-room_t0` — raw: "bg logos mirrored"** — background logos rendered reversed.
`violates_requirement` → `brand.logo` exactness. `related_to` → `og_004` at consequence level.

**E-12 · Wan `chai-sign` — raw: "सुवह की पहली चाथ (ब→व, य→थ)"** — character substitution in
generated Devanagari. `violates_requirement` → `copy.headline` exactness.
`no_known_connection` to any source term. Consequence: `og_005` — shoddy execution transfers to
the product — applies, but as commercial reasoning, not diagnosis.

**E-13 · `still_seedream_headline` — raw: "gibberish"** — Devanagari headline unreadable.
Same profile as E-12.

### Group 4 — No useful Canon relationship (7)

**E-14 · `seedream_sign_t1` — raw: "rendered hex codes from prompt"**
Colour hex values from the prompt appear as visible text under the logo. Prompt-leakage artefact
with no analogue in any craft literature. `no_known_connection`.
**Also carries E-03's head-collision defect** — see §Co-occurrence.

**E-15 · Finding 01 — raw: "Claude Sonnet 4.5 reported 'exact match' for six visibly broken frames"**
Evaluator false-pass. Relates to `governance: evidence_interpretation`, not to creative knowledge.

**E-16 · Finding 01 — raw: "tesseract (hin) 0/14, unreadable output"** — tool incapacity.

**E-17 · HANDOFF §10 — raw: "paid orders still wedge on redeploy"** — infrastructure.

**E-18 · HANDOFF §10 — raw: "`/tmp` loses approved previews on restart"** — infrastructure.

**E-19 · HANDOFF §10 — raw: "Sarvam bulbul:v3 speaker names differ from v2 (v2's anushka/meera invalid)"** — provider API drift.

**E-20 · HANDOFF §10 — raw: "Plivo: one media per message"** — platform constraint.
Notable: this is a **`delivery` constraint**, and `delivery` was one of the IR sections that
received **zero bindings** from six books. Independent confirmation that some IR fields are
structurally not Canon-fillable.

---

## Results

| Category | n | % |
|---|---:|---:|
| **Direct creative-knowledge relationship** (mechanism or effect recognisably shared) | 4 | **20%** |
| **Family-level only** (broad concept, mechanism differs) | 4 | **20%** |
| **Requirement / consequence only** (no knowledge relation) | 5 | **25%** |
| **No useful Canon relationship** | 7 | **35%** |

**Ambiguous mappings: 3.** E-02 (mechanism shared, intent inverted — technique vs defect).
E-07 (partial mechanism link to `lsm_004` from a source that never discusses identity).
E-10/E-11 (Ogilvy relates at consequence level; whether that counts as "connected" is a judgement
this experiment had to make and could have made either way).

### What the shape means

The join **exists and is not uniform.** Where it is strong it is very strong — Molly Bang explains
a 2026 diffusion artefact at mechanism level, and the mechanism implies the fix. Where it is
absent it is completely absent: no craft literature has anything to say about hex codes leaking
into pixels.

**The most common connection is not term-to-term.** Only 4 of 20 relate at term level. Twice as
many connect through the Creative IR requirement they violate, or through a commercial consequence
a book explains. That is a real join — but it runs **through the IR and the acceptance contract,
not through the ontology.** Assumption 4 as written ("a shared ontology improves joins between
books and empirical failures") is too narrow: the ontology handled the strong cases, and the
architecture handled more of them.

**The failures cluster where the books do not reach.** All four direct hits are composition and
physical plausibility — exactly the six probes' territory. Every text-corruption, identity-drift
and operational failure falls outside it. This is consistent with FINDINGS-09: three IR fields
absorbed most bindings, and `delivery` and `acceptance` got none.

---

## Was the ontology expressive enough?

**Mostly — with three gaps found by use.**

**1. No way to say "same mechanism, opposite intent."** Bang's overlap (E-02) is a deliberate tool
for binding elements. In the generation it is a defect. `same_mechanism` overstates the
correspondence; `related_to` loses the mechanism. Proposed: `unintended_instance_of`.

**2. No way to record the abstraction level of a relation.** E-05 through E-08 relate to GoS terms
only through a broad family, with mechanisms explicitly unrelated. Expressing that currently needs
two relations pointing opposite ways — `same_observed_effect` plus `distinct_from` — which reads
as a contradiction rather than a precise statement. Proposed: a `level` qualifier
(`mechanism` · `effect` · `family` · `requirement` · `consequence`) on the relation itself.

**3. No relation between two empirical terms.** E-14 carries two independent defects; the
ontology has no `co_occurs_with`.

`no_known_connection` earned its place immediately — 7 of 20 — and recording it is what makes the
35% legible rather than looking like extraction failure.

---

## Co-occurrence: a finding about the data, not the ontology

`seedream_sign_t1` was scored **"rendered hex codes from prompt."** On inspection it *also* shows
the head-collision defect that `seedream_sign_t0` was scored for. The human recorded the most
salient failure and the second was lost.

Every record in `scores.json` is a single free-text label. If Empirical Memory inherits that shape,
failure counts will be systematically undercounted and co-occurrence — which is exactly what would
reveal a shared cause — will be invisible. **An empirical failure record must permit multiple
defects per output.**

---

## Does joining improve diagnosis, evaluation, routing, repair?

**Diagnosis — yes, demonstrated once, clearly.** E-01's floating logo has a cause stated in the
source: no defined ground or baseline. That is a better diagnosis than "logo floating mid-air", and
it names the repair. One case in twenty, but it is a real one.

**Evaluation — yes, and this is the strongest result.** `gos_005` says a continuity break is
invisible in any single shot and appears only across shots. E-05 is exactly that: the Devanagari
sign is misspelled in every frame, but the *drift* — की to के — exists only between frames 1–4 and
5–6. Finding 01 recorded it as an "incidental finding" because a frame-level checker cannot
represent it.

**The book knowledge predicted the observation unit the evaluator needed, and the empirical data
independently confirmed it.** That is the join working in the direction that matters — book
knowledge shaping how we look, not just labelling what we found.

**Routing — no evidence.** Nothing in six books says which model to use. Routing needs the
Capability Registry; the Canon has no part in it. The one usable routing signal here is empirical
and needs no books: nano-banana-pro failed 7/32, seedream 3/32, and their failure profiles differ —
nano drifts identity, seedream corrupts text and leaks prompts.

**Repair — partial.** Book-derived repairs exist for the 4 direct cases. For the other 16 the
repair is respecify-and-regenerate, which needs no Canon. Consistent with FINDINGS-08: failure
modes transfer, repairs largely do not.

---

## What this does to assumption 4

**Status: partially supported, and the claim needs restating.**

Supported: the join exists, is real at mechanism level in a minority of cases, and demonstrably
improved evaluation design in at least one case.

Not supported as written: "a shared ontology improves joins" implies the ontology is the mechanism.
Most connections ran through the Creative IR requirement or the commercial consequence instead.

**Restated:** *Book knowledge connects to empirical failure through at least three distinct
channels — shared mechanism, violated requirement, and commercial consequence — and the ontology
serves only the first.*

Register entry 4 should be updated to reflect this, and the three expressiveness gaps recorded.

---

## Recommended next steps

1. **Update assumption 4** with the restated claim and this evidence.
2. **Add the three relation extensions** — `unintended_instance_of`, a `level` qualifier,
   `co_occurs_with` — to SPEC-05.
3. **Change the empirical failure record shape** to allow multiple defects per output, before any
   more failures are logged in the single-label form.
4. **Do not expand the Canon toward generator artefacts.** 35% of failures have no craft-literature
   partner and never will. That is the Capability Lab's territory.
5. The A/B/C experiment remains queued and untouched.
