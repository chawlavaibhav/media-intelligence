# What has actually been going wrong — 225 defects, nine jobs, read end to end

*Media Intelligence · 22 September 2026 · findings only, no plan. Source: `FAILURE-ATLAS-RAW.yaml`. Every row, with its bucket, is in `FAILURE-ATLAS-CLASSIFIED.yaml`.*

## How to read this

Every one of the 225 recorded defects has been put into exactly one of ten buckets. The buckets are named after **the mechanism that produced the failure** — what would have had to be different for it not to happen — not after what it looked like on screen. Two defects that look identical ("text is unreadable") sit in different buckets if one happened because a rule we had was never measured and the other because nobody ever wrote the rule.

The buckets were derived from the rows, not imposed on them. Inside each bucket the rows carry a **failure mode** — the same label wherever the same mechanism appears — so we can count how often a thing came back.

## The ten buckets

| # | Bucket | Rows | Jobs | What it means |
| --- | --- | ---: | ---: | --- |
| B1 | **Declared output rule never measured on the rendered file** | 62 | 8 | We had the rule and shipped without measuring it on the finished file. |
| B8 | **Process, orchestration, records and spend** | 35 | 9 | The machinery around the work: no frozen plan before spending, bypassed runtime, colliding ids, records that disagree, our own measuring tools wrong. |
| B6 | **Not good enough by human judgement** | 31 | 7 | Nothing was broken. The work just was not good enough for the person looking at it. |
| B2 | **Generative output never checked against its own prompt** | 26 | 8 | We told a model to do something, it did something else, and nothing read the result back against the instruction. |
| B7 | **A route asked for work its qualification never covered** | 19 | 7 | We bought a route for work its qualification never covered — a longer line, a longer clip, another language, a style it cannot hold. |
| B4 | **The plan never said it** | 17 | 7 | The board simply never said it — no check could have caught it, because there was no rule to check. |
| B3 | **Nothing binds one generated asset to the next** | 12 | 6 | Each shot was made on its own, so the man, the bag, the props, the voice and the style were free to change between them. |
| B10 | **A check that could not, or did not, run** | 12 | 6 | The check was named and then could not, or did not, run — above all: nobody can listen to the audio. |
| B9 | **Provider-side failure outside our control** | 8 | 5 | The provider failed, refused or ran out of quota. Not a creative decision. |
| B5 | **A claim about the real world asserted, never sourced** | 3 | 3 | We stated something about the real product or brand that was not true, or drew the product doing something it cannot do. |

One example in the record's own words for each:

- **B1 — Declared output rule never measured on the rendered file.** UPW2-10: “"9:16 offer-in-motion clip — '15% OFF' runs off the panel" / customer: "9X 16 motion is getting text cutoff."”
- **B8 — Process, orchestration, records and spend.** UPW2-01: “no normalized request, blueprint, acceptance contract or route plan existed before the first paid call of the batch”
- **B6 — Not good enough by human judgement.** UPW1-22: “"competent, not extraordinary" (verdict rebuild_direction)”
- **B2 — Generative output never checked against its own prompt.** MOKO7-07: “att-024: coconut in, lid closed at 1.5 s, then the model RE-OPENED the bag for 2-4 s — 1.9 s usable”
- **B7 — A route asked for work its qualification never covered.** UPW1-05: “narration judged horribly robotic [Sarvam bulbul:v3 chosen for ~48 s of continuous narration on the strength of Lab evidence gathered on <= 70-character lines]”
- **B4 — The plan never said it.** MDR8-05: “also, it looks like a drain and not sea.”
- **B3 — Nothing binds one generated asset to the next.** MDR8-01: “two person. the chracter was young and then gotten old”
- **B10 — A check that could not, or did not, run.** MDR8-12: “audio content by ear (is there any speech or singing?) — NOT CHECKED — I cannot listen ... this needs a human ear or a speech detector before release”
- **B9 — Provider-side failure outside our control.** UPW1-09: “Vertex Veo returned gRPC 14 UNAVAILABLE twice, then succeeded 100 s later”
- **B5 — A claim about the real world asserted, never sourced.** MDR8-03: “"it also opens weirdly. i dont think so there is a zip there" — board asserted "ONE long zip running the full height of the bag's side"; the product page says "180 degree flat opening"”

## The point of the exercise: what came back

Of 104 distinct failure modes, **39 appeared in more than one job** and 65 have been seen once so far. The 39 repeats break down like this:

| Classification | Modes | Meaning |
| --- | ---: | --- |
| RECURRED-NOTE-ONLY | **16** | The "fix" was prose — a candidate pattern, a directional note, a paragraph in a case file. It came back. |
| RECURRED-NO-FIX | 11 | Recorded, nothing done, came back. |
| RECURRED-DESPITE-CODE | 8 | A real code gate existed and it happened anyway — bypassed, or scoped too narrowly to catch the next form of it. |
| PREVENTED | 4 | The promoted code caught the same condition in a later job before it cost anything. |

**The headline number is 16.** 16 of the 39 repeated mechanisms had been "fixed" by writing something down, and writing it down did not stop them. Add the 11 where nothing at all was done and 27 of 39 repeats — 69% — never had a machine standing behind them. Only 4 mechanisms in the whole programme can be shown to have been stopped by a fix.

### The recurrence table

Jobs in date order: 001 Upwork intro (14 Sep) → 002 Upwork portfolio (15 Sep) → 003 Cumin Co. (15–16 Sep) → 004/005 RentOk A and B (20–21 Sep) → CQ1 quality probe (21 Sep) → 006 RentOk V2 (21 Sep) → 007 Mokobara (21–22 Sep) → today's rejected Mokobara film (22 Sep).

