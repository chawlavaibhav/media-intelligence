# E8-A — Independent model universe

**Task:** EVAL-008 · **Date:** 26 Aug 2026 · **Branch:** `claude/eval-008-cloud-model-access-i3fl86`
(the task file names the logical branch `work/eval-008-model-access`; see the Controller Brief)

**Status: COMPLETE, with one dominant evidence caveat.**
**0 API calls · ₹0 spent · no account created · no terms accepted · no Registry row.**

---

## Read this first — what this document is, and how much weight it can carry

This is the **candidate list**: every current image, video and supporting-media model
family that plausibly deserves empirical testing, described by what it can uniquely do.
It is deliberately built **before** anyone looked at which provider we can reach cheaply.

The next document, `MODEL-ROSTER-FIRST.md`, cuts this list down to what we should
actually pay to measure. Only after that do the sourcing documents exist.

### The evidence caveat, stated once and applied everywhere

**This session could not open almost any provider's own website.** The cloud
environment's network policy answered `403` to nearly every vendor domain we tried —
OpenAI, fal, Black Forest Labs, Runway, ElevenLabs, ByteDance/BytePlus, MiniMax, Kling,
Ideogram, Stability, Replicate, Luma, Sarvam, Hugging Face, Artificial Analysis and
others. Twenty-six domains were probed directly and one answered.

That means most facts below reach us **second-hand**, through a web-search tool that
reads pages on our behalf and summarises them. That is real retrieved current
information, not memory — it repeatedly returned models released *after* this
assistant's May 2026 training cutoff, which memory could not have produced. But it is
**not** the same as reading a vendor's documentation, and it must not be treated as if
it were.

So every claim below carries an evidence tier:

| Tier | Meaning | How much it can support |
|---|---|---|
| **T1 — primary, read directly** | We fetched the page ourselves in this session. Only `cloud.google.com` was reachable. | Exact model IDs, prices, availability. Good enough to act on. |
| **T2 — provider page, read via search** | The search tool read a page **owned by the vendor or the platform** (e.g. `fal.ai/models/...`, `sarvam.ai`, `developers.openai.com`) and summarised it. | Good enough to say a model/route **probably** exists and roughly what it does. **Not** good enough to pin a version or a price. |
| **T3 — third-party** | A comparison blog, leaderboard summary or news article. | Good enough to say a model is **currently talked about as serious**, and to compare families. **Never** good enough for identity, availability or price. |

**Practical consequence:** nothing in this whole task authorises spending money. Before
any paid run, each selected model's exact version and price must be confirmed from the
provider's own catalogue — which is a lookup, not research, and needs an environment
that can reach those sites.

### One demonstrated reason to distrust T3 for prices

Third-party pages said Veo 3.1 costs "$0.03/sec" and "$0.40/sec" in different articles.
Google's own pricing page (T1, read directly today) prices **Veo 3.1 at $0.40 per
generated video with audio at 720p/1080p**, billed per count, not per second. Two
third-party sources, two different numbers, both wrong in unit and magnitude. This is
exactly the trap the previous task (E2) refused to walk into, and the rule stands:
**a price is only a price when it comes from the provider.**

---

## How a candidate earned a place here

A model is listed if it represents **at least one materially distinct production
hypothesis** — something we would learn by testing it that we would not learn from the
others. Being popular is not a hypothesis. Being #1 on a leaderboard is not a
hypothesis either; it is evidence that a model is currently serious.

Provider availability was **not** a criterion and was not consulted while building
this list.

### The nine production lanes

1. Image — text-to-image / commercial creative
2. Image — editing / inpainting / instruction edits
3. Image — reference / person / product / identity conditioning
4. Image — text, typography, design, vector
5. Video — text-to-video
6. Video — image / reference-to-video
7. Video — video-to-video, edit, extend, keyframe, multi-shot control
8. Video — native audio / dialogue
9. Supporting media — TTS / voice / lip-sync / avatar

### Two product facts that shape every judgement below

- **The product is Indian-market commercial media in English, Hindi and Hinglish.** A
  model that is beautiful but cannot spell a Hindi brand name is not usable for the
  first product. The project already owns a battery built to catch exactly that failure
  (`eval/battery/devanagari-exactness/`, 96 items with labels known by construction).
