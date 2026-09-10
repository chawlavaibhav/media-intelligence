# Audit brief — media-intelligence, whole project — issued by the Controller, 10 Sep 2026

You are the **Auditor**. Your job is to audit the whole `media-intelligence` project — the Canon workstream, the
Capability Lab (EVAL-040..043), the harness, the spend, the governance — and to report what is true, what is claimed
but not evidenced, what is broken, and what the Controller should decide next. You do not fix, you do not spend, you do
not judge media. You read, re-compute, and report.

## 1. Ground rules (hard)

1. **Read-only.** Do not edit, delete, move or regenerate anything under the repository except your own report under
   `coordination/audits/`. Never touch `eval/experiments/**` (sealed evidence, write-once) or any `authorization*.local.yaml`.
2. **No spend, no model call.** Do not run `run_live.py execute/smoke`, `qualify_screen.py` without `--dry-run`, or any
   script that contacts a provider. Dry-run, `status`, `validate_registry.py`, `evidence_map.py`, the unit tests and
   `registry_rows.py` without `--write` are allowed.
3. **Keys by name only.** Key files exist (below); you may `grep -c` a NAME to confirm presence. Never print, copy, hash
   or quote a key value. If a value appears in any file or log you read, report the path and stop reading it.
4. **Cloud identities.** Azure subscription `d3ee8dc2-…` is Wherehouse production — **never** run anything against it
   (it is the `az` default; every `az` call must pass `--subscription b832f4a1-…`, the getaight tenant). AWS account
   `528730633804` (claude-aight) and GCP project `vertexaiproject-507518` are the programme's credit accounts.
   You have no reason to call any cloud API in this audit; if you must list a resource, read-only only.
5. Report facts with file paths and line numbers or commit hashes. A claim you cannot tie to a file is a finding
   ("unsupported"), not a fact.

## 2. Where everything is

