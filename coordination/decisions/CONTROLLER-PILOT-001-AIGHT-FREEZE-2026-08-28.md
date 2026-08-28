# Controller — PILOT-001 Aight Vertical-Slice Freeze — 2026-08-28

## Status
**BRIEF / BRAND / RECIPE / ACCEPTANCE FROZEN. PAID EXECUTION PENDING EXPLICIT USER SPEND APPROVAL.**

This decision begins T1 of the revised outcome-first programme. It does not qualify any model,
populate the Capability Registry, or authorise paid execution by itself.

## Purpose

Produce the project's first real end-to-end customer-style outcome:

customer brief → Normalized Request → Creative IR → manually frozen production recipe →
real provider generation → deterministic composition → explicit human acceptance →
at most one bounded repair → accepted outcome or honest failure.

PILOT-001 is product-learning evidence only.

## Upstream frozen inputs

- `canon/experiments/pilot-001/aight-normalized-request.yaml`
- `canon/experiments/pilot-001/aight-creative-ir.yaml`
- merged RES-007 outcome writer
- merged EVAL-035 direct Gemini/Veo substrate

## Official Aight brand source — blocker resolved

CANON-012 correctly recorded that no logo asset existed inside media-intelligence. The Controller
has now located the official source-of-truth in the user's Aight website repositories and verified
the same wordmark is live at `https://getaight.ai/`.

Primary durable source:
- repo: `chawlavaibhav/Aight_Website`
- commit: `38a9fb6e5d7d5d946f53e731f3d214d27b425cae`
- `index.html` blob SHA: `02469cdaf95cf32eb4ae49005b73aa75ac1c4f3b`

Independent staging source with the same wordmark treatment:
- repo: `chawlavaibhav/aight-site-preview`
- commit: `c1725a5bbb32cf314703dc155f8765554e28479b`

The official source defines:
- wordmark text: `Aight.`
- wordmark font: Source Serif 4
- weight: 600
- optical sizing: auto
- letter spacing: -0.01em
- normal wordmark ink: `#141f31`
- terminal full stop: `#b0341f`
- inverse wordmark on dark: `#f8f5ef` with the same `#b0341f` stop
- supporting brand tokens: paper `#f8f5ef`, ink `#141f31`, stamp red `#b0341f`,
  Public Sans for sans/currency text, IBM Plex Mono for mono annotations.

For PILOT-001 this source specification is the **official wordmark master**. The execution worker
must render/capture it deterministically from the cited source; the generative model must never
invent or repaint it.

This supersedes CANON-012's *current-state blocker* that the wordmark ground truth was unavailable;
the historical CANON-012 record remains unchanged and truthful for when it was written.

## Frozen brief choices

The previously open choices are resolved for this pilot only:

- deliverables: 1
- modality: video
- duration: exactly 12 seconds (experiment fixture, not customer-intent precedent)
- aspect ratio: 9:16 (experiment fixture)
- target raster: 720 × 1280
- festival specificity: generic Indian festive; **no named festival**
- audience: Indian commercial buyers of AI/media APIs
- dialogue: none
- voiceover: none
- lyrics: none
- CTA / destination: `getaight.ai` on the closing card
- brand presence: official `Aight.` wordmark on the closing card
- positioning copy: `Outcome API`
- mandatory exact commercial strings:
  - `Image ₹9`
  - `Video ₹99`

The only customer-authoritative exact strings remain the two price claims. `Outcome API`,
`getaight.ai`, and the exact closing layout are frozen system decisions for PILOT-001 rather than
new customer facts.

## Frozen visual direction

Use the official Aight brand register rather than inventing an unrelated festive palette:

- base: Aight ink / deep navy (`#141f31`)
- type / light ground: warm paper (`#f8f5ef`)
- accent: stamp red (`#b0341f`) sparingly
- generative plate may add restrained warm metallic / amber / glass / textile light cues
- atmosphere: modern, premium, Indian-festive, warm, restrained
- avoid gaudy saturation, dense ornament, glitter overload, religious iconography, named-festival
  symbols, people/identity requirements, and any model-generated readable text or logos.

## Frozen production recipe — manual PIR seed #1

### Step P1 — provider motion plate

One direct Gemini Developer API call through merged EVAL-035:

- model: `veo-3.1-fast-generate-preview`
- 8 seconds
- 720p
- 9:16
- generative role: **motion / atmosphere plate only**
- prompt must explicitly request:
  - no text
  - no typography
  - no logos
  - no letters
  - no numbers
  - no people
  - no voice/dialogue/lyrics
  - a premium restrained festive motion field consistent with the frozen visual direction.

The prompt may ask for subtle non-lyrical ambient sound / sound design. Audio is not a required
success criterion. If provider audio contains speech, lyrics, or distracts materially, the local
step may strip it without another provider call.

### Step P2 — deterministic claims composition

Over the provider plate, deterministically add the exact strings:

- `Image ₹9`
- `Video ₹99`

Timing target:
- 0–4s: clean festive motion field / hook
- 4–8s: both exact price claims legible over the motion field

Use Aight's official typography register. Price/currency text should use the official Public Sans /
currency fallback treatment or a deterministic equivalent rendered from the website source.
Stamp red is accent only; price text itself must remain highly legible.