- **The metric is Cost per Accepted Outcome, not cost per generation.** A cheap model
  that needs six retries is not cheap. This is why cost-tier variants of the *same*
  model (fast/lite tiers) are treated as genuine candidates and not as noise.

---

## The candidate records

Fields per candidate: vendor/family · version evidence · lanes · what it uniquely does ·
why it is currently serious · the hypothesis it would test · redundancy · status.

Status values: `must_test` · `should_test` · `reserve` · `exclude`.
Statuses here are the **outcome** of the selection reasoning in `MODEL-ROSTER-FIRST.md`;
that document is where the reasoning is argued.

---

### Lane 1 + 2 + 3 + 4 — Image

#### GPT Image 2 — OpenAI
- **Version evidence:** model id `gpt-image-2` (T2, `developers.openai.com` via search). Released April 2026; successor to GPT Image 1 and 1.5.
- **Lanes:** 1, 2, 3, 4
- **Uniquely does:** plans a layout and can self-check before rendering ("thinks before it draws"), rather than denoising in one shot. Vendor-side claim of ~99% character accuracy across Latin, Chinese, Japanese, Korean, **Hindi and Bengali**, up from 90–95% on its predecessor (T3, multiple).
- **Currently serious:** reported #1 on the Artificial Analysis Text-to-Image Arena at ~1370 Elo, August 2026 (T3). Reported #3 on the editing arena (T3).
- **Hypothesis it tests:** *does a frontier vendor's typography claim survive a battery whose right answers are known by construction?* This is the single most valuable measurement available to this project, because the claim is specific, falsifiable, and about the exact script the product needs.
- **Redundancy:** overlaps Nano Banana and Reve on general image quality. Does not overlap on the Devanagari claim — nobody else makes one.
- **Status:** `must_test`

#### Gemini 3.1 Flash Image ("Nano Banana 2") — Google
- **Version evidence:** **T1.** `Nano Banana 2` = `Gemini 3.1 Flash Image`; generally available 28 May 2026 on Vertex AI (Gemini Enterprise Agent Platform) and the Gemini API; 1K and 2K GA, 4K in preview. Console model parameter observed as `gemini-3.1-flash-image`. Priced on Google's own page at **$60.00 / 1M image output tokens**, $0.50 / 1M text-image-video input tokens. A **Gemini 3.1 Flash-Lite Image ("Nano Banana 2 Lite")** exists at $30.00 / 1M image output tokens.
- **Lanes:** 1, 2, 3
- **Uniquely does:** described as purpose-built for **identity preservation** across edits (T3); the fast tier of a frontier family, 2–3× faster and about half the cost of the Pro tier (T3).
- **Currently serious:** in the elite arena cluster (T3); default image model in the Gemini app since Feb 2026 (T3); GA with enterprise SLA on Vertex (T1).
- **Hypothesis it tests:** *is the cheap tier of a frontier family good enough to be our production default?* Directly a Cost-per-Accepted-Outcome question, and the answer changes our unit economics more than any leaderboard rank.
- **Redundancy:** high overlap with Nano Banana Pro — deliberately, because the pair is the test.
- **Status:** `must_test`

#### Gemini 3 Pro Image ("Nano Banana Pro") — Google
- **Version evidence:** **T1.** `Nano Banana Pro` = `Gemini 3 Pro Image`, GA 28 May 2026, same platforms. Priced at $0.20 / 1M cached input tokens and $12.00 / 1M text output tokens on Google's page; the image-output cell is not populated in the table we read, so **its image price is NOT VERIFIED**.
- **Lanes:** 1, 2, 3, 4
- **Uniquely does:** built on the flagship reasoning model, so deeper scene understanding, complex multi-element composition, and fine typography for packaging and print (T3).
- **Currently serious:** GA, retained for paid Gemini tiers after Nano Banana 2 became default (T1/T3).
- **Hypothesis it tests:** *what does the extra money actually buy?* Only meaningful when measured against Nano Banana 2 on the same items.
- **Redundancy:** paired with Nano Banana 2 by design.
- **Status:** `should_test`

