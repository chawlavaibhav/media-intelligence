# PILOT-001 — Key-Bearing Execution Runbook

**Date:** 2026-08-28  
**Status:** AUTHORISED FOR PAID EXECUTION  
**Spend ceiling:** USD 2.00 max consumed API spend  
**Retries:** 0  
**Maximum provider generations:** 2 only if generation #2 is the single authorised repair  
**Primary authority:** `coordination/decisions/CONTROLLER-PILOT-001-SPEND-AUTHORISATION-2026-08-28.md`  
**Frozen recipe:** `coordination/decisions/CONTROLLER-PILOT-001-AIGHT-FREEZE-2026-08-28.md`

This runbook is the exact execution packet for a key-bearing worker. It is not permission to redesign
the brief, route, acceptance criteria, or budget.

## Branch

Create fresh branch:

`work/pilot-001-aight-execution`

from current `main`.

Do not reuse EVAL-035 or RES-007 worker branches.

## Required startup

Read in order:

1. `PROJECT-MEMORY.md`
2. `coordination/CONTROL-STATE.md`
3. `coordination/PROJECT-CONTRACT.md`
4. `shared/COMMUNICATION-STANDARD.md`
5. `shared/CONTEXT-SUFFICIENCY-POLICY.md`
6. `coordination/decisions/CONTROLLER-PILOT-001-AIGHT-FREEZE-2026-08-28.md`
7. `coordination/decisions/CONTROLLER-PILOT-001-SPEND-AUTHORISATION-2026-08-28.md`
8. `coordination/plans/2026-08-28-PILOT-001-AIGHT-VERTICAL-SLICE.md`
9. merged `eval/pilot-substrate/`
10. merged `resources/pilot-writer/outcome_writer.py`
11. merged v3 topology/CpAO validators
12. CANON-012 NR/CIR for PILOT-001.

Confirm `shared/COMMUNICATION-STANDARD.md` once.

## Hard preflight — before any provider send

### P0.1 Current-main freshness
- fetch current `main`;
- branch must start from current main;
- if a newer Controller decision changes PILOT-001, stop and obey it.

### P0.2 Credential
Check only whether `GEMINI_API_KEY` exists.

Never print, persist, hash, log, echo, or commit the key.

If absent:

`STOP — GEMINI_API_KEY_MISSING`

No dispatch.

### P0.3 Provider contract re-verification
Using official Google documentation only, reverify:
- `veo-3.1-fast-generate-preview` remains a Gemini API model id;
- direct REST base `https://generativelanguage.googleapis.com/v1beta`;
- submit endpoint `:predictLongRunning`;
- auth header `x-goog-api-key`;
- 8 seconds supported;
- 9:16 supported;
- 720p supported;
- polling/download contract still matches merged EVAL-035;
- Veo 3.1 Fast 720p current price is compatible with the USD 2.00 ceiling.

If any essential contract changed:

`STOP — PROVIDER_CONTRACT_CHANGED`

Do not silently substitute another model.

### P0.4 Local authority
Materialise, locally only:

`eval/pilot-substrate/authorization.pilot.local.yaml`

with exactly:

```yaml
tranche_id: PILOT-001
authorised: true
max_consumed_api_spend_usd: "2.00"
retries_authorised: 0
approved_by: "Vaibhav Chawla"
approved_at: "2026-08-28T07:22:45Z"
decision_ref: "coordination/decisions/CONTROLLER-PILOT-001-SPEND-AUTHORISATION-2026-08-28.md"
```

This file is git-ignored and MUST NOT be committed.

Run the real authority verifier and prove it opens.

### P0.5 Persistent run identity
Create/open exactly one PILOT-001 spend run under the git-ignored runtime root.

Recommended run id:

`pilot-001-aight-2026-08-28`

If that run id already exists, OPEN it. Do not overwrite or create a second run to reset spend.

### P0.6 Brand source
Materialise the official Aight website source at exactly:

- repo `chawlavaibhav/Aight_Website`
- commit `38a9fb6e5d7d5d946f53e731f3d214d27b425cae`
- `index.html` expected Git blob SHA `02469cdaf95cf32eb4ae49005b73aa75ac1c4f3b`.

