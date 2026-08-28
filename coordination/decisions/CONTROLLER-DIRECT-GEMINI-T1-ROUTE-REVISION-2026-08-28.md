# Controller — Direct Gemini Route Policy and T1 Executor Revision — 2026-08-28

## Status
**APPROVED. SUPERSEDES THE FAL ROUTE SELECTION INSIDE THE EVAL-035 RETURN REVIEW.**

Current main at decision time: `7c4ef451b13a1c4791a66fc17bcfbb43dc10392f`.

## User-supplied infrastructure constraint

For Google generation models used by this project, use the **direct Gemini Developer API / Google GenAI surface with `GEMINI_API_KEY`**, not fal as an intermediary, unless a later Controller decision explicitly approves an aggregator for a specific reason.

This applies to EVAL-035 and PILOT-001.

## Why

A direct Gemini Veo API is currently available. Using fal for a Google model would add an unnecessary provider layer, its own retry/fallback/routing behaviour, separate auth, and extra provenance ambiguity. None of that helps the first vertical slice.

## T1 route decision

T1 does **not** select the project's winning production video model.

T1 only needs one credible execution route to prove:
customer brief → NR → Creative IR → production recipe → generation → deterministic composition → human acceptance → persisted outcome/cost.

The temporary T1 execution route is:

- provider surface: **Gemini Developer API**
- credential: **`GEMINI_API_KEY`**
- model: **`veo-3.1-fast-generate-preview`**
- resolution: **720p**
- aspect ratio for Aight pilot: **9:16**
- role: **generative motion/visual plate**, not exact brand/text rendering

This is an infrastructure choice for PILOT-001 only, not model qualification and not a Registry row.

Reason for Fast rather than Standard for T1:
- credible commercial-quality route;
- materially cheaper than Standard;
- direct API;
- sufficient for a real vertical-slice learning run.
T2 remains responsible for demand-driven comparison of serious production candidates.

## First Aight production shape

PILOT-001 should be a **hybrid production**, not a single text-to-video call asked to do everything.

Target working recipe:

1. Generate an approximately **8-second 9:16 festive premium motion plate** with Veo 3.1 Fast.
2. Do **not** rely on Veo to render the exact Aight wordmark or exact price copy.
3. Composite exact brand/text deterministically after generation.
4. Use the exact required strings:
   - `Image ₹9`
   - `Video ₹99`
5. Use the official Aight wordmark/master supplied at the pilot gate.
6. Reach the 12-second fixture through local deterministic assembly (for example, generated motion followed by a deterministic branded end-card / held frame), not by pretending Veo can produce a native 12-second clip in one call.
7. Persist every provider and local step through the corrected v3 journey writer.

The exact production recipe is frozen only after CANON-012, EVAL-035 and RES-007 corrections return and the Aight asset package exists.

## EVAL-035 correction impact

The prior EVAL-035 branch implementation against fal is no longer the desired provider substrate.

EVAL-035 must resume on the same task branch and replace the fal-specific transport with a direct Gemini/Veo transport.

Required preserved semantics:
- one provider generation request = one attempt = one trial;
- no client-side retry;
- explicit request/model/config provenance;
- async long-running-operation polling does not inflate generation counts;
- actual binary video download/persistence;
- SHA-256 and byte count;
- ambiguous post-dispatch failures settled conservatively;
- hard spend gate;
- zero live/provider calls in EVAL-035 itself;
- complete production-attempt handoff to RES-007.

fal-specific retry/fallback headers and fal auth are removed because fal is no longer the provider.

## Spend posture

No paid call is authorised by this decision.

PILOT-001 spend still requires:
1. corrected pre-pilot tasks accepted;
2. Aight asset package present;
3. execution-time direct Gemini route/model/price verification;
4. explicit user-approved pilot spend cap recorded durably.

## T2 remains unchanged

After T1, T2 evaluates relevant serious routes. Veo 3.1 Fast is not privileged because it was used in the pilot. It is simply the first plumbing route.
