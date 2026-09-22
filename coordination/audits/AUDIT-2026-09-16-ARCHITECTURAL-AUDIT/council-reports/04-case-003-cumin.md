# AGENT 4 — CASE 003 (Cumin Co. chopsticks) forensic report

Sources read: MI branch `work/agency-job-cuminco-chopsticks-001` @ `de1f978` (job dir `agency/jobs/AGY-2026-09-15-CUMINCO-CHOPSTICKS-001/`, 1,403 files: 1,153 png, 85 mp4, 65 wav, 5 py, 3 yaml, 2 jsonl — `git diff main...de1f978 --name-only | sed 's/.*\.//' | sort | uniq -c`); PR #103 branch `work/agency-sync-2026-09-16` @ `1de2b37`; skill on `main` @ `3bb9a3c` (`.claude/skills/media-agency/SKILL.md` blob `7e324b0` = the job's recorded `skill_version`, so the skill audited is byte-identical to the one the job ran under); `canon/knowledge/current/**`, `canon/compilation/**`, `canon/packs/pack-triggers-v0.yaml`, `coordination/CONTROL-STATE.md`; production-learning cases 001/002; `eval/historical-priors/media-factory-v1/**`; MFH `MEDIA-FACTORY-ROUTING-PRIOR.md`. Media extracted and inspected: V1/V2/V3 9:16 finals (ffprobe), V1/V2/V3 contact sheets, plate-A accepted, VO wavs b1/b2/b6 (re-measured). Never checked out; nothing modified.

Labels: OBSERVED / INFERENCE / HYPOTHESIS / UNKNOWN as per preamble.

---

## A. The brief, the questions, and what was decided before the first dollar

### A.1 Customer brief verbatim (OBSERVED — `JOB.yaml brief.verbatim` @ de1f978, also `brief.job.json`)

> I am thiknig to make an ad for cumin. co. I would prefer making a video ad instead of image. They have some classy cookware products and the d2c brand discovery routine got a lot of information about them. i would be keen to make a video on how to hold chopsticks for them using their product images. they also wrote a blog post about it. preferably a short video, a very calm empathetic voice doing a voice over. A charchater trying to hold the chopsticks with a bowl or sorts from cumin co infront of him- mostly a young adult. the girl trying to explain him hoe to hold- step 1, step 2, step 3. the steps are visual with a very short text companion. the boy fails but they still happily eat through their cumin cookware.

Received 2026-09-15T13:17:42Z (`ttao.job_start_utc`; first commit 26cb349 at 13:18:36Z). The customer is the user himself (class `spec_work`; "the user is the release authority").

Note (OBSERVED): the brief literally asks for "a video on how to hold chopsticks … step 1, step 2, step 3". It uses the word "ad" once and "how to hold chopsticks" as the content. A tutorial is what was briefed; the reframing into an ad was the agency's job.

### A.2 What the operator asked vs decided (OBSERVED — `intake.questions_asked`, `intake.assumptions` @ de1f978; identical list already present at 86ec183 13:27Z with `answer: null`)

Asked (4 questions, all answered at the 13:28:37Z start-of-job summary):
1. Spend cap → "USD 8 (Recommended) — whole job incl. repairs, 0 retries, hard stop"
2. "Approve the frozen copy deck and VO lines before generation?" → "Approve, freeze the deck — five on-screen strings and five VO lines as written"
3. Pool balances / attestation → "I attest all pools cover the cap"
4. Ending: spoon vs fist-grip → "Spoon from the bowl"

Plus one unsolicited user intervention pre-spend: "not fal" (fal cash excluded, 42fab25 13:39Z).

Decided by the operator alone (`intake.assumptions`, `blueprint.*`): product = the 15 cm Ceramic Ramen Bowl (from the blog); five blog steps compressed to three; single generated narrator instead of on-camera speech; two generated characters; 18 s / five beats; 9:16 master with 4:5 and 1:1 as crops; **`cta: none in-frame (brand line closes the film)`**; `offer_placement: none`; `cta_placement: "brand line 'Cumin Co.' bottom-centre of the end beat; 'Ramen night at home.' above it; no other CTA"`; hook = "a noodle slips back into the bowl in the first second"; VO line timings (t: "0.4–2.6", "3.4–6.2" …) fixed in the blueprint at 13:27Z, 31 minutes before the first TTS call (att-009, 13:58:07Z).

### A.3 Professional elements — resolved before first paid generation (13:39:37Z, att-001)?

