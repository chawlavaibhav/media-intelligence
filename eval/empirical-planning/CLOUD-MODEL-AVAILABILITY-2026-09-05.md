# Cloud model availability survey — 2026-09-05

**Purpose.** Which candidate media-generation models (image / video / audio-TTS / lipsync) can be run on AWS Bedrock, Google Cloud Vertex AI, or Microsoft Azure AI Foundry against cloud credits, instead of cash on fal.ai.

**Method.** (1) Public catalogues and pricing pages (URLs cited inline). (2) Read-only checks with the credentials already on this machine — `aws bedrock list-foundation-models`, Vertex `publishers/google/models/<id>` GETs with the service account, `az cognitiveservices model list` / `deployment list` scoped explicitly to the getaight subscription, and the public Azure Retail Prices API. (3) Credit-programme terms.

**Nothing was enabled, created, deployed, subscribed, invoked, or paid for.** No `az account set`, no gcloud default-config change (an isolated `CLOUDSDK_CONFIG` directory was used), no model invocations. This is a survey only.

**Evidence labels.** `OBSERVED` = seen on a catalogue/pricing page or in CLI output (source given). `REPORTED` = a secondary source (search summary / vendor blog) that I could not verify on a primary page. `INFERRED` = my reading of terms or of absence from a catalogue. Prices are USD list, on-demand, unless stated.

---

## 0. Headline

| | AWS Bedrock | Vertex AI | Azure Foundry |
|---|---|---|---|
| Native (credit-eligible) image gen | Stability SD3.5 Large / Stable Image Core / Ultra (us-west-2). Nova Canvas is **Legacy, EOL 2026-09-30**. | Nano Banana 2 (`gemini-3.1-flash-image`, GA), Nano Banana Pro (`gemini-3-pro-image`, GA), Nano Banana (`gemini-2.5-flash-image`, GA). Imagen 4 **retired**. | `gpt-image-2` (GA), `FLUX.2-pro` / `FLUX.2-flex` / `FLUX-1.1-pro` / `FLUX.1-Kontext-pro` (GA), `MAI-Image-2.6` / `-Flash` (Preview) |
| Native (credit-eligible) video gen | Luma `luma.ray-v2:0` (us-west-2). Nova Reel **Legacy, EOL 2026-09-30**. | Veo 3.1 / Fast (GA), Veo 3.1 Lite (preview), Gemini Omni Flash / Omni 1.1 Flash (preview) | `sora-2` (Preview; eastus2 / swedencentral) |
| Native TTS (Hindi) | Polly `Kajal` hi-IN neural | Chirp 3 HD hi-IN; Gemini TTS | Azure Neural TTS hi-IN voices; `gpt-4o-mini-tts` |
| Lipsync / talking head | none | none | Azure Speech **TTS Avatar** (TTS-driven avatar, not audio-to-video lipsync) |
| **Not on any of the three** | Kling v3, MiniMax Hailuo/H3, Seedance 2.5, Wan 3.0, Runway, Pika, LTX, Recraft V4, Qwen Image 3, ElevenLabs (except GCP Marketplace, not credit-eligible), Sarvam bulbul (Azure Marketplace SaaS only, not credit-eligible), any audio-driven lipsync model | | |

---

## 1. Image models

Columns: candidate | AWS Bedrock | Vertex AI | Azure Foundry | fal.ai fallback.

