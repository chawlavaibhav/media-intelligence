# E10-G — Route-equivalence risks

**Task:** EVAL-010 · **Date:** 26 Aug 2026
**No models were run.** This file specifies what a later equivalence test must show **before**
evidence rows taken through two different routes may be pooled.

---

## Why this matters more than it sounds

The same nominal model reached two ways is often not the same measurement. If we pool a Registry
row taken through fal with one taken direct, and the two routes serve different builds or expose
different controls, we will have manufactured a contradiction and blamed the model for it.

The default is therefore: **two routes are two rows until an equivalence test says otherwise.**

Five cases are worth the cost of testing. They are ranked by how much damage silent pooling
would do.

---

## RE-1 — Google image models: fal `-preview` builds vs Google GA

**The risk, concretely.** fal exposes `fal-ai/gemini-3.1-flash-image-preview` and
`fal-ai/gemini-3-pro-image-preview` **alongside** its `nano-banana-2` and `nano-banana-pro`
aliases. Google's own route for the same models is **GA since 28 May 2026**.

So fal may be serving a *preview* build of a model that is generally available elsewhere. Preview
and GA builds of an image model can differ in output distribution, safety behaviour and
resolution support.

**Compounding it:** fal's `nano-banana-2` alias does not say which build it points at, and it can
be repointed with no signal to us.

**Equivalence test required before pooling.** Hold prompt, seed, resolution and aspect ratio
fixed. Run the same item set through Google direct at a pinned model id and through
`fal-ai/nano-banana-2`. Compare output distribution, not single images. Additionally compare
`fal-ai/nano-banana-2` against `fal-ai/gemini-3.1-flash-image-preview` to detect whether the alias
is simply the preview build under another name. **If the alias cannot be shown to track GA, do not
pool, and prefer Google direct** — which is also the only route where we have a verified price.

## RE-2 — GPT Image 2 across three routes with three different control surfaces

**Three routes exist and none is a drop-in for another.**

| Route | Evidence | Notable difference |
|---|---|---|
| OpenAI direct | OpenAI SDK | `input_fidelity`, `mask`, `background`, sizes `1024x1024 / 1536x1024 / 1024x1536`; **no seed** |
| Runway | Runway SDK, model `gpt_image_2` | reference images with `uri`; a **completely different ratio set** including `2048:880`, `1920:1088`, `1920:1280` |
| fal | fal SDK | **`gpt-image-2` is not enumerated at all** — only `gpt-image-1`, `-1-mini`, `-1.5` |

**The trap.** Runway's ratio set is not a superset or subset of OpenAI's — it is a different set
at different pixel dimensions. An image generated at `1920:1088` through Runway is not comparable
to one at `1536x1024` through OpenAI on any framing- or composition-sensitive measure.

**Equivalence test required.** Only compare at dimensions both routes actually offer. If no shared
dimension exists, **the routes cannot be pooled at all** for framing-sensitive capabilities, and
each needs its own Registry row. Also establish whether Runway pins the dated snapshot
`gpt-image-2-2026-04-21` or the floating `gpt-image-2` alias.

## RE-3 — Veo 3.1 across Google, fal and Runway, with different workflow coverage

**The control surfaces genuinely differ**, and in a way that changes which hypotheses each route
can even test.

- **Google direct** — `GenerateVideosConfig` carries `last_frame`, typed `reference_images`
  (ASSET/STYLE) and a video `mask` with modes INSERT / REMOVE / REMOVE_STATIC / OUTPAINT. This is
  the richest surface. Only a `-preview` id is enumerated for the full tier.
- **fal** — splits the same capabilities into *separate endpoints*:
  `first-last-frame-to-video`, `extend-video`, `reference-to-video`, `image-to-video`. Note that
  `reference-to-video` **has no seed** while `first-last-frame-to-video` and `extend-video` do.
- **Runway** — `veo3.1` and `veo3.1_fast` with `duration` restricted to **4, 6 or 8 seconds** and
  only four aspect ratios, plus `audio: bool`. Narrower than either.

**Equivalence test required.** Pick the intersection — text-to-video, audio on, 720p, a duration
all three accept — and test there first. **Do not pool a seeded fal run with an unseeded one**
even on the same endpoint family. Treat the Google mask modes as a Google-only capability until
another route demonstrably exposes them.

## RE-4 — ElevenLabs v3: fal wrapper is materially thinner than direct

**Same model id, very different control.**

| Control | ElevenLabs direct | fal `tts/eleven-v3` |
|---|---|---|
| `seed` | present | **absent** |
| `pronunciation_dictionary_locators` | present | **absent** |
| `previous_text` / `next_text` | present | **absent** |
| `previous_request_ids` / `next_request_ids` | present | **absent** |
| `voice_settings` | present (object) | partial (`stability` only) |

**Why this is the most consequential wrapper gap found.** The pronunciation dictionary is exactly
the mechanism for forcing correct Indian brand-name pronunciation, and the previous/next-text
controls are what hold prosody stable across a long script. A voice measurement taken through fal
cannot test either.

**Equivalence test required.** For any voice-identity or long-form-consistency hypothesis, use
**ElevenLabs direct**. Rows taken through the fal wrapper must not be pooled with direct rows and
should be labelled as a reduced-control route.

## RE-5 — Sarvam vs ElevenLabs: not a route difference, a *reproducibility* difference

This is not a wrapper problem — it is a comparability problem the measurement design has to absorb.

- **ElevenLabs direct** exposes `seed`.
- **Sarvam** exposes `temperature` and **no seed**.

So a repeat-consistency number from ElevenLabs (variance under a held seed) and one from Sarvam
(inherent variance) are **not the same quantity**, and neither is comparable to the project's
proposed 0.95 repeat-consistency threshold in the same sense.

**Required before either number is used.** EVAL-009 should decide whether repeat consistency is
measured (a) under a held seed where available, or (b) as inherent variance with seed unset
everywhere, and apply one convention across the whole wave. Mixing them silently would make the
Indic-voice comparison — arguably the most product-relevant one on the list — meaningless.

---

## The general rule this produces

Where the same nominal model is reachable by more than one route, **record the route in the
Registry row**, and treat pooling as a claim requiring evidence rather than a default. Concretely,
a row should carry: provider, exact endpoint or model id, whether the id is pinned or floating,
and the control set actually used.

The cheapest useful first experiment is **RE-1**, because Google is the one vendor where we hold
both a verified price and a verified GA identity, so a wrapper difference there is measurable
without spending on an unpriced route.

## What none of this authorises

No model was run and none may be. These are specifications for tests that require an approved
budget, a qualified checker and a Controller decision that does not yet exist.
