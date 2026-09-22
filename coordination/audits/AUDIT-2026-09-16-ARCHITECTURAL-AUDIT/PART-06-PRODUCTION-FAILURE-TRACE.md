# PART 6 — REAL-PRODUCTION FAILURE TRACE (cases 001, 002, 003)

Sources: council reports 04 (Cumin forensic), 05 (cases 001/002 + recurrence), 12 (craft jury on the actual media), 09 (operator/runtime), 10 (learning loop), 08 §3–4 (voice/routing), 02 §6 (Media Factory analogues). Refs: MI `main @ 3bb9a3c`; PR #103 `1de2b37`; Cumin evidence `de1f978`; case-001 branch `work/pilot-upwork-intro-video-v4` (`7629894` = V1, `f6ca66f` = head); case-002 branch `work/upwork-portfolio-samples-2026-09-15` (`b4b77fa`). Media cited by path + sha256 (§0). Labels: OBSERVED / INFERENCE / HYPOTHESIS / UNKNOWN. K-codes K0–K15 as defined in the commission; eight-state chain E→R→C→U→D→K→S→Q (exists, retrieved, in context, understood, changed decision, decision correct, survived production, QA detected).

---

## 0. Artifacts judged (path @ ref, sha256) — OBSERVED (council 12 §0, recomputed with `shasum -a 256`)

| Case | Artifact | sha256 |
|---|---|---|
| 003 | `de1f978:agency/jobs/AGY-2026-09-15-CUMINCO-CHOPSTICKS-001/gen/final/cuminco-chopsticks-9x16.mp4` (V1, 23.50 s) | `097e428e5929f1bd10d71bc68479dcbe6e011803629b198b616858e17b205d9d` |
| 003 | `…/gen/final/v2/cuminco-chopsticks-9x16.mp4` (22.875 s) | `adaeaa37e4c647a9ac24e986d8124ca6f86265172d23194019333db437693f8a` |
| 003 | `…/gen/final/v3/cuminco-chopsticks-9x16.mp4` (25.583 s) | `85d7410e8bc52717b4630944a5c3664cddf54ba776d43a689cfa9e9e766e67ae` |
| 003 | `…/gen/final/v3/cuminco-chopsticks-4x5.mp4` / `-1x1.mp4` | `f2252fd0…eea797` / `6b19bc1a…54d27e` |
| 003 | `…/gen/plates/plate-A-accepted.png` / `plate-B-accepted.png` | `9f4d17c3…790536e` / `c5c39a2d…ff6292a4` |
| 003 | `…/gen/vo/final-b1.wav` … `final-b6.wav` (raw 6.48 / 5.16 / 5.24 / 4.88 / 5.36 / 5.76 s) | `6f0b7f56…`, `18f8c3c0…`, `2917d1ef…`, `60dfb3a5…`, `f479ce69…`, `2b3f0600…` (full hashes in council 12 §0) |
| 001 | `f6ca66f:pilots/upwork-intro-video-2026-09-14/v4/assembly/v4.1/upwork-intro-v4.1.mp4` (ACCEPTED, 57.13 s, −14.9 LUFS) | `d1a5edf8836936eb7e27cec4350f4cce6f21f1d966778f7241544a2ad07e008a` |
| 001 | `…/v3/assembly/v3/upwork-intro-v3.mp4` (REJECTED, 59.87 s) | `ea81264d4103faa346b8937b50da4f785d5351f08aefc1e9bceb8d5df0052e51` |
| 002 | UPM (non-git) `tile-03-kora-threads/kora-hook-1-1x1.png`; `_rejected/tile-07-nivaas-homes-REJECTED-2026-09-15/nivaas-story-9x16-15s.mp4` | `d6a09e2e…327a536` / `d501c1fb…decfa14` |

Record conflict (OBSERVED, council 12 §0): `JOB.yaml versions[V1].assets` records the V1 9:16 file as `0fa7df99…` while the same file's QA row and the committed blob hash to `097e428e…`. UNKNOWN whether the human watched the committed blob.

---

## 1. Case 001 — UPWORK-INTRO-001 (57-s Upwork profile film; ACCEPTED at V4.1)

### 1.1 Timeline (OBSERVED; council 05 §1.1, council 11 §1.1)

| Version | Commit | Time (IST, 14 Sep) | Human verdict (`HUMAN-VERDICTS.yaml @ 3bb9a3c`) | USD reserved | Dispatches |
|---|---|---|---|---|---|
| package 1 | session created | 15:02 | — | — | — |
| V1 | `7629894` | 16:44 | `specific_repair`: "commercially clear, strong sales logic" but proof too small, phone/mockup framing, opening not exceptional, presenter blocks too long, range insufficient | 3.762 | 10 |
| V2 | `7b39aeb` | 17:21 | `rebuild_direction`: "competent, not extraordinary"; strategic correction — images AND videos co-equal, work owns majority of screen time | 4.320 | 2 |
| V3 | `70f687e` | 18:56 | `reject`: text cut off, colour lost, crops, inconsistent card geometry, **voice horribly robotic**, pacing rushed, presenter missing → HARD REQUIREMENT | 3.284 | 36 |
| V4 | `11d3e59` | 22:40 | `specific_repair`: "architecture finally worked"; offer/code collision, "and it can't suck" lost, bubble persisted, range proof, Express weak | 4.028 | 6 |
| V4.1 | `f6ca66f` | 22:56 | `accept` | 0 | 0 |