#### Seedream 5.0 Pro — ByteDance
- **Version evidence:** Seedream 5.0 Pro documented on BytePlus ModelArk (T2, `docs.byteplus.com` title via search). Predecessor Seedream 4.5 shipped early 2026 (T3). **Which version we would test is NOT VERIFIED** — 4.5 and 5.0 both appear in current sources.
- **Lanes:** 1, 2, 3
- **Uniquely does:** described as the "intelligent reasoning" pole of the 2026 image landscape; strongest on editorial/fashion and stylisation (T3).
- **Currently serious:** consistently placed in the elite cluster across independent comparisons (T3).
- **Hypothesis it tests:** *does a non-US training lineage change what gets accepted for Indian-market commercial creative?* Every other frontier image candidate is US or European. Aesthetic priors are not universal, and acceptance is a human judgement.
- **Redundancy:** overlaps GPT Image 2 / Nano Banana on general quality; the lineage difference is the point.
- **Status:** `must_test`

#### Reve 2.1 — Reve AI
- **Version evidence:** launched 9 July 2026 (T3). Reve API documented on the vendor's own blog (T2, `blog.reve.com/posts/the-reve-api`).
- **Lanes:** 1, 2, 4
- **Uniquely does:** treats an image as a **structured, addressable set of regions** — "image as code" — planning a hierarchical layout before rendering, so a single element can be edited without re-rolling the whole picture. Reported native 4K, and lossless iterative edits that preserve typography and brand elements. Edit endpoints reportedly out-perform its own create endpoint (all T3, with the architecture claim also on the vendor blog, T2).
- **Currently serious:** reported #2 on the Text-to-Image Arena at ~1306 Elo and #2 on the editing arena at ~1263 Elo (T3).
- **Hypothesis it tests:** *does a structured intermediate representation reduce Cost per Accepted Outcome by removing the re-roll?* This is the most architecturally interesting candidate in the entire universe for this project specifically, because the project's own design separates a Creative IR from a Production IR. Reve is the first commercial model that appears to expose something like that separation at the API surface.
- **Redundancy:** none on the mechanism. Overlaps on raw quality only.
- **Status:** `must_test`

#### FLUX.2 family — Black Forest Labs
- **Version evidence:** FLUX.2 released 25 Nov 2025; variants `[max]`, `[pro]`, `[flex]`, `[dev]`, `[klein]` (T2/T3, incl. `bfl.ai` page titles). `[dev]` ~32B, needs ~32GB VRAM at FP8 and a **separate commercial licence**; `[klein]` is Apache-2.0 open weights. **Sources conflict on `[klein]`'s size — 9B in one, 4B in another. NOT VERIFIED.**
- **Lanes:** 1, 2, 3
- **Uniquely does:** one family spanning a closed top tier and genuinely open weights, with instruction-based context editing (the Kontext line) as its headline. Native generation up to 4MP.
- **Currently serious:** repeatedly described as the open-weight quality benchmark and a frontier-adjacent closed option (T3).
- **Hypothesis it tests (closed tier):** *how good is dedicated instruction-editing compared with a general frontier model doing edits as a side capability?*
- **Hypothesis it tests (open tier):** *what does self-hosting cost us per accepted outcome, once GPU time and engineering are counted?*
- **Redundancy:** the closed tier overlaps Reve and Nano Banana on editing. The open tier overlaps Qwen-Image on open economics, but at a very different size and licence.
- **Status:** `[pro]` `must_test` · `[klein]` `should_test` · `[max]`/`[flex]`/`[dev]` `reserve`

#### Qwen-Image / Qwen-Image-Edit — Alibaba
- **Version evidence:** `Qwen-Image-2512` cited as the current deployable Apache-2.0 build; `Qwen-Image-Edit` is the instruction-tuned editor on a ~20B base (T3). Version currency **NOT VERIFIED**.
- **Lanes:** 1, 2, 4
- **Uniquely does:** among open models, reported best at rendering **legible in-image text**, with strong multilingual prompt support — under Apache 2.0, which permits commercial use without a separate licence negotiation.
- **Currently serious:** named in multiple independent 2026 round-ups as the deployable open standard (T3).
- **Hypothesis it tests:** *can an open, self-hostable model carry the text-exactness burden — and if so, what does that do to our marginal cost?* If the answer is yes even at a lower quality ceiling, the economics of the whole product change, because marginal cost stops scaling with volume.
- **Redundancy:** overlaps FLUX.2 `[klein]` on "open economics", but Qwen's distinctive claim is text and multilingual, which is our exact pain.
- **Status:** `must_test`

