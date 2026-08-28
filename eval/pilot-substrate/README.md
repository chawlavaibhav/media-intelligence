# Pilot video-route substrate (EVAL-035)

The minimum execution machinery a later PILOT-001 needs to dispatch **one** real video
generation and persist the returned media as **binary bytes**. Built under
`CONTROLLER-REVISED-PROGRAM-AND-PREPILOT-TRANCHE-2026-08-28.md` with **USD 0 spend, zero
provider calls, zero real generations**.

## What this package is

- **One route, exactly.** `fal-ai/veo3.1` (Google Veo 3.1, text-to-video, native audio) on
  fal's queue surface. The route identity is frozen in a table in `video_route.py`; nothing a
  caller passes can change it at runtime. Changing the pilot route is a Controller decision.
- **The EMP-001 spend discipline, unchanged.** No transport injected → no dispatch. No budget
  guard → no dispatch. Reservation before send; provably-pre-dispatch failures release the
  reservation; anything after the send began is AMBIGUOUS — counted conservatively, persisted
  as a real failed trial, never retried. The exception classes are imported from
  `eval/empirical-tranche-1/providers.py` rather than re-declared, so the semantics cannot
  drift from the machinery that already ran real money.
- **The async lifecycle, explicitly.** fal queues video jobs: submit → `request_id` → status
  polling → result fetch → artifact download. The **submit is the generation trial**. Polls,
  the result fetch and the download are lifecycle steps of that one trial and never inflate
  the generation count.
- **Binary artifact handling.** `artifact_store.py` accepts `bytes` only (a `str` is refused
  with `TypeError`), writes with `write_bytes`, and records SHA-256, byte length, media kind,
  location, route/model identity and the provider request id. Test fixtures are deliberately
  invalid UTF-8 so any accidental text-API path fails loudly.
- **Zero platform retries.** fal automatically retries queued requests (up to 10×) unless the
  client sends `X-Fal-No-Retry`. This substrate always sends it: one submit is one trial, and
  a platform-side re-run would be a silent retry we did not authorise.

## What this package is NOT

Not a model comparison, not model qualification, not a Planner, not general routing, and not
an authorisation to spend. `pilot_authorisation.py` fails closed: **no PILOT-001 spend
authority exists**, and live dispatch is impossible until the Controller and user create it.

## Contract provenance

| Fact | Source |
|---|---|
| Endpoint identity `fal-ai/veo3.1` (version pinned in path) | `eval/pre-execution-freeze/model-supply/FAL-VERIFIED-ROUTES.yaml` (fal's own SDK enumeration) |
| Billing per generated **second**; fal veo3.1 USD 0.40/s with audio | `coordination/decisions/CONTROLLER-VEO-PRICING-UNIT-CORRECTION-2026-08-26.md` — provisional planning rate, NOT invoice evidence |
| Queue API (`queue.fal.run` submit/status/response, `IN_QUEUE`/`IN_PROGRESS`/`COMPLETED`) | fal official docs, fetched 2026-08-28 (`fal.ai/docs/documentation/model-apis/inference/queue`) |
| veo3.1 input schema (`prompt`, `aspect_ratio` 16:9\|9:16, `duration` 4s\|6s\|8s, `resolution`, `generate_audio`, `auto_fix`) and output (`video.url/content_type/file_name/file_size`) | fal official model API page, fetched 2026-08-28 |
| Auto-retry default and `X-Fal-No-Retry` | fal official reliability docs, fetched 2026-08-28 |

**Route identity, availability, schema and price must all be re-verified at execution time
before any live PILOT-001 call** (CONTROL-STATE "Next gate" item 5). The table above is
planning evidence, and provider docs move.

## Tests

`python3 -m pytest eval/pilot-substrate/tests/ -q` — every test runs against injected fake
transports; an autouse fixture makes any real socket use raise. No network, no key, no spend.