Totals: USD 15.393 / 54 dispatches; TTAO ≥ 7 h 53 m 35 s; 5 versions / 5 human cycles / 25 human-listed feedback items; USD 8.08 (52.5 %) in discarded lineages V1/V2; generation wait 14 %; unattributed human review + packaging gaps 48 % of the clock. Media-model failures reaching the Controller: 0 by the case's own count (with the internal inconsistency that REVISION-TRACE codes two defects `model_generation` / `model_audio` — council 10 §3.1).

### 1.2 Failure chains (K-coded)

| # | Failure | E | R | C | U | D | K | S | Q | Break + mechanism | K-codes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| a | Robotic long-form voice (V3, Sarvam ×16, ~48 s) | ✔ MF P8 "raw TTS robotic without rhythm rewrite"; RR-12 6/6 on ≤70-char lines | ✔ `preprod/ROUTE-ANALYSIS.md:38` lists the prior dir and says "**none is relied on below**" | ✔ | ✘ Lab 6/6 extrapolated to 1,000 chars | ✘ | ✘ | — | ✘ `vo_check.py` = transcript match 16/16 | Prior discarded by evidence-hierarchy rule (K4/K6); Lab cell mis-scoped (K5/K8); QA measured presence not delivery (K11); verdict after full assembly (K14) | K1 K4 K5 K6 K8 K11 K14 |
| b | Creative architecture re-litigated V1→V2→V3 | ✔ CANON-BRIEF `7629894` L18/L20/L65 ("open tight", "seller mark opening + last frame", "end on the package") | ✔ | ✔ | partial | ✘ opening rejected twice | ✘ | — | — | Knowledge in context did not change the opening; Karl review is an AI persona (K7); visual architecture never approved at storyboard level, only the script (K14); strategic correction supplied by the human after V2 (K6) | K3 K4 K6 K7 K14 |
| c | Text clipping (V3) | ✘ no layout rule in Canon; MF Theme 1 "Latin-only width math, no overflow guard" | ✘ | ✘ | — | — | — | ✘ `wrap2()` measures nothing after drawing | ✘ | Engineering; `v3-t33.5.png` "FIRST ORDER" pill cut (OBSERVED) | K0(Canon)/K1(MF) K10 K11 K7 |
| d | Contrast lost (V3, "HUMAN-CHECKED" over the dal photo) | ✔ CANON-BRIEF L52: ≥4.5:1, "headlines over the picture are named failures (sk_ogx_0028)" | ✔ | ✔ | ✔ | ✘ | ✘ | — | ✘ | **In context and ignored (K4), not absent (K0)**; a number in a 22.7 KB prose brief did not bind the compositor | K4 K11 K7 |
| e | Crops (V3) | K1 at best (CA-D6 is not a crop rule) | — | — | — | ✘ `cover()` default with fractional anchor | — | — | ✘ | Design default (K5/K10) | K5 K10 K11 |
| f | Video-created lettering (V3 Kling B2) | ✔ RR-11 / `canon/gate/textscan.py:234` "wired, never invoked" | ✔ | partial | — | — | — | — | ✘ still scanned, clip not | QA on the wrong artefact (K11); caught by the executor's eye | K1 K3 K11 |
| g | Route liquidity (fal 3.23 → 0.26) | ✔ balance read at plan time | ✔ | ✔ | ✘ cap ≠ liquidity | ✘ | — | — | — | K5 + no owner | K5 K6 |
| h | Long TTAO (5 assemblies, 48 % gaps) | — | — | — | — | — | — | — | — | Every human verdict on a fully assembled film; no storyboard round | K14 K6 K15 |

Decisive human inputs (OBSERVED, council 05 §5): touch 4 (V2 verdict: "work owns the majority of screen time") and touch 6 (V3: presenter = hard requirement + four compositor classes) define V4; they arrived after USD 8.08 and USD 3.28. Touches 1–3 produced two discarded lineages.

Jury verdict on V4.1 (council 12 §2.2, OBSERVED on frames): ACCEPT by 20 of 21 personas; residual fixes: 8.5 s with no super for a muted viewer, thumbnail grids unreadable at player size, Express card reads as a slide, diya flame at ≈36 s reads as fire. The one film of the three with assembly-level QA artefacts that match the frames.

---

## 2. Case 002 — UPWORK-PORTFOLIO-002 (nine tiles accepted, Nivaas story tile rejected twice and skipped)

### 2.1 Timeline (OBSERVED; council 05 §2.1)

