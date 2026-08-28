# Controller Brief — EVAL-035 (correction pass)

**TASK:** EVAL-035
**STATUS:** completed (correction pass under
`CONTROLLER-EVAL-035-RETURN-REVIEW-2026-08-28.md`, route superseded by
`CONTROLLER-DIRECT-GEMINI-T1-ROUTE-REVISION-2026-08-28.md`)

**HUMAN SUMMARY:** The first-pass video substrate talked to Google's Veo model through fal,
an aggregator. The Controller and user ruled that for Google models this project calls
Google directly, so the fal execution path was **superseded by infrastructure policy** and
has been replaced: the substrate now talks to the **direct Gemini Developer API** with the
`GEMINI_API_KEY` credential, using the exact model identifier
**`veo-3.1-fast-generate-preview`**. Everything the first pass got right survives — one
generation request is one recorded trial, waiting-room polling never multiplies that count,
the returned video is stored as exact fingerprinted binary bytes, money can only move
behind a budget guard, and any failure after a request may have reached Google is charged
conservatively and never retried. Two review defects are also fixed: the **spend gate is
now mechanically real** (a locally written file can no longer manufacture authority by
pointing at any existing decision — a committed Controller decision must carry an explicit
machine-readable authorisation block, and none does, which a test proves), and every
attempt now carries the **full production provenance the corrected RES-007 writer
requires**, with a ready-made handoff so PILOT-001 needs no field translation. No money
was spent and no provider was contacted; the live network path remains unproven until the
first authorised pilot call, which per Controller decision should be a real production
shot, not a throwaway smoke test.

**WHAT I DID:** Re-read the changed authority (CONTROL-STATE, the return review, the
direct-Gemini decision, the RES-007 correction and its corrected writer interface);
verified the current official Google documentation for the Veo 3.1 Fast contract
(endpoint, request schema, long-running-operation lifecycle, download, retention, safety
behaviour, price); replaced the fal transport/route/tests with the direct Gemini
equivalents while keeping the provider-neutral pieces (binary artifact store, EMP-001
ambiguity semantics, fake-transport patterns); rebuilt the spend gate as a two-document
chain (committed machine-verifiable Controller authority + matching local runtime file);
added the RES-007 production-attempt adapter; rebased the branch onto current `main` and
reverted the first pass's root `.gitignore` edit in favour of a task-local ignore file.

**OBSERVED:**
- **78/78 substrate tests pass** (`eval/pilot-substrate/tests/`, pytest; zero network — an
  autouse fixture makes socket use raise and strips `GEMINI_API_KEY`; one test proves the
  fixture bites). Regression: the EMP-001 machinery this package imports
  (budget guard, transports, ambiguous dispatch) passes 76/76 on this machine.
- **Current official contract** (ai.google.dev, fetched 2026-08-28): model
  `veo-3.1-fast-generate-preview`; `POST /v1beta/models/{model}:predictLongRunning` with
  header `x-goog-api-key`; body `instances[{prompt}]` +
  `parameters{aspectRatio, durationSeconds, resolution}`; durations 4|6|8 s; aspects
  16:9|9:16; 720p (1080p/4k need 8 s); audio is native with **no audio request
  parameter**; poll `GET /v1beta/{operation.name}` until `done`; video at
  `response.generateVideoResponse.generatedSamples[0].video.uri`; download authenticates
  with the same header; **server retains the file 2 days only**; safety filters sometimes
  block a generation and Google documents blocked videos as **not charged**.
- **Current price evidence:** official Gemini API pricing page (fetched 2026-08-28): Veo
  3.1 Fast 720p = **USD 0.10 per generated second, audio included** → an 8 s clip reserves
  USD 0.80. Status: provisional published rate for reservation sizing; not invoice
  evidence; execution-time re-verification still required.
- **fal removal:** no `FAL_KEY`, `fal.run`, `X-Fal-*` or `fal-ai/` reference remains in
  any executable file; fal appears only in prose recording the supersession.
- **Spend gate result:** tests prove the current committed repository state cannot open a
  paid PILOT-001 guard; a perfectly-formed local YAML is refused (no committed
  `machine_authorisation` block exists); pointing at an existing non-authorising decision
  is refused; defective committed blocks (string-true, wrong tranche, nonzero retries,
  zero cap, missing approver) are each refused with their specific reason; two valid
  committed authorities are a conflict, not a choice; a local ceiling above the committed
  cap is refused. The positive path is proven only against a synthetic decisions
  directory, never the repository.
- **One-call-one-trial result:** ten polls still record one submit, one trial, one
  settlement; a transport that would succeed on a second call never receives one; ambiguous
  submit/poll/result/download failures settle at the reserved estimate
  (`unknown_provisional`), persist the attempt, and dispatch nothing again.
- **Binary result:** deliberately invalid-UTF-8 MP4-shaped fixtures round-trip with exact
  SHA-256 and byte count; `str` payloads are refused; artifacts are immutable; provenance
  survives JSON round-trips.