#### MAI-Image-2.5 / MAI-Image-2.5-Pro — Microsoft
- **Version evidence:** T3 only. Reported as leading the Artificial Analysis **Image Editing** Arena at ~1271 Elo. Access route **NOT VERIFIED**.
- **Lanes:** 1, 2
- **Uniquely does:** currently reported as the best instruction editor by blind human preference.
- **Currently serious:** editing-arena #1 (T3), elite cluster on text-to-image (T3).
- **Hypothesis it tests:** *is the blind-preference editing leader also the best editor for commercial production work, where "preferred" and "usable" are different questions?*
- **Redundancy:** substantial with Reve 2.1 and FLUX.2 on editing. Kept because it comes from a lineage none of our other picks share.
- **Status:** `should_test`

#### Ideogram V3 — Ideogram
- **Version evidence:** V3 with Turbo / Default / Quality tiers (T2, seen on partner platform pages and `fal.ai/models`).
- **Lanes:** 1, 4
- **Uniquely does:** the long-standing typography specialist — signage, packaging, labels, posters, logos. Reported ~90–95% text accuracy against 30–50% for general models (T3, and that comparison predates GPT Image 2).
- **Currently serious:** still the reference point every typography comparison is written against (T3).
- **Hypothesis it tests:** *if the frontier generalist fails on Devanagari, does the specialist succeed?* Its value is as a **named fallback that is already measured** on the day GPT Image 2 disappoints — not as a challenger for the top slot.
- **Redundancy:** overlaps GPT Image 2 on the text hypothesis. Justified in the roster document.
- **Status:** `should_test`

#### Recraft V3 — Recraft
- **Version evidence:** T3. Topped the text-to-image arena in late 2024; still cited in 2026 as the only major model with **native SVG vector output**.
- **Lanes:** 1, 4
- **Uniquely does:** emits real vector artwork, not pixels. Type stays type: scalable, re-editable, and correct by construction rather than by luck.
- **Currently serious:** its ranking is stale, but its capability is still described as unique in 2026 sources (T3).
- **Hypothesis it tests:** *can we sidestep raster text failure entirely for the parts of a creative that are design rather than photography?* A logo, a price flash, a packaging lockup rendered as vector cannot misspell Hindi in the way a diffusion model can.
- **Redundancy:** none on output format. Its risk is scope, not overlap — see the roster document.
- **Status:** `should_test`

#### Others considered in the image lanes
| Candidate | Why it is here | Status | Reason |
|---|---|---|---|
| Imagen 4 / 4 Ultra / 4 Fast (Google) | Priced on Google's page today at $0.04 / $0.06 / $0.02 per image (**T1**) | `exclude` | Superseded within its own vendor by the Gemini 3.x image models we already selected. Testing both spends money to learn the same thing. |
| Nano Banana (v1), Ideogram V2, Seedream 4.5, FLUX.1 Kontext | Named in current comparisons | `exclude` | Superseded by a newer version of the same family already on the list. |
| Midjourney | Aesthetic ceiling is genuinely distinct | `reserve` | Its hypothesis ("is there an aesthetic ceiling we are missing?") is real but weakly separable from the frontier picks, and its production-API route is unclear. Reserve on **redundancy**, with the route question recorded separately so it is not mistaken for the reason. |
| NVIDIA Cosmos 3 Super | Reported strongest open-weight image model at #7 overall (T3) | `reserve` | Overlaps Qwen-Image and FLUX.2 `[klein]` on the open-economics hypothesis; its identity and licence are less clearly evidenced. |
| GLM Image, Grok Imagine | Appear in current platform catalogues (T2) | `reserve` | No differentiated capability evidence found. Listing them is honest; testing them now would be shopping, not measuring. |

---

### Lane 5 + 6 + 7 + 8 — Video

