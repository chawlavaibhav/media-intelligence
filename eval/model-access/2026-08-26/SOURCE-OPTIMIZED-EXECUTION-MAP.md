# E8-F — Source-optimized execution map

**Task:** EVAL-008 · **Date:** 26 Aug 2026
**Rows are models. Providers are columns.** The roster was frozen before this page existed.
**Updated 26 Aug 2026:** Frontier Clouds resolved to GCP + AWS + Azure, so the Frontier Clouds
column is now filled. Seven rows moved to a route the user already pays for. **No roster row
changed.**
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

**Step 1 is now evaluable.** The Controller resolved Frontier Clouds to the three hyperscalers,
and `FRONTIER-CLOUDS-AVAILABILITY.md` records the pass: **7 of 26 rows covered** — four on Google
Cloud at verified prices, three on Azure, **none on AWS Bedrock**. Those seven rows have moved
left into the preferred column. **Only routes changed; no row was added, removed or
reprioritised.** The remaining 19 rows keep the fal-then-direct routing below.

**One counting rule applied deliberately.** The four open-weight rows (Qwen-Image, FLUX.2
[klein], Wan 2.7, LTX-2) can be *run on* hyperscaler GPUs, but that is renting compute, not a
catalogue model — a different purchase, and the very thing those rows exist to measure. They are
counted as **not covered**.

Column meanings: **Preferred** = the best route we can currently justify · **Fallback** = the
next route if the preferred fails or fails version-pinning · **Last resort** = what we would do
rather than drop the row · **Account action** = the one-line consequence for the user.

---

## Must-test rows

| # | Model | Frontier Clouds | Preferred | Fallback | Last resort | Account action |
|---:|---|---|---|---|---|---|
| 1 | GPT Image 2 | **Azure Foundry — `gpt-image-2` listed** | **Azure Foundry** (existing credits) | fal (`openai/gpt-image-2`) | OpenAI API direct | **None — existing Azure access** |
| 2 | Nano Banana 2 | **GCP Vertex — T1 verified** | **GCP Vertex AI** (existing credits) | fal (version unresolved) | Gemini API (no enterprise SLA) | **None — existing GCP access** |
| 3 | Seedream 5.0 Pro | Not on GCP/AWS/Azure | **fal** (family confirmed, version not) | BytePlus ModelArk direct | — | None if fal confirms the version |
| 4 | Reve 2.1 | Not on GCP/AWS/Azure | **fal** (model page seen, T2) | Reve API direct | — | None if fal confirms |
| 5 | FLUX.2 [pro] | **Azure Foundry — FLUX 2 Pro deployable** | **Azure Foundry** (existing credits) | fal, if `[pro]` is exposed | BFL direct | **None — existing Azure access** |
| 6 | Qwen-Image / -Edit | Not on GCP/AWS/Azure | **fal** (not verified either way) | Alibaba Cloud model service | Self-host on open weights | GPU account **only if** we test self-host economics — which is a *separate hypothesis*, see below |
| 7 | Seedance 2.0 Pro | Not on GCP/AWS/Azure | **fal** (dedicated page, T2) | BytePlus ModelArk | — | None if fal confirms |
| 8 | Seedance 2.0 Fast | Not on GCP/AWS/Azure | **fal** (T3 only) | BytePlus ModelArk | — | None if fal confirms |
| 9 | HappyHorse 1.1 | Not on GCP/AWS/Azure | **fal** — best-evidenced row on the page; fal was the launch developer route | Alibaba direct (unverified) | — | None |
| 10 | Veo 3.1 (+Fast, +Lite) | **GCP Vertex — T1, all three tiers priced** | **GCP Vertex AI** (existing credits) | fal (3.1 and Lite reported) | Gemini API | **None — existing GCP access** |
| 11 | Kling 3.0 | Not on GCP/AWS/Azure | **fal** (`Kling 3.0 Pro`, elements + native audio, T2) | Kling direct | — | None if fal confirms |
| 12 | MiniMax H3 | Not on GCP/AWS/Azure | **fal** (dedicated page, T2) | MiniMax platform direct | Self-host, *if* open weights is true | None; resolve the open-weights contradiction first |
| 13 | **Runway Aleph 2.0** | Not on GCP/AWS/Azure | **Runway API direct** — not seen on fal | Adobe Firefly (**materially different wrapper** — a product surface, not an API) | — | **NEW ACCOUNT LIKELY, and possibly an enterprise conversation** |
| 14 | **Sarvam Bulbul v3** | Not on GCP/AWS/Azure | **Sarvam API direct** — not seen on fal | — | — | **NEW ACCOUNT REQUIRED.** Indian vendor, rupee billing, ₹30/10k chars in beta |
| 15 | ElevenLabs v3 | Not on GCP/AWS/Azure | **fal** (`fal-ai/elevenlabs/tts/eleven-v3`, T2) | ElevenLabs direct | — | None if fal confirms |
| 16 | Sync-3 | Not on GCP/AWS/Azure | **fal** (`Sync-3`, T2) | sync.so direct | — | None if fal confirms |