| Failure mode | Bucket | First seen | What was done about it | Came back in | Verdict |
| --- | --- | --- | --- | --- | --- |
| no human ear on the delivered audio | B10 | 004 (RGA4-26) | nothing — 004 recorded it open ('directional_only'); at 005 a written pattern VOICE_CAST_BY_A_HUMAN_EAR was raised as a candidate and never became code | 005 (RGB5-10, RGB5-27); CQ1 (CQ1-21); 006 (RGV6-24); 007 (MOKO7-16); today (MDR8-12) | **RECURRED-NOTE-ONLY** |
| element overlap collision | B1 | 001 (UPW1-07) | ELEMENT_DISJOINTNESS promoted_now after 001 | 002 (UPW2-17, UPW2-18, UPW2-19); 004 (RGA4-05, RGA4-21); 005 (RGB5-02, RGB5-15, RGB5-16); 006 (RGV6-10) | **RECURRED-DESPITE-CODE** |
| prompt instruction ignored by the model | B2 | 001 (UPW1-27, UPW1-30) | nothing — 001 accepted it and filed 'directional_only — RO-01, routing_authority none' | CQ1 (CQ1-16); 006 (RGV6-18); 007 (MOKO7-06, MOKO7-08); today (MDR8-02, MDR8-07) | **RECURRED-NO-FIX** |
| hero or key content occluded | B1 | 001 (UPW1-26) | 001 repaired in V4.1, not_promoted; GRAPHIC_TEXT_DISJOINT promoted_now after 004 | 004 (RGA4-02); 005 (RGB5-01); CQ1 (CQ1-08); 006 (RGV6-01, RGV6-02) | **RECURRED-DESPITE-CODE** |
| overall verdict not good enough | B6 | 001 (UPW1-22) | nothing — not_promoted | 003 (CUM3-17); CQ1 (CQ1-20); 007 (MOKO7-23); today (MDR8-15) | **RECURRED-NO-FIX** |
| records inconsistent between files | B8 | 004 (RGA4-19, RGA4-22) | fixed by hand in 004 ('one pass over both files'), not_promoted | 005 (RGB5-08, RGB5-12, RGB5-22); 006 (RGV6-23, RGV6-26); 007 (MOKO7-17) | **RECURRED-NO-FIX** |
| route cannot meet the demand | B7 | 001 (UPW1-28) | directional_only — RO-03, n=1 (a Registry note with routing_authority none) | 003 (CUM3-14, CUM3-15); 005 (RGB5-28); today (MDR8-14) | **RECURRED-NOTE-ONLY** |
| codec true peak overshoot | B1 | 004 (RGA4-10) | pre-encode target lowered inside 004; CODEC_TRUE_PEAK_MARGIN raised as a candidate and never promoted | 005 (RGB5-14); CQ1 (CQ1-15); 006 (RGV6-12) | **RECURRED-NOTE-ONLY** |
| unrequested object in frame | B2 | 001 (UPW1-31) | directional_only — RO-08 after 001 | 002 (UPW2-24); CQ1 (CQ1-14); 007 (MOKO7-05) | **RECURRED-NOTE-ONLY** |
| effect or payoff reads weak at phone size | B6 | 004 (RGA4-24) | nothing — not_promoted at 004 | CQ1 (CQ1-01, CQ1-09, CQ1-10); 006 (RGV6-20, RGV6-21) | **RECURRED-NO-FIX** |
| proof or subject reads too small | B6 | 001 (UPW1-14, UPW1-20) | nothing — not_promoted | 004 (RGA4-09, RGA4-25); CQ1 (CQ1-03) | **RECURRED-NO-FIX** |
| voice route shipped without a human ear on the real demand | B7 | 001 (UPW1-05) | SPEAKER_MICROQUALIFICATION — candidate_pattern after 001; VOICE_BY_EAR_FIRST — candidate after 003 | 003 (CUM3-10, CUM3-11, CUM3-12); 005 (RGB5-25) | **RECURRED-NOTE-ONLY** |
| unrequested lettering in frame | B2 | 001 (UPW1-06, UPW1-29) | VIDEO_FRAME_TEXT_HYGIENE promoted_now after 001 | 005 (RGB5-09); CQ1 (CQ1-06) | **RECURRED-DESPITE-CODE** |
| audio hole at a clip join | B1 | 002 (UPW2-22) | 002 promoted CROSS_CLIP_VOICE_CONTINUITY (identity, not silence); the hole itself only ever drew a candidate | 005 (RGB5-21); 007 (MOKO7-03) | **RECURRED-NOTE-ONLY** |
| text contrast on background | B1 | 001 (UPW1-02) | CONTRAST_GATE promoted_now after 001 | 002 (UPW2-13); 007 (MOKO7-04) | **RECURRED-DESPITE-CODE** |
| copy over photographic content | B1 | 002 (UPW2-12, UPW2-14, UPW2-16) | REJECTED_DESIGN_REUSE and FORMAT_SPECIFIC_REVALIDATION promoted_now after 002 | 003 (CUM3-04) | **RECURRED-DESPITE-CODE** |
| brand colour measured wrong on the frame | B1 | 004 (RGA4-03, RGA4-17) | BRAND_COLOUR_ON_RENDERED_FRAME promoted_now after 004 | 006 (RGV6-17) | **RECURRED-DESPITE-CODE** |
| character identity drifts between shots | B3 | 007 (MOKO7-12) | directional_only — RO-01; left UNREPAIRED on the accepted 007 film | today (MDR8-01, MDR8-10) | **RECURRED-NOTE-ONLY** |
| crop cuts the subject | B1 | 001 (UPW1-03) | CROP_FIT_DECLARATION promoted_now after 001 | 002 (UPW2-15, UPW2-20) | **RECURRED-DESPITE-CODE** |
| element leaves the safe box | B1 | 004 (RGA4-06, RGA4-07) | LAYOUT_LOG_GATES — candidate after 004 | 005 (RGB5-13) | **RECURRED-NOTE-ONLY** |
| mandatory event never happens on screen | B2 | 007 (MOKO7-02, MOKO7-11) | MANDATORY_EVENT_VISIBILITY_LJ_LINE — class 2 candidate after 007 | today (MDR8-13) | **RECURRED-NOTE-ONLY** |
| pacing wrong | B6 | 001 (UPW1-16, UPW1-23) | nothing — not_promoted | 007 (MOKO7-22) | **RECURRED-NO-FIX** |
| provider transient 5xx or unavailable | B9 | 001 (UPW1-09, UPW1-10) | TRANSIENT_ERROR_CLASSIFICATION promoted_now after 001 | 007 (MOKO7-13) | **PREVENTED** |
| renderer capability limit | B7 | CQ1 (CQ1-11, CQ1-23) | documented in TREATMENT-C.md, not_promoted | 006 (RGV6-19) | **RECURRED-NOTE-ONLY** |
| world not composed across the full frame | B4 | 004 (RGA4-16) | COMPOSE_WORLD_ACROSS_THE_FULL_FRAME — candidate after 004 | 005 (RGB5-19, RGB5-26) | **RECURRED-NOTE-ONLY** |
| ad structure element missing from the board | B4 | 001 (UPW1-24) | nothing — not_promoted at 001 | 003 (CUM3-07) | **RECURRED-NO-FIX** |
| attempt id collision | B8 | 003 (CUM3-06) | ATTEMPT_ID_LOCK — candidate; the record says explicitly 'not fixed in code on this job' | 007 (MOKO7-01) | **RECURRED-NOTE-ONLY** |
| container spec violation | B1 | 004 (RGA4-01) | CONTAINER_EDIT_LIST_CHECK promoted_now after 004 | 006 (RGV6-08) | **PREVENTED** |
| coverage asserted but never verified | B10 | 004 (RGA4-27) | nothing — not_promoted | CQ1 (CQ1-24) | **RECURRED-NO-FIX** |
| keying residue on a cut out | B1 | 004 (RGA4-08) | KEYING_HELPER — candidate after 004 | 006 (RGV6-14) | **RECURRED-NOTE-ONLY** |
| layer order error | B1 | 005 (RGB5-18) | 005 repaired it in place, not_promoted; GRAPHIC_TEXT_DISJOINT from 004 was already in code | 006 (RGV6-09) | **PREVENTED** |
| our own measuring instrument was wrong | B8 | 004 (RGA4-11) | fixed in the job's own script, not_promoted | 006 (RGV6-03) | **RECURRED-NO-FIX** |
| our qa instrument is unreliable | B10 | 005 (RGB5-29) | noted only (directional) after 005 | 007 (MOKO7-14) | **RECURRED-NOTE-ONLY** |
| picture depicts a capability the product lacks | B5 | 004 (RGA4-20) | fixed at the gate at USD 0, not_promoted | 005 (RGB5-24) | **RECURRED-NO-FIX** |
| provider content refusal false positive | B9 | 003 (CUM3-13) | directional_only — RO-03, n=12 after 003 | 005 (RGB5-07) | **RECURRED-NOTE-ONLY** |
| spend authorisation or cap missing | B8 | 002 (UPW2-08) | PAID_PRODUCTION_PREFLIGHT promoted_now after 002 | 004 (RGA4-23) | **PREVENTED** |
| spend records incomplete or unreconciled | B8 | 001 (UPW1-32) | nothing — not_promoted | 002 (UPW2-26) | **RECURRED-NO-FIX** |
| supplied brand mark copied or mangled by the model | B2 | 003 (CUM3-01) | a candidate prompt clause ('turn the mark away') after 003 | 007 (MOKO7-24) | **RECURRED-NOTE-ONLY** |
| text out of bounds | B1 | 001 (UPW1-01) | TEXT_BOUNDS_GATE promoted_now after 001 | 002 (UPW2-10) | **RECURRED-DESPITE-CODE** |