#### Seedance 2.0 (Pro / Fast) — ByteDance
- **Version evidence:** released Feb 2026; documented on BytePlus ModelArk as the "Dreamina Seedance 2.0 series" (T2, doc page titles). Unified multimodal architecture taking text, image, audio and video inputs (T2).
- **Lanes:** 5, 6, 8
- **Uniquely does:** native audio, camera control and physics, at the best reported quality-per-rupee of any credible tier — a Fast tier at roughly $0.022/sec against a Pro tier at roughly $0.70 per video (T3, both unverified).
- **Currently serious:** took #1 on both text-to-video and image-to-video arenas on launch and remains top-three through August 2026 across several independent summaries (T3). Numbers disagree between sources; the ordering does not.
- **Hypothesis it tests:** *where is the cost/quality knee?* Testing Pro and Fast as two separate workflow rows is the cheapest way this project can ever measure whether paying more buys accepted outcomes.
- **Redundancy:** overlaps every other T2V candidate on raw quality; unique on the price/quality frontier at credible quality.
- **Status:** `must_test` (two rows: Pro and Fast)

#### HappyHorse 1.1 (and 1.0) — Alibaba
- **Version evidence:** 1.0 debuted anonymously on the arena ~7 April 2026 and took #1 in both T2V and I2V by a reported 107-Elo margin; 1.1 is the newer, stronger audio-video release while 1.0 still scores higher on silent video (T3). 15B unified transformer generating video and audio in one forward pass (T3).
- **Lanes:** 5, 6, 7, 8
- **Uniquely does:** **lip-synced dialogue in seven languages generated in a single pass**, plus a natural-language **video-edit** capability alongside text-to-video, image-to-video and reference-to-video.
- **Currently serious:** the anonymous arena debut is unusually strong evidence — it was preferred before anyone knew whose model it was, which removes brand bias from the result.
- **Hypothesis it tests:** *is one-pass multilingual dialogue video good enough to replace our compose-from-parts route?* If yes, an entire pipeline stage disappears. If no — and specifically if Hindi is not among the seven languages — that finding alone justifies keeping the TTS + lip-sync route.
- **Redundancy:** overlaps Kling and Veo on native audio; unique on breadth of language coverage claimed.
- **Status:** `must_test`

#### Veo 3.1 (and Fast / Lite tiers) — Google
- **Version evidence:** **T1.** Priced on Google's own page: Veo 3.1 video+audio **$0.40 per generation** at 720p/1080p, **$0.60** at 4K; silent video $0.20 / $0.40. Veo 3.1 Fast: $0.10 (720p) / $0.12 (1080p) / $0.30 (4K) with audio. Veo 3.1 Lite: $0.05 (720p) / $0.08 (1080p) with audio. Veo 2 is separately priced at $0.50 and is the only Veo row whose listed features include **"Advanced Controls — start and end frame interpolation, extend generated videos, and apply camera controls."**
- **Lanes:** 5, 6, 8 (and 7, subject to the control question below)
- **Uniquely does:** synchronised speech at 48kHz and the most "stock-footage-like" default output (T3); a full published price ladder across three cost tiers (T1); enterprise SLA on Vertex (T1).
- **Currently serious:** consistently top-three, and the reference point every competitor is measured against (T3).
- **Hypothesis it tests:** *what is the accepted-outcome rate of the market's default choice, and how far down its own cost ladder can we go before acceptance breaks?*
- **Open question worth flagging:** Google's live pricing table lists advanced frame/extend/camera controls under **Veo 2**, not under Veo 3.1. Whether Veo 3.1 exposes those controls is **NOT VERIFIED** and matters, because it decides whether Veo can serve lane 7 at all.
- **Redundancy:** overlaps Seedance and Kling on native-audio T2V.
- **Status:** `must_test`

#### Kling 3.0 — Kuaishou
- **Version evidence:** T2/T3. Native audio generation new in 3.0, with lip-sync in **five documented languages: English, Chinese, Japanese, Korean, Spanish** (T3 — and the absence of Hindi from that list is itself a finding). Custom "element" support for subject consistency (T2, platform page).
- **Lanes:** 5, 6, 7, 8
- **Uniquely does:** **multi-shot cinematic sequences with subject consistency across cuts** — the thing an advert actually is. Reported as the most accurate lip-sync among the general video models.
- **Currently serious:** four entries in the reported top ten (T3).
- **Hypothesis it tests:** *can a model hold a person or product identical across several shots?* Multi-shot state continuity is a distinct failure mode: a model can be excellent per clip and useless across a 20-second spot.
- **Redundancy:** overlaps on native audio; unique on multi-shot continuity as an explicit product feature.
- **Status:** `must_test`

