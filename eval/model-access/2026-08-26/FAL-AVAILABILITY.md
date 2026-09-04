# E8-D — fal fallback pass

**Task:** EVAL-008 · **Date:** 26 Aug 2026
**Status: INDICATIVE, NOT VERIFIED.** Useful for planning; not sufficient to authorise spend.
**0 API calls · ₹0 spent · no account created · no terms accepted.**

---

## Read this first — how much this page can be trusted

**`fal.ai` and `docs.fal.ai` were both unreachable from this session** (the network policy
answered `403`). So no fal endpoint page was opened directly, and **no line below is a
verified endpoint identity**.

What we do have is better than nothing and worse than documentation: a web-search tool read
**fal's own pages** — model pages under `fal.ai/models/...`, landing pages, and fal's own
`learn/` and `blog.fal.ai` articles — and summarised them. That is fal describing fal, which
is the right source; we simply could not read it ourselves. Call it **T2** evidence, in the
tiering used throughout this task.

**What T2 is good for:** deciding that a model is *probably* on fal, and planning around it.
**What T2 is not good for:** the exact endpoint id, the exact model version behind it, the
controls it exposes, or the price. Those decide whether a measurement means anything, and
they need the catalogue.

**Consequence for the roster: none.** The task forbids swapping a selected model for a fal
alternative just because the selected one is absent, and nothing here changed a single row.

Also relevant: fal reportedly exposes a **model search API** at `docs.fal.ai/platform-apis/v1/models`
(T2). If that is real and unauthenticated, the entire verification below becomes one scripted
call from a machine that can reach fal — worth trying first.

---

## The four verdicts this pass must distinguish

The task requires we separate these, and they carry very different consequences:

- **`exact_selected_version`** — the version we chose, present on fal.
- **`same_family_different_version`** — the family is there but the version differs. **This is
  not a substitute.** Measuring a different version produces a Registry row about a model we
  did not select.
- **`materially_different_wrapper`** — present, but the route changes the workflow: fewer
  controls, a fixed resolution, a bundled pipeline. Flag for route-equivalence testing.
- **`unavailable` / `not_verified`** — and we distinguish these two carefully. **"We did not
  see it" is not "it is not there."** Given we could not read the catalogue, almost everything
  we did not find is `not_verified`, not `unavailable`.

---

## Must-test rows

| # | Selected model | Seen on fal? | What fal's own pages say | Verdict | Confidence |
|---:|---|---|---|---|---|
| 1 | GPT Image 2 | Yes | Model page `fal.ai/models/openai/gpt-image-2`, described as OpenAI's latest image model, "extremely detailed images with fine typography" | `exact_selected_version` (version string unconfirmed) | T2 |
| 2 | Nano Banana 2 | Family yes | "Nano Banana" listed as Google's SOTA image generation and editing model; a fal explainer page compares Nano Banana Pro vs Nano Banana 2, implying both are known there | **`same_family_different_version` risk — which tier is exposed is NOT VERIFIED** | T2, low |
| 3 | Seedream 5.0 Pro | Family yes | Seedream listed among fal's image models; one summary named "Seedream 5.0" | version NOT VERIFIED | T2, low |
| 4 | Reve 2.1 | Yes | Model page describes Reve 2.1: "strong prompt adherence, layout intelligence, and accurate text rendering" | `exact_selected_version` | T2 |
| 5 | FLUX.2 [pro] | Family yes | FLUX 2 listed; a third-party summary named Flux 2 Pro/Dev/Schnell tiers on fal | **which variants are exposed NOT VERIFIED** — and the variant is the whole point | T2, low |
| 6 | Qwen-Image / Qwen-Image-Edit | Not seen | — | `not_verified` (fal hosts many open models; absence here is our blindness, not evidence) | — |
| 7 | Seedance 2.0 Pro | Yes | fal has a dedicated `fal.ai/seedance-2.0` page: "API live on fal (April 2026)", cinematic video with native audio, real-world physics, camera control | `exact_selected_version` | T2 |
| 8 | Seedance 2.0 Fast | Probably | A third-party summary lists "Seedance 2.0 (Fast + Pro)" on fal | `not_verified` | T3 |
| 9 | HappyHorse 1.1 | Yes | fal published `fal.ai/learn/devs/happyhorse-1-0-...`; developer/enterprise API access went live **27 April 2026 through fal** with four endpoints — text-to-video, image-to-video, reference-to-video, video-edit. A later fal page lists "Happy Horse 1.1" | `exact_selected_version` — **and this is the best-evidenced fal row on the page** | T2 |
| 10 | Veo 3.1 | Yes | Listed on fal's video tooling page as "Google's most advanced AI video generation model"; a third-party summary adds "Veo 3.1 Lite" | `exact_selected_version` | T2 |
| 11 | Kling 3.0 | Yes | "Kling 3.0 Pro — top-tier image-to-video with cinematic visuals, fluid motion, native audio generation, with custom element support" | `exact_selected_version` | T2 |
| 12 | MiniMax H3 | Yes | Dedicated page `fal.ai/minimax-h3`: "one context for text, images, video and audio, producing 2K video with native stereo audio", described there as **open-weights** | `exact_selected_version`, but the open-weights description conflicts with other sources — resolve it | T2 |
| 13 | Runway Aleph 2.0 | **Not seen** | Searching fal's domain for Aleph returned nothing | `not_verified`, leaning unavailable — Runway has historically sold its own API | — |
| 14 | Sarvam Bulbul v3 | **Not seen** | Searching fal's domain for Sarvam returned nothing; fal's TTS surface that we saw is ElevenLabs-centric | `not_verified`, leaning unavailable | — |
| 15 | ElevenLabs v3 | Yes | Model pages `fal-ai/elevenlabs/tts/eleven-v3` and `.../text-to-dialogue/eleven-v3`; fal published a blog post on the ElevenLabs audio suite; v3 stated as 70+ languages, with Multilingual v2 (29) and Turbo v2.5 also present | `exact_selected_version` | T2 |
| 16 | Sync-3 | Yes | "Sync-3 — the most powerful lipsync model yet, native visual intelligence"; Sync Lipsync 2.0 also listed | `exact_selected_version` | T2 |

