# E11-D — Scientific slots against supply evidence, in plain English

**Task:** EVAL-011 · **Date:** 26 Aug 2026
**Machine-readable record:** `SCIENTIFIC-SLOT-SUPPLY-RECONCILIATION.yaml`
**₹0 · no model/API/evaluator calls · no accounts · no Registry rows.**

---

## What this is, and what it deliberately is not

EVAL-009 chose **12 core scientific questions plus 2 reserves** — questions, not vendors.
EVAL-010 then verified, from providers' own published material, which models can actually be
called and at what exact version.

**This document joins the two. It is a reconciliation, not a re-selection.** No slot was added,
removed, or reprioritised. No sibling model was quietly slipped into a slot whose named candidate
could not be verified.

The rule the Controller set is the one that governs every row: **sourcing may qualify how a slot is
executed; it may never decide whether the question gets asked.**

## The result

| | Count |
|---|---:|
| Slots | 14 (12 core + 2 reserve) |
| Exact version verified from a provider-authorised source | **12** |
| Exact version could not be confirmed | **2** — IMG-04, AUD-03 |
| Slots with a verified price | 2 — VID-01, VID-05 |
| Slots fully execution-ready (identity + route + billing unit + price) | **1** — VID-05 |
| Slots deleted because sourcing was hard | **0** |
| Sibling substitutions performed | **0** |

So: **we know what to call for twelve of fourteen questions, and what it costs for one of them.**

## The two slots we could not pin — and why they stayed

**IMG-04 — Seedream 5.0 Pro.** fal carries Seedream v3, v4, v4.5 and **v5/lite**. It does not
carry v5/**pro**. A family match is not a match: v5/lite is a different model, and running it while
calling it IMG-04 would answer a different question than the one admitted.

**AUD-03 — Sync-3.** fal's highest enumerated lip-sync version is `sync-lipsync/v2/pro`. There is
no `sync-3`. The vendor's own site was unreachable, and the PyPI package of that name had no
verifiable publisher, so it was rejected rather than trusted.

**Both slots remain.** IMG-04 carries the only cross-asset identity question on the roster. AUD-03
carries the fallback route for Hindi dialogue video — which matters because the video models that
generate speech natively document five or seven languages and **Hindi is generally not among them**.
Deleting either because a version string could not be confirmed would have removed a question the
product actually needs answered.

What happens to them is a Controller call, recorded as **SUP-2**: accept a documented version
difference, defer the slot, or wait for direct catalogue access. EVAL-011 chose none of these.

## What the supply evidence changed about how slots run

Three findings alter execution without touching admission.

**AUD-02 must run direct, not through fal.** fal's ElevenLabs wrapper omits `seed`, the
pronunciation-dictionary locators, and the previous/next-text controls that ElevenLabs direct
exposes. The pronunciation dictionary is the mechanism the AUD-01 versus AUD-02 comparison turns
on, and the continuity controls are what hold prosody steady across a long script. **A measurement
taken through fal cannot test either.** Rows from the two routes must never be pooled.

**AUD-01 and AUD-02 are not currently like-for-like.** ElevenLabs exposes a seed; Sarvam exposes
`temperature` and no seed. Their repeat evidence measures different quantities until one convention
is declared for both. That decision — **SUP-3** — has to be made before Stage A runs, or the most
product-relevant comparison on the roster produces two numbers that cannot be set beside each other.

**Three slots have no seed at all on their verified route** — IMG-01, VID-02 and AUD-01. Their
repeats can only measure inherent variance. That is a real measurement, but it is not held-seed
repeatability and must not be reported as though it were.

## One EVAL-009 open question closed, one earlier claim withdrawn

**Closed:** EVAL-009 could not tell whether Veo 3.1 exposes advanced frame and extend controls,
because Google's pricing table lists them only under Veo 2. It does. Google's own SDK config
carries `last_frame`, typed reference images and four video mask modes, and fal exposes
`veo3.1/first-last-frame-to-video` and `veo3.1/extend-video` as endpoints. VID-01 can run its
intended controls.

**Withdrawn:** earlier research flagged Runway as possibly Enterprise-only and called VID-04 the
hardest access problem on the roster. Runway's own published SDK exposes `aleph2` through the
standard public API. That concern is dropped. Whether a particular account is entitled is a
separate question this task did not test.

## The awkward finding worth stating plainly

**The only image model with a fully verified price is not on the roster.**

Nano Banana 2 (`gemini-3.1-flash-image`, $0.067 per generated 1K image) is execution-ready. It is
not the named candidate for any slot. It genuinely answers IMG-01's question — it is a frontier
general image model, which is exactly what IMG-01 asks about — so it is recorded as an *equivalent
candidate* for the Controller (**SUP-4**).

It was **not** added. Adding a model because it happens to be the one we can price is precisely the
substitution the independence rule exists to prevent. gpt-image-2 remains IMG-01's candidate,
because the vendor typography claim it carries is the specific thing IMG-01 was admitted to test.

## Four decisions this surfaces for the Controller

| id | Slots | Decision |
|---|---|---|
| **SUP-1** | IMG-06 | Run Recraft v3 as named, or v4 where native `text-to-vector` is a first-class endpoint? The slot exists *because of* vector output, so this is a scientific-fit question. |
| **SUP-2** | IMG-04, AUD-03 | Accept a recorded version difference, defer the slot, or wait for catalogue access? |
| **SUP-3** | AUD-01, AUD-02 | Which seed convention governs the Indic voice comparison? Must be settled before Stage A. |
| **SUP-4** | IMG-01 | Add Nano Banana 2 as a second candidate — the only priced image model — or leave the slot as admitted? |

None of these is a sourcing decision dressed up as a scientific one, and EVAL-011 resolved none of
them on its own authority.