| Event | 15 Sep | Source |
|---|---|---|
| pilot gates `v4/tools/design4.py` (TextBox, `contrast_ratio`, `place_text`, contain/cover) exist on the batch's base commit | 14 Sep 22:56 (`f6ca66f`) | branch |
| runtime gates on PR #98 branch (`344f517` 23:34; frame hygiene 23:49; pools 00:02) | 14–15 Sep | `git log --follow` |
| B1 export folder born | 07:52:24 | APFS birth |
| B1 defects: 8 messages / 10 defects | 07:59–08:18 | HUMAN-VERDICTS |
| PR #98 merged to main | **08:04:05** | `git log --merges` |
| first paid call | 08:05:49 | ledger |
| N1 call / operator accept / Controller reject | 08:28 / 08:39 / 08:43 | |
| N2 reject + skip; handover (implicit accept of 9) | 08:58 / ~09:05 | chat only |
| archive commit | 12:31 (`b4b77fa`) | |

Totals: USD 4.660 / 8 paid calls; 1 h 07 m 33 s lower bound; 13 human-flagged defects on the first export; 5 review cycles; USD 3.53 (75.7 %) on the rejected Nivaas tile; 7 of 9 accepted tiles were USD-0 re-exports; process NON-CONFORMANT (PD-01…PD-09).

**The decisive bypass (OBSERVED):** the batch tools `compose_v4.py`, `compose_pf.py`, `export_tiles.py`, `ad_9x16.py`, `nivaas*_build.py` import `adcomp` (the V2 rasteriser) and none of `design4`, `runtime.compositor`, `frame_hygiene`, `pools`. The case README's "bypassed the workflow merged the same day" is literally true, but the same-branch gates written nine hours earlier were also skipped. Three copies of the same gate ideas existed (runtime, pilot design4, job compose) and the deliverable path used the one without gates.

### 2.2 Failure chains

| Defect | Chain | K-codes |
|---|---|---|
| Text clipping HD-01/02 | Gates existed twice (design4, runtime `check_text_bounds`); neither imported; fix lives only in `compose_v4.py:120` (5 % margin) on the archival branch | K12 K13 K11 |
| Low contrast HD-04 (Kora cream serif on beige) | CONTRAST_GATE existed twice; V3 Kora poster exported as-is; `PRODUCT-LEARNING-V3.md §G` had proposed the Kora register as a template minutes before V3 was rejected — nobody revoked it | K12 K13 K7 K6 |
| Text over subject HD-03/05/07/08/09/10 | No obstruction check anywhere (K0 in code); Canon named it (sk_ogx_0028 in CANON-BRIEF) (K4); MF prompt had reserved a copy zone in the plate (K13 vs MF) | K0 K4 K13 K6 |
| Destructive crop HD-06/11 | `compose_v4.cover()` is the V3 `cover()` verbatim; CROP_FIT_DECLARATION existed in design4 and runtime | K12 K13 K10 |
| Narration hole HD-13a (Nivaas N1, 1.5–2.9 s silence inside a sentence) | `speaker_check.py` transcript-presence accepted 08:39; Controller rejected 08:43; same operator wrote RO-05 ("verbatim on transcript; rejected by ear") ~10 h earlier and chose Veo t2v+extend again despite RO-02 | K11 K13 K5 |
| Two narrator identities HD-13b | No cross-clip check existed; MF HANDOFF had named "no cross-asset consistency" as a known gap | K0 K5 K1 |
| Process PD-01..09 | chat "go" as the only authority; copy invented during execution; no packet/cap/ledger | K12 K14 |

Jury (council 12 §3): published tiles are clean and consistent; every HD-01…10 defect is fixed in the B2 files on disk; honest weaknesses are creative range (one photo per brand), Kora type size, "in motion" clips that are crossfaded stills. Nivaas rejection confirmed by measurement (silence 6.63–8.15 s mid-narration; 720p soft exterior). All 13 defects except HD-13b were single-frame or audio-measurable; HD-13b (two voices) is ear-only.

---

## 3. Case 003 — CUMINCO-CHOPSTICKS-003 (18–25 s spec film; REJECTED ×3)

### 3.1 The brief and what was decided before the first dollar (OBSERVED; council 04 §A)

Brief (`JOB.yaml brief.verbatim @ de1f978`, received 13:17:42Z 15 Sep): "…make a video on how to hold chopsticks for them using their product images … a very calm empathetic voice doing a voice over … step 1, step 2, step 3 … the boy fails but they still happily eat through their cumin cookware." The word "ad" appears once; the content described is a tutorial. Reframing into an ad was the agency's job.

Asked of the human (four questions, answered 13:28:37Z): spend cap (USD 8); "approve the frozen copy deck and VO lines" (five strings + five VO lines); pool attestation; spoon vs fist ending. Plus one unsolicited intervention: "not fal" (13:39Z).

