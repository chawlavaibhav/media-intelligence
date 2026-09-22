# PART 2 — PERSONA EXPECTATION MAP

Each row: what the persona expects from the pipeline → what the current system actually supports → the observed failure with its citation. Verdict evidence: `production-learning/cases/UPWORK-INTRO-001/HUMAN-VERDICTS.yaml @ 3bb9a3c` (001), `…/UPWORK-PORTFOLIO-002/HUMAN-VERDICTS.yaml @ 3bb9a3c` (002), `de1f978:agency/jobs/AGY-2026-09-15-CUMINCO-CHOPSTICKS-001/JOB.yaml versions[]` and `1de2b37:production-learning/cases/CUMINCO-CHOPSTICKS-003/HUMAN-VERDICTS.yaml` (003). Jury verdicts on the actual media: `council-reports/12-craft-jury.md`. All OBSERVED unless marked.

## A. Customer / commercial

| Persona | Expectation | Current support | Observed failure |
|---|---|---|---|
| 1 Founder / Brand Owner | "Did you infer what I didn't know to tell you?" | Intake fields + `intake.assumptions`; four questions asked (cap, deck freeze, pool attestation, spoon-vs-fist) | Cumin brief said "an ad … how to hold chopsticks step 1 2 3"; the operator built the tutorial literally, decided `cta: none in-frame`, never surfaced proposition/product role/close as decisions. V2 verdict: "did cannon say nothing about product positioning? … it does not look like ad at all." (`04` §A.3) |
| 2 CMO | Brand-safe, predictable review cycle, two rounds | Verbatim verdict capture; bounded repair | 5 / 5 / 10 owner review cycles; a CMO's two rounds exhausted before internal repair round 3 (`03` §3) |
| 3 Performance Marketer | Stop, communicate, prove, move to action | Blueprint fields hook/offer/proof/cta exist | Cumin: hook not in picture (first 3 s a static two-shot), no proposition, CTA only in the last 4.6 s at 38 px (jury §1.3); 001 V1 "video proof too small", "opening not visually exceptional" |
| 4 Media Buyer | Placement-correct: Reels safe band, 4:5, 1:1, clean audio | Per-geometry QA rows (CF1–CF5) after case 002 | 003 4:5/1:1: nine and eleven CF2 deviations "recorded for the human", brand mark absent on most beats, delivered anyway ×3; V1 "random audio", V3 "voices overlapping" (measured 0.92 s) |
| 5 DTC Growth Lead | Product visible, understandable, persuasive; "every request within 24 h" | Product fidelity check B2 (human eye vs packshot) | Product as scenery: generic bowl would change nothing (Product Storytelling test FAILS, jury); no retainer request ever fulfilled; clock board deleted for lack of honest time (UP LOG l.115) |
| 6 Agency Account Director | Translate vague brief into a complete production brief without making the client do our job | Intake→NR→blueprint stages exist on paper | Plate choices, voice casting by ear (26 takes), pool attestation pushed to the owner; 39 decision points across three jobs; no acceptance contract on 002/003 (`11` §5, `10` §4) |
| 70 Skeptical Agency Owner | Show me money and misses | Honest ledgers; ACCOUNTABILITY floor | USD 0 revenue, 2 proposals sent 0 viewed; net ≈ −USD 440/month at 10 jobs if owner time is priced (`11` §7) |

## B. Audience / communication (jury on the actual media)

| Persona | Expectation | Current support | Observed failure |
|---|---|---|---|
| 7 Cold Viewer | A reason to continue in 1–3 s | `blueprint.hook` field | Cumin V3 first 3 s: two people looking down at bowls; the promised "noodle slips back" is not on screen. V1 first frame: man slurping with a grimace. REJECT (jury) |
| 8 Target Customer | Understand what is sold and why it matters | `remember` field | "How to hold chopsticks" reads as instruction; the demo is no clearer than the blog. ACCEPT-WITH-FIXES |
| 9 Distracted Mobile Viewer | Works muted, low attention | `muted_test` field (self-marked yes) | Muted test genuinely passes; beat 2 is 5.5 s of a static hand (dead time). Intro film: 8.5 s with no super for silent viewers |
| 10 Persuasion / Attention | Attention directed intentionally | CA-D1 "one cue per beat" (self-marked pass) | Attention order text→hand→bowl; the bowl is never the object of a cue. REJECT |
| 11 Communication Strategist | One proposition, one hierarchy | `proposition` absent from intake; `remember` = mood line | "Ramen night at home" is a mood, not a reason. V1/V2 no proposition, no brand early, no end. |