## Should-test rows

| # | Selected model | Seen on fal? | Note | Verdict |
|---:|---|---|---|---|
| 17 | Nano Banana Pro | Family yes | fal's own comparison page names it | version exposure `not_verified` |
| 18 | MAI-Image-2.5-Pro | **Not seen** | No Microsoft image model surfaced on fal | `not_verified`, leaning unavailable |
| 19 | Ideogram V3 | Yes | "high-quality images, posters and logos with exceptional typography, optimised for commercial and creative use" | `exact_selected_version` |
| 20 | Recraft V3 | Probably | A third-party summary lists Recraft V3 among fal image models | `not_verified` |
| 21 | FLUX.2 [klein] | Not seen separately | FLUX 2 family present; the `[klein]` variant specifically was not surfaced | `not_verified` |
| 22 | Gemini Omni Flash | Yes | Listed among fal's frontier video models as "Gemini Omni" | `exact_selected_version` (tier naming unconfirmed) |
| 23 | Wan 2.7 | Yes | "Wan 2.7 is the latest generation AI video model — enhanced motion smoothness, superior scene fidelity, greater visual coherence"; a separate summary named Wan 2.6 | **`same_family_different_version` risk — 2.6 and 2.7 both appear** |
| 24 | LTX-2 | Yes | Dedicated page `fal.ai/ltx-2.3`: "open-source 4K video generation with native audio, up to 20 seconds, LoRA fine-tuning" | present, but **fal's page says 2.3 while our roster says "LTX-2, version TBD"** — pin it |
| 25 | Marey Realism V1.5 | Yes | Three distinct endpoints: `moonvalley/marey/t2v`, `/i2v`, `/motion-transfer`; described as the first commercially-safe model trained exclusively on licensed data | `exact_selected_version`, and **the three-endpoint split matters** — motion-transfer is the video-edit operation |
| 26 | OmniHuman v1.5 | Yes | `fal-ai/bytedance/omnihuman` — image of a human plus an audio file, emotions and movement correlated to the audio | `exact_selected_version` |

---

## Summary — what fal appears to cover

| Verdict | Count | Rows |
|---|---:|---|
| Exact selected version, T2 evidence | **13** | Must: GPT Image 2, Reve 2.1, Seedance 2.0 Pro, HappyHorse 1.1, Veo 3.1, Kling 3.0, MiniMax H3, ElevenLabs v3, Sync-3 (**9 of 16**). Should: Ideogram V3, Gemini Omni Flash, Marey V1.5, OmniHuman v1.5 (**4 of 10**) |
| Present, version or variant unresolved | 7 | Nano Banana 2, Nano Banana Pro, Seedream 5.0, FLUX.2 [pro], Seedance 2.0 Fast, Wan 2.7, LTX-2 |
| Not seen, leaning unavailable | 3 | **Runway Aleph 2.0, Sarvam Bulbul v3, MAI-Image-2.5-Pro** |
| Not verified either way | 3 | Qwen-Image, Recraft V3, FLUX.2 [klein] |

**The headline for planning:** fal plausibly covers the large majority of the roster,
including nine of the sixteen Must rows with model-page-level evidence. **Three selected
models look genuinely absent**, and those three are what drive the new-account question in
`ACCOUNT-ACTIONS.md`.

---

## Two route facts worth carrying forward

**Pricing model.** fal reportedly charges **per generation or per GPU-second, with no
subscription** (T2/T3). Per-generation billing is materially better for a Capability Lab than
a subscription: cost attaches to the trial, which is exactly the unit Cost-per-Accepted-Outcome
is computed over. Specific rates seen (H100 $1.89/h, A100 $0.99/h, per-image and per-second
model rates) are **T3 and must not be used for a budget.**

**One key, one bill, many vendors.** fal runs every model behind a single key and account.
That is an operational advantage worth stating plainly: one signup covers most of the roster,
which is why it sits above new direct accounts in the user's preference order.

**And one caution.** An aggregator's wrapper can differ from the vendor's own endpoint — fewer
controls, a different default resolution, a pinned or floating version. Where a model is
reachable both on fal and directly, that difference is itself a measurable thing and is
flagged for **route-equivalence testing** in the execution map rather than assumed away.