The model output is never trusted for these exact strings.

### Step P3 — deterministic 4-second endcard

Create a 4-second deterministic endcard from 8–12s.

Required content:
- official `Aight.` wordmark rendered from the cited website source
- `Outcome API`
- `Image ₹9`
- `Video ₹99`
- `getaight.ai`

Default endcard ground:
- `#141f31`

Wordmark:
- inverse `Aight` in `#f8f5ef`
- terminal `.` in `#b0341f`
- Source Serif 4 / 600 / -0.01em, matching the official source.

Other text uses the official Aight sans/currency register.

The exact prices are intentionally repeated on the endcard to maximise legibility and make
acceptance auditable.

### Step P4 — assembly

Assemble P1/P2/P3 locally into one final 12-second 9:16 video.

Record:
- transform tool + version;
- exact composition parameters;
- source artifact hashes;
- rendered brand-asset provenance;
- final output hash/bytes/location;
- local-compute cost where measurable.

Do not create a provider attempt for local deterministic work.

## Frozen repair policy

**Maximum one repair total for the outcome journey.**

After the first complete composite is inspected:

- if the defect is deterministic (copy placement, timing, endcard, audio strip, composition),
  the one repair may be a local deterministic correction;
- if the defect originates in the provider motion plate and cannot reasonably be fixed locally,
  the one repair may instead be a second provider generation followed by the same deterministic
  composition recipe.

There is never:
- an automatic retry;
- a third provider generation;
- a second repair after the repair attempt.

Exact price/logo problems should normally be repaired deterministically, not by asking Veo to
render text again.

If the repaired outcome still fails, PILOT-001 ends as an honest failed vertical slice.

## Frozen acceptance contract

### Machine / hard checks

The final candidate must:

1. be a playable video artifact with retained bytes;
2. be exactly 12 seconds within normal container/frame-duration tolerance;
3. be 720 × 1280 / 9:16;
4. contain `Image ₹9` exactly;
5. contain `Video ₹99` exactly;
6. contain closing `Aight.` matching the official source definition;
7. contain `Outcome API` on the closing card;
8. contain `getaight.ai` on the closing card;
9. contain no unintended model-generated readable/gibberish text or logos that remain visible;
10. contain no dialogue, voiceover, or lyrics.

For the two customer-authoritative prices, machine/OCR evidence may assist but does not certify
strict exactness; the human inspection must visually confirm the deterministic overlays.

### Human subjective checks

The final human reviewer must answer PASS/FAIL separately for:

- H1 modern and premium;
- H2 recognisably Indian-festive without needing a named festival;
- H3 restrained / not gaudy;
- H4 the primary takeaway is that Aight is an outcome API;
- H5 the two prices are immediately legible and feel like the primary commercial message;
- H6 the final artifact is something the reviewer would be willing to put in front of an Aight
  customer / publish as an Aight promotional asset.

All six must PASS for customer-level acceptance.

No numeric creative-quality score is invented for this pilot.

### Acceptance authority

PILOT-001 requires an explicit human outcome-acceptance row in RES-007. The final user/Controller
acts as the customer proxy for this pilot. Blinding is not required.

## Spend posture

Published planning rate at freeze time:
- Veo 3.1 Fast 720p: USD 0.10/generated second
- one 8s provider attempt: approximately USD 0.80
- maximum two provider attempts under the one-repair policy: approximately USD 1.60

**Controller recommendation: PILOT-001 API-spend cap = USD 2.00, retries authorised = 0.**

The extra USD 0.40 is ceiling headroom only, not a target. It does not authorise a third call.

PAID EXECUTION IS NOT YET AUTHORISED because the user has not explicitly approved this cap.

For safety, this decision deliberately contains **no** top-level `machine_authorisation` block
that EVAL-035 could parse as permission.

Proposed future authority after explicit user approval:

```yaml
proposed_machine_authorisation:
  tranche: PILOT-001
  authorised: true
  max_consumed_api_spend_usd: "2.00"
  retries_authorised: 0
  approval_identity: user
  approval_date: 2026-08-28
```

A separate Controller spend-authorisation decision must replace this proposal with the exact
machine-readable authority format only after explicit approval.

## Execution-time stop conditions

Before the first provider dispatch, reverify:
- the exact Gemini model identifier still exists;
- the direct API request contract still matches EVAL-035;
- 8s / 9:16 / 720p remain supported;
- current price fits within the approved ceiling;
- `GEMINI_API_KEY` is present at runtime;
- no provider funding/minimum-deposit condition exceeds the approved ceiling;
- the official Aight brand source commit is accessible locally or has been materialised
  reproducibly for deterministic rendering.

If an essential provider contract changed, stop rather than silently substituting a different
model/route.

## What this freeze does not authorise

- no provider call yet;
- no API spend yet;
- no Registry row;
- no model qualification;
- no T2 model comparison;
- no Stage B/C;
- no Planner implementation;
- no formal Production IR schema;
- no extra evaluator qualification.

## Next action

Obtain explicit user approval of the recommended **USD 2.00 PILOT-001 cap / 0 retries**.

After that approval, create the machine-readable spend-authorisation decision and execute this
frozen vertical slice without another design round.