| Element | Decided? | When (vs first spend 13:39:37Z) | By whom | Challenged by anyone independent? |
|---|---|---|---|---|
| Proposition / what the ad sells | Weakly: `remember: "The bottom one doesn't move — and Cumin Co. is the bowl on a noodle night."` | Before (13:27Z) | Operator | No. User approved *strings* only ("freeze the deck") |
| Product role | Stated as "the two bowls are in every beat: hero-sized in the macro inserts … table-scale in the two-shots" — i.e. product as *prop*, not hero | Before | Operator | No |
| Opening / hook | "A noodle slips back into the bowl in the first second" (blueprint.hook) — in the delivered V1 the first 3 s are a wide two-shot at table scale (OBSERVED on `qa/final-9x16-contact.png`, t=0–3) | Before | Operator | No; the user named it at V2 ("the opening is missing too") |
| Brand intro | Brand line only in the last beat (V1/V2). Persistent brand mark added in V3 only | V1: before, as "no"; V3 fix after V2 reject (17:48Z) | Operator; V3 fix prompted by user | Only by the user, post hoc |
| Proof | "the grip itself, shown not told" — proof of the *blog*, not of the product | Before | Operator | No |
| Payoff / close | "both laugh; he eats with a spoon; her chopsticks rest in the rim notch" | Before | Operator (spoon vs fist asked) | User chose spoon; nobody asked whether the close should be a product shot |
| CTA | **Decided as none** (`intake.cta`) | Before | Operator | No; user named it at V2 ("closing shot should have cumin product and final caption") |
| End card | None in V1/V2; V3 builds one from the brand's blog photo + PDP name + cuminco.com | After V2 reject | Operator; user "go ahead fix it" | Post hoc |
| Voice character | "calm, empathetic, Indian English, female"; provider "human ear decides at micro-qualification" | Before (direction) / after (voice: locked 14:17Z, 38 min after first paid plate) | Operator direction; user's ear over 5 rounds | User re-directed twice ("clam + cheerful … excitement") |
| Music | Lyria bed, "warm, sparse", ducked | Before | Operator | No; never judged separately |
| Hierarchy | CA-D1 "one cue per beat"; text upper third | Before | Operator (self-rendered pass) | No |
| Copy-safe placement | "text sits in the upper third clear zone or the lower third above the Reels UI band"; 4:5/1:1 declared as crops | Before | Operator | No; failed at V1 ("text is coming on figures") and every 4:5/1:1 to V3 |
| Timing | 18 s, beats 3/3.5/3.5/3/5 s, VO slots 2.2–3.0 s each, fixed before any VO existed | Before | Operator | No; final films ran 23.5 / 22.9 / 25.6 s |
| Continuity | plate-A anchors identity; plates H2/H3/B reference H1/A; D3 rows | Before | Operator | Held (OBSERVED: identity stable across V1–V3 frames) |
| Platform | Reels 9:16 master; 4:5, 1:1 "compositor renditions" | Before | Operator | No; the crops never worked (CF2 flags V1–V3) |

INFERENCE: every creative decision was made by the operator in the 10 minutes 13:17–13:28Z and "approved" by the user only at the level of five strings and a spend cap. The single human question that touched structure (spoon vs fist) is a detail of beat 5. No independent challenge step ran: `blueprint.reviews: []` although PRODUCTION-WORKFLOW §5 says "Consult Canon persona review (Karl disconfirmer, Ezra copy) when the job is customer-facing copy" — and **no such personas exist anywhere in the repo** (`grep -rl -iE 'disconfirmer|persona review'` hits only the skill file and its worktree copy).

---

## B. Production timeline (all UTC; commit times converted with `TZ=UTC git log --date=iso-local`; ledger from `gen/LEDGER.jsonl`)

Money: 50 reserved ledger lines, Σ **USD 5.0907** (my recompute equals the record); by route nano-banana-2 ×8 0.536 · veo-3.1-fast-i2v ×7 4.200 · sarvam ×8 0.0229 · elevenlabs ×8 0.0987 · gemini-tts ×18 0.1732 · lyria ×1 0.060. Distinct attempt ids 50 (att-019 collided and was aliased att-028). Voice: 34 attempts USD 0.2947, of which **27 search/qualification takes (26 ok, 1 http_401)** across three providers (Sarvam 8, ElevenLabs 8, Gemini 11) and 7 final-line draws.

