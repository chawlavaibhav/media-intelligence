# E8-G — What the user actually needs to do

**Task:** EVAL-008 · **Date:** 26 Aug 2026
**Written after all sourcing passes, as required.**
**Nothing here has been done. No account created, no terms accepted, no payment made, ₹0 spent.**

---

## The short version

**You need to do one thing before anything else, and it is not creating an account.**

Tell us what **Frontier Clouds** actually is — the URL you sign in at, or a screenshot of its
model list. Three searches could not identify any public service by that name, and until we
know what it is, we cannot tell you which of the 26 models you are already paying for. That
one answer could remove most of the rest of this page.

Everything below assumes Frontier Clouds stays unknown. If it turns out to carry a lot of the
roster, several of these actions disappear.

**Nothing on this page needs money today.** Every account named can be created, or at least
inspected, without a payment commitment, and no paid run is authorised by this task anyway.
Prepaid credits are deliberately not recommended — that decision belongs after a budget is
approved, not before.

---

## Bucket 1 — No action, covered by your existing Frontier Clouds credits

**Currently: cannot be filled. 0 of 26 rows.**

This is not "none of your credits are useful". It is "we do not know what your credits buy",
which is a different and much more fixable problem. `FRONTIER-CLOUDS-VERIFY.md` holds the exact
26-row checklist to run against that catalogue once you tell us where it is; it is a lookup of
well under an hour, not a research task.

Two questions worth answering at the same time, because both are cheap now and expensive later:

- **Do the credits cover image and video generation, or only text models?** Many credit grants
  quietly exclude media generation, which is where essentially all our cost sits.
- **Is it a first-party host or a reseller?** If it resells someone else's endpoints, its version
  pinning and controls are inherited, and a Capability Registry row has to name whatever actually
  ran the generation.

---

## Bucket 2 — Covered by your existing fal access, no new account

**Currently: up to 20 of 26 rows, at varying confidence. No new signup needed for any of them.**

Your existing fal access appears to be the single most valuable thing you already have for this
work: one key, one bill, and most of the roster behind it.

**High confidence — fal's own model pages describe these (13 rows):**

> GPT Image 2 · Reve 2.1 · Seedance 2.0 Pro · HappyHorse 1.1 · Veo 3.1 · Kling 3.0 ·
> MiniMax H3 · ElevenLabs v3 · Sync-3 · Ideogram V3 · Gemini Omni Flash ·
> Marey Realism V1.5 · OmniHuman v1.5

**Present but the version needs pinning before use (7 rows):**

> Nano Banana 2 · Nano Banana Pro · Seedream 5.0 Pro · FLUX.2 [pro] · Seedance 2.0 Fast ·
> Wan 2.7 (2.6 also appears) · LTX-2 (fal's page says 2.3)

**The one action here is not a signup — it is a look.** From any machine that can reach
`fal.ai`, open each model page and write down the **exact endpoint id and version**. That
converts this whole bucket from "probably fine" to "confirmed", and it is the difference between
a Registry row that means something and one that does not. fal reportedly also offers a model
search API, which would make this a single scripted call rather than 20 page visits.

**Why this matters more than it sounds.** We could not open a single fal page from this session
— the network policy blocked it. Everything above comes from a search tool reading fal's pages
on our behalf. It is good enough to plan with. It is not good enough to spend with.

---

## Bucket 3 — New access genuinely required

**Three rows. One is a Must, and it is the difficult one.**

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

### 3c. Microsoft / Azure — for MAI-Image-2.5-Pro · *do not act yet*

**What to do: nothing, until the route exists.** We found this model only through leaderboard
reporting — currently first on blind-preference image *editing* — and **no documented API route
at all**. Azure AI Foundry is the plausible home, but that is an inference, not a finding.

**Recommendation: leave it.** It is a Should row, not a Must, and two other editing models on the
roster (Reve 2.1 and FLUX.2) cover the same hypothesis. Establish the route first; create an
account only if the row survives that check.

---

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
| **First** | Tell us what Frontier Clouds is — URL or model-list screenshot | Minutes | ₹0 |
| **Second** | From a machine that can reach `fal.ai`, capture exact endpoint ids and versions for the ~20 rows in Bucket 2 | Under an hour, or one API call | ₹0 |
| **Third** | Check whether Runway's API is still open to standard signups | Minutes | ₹0 |
| **Fourth** | Create a Sarvam AI account and read its current pricing and terms | Minutes | ₹0 |
| **Fifth** | Confirm the exact version of every row from the provider's own catalogue | A few hours | ₹0 |
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
