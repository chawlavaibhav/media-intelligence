# E8-F — Source-optimized execution map

**Task:** EVAL-008 · **Date:** 26 Aug 2026
**Rows are models. Providers are columns.** The roster was frozen before this page existed.
**0 API calls · ₹0 spent · no account created · no Registry row.**

---

## The rule this map applies, mechanically

The user's route preference, applied as an algorithm and nothing more:

1. If the **equivalent selected version** is on Frontier Clouds → prefer Frontier Clouds.
2. Otherwise, if the **equivalent selected version** is on fal → prefer fal.
3. Otherwise → source the selected model directly or from the best legitimate provider.

The words **"equivalent selected version"** are doing real work. A route only wins if it
carries the version we chose. A different version of the same family is a different model for
our purposes, and routing to it would quietly change what we measure.

**Step 1 cannot be evaluated in this pass.** Frontier Clouds could not be identified, so every
row's Frontier Clouds cell reads `UNRESOLVED`. That is a gap in the *route*, not in the roster.
When the catalogue arrives, the preferred column may shift left for many rows — and **only the
route changes; no row is added, removed or reprioritised.**

Column meanings: **Preferred** = the best route we can currently justify · **Fallback** = the
next route if the preferred fails or fails version-pinning · **Last resort** = what we would do
rather than drop the row · **Account action** = the one-line consequence for the user.

---

## Must-test rows

| # | Model | Frontier Clouds | Preferred | Fallback | Last resort | Account action |
|---:|---|---|---|---|---|---|
| 1 | GPT Image 2 | UNRESOLVED | **fal** (`openai/gpt-image-2`, T2) | OpenAI API direct (`gpt-image-2`) | — | None if fal confirms |
| 2 | Nano Banana 2 | UNRESOLVED | **Google Vertex AI** — the only T1-verified identity + price we hold | fal (version exposure unresolved) | Gemini API (no enterprise SLA) | Google Cloud account, unless Frontier Clouds is Google |
| 3 | Seedream 5.0 Pro | UNRESOLVED | **fal** (family confirmed, version not) | BytePlus ModelArk direct | — | None if fal confirms the version |
| 4 | Reve 2.1 | UNRESOLVED | **fal** (model page seen, T2) | Reve API direct | — | None if fal confirms |
| 5 | FLUX.2 [pro] | UNRESOLVED | **fal** — *only if the `[pro]` variant specifically is exposed* | Black Forest Labs direct | — | BFL account if fal exposes only other variants |
| 6 | Qwen-Image / -Edit | UNRESOLVED | **fal** (not verified either way) | Alibaba Cloud model service | Self-host on open weights | GPU account **only if** we test self-host economics — which is a *separate hypothesis*, see below |
| 7 | Seedance 2.0 Pro | UNRESOLVED | **fal** (dedicated page, T2) | BytePlus ModelArk | — | None if fal confirms |
| 8 | Seedance 2.0 Fast | UNRESOLVED | **fal** (T3 only) | BytePlus ModelArk | — | None if fal confirms |
| 9 | HappyHorse 1.1 | UNRESOLVED | **fal** — best-evidenced row on the page; fal was the launch developer route | Alibaba direct (unverified) | — | None |
| 10 | Veo 3.1 (+Fast, +Lite) | UNRESOLVED | **Google Vertex AI** — T1 prices for all three tiers; the cost-ladder experiment needs exactly these | fal (Veo 3.1 and Lite reported) | Gemini API | Google Cloud account, unless Frontier Clouds is Google |
| 11 | Kling 3.0 | UNRESOLVED | **fal** (`Kling 3.0 Pro`, elements + native audio, T2) | Kling direct | — | None if fal confirms |
| 12 | MiniMax H3 | UNRESOLVED | **fal** (dedicated page, T2) | MiniMax platform direct | Self-host, *if* open weights is true | None; resolve the open-weights contradiction first |
| 13 | **Runway Aleph 2.0** | UNRESOLVED | **Runway API direct** — not seen on fal | Adobe Firefly (**materially different wrapper** — a product surface, not an API) | — | **NEW ACCOUNT LIKELY, and possibly an enterprise conversation** |
| 14 | **Sarvam Bulbul v3** | UNRESOLVED | **Sarvam API direct** — not seen on fal | — | — | **NEW ACCOUNT REQUIRED.** Indian vendor, rupee billing, ₹30/10k chars in beta |
| 15 | ElevenLabs v3 | UNRESOLVED | **fal** (`fal-ai/elevenlabs/tts/eleven-v3`, T2) | ElevenLabs direct | — | None if fal confirms |
| 16 | Sync-3 | UNRESOLVED | **fal** (`Sync-3`, T2) | sync.so direct | — | None if fal confirms |

## Should-test rows

