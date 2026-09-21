## What this PR is

The `/media-agency-sync` integration of the accepted RentOK game-film jobs into `production-learning/`, cut from
`origin/main @ 4d919c9`. Originally two cases (the two-lane live experiment of 20–21 Sep 2026); **case 006 was appended on
21 Sep** (the same brief re-made "the Treatment C way" — see the section at the end). Three cases, nine deterministic
engineering changes with regression tests, and a set of proposals for Controller decisions. Nothing in `canon/**`, `eval/registry/**`,
`eval/capability-map/**`, `coordination/**` or `PROJECT-MEMORY.md` is touched. **Do not merge the raw job branches.**

## Per job

| | `RENTOK-GAME-A-004` — lane A, autonomous | `RENTOK-GAME-B-005` — lane B, ChatGPT-directed |
|---|---|---|
| Job | `AGY-2026-09-20-RENTOK-GAME-LANE-A-001` | `AGY-2026-09-20-RENTOK-GAME-LANE-B-001` |
| Base sha (`production_base_sha`) | `4d919c9` | `4d919c9` |
| Job commit validated against | `7dab37a70b004881a1ef9dea465b8aac41e6a979` | `d0a0583d3372c6f7c49fdeee18643d4cb860cd67` |
| Verdict (verbatim, one message for both) | "both accepted. vidoe one has robotic voice over althouh. video 2 is better" — this film = Video Y, **ACCEPT, preferred** | same message — this film = Video X, **ACCEPT**, voice noted as robotic |
| CpAO (USD, ledger upper bound) | **0.529** (8 calls, 0 failed, 0 paid repairs) | **0.58675** (25 calls incl. 9 voice-audition + 8 QA transcription; 3 failed, counted) |
| TTAO (job_start → customer accept) | **1:54:18** | **1:53:07** |
| Cycles / versions to accept | 1 / 1 (two internal checker rounds before) | 1 / 1 (one internal checker round before) |
| Baseline (case 001) | 7 h 54 m / USD 15.39 / 5 cycles — a different production class, side by side only | same |
| Validator | PASS with `--source-ref`, accepted film byte-verified | PASS with `--source-ref`, accepted film byte-verified |
| Template | `code_rendered_side_scroller_with_ai_sprites` — both lanes reached it independently; n = 2 jobs, 1 customer, 1 brief | same template id, this lane's beat times |

Both lanes' quality was won in the independent-checker → USD-0 repair loop, not at the generation layer (A: 18 defects
closed before presentation, 0 model failures at a gate; B: 16 closed, 1 model failure at a gate, 1 at the customer — the
voice no human had heard).

## The five classes

