# PART 9 — REQUIREMENT MODEL BY MEDIA JOB CLASS

What an expert team supplies that a customer often omits. Built by the lead from: council 13B (agency brief practice, platform guidance, pipeline and TTS controls — Part 8 §G–J), council 03 (18 real marketplace briefs, Nadia's screened posts, the Upwork promise), councils 04/05/12 (what actually failed in three productions), council 02 §7 (Media Factory's intent-completion layer: Truth / Craft / Spec input classes), council 09 §Q5 (rules-vs-judgment classification). The wave-two requirement-model agent (council 16) was stopped before writing; this Part replaces it.

Conventions. Each field carries a class per the commission: **DET** = deterministic (code); **RSR** = retrieval-supported reasoning; **LJ** = learned judgment (operator craft today, possibly a trained judge later); **HJ** = human judgment; **EMC** = empirical model capability (only a draw tells). "MUST BE ASKED" means unsafe to decide without the customer; "SAFELY DECIDED" means an agency decides and shows, the customer vetoes. Platform-specific numbers are given as examples with their source and are **not** to be hard-coded (Part 8 §H). Labels: OBSERVED (from cited evidence), INFERENCE (synthesis), RECOMMENDATION.

---

## 0. What real buyers supply and omit (OBSERVED; council 03 §2)

Across the 18 marketplace cases (`canon/research/marketplace-demand-v1/derived/marketplace-brief-bank-v1.yaml @ 3bb9a3c`, computed): on-screen text absent in **18/18**; rejection criteria stated by 1/18; brand kit omitted 15/18; language omitted 16/18; delivery format omitted 9/18; acceptance basis stated by 2 ("$30–45 per approved video"). The authored 30-brief bank had exact text in 28/30 — the programme tested what buyers do not ask for. Buyers who pay well specify *method and fidelity* (image-to-video from a still; product never regenerated; text/logos in the edit; faces locked; a shot approach *before* generating; a paid test) and delivery geometry (9:16 + 1:1/4:5, re-captionable). Two of three well-written posts ask "which model" as a screening question. The three real MI briefs matched: Cumin supplied a story shape and a voice register and omitted proposition, product role, CTA, formats, spend, legal; the Upwork intro supplied a positioning paragraph and omitted face/no-face, brand spoken/shown, hosting; the Nivaas tile supplied a three-shot shape and omitted everything else.

INFERENCE: an incomplete request is one where a *decision* is missing, not a detail (Part 8 §G). The missing decisions are the same twelve every time: objective/clock, who, to-what, single proposition, proof, product role, distinctive assets, tone, mandatories, deliverables/formats, budget/timeline, approver.

---

## 1. Universal layer (applies to every class below; RECOMMENDATION unless cited)

**1.1 Intake — the twelve decisions and their class**

| Decision | Class | Ask / decide | Evidence it matters |
|---|---|---|---|
| Objective and clock (activation vs brand; what counts as success) | HJ | **ASK** — one question with a default offered | Binet & Field (Part 8 G4); no `objective` field exists in NR or JOB-TEMPLATE (council 06 §5) |
| Who (segment + current belief/behaviour) | RSR | decide from brand discovery; show | brand dossiers exist (`coordination/commercial/dossiers/`) |
| To-what (desired response) | HJ | **ASK** if unclear from objective | — |
| Single proposition | LJ → HJ veto | **decide and show** as one sentence before any spend | Cumin: "Ramen night at home" is a mood, not a reason (jury) |
| Proof / reason to believe | RSR | decide from product facts; never invent | Cumin `forbidden:` list (no health/PTFE/patent claims) |
| Product role (hero / enabler / incidental) | LJ → HJ veto | **decide and show**; default hero for any product ad | Cumin `product as prop`; MF receptionist forced `productVisual` |
| Distinctive assets that must appear (pack shape, logo, colour, sonic, character) | DET once listed | **ASK** for the list; then enforce | Ehrenberg-Bass 2026 (G5); embossed mark garbled (DF-01) |
| Tone / register with an example | HJ | **ASK** with 2–3 offered examples | Cumin "calm empathetic" asked for, "bubbly" delivered (jury C10) |
| Mandatories (legal, offer terms, logo, disclosure) | DET | **ASK** once; then byte-frozen | exact-text mechanism already works (0 exact-text defects in 3 cases) |
| Deliverables / formats / durations | DET | decide from channel; confirm | 9:16 crops to 4:5/1:1 failed in 002 and 003 |
| Budget / timeline / spend cap | HJ | **ASK** (already done) | the one mechanism that held in all three cases |
| Approver and acceptance basis | HJ | **ASK**: who accepts, on what (3–6 statements) | 3/42 rejection reasons mapped to a pre-declared criterion (council 10 §4.3) |

