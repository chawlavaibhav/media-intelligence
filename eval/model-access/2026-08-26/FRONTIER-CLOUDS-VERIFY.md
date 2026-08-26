# E8-C — Frontier Clouds: not identified, verification list instead

**Task:** EVAL-008 · **Date:** 26 Aug 2026
**Status: BLOCKED ON IDENTITY — this is the outcome the task file anticipated and permits.**
**0 API calls · ₹0 spent · no account created · no terms accepted.**

---

## What happened, in one paragraph

The user has credits on a service they call **Frontier Clouds** and that is the route we
would prefer to use. **We could not establish what that service publicly is.** Three
independent web searches — for the exact phrase, for the singular variant, and for
"frontier"-named credit programmes aimed at Indian startups — returned no service by that
name. They returned neighbours that are *not* it: several unified media-model API platforms
with different names, several startup-credit directories, and a lot of ordinary use of the
word "frontier" as an adjective for frontier models.

The task file is explicit about what to do here, and we did exactly that: **do not guess, do
not substitute a provider because its name sounds similar, finish the roster anyway, and
leave a compact list of what to check once the real catalogue is in hand.** The user's
literal service name is preserved throughout.

**What this does not mean.** It does not mean the service does not exist. Private or
regional platforms, reseller portals, enterprise marketplaces and internal credit programmes
are frequently not indexed under the name a customer knows them by. The most likely
explanations are simply that it is not publicly indexed under that exact name, or that the
name the user remembers differs slightly from the registered one.

---

## What we searched, and what came back

| Query | Result |
|---|---|
| `"Frontier Clouds" AI model inference platform credits` | No match. Returned FriendliAI, CLōD, Cerebras, Inference.net, Mistral. |
| `"Frontier Cloud" OR "frontiercloud" image video generation model API platform` | No match. Returned Atlas Cloud, Pixazo, SiliconFlow, Apiframe, and fal described as serving "frontier open models". |
| `"Frontier" cloud credits programme, India, generative media API credits 2026` | No match. Returned Google Cloud for Startups, AWS GenAI Spotlight, Runware's grant programme, and general credit directories. |

**None of these was treated as a candidate identification, and none should be.** They are
recorded only to show the search was genuine and to save the next session from repeating it.

**A second, independent blocker also applies.** Even with the correct name, this session
could not have verified the catalogue: the network policy answered `403` to essentially
every vendor and platform domain we probed (37 probed, 1 reachable — `cloud.google.com`).
So Frontier Clouds verification needs **two** things: the exact service identity, and an
environment that can reach it.

---

## What the Controller needs to supply

One of these is enough to unblock the whole pass:

1. **The service URL** — the address the user actually signs in at; or
2. **The catalogue or model-list page**, however it is reached; or
3. **A screenshot of the model list**, which is sufficient for a first cut; or
4. **The invoice, dashboard header or console name**, which usually carries the registered
   legal name even when the informal name differs.

We are explicitly **not** asking for credentials, API keys, or anything that would require
accepting terms. Availability is a catalogue question, not an access question.

---

## The verification list — 26 rows to check against that catalogue

These are the Must and Should rows from `MODEL-ROSTER-FIRST.md`, unchanged. The roster was
frozen in an earlier commit; nothing on this page was allowed to alter it.

For each row, four questions, in this order:

- **A. Is the model in the catalogue at all?**
- **B. Is it the *same version* we selected?** (a family name is not a version)
- **C. Which operations does it expose?** (generate / edit / reference-condition / extend — a
  route that only does text-to-image cannot serve an editing hypothesis)
- **D. Can the version be pinned?** An endpoint that silently changes model underneath us
  makes every measurement provisional, because a Registry row can go stale with no signal.

| # | Model to check | Selected version | Operations the hypothesis needs |
|---:|---|---|---|
| 1 | GPT Image 2 | `gpt-image-2` | text-to-image, edit |
| 2 | Nano Banana 2 | Gemini 3.1 Flash Image | text-to-image, edit, reference |
| 3 | Seedream 5.0 Pro | 5.0 Pro (**or 4.5 — confirm which**) | text-to-image, edit, reference |
| 4 | Reve 2.1 | 2.1 | text-to-image, **region/element edit** |
| 5 | FLUX.2 [pro] | `[pro]` specifically | text-to-image, instruction edit |
| 6 | Qwen-Image / Qwen-Image-Edit | Qwen-Image-2512 | text-to-image, instruction edit |
| 7 | Seedance 2.0 Pro | 2.0 Pro | text-to-video, image-to-video, native audio |
| 8 | Seedance 2.0 Fast | 2.0 Fast | text-to-video, image-to-video |
| 9 | HappyHorse 1.1 | 1.1 (**and whether 1.0 is separately listed**) | t2v, i2v, reference-to-video, video-edit |
| 10 | Veo 3.1 | 3.1, and its Fast and Lite tiers | t2v, i2v, native audio, **advanced frame/extend controls** |
| 11 | Kling 3.0 | 3.0 Pro | t2v, i2v, elements, native audio, multi-shot |
| 12 | MiniMax H3 | H3 / Hailuo 03 | **omni-reference (9 images / 3 video / 3 audio)**, V2V |
| 13 | Runway Aleph 2.0 | 2.0 | **video-to-video edit with keyframes** |
| 14 | Sarvam Bulbul v3 | v3 | text-to-speech, Hindi + Hinglish |
| 15 | ElevenLabs v3 | Eleven v3 | text-to-speech |
| 16 | Sync-3 | Sync-3 | lip-sync (video + audio in) |
| 17 | Nano Banana Pro | Gemini 3 Pro Image | text-to-image, edit |
| 18 | MAI-Image-2.5-Pro | 2.5 Pro | edit (primary), text-to-image |
| 19 | Ideogram V3 | V3, and which of Turbo/Default/Quality | text-to-image |
| 20 | Recraft V3 | V3 | text-to-image, **native SVG output** |
| 21 | FLUX.2 [klein] | `[klein]` (**4B or 9B — confirm**) | text-to-image |
| 22 | Gemini Omni Flash | Omni Flash | video generate **and conversational edit** |
| 23 | Wan 2.7 | 2.7 (**or 2.6 — confirm, with licence**) | t2v, i2v |
| 24 | LTX-2 | which of 2.0 / 2.3 / 2.5 | t2v, **native audio** |
| 25 | Marey Realism V1.5 | V1.5 | t2v, i2v, motion transfer |
| 26 | OmniHuman v1.5 | v1.5 | image + audio → video |

---

## Two catalogue-level questions worth asking at the same time

Both are cheap to answer while looking and expensive to discover later.

**1. Is it a first-party host or a reseller?** If Frontier Clouds resells another
platform's endpoints, then its version pinning, controls and reliability are inherited from
that platform, not chosen by it. That matters because a Registry row must name the thing
that actually ran the generation.

**2. Do the credits cover media generation, or only text models?** Many credit grants are
scoped to language models and silently exclude image and video generation, which is where
essentially all of our cost sits. If the credits do not cover media, the entire sourcing
preference collapses to fal and direct — and it is much better to learn that before a budget
is approved than after.

---

## What this blocker does and does not stop

**Does not stop:** the model roster, which is complete and frozen. The fal pass. The direct
sourcing pass. The execution map. The account-action list, which is complete in every bucket
except the one that depends on this answer.

**Does stop:** any statement about which selected models the user's existing credits already
cover — and therefore any claim about what the first paid wave would actually cost.

**Estimated effort once the URL is known:** this is a lookup against 26 named rows, not
research. On a network that can reach the catalogue it is well under an hour.
