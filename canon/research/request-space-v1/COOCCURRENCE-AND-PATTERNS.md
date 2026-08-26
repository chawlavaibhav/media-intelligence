# CANON-009 — recurring patterns and co-occurrences (C9-C)

**Task:** CANON-009 / C9-C · **Date:** 26 Aug 2026 · **Status: PROPOSED, evidence-labelled**
**Input:** `request-source-register.yaml`, `MEDIA-REQUEST-GRAMMAR-v1-PROPOSAL.yaml`

---

## 0. What this document is trying to find, and what it refuses to do

**Purpose:** identify the request *combinations* that deserve direct benchmark coverage later —
because a combination can be hard in a way none of its parts are.

**Two things it deliberately does not do.**

It does not enumerate the cartesian product. Fourteen grammar components would give thousands of
combinations, almost all of which never occur and none of which anyone would test.

And **it does not produce a global prevalence number.** No percentage here is combined across
corpora. DiffusionDB, r/PhotoshopRequest and a Pika Discord are three different populations, and
averaging them would manufacture a figure describing nobody.

## 1. The honest starting point: co-occurrence is barely measurable

Of the register's eight real-user sources, **how many support genuine co-occurrence analysis?**

| Source | Co-occurrence inferable? | Why |
|---|---|---|
| PSR (SRC-03) | **Yes** | Three annotated dimensions over 82,976 requests |
| TIP-I2V (SRC-08) | **Yes** | Subject, background, action and camera motion annotated separately |
| DiffusionDB (SRC-01) | Partially | Co-occurrence of *words in a prompt*, which is not co-occurrence of requirements |
| VidProM (SRC-07) | Partially | Same limitation |
| RealEdit / SEED (04, 05) | Partially | Same population as PSR — not independent |

**Only two sources genuinely support it, and one of them shares its population with two others.**

So this document is mostly **structural inference from documented components**, not measured
co-occurrence. Every pattern below carries a label saying which it is. Where the honest answer is
"the combination is plausible and nobody has measured it", that is what it says.

## 2. Patterns with real supporting evidence

### P1 · Edit + preservation — `SOURCE-SUPPORTED`

**The single best-evidenced pattern in the request space.**

An edit request is *constituted* by this combination: something must change, against an implied
background of everything that must not. PSR's 82,976 requests are all of this shape, and RealEdit's
authors make ecological validity — anchoring to the user's own image — their stated motivation.

**Why it matters to us:** it is the shape of most commercial revision work. "Same ad, new price."
"Same pack shot, festival background." And it is the pattern our brief bank contains **zero** of.

**What is still unknown:** *which dimensions* of identity requesters expect preserved. No corpus
records that. SPEC-01's `entities[].invariants` already draws the distinction more finely than any
evidence source found.

### P2 · Supplied image + motion instruction — `SOURCE-SUPPORTED`

1.70M+ real TIP-I2V requests. The text does not describe a scene; it instructs motion on the
supplied image.

**Why it matters:** this is the most likely production route for short commercial video — a customer
has a product photograph and wants it to move. It is also a distinct operation, and our bank
contains **zero** of it.

**Sub-pattern worth separating:** requested motions split into camera ("zoom"), subject locomotion
("walk") and micro-expression ("blink"). Three production problems, three failure modes, one grammar
component. A benchmark that tests "motion" as one thing will miss two of them.

### P3 · Human subject + everything else — `SOURCE-SUPPORTED (with a caveat that must travel with it)`

People dominate two independent corpora, two modalities and two interfaces: woman 22.26% and man
16.2% of images in the >3M-prompt analysis; all three top TIP-I2V subjects human-related.

**The caveat:** those populations are recreational-dominant, and "astronaut" sits in the same top-3.
The transferable claim is **humans are the most common subject**, not the specific subjects.

**Why it matters:** human realism, identity consistency and — where speech is involved — lip
plausibility are load-bearing wherever a person appears, which is most of the time.

### P4 · Multi-turn refinement — `SOURCE-SUPPORTED`

SEED-Data-Edit part 3: **95K multi-turn sequences, up to five rounds.**

**Why it matters more than it first appears:** it says the atomic unit of real work is often a
*conversation*, not a specification. Every brief we hold is a single complete statement issued once.
That may be the least realistic property of our entire bank — and it is a property of the bank's
*format*, not of any individual brief, so no amount of rebalancing fixes it.

### P5 · Style/quality modifiers attached to everything — `SOURCE-SUPPORTED, and decaying`

Style and quality modifiers dominate prompt text — "cinematic", "highly detailed", "8k". And
"trending on artstation" went from top-prominent in 2022 to outside the top 10 by 2023.

**Why it matters:** this is a *tool-shaped* component, not a customer-shaped one. It supports
SPEC-01's exclusion of `render_method` from Creative IR. A benchmark built on these modifiers would
be measuring a convention with a shelf life.