**1.2 Pause points (the human-in-the-loop model; estimates are INFERENCE from the three cases)**

| # | Review point | Information gain | Review cost | Cost if skipped | Dependent spend | Verdict |
|---|---|---|---|---|---|---|
| P1 | **Brief-complete + proposition + product role + CTA** (one page; the twelve decisions with defaults filled) | very high — every Cumin structural rejection lived here | 3–5 min | whole job (Cumin V2: USD 5.08 of 5.09 spent before this was challenged) | 100 % | **unconditional human** (no confidence estimator exists for concept correctness — Part 8 J10) |
| P2 | **Six-frame board + scratch/measured VO** (from accepted plates; timeline derived from VO durations) | high — 8 of 12 Cumin defects visible here (Part 6 §3.5) | 5 min | rebuilds (001: USD 8.08 in discarded lineages) | 70–90 % | **human**, replaces plate-by-plate approvals |
| P3 | Voice cast by ear on the longest line at final pace, 2–3 candidates | high for VO jobs — the register | 3 min | 5 rounds / 26 takes (Cumin); V3 reject (001) | all clips if VO-first ordering is kept | **human** today; must precede plates; LJ later with a naturalness judge |
| P4 | First hero plate / first product plate against the reference | medium — fidelity | 2 min | dependent clips inherit the plate | clips | human today (B2 side-by-side); DET later if a drift measure exists |
| P5 | Assembly (rough cut) | medium — mostly deterministic defects now | 5 min | — | 0 | gates first; human only on flags |
| P6 | Release | required (C-8) | 2–5 min | reputational | 0 | human |

Drop from the human's plate: individual plate r1/r2 choices, individual clip accepts, pool attestation (read the balance), take-level casting across three providers, reading QA flags (a flagged file is not a candidate — DET).

**1.3 Universal production requirements (RECOMMENDATION, each with its class)**

- Hook in the first 2–6 s; brand or product recognisable early *in context* (Part 8 H1, H5) — LJ, checked by a binary question at P1/P2.
- Explicit close: product + name + direction, via card and/or VO — LJ at P1; DET that the card exists and strings match.
- On-screen copy composited, never generated; strings byte-frozen; bounds/contrast/disjoint/obstruction gated — DET (exists for bounds/contrast/disjoint; obstruction needs a subject box).
- Identity references supplied to every shot (≤ 3–4 per Veo/Kling; character bank + **product bank**, which no published pipeline takes as input) — DET (presence) + EMC (holds or not).
- VO recorded and measured before shot durations are fixed; two lines never overlap; last line ends before the film — DET (`check_vo_schedule` exists, 0 callers).
- Loudness and true-peak declared per target (e.g. EBU R128 s1 −23 LUFS / −18 short-term / −1 dBTP for broadcast; social has no standard — declare a house default) — DET.
- Each delivered geometry composed for itself or verified against the platform's own template; a CF-flagged file is not a deliverable — DET.
- Mouths closed on any face under a VO unless it speaks — LJ prompt clause + frame check; EMC.
- Enhancement state (Meta Advantage+) declared at delivery — DET.

---

## 2. Per-class requirements

Each table: SUPPLIES / FORGETS / MUST ASK / SAFELY DECIDED / KNOWLEDGE / CREATIVE DECISIONS / PRODUCTION DECISIONS / FAILURE PATTERNS / HUMAN-APPROVED TODAY / MAY BE AUTOMATED. Evidence sources in brackets.

### 2.1 Static performance ad (Meta/IG feed static; the Upwork Static Starter/Standard)

