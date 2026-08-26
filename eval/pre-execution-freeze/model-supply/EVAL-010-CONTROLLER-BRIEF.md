# EVAL-010 — Controller Brief

**Task:** EVAL-010 — Model Route / Version / Price Verification
**Date:** 26 Aug 2026 · **Autonomy:** autonomous · **Branch:** `work/eval-010-route-verification`

**Status: COMPLETE as a program. The supply table it produced is PARTIAL, and is labelled partial.**
**0 API/model calls · 0 evaluator calls · ₹0 spent · no accounts · no terms accepted · no Registry rows · no merge.**

> **Communication check:** I will explain technical ideas in plain English, including what they
> mean, why they matter, and their practical consequence; use minimum sufficient wording without
> sacrificing understandability; separate evidence from inference; and never invent facts.
> I have read `shared/COMMUNICATION-STANDARD.md`.

---

## 1. The result in one paragraph

We can now name, version-pin and describe the controls of most of the EVAL-008 candidates from the
providers' own published material. **We cannot pay for almost any of them.** Only
`cloud.google.com` was reachable; 33 of 34 provider hosts returned `403`. Package registries were
open, so vendor-published SDKs supplied genuine primary evidence for identity and controls — but
SDKs never carry prices. The result is **2 execution-ready routes out of 26 candidate rows**, both
Google, and **8 EVAL-008 claims that did not survive contact with the providers' own material.**

## 2. Direct answers

**Execution-ready verified routes: 2.**
- **Nano Banana 2** — `gemini-3.1-flash-image`, GA 28 May 2026, $0.067 per 1K image (vendor-published).
- **Veo 3.1 Lite** — `veo-3.1-lite-generate-001`, $0.05 per 720p video with audio.

Both are Google. "Execution-ready" here means identity, route, billing unit **and** current price
are all verified from provider-authorised evidence. Nineteen further rows are
`verified_fallback_only` — we know exactly what and where they are, we just cannot cost them.

**Frontier Clouds: `unresolved_service_identity`.** Not identified, and not guessed. Details in §4.

**fal coverage: 12 of 26 candidate rows carry the exact selected version**, verified from fal's own
published client. Five more have the family but **not** the selected version, and were not
substituted. **No fal price could be verified**, so no fal route is execution-ready.

**Unresolved identities: 7.** Five where the exact version could not be confirmed — Seedream 5.0
Pro, Seedance 2.0 Pro, Seedance 2.0 Fast, HappyHorse 1.1, Sync-3 — and two with no
provider-authorised route at all: Reve 2.1 and MAI-Image-2.5-Pro.

**Required new accounts: none established as necessary.** Six providers need a *pricing page read*,
not a signup. One EVAL-008 account action should be withdrawn (§5).

**Verified budget inputs: Google only.** Per-image and per-generation prices for Nano Banana 2,
Nano Banana Pro, Nano Banana 2 Lite, Veo 3.1 (all three tiers), Gemini Omni Flash, Imagen 4 and
Lyria 3. Twenty-two candidate rows have no verified price.

## 3. How this was verified without provider websites

The task forbids search snippets from populating version or price fields, and almost every vendor
site was blocked. The route through was **vendor-published SDKs**: packages the vendors themselves
ship to PyPI and npm, whose generated type definitions are the vendor's own statement of model ids
and request parameters.

Nine provider-authorised sources were used, including OpenAI's, Google's, Runway's, Sarvam's,
ElevenLabs', Alibaba's, BytePlus's and fal's own clients. **The most valuable single artifact was
fal's npm client**, which ships 1,117 endpoint identifiers with typed inputs — fal stating in its
own code exactly what it exposes.

**Four candidate packages were rejected** rather than used: one self-declares as an *unofficial*
Black Forest Labs client, and three had no verifiable publisher. Provenance was checked before
anything was trusted.

**The limit is stated everywhere it applies:** an SDK can lag a live catalogue. Missing entries are
recorded as `not_present_in_sdk_version`, never as "unavailable". Unavailable and undocumented are
kept apart throughout.

## 4. Frontier Clouds — and why the EVAL-008 claim was not adopted

EVAL-008's branch claims Frontier Clouds means **GCP + AWS + Azure** and builds an availability
table on it. **Not adopted, for three independent reasons.**

1. **You have already ruled on it.** `CONTROL-STATE.md` records it as "not a Controller decision on
   record" that "must be reverified/confirmed rather than assumed".