| Class | Items |
|---|---|
| **1 Promoted — deterministic, in code, with tests** (`runtime/tests/test_j_rentok_game_004_005.py`, 19 tests; full suite 503 OK) | `runtime/loop/container.py` MP4 edit-list box walk (A D-1) · `gates.check_graphic_text_disjoint` (A D-2, B D-1/D-9) · `gates.check_vo_text_alignment` (B D-3) · `gates.check_brand_colour` (A D-11/D-8) · `runtime/execute/bridge.py`: a harness-refused attempt reserves neither ceiling nor pool (B att-016/T1 — the runtime had the same ordering fault: four refused motion attempts reserved USD 2.304 and blocked a later one by pool) |
| **2 Candidate patterns** (each with a promotion condition) | CODE_RENDERED_GAME_WITH_AI_SPRITES (template) · ANIMATIC_BEFORE_SPEND · MICRO_QUALIFY_THE_RISKIEST_ASSET_FIRST / SPRITE_SHEET_SINGLE_DRAW (case 001's "≥ 2 more successes" is arithmetically reached on one brief — a Controller call) · FIVE_STAGE_PROTOCOL_WITH_NON_AUTHOR_CHECKER · REPAIR_STATEMENT_QUOTES_MEASURED_VALUE · LAYOUT_LOG_GATES · CODEC_TRUE_PEAK_MARGIN (n = 2 jobs, ≈ 2 dB AAC overshoot) · COMPOSE_WORLD_ACROSS_THE_FULL_FRAME (both lanes left the lower band empty) · KEYING_HELPER · VOICE_CAST_BY_A_HUMAN_EAR · PER_KEY_QUOTA_IN_POOL_READINGS · MEASURED_VO_DRIVES_TIMELINE · WORLD_AT_LOWRES_TEXT_AT_FULLRES · CANON_GAP_DECLARATION_VERIFIED |
| **3 Directional route observations** (`routing_authority: none`, exact n) | nano-banana-2 multi-pose sheets 2/2 held identity with no lettering (each lost/hid one identifier in ≥ 1 pose); 14/14 textless stills usable first draw; lyria-002 2/2; Sarvam bulbul:v3 heard as robotic by the customer (n = 1; second hearing after case 001); Gemini TTS refused one 16-char brand line as PROHIBITED_CONTENT (n = 1); ElevenLabs per-key quota invisible to the balance read; AAC overshoot n = 5 encodes across both lanes |
| **4 Canon gap candidates** (report only) | no accepted Canon on game/arcade readability, pixel art, chiptune — both lanes declared it, no failure followed · lane B declared audio/colour domains as gaps that had accepted claims (found by the gate checker) → a "verify a declared gap against the index" checker step |
| **5 Job-specific, not promoted** | metaphors, palette, layouts, copy, the 1.2 s / 1.6 s clear tempos, the ten changes from the ChatGPT direction, the one refused line, the invented app icon, the customer's ranking of the two films, session-token counts |

## Proposals awaiting a Controller decision (written in the cases, not applied)

1. **Roster pool labels** — `eval/empirical-planning/ROSTER-REFRESH-2026-09.yaml` labels `sarvam-bulbul-v3` and `elevenlabs-v3`
   `billing_pool: cash`; `eval/capability-map/ROUTING-EVIDENCE-MAP-v0.yaml` says `sarvam_credits` / `elevenlabs_credits`; the
   Controller ruled 20 Sep that they are credits pools. Reconcile under the roster's refresh process (verified in this checkout; not edited).
2. **Gemini TTS** was used under a job-local pin with no Registry cell — whether the routing map should carry a row (directional only).
3. **Canon gap** (item 4 above) — whether to seek sources for the game/arcade domain; whether to add the gap-verification checker step.
4. **Micro-qualification promotion** — case 001's condition is met in count but on one brief; decide whether that counts.
5. **Governor refresh** — `PROJECT-MEMORY.md` / `coordination/CONTROL-STATE.md` are not edited here; a refresh may be wanted for cases 004/005 and the five promoted checks.

## Notes for the reviewer

- **Merge overlap with PR #103** (`work/agency-sync-2026-09-16`, case 003): both PRs append to `runtime/compositor/gates.py`
  (this one adds three gates; #103 adds `check_vo_schedule`), and both edit `production-learning/README.md`. The additions are
  complementary and non-overlapping in meaning; expect a textual conflict at the end of `gates.py` and in the README case list.
  This branch does not touch `runtime/tests/test_i_compositor_gates.py` (its tests are in a new file) to keep that conflict away.
- **Committed dry battery re-recorded** (`runtime/battery/results/2026-09-14/`, run B05 only): the bridge fix changes what a
  manifest with harness-refused attempts records (`reserved_total` 2.16 → 0.96; two `refusal_reason` strings gain
  `not_reserved: …`), and the outcome-event / template ids re-hash. `test_alpha_cli.BatteryManifest` regenerates and compares;
  the other 13 runs are byte-identical in the compared fields.
- The customer's verdict is chat-only evidence, transcribed verbatim on the experiment branch before the blind mapping was
  opened; the blindness limitation (the human had seen per-lane progress facts in chat) is recorded in both cases.
- Skipped by this sync: `work/agency-job-skateboard-slowmo-001` (`AGY-2026-09-16-SKATEBOARD-SLOWMO-001`, accepted, `pending_sync`) — out of
  scope, still awaiting its own sync; `work/agency-job-cuminco-chopsticks-001` is already `synced` (case 003, PR #103).

## Raw job branches (archival; never merged)

- `work/agency-job-rentok-game-lane-a-001` @ `7dab37a`
- `work/agency-job-rentok-game-lane-b-001` @ `d0a0583`
- `work/experiment-rentok-two-lane-2026-09-20` @ `594e7c9` (contract, spend authorisation, blind packet, Controller comparison)

---

## Case 006 (added 2026-09-21) — `RENTOK-GAME-V2-006`, the film re-made "the video 4 way"

**Branch-cut deviation, stated.** The skill says to cut a fresh `work/agency-sync-<date>` from `origin/main`. This case was
instead **appended to this open PR's branch** (`work/agency-sync-2026-09-21`, on top of `1510b75`), because it is the same
RentOK line as cases 004/005 already on it and a branch cut from main would conflict with them (README case list,
`gates.py`, and the shared template id). Nothing else about the skill was skipped.

**The job branch is local-only.** `work/agency-job-rentok-game-v2-001` existed only in the local repository when the case was
written; the case validates against the immutable commit `b06deaf7907de9c64d574a5f042a014c2e519ce6`. A push of the job branch
is attempted in step 7 of the sync; if this PR's reviewer cannot resolve that commit, the branch has not been pushed yet and
the validator will (correctly) FAIL until it is.

### Per job

| | `RENTOK-GAME-V2-006` |
|---|---|
| Job | `AGY-2026-09-21-RENTOK-GAME-V2-001` — supersedes Lane A (`7dab37a`, case 004); asked for after experiment `RENTOK-CREATIVE-QUALITY-001` ranked Treatment C above the accepted Lane A beat |
| Base sha (`production_base_sha`) | `c88c0d5` |
| Job commit validated against | `b06deaf7907de9c64d574a5f042a014c2e519ce6` |
| Verdict (verbatim) | **"its already good"** — ACCEPT on first presentation; the checker's USD-0 repair round was offered and declined: **"not required"**; earlier: "Also, this is finally one amazinh outcome" |
| CpAO (USD, ledger upper bound) | **0.067** (1 call, 0 failed, 0 paid repairs). Separate line, never blended: **0.663** for every drawing that appears in the film across three ledgers (Lane A 0.529 + Treatment C 0.067 + this 0.067) |
| TTAO | **0:51:13** job start → DET-clean deliverable (the pipeline's clock) · **5:09:28** job start → ACCEPT (the outcome's clock; the file was presented at 12:33Z and the customer answered at 16:34Z — the difference is waiting) |
| Cycles / versions to accept | 1 / 1 (one USD-0 animatic round and one producer repair round before; one independent checker round whose repairs were declined) |
| Baseline (case 001) / Lane A (case 004) | 7 h 54 m / USD 15.39 / 5 cycles — 1:54:18 / USD 0.529 / 1 cycle — side by side only |
| Validator | PASS with `--source-ref b06deaf…`, accepted film byte-verified |
| Template | `code_rendered_side_scroller_with_ai_sprites`, new variant `directed_board_v2` (feeling / framing / impact per beat + primitive renderer + textless AI sprites); n = 2 accepted jobs on the skeleton, 1 customer, 1 brief; `evidence_scope: this_accepted_template` |

The accepted file carries **ten recorded, unrepaired defects** (checker N1–N9 + P1) by the customer's choice. The packet
and JOB.yaml say "six" were offered; which six is chat-only. The case records all ten as unrepaired and does not present the file as clean.

### The five classes

| Class | Items |
|---|---|
| **1 Promoted — deterministic, in code, with tests** (`runtime/tests/test_k_rentok_game_v2_006.py`, 17 tests, every number from the job's layout log and cut-out records) | `gates.check_hero_visible` — a declared hero region (whole box at the flag beat; the face while he holds the phone) may not be covered by a graphic drawn in front of it (N1: flag through the cheering owner, 26 frames; N2: phone over the face, 6 frames — the graphic-vs-text gate could not see either) · `gates.check_framing_target` — hero height ÷ frame read at ONE named focus frame against a per-pose target; missing frame refuses; optional hero-inside-canvas (A-4 mid-ease measurement; R-1 0.202 < 0.21; N4 dazed pose 52 px off the left edge) · `gates.check_world_fills_frame` — every camera scale ≥ 1.0, none logged refuses (LJ-15; promoted from a passing job-local DET row) · `gates.check_sprite_density` — one character's sheets within a stated standing-height ratio (N5: 561 / 344 / 342 px = 0.61, a visible pop at ~150 swaps; the producer had the number and read it as invisible at phone size) |
| **2 Candidate patterns** (each with a promotion condition) | **BOARD_FEELING_FRAMING_IMPACT** — the single change that moved the customer's rank in CQ-001; promotion: one more accepted job on a *different* brief · **ANIMATIC_BEFORE_SPEND** — n now 4 productions (Lane A, Cumin B — a rejected job whose animatic still caught a wrong-product end card, CQ-001 Treatment C, this); case 004's condition is MET → proposal below · TREATMENT_C_RENDERER_PRIMITIVES (25 named primitives, board-driven) · **CUSTOMER_MAY_DECLINE_A_REPAIR_ROUND** — record offered defects on disk at the time of the offer and as unrepaired on the accepted file · SPRITE_STATE_SEMANTICS_IN_OCCLUSION_GATES · WORLD_STOPS_WHEN_HE_IS_DOWN · CODEC_TRUE_PEAK_MARGIN (n now 3 jobs; a limiter stage held where headroom did not) · POSE_HEIGHT_JUMP_CHECK (nameable, not yet safe) · REUSED_ASSET_STYLE_CHECK · KEYING_HELPER (third sheet with a fringe) · BRAND_COLOUR_SAMPLING_PLAN |
| **3 Directional route observations** (`routing_authority: none`, exact n) | nano-banana-2 8-pose sheet from text: 1/1 first draw passed the consistency card with one pose miss (the look-back drawn facing forward) — four such sheets across the RentOK jobs, each with one limitation; 53.6-s latency on one 16:9 sheet (n = 1); AAC overshoot held by a limiter (n = 2 encodes) |
| **4 Canon gap candidates** (report only) | no accepted Canon on animation principles / game feel — now declared on three records (CQ-001, this job's Stage 3, JOB.yaml), bridged each time by named references recorded as reasoning; no failure followed |
| **5 Job-specific, not promoted** | the fifteen beats' feelings, camera keyframes, hit-stop counts, shake amplitudes, the 53 audio cues; the five obstacle motions and payoffs; the no-redraw decision on the look-back pose; the bed-reuse decision; the customer's "finally" as a comparison with Lane A; the layout numbers |

### Proposals awaiting a Controller decision (written in the case, not applied)

6. **Animatic-before-spend as a required step** for code-rendered classes in `/media-agency` Stage 5 — case 004's promotion condition ("one more code-rendered job") is met; making it mandatory is a skill edit.
7. **Board schema fields** `feeling / framing / impact` — whether to require them in Stage 3 for code-rendered classes now (n = 1 brief) or after one more brief (the case's stated condition).
8. **Canon gap: animation principles / game feel** — three records now reason without Canon; whether to seek sources.
9. **Repair-offer records** — whether `/media-agency` should require the offered-defect list to be written to `JOB.yaml` before the customer is asked (this job's "six" is unrecoverable).
10. **Governor refresh** — `PROJECT-MEMORY.md` / `coordination/CONTROL-STATE.md` untouched; a refresh may be wanted for case 006 and the four new gates.

### Notes for the reviewer (case 006)

- `runtime/compositor/gates.py` gains four gates and six refusal codes at the end of the file; the PR #103 conflict note above still applies (both append to the same file).
- Full suite result is stated in the commit message for this case.
- The sync also found `work/agency-job-cumin-exp-b-fivestage` (`AGY-2026-09-20-CUMIN-EXP-B-FIVESTAGE-001`, rejected, `pending_sync`, local-only) and `work/agency-job-cumin-exp-a-existing` — out of scope here; still awaiting their own sync. The skateboard job noted above is unchanged.

### Raw job branch (archival; never merged)

- `work/agency-job-rentok-game-v2-001` @ `b06deaf7907de9c64d574a5f042a014c2e519ce6` — **local-only until pushed** (see above)
- context: `work/experiment-rentok-creative-quality-001` @ `41d97c6` (CQ-001 diagnosis, Treatment C) — local-only

🤖 Generated with [Claude Code](https://claude.com/claude-code)
