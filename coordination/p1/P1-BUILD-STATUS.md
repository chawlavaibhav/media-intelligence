# Media Intelligence P1 — build status and continuation record

Branch `claude/confident-franklin-s1v8ln` (from main `f0ad1fa`). PR #108 (draft). Nothing merged to main; no paid call
made; no cloud resource created. Session 1: cloud, 2026-09-22 (built). Session 2: founder's laptop, 2026-09-23 (below).

**State: implementation-complete milestone reached on the laptop in dry mode (STATE 1, dry).** The media engine runs on real
ffmpeg; image and film jobs complete the whole customer journey over HTTP. NOT reached: real-media validated (needs live spend),
deployed (needs hosting decision), authorised for beta (founder). See §0.

Labels: **TESTED** = exercised by an automated test, with the result shown; **WRITTEN** = code exists and is on the production
path but has not executed; **MISSING** = not built.

## 0. Laptop session 2026-09-23 — what changed, what is proven, what is blocked

**Proven on this Mac (USD 0).** 51 product tests OK (twice); `python3 -m product.smoke` all PASS; `python3 -m product.journey
--dry` PASS for film and image against the running web app + worker: invite → brief + uploads → direction → approval →
production → operator release → preview of the real file → text change → re-release → accept → download (sha256 = accepted
version); a second account gets 404 on the job and its file. Engine overhead approval → verified 30-s cut: ~20 s
(composition 10.6 s, deterministic checks 4.4 s); provider and reasoning time unmeasured until live.

**Defects found by running real media, all fixed with regressions:** ffmpeg `drawtext` absent from Homebrew builds (text now
Pillow/raqm, coverage-aware font choice — Arial Bold has no ₹); supers composed on an opaque black canvas blacked out every
beat under a super while all checks passed (compose rewritten with real alpha; `no_black_frames` added); a half-transparent
plate shipped a washed-out still whose contrast was measured on opaque pixels; 41-px lines judged as "large text"; a heartbeat
race could re-lock a released job for 15 min; recovery of paid in-flight calls depended on detecting a takeover.

**Controller concerns on PR #108.** (1) Every PASS is now evidence on the delivered file: exact copy judged on the strings drawn;
reviewer answers are enums with evidence (silence = NOT_VERIFIED); a review of another file proves nothing (sha-bound);
unmeasurable = NOT_VERIFIED. (2) A permanent test asserts every applicable enforced/reviewer control leaves a row on image and
film deliverables; process controls are proven from the ledger/graph/events. (3) Real media: `audio_joins` calibrated on
MOKOBARA v1/v2 (v1 fails at its two recorded holes, v2 passes); the rejected MDR8 film fails true peak (−0.9 dBTP) — a defect
the atlas never recorded. The reviewer MODEL is not yet qualified: `product/qualification/` runs the product's own reviewer on
MOKO7 v1/v2 against a key from the human checker + customer verdict — needs the spend record below.

