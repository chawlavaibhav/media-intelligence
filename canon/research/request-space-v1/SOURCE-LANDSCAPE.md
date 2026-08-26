# CANON-009 — request-source landscape (C9-A)

**Task:** `canon/tasks/CANON-009-CLOUD-SCOPE-PROGRAM.md` · **Date:** 26 Aug 2026
**Branch:** `work/canon-009-request-space` · **Spend: ₹0** · **Machine-readable:** `request-source-register.yaml`

---

## 0. What this session could and could not do

**Web search works. Opening a web page does not.** Every fetch attempt returned `EGRESS_BLOCKED` —
`arxiv.org`, `huggingface.co`, `openreview.net` — and direct `curl` to any host returned nothing.

So every fact in this landscape is **`search_verified`**: established from search results that
surfaced first-party pages — arXiv listings, project sites, dataset cards, GitHub repositories — but
**no primary page was opened and read here.** Figures were consistent across independent result sets,
which is worth something and is not the same as having read the paper.

**Practical rule for the Controller:** treat every number below as good enough to plan with and not
good enough to spend on. Anything that would drive a budget decision must be re-verified against the
primary source first.

Nothing was downloaded. The task forbids pulling large payloads merely to prove they exist, and no
corpus here needed it — papers, dataset cards and project pages carry what C9-A asked for.

## 1. Thirteen sources, and the line that runs through them

| # | Source | Modality | Class | Scale |
|---|---|---|---|---|
| 01 | DiffusionDB | text→image | real user | 14M images / 1.8M prompts |
| 02 | *No Longer Trending on Artstation* | analysis of T2I | derived | >3M prompts |
| 03 | **PSR** (r/PhotoshopRequest study) | image editing | **real user** | **82,976 requests** |
| 04 | RealEdit | image editing | real user | 57K+ examples |
| 05 | SEED-Data-Edit | image editing | mixed | 52K real + 95K multi-turn |
| 06 | MagicBrush / HumanEdit / ImgEdit | image editing | **benchmark** | 5–10K each |
| 07 | VidProM | text→video | real user | 1.67M prompts |
| 08 | **TIP-I2V** | image→video | **real user** | **1.70M+ text+image pairs** |
| 09 | Artificial Analysis Image Arena | text→image | **benchmark** | >45K preferences |
| 10 | Arena-T2I-Hard | text→image | **unresolved** | — |
| 11 | *Journal of Advertising Research* 2025 | commercial process | practitioner | interviews |
| 12 | Agency adoption surveys | commercial process | practitioner | — |
| 13 | Text-rendering benchmark family | text→image | **benchmark** | 100–2,000 prompts |

**The line that matters is not modality. It is this:**

> **Every large real-user corpus in existence is a MODEL-INTERFACE corpus. None of them is a BRIEF
> corpus.**

A prompt is what someone types into a tool *after* they have already decided what they want. A brief
is a customer telling you what they want and why. Objective, audience, brand constraints and
acceptance criteria are **structurally absent** from all thirteen sources — not rare, absent, because
the interfaces that produced them have no field for such things.

This is the finding that shapes everything downstream, and §5 works through what it does and does not
license us to conclude.

## 2. The three sources that carry most of the weight

### PSR — 82,976 real editing requests, 2013–2025

The strongest source found, and the one closest to our product's actual shape. Ordinary people
posting their own photograph to r/PhotoshopRequest and asking a human for a specific outcome.

**These are requests for outcomes, not prompts.** The requester wants a result and does not care how
it is produced — which is exactly the relationship our product has with its customer.

Its taxonomy has three dimensions: **subject** (what is modified, mapped to WordNet synsets → 5 main
categories, 12 subcategories), **action verb** (what modification), and **creativity level**
(routine tasks versus those admitting multiple open-ended interpretations).

That third dimension is quietly the most interesting thing in this landscape. It is a coarse measure
of *how much latitude the requester granted* — which is what SPEC-01's six operations
(preserve / derive / decide / delegate / ask / flag) measure per field, at finer grain, and which we
designed independently. Convergent structure from an unrelated direction is the best kind of
corroboration a schema can get.

### TIP-I2V — 1.70M+ real image-to-video requests

Closest large corpus to the commercial job: a customer supplies an asset and asks for motion on it.

Its structural finding has architectural consequences for us. Each text prompt focuses on **how to
bring the static elements of the supplied image to life**, rather than describing a scene from
nothing. An I2V request is an *operation on a supplied asset*. Our Creative IR has no field that says
which operation is being requested.

Two other findings, with their caveats attached:

- **Top-3 subjects — "person", "astronaut", "portrait painting" — are all human-related**, and the
  paper describes user preferences as unbalanced. The *human dominance* transfers. "Astronaut" and
  "portrait painting" are a hobbyist signature and transfer to nothing.