### The same table, in the record's own words

A repeat is only counted when the *mechanism* is the same, not the symptom. Both verbatims are quoted so the claim can be checked.

**no human ear on the delivered audio** — RECURRED-NOTE-ONLY · bucket B10

- *first, 004 RentOk A* — RGA4-26: “"the paid text detector was not run — recorded NOT_RUN" / "the checker could not listen — the customer's ACCEPT is the only ear on it"”
- *again, 005 RentOk B* — RGB5-10: “code-synthesised 'power-up chime', 'hurt blip' and 'coin-like' stamp sounds can drift towards the famous motifs by accident — the QA plan has no explicit by-ear check on SFX/music against Nintendo motifs”
- *again, 005 RentOk B* — RGB5-27: “Sound remains unheard by anyone — the one open check”
- *again, CQ1 quality probe* — CQ1-21: “a human should listen to those two stretches to be sure [speech-band level within 1 dB of full band]”
- *again, 006 RentOk V2* — RGV6-24: “"obstacle 3 is not visibly stopped and obstacle 5's payoff reads weakly" / "sound by ear (LJ-14) and the melody's originality — both CANNOT_DETERMINE from this session"”
- *again, 007 Mokobara* — MOKO7-16: “speech or singing in the native Veo audio was never checked by a human on v1 or v2; no local recogniser ... the producer 'heard none on a quick listen'”
- *again, today Mokobara deepread* — MDR8-12: “audio content by ear (is there any speech or singing?) — NOT CHECKED — I cannot listen ... this needs a human ear or a speech detector before release”
- Response after the first: nothing — 004 recorded it open ('directional_only'); at 005 a written pattern VOICE_CAST_BY_A_HUMAN_EAR was raised as a candidate and never became code.
- Note: The single most repeated mode in the atlas: six jobs, seven rows. MDR8-12 itself says 'same gap as MOKO7-16 and RGB5-27'.

**element overlap collision** — RECURRED-DESPITE-CODE · bucket B1

- *first, 001 Upwork intro* — UPW1-07: “offer pill and code line collided to the eye”
- *again, 002 Upwork portfolio* — UPW2-17: “GyaanBox 1:1 — the offer pill on the seam cuts the plant”
- *again, 002 Upwork portfolio* — UPW2-18: “Dhaba contact sheet 2 — banner overlapping the photos”
- *again, 002 Upwork portfolio* — UPW2-19: “all GyaanBox files — banner overlapping the photos”
- *again, 004 RentOk A* — RGA4-05: “checklist chip backings overlapped, 171 frames [row pitch 48 < backing 62 px]”
- *again, 004 RentOk A* — RGA4-21: “Two zone problems found — REOPENED 3-B and NOTE 6 [a text collision on the flag frame]”
- *again, 005 RentOk B* — RGB5-02: “the O5 beam ran 8 px under the name tag at 23.9-24.1 s”
- *again, 005 RentOk B* — RGB5-15: “name tag rode up with the jump into the label plate”
- *again, 005 RentOk B* — RGB5-16: “cheat bar 8 px above the name tag”
- *again, 006 RentOk V2* — RGV6-10: “the toppling tower's far corner rose 46 px into the label zone (2 frames); the departing swarm crossed the HUD row”
- Response after the first: ELEMENT_DISJOINTNESS promoted_now after 001.
- Note: Recurred in 002 with the runtime bypassed, then repeatedly inside 004/005/006 where the layout-log gates caught it before delivery.

**prompt instruction ignored by the model** — RECURRED-NO-FIX · bucket B2

- *first, 001 Upwork intro* — UPW1-27: “framing drifted slightly wider than the still; a hand entered the frame edge briefly despite 'hands out of frame'”
- *first, 001 Upwork intro* — UPW1-30: “two scene instructions partly ignored (diya placement, 'dark burgundy' world)”
- *again, CQ1 quality probe* — CQ1-16: “the finished cheat code 'INSTALL RENTOK APP' is on screen for exactly one frame (1/30 s) before the box clears”
- *again, 006 RentOk V2* — RGV6-18: “cell 1 'standing and looking back over his left shoulder' came out facing forward with raised eyebrows and an open mouth; used 0.25 s”
- *again, 007 Mokobara* — MOKO7-06: “take 1 (4 s): one coconut in, zip closed with fish, rope, gourd, flare and two coconuts still out; take 2 (6 s, 'EVERY item goes in'): fish, rope, flare in, coconuts + gourd out at the zip”
- *again, 007 Mokobara* — MOKO7-08: “the one change that emptied the shore also produced a hard in-model cut at 1.54 s to a static full-length portrait looking into the lens, a sleeved buttoned shirt ... and no marked rock in the wide; no pull-back exists”
- *again, today Mokobara deepread* — MDR8-02: “bag was not closed/zipped properly- AI slops”
- *again, today Mokobara deepread* — MDR8-07: “bag standing upright in the surf, clean, no yellow visible [board asked for half-buried in wet sand, side-on, one thread of yellow]”
- Response after the first: nothing — 001 accepted it and filed 'directional_only — RO-01, routing_authority none'.
- Note: Five jobs. No check ever reads a returned asset back against the instruction that bought it.

**hero or key content occluded** — RECURRED-DESPITE-CODE · bucket B1

