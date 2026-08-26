# E8-C — Frontier Clouds availability

**Task:** EVAL-008 · **Date:** 26 Aug 2026 · **Branch:** `work/eval-008-model-access`
**Status: IDENTITY RESOLVED by the Controller. Availability established for 7 of 26 rows.**
**0 API calls · ₹0 spent · no account created · no terms accepted.**

**Supersedes `FRONTIER-CLOUDS-VERIFY.md`**, which was written when the service could not be
identified. That file now holds only the residual checks this pass could not close.

---

## What Frontier Clouds turned out to be

**Controller-supplied, 26 Aug 2026:** *"Frontier clouds are usually GCP, AWS and Azure."*

So **Frontier Clouds is not one service — it is the three hyperscalers**: Google Cloud
(Vertex AI / Gemini Enterprise Agent Platform), Amazon Web Services (Bedrock), and Microsoft
Azure (Microsoft Foundry, formerly Azure AI Foundry).

This is recorded as a **Controller statement**, which is what settles it. It is not a research
finding, and it explains cleanly why three searches found nothing: we were hunting for a
product name that was never a product name.

**Why this matters more than a naming correction.** Hyperscaler credits are the cheapest
capacity this project has, and the question "what do they actually carry?" has a very
different answer for media generation than it does for language models. The short version is
below.

---

## The headline, before the detail

| Cloud | What it carries from our roster | Verdict |
|---|---:|---|
| **Google Cloud** | **4 of 26**, all first-party, all price-verified | **The strongest media cloud for us by a wide margin** |
| **Microsoft Azure** | **3 of 26**, including one that fixes a gap | Genuinely useful, and the only home for two roster rows |
| **AWS Bedrock** | **0 of 26** | **Effectively useless for this roster** — see the warning below |
| **Total covered** | **7 of 26** | **19 rows still need fal or a direct route** |

**The AWS finding is the one to act on.** Bedrock's own media models are being retired, not
expanded: Amazon Nova Canvas is marked Legacy with an **end-of-life of 30 September 2026**,
with migration pointed at Stability AI; Amazon Nova Reel is Legacy across all regions with
Luma Ray v2 named as its successor (T3). What Bedrock offers for image and video is therefore
Stability and Luma — **neither of which earned a slot on our roster**. If a meaningful share of
your credits sits on AWS, they will not buy this programme, and that is better known now than
at budget time.

---

## Evidence tiers, as used throughout this task

- **T1** — we fetched the page ourselves. Only `cloud.google.com` was reachable.
- **T2** — a search tool read a vendor-owned page and summarised it.
- **T3** — third-party reporting.

**AWS and Azure documentation remained unreachable from this session** (`aws.amazon.com`,
`docs.aws.amazon.com`, `azure.microsoft.com`, `learn.microsoft.com`, `ai.azure.com` all
answered `403` on re-probe after the identity was resolved). So every Azure and AWS line below
is **T2/T3 and must be confirmed in your own console** — which, unlike this session, you can
actually open.

---

## Row-by-row: the 7 covered

### Google Cloud — Vertex AI · 4 rows, all T1

Exact identities, GA dates and prices read directly from Google's own pricing page today. This
is the only part of the entire sourcing analysis that would survive an audit without re-checking.

| # | Model | Identity | Operations | Price as printed (USD) |
|---:|---|---|---|---|
| 2 | **Nano Banana 2** (Must) | `Gemini 3.1 Flash Image`, console param `gemini-3.1-flash-image`, **GA 28 May 2026**, 1K/2K GA and 4K preview | text-to-image, edit, reference | Image output **$60.00 / 1M tokens**; input $0.50 / 1M |
| 10 | **Veo 3.1** (Must) | Veo 3.1, plus **Fast** and **Lite** tiers | t2v, i2v, native audio | Video+audio **$0.40 / generation** (720p–1080p), $0.60 (4K); silent $0.20 / $0.40. Fast $0.10 / $0.12 / $0.30. **Lite $0.05 / $0.08** |
| 17 | **Nano Banana Pro** (Should) | `Gemini 3 Pro Image`, **GA 28 May 2026** | text-to-image, edit, reference | Cached input $0.20 / 1M; text output $12.00 / 1M. **Image-output cell not populated — price NOT VERIFIED** |
| 22 | **Gemini Omni Flash** (Should) | Gemini Omni Flash | video generate + conversational edit, native audio | Video output **$17.50 / 1M tokens** at **5,792 tokens per second of 720p-with-audio** → **≈ $0.101/sec** |