| UTC | Event | USD cum. | Human touch |
|---|---|---|---|
| 13:17:42 | job opened, brief verbatim (26cb349 13:18:36) | 0 | brief |
| 13:23 | Canon lookup: 10 packs selected, 2 injected, 8 gaps; prefix 5,298 tokens, 21 check ids | 0 | — |
| 13:27:15 | 86ec183: intake, NR, blueprint (21 check lines all "pass"), plan, VO lines with timings | 0 | — |
| 13:28:37 | start-of-job summary; cap USD 8; deck frozen; pools attested; ending = spoon | 0 | 4 answers |
| 13:33:14 | fal balance read USD 0.147 → fal plan blocked | 0 | — |
| 13:39:26 | user: "not fal"; 42fab25 credits-only routes; 10 prompts gated (GATE PASS ×10) | 0 | "not fal" |
| 13:39:37 | att-001 plate-H1 local fault (reserved, unsent) | 0.067 | — |
| 13:39:57–13:41 | att-002/003 plate-H1 r1/r2 | 0.201 | 13:46:31 "r2" |
| 13:44:38 | att-004 clip-2 (Veo, micro-qualification of the grip) | 0.801 | "accpet" |
| 13:55–13:57 | att-005..008 plates A r1 (garbled embossed mark, DF-01), H2, H3, A r2 | 1.069 | "plates are good to go" |
| 13:58:07 | **voice search begins** (att-009..011 Sarvam priya/shreya, ElevenLabs Sarah) — 18 min after the first paid plate | 1.085 | round 1: "all three are robotic … we could use hidi comfoting voice" |
| 14:00:32 | round 2: Hindi — Sarvam ×4, ElevenLabs Sarah/Lily ×2 (att-012..017) | 1.114 | "stick to english. but voices are not good. at all. why ae we not using veo models with voice? … clam + cheerful" |
| 14:06:36 | att-018 plate-B | 1.181 | "plate b is accepted" |
| 14:06:50–14:09 | clips 1, 3, 4 (att-019→028, 023, 029) — **drawn while the voice was still unresolved** | 2.98 | — |
| 14:07:34–14:08:21 | round 3: Gemini TTS Aoede/Leda/Kore/Sulafat, ElevenLabs tagged Lily/Jessica, Sarvam kavya/roopa slow (att-019..022, 024..027) | | rejected |
| 14:10:54 | att-031 music (Lyria) | 3.04 | — |
| 14:11:45–14:12:33 | round 4: Gemini Aoede/Leda/Zephyr/Despina, ElevenLabs Jessica/Bella/Lily (att-032..038; 038 = quota_exceeded, 54 credits) | 3.15 | "leda is good. a little slower though. the shrillness and excitement is still miissing" |
| 14:16:49–14:17:11 | round 5: Leda v1/v2/full (att-039..041) | 3.18 | "bubbly" (voice locked) |
| 14:17:46 | att-042 clip-5 | 3.78 | — |
| 14:21:10–14:21:47 | att-043..048 five VO lines (045 PROHIBITED_CONTENT false positive → 048) | 3.84 | — |
| 14:37:21 | qa_complete; 8a5927a "voice locked … compose.py … delivery note"; V1 9:16/4:5/1:1 23.5 s | 3.88 | — |
| 14:52 (record) | V1 presented | | ~15:0xZ **"crapy. the video has got some random audio. her lips are omving. the text is coming on figures. all messed up"** |
| 16:59:06, 17:00:03 | att-049/050 clip-1 r2, clip-5 r2 (closed mouths) | 5.08 | — |
| 17:22:51 | b53d210: V1 REJECTED recorded; V2 built (22.9 s, beat-1 VO dropped, 9:16 0 cards; 4:5/1:1 CF2-flagged; no-music variant) | 5.08 | **"did cannon say nothing about product positioning? the closing shot should have cumin product and final caption. it does not look like ad at all. the opening is missing too. canon had this knowledge. how's that possible?"** |
| 17:30:00 | att-051 spoken close "Ramen night at home. Cumin Co." | 5.0907 | "go ahead fix it" (product name + cuminco.com approved) |
| 17:47:49 | V3 review requested; c0f849c 17:48:00 (25.6 s; persistent brand mark; end card from brand photo) | 5.0907 | — |
| 2026-09-16 03:45:05 | **"this is still bad. the voices are overlapping. not at all happy with it. reject completely. we need to do the diagnosis now. tranfer the info to canon"**; de1f978 03:45Z packet written | 5.0907 | V3 REJECT |

Totals (computed): attempts 50 (47 ok); versions 3, all rejected; **human touches 18** by my count (brief, "not fal", 4 answers, MQ plate, MQ clip, plates A/H2/H3, plate-B, voice verdicts ×4, V1, V2, "go ahead fix it", V3) vs the record's "human_review_cycles: 10"; wall clock job-open → final reject 14 h 27 m; job-open → V1 review 1 h 20 m; job-open → V3 presented **4 h 30 m**; per-call latency sum 824 s (from ATTEMPTS.jsonl per the case).

**Timestamp conflict (OBSERVED).** `JOB.yaml versions[]` says V2 "presented_utc 15:2xZ" and V3 "16:0xZ"; the case's TIME-AND-COST says "working span 13:17Z–16:15Z (≈ 3 h)"; REVISION-TRACE says V2 elapsed "≈0:35". But the ledger shows the V2 clips were dispatched at 16:59–17:00Z, the V2 commit is 17:22:51Z, the V3 spoken close at 17:30Z, and `ttao.human_review_requested_utc` for V3 is 17:47:49Z. The V2/V3 presentation times in the record and the "≈3 h" working span are wrong by at least 1.5 h; the honest working span to V3 is ≥ 4 h 30 m. UNKNOWN: whether V1's verdict really arrived at "15:0xZ" (chat-only) — if so, ~2 h elapsed between the V1 verdict and the first repair dispatch, not 35 min.

Voice rounds in detail (OBSERVED, `ATTEMPTS.jsonl`): round 1 en-IN Sarvam priya/shreya (no pace), ElevenLabs Sarah (`EXAVITQu4vr4xnSDxMaL`, eleven_v3) — "all three are robotic"; round 2 hi-IN Sarvam ×4 (pace 0.85–0.9) + ElevenLabs Sarah/Lily Hindi — "stick to english … voices are not good"; round 3 Gemini ×4 + ElevenLabs tagged ×2 + Sarvam en slow ×2 — rejected; round 4 Gemini ×4 with a longer style prompt + ElevenLabs Jessica/Bella (Lily quota-failed) — Leda "good… slower… shrillness missing"; round 5 Leda "bubbly" accepted. Rejection reasons are chat-only, transcribed in `HUMAN-VERDICTS.yaml`.

