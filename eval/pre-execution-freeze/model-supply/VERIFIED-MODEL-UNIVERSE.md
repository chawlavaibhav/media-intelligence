# E10-A / E10-B — Verified model universe, in plain English

**Task:** EVAL-010 · **Date:** 26 Aug 2026 · **Branch:** `work/eval-010-route-verification`
**Machine-readable record:** `VERIFIED-MODEL-UNIVERSE.yaml`
**No API calls · ₹0 spent · no accounts · no terms accepted · no Registry rows.**

---

## What this document is

EVAL-008 produced a list of models worth considering. **This task checked whether those models are
actually real, current, and callable** — exact version, exact workflow, exact controls, exact
billing unit, exact price.

It does **not** decide which models deserve testing. EVAL-009 owns that. Nothing here added,
removed or reprioritised a candidate.

**The short answer: about two thirds of the identities hold up, most of the prices do not, and
eight specific EVAL-008 claims did not survive contact with the providers' own material.**

---

## How evidence was graded

The task forbids search snippets from populating version or price fields. That left two
acceptable kinds of evidence, and one lucky break.

| Grade | What it is | What it can support |
|---|---|---|
| **Provider page, fetched** | We retrieved the page ourselves. **Only `cloud.google.com` was reachable** — 34 provider hosts were probed and 33 returned `403`. | Everything, including price |
| **Provider SDK** | A package the vendor publishes to PyPI or npm. Its generated type definitions are the vendor's own statement of model ids and request parameters. | Identity, version, controls — **never price** |
| **Lead only** | Blogs, leaderboards, search summaries | Nothing execution-grade |

**The lucky break was the SDKs.** Package registries were reachable even though vendor websites
were not. That turned a near-total blackout into genuine primary evidence for OpenAI, Google,
Runway, Sarvam, ElevenLabs, Alibaba, BytePlus and fal.

**The single most valuable artifact** was fal's own npm client, which ships a file declaring
**1,117 endpoint identifiers with their typed inputs**. That is fal stating, in its own published
code, exactly what it exposes and what each endpoint accepts.

**One honest limit, applied throughout.** An SDK can lag the live catalogue. Where a model is
missing from one, this document says `not_present_in_sdk_version` — never "unavailable". That
distinction is load-bearing and is not collapsed anywhere.

---

## Result in one table

| Outcome | Rows | Meaning |
|---|---:|---|
| **Execution-ready** | **2** | identity, route, billing unit and price all verified |
| Verified fallback only | 19 | route and identity verified, price missing |
| Identity or version unresolved | 5 | the exact selected version could not be confirmed |
| Route unresolved | 2 | no provider-authorised route found at all |

*(Statuses sum to 28 because the Veo 3.1 row carries three per-tier verdicts.)*

**The two execution-ready rows are both Google:** Nano Banana 2 (`gemini-3.1-flash-image`, $0.067
per 1K image) and Veo 3.1 Lite (`veo-3.1-lite-generate-001`, $0.05 per 720p video with audio).

**That is the headline, and it is uncomfortable on purpose.** We can identify most of these models
and describe their controls in detail. We can *pay* for almost none of them, because every pricing
page except Google's was unreachable.

---

## What EVAL-008 got right

Worth saying, because the corrections below are longer.

- **Sarvam Bulbul v3's 11 languages** — confirmed exactly against Sarvam's own API enum:
  Bengali, Indian English, Gujarati, Hindi, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil,
  Telugu. The model id `bulbul:v3` carries its version explicitly, which is good pinning hygiene.
- **Wan 2.7 is real** — Alibaba's own SDK lists `wan2.7-t2v`, `wan2.7-i2v`, `wan2.7-image-pro`.
- **ElevenLabs v3, OmniHuman v1.5, Ideogram V3, Kling v3, FLUX.2 [pro], Marey** — all present on
  fal at the selected version.
- **Its instinct about Google's prices** — re-fetched today and they match.

## What did not survive verification

**Eight EVAL-008 claims are not supported by any provider-authorised source we could reach.**
Most concern fal, and they matter because EVAL-008 routed most of the roster through fal.

| Claim | What the provider's own material shows |
|---|---|
| GPT Image 2 is on fal | fal's client enumerates `gpt-image-1`, `-1-mini`, `-1.5` — **no gpt-image-2** |
| Seedance 2.0 is on fal, live April 2026 | highest enumerated is `seedance/v1.5/pro` |
| HappyHorse 1.1 on fal — "best-evidenced fal row" | **zero** happyhorse endpoints in fal's client |
| MiniMax H3 has a dedicated fal page | highest enumerated is `hailuo-2.3` |
| Sync-3 is on fal | highest enumerated is `sync-lipsync/v2/pro` |
| Reve 2.1 model page on fal | no reve endpoint at all |
| Gemini Omni on fal | no omni endpoint |
| Runway API is Enterprise-only since Jan 2026 | Runway's own SDK exposes the full public API including `aleph2` |

