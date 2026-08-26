# E8-E — Direct and other sourcing

**Task:** EVAL-008 · **Date:** 26 Aug 2026
**Status: COMPLETE for the models that need it; one tier of evidence is genuinely solid.**
**0 API calls · ₹0 spent · no account created · no terms accepted.**

---

## Scope of this pass

This step exists only for selected models **still uncovered** after the two preferred routes.
Because Frontier Clouds could not be identified (`FRONTIER-CLOUDS-VERIFY.md`) and fal could
not be read directly (`FAL-AVAILABILITY.md`), "uncovered" is currently a wider set than it
should be. Rather than under-deliver, this page records the direct route for **every** Must
and Should model, so that whichever of the two preferred routes falls through, the fallback is
already written down.

The preference order inside this final step, as the task specifies:
**official vendor API → established production API/provider → other legitimate access, only
where provenance and version are clear enough to support evidence.**

---

## The one place we have real documentation

**Google is the only vendor whose own pages this session could read.** Everything in this
block is **T1** — fetched directly today from `cloud.google.com`, prices quoted as printed.
It is the only part of this entire task that would survive an audit without re-checking.

### Google — Vertex AI (Gemini Enterprise Agent Platform) and the Gemini API

Both surfaces exist. Google's own page distinguishes them plainly: Vertex AI is
**backed by the enterprise SLA**; the Gemini API is **not**. For a Capability Lab that
difference matters less than version pinning, but for production it matters a great deal.

| Selected model | Model identity (T1) | Price as printed (T1, USD) |
|---|---|---|
| Nano Banana 2 | `Gemini 3.1 Flash Image` · console param `gemini-3.1-flash-image` · **GA 28 May 2026** · 1K/2K GA, 4K preview | Image output **$60.00 / 1M tokens**; input (text/image/video) $0.50 / 1M |
| Nano Banana Pro | `Gemini 3 Pro Image` · **GA 28 May 2026** | Cached input $0.20 / 1M; text output $12.00 / 1M. **Image-output cell not populated in the table we read — price NOT VERIFIED** |
| *(cost-tier sibling, not on the roster)* | `Gemini 3.1 Flash-Lite Image` ("Nano Banana 2 Lite") | Image output **$30.00 / 1M tokens** — half of Nano Banana 2 |
| Veo 3.1 | Veo 3.1, plus **Fast** and **Lite** tiers | Video+audio **$0.40 / generation** at 720p–1080p, **$0.60** at 4K. Silent $0.20 / $0.40. **Fast:** $0.10 / $0.12 / $0.30 with audio. **Lite:** $0.05 / $0.08 with audio; $0.03 / $0.05 silent |
| Gemini Omni Flash | Gemini Omni Flash | Video output **$17.50 / 1M tokens**, charged at **5,792 tokens per second of 720p video with audio** → **≈ $0.101 per second**, i.e. ~$1.01 for a 10-second clip. Input $1.50 / 1M |

**Two things this table settles that nothing else in the task could.**

First, **a real cost ladder exists and is steep**: Veo 3.1 Lite with audio at $0.05 against
Veo 3.1 at $0.40 is an **8× spread inside one family**. That is precisely the
Cost-per-Accepted-Outcome question, priced, from the vendor. Any budget forecast should use
these numbers and not the third-party ones.

Second, **Gemini Omni Flash is expensive per second** — about $0.101/sec, so roughly twice
Veo 3.1 Lite per second of finished video. Its case has to rest on converging in fewer
attempts, not on unit price. Worth knowing before we design its trials.

**One open control question, also from Google's own page:** the advanced controls we need for
the video-edit lane — start/end frame interpolation, extending a generated video, camera
controls — are listed under **Veo 2**, priced at $0.50, and **not under Veo 3.1**. If Veo 3.1
does not expose them, Veo cannot serve that lane and the lane rests entirely on Runway Aleph,
HappyHorse and MiniMax. This should be checked in the model documentation, which redirects to
`docs.cloud.google.com` — a host this session could not reach.

---

## Everything else — indicative routes, not verified

Every row below is **T2 or T3**. The route is named because it is the right place to look
first, not because we confirmed it.

### Models that appear to need a direct route (not seen on fal)