Compositor gates: V1/V2/V3 each ran bounds/contrast/fit/tokens/disjoint/exact/export (C1–C8) and CF1–CF5 rows on all three geometries — every row PASS on 9:16, CF2 "REVIEW/FLAGGED" on 4:5 and 1:1 in all three versions, and all three versions were nevertheless presented. The V3 QA (`qa.final_geometry`) is all PASS on the file that the human rejected for overlapping voices; no audio-schedule check existed.

VO overlap re-measured (OBSERVED, my method: first/last sample above −50 dBFS on the committed wavs; the operator's method was ffmpeg `silenceremove` at −50 dB then `atempo=1.10`): b1 raw 6.48 s, speech 5.92 s placed at 0.30 → ends 6.22 s vs b2 at 4.70 → **overlap 1.5 s** (record: 0.92 s after tempo 1.10 — 5.92/1.10 = 5.38 s ≈ the record's 5.32 s, so the two figures reconcile); b6 5.03 s at 22.0 → ends 27.0 vs film end 25.6 → **overrun ≈ 0.9–1.4 s**. The human's "voices are overlapping" is mechanically true.

---

## C. Failure chains

Eight-state ladder used per chain: exists → retrieved → in context → understood → changed a decision → decision correct → survived production → QA detected. K-codes as defined in the task.

### (1) The ad became a chopsticks tutorial, not a product-led ad
- **Expert would know:** an ad's spine is product role → promise → proof → close/CTA; a how-to is a content format, and the product must be the reason the how-to exists (bowl that makes noodle night easy), shown as hero at open and close.
- **Repo knowledge:** EXISTS. `canon/knowledge/current/google-abcd-video-ads/source-knowledge.yaml @ 4e3dc358` L667 "Brand early, often, and richly"; L736 "Introduce your brand or product from the start and maintain that presence"; L1291 "Ask them to take action"; L1640 "Consideration: Show users how your product fits into their lives". Ogilvy ch2 binding `bnd_ogl_c003_0001` (positioning = "what the product does and who it is for" → objective.description). StoryBrand `bnd_sb_c003_0002` → `message.proposition`. Hopkins `bnd_hop_sa_*` on specificity. **Authoritative?** Partly: the sources are among the 37 "accepted" sources in `canon/knowledge/current/`, but every operational binding of all five sources is `status: proposed / "not reviewed"` (counts: ABCD 9/0, Ogilvy 5/0, Hopkins 8/0, StoryBrand 7/0, Sullivan 10/0), `CANON-014-ADMISSION-MANIFEST.md` L118 flags ABCD as a living web artifact "read without a fingerprint … platform-contingent throughout", and Sullivan L114 "blocks promotion". Nothing from these sources is in either compiled pack.
- **Retrieved?** NO evidence before the V2 rejection. The string "ABCD" first enters the job record at c0f849c (17:48Z) — after the user wrote "canon had this knowledge. how's that possible?" (`git log -S'ABCD' main..de1f978`). The Canon lookup at 13:23Z recorded `commercial_communication` as fired-but-uncompiled and listed it under `missing_domains`.
- **In mandated context?** NO. `BOOTSTRAP.md §2` mandates reading only "the two compiled packs' decision ids + CHECK lines"; `canon/knowledge/current` is never on the reading list. Worse, PRODUCTION-WORKFLOW §4 instructs: "Do not compile, paraphrase or invent a pack for a missing domain. Proceed on the brief and record the gap … only if the production actually fails for want of it." — retrieval of the ad-structure knowledge was *policy-blocked*, and C-10 (`CONTROL-STATE.md` L81/L95) forbids compiling the pack until "a real runtime failure demands one".
- **Transformed into a job requirement?** NO. `intake.cta: none in-frame`; `offer_placement: none`; `proof` = the grip. PA-D7 ("does the imagery earn its space commercially?") was rendered "pass — 'the bowl on a noodle night' sells at a glance; the hero image needs no copy" — self-review.
- **Decision by / challenged by:** operator / nobody (reviews: []; personas do not exist). The user approved five strings at 13:28Z (K14: approval at the wrong level).
- **Tested before dependent spend?** No: the whole USD 3.88 of plates/clips/VO was drawn against a structure nobody had questioned.
- **QA check existed?** None. QA-CHECKLIST has ~50 rows; none asks "is there a product hero / brand early / CTA". CF5 "hierarchy survives the fit" is the nearest and is about type sizes.
- **Why it reached the human:** the workflow has no creative gate between blueprint and dispatch, the brief was followed literally, and the only reviewer was the author.
- **K-codes:** **K2** (retrieval blocked by design), **K6** (no owner of the commercial question — "Canon constrains; it does not direct"), **K7**, **K14**, **K5** (from PA-D7 "picture must earn its space" the operator reasoned "the bowl demonstrates its own feature without a line of copy", i.e. no CTA). Not K0: the knowledge exists in the repo *and* in any frontier LLM (see F).

