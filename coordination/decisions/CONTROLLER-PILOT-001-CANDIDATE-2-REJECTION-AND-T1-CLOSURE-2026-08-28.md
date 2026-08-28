# Controller — PILOT-001 Candidate 2 Rejection and T1 Closure — 2026-08-28

## Status
**CANDIDATE 2 REJECTED BY THE HUMAN ACCEPTANCE AUTHORITY. PILOT-001 / T1 IS CLOSED AS AN HONEST,
FULLY-EVIDENCED FAILED VERTICAL SLICE. NO REPAIR REMAINS. NO FURTHER PILOT-001 PROVIDER CALL IS
AUTHORISED, EVER.**

## Human verdict on Candidate 2

User feedback (customer proxy / acceptance authority, 2026-08-28, recorded durably here):
- technically, the output is exactly what the prompt asked for — no errors at all;
- the video is still not acceptable ("still garbage");
- the user attributes the failure to the prompt itself, not the pipeline;
- what held both times: text, logo and symbol consistency (the deterministic layer).

Controller mapping against the frozen acceptance contract:
- H1 modern and premium: **FAIL**
- H6 publishable / customer-facing: **FAIL**
- H5 price legibility: **PASS**
- deterministic brand rendering: **PASS**
- H2/H3/H4 cannot rescue a candidate that fails H1/H6.

Candidate 2 is **REJECTED**. Under the freeze, the repair budget is exhausted; T1 closes.

## Evidence state (verified on `origin/work/pilot-001-aight-execution` @ `3548b73`)

- Attempt 2 executed under the superseded single-scene prompt: one provider call,
  `veo-3.1-fast-generate-preview`, 8s/9:16/720p, provisional USD 0.80
  (`pilot-cost-res-000003`), 0 retries.
- Hard checks: **13/13 PASS** (`hard-check-report-attempt-2.json`, candidate sha256 `a18bbdae…`).
- Candidate 1 evidence preserved unchanged; Candidate 1 rejection recorded in the journey record.
- The execution branch is to be merged to `main` as-is to seal all evidence. Both candidates and
  both provider plates remain durable REJECTED evidence. Do not regenerate anything.

## PILOT-001 outcome line (first real CpAO datum)

- Provider attempts: 2 of 2 allowed (1 original + 1 repair). Retries: 0. Cap breaches: none.
- Consumed API spend: **USD 1.60 provisional** (2 × USD 0.80 modelled at the published rate;
  no invoice evidence), within the authorised USD 2.00.
- Accepted outcomes: **0**.
- **CpAO: undefined for this journey — cost with zero accepted outcomes.** Recorded as
  USD 1.60 spent / 0 accepted. This is the honest first datum for the primary metric.
- HED-1 scoping note for this line: human review time (two reviews by the user) is **not** costed
  in this pilot line; only consumed API spend is included. Full HED-1 remains open.

## Root-cause finding (product learning — the point of T1)

Three prompts have now been tried against the same substrate by two different Controllers:
abstract mood adjectives (Attempt 1), timed multi-phase choreography (withdrawn before dispatch),
and a simplified single-scene mood prompt (Attempt 2). All are variants of the same pattern:
**text-to-video from descriptive words, with no concrete product hero and no pre-approved visual**.
Both dispatched attempts passed every mechanical check and failed the same human bar (H1/H6).

The conclusion is now supported by the project's own paid evidence, the market review
(`coordination/plans/2026-08-28-EXTERNAL-PM-REVIEW-VIDEO-MARKET-2026-08.md` §A4/B2), **and the
user's own prior working system**:

### The media-factory precedent (new durable input)

The user's earlier project `chawlavaibhav/media-factory` (inspected read-only at commit
`7279ec5f61971a53a7069ec5149c2cb453b67a0a`) produced accepted stills and videos with one
consistent recipe family (`packages/recipes/src/static-ad.ts`, `video-ad.ts`, `campaign.ts`):

1. **Image first, with a concrete hero.** One still: *"Editorial commercial advertising photograph
   of {product} as the clear hero subject, {scene}. {tone} mood. The product anchored in the
   lower-left third; the upper-right two-thirds a soft, clean, empty gradient area kept open for a
   caption. Three-point softbox lighting, diffused highlights, no harsh shadows, shot on a 100mm
   lens at f/4, shallow depth of field. Surfaces clean, unmarked and blank, no text, no lettering,
   no logos, no signage. Advertising-catalog quality, ultra-sharp, 4k."*
2. **Motion prompt nearly empty.** Animate that approved still with only: *"A slow, gentle camera
   push-in. Soft natural light drifts across the scene. One smooth continuous move, no cuts. Keep
   everything stable — no warping, no morphing, no fast motion."*
3. **Deterministic composition of all text/logos** (media-factory hard rule 5 — identical to this
   project's posture, independently arrived at and validated there too).

The creative content lives in the *still*, where it is cheap to inspect and reject; the video step
only adds camera motion. PILOT-001 inverted this: it asked the video model to invent the creative
content, twice. That inversion — not prompt wording skill, not the Veo substrate, not the
deterministic pipeline — is the root cause of the T1 failure.

## What T1 delivered (for the record)

Validated end-to-end with real money: request → NR → Creative IR → manual recipe → real provider
call → deterministic brand/claims/endcard composition (100% pass rate across both candidates) →
hard-check gate → RES-007 journey/cost/lineage recording → bounded repair discipline → honest
human acceptance gate. The system works; the production pattern it was pointed at does not.

## Directives

1. **T1 is closed.** The execution branch is merged to seal evidence; no new PILOT-001 attempt
   may be created under any existing authority. A future Aight ad is a new task under a new
   decision, and must not run before the T2 screen answers the workflow question.
2. **T2 (programme plan §3) is confirmed as the next paid tranche** and its primary arm is
   image-first→animate, exactly as planned. The media-factory prompt family above is adopted as
   the **seed prompt pattern for T2 Phase 1** (parameterised per brief), replacing invention from
   scratch. The pure T2V control arm stays, so the pattern's superiority is measured, not assumed.
3. **Zero-spend task authorised now:** import the media-factory recipe/prompt/compositor patterns
   as recorded production knowledge — a documented pattern file with provenance (repo, commit,
   file paths), not a Canon source claim and not capability evidence. This seeds the "production
   intelligence extracted from successful real recipes" the revised programme requires.
4. Remaining PILOT-001 spend authority (USD 0.40 headroom) **lapses** with this closure. The T2
   envelope (USD 25) still requires explicit user approval before any paid call.
