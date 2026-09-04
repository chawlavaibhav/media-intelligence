# EVAL-008 — Controller Brief

**Task:** EVAL-008 — Cloud Model Selection & Sourcing Research
**Date:** 26 Aug 2026 · **Autonomy:** autonomous · **Environment:** Claude cloud session
**Branch:** `work/eval-008-model-access`

**Status: COMPLETE.** Frontier Clouds identity resolved by the Controller on 26 Aug 2026; the
E8-C availability pass was then executed against all three hyperscalers.
**0 API calls · ₹0 spent · no account created · no terms accepted · no Registry row · no merge.**

> **Communication check:** I will explain technical ideas in plain English, including what
> they mean, why they matter, and their practical consequence; use minimum sufficient wording
> without sacrificing understandability; separate evidence from inference; and never invent
> facts. I have read `shared/COMMUNICATION-STANDARD.md`.

---

## 1. The five answers, in the order the task asks for them

**1. Which models should we test, independent of sourcing, and why?**
**26 rows — 16 Must (15 distinct models; Seedance 2.0 contributes two workflow rows) and 10
Should.** Each earns its place by answering a question no other row answers. The full argument
is in `MODEL-ROSTER-FIRST.md`; §3 below gives the shape of it.

**2. Which of those are available on Frontier Clouds?**
**7 of 26.** The Controller resolved the name: *Frontier Clouds* means the three hyperscalers —
GCP, AWS and Azure — not one service, which is why three searches for a product name found
nothing. **Google Cloud carries 4** (Nano Banana 2, Veo 3.1 with its Fast and Lite tiers, Nano
Banana Pro, Gemini Omni Flash), all with prices we read from Google's own pages. **Azure carries
3** (GPT Image 2, FLUX.2 [pro], MAI-Image-2.5-Pro). **AWS Bedrock carries none** — see §4c, it is
the finding with the most immediate money attached. Detail in `FRONTIER-CLOUDS-AVAILABILITY.md`.

**3. Of the remainder, which are on fal?**
**14 of the remaining 19, at planning confidence only.** Ten are described on fal's own model
pages; four more are present as a family with the version unresolved. **fal.ai itself was
unreachable from this session**, so none of it is verified — see §5.

**4. For the remainder, exactly where do we source them?**
Two rows look genuinely absent from both preferred routes: **Runway Aleph 2.0** (Runway's own API,
possibly enterprise-gated) and **Sarvam Bulbul v3** (Sarvam's own API, Indian vendor, rupee
billing). Three more — Qwen-Image, Recraft V3, FLUX.2 [klein] — we could not confirm either way.
Details in `DIRECT-AND-OTHER-SOURCES.md`.

**5. Which new accounts does the user actually need?**
**Two at most, neither needing money today:** Sarvam AI, and — subject to one check — Runway.
**Microsoft/Azure is no longer on this list**: MAI-Image-2.5-Pro turned out to be on Foundry, on
existing credits. `ACCOUNT-ACTIONS.md` is the actionable page.

---

## 2. Required anti-bias check — proof that sourcing did not shape selection

This is the part of the task that matters most, so it is evidenced mechanically rather than
asserted.

### 2a. Order of work, provable from git

| Commit | Time (UTC) | Contents |
|---|---|---|
| `9583864` | **2026-08-26 08:26:47** | `MODEL-UNIVERSE.md`, `MODEL-ROSTER-FIRST.md`, `model-selection-evidence.yaml` — **selection only, zero provider-route recommendations** |
| `469331e` | **2026-08-26 08:31:36** | The five sourcing artifacts — **zero changes to any selection file** |

Checkable in one command: `git diff --name-only 9583864 469331e -- <the three selection files>`
returns **nothing**. The roster was frozen before any route recommendation existed, and no
sourcing finding was allowed back into it.

**The invariant still holds after the Frontier Clouds identity arrived.** That answer changed
seven routes, corrected one model we had written off as unsourceable, and produced a warning about
AWS credits. **It changed no selection content.**

Stated precisely, because the check should be reproducible rather than rhetorical:

- `git diff --name-only 9583864 HEAD -- eval/model-access/2026-08-26/MODEL-ROSTER-FIRST.md`
  returns **nothing**. The roster is byte-identical to the moment it was frozen.