### (2) Weak/no opening
- Expert: open on the product or the problem in the first 1–2 s; a close-up, mid-action (ABCD L462 "start your ad in the middle of the action, or open with a close-up").
- Repo: EXISTS (same file; `bnd_abcd_001` "opening sequence … whether the brand or product is present"). Also case 001 HUMAN-VERDICTS L19/L31 "opening not visually exceptional enough" / "opening still not strong enough" — the *previous* accepted case was rejected twice on the opening.
- Retrieved/in context: case 001 README/PROMOTION-QUEUE are mandated reading; the opening lesson was not promoted into any pattern (only SPEAKER_MICROQUALIFICATION was), so it was in context as narrative, not as a requirement → **K1/K13**.
- Decision: blueprint.hook says "a noodle slips back into the bowl in the first second" but beat 1 is a wide static two-shot from plate-A (OBSERVED: V1 contact t=0–3 s, both figures small, bowls at table scale); the V1 clip-1 window used 2.5–6.0 s of the clip "because 1.5–2.5 s he lands noodles in his mouth (contradicts 'he fails')" — the hook was chosen by exclusion of defects, not for attention. V2 then *dropped* the beat-1 VO for pacing → an opening with no words, no product, no brand.
- QA: none for "does the opening hook". **K13, K5, K7, K11.**

### (3) Insufficient product role / limelight
- Expert: the bowl is the client's product; the noodles, hands and chopsticks are not. In V1 the product is a coloured bowl below the action for 14 s of 23.5 (OBSERVED contact sheet: macro beats 4–17 s frame the *hand* and the *noodle*; the bowl is the base of the frame). The brand's own photography (16 images) was on disk from 13:27Z (`source/images/*`, hashed) and was used only as a generation reference until V3 built the end card from it.
- Repo: EXISTS — ABCD L876 "Whether with product shots, pack shots, in situ branding … work your brand identity into the story"; PA-D7 default "size imagery by importance to the sale, never decoration" (in the *injected* pack).
- In context: YES (PA-D7 was injected and rendered). Understood/changed a decision: NO — rendered "pass" against a blueprint in which the product is a prop. **K4** (context present, diluted among 21 check lines all self-marked pass), **K7**.
- QA: none (B2 product fidelity checks shape/hue, not prominence). **K11.**

### (4) Missing/weak close
- Expert: finish on the product with name + where to get it.
- Repo: EXISTS — ABCD "full_funnel finish with the product" (cited by the operator itself at c0f849c), L1358 "Include a call to action (CTA)". Case 001 ACCEPTED-TEMPLATE beat 10 `human_cta` "CTA card" — the previous accepted film ended on a CTA card.
- Decision: close = laughing two-shot + "Ramen night at home. / Cumin Co." over the two-shot (V1 t=18–23 s, OBSERVED). Fixed in V3 (end card 21–25.6 s, product photo, PDP name, cuminco.com) only after the user's V2 verdict.
- **K13** (template evidence in mandated reading not carried), **K6**, **K14**.

### (5) CTA weakness
- Expert: every ad has a Direction, even a spec ("cuminco.com", "Shop the Ramen Bowl").
- Repo: EXISTS (ABCD L1291–1358 "Ask them to take action"; the accepted template's CTA beat; case 002's SHOP NOW pills). Skill: JOB-TEMPLATE has `cta_placement` as a field but no rule that it be non-empty; SKILL.md lists "CTA" only as an *exact-text mechanism* ("price, offer, code, CTA, legal … composed by code").
- Decision: `cta: none in-frame` at 13:27Z, operator, unchallenged; "cuminco.com" added in V3 with user approval. **K6, K14, K7.** The skill treats CTA as a typesetting problem, not a commercial decision (see D).

### (6) Text over people/action
- Expert: copy never crosses the subject; feed crops need their own composition.
- Repo: EXISTS and PROMOTED — case 002 HD-03 "headline placed over the figure/garment once the 16:9 poster is cropped", HD-09/10 "banner overlapping the photos"; QA-CHECKLIST CF2 "no text or UI element sits over the product, face or hero object"; FORMAT_SPECIFIC_REVALIDATION in SKILL.md.
- In context: YES (mandated). Transformed: `product_placement: "never obstructed by text"`. Tested: V1's contrast probe sampled 4 frames and had no subject-obstruction test (DF-04). QA detected: CF2 was marked "PASS on 9:16" for V1 and "REVIEW" for 4:5/1:1 — and the human rejected V1 9:16 for "text coming on figures" → the operator's own CF2 PASS on 9:16 was wrong (K11), and the flagged 4:5/1:1 files were presented anyway in V1, V2 and V3 (K14: a REVIEW-flagged file is not a candidate). **K13** (the same failure class as case 002 a day earlier), **K11**, **K10** (compositor lacked the gate it said it had), **K14**.