**Recovered failure atlas.** `FAILURE-ANALYSIS.md` (~/Documents) and `FAILURE-ATLAS-RAW/CLASSIFIED.yaml` (uncommitted
MOKOBARA-DEEPREAD job folder) committed verbatim in `production-learning/atlas/2026-09-22/`. Totals confirmed: 225 rows,
104 modes, 39 recurring. All 104 modes have one P1 disposition in `product/data/FAILURE-CONTROLS-v1.yaml`
(`atlas_reconciliation`; 44 enforced, 14 reviewer, 12 by construction, 13 human judgement, 10 not applicable, 8 excluded,
2 operator process, 1 deferred: per-customer product dossier). All 50 beta-critical modes have a machine or a named person
behind them (tested). New on the production path: PRODUCT_AND_WORLD_TRUTH_BEFORE_SPEND (a reviewer blocker previously never
stopped a customer approval — now approve() refuses it; override is named and reasoned); audio_heard_by_person (required,
NON-WAIVABLE, a person's recorded listen); PRODUCT_CONTINUITY_ACROSS_SHOTS; approved copy lines must be drawn; frame timing.

**Decisions needed (exact):**
- D1 Spend record for live validation — proposed cap **USD 20**: reviewer qualification on MOKO7 v1+v2 (≤ USD 1), one live
  image job through the UI (≤ USD 4), one live 30-s film job (≤ USD 15; dry quote: providers USD 8.19 incl. one retake per
  clip, reasoning ≈ 2–3). Pools: Gemini API key (stills + reviewer) and Vertex (Veo, Lyria).
- D2 A valid **ANTHROPIC_API_KEY**: the key in ~/.mi-keys returns `authentication_error: API key is invalid`.
- D3 **Vertex credentials** for Veo/Lyria: the product authenticates with a service-account key file + project
  (`MI_VERTEX_SA_JSON`, `MI_VERTEX_PROJECT`); this Mac has only a personal gcloud login. Which project/account is authorised?
- D4 **Hosting**: one small VM (assessment H-3: GCE e2-standard-2 on credits), a DNS name, approval to create it. `deploy/install.sh`
  then runs the smoke test before taking traffic; `product.journey` is the post-deploy end-to-end test.
- D5 A **non-builder reviewer** for the first real outputs, and the founder's beta-release decision.

**Next executable action once D1–D3 land:** `python3 -m product.qualification.qualify_reviewer --film v1 --live` and `--film v2
--live` (confirm the proposed matches by hand; pass mark ≥ 4 of 6 on v1); then one live image job and one live film job
through the web UI with `MI_PROVIDER_MODE=live MI_REASONING_MODE=live`, recording `product.admin metrics --job <id>`.

---

## 1. What exists now (the product in one paragraph)

`product/` is a persistent, invite-only web product in which code holds the job state and LLMs are components.
A customer submits a brief with product photos, logo and exact copy; a strategist call writes the intent record
and asks at most five questions; a creative-director call (with the ten adopted Canon packs injected by the
runtime lookup, plus bounded, logged deep retrieval on request) writes the concept, storyboard, copy deck and
product anchor; an isolated reviewer checks the direction before spend; the customer sees the direction, a
preview frame and a PriceBook quote, and authorises a budget. The orchestrator then builds a dependency graph
(character → stills → riskiest clip first → other clips; music and end card in parallel; supers; assembly),
runs it concurrently through one shared dispatcher (reserve-before-send, atomic attempt ids, classified failures,
crash recovery), composes exact text/logos by code through the compositor gates, runs deterministic checks and an
isolated reviewer on the finished file, and a presentation gateway refuses anything with an unrun or failed check
unless a named person waives it. The customer previews, requests targeted changes (only the affected nodes are
redone), accepts, and downloads the exact accepted version; a production-learning case skeleton is generated.

| Area | Files | Status |
|---|---|---|
| Job store, ledger, leases, events, timings | `product/store.py`, `states.py` | TESTED |
| Orchestrator (5 stages, graph, pauses, revision) | `product/orchestrator.py`, `worker.py` | TESTED (simulated providers/reasoning) |
| Reasoning components + contracts + isolation | `product/reasoning.py`, `contracts.py`, `schema.py` | TESTED with simulated backend; live Anthropic/Gemini transport WRITTEN, never called |
| Canon: ten packs + deep retrieval | `product/canon_access.py` | TESTED (10 packs, 25,095 tokens, 0 gaps on a film job; 1,300 claims indexed) |
| Shared dispatch (nano-banana-2, veo-3.1-fast-i2v, lyria) | `product/providers.py`, `dispatch.py` | ledger/guard/classify/recover TESTED; live HTTP WRITTEN (request shapes byte-for-byte from the Mokobara kit), never called |
| Media engine (compose, end card, supers, assembly, loudness, cuts) | `product/media.py`, `compose.py` | **WRITTEN, NEVER EXECUTED** — no ffmpeg on this host (install declined) |
| Verification + gateway + control register | `product/verify.py`, `data/FAILURE-CONTROLS-v1.yaml` | TESTED (gateway logic, regressions); film/still pixel checks depend on the media engine |
| Web app (customer + operator) | `product/web/` | TESTED (WSGI tests + Chromium render of the direction and review pages) |
| Learning capture + metrics | `product/learning.py` | TESTED (generated case passes `check_case.py`, structural) |
| Deployment kit, backup/restore, smoke | `deploy/`, `product/admin.py`, `product/smoke.py` | backup/restore TESTED; install/systemd/Caddy WRITTEN, never run |

Tests: `python3 -m unittest discover -s product/tests -t .` → **37 tests, OK** (≈7 s, USD 0).
`python3 -m product.smoke` here → dry jobs PASS, backup/restore PASS, **media engine FAIL (ffmpeg absent)**.

Pre-existing, not caused by this branch: `runtime/tests` on main = 493 tests, 12 failures + 101 errors. The
representative cause is `PLANNER_FIXTURE_MISSING`: the 22 Sep ten-pack adoption changed the Canon prefix, so the
recorded planner fixtures (keyed by prompt hash) no longer match. Not fixed here (re-recording needs a model call).

## 2. Decisions taken (engineering; recorded, reversible)

1. **Stack: Python stdlib + PyYAML + Jinja2 (+ `cryptography` for Vertex tokens), SQLite WAL, ffmpeg.** Same
   dependency floor as `runtime/`; one VM; no framework, queue or external DB. The package installs in this
   session were declined, so the web layer is WSGI (wsgiref threading server behind Caddy) and the media
   engine is ffmpeg-only (no PIL/numpy).
2. **Reasoning via raw HTTPS** (Anthropic Messages API; Gemini generateContent) — no SDK dependency, matching the
   job kits' urllib transport. Creative/strategist default `claude-opus-5` (configurable `MI_CREATIVE_MODEL`);
   independent reviewer default Gemini `gemini-3.5-flash` (a different family, and it can take the assembled MP4
   with sound). **The reviewer is not qualified** — see B4.
3. **Budget in two authorisations**: a planning allowance (≤ USD 3, ticked at submission) covers reasoning and
   preview frames; production spend needs the customer's approval of a stated budget ≤ the account ceiling
   (set by the operator). Every provider reservation checks `budget_authorised_by`.
4. **Format adaptations = one plate per format**, not crops of a master (avoids UPWORK-PORTFOLIO-002 SD-HD-06
   subject cropping without building subject-aware crop).
5. **Transient provider failures don't consume the take allowance** (max 2 quality draws per node; 3 transient
   retries per run, then `paused_provider`, auto-retry after 60 s).