- *first, 001 Upwork intro* — UPW1-26: “speaker bubble persisted over hero creative — read as a watermark”
- *again, 004 RentOk A* — RGA4-02: “the raised flag — the customer's 'gets the flag' payoff — was hidden behind the checklist and `LEVEL CLEAR!` for 27.2-27.6 s”
- *again, 005 RentOk B* — RGB5-01: “the phone graphic rose over the PG OWNER name tag 14.9-15.3 s, hiding most of the final R on the brand-moment frame”
- *again, CQ1 quality probe* — CQ1-08: “the cheat box slides up over the character for a few frames (f012) and a translucent ghost of the box hangs over the scene after the flash (f037)”
- *again, 006 RentOk V2* — RGV6-01: “the flag rises THROUGH the cheering owner for 26 frames, 26.53-27.37 s ... the triumph beat shows the hero half-hidden by a blue rectangle”
- *again, 006 RentOk V2* — RGV6-02: “the raised phone sits exactly over the owner's head for 6 frames, 18.20-18.37 s, at 'rising confidence'”
- Response after the first: 001 repaired in V4.1, not_promoted; GRAPHIC_TEXT_DISJOINT promoted_now after 004.
- Note: The promoted gate measures graphic-vs-text, so 006's graphic-over-hero cases (RGV6-01/02) passed it.

**overall verdict not good enough** — RECURRED-NO-FIX · bucket B6

- *first, 001 Upwork intro* — UPW1-22: “"competent, not extraordinary" (verdict rebuild_direction)”
- *again, 003 Cumin Co.* — CUM3-17: “FAILED — no version accepted; the last rejection was on assembly audio (VO lines overlapping), the previous on ad structure, the first on mix / mouths / text placement”
- *again, CQ1 quality probe* — CQ1-20: “neither [clip-1 nor clip-4] would be accepted as-is”
- *again, 007 Mokobara* — MOKO7-23: “As a paid placement: not yet — the arms gag, the packing leftovers, the non-departure and the beat-1 costume would each draw a note from a brand manager”
- *again, today Mokobara deepread* — MDR8-15: “A1 the bag is recognisably the Transit Backpack in every beat — NO; A2 the gag reads — NO; A3 with sound off the story reads — PARTIAL ... the changing man breaks it”
- Response after the first: nothing — not_promoted.
- Note: The bar-miss verdict itself, five jobs.

**records inconsistent between files** — RECURRED-NO-FIX · bucket B8

- *first, 004 RentOk A* — RGA4-19: “ATTEMPTS.jsonl verdict pending vs JOB.yaml accepted; frozen_asset null; checker_inspected false”
- *first, 004 RentOk A* — RGA4-22: “02-STRUCTURE.md §2.2 says the safe-area page's sha256 is 'in SHA256SUMS.txt' — OBSERVED it is not (the sums file lists 8 entries; three files are absent)”
- *again, 005 RentOk B* — RGB5-08: “the PriceBook roster labels sarvam-bulbul-v3 and elevenlabs-v3 billing_pool: cash, while the routing map lists sarvam_credits / elevenlabs_credits”
- *again, 005 RentOk B* — RGB5-12: “the IMG-CORE cell's registered surface is `vertex` but the tool calls the Gemini API ... whether that key bills the same credit pool is not established in the record”
- *again, 005 RentOk B* — RGB5-22: “ATTEMPTS.jsonl verdicts all pending vs JOB.yaml”
- *again, 006 RentOk V2* — RGV6-23: “Records: 'back by 4.4' vs 4.9; 'one white frame' vs two [Stage 3 table] — a records mismatch, not a film defect”
- *again, 006 RentOk V2* — RGV6-26: “JOB.yaml and LEARNING-PACKET.yaml say the customer declined a round for 'six recorded defects'; the checker's table records N1-N9 + P1 (ten) ... Which six were put to the customer is chat-only and NOT on disk”
- *again, 007 Mokobara* — MOKO7-17: “presented_utc for v2 (18:37:00Z) precedes the repair round's qa_complete (18:38:34Z) by 94 s; versions[] carries a stale duplicate v2 entry ... first_pass_usd 3.529 omits the counted 0.06 failure (ledger 3.589)”
- Response after the first: fixed by hand in 004 ('one pass over both files'), not_promoted.
- Note: Four jobs; every time repaired by hand, never by code.

**route cannot meet the demand** — RECURRED-NOTE-ONLY · bucket B7

- *first, 001 Upwork intro* — UPW1-28: “transcript not verbatim (inserted 'make'); timbre judged synthetic/robotic ... scored 45/60; rejected on this job”
- *again, 003 Cumin Co.* — CUM3-14: “rejected by ear; no Indian-English premade voice on the account; quota exhausted at 54 credits”
- *again, 003 Cumin Co.* — CUM3-15: “two-shots animate mouths unless told 'nobody speaks, mouths closed' and even then open-mouth laughter persisted ~1.2 s from a plate that had it baked in”
- *again, 005 RentOk B* — RGB5-28: “the four run cells differed only slightly in leg phase (motion had to come from code bob/tilt)”
- *again, today Mokobara deepread* — MDR8-14: “arms-in-bag failed 4 paid attempts; carried instead by a pole twice the bag's length”
- Response after the first: directional_only — RO-03, n=1 (a Registry note with routing_authority none).

**codec true peak overshoot** — RECURRED-NOTE-ONLY · bucket B1

- *first, 004 RentOk A* — RGA4-10: “AAC true peak -0.4 / -0.3 dBTP after encoding a -2.6 dBTP wav (target <= -1)”
- *again, 005 RentOk B* — RGB5-14: “TP +0.6 dBTP after loudnorm; then +1.9 dB AAC overshoot”
- *again, CQ1 quality probe* — CQ1-15: “True peak -0.2 dBTP — over the -1 dBTP limit”
- *again, 006 RentOk V2* — RGV6-12: “true peak -0.4 dBTP after AAC with Lane A's loudnorm settings (TP -4 pre-encode) — denser SFX overshoot more”
- Response after the first: pre-encode target lowered inside 004; CODEC_TRUE_PEAK_MARGIN raised as a candidate and never promoted.
- Note: Four jobs, each one re-derived its own margin by hand (-4, -3.6, -6 dBFS).

**unrequested object in frame** — RECURRED-NOTE-ONLY · bucket B2

- *first, 001 Upwork intro* — UPW1-31: “FLUX.2 Pro 0/1 (extra rice bowl, no copy space) — GPT Image 2 redraw accepted”
- *again, 002 Upwork portfolio* — UPW2-24: “steam wisps grew strong in the last 3 s (noted, not rejected)”
- *again, CQ1 quality probe* — CQ1-14: “one or two unrequested elements per draw (duplicate book 2/3, spark flash 2/3)”
- *again, 007 Mokobara* — MOKO7-05: “the open bag with yellow showing lies at his feet before he has found it — the prompt never mentioned the bag”
- Response after the first: directional_only — RO-08 after 001.

**effect or payoff reads weak at phone size** — RECURRED-NO-FIX · bucket B6