### (7) Robotic/poor voices; repeated voice search
- Expert: cast the voice first, by ear, with a directed read; do not audition Western premade voices for an Indian-English brief; Sarvam raw TTS reads robotic without rhythm work.
- Repo: EXISTS in three places. (a) MFH `MEDIA-FACTORY-ROUTING-PRIOR.md` L28–29: "Sarvam bulbul:v3, speaker chosen by human ear … raw TTS sounds robotic without speech-rhythm rewrite + mix" and "**EL western voices for Hindi-accent work — western accent rejected by ear even in English (el_sarah_v3.mp3)**". (b) `eval/historical-priors/media-factory-v1/` carries the same text. (c) Case 001 RO-05 "rejected by ear as robotic" and SPEAKER_MICROQUALIFICATION "before any dependent spend".
- Retrieved/in context: case 001 yes (`template.learning_applied` cites RO-05); MFH/historical-priors NOT in mandated reading (K3).
- Changed a decision? Partially: "qualify by ear first" was planned. But the **first ElevenLabs take dispatched was Sarah `EXAVITQu4vr4xnSDxMaL`** — the very voice the prior recorded as rejected — and 8 ElevenLabs Western-voice takes followed (K13 hard evidence). Sarvam got 8 takes despite RO-05. The voice search ran *after* plates (13:58Z vs 13:39Z) and *during* clips 1/3/4 (14:06–14:09Z) — contrary to the micro-qualification-first principle the job itself listed. Gemini TTS (no Registry cell) was the eventual answer.
- Human role: the user redirected the search (Hindi detour, "why ae we not using veo models with voice?", "shrillness and excitement") — five rounds of take-level human judgment (K14: the human was the casting director at take granularity).
- QA: D10/D14 exist and are "human ear" rows — i.e. the QA is the human. **K13, K3, K12 (ordering), K14, K15** (27 takes, 5 rounds, USD 0.29 — cheap in dollars, expensive in human touches).

### (8) Timeline fixed before actual VO existed
- Expert: read-to-picture — record/measure the VO, then cut; a 2.2-s slot cannot hold a 5-s "slow, bubbly" read.
- Repo: NOT as a rule (K0 within the repo; K1 as universal craft). Case 001 ACCEPTED-TEMPLATE records narration distribution but no VO-first ordering.
- Decision: `blueprint.voice_over.lines[].t` fixed at 13:27Z; compose.py `VO = {1: ("final-b1.wav", 0.3), 2: (…, 4.0) …}` hand-set at 8a5927a; V2 dropped a line and applied `atempo=1.06→1.10`; V3 restored the line and added a sixth into a 25.6-s film with the same hand-set starts. The user's "bubbly, slower" direction (round 4–5) made each line 4.5–6.5 s. Nobody re-planned the timeline after the voice changed character. **K5** (correct knowledge that text overflow fails closed was not generalised to audio), **K10**, **K11**.

### (9) Overlapping voices (DF-08)
- Expert: trivially, two lines may not overlap; measure durations.
- Repo: analog existed as code (`runtime/compositor/gates.py check_text_bounds`, `check_disjoint`) and as doctrine in SKILL.md "Text overflow fails closed". Not applied to audio (K5). compose.py measures ink boxes to the pixel (L112) and never measures a wav (grep: no ffprobe/duration on VO). The assembly D14 row was "pending human ear" — QA by the release authority. **K10, K11, K5.** Post hoc the PR promotes `check_vo_schedule` (correct, narrow).

### (10) Repeated iterations V1→V3
- Expert: after a REJECT, re-brief the whole piece; do not patch the named defect only.
- Skill: §12 "repair that layer only" and the red flag "Regenerate everything → classify the defect; repair that layer only" *encourage* narrow patching. V2 fixed exactly V1's three named defects; V3 fixed exactly V2's named structure defects and introduced DF-08 by adding a sixth line to hand-set starts. Each version was reviewed only by the author before the human. **K7, K12/K15 (a rule optimised for the wrong failure class), K14** (human as the only reviewer, three times).

### (11) High process/time relative to result
- OBSERVED: 8,035 words of skill; JOB.yaml 65,875 bytes / 405 lines; 21 check lines + A1–A10 + B/C/CF/D rows, all rendered by the operator, all PASS on every version; 1,153 frame PNGs committed; a 450-line dispatch tool and 414-line compositor written per job; 14 h 27 m / ≥ 4 h 30 m working / 18 human touches / USD 5.09 / zero accepted output. None of the gates that consumed the bookkeeping caught any of the seven rejection reasons. **K15, K7.** The PR #103 response is to add another gate.

---

## D. Actual sequence vs PRODUCTION-WORKFLOW.md