| Field | Content |
|---|---|
| Supplies | product photo or link; offer or price; sometimes a headline; brand name (OBSERVED: FAMAG post supplied lines verbatim; marketplace 18/18 no exact text otherwise) |
| Forgets | legal line / T&Cs; which sizes; brand colours and font; CTA verb; landing URL; what a rejected file looks like |
| Must ask | offer terms and legal line (mandatories, DET once given); logo file; approver; language(s) |
| Safely decided | headline (3–7 words, benefit-led — MF receptionist did this; RSR/LJ); CTA verb (specific: "Shop now" vs "Learn more" by objective — H1); layout system (photo top / panel bottom held in 002); sizes from channel; hierarchy 1st/2nd/3rd read (CA-D1/D2) |
| Knowledge required | offer-ad conventions (prices/codes appear on a third to all competitor creatives — council 03 §1); WCAG 4.5:1 / 3:1 large; platform pixel specs; text-to-image policies; category legal norms (RSR) |
| Creative decisions | proposition; hero framing; hook line; one boss element (offer vs headline); colour of ink against the photo band (LJ) |
| Production decisions | mechanism B (code-set text on a textless plate — RR-1) vs native text (RR-2 allowed for NB2/GPT Image 2); plate per size vs one master; contain vs cover for product proof (DET, declared) |
| Common failures | text over the subject (002 HD-03/05/07); banner over photo (HD-08/09/10); contrast lost (HD-04); clipping at panel edge (HD-01/02); destructive crop (HD-06/11); Hindi headline shrunk below the pill (HD-12); offer/code collision (001 SD-07) |
| Human-approved today | strings and offer (P1); first plate against the product photo (P4); release |
| May be automated | everything in "common failures" is single-frame and deterministic given a subject box; variant composition already is; product-fidelity drift needs a measure (currently a human side-by-side, council 03 §3) |

### 2.2 Product hero / product-in-scene (customer photo placed in a new scene)

| Field | Content |
|---|---|
| Supplies | one or more product photos; the scene idea ("kitchen", "festive"); sometimes a competitor reference |
| Forgets | which surfaces/marks must survive (embossing, label text, cap colour); proportions; whether the product may be re-lit; multiple angles |
| Must ask | distinctive assets that must be exact (label words, logo, moulded marks) — the decision-7 gate in `UP/PROFILE.md` (5 % proportions, hue family, label words); whether a clean cut-out composite fallback is acceptable |
| Safely decided | scene, light direction and finish vocabulary (PA-D1/D4 held in Cumin); camera height; copy zone reserved in the plate (MF `campaign.ts` did this; Cumin lacked it); one window source |
| Knowledge required | packshot lighting (LSM: background carries the extreme, `qa_lsmx_0039`); reference-conditioning limits per model (Seedream edit held identity 10/12 vs NB-pro edit 3/12; NB2 inline refs 5/6 with one garbled mark) — RSR + EMC |
| Creative decisions | hero vs in-use; whether hands appear (hands are the highest-risk generative element — Part 8 J5); scale of product in frame (PA-D7 "size by importance to the sale") |
| Production decisions | edit route (Seedream 5 Pro edit clean 4/4 IMG-REF) vs generate-with-references; mark turned away vs masked; per-geometry plates; fidelity check method |
| Common failures | embossed/moulded mark garbled ("cumin ca.", DF-01); extra objects; size/colour drift (2/4 on supplied packs — PLAN §1); product regenerated when the buyer said never regenerate |
| Human-approved today | fidelity side-by-side on the first plate (P4); scene choice at P1 |
| May be automated | drift measurement (proportions / hue) — declared deterministic-eligible in the Lab (`packaging_brand_colour_fidelity`, 0 rows); one-draw-then-judge policy |

**OBSERVED gap:** no production has ever placed a *customer's* photo; all tile packshots were GPT Image 2 generations (council 03 §3).

### 2.3 Offer ad (price / code / date-bound)