If the pinned source cannot be obtained or does not match:

`STOP — BRAND_SOURCE_MISMATCH`

Do not substitute a logo from search or regenerate it.

## Provider prompt — frozen

Use this semantic prompt. Minor punctuation changes for API encoding are allowed; no creative
rewriting after seeing the result.

> Create an 8-second vertical cinematic motion plate for a premium Indian AI brand during the festive season. Deep ink-navy atmosphere with restrained warm amber and metallic light, subtle premium glass/brass/silk material cues, elegant dimensional glow, modern and minimal, celebratory but sophisticated and understated. Slow controlled cinematic movement, visually rich enough to support later typography overlays, with clean negative space and no identity-bearing subject. Generic Indian festive mood only; do not depict a named festival or religious symbol. Absolutely no text, no typography, no logos, no letters, no numbers, no signage, no people, no dialogue, no voiceover, no lyrics. Avoid gaudy saturation, glitter overload, dense ornament, kitsch, or clutter.

Call:
- direct Gemini Developer API;
- model `veo-3.1-fast-generate-preview`;
- duration 8;
- aspect 9:16;
- resolution 720p;
- merged EVAL-035 route only.

Do not set an undocumented seed or extra provider parameter.

## Attempt 1

Use merged:

- `pilot_authorisation.verify_authority`;
- `pilot_spend_ledger.open_pilot_runtime`;
- `video_route.LiveGeminiTransport`;
- `video_route.generate_pilot_video`.

Before network send the persistent ledger must contain the USD 0.80 reservation.

Call context must include stable production identities sufficient for RES-007.

Do not retry transport failures.

### Provider evidence persistence

Persist the returned provider MP4 under a durable, non-ignored project evidence path, e.g.:

`eval/pilot-001/evidence/artifacts/provider-attempt-001.mp4`

The exact path may vary only to preserve immutable IDs.

**Do not put irreplaceable provider bytes under `eval/runs/`**: that tree is intentionally
git-ignored for machine-local runtime state, while class-C provider media is irreplaceable evidence.

Also persist:
- exact request config JSON;
- provider attempt record;
- cost ledger handoff;
- SHA-256;
- byte count;
- operation id;
- timestamps;
- raw provider status fields needed to reconstruct lifecycle.

Commit the provider media if it is within normal GitHub file limits.

If any irreplaceable provider/final artifact is too large for ordinary git and no approved durable
artifact store already exists:

`STOP — DURABLE_ARTIFACT_STORE_REQUIRED`

Do not silently leave the only copy in an ignored runtime directory.

## Deterministic brand rendering

Do not ask an image/video model to render any Aight text.

Use a deterministic headless-browser render sourced from the pinned Aight website HTML/CSS.

Preferred method:
1. open the pinned `index.html` locally in Playwright/Chromium;
2. wait for embedded fonts to load;
3. use its own CSS/font definitions;
4. render transparent/full-frame PNG overlays at 720×1280.

Required brand identity from source:
- `Aight.`
- Source Serif 4, weight 600;
- letter-spacing -0.01em;
- ink `#141f31`;
- inverse `#f8f5ef`;
- terminal stop `#b0341f`;
- other text in official Public Sans/currency register.

Do not extract or publish font files as user-facing artifacts.

## Deterministic composition

Create:

### Overlay A — claims
Used 4.0s–8.0s over the Veo plate.

Exact:
- `Image ₹9`
- `Video ₹99`

Both must be large, immediately readable, and rendered deterministically from the official Aight
type register.

### Endcard
Used 8.0s–12.0s.

Ground:
- `#141f31`

Required:
- `Aight.`
- `Outcome API`
- `Image ₹9`
- `Video ₹99`
- `getaight.ai`

Use official source-derived rendering.

### Audio
Strip provider audio from the final candidate by default for PILOT-001.

Reason: the acceptance contract prohibits dialogue/voiceover/lyrics and audio is not required for
the pilot. Silence satisfies the frozen contract without introducing an unqualified speech/audio
judgement.

This is a deterministic local transform, not a provider repair.

### Assembly
Use deterministic local media tooling such as ffmpeg.