- `MODEL-UNIVERSE.md` and `model-selection-evidence.yaml` each carry **one** post-freeze edit, in
  commit `8761b9c`: a branch-name line in the header, made when the work moved to
  `work/eval-008-model-access`. In each file a two-line branch header collapsed to one line; the
  combined diff is six lines, all of it metadata, touching no candidate, no status and no
  hypothesis — inspect it directly rather than taking this on trust.
- The Frontier Clouds revisions are confined to the sourcing artifacts.

### 2b. Must/Should models NOT covered by Frontier Clouds or fal

The roster kept these anyway. That is the rule working.

| Model | Level | Access position | Why it stayed |
|---|---|---|---|
| **Runway Aleph 2.0** | **Must** | Not seen on fal; its own API may be **enterprise-only since Jan 2026** | It is the only row that edits footage we already have. For a client with an existing shoot that is a different business, not a better model. A hard access route does not change what we would learn. |
| **Sarvam Bulbul v3** | **Must** | Not seen on fal; needs a new account | The native-audio video models document five or seven languages and **Hindi is generally not among them**. Our first product is Hindi and Hinglish. Dropping this would leave the product's core language need unmeasured. |
| ~~MAI-Image-2.5-Pro~~ | Should | **Resolved — it is on Azure Foundry** | Kept at Should when we believed it had *no route at all*. That belief was wrong: resolving Frontier Clouds to the hyperscalers put it on Microsoft's own cloud, on existing credits. **The row survived a period of looking unsourceable, which is the rule working.** |
| Qwen-Image, Recraft V3, FLUX.2 [klein] | 1 Must, 2 Should | Not verified either way | Absence of evidence, not evidence of absence — we could not read the catalogue. |

**The headline number, now that the credits are known: 19 of 26 Must/Should rows are not on
Frontier Clouds, and not one row changed.** Twelve of the sixteen Must rows sit outside the
user's preferred credits entirely. If credits had been steering selection, that ratio would be
inverted.

Also worth stating: the **four open-weight rows** (Qwen-Image, FLUX.2 [klein], Wan 2.7, LTX-2)
carry an economics question that **neither fal nor a hyperscaler catalogue can answer**, because
running them as someone else's hosted endpoint measures that host's economics, not ours. Keeping
them is a deliberate acceptance that the convenient route does not serve the hypothesis.

### 2c. Attractive Frontier Clouds/fal models deliberately excluded

Models we saw in platform catalogues — cheap and immediately reachable — that did **not** earn a
slot. Credits made none of these tempting enough to admit.