**Two things this settles.** The **cost ladder is real and steep** — Veo 3.1 Lite with audio at
$0.05 against Veo 3.1 at $0.40 is an **8× spread inside one family**, which is exactly the
Cost-per-Accepted-Outcome experiment, priced by the vendor. And **Gemini Omni Flash is
expensive per second** (~$0.101/sec, roughly twice Veo 3.1 Lite), so its case has to rest on
converging in fewer attempts, not on unit price.

**One open control question, from Google's own table:** the advanced controls the video-edit
lane needs — start/end frame interpolation, extend, camera controls — are listed under **Veo 2**
($0.50), **not under Veo 3.1**. If Veo 3.1 does not expose them, Veo cannot serve that lane.
The model documentation that would answer this redirects to `docs.cloud.google.com`, which this
session could not reach.

**Also on GCP but deliberately refused:** Imagen 4 / Ultra / Fast at $0.04 / $0.06 / $0.02 per
image, and Lyria 3 music at $0.04–$0.08 per count. Cheap, verified, and still not on the roster
— see the anti-bias note below.

### Microsoft Azure — Microsoft Foundry · 3 rows, T2/T3

| # | Model | What the evidence says | Verdict |
|---:|---|---|---|
| 1 | **GPT Image 2** (Must) | Foundry's image-generation line-up is listed as `gpt-image-1`, `gpt-image-1-mini`, `gpt-image-1.5` and **`gpt-image-2`** | **Available.** Same model id we selected |
| 5 | **FLUX.2 [pro]** (Must) | Black Forest Labs is a Foundry publisher; Foundry "supports both FLUX 1.1 Pro and **FLUX 2 Pro** deployments", with **FLUX.2 [flex]** also in the catalogue, pay-as-you-go or provisioned | **Available.** `[pro]` is the variant we selected; `[flex]` is a bonus, `[klein]` not mentioned |
| 18 | **MAI-Image-2.5-Pro** (Should) | **Released 23 July 2026 on Microsoft Foundry.** Deployable from the portal or Azure CLI at **model version 2026-06-02 or later**. Regions include East US, West US 3, Sweden Central, **South India**, UAE North, West Europe. **$5 / 1M text input, $106 / 1M image output.** Accepts text and images; **up to 1 reference image per request** | **Available** |

**Row 18 is the important one.** In the first pass I recorded MAI-Image-2.5-Pro as having **no
evidenced route at all** and recommended taking no action on it. That was wrong, and resolving
the Frontier Clouds identity is what fixed it: it is a Microsoft model, so it lives on
Microsoft's cloud. It is now the best-evidenced non-Google row on this page, it is in a
**South India** region, and it needs **no new vendor account** — only the Azure access you
already have.

**One capability caveat worth carrying into the measurement design:** MAI-Image-2.5-Pro accepts
**up to one reference image**. Several of our identity-consistency hypotheses assume richer
conditioning — MiniMax H3 accepts nine. That is not a reason to drop the row; it is a reason not
to compare them naively on a reference-conditioning task.

**Also on Azure but deliberately refused:** Sora and `sora-2` (excluded on model viability —
reported API shutdown 24 Sep 2026), and the Stability collection.

### AWS — Bedrock · 0 rows