- **RES-007 handoff result:** `res007_production_attempt()` emits the corrected writer's
  exact production field set (verified against `work/res-007-pilot-writer`'s
  `record_attempt` signature and G12 gate: status vocabulary, lane `native_av`, explicit
  `completed_at` that is None only for genuinely unresolved calls, `error_detail` on
  non-ok, `reference_asset_hashes` as an empty list, repeat/retry pinned to first-attempt
  values) — and **no `eval_item_id`** anywhere on a production attempt. Provider extras
  (operation name, raw status, artifact URI, poll count, billing state) ride in a separate
  mapping because the corrected writer refuses unknown fields.
- The request-config file written next to the artifact is hash-bound
  (`config_hash` = SHA-256 of its bytes) and complete enough to reconstruct the exact
  request; `prompt_hash` binds the exact prompt.

**INFERRED:**
- The blocked-video representation (`raiMediaFilteredCount`/`raiMediaFilteredReasons`) is
  documented by Google on the sibling Vertex surface for the same response type; the
  Gemini-API page confirms blocking happens but does not show the fields. The substrate
  reads them only if present and never interprets their absence — the conservative
  handling stands even if the field names differ live.
- Google documents blocked videos as unbilled, but the ledger still settles refusals at
  the reserved estimate: a conservative overstatement is correctable by billing evidence;
  an optimistic release is not. This slightly overstates spend against the pilot cap in
  refusal scenarios.

**SURPRISES / BELIEF UPDATES:** none material this pass. The direct surface is simpler
than fal's (no platform retry or model-fallback mechanisms to suppress), which removes two
whole classes of silent-identity risk the first pass had to defend against.

**FAILURES / BLOCKERS:** none blocking. The broader EMP-001 suite still carries the known
environmental Tesseract-model failures on a fresh machine; unrelated to this task.

**UNKNOWN / NOT VERIFIED:**
- The live network path (real dispatch, real operation cadence, real download) has never
  run — by design at USD 0. The `-preview` model id may be renamed or retired; route,
  schema and price must be re-verified at execution time (CONTROL-STATE next-gate item).
- Actual billed amounts, the live blocked-video response shape, and the operation's error
  vocabulary are unverified until a real call.
- Whether the served download `Content-Type` is exactly `video/mp4` live; an unexpected
  type is recorded, not guessed away.

**ASSUMPTIONS CHALLENGED:** none new.

**LOCAL IMPLICATIONS:** Eval's pilot seam is unchanged in shape
(`generate_pilot_video(...)`) but now returns attempts already speaking the corrected
production vocabulary, so the pilot's journey recording is a direct pass-through.

**CROSS-STREAM IMPLICATIONS:** CROSS_STREAM (Resources): the handoff was aligned to the
corrected writer on `work/res-007-pilot-writer` as of `068f235`; if RES-007's final merged
interface changes further, the adapter (one function) is the only touch point — proposed
integration check at the pilot boundary, not enacted here.

**ARCHITECTURAL IMPLICATIONS:** none.

**DECISIONS NEEDED FROM CONTROLLER:**
1. Accept the corrected EVAL-035 for bounded Level-1 Governor review (the review gate the
   return-review decision names).
2. When pilot spend is eventually approved, the approving decision must carry the
   `machine_authorisation` YAML block this substrate verifies (format documented in
   `pilot_authorisation.py`); without it the gate stays closed by design.

**EVIDENCE WORTH HUMAN INSPECTION:**
- `eval/pilot-substrate/tests/test_auth_and_gating.py` — the spend-authority tests are
  the correction's core: read
  `test_current_committed_repository_state_cannot_open_a_paid_guard`.
- `eval/pilot-substrate/tests/test_provenance_res007.py` — the RES-007 boundary in
  executable form.

**FILES CREATED / MODIFIED:** rewrote `video_route.py` (direct Gemini/Veo),
`pilot_authorisation.py` (machine-verifiable chain), `README.md`, `tests/conftest.py` and
all test modules; added `tests/test_provenance_res007.py` and a task-local
`eval/pilot-substrate/.gitignore`; reverted the first pass's root `.gitignore` change;
`artifact_store.py` preserved unchanged (provider-neutral). EMP-001 code untouched
(semantics imported, not copied).

**RECOMMENDED NEXT STEP:** Level-1 Governor review of this branch. Before any live
PILOT-001 call: execution-time verification of model id/schema/price on the funded
account, the Aight asset package, the frozen pilot brief/acceptance record, and a
Controller decision carrying the machine-verifiable spend block after explicit user
approval. Per Controller disposition, the first paid call should be a real PILOT-001
production shot chosen so an early transport failure is still useful pilot evidence — no
separate smoke tranche.

**EPISTEMIC CHECK:** Confirmed — provider-contract facts are labelled with source and
fetch date; the one cross-surface field-name inference is labelled as such; the live path
is stated as unproven; no number is presented as invoice evidence; no authority was
created.

**CONFIRMATION:** No unapproved next strategic step was started. No paid call, no real
generation, no Registry write, no second provider, no spend authority created, no
Resources-owned file modified.