| Model | Where it was attractive | Why it was still excluded |
|---|---|---|
| **Sora 2** | Named repeatedly, brand recognition — **and listed on Azure Foundry**, so free to reach on existing credits | **Reported deprecated 26 Apr 2026, API shutdown 24 Sep 2026.** A Registry row would expire within weeks. Exclusion on model viability, not on route. |
| **Imagen 4 / 4 Fast / 4 Ultra** | The **cheapest** thing we found with a real verified price ($0.02–$0.06/image, from Google's own page) — **and it sits on Frontier Clouds** | Superseded within Google by the Gemini 3.x image models we already selected. **Cheapness is not a hypothesis.** This is the clearest case on the page: the best price we hold, on the credits we already own, rejected. |
| **Amazon Nova Canvas · Nova Reel** | On Bedrock, i.e. on Frontier Clouds credits | Never earned a slot — and both are now **Legacy**, Canvas with an end-of-life of 30 Sep 2026. Same reasoning that excluded Sora 2. |
| **Luma Ray v2 · Stability (Stable Image Core/Ultra, SD 3.5 Large)** | On Bedrock and Azure, i.e. on Frontier Clouds credits | Neither answers a hypothesis the roster asks. Being the thing our credits happen to carry is not a qualification. |
| **Runway Gen-4.5** | On platform catalogues | Superseded in-vendor by Aleph 2.0 for the capability we want. |
| Vidu Q3, PixVerse V6 | Genuine cost-frontier video with native audio, on fal | The cost knee is already readable from Seedance 2.0 Fast and Veo 3.1 Lite — tiers of models we test anyway — without adding two vendors. |
| HunyuanVideo 1.5, Wan 2.5, SDXL, FLUX schnell/dev, Kling 2.5, Seedream 4.5, Hailuo 02, LTX earlier builds | All reported on fal | Superseded in-family, or redundant with a selected row. |
| Grok Imagine, GLM Image | On fal, currently topical | **No differentiated capability evidence found.** Testing them would be shopping, not measuring. |
| Hedra, HeyGen, Veed Fabric 1.0 | Strong avatar/dubbing products | Same hypothesis as Sync-3 and OmniHuman, with more product wrapper around it. |
| Cartesia Sonic 3.5, Inworld TTS | Speech-arena leaders | Their advantage is latency and general-speech preference. Produced media is not latency-bound, and general-speech leadership is not evidence of Indic competence — which is our only current voice question. |
| Lyria 3 / Lyria 3 Pro | Verified Google prices, $0.04–$0.08 per count | Music is not established as part of our production route. Cheap to add later; premature now. |

---

## 3. What the roster actually says — the shape of the answer

Three findings changed how the roster looks, and none of them is a leaderboard rank.

**The frontier stopped being a ranking; control became the scarce thing.** In video, quality is
broadly available and what differs is *control*: how many references you can condition on, whether
identity survives a cut, whether you can edit a take you already have. That is why MiniMax H3 is on
the list as an **instrument** (nine reference images makes reference count an experimental variable
nobody else offers) and why Runway Aleph is a Must despite being the hardest thing here to source.

**One vendor claim is worth more to us than any Elo score.** OpenAI's material claims roughly 99%
character accuracy including **Hindi and Bengali**. This project already owns a 96-item Devanagari
exactness battery whose right answers are known by construction — built precisely because a model
can produce text that is *subtly* wrong. That is a specific, falsifiable claim meeting an instrument
already built to test it. Either answer changes what we build.

**The models that speak natively mostly do not speak Hindi.** Kling 3.0 documents English, Chinese,
Japanese, Korean and Spanish. HappyHorse claims seven languages, unnamed. This single observation is
why the voice and lip-sync rows are not a completeness exercise: if one-pass dialogue video cannot
reach our market, **text-to-speech plus lip-sync is not a fallback, it is the route** — and Sarvam
Bulbul v3 is the only candidate documenting Hinglish code-switching, which is how Indian ad copy is
actually written.

One row is worth flagging for architectural reasons: **Reve 2.1** plans an image as addressable
regions and edits one element without re-rolling the frame. It is the closest commercial analogue we
found to this project's own separation of a Creative IR from a Production IR. Testing it produces
evidence about our design, not only about a vendor.

---

## 4. Decisions that are yours, not the Lab's

**4a. The roster is larger than the previously planned rig, and that has to be reconciled.**
`eval/v1/MODEL-WORKFLOW-INVENTORY-2026-08-26.md` reserved **19** endpoint/workflow slots, none
filled. This task, told not to impose a quota, produced **26** Must/Should rows. Both numbers are
honest: one was a capacity plan, the other a measurement plan built from capability evidence.
*Recommendation, not a decision:* the 15 Must models fit inside 19 with room for the four highest-value
Should rows — **Nano Banana Pro, Ideogram V3, Gemini Omni Flash, Marey Realism V1.5** — and the rest
wait for a second wave.

**4b. Recraft V3's slot is a scope question.** It is the only row emitting **native vector output**,
which would let us take type out of the raster generator entirely for design elements — a logo or a
price flash in vector cannot misspell Hindi. But it is only valuable if the product takes on design
deliverables. That is a product-direction call.

**4c. Your AWS credits will not buy this programme — check the split before budgeting.**
Bedrock carries **none** of the roster. Its media catalogue is Stability and Luma Ray v2, and
Amazon's own models are being retired rather than expanded: **Nova Canvas is Legacy with an
end-of-life of 30 September 2026**, Nova Reel is Legacy across all regions. So the value of your
Frontier Clouds credits to this work depends heavily on **how they are split across the three
clouds** — GCP is worth the most by a wide margin, Azure is genuinely useful, AWS is close to
zero here. Worth establishing before a budget is set, not after.

There is a second, larger unknown behind it: **credit grants frequently cover language-model
inference and exclude image and video generation**, which is where essentially all of this
programme's cost sits. If media is excluded on a given cloud, that cloud's contribution drops to
nothing regardless of catalogue.

**4d. Whether we ever answer the open-weight economics question.** Four rows carry it, and answering
it needs our own GPU, which is a different kind of account with a different cost shape. Deferring is
reasonable. Reporting a hosted number as if it were an open-economics number would not be.

---

## 5. What is genuinely weak here, stated plainly

**We could not read almost any provider's own website.** Forty-three domains were probed across
the task; **one answered** (`cloud.google.com`). OpenAI, fal, Black Forest Labs, Runway, ElevenLabs,
BytePlus, MiniMax, Kling, Ideogram, Sarvam, Hugging Face and Artificial Analysis were all blocked by
the session's network policy with a `403`. **AWS and Azure were re-probed after the Frontier Clouds
identity was resolved and are also blocked** — `aws.amazon.com`, `docs.aws.amazon.com`,
`azure.microsoft.com`, `learn.microsoft.com` and `ai.azure.com` all answered `403`. This is the same
blocker that stopped the earlier E2 pricing task, and it is unchanged.

**So the Frontier Clouds pass is uneven by construction:** the four Google rows are verified, and
the three Azure rows and the AWS finding are T2/T3 and need confirming in a console you can open and
this session cannot.

**So most of this rests on a web-search tool reading pages on our behalf.** That is real, current,
retrieved information — it repeatedly returned models released after this assistant's May 2026
training cutoff, which memory could not have produced — but it is **not documentation**, and every
claim in the artifacts carries an explicit evidence tier saying which it is.

**Here is the concrete demonstration of why that distinction matters.** Third-party pages told us
Veo 3.1 costs "$0.03/sec" in one article and "$0.40/sec" in another. Google's own page, read
directly today, prices **Veo 3.1 video-with-audio at $0.40 per generated video, billed per count,
not per second.** Two sources, two numbers, both wrong in unit and in magnitude. **Do not budget from
any price in these artifacts except the Google ones.**

**Version identity is genuinely ambiguous in public sources** for FLUX.2 [klein] (4B or 9B), LTX-2
(2.0 / 2.3 / 2.5), Wan (2.6 or 2.7), Seedream (4.5 or 5.0), and MiniMax H3 (open-weights or closed).
I judged this **not** severe enough to trigger the task's stop condition, because families are
cleanly distinguishable and the ambiguity is confined to version numbers — but **every row must be
version-pinned from the provider's own catalogue before it is measured**, or the Registry row will
not mean anything.

**And the standing dependency is unchanged: no checker has ever been qualified in this project.**
Choosing what to measure does not create the ability to measure it.

---

## 6. Stop conditions — considered, and what I did

The task lists five conditions where I should stop and report rather than decide.

| Condition | Triggered? | What I did |
|---|---|---|
| Model universe too ambiguous to distinguish versions | **Partly** | Families are clearly distinguishable; version numbers are not, for five models. Continued, recorded each ambiguity explicitly, and made version-pinning a precondition of measurement rather than stopping. |
| An important model has no legitimate version-identifiable route | **Yes, once — since resolved** | **MAI-Image-2.5-Pro** had no evidenced route in the first pass. I kept the row, flagged it, and recommended establishing the route before any account. Resolving Frontier Clouds to the hyperscalers then found it on Microsoft Foundry. **The first pass was confidently wrong here**; holding the row rather than dropping it is what let the correction land. |
| Provider access requires terms/payment/verification merely to inspect | **No** | No signup or terms page was reached. The blocker was network policy, not a gate. |
| Evidence materially contradicts the product architecture | **No** | If anything the opposite — Reve 2.1's structured-region editing is convergent with our IR separation. |
| Completing research requires paid API calls | **No** | Zero calls made; none were needed for selection or availability research. |

**One note on delivery, for the record.** The work was first committed on a session-designated
branch (`claude/eval-008-cloud-model-access-i3fl86`) while the task file's branch name was
confirmed. It was then delivered on **`work/eval-008-model-access`**, the branch this task file
specifies, carrying the same commits. No artifact content changed in the move — only the branch
name recorded in these headers. The three-commit ordering that proves the anti-bias check
(§2a) is preserved intact on this branch.

---

## 7. What happens next — and what nothing here authorises

**The single highest-value thing you can do is not more research.** Tell us what **Frontier Clouds**
is. That one answer could move a large number of rows onto credits you have already paid for, and it
is a lookup of well under an hour against a checklist that is already written.

**Second most valuable:** run the fal verification from a machine that can reach `fal.ai` — the exact
endpoint id and version for around twenty rows. fal reportedly exposes a model-search API, which could
make that one scripted call instead of twenty page visits. That converts the largest block of this
work from "probably fine" to "confirmed".

**This task authorises nothing.** No model is qualified, ranked, admitted or entered in any Registry.
No budget is approved, no account created, no terms accepted, ₹0 spent, no merge requested. The
project's audit freeze is untouched: this was research inside an assigned task, and the next step in
every direction is a Controller decision.