- *first, 004 RentOk A* — RGA4-24: “the 'gun sort of power' reads as a small cyan dot and the app itself is a blue rectangle on screen for a third of a second — the transformation is told by words more than shown by picture”
- *again, CQ1 quality probe* — CQ1-01: “power is a thin cyan outline and a fingernail-sized tick ... invisible at phone width, so the paper wall appears to dissolve on its own”
- *again, CQ1 quality probe* — CQ1-09: “its 'power' is a projectile the size of a fingernail and the wall fades away rather than breaking, so the payoff feels like a label rather than a win ... a customer would ask 'where is the power?'”
- *again, CQ1 quality probe* — CQ1-10: “the chip lasts 0.4 s and disappears before the end, and the power is hard to see at phone width”
- *again, 006 RentOk V2* — RGV6-20: “Do not read: the ledger tag on the runner (3 — a 60-px card over a man who simply keeps running away), the swarm flip (5 — red -> olive ... reads as 'muddied', not 'solved')”
- *again, 006 RentOk V2* — RGV6-21: “the muzzle flash is a small sparkle, the tick is a dot with a faint trail, the shockwave ring is thin, and the bursts are speckle — modest at 1080, faint on a phone”
- Response after the first: nothing — not_promoted at 004.
- Note: CQ1 was commissioned to diagnose exactly this and it still shipped in 006.

**proof or subject reads too small** — RECURRED-NO-FIX · bucket B6

- *first, 001 Upwork intro* — UPW1-14: “actual video proof too small; too much phone/mockup framing”
- *first, 001 Upwork intro* — UPW1-20: “still cautious phone/mockup presentation”
- *again, 004 RentOk A* — RGA4-09: “sprites read small at phone size [the checker still called the sprites small at 360 px (§7); the customer did not]”
- *again, 004 RentOk A* — RGA4-25: “the bottom 40 % of every frame is an empty brown band and the sprites are small in the middle of a tall phone screen, which at Reels size can feel like a game viewed from too far away”
- *again, CQ1 quality probe* — CQ1-03: “a plainer backdrop than clip-2 and the smallest sprite of the four, so less to look at ... the small sprite makes the product moment even easier to miss”
- Response after the first: nothing — not_promoted.

**voice route shipped without a human ear on the real demand** — RECURRED-NOTE-ONLY · bucket B7

- *first, 001 Upwork intro* — UPW1-05: “narration judged horribly robotic [Sarvam bulbul:v3 chosen for ~48 s of continuous narration on the strength of Lab evidence gathered on <= 70-character lines]”
- *again, 003 Cumin Co.* — CUM3-10: “"we could use hidi comfoting voice. all three are robotic" (Sarvam priya/shreya, ElevenLabs Sarah)”
- *again, 003 Cumin Co.* — CUM3-11: “stick to english. but voices are not good. at all. why ae we not using veo models with voice? ... i also dont agree on voice being an issue”
- *again, 003 Cumin Co.* — CUM3-12: “leda is good. a little slower though. the shrillness and excitement is still miissing.”
- *again, 005 RentOk B* — RGB5-25: “'vidoe one has robotic voice over' — the customer, blind [the first human ear on the voice]”
- Response after the first: SPEAKER_MICROQUALIFICATION — candidate_pattern after 001; VOICE_BY_EAR_FIRST — candidate after 003.
- Note: Three jobs; by 005 the customer was still the first human ear on the voice.

**unrequested lettering in frame** — RECURRED-DESPITE-CODE · bucket B2