| # | Model | Frontier Clouds | Preferred | Fallback | Last resort | Account action |
|---:|---|---|---|---|---|---|
| 17 | Nano Banana Pro | UNRESOLVED | **Google Vertex AI** (T1 identity; image price NOT VERIFIED) | fal | Gemini API | Same Google account as rows 2 and 10 |
| 18 | **MAI-Image-2.5-Pro** | UNRESOLVED | **Microsoft — route NOT VERIFIED**, most plausibly Azure AI Foundry | — | — | **Unknown. Establish the route before promising the row** |
| 19 | Ideogram V3 | UNRESOLVED | **fal** (T2) | Ideogram direct | — | None if fal confirms |
| 20 | Recraft V3 | UNRESOLVED | **Recraft direct** — native SVG output may exist only there, and the format *is* the hypothesis | fal (T3) | — | Recraft account if fal cannot emit SVG |
| 21 | FLUX.2 [klein] | UNRESOLVED | **Self-host** (Apache-2.0 claimed) — hosting it is the point | fal, if exposed | BFL direct | GPU account, shared with row 6 |
| 22 | Gemini Omni Flash | UNRESOLVED | **Google Vertex AI** (T1 price; ≈$0.101/sec derived) | fal ("Gemini Omni" listed) | Gemini API | Same Google account |
| 23 | Wan 2.7 | UNRESOLVED | **fal** — *pin 2.6 vs 2.7 first* | Alibaba Cloud | Self-host | None; version risk |
| 24 | LTX-2 | UNRESOLVED | **fal** — fal's page says **2.3**; pin before use | Lightricks direct | Self-host | None; version risk |
| 25 | Marey Realism V1.5 | UNRESOLVED | **fal** — three separate endpoints (t2v / i2v / motion-transfer) | Moonvalley direct | Adobe Firefly | None if fal confirms |
| 26 | OmniHuman v1.5 | UNRESOLVED | **fal** (`fal-ai/bytedance/omnihuman`, T2) | BytePlus | — | None if fal confirms |

---

## Where the route materially changes the workflow — flag, don't silently equate

The task requires these be flagged for later route-equivalence testing rather than treated as
the same thing. Four cases, in order of how much they matter:

**1. Runway Aleph 2.0 — API versus Adobe Firefly.** These are not two prices for one thing.
The API is programmable and chainable; Firefly Boards is a human-operated creative surface. A
Capability Lab measurement taken through a product UI is not comparable to one taken through
an API, and it cannot be automated. If the API route is genuinely enterprise-gated, **the honest
options are to pursue enterprise access or to record the row as unmeasurable — not to quietly
substitute the product.**

**2. Google — Vertex AI versus the Gemini API.** Google's own page says Vertex is backed by the
enterprise SLA and the Gemini API is not. Same model, different reliability and probably
different quota behaviour. For measurement, pick one and stay on it; mixing them inside one
Registry row would make the row mean two things.

**3. Aggregator wrapper versus vendor endpoint, generally.** Wherever a model is reachable both
on fal and directly — which is most of the roster — the wrapper may expose fewer controls, a
different default resolution, or a floating rather than pinned version. **This is measurable and
worth measuring once**, on one well-understood model, rather than being assumed away on all of
them. Recommended probe: run the same items through fal and through the vendor for **Veo 3.1**,
because it is the row where we hold T1 prices and identities on the direct side and so can tell
exactly what the wrapper changed.

**4. Hosted open weights versus self-hosted open weights.** Running Qwen-Image, FLUX.2 [klein],
Wan or LTX **on fal is not the open-economics test** — it is the same convenience economics as
any other fal row. The hypothesis those rows carry is *what it costs us to own the step*, and
answering it requires our own GPU. Using the hosted route and reporting it as open economics
would be a quiet substitution of the question. Two legitimate ways forward: run the hosted route
for **capability** and a separate small self-host study for **economics**, or defer the economics
question until capability justifies it.

---

## What this map is worth right now

**Directionally reliable, operationally not yet actionable.**

- Roughly **twenty of twenty-six rows** point at fal as the preferred route, which is the outcome
  the user's stated preference was designed to produce — and it was produced without any row being
  selected because fal carries it.
- **Four Google rows** are the only ones whose preferred route we can defend with documentation we
  read ourselves.
- **Three rows** (Runway Aleph, Sarvam Bulbul, MAI-Image) need something new, and one of those three
  is a Must row with a possible enterprise gate.
- **Every fal cell is T2 at best**, so the whole middle column is a plan, not a fact.

The single change that would most improve this map is not more research — it is **the Frontier
Clouds catalogue**, which could move a large number of rows into a route the user has already paid
for. The second is **an environment that can reach provider documentation**, which turns every T2
cell into a T1 cell in a few hours of lookup.