| Stage | Followed? | Evidence / note |
|---|---|---|
| 0 sync from main | Yes | `production_base_sha` = main 3bb9a3c; branch from origin/main |
| 1 open + clock | Yes | 26cb349 13:18:36Z, brief verbatim |
| 2 intake → NR | Yes, formally complete | `questions_asked` limited to cap/deck/pools/ending |
| 3 template/learning-first | Yes (none reused; 13 `learning_applied` ids) | but the two most relevant lessons (case 001 opening ×2, CTA beat; case 002 text-over-figure) did not change the plan |
| 4 Canon lookup | Yes | 2 injected, 8 gaps; §4 forbids reading the gap domains |
| 5 blueprint | Yes, fields filled; **persona review skipped** (`reviews: []`), personas don't exist | check lines self-rendered 20 pass / 1 n-a |
| 6 plan | Yes | 4:5/1:1 declared as crops of one master (the workflow's own rule "never separate draws") → structural cause of DF-09 |
| 7 routes | Yes | Gemini TTS no cell — used as directional; fine |
| 8 pre-dispatch A1–A10 | Yes (A9 NOT_RUN by design) | start-of-job summary shown 13:28:37Z |
| 9 generation | Yes | per-job dispatch tool, ledger, 0 retries; att-019 id collision |
| micro-qualification order | **Reordered**: plan listed voice as MQ-2 "by ear first"; voice search started after plates and during clips 1/3/4 | ATTEMPTS timestamps |
| 10 composition gates | Yes | + an obstruction gate invented in V2 that the runtime lacked |
| 11 post-draw QA | Yes | CF2 flagged geometries presented; D14 "pending human ear" |
| 12 bounded repair | Yes — too literally | narrow patches ×2 |
| 13 human release | Yes | "REJECT → ask what to change before spending again": V1 verdict was self-explanatory; V3 got "go ahead fix it"; conformant |
| 14 packet | Yes (on reject) | |

Where the skill is silent on the creative questions (OBSERVED): the only creative guidance in 8,035 words is PRODUCTION-WORKFLOW §5 (**192 words** of 2,803, 6.8%) — a table of field names with one-line prompts ("`offer`, `product`, `proof`, `cta` — where each sits and how big") — plus the JOB-TEMPLATE `blueprint:` block (**115 words** of 1,504) and one sentence in SKILL.md ("A technically perfect picture can still be a bad ad; you own the advertising craft"). Nothing says a product must be hero, an ad must open on something, a CTA must exist, or brand must appear early; "Canon constrains; it does not direct" and §4 "proceed on the brief" push the operator toward literal execution. The 11-row red-flag table has zero creative rows; QA-CHECKLIST (1,554 words) has zero ad-structure rows. Counting method: manual classification of sections — creative/expert ≈ 192 + 115 + ~60 ≈ **370 words ≈ 4.6 %**; process/bookkeeping ≈ 95 %. (A looser keyword heuristic — paragraphs mentioning any of hook/cta/proof/offer/… — gives 22 %, inflated because "cta/offer/copy" appear mostly as *exact-text mechanics*; script in my notes.)

---

## E. The operator's diagnosis and PR #103 — does it hold?

What they concluded (OBSERVED, `LEARNING-PACKET.yaml` @ de1f978; `PROMOTION-QUEUE.yaml`, `SYSTEM-DEFECTS.yaml`, `OUTCOME.yaml` @ 1de2b37): 8 defects; tally "1 model failure / 5 pipeline failures reaching the human"; "process conformance: CONFORMANT … and it still failed"; promoted VO_SCHEDULE_GATE (35 lines in `runtime/compositor/gates.py` + tests); 7 candidates (obstruction gate, VO-first, closed-mouth, AD_STRUCTURE_MINIMUM "until commercial_communication is compiled", plates-per-geometry, voice-by-ear-first, audio edge trim, attempt-id lock); Canon gap "commercial_communication uncompiled; ABCD knowledge exists in accepted Canon → Controller decision under C-10".

Where I agree: the mechanical facts are accurate and well-evidenced (ledger totals reconcile; overlap is real; every rejection landed on an unmeasured dimension); VO-first and the schedule gate are correct; the model-vs-pipeline tally is fair.

Where it does not hold:
1. **"Canon gap" is the wrong root cause.** The ABCD/Ogilvy/Hopkins material exists (`canon/knowledge/current/*`), but (a) all its bindings are `proposed / not reviewed`, ABCD is flagged unfingerprinted and platform-contingent — "exists in accepted Canon" overstates its standing; (b) the operator is a frontier LLM that does not need a 4,096-token pack to know an ad ends on the product with a CTA (see F); (c) the real mechanism was that the workflow told the operator to *proceed on the brief* for uncompiled domains, gave it no creative gate, no reviewer, and let it self-mark 21 checks pass. Coding it K0/K2 shifts ownership to the Controller (C-10) when the failure is K6/K7/K14 inside the skill. AD_STRUCTURE_MINIMUM is the right instinct but is framed as a stop-gap "until the pack is compiled" — it should be unconditional practice.
2. **Could a pack ever have carried it?** Mechanically yes: the trigger table budgets `commercial_communication: 4096` tokens; the compiler renders by id from `canon/knowledge/current` and fails closed only on incomplete audit records (an ABCD audit record exists). But the pack format (questions-with-defaults, CHECK per id, `INJECTION-CONTRACT-v0.md`) was designed for a *weak* model (Gemma 0/18 retrieval) and is consumed by the operator by copying check lines into JOB.yaml and marking them pass; PA-D7 — the one injected check that *does* ask "does the imagery earn its space commercially?" — was marked pass on a film with no product hero. INFERENCE: a compiled commercial_communication pack would most likely have produced a 22nd self-rendered "pass" line, not a different film, unless an independent reviewer is added.
3. **"CONFORMANT" is misleading.** §5 persona review was skipped against non-existent personas; CF2-flagged geometries were presented three times; the voice MQ ran after plates. Conformance to a process with no creative gate is not a defence.
4. **Time claims are contradicted by the ledger** (see B): "≈3 h working span 13:17–16:15Z" vs V2 clips at 16:59Z, V3 at 17:48Z; V2 "≈0:35" vs ≥ 2 h.
5. **Every remedy is another gate/rule.** PR #103 adds code and eight candidates; none adds a decision owner or a challenge step. The three cases now show the same shape: models deliver, direction/assembly lose the job — and the response each time enlarges the bookkeeping.
6. Minor: `voice_takes: 26` counts ok takes; 27 were dispatched, 34 voice attempts in total; "human_review_cycles: 10" undercounts human touches (18).

---

## F. Strong-baseline thought experiment (≤300 words)

*Brief completion a strong LLM with no Canon would write from the verbatim brief:*

> **Product role.** Cumin Co.'s ramen bowl is the hero, not the chopsticks: the bowl is what makes noodle night at home possible (wide rim, rim notch that parks chopsticks or a spoon). Open and close on it.
> **Opening (0–2 s).** Close-up: steam rising from the mint bowl, chopsticks dropping into the rim notch; brand mark on screen from frame 1. VO: "Noodle night. First time with chopsticks?"
> **Body (2–12 s).** Three macro beats, her hand teaching, his failing — each with a 3–5-word super; the bowl fills the lower half of every frame, notch visible.
> **Payoff (12–15 s).** He gives up, grabs the spoon from the notch, both laugh — "the bowl doesn't mind."
> **Close / end card (15–18 s).** Packshot of the Kairi + Rosé bowls, "15 cm Ceramic Ramen Bowl · Cumin Co. · cuminco.com" — VO says the brand name.
> **Voice.** One warm Indian-English female narrator, unhurried; cast by ear from 2–3 takes before anything else is generated; VO recorded first, picture cut to the VO.
> **Music.** Sparse, ducked.
> **Text.** Supers in the clear wall zone; never over hands or bowl; 4:5 and 1:1 re-framed, not cropped.
> **Muted test.** Works without sound; brand and product readable in the first and last 2 s.

*What Canon added in the actual job:* lighting consistency, one cue per beat, no lettering in plates, product fidelity to the packshot, hold lengths — all of which held (OBSERVED: plates are clean, identity stable, no stray text). *What it should have added:* nothing the baseline lacks; at most the same structural checklist as a forced pre-spend question.

*Where the failure occurred:* between 13:17 and 13:28Z, in the blueprint — the operator followed the brief's "how to hold chopsticks" literally, decided `cta: none`, marked its own checks pass, froze the deck, and the user approved five strings. Everything after that was competent execution of a wrong plan, patched three times.

---

## Findings ranked

1. **The creative failure was not a knowledge gap.** ABCD/Ogilvy/Hopkins exist in `canon/knowledge/current` (unreviewed bindings), and the operator itself knows ad structure; the workflow policy-blocked reading uncompiled domains (§4), provided no creative gate, no reviewer (personas named in §5 do not exist), and let the operator self-mark 21 checks pass. K2-by-design + K6 + K7 + K14. (JOB.yaml `intake.cta: none in-frame`, `reviews: []`; `git log -S'ABCD'` first hit c0f849c after the user's complaint.)
2. **Approval happened at the wrong level.** The user approved five strings and USD 8 at 13:28Z; product role, opening, CTA, end card were never surfaced as decisions. K14.
3. **Prior learning did not propagate.** Case 001's opening/CTA verdicts and template CTA beat; case 002's text-over-figure and format-specific rules; MFH's "EL western voices rejected by ear even in English (el_sarah_v3)" — the job's first ElevenLabs take was Sarah. K13, with the strongest single citation in this audit.
4. **The gates measured nothing the human rejected.** All C/CF/D rows PASS on V3; CF2-flagged 4:5/1:1 files presented three times; D14 "pending human ear". K11/K14.
5. **Timeline before VO; VO placed by hand; no audio measurement** — DF-05/DF-08 mechanically confirmed (overlap 0.9–1.5 s, overrun 0.9–1.4 s). K5/K10/K11.
6. **Process overhead ≈ 95 % of the skill; creative guidance ≈ 4.6 %** (370 of 8,035 words); 1,403 files, 65 KB job record, 18 human touches, 3 versions, 0 accepted. K15.
7. **The case's own timestamps and "≈3 h" claim are contradicted by its ledger** (V3 presented 17:48Z, ≥ 4 h 30 m).
8. **PR #103's remedy (another gate + eight candidates) repeats the pattern**: each failure becomes bookkeeping, not ownership.

## Open questions / unknowns

- UNKNOWN: exact V1 verdict time (chat-only, "15:0xZ"); whether the 2 h gap to the V2 clips was idle or unrecorded work.
- UNKNOWN: whether the operator ever *read* the ABCD source before V2 (no artifact says so; absence of the string is the only evidence).
- UNKNOWN: the prior cloud session ("The Still One", Downloads/HANDOFF.md) is not in any repo — its concept reportedly had no characters; cannot compare.
- HYPOTHESIS (untested): a compiled `commercial_communication` pack, consumed the way PA-D7 was, would have added a 22nd self-rendered "pass"; the counterfactual that would have changed V1 is a forced, human-visible structure question before the deck freeze, or an independent reviewer.
- Method note: my VO overlap figure (1.5 s) differs from the record's (0.92 s) because the record applied `atempo=1.10`; both establish overlap.