No roster model was found on Bedrock. Bedrock's media catalogue is Stability AI (Stable Image
Core / Ultra / SD 3.5 Large) and Luma Ray v2, plus Amazon's own Nova Canvas and Nova Reel — both
now **Legacy**, with Nova Canvas carrying an **EOL of 30 September 2026** (T3).

**Nothing here earned a roster slot**, and the retirement notices are an additional reason not
to add one now: a Capability Registry entry against a model with a published end-of-life would
expire almost immediately, which is the same reasoning that excluded Sora 2.

---

## Row-by-row: the 19 not covered

Searched against all three clouds; not found on any. These fall through to fal, then direct —
see `FAL-AVAILABILITY.md` and `DIRECT-AND-OTHER-SOURCES.md`.

**Must — 12 of the 16 Must rows:** Seedream 5.0 Pro · Reve 2.1 · Qwen-Image / Qwen-Image-Edit ·
Seedance 2.0 Pro · Seedance 2.0 Fast · HappyHorse 1.1 · Kling 3.0 · MiniMax H3 ·
Runway Aleph 2.0 · Sarvam Bulbul v3 · ElevenLabs v3 · Sync-3
*(11 distinct models; Seedance 2.0 contributes two workflow rows)*

**Should — 7 of the 10 Should rows:** Ideogram V3 · Recraft V3 · FLUX.2 [klein] · Wan 2.7 · LTX-2 ·
Marey Realism V1.5 · OmniHuman v1.5

**Specifically checked and not found:** we looked for Kling, Seedance and Runway on Vertex AI
Model Garden and found no evidence of any partnership. Model Garden's third-party media story
appears to be Stability; its headline partner models are language models (Claude, Llama,
Mistral). Recorded as **not found / not verified**, not as "confirmed absent" — we could not read
the catalogue.

**A distinction that matters for the four open-weight rows.** Qwen-Image, FLUX.2 [klein],
Wan 2.7 and LTX-2 can all be *run on* GCP, AWS or Azure GPUs, because the weights are public.
**That is not the same as the cloud carrying them as a catalogue model**, and it is not the same
purchase: it consumes GPU capacity, not model credits, and it needs engineering. It is also
precisely the hypothesis those rows exist to test. Counting them as "covered by Frontier Clouds"
would quietly convert a measurement into an assumption, so they are counted as not covered.

---

## What this changes about the anti-bias check — it gets stronger

Knowing what the credits carry lets us state the result rather than defer it:

**19 of 26 Must/Should rows are not on the user's preferred credits, and not one row changed.**
The roster was frozen in commit `9583864` before any of this was known, and the selection files
have not been touched since — checkable with
`git diff --name-only 9583864 HEAD -- <the three selection files>`.

**Attractive, credit-covered models we still refuse:** Imagen 4 Fast at **$0.02/image** — the
cheapest verified price found in this entire task, sitting on the cloud we are most likely to
have credits on, and rejected as superseded in-vendor. Also Sora 2 on Azure, Stability on both
Azure and Bedrock, Luma Ray v2 on Bedrock, and Amazon's own Nova Canvas and Nova Reel. Credits
made every one of these nearly free to reach. None of them answers a question the roster asks.

---

## What still needs checking, and by whom

This pass could not open an AWS or Azure console. Three things need your eyes, and all three
are lookups rather than research:

1. **Confirm the three Azure rows in your own Foundry catalogue** — `gpt-image-2`, FLUX 2 Pro,
   and MAI-Image-2.5-Pro at model version 2026-06-02 or later — and note the exact deployed
   version string for each.
2. **Confirm what your credits actually cover on each cloud.** Media generation is frequently
   excluded from credit grants that cover language models, and that exclusion would change the
   entire cost picture.
3. **Check how your credits are split across GCP, AWS and Azure.** Given Bedrock carries none
   of this roster, credits weighted toward AWS are worth much less to this programme than the
   headline total suggests.

The residual per-row checklist is in `FRONTIER-CLOUDS-VERIFY.md`.