| Candidate | AWS Bedrock (id / status / price / credits?) | Vertex AI (id / status / price / credits?) | Azure Foundry (id / status / price / credits?) | fal.ai fallback |
|---|---|---|---|---|
| **GPT Image 2** (OpenAI) | Not on Bedrock (OBSERVED: absent from `list-foundation-models` us-east-1/us-west-2/ap-south-1/eu-west-1). | Not on Vertex (OBSERVED: absent from partner-models page). | `gpt-image-2` version 2026-04-21, **GA**, "sold directly by Azure" (OBSERVED: [models-sold-directly-by-azure](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure); `az cognitiveservices model list` shows it deployable in **eastus2, swedencentral, westus3, uaenorth, polandcentral**; NOT in eastus/southindia/centralindia). Price (OBSERVED, Azure Retail Prices API, Global Standard): text in $5.00/1M tok, image in $8.00/1M, image **output $30.00/1M tok** (Data Zone $33.00); batch output $15.00/1M. Per-image cost depends on tokens per output image (not published on the meter). **Credits: YES** (sold by Azure). | `openai/gpt-image-2` (OBSERVED in Stage-A yaml, $0.053/image projection) |
| **Nano Banana 2** = `gemini-3.1-flash-image` | No | `gemini-3.1-flash-image` **GA** and `gemini-3.1-flash-image-preview` PUBLIC_PREVIEW (OBSERVED: publisher-model GET with our SA). Price (OBSERVED, [Vertex pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)): $60/1M image-output tokens → **$0.045 (512px), $0.067 (1K), $0.101 (2K), $0.151 (4K) per image**; 1120 tok per input image. Also listed: `Gemini 3.1 Flash-Lite Image (Nano Banana 2 Lite)`, Global, $0.25/1M in, output tokens — id not probed. **Credits: YES** (Google model). | No | fal has a Nano Banana family; exact route id not verified in this survey |
| **Nano Banana Pro** = `gemini-3-pro-image` | No | `gemini-3-pro-image` **GA** (OBSERVED GET). `gemini-3-pro-image-preview` NOT FOUND. Price (OBSERVED): $120/1M image-output tokens → **$0.134 (1K/2K), $0.24 (4K) per image**; 560 tok per input image. **Credits: YES.** | No | fal route not verified |
| **Imagen 4** family | No | **Retired on Vertex.** `imagen-4.0-generate-001`, `-ultra-`, `-fast-` all NOT FOUND on the publisher endpoint (OBSERVED GET). Pricing page still shows rows ($0.06 Ultra, $0.04 Imagen 4, $0.02 Fast — OBSERVED) but REPORTED shutdown: deprecated on Vertex 2026-03-24, migration deadline 2026-06-30, Gemini API shutdown 2026-08-17 ([kingy.ai](https://kingy.ai/ai-launch-tracker/google-will-shut-down-three-imagen-4-api-models-august-17/), [vorplabs](https://vorplabs.com/models/google-model-retirements)). `imagen-3.0-generate-002` also NOT FOUND. **Treat as unavailable.** | No | fal route not verified; candidate should be dropped |
| **Seedream 5.0 Pro** (ByteDance) | No (OBSERVED absent) | No (`publishers/bytedance/...` NOT FOUND; partner page has no ByteDance) | No (absent from sold-by-Azure and partners pages) | `bytedance/seedream/v5/pro/text-to-image` (OBSERVED Stage-A yaml, $0.0675/image tentative) — **fal-only** |
| **FLUX.2 Pro** (BFL) | No | No (`publishers/blackforestlabs/...` NOT FOUND) | `FLUX.2-pro` v1 **GA**, "Black Forest Labs models sold by Azure" (OBSERVED catalogue page; deployable in **eastus, southindia, eastus2, swedencentral, westus3, uaenorth, polandcentral** per `az cognitiveservices model list`; NOT centralindia). Price (OBSERVED Retail API, Global): **$0.030 first megapixel + $0.015 each additional MP**; reference-image MP $0.015; Data Zone ×1.1. Siblings: `FLUX.2-flex` $0.05/MP; `FLUX-1.1-pro` $0.040/image; `FLUX.1-Kontext-pro` $0.040/image. **Credits: YES** (sold by Azure). | `fal-ai/flux-2-pro` (OBSERVED Stage-A yaml, $0.03/image) |
| **Qwen Image 3** (Alibaba) | No (Qwen text models exist on Bedrock; no image model in listing — OBSERVED) | No | No | fal route not verified — **fal-only** |
| **Recraft V4** | No | No | No | fal route not verified — **fal-only** |
| **Stable Diffusion 3.5 / Stability** | `stability.sd3-5-large-v1:0` ON_DEMAND ACTIVE, `stability.stable-image-core-v1:1`, `stability.stable-image-ultra-v1:1` ACTIVE — **us-west-2 only** (OBSERVED CLI). In us-east-1 only the 13 editing primitives (`stability.stable-image-inpaint-v1:0` etc.) via INFERENCE_PROFILE, priced $0.03–$0.60 per generation (OBSERVED [Bedrock pricing](https://aws.amazon.com/bedrock/pricing/)). Per-image price for SD3.5L/Core/Ultra: page loads via JS; REPORTED Stable Image Ultra $0.14/image; Core and SD3.5 Large not verified. **Credits: YES** (Bedrock-native serverless; see §4). | Not as a managed API (Model Garden has self-deploy open models only — INFERRED). | `Stable-Diffusion-3.5-Large` exists in the Foundry catalogue as a **partner** model (Marketplace-billed; REPORTED [stability.ai](https://stability.ai/news-updates/stable-diffusion-35-large-is-now-available-on-microsoft-ai-foundry)). **Credits: NO** (partner/Marketplace). | fal route not verified |
| **Amazon Nova Canvas** | `amazon.nova-canvas-v1:0` — **LEGACY**, EOL **2026-09-30**, regions us-east-1 / eu-west-1 / ap-northeast-1 (OBSERVED CLI + [model-lifecycle](https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html)). Docs: "New customers can't use Legacy models and existing customers may lose access after 15 days of inactivity." REPORTED price $0.04–$0.08/image. **Effectively unavailable to a new account.** | — | — | n/a |
| **Microsoft MAI image** | — | — | `MAI-Image-2.6` and `MAI-Image-2.6-Flash` (2026-07-31) **Preview**, `MAI-Image-2.5` / `-Flash` / `-Pro` Preview, `MAI-Image-2` / `2e` Deprecated (OBSERVED `az` model list: eastus, southindia, swedencentral, uaenorth). Sold by Azure (OBSERVED catalogue page, "Microsoft models sold by Azure"). Price (OBSERVED Retail API): 2.5 output $47/1M tok ($0.047/1K), 2.5 Flash output $19.5/1M, 2.5 Pro output $106/1M; **2.6 meters not yet in Retail API** (announced 2026-09-04, [microsoft.ai](https://microsoft.ai/news/pushing-the-quality-cost-frontier-with-mai-image-2-6/)). **Credits: YES.** | n/a (Azure-only model) |

## 2. Video models

| Candidate | AWS Bedrock | Vertex AI | Azure Foundry | fal.ai fallback |
|---|---|---|---|---|
| **Veo 3.1** (full / fast / lite) | No | `veo-3.1-generate-001` **GA**, `veo-3.1-fast-generate-001` **GA**, `veo-3.1-lite-generate-001` **PUBLIC_PREVIEW**; `-preview` ids also exist for full/fast (OBSERVED GET). Price per second (OBSERVED [Vertex pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)): **Veo 3.1 $0.40 (720p/1080p, with audio), $0.60 (4K); Fast $0.10 (720p), $0.12 (1080p), $0.30 (4K); Lite $0.05 (720p), $0.08 (1080p)**. **Credits: YES.** | No | `fal-ai/veo3.1` ($0.40/s), `fal-ai/veo3.1/lite` ($0.05/s) (OBSERVED Stage-A yaml) — same price as Vertex |
| **Kling v3** (Kuaishou) | No | No (`publishers/kuaishou/...` NOT FOUND) | No | `fal-ai/kling-video/v3/pro/text-to-video` ($0.112/s, OBSERVED Stage-A yaml) — **fal-only** |
| **MiniMax H3 Max / Hailuo** | No | No — Vertex partner page lists **MiniMax M2 (text) only** (OBSERVED) | No — MiniMax not in sold-by-Azure or partners media lists (OBSERVED) | Stage-A yaml routes Hailuo 3 via **Runway** (`hailuo3`, credits-based); fal route not verified — **not on any hyperscaler** |
| **Seedance 2.5** (ByteDance) | No | No | No | fal route not verified — **fal-only** |
| **Wan 3.0 Prime** (Alibaba) | No | No | No | fal route not verified — **fal-only** |
| **Gemini Omni Flash 1.1** | No | `gemini-omni-1.1-flash-preview` **Preview** and `gemini-omni-flash-preview` Preview (OBSERVED on Vertex docs pages [omni-1-1-flash](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/gemini/omni-1-1-flash)); `gemini-omni-flash` returned GA on the publisher endpoint (OBSERVED GET). Price (OBSERVED pricing page): input $1.50/1M, text out $9.00/1M, **video out $17.50/1M tokens** at 5,792 tok/s (720p) ≈ **$0.101/s**, 8,688 tok/s (1080p) ≈ $0.152/s, 17,376 tok/s (4K) ≈ $0.304/s. **Credits: YES.** | No | n/a (Google-only) |
| **Sora** (OpenAI) | No | No | `sora-2` version 2025-10-06 **Preview**, sold by Azure; deployable in **eastus2, swedencentral** only (OBSERVED `az` list + catalogue). Price (OBSERVED Retail API): **Sora 2 $0.10/s Global** ($0.11 Data Zone); Sora 2 Pro $0.30/s; Sora 2 Pro high-res $0.50/s. (Sora 1 meters also exist, $0.15–$3.60/s by resolution/length.) **Credits: YES** (sold by Azure). | fal route not verified |
| **Amazon Nova Reel** | `amazon.nova-reel-v1:0` and `v1:1` — **LEGACY, EOL 2026-09-30**; new customers can't use Legacy models (OBSERVED lifecycle page). REPORTED $0.08/s. **Effectively unavailable.** | — | — | n/a |
| **Luma Ray** | `luma.ray-v2:0` ON_DEMAND ACTIVE, **us-west-2 only** (OBSERVED CLI). Price REPORTED $0.75/s (540p), $1.50/s (720p) ([AWS blog](https://aws.amazon.com/blogs/aws/luma-ai-ray-2-video-model-is-now-available-in-amazon-bedrock/) + search summary; not verified on the JS pricing page). Ray 3 not on Bedrock. **Credits: YES** (Bedrock-native). Expensive vs Veo. | No | No | fal route not verified |
| **Runway Gen / Aleph** | No | No | No | Runway direct (`aleph2`, OBSERVED Stage-A yaml) — **not on any hyperscaler** |
| **Pika** | No | No | No | fal route not verified — fal-only |
| **LTX** (Lightricks) | No (REPORTED "marketplace availability later" in Oct-2025 PR; not in Bedrock listing) | No | No | fal route not verified — fal-only |

## 3. Audio / TTS / lipsync

| Candidate | AWS | Google Cloud | Azure | fal / direct fallback |
|---|---|---|---|---|
| **ElevenLabs v3** | Not on Bedrock (OBSERVED absence) | ElevenLabs says ElevenAPI / ElevenCreative / ElevenAgents are on **Google Cloud Marketplace and Model Garden**, purchasable with cloud commit funds (OBSERVED [elevenlabs.io/blog/googlecloud](https://elevenlabs.io/blog/googlecloud)). `publishers/elevenlabs/models/eleven-v3` NOT FOUND via API (listing id unknown). **Credits: NO** — Google FAQ: credits "cannot be applied to any third-party services or offerings including those on Google Cloud Marketplace" (OBSERVED). | Not in Foundry sold-by-Azure or partners pages (OBSERVED) | `eleven_v3` direct ($0.10/1K chars, OBSERVED Stage-A yaml) |
| **Sarvam bulbul v3** | No | No | Azure **Marketplace SaaS** listing "Sarvam Models APIs" (`sarvam.sarvam_api_prod`) (REPORTED via [marketplace.microsoft.com](https://marketplace.microsoft.com/en-us/product/saas/sarvam.sarvam_api_prod?tab=overview)); Sarvam text model in Foundry catalogue; bulbul not in sold-by-Azure list (OBSERVED). **Credits: NO** (Marketplace). | `bulbul:v3` direct (₹30/10K chars, OBSERVED Stage-A yaml) |
| **Amazon Polly (Hindi neural)** | hi-IN: **`Kajal`** (Neural, bilingual hi-IN/en-IN), `Aditi` (Standard). en-IN: `Kajal` (Generative + Neural), `Raveena`, `Aditi` (Standard) (OBSERVED [available-voices](https://docs.aws.amazon.com/polly/latest/dg/available-voices.html)). Price (OBSERVED [polly/pricing](https://aws.amazon.com/polly/pricing/)): Standard $4, **Neural $16**, Generative $30, Long-form $100 per 1M chars; neural free tier 1M chars/mo first 12 months. **Credits: YES** (AWS-native). Note: our IAM user is denied `polly:DescribeVoices` (OBSERVED) — invoking Polly would need a policy change. | — | — | — |
| **Google Cloud TTS Chirp 3 HD (Hindi)** | — | Chirp 3: HD supports **hi-IN** (OBSERVED [chirp3-hd docs](https://docs.cloud.google.com/text-to-speech/docs/chirp3-hd)); voice names follow `hi-IN-Chirp3-HD-<name>`; per-1M-char price not extracted (pricing page is JS-rendered). Also on Vertex: `gemini-2.5-pro-tts` GA, `gemini-2.5-flash-preview-tts` Preview (OBSERVED GET); Gemini 3.1 Flash TTS $20/1M audio tokens (OBSERVED Gemini API pricing). **Credits: YES.** Caveat: the Cloud Text-to-Speech API is **not enabled** in `vertexaiproject-507518` (OBSERVED error) — enabling is an action, not done. | — | — |
| **Azure Neural TTS (hi-IN)** | — | — | Azure Speech is "Foundry Tools", sold by Azure. hi-IN neural voices: Swara, Madhur, Aarav, Ananya, Kavya, Kunal, Rehaan, Aarti, Arjun (REPORTED via [language-support](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support) / community blog). Price (OBSERVED Retail API, centralindia): **Neural TTS $15/1M chars**, Neural HD $22/1M, Custom Neural realtime $24/1M. Also `gpt-4o-mini-tts` (eastus2) and OpenAI `tts`/`tts-hd` (swedencentral, westus3) sold by Azure (OBSERVED `az` list). **Credits: YES.** | — |
| **Lip-sync / talking head** | None on Bedrock (OBSERVED listing). | None on Vertex (Veo generates its own speech; no audio-driven lipsync model). | **Azure Speech Text-to-Speech Avatar** — TTS-driven synthetic presenter, sold by Azure. Price (OBSERVED Retail API, centralindia): Standard avatar **batch $1.00/min**, HD standard batch $1.35/min, realtime $0.50/min; custom avatar batch $2.00/min. It is *not* an audio-to-existing-video lipsync (INFERRED from product description). **Credits: YES.** | `fal-ai/sync-lipsync/v3` ($8/min, OBSERVED Stage-A yaml) — **fal-only** for true lipsync |

---

## 4. Credits — what each programme covers (with sources)

**AWS (Activate / promotional credits).**
- OBSERVED: AWS Activate credits are redeemable on third-party foundation models in Bedrock (AI21, Anthropic, Cohere, Meta, Mistral, Stability, Amazon) — [AWS Startups blog, 2 Apr 2024](https://aws.amazon.com/blogs/startups/aws-activate-credits-now-accepted-for-third-party-models-on-amazon-bedrock/).
- OBSERVED: AWS Promotional Credit terms exclude "AWS Marketplace" among ineligible services — [aws.amazon.com/awscredits](https://aws.amazon.com/awscredits/).
- INFERRED: Bedrock-native serverless models (Nova, Stability, Luma — all `ON_DEMAND` in the CLI listing) are eligible; **Bedrock Marketplace** listings (SageMaker-hosted, software fee billed through AWS Marketplace) are *not* eligible for the software fee. I could not read the Bedrock Marketplace docs page (JS-rendered). None of our candidates were found on Bedrock Marketplace anyway.

**Google Cloud (Google for Startups Cloud Program).**
- OBSERVED [startup FAQ](https://cloud.google.com/startup/faq): "The credits cannot be applied to any third-party services or offerings including those on Google Cloud Marketplace." and "*Third-party models are billed directly and are not covered by the program credits."
- INFERRED: Veo, Nano Banana 2/Pro, Omni Flash, Lyria, Chirp 3 HD, Gemini TTS = covered. Claude on Vertex, ElevenLabs via Model Garden/Marketplace = not covered.

**Azure (Microsoft for Startups sponsorship).**
- OBSERVED [foundry-model-sponsorship-coverage](https://learn.microsoft.com/en-us/startups/benefits/technical-benefits/azure-credits/foundry-model-sponsorship-coverage) (updated 2026-04-14): "sponsorship credits apply to Microsoft Foundry models that are sold and billed directly by Azure. Models billed by third-party providers, partner services, or available through the Azure Marketplace are not eligible." Use the "Direct from Azure" collection in the portal.
- OBSERVED [models-from-partners](https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-from-partners): "Free credit" subscriptions cannot purchase SaaS offers; "Sponsored subscriptions that only use Azure credits" are unsupported for Claude — i.e. partner models may not even be deployable on a credits-only sub.
- INFERRED: gpt-image-2, sora-2, FLUX (BFL "sold by Azure"), MAI-Image, Azure Speech TTS/Avatar, OpenAI tts = covered. Stability SD3.5 (partner), Sarvam (Marketplace SaaS) = not.

---

## 5. Account reality (identities confirmed; ids only)

**AWS** — `aws sts get-caller-identity`: account **528730633804**, principal type IAM user (`claude-aight`), `AWS_DEFAULT_REGION=us-east-1`. (Note: `aws.env` lines are not `export`ed; needed `set -a` to source.)
- `bedrock list-foundation-models` works. Media-output models actually visible to this account:
  - us-east-1 (122 models): `amazon.nova-canvas-v1:0` LEGACY, `amazon.nova-reel-v1:0` / `v1:1` LEGACY, `amazon.nova-sonic-v1:0` LEGACY, `amazon.nova-2-sonic-v1:0` ACTIVE, 13 `stability.stable-image-*` / `stable-*-upscale` editing primitives (INFERENCE_PROFILE only). No text-to-image base model, no Luma.
  - us-west-2 (115): `stability.sd3-5-large-v1:0` ON_DEMAND, `stability.stable-image-core-v1:1`, `stability.stable-image-ultra-v1:1`, `luma.ray-v2:0` ON_DEMAND, plus Stability primitives.
  - **ap-south-1 (74): zero image/video/speech models.** eu-west-1 (63): only Legacy Nova Canvas/Reel.
- Denied: `polly:DescribeVoices`, `pricing:GetProducts` (OBSERVED AccessDenied). Whether `bedrock:InvokeModel` is allowed and whether Stability/Luma model access is already granted in the account was **not tested** (would be an invocation / access-request action).
- Whether this account holds AWS Activate credits: **unknown** (no billing read attempted).

**Google Cloud** — service account `aight-gateway-sa@vertexaiproject-507518…`, project **vertexaiproject-507518** (project number 148505173459), `VERTEX_LOCATION=global`. Activated only inside an isolated `CLOUDSDK_CONFIG`; the user's default gcloud config (account vaibhav@wherehouse.io, project `supe-ask-staging`) was verified untouched before and after — that default is a Wherehouse project and must not be used for this programme.
- Publisher-model GETs succeed (so the SA has `aiplatform` read): `veo-3.1-generate-001` GA, `veo-3.1-fast-generate-001` GA, `veo-3.1-lite-generate-001` preview, `veo-3.0-generate-001` GA, `gemini-3-pro-image` GA, `gemini-3.1-flash-image` GA, `gemini-2.5-flash-image` GA, `gemini-omni-flash` GA, `gemini-omni-flash-preview` preview, `lyria-002` GA, `gemini-2.5-pro-tts` GA, `anthropic/claude-sonnet-4-5` OK.
- The list endpoint (`publishers/google/models`) returns 404/empty; the SA lacks `serviceusage.services.list`; **Text-to-Speech API not enabled** in the project. Whether the project has Google for Startups credits: **unknown**.

**Azure** — `az account show` default subscription is **d3ee8dc2-9220-43fb-bd16-787a52f9ffa3** ("Azure subscription 1", tenant b9023489…) — **this is NOT the getaight subscription**. The getaight sub **b832f4a1-79be-4fb2-ae93-6ba6efd209d2** (also named "Azure subscription 1") is present in `az account list` but is not the default. I did **not** change the default; every Azure query was run with `--subscription b832f4a1-…`. Identity/purpose of d3ee8dc2 is unknown — treat as a concern before anyone runs Azure commands without an explicit `--subscription`.
- Cognitive Services accounts in b832f4a1 (OBSERVED, read-only): `aight-openai-southindia` (OpenAI, southindia, rg aight-gateway — this is the endpoint in `azure.env`), `aight-openai-c3bits` (OpenAI, eastus), `aight-openai-c1wher` (OpenAI, southindia). Existing deployments are all text/embedding (gpt-5.x, gpt-4.1, gpt-4o, text-embedding-3-small). **No image, video, or TTS deployment exists today.**
- Deployable from this subscription (catalogue, OBSERVED via `az cognitiveservices model list`): FLUX.2-pro/flex, FLUX-1.1-pro, Kontext-pro and MAI-Image-2.5/2.6 in **eastus and southindia** (i.e. in existing resources' regions); `gpt-image-2` only in eastus2/swedencentral/westus3/uaenorth/polandcentral; `sora-2` only in eastus2/swedencentral; `gpt-4o-mini-tts` eastus2. **centralindia: nothing media-related.** Using gpt-image-2 or sora-2 would require a new Foundry/OpenAI resource in one of those regions (not created).
- Whether b832f4a1 carries Microsoft for Startups sponsorship credits: **unknown** (no billing read attempted; memory says it is the getaight sub).

---

## 6. Recommended cloud-first routing for the battery

Cheapest credit-eligible surface first; else fal/direct. Prices per §1–3.

| Candidate | Route | Why |
|---|---|---|
| GPT Image 2 | **Azure `gpt-image-2`** (needs new resource in eastus2/swedencentral/westus3/uaenorth/polandcentral) | Only cloud with it; sold by Azure → credits. Fallback fal `openai/gpt-image-2`. |
| Nano Banana 2 | **Vertex `gemini-3.1-flash-image`** ($0.067 @1K) | GA, credits. |
| Nano Banana Pro | **Vertex `gemini-3-pro-image`** ($0.134 @1K/2K) | GA, credits. |
| Imagen 4 | **Drop** — retired on Vertex | — |
| Seedream 5.0 Pro | fal `bytedance/seedream/v5/pro/text-to-image` | fal-only. |
| FLUX.2 Pro | **Azure `FLUX.2-pro`** (eastus or southindia; $0.03 first MP) | Sold by Azure → credits; same list price as fal. |
| Qwen Image 3, Recraft V4 | fal | fal-only. |
| Stability SD3.5 / Ultra | **Bedrock us-west-2** (`stability.sd3-5-large-v1:0`, `stable-image-ultra-v1:1`) | Bedrock-native → credits; confirm model access + per-image price first. |
| Nova Canvas / Reel | **Drop** — Legacy, EOL 2026-09-30, closed to new customers | — |
| MAI-Image-2.6 (bonus) | Azure (eastus/southindia), Preview | Credits; 2.6 price not yet published. |
| Veo 3.1 / Fast / Lite | **Vertex** (`veo-3.1-generate-001` $0.40/s, `-fast-` $0.10/s, `-lite-` $0.05/s) | Same list price as fal, but credits. |
| Kling v3 | fal `fal-ai/kling-video/v3/pro/text-to-video` | Not on any hyperscaler. |
| MiniMax Hailuo / H3 | Runway `hailuo3` (Stage-A) or fal | Not on any hyperscaler. |
| Seedance 2.5, Wan 3.0, Pika, LTX | fal | Not on any hyperscaler. |
| Gemini Omni Flash 1.1 | **Vertex `gemini-omni-1.1-flash-preview`** (≈$0.10/s 720p) | Google-only; credits. |
| Sora 2 | **Azure `sora-2`** ($0.10/s; eastus2/swedencentral; Preview; new resource needed) | Sold by Azure → credits. |
| Luma Ray 2 | Bedrock us-west-2 `luma.ray-v2:0` only if a Luma data point is required | Credits, but $0.75–$1.50/s is 2–4× Veo. |
| Runway Gen / Aleph | Runway direct | Not on any hyperscaler. |
| ElevenLabs v3 | direct `eleven_v3` | GCP Marketplace listing exists but is credit-ineligible. |
| Sarvam bulbul v3 | direct `bulbul:v3` | Azure Marketplace SaaS only, credit-ineligible. |
| Hindi TTS (cloud-native, credit-eligible) | **Polly `Kajal` neural ($16/1M)**, **Azure Neural TTS hi-IN ($15/1M)**, **Chirp 3 HD hi-IN** (API needs enabling) | All three are first-party → credits. |
| Lipsync | fal `fal-ai/sync-lipsync/v3` | No audio-driven lipsync on any cloud. Azure TTS Avatar ($1.00/min) is a different product (TTS-driven presenter). |

---

## 7. Explicit unknowns

1. **Credit balances / programme enrolment** on all three accounts — not checked (no billing reads attempted).
2. **AWS**: whether `claude-aight` may `bedrock:InvokeModel`, and whether Stability / Luma model access is granted; per-image list prices for SD3.5 Large / Stable Image Core / Ultra (pricing page is JS; only Ultra $0.14 REPORTED); Luma Ray 2 per-second price is REPORTED, not verified on a primary page; Bedrock Marketplace billing text not read (JS page).
3. **Google**: exact fal/Vertex parity assumed only where the Stage-A yaml gave a fal price (Veo); Chirp 3 HD per-character price and hi-IN voice names not extracted; whether `gemini-omni-flash` (GA on the publisher endpoint) is the same model the docs call Omni 1.1 Flash preview; ElevenLabs Model Garden listing id.
4. **Azure**: identity/purpose of default subscription d3ee8dc2…; MAI-Image-2.6 price (meters absent from Retail API); tokens-per-image for `gpt-image-2` (needed to convert $30/1M output tokens to a per-image figure); whether sora-2 preview access is auto-granted or gated for this subscription (Q&A threads REPORT gating).
5. **fal route ids** for candidates not present in the Stage-A yaml (Nano Banana 2/Pro, Seedance 2.5, Wan 3.0, Sora, Luma Ray 3, Pika, LTX, Recraft V4, Qwen Image 3, SD3.5) were not verified against fal.ai in this survey.
6. Sarvam and ElevenLabs availability on Azure Foundry / Bedrock is INFERRED from absence in the catalogue pages, not from a vendor statement.
