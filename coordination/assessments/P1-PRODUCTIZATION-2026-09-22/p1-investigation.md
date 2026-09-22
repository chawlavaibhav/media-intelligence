# P1 investigation — what the code does vs what the documents say

Read-only, 2026-09-22. Worktree `media-intelligence-rentok-sync` @ `f57246f` (branch `work/agency-sync-2026-09-21`, PR #104, base `origin/main @ c88c0d5`). Mokobara job read from `media-intelligence-mokobara` (branch `work/agency-job-mokobara-odyssey-001`). RentOK jobs read via `git show origin/<branch>:<path>`. No paid call. `/usr/bin/python3` throughout.

Labels: **OBSERVED** (path @ ref, or command output reproduced here) · **INFERRED** · **UNKNOWN**.

**Housekeeping disclosure (OBSERVED):** running `python3 -m runtime.alpha.cli` on the Mokobara brief under profile `dry_permissive` wrote one untracked file into the sync worktree: `runtime/fixtures/planner/unanswered/02d9d035…prompt.json`. This is the runtime's own documented behaviour (`PRODUCTION-WORKFLOW.md` §4 warns of exactly this "spill"). I was not permitted to delete it; it is untracked and uncommitted. Please `rm -rf runtime/fixtures/planner/unanswered` in that worktree.

---

## 1. ★ Canon — exact state

### 1.1 The ten packs

Trigger table: `canon/packs/pack-triggers-v0.yaml` — `status: PROPOSED` ("no Controller decision adopts it"). Its closed set of ten ids, in table order, and what exists for each:

| # | pack id | compiled file | status field | decisions / check lines | would `lookup()` inject it? | accepted SourceKnowledge reachable only by direct reading |
|---|---|---|---|---|---|---|
| 1 | camera_and_spatial_grammar | none | — | 0 / 0 | never (no file) | 190 objects across 6 sources (4 domains, 2 critical) |
| 2 | colour_and_visual_register | none | — | 0 / 0 | never | 328 objects / 10 sources (3 domains; 1 `absent`) |
| 3 | commercial_communication | none | — | 0 / 0 | never | 555 objects / 15 sources (9 domains, **7 critical**) |
| 4 | composition_and_attention | `canon/compilation/PACK-composition_and_attention-v0.yaml` (47,486 B) | `PROPOSED — Canon-stream worker output; no Controller decision adopts it` | **11 / 11** (CA-D1..D11), 69 cited SK objects, terse text 9,986 chars ≈ 2,497 tokens | yes, when selected (digest matches) | pack cites 69 of 356 objects in its domains' sources |
| 5 | concept_and_distinctiveness | none | — | 0 / 0 | never | 542 objects / 17 sources (7 domains) |
| 6 | critique_and_effectiveness | none | — | 0 / 0 | never | 987 objects / 28 sources (10 domains) |
| 7 | editing_pacing_and_short_form | none | — | 0 / 0 | never | 172 objects / 5 sources (7 domains, 3 critical; 1 `absent`, 1 `representation_or_evidence_limited`) |
| 8 | indian_indic_context | none | — | 0 / 0 | never | 97 objects / 5 sources (1 domain, `present_but_operationally_limited`) |
| 9 | product_appearance | `canon/compilation/PACK-product_appearance-v0.yaml` (40,043 B) | same PROPOSED wording | **10 / 10** (PA-D1..D10), 35 cited SK objects, terse text 9,889 chars ≈ 2,473 tokens | yes, when selected | pack cites 35 of 310 objects in its domains' sources |
| 10 | typography_and_copy | none | — | 0 / 0 | never | 271 objects / 7 sources (4 domains, 3 critical; 1 `absent`) |

Sources for the right-hand column (OBSERVED, computed): `canon/planning/CANON-V1-LIVE37-COVERAGE.yaml` (packs → domains → contributor sources; every one of the 37 accepted sources is mapped) joined to `canon/knowledge/CANON-CORPUS-INDEX.yaml` (per-source `source_knowledge` counts; 1,300 accepted objects total). Sources contribute to several packs, so the column does not sum to 1,300. What the number means: for eight of ten packs, hundreds of accepted, audited claims exist on disk and **nothing in code can put any of them in front of a model**; a producer reaches them only by opening YAML files and reading.

How "accepted" is decided for the two compiled packs (OBSERVED, `runtime/canon/packs.py` L156–176): a pack is injectable only if its `corpus_digest` equals `fingerprints.accepted_canon.combined_digest` in the corpus index. Both compiled packs carry `3f7e3fad…` and match, so the runtime reports them `compiled_accepted` — even though the pack files themselves say PROPOSED. Two different meanings of "accepted" (corpus bytes vs. Controller adoption) coexist; the code uses the first.

### 1.2 Run on the Mokobara brief (OBSERVED, command output)

`from runtime.canon import normalize, lookup` on `agency/jobs/AGY-2026-09-21-MOKOBARA-ODYSSEY-001/brief.job.json`:

```
NR modality: video | op: generate | market: IN | text_requirements: 3 | acceptance_intent: {'advertising': True}
SELECTED (10): concept_and_distinctiveness [universal, uncompiled] · critique_and_effectiveness [universal, uncompiled]
  · composition_and_attention [base:video, COMPILED] · colour_and_visual_register [base:video, uncompiled]
  · camera_and_spatial_grammar [base:video, uncompiled] · editing_pacing_and_short_form [base:video, uncompiled]
  · typography_and_copy [text_requirements_nonempty, uncompiled] · product_appearance [product entity, COMPILED]
  · indian_indic_context [market IN, uncompiled] · commercial_communication [advertising intent, uncompiled]
INJECTED: ('composition_and_attention', 'product_appearance')
GAPS (8): camera_and_spatial_grammar, colour_and_visual_register, commercial_communication, concept_and_distinctiveness,
  critique_and_effectiveness, editing_pacing_and_short_form, indian_indic_context, typography_and_copy
canon_gap: True | tokens: 5298 | check_ids: 21 (CA-D1..11, PA-D1..10) | prefix_sha256: 4d7a5b27e17c5ff3… | injection_version: v1
notice: "receipt vocabulary retired by CANON-SHAPE-v1 §5 is still carried by the canon-owned pack text of composition_and_attention, product_appearance"
```

This reproduces the producer's own record byte-for-byte (`stages/evidence/canon-lookup.txt`, same sha). **Every trigger fires for a video ad with text, a product, an Indian market and advertising intent — all ten packs — and eight of the ten return nothing.** The payload the model would receive is the 328-token system block plus two packs; the gap is recorded as `missing_domain` and the job continues (`packs.py` docstring: "a missing pack never blocks a job and never starts a compilation programme").

### 1.3 Trigger-table coverage of media classes (OBSERVED)

The table is total over the frozen grammar's 4 modalities × 7 operations = 28 cells (`static_image`, `video`, `image_sequence`, `audio` × generate/edit/animate/restore/extend/compose/variants). There is **no modality for "story", "animation" or "game"** — those are deliverable *kinds* (`runtime/contracts/DELIVERABLE-KINDS.yaml`: static_ad, static_ad_from_supplied_photo, short_motion_from_accepted_still, text_in_motion, multi_shot_story, spoken_voiceover, music_bed, two_speaker_dialogue, lipsync_to_supplied_audio) that `runtime/canon/KIND-NR-BINDING-v0.yaml` maps onto one of the four modalities. Consequences:

- **video** → base set of 4 packs, of which 1 is compiled (composition_and_attention). Camera, editing/pacing, colour: uncompiled.
- **audio** → `audio: []` — zero packs; the table injects a verbatim `coverage_gap_notice` ("no accepted Canon source covers audio production… do not attribute audio decisions to Canon").
- **animation / code-rendered game** → no pack, no domain; the RentOK cases record this as a Canon gap three times (PR body L109).
- The uncompiled state is disclosed inside the table itself (header comment: "Only product_appearance and composition_and_attention are compiled today") and its `notes:` ("Three packs compile thin today…").

### 1.4 The consumption rule (OBSERVED, `canon/CANON-SHAPE-v1.md` §4)

> "customer request → Normalized Request → pack lookup (deterministic: NR → 2–4 pack ids) → blueprint: a reasoning model writes ONE production plan · packs injected UNCONDITIONALLY as a stable, byte-identical, cache-served prefix … → PRE-DISPATCH GATE (code, zero tokens) … → POST-DRAW GATE (code, ≈zero) … → human acceptance … → EMPIRICAL MEMORY. Canon touches this pipeline in exactly three places: the injected packs, the two gates, and the template library. **Nowhere does the consuming model decide whether to consult Canon, search it, or read it** — the self-diagnosis trap that produced Gemma's 0/18 in EVAL-037 is designed out."

§2 of the same document states plainly: "Compiled packs | **2 of 10**". §7 item 4: "Remaining packs only as the gate needs them".

### 1.5 The decision that forbids compiling (OBSERVED)

`coordination/decisions/CONTROLLER-CAPABILITY-LAB-STOP-WIDENING-AND-CANON-INJECTION-V1-2026-09-14.md`, C-10, verbatim:

> "Authorise USD-0 implementation of: Canon Injection v1; template / empirical-memory integration. Do NOT compile the remaining eight packs unless a real runtime failure later demands one."
> "7. **The remaining eight compiled packs are NOT to be compiled** unless a real runtime failure later demands one. 'Real runtime failure' means an observed failure in the production runtime, not an anticipated one; each such pack would need its own Controller decision at that time."

Mirrored in `coordination/CONTROL-STATE.md` L81 and `PROJECT-MEMORY.md` L39/L239/L267. So the 2-of-10 state is documented in five places; it was a ruling, not an oversight. What the ruling did not anticipate (INFERRED): five agency jobs have since run, none through the runtime, so the "real runtime failure" trigger can never fire — the producer sessions read the uncompiled knowledge by hand instead (§2 below).

---

## 2. ★ Retrieval-and-application trace — Mokobara

### 2.1 Every Canon id cited on the job (OBSERVED, grep over `stages/*.md`, `board.json`, `copy-deck.json`, `gen/prompts/*.txt`, `JOB.yaml`, `LEARNING-PACKET.yaml`)

Compiled check ids: CA-D1..D11 and PA-D1..D10 (all 21 named in `stages/03-CREATIVE.md` A3).
Raw SourceKnowledge ids (**not in any compiled pack**): `sk_abcd_0007, sk_abcd_0010, sk_abcd_0011, sk_abcd_0012, sk_ogx_0039, sk_ogx_0040, sk_ogx_0032, sk_ogl_c003_0014, sk_sb_c003_0014, sk_whip_0011, sk_whip_0058, sk_whip_0031, sk_mla_0064, sk_fre_c003_0025, sk_hea_mts_0011, sk_gote_c003_0004, sk_gote_c003_0006, sk_murch_c003_0020, sk_gos_c003_0007, sk_alt_c003_0018, sk_vig_c003_0013, sk_hop_sa_0026` — 22 ids from 13 sources.

Of those 22, the sources google-abcd, ogilvy-beyond, sullivan-hey-whipple, hopkins-my-life are among the 13 sources that the older LIVE24 map did not even place in a pack (LIVE37 does). None is in a compiled pack. The prompts (`gen/prompts/*.txt`) contain **zero** Canon ids — the doctrine reaches the model only as English words the producer wrote.

### 2.2 Twelve claims opened and traced

Quotes are from `canon/knowledge/current/<source>/source-knowledge.yaml` (key `sk_id`; field `claim`), truncated. (a) = decision in board/copy deck; (b) = the prompt or code that carried it; (c) = the frame in the accepted v2 file (`gen/final/mokobara-odyssey-9x16-30s.mp4`, sha `71850d1c…`) per the checker's frame citations in `stages/CHECK-STAGE-5.md` and the v2 verdict in `HUMAN-VERDICT-V1.md`.

| id (source) | Claim (quoted) | (a) decision | (b) carrier | (c) in the final | Class |
|---|---|---|---|---|---|
| sk_abcd_0007 (google-abcd) | "two concrete opening constructions — beginning in the middle of the action, and opening on a close-up" | board beat 1 `canon:` "open in the middle of the action on a close-up" | `gen/prompts/b1-still.txt`: "Extreme close-up: the weathered right hand … scratching one more mark" | checker `f003-01.0s`: tally-mark ECU at 0–1.5 s. But the clip then hard-cuts at 1.54 s to a static frontal portrait (checker §4 "NEW defect") — the open is only half the board | **APPLIED-VISIBLE** (partially) |
| sk_ogx_0040 (ogilvy-beyond) | "the first frame as the gate: grabbing attention there with a visual surprise" | board beat 1: first frame = hundreds of marks | same prompt ("covered edge to edge in hundreds of small scratched tally marks") | same frame | APPLIED-VISIBLE |
| sk_abcd_0010 (google-abcd) | "brand … when it first appears (early), how often it recurs (often), how many different kinds of branding element carry it (richly)" | copy-deck `wordmark_super` t 5.0–7.5 s "why: name within the first ten seconds (sk_ogx_0039)"; bag in frame 3.5–28 s | `tools/assemble.py` L42 reads `copy-deck.json["placements"]["wordmark_super"]` t_in/t_out and composites the SVG by code | checker R7: super at 5.0–7.5 s (`f012-05.5s`), end card 28–30 s (`f058-28.5s`); wordmark pixel-identical to the site SVG (PSNR ∞) | **APPLIED-VISIBLE** (the clearest code-carried case) |
| sk_ogx_0039 (ogilvy-beyond) | "use the name within the first ten seconds … Commercials which end by showing the package are more effective" | same as above + beat 7 "package close" | assemble.py end card | same | APPLIED-VISIBLE |
| sk_ogl_c003_0014 (ogilvy-ch2) | "The product itself should be made the hero of the advertising wherever possible" | board `identity_anchors.bag`; every beat turns on the bag | every clip prompt carries the verbatim bag description ("deep navy-blue backpack … bright sunshine-yellow lining, no lettering and no logo") | checker §3: bag present at 5.5 / 16.5 / 22.5 / 26.0 s; likeness bends (lid opening, pocket hanging down) | APPLIED-VISIBLE |
| sk_whip_0058 (sullivan) | "Funny is a subset of interesting; it is not a language but an accent" | board beat 4 `canon:` "played dry, no mugging" | `b4-clip-take2.txt`: "Action, played completely deadpan … Camera: no movement at all — the joke is the hold" | checker R6: arms only to forearm depth; paddle reveal lands; "5 s of ordinary rummaging" — the *register* is visible, the gag is half-delivered; customer v1 "oar … looked weird", v2 "still some minor issues" | APPLIED-VISIBLE (register) / gag itself **unrepaired D1** |
| sk_whip_0031 (sullivan) | exaggeration "must be based on a truth" (per producer's quote; source: "requires the maker to notice when they are using [it]") | board beat 4: truth = "Capacity: 30L" from `transit-backpack.json` | copy-deck `product_line: "Transit Backpack · 30L"`; end card by code | end card frame `f058-28.5s` | APPLIED-VISIBLE |
| sk_gos_c003_0007 (grammar-of-the-shot) | "A subject's left or right movement must be maintained from one shot to the next" | board beat 6 `canon:` "he travels left-to-right in beats 1 and 6" | `b6-clip-take2.txt`: "toward the band of pale gold light on the horizon at frame right" | checker §4 records no screen-direction fault; not explicitly measured | APPLIED-IN-PLAN-ONLY → INFERRED visible (no frame evidence either way) |
| sk_alt_c003_0018 (alton) | "comedy … drama … mystery — each requiring a different approach [to illumination]" | 03-CREATIVE A2 records a **deviation**: comedy would be "lit high"; film stays low grey; forcing clause = the brief's survival story | every prompt: "soft overcast skylight from the upper left, the only source" | checker §5 "cinematic look 4/5 … grey pebble shore" | APPLIED-VISIBLE (as a recorded deviation) |
| sk_abcd_0012 (google-abcd) | "an audio mention of the brand raises the performance of the on-screen brand visual" | recorded **deviation**: no VO (Stage 1 language decision); "cost = weaker brand recall" | nothing — deliberately not carried | absent by decision | **CITED-NOT-USED** (honestly, as a deviation) |
| sk_vig_c003_0013 (vignelli) | "A real corporate identity rests on an overall system rather than on a logo alone … [a logo] should not be discarded" | copy-deck: "the wordmark is the site's own SVG asset, not a string" | `tools/assemble.py` rasterises `source/mokobara/wordmark-white.svg` (sha `c443658f…`) | checker §1: "fresh rsvg-convert … pixel-identical" | APPLIED-VISIBLE |
| sk_mla_0064 (hopkins) vs sk_ogx_0032 | Hopkins: "rules out humour and frivolity"; Ogilvy: "humor can now sell" | 03-CREATIVE A2: "a real tension in Canon, uncompiled; resolved by the brief clause 'would be funny…'" | n/a — a conflict the producer arbitrated by hand | n/a | CITED-NOT-USED (arbitration recorded, not a rule) |

Tally over the 12: 9 APPLIED-VISIBLE (one partial, one as deviation), 1 APPLIED-IN-PLAN-ONLY, 2 CITED-NOT-USED (both honestly labelled). The compiled checks (CA-D1, CA-D2, CA-D7, CA-D9, CA-D11, PA-D1, PA-D4, PA-D5, PA-D7, PA-D9) are applied in `03-CREATIVE.md` A3 as prose ("CA-D1 one dominant cue per beat …"); no code rendered them against the board or prompts — `canon/gate/run_gate.py` was **not** run on this job (no `gate` output in `stages/evidence/`; the workflow §8 asks for it, the job record does not show it). UNKNOWN whether the producer ran it un-recorded.

### 2.3 Was retrieval done by code or by Claude reading? (OBSERVED)

- **Pack lookup: by code**, once, at USD 0 — `stages/evidence/canon-lookup.txt` line: "run: runtime.canon.packs.lookup(runtime.canon.normalize.normalize(brief.job.json minus _provenance))". It returned two packs.
- **The 22 raw claims: by Claude reading the YAML.** `stages/03-CREATIVE.md` L9: "**A2. Accepted claims retrieved by id from `canon/knowledge/current/**`** (text quoted from the source-knowledge files; used for the decisions named)". There is no retrieval function in `runtime/` that returns a SourceKnowledge object by id or by topic (`runtime/canon/` = normalize.py, packs.py, templates.py; none opens `canon/knowledge/current`). The corpus index itself says (`CANON-CORPUS-INDEX.yaml` `retrieval_note`): "Runtime retrieval today reads canon/knowledge/current/** only" — but "runtime retrieval" there means a person or model with a file browser; no code path exists. INFERRED: the producer session grepped/opened files under the eight gap domains and chose claims by judgement — exactly the "model decides whether to consult Canon" pattern CANON-SHAPE §4 says is designed out.
- **Question generation: by hand.** `stages/01-INTENT.md` §1–§3 (mandatory items M1–M7 with verification, decisions with "cost if wrong", "questions that would have changed a decision") is prose written by the producer session following `.claude/skills/media-agency/PRODUCTION-WORKFLOW.md` §5 ("Write `blueprint.*` before any route is chosen … `first_read`, `hook`, `offer`…"). No file in the repo is named `QUESTION-TEMPLATE` (grep over `*.md|*.yaml|*.py` in the sync worktree and the Mokobara worktree: zero hits); the closest is the workflow's blueprint table. There is no code in `runtime/intake/intake.py` (310 lines: schema, consent, kind/profile gates) that derives questions, mandatory items or a board from a brief.
- The Lane A checker confirms the same shape (`stages/CHECK-GATES-1-4.md` L133 @ origin/work/agency-job-rentok-game-lane-a-001): "`runtime.canon.lookup(normalize(brief.job.json))` — reproduces the producer's `canon-lookup.txt` exactly".

---

## 3. ★ What the runtime does unattended vs what Claude did by hand

### 3.1 Can `python3 -m runtime.alpha.cli` take a brief to a paid, delivered artifact today? **No.** (OBSERVED)

- `runtime/alpha/cli.py` docstring: "Nothing is sent anywhere; nothing costs money." Exit 3 on refusal "is a valid result — a precise refusal is the product working".
- `runtime/execute/bridge.py` L16–20: "dispatch_mode dry: every attempt becomes `dry_not_sent`… dispatch_mode live: refuses, in this order — the profile's may_spend() … then the signed record … then, because no transport exists in this tranche, 'live dispatch is not wired'." L432–435, the terminal refusal even with a signed record: *"live dispatch is not wired in this tranche: the profile is adopted and its signed spend authorisation record parsed, and still nothing is sent, because no provider transport exists in runtime/execute and none will be constructed here. Plain statement, not a bug."*
- `runtime/execute/authorisation.py`: "None exists on this branch… Every profile row today says `status: none, record: null`". Confirmed: all four profiles in `runtime/contracts/POLICY-PROFILES.yaml` carry `spend_authority: none` (alpha_human_release adopted/live; alpha_wider_example not adopted; dry adopted; dry_permissive adopted, kinds `__all__`).
- No network client is imported anywhere in `runtime/` outside tests (grep for requests/httpx/anthropic/openai/google/urllib/socket/fastapi/flask: zero non-test hits).
- `runtime/ALPHA-1.md` "Does not exist": "A live dispatch… A real post-draw artifact and a paid text detector… Gate-conformant plate prompts for the frozen Stage-A blueprints… A second usable route for photo edits… A customer-facing API."

Actual runs (OBSERVED, this session, USD 0):
- Fixture `img-text-02-conformant.json --accept`: all nine stages OK, `FINAL STATE: accepted`, but `manifest: would_dispatch=0 (if funded: 2; pool liquidity not_read)`, `dry_execution: network=none`, template `status=reusable_dry_only`. The "plan" came from `planner=recorded_fixture`.
- Mokobara brief, profile `dry`: `REF intake KIND_NOT_IN_PROFILE: deliverable kind 'multi_shot_story' is not in the allowed list of policy profile 'dry'`.
- Mokobara brief, profile `dry_permissive`: intake OK, then `REF spec PLANNER_FIXTURE_MISSING: no recorded reasoning pass for this prompt; the lane will not call a model.` The runtime **has no reasoning-model call at all** (`runtime/spec/planner_seam.py`: "There is no live client here on purpose. This lane spends nothing." Planners: `FixturePlanner` (recorded response keyed by prompt sha), `NoCallPlanner` (refuses everything), `BlueprintPlanner` (parses a frozen Stage-A blueprint)).
- Test suite: `python3 -m unittest discover -s runtime/tests -p 'test_*.py'` → **Ran 520 tests, OK** (320 s). (With `-t .` it errors on 22 import paths — the documented invocation is the one without `-t`.)

### 3.2 Which of the five agency stages has any code in `runtime/`

| Agency stage (workflow §) | Code in runtime? | Evidence |
|---|---|---|
| 1 Intent — parse the brief, list mandatory items, questions | **No.** Schema validation only | `runtime/intake/intake.py`: PRODUCTION-JOB-v1 shape, consent (`depicts_identifiable_person`), kind ∈ profile, motion-requires-accepted-still. No text understanding of `brief.text`. |
| 2 Structure / NR | **Yes** | `runtime/canon/normalize.py` — job → CANON-010 NR via `KIND-NR-BINDING-v0.yaml`, no model |
| 3 Creative — Canon lookup | **Yes** (2 packs) | `runtime/canon/packs.py` (§1.2) |
| 3 Creative — board / blueprint / copy deck | **No.** A seam that replays a fixture | `runtime/spec/planner_seam.py`, `blueprint_planner.py`, `compile.py` — "planner=recorded_fixture / stage_a_blueprint_fixture / template:<id>" |
| 3 Creative — template reuse (empirical memory) | Yes, exact-identity match only | `runtime/canon/templates.py`: "Exact comparison of one sha; no fuzzy matching, no search, no model" |
| 4 Route selection | **Yes**, for spec fixtures | `runtime/route/decision.py` (592 lines), price pins, taint register (`production_use_allowed`), evidence cells; CLI `runtime/route/cli.py` |
| 5 Dispatch | **Dry only** | `runtime/execute/bridge.py` renders bodies via the harness `dry_run()`; pools (`pools.py`) and `provider_errors.classify` exist |
| 5 Pre-dispatch gate | Yes | `runtime/loop/predispatch.py` → `canon.gate.predispatch` (LIMIT-TEXT etc.) |
| 5 Post-draw gate | Yes, on a **synthetic** artifact with a **scripted** detector | `runtime/loop/postdraw.py`, `synthetic.py`; ALPHA-1: "measure nothing; Cloud Vision stays uninvoked" |
| 5 Repair | Bounded, from a failure table | `runtime/loop/repair.py`: `repair_allowance` from the profile; "'Try again' is not a repair" |
| 5 Acceptance state | Yes | `runtime/loop/acceptance.py`: pending_human → accepted/rejected/repair_requested; `release()` only by a named person |
| Close — memory event | Yes | `runtime/loop/memory.py` → OUTCOME-EVENT-v1 (`dry_run: true`) |

Contract ids in `runtime/contracts/` (OBSERVED, `schema:` fields): DELIVERABLE-KINDS-v0, EXECUTION-MANIFEST-v0 (+ additive fields note), OUTCOME-EVENT-v0, OUTCOME-EVENT-v1, PRODUCTION-JOB-v0, PRODUCTION-JOB-v1 (`status: FROZEN_CONTRACT`), POLICY-PROFILES-v0, PRODUCTION-SPEC-v0, PRODUCTION-SPEC-v1, ROUTE-DECISION-v0, TEMPLATE-v0. Battery: `runtime/battery/DRY-ALPHA-BATTERY-2026-09-14.yaml` + `results/2026-09-14/` — 14 dry runs.

### 3.3 The tooling that actually produced media on the five jobs (OBSERVED)

None of it lives in `runtime/`. Each job carries a `tools/` folder on its branch, copied from the previous job with a hand-written provenance table.

| File | Lines (Lane A / V2 / Mokobara) | What it does | Provenance chain (as recorded) | Job-specific vs generic |
|---|---|---|---|---|
| `tools/_common.py` | 135 / 135 / 137 | stdlib urllib transport, key-by-name, scrub, bounded poll | Lane A: "Adapted from tools/reference-kit/_common.py (Cumin Job B kit @ 5c33173)"; rules copied from `eval/harness-v2/adapters/base.py`, `transports.py`. **Lane A and V2 are byte-identical** (sha 22cdc2f6…); Mokobara differs by header only | generic |
| `tools/dispatch.py` | 253 / 253 / 407 | paid dispatch: `reserve()` before send, `settle()` after, `ATTEMPTS.jsonl`, cap check, prompt guard (IP/claim word list, exact-string leak), `route_allowed()`. Providers: Lane A/V2 = nano-banana-2 (Gemini API) + lyria (Vertex); Mokobara adds veo-3.1-fast t2v/i2v/ref2v and gemini-omni. Prices "re-read live from the runtime PriceBook at import" | Lane A: from `tools/reference-kit/dispatch.py` (Cumin Job B @ 5c33173 ← pilot recipes on cases 001/002). Mokobara: from `RENTOK-CREATIVE-QUALITY-001/treatments/tools/dispatch.py @ 41d97c6`, Lyria recipe from Lane A @ 0405feb0 L206–231, Veo shape from `eval/harness-v2/adapters/vertex_veo.py` | ledger/cap/guard generic; ROUTES dict, CAP_USD, word list, copy-deck path per job |
| `tools/render_game.py` | 701 / 701 / — | code renderer for the endless-runner film (sprites, HUD, parallax, pixfont) | written for Lane A; V2 carries it byte-identical | job-specific (RentOK game) |
| `tools/render_v2.py` | — / 936 / — | BOARD-v2-driven renderer: camera crop-and-scale, hit-stop, shake, grade, particles | V2 only, from CQ-001 Treatment C `render_c.py` | job-specific |
| `tools/assemble.py` / `assemble_v2.py` | 65 / 65+48 / 69 | ffmpeg mux: loudnorm two-pass, `-use_editlist 0`, `+faststart`; Mokobara: concat 6 clips + super + end card | Mokobara: flags "carried from V2 `assemble_v2.py` @ ffefe44b" | half generic (mux flags), half job (edit list) |
| `tools/qa_checks.py` | 188 / 224 / 102 | ffprobe geometry/duration/elst/loudness/silence; imports `runtime.compositor.gates` (`check_text_bounds`, `check_contrast`, `check_disjoint`); Mokobara adds 2-fps frame text scan + keyframes | Mokobara: "rewritten for a generated-footage film" from V2 @ ffefe44b | mixed |
| `tools/render_text.py` (Mokobara) / `pixfont.py` (RentOK) | 108 / 169 | code-set exact strings; Mokobara calls `runtime.compositor.gates.check_text_bounds/check_contrast/check_disjoint` at render time and raises `LayoutRefused` | — | generic pattern, per-job layout |
| `tools/paintout.py` (Mokobara) | 21 | strips copied wordmark marks from stills before dispatch | new | job-specific |
| `tools/cutout.py`, `sfx.py`, `sfx_v2.py`, `prompts.py`, `make_board.py`, `preview.py`, `inspect_sheet.py` (RentOK) | 119 / 94+106 / 92 / 195 / 50 / 124 | chroma-key cutouts, square-wave SFX, prompt builders, board→JSON, contact sheets | Lane A → V2 copies | job-specific |
| `tools/reference-kit/` (Lane A) | dispatch 450, vo_schedule_gate 55, overlay_text_video 189 | the Cumin Job B kit, carried but pruned | Cumin Job B @ 5c33173 | generic-ish |

Mokobara `tools/PROVENANCE.md` is the explicit copy record (five rows, each with source path @ commit, sha256 and "change made here"). Same shape on V2 (`PROVENANCE.md` at the job root).

**Duplicated in 3+ places (same function, no runtime home):** the ledger pair `reserve()`/`settle()` with the cap check; `next_attempt_id()`; the prompt guard; key-by-name transport (`_common.py`); the loudnorm/edit-list mux flags; per-job `qa_checks.py` container checks. The runtime has a *different* implementation of some of these ideas (`bridge.py` reservation-first, `pools.py`), which no job tool calls — the job tools call the runtime only for `PriceBook.quote()`, `provider_errors.classify()`, `compositor.gates` and the Canon lookup.

**No runtime home at all:** still→i2v topology and per-beat re-take discipline (Mokobara `RETAKES.md`), the code renderers, SFX synthesis, chroma keying, contact sheets, the assembly EDL, the frame-by-frame checker method (`stages/CHECK-STAGE-5.md`).

---

## 4. Persistence, resumability, failure

**State between steps (OBSERVED):** per-job files on a git branch, all written by the producer session — `JOB.yaml` (schema AGENCY-JOB-v1: `production_status`, `learning_status`, `spend.attempts[]`, `ttao.*`, `qa.defects`, `versions[]`), `gen/LEDGER.jsonl` (reserve/settle lines), `gen/ATTEMPTS.jsonl`, `TTAO-START.yaml`, `stages/0N-*.md`, `board.json`, `copy-deck.json`, `HUMAN-VERDICT-V1.md`. The runtime's own store (`--store DIR`, default a throwaway `tempfile.mkdtemp`) holds JSON per stage for dry runs; `runtime/store/` does not exist in the checkout.

**Resumable job runner / queue / DB / lock:** none. grep over `runtime/` for lock/flock/fcntl/resume/queue/sqlite/redis/threading: only `acceptance.reopen()` (repair_requested → pending_human, L97) and `PreDispatchRefusal`. `AlphaRunner.run()` is one linear pass that "stops at the first refusal" (`run.py` docstring); nothing reads a partially completed run dir back.

**Session end mid-job:**
- The Mokobara collision (OBSERVED): `stages/06-REPAIR-ROUND-1.md` L23: "the b3 clip and the b6 still were dispatched concurrently and both counted the ledger at the same moment, so both were issued `att-020`; the b6 still is relabelled `att-020b` in both files… The dispatch tool should lock the ledger." Root cause in `SYSTEM-DEFECTS.yaml` L21: `next_attempt_id()` = 1 + lines in `ATTEMPTS.jsonl`, "a file appended only at SETTLE. Any attempt that is reserved but not yet settled is invisible to the counter, so the collision window is the full latency of every in-flight call (48–74 s for a Veo clip)". Code: `tools/dispatch.py` L100–102. The fix is a queue candidate, not done (`PROMOTION-QUEUE.yaml` L78: "the kit is copied job to job … so the fault travels").
- The CQ-001 producer dropped on a network error: **UNKNOWN in the repo.** Nothing on `origin/work/experiment-rentok-creative-quality-001` (00-README, 05, 07, evaluation) or in the six cases records a producer session dropping; the only network-outage handling in the codebase is in the Lab harness (commit `26c7716`: "DNS failure before any byte is a pre-dispatch refusal… `run_live plan --redo-from` replans only a previous run's infrastructure-failure trials") — `eval/harness-v2`, not `runtime/`, not the job tools. If the stall happened, its recovery was a human re-issuing instructions to a new session; there is no code path for it.

**Provider failure (OBSERVED):** `runtime/execute/provider_errors.py` `classify()` → `infrastructure_transient` (HTTP 408/425/429/500/502/503/504, gRPC 4/8/13/14, timeout, or words like "unavailable|overloaded|rate limit") with `retry: True`; `provider_refusal` (400/403/422 or "content filter|safety|policy…") `retry: False`; else `unclassified`. Doc: "an outage is not a bad draw… `model_quality_failure` … never by this classifier". But *retry* is only a flag: the job tools do "No hidden retry: a re-send is a new attempt with its own line" (`dispatch.py` header), by the producer's hand. Mokobara att-014 (Lyria http_500, charged 0.06) was re-sent by hand as att-015 with a re-worded prompt.

**Cap exhaustion (OBSERVED, Mokobara `tools/dispatch.py` L113–119):**
```
if CAP_USD <= 0.0 or not CAP_STATED_BY:
    sys.exit("REFUSED: no written spend cap recorded. Nothing sent.")
…
if cum > CAP_USD + 1e-9:
    sys.exit(f"REFUSED: cumulative reserved USD {cum:.4f} would exceed the job cap USD {CAP_USD:.2f}. HARD STOP; nothing sent.")
```
A hard process exit; nothing queues the attempt or asks for more budget.

**Brief change mid-job:** no "reopen at stage N" code anywhere. The only structured answer is prose: the checker's "Failure classification (earliest stage, one repair each)" table (`CHECK-STAGE-5.md` §6, e.g. "D1 … Earliest stage: Stage 4 (route) …") and the case's `REVISION-TRACE.yaml` root-cause classes. The media-agency workflow (`PRODUCTION-WORKFLOW.md`, `SKILL.md`, `QA-CHECKLIST.md`) has no section on brief change, scope change, resume or hand-off (grep: zero hits). The runtime's `repair.py` handles only a failed check/verdict on an existing spec; a changed brief would be a new job.

---

## 5. Independent checking

**Is there code that runs a non-author check?** No orchestration. Every "independent checker" in the five jobs is a fresh Claude session reading a prompt (`CHECK-STAGE-5.md` L3: "Checker: a fresh session that wrote none of the job… Spend: USD 0 (ffprobe/ffmpeg/python only)"). The checker's *instruments* are code; the checker itself is a person-prompted session, and its independence is a process rule, not enforced by anything.

**Deterministic checks that exist as code (OBSERVED):**

| Check | File | Tests |
|---|---|---|
| text bounds / safe box, contrast (WCAG ratio on sampled luminance), fit declaration, card geometry tokens, region disjointness | `runtime/compositor/gates.py` `check_text_bounds`, `check_contrast`, `check_fit`, `check_geometry`, `check_disjoint` (+ `tokens.py`) | `test_i_compositor_gates.py` 24 |
| frame text hygiene (video) | `runtime/loop/frame_hygiene.py` `assess()` | `test_i_frame_hygiene.py` 14 |
| pool availability, transient classification, validate-before-reserve | `runtime/execute/pools.py`, `provider_errors.py`, `bridge.py` | `test_i_pools_and_errors.py`, `test_j…` |
| MP4 edit-list walk (`elst` count, top-level box order, largesize) | `runtime/loop/container.py` `assess_edit_lists` | `test_j_rentok_game_004_005.py` (part of 19) |
| graphic/text disjoint with min gap, VO↔text schedule alignment, brand colour on rendered pixels | `gates.py` `check_graphic_text_disjoint`, `check_vo_text_alignment`, `check_brand_colour` | `test_j_rentok_game_004_005.py` 19 total |
| hero visible (foreground over hero region), framing target at focus frame, world fills frame (camera scale ≥ 1.0), sprite density consistency | `gates.py` `check_hero_visible`, `check_framing_target`, `check_world_fills_frame`, `check_sprite_density` (PR #104, +238 lines) | `test_k_rentok_game_v2_006.py` 17 |
| Canon pre-dispatch / post-draw (LIMIT-TEXT etc.) | `canon/gate/*`, `runtime/loop/predispatch.py`, `postdraw.py` | `test_g_gates.py` 21 |

Adversarial note (OBSERVED): the eight gates promoted on PR #104 (`hero_visible`, `framing_target`, `world_fills_frame`, `sprite_density`, `graphic_text_disjoint`, `vo_text_alignment`, `brand_colour`, `assess_edit_lists`) have **no caller outside their tests** — not in `runtime/loop/driver.py`, not in `runtime/alpha/run.py`, and not in any job's `tools/qa_checks.py` (the RentOK jobs predate them; Mokobara imports only `check_text_bounds/contrast/disjoint`). They are library functions with unit tests, "promoted" in the sense of existing, not in the sense of running on anything.

**LJ (human-judgement) items with no code (OBSERVED from `CHECK-STAGE-5.md` and `01-INTENT.md` verification column):** identity continuity of the character across clips (checker §4, by eye: shirt/beard drift); gag readability ("does the gag read?" M5); claim depiction — does the frame show what the brief said (R2 "kept", R5 "goes back" judged PARTIAL by eye); product likeness vs reference photo (M1, contact sheet by eye); audio by ear (checker: "Speech or singing in the native audio: CANNOT_DETERMINE by code"); resemblance to a specific film (M6 LJ). None of these has a scorer, a threshold, or a test.

---

## 6. Customer-facing surface

- **No API, no UI, no auth (OBSERVED).** grep for fastapi/flask/aiohttp/http.server in `runtime/`: none. Entry points are three argparse CLIs over a brief file: `runtime/cli.py`, `runtime/alpha/cli.py`, `runtime/route/cli.py`. ALPHA-1 "Does not exist": "**A customer-facing API.** The entry point is a CLI over a brief file."
- **Storage:** git branches (one per job) plus a throwaway `--store` directory for dry runs. No database, no object store, no customer record beyond `customer_ref` ("opaque customer/account id; never a person's name").
- **The only intake schema:** `runtime/contracts/PRODUCTION-JOB-v1.yaml` (`status: FROZEN_CONTRACT`). Fields: job_id, received_utc, customer_ref, brief{language, market, text}, exact_text_strings[] (value/script/placement/may_reflow), reference_assets[] (asset_id, content_type, role ∈ product|logo|person|scene|prior_creative|other, provenance, sha256, depicts_identifiable_person), deliverable_request{kind, modality, operation, aspect, count, subject{entity, entity_id, identity_invariants}, motion{from, seconds, audio}}, policy_profile, cost_ceiling_usd, deadline_utc, retention, submitted_by.
  - Reference assets: **yes** (roles incl. `logo`, `prior_creative`; hashed).
  - Brand assets: partially — a logo is a reference asset with `role: logo`; there is no brand kit (palette, typeface, tone) field. The Mokobara job carried these in prose (`stages/02-STRUCTURE.md`, dossier).
  - Revisions: **no** — no `parent_job`, `revision_of`, `feedback`, or version field (grep: none). The Mokobara v2 was recorded as `versions[]` in the agency `JOB.yaml`, not in the contract; the customer's verdict lives in `HUMAN-VERDICT-V1.md` prose.
  - `ambiguity_markers` is refused inside `deliverable_request` on this base (Mokobara `_provenance.schema_note`) and was moved into `_provenance`, which the normaliser strips — so the runtime NR showed `ambiguity: 0` and the uncertainty rule could not fire (§1.2).

---

## 7. Production learning

- **Cases (OBSERVED):** 6 directories under `production-learning/cases/` — UPWORK-INTRO-001, UPWORK-PORTFOLIO-002, RENTOK-GAME-A-004, RENTOK-GAME-B-005, RENTOK-GAME-V2-006, MOKOBARA-ODYSSEY-007. **There is no case 003 in this tree** (numbering skips; UNKNOWN whether it exists elsewhere — the README does not name it). Each case: README, EVIDENCE-MAP.md, OUTCOME, HUMAN-VERDICTS, REVISION-TRACE, ROUTE-OBSERVATIONS, SYSTEM-DEFECTS, PROMOTION-QUEUE, TIME-AND-COST (+ ACCEPTED-TEMPLATE on 5 of 6; 002 is `job_specific`).
- **`production-learning/tools/check_case.py` (434 lines):** structure and honesty only — "never the outcome of any particular job". It checks: OUTCOME names accepted/rejected/abandoned with asset path+commit+sha; REVISION-TRACE uses the eleven root-cause classes; ROUTE-OBSERVATIONS rows are `routing_authority: none` with integer n; PROMOTION-QUEUE "has its four sections"; TIME-AND-COST has one mechanical clock and a CpAO; EVIDENCE-MAP rows resolve with `git cat-file -e` and blob sha256 matches. It does not read the film, the prompts, or judge any claim.
- **PROMOTION-QUEUE counts across the six cases (OBSERVED, computed):**

| case | promoted_now | candidate_patterns | directional_only | canon_gap_candidates | not_promoted |
|---|---|---|---|---|---|
| 001 | 8 | 4 | 6 | 0 | 5 |
| 002 | 5 | 6 | 5 | 0 | 6 |
| 004 | 3 | 9 | 6 | 2 | 5 |
| 005 | 3 | 9 | 9 | 2 | 6 |
| 006 | 4 | 11 | 4 | 1 | 6 |
| 007 | **0** | 16 | 5 | 0 | 9 |
| total | 23 | 55 | 35 | 5 | 37 |

- **What "promoted" means, case by case:** 001's eight and 004/005/006's ten are code in `runtime/` with tests (§5 table; PR #104 = 004/005/006, `git diff --stat origin/main..HEAD -- runtime` = +725 lines: gates.py, container.py, bridge.py, two test files). **Case 002's five "promoted_now" entries are not code** — `kind: process_requirement / qa_requirement / production_system_requirement`, `where: media-agency workflow (PR #99)`; they are rules in a skill document. Case 007 promoted nothing ("each candidate names its check and the missing runtime file"). Who: the sync sessions that wrote PR #98/#99/#104 (Claude), reviewed by the Controller per the case READMEs.
- **Is anything reading the cases at job time?** No. `runtime/canon/templates.py` reads `runtime/store/templates` (its own promoted TEMPLATE-v0 objects from dry runs), never `production-learning/`. The five `ACCEPTED-TEMPLATE.yaml` files are read by no code. `production-learning` appears in `runtime/*.py` only inside docstrings/comments as provenance ("production-learning RENTOK-GAME-A-004, defect D-1"). The workflow's "template-first / learning-first" step (§3) is a person opening the case directory.

---

## 8. Evidence of supported classes (OBSERVED from the six cases)

| Deliverable class | case | n accepted | CpAO (USD, provider spend only; every case says `numerator_complete: false`) | TTAO (mechanical) | Unrepaired on the accepted file |
|---|---|---|---|---|---|
| Presenter film, 57 s, Veo i2v + native speech + Sarvam narration (talking-head class C-7 excludes) | 001 | 1 (V4.1, 5 review cycles) | 15.39 | 7:53:35 (lower bound) | SD-01..12 listed; voice "robotic" per Controller carried into v4.1 via re-record — UNKNOWN which remain |
| Portfolio tile set (9 tiles, deterministic compose over mixed sources) | 002 | 1 set (B3, 5 cycles) | 4.66 for the set (0.518/tile loaded) | 1:07:33 (lower bound, batch) | PD-01..09, SD-HD-01..13 recorded; tile-7 two rejected attempts |
| Code-rendered game film, 30 s, sprites from nano-banana-2, code SFX, Lyria bed, no voice | 004 (Lane A) | 1 (v1, blind) | 0.529 | 1:54:18 | 19 system defects, all closed at USD 0 before presentation; D-1 edit lists, D-2, D-11 repaired |
| Same, with Sarvam announcer voice | 005 (Lane B) | 1 (v1, blind) | 0.587 | 1:53:07 | 21 defects; att-006/013 dropped candidates; two TTS auditions unused |
| Code-rendered *directed* board film (Treatment C), 1 new sheet, everything else reused | 006 | 1 (v1, "its already good") | 0.067 (+0.596 reused assets outside CpAO) | 5:09:28 (0:51:13 to DET-clean file) | N1–N9, P1 offered as a USD-0 repair round and **declined by the customer** — all remain |
| Still→i2v story film, 30 s, 6 Veo clips from nano-banana-2 stills, Lyria bed, no voice | 007 | 1 (v2, after SPECIFIC REPAIR) | 7.857 | 10:23:37 (0:43:29 to v1 DET-clean) | D1 arms only to forearm depth; D5 paddle whereabouts 21–24 s; D8 720p sources upscaled; native audio not ear-checked; DF-3, DF-14 "none" |
| Static overlay ad (Alpha-1's own class) | **none** | 0 | — | — | The only class the runtime is built for has **no accepted production case**; its evidence is the dry battery and the Lab's Stage-A cases |

Routing cells used and `production_use_allowed` (OBSERVED, `eval/capability-map/TAINT-REGISTER-v1.yaml`, 61 cells: 29 true / 17 false / 15 manual_only): nano-banana-2 IMG-CORE **true** (one edit/ref cell `manual_only` — Mokobara used it *with reference images*, which the case itself calls "an unregistered IMG-REF use, micro-qualified for this job"); veo-3.1-fast-i2v **true**; veo-3.1-fast t2v: one cell true, one manual_only; veo-3.1-fast-extend manual_only (used on 001); gemini-omni-1.1-flash: true / manual_only by cell; lyria true; sarvam-bulbul-v3 true; elevenlabs-v3-direct true; gpt-image-2 true; flux-2-pro true/false by cell; kling-v3-pro-i2v true (001), kling-v3-pro-audio false, kling-lipsync-a2v false. Every ROUTE-OBSERVATIONS row in all six cases carries `routing_authority: none` and `evidence_class: directional_production_observation` — by the cases' own rule they change no routing.

---

## What would surprise the founder — every place a document claims more than the code does

1. **"Canon retrieval is deterministic table lookup; the model never decides what to read" (CANON-SHAPE-v1 §4).** True for 2 packs. On the Mokobara job 8 of 10 selected packs returned nothing and the producer session then read 22 raw claims from 13 sources by hand — the exact pattern §4 says was "designed out". Retrieval on real jobs is Claude grepping YAML.
2. **"2 of 10 compiled" is stated in five documents and is a Controller ruling (C-10)** — but the ruling's release condition ("a real runtime failure") cannot occur, because no production job runs through the runtime. The eight uncompiled packs cover the domains a video ad needs most (camera, editing/pacing, colour, commercial communication with 7 critical domains, typography). ~1,300 accepted objects; a few dozen reach a model.
3. **The trigger table fires all ten packs on an ordinary Indian video ad and delivers two.** `canon_gap: True` is the normal state, not the exception.
4. **The compiled packs are PROPOSED in their own headers** ("no Controller decision adopts it") while the runtime labels them `compiled_accepted` because a corpus hash matches. Two meanings of "accepted".
5. **"Alpha-1 chain proven end-to-end"** — proven dry: recorded-fixture plan, synthetic PNG, scripted detector, `would_dispatch=0`, `network=none`. There is no reasoning-model call in the runtime at all (`planner_seam.py`: "no live client here on purpose"). Any new brief without a recorded fixture refuses at `spec` (`PLANNER_FIXTURE_MISSING`) — and writes a file into the repo when it does.
6. **Every accepted deliverable was produced by per-job `tools/` copied branch-to-branch**, not by `runtime/`. The ledger, cap, attempt-id, prompt guard and transport code exist in ≥3 copies; `next_attempt_id()` is a known race (att-020) that "travels" with each copy.
7. **The only class the runtime is built for (static overlay ad) has zero accepted production cases.** All six accepted cases are classes Alpha-1 excludes or omits (presenter film, portfolio tiles, code-rendered game, multi-shot story).
8. **"Independent checker"** = a second Claude session; nothing enforces that it is not the author. Its judgements on identity, gag, claim depiction and audio are by eye/ear with no scorer.
9. **PR #104's eight "promoted" gates have no caller** — not in the loop, not in the alpha runner, not in any job's QA. They are tested library functions. Case 002's five "promoted" items are workflow rules, not code.
10. **Production-learning is write-only at job time.** No code reads the cases or the five `ACCEPTED-TEMPLATE.yaml` files; `templates.py` reads its own dry-run store and matches only on an exact identity hash.
11. **No persistence, resume, lock or queue.** State is Markdown/JSON/YAML on a branch, written by the session. A dropped session is recovered by a human re-briefing a new session; nothing in the repo records the CQ-001 drop (UNKNOWN).
12. **Cap exhaustion is `sys.exit`.** Provider transient errors are classified with `retry: True`, but the retry is a person re-running a command.
13. **A brief change mid-job has no code path**; the workflow documents have no section on it.
14. **Intake covers reference assets but not revisions or a brand kit**; `ambiguity_markers` cannot be carried in `deliverable_request` on this base, so the uncertainty rule (the "Gemma 0/18 lesson") was silently inert on Mokobara.
15. **The taint register is descriptive.** Mokobara's core still route (nano-banana-2 *with* reference photos) is a `manual_only` / unregistered use; the cases label every route row `routing_authority: none`, so five accepted jobs have moved the routing map by exactly nothing, by design.
16. **CpAO figures are provider spend only** — every case says `numerator_complete: false` (no LLM session tokens, no human time); TTAO on 001/002 are lower bounds; 007's 10 h 23 m is mostly waiting for the customer.

**What I did not check (UNKNOWN):** whether `canon/gate/run_gate.py` was run on Mokobara un-recorded; the harness `eval/harness-v2` live path (out of scope; the workflow says paid dispatch uses it); the content of case 003 if it exists elsewhere; the Chrome/Upwork side of cases 001/002.
