## What this PR is

The `/media-agency-sync` integration of the two accepted RentOK game-film jobs (the two-lane live experiment of
20–21 Sep 2026) into `production-learning/`, cut from `origin/main @ 4d919c9`. Two cases, five deterministic engineering
changes with regression tests, and a set of proposals for Controller decisions. Nothing in `canon/**`, `eval/registry/**`,
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

🤖 Generated with [Claude Code](https://claude.com/claude-code)
