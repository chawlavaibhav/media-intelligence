# Controller Brief — EVAL-035

**TASK:** EVAL-035
**STATUS:** completed

**HUMAN SUMMARY:** The project can now, in software, do the thing PILOT-001 needs and could
not do before: send one real video-generation job to a provider, follow it through the
provider's waiting room ("submit the job, get a ticket number, keep checking until it is
done"), download the finished video, and store it as exact binary bytes with a
fingerprint — all under the same money discipline the paid image experiment used. One route
was implemented: **Google's Veo 3.1 via fal** (the same aggregator whose account and
authentication the project already used for real paid image generation). No money was spent,
no provider was contacted — every test runs against stand-in transports, and the test
harness makes a real network connection physically raise an error. Two provider facts found
in fal's current official documentation materially changed the implementation: fal silently
**re-runs failed jobs up to 10 times** unless a specific header disables it (our rule is
zero retries, so every request now sends that header), and the Veo endpoint **rewrites
prompts by default** when they trip content policy (`auto_fix` — pinned off, because a
silently rewritten prompt breaks the record of what actually ran). The main uncertainty is
unavoidable at USD 0: the real network path has never been exercised, and route, schema and
price must be re-verified at execution time before the first paid call.

**WHAT I DID:** Read the bootstrap chain, the authorising decision, and the EMP-001
dispatch/budget machinery the task requires me to preserve; selected the route from committed
Wave-1/route/price evidence; fetched fal's current official queue, model-schema and
reliability documentation to pin the exact request/response contract (the repo held endpoint
identifiers but no schemas); implemented the substrate as a new package `eval/pilot-substrate/`
that imports EMP-001's exception semantics rather than copying them; and wrote 59
fake-transport tests covering the required behaviours plus the extra failure modes the async
lifecycle introduces.

**OBSERVED:**
- 59/59 substrate tests pass (`eval/pilot-substrate/tests/`, pytest, 0 network calls — an
  autouse fixture makes any socket attempt raise, and one test proves the fixture bites).
- Binary handling works against bytes that are deliberately invalid UTF-8: exact SHA-256 and
  byte count survive persistence and a JSON round-trip, a `str` payload is refused with
  `TypeError`, overwrites are refused, and a provider-declared file size that disagrees with
  the actual bytes is recorded as a mismatch rather than hidden.
- The EMP-001 distinctions hold under test: no transport → refuse; no guard → refuse; missing
  key → provably pre-dispatch, reservation released, zero calls; any failure after the send —
  submit timeout, malformed reply, poll failure, undocumented queue status — settles the
  reserved estimate conservatively (`billing_state: unknown_provisional`), persists a real
  failed attempt, and dispatches nothing a second time (measured by counting calls).
- Polling never inflates generation counts: 10 polls before completion still record exactly
  one submit, one trial, one settlement.
- fal official docs (fetched 2026-08-28): queue contract is POST `queue.fal.run/{model}` →
  `request_id` → GET `.../requests/{id}/status` (`IN_QUEUE`/`IN_PROGRESS`/`COMPLETED`) → GET
  `.../requests/{id}` → `video.url/content_type/file_name/file_size`; platform auto-retries
  up to 10× unless `X-Fal-No-Retry` is sent; veo3.1 inputs are `prompt`, `aspect_ratio`
  (16:9|9:16), `duration` (4s|6s|8s), `resolution`, `generate_audio`, `auto_fix` (default
  true), `seed`.
- Regression: the EMP-001 suite on this machine gives 550 passed / 20 failed; every failure
  is `TesseractUnavailable` (the pinned EVAL-023 `tessdata` files are not installed locally)
  and pre-exists this branch, which adds files only (plus the `.gitignore` entry).
- **Incident, resolved:** this local clone is shared by the parallel pre-pilot workers.
  CANON-013 and RES-007 commits landed on my checked-out branch mid-task, and the RES-007
  commit here (`2b0e31f`) differs slightly from the one on `work/res-007-pilot-writer`
  (`9cf1dc2`, same message/timestamp; ~10 differing lines in their brief). I re-pointed
  `work/eval-035-video-route` to main's tip and preserved the divergent duplicate on local
  branch `rescue/res-007-duplicate-from-eval-035` rather than adjudicating another stream's
  content. Also: running the documented `render_latin_pack.py` rebuild rewrites the
  **committed** file `text_qualification/perceptibility-mechanical.json` (semantically
  equivalent, reordered keys); I restored the committed bytes.