Decided by the operator alone at 13:27Z, unchallenged: product = 15 cm Ceramic Ramen Bowl; three steps; single generated narrator; 18 s / five beats; 9:16 master with 4:5 and 1:1 as crops; **`cta: none in-frame`**; `offer_placement: none`; brand line only in the last beat; hook "a noodle slips back into the bowl in the first second"; VO line timings fixed 31 minutes before the first TTS call; 21 Canon check lines all rendered "pass" (20) / "n-a" (1); `deviations: []`; **`reviews: []`**. The "Karl disconfirmer / Ezra copy" personas PRODUCTION-WORKFLOW §5 tells the operator to consult do not exist anywhere in the repository (`grep -rl -iE 'disconfirmer|persona review'` hits only the skill).

### 3.2 Timeline (UTC; OBSERVED from `gen/LEDGER.jsonl`, `gen/ATTEMPTS.jsonl`, commit times; council 04 §B)

| UTC | Event | USD cum. | Human touch |
|---|---|---|---|
| 13:17:42 | job opened; brief verbatim | 0 | brief |
| 13:23 | Canon lookup: 10 packs selected, **2 injected, 8 gaps** (incl. `commercial_communication`, `critique_and_effectiveness`); prefix 5,298 tokens, 21 check ids | 0 | — |
| 13:27:15 | `86ec183`: intake, NR, blueprint (21 checks "pass"), plan, VO lines **with timings** | 0 | — |
| 13:28:37 | start-of-job summary; cap USD 8; deck frozen; pools attested; ending = spoon | 0 | 4 answers |
| 13:33 | fal balance USD 0.147 → fal plan blocked | 0 | — |
| 13:39:26 | "not fal"; credits-only routes; 10 prompts gated GATE PASS ×10 | 0 | "not fal" |
| 13:39:37–13:57 | plates H1 r1/r2, A r1 (garbled embossed mark, DF-01) → A r2, H2, H3; clip-2 micro-qualified | 1.069 | "r2", "accpet", "plates are good to go" |
| **13:58:07** | **voice search begins** — 18 min after the first paid plate: Sarvam priya/shreya, ElevenLabs Sarah `EXAVITQu4vr4xnSDxMaL` (the voice MF recorded as rejected in July) | 1.085 | round 1: "all three are robotic" |
| 14:00–14:17 | rounds 2–5: Hindi Sarvam ×4, ElevenLabs ×5 (one quota fail at 54 credits after the pool was attested), Gemini TTS ×11 | 3.18 | "stick to english… why ae we not using veo models with voice?… clam + cheerful"; "leda is good… slower… shrillness missing"; "bubbly" (locked 14:17) |
| 14:06:36–14:09 | plate-B; **clips 1, 3, 4 dispatched during voice rounds 2–4** | 2.98 | "plate b is accepted" |
| 14:10–14:21 | music; clip-5; five VO lines generated **after every clip** (one PROHIBITED_CONTENT false positive) | 3.84 | — |
| 14:37 | V1 assembled (23.5 s vs 18-s plan) | 3.88 | — |
| ~15:0x | V1 verdict | | **"crapy. the video has got some random audio. her lips are omving. the text is coming on figures. all messed up"** |
| 16:59–17:00 | clip-1 r2, clip-5 r2 (closed mouths) | 5.08 | — |
| 17:22 | V2 (22.9 s; beat-1 VO dropped) | 5.08 | **"did cannon say nothing about product positioning? the closing shot should have cumin product and final caption. it does not look like ad at all. the opening is missing too. canon had this knowledge. how's that possible?"** |
| 17:30 | spoken close "Ramen night at home. Cumin Co." (one TTS line) | 5.0907 | "go ahead fix it" |
| 17:48 | V3 (25.6 s; persistent brand mark; end card from brand photo; "ABCD" first appears in the job record at `c0f849c`) | 5.0907 | — |
| 16 Sep 03:45 | **"this is still bad. the voices are overlapping. not at all happy with it. reject completely. we need to do the diagnosis now. tranfer the info to canon"** | 5.0907 | V3 REJECT |

Totals (recomputed): 50 attempts (47 ok); USD 5.0907 of an 8.00 cap (Veo ×7 4.200; NB2 ×8 0.536; Gemini TTS ×18 0.173; ElevenLabs ×8 0.099; Lyria 0.060; Sarvam ×8 0.023); 34 voice attempts / 27 qualification takes / 5 rounds / USD 0.295; 18 human touches by enumeration (record says 10 cycles); job-open → V3 presented ≥ 4 h 30 m; job-open → final reject 14 h 27 m. **Timestamp conflict (OBSERVED):** the case's TIME-AND-COST says "working span ≈ 3 h (13:17–16:15Z)" and REVISION-TRACE says V2 elapsed "≈0:35"; the ledger shows V2 clips at 16:59Z, V3 at 17:48Z. The record understates the working span by ≥ 1.5 h.

### 3.3 What is actually on screen (OBSERVED on frames; council 12 §1.1)