- *first, 001 Upwork intro* — UPW1-06: “Kling i2v clip showed letter-shaped signage although the source still was text-clean”
- *first, 001 Upwork intro* — UPW1-29: “r1 drew blurred handwriting-like sheets on the wall despite the no-text instruction”
- *again, 005 RentOk B* — RGB5-09: “the world contains a 'PG' nameplate on the building ... So the nameplate is either model-drawn text (contradicts §4.4 'no text generated') or does not exist (then G2's identifier list is wrong)”
- *again, CQ1 quality probe* — CQ1-06: “an extra 'COLLECTING RENT' label intrudes at the end (f069)”
- Response after the first: VIDEO_FRAME_TEXT_HYGIENE promoted_now after 001.
- Note: 005 caught it at the gate before spend; CQ1 still shipped a clip with an intruding label.

**audio hole at a clip join** — RECURRED-NOTE-ONLY · bucket B1

- *first, 002 Upwork portfolio* — UPW2-22: “"Nivaas v1 — narration line 2 split by a 2.9-s hole across the extend; 720p images soft/generic; statics cut from video frames" / customer: "all nivas homes are pathetic. voice not continous, images that are scarppy."”
- *again, 005 RentOk B* — RGB5-21: “0.6 s near-silence between V1 and V2 (14.1-14.7 s)”
- *again, 007 Mokobara* — MOKO7-03: “at the 3.5-s and 7.5-s cuts the incoming clip's native ambience sits ~15-20 dB below the outgoing for the first ~40 ms then recovers — a faint hole”
- Response after the first: 002 promoted CROSS_CLIP_VOICE_CONTINUITY (identity, not silence); the hole itself only ever drew a candidate.
- Note: Three jobs; nothing measures level or silence across a join.

**text contrast on background** — RECURRED-DESPITE-CODE · bucket B1

- *first, 001 Upwork intro* — UPW1-02: “text colour lost against photographic backgrounds”
- *again, 002 Upwork portfolio* — UPW2-13: “all Kora files — cream type on a light beige wall, hard to read, unfinished”
- *again, 007 Mokobara* — MOKO7-04: “"wordmark super = the site's white SVG at 300 px on a grey backing box; end card text in Avenir Next" / customer: "use mokobara logo/name properly", "the text font style could be better"”
- Response after the first: CONTRAST_GATE promoted_now after 001.
- Note: 002's record states the gate existed and was NOT RUN; 007 placed a white wordmark at 1.3:1 on a grey box.

**copy over photographic content** — RECURRED-DESPITE-CODE · bucket B1

- *first, 002 Upwork portfolio* — UPW2-12: “Kora hook 1 in 1:1 / 4:5 / 9:16 / WA — headline over the figure and garment”
- *first, 002 Upwork portfolio* — UPW2-14: “Dhaba 47 1:1 — Hindi copy over the food; colour combination poor”
- *first, 002 Upwork portfolio* — UPW2-16: “Dhaba 47 WA — same copy-over-photo defect”
- *again, 003 Cumin Co.* — CUM3-04: “"text and cards over chopsticks/noodles" / customer: "the text is coming on figures"”
- Response after the first: REJECTED_DESIGN_REUSE and FORMAT_SPECIFIC_REVALIDATION promoted_now after 002.
- Note: 003 ran alongside 002 in time, so read this as at best contemporaneous code; the customer found it again on video frames.

**brand colour measured wrong on the frame** — RECURRED-DESPITE-CODE · bucket B1

- *first, 004 RentOk A* — RGA4-03: “the repair for D-8 sampled pixel (100,100) of the logo raster — a fully transparent rounded corner — so the end card and the 0.3-s freeze-dim rendered black (0,0,0) instead of brand blue”
- *first, 004 RentOk A* — RGA4-17: “faint rectangle: the logo raster's card blue vs #0038FF”
- *again, 006 RentOk V2* — RGV6-17: “the wordmark raster's own gradient backing is faintly visible against the card blue: card (1,55,253); raster box (1,54,250) -> (0,40,231)”
- Response after the first: BRAND_COLOUR_ON_RENDERED_FRAME promoted_now after 004.
- Note: 006 found the wordmark raster's own gradient against the card blue — the record calls it 'a sampling-plan gap, not a gate gap'.

**character identity drifts between shots** — RECURRED-NOTE-ONLY · bucket B3

- *first, 007 Mokobara* — MOKO7-12: “beard jet-black/fuller in beat 1 vs grey-streaked in beats 3-4; bracelet on the right wrist in beats 2, 4, 5 (anchor: left); the bag's top opens as a hinged lid at 16.5 s and the front pocket hangs open downward at 22.5 s”
- *again, today Mokobara deepread* — MDR8-01: “two person. the chracter was young and then gotten old”
- *again, today Mokobara deepread* — MDR8-10: “'The EXACT same man' in every prompt — FAIL — at least three distinct men: b2 (young, dark), b3 (older, grey-bearded), b4 (the hero still's man)”
- Response after the first: directional_only — RO-01; left UNREPAIRED on the accepted 007 film.
- Note: Recurred the next day and is the first line of today's rejection.

**crop cuts the subject** — RECURRED-DESPITE-CODE · bucket B1

- *first, 001 Upwork intro* — UPW1-03: “creatives cropped in wrappers and full-screen slots”
- *again, 002 Upwork portfolio* — UPW2-15: “Dhaba 47 9:16 — the dal bowl cut at the right edge”
- *again, 002 Upwork portfolio* — UPW2-20: “IronLeaf — packshot lid cut by the cover crop; then a visible rectangle behind the contained packshot; then a dark halo (operator-caught over three renders)”
- Response after the first: CROP_FIT_DECLARATION promoted_now after 001.
- Note: 002's record states the rule existed and was NOT APPLIED.

**element leaves the safe box** — RECURRED-NOTE-ONLY · bucket B1

- *first, 004 RentOk A* — RGA4-06: “cheat-panel text left the safe box during slide-out, 33 frames”
- *first, 004 RentOk A* — RGA4-07: “chip flight start outside the safe box, 29 frames”
- *again, 005 RentOk B* — RGB5-13: “first render: a 1031-px card, a CTA 1 px outside the safe box, two 3-10 px overlaps”
- Response after the first: LAYOUT_LOG_GATES — candidate after 004.
- Note: Caught before delivery in both jobs, so nothing shipped; the gate is still a candidate.

**mandatory event never happens on screen** — RECURRED-NOTE-ONLY · bucket B2

- *first, 007 Mokobara* — MOKO7-02: “v1 beat 6 (att-013): he stands knee-deep beside the raft for all 4 s ... the customer's mandatory 'goes back' never happens on screen”
- *first, 007 Mokobara* — MOKO7-11: “both hands inside the open bag at wrist-to-forearm depth ... no frame with an arm past the elbow, no chin on the rim ... Stage 5's LJ-3 overstated what the take contains”
- *again, today Mokobara deepread* — MDR8-13: “the hand-repaired strap is visible in b1; the *touch* that says 'his' was never shot”
- Response after the first: MANDATORY_EVENT_VISIBILITY_LJ_LINE — class 2 candidate after 007.
- Note: Recurred the next day in today's job.

**pacing wrong** — RECURRED-NO-FIX · bucket B6

- *first, 001 Upwork intro* — UPW1-16: “presenter blocks too long”
- *first, 001 Upwork intro* — UPW1-23: “pacing too rushed to focus on one creative”
- *again, 007 Mokobara* — MOKO7-22: “5 s set-up / 2.5 s payoff is the wrong ratio ... The 5 s of ordinary rummaging before it is the weak stretch: nothing impossible happens, so the disbelief is not built before the paddle”
- Response after the first: nothing — not_promoted.

**provider transient 5xx or unavailable** — PREVENTED · bucket B9

- *first, 001 Upwork intro* — UPW1-09: “Vertex Veo returned gRPC 14 UNAVAILABLE twice, then succeeded 100 s later”
- *first, 001 Upwork intro* — UPW1-10: “Lyria HTTP 503 / 500 / 500 on the frozen prompt; neutral rewrite succeeded first time”
- *again, 007 Mokobara* — MOKO7-13: “att-014 HTTP 500 'Could not generate audio. Please try again with a different prompt.' ... counted USD 0.06; att-015 with [neutral wording] ok in 60.7 s”
- Response after the first: TRANSIENT_ERROR_CLASSIFICATION promoted_now after 001.
- Note: 007 hit a Lyria HTTP 500 and the promoted classification handled it — 'worked as designed, not re-promoted'.

**renderer capability limit** — RECURRED-NOTE-ONLY · bucket B7

- *first, CQ1 quality probe* — CQ1-11: “the states cut rather than flow, so not a 5”
- *first, CQ1 quality probe* — CQ1-23: “the renderer's remaining gaps (secondary motion, true contact, squash-and-stretch on pixel art) are documented in TREATMENT-C.md and do not go away”
- *again, 006 RentOk V2* — RGV6-19: “Rigid bitmaps: no secondary motion, no squash-and-stretch on the character, two-frame run cycle, contact stood in by overlap (producer-recorded §5.6)”
- Response after the first: documented in TREATMENT-C.md, not_promoted.
- Note: The CQ1 record predicts it: 'recurs as RGV6-19'.

**world not composed across the full frame** — RECURRED-NOTE-ONLY · bucket B4

- *first, 004 RentOk A* — RGA4-16: “lower 40 % of every gameplay frame a plain ochre lane [the world was composed only inside the safe box]”
- *again, 005 RentOk B* — RGB5-19: “lower third of every game frame empty road — a 16:9 plate in a 9:16 frame; 640 near-uniform rows (33 %)”
- *again, 005 RentOk B* — RGB5-26: “N-3 the foreground band is sparse ... about a third of the picture below the action is scenery, kept so the player's feet stay inside the Meta safe box”
- Response after the first: COMPOSE_WORLD_ACROSS_THE_FULL_FRAME — candidate after 004.

**ad structure element missing from the board** — RECURRED-NO-FIX · bucket B4

- *first, 001 Upwork intro* — UPW1-24: “no direct-to-camera speaker ... became a hard requirement”
- *again, 003 Cumin Co.* — CUM3-07: “"no product hero, no end card, no brand early/throughout, no Direction — 'does not look like an ad'" / customer: "did cannon say nothing about product positioning? ... it does not look like ad at all"”
- Response after the first: nothing — not_promoted at 001.

**attempt id collision** — RECURRED-NOTE-ONLY · bucket B8

- *first, 003 Cumin Co.* — CUM3-06: “two concurrent dispatch processes issued the same attempt id”
- *again, 007 Mokobara* — MOKO7-01: “att-020 was issued to two attempts ... next_attempt_id() = 1 + the number of lines in gen/ATTEMPTS.jsonl — a file appended only at SETTLE ... the collision window is the full latency of every in-flight call”
- Response after the first: ATTEMPT_ID_LOCK — candidate; the record says explicitly 'not fixed in code on this job'.
- Note: 007 collided again; that job promoted nothing to code either.

**container spec violation** — PREVENTED · bucket B1

- *first, 004 RentOk A* — RGA4-01: “the first deliverable carried two `elst` (edit list) atoms ... while the lane's own platform spec row said none; DET-A8 passed the container on geometry, codec, size and moov-first”
- *again, 006 RentOk V2* — RGV6-08: “animatic v1 (video-only H.264 with B-frames) carried an edit list; the mux step had -use_editlist 0, the render encode did not”
- Response after the first: CONTAINER_EDIT_LIST_CHECK promoted_now after 004.
- Note: 006 hit the same condition and the promoted check caught it at USD 0 before spend — the record calls it 'evidence CONTAINER_EDIT_LIST_CHECK works (second job)'.

**coverage asserted but never verified** — RECURRED-NO-FIX · bucket B10

- *first, 004 RentOk A* — RGA4-27: “this lane's canon block also lists colour_and_visual_register and audio under missing_domains ... whether accepted claims existed for those is NOT VERIFIED here”
- *again, CQ1 quality probe* — CQ1-24: “a strong 7-s beat does not guarantee a strong 30-s film — the 30-s cut has five obstacle beats and the same customer will judge pacing across all of them”
- Response after the first: nothing — not_promoted.

**keying residue on a cut out** — RECURRED-NOTE-ONLY · bucket B1

- *first, 004 RentOk A* — RGA4-08: “enclosed green pockets and the model's dark-green ground shadow survived the flood-fill key”
- *again, 006 RentOk V2* — RGV6-14: “green key fringe on the new sheet's cut-outs: 194 tinted px around the trip pose, 153 around dazed, 36-52 around brace/lookback/cover ... a 1-px halo at native, invisible at 360 px”
- Response after the first: KEYING_HELPER — candidate after 004.

**layer order error** — PREVENTED · bucket B1

- *first, 005 RentOk B* — RGB5-18: “flag pole drawn through the character 26.6-27.8 s”
- *again, 006 RentOk V2* — RGV6-09: “the falling phone (world layer) passed behind the cheat panel and under the INSTALL backing for 2 frames”
- Response after the first: 005 repaired it in place, not_promoted; GRAPHIC_TEXT_DISJOINT from 004 was already in code.
- Note: 006's instance was caught before spend by that promoted gate.

**our own measuring instrument was wrong** — RECURRED-NO-FIX · bucket B8

- *first, 004 RentOk A* — RGA4-11: “the first ebur128 regex read the running 'I:' line (-70 LUFS at t=0) instead of the summary”
- *again, 006 RentOk V2* — RGV6-03: “on animatic v1 the framing check read owner_frac at a moment the camera was still easing (0.156 at 8.40 s against 0.21) and failed for the wrong reason; the 'cover' stand-in was also double-shrunk”
- Response after the first: fixed in the job's own script, not_promoted.
- Note: 004's loudness regex read the wrong line; 006's framing gate measured at the wrong moment.

**our qa instrument is unreliable** — RECURRED-NOTE-ONLY · bucket B10

- *first, 005 RentOk B* — RGB5-29: “"the brand name rendered as 'rent okay' / 'Rent OK'" (QA transcription route)”
- *again, 007 Mokobara* — MOKO7-14: “tesseract returned tokens on 40 of 56 generated frames — tally marks, pebbles and sea ('fiat', 'Wars', 'PULA') ... no readable lettering exists”
- Response after the first: noted only (directional) after 005.
- Note: 007's OCR flagged 40 of 56 frames with no lettering present.

**picture depicts a capability the product lacks** — RECURRED-NO-FIX · bucket B5

- *first, 004 RentOk A* — RGA4-20: “the clearing of obstacle 3 (F9.3, 'a tick tags him; he freezes') shows RentOk stopping a tenant who is leaving. The site offers tracking ... not stopping anyone. The chip text is honest; the picture is not.”
- *again, 005 RentOk B* — RGB5-24: “a green tick on the drifting ghost's tag could read as 'paid' — the film must not imply recovery”
- Response after the first: fixed at the gate at USD 0, not_promoted.

**provider content refusal false positive** — RECURRED-NOTE-ONLY · bucket B9

- *first, 003 Cumin Co.* — CUM3-13: “1 PROHIBITED_CONTENT false-positive on an innocuous line; raw output is L16 PCM 24 kHz with long silent tails”
- *again, 005 RentOk B* — RGB5-07: “Gemini TTS refused the 16-character line 'RentOk mode: on.' as PROHIBITED_CONTENT (blockReason; no further reason); the other two lines on the same route succeeded”
- Response after the first: directional_only — RO-03, n=12 after 003.
- Note: 005 counted the refusal against the route and dropped the candidate with no re-send.

**spend authorisation or cap missing** — PREVENTED · bucket B8

- *first, 002 Upwork portfolio* — UPW2-08: “the spend record (v4/plan/SPEND-AMENDMENT-V4.md) was not amended before the portfolio calls ... no per-job cap was written”
- *again, 004 RentOk A* — RGA4-23: “JOB.yaml spend.cap = null and spend.pool_readings = [] ... the dispatch tool correctly refuses everything until they exist”
- Response after the first: PAID_PRODUCTION_PREFLIGHT promoted_now after 002.
- Note: 004's dispatch tool refused every paid call until a cap and a pool reading existed.

**spend records incomplete or unreconciled** — RECURRED-NO-FIX · bucket B8

- *first, 001 Upwork intro* — UPW1-32: “vendor statements (fal, GCP, Sarvam) never reconciled ... unknown whether Lyria's 3 failed calls or Veo's 2 UNAVAILABLE operations billed; ~12 triage calls ... not in any ledger”
- *again, 002 Upwork portfolio* — UPW2-26: “operator_reported_in_chat_usd 3.9 ... WRONG — a chat figure quoted before the second Nivaas attempt and never recomputed; the ledger governs (4.6596)”
- Response after the first: nothing — not_promoted.

**supplied brand mark copied or mangled by the model** — RECURRED-NOTE-ONLY · bucket B2

- *first, 003 Cumin Co.* — CUM3-01: “the model reproduced the bowl's embossed brand mark from the reference and garbled it ('cumin ca.'); his bowl held a curry”
- *again, 007 Mokobara* — MOKO7-24: “two [stills] carried a copied wordmark mark painted out by code”
- Response after the first: a candidate prompt clause ('turn the mark away') after 003.
- Note: 007 caught it with a per-job code paint-out, not with the written clause.

**text out of bounds** — RECURRED-DESPITE-CODE · bucket B1

- *first, 001 Upwork intro* — UPW1-01: “text clipped at canvas / card edges”
- *again, 002 Upwork portfolio* — UPW2-10: “"9:16 offer-in-motion clip — '15% OFF' runs off the panel" / customer: "9X 16 motion is getting text cutoff."”
- Response after the first: TEXT_BOUNDS_GATE promoted_now after 001.
- Note: 002's record states the gate existed and was NOT RUN.

## The most repeated mechanism in the programme

**Nobody can hear the audio.** Six of the nine jobs, seven rows, and the label has been the same every time: the check is named in the plan, and then no session on earth can execute it.

- 004 RentOk A — RGA4-26: “"the paid text detector was not run — recorded NOT_RUN" / "the checker could not listen — the customer's ACCEPT is the only ear on it"”
- 005 RentOk B — RGB5-10: “code-synthesised 'power-up chime', 'hurt blip' and 'coin-like' stamp sounds can drift towards the famous motifs by accident — the QA plan has no explicit by-ear check on SFX/music against Nintendo motifs”
- 005 RentOk B — RGB5-27: “Sound remains unheard by anyone — the one open check”
- CQ1 quality probe — CQ1-21: “a human should listen to those two stretches to be sure [speech-band level within 1 dB of full band]”
- 006 RentOk V2 — RGV6-24: “"obstacle 3 is not visibly stopped and obstacle 5's payoff reads weakly" / "sound by ear (LJ-14) and the melody's originality — both CANNOT_DETERMINE from this session"”
- 007 Mokobara — MOKO7-16: “speech or singing in the native Veo audio was never checked by a human on v1 or v2; no local recogniser ... the producer 'heard none on a quick listen'”
- today Mokobara deepread — MDR8-12: “audio content by ear (is there any speech or singing?) — NOT CHECKED — I cannot listen ... this needs a human ear or a speech detector before release”

Today's row says it in the atlas itself: MDR8-12 is recorded as "same gap as MOKO7-16 and RGB5-27". The first response (job 004) was to leave it open; at job 005 a pattern called VOICE_CAST_BY_A_HUMAN_EAR was written down as a candidate. It was still a candidate today, four jobs later.

Four other mechanisms sit just behind it at five jobs each: **graphics colliding with other graphics** (B1, 10 rows, 001→002→004→005→006 — a promoted gate existed throughout), **the model ignoring an instruction it was paid to follow** (B2, 8 rows, 001→CQ1→006→007→today — never fixed at all), **the hero hidden behind another graphic** (B1, 6 rows, 001→004→005→CQ1→006) and the plain verdict **"not good enough"** (B6, 5 rows, 001→003→CQ1→007→today).

## The plain numbers

### Rows and jobs per bucket, who found them, and what was promoted

"Found by" is the first party named in the record. "Customer" means it reached the person paying. "Checker" is the independent checker. "Us" is the producer or the Controller — i.e. caught in-house.

| Bucket | Rows | Jobs | Customer | Checker | Us | promoted_now | candidate | directional | not_promoted | none |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| B1 | 62 | 8 | 21 | 22 | 19 | 29 | 18 | 0 | 15 | 0 |
| B8 | 35 | 9 | 1 | 8 | 26 | 13 | 3 | 0 | 13 | 6 |
| B6 | 31 | 7 | 12 | 17 | 2 | 1 | 1 | 0 | 20 | 9 |
| B2 | 26 | 8 | 4 | 5 | 17 | 1 | 8 | 9 | 5 | 3 |
| B7 | 19 | 7 | 6 | 6 | 7 | 0 | 7 | 5 | 5 | 2 |
| B4 | 17 | 7 | 6 | 7 | 4 | 0 | 9 | 0 | 5 | 3 |
| B3 | 12 | 6 | 2 | 5 | 5 | 3 | 2 | 1 | 1 | 5 |
| B10 | 12 | 6 | 0 | 5 | 7 | 0 | 3 | 2 | 6 | 1 |
| B9 | 8 | 5 | 0 | 0 | 8 | 3 | 1 | 3 | 1 | 0 |
| B5 | 3 | 3 | 1 | 1 | 1 | 0 | 0 | 0 | 2 | 1 |
| **All** | **225** | **9** | **53** | **76** | **96** | **50** | **52** | **20** | **73** | **30** |

What that table says in words:

- **53 of 225 defects were found by the customer** — 24%. Nearly all of them (21) are bucket B1, things we had a written rule for and did not measure, and 12 more are bucket B6, work that was simply not good enough.
- **76 were found by the independent checker** and **96 by us** (producer gates and the Controller). The checker is the only party that finds craft problems in any volume: 17 of the 31 "not good enough" rows are his.
- **50 of 225 rows ended in code** (`promoted_now`). **52 ended as a candidate**, **20 as a directional note**, **73 were explicitly not promoted** and **30 had no promotion field at all** (today's job has no promotion queue yet). So 175 of 225 — 78% — left nothing behind that a machine will enforce.
- The two buckets that produce rejections carry almost no code: **B6 (not good enough) has 1 promotion in 31 rows**, **B4 (the plan never said it) has 0 in 17**, **B7 (route asked for what it cannot do) has 0 in 19**, **B5 (false real-world claim) has 0 in 3** and **B10 (a check that cannot run) has 0 in 12**. The code sits almost entirely in B1 (29) and B8 (13) — the two buckets we are best at measuring.
- **Customers found 0 rows in B8, B9 and B10** and only 1 in B3. They are not seeing our process problems; they are seeing pictures.

### Where the customer's eye lands

| Bucket | Customer-found rows |
| --- | ---: |
| B1 — Declared output rule never measured on the rendered file | 21 |
| B8 — Process, orchestration, records and spend | 1 |
| B6 — Not good enough by human judgement | 12 |
| B2 — Generative output never checked against its own prompt | 4 |
| B7 — A route asked for work its qualification never covered | 6 |
| B4 — The plan never said it | 6 |
| B3 — Nothing binds one generated asset to the next | 2 |
| B5 — A claim about the real world asserted, never sourced | 1 |

### Today's job against the rest

Today's rejected film contributes 20 rows: 5 in B8, 1 in B6, 3 in B2, 1 in B7, 3 in B4, 5 in B3, 1 in B10, 1 in B5.

Eight of today's twenty rows repeat six mechanisms already recorded on earlier jobs — identity drift between shots (MDR8-01, MDR8-10; first seen 007), the model ignoring an instruction (MDR8-02, MDR8-07; 001, CQ1, 006, 007), a mandatory action that never happens on screen (MDR8-13; 007), a route asked for what it cannot do (MDR8-14; 001, 003, 005), the verdict "not good enough" (MDR8-15; 001, 003, CQ1, 007) and nobody being able to hear the audio (MDR8-12; 004, 005, CQ1, 006, 007). None of today's twenty rows has a promotion recorded against it, because this job has no promotion queue yet.

### Two things the data refuses to support

- **It is not mainly a model problem.** 26 rows are a model disobeying its prompt (B2) and 19 are a route asked for what it cannot do (B7) — 45 of 225. 62 rows are rules we had written and did not measure (B1), and 35 are our own process and records (B8).
- **Better inputs did not buy a better verdict.** CQ1-05, from the quality probe: "Treatment B, which changed only the asset prompts and produced visibly richer stills, scored identical to the baseline with the evaluator (18 = 18) … Better pictures did not move the beat".

*Findings only. The Controller writes the plan.*
