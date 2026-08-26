# E2 — Current workflow / API / access / pricing inventory

**Task:** E2 · **Date:** 26 Aug 2026 · **Branch:** `work/eval-v1-overnight`
**Status: PARTIALLY BLOCKED** · **0 endpoints admitted · 0 API calls · ₹0 spent**

Machine-readable record: [`model-workflow-inventory-2026-08-26.yaml`](model-workflow-inventory-2026-08-26.yaml)

---

## Read this first

E2 was to produce a roster of up to 19 current model endpoints with their exact
identities, availability and **official** prices, so the Controller could
approve a budget for the first paid wave.

**The roster architecture is finished. The prices are not, and could not be.**
This session's network policy blocks essentially every official provider
documentation site, and E2's own rule says official documentation is the only
acceptable evidence for identity, availability and price.

So this document delivers: the complete lane architecture, the admission
criteria, the per-endpoint record schema, the access-visibility record, the
exact forward call counts — and a precisely evidenced account of what is
missing and how cheaply it can be finished.

**No endpoint is admitted. Nothing here authorises spend.**

---

## Correction E-C2 — re-tested, and the route that half-worked is now closed

The environment was **re-probed on 26 August** after GitHub access was restored.

| Check | Result |
|---|---|
| Official provider domains probed | **22** |
| Reachable from this session | **1** (`cloud.google.com`, HTTP 200) |
| Of those, yielding an extractable pricing table | **0** |
| Model/pricing docs on the reachable domain | **301 → `docs.cloud.google.com`, which is also blocked** |
| Web search available | Yes |
| Web search results usable as price evidence | **No** — reseller blogs and cost calculators |

The one partial route that existed before has closed: Google's model and pricing
documentation now redirects to a host this session cannot reach. Neither a price
**nor an exact model identity** could be obtained by any available means.

## The roster — all 19 slots, each explicitly unresolved

E-C2 requires each row to be officially evidenced **or explicitly unresolved**,
row by row. None could be evidenced, so all 19 are enumerated as unresolved
slots in the YAML rather than summarised as a single blocker.

| Lane | Slots | Resolved |
|---|---:|---:|
| Image | 4 | 0 |
| General video | 5 | 0 |
| Native audio-video | 4 | 0 |
| Lip-sync | 3 | 0 |
| TTS | 3 | 0 |
| **Total** | **19** | **0** |

A slot is a **reserved position, not a candidate**. It names no model, because
naming one from memory is exactly the invented certainty E-C2 forbids.

**A partially filled roster remains the intended outcome** — it simply could not
be reached, because zero slots could be evidenced rather than some. If a later
session reaches even one official pricing page, that slot fills and the other
eighteen stay as they are. This does not have to be completed in one pass.

Blocked domains included every one that matters for this roster: the Gemini
developer site, OpenAI, ElevenLabs, fal, Replicate, Runway, Black Forest Labs,
Sarvam, HeyGen, Sync, Luma, Kling, MiniMax, Stability, Ideogram, Azure and AWS.
The single reachable domain returns pricing through JavaScript, and two fetch
attempts — the Vertex AI generative-AI pricing page and the Cloud
Text-to-Speech pricing page — both came back with no pricing table.

This is the runbook's stop condition *"official model version/access/pricing
cannot be pinned"*. Per the overnight rules I documented it and continued with
the independent work rather than waking you.

### Why I did not just write the prices from memory

This is worth stating plainly because it is the difference between a useful
document and a dangerous one.

I could have produced a confident-looking table of model ids and prices from
training data. I did not, and the reason is demonstrable rather than principled:
a search lead indicated that legacy `veo-3.0-generate-001` endpoints reached
their **shutdown date on 30 June 2026** — *after* my May 2026 training cutoff.
Model identities, tiers and prices in this market move faster than the gap
between that cutoff and today.

A remembered price in a document that gates a real budget decision is invented
evidence, no matter how plausible it reads. The project has a rule for this and
it applies exactly here: **never invent costs or model capabilities.**

### What this blocks — and what it does not