V3 9:16: 0–3 s static two-shot, she lifts noodles to her mouth, he holds one stick in a fist, nobody fumbles; brand mark absent at frame 0 (fades in by 0.3 s, top-right although the code comment says top-left); 3–8.5 s macro of her hand, sticks crossed, **5.5 s in which nothing moves**; 8.5–13.5 s noodle bundle lifted and dropped; 13.5–17.5 s his hand — a single strand lifts cleanly, sticks go progressively vertical (the etiquette the brief forbids); 17.5–21 s two-shot, **she laughs mouth wide open 17.5–18.8 s under the VO line**, he eats with a wooden spoon, her chopsticks lie across the rim, **not in the rim notch** the blueprint called "the blog's own product argument"; 21–25.6 s end card built from the brand's lifestyle photograph (different bowl finish, different kitchen, stir-fry not ramen), bottom 25 % empty.

Audio (measured): VO chain re-run on the committed wavs (edge trim −50 dB, atempo 1.10): b1 ends 5.62 s → **overlaps b2 by 0.92 s**; b6 ends 26.54 s → **overruns the 25.6-s film by 0.94 s**. Confirmed on the no-music master (speech continuous 3.49–8.81 s; last silence at 25.21 s). **V1 had the same class of defect (0.63 s overlap) and the V1 diagnosis missed it** — DF-02 blamed silence removal and loudnorm only; V2 masked it by dropping b1; V3 restored b1 with the same hand-set start table. TTS direction was "bubbly, bright, high-energy" against a brief that asked for "a very calm empathetic voice"; no human verdict on voice character was ever recorded (`human_ear_verdict: null`).

### 3.4 The six load-bearing chains (OBSERVED unless marked; councils 04 §C, 06 §4, 15 §1)

