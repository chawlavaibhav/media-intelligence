# E10-C — Frontier Clouds: unresolved, with a ready-to-run checklist

**Task:** EVAL-010 · **Date:** 26 Aug 2026 · **Branch:** `work/eval-010-route-verification`
**Status: `unresolved_service_identity`.**
**No API calls · ₹0 spent · no account created · no terms accepted.**

---

## The finding

**We could not establish what "Frontier Clouds" is, and we did not guess.**

Every Frontier cell in every EVAL-010 artifact therefore reads `unresolved_service_identity`,
and verification continued down the ladder to fal and direct routes, exactly as the task directs.

## Why the EVAL-008 claim was not adopted

The EVAL-008 branch carries a worker-side claim that Frontier Clouds means **GCP + AWS + Azure**,
and its second pass built a whole availability table on that basis.

**That claim is not adopted here, for three independent reasons.**

1. **The Controller has ruled on it.** `coordination/CONTROL-STATE.md` states that this is
   "**not a Controller decision on record**" and "must be reverified/confirmed rather than
   assumed". `coordination/decisions/CONTROLLER-FINAL-PRE-EXECUTION-FREEZE-2026-08-26.md` puts
   non-primary provider availability among the things that are not execution-grade without
   re-verification. That settles it regardless of what the claim's origin was.

2. **The underlying statement did not say what EVAL-008 used it for.** The claim traces to a
   remark that frontier clouds are *usually* GCP, AWS and Azure. That is a general observation
   about what the phrase tends to mean. It is not a statement that **this user's credits sit on
   those three**, which is the thing EVAL-008 needed and treated as established. A hedged general
   remark was promoted into a specific factual premise.

3. **It cannot be verified from here anyway.** `aws.amazon.com`, `docs.aws.amazon.com`,
   `azure.microsoft.com`, `learn.microsoft.com` and `ai.azure.com` were all re-probed in this
   session and all returned `403` from the egress proxy. So even under the assumed reading, no
   AWS or Azure catalogue could be checked.

**Nothing found here refutes the claim either.** It is unevidenced, not disproven.

## What public search returned

One targeted search for the exact phrase returned no dedicated cloud platform of that name. It
surfaced unrelated companies that share the word "Frontier" — a US telecom's enterprise cloud
connect product, an Indian IT infrastructure provider, and a data-platform consultancy. **None of
these was treated as a candidate identification and none should be.** They are recorded only so
the next session does not repeat the search.

## What we need from the Controller

Any **one** of these unblocks the whole pass:

1. the **URL** the user signs in at;
2. the **catalogue or model-list page**;
3. a **screenshot** of the model list — sufficient for a first cut;
4. the **invoice or console header**, which usually carries the registered name even when the
   informal name differs.

Credentials are not required and must not be supplied. Availability is a catalogue question.

---

## Ready-to-run checklist — 26 candidate rows

Run this against the catalogue once identified. For each row, in this order:

- **A. Present at all?**
- **B. Is it the *exact* version below?** A family match is not a match.
- **C. Which workflows and controls?** A route that only does text-to-image cannot serve an
  editing hypothesis.
- **D. Can the version be pinned**, or does the identifier float?
- **E. Billing unit and current price.**

| # | Candidate | Exact version to look for | Verified elsewhere? |
|---:|---|---|---|
| 1 | GPT Image 2 | `gpt-image-2-2026-04-21` (pinned) | ✅ OpenAI SDK |
| 2 | Nano Banana 2 | `gemini-3.1-flash-image` | ✅ Google, priced |
| 3 | Seedream 5.0 Pro | v5 **Pro** specifically | ❌ unresolved |
| 4 | Reve 2.1 | Reve 2.1 | ❌ no route found |
| 5 | FLUX.2 [pro] | `[pro]` variant | ✅ fal `flux-2-pro` |
| 6 | Qwen-Image | `qwen-image-2.0-pro` | ✅ Alibaba SDK |
| 7 | Seedance 2.0 Pro | v2.0 **Pro** | ❌ unresolved |
| 8 | Seedance 2.0 Fast | v2.0 **Fast** | ❌ unresolved |
| 9 | HappyHorse 1.1 | 1.1 (only 1.0 found) | ⚠️ 1.0 on Alibaba |
| 10 | Veo 3.1 (+Fast, +Lite) | stable GA id, not `-preview` | ✅ Google, priced |
| 11 | Kling 3.0 | v3 Pro | ✅ fal |
| 12 | MiniMax H3 | `hailuo3` | ✅ Runway SDK |
| 13 | Runway Aleph 2.0 | `aleph2` | ✅ Runway SDK |
| 14 | Sarvam Bulbul v3 | `bulbul:v3` | ✅ Sarvam SDK |
| 15 | ElevenLabs v3 | `eleven_v3` | ✅ ElevenLabs SDK |
| 16 | Sync-3 | Sync-3 (only v2/pro found) | ❌ unresolved |
| 17 | Nano Banana Pro | Gemini 3 Pro Image — **get the API id** | ⚠️ priced, id unknown |
| 18 | MAI-Image-2.5-Pro | 2.5 Pro | ❌ no route found |
| 19 | Ideogram V3 | v3 | ✅ fal |
| 20 | Recraft V3 | v3 (v4 also exists) | ✅ fal |
| 21 | FLUX.2 [klein] | 4B **and** 9B both exist | ✅ fal |
| 22 | Gemini Omni Flash | **get the API id** | ⚠️ priced, id unknown |
| 23 | Wan 2.7 | `wan2.7-t2v` / `wan2.7-i2v` | ✅ Alibaba SDK |
| 24 | LTX-2 | `ltx-2-19b` | ✅ fal |
| 25 | Marey Realism V1.5 | V1.5 — endpoint carries no version | ⚠️ version unpinned |
| 26 | OmniHuman v1.5 | v1.5 | ✅ fal |

## Two catalogue-level questions to answer at the same time

**1. Do the credits cover media generation, or only language models?** Credit grants routinely
exclude image and video generation, which is where essentially all of this programme's cost sits.
If media is excluded, the sourcing preference collapses to fal and direct, and
`BUDGET-INPUTS.yaml` shows we cannot cost those today.

**2. First-party host or reseller?** If Frontier Clouds resells another platform's endpoints, its
version pinning and controls are inherited rather than chosen, and a Capability Registry row must
name whatever actually served the generation.

## What this blocker does and does not stop

**Does not stop:** identity verification, control verification, fal route verification, direct
route verification, Google price verification, or the route-equivalence analysis. All were completed.

**Does stop:** any statement about which candidates the user's existing credits cover, and
therefore any conversion of nominal benchmark cost into **actual cash outlay**. That separation is
held explicitly in `BUDGET-INPUTS.yaml`.
