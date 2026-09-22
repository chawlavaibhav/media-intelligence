## What this PR is

The `/media-agency-sync` integration of the accepted RentOK game-film jobs into `production-learning/`, cut from
`origin/main @ 4d919c9`. Originally two cases (the two-lane live experiment of 20–21 Sep 2026); **case 006 was appended on
21 Sep** (the same brief re-made "the Treatment C way") and **case 007 on 22 Sep** (the Mokobara castaway film — the first agency
job on generated footage; no code change) — see the sections at the end. Four cases, nine deterministic engineering changes with
regression tests (all from cases 004–006), and a set of proposals for Controller decisions. Nothing in `canon/**`, `eval/registry/**`,
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

**The job branch is on origin.** The sync brief described `work/agency-job-rentok-game-v2-001` as local-only; the remote-tracking
reflog shows origin received `b06deaf` at 2026-09-21T16:42Z (before the case was written), and the step-7 sync commit `b129bdd`
was pushed on top. The case validates against the immutable commit `b06deaf7907de9c64d574a5f042a014c2e519ce6`; fetch the
branch before running the validator.

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

- `work/agency-job-rentok-game-v2-001` @ `b06deaf7907de9c64d574a5f042a014c2e519ce6` (on origin; sync commit `b129bdd` on top)
- context: `work/experiment-rentok-creative-quality-001` @ `41d97c6` (CQ-001 diagnosis, Treatment C; on origin)

---

## Case 007 (added 2026-09-22) — `MOKOBARA-ODYSSEY-007`, the Mokobara castaway film: the first agency job on generated footage

**Branch-cut deviation, stated (third time).** The skill says to cut a fresh `work/agency-sync-<date>` from `origin/main`. This case is
**appended to this open PR's branch** (`work/agency-sync-2026-09-21`, on top of `7201ce0`) for the same reason as case 006: a branch
cut from main would conflict with cases 004–006 already here (README case list). No code file is touched by this case, so no new
`gates.py` overlap is added. Nothing else about the skill was skipped.

**Two things the sync brief and the record disagree on, resolved in the record's favour.** The brief called the job `customer_work`;
`JOB.yaml` says `class: spec_work` (Mokobara is a prospecting target; the human Controller acted as the customer) — the case says
`spec_work`. The brief said the collision fix should go in `runtime/execute/` if a runtime module owns attempt ids; none does (the runtime
mints ids structurally in `runtime/route/attempt_id.py`, collision-free by construction), so the item is class 2 with the exact
requirement, not class 1.

### Per job

