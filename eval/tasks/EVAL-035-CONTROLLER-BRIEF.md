# Controller Brief — EVAL-035 (third pass: RES-007 integration correction)

**TASK:** EVAL-035
**STATUS:** completed (third implementation pass, under
`CONTROLLER-EVAL-035-RETURN-REVIEW-2-2026-08-28.md`; route authority
`CONTROLLER-DIRECT-GEMINI-T1-ROUTE-REVISION-2026-08-28.md`)

**HUMAN SUMMARY:** This is the **third pass** on EVAL-035, and it exists because the
second pass had a defect its own 78 green tests could not see: EVAL-035 claimed its
records were compatible with Resources' journey writer by checking them against a
**hand-maintained field list** instead of the real thing. That list was wrong in one place
(it passed `storage_class`, which the real writer refuses) and, worse, the method could
not catch drift at all — a list that claims to be someone else's interface is a mock
wearing a contract's clothes. The fix is structural, not cosmetic: the acceptance test now
**imports the actual merged Resources writer from `main`, feeds it EVAL-035's real cost
and attempt handoffs, records the real binary artifact, and runs the actual merged
topology validator over the resulting journey — for both a successful generation and a
preserved ambiguous failure — plus a negative control proving the validator run can
fail.** If Resources' interface ever changes incompatibly, these tests break loudly, which
is exactly their job. The second review also found that live spend still rested on an
in-memory budget object — the same per-process-ceiling mistake EMP-001 already paid to
learn, and one that produced no durable cost reference for Resources to resolve. The
pilot now has its own **append-only, on-disk spend ledger**: reservations are persisted
before dispatch, count against the cap, settle under a stable cost identity, survive a
real process restart (proven with a second OS process, not a second Python object), and
any corruption fails closed. Spend authority itself is unchanged and still closed: no
committed Controller decision authorises pilot spend, and tests prove the repository
state cannot open a live runtime. No provider was contacted; USD 0 spent.

**WHAT I DID:** Confirmed the merged RES-007 on `main` (hard precondition), read the
merged `outcome_writer.py` and `validate_topology_v3.py` as the interface authority,
rebased the branch onto that `main`, re-verified the official Gemini/Veo contract and
price, removed the copied field list and the `storage_class` writer kwarg, built the
persistent PILOT-001 spend ledger on EMP-001's accepted durable-ledger precedent (without
touching EMP-001's frozen constants or history), wired the route's cost settlement to
emit a writer-ready immutable cost row sharing the attempt's `cost_ref`, and wrote the
real-writer/real-validator integration tests and the persistent-spend test matrix.

**OBSERVED:**
- **Baseline:** merged RES-007 present on `main` at start (`745f43c`, writer commit
  `85f3a4d`, G12 correction included). Branch rebased onto it; at completion the branch is
  `behind_by: 0` against `origin/main` (re-fetched before returning).
- **103/103 substrate tests pass**, zero network (socket-blocking autouse fixture with
  its own sanity test; `GEMINI_API_KEY` stripped from the test environment).