- **Repository**: `https://github.com/chawlavaibhav/media-intelligence` (private). Main checkout
  `/Users/vaibhavchawla/Vaibhav_Personal_Projects/media-intelligence` (branch `main`). The Capability Lab was run from the
  worktree `/Users/vaibhavchawla/Vaibhav_Personal_Projects/media-intelligence-wt-controller` (branches `work/eval-04x-*`,
  all merged: PR #91, #92, #93; the merge commit on main is `dcfa6af`). Other worktrees under
  `…/media-intelligence-worktrees/` and `…/media-intelligence-canon-*` belong to the Canon workstream and earlier
  EVALs; do not check them out or reset them. Run every command from the main checkout at `main`.
- **Governance**: `coordination/CONTROL-STATE.md` (the state of record; the "Audit index" paragraph summarises the two-day
  run), `coordination/RUNBOOK.md`, `coordination/PROJECT-CONTRACT.md`, `coordination/DECISION-LOG.md`,
  `coordination/decisions/` (every Controller decision and every spend authorisation record, each quoting the Controller's
  words), `governance/`, `PROJECT-MEMORY.md`.
- **Plan**: `coordination/plans/2026-09-05-CAPABILITY-LAB-CAMPAIGN-v1.md`;
  direction record `coordination/decisions/CONTROLLER-CAPABILITY-LAB-DIRECTION-2026-09-05.md`.
- **Frozen package (generated)**: `eval/empirical-planning/STAGE-A-FREEZE-2026-09/` — `TEST-CASES.yaml`, `COST-TABLE.yaml`,
  `BLUEPRINTS/*.blueprint.md`, `ELIMINATION-RULES.md`, `tools/build.py` (+ `routes.py`, `cases_*.py`) which generates the
  package from `eval/empirical-planning/ROSTER-REFRESH-2026-09.yaml`; price pins (fetched vendor bytes + sha256 + quotes)
  under `eval/empirical-planning/price-pins-2026-09/`.
- **Harness**: `eval/harness-v2/` — `run_live.py` (plan/smoke/execute/status/fixtures), `ledger.py` (caps by pool),
  `pricing.py`, `surfaces.py` (route registry), `adapters/` (fal_queue, vertex_veo, vertex_lyria, gemini_api_image,
  gemini_api_omni, vertex_*, sarvam_tts, elevenlabs_direct), `transports.py` (the only module with network imports),
  `store.py` (sealed write-once store), `judging_packet.py`, `composite.py`, `stack_audio.py`, `registry_rows.py`,
  `evidence_map.py`, `qualify_screen.py`, `instruments/` (`format_probe`, `ledger_metrics`, `repeat_consistency`,
  `registry_gate`, `vlm_screen`, `PASS-CRITERIA-v0.yaml` frozen v1, `SCREEN-QUALIFICATION-CRITERIA-v0.yaml` unfrozen),
  `tests/` (326 tests; run `cd eval/harness-v2 && python3 -m unittest discover -s tests -p 'test_*.py'`),
  `DRY-RUN-MANIFEST-2026-09.yaml`, `README.md`, `authorization.example.yaml`.
- **Evidence**: `eval/experiments/EVAL-040/runs/<run_id>/` — `PLAN.yaml` + `PLAN.sha256`, `artifacts/` (`*.request.json`,
  `*.attempt.json`, `*.record.json`, `media/`), `ledger/`, `instruments/`, `RUN-STATE.json`, `RUN-LOG.jsonl`,
  `judging*/` (blind copies, `MAPPING.json`, `VERDICTS.yaml`), `RESULTS.yaml` (reveal), `SCREEN-RESULTS.yaml` (judge),
  `INPUTS.yaml`. Runs: img-r1, img-r1-redo, img-r1-composite, half2(-fixtures/-smoke), topo3-plates, topo3-video,
  topo3-nb-plates, topo3-nb-video, vid-knee, vid-ms, vid-i2v, vid-ref, vid-2spk, vid-2spk-kling, vid-t2v, vid-wan2,
  vid-wan2-i2v, aud-tts-sarvam, aud-tts-eleven, aud-music-lyria, aud-lip (+ their `-smoke` runs).
  Summaries: `runs/img-r1/IMAGE-ROUND-1-SUMMARY.md`, `runs/half2/IMAGE-HALF-TWO-SUMMARY.md`,
  `runs/topo3-video/VIDEO-PIECE-1-SUMMARY.md`, `EVAL-040/DAY-2-SUMMARY-2026-09-09.md`,
  `EVAL-040/QUALIFICATION-REPORT-2026-09-09.yaml`, `EVAL-040/fixtures/STAND-IN-SPEC.yaml`.
- **Outputs**: `eval/registry/registry-v1.jsonl` (575 deterministic rows) + `SCHEMA-v1-draft.yaml` + `validate_registry.py`;
  `eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml` (61 cells, rules RR-1..RR-16, four tiers);
  `eval/empirical-planning/ROUND-TWO-STILLS-SIZING-2026-09-09.md`; `eval/historical-priors/media-factory-v1/`.
- **Canon workstream**: `canon/` (CANON-SHAPE-v1.md, packs, gate CANON-GATE-001), `coordination/CANON-003-*-AUDIT.md`,
  decisions `coordination/decisions/CONTROLLER-CANON-GATE-001-*`.
- **Off-repo (names only)**: `~/.mi-keys` exports `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `FAL_KEY`, `GOOGLE_CLOUD_VISION_API_KEY`,
  `SARVAM_API_KEY`, `ELEVENLABS_API_KEY`; `~/.aight-litellm-keys/vertex-sa.json` (Vertex service account, GCP);
  `~/.eval040-keys/REVEAL-img-r1.json`, `REVEAL-half2.json` (blind-packet reveal keys, must stay off-repo);
  `eval/harness-v2/authorization.*.local.yaml` (17 gitignored files, each materialised from a signed record in
  `coordination/decisions/`); judging galleries served locally from `eval/experiments/EVAL-040/runs/JUDGING-GALLERY-2026-09-09/`.
- **Review page** (Controller's): the "Capability Lab Audit Sheet" artifact, and the memory notes at
  `~/.claude/projects/-Users-vaibhavchawla-Vaibhav-Personal-Projects/memory/media-intelligence-capability-lab-direction.md`.

## 3. What to audit (answer each with evidence)

A. **Governance and authority.** For every paid call in every `ledger/`, name the spend record that authorised it and
   show cap ≥ ledger. Flag any run without a record, any cap crossed, any addendum written after the spend it covers,
   and any decision file whose quoted words you cannot find in the Controller's messages as recorded.
B. **Evidence integrity.** Re-hash sealed media against `*.record.json`; confirm no sealed file was modified after
   sealing (git history); confirm blind mappings were written before verdicts (timestamps, commitment files); confirm the
   reveal keys are not in the repo; confirm judge copies (re-encoded PNG/small mp4) never replaced originals.
C. **Registry discipline.** Every row: `instrument_qualification_status ∈ {deterministic, qualified}`, criteria sha =
   sha256 of the frozen `PASS-CRITERIA-v0.yaml` (v1), no human verdict encoded; re-run `registry_rows.py` dry on two runs
   and diff against the committed rows. Run `validate_registry.py`.
D. **Map discipline.** Tiers never mixed; every human number traceable to a `RESULTS.yaml`; rules RR-1..RR-16 each cite a
   run that exists and numbers that match the RESULTS; `screened_not_qualified` tier says registry: false everywhere.
E. **Pricing and package.** For a sample of 10 routes: the roster price equals the pinned page quote (open the bytes);
   `COST-TABLE.yaml` is byte-for-byte what `tools/build.py` regenerates from the roster (run it into a temp dir); the
   authorisation files' roster sha equals the roster on disk; the package basis commit in tests equals HEAD's package.
F. **Harness claims.** Run the test suite; hygiene: network imports only in `transports.py`; zero-retry and
   reservation-before-dispatch hold in `adapters/base.py` + `ledger.py`; keys never serialised (grep sealed json/yaml for
   `sk_`, `AIza`, `key=`; report paths only).
G. **Method.** Does the blind-judging protocol hold (names hide route; verdicts against the case contract; one call = one
   trial; repeat ≠ retry)? Where did the Controller judge stricter or looser than the written contract (notes say so)?
   Are the eliminations (E1/E2) computed correctly per `ELIMINATION-RULES.md`?
H. **Honesty of the narrative.** Compare `DAY-2-SUMMARY`, `CONTROL-STATE`'s audit index and the review page against the
   RESULTS files; list every number that does not match. Check the two conceded failures (roster tier gap; judge
   unqualified) are stated, not softened.
I. **Canon workstream** (lighter): is `canon/CANON-SHAPE-v1.md` §7 status consistent with the gate decisions and the
   CONTROL-STATE queue? Any Canon claim of "used in production" that the EVAL-040 blueprints do not bear out?
J. **Risks and next decisions.** Rank what could invalidate the routing map (n = 2 per cell; stand-in photos; judge
   bias; silent Wan tier), and list the decisions only the Controller can take, each with its cost.

## 4. Deliverable

`coordination/audits/AUDIT-2026-09-10-REPORT.md`: findings first (severity, path, evidence, one-line fix), then a
per-section verdict table (PASS / PASS-WITH-NOTES / FAIL / UNSUPPORTED), then the decision list. Plain English; the
Controller is not a native English speaker and not an engineer; keep code out of prose. Do not open a PR: leave the
report as an uncommitted file and tell the Controller where it is.