## C. Creative / advertising

| Persona | Expectation | Current support | Observed failure |
|---|---|---|---|
| 12 Advertising Strategist | Is it an ad? proposition? action? | PA-D7 (one compiled decision; self-attested; NOT-MECHANISED) | V1/V2 not an ad by any structural test; V3 formally an ad (mark + end card + URL) with no proposition. Hook→proposition→proof→payoff→action: hook missing, proposition missing, proof is of chopsticks not bowl |
| 13 Creative Director | One coherent idea worth producing | `blueprint.concept` | Concept "Bottom stick, still." is the blog's idea, not the brand's; no independent CD review (`reviews: []`) |
| 14 Art Director | Composition, hierarchy, product, type, palette support the idea | PA-D1..D10, CA-D1..D11 injected; compositor gates | 9:16 clean (ACCEPT); 4:5 and 1:1 cards over chopsticks (REJECT); end card is a slide |
| 15 Copywriter | Hook, headline, proof, brand line, CTA doing distinct jobs | Frozen copy deck; C6 byte-check | Deck has no hook line and no proposition line; "Pinch… and… nearly." buried under an open-mouth laugh |
| 16 Brand Strategist | Remembered for the intended reason | `brand_world` | End-card photo breaks the film's world (different bowl finish, kitchen, dish); embossed mark hidden by design after DF-01 |
| 17 Product Storytelling Director | Could a generic object replace the product? | None | **YES, it could.** Rim-notch payoff (the blueprint's own "product argument") is in no frame (`plate-B-accepted.png` sticks across the rim) |
| 18 Story / Narrative Designer | What changes beginning→end; product's role | Beats table | Brief's story (he fumbles→she shows→he fails→they eat) is not on screen: plate-A shows HER eating; clip-4 shows a clean lift then upright sticks (forbidden); beat 5 spoon pays off a failure that never happened |
| 19 Direct-response | Hook→proposition→proof→payoff→action located | `cta_placement` field | `cta: none in-frame` decided by the operator at 13:27 Z; URL added in V3 after rejection |
| 20 Indian-market Creative | Native handling of language, register, platform | Hindi copy origination rule; Sarvam/ElevenLabs/Gemini routes | Voice: 26 takes; "bubbly, high-energy" direction contradicts brief's "very calm empathetic"; Hindi option tested and dropped without recorded reason; 001 Hindi tiles shaped correctly (Devanagari OK) |

## D. Visual craft

| Persona | Expectation | Current support | Observed failure |
|---|---|---|---|
| 21 Graphic Designer | Hierarchy, spacing, safe areas, consistency | `check_text_bounds/contrast/fit/geometry/disjoint` (case 001 → runtime lib) | 002 B1: 13 defects incl. text over figure, banner over photos, edge touch — gates existed on the same branch and were not imported (`05` §2) |
| 22 Typography | Legibility, shaping, exactness | HarfBuzz + Pillow; byte-check | Exact characters held in all three cases (the one promise that holds); Kora 16:9 ≈ 24 px; end-card stack over-articulated |
| 23 Composition Photographer | Figure/ground, lighting, product | PA-D1..D6 | Held: one window source, consistent palette (Canon's real contribution, `04` §F) |
| 24 Product Photographer | Product identifiable, desirable, important | B2 fidelity vs packshot | Bowl reproduction good; identifiable only by colour (mark hidden); product as base of frame for 14 of 23.5 s |
| 25 Cinematographer | Framing, motivation, continuity | CA-D7..D11 | Identity stable across V1–V3 (held); macros static locked-off; nothing motivates the cut two-shot→macro |
| 26 Storyboard Artist | Story understood before spend | None — no storyboard artifact exists in any of the three jobs | 5 of 7 Cumin story defects visible on a six-panel board from the accepted plates (jury §1.5) |
| 27 Motion Designer | Animation hierarchy, transitions | Fades 0.35/0.3 s | End-card zoompan reads as slideshow; "in motion" portfolio clips are crossfaded stills |
| 28 Compositor | No obstruction, no clipping, no collisions | Gates for bounds/contrast/disjoint (text-vs-text); CF2 obstruction is a **human** row | Obstruction of the subject by copy occurred in all three cases and is still not code (`05` §3); Cumin CF2 self-marked PASS then "text is coming on figures" |

## E. Film / audio / post

| Persona | Expectation | Current support | Observed failure |
|---|---|---|---|
| 29 Film Director | Performance + camera + pacing serve intent | i2v prompts "one cue" | The film has no event; the miss was never staged; model returned clean lifts |
| 30 Editor | Cut motivation, beats, no dead time | CA-D10 hold ≥ 3.3 s (template number) | Cuts on VO starts not action; 5.5-s static beat; 25.6 s vs 18-s plan (+42 %) |
| 31 Sound Designer | Music role, ducking, atmosphere | ffmpeg chain (job-local) | V1 mix pumps −14→−37 dB per-second RMS; no room tone, no foley (chopstick-on-ceramic would sell the product) |
| 32 Voice / Casting Director | What should the speaker feel like; is robotic fatal? | Micro-qualification by ear (candidate pattern) | 5 rounds / 26 takes AFTER plates; first ElevenLabs take was the voice MF recorded as rejected by ear (`04` §C.7); no naturalness instrument at any tier (`08` §2.6) |
| 33 Dialogue / VO Editor | Cadence, pauses, overlaps, timing | None until PR #103's `check_vo_schedule` (0 callers) | b1→b2 overlap 0.92 s, b6 overrun 0.94 s; the same class of overlap (0.63 s) was present in V1 and misdiagnosed (jury §1.2) |
| 34 Music Supervisor | Emotion/energy; not fighting dialogue | Lyria bed, sidechain 4:1 | Never judged separately; a no-music variant shipped (operator unsure) |
| 35 Post-production Supervisor | Individually acceptable assets compose into one acceptable film | Acceptance per asset (plates, clip-2, voice) | Assembly never approved as a timeline: overlap, open mouth under VO, card-over-subject, end-card world mismatch are all assembly-level. REJECT |

## F. Production

| Persona | Expectation | Current support | Observed failure |
|---|---|---|---|
| 36 Agency Producer | What is locked before money moves | Stage 8 preflight (brief, deck, deliverables, plan, cap) | Words and money locked; **proposition, product role, storyboard, voice not locked**; clips bought during voice rounds 2–4 (`09` §Q6) |
| 37 Production Designer | Assets, props, plates, visual systems | `plan.assets[]` with dependencies | Copy zone never planned into the plate ("footage has no room" for 4:5/1:1); MF's recipe reserved an empty caption zone in the prompt (`02` §6) |
| 38 Production Planner | Dependency graph; which decision first | Dependencies recorded | Voice (register-defining) qualified last; VO generated after every clip; timeline before VO (DF-05/08) |
| 39 Delivery / Format | Each geometry works independently | FORMAT_SPECIFIC_REVALIDATION (from 002) | It **flagged** 4:5/1:1 (state 8 reached) and the flagged files were presented three times — flags written, not read |
| 40 Human Review Coordinator | Maximum information per human minute | ACCEPT / SPECIFIC REPAIR / REJECT at release | 10 cycles in Cumin; only the 7th (V2) carried decisive information; 4 plate/clip gates confirmed things already fine; the decisive V2 verdict arrived after 99.8 % of spend |

## G. Model / routing

| Persona | Expectation | Current support | Observed failure |
|---|---|---|---|
| 41 Image-gen | Freeze packshot marks; micro-qualify | NB2 + refs micro-qualified (MQ1 r2) | Worked: DF-01 caught before review — the one end-to-end success of the eight-state chain (`03` §3) |
| 42 Video-gen | Mouths closed under VO; frame-sample | D1 human-eye frame pass; `frame_hygiene` NOT-RUN | Mouths moved (DF-03) ×2; r2 repair still cut in on an open mouth (jury §1.3); MF idle-plate prompt "Mouth stays closed" never ported |
| 43 Audio / TTS | Cast by ear on the longest line at final tempo before dependents | Candidate pattern | Sarvam 8 takes despite RO-05 (n=16) and MF P8; ElevenLabs 8 takes on an account with no Indian voice; Gemini TTS accepted with no cell, no roster row |
| 44 Multimodal | Cross-asset invariants | D3/D14 human rows | Two narrators (002), open-mouth-under-VO (003) — both foreseeable from prior notes |
| 45 Model-routing Engineer | Strongest evidence across both programmes | `runtime/route/evidence.py` reads TAINT-REGISTER only | `grep historical runtime/` = 0; 52/61 cells have no MF row; 0/24 route decisions cite MF; 0/3 verdict-deciding routes were Lab-backed (`08` §4–5) |
| 46 Provider Reliability | Liquidity read, fallback declared | `pools.py` (dry), A7 attestation | Balance machine-read once (fal, 003) — it changed the plan; ElevenLabs quota failed 45 min after human attestation; attempt-id collision worked around not fixed |

## H–K. Knowledge, evaluation, economics, adversarial — summarised (full argument in Parts 5, 7, 8, 11, 12)

| Persona | Expectation | Observed |
|---|---|---|
| 47 Canon Librarian | Did we already possess the knowledge? | Yes for structure/opening/CTA (ABCD, Ogilvy, StoryBrand, Hopkins at state 1); no for obstruction and voice register (K0) |
| 48 Retrieval Engineer | Why not selected? | Not a ranking failure: pack uncompiled by policy C-10; gate hard-codes two packs; skill §4 "proceed on the brief" |
| 49 RAG Architect | Chunking, ranking, depth | No retrieval exists on main; CANON-015 BM25 on an unmerged branch, dispositioned SUPERSEDE; EVAL-037 controlled lane 53 searches, 1 read |
| 50 Context-engine | What reaches the model at decision time | ≈ 62–82 k tokens of process/commercial text; craft = one 14-row table in the middle of a 14-stage document; 21 CHECK lines; DEFAULT text not on the read list |
| 51 Context-window | Dilution, lost-in-middle | Instructed floor 60–80 k tokens before the brief; PROFILE.md (22–25 k) is the largest block; JOB.yaml grows to 16 k tokens and is re-read |
| 52 Memory Systems | Episodic/semantic/procedural; triggers | Episodic keyed by CASE-ID, no defect-class index; procedural = prose + opt-in gates; no consolidation; OUTCOME-EVENT store does not exist |
| 53/54 Fine-tuning / SLM | Learned policy where judgment repeats | Nothing trained; Q&A unsuitable as knowledge-injection data; narrow checklist-judge is the precedented use |
| 55 Ontology | Traversable relationships | 0 of 422 relationships cross a source; 291 bindings all unreviewed, 249 without a target |
| 56 Q&A Specialist | Practitioner questions? | 12/20 reading comprehension, 2/20 practitioner checks; consumed by nothing |
| 57 Prompt Architect | Which form changes behaviour | Compiled = constraint + self-attested check; Q&A = worked negative example (`qa_abcd_0010` describes Cumin V2 almost verbatim) — the excluded form |
| 58–63 Evaluation / Learning | Distinguish failure classes | Taxonomy collapses K1–K7, K13–K15 into "pipeline_failure"; 3/42 rejection reasons map to a declared criterion; no experiment can separate the hypotheses |
| 64–68 Economics / Ops | Complexity lowers CpAO/TTAO? | Only spend caps, code-set text, micro-qualification, pool read, frame sampling show observed defect-class elimination; Registry, Canon injection, governance show none |
| 69–75 Adversarial | Simpler beats current? | Strong-baseline reconstructions produce the operator's blueprint plus the missing end card/early brand; would make the same execution errors (which need gates, not knowledge) |
| 76 / 77 Prosecutor / Defender | — | Part 12 |