**INFERRED:**
- fal Veo 3.1 is the right substrate choice *for this infrastructure task*: it is the Wave-1
  VID-01 candidate family (rendered text/logo stability + native audio — the Aight pilot's
  shape) reachable in ONE call rather than a three-route TTS+lipsync composite; the endpoint
  identity is provider-authorised committed evidence (fal's own SDK enumeration); a fal
  per-second price is committed Controller evidence (USD 0.40/s with audio → USD 2.40 for a
  6-second clip); and EMP-001 already proved this exact auth surface with real money. This is
  a route-plumbing judgement, not a model-quality claim.
- Without `X-Fal-No-Retry`, "one call = one trial" would have been false at the platform
  layer no matter how disciplined our code was. The stale-assumption warning in the task was
  earned: nothing in the repository recorded this behaviour.
- The gap the task predicted is real: the V1 harness stores artifacts via text APIs
  (`write_text`/string hashes — `eval/v1/harness/harness.py:226,373`). The substrate does not
  touch the harness; it provides the byte-safe path PILOT-001 should use. Retrofitting the
  harness is a separate decision, not needed for the pilot.

**SURPRISES / BELIEF UPDATES:** The provider-side auto-retry and auto-prompt-rewrite
defaults both silently violate project invariants; current-doc verification before live
calls is not ceremony. The shared-clone parallel-worker collision is a process hazard the
Controller should know about — it produced a divergent duplicate of another stream's commit.

**FAILURES / BLOCKERS:** none blocking this task. The 20 environmental EMP-001 test failures
mean a fresh machine cannot run the Tesseract leg of that suite without the documented
tessdata download; unrelated to video work.

**UNKNOWN / NOT VERIFIED:**
- The live network path (real fal dispatch, real polling cadence, real MP4 download) has
  never run — by design of the USD 0 budget. It stays unproven until the first authorised
  pilot call.
- fal's current live catalogue/schema for veo3.1 beyond the fetched docs (e.g. whether a
  submit-time 422 is ever billed; actual `content_type` served). Conservative accounting is
  used wherever the answer is unknown.
- Fast/lite tier fal prices are not committed evidence; only full-tier ($0.40/s) and lite
  ($0.05/s) figures exist in the pricing decision. The substrate's reservation uses the
  full-tier rate.

**ASSUMPTIONS CHALLENGED:** none in `coordination/ASSUMPTIONS.md` directly; the implicit
assumption "our zero-retry discipline is enforceable client-side alone" is false for fal
without the header, now handled and tested.

**LOCAL IMPLICATIONS:** Eval now has a pilot-callable seam:
`generate_pilot_video(prompt, duration_s, aspect_ratio, out_dir, guard, transport)` — one
route, one trial, one persisted attempt+artifact pair, vocabulary aligned with the existing
attempt/artifact records so RES-007's outcome writer can consume it.

**CROSS-STREAM IMPLICATIONS:** CROSS_STREAM (Resources/RES-007): the artifact record emitted
here (`output_sha256`, `output_bytes`, `output_location`, `media_kind`, route identity,
`provider_request_id`) should be reconciled with the v3 outcome writer's expected shape at
the pilot integration boundary — proposed, not enacted. CROSS_STREAM (coordination): the
rescue branch and the shared-clone collision need a Writer-Controller disposition.

**ARCHITECTURAL IMPLICATIONS:** none.

**DECISIONS NEEDED FROM CONTROLLER:**
1. Accept or change the selected pilot route (`fal-ai/veo3.1`, full tier, native audio,
   720p). Changing tier (fast/lite) is a one-line frozen-table change but needs a committed
   price for reservation.
2. Disposition of `rescue/res-007-duplicate-from-eval-035` (keep RES-007's own branch as
   authoritative and delete the rescue ref, or reconcile the 10-line brief difference).
3. Whether the parallel workers should each use isolated clones/worktrees going forward.

**EVIDENCE WORTH HUMAN INSPECTION:**
- `eval/pilot-substrate/tests/test_failure_modes.py` — read the ambiguity tests; they are
  the money-safety story in executable form.
- `eval/pilot-substrate/README.md` — the contract-provenance table distinguishes committed
  evidence from fetched-today provider docs.

**FILES CREATED / MODIFIED:** created `eval/pilot-substrate/` (README, `video_route.py`,
`artifact_store.py`, `pilot_authorisation.py`, `tests/` — 5 test modules, 59 tests) and this
brief; modified `.gitignore` (one entry for the never-committed pilot authorisation file).
No existing code was modified; EMP-001 semantics are imported, not copied.

**RECOMMENDED NEXT STEP:** Before any live PILOT-001 call: (1) execution-time verification
that `fal-ai/veo3.1` is live with this schema and current price on the funded account;
(2) user-approved pilot spend cap materialised as `authorization.pilot.local.yaml` naming
the authorising decision; (3) a single smallest-possible real dispatch (one 4s clip) as the
first exercise of the untested live path before the pilot brief's real generation. This
sequences the cheapest possible failure of the unproven path ahead of the pilot itself.

**EPISTEMIC CHECK:** Confirmed — provider-contract facts are labelled by source and fetch
date; committed-evidence facts carry their repository paths; the route choice is labelled a
recommendation-grade infrastructure judgement; the live path is stated as unproven; no
number here is invoice evidence.

**CONFIRMATION:** No unapproved next strategic step was started. No paid call, no real
generation, no Registry write, no second provider, no change to Resources-owned contracts.