| | `MOKOBARA-ODYSSEY-007` |
|---|---|
| Job | `AGY-2026-09-21-MOKOBARA-ODYSSEY-001` — a 30-s 9:16 spec film: a castaway finds his Transit Backpack, it holds more than seems possible, he goes home; the customer's own brief with five execution instructions (five stages, feeling/framing/impact per beat, an independent route decision, a fast first pass) |
| Base sha (`production_base_sha`) | `c88c0d5` |
| Job commit validated against | `130be42caae351a5bf8dc8d062b6fbf51e32b353` (on origin) |
| Verdicts (verbatim) | v1 **SPECIFIC REPAIR**: "the bag was slightly torn when he saw her wife photo. the instrument to run boat(oar or something) looked weird coming out of bag, when he takes the boat the oar was already on the bat but comes out magically again. overall excellent just few fixes. also we could use mokobara logo/name properly. the text font style could be better. excpetional work otherwise" · v2 **ACCEPT**: "still some minor issues but excellent. pass/" |
| CpAO (USD, ledger upper bound) | **7.857** — 27 paid calls (11 Nano Banana 2 stills 0.737; 14 Veo 3.1 Fast i2v clips, 70 s bought, 7.000; 2 Lyria 0.120), 26 ok, 1 HTTP 500 counted; v1 5.389 + repair round 2.468; USD 4.27 of it on re-takes; 28.0 s of the 70 bought are in the film |
| TTAO clocks (never blended) | **0:43:29** job start → v1 DET-clean file · **0:51:53** → v1 verdict · **1:15:46** → v2 DET-clean (the pipeline's clock for the accepted file) · **10:23:37** → ACCEPT (the outcome's clock; 9:07:51 of it is the customer's overnight reply) |
| Cycles / versions to accept | 2 / 2 (one independent checker round, on v1 only; v2 not re-checked) |
| Baseline (case 001, generative video) / RentOK V2 (case 006, code) | 7 h 54 m / USD 15.39 / 5 cycles — MET · 0:51 / USD 0.067 / 1 — a different class: 25 min slower to a clean file, ~117x the spend, which is what generated footage costs |
| Validator | PASS with `--source-ref 130be42…`, accepted film byte-verified (33,188,717 bytes) |
| Template | `still_to_i2v_story_film_with_product_photo_references` — reusable_candidate, **n = 1** accepted job, 1 customer, 1 brief, 1 product; `evidence_scope: this_accepted_template`; why candidate rather than job-specific is stated in the file |

The accepted file carries **five recorded, unrepaired items** (the arms never go in past the forearm — the customer's own named gag,
left out by the round's priority; the paddle's whereabouts for three seconds; the lid-style bag opening and beard/bracelet drift; 720p
sources; native audio never ear-checked) **plus the customer's unitemised "minor issues"**. The case does not present the file as clean.

### The five classes

| Class | Items |
|---|---|
| **1 Promoted — deterministic, in code, with tests** | **None.** Each candidate was tested against "name the check AND the runtime file": the ledger id collision (att-020 minted twice — the tool counts the settle-time `ATTEMPTS.jsonl`, so the window is the whole latency of any in-flight call, not "the same moment") has no runtime ledger to live in; the audio dips at two cuts (15–20 dB for 40 ms) have no runtime assembly step (the same reason `CODEC_TRUE_PEAK_MARGIN` is still class 2); "he never departs" is a human judgment. Evidence the earlier promotions work: `runtime.compositor.gates` (`check_text_bounds`, `check_contrast` on real pixels, `check_disjoint`) ran in production on this class for the first time — 10 gates PASS at render — and decided customer item 4 (black logo 6.58:1 vs white 1.3:1 on the sky). Suite: **520 OK**, unchanged by this case. |
| **2 Candidate patterns** (each with a promotion condition) | **STILL_TO_I2V_PER_BEAT_WITH_PRODUCT_PHOTO_REFERENCES** (the template, n = 1) · **MICRO_QUALIFY_THE_RISKIEST_ASSET_FIRST** (the comic beat bought first; now n = 4 jobs, 2 briefs, 2 classes — case 001's "≥ 2 more successes" is reached across briefs, see proposal 11) · **BOARD_FEELING_FRAMING_IMPACT** (case 006's condition — see proposal 12) · END_STATE_STILL_PLUS_LAST_ACTION_I2V (beats 5 and 6 fixed first draw only after the still moved to the end state) · EXIT_ACTION_AFTER_GOAL_STATE (the model re-opened the bag with 2.5 s left until told to lift it out of frame) · NEGATIVE_PROMPT_THE_PRODUCT_BEFORE_ITS_REVEAL · PAINT_OUT_COPIED_REFERENCE_MARKS_BEFORE_I2V (NB2 copied the tiny wordmark 2/2) · TAKE_SELECTION_BEFORE_RETAKE (the "weird" paddle was a warped blade on take 2; take 1 was on disk, USD 0) · MERGED_REPAIR_LIST_CUSTOMER_EVENTS_FIRST · MANDATORY_EVENT_VISIBILITY_LJ_LINE (one LJ line per M-table event before presentation) · BRAND_FONT_FALLBACK_WITH_SITE_CSS_STYLING (NeurialGrotesk absent → Helvetica Neue + the site's uppercase/.08em label CSS; licensed font = customer-supplied asset) · **LEDGER_LOCK_ATOMIC_ATTEMPT_IDS** (exact requirement: mint from the reserve-time ledger under an exclusive file lock, or structurally as the runtime does; an integrity check refusing duplicate ids) · AUDIO_JOIN_CROSSFADE (60-ms joins + a nameable RMS-at-cut gate) · OCR_ON_TEXTURE_IS_A_FLAG_NOT_A_GATE · SOURCE_RESOLUTION_STATED_BESIDE_DELIVERED · CODEC_TRUE_PEAK_MARGIN (fourth job the limiter stage held) |
| **3 Directional route observations** (`routing_authority: none`, exact n) | Veo 3.1 Fast i2v from NB2 stills: 14/14 returned, 7 in the film; identity and bag likeness held per the checker; seven named limits (a pull-back became a cut; arm-to-shoulder stayed at the forearm 2/2; seven items in 4–6 s 0/2; a rigid prop warped 1/2; a goal state undone 1/1 until an exit action; costume drift on a re-take 1/1; the product added unasked 1/1 until negative-prompted); 720p soft · NB2 with product-photo references: 11/11 usable first draw, copied the wordmark 2/2, a tear-like lining flap 1/1 then intact 1/1 · Lyria HTTP 500 on a story-laden wording, ok on neutral (cross-job: 4 errors on descriptive wordings over 2 jobs; 4/4 neutral first tries over 4 jobs) · AAC with a limiter: TP −4.1 / −4.0, n = 2 |
| **4 Canon gap candidates** (report only) | **None new.** The Ogilvy-vs-Hopkins humour tension (`sk_ogx_0032` vs `sk_mla_0064`) was named at Stage 3 and resolved from existing claims by the brief's own "would be funny" clause — a tension inside accepted Canon, not a missing domain; no production failure traces to missing Canon (the creative defects trace to the model's execution and a clip length the board over-asked); the eight uncompiled packs are the known gap already on the Controller's list |
| **5 Job-specific, not promoted** | the seven beats' feelings/framings/impacts, the tagline "Room for the long way home.", the Private Island colourway and its reasons, the Stage 1 decisions (9:16 only, ~30 s, no dialogue, no price, 24 fps), the reading of "arms" and "odysey", the man's design, the repair priority letters, the disk-space note |

### Proposals awaiting a Controller decision (written in the case, not applied)

11. **Micro-qualification as a required Stage 4 line** — case 001's "≥ 2 more successes" is now reached across two briefs and two
    production classes (cases 004, 005, 006, 007); proposal 4 above asked whether one brief counts — it no longer has to.
12. **Feeling / framing / impact per beat — case 006's promotion condition.** The condition ("one more accepted job on a DIFFERENT
    brief") is **met in letter** by this job and **not in spirit** for its stated consequence ("required … for code-rendered classes"):
    this job is generated footage, not code-rendered; the same customer judged both; acceptance came on v2 after re-takes; nothing
    isolates the schema's contribution (no A/B, no rank). What n = 2 briefs / 2 classes / 1 customer supports: the three fields are a
    usable, free direction checklist on both classes. What it does not support: that they cause acceptance (still CQ-001's n = 1 beat).
    **Proposed:** require the fields in `/media-agency` Stage 3 for every per-beat film class (a skill edit), with the causal claim kept at
    its real n. Not promoted here.
13. **The dispatch kit's attempt-id minting** — `LEDGER_LOCK_ATOMIC_ATTEMPT_IDS` should be applied on the kit's next copy (the tool
    travels job to job on job branches: `tools/PROVENANCE.md`); a `/media-agency` skill note pointing at the rule is the smallest change.
14. **The still → i2v topology as the named default route** for live-action-style story films in `/media-agency` Stage 4 — after one
    more accepted job on a different brief and product (the template's stated condition); not before.
15. **Presentation-gate records** — one LJ line per mandatory customer event before presentation (this job presented a beat as
    realised in which the mandatory "goes back" does not happen); a Stage 5 template edit.
16. **Governor refresh** — `PROJECT-MEMORY.md` / `coordination/CONTROL-STATE.md` untouched; a refresh may be wanted for case 007
    (the first generated-footage agency job) and for the class-2 backlog, which now has 15 items from this case alone.

### Notes for the reviewer (case 007)

- No code change in this case; the suite was run anyway (520 OK). The `gates.py` / README conflict note for PR #103 still applies
  to cases 004–006's edits; this case adds one line to the README case list.
- The job's own records carry three arithmetic/stamp discrepancies the case records rather than adopts: the packet's `first_pass_usd
  3.529` omits the counted 0.06 failure (ledger 3.589), `clips_bought_s 46` ≠ the ledger's 70 s, `repair_round_1_minutes ~50` is not
  derivable (18:14:41 → 18:38:34 = 23:53); `JOB.yaml` stamps v2 presented 94 s before its QA completed and holds a stale duplicate
  v2 entry. The money total (7.857) and both verdicts are unaffected. Nothing on the job branch was edited.
- Not on the branch, stated as such: no independent check of v2; no human ear check of the native audio on either version; no record
  of which "minor issues" the customer meant.
- Disk: no media was copied into the case; the validator reads the accepted film from the commit.
- Still awaiting their own sync, unchanged from the notes above: `work/agency-job-skateboard-slowmo-001`, the two Cumin experiment jobs.

### Raw job branch (archival; never merged)

- `work/agency-job-mokobara-odyssey-001` @ `130be42caae351a5bf8dc8d062b6fbf51e32b353` (on origin; the step-7 sync commit follows on top)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