Target:
- exact 12s final duration within normal frame/container tolerance;
- 720×1280;
- 9:16;
- playable MP4.

Record exact command/tool version and hashes of all parents.

## Durable final artifacts

Persist outside ignored runtime state:

- provider attempt MP4;
- claims overlay/render artifact;
- endcard render artifact;
- final 12s candidate MP4;
- request config;
- production/run manifest;
- RES-007 archive;
- hard-check report.

Suggested root:

`eval/pilot-001/evidence/`

Generated media must be labelled empirical PILOT-001 evidence, not Registry qualification evidence.

## RES-007 recording

Use the actual merged `OutcomeWriter`.

Minimum journey:
- job;
- outcome;
- set;
- unit;
- provider step;
- provider attempt + cost row;
- provider artifact;
- local claims-composition step;
- local endcard-render step;
- local assembly/audio-strip step;
- final artifact;
- human-review step/acceptance only when the user/Controller has actually reviewed it.

No fake provider attempt for local work.

Run merged topology validator on the archive.

Run available CpAO computation, but do not invent HED-1 semantics or customer-acceptance status.

## Hard pre-human QC

Before returning the candidate, mechanically verify:

1. final MP4 exists and hashes;
2. playable/container probe succeeds;
3. 720×1280;
4. 9:16;
5. ~12s within one-frame/container tolerance;
6. exact deterministic render source contains `Image ₹9`;
7. exact deterministic render source contains `Video ₹99`;
8. exact endcard source contains `Aight.`, `Outcome API`, `getaight.ai`;
9. final has no audio stream;
10. no second provider call occurred;
11. spend runtime shows no more than USD 0.80 consumed after successful attempt 1;
12. RES topology validator passes for the pre-acceptance archive.

Also inspect the provider plate visually for unintended generated text/logos. If obvious model-generated
text/logo survives into the final plate, mark the candidate failed before user review.

## Return after attempt 1 — mandatory human gate

Do **not** consume the one repair merely because the worker personally dislikes the creative.

Return the first complete candidate to the Controller/user with:
- final MP4;
- provider plate MP4;
- hard-check report;
- actual API spend;
- operation id;
- attempt/cost ids;
- any obvious provider-origin defect;
- pre-acceptance RES archive/validator result.

The user/Controller then judges H1–H6.

Do not write an accepted outcome row before that human decision.

## Repair — only after explicit Controller disposition on candidate 1

There is at most ONE repair total.

If Controller says PASS:
- record acceptance;
- no repair.

If Controller identifies deterministic defect:
- repair locally once;
- no second provider call unless specifically necessary.

If Controller identifies provider-plate defect that cannot reasonably be fixed locally:
- a second and final provider generation may be executed as the one repair;
- reserve another USD 0.80 before send;
- same frozen prompt/route unless Controller's defect disposition explicitly changes only the
  repairable production parameter allowed by the freeze;
- no third call under any condition.

After repair, return final candidate for one final human acceptance decision.

## Stop conditions

Stop immediately without improvisation for:
- missing key;
- provider contract change;
- authority verification failure;
- spend-ledger corruption;
- cap mismatch;
- brand-source mismatch;
- unknown live provider response that makes dispatch state ambiguous;
- inability to persist irreplaceable media durably;
- a required cross-stream contract change;
- any proposal to use a different provider/model.

For an ambiguous post-dispatch condition, preserve the failed attempt and conservative spend; never
resubmit automatically.

## Commit / push

Commit and push branch `work/pilot-001-aight-execution`.

Do not merge.

Do not commit:
- API key;
- local runtime authorisation;
- machine-local spend run under `eval/runs/`.

Do commit durable empirical evidence and manifests permitted by repository policy.

## Completion response for candidate 1

Return only:
- PILOT-001
- branch
- commit SHA
- base-main SHA
- provider/model
- provider attempts used
- real spend consumed
- provider operation id
- provider artifact SHA/path
- final candidate SHA/path
- hard checks
- RES topology validator
- CpAO views available / unavailable and why
- live unknowns encountered
- whether candidate is ready for H1–H6 human review
- no acceptance verdict yet.