- Beyond generic "move", users ask for **"zoom", "walk", "blink"**. Worth noticing that these are
  three different production problems — camera, subject locomotion, micro-expression — sitting inside
  one grammar component.

### *No Longer Trending on Artstation* — >3M prompts analysed

The only source giving hard subject percentages, and the source of the most important warning here.

After removing adjectives and aesthetic/style words, the top subjects were **woman 22.26% of images,
man 16.2%, dress 6.92%, hair 5.51%, room 5.44%, flower 5.33%.**

And the authors' conclusion: prompting focuses largely on surface aesthetics and conventional
imagery, and **the dominant use of the systems analysed is recreational rather than artistic.**

They also found that **"artstation" and "trending on artstation" were prominent in 2022 and gone from
the top 10 by 2023** — prompt conventions decay as models improve. §5.3 takes that up, because it
independently supports a decision SPEC-01 already made.

## 3. What the benchmark sources are for — and are not

SRC-06, SRC-09, SRC-10 and SRC-13 are **benchmark-authored**. The task's research standard is
explicit that benchmark prompts are not evidence of user demand, and it is right: their category
balance reflects what their authors chose to test.

They are still useful, for one narrow thing: **operation vocabulary**. Three independent editing
benchmarks converge on much the same verb set — add, remove, replace, alter, background change, style,
action change, extraction — and vocabulary convergence is meaningful even when proportions are not.

**Their proportions appear nowhere in this landscape**, and no percentage from them is carried into
the grammar.

Two honest gaps in this group:

- **Artificial Analysis Image Arena:** how its prompt set is selected, and what use cases it spans,
  **could not be established.** The publisher states it reflects a wide range of use cases; no
  taxonomy was visible. Recorded as UNKNOWN.
- **Arena-T2I-Hard:** named in the runbook as a seed source. Search returned no first-party page
  sufficient to describe its population or construction. **Left unresolved rather than described** —
  inventing a characterisation would be worse than an empty row.

## 4. Source lineage — three of the editing sources are one population

PSR, RealEdit and SEED-Data-Edit part 2 **all draw on r/PhotoshopRequest.**

They are **not independent corroboration of each other.** Three papers agreeing about editing request
structure is, on this axis, one community agreeing with itself.

This is the same trap the Canon has been caught by twice — companion volumes, and two books recording
the same practitioner — and the same rule applies: **treat them as one source lineage.** Where this
document says editing evidence is strong, it means one large well-studied population, not three.

## 5. What the landscape licenses, and what it does not

### 5.1 It does not license a demand claim

No corpus here measures commercial demand. The largest are recreational-dominant by their own
authors' conclusion. **Frequency in DiffusionDB is not commercial priority**, and a component can be
rare there and central to our product.

Any move to rebalance our brief bank *toward* corpus frequency would import a hobbyist distribution
into a commercial product. That would be the specific mistake this whole exercise exists to avoid.

### 5.2 It does license structural claims

What the corpora are good for is **structure**: which components recur, which co-occur, and which
distinctions are real. Requests do split by operation before anything else. Identity preservation is
the whole content of an edit request. Requests arrive in rounds. Those are structural facts about the
world, visible even through a biased sample.

### 5.3 One finding independently supports a decision we already made

SPEC-01 deliberately excludes `render_method` from Creative IR, on the reasoning that keeping it
would bake today's model limitations into a permanent specification.

The Artstation decay is external evidence for exactly that. A style incantation that was near-mandatory
in 2022 was noise by 2023, because the models changed. **Style vocabulary is model-contingent**, and a
Creative IR that had absorbed it would now be carrying dead weight. The project reached this
conclusion on its own reasoning; it now has evidence.

### 5.4 The largest hole is in the world, not in this session

**No corpus of commercial briefs was found** — no agency intake forms, no marketplace job posts, no
RFP text. Nothing that records objective, audience, brand mandatories and acceptance criteria at scale.

This is not an artifact of blocked egress. Such corpora are commercially sensitive and largely
unpublished. It means our 30-brief bank occupies a space **no public corpus covers** — which is an
argument for keeping it, and against ever calling it evidence-backed.

## 6. Explicit unknowns

| Question | Status |
|---|---|
| How often do real users request **text in an image**? | **Unknown.** No figure in any real-user corpus. Directly relevant: 28 of our 30 briefs demand exact strings. |
| How often is the subject a **product** rather than a person? | **Unknown.** No corpus reports product frequency. |
| What **duration, shot count or beat structure** do users request? | **Unknown.** No corpus records them. |
| Anything about **speech or voiceover** requests | **Unknown.** No corpus covers audio. |
| Any **India-specific, Hinglish or Devanagari** request corpus | **None found.** |
| Arena-T2I-Hard's construction | **Unresolved.** |
| Artificial Analysis prompt-set selection | **Unknown.** |

Seven unknowns, four of which sit directly under first-product requirements. They are listed rather
than estimated, because an estimate here would become a number someone later plans against.