- **Primary acceptance test result: PASS.** The successful path — fake Gemini transport →
  route → persistent ledger reservation/settlement → `res007_cost_ledger_entry` →
  **actual merged** `OutcomeWriter.add_ledger_entry` → **actual merged**
  `record_attempt(step_id=…, **handoff)` → **actual** `record_artifact` from the real
  bytes → `write_archive` → **actual merged** `validate_topology_v3.py` (subprocess,
  exactly as RES-007's own tests invoke it) → **exit 0**. The archive's single attempt,
  single ledger row and the route outcome share one `cost_ref`; the writer's recomputed
  artifact hash equals the route's persisted SHA-256.
- **Failure-side integration: PASS.** An ambiguous submit timeout flows through the same
  real chain: non-ok status, non-empty `error_detail`, `completed_at: null` (genuinely
  unresolved), no artifact (and a test proves the merged writer itself refuses one),
  conservative immutable cost row, validator exit 0. A negative control (attempt stripped
  of `prompt_hash`) makes the validator exit 1, proving the subprocess judgement is real.
- **Persistent spend results:** reservation on disk before dispatch; pending counts
  against the cap; committed+pending can never exceed the cap; `cost_ref` stable from
  reservation through settlement; pre-dispatch refusal releases exactly its own
  reservation as a new record; ambiguous dispatch settles conservatively and keeps
  headroom consumed; **a real second process (subprocess) reopening the same run sees
  committed 0.80 / pending 0 — never zero**; malformed line, sequence gap, in-process
  truncation, unknown record type, missing run record and run-vs-authority ceiling drift
  all raise `LedgerCorrupt`.
- **Spend authority unchanged and closed:** the persistent runtime opens only behind
  `verify_authority` (committed `machine_authorisation` block + matching local file);
  tests prove the real repository state cannot open a live runtime and that no run
  directory is even created on refusal.
- **Gemini contract re-verified at execution time** (official `ai.google.dev` docs +
  pricing, fetched 2026-08-28, this pass): model `veo-3.1-fast-generate-preview` listed;
  `POST /v1beta/models/{model}:predictLongRunning`, `x-goog-api-key`; durations 4|6|8 s;
  16:9|9:16; 720p default; poll `GET /v1beta/{operation.name}` to `done`; result at
  `generateVideoResponse.generatedSamples[0].video.uri`; authenticated download; 2-day
  retention; native audio; blocked videos documented as not charged. **Price unchanged:
  Veo 3.1 Fast 720p USD 0.10/generated second with audio** — provisional planning rate,
  and every emitted cost row's basis text says so explicitly ("not invoice evidence").
- No remaining fal reference in executable code (prose history only). No mocked or copied
  Resources interface remains anywhere in the package.

**INFERRED:**
- The recurrence-prevention is the test architecture itself: EVAL-035 now has no private
  belief about Resources' contract to go stale — the merged writer and validator are
  executed, so incompatible drift surfaces as a natural test failure on either side's
  branch.
- The prior "78 tests green" result is a caution worth keeping: unit coverage of one's
  own code proves nothing about a cross-stream boundary. Only calling the counterpart's
  production code does.

**SURPRISES / BELIEF UPDATES:** none beyond the above; the merged writer accepted the
corrected handoff on the first integration run once `storage_class` was removed, which is
consistent with the review's diagnosis that it was the single blocking kwarg.

**FAILURES / BLOCKERS:** none blocking. (Known environmental Tesseract failures in the
wider EMP-001 suite persist on this machine; unrelated.)

**UNKNOWN / NOT VERIFIED:**
- The live network path — real dispatch, operation cadence, blocked-video response shape,
  operation error vocabulary, served content type, actual billed amounts — remains
  unproven at USD 0 and must be verified at execution time before PILOT-001, including
  re-verifying the `-preview` model identifier and price on the funded account.
- File-locking is `fcntl`-based (this platform); cross-machine concurrency is out of
  scope for a single-operator pilot.

**ASSUMPTIONS CHALLENGED:** none in `coordination/ASSUMPTIONS.md`.

**LOCAL IMPLICATIONS:** PILOT-001's integration burden is now one pass-through:
`add_ledger_entry(**res007_cost_ledger_entry(outcome))` then
`record_attempt(step_id=…, **res007_production_attempt(outcome)["writer_fields"])`, with
the persistent runtime supplying the durable `cost_ref`.

**CROSS-STREAM IMPLICATIONS:** none pending — the boundary is now proven against merged
Resources code, not proposed. Any future Resources interface change will surface here as
a failing integration test, which is the intended coupling.

**ARCHITECTURAL IMPLICATIONS:** none.

**DECISIONS NEEDED FROM CONTROLLER:**
1. Accept the third pass and route EVAL-035 to bounded Level-1 Governor review.
2. When pilot spend is eventually approved, the approving decision must carry the
   `machine_authorisation` block (format in `pilot_authorisation.py`); the persistent
   runtime then opens against it with the run ceiling bound to that authority.

**EVIDENCE WORTH HUMAN INSPECTION:**
- `eval/pilot-substrate/tests/test_res007_integration.py` — the whole point of this
  pass: real writer, real validator, success + preserved failure + negative control.
- `eval/pilot-substrate/tests/test_pilot_spend_ledger.py` — restart continuity proven
  with a second OS process.

**FILES CREATED / MODIFIED:** added `pilot_spend_ledger.py`,
`tests/test_pilot_spend_ledger.py`, `tests/test_res007_integration.py`; modified
`video_route.py` (cost-record emission, handoff without `storage_class`/field list,
`res007_cost_ledger_entry`), `pilot_authorisation.py` (`verify_authority` replaces the
in-memory guard opener), `tests/conftest.py`, `tests/test_provenance_res007.py`,
`tests/test_auth_and_gating.py`, `README.md`, this brief. EMP-001 and Resources files
untouched.

**RECOMMENDED NEXT STEP:** Level-1 Governor review. The pre-PILOT-001 gates are
unchanged: Aight asset package, frozen brief/acceptance record, execution-time
route/price verification on the funded account, and the user-approved spend cap recorded
as committed machine-verifiable authority. Per the standing Controller disposition, the
first paid call is a real production shot — no smoke tranche.

**EPISTEMIC CHECK:** Confirmed — the integration claims name the exact merged files and
their invocation form; the prior pass's defect is stated plainly rather than reframed;
cost rows are labelled modelled/conservative, never invoice truth; live-path unknowns are
listed; no authority was created.

**CONFIRMATION:** No unapproved next strategic step was started. Real provider calls: 0.
Spend: USD 0. Generations: 0. Registry writes: 0. Resources contracts unchanged.
