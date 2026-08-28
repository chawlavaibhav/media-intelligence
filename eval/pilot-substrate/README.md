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
- **Machine-verifiable spend gate + persistent spend ledger.** `pilot_authorisation.py`
  verifies PERMISSION: a COMMITTED Controller decision carrying an explicit
  `machine_authorisation` YAML block for `PILOT-001` (cap, zero retries, approval
  identity/date), matched by the local, git-ignored runtime file. No such committed
  decision exists — tests prove the current repository state cannot open a live runtime,
  and a locally authored YAML cannot manufacture authority. The live guard itself is
  `pilot_spend_ledger.py`: an append-only on-disk ledger keyed to a PILOT-001 run
  (EMP-001's durable-ledger semantics as precedent, EMP-001's frozen constants untouched)
  — reservations persist before dispatch and count against the cap, settlements keep the
  reservation's stable `cost_ref`, releases happen only on provably pre-dispatch failure,
  process restart reconstructs committed + pending spend from disk, and corruption
  (bad line, sequence gap, truncation, missing run record, ceiling drift) fails closed.
- **RES-007 integration, against the MERGED implementation.** There is deliberately no
  local copy of the writer's field list. `res007_production_attempt()` and
  `res007_cost_ledger_entry()` emit writer-ready kwargs, and
  `tests/test_res007_integration.py` — the task's primary acceptance test — imports the
  merged `resources/pilot-writer/outcome_writer.py`, builds the minimum real v3 journey,
  calls the real `add_ledger_entry` → `record_attempt` → `record_artifact`, writes the
  archive, and runs the merged v3 topology validator (subprocess) — for the successful
  path AND a preserved ambiguous-failure path, plus a negative control proving the
  validator run can fail. `storage_class` is not passed to the writer (it owns the frozen
  storage class); no fabricated `eval_item_id`; provider evidence rides in
  `provider_extras`.
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
| Production-attempt requirements (G12), status vocab `ok\|error\|refusal\|timeout\|cancelled`, lane `native_av`, no `eval_item_id` on production attempts, writer-owned `storage_class` | The MERGED `resources/pilot-writer/outcome_writer.py` and `resources/pre-execution-freeze/validators/validate_topology_v3.py` on current `main` — called directly by the integration tests |

**Route identity, availability, schema and price must all be re-verified at execution time
before any live PILOT-001 call** (CONTROL-STATE "Next gate"). Provider docs move; the
`-preview` suffix means the model identifier itself may be retired or renamed.

## Tests

`python3 -m pytest eval/pilot-substrate/tests/ -q` — every test runs against injected fake
transports; an autouse fixture makes any real socket use raise and strips
`GEMINI_API_KEY` from the environment. No network, no key, no spend.