#### MiniMax H3 / Hailuo 03 — MiniMax
- **Version evidence:** T2/T3. Native 2K, 24fps, 5–15s extendable to ~30s, synchronised dialogue plus sound effects and ambience in one pass. **Omni-reference: up to 9 reference images, 3 video clips and 3 audio clips.** Also V2V motion transfer and instruction editing. One platform page describes it as **open-weights**, which conflicts with its API-product framing elsewhere — **NOT VERIFIED**.
- **Lanes:** 5, 6, 7, 8
- **Uniquely does:** by far the **richest reference-conditioning surface** of any candidate — nine images plus video plus audio as conditioning in one call.
- **Currently serious:** reported ~1242 Elo, second on text-to-video with audio (T3).
- **Hypothesis it tests:** *does giving a model many references actually make a person or product stay itself?* Nobody else lets us vary reference count as an experimental variable. That makes H3 the instrument for the identity-consistency question, not merely a competitor.
- **Redundancy:** overlaps Kling on consistency; unique on controllable reference richness.
- **Status:** `must_test`

#### Runway Aleph 2.0 — Runway
- **Version evidence:** T2/T3. Announced 21 May 2026 with an "Edit Studio" product. Up to 30s at 1080p, edits across up to 10 cuts, up to 5 keyframe anchor images at chosen timestamps. **A T3 source states Runway API access moved to Enterprise in January 2026** — a material access constraint, **NOT VERIFIED**.
- **Lanes:** 7 (primary), 6
- **Uniquely does:** **edits real footage** from a natural-language instruction — changes camera angle, relights, isolates subjects, swaps objects — while preserving the original motion and continuity. Every other video candidate generates from nothing.
- **Currently serious:** the category-defining product for in-context video editing (T3), also surfaced inside Adobe Firefly (T3).
- **Hypothesis it tests:** *is fixing footage cheaper per accepted outcome than generating it?* For a client who already has a shoot, this is not a marginal improvement, it is a different business. No other candidate answers it.
- **Redundancy:** partially overlaps HappyHorse's video-edit and MiniMax's V2V. Distinct in that it is built around preserving an existing take rather than re-generating one.
- **Status:** `must_test`

#### Gemini Omni Flash — Google
- **Version evidence:** **T1 for price and existence** — Google's own pricing page lists "Gemini Omni Flash" with **video output at $17.50 / 1M tokens, charging 5,792 tokens per second of 720p video output with audio** (≈ $0.101 per second, computed from Google's own numbers), $1.50 / 1M multimodal input. T2/T3 for capability: announced at Google I/O 19 May 2026; accepts any combination of text, image, audio, video; 10-second clips; audio generated natively rather than dubbed on. Audio *reference inputs* reportedly not yet supported in the June 30 API version.
- **Lanes:** 5, 6, 7, 8
- **Uniquely does:** a **conversational generate-and-edit loop** — the video is revised by continuing a conversation rather than by re-prompting from scratch.
- **Currently serious:** reported leading text-to-video-with-audio at ~1245 Elo (T3).
- **Hypothesis it tests:** *does conversational iteration converge on an accepted outcome faster than re-prompting?* That is a Cost-per-Accepted-Outcome question about the interaction pattern, not about the pixels.
- **Redundancy:** shares Google's lineage with Veo 3.1. Kept because the interaction model is different, and that is what we would be measuring.
- **Status:** `should_test`

#### Wan 2.7 / 2.6 — Alibaba (open weights)
- **Version evidence:** Wan 2.2 is the widely documented Apache-2.0 release; catalogues currently list **Wan 2.6 and Wan 2.7**, and one platform page calls 2.7 "the latest generation" (T2). **Which version carries which licence is NOT VERIFIED** and matters a great deal.
- **Lanes:** 5, 6
- **Uniquely does:** open weights under a permissive licence, with the best reported photorealistic human rendering among open video models. No native audio.
- **Currently serious:** the default open video baseline in every 2026 open-source round-up (T3).
- **Hypothesis it tests:** *what is the true cost of owning the video step?* Requires ~80GB-class GPUs at full quality (T3), so the honest answer includes GPU hours and engineering time, not just "free".
- **Redundancy:** overlaps LTX on open economics; differs in having no native audio.
- **Status:** `should_test`