| # | Failure | E | R | C | U | D | K | S | Q | Break + mechanism (cite) | K-codes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Tutorial, not an ad (HD-06 / DF-07) | ✔ `google-abcd-video-ads/source-knowledge.yaml @ 711163e` L667 "Brand early, often, and richly", L737, L1291 "Ask them to take action", L1799 "finish with the product"; Hopkins `sk_hop_sa_0026`; StoryBrand `sk_sb_c003_0011`; `qa_abcd_0010`; MF receptionist forced `cta`/`headline` | ✘ **BROKE**: `commercial_communication` fired (JOB.yaml L113), excluded (L114), listed under `missing_domains` (L115). Five separate blocks: C-10 (`CONTROL-STATE.md` L81/L95/L247), `packs.py` L11 continue-on-gap, `doctrine.py` L33 two-pack hard-code, `compile_pilot_packs.py` L491-503 two-pack hard-code, WORKFLOW L118-119 "Do not compile, paraphrase or invent a pack for a missing domain. Proceed on the brief… record the gap only if the production actually fails for want of it"; Q&A form excluded by four contracts | ✘ by policy | — | ✘ `cta: none in-frame` (L48), `offer_placement: none`, brand line last beat | ✘ | — | ✘ human | Retrieval blocked by **policy, not algorithm**; then no owner and no challenger (`reviews: []`); the human approved five strings, never the proposition. Post hoc proof that rungs 4–6 work: once the human named it, the operator applied ABCD correctly in one pass at USD 0 + one TTS line (`c0f849c`) | **K2 (by design) K3 K6 K7 K14 K5** — not K0 |
| 2 | No opening / hook (HD-05) | ✔ ABCD L462 "start in the middle of the action, or open with a close-up"; case 001 rejected **twice** on the opening (HUMAN-VERDICTS L19, L31) — mandated reading | ✘ pack; case in context as narrative only | partial | ✘ | ✘ hook chosen by *excluding* a clip window where "he lands noodles in his mouth"; V2 dropped beat-1 VO → an opening with no words, no product, no brand | ✘ | — | ✘ | Field (`hook`) with no doctrine and no check behind it; 001's opening verdicts never promoted beyond README prose | K2 K13 K5 K7 K11 |
| 3 | Weak product role (HD-04) | ✔ **PA-D7 compiled and injected** ("does the imagery earn its space commercially?") | ✔ | ✔ | ✔ operator wrote it in pack vocabulary | ✘ **self-marked "pass — 'the bowl on a noodle night' sells at a glance; the hero image needs no copy"** (L157) | ✘ | — | ✘ NOT_MECHANISED (`predispatch.py` L39-41) | **Rung 5–6: self-attestation.** DEFAULT text ("size imagery by importance to the sale, never decoration") never printed by BOOTSTRAP §2; CHECK is a one-line self-test; no reviewer. Jury: product is scenery; Product Storytelling test FAILS (replace the bowl with any pastel bowl and nothing changes); rim-notch argument in no frame | **K7 K4 K11** |
| 4 | Text over people (V1 "text is coming on figures"; DF-04; 4:5/1:1 to V3) | ✘ **no Canon claim (K0)** — regex over 1,300 SK + 1,191 terms: 0 hits; adjacent: 002 candidate TEXT_OVER_IMAGERY_CONDITIONAL, CF2 human row, MF copy-zone prompt | ✔ case read | ✔ `product_placement: "never obstructed by text"` | partial | ✘ CF2 self-marked "PASS on 9:16 (copy on empty wall, nothing over bowl/hands/faces)" (L326) against a 4-frame contrast probe with no obstruction test | ✘ | — | flag written, not read: CF2 FLAGGED on 4:5/1:1 in V1, V2, V3 — presented anyway (9 deviations in `4x5.qa.json`, 11 in `1x1.qa.json`) | Engineering gap + self-attestation + "flagged ≠ not a candidate" has no rule | K0(Canon) K7 K11 K13 K14 |
| 5 | Robotic / wrong-register voice; 26 takes, 5 rounds | ✔ MFH `MEDIA-FACTORY-ROUTING-PRIOR.md` L28-29 "raw TTS sounds robotic without speech-rhythm rewrite + mix"; "EL western voices … rejected by ear even in English (el_sarah_v3.mp3)"; 001 RO-05 (n=16) | MF ✘ (`runtime/route/evidence.py` reads TAINT-REGISTER only; `historical_prior` unjoined; BOOTSTRAP never loads priors) / case ✔ (`learning_applied` cites RO-05) | case ✔ | rationalised: "VO here is ≤ 5 short lines" | ✘ Sarvam ×8, ElevenLabs Sarah first | ✘ | — | human ear ×5 | RO-05 is `routing_authority: none` **by rule**, so it can never change route rank; voice qualified *after* plates and *during* clips 1/3/4 (contrary to the job's own MQ order); no house default for "calm-cheerful Indian English"; Gemini TTS (the route that worked) has no cell and no roster row | K1 K3 K4 K5 K6 K8 K13 K14 K15 |
| 6 | VO overlap / overrun (DF-08) | ✔ interval arithmetic; MF `spike/assemble.py` placed VO by measured wav duration (never referenced in MI); doctrine "text overflow fails closed" not generalised to audio | ✘ | ✘ | — | ✘ `VO = {beat: (file, start_s)}` hand-set from the 18-s plan; no wav ever measured | ✘ | ✘ | ✘ D14 "pending human ear" when V3 was presented | Engineering (K10) + declared check not run (K11) + intra-job K13 (V1's overlap undiagnosed) + K5 (VO before timeline); `check_vo_schedule` now exists on PR #103 with **0 callers** | K5 K10 K11 K13 |

Other Cumin defects (council 10 §3.2 re-coding): DF-01 garbled embossed mark = K9 + K4 (001 RO-04 "environmental-text redraw" not in `learning_applied`), caught by the human plate gate (K14 correct); DF-02 "random audio" = K10 + K11 + K7 (D11 "loudnorm −14 LUFS" self-PASS on the pumping V1 mix, measured −14 → −37 dB per-second RMS); DF-03 mouths under VO = K5 planning (001 RO-01 / 002 RO-02 recorded Veo animating mouths; prompt did not forbid speech) + K9; **the r2 repair still cut in on an open mouth** (clip-5-r2 in-point 1.0 s inside a laugh to ≈2.5 s; compose comment says 1.2 s); DF-05 23.5 s vs 18-s plan = K5 + K1 (blueprint stores VO `t:` as plan values); DF-06 attempt-id collision = K10/K12 tooling, misclassed `infrastructure_transient`.

### 3.5 Detectability before spend (OBSERVED; council 12 §1.5)

| # | Defect | Visible before any clip credit was spent? |
|---|---|---|
| C1 | No hook event in beat 1 (she eats; he is passive) | **YES — on `plate-A-accepted.png`** |
| C2 | Beat 4 shows a clean lift, then vertical sticks (forbidden) | on the first clip contact sheet; a storyboard would have specified the miss |
| C3 | Rim-notch payoff absent | **YES — on `plate-B-accepted.png`** (sticks across the rim / on the table) |
| C4 | Mouth open under VO | per clip YES from `qa/clips-1-5-r2-faces.png`; whether it lands under a VO start only after assembly |
| C5 | VO overlap / overrun | **YES by arithmetic** (start table + trimmed durations), no frames needed |
| C6 | Cards over chopsticks in 4:5 / 1:1 | **YES — the QA JSON already flagged it (CF2)**; needed a reader, not a detector |
| C7 | End-card world mismatch | YES from the composite alone |
| C8 | Beat 2 dead time (5.5 s static) | YES — seven identical frames on the contact sheet |
| C9 | Product Storytelling failure (generic bowl would do) | YES from the blueprint + plate set |
| C10 | Voice register vs brief ("bubbly" vs "calm") | YES from the TTS direction string |
| C11 | V1 mix pumping | only after mix; measurable without listening |
| C12 | Brand mark missing at frame 0 | YES — first frame |

**Eight of twelve were visible on plates, a storyboard, a prompt string, or by timeline arithmetic before assembly.** No storyboard artefact exists in any of the three jobs; the closest thing (001 `CREATIVE-BLUEPRINT-V4` per-beat table) belongs to the accepted film.

### 3.6 Actual sequence vs PRODUCTION-WORKFLOW (OBSERVED; council 04 §D)

Fourteen stages followed formally; three departures matter: §5 persona review skipped against personas that do not exist; micro-qualification order reversed (voice was MQ-2 "by ear first", ran after plates and during clips); §11 CF2-flagged geometries presented three times. Where the skill is silent: the only creative guidance in 8,035 words is §5's 14-row field table (192 words) + the JOB-TEMPLATE blueprint block (115 words) + one sentence in SKILL.md ≈ 370 words ≈ 4.6 %. Nothing says a product must be hero, an ad must open on something, a CTA must exist, or brand must appear early; "Canon constrains; it does not direct" and §4 "proceed on the brief" push toward literal execution. Zero creative rows in the red-flag table; zero ad-structure rows in QA-CHECKLIST.

### 3.7 The operator's own diagnosis and PR #103 (OBSERVED; council 04 §E)

Accurate: ledger totals reconcile; overlap is real; "every rejection landed on an unmeasured dimension"; VO-first and the schedule gate are correct; model-vs-pipeline tally (1 vs 5, actually 6 with SD-09) is fair.

Does not hold: (1) "Canon gap" as root cause — the ABCD material exists but all its bindings are `proposed / not reviewed`, ABCD is flagged unfingerprinted and platform-contingent, and the operator (a frontier model) does not need a 4,096-token pack to know an ad ends on the product; the mechanism was §4 "proceed on the brief" + no gate + no reviewer + 21 self-passes. Coding it K0/K2 moves ownership to the Controller (C-10) when the failure is K6/K7/K14 inside the skill. (2) "CONFORMANT" is misleading (see §3.6). (3) Time claims contradicted by the ledger. (4) Every remedy is another gate or candidate; none adds a decision owner or a challenge step. AD_STRUCTURE_MINIMUM is the right instinct framed as a stop-gap "until commercial_communication is compiled"; it should be unconditional practice.

---

## 4. Recurrence table 001 → 002 → 003 (OBSERVED; council 05 §3, 10 §2, 02 §6)

| Defect class | 001 | 002 | 003 | Learning artefact between | Why it did not prevent |
|---|---|---|---|---|---|
| Text clipped / overflow | V3 SD-01 | HD-01/02 | not reported | TEXT_BOUNDS_GATE → `gates.check_text_bounds` (code, on main 08:04 15 Sep) | 002: tools import `adcomp`, not the gate; 003: imported by the job tool → held |
| Contrast lost | V3 SD-02 | HD-04 | V1 mis-sampled (4 frames) | CONTRAST_GATE; CANON-BRIEF numbers | 002: not imported; 003: gate present, sampling wrong (K10 in the caller) |
| Text / UI over subject | V3 (HUMAN-CHECKED over dal); V4 SD-07 | HD-03/05/07/08/09/10 | **V1 "text is coming on figures"**; 4:5/1:1 to V3 | 002 candidates TEXT_OVER_IMAGERY_CONDITIONAL / SUBJECT_AWARE_CROP_ANCHORING; skill CF2 (human row) | Promoted only to a human row; self-assessed PASS; third private implementation (`wall_obstruction`) now a candidate again; not in runtime on main or PR #103 |
| Destructive / accidental crop | V3 SD-03 | HD-06/11 | SD-09 (4:5/1:1 no copy zone) | CROP_FIT_DECLARATION; FORMAT_SPECIFIC_REVALIDATION | 003 per-geometry QA **flagged** it (state 8) and the deliverable was still a re-crop; new candidate GEOMETRY_NEEDS_ITS_OWN_PLATES |
| Robotic TTS | V3 SD-05 / RO-05 (Sarvam ×16) | — | rounds 1–3 (Sarvam 8/8, ElevenLabs 6/6 rejected) | MF P8 (Jul) → RO-05 directional → skill D10 → JOB micro-qualification by ear | Written **three times** (MF, 001, 003); promoted ✗ (RR-12 unchanged; MF fix never entered MI); VOICE_BY_EAR_FIRST (003) = SPEAKER_MICROQUALIFICATION (001) = MF "speaker chosen by human ear" |
| Chained-generation degradation | V2 RO-02 | N1 (extend split narration) | — (003 cited "no extend chains") | RO-02 directional | Same operator chose extend again next morning; propagated on the third job |
| Narration holes / overlap at joins | — | HD-13a/b | **DF-08** | CROSS_CLIP_VOICE_CONTINUITY (skill D14, human ear) | Promoted to a human row; V3 shipped with D14 "pending"; `check_vo_schedule` now first deterministic audio gate, 0 callers |
| Video lettering | V3 SD-06 | — | — (7/7 clips clean) | VIDEO_FRAME_TEXT_HYGIENE (dry loop) + skill D1 | Propagated as a human-eye pass; detector "not authorised" |
| Pool liquidity ≠ cap | V3/V4 SD-11 | — | ElevenLabs quota at 54 credits mid-search; pools *attested* not read | PROVIDER_POOL_AVAILABILITY (`pools.py`, dry bridge) + skill A7 | Code exists; agency path satisfied A7 by chat attestation |
| Creative architecture unowned / "not an ad" | V1–V3 (three architectures) | — | V2 "does not look like an ad at all" | 001 CANON-BRIEF had ABCD/Ogilvy by id; pack uncompiled; **three cases, three contradictory diagnoses** (001 "no new Canon need was proven"; 002 "not missing Canon knowledge"; 003 "Canon gap") — never reconciled | Knowledge reached 001 by a hand-written brief, not a pack; the agency path consumes packs only |
| Paid calls without packet/cap/ledger | — | PD-01..09 | conformant | PAID_PRODUCTION_PREFLIGHT | **The one clean propagation success** — and the job still failed on quality |

Summary (INFERENCE): of ten recurring classes, one was prevented by propagation; three were *detected* by the propagated mechanism and still shipped or still cost rounds; six recurred because the artefact was a case file or a checklist row that no code path or independent reviewer enforced. Every class had a documented Media Factory analogue (council 02 §6) and nothing in MI references MF's fixes (`contrast.ts pickInk`, `assemble.py` measured-duration VO, receptionist forced `cta`/`headline`, idle-plate "mouth stays closed" prompt).

---

## 5. Human attention accounting (OBSERVED; councils 05 §5, 09 §Q6, 11 §5)

| Case | Questions asked of the owner | Verdict / gate rounds | Defects the human found | Defects a gate found first | Decision points |
|---|---|---|---|---|---|
| 001 | 7 blocking questions + script v5 approval | 5 | 25 | 0 | 13 |
| 002 | 3 confirmations + 3 "go" | 5 | 13 | 2 (operator eye) | 11 |
| 003 | 4 intake questions | 8 pre-assembly gates (plates, clip, 5 voice rounds = 26 takes judged by ear) + 3 versions | 8 | 1 (DF-01) | 15 |
| Total | 14 | 25 | **46** | **3** | **39** |

Case-003 review points ranked by information gain vs when they happened:

| # | Intervention | UTC | Info gain | Review cost | Dependent spend | Altitude |
|---|---|---|---|---|---|---|
| 1 | Start-of-job bundle (cap + five strings + attestation + ending) | 13:28 | high but **bundled**; blueprint never approved separately | ~5 min | USD 5.09 | strings, not proposition |
| 2–4 | plate r1/r2; clip-2; plates A/H2/H3/B | 13:42–14:06 | medium (confirmed things that were already fine) | ~11 min | clips 3.00 + music + VO | component |
| 5 | Voice rounds 1–5 | 13:58–14:17 | **high — the register** — but clips 1/3/4 bought during rounds 2–4 | ~20 min | in practice nothing: dependents already bought | take-level casting by the customer |
| 6 | V1 reject | ~15:0x | high (3 defect classes) | ~5 min | 1.20 redraws | assembly |
| 7 | V2 reject | ~17:2x | **very high; proposition-level; after USD 5.08 of 5.09** | ~5 min | 0.01 + V3 | assembly |
| 8 | V3 reject | 03:45 +1 d | low (deterministic defect) | ~3 min + overnight | 0 | assembly |

INFERENCE: in all three cases the decisive information arrived after full assembly (001, 003) or after export (002); no case had a human touch at storyboard or animatic altitude; the human was simultaneously client, art director, casting director, QA and treasurer. Expert work pushed upward: plate choices, voice casting by ear (26 takes), pool attestation, tile direction before render.

---

## 6. Cross-case pattern (INFERENCE from §1–5)

1. **Models delivered; the system around them lost the jobs.** 3 of 46 defects reaching the human were media-model failures.
2. **Gates measure layout arithmetic on numbers the caller supplies**; every rejection landed on delivery (voice), structure (ad-ness), obstruction, continuity or scheduling — none seen by a gate that was on the path.
3. **Approval altitude was wrong in every case**: strings, plates, takes and full films were approved; proposition, structure and storyboard never.
4. **Self-attestation stood in for review** in every case: Karl (an AI persona) in 001; the operator's accept overturned by the Controller four minutes later in 002; 21 check lines + CF2 + D11 + D14 in 003.
5. **Learning propagated as prose or as library code**, and only the one propagation that became a mandatory preflight step (packet/cap/ledger) actually held. The taxonomy has no slot for K7, K13 or K14, so each recurrence was filed as "pipeline failure" and answered with another gate.
6. **Case 002 — the bypassed workflow — had the best TTAO and lowest per-tile CpAO; case 003 — fully conformant — failed three times.** At n = 3, process conformance is not correlated with acceptance (council 11 §9).

Conflicts reported, not harmonised (OBSERVED): 003 human cycles 10 stated / 11–12 enumerated; 003 V2/V3 times (record vs ledger); 001 "54 dispatches" vs V3 "37 calls" vs ledger 36; 001 SD-05 `pipeline_failure` vs REVISION-TRACE `model_audio` vs 003 RO-04 "model observation" vs RR-12 clean default (four statuses for one Sarvam behaviour); `CONTROL-STATE.md:196-199` "gates promoted into the runtime" vs the call graph (library only); 001 V1 9:16 hash mismatch in `versions[]`.
