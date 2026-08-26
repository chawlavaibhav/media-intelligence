# E10-H — Account and access checklist

**Task:** EVAL-010 · **Date:** 26 Aug 2026
**Nothing here has been done.** No account created, no terms accepted, no payment, ₹0 spent.
This is a list of what *would* be needed, not an instruction to act.

---

## The one thing that changes everything else

**Tell us what Frontier Clouds is** — a URL, a catalogue page, or a screenshot of its model list.

Until then we cannot say which candidates your existing credits cover, and we cannot convert any
verified price into actual cash outlay. `FRONTIER-CLOUDS-CHECKLIST.md` holds a 26-row list ready
to run against that catalogue.

While answering, also settle two things that can quietly void the whole benefit:

- **Do the credits cover image and video generation, or only language models?** Media generation
  is frequently excluded, and it is where essentially all of this programme's cost sits.
- **Is it a first-party host or a reseller?** A reseller inherits version pinning rather than
  choosing it, which affects whether a Registry row can name what actually ran.

---

## What is already verified enough to act on, when the time comes

**Google — no new account needed if you already have Google Cloud.**
Two rows are execution-ready: **Nano Banana 2** (`gemini-3.1-flash-image`, $0.067 per 1K image)
and **Veo 3.1 Lite** (`veo-3.1-lite-generate-001`, $0.05 per 720p video with audio). Prices read
from Google's own page today. Two surfaces exist — Vertex AI carries an enterprise SLA, the Gemini
API does not — and **you should pick one and stay on it**, because mixing them inside one Registry
row would make the row mean two things.

## Access still to be established — in the order that unblocks the most

| Priority | Provider | What is needed | Why it matters | Cost to ask |
|---|---|---|---|---|
| 1 | **Frontier Clouds** | identity | unblocks the entire preferred route and all cash-outlay figures | ₹0 |
| 2 | **fal** | reach `fal.ai` to read **prices** | fal verifiably carries 12 candidate rows at the exact selected version, and we cannot cost a single one | ₹0 |
| 3 | **OpenAI** | reach pricing for `gpt-image-2` | carries the roster's most product-relevant image hypothesis | ₹0 |
| 4 | **Sarvam AI** | reach pricing for `bulbul:v3` | the only verified Indic voice route; 11 languages confirmed from Sarvam's own API | ₹0 |
| 5 | **ElevenLabs** | reach pricing for `eleven_v3` | the control arm for the Indic voice comparison | ₹0 |
| 6 | **Runway** | the **credit-to-currency rate** | Runway bills in credits; without the rate, Aleph 2.0 and its aggregated Veo/Hailuo routes cannot be costed at all | ₹0 |

**None of these requires creating an account.** Every one is a public pricing page that this
session's network policy blocked. A machine that can reach them turns most of
`PRICE-VERIFICATION.yaml` from null into verified in an afternoon.

## One EVAL-008 action item that should be withdrawn

EVAL-008's account checklist flagged **Runway** as possibly requiring an enterprise sales
conversation, on the strength of a third-party report that API access moved to Enterprise-only in
January 2026.

**Runway's own published Python SDK exposes the full public API surface**, including `aleph2`
video-to-video with keyframes. The enterprise-gating claim is not supported by any
provider-authorised evidence we could reach. Whether *your* account is entitled to a given model
is a separate question that this task must not test — but the premise that the API is closed to
ordinary developers should not be carried forward as fact.

## Two candidates that cannot be actioned at all yet

- **Reve 2.1** — no provider-authorised route found anywhere. Not on fal, no reachable vendor
  host, and the PyPI package of that name has no verifiable publisher. `route_unresolved`.
- **MAI-Image-2.5-Pro** — every Microsoft host was blocked, no vendor SDK enumerates it, and it is
  absent from fal. EVAL-008's second pass reported a Foundry release date, model version, regions
  and prices; all of that is lead-only here. Neither confirmed nor refuted. `route_unresolved`.

**Do not create a Microsoft or Reve account on the strength of the EVAL-008 write-up.** Establish
the route first.

## What must not happen next

- No account creation, no terms acceptance, no payment, no prepaid credits.
- No API or model calls, including "just one test call" to check whether an endpoint exists.
- No Registry rows.
- No treating this table as a purchase plan. It is an access-gap list.

Paid work remains blocked until the four freeze programs return, the Controller freezes the
executable package, one bounded Governor review passes, and the Controller explicitly approves a
budget.
