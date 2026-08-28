# Pilot video-route substrate (EVAL-035, corrected)

The minimum execution machinery a later PILOT-001 needs to dispatch **one** real video
generation and persist the returned media as **binary bytes**. Built under
`CONTROLLER-REVISED-PROGRAM-AND-PREPILOT-TRANCHE-2026-08-28.md`; corrected under
`CONTROLLER-EVAL-035-RETURN-REVIEW-2026-08-28.md` and
`CONTROLLER-DIRECT-GEMINI-T1-ROUTE-REVISION-2026-08-28.md` with **USD 0 spend, zero
provider calls, zero real generations**.

## Route policy (superseding the first pass)

The first-pass fal implementation was **superseded by Controller/user infrastructure
policy**: for Google generation models this project talks to the **direct Gemini Developer
API** with `GEMINI_API_KEY` — no aggregator layer, no aggregator retry/fallback/auth
behaviour. All fal-specific execution code (fal route identity, `FAL_KEY`, queue URLs,
`X-Fal-No-Retry`, fal schemas and pricing) has been removed.

- **One route, exactly.** `veo-3.1-fast-generate-preview` on
  `generativelanguage.googleapis.com` (`:predictLongRunning`). T1 plumbing only — not model
  qualification, not a Registry row, not a claim Veo is the best production model. Veo's
  pilot role is the generative motion/visual plate; exact Aight brand/text elements are
  composited deterministically later and this route is not designed around rendering them.
- **The EMP-001 spend discipline, unchanged.** No transport injected → no dispatch. No
  budget guard → no dispatch. Reservation before send; provably-pre-dispatch failures
  release the reservation; anything after the send began is AMBIGUOUS — counted
  conservatively, persisted as a real failed trial, never retried. The exception classes
  are imported from `eval/empirical-tranche-1/providers.py` rather than re-declared.
- **The long-running-operation lifecycle, explicitly.** submit → operation name → poll
  `done` → read `generateVideoResponse.generatedSamples[0].video.uri` → authenticated
  binary download. The **submit is the generation trial**; polls, the result read and the
  download never inflate the generation count. Google retains the server-side file for
  2 days only, so the local binary copy is the artifact.
- **Machine-verifiable spend gate.** `pilot_authorisation.py` opens a guard only when a
  COMMITTED Controller decision carries an explicit `machine_authorisation` YAML block for
  `PILOT-001` (cap, zero retries, approval identity/date) AND the local, git-ignored
  runtime file matches it. No such committed decision exists — tests prove the current
  repository state cannot open a paid guard, and a locally authored YAML cannot
  manufacture authority.
- **RES-007 handoff.** `res007_production_attempt()` emits exactly the corrected v3
  writer's production-attempt field set (provider/model_id/model_version/endpoint/
  workflow/prompt_hash/config_hash/config_location/reference_asset_hashes/timestamps/
  lane/status/repeat/retry/cost_ref/storage_class) with **no fabricated `eval_item_id`**;
  provider-specific evidence rides in a separate `provider_extras` mapping because the
  corrected writer refuses unknown fields.
- **Binary artifact handling.** `artifact_store.py` accepts `bytes` only (a `str` is
  refused with `TypeError`), writes with `write_bytes`, records SHA-256, byte length,
  media kind, location, exact route/model identity and the provider operation name. Test
  fixtures are deliberately invalid UTF-8 so any accidental text-API path fails loudly.

## Contract provenance

| Fact | Source |
|---|---|
| Route policy: direct Gemini API, `GEMINI_API_KEY`, model `veo-3.1-fast-generate-preview`, 720p, 9:16 | `coordination/decisions/CONTROLLER-DIRECT-GEMINI-T1-ROUTE-REVISION-2026-08-28.md` |
| Endpoint `POST /v1beta/models/{model}:predictLongRunning`, header `x-goog-api-key`, body `instances[{prompt}]` + `parameters{aspectRatio, durationSeconds, resolution}`; durations 4\|6\|8 s; aspect 16:9\|9:16; operation polling via `GET /v1beta/{operation.name}`; result at `response.generateVideoResponse.generatedSamples[].video.uri`; authenticated download; 2-day retention; native audio; safety filters may block (blocked videos documented as not charged) | Official Google docs, `ai.google.dev/gemini-api/docs/veo`, fetched 2026-08-28 |
| Price: Veo 3.1 Fast 720p **USD 0.10 per generated second, audio included** | Official Gemini API pricing page, fetched 2026-08-28 — provisional planning rate, NOT invoice evidence |
| `raiMediaFilteredCount` / `raiMediaFilteredReasons` field names | Google's Veo reference on the sibling Vertex surface (same response proto); read **only if present**, never interpreted when absent |
| Corrected production-attempt field requirements (G12), status vocab `ok\|error\|refusal\|timeout\|cancelled`, lane `native_av`, no `eval_item_id` on production attempts | `CONTROLLER-PREPILOT-RETURN-REVIEW-1-2026-08-28.md` + `work/res-007-pilot-writer` `outcome_writer.py` |

**Route identity, availability, schema and price must all be re-verified at execution time
before any live PILOT-001 call** (CONTROL-STATE "Next gate"). Provider docs move; the
`-preview` suffix means the model identifier itself may be retired or renamed.

## Tests

`python3 -m pytest eval/pilot-substrate/tests/ -q` — every test runs against injected fake
transports; an autouse fixture makes any real socket use raise and strips
`GEMINI_API_KEY` from the environment. No network, no key, no spend.