## 3. Patterns our product needs where evidence is thin or absent

Stated plainly, because these are exactly the places where it would be easy to assume the evidence
exists.

### P6 · Product + person + supplied reference — `INFERRED, not measured`

Each part is attested. **The combination is not.** No corpus reports how often a request involves a
commercial product, a person, and a supplied brand reference together.

Our bank has 19 briefs with people and 13 with a hero product, so we treat this as central. That is a
**product-scope decision**, and it should not be presented as evidence-backed.

### P7 · Exact text + commercial design — `WEAK EXTERNAL SUPPORT`

A whole benchmark family exists for text rendering, and its authors motivate it with advertising and
brand-name rendering. One benchmark lists ten "visual-text carriers" said to cover use cases observed
in real deployment — poster, advertisement, cover, logo, sticker, and others.

**But no real-user corpus reports how often text is requested.** Not one.

**And 28 of our 30 briefs require exact strings.** That is the sharpest mismatch between our bank and
the available evidence. It does not mean the bank is wrong — commercial creative genuinely does carry
copy, and the benchmark community clearly considers it important. It means **we cannot currently
defend the weighting with evidence**, and should stop implying we can.

### P8 · Person + speech + video — `NO EXTERNAL SUPPORT`

No corpus in the register covers speech, voiceover or dialogue. Twelve of our 30 briefs carry exact
spoken scripts.

This follows from the first-product scope rather than from observed demand. Legitimate — and it must
be labelled as scope-derived, not evidence-derived.

### P9 · Multi-shot + identity continuity — `INFERRED`

Identity preservation is well attested for *editing*. Continuity *across shots in a generated
sequence* is not measured by any source here.

Our bank has 10 briefs with explicit identity-continuity requirements. Canon's own coverage
rebaseline rates continuity as one of its stronger domains, so we have the knowledge; what we lack is
external evidence about how often customers ask for it.

### P10 · Variant sets and campaign families — `QUALITATIVE ONLY`

"Creative versioning" recurs as a named commercial activity in practitioner reports — many variants
of one creative across markets, formats and placements. No frequency, no traceable primary source.

Our bank has **zero** briefs whose output is a set. Given that the product optimises *Cost per
Accepted Outcome*, a request producing twelve variants has completely different economics from one
producing a single asset — and we cannot currently represent it at all.

## 4. Population bias, stated per source

The runbook requires this to be explicit, and it is the reason no number in this document is pooled.

| Population | What it over-represents | What it under-represents |
|---|---|---|
| **SD Discord** (DiffusionDB) | Recreational art, fantasy, portraiture, style incantation | Products, brands, commercial copy, deadlines |
| **Pika Discord** (VidProM) | Enthusiast video, spectacle | Commercial video, duration and platform constraints |
| **I2V users** (TIP-I2V) | Animating existing images; human subjects; hobby subjects like astronauts | Brand assets, product motion, commercial acceptance |
| **r/PhotoshopRequest** (PSR, RealEdit, SEED-2) | Personal photo repair, removal, restoration | Original creative production, brand systems |
| **Arena voters** | Aesthetic preference between two models | Anything about what people wanted in the first place |
| **Agency practitioners** | Process and workflow narrative | Frequency of anything |

**Three of these are one population.** PSR, RealEdit and SEED part 2 all draw on r/PhotoshopRequest,
and must not be counted as three agreeing sources.

## 5. What deserves direct benchmark coverage — a proposal

Ranked by *evidence strength × relevance to the first product*. This is a **recommendation to the
Controller**, not a decision, and it is Eval's to act on if approved.

| Rank | Combination | Evidence | Currently in our bank |
|---|---|---|---|
| 1 | **Edit supplied asset + preservation** | Strong (82,976 real requests) | **0 briefs** |
| 2 | **Animate supplied image + motion type** | Strong (1.70M+ real requests) | **0 briefs** |
| 3 | Human subject + identity consistency | Strong on subject, inferred on consistency | 10 briefs |
| 4 | Exact text + commercial layout | Weak external, strong product need | 28 briefs |
| 5 | Multi-turn refinement | Strong (95K sequences) | **0 briefs** |
| 6 | Variant set / campaign family | Qualitative only | **0 briefs** |
| 7 | Person + speech + video | None external; scope-derived | 12 briefs |

**The pattern in that table is the finding.** The two best-evidenced combinations in the entire
request space have **zero coverage** in our bank, and the two with the heaviest coverage have the
weakest external support.

That is not an indictment of the bank. It was built from the first-product scope before any of this
research existed, and it does one thing no public corpus does at all — it carries objectives,
audiences and acceptance criteria. But it means the bank is currently a **narrow probe of a wide
space**, and the Controller should know which parts of the space it does not touch.
