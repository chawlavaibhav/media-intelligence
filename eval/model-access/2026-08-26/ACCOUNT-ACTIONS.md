# E8-G — What the user actually needs to do

**Task:** EVAL-008 · **Date:** 26 Aug 2026
**Written after all sourcing passes, as required.**
**Nothing here has been done. No account created, no terms accepted, no payment made, ₹0 spent.**

---

## The short version

**Frontier Clouds is resolved: it means GCP, AWS and Azure.** That answer alone moved seven
roster rows onto credits you already hold, and removed one model from the "new account" list.

Where that leaves you:

- **7 of 26 rows — no action.** Already on your Google Cloud and Azure credits.
- **~15 rows — no new account.** Covered by your existing fal access, pending a version check.
- **2 rows — new access needed.** Sarvam AI, and Runway subject to one check.
- **AWS contributes nothing** to this roster, and that is worth knowing before a budget.

**Nothing on this page needs money today.** Every account named can be created, or inspected,
without a payment commitment, and no paid run is authorised by this task anyway. Prepaid
credits are deliberately not recommended — that decision belongs after a budget is approved.

## Bucket 1 — No action, covered by your existing Frontier Clouds credits

**7 of 26 rows.** Full detail in `FRONTIER-CLOUDS-AVAILABILITY.md`.

