# Checker verdict — Gates 1–4 (lane A)

Job `AGY-2026-09-20-RENTOK-GAME-LANE-A-001` · branch `work/agency-job-rentok-game-lane-a-001` · checked 2026-09-21 by an independent session that wrote none of the records below.
Method: every answer is checked against the records in this job directory (inputs, stage files, `board.json`, `copy-deck.json`, `JOB.yaml`, `source/`, `tools/`). USD-0 commands re-run by the checker are listed at the end. No paid call was made; no producer file was edited.

**Communication check:** I will explain technical ideas in plain English, including what they mean, why they matter, and their practical consequence; use minimum sufficient wording without sacrificing understandability; separate evidence from inference; and never invent facts. I have read `shared/COMMUNICATION-STANDARD.md`.

Vocabulary used below: OBSERVED = seen by the checker in a file or command output · INFERRED = the checker's reading of what was observed · REOPENED = a producer answer that must be redone before that question counts as closed · NOTE = non-blocking.

---

## Gate 1 — Intent contract — **PASS WITH NOTES**

Criterion: nothing invented; every mandatory item has a verification method.

**Q1 — requirements trace to customer sentences.** OBSERVED: every requirement in `01-INTENT.md` §1.1–1.5, 1.8, 1.10 quotes the frozen brief verbatim; M1–M11 in table 1.4 each carry a customer quotation. The only requirement-shaped values not from the customer are 1080×1920 / MP4 / H.264-AAC, and the record says where they come from (the Controller's acceptance contract A8, re-verified at Stage 2). Non-customer forbidden items (no live filming, no stock, no fal, no prior RentOK material) are labelled "Controller, governance not creative". Nothing was promoted from an assumption into a requirement.

**Q2 — six intent statements and five obstacles.** OBSERVED: platform-game feel → M1; PG owner recognisable → M2; obstacles = genuine problems → M3; install = turning point → M4; enhanced ability, used, flag reached → M5 + M6; communicates relevance → M10; the two "do not" statements → 1.5 forbidden list + M11. The five obstacles are in ONE row (M3) with a per-obstacle LJ checklist and a DET check that all five label strings render. INFERRED: acceptable — each obstacle is individually checkable — but see NOTE 1.

**Q3 — verification method per mandatory item.** OBSERVED: all eleven rows have one (DET where a file can be measured: M3 labels, M4 timecode + string, M5 asset ledger, M6 timeline, M7 ffprobe, M8 ffprobe + safe-box, M11 string scan; LJ named as "the checker session … never the author"; HJ = the customer blind). No row is empty.

**Q4 — delegated decisions and "do not" lines.** OBSERVED: visual treatment = D3 (cost: creative-direction repair ≈ USD 0.07–0.20 + dependents, mitigated by drawing the character first); power-up design = D4 / flag F3 (cost: one sprite swap ≈ USD 0.07–0.13). Testimonial / generic SaaS ad / lifestyle film and the three guarantee claims are in `contract.forbidden`.

**Q5 — anything asked of the customer.** OBSERVED: `JOB.yaml questions_asked: []`; the one open ask is the Controller's written cap. Nothing is deferred to the customer.

NOTES (non-blocking)
1. M3 bundles five obstacles into one row. The verification still covers each one (DET per label, LJ per obstacle), so this passes; a Stage 5 checker should score the five separately, as the acceptance contract A3 says ("per-obstacle checklist").
2. M4's DET says the install event must land "inside the middle third" (10–20 s). The board puts the panel at 15.0 s and the install moment at 17.4 s — inside, but in the back half of that window. Fine by the rule; just noting the film's "turn" happens at 58 % of runtime, not 50 %.

---

## Gate 2 — Structure — **PASS WITH NOTES**

Criterion: every fact has a source; nothing platform-specific asserted from memory.

**Q6 — platform specs.** OBSERVED (checker re-read the files): the Meta extracts carry SOURCE URL, TITLE and FETCHED UTC in their headers and contain the exact lines the record quotes (9:16, H.264 + AAC 128 kbps+, 1440×2560, 4 GB, 0 s–15 min / no maximum, no edit lists, minimum width 500 px for ≥ 30 s). YouTube: "maximum resolution of 1080p", "up to 3 minutes", MP4, no edit lists, moov first, 48 kHz, High profile, 4:2:0, 8 Mbps, 384 kbps — all present in the saved `.txt`, and the three `.html` files verify against `SHA256SUMS.txt`. Safe zones: 14 % / 35 % / 6 % quoted from both Meta pages; YouTube's 288 / 672 / 48 / 192 px margins are the text labels inside the saved figure `yt-vertical-safe-area-figure.svg` (checker extracted them). The arithmetic (269 / 672 / 65 px; intersection (65,288)–(888,1248)) is correct. Values that are decisions, not facts (30 fps, 192 kbps audio, ≈ 8–10 Mbps, −14 LUFS), are labelled as decisions inside sourced ranges.
   One record defect: `02-STRUCTURE.md` §2.2 says the safe-area page's sha256 is "in `SHA256SUMS.txt`" — OBSERVED it is not (the sums file lists 8 entries; `yt-vertical-safe-area.html/.txt/-figure.svg` are absent). The files exist; checker-computed sha256: html `e9109a41adde7f4a237ba7d2d64d570816ef8a3b2257fc73adee1b39df2c96d2`, txt `a221c3bdcd4232024fc5cbff9155cb4622b319392eee4803b90ec406d67c30e5`, svg `689512b5239f84cc5f51185259e9f57c404c48ca8a8f3d4d0099c216f0ba4afd`. See NOTE 3.

**Q7 — product facts.** OBSERVED by grep over `source/rentok-snapshot/*.txt`: every quoted line in the 2.4 table exists at the cited file:line (Digital KYC home:99; Police Verification home:96 / tenant-verification:51–53; real-time verification tracking tv:60; Autopay home:19–20, autopay:4–5, 58–59; reminders / WhatsApp link / late fine home:86–88; filled-vacant-under-notice home:104; Rent Not Paid / Tenants Not Paid autopay:104–107; Pending Dues autopay:136; retries autopay:232; Digital Accountant home:89; Excel reports home:92; UTR home:94; one dashboard autopay:95; complaint tickets cm:10; auto-assigned cm:49; flagged cm:48; live status cm:51). The five clearing chips in `copy-deck.json` map to these lines. The permitted list contains no guarantee, number or outcome; the forbidden list covers guarantee / 100 % / never / prevent / recover / eliminate / all problems / any %. The Eqaro "Zero Deposit / 100 % Claim" block (home:110–115) is explicitly NOT used, and the site's own line "Timely issue resolution prevents tenants from leaving" (cm:177) is explicitly excluded because the customer forbids that claim. Correct handling.
   Depiction the site does not support: the clearing of obstacle 3 (F9.3, "a tick tags him; he **freezes**") shows RentOk stopping a tenant who is leaving. The site offers tracking, ledger, reminders, late fine — not stopping anyone. The chip text (`✓ DUES TRACKED LIVE`) is honest; the picture is not. Raised under Gate 3 (REOPENED 3-A) because it is a board question.

**Q8 — IP rules.** OBSERVED: the 2c table is concrete per element (character, power-up, obstacles, world, flag, HUD, music, words) and the dispatch tool refuses any prompt containing the Nintendo names (checker-proven, see Gate 4). Residual risks the checker names, all INFERRED:
   - Ground "plain ochre brick" tiles: a brown/ochre brick-pattern ground is one of the most recognisable elements of the original 1-1 level. Recommend a lane/road or plain stone texture without a brick bond.
   - The floating `?` above the document wall (F2): keep it a bare question mark, never a yellow block.
   - The flagpole: the customer's "gets the flag" is inherently reminiscent; the producer's version (flag rises, no castle, no descent animation) is the right direction. Keep the pole plain (no ball finial) and the flag rectangular in RentOk blue.
   - The "chip ding" and the fleeing tenant's coin bag: the SFX are code-synthesised (no sampled jingle), which is the right control; the audio must be checked by ear against the coin/1-up jingles at Stage 5.
   - Pixel-art with 2-px outlines and a health bar is genre, not Nintendo property. No block.

**Q9 — brand spelling.** OBSERVED: the site never writes "RentOK" (checker grep: zero hits, case-sensitive); it writes "RentOk". Decision: raster wordmark carries "RentOk"; all typed strings are capitals (`RENTOK`), which is spelling-neutral and matches the customer's own capitals. Justified, cost if wrong USD 0.

NOTES (non-blocking)
3. Add the three safe-area files to `source/platform/SHA256SUMS.txt` (checker values above) so the §2.2 sentence becomes true. USD 0.
4. The Meta pages are the *ads* specs, recorded as such with the limitation that no organic-Reels spec page could be fetched. Acceptable; the values used are the conservative intersection.

---

## Gate 3 — Creative package — **PASS WITH NOTES** (two questions REOPENED, both USD-0 record fixes)

Criterion: a board exists; a non-author has answered the structure checklist against it. This file is that answer.

**Q10 — numbered board summing to 30.0 s.** OBSERVED (checker summed `board.json`): 15 frames F1–F11 (F9 split into F9.1–F9.5), contiguous with no gaps or overlaps, durations 1.8 + 2.8 + 2.8 + 2.8 + 2.4 + 2.4 + 3.0 + 1.6 + 1.2×5 + 2.0 + 2.4 = **30.0 s**. `03-CREATIVE.md` Part D matches the JSON.

**Q11 — numbered hero frame.** OBSERVED: F9.2, t = 21.40 s, `hero: true` in `board.json`. This is a frame, not a sentence. INFERRED: whether the picture alone says "app-powered owner clears the rent problem" depends on sprites that do not exist yet (a padlocked sack bursting under a cyan tick, an aura'd figure with keys, the phone icon in the HUD). The producer says this itself (3.13). The frame is accepted as the hero; its no-copy claim is tested at the Stage 5 contact sheet.

**Q12 — every mandatory event on a numbered frame.** OBSERVED in `board.json` `mandatory[]` and Part D: PG owner as player F1 (HUD `PG OWNER` + keys + register) · obstacles 1–5 on F2–F6 · install cheat code F7 (17.4 s) · enhanced ability F8 (aura + projectile + phone icon) · obstacles overcome F9.1–F9.5 (five clears) · flag F10 (26.6 s) · brand + CTA F11. All present.

**Q13 — platform game, not a promo with game graphics.** Evidence FROM THE BOARD: level geometry (rooftop blocks with a gap jumped at F1, a ground line at y 1130 with scrolling tiles, a flagpole at the level end) · HUD (`PG OWNER`, five health segments that fall 5→0 and refill, `LEVEL 1`) · player movement (run, 0.5-s jump arcs at F1/F3/F10, 60-px knock-back on hit, white hit-flash) · collision and interaction (obstacles block/hit/escape; projectiles burst obstacles into pixel debris; chips fly to a checklist) · a game pause for the cheat-code panel. Counter-evidence, INFERRED: the first half is an auto-runner where the owner loses to every obstacle on cue — closer to an "endless runner" than to a jump-over-enemies platformer; only three jumps in 30 s. The acceptance contract's own definition of A1 (side-scrolling level, player character, obstacles, HUD, flag) is met. Whether it *feels* like a game is exactly what the USD-0 animatic exists to test — see NOTE 5.

**Q14 — copy deck and copy zones.** OBSERVED: every string on every board frame is in `copy-deck.json` and every deck string is on a frame (checker set comparison: no differences). The raster wordmark's baked-in tagline is declared in `raster_marks.contains_text`. Widths re-measured by the checker with `tools/pixfont.py`: `TENANT VERIFICATION` / `LEFT WITHOUT PAYING` 791×49 px at scale 7, `RENTOK APP` 590×70 at scale 10, chips 678×42 at scale 6 — all fit the 823-px safe box when centred on the box (the audition centres on the box, not the canvas). Copy zones: labels at y ≈ 720 sit above the play band (owner/obstacles y 900–1130); HUD at y 300–345 inside the box; nothing planned on the character, obstacles or phone. Two zone problems found — REOPENED 3-B and NOTE 6.

**Q15 — Canon honesty.** OBSERVED: the pack lookup re-run by the checker on `brief.job.json` reproduces exactly (10 selected, 2 injected, 8 gaps, prefix sha256 `4d7a5b27…`, 5,298 tokens, 21 check ids). 14 of the 23 cited claim ids were opened in `canon/knowledge/current/**` across every domain the producer lists — `sk_abcd_0007/0011/0026`, `sk_ogx_0039`, `sk_sb_c003_0008`, `sk_whip_0011`, `sk_hea_mts_0018`, `sk_hop_sa_0026`, `sk_gote_c003_0004`, `sk_gos_c003_0007`, `sk_murch_c003_0013`, `sk_wcag_0001`, `sk_vig_c003_0013`, `sk_ogl_c003_0014` — and each claim text matches the producer's abridgement (e.g. sk_abcd_0011: "introduced from the start of the ad and its presence maintained across the ad's whole length … an early appearance that then lapses does not satisfy it"; sk_hop_sa_0026: "A picture in an advertisement must be a salesman in itself and earn the space it occupies"). `qa_abcd_0011` is not in `knowledge/current` — it lives in `canon/qa/canon-014/google-abcd-video-ads-qa-bank.yaml`, and the producer labelled it "Q&A bank, ungraded". Honest. Declared gaps are real: checker grep for "platform game", "platformer", "arcade", "pixel art", "chiptune", "video game", "side-scroll" in `knowledge/current` = 0 hits each; `pack-triggers-v0.yaml` line 77 confirms "zero packs and zero accepted sources cover audio".

**Q16 — answers that are claims rather than frames/lines.** The producer's own 3.13 list is accurate (contrast not yet measured; identity-cue strength a prediction). The checker adds:
   - A3 `CA-D10: pass` states "each [hold] ending when its label has been readable ≥ 1.0 s", but the board shows the re-entered obstacle labels for **0.4 s** in the clearing run (F9.1–F9.5). The producer's reason (labels already known; the chip is the new information and persists) is sound, but the check-line basis as written is contradicted by the board. → NOTE 5 (restate the basis; verify at the animatic). Not reopened because the contract element (chip readable, persistent) is on the board.
   - Every other 3.x answer is a frame, a line, a timecode or a measured width. 3.8 (on-screen = spoken) is trivially met with `vo_lines: []`.

**Q17 — power-up fidelity and relevance of clearing.** OBSERVED: aura (visible change) + cyan tick projectiles fired forward ("gun sort of" without a firearm) + immunity (contact no longer costs health) — the customer's mechanic is preserved and none of it is a Nintendo item (no mushroom/star/flower). Clearing relevance per obstacle: F9.1 paper wall bursts → `✓ DIGITAL KYC` (relevant: digital KYC replaces paper) · F9.2 padlocked sack bursts → `✓ AUTOPAY` (acceptable) · F9.4 ledger tower becomes one neat stack/screen → `✓ ONE DASHBOARD` (the best of the five: the picture shows what the product does) · F9.5 red tickets turn green → `✓ COMPLAINT TICKETS` (relevant: tickets resolved) · **F9.3 fleeing tenant "freezes"** → depicts prevention, which the customer forbids and the site does not offer → REOPENED 3-A.

REOPENED (each must be closed in the record before the animatic is inspected; both are USD 0)
- **3-A (3.7 / M6 / M11 for obstacle 3, frame F9.3).** Missing: a clearing image that matches what RentOk actually does about a tenant leaving without paying (dues tracked, ledger, reminders, late fine, under-notice status — Stage 2b). "He freezes" is a picture of *stopping* the tenant. What closes it: rewrite F9.3 in `03-CREATIVE.md` Part D and `board.json` `beat` so the tenant keeps going but is *tagged* — e.g. the tick sticks a ledger line / dues marker to him that stays visible as he exits, the chip `✓ DUES TRACKED LIVE` lands, health unchanged. Same sprite, code choreography only.
- **3-B (3.9 copy zones, frame F10).** Missing: a disjoint position for `LEVEL CLEAR!`. OBSERVED: state flashes are "centred at y ≈ 560"; the checklist column occupies x 90 → ≈ 768, y 400 → 640 from F9 onward and "persists"; at F10 all five chips are visible, so a 568-px-wide flash at y 532–588 lands on chip rows. What closes it: state the F10 rule — hide the checklist during F10, or move `LEVEL CLEAR!` to the label zone (y ≈ 720) — and record the y value in the layout constants. The Stage 5 disjointness gate would catch this anyway; the plan should not carry a known collision.

NOTES (non-blocking)
5. Clearing-run tempo (1.2 s per obstacle: enter, hit, burst, chip flight, chip read) is the film's biggest pacing risk and is not covered by any Canon claim. The producer's USD-0 animatic (Stage 4 A0) is the right test; the checker should look specifically at whether five clears in 6 s read at phone size, and whether the 0.4-s label flash is a help or a flicker. Restate the CA-D10 basis to say the chip, not the label, is the ≥ 1.0-s readable element.
6. End card: the wordmark at "≈ 700 px wide centred" must be centred on the safe box (x 126–826), not the canvas (x 190–890 would cross the 888-px right edge by 2 px). Record which. Also: the HUD line `PG OWNER ▮▮▮▮▮` (498 px at scale 6) plus the 150-px chip at x 738–888 leaves ≈ 175 px between them — fine, but `LEVEL 1` must be a centre flash, not a third HUD element, or the row overflows (the audition's single-line HUD is 822 px of 823).
7. The audition PNG shows `RENTOK.COM` outside the box only because the audition stacks ten lines vertically and runs out of height; it is not a design fact. In the film the URL is one of three lines on the end card.

---

## Gate 4 — Production selection — **PASS WITH NOTES — conditional; the gate is NOT closed for spend**

Criterion: riskiest element tested first; every route has evidence or a test; balances read/attested. The third part is unmet (by the producer's own record), so no paid call may be made until it is.

**Q18 — method reasoned from this plan.** OBSERVED §4.0: code animation chosen for four stated requirements — one character identical for 30 s, readable in-game text on every frame, projectile hits at exact times, 30.0 s exactly — with the reasons generative video cannot meet them (4–15-s clips; identity drift case 002 RO-02 / case 001 RO-02; in-motion text EVAL-038, RR-6). Generative models are limited to textless stills; the powered state is a code recolour of the same bitmap so identity cannot drift. Reasoned, not name-driven.

**Q19 — routes, cells, prices, pools.** OBSERVED, re-quoted live by the checker from the runtime PriceBook: nano-banana-2 USD 0.067 per_image credits · nano-banana-pro USD 0.134 per_image credits · lyria USD 0.06 per_clip credits — identical to the plan. Routing table (`stages/evidence/routing-table.txt`): IMG-CORE/nano-banana-2 clean_observed, True, 7/8; MUS/lyria+native clean_observed, True, 4/4; fallback IMG-CORE/nano-banana-pro clean_observed, True, 4/8 with "on the Controller's OK" recorded. No `False` cell, no `manual_only` cell, no fal route, no cash pool. Two surface facts to keep visible: (a) the map lists nano-banana-2 on `vertex`; the tool calls the Gemini API with `GOOGLE_API_KEY` (as cases 001/002 did, case 002 RO-04 = a 9:16 textless plate on that surface, 1/1 clean); (b) Lyria authenticates with a service-account file `~/.aight-litellm-keys/vertex-sa.json` on project `vertexaiproject-507518`. Two different credentials → the Controller's pool reading (Q4.8) must confirm both draw on the credits pool named for this job. NOTE 8 on the 9:16 plate cell.

**Q20 — riskiest capability first.** OBSERVED §4.1: rank 1 = the PG-owner sprite sheet, with evidence (case 001 RO-04: nb2 drew handwriting-like marks despite a no-text clause, 1/2; and a declared GAP: no evidence anywhere for multi-pose sprite-sheet consistency or a keyable flat background → `test`). Micro-qualification defined (one draw USD 0.067, cut-out, placed at 220 px on the animatic, five named pass criteria, freeze by sha256, fallback after two failures). Order of work: USD-0 animatic → pre-dispatch checks → A1 sprite sheet → verdict → dependents. Correct.

**Q21 — text.** OBSERVED: every string is rendered by `tools/pixfont.py` (an original code bitmap font; checker ran `coverage`: no missing glyphs). No in-model text is planned anywhere. Post-draw scan: every still by eye plus the gate path; sampled frames of the assembled film (the case 001 SD-06 lesson); Cloud Vision not authorised, so the frame scan is human-eye — stated. The dispatch tool refuses any prompt containing a deck string or lacking a no-lettering clause (checker-proven below).

**Q22 — spend.** OBSERVED and re-added: base 0.067 + 5×0.067 + 0.067 + 0.060 = **0.529**; repair round 0.067 + 2×0.067 + 0.067 + 0.060 = 0.328 → **0.857**; + 3×0.067 customer-repair reserve = **1.058** = 10.6 % of the provisional USD 10.00. Cut list stated for ≤ 1.00 / ≤ 0.60 / ≤ 0.30 / 0. One arithmetic slip: the plan says "17 calls"; 8 + 5 + 3 = **16** (the USD totals are right).

**Q23 — QA plan.** OBSERVED §4.12: A1–A11 each map to a named check — DET by ffprobe for duration/geometry/codec/moov (A7, A8), byte-exact string presence in the layout log (A3, A4, A5), event log (A6), forbidden-substring scan (A11), prompt-guard log (A9); LJ by the checker on the contact sheet for A1, A2, A3 (per obstacle), A4–A6, A8 safe-zone visual, A9 IP table, A11 visual; HJ = customer for A1, A2, A4–A6, A10. Complete.

**Q24 — `tools/dispatch.py`.** OBSERVED by reading and by running it at USD 0: `CAP_USD = 0.0`, `CAP_STATED_BY = None`; `reserve()` refuses when either is unset, checks cumulative reserved against the cap, and appends the ledger line BEFORE the request leaves; `settle()` appends after, failed calls included; `failure()` classifies via `runtime/execute/provider_errors.classify`; `ROUTES` contains only `nano-banana-2` and `lyria`; no fal code path (`_common.py` keeps `FAL_KEY` only in the scrub list so a stray value never prints). Checker test results (no network, no `gen/` directory created): prompt with "mario" → `REFUSED: forbidden IP word`; prompt containing `COLLECTING RENT` → `REFUSED: exact copy-deck string`; prompt without a no-text clause → `REFUSED: … LIMIT-TEXT`; clean prompt → `REFUSED: no written spend cap recorded`. The "refusals proven" claim in §4 is now independently true.

Why the gate is not closed: `JOB.yaml spend.cap = null` and `spend.pool_readings = []`. The producer records both as unresolved and blocks its own dispatch on them (PROVIDER_POOL_AVAILABILITY, case 001 SD-11). Both are Controller inputs, not producer defects.

REOPENED — none for the producer. Two items for the **Controller** before any paid call:
- **4-A (1.9 / spend.cap).** Missing: the written cap (amount, currency, stated_by, stated_utc, covers, retries_allowed 0) in `JOB.yaml spend.cap`, then `CAP_USD` / `CAP_STATED_BY` in `tools/dispatch.py`.
- **4-B (4.8 / pool_readings).** Missing: a read balance for the Google credits pool (value, read_utc, source) — and confirmation that BOTH credentials the tool uses (Gemini API key; the Vertex service account) draw on that pool.

NOTES (non-blocking)
8. The 9:16 background plate (A7) is routed under the general clean cell IMG-CORE/nano-banana-2. A more specific cell, VID-TOPO3/nano-banana-2+A2_nb_plate_9x16, is `directional_only / manual_only 1/2` — but that cell records the plate as one step of a still-to-video topology, which this plan does not use, and case 002 RO-04 (1/1 clean 9:16 plate on the same surface) supports the draw. Acceptable, with the code-drawn plate as a USD-0 fallback; record the cell choice reasoning in one line.
9. `JOB.yaml plan.micro_qualifications[0].checker_inspected: true` is set before any inspection exists. It should read `false`/`null` until this checker (or the Stage 5 checker) records a verdict on the drawn sheet.
10. The A1 draw has no reference image, so the character depends on the prompt alone; obstacle draws may optionally use the accepted sheet as one style reference, which the plan correctly marks as an unregistered reference use requiring its own micro-qualification. Keep it that way.

---

## Summary for the Controller (plain English)

This lane is about to make a 30-second vertical film that is a small, original, code-rendered side-scrolling game: a pixel-art PG owner (keys at his belt, ledger under his arm) runs into five obstacles named exactly as the customer named them, loses all his health, gets the cheat code "INSTALL / RENTOK APP", and then — immune and firing cyan tick-marks — clears the same five obstacles, each clear stamping a product feature the website actually offers, and reaches the flag; the film closes on the RentOk wordmark and the same install call. Every word on screen is typed by code (no AI-drawn lettering), all product statements trace to a line of the frozen website snapshot, the guarantee-type claims the customer forbade are on a scan list, and the Nintendo-specific elements are excluded by a written table plus a tool that refuses prompts containing those names. Gates 1–3 pass with two small record fixes (the "leaving tenant" clear must show tracking, not stopping; a text collision on the flag frame) and Gate 4's plan is sound, cheap (≈ USD 0.53 base, ≈ USD 1.06 worst case) and tests the riskiest thing first — but **it may not proceed to paid production yet**: the written spend cap and a read balance for the Google credits pool are both still missing, and the dispatch tool correctly refuses everything until they exist. The two biggest risks I see: (1) the single AI-drawn character sheet — if the four poses do not read as one person with visible keys and ledger at 220 px, the whole look must be redrawn (the plan tests this first for USD 0.067, which is the right mitigation); (2) whether the piece *feels* like a game rather than a scripted runner with game furniture, especially the clearing run at 1.2 s per obstacle — a creative-quality judgment no Canon covers, which only the USD-0 animatic and then the customer can answer.

---

## USD-0 commands the checker ran (all read-only against this worktree)

- `shasum -a 256 -c` on `source/platform`, `source/rentok-snapshot`, `source/rentok-brand` — all OK; the three safe-area files hashed separately (values above).
- `grep` of every cited product line in `source/rentok-snapshot/*.txt`; case-sensitive grep for "RentOK" (0 hits).
- Text labels extracted from `yt-vertical-safe-area-figure.svg` (288 / 672 / 48 / 192 / 1080x1920).
- Board sum, contiguity, deck ⇄ board string set comparison, forbidden-substring scan over the deck (no hits), install/flag timecodes — a short Python script over `board.json` and `copy-deck.json`.
- `runtime.canon.lookup(normalize(brief.job.json))` — reproduces the producer's `canon-lookup.txt` exactly; `git status` clean afterwards.
- `build_router()[0].prices.quote(...)` for nano-banana-2, nano-banana-pro, lyria — match the plan.
- `tools/pixfont.py coverage copy-deck.json` (none missing) and `audition` to the checker's scratchpad.
- Import of `tools/dispatch.py` and four `nb2()` calls that each exit at the guards before any network use; no `gen/` directory created.
- grep of `canon/knowledge/current/**` for the cited claim ids and for the declared-gap topics; grep of `production-learning/cases/*/` for RO-02/03/04/05/06/09 and SD-05/06/10/11/13 (all exist and say what the producer says).