**And per the Controller's explicit instruction:** the reported **~99% Hindi/Bengali character
accuracy** attributed to OpenAI is **rejected as unverified**. No primary source was reachable and
no provider artifact carries such a figure. It is unevidenced, not disproven — but it must not be
load-bearing for anything.

---

## Ambiguities EVAL-008 flagged, now resolved

This is where the SDK evidence paid off.

- **FLUX.2 [klein] — 4B or 9B?** **Both.** fal enumerates `flux-2-klein-4b-base-trainer` *and*
  `flux-2-klein-9b-base-trainer`. Two distinct models, not a reporting error.
- **LTX-2 — 2.0, 2.3 or 2.5?** Resolves to a concrete family: **`ltx-2-19b`**, with base,
  distilled and LoRA variants.
- **Wan — 2.6 or 2.7?** **2.7**, confirmed independently by Alibaba's SDK and fal.
- **Qwen-Image — is `Qwen-Image-2512` current?** Both exist and they are different. Alibaba's own
  current id is **`qwen-image-2.0-pro`**; `qwen-image-2512` is an older build fal still carries.
- **Does Veo 3.1 support first/last-frame and extend controls?** **Yes.** EVAL-008 could not tell,
  because Google's price table lists advanced controls only under Veo 2. Google's own SDK carries
  `last_frame`, typed `reference_images` and four video mask modes, and fal exposes
  `veo3.1/first-last-frame-to-video` and `veo3.1/extend-video` as endpoints.
- **Nano Banana Pro's price** — EVAL-008 recorded it as unverified because the table cell was
  blank. **The price is in the footnote:** $0.134 at 1K/2K, $0.24 at 4K. Its *identity* is what is
  actually missing, not its price.

## New ambiguities this task found

- **GPT Image 2 has a pinnable snapshot.** `gpt-image-2` is a floating alias;
  **`gpt-image-2-2026-04-21`** is the dated version. Pin the snapshot — a floating alias makes
  every measurement provisional.
- **Veo 3.1's full tier only appears as `veo-3.1-generate-preview`** in Google's own SDK, while
  the Lite tier has a stable `-001` id. A GA id may exist; we could not reach the catalogue.
- **Marey's endpoints carry no version at all** (`moonvalley/marey/t2v`), so "V1.5" cannot be
  pinned through that route.
- **Runway is itself an aggregator** — it exposes `veo3.1`, `veo3.1_fast`, `hailuo3` and
  `gpt_image_2` alongside its own models. That creates alternative routes and route-equivalence
  risk in equal measure.

---

## Two findings that should shape the measurement design

**1. Reproducibility is not available everywhere, and that breaks a threshold.**

Twelve verified routes expose a `seed`. Seven do not — including **OpenAI's image API**, which has
no seed parameter on either generate or edit, and **Kling v3 text-to-video**.

The project has a proposed **0.95 repeat-consistency threshold**. On a seeded route that measures
variance *under a held seed*. On an unseeded route it can only measure *inherent* variance. **These
are different quantities**, and comparing them would be a category error. Sarvam vs ElevenLabs is
the sharpest case: ElevenLabs exposes `seed`, Sarvam exposes `temperature` — so the most
product-relevant voice comparison on the list is not currently like-for-like.

**2. Wrappers are thinner than they look, and the gaps land on our hardest problem.**

fal's ElevenLabs wrapper omits `seed`, `pronunciation_dictionary_locators` and the
previous/next-text continuity controls that ElevenLabs direct exposes. The pronunciation dictionary
is precisely the mechanism for forcing correct Indian brand-name pronunciation. **A voice
measurement taken through fal cannot test the thing we most need to test.**

Sarvam direct, by contrast, exposes a dedicated pronunciation-dictionary resource and a `dict_id`
parameter — a genuinely relevant control that no summary had surfaced.

Full detail in `WORKFLOW-CONTROL-MATRIX.yaml` and `ROUTE-EQUIVALENCE-RISKS.md`.

---

## What this task did not do

- It did not choose models. EVAL-009 does that, and this file must not be read as a roster.
- It did not run anything, create anything, or spend anything.
- It did not resolve **Frontier Clouds**, and did not guess — see `FRONTIER-CLOUDS-CHECKLIST.md`.
- It did not produce a budget. `BUDGET-INPUTS.yaml` holds verified prices for Google only and keeps
  nominal cost strictly separate from cash-outlay-after-credits, which remains unresolved.

**This supply table is partial and is described as partial.** Two rows are execution-ready out of
twenty-six. Anyone reading it as a green light has read it wrong.