## Should-test rows

| # | Model | Frontier Clouds | Preferred | Fallback | Last resort | Account action |
|---:|---|---|---|---|---|---|
| 17 | Nano Banana Pro | **GCP Vertex — T1 identity; image price NOT VERIFIED** | **GCP Vertex AI** (existing credits) | fal | Gemini API | **None — existing GCP access** |
| 18 | **MAI-Image-2.5-Pro** | **Azure Foundry — released 23 Jul 2026, South India region** | **Azure Foundry** (existing credits) | — | — | **None — existing Azure access.** Was "no route evidenced"; resolved by the Frontier Clouds identity |
| 19 | Ideogram V3 | Not on GCP/AWS/Azure | **fal** (T2) | Ideogram direct | — | None if fal confirms |
| 20 | Recraft V3 | Not on GCP/AWS/Azure | **Recraft direct** — native SVG output may exist only there, and the format *is* the hypothesis | fal (T3) | — | Recraft account if fal cannot emit SVG |
| 21 | FLUX.2 [klein] | Not on GCP/AWS/Azure | **Self-host** (Apache-2.0 claimed) — hosting it is the point | fal, if exposed | BFL direct | GPU account, shared with row 6 |
| 22 | Gemini Omni Flash | **GCP Vertex — T1, ≈$0.101/sec derived** | **GCP Vertex AI** (existing credits) | fal ("Gemini Omni" listed) | Gemini API | **None — existing GCP access** |
| 23 | Wan 2.7 | Not on GCP/AWS/Azure | **fal** — *pin 2.6 vs 2.7 first* | Alibaba Cloud | Self-host | None; version risk |
| 24 | LTX-2 | Not on GCP/AWS/Azure | **fal** — fal's page says **2.3**; pin before use | Lightricks direct | Self-host | None; version risk |
| 25 | Marey Realism V1.5 | Not on GCP/AWS/Azure | **fal** — three separate endpoints (t2v / i2v / motion-transfer) | Moonvalley direct | Adobe Firefly | None if fal confirms |
| 26 | OmniHuman v1.5 | Not on GCP/AWS/Azure | **fal** (`fal-ai/bytedance/omnihuman`, T2) | BytePlus | — | None if fal confirms |

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

## What this map is worth now

**Directionally reliable; one quarter of it is operationally solid.**

- **7 of 26 rows sit on credits the user already holds** — 4 on Google Cloud with prices we read
  ourselves, 3 on Azure. That is the preference ladder doing its job.
- **AWS Bedrock contributes nothing.** It carries none of the roster, and its own media models
  (Nova Canvas, Nova Reel) are Legacy, Canvas with an end-of-life of 30 Sep 2026. Credits weighted
  toward AWS are worth far less to this programme than a headline total implies.
- **14 rows point at fal**, which is the outcome the user's stated preference was designed
  to produce — reached without any row being selected because fal carries it.
- **Two rows still need a new vendor account:** Sarvam Bulbul v3 and Runway Aleph 2.0. MAI-Image-2.5-Pro
  no longer does — resolving the Frontier Clouds identity moved it onto existing Azure access.
- **Confidence is uneven.** The four Google rows are T1. Everything else — the three Azure rows and
  every fal cell — is T2 at best, because this session could not open an AWS, Azure or fal page.

The two changes that would most improve this map are both lookups rather than research:
**confirm the three Azure rows and the credit coverage in your own console**, and **capture exact
fal endpoint ids and versions** from a machine that can reach `fal.ai`. Together they convert the
majority of this table from plan to fact in an afternoon.