| Selected model | Best direct route | What we know | Constraints to check |
|---|---|---|---|
| **Runway Aleph 2.0** | Runway's own API (`runway.com` / `dev.runwayml.com`) | Announced 21 May 2026 with Edit Studio; up to 30s at 1080p, edits across up to 10 cuts, up to 5 keyframe anchors. Reportedly also surfaced inside Adobe Firefly Boards, which is a product route rather than an API route | **A T3 source states API access moved to Enterprise-only in January 2026.** If true this is the single hardest access problem on the roster: an enterprise sales motion, not a signup. **Verify before assuming.** Adobe Firefly is the fallback route and would change the workflow materially |
| **Sarvam Bulbul v3** | Sarvam's own API (`sarvam.ai`, docs at `docs.sarvam.ai`) | 11 Indian languages, 30+ voices, Hinglish code-switching, sub-250ms streaming, **₹30 per 10,000 characters in beta as of Aug 2026**, data resident in India | Indian company, rupee billing, so no FX or geographic friction for this user. Beta pricing may change. Confirm whether beta access needs an application |
| **MAI-Image-2.5-Pro** | Microsoft — most plausibly Azure AI Foundry | Only T3 evidence exists: an arena ranking. **We found no documented API route at all** | **Route entirely NOT VERIFIED.** This is the roster's weakest sourcing story and the reason it sits at Should, not Must |

### Models covered elsewhere, with their direct route recorded as fallback

| Selected model | Direct route | Notes |
|---|---|---|
| GPT Image 2 | OpenAI API, `gpt-image-2` | Token-priced: reportedly $8/1M image input, $30/1M image output, $5/1M text input (T2/T3). Token pricing makes per-image cost depend on resolution — forecast carefully |
| Seedream 5.0 Pro · Seedance 2.0 · OmniHuman v1.5 | **BytePlus ModelArk** (`docs.byteplus.com`) | BytePlus is ByteDance's international arm and documents "Dreamina Seedance 2.0 series" and "Seedream 5.0 pro" tutorials, a model list and a pricing page (T2). Also documents an inference free trial and "Advanced Creation Rights" — read the rights page before any customer-facing use |
| Reve 2.1 | Reve API — the vendor's own blog documents it (`blog.reve.com/posts/the-reve-api`) | Credit-based; a reported $10 minimum for 7,500 credits, and an unusually cheap edit tier (T3) |
| FLUX.2 [pro] / [klein] | Black Forest Labs (`bfl.ai`) for the closed tiers; open weights for `[dev]` and `[klein]` | **`[dev]` requires a separate commercial licence from BFL** (T3). `[klein]` is reported Apache-2.0. The licence, not the download, is the gate |
| Qwen-Image / Qwen-Image-Edit | Open weights (Apache-2.0 claimed), plus Alibaba Cloud's own model service | Self-hosting means a GPU account, which is a **different kind of account** from an API signup — see `ACCOUNT-ACTIONS.md` |
| Wan 2.7 | Open weights (Apache-2.0 claimed for the 2.2 line); Alibaba Cloud | ~80GB-class GPU for full quality (T3). Confirm which version carries which licence |
| LTX-2 | Lightricks; open weights | Licence reported free below $10M ARR (T3) — a revenue-conditional licence, so re-read it if the product ever earns |
| Kling 3.0 | Kuaishou / Kling's own API | Direct route exists; unverified |
| MiniMax H3 | MiniMax platform | Whether weights are open is contradicted between sources; that changes the sourcing story completely |
| HappyHorse 1.1 | Alibaba | fal was reported as the **launch** developer route (27 Apr 2026); Alibaba's own route is unverified |
| Marey Realism V1.5 | Moonvalley; also inside Adobe Firefly | Read the indemnification scope, not the headline — one source notes indemnification covering the company's data-collection contractors, which is not the same as indemnifying us |
| ElevenLabs v3 | ElevenLabs API | Direct route well established |
| Sync-3 | sync.so API | Sold as raw API access, which is what we want |
| Ideogram V3 · Recraft V3 | Each vendor's own API | Recraft's native SVG output may only exist on the direct route — worth checking, since the output format is the entire reason it is on the roster |

---

## What "other legitimate access" would mean, and why we are not recommending it

Several unified aggregators appeared repeatedly in research — Replicate, OpenRouter, Atlas
Cloud, WaveSpeed, Runware, SiliconFlow, AI/ML API, ModelsLab and others. They are real
production platforms and some carry roster models.

**We are not recommending any of them, for one reason: version provenance.** An aggregator
that cannot tell us exactly which build served a request makes every measurement taken through
it provisional, because the model can change underneath a Registry row with no signal to us.
The existing rule in this project is the right one — **prefer whichever route can be
version-pinned** — and it is the rule that should decide, not catalogue breadth.

If a Must-test model turns out to be reachable *only* through an aggregator, that is worth
revisiting deliberately, with the pinning question answered first. No roster model is in that
position today.

---

## Honest summary of this pass

- **Solid:** four Google-lineage rows, with exact identities, GA dates and printed prices.
- **Plausible and specific:** direct routes for roughly a dozen more, named at vendor level
  with the right documentation host identified.
- **Weak:** MAI-Image-2.5-Pro has no evidenced route at all.
- **Risky:** Runway Aleph 2.0 may be enterprise-only, and it is a Must row.
- **Not attempted, deliberately:** no signup, no terms accepted, no key requested, no call made.