#### LTX-2 family — Lightricks (open weights)
- **Version evidence:** T2/T3, and **badly ambiguous**: current sources name LTX-2, LTX-2.3, LTX-2.3 Fast and LTX-2.5 as if all were current. Licence reported as free below $10M ARR (T3). **NOT VERIFIED.**
- **Lanes:** 5, 8
- **Uniquely does:** among open models, reported to be the only one generating **audio and video together natively**, plus 4K, up to ~20s, LoRA fine-tuning, and markedly faster inference (roughly 3× a comparable open model on the same GPU, T3).
- **Currently serious:** named in every open-video comparison (T3).
- **Hypothesis it tests:** *can we own the native-audio-video step, not just the silent one?* Distinct from Wan precisely because of the audio.
- **Redundancy:** overlaps Wan on open economics only.
- **Status:** `should_test`

#### Marey Realism V1.5 — Moonvalley
- **Version evidence:** T2 — endpoints for text-to-video, image-to-video and motion-transfer appear on a platform's own model pages. Trained exclusively on licensed data; Moonvalley provides indemnification, though one source notes it covers its data-collection contractors specifically (T3).
- **Lanes:** 5, 6, 7
- **Uniquely does:** the **clean-rights** hypothesis. Every other video candidate's training data provenance is either undisclosed or contested.
- **Currently serious:** partnered into Adobe Firefly as a commercially-safe option (T3).
- **Hypothesis it tests:** *what does commercial safety cost us in quality?* The project's stated rights posture is internal-research-only, and says the rights question must be reopened before anything is shown to a customer. That day, this number is the one we will need and will not have time to measure.
- **Redundancy:** none on provenance. Quality likely below frontier.
- **Status:** `should_test`

#### Others considered in the video lanes
| Candidate | Why it is here | Status | Reason |
|---|---|---|---|
| **Sora 2 (OpenAI)** | Was a category leader | `exclude` | **Reported deprecated 26 April 2026 with the API shutting down 24 September 2026 (T3).** Measuring it would create a Capability Registry row that expires within weeks of being written. This is an exclusion on **model viability**, not on sourcing. Verify before finalising. |
| Runway Gen-4.5 | Led at launch in late 2025 | `exclude` | Reported to have dropped out of the top ten (T3), and superseded within its own vendor by Aleph 2.0 for the capability we actually want. |
| Veo 2, Veo 3, Kling 2.5, Hailuo 02, Seedance 1.5 | Still sold and priced | `exclude` | Superseded within their own families by a candidate already selected. |
| Vidu Q3, PixVerse V6 | Genuine cost-frontier options with native audio (T3) | `reserve` | The cheap tier is already covered by Seedance 2.0 Fast and Veo 3.1 Lite, which are variants of models we are testing anyway — so we learn the cost/quality knee without adding two vendors. |
| HunyuanVideo 1.5 (Tencent) | Major open video model, slimmed to 8.3B (T3) | `reserve` | Wan and LTX cover the open lane; Hunyuan's licence is reported as more restrictive. |
| Grok Imagine | Appears in current catalogues (T2) | `reserve` | No differentiated capability evidence found. |

---

### Lane 9 — Supporting media: voice, lip-sync, avatar

#### Sarvam Bulbul v3 — Sarvam AI
- **Version evidence:** T2 (`sarvam.ai`, `docs.sarvam.ai` via search). 11 Indian languages — Indian English, Hindi, Bengali, Tamil, Telugu, Kannada, Malayalam, Marathi, Gujarati, Punjabi, Odia — with an expansion to 22 stated as forthcoming. 30+ persona voices. **Explicit Hinglish code-switching.** Sub-250ms streaming. Beta pricing stated as **₹30 per 10,000 characters, August 2026**. Data processed and stored in India.
- **Lanes:** 9
- **Uniquely does:** treats Hindi and Hinglish as first-class rather than as entries in a long language list, and prices in rupees at roughly an order of magnitude below Western per-character rates (T2/T3).
- **Currently serious:** it is the Indian-language voice reference in current comparisons, and no global model documents Hinglish code-switching.
- **Hypothesis it tests:** *does an India-first voice model pronounce Indian brand names, Hinglish ad copy and Devanagari numerals correctly where a global model does not?* This is the same class of failure as the Devanagari image problem, in audio.
- **Redundancy:** none. It is the only India-first candidate.
- **Status:** `must_test`