| Field | Content |
|---|---|
| Supplies | the offer, often verbatim; dates; sometimes a code |
| Forgets | T&Cs and exclusions; urgency framing; what happens after the date; whether the price is struck-through vs new |
| Must ask | exact offer terms and legal (DET once given); market-specific disclaimer conventions (RSR, not universal) |
| Safely decided | urgency device (ABCD "Inspire"); CTA verb; one boss element; pill/button hierarchy |
| Knowledge required | direct-response structure (Hopkins: picture shows the result; CTA assumes compliance — `qa_sa8_0048`); category legal norms |
| Creative decisions | offer as hero vs product as hero; reason-to-believe line |
| Production decisions | code-set text; per-size composition; variant matrix (offer × hook) |
| Common failures | offer/code collision (001 V4); "no offer, no button" (Kora, Brewa rejected as ads by the owner's own five-question rubric); expiry not updated across variants |
| Human-approved today | offer string and legal (P1); release |
| May be automated | variant generation and diff (variants differ only in ratio/duration/CTA/legal/language → QA is a variant-diff, not a re-review) |

### 2.4 UGC / spokesperson / presenter

| Field | Content |
|---|---|
| Supplies | script or talking points; "a person speaking to camera"; sometimes a reference creator video |
| Forgets | disclosure (AI presenter); age/tone/accent of the person; whether the brand is *spoken*; lo-fi vs polished register; how long the presenter is on screen |
| Must ask | disclosure line; face or no face (conflicted with the live "not on the menu" line in 001); brand spoken or shown; register (TikTok lo-fi vs YouTube polished — platform-specific) |
| Safely decided | presenter ≤ ~20 s of a 60-s piece, bookends (001 verdict "presenter blocks too long"); one anchored still, no extend chains (RO-02); supers word-identical to speech |
| Knowledge required | on-screen person mentioning the brand beats VO for recall (ABCD H1); creators win attention but halve brand ID unless early branding is engineered (System1 H5); casting brief before audition (Ricketts I10) |
| Creative decisions | who the presenter is; what they say first; where proof interrupts them |
| Production decisions | native speech route (no Registry cell for single-speaker English from an anchored still — 001 SD-08) → micro-qualify one take; identity references per take; transcript verbatim check |
| Common failures | presenter drift across extends (001 RO-02); synthetic timbre (Omni, RO-03); inserted/changed words; bared-teeth frames; 8.5 s with no super for muted viewers (jury on V4.1) |
| Human-approved today | speaker take by ear + transcript (P3); script (P1) |
| May be automated | transcript verbatim (DET, exists); word-insertion detection (DET); naturalness — LJ only after a judge is qualified (κ 0.33 today) |

### 2.5 Tutorial / demonstration (the Cumin class)

| Field | Content |
|---|---|
| Supplies | the how-to content (blog steps); a story shape ("step 1, 2, 3; he fails; they eat"); a voice register |
| Forgets | **that it must still be an ad**: proposition, product role, CTA, end card, brand-early; which product is the hero; number of steps that fit the duration; the payoff shot |
| Must ask | which product is the hero (Cumin: bowl vs chopsticks); may the embossed mark appear; on-camera speech vs VO; ending (asked: spoon vs fist) |
| Safely decided | compress steps to what fits (5 → 3 was right); one narrator; supers ≤ 5 words per step; product fills the lower half of every macro; the *miss* is staged as the event |
| Knowledge required | consideration-objective ABCD (show function); hands + product interaction are the highest-risk generative elements — require reference stills of the action; "reduce how much the hands are asked to do" (Part 8 J5); demonstration ≠ ad (`qa_abcd_0010`) |
| Creative decisions | the product argument the demo proves (rim notch — named in the blueprint, in no frame); the event (fumble) and where it lands; payoff |
| Production decisions | i2v from accepted plates that already show the action; clip in-points chosen for the event, not by excluding defects; VO first, timeline from VO |
| Common failures | tutorial-not-ad (DF-07); no hook event (C1); forbidden etiquette rendered (sticks vertical); clean lift where a miss was scripted; open mouth under VO; 5.5 s dead macro; product argument not in frame (C3) |
| Human-approved today | proposition + product role + CTA + end card at P1; six-frame board at P2; voice at P3 |
| May be automated | none of the structural decisions; the board build from accepted plates (DET assembly); VO schedule (DET) |

### 2.6 Explainer (service / feature explanation, VO-led; the Upwork intro class)

| Field | Content |
|---|---|
| Supplies | positioning paragraph; list of things to show; duration band |
| Forgets | proof order; which proofs get full frame; what a muted viewer reads; hosting/aspect; brand shown or spoken |
| Must ask | hosting and aspect (16:9 YouTube vs 9:16); brand name spoken/shown; whether the film's own examples may be generated |
| Safely decided | script lock → VO → timing to track; every proof ≥ 3 s full-frame (001 "important still ≥ 3.3 s" template); supers composited; end card with the offer |
| Knowledge required | pacing/hold doctrine (Murch/GoS in Canon); ABCD consideration; duration norms by placement (Shorts ≤ 60 s) |
| Creative decisions | movement structure (001 V4 four movements); the one memorable sentence ("and it can't suck"); what interrupts the presenter |
| Production decisions | VO route qualified on the longest line at final pace (001 V3 failed this); one voice source; card geometry tokens (001 V4 fix) |
| Common failures | proof too small / phone mock-ups (001 V1/V2); robotic long-form TTS (V3); text clipping/contrast/crops/mixed radii (V3); pacing rushed; thumbnail grids unreadable |
| Human-approved today | script (P1); VO take (P3); assembly |
| May be automated | all V3 compositor defects (DET, now gates); pacing arithmetic (beats < 2 s) |

### 2.7 Product story (short narrative around a product; the Nivaas class)

| Field | Content |
|---|---|
| Supplies | three-shot shape; a mood; sometimes a script |
| Forgets | continuity across shots (same people, same place, same voice); end card; who narrates |
| Must ask | narrator language; offer/price line if any; the one product argument |
| Safely decided | stills first → i2v per shot without native speech; one TTS narrator generated once and split across the cut (MF `assemble.py`; 002 candidate SINGLE_VOICE_SOURCE); end card by code |
| Knowledge required | emerging story arc with brand cues throughout (ABCD); entity registry with consistency groupings (VideoDirectorGPT/MovieAgent — J1); chaining decay law (MF P10; RO-02) |
| Creative decisions | the arc in three beats; where the product enters |
| Production decisions | never extend-chain; ≤ 3–4 references per shot; VO measured before cut |
| Common failures | two narrator identities (002 HD-13b); narration hole inside a sentence (HD-13a); soft 720p architecture; extend restructures narration (RO-01) |
| Human-approved today | board (P2); narrator (P3) |
| May be automated | narration hole detection (`silencedetect`, DET); cross-clip voice identity — LJ/EMC (ear-only today) |

### 2.8 Multi-shot commercial (18–60 s, several scenes, VO and/or dialogue; the C-7-excluded class sold as "quoted")

| Field | Content |
|---|---|
| Supplies | a concept or script; duration; sometimes references |
| Forgets | everything in §1.1 plus: dialogue vs VO; number of characters; language mix; music; safe zones per platform |
| Must ask | dialogue (≤ 2 turns per clip is the only proven form — VID-2SPK 6/6; >2 turns untested); language; music licence expectations; approver per stage (AICP: script and storyboard are contractual inputs) |
| Safely decided | shot list with entity registry; character and product banks; VO-first timeline; music ducked; loudness target |
| Knowledge required | J1 pipeline order; ABCD full-funnel; chaining ban; loudness norms (I7–I9) |
| Creative decisions | arc; hero moment; casting; where brand cues sit in each shot |
| Production decisions | per-shot route by capability + price + reliability; micro-qualify the riskiest shot first; picture lock before sound |
| Common failures | all Cumin failures; voice drift across clips; extend decay; 42 % over planned duration |
| Human-approved today | P1, P2, P3 in order; rough cut |
| May be automated | schedule/overlap/loudness/duration/safe-zone gates (DET); shot-consistency checks (EMC + LJ) |

### 2.9 Social Reel (9:16-first short piece with feed derivatives)

| Field | Content |
|---|---|
| Supplies | 9:16 intent; sometimes a trend/sound reference |
| Forgets | that 4:5 and 1:1 need their own composition; UI-occluded bands; captions for muted play; re-captionable version |
| Must ask | target platform(s) (safe zones differ and change: Meta 14/35/6 % for 9:16, TikTok template, YouTube PNG — H2, H4, H8); whether captions are burned in |
| Safely decided | critical content in the centre band; brand mark in every geometry; per-geometry plates or verified re-frame |
| Knowledge required | platform safe-zone templates (fetch current, do not hard-code); muted-first design (H7); TikTok "subtle brand in the hook" vs Meta "brand in 3 s" |
| Creative decisions | hook in 1–2 s; sound-on vs sound-off design |
| Production decisions | 9:16 master + separate feed compositions (not crops — SD-09); safe-zone overlay on the board |
| Common failures | 4:5/1:1 cards over the subject and no brand mark (Cumin V1–V3, flagged and shipped); text in the bottom 35 % band |
| Human-approved today | board with safe-zone overlay (P2) |
| May be automated | safe-zone compliance per platform template (DET); per-geometry re-validation (exists as CF rows; must be code with a "flagged ≠ deliverable" rule) |

### 2.10 Hindi / Indian-language ad

| Field | Content |
|---|---|
| Supplies | "Hindi" or "Hinglish" as a word; sometimes the English copy |
| Forgets | script vs transliteration; register (formal/colloquial); who the voice is; that Veo audio is "not evaluated" for non-English (J2); numbers/dates pronunciation; Devanagari typography rules |
| Must ask | language and script per surface (VO vs supers); register with an example; native-reader approval (a human gate, not automatable today) |
| Safely decided | text composited never generated (Devanagari fabricated by video models; textless plate + overlay proven — RR-1, 002 tiles, Aight gallery); TTS by *audition* between ElevenLabs v3 and Sarvam Bulbul V3 (no Pareto winner — J7); emotion written into the script for Bulbul (no tags); Gemini TTS Hindi at GA as a third candidate |
| Knowledge required | Indian-context sources in Canon (Bijapurkar, Pandey, Parameswaran, Jain, Desai — the one content a frontier prior plausibly lacks, value UNKNOWN); retroflex/number checks (PSP benchmark) |
| Creative decisions | Hinglish mix; cultural cue; festival context |
| Production decisions | voice route by ear on the longest line; shaping check on every Devanagari render (correct in every 002 file zoomed — jury) |
| Common failures | ElevenLabs premade voices Western-accented (rejected by ear in MF and 003); Sarvam robotic on long reads; Hindi headline shrunk (HD-12); Hindi CTA button absent on one tile |
| Human-approved today | voice by ear (P3); native-reader copy check (P1) |
| May be automated | shaping/glyph check (DET); pronunciation of numbers (EMC + transcript check) |

### 2.11 Poster / banner (print or large-format static)

| Field | Content |
|---|---|
| Supplies | event/offer facts; a photo; a size |
| Forgets | bleed and safe margins; viewing distance (type size); print colour; hierarchy at a glance |
| Must ask | final size and medium; bleed; brand kit |
| Safely decided | type scale from viewing distance; one boss element; grid |
| Knowledge required | Samara/Vignelli/Albers in Canon (grid, hierarchy, colour interaction); WCAG as a floor; print bleed conventions (not universal) |
| Creative decisions | the one image; the one line |
| Production decisions | native text allowed on NB2/GPT Image 2 (RR-2) vs composite; resolution |
| Common failures | same as 2.1 plus resolution/bleed |
| Human-approved today | P1; first composite |
| May be automated | bounds/contrast/margins (DET) |

### 2.12 Campaign variant pack (one approved concept → N hooks × sizes × languages × offers)

| Field | Content |
|---|---|
| Supplies | "give me variants"; sometimes the dimensions of variation |
| Forgets | what is *fixed* (the approved master) vs *varies*; naming; that each variant is a separate deliverable with its own QA; enhancement opt-outs |
| Must ask | the variation matrix (hooks / colours / offers / languages / sizes); naming convention; where they run (enhancement state) |
| Safely decided | one approved master; variants differ only in ratio/duration/CTA/legal/language; QA = variant-diff against the master |
| Knowledge required | ABCD/Meta placement specs; the "unlimited variants" promise (`PROFILE.md` l.79) is the compositor's genuine strength (002 RO-06) |
| Creative decisions | which hooks; which one leads |
| Production decisions | deterministic composition; provenance per asset (DESIGN_REUSE_PROVENANCE) |
| Common failures | a rejected design reused as a variant (002 REJECTED_DESIGN_REUSE); expiry/legal not updated; "six hooks" = six headlines on one photo (jury: range not demonstrated) |
| Human-approved today | the master; the matrix |
| May be automated | everything downstream of the master (already is at USD 0 per variant) |

---

## 3. Classification of requirements (rules vs judgment; council 09 §Q5 extended)

| Class | Requirements | Status in MI today |
|---|---|---|
| **DETERMINISTIC** | text bounds, contrast, disjointness, fit/crop declaration, geometry tokens; VO overlap/overrun; duration vs plan; loudness/true-peak; narration holes; safe-zone per template; per-geometry re-validation with "flagged ≠ deliverable"; exact-string byte check; identity references present; provider balance read (all four pools); attempt-id lock; sha integrity; variant-diff; enhancement state declared; subject obstruction **given a subject box** | exist as library code for 6 (no callers on any mandatory path); VO schedule on PR #103 (0 callers); obstruction and balance-read for 3 pools do not exist; loudness measurable, no module |
| **RETRIEVAL-SUPPORTED REASONING** | ad structure by objective (ABCD, Ogilvy, Hopkins, StoryBrand); category legal norms; packshot lighting; Indian-context cues; route choice for long narration (prior + observation); platform-specific placement rules (fetched, not hard-coded) | exists in Canon (uncompiled for advertising), in MF priors (unread), in cases (prose) |
| **LEARNED JUDGMENT** (operator craft now; trainable narrow judges later) | VO-first timeline; closed-mouth prompt clause; geometry needs its own plates; hierarchy survives fit; hook chosen for the event; "is this a tutorial or an ad?" classifier; voice naturalness (after a qualified judge exists) | prose candidates; no judge qualified (vision judge κ 0.33; no audio judge) |
| **HUMAN JUDGMENT** | proposition; product role; "does it feel like an ad"; "competent, not extraordinary"; voice register by ear; opening strength; narrator identity across clips (ear); plate acceptance on sight; creative range; native-reader Hindi check; release | all present today, but taken at the wrong altitude (strings, plates, takes, full films) |
| **EMPIRICAL MODEL CAPABILITY** | embossed marks from references; mouths under VO; hands/chopsticks; extend chains; native narration identity; Gemini TTS refusals; Veo non-English audio; Sarvam long-read cadence | recorded as `routing_authority: none` observations; the Registry measures none of them (31/36 capabilities 0 rows) |

Do not convert to gates: "does it feel like an ad", "is the product meaningfully central", "is this voice emotionally right", "is the opening strong", "does the story work". Convert them instead into **binary questions answered by a non-author at P1/P2** (Part 8 §F), with the answers, not the judgment, recorded.

---

## 4. What must be asked vs decided — the two lists an operator should carry (RECOMMENDATION)

**Always ask (unsafe to decide):** objective/clock and success basis; the hero product and its exact-fidelity assets; mandatories (offer terms, legal, disclosure); tone with an example; language/script per surface; deliverables/platforms; spend cap; approver and 3–6 acceptance statements; for presenters: face/no-face, brand spoken; for Hindi: native-reader approval.

**Decide and show (customer vetoes):** proposition in one sentence; product role; hook event; structure (open / body / close with product + direction); copy lines; voice casting shortlist (2–3 by ear); shot list and references; per-geometry composition; music/loudness; route per asset by capability + price + reliability + liquidity; micro-qualification order (riskiest first, voice before plates for VO jobs).

**Never ask (derive):** ratios, character limits, safe zones, captions/mute, variant naming, file specs, enhancement state.

This is Media Factory's Truth / Craft / Spec split (council 02 §7), which MI did not port and re-derived as `AD_STRUCTURE_MINIMUM` after paying for the lesson.

---

## 5. Not universal — do not hard-code (OBSERVED from Part 8 §H)

"Brand in 3 s" (Meta) vs "5 s" (YouTube) vs "subtle in the hook" (TikTok); any safe-zone pixel value; social loudness targets; "UGC outperforms"; a single "best" TTS; ~60:40 brand/activation split (category-dependent); Hopkins/Ogilvy print-era rules carrying `MEDIUM-UNTESTED` markers (PA-D7's 1926 citation) as video defaults; Indian-market early-branding effects (no India-specific evidence found — UNKNOWN).