6. **Failure register keyed to existing ids**: all 120 defect rows in `production-learning/cases/*/SYSTEM-DEFECTS.yaml`
   are mapped (test enforces full coverage and no invented ids). The 225-row atlas was not found (A7).
7. **Hold before preview on** by default (P1 assessment H-6).

## 3. Execution checklist (Part XIV) — checked only with evidence

Evidence key: `T:` test name in `product/tests/`; `S:` smoke step; `R:` record/file.

**A. Repository and authority**
- [x] Current main and active work inspected — main `f0ad1fa`; open PRs are old eval/audit/canon lanes (#23–#94); no other P1 writer.
- [x] Governing decisions and project contract read — PROJECT-CONTRACT, both 22 Sep Canon decisions, P1 assessment + investigation.
- [x] Production operator and five-stage framework inspected — `.claude/skills/media-agency` (workflow §5–§6, form fields reused in `contracts.py`).
- [x] Ten Canon packs and retrieval verified — `canon_access.practical_packs` injects 10/10, 0 gaps (film job).
- [x] Runtime components and adapters inventoried — reused: canon lookup/normalize, PriceBook, compositor gates, provider_errors, container edit-list check, synthetic media.
- [x] Production-learning cases and archived tools inspected — Mokobara `tools/` (dispatch, _common, assemble, render_text, paintout) read and promoted.
- [x] **Failure atlas: absence recorded** — not on main, fetched job branches, or this machine; totals not claimed (R: FAILURE-CONTROLS-v1.yaml header).
- [x] Branch and change boundaries established — new `product/`, `deploy/`, `coordination/p1/`; `runtime/`, `canon/`, cases untouched.

**B. Customer product** (all through the real web app, simulated media)
- [x] Authenticate (invite → password → session) — T: test_web.
- [x] Create a job — T: test_customer_can_submit_approve_and_see_every_stage_page.
- [x] Upload product/brand assets (type-sniffed, size-limited, script-SVG refused) — T: test_unsupported_upload_types_are_refused.
- [x] Simple or detailed brief — T: Clarification (one line) / FilmJourney (detailed).
- [x] Answer clarification questions — T: Clarification.
- [x] Review and approve direction — T: test_web; Chromium screenshot of the direction page.
- [x] Authorise a production budget — T: test_web (approve with budget).
- [x] Monitor progress — rail + auto-refresh page (screenshot); no provider internals (T: asserts no route names on the page).
- [ ] Preview **actual completed media** — the page plays/shows the file, but no real media has been produced (B1–B2).
- [x] Request targeted changes — T: FilmJourney (beat), copy change, concept change.
- [x] Accept or reject — T: test_web, FilmJourney.
- [x] Download the approved media (only the accepted version) — T: test_web.
- [x] Persists across session and worker interruption — T: WorkerCrash; store is the only state.

**C. Creative intelligence**
- [x] Original brief preserved unchanged — frozen + fingerprinted; T: test_the_original_brief_is_frozen_and_fingerprinted.
- [~] Valid normalized request — the runtime NR is built for the Canon lookup; the intent record is schema-validated. Live model output **not yet seen**.
- [~] Mandatory requirements/acceptance extracted — contract + deterministic floor (exact strings always mandatory); live quality unmeasured.
- [x] Material ambiguity resolved before spend — `needs_answers` before any provider attempt; T: Clarification.
- [~] Verified facts vs assumptions — contract separates `product.facts` / `assumptions`; live behaviour unmeasured.
- [x] Relevant Canon packs retrieved automatically — ten packs; trace artifact per job.
- [x] Deeper Canon on request — `knowledge_requests` → bounded retrieval (≤12 claims), ids logged `retrieved_by: model_request`. Ranking **not** measured with `canon_done` coverage.
- [x] Retrieved knowledge traceable to decisions — `canon_consulted[{id, decision}]` stored and shown on the operator page.
- [ ] Appropriate creative concept — needs live runs and human verdicts.
- [ ] Storyboard executable — contract encodes the Mokobara clip grammar; unproven live.
- [x] Mandatory actions have observable verification — `observable_as` per item; reviewer answers each; gateway blocks otherwise.
- [x] Continuity requirements established — character reference node feeds every beat still; `continuity` per beat.
- [x] Independent creative review before spend — isolated `direction_reviewer`; one revise loop on blockers.
- [x] Approved decisions preserved — direction versioned; revisions change only routed parts; T: copy change keeps pictures.

**D. Production intelligence**
- [x] Blueprint → asset dependency plan — T: FilmJourney (graph deps).
- [~] Route capability vs requirements — fixed P1 route table with taint-register evidence noted; no per-request capability matching beyond it.
- [x] Consequential action qualified first — riskiest beat's clip gates all other clips; failed qualification stops dependent spend.
- [x] Cost and repair allowance estimated — quote from PriceBook incl. one re-take per asset.
- [x] No paid request without authorisation — T: NoSpendWithoutAuthorisation.
- [x] Unique atomic attempt ids — T: ConcurrentReservation (40 threads).
- [x] Budget enforced across concurrent attempts — same test (never crosses cap).
- [x] Independent assets concurrent — thread pool over ready nodes.
- [x] Dependents wait for approved references — graph deps (stills ← character; clips ← stills).
- [x] Provider errors classified correctly — T: FailureClassification.
- [x] No duplicate attempts/untracked charges on interruption — T: WorkerCrash, Recovery.
- [x] Records reconcile — ledger integrity check on every presented file. Reconciliation to provider consoles: not possible without live runs.
- [x] Job-specific tooling uses common services — no per-job tools exist in the product path.

**E. Media execution and verification**
- [ ] P1-IMG end to end on a real brief — blocked (B1, B2).
- [ ] P1-VIDEO end to end on a real 30 s brief — blocked (B1, B2).
- [~] Exact text and brand marks preserved — code-set via textfile + EXACT_COPY_MATCH (T); pixel rendering unexecuted.
- [x] Generated assets checked against source requirements — inspector per still/clip against its instruction (live quality unmeasured).
- [~] Product/character continuity evaluated — inspector + reviewer obligations; unmeasured.
- [~] Mandatory physical actions verified in media — reviewer obligation, gateway-enforced; unmeasured.
- [~] Completed video independently reviewed — reviewer receives the MP4 with sound (Gemini); never run live.
- [~] Actual audio evaluated — AUDIO_REVIEWED_BY_EAR is NOT_VERIFIED unless the reviewer evaluated audio; T: live-review-without-audio test.
- [~] Technical checks on the actual deliverable — written (edit lists, loudness/true peak, joins, in-model cuts); unexecuted (B1).
- [x] Applicable historical-failure checks run on the pathway — register + gateway; T: ControlRegister.
- [x] Unexecuted checks cannot pass — T: UnrunCheckBlocks, simulated review never passes, sha mismatch.
- [x] Defective historical asset triggers the check — T: HistoricalRegressions (DF-9 contrast, A-004 D-1 edit lists, V2 N1 hero, Lane A D-11 colour, exact price, rejected reuse). Audio-join (DF-10) regression needs ffmpeg.
- [x] Documented corrected asset passes — same tests (black wordmark, remuxed file, clear layout, correct colour/price).
- [x] Job scripts cannot bypass the gateway — only `accept`/`release_hold` present, both re-run the gateway.
- [x] Residual defects and exceptions recorded — waivers with person + reason per check per file version.
- [x] Repair reruns only necessary work — T: FilmJourney, copy change.
- [x] Acceptance applies to the exact version — deliveries store asset id + sha256.

**F. Reliability and security**
- [x] Survives worker restart mid-job — T: WorkerCrash.
- [x] Provider failure injection recoverable — T: ProviderFailureInjection (both).
- [x] Budget exhaustion pauses without exceeding cap — T: BudgetExhaustion.
- [x] Resumes after authorised increase — same.
- [x] Unsupported requests caught before spend — T: Refusal (live strategist behaviour unmeasured).
- [x] Cross-account isolation — T: test_another_account_cannot_see_the_job_or_its_files…
- [x] Credentials not exposed — read by name, scrubbed from stored errors; never in prompts/pages. (No secret was present in this session.)
- [x] Customer media outside the repo — `.mi-data/` gitignored; cases written under the data dir.
- [x] Backups and recovery tested — S: backup and restore (integrity ok, all asset files present). Off-host copy untested.
- [x] Customer approval required for delivery — download only after accept.
- [ ] Deployed workflow without terminal intervention — not deployed (B3).

**G. Production time and learning**
- [x] Stage timings captured automatically — `timings` table, per phase.
- [x] Provider latency separated — `provider` phase.
- [x] Customer waiting separated — `customer_wait` phase.
- [x] Parallel work not double-counted — union vs sum; T: Learning asserts elapsed ≤ accumulated.
- [ ] First-cut latency on actual production — instrumented (`approved_at → first_cut_at`); no real run.
- [x] Actual cost includes failed attempts and repairs — ledger; T: FailureClassification, metrics.
- [x] Historical engineering failures don't need manual debugging — attempt-id race, retry, edit lists, joins, true peak are code.
- [x] Final acceptance/rejection recorded — deliveries/feedback/events.
- [x] Completed job generates a learning record — T: Learning (`check_case.py` PASS, structural).
- [x] No automatic promotion — PROMOTION-QUEUE empty; routing_authority none.
- [ ] Effect of controls on latency/escape rate measured — needs live jobs.

## 4. Blockers — each with the exact decision or access needed

- **B1 — media engine unexecuted.** Needs a host with ffmpeg + rsvg-convert + fonts. Either allow
  `apt-get install ffmpeg librsvg2-bin fonts-dejavu-core fonts-noto-core` in a session, or run `deploy/install.sh` on
  a VM (its smoke step exercises the engine end to end). Expect first-run fixes in `media.py`/`compose.py`.
- **B2 — no live generation or reasoning has run.** Needs a founder-stated validation cap (assessment H-5 proposed
  USD 40 provider + a token ceiling) and credentials on the host: `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, Vertex
  service-account file + project (credits pools only).
- **B3 — no deployment.** Needs the founder's hosting decision (assessment H-3: one GCE VM on credits), DNS name,
  and approval to create it.
- **B4 — reviewer not qualified.** The independent reviewer/inspector (Gemini default) has no qualification evidence
  in this repo; its Gemini token price is a placeholder (`MI_PRICE_GEMINI_3_5_FLASH` to set). Until qualified on the
  Mokobara v1 defects (assessment T2.4: find ≥4 of 6), keep `MI_HOLD_BEFORE_PREVIEW=1` so a person looks at every cut.
- **B5 — human verdicts.** STATE 2/3 require non-author accepted outcomes for both classes and the founder's release decision.

## 5. Not built (known gaps, none hidden)

- Email notifications (customer learns state from the page only).
- A one-command customer-data purge (runbook gives the manual procedure).
- Per-request capability matching beyond the fixed P1 route table; voice-over stays refused.
- Coverage measurement of the deep-retrieval ranking against `HAND-RETRIEVED-CLAIMS.yaml`.
- Re-recording the runtime planner fixtures broken by the Canon adoption.

## 6. Next executable task

**Run the media engine for the first time and fix what breaks.** On a host with ffmpeg (B1):
`PYTHONPATH=. python3 -m product.smoke`. Acceptance: all three smoke steps PASS; the composed still passes every
compositor gate; the assembled film probes 1080×1920 at the planned duration; `film_checks` PASS (edit lists,
−14±2 LUFS / ≤ −1 dBTP, joins ≤ 12 dB). Files: `product/media.py`, `product/compose.py`, `product/verify.py`.
Then: first live micro-run under an authorised cap (one P1-IMG job through the web UI), then one P1-VIDEO job,
recording first-cut latency and cost from `product.admin metrics --job <id>`.