#### ElevenLabs v3 — ElevenLabs
- **Version evidence:** T2 (platform model page). "Eleven v3" — natural, emotionally-aware, **70+ languages**; Multilingual v2 (29 languages) and Turbo v2.5 also current.
- **Lanes:** 9
- **Uniquely does:** the global quality reference for expressive narration.
- **Currently serious:** named at the top of every 2026 TTS comparison (T3); arena leadership currently contested by Inworld and Cartesia (T3).
- **Hypothesis it tests:** *is the global leader actually worse than the India-first model on Hindi and Hinglish?* Without this arm, the Bulbul result is a number with nothing to compare it to. **It is on the roster as a control, and that is the honest reason.**
- **Redundancy:** paired with Bulbul by design.
- **Status:** `must_test`

#### Sync-3 — sync.so
- **Version evidence:** T2 (platform model pages list `sync-3` and `sync lipsync 2.0`). Described as their most powerful lip-sync model, with "native visual intelligence".
- **Lanes:** 9
- **Uniquely does:** a **transformation**, not a generation: it takes video we already have plus audio we already have and makes the mouth match. Because both inputs are ours, some checks become deterministic — we know exactly what was said.
- **Currently serious:** the reference raw-API lip-sync product (T3).
- **Hypothesis it tests:** *is TTS + lip-sync the only working route to Hindi dialogue video?* This matters because the native-audio video models document five or seven languages and **Hindi is not among the documented ones**. If that holds, this route is not a fallback — it is the route.
- **Redundancy:** overlaps OmniHuman on outcome, not on workflow.
- **Status:** `must_test`

#### OmniHuman v1.5 — ByteDance
- **Version evidence:** T2 (platform model page). Generates video from **a single human image plus an audio file**, with emotion and movement correlated to the audio.
- **Lanes:** 9
- **Uniquely does:** needs no source video at all — one photograph becomes a speaking presenter.
- **Currently serious:** benchmarked against the major avatar products in current comparisons (T3).
- **Hypothesis it tests:** *can we produce a spokesperson without ever shooting one?* Different input contract from Sync-3, so a different cost structure and a different set of failure modes.
- **Redundancy:** overlaps Sync-3 on the finished artefact only.
- **Status:** `should_test`

#### Others considered in lane 9
| Candidate | Why it is here | Status | Reason |
|---|---|---|---|
| Cartesia Sonic 3.5 | ~90ms time-to-first-byte; Hindi added in a May 2026 multilingual update (T3) | `reserve` | Its distinctive advantage is latency, and produced media is not latency-bound. Promote if we ever build a real-time product. |
| Inworld TTS-1.5 Max / TTS-2 | Reported top of the Artificial Analysis Speech Arena at ~1236 Elo (T3) | `reserve` | Arena leadership in general speech does not evidence Indic competence, which is the only voice question we currently have. |
| Gemini 3.1 Flash TTS | In the reported top tier (T3) | `reserve` | Redundant with the Google lineage we already test, unless Google documents Indic quality specifically. |
| Chatterbox (open) | 23 languages including Hindi; reported to beat ElevenLabs in blind preference (T3) | `reserve` | Real open-economics candidate for voice. Held back only because voice is not yet the binding constraint; promote if Bulbul and ElevenLabs both prove expensive at volume. |
| HeyGen, Veed Fabric 1.0, Hedra | Strong avatar/dubbing products (T3) | `reserve` | Product suites rather than model endpoints; they answer the same hypothesis as Sync-3 and OmniHuman with more wrapper. |
| Lyria 3 / Lyria 3 Pro (Google) | Music generation, priced today at $0.04 / $0.08 per count (**T1**) | `reserve` | Music has not been established as part of our production route. Cheap to add later; premature to admit now. |

---

## What this universe says, in one paragraph

The frontier has stopped being a single ranking. In images, one model plans before it
draws, another treats the picture as editable structure, another preserves identity
cheaply, and an open Apache-2.0 model is credibly good at exactly the multilingual text
we struggle with. In video, quality is no longer the scarce thing — **control** is:
reference conditioning, multi-shot continuity, and editing footage that already exists.
And across the whole board there is one gap that matters more to this product than any
Elo score: **the models that generate speech natively document five or seven languages,
and Hindi is generally not one of them.** That single observation is why the supporting
voice and lip-sync lane is not a nice-to-have in the roster that follows.