**Google Cloud — Vertex AI (4 rows, prices verified from Google's own pages):**

> **Nano Banana 2** · **Veo 3.1** (plus its Fast and Lite tiers) · **Nano Banana Pro** ·
> **Gemini Omni Flash**

These are the only rows in the whole task with exact identities, GA dates and printed prices we
read ourselves. Veo's three tiers also give us the cost-ladder experiment — **$0.05 to $0.40 per
generation, an 8× spread inside one family** — priced by the vendor.

**Microsoft Azure — Microsoft Foundry (3 rows, needs console confirmation):**

> **GPT Image 2** (`gpt-image-2`) · **FLUX.2 [pro]** (FLUX 2 Pro) · **MAI-Image-2.5-Pro**

**MAI-Image-2.5-Pro is a correction to our first pass.** We previously recorded it as having no
evidenced route at all and recommended taking no action. That was wrong. It is a Microsoft model,
so it lives on Microsoft's cloud: released on Foundry 23 July 2026, deployable from the portal or
Azure CLI at model version 2026-06-02 or later, with **South India** among its regions. It needs
no new vendor account.

**AWS — Bedrock: 0 rows, and a warning.**

Bedrock carries none of this roster. Its media catalogue is Stability AI and Luma Ray v2, and
Amazon's own models are being retired rather than expanded — **Nova Canvas is Legacy with an
end-of-life of 30 September 2026**, Nova Reel is Legacy across all regions. None of those earned a
roster slot, and a Registry entry against a model with a published end-of-life would expire almost
immediately.

**Practical consequence: if a large share of your credits sits on AWS, they will not buy this
programme.** Worth checking the split before a budget is set.

**Two things to confirm in your own console** — this session could not reach AWS or Azure pages:

1. **The three Azure rows**, recording the exact deployed version string for each.
2. **Whether your credits actually cover media generation.** Credit grants frequently cover
   language models and exclude image and video, which is where all of this programme's cost sits.
   This is the largest remaining unknown in the task.

## Bucket 2 — Covered by your existing fal access, no new account

**14 of the 19 rows your cloud credits do not cover, at varying confidence. No new signup needed.**

fal appears to carry more of this roster than all three hyperscalers combined — one key, one bill,
and the entire video and voice middle of the list. Six rows that fal also carries (GPT Image 2,
Nano Banana 2 and Pro, FLUX.2 [pro], Veo 3.1, Gemini Omni Flash) are routed to your cloud credits
instead, per your stated preference; fal remains their fallback.

Three further rows — **Qwen-Image, Recraft V3, FLUX.2 [klein]** — we could not confirm either way,
and two (**Runway Aleph 2.0, Sarvam Bulbul v3**) appear genuinely absent.

**High confidence — fal's own model pages describe these (10 rows):**

> Reve 2.1 · Seedance 2.0 Pro · HappyHorse 1.1 · Kling 3.0 · MiniMax H3 · ElevenLabs v3 ·
> Sync-3 · Ideogram V3 · Marey Realism V1.5 · OmniHuman v1.5

**Present but the version needs pinning before use (4 rows):**

> Seedream 5.0 Pro · Seedance 2.0 Fast · Wan 2.7 (2.6 also appears) · LTX-2 (fal's page says 2.3)

**The one action here is not a signup — it is a look.** From any machine that can reach
`fal.ai`, open each model page and write down the **exact endpoint id and version**. That
converts this whole bucket from "probably fine" to "confirmed", and it is the difference between
a Registry row that means something and one that does not. fal reportedly also offers a model
search API, which would make this a single scripted call rather than a page-by-page trawl.

**Why this matters more than it sounds.** We could not open a single fal page from this session
— the network policy blocked it. Everything above comes from a search tool reading fal's pages
on our behalf. It is good enough to plan with. It is not good enough to spend with.

---

## Bucket 3 — New access genuinely required

**Two rows, down from three.** MAI-Image-2.5-Pro left this bucket when Frontier Clouds resolved
to the hyperscalers — it is on Azure, on credits you already have.

### 3a. Sarvam AI — for Bulbul v3 · *recommended, low friction*

**What to create:** a Sarvam AI developer account at `sarvam.ai`.

**Why this model is worth its own account.** Your first product is Indian-market commercial
media in English, Hindi and Hinglish. The single most consequential thing this research found is
that **the video models which generate speech natively document five or seven languages, and
Hindi is generally not among them.** Kling 3.0's documented audio languages are English, Chinese,
Japanese, Korean and Spanish. So the "one model does everything" route probably does not reach
your market, and a separate Indian-language voice step is likely mandatory rather than optional.

Bulbul v3 is the only candidate that documents **Hinglish code-switching** — mixing Hindi and
English mid-sentence, which is how Indian advertising copy is actually written. It also bills in
rupees at a reported **₹30 per 10,000 characters**, so there is no foreign-exchange friction, and
data stays in India.

**Can payment wait?** Yes. Create the account and read the current pricing and any beta-access
terms. Do not buy anything until a benchmark budget is approved.

### 3b. Runway — for Aleph 2.0 · *needed, but check the gate first*

**What to check before creating anything:** whether Runway's API is still open to ordinary
signups. One third-party source states **API access moved to Enterprise-only in January 2026**.
We could not reach Runway's site to confirm it, and it changes the action completely — a signup
is minutes, an enterprise conversation is weeks.

**Why this model is worth the trouble.** It is the only thing on the roster that **edits footage
you already have** — relight it, change the camera angle, swap an object, across up to ten cuts,
while preserving the original motion. Everything else generates from nothing. For a client who
has already shot something, that is a different business, not a better model, and it is very
plausibly the cheapest route to an accepted outcome we have.

**If the API really is enterprise-gated,** there are three honest options and you should pick one
deliberately: pursue enterprise access; use Adobe Firefly's Runway integration and **record it as
a different route**, because a human-operated creative surface is not comparable to an API and
cannot be automated; or mark the row unmeasurable for now and say so. What we should not do is
quietly swap in the product and call it the same measurement.

**Can payment wait?** Yes for a standard signup. If it is enterprise-only, cost is unknown and
that is itself the finding.

### 3c. Microsoft / Azure — *no longer needed*

**Previously in this bucket; now resolved.** MAI-Image-2.5-Pro was recorded as having no evidenced
route, with a recommendation to take no action. Resolving Frontier Clouds to the three hyperscalers
fixed it: it is a Microsoft model on Microsoft Foundry, released 23 July 2026, available in a South
India region, on your existing Azure access. It has moved to Bucket 1.

**Worth stating plainly, because it cuts both ways.** This is the clearest case in the task of an
answer improving once the route question was settled — and also a reminder that our first pass was
confidently wrong about it. Confirm it in your own catalogue before relying on it.

## A fourth kind of account, which is not an API signup

**GPU capacity — only if you want the open-weight economics answer.**

Four roster rows (Qwen-Image, FLUX.2 [klein], Wan 2.7, LTX-2) carry the question *"what would it
cost us to own this step ourselves?"* Running them **on fal does not answer that question** — it
measures fal's convenience economics, same as every other fal row.

Answering it properly needs our own GPU time, which is a different kind of account with a
different cost shape, and it is worth being explicit rather than discovering it mid-run.

**Recommendation: defer.** Run those four on fal for **capability** now, and only stand up a
self-hosting study once capability justifies the question. If we do report an economics number
from a hosted route, we must label it as hosted economics — not as open economics.

---

## The order to do things in

| When | Action | Effort | Cost |
|---|---|---|---|
| **First** | Check whether your GCP/AWS/Azure credits cover **media generation**, not just language models — and how the credit is split across the three | Minutes | ₹0 |
| **Second** | Confirm the three Azure rows in Microsoft Foundry (`gpt-image-2`, FLUX 2 Pro, MAI-Image-2.5-Pro at version 2026-06-02+), recording exact version strings | Minutes | ₹0 |
| **Third** | From a machine that can reach `fal.ai`, capture exact endpoint ids and versions for the ~15 rows in Bucket 2 | Under an hour, or one API call | ₹0 |
| **Fourth** | Check whether Runway's API is still open to standard signups | Minutes | ₹0 |
| **Fifth** | Create a Sarvam AI account and read its current pricing and terms | Minutes | ₹0 |
| **Sixth** | Version-pin every remaining row from the provider's own catalogue | A few hours | ₹0 |
| **Later, and only with Controller approval** | Reconcile 26 roster rows against the previously planned 19-slot capacity, approve a budget, then run | — | Not authorised by this task |

---

## Three honest cautions

**We could not read almost any provider's own website.** Thirty-seven domains were probed; one
answered. Only Google's pages were read directly. Everything else here came through a search tool
reading pages on our behalf — real current information, but not documentation.

**Do not budget from any price on these pages except the Google ones.** Third-party sources gave
us Veo 3.1 at "$0.03/sec" and "$0.40/sec"; Google's own page prices it at **$0.40 per generated
video**, billed per count, not per second. Two sources, two numbers, both wrong in unit and
magnitude.

**Choosing what to measure is not the ability to measure it.** No checker has ever been qualified
in this project, so we still have no trusted way to judge a generated image or video at scale.
This roster tells you what to point the instrument at. It does not build the instrument.