**Blocked:** admitting any endpoint; producing any cost figure; confirming what
is currently generally available or region-restricted.

**Not blocked, and complete:** the five-lane architecture and caps; the
admission criteria and per-endpoint schema; the access-visibility record; the
forward call counts; the entire cost-forecast machinery.

---

## Execution access — what this session can actually see

**No secret value was read, printed or committed.** Only the presence or absence
of environment-variable *names* was checked, in this container only.

| Field | Value |
|---|---|
| `user_laptop_credentials` | **`not_visible_to_cloud_session`** |
| `cloud_session_configured_access` | **`no_or_unknown`** |
| Media-provider credentials present | **None** |

Fifteen provider credential names were checked and all were absent. Two
credential sets *are* present and were deliberately **not used**: AWS keys
(session harness infrastructure, not an approved project media account — using
them to reach a model API would be spending on an unapproved account) and
GitHub/Cloud SDK tokens (repository and harness infrastructure).

**Consequence:** even if the roster were approved tonight, this session could
not execute a paid run. That matches the overnight prohibition, and it is
recorded so no later session assumes access exists.

---

## The five lanes — complete, and this part is Eval's real design work

Maximum **19** endpoint/workflow combinations. **0 admitted.**

| Lane | Cap | Why it exists |
|---|---:|---|
| **Image** generation/editing | 4 | Static creatives, packshots, reference edits — the largest share of the first product and the cheapest per trial, so screen it widest |
| **General video** (text/image→video) | 5 | 6–20 second product and brand video without visible speech. Widest cap: most credible competing providers, largest quality spread |
| **Native audio-video** | 4 | Audio and picture from **one** model, so sync and speech correctness are properties of the *same trial* rather than of a compositing step |
| **Lip-sync / digital human** | 3 | A **transformation** lane — consumes our video plus our audio. Outputs counted separately from generations, and some checks become deterministic because the input is ours |
| **TTS / external VO** | 3 | Cheapest per trial, and the lane where Hindi, Hinglish and Indian-English pronunciation matter most |

**One model may occupy two lanes only** where the workflow conditions genuinely
differ, recorded as separate rows. A model used text-to-video and again as
native-AV is two rows, never one — carrying forward the V0 Registry rule that
one entry is one vendor + model + version + workflow.

### Two selection criteria Eval owns, which stand independently of the blocker

**Indic-specialist TTS deserves a slot on merit.** The first product is
Indian-market commercial media in English, Hindi and Hinglish. A globally strong
voice model that mispronounces Hindi brand names is not usable for this product.
That is a measurement-design judgement, not a pricing question.

**Direct access and aggregator access are different endpoints.** Different
prices, different version pinning, different reliability. They must never share
a Registry row. Where both exist, prefer whichever can be **version-pinned** —
an endpoint that cannot be pinned makes every measurement against it
provisional, because the model can change underneath a Registry row with no
signal to us.

---

## Candidate leads — explicitly not evidence

The YAML records candidate vendor/product **families** per lane, marked
`UNVERIFIED_LEADS_ONLY` with `evidential_weight: none`.

They are recorded as *families*, not exact model ids, on purpose: an exact id
written from memory would look like verified identity, which is the very thing
the blocker forbids. A family name is a starting point for deciding which
official pricing page to open first — nothing more.

---

## Forward call counts — complete and self-checked

| Wave | Outputs | Verified against runbook max |
|---|---:|---|
| E7 admission screen | **204** | ✅ matches |
| E8 deep qualification | **520** | ✅ matches |

Full per-lane breakdown and the ~8,000 implied evaluator calls are in
[`COST-FORECAST-PRE-RUN.md`](COST-FORECAST-PRE-RUN.md). Retries are excluded and
must be predeclared separately.

---

## What the morning needs to do

1. Open `eval/v1/prices-TEMPLATE.yaml`.
2. Fill each cell from official pricing pages, recording `source_url`,
   `read_date`, `model_api_id`, `billing_unit`.
3. Run `python3 eval/v1/cost_forecast.py --prices <file>`.

The totals appear immediately. **This is a lookup task, not a design task** —
all the design around it is finished and tested.