2. **The underlying statement did not say what EVAL-008 used it for.** It traces to a remark that
   frontier clouds are *usually* those three — a general observation about the phrase, not a
   statement that **your credits sit there**. A hedged generality was promoted into a specific premise.
3. **It could not be checked anyway.** AWS and Azure hosts were re-probed this session and all
   returned `403`.

Nothing found refutes the claim either. It is unevidenced, not disproven. A 26-row checklist is
ready to run the moment the service is identified — see `FRONTIER-CLOUDS-CHECKLIST.md`.

## 5. Corrections to EVAL-008 you should carry forward

**Eight fal and access claims contradicted by the providers' own material** — notably that GPT
Image 2, Seedance 2.0, HappyHorse 1.1, MiniMax H3, Sync-3, Reve 2.1 and Gemini Omni are on fal.
fal's own client enumerates none of them at the claimed version. HappyHorse, which EVAL-008 called
its "best-evidenced fal row", has **zero** endpoints there.

**The ~99% Hindi/Bengali accuracy claim is rejected as unverified**, per your instruction. No
primary source was reachable and no provider artifact carries such a figure.

**One correction runs the other way.** EVAL-008 flagged **Runway** as possibly Enterprise-gated and
called it the roster's hardest access problem. **Runway's own published SDK exposes the full public
API**, including `aleph2` video-to-video with keyframes. That account action should be withdrawn.
Whether *your* account is entitled is a separate question this task must not test.

**And a price correction:** Nano Banana Pro's image price is **not** missing — EVAL-008 read an
empty table cell, but the value is published in the footnote ($0.134 at 1K/2K, $0.24 at 4K). Its
*identity* is the actual gap.

## 6. Two findings that should reach EVAL-009 before it freezes measurement

These are supply facts with measurement consequences. They are offered as findings, not as
selection advice.

**Reproducibility is not uniformly available, and it breaks a proposed threshold.** Twelve verified
routes expose a `seed`; seven do not — including **OpenAI's image API**, which has none on either
generate or edit. The proposed **0.95 repeat-consistency threshold** therefore cannot mean the same
thing across routes: seeded routes measure variance under a held seed, unseeded routes measure
inherent variance. **Sarvam exposes `temperature` and no seed while ElevenLabs exposes `seed`** — so
the most product-relevant voice comparison on the list is not currently like-for-like. EVAL-009
should pick one convention and apply it across the wave.

**Aggregator wrappers are thinner than they look, and the gaps land on our hardest problem.** fal's
ElevenLabs wrapper omits `seed`, the pronunciation-dictionary locators and the previous/next-text
continuity controls that ElevenLabs direct exposes. The pronunciation dictionary is exactly the
mechanism for forcing correct Indian brand-name pronunciation — **so a voice measurement taken
through fal cannot test the thing we most need to test.** Sarvam direct, by contrast, exposes a
dedicated pronunciation-dictionary resource.

Five route-equivalence risks are specified in `ROUTE-EQUIVALENCE-RISKS.md`, with the exact test
each needs before rows from two routes may be pooled. The cheapest useful one is the Google
fal-vs-direct comparison, because Google is the only vendor where we hold both a verified price and
a verified GA identity.

## 7. Mechanical gates — self-check

| Gate | Status |
|---|---|
| Selection rationale changed because of sourcing | **No** — no candidate added, removed or reprioritised |
| A sibling model silently substituted | **No** — five family-only matches recorded as `do_not_substitute` |
| A search snippet populated a version or price field | **No** — every execution-grade field cites a provider page or vendor SDK |
| Price without billing unit, date and source | **No** — all seven price blocks carry all three |
| Unavailable and undocumented conflated | **No** — `not_present_in_sdk_version` used throughout |
| Aggregator and direct routes pooled | **No** — kept separate, with five equivalence risks specified |
| Frontier Clouds guessed | **No** — left `unresolved_service_identity` |
| Any login, account, terms or payment action | **No** |
| Partial table described as complete | **No** — "2 of 26 execution-ready" is stated in every summary |

## 8. What is still blocked

Everything that was blocked before. No model is qualified, no checker exists, no Registry row was
created, no budget is approved, and nothing here authorises spend. **Choosing what to measure and
knowing how to call it are still not the same as being able to measure it** — the unqualified-checker
dependency is untouched by this task.

The single highest-value unblock is not more research: it is **network access to provider pricing
pages**, which would convert most of `PRICE-VERIFICATION.yaml` from null to verified in an
afternoon. The second is **the Frontier Clouds identity**, which is the only thing that can turn
nominal cost into actual cash outlay.
