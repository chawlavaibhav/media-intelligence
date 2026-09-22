# Agent 3 — Customer / Commercial Council

Read-only audit, 2026-09-16. Personas embodied: Founder/Brand Owner, CMO, Performance Marketer, Media Buyer, DTC Growth Lead, Agency Account Director, Skeptical Agency Owner.

Repos read (HEADs verified): MI `3bb9a3c` (main), PR #103 branch `1de2b37`, Cumin job branch `de1f978` (evidence commit; branch head `1aea4d2` = one sync commit that only fills `sync.*`), UP `ff06dab`, UPT `f236c54`, UPM (non-git, mtime 15 Sep 2026). Every label below is OBSERVED / INFERENCE / HYPOTHESIS / UNKNOWN as the preamble requires. Counts marked "computed" were produced by the commands shown.

---

## 0. Evidence base actually opened

| Source | Files read | Notes |
|---|---|---|
| UP @ ff06dab | README, PROFILE.md (667 lines, whole), BENCHMARKS.md (whole), LOG.md (state of record + grep'd entries), ACCOUNTABILITY.md, CONNECTS.md §(d), context/PLAN-2026-09-09.md §1, §7, context/UPWORK-RESEARCH-NOTES.md, research/2026-09-14-intro-video-script.md, research/2026-09-14-portfolio-benchmark.md, research/2026-09-15-project-pricing-benchmark.md, research/2026-09-15-first-proposals-plan.md, all 8 files in proposals/ | LOG.md is 140 KB; read by grep + state-of-record head |
| UPT @ f236c54 | MANIFEST.json (files + sha256 + sources), UPLOAD-LIST.md, all nine TILE.md | |
| UPM (non-git) | README.md, full tree incl. `_rejected/` | |
| MI production-learning | UPWORK-INTRO-001 (all 10 files), UPWORK-PORTFOLIO-002 (all 9 files), CUMINCO-CHOPSTICKS-003 @ 1de2b37 (README, HUMAN-VERDICTS, TIME-AND-COST, SYSTEM-DEFECTS, PROMOTION-QUEUE) | |
| Cumin job @ de1f978 | JOB.yaml (whole), brief.job.json, LEARNING-PACKET.yaml, DELIVERY-NOTE.md, LEDGER.jsonl (101 rows), ATTEMPTS.jsonl (51 rows) | |
| MI coordination/commercial | README, PROSPECT-PIPELINE.md, dossiers/cumin-co.md | |
| MI canon/research | marketplace-demand-v1 README, sources/upwork-ai-video-demand-2026-08-26.md (whole, 114-row appendix), derived/COVERAGE-REPORT.md, derived/marketplace-brief-bank-v1.yaml (18 cases; customer_brief + R08 + R16 extracted by script); request-space-v1 SOURCE-LANDSCAPE, CURRENT-30-BANK-COVERAGE-AUDIT, CREATIVE-IR-AND-CANON-GAPS (head) | |
| MI runtime / skills | .claude/skills/media-agency/{SKILL,QA-CHECKLIST,PRODUCTION-WORKFLOW}.md, runtime/ALPHA-1.md (grep), runtime/contracts/DELIVERABLE-KINDS.yaml, runtime/compositor/gates.py (function list), runtime/contracts/PRODUCTION-JOB-v1.yaml (deadline field) | |
| Local non-git dirs | rentok-ad (ad_script.json, assets/brief.md, listing), voice-workshop-agent (README, SPEC), aight-website (assets/gallery README + manifest, gallery-plan head) | see §8 |

---

## 1. What exactly is being SOLD on Upwork today

All quotes are `PROFILE.md @ ff06dab` unless stated. The "live" values were read back off the profile by Nadia (OBSERVED by her, chat/browser evidence; I can only verify the repo text).

**Title (live since 14 Sep 14:24 IST), l.66:**
> `AI Meta Ad Creatives in 24h | Statics + Video Ads | 4-Hour Express`

**Overview, live block l.70–101.** The operative promises, verbatim:

- l.71: "Meta and Instagram ad creatives within 24 hours, standard on every package: static ads with your exact offer, price and legal line, plus 10-15 second vertical video ads. Need them today? Express brings the smaller packs back in 4 hours."
- l.76: "• Your product photo placed in a new scene (kitchen, gym, festive, outdoor), no photoshoot"
- l.77: "• 10-15 s video ads: your offer as animated text in motion, or a three-shot product story clip, with English, Hindi or Indian-English voice-over"
- l.78: "• Text rendered exactly as you send it, every time: prices, dates, codes, T&Cs and brand names, in English or Hindi"
- l.79: "• Unlimited variants of an approved concept for A/B testing: hooks, colours, offers"
- l.82 (the clock): "The clock starts when I have your product photo, logo, brand colours and final offer text, and you have approved the words. Express covers the one- and two-concept static packs and the single video clip, ordered 09:00-19:00 India time, Monday to Saturday … Product-in-new-scene images and the larger packs take up to 24 hours from the same starting point. If I miss an express slot, the express fee comes back to you."
- l.85–87 (process): "1. You send the brief. I write the headline, offer line and CTA per language and you approve the words before anything is generated. 2. I generate, lay out and check every file: exact text, brand colours, no stray lettering, correct export specs. 3. Files land inside the window. Revisions come back within 24 hours, same day on express orders."
- l.89: "AI-generated, human-directed, custom per order. Every image is made fresh for you and never reused for another buyer. The delivery note lists the models used and the usage rights you get."
- l.91 (quoted tier): "Quoted per project, on top of the standard packages: presenter videos, where a clearly disclosed AI presenter reads your script to camera and stays the same person across a 35-40 second piece; two-speaker dialogue clips in Hindi or English, 8-10 second scenes with your product in frame, which can be chained into a longer piece; and 30-60 second films assembled from these parts, with music. These are scoped and priced from your script and typically take 2 to 4 working days, agreed per project."
- l.93–95: "Formats: 1080x1080, 1080x1350, 1080x1920, WhatsApp 800x800 and 9:16 MP4. Languages: English, Hindi, Indian English (text and voice-over). Revisions: two rounds on every package, more at a flat per-round price."

**Explicit exclusions.** OBSERVED: none remain on the live overview. l.70 header: "Nothing is listed as 'not offered' any more." (The 07:38 IST 15 Sep version still said "Not offered: the same character carried across several clips, and 30-60 second commercials"; replaced at 07:48 IST — LOG.md l.558–571.) The only exclusion that survives is inside the 4-hour scope table l.103–112: express covers "Static Starter … Static Standard … Video Starter (1 clip). Nothing else."

**Catalog, approved and public 15 Sep (l.247–273, "Catalog as entered"; confirmed public in LOG.md l.327):**

| Project | Tiers | Delivery field | Express add-on | Revisions |
|---|---|---|---|---|
| A. "AI Meta ad creatives with your exact offer text in 4 sizes, within 24 hours" | $60 (1 concept × 4 sizes) / $120 (2 concepts + 1 product-scene) / $220 (4 concepts + 2 scenes + Hindi) | 1 / 1 / 1 day | +$30 "4-hour express (Starter and Standard)" | 2/2/3 |
| B. "a 10-15s AI video ad for Reels & Meta, exact text + voice-over, in 24 hours" | $75 / $180 / $350 | 1 / 1 / 1 day | +$40 "4-hour express (single clip, Starter)" | 2/2/3 |
| C. "a month of AI ad creatives, statics + video, every request within 24 hours" | $900 / $1,600 / $2,800 | 30 days | +$30 per static pack request, +$40 per clip request | 2/2/3 per piece |

OBSERVED (l.205): Upwork's catalog delivery field is whole days, so "4 hours" cannot be entered; it lives only in the add-on name and description line 1. INFERENCE: the platform never enforces the 4-hour promise; only the refund line does.

**Quoted tier prices: PROPOSED, not live** (l.275–286): presenter $150; two-speaker $90/scene; 30 s piece $250; 30-60 s film $300. Decision 15 (l.39): "Stay 'quoted', no public 'from $X' yet".

**Product-in-scene claim, decision 7 (l.25 and l.586–603).** "The pipeline's own numbers are 10/12 overall but 2/4 on clean edits of a supplied product pack, and the two failures were size and colour drift. Vaibhav decided to keep the claim. That makes the drift check a hard gate … Any FAIL means regenerate, never ship-and-apologise." Checks 1–3 are side-by-side human comparisons (proportions within ~5 %, hue family, label words). Fallback: "If a product pack fails checks 1-3 twice in a row, tell the customer before the deadline and deliver a clean cut-out composite … If this happens on more than one order in five, tell Nadia and the claim moves from the overview to a paid add-on."

**Quality bar implied by the benchmarks.** `research/2026-09-14-portfolio-benchmark.md @ ff06dab`:
- l.123: "Grids beat single ads. Yes, without exception. Every tile opened shows 6 to 12 ads per board and several boards per tile."
- l.125: "Prices and offers on the creatives. Yes, everywhere: $10, $250 with a struck-through $312 … Exact offer text is the mainstream expectation of a Meta ad creative, not a niche."
- l.127: "A typical benchmark ad has a 3-8 word caps headline, a sub-line, three to five benefit bullets or a review quote with stars, an offer badge, a CTA button and a small logo: 20-40 words. The text is the ad."
- l.129: "Numbers are optional; reviews are the currency."
BENCHMARKS.md l.76 synthesis: earners sell "small fixed-price packages many times over … name a turnaround (72 hours is the norm, 24-48 hours is Egor's edge)". Pricing benchmark (`research/2026-09-15-project-pricing-benchmark.md` l.49, l.99, l.124): presenter median $45, top $150; 30 s ads median $40, top $80; 30-60 s commercials median $62, top $300 (Denis G., 5-7 days); l.128: "not one listing on either page sells a two-person dialogue scene … nobody sells Hindi AI speech as a named product".

**Commercial accountability frame.** ACCOUNTABILITY.md l.7–8: floor "minimum USD 250 net revenue per month" after Connects + Claude Max USD 200 + pipeline cost; month-1 target USD 1,000 in orders; l.13 kill test day 30: "1 order, or 2 interviews with a live negotiation". State of record LOG.md l.5: **proposals sent 2, viewed 0** (16 Sep 11:30 IST). Proposals drafted: 5 (3 in `proposals/2026-09-15-afternoon.md`, 1 in `-afternoon-chrome.md`, 1 in `2026-09-16-morning-chrome.md`; computed by reading each file). Connects 125 of 150.

INFERENCE on what is *actually* being sold: the title sells speed; the body sells exact text, product-in-scene, 10-15 s clips with VO, Hindi; the quoted paragraph sells everything the lab has ever accepted (presenter, two-speaker, films). Nothing on the profile is priced or timed against a delivered customer order — zero orders exist.

---

## 2. What a buyer on this marketplace actually asks for

### 2a. The 18 marketplace cases (`canon/research/marketplace-demand-v1/derived/marketplace-brief-bank-v1.yaml @ 3bb9a3c`)

Computed (python regex over the yaml): 18 cases; **R08 text requirements `absent` in 18 of 18** (the bank's own MKT-001 rationale l.267–269: "the authored 30-brief bank puts an exact-text requirement in 28 of 30 briefs, and this real, fully specified commercial job has none"). COVERAGE-REPORT.md l.14–24: "one of eighteen real, paid commercial jobs asks for exact text in the picture … Real buyers almost never say what would make them reject the work: one of eighteen states a rejection criterion". l.187–215: only 2 of 18 buyers state a spoken language (both Indic, both not runnable); "R18 acceptance intent: customer_stated in all 18"; acceptance basis stated outright by 2 (Knox Deco "$30–45 per approved video", the university "$20 per video").

Per-case R16 (computed): customer-omitted fields always include R03 (mutation intents), R07 (relationships), R08 (text), R13/R14 (subject/camera motion); R09 brand kit omitted in 15 of 18; R10 language omitted in 16 of 18; R15 delivery format omitted in 9 of 18.

Source sweep (`sources/upwork-ai-video-demand-2026-08-26.md`): 114 postings, 67 addressable; fixed-price under $100 = 53 %; "character or product consistency across a series is the single thing that flips an AI-video job from productized to custom" (l.104); "0 (zero) explicitly forbid AI" (l.151); Hindi "voice-over, dubbing, translation and data annotation — the inputs to Indic media, not Indic ad production" (l.247); UW-107 (the one Hindi/Hinglish creative buyer, $500) buys a script, not a video.

### 2b. Nadia's screened job posts (Sept 15–16, Chrome reads, OBSERVED by her)

`proposals/2026-09-15-afternoon.md` l.11–19: 20 listings, 5 opened, 3 pass. `proposals/2026-09-16-morning-chrome.md`: 32 listings, 2 opened, 1 pass. Two on-demand reviews, both SKIP. BENCHMARKS.md l.118 reads the feed as a benchmark: "The three well-written briefs of the day … all ask for the same four things in their own words: image-to-video from a still, not text prompts; the product kept accurate (never regenerated) and text kept clean or added in the edit; a shot approach or concept before generating; and finished cuts in 9:16 plus 1:1 or 4:5 with a re-captionable version. Two of the three ask 'which model' as a direct screening question."

### 2c. Five concrete examples — what the buyer supplied vs omitted

| # | Buyer (source) | Supplied | Omitted / left to the seller |
|---|---|---|---|
| 1 | **Mumbai agency, "Photoreal Brand Content, Ongoing", $1,000** (`proposals/2026-09-15-afternoon-chrome.md` l.33) | Duration band 15–45 s; batch size 4–8 cuts; three shot types incl. "interiors and architecture (their hardest)"; method mandate "image-to-video with first/last-frame control, not text prompts"; 3–5 working days per batch; three screening questions incl. "which AI video model … and why"; exclusion "not for templated talking-head avatar reels" | Which brand/product the first batch is for (the proposal's closing question); no copy, no offer, no language, no brand kit, no rejection criteria beyond the shot checklist |
| 2 | **FAMAG spiral mixers, AU, $150** (`afternoon.md` l.14, l.61–77) | Real product photos from famagmixer.com; product range 5–60 kg; exact lines "SALE ON NOW. SAVE UP TO 30%" and "5 kg to 60 kg. Built Your Way."; 7-day shipping line; four direct questions (Runway? accuracy? first 3 seconds? do you edit/typography/music/export?) | Duration (proposal chose 15–20 s), formats (proposal chose 9:16 + 4:5 + 1:1), music, VO, number of scenes; which mixers open and close (the proposal's question) |
| 3 | **US jewelry brand, couple skits, $1,000/month retainer with $75 trial** (`afternoon.md` l.15, l.79–91) | Narrative shape (husband, wife, "three jabs", engraved box reveal); 4 segments, 45 s cut + 3 s plate; explicit "link to one AI video with two people talking"; tool workspace question (Higgsfield/TopView) | The engraving text itself (proposal asks "Which engraving comes first"); language; ratio; acceptance criteria; brand kit |
| 4 | **enCappture, "Photoreal AI commercial editor ~40s LinkedIn", $150, 0-hire client** (`2026-09-16-morning-chrome.md` l.103) | Locked shot list (promised); "lock character refs and keep faces consistent"; "no logos, UI text or readable brand marks in the generation"; composite icons/UI/logo/QR/end card in Premiere/AE/CapCut; 1080×1920 + 1920×1080; project-file handoff; one revision round; paid 10–15 s test first; a named person as publish gate; "Skip if you only do prompt-to-export" | Whether the shot list is actually locked, where the "gather" beat is set (the proposal's question); VO; music; copy |
| 5 | **Knox Deco furniture catalogue (MKT-002)** (bank l.555–563) | 15–30 s each; 1080×1080 master; up to two revision rounds; no watermark; 9:16/16:9 on request; "$30–45 per approved video"; paid test then a "substantial portion" of the catalogue | Any on-screen text; any language; visual style beyond "product video"; what makes a video approved |

Counter-examples of thin briefs: MKT-012 "A short cinematic product ad, 10 to 20 seconds. $80 fixed." and MKT-014 "An AI video ad, produced from images. $10 fixed." — nothing else recorded. Lithuania Shopify post (`2026-09-16-review-~022099905412519082561.md` l.13): "I will provide the products and references/examples of the style I'm looking for. Please send me your portfolio and your pricing" — the buyer supplies physical goods and expects a shoot.

**INFERENCE on brief completeness.** Buyers who pay well specify *method and fidelity constraints* (image-to-video from a still, product never regenerated, text in the edit, faces locked, paid test) and *delivery geometry*; they almost never specify copy, language, brand palette, or rejection criteria. The one thing they consistently specify that the profile does not sell is *the process* ("shot approach before generating"). The Upwork profile's headline promises (exact text, 4 h) are answers to questions these buyers did not ask; the profile's method line ("You approve the words before anything is generated") is the part that matched.

---

## 3. Does the Upwork promise require capabilities the MI architecture does not yet operationalise?

Cross-check of each promise against (a) what the architecture has, (b) what the three productions achieved. Turnaround/iteration/cost numbers are from the case TIME-AND-COST.yaml files (mechanical clocks).

| Promise (PROFILE.md) | MI operationalisation today | Production evidence 001 / 002 / 003 | Verdict |
|---|---|---|---|
| **24 h standard** on every package; **4 h express** on Static Starter/Standard and Video Starter (l.71, l.103–112) | No SLA, deadline or turnaround logic anywhere in runtime: `PRODUCTION-JOB-v1.yaml` l.139 `deadline_utc … required: false`; `grep -rn deadline\|turnaround runtime` finds only that field and gRPC DEADLINE_EXCEEDED classification. TTAO is *measured* (QA-CHECKLIST A10, workflow §1) and adopted as a KPI (case 001 PROMOTION-QUEUE l.60–65), never *enforced*. | 001: TTAO **7:53:35** lower bound, 5 versions, 5 review cycles, USD 15.39 for one 57 s film (quoted tier — inside "2 to 4 working days"). 002: **1:07:33** lower bound for 9 tiles after **13 human-flagged defects** on the first export; TTAO "NOT_MEASURABLE" (chat-only accept). 003: **14:27:50** to final REJECT, 3 versions, 10 review cycles, USD 5.09, nothing accepted. The only sub-4-hour figure anywhere is UPM README tile 1 "brief 18:13:59 → files 18:40:52 IST, 26 m 52 s, pipeline stamps" = case 001 V3 CLOCK.json 1,612 s — a *generation-to-bundle* clock inside a version that was then REJECTED as a film; the same tile's 9:16 clip had "15% OFF" run off the panel (002 HD-01) when exported on 15 Sep. | **Not operationalised.** No customer order has been timed. Vaibhav himself deleted every time claim from the tiles (LOG.md l.115: "clock board deleted; no '24 hours', 'same day' or timestamps anywhere"), i.e. the speed proof the whole positioning rests on (PROFILE l.293 "This is the board the whole positioning rests on") does not exist. |
| **Exact text "every time"** (l.78); catalog title "with your exact offer text" | Code-set composition on textless plates (SKILL "Exact text … composed by code onto a textless plate by default"); QA C6 byte-check; `check_text_bounds`, `check_contrast`, `check_disjoint` in `runtime/compositor/gates.py` (l.46, 86, 185). | Characters: 4/4 and 6/6 in the Lab (PLAN §1). Layout: **text clipped** 001 V3 SD-01; **clipped again** 002 HD-01/HD-02 on the first tile export because "no gate ran on that path" (002 SYSTEM-DEFECTS tally); 003: 9:16 zero text deviations but 4:5/1:1 "copy has no wall to sit on after the crop" (SD-09). Hindi headline shrank "until it was smaller than the pill" (002 HD-12). | **Characters yes; delivery no.** "Exactly as you send it" held on every accepted file; "every time" was false on the first export of two of three productions. FORMAT_SPECIFIC_REVALIDATION now in QA-CHECKLIST C-final, promoted from 002. |
| **"Your product photo placed in a new scene"** (l.76) + decision-7 drift gate | QA-CHECKLIST B2 is a *human* side-by-side ("proportions within ~5 %, hue family unchanged") and D2 "product drift" on video frames; no deterministic drift measurement exists in runtime (`grep -rl drift runtime --include=*.py` hits only two test files). ALPHA-1.md l.114: supplied photo "Seedream 5 Pro edit 10/12, every draw on a constructed stand-in"; l.157: "a static ad with a supplied product photo demands … from one call, which no route answers today" → goes to a person. | **No production has ever placed a customer's photo.** Tile 9 (Brewa) packshot was GPT Image 2 generated (001 RO-08 "GPT Image 2 4/4 … premium packshots"); IronLeaf packshot GPT Image 2 (002 RO-03); Cumin used the brand's PDP JPEG as an *inline reference* to Nano Banana 2 (003 JOB.yaml plan) and 1/6 draws "reproduced and garbled the embossed mark" (SD-01, caught by the human B2 check before review). | **Claim is proven only on generated stand-ins.** The hard gate exists as a checklist row; the fallback ("clean cut-out composite") has never been exercised. HYPOTHESIS: the first real DTC order with a real bottle is the first test of decision 7. |
| **10-15 s video ads … with English, Hindi or Indian-English voice-over** (l.77; catalog B) | ALPHA-1 (C-7) excludes "native speech" and `spoken_voiceover` "on the most restrictive reading" (ALPHA-1.md l.29); the agency may produce it only under job-specific authorisation (SKILL "Alpha-1 … does not bound what the agency may produce"). Voice route: PLAN §1 "Sarvam bulbul v3 6/6 … Use Sarvam." | 001 RO-05: 16/16 verbatim transcripts, **rejected by ear** as "horribly robotic" over 48 s. 003: Sarvam 8 takes, 0 accepted ("all three are robotic"); ElevenLabs 6, 0 ("no Indian-English premade voice"); Gemini TTS Leda accepted on round 5 after **26 takes**; final V3 rejected for "voices are overlapping" (DF-08, no VO schedule gate). 002 N2: native narration "two different narrator voices" across two clips. | **Voice-over is sold as standard and has no accepted route.** Every VO the owner has heard in production was rejected at least once; the one accepted voice (Leda "bubbly") sits in a rejected film. |
| **"Unlimited variants of an approved concept"** (l.79) and "six hooks" tiles | Deterministic composition of variants is the strongest thing the compositor does (002 RO-06: "every defect … on statics was a composition/process defect on accepted plates; no model re-draw was needed"). | Tile 2 six hooks + Hindi four sizes accepted; Kora six hooks "REJECT as an ad (no offer, no button)" then published as "shows range and consistency" (UPT tile-08 TILE.md: "This set carries no offer or price"). | **Supported**, with the caveat that "approved concept" has never been a buyer's concept. |
| **Two revision rounds** (l.95) | Workflow §12 bounded repair; human ACCEPT/SPECIFIC REPAIR/REJECT. | Human review cycles to acceptance: 001 = 5; 002 = 5 (13 defects in round 1); 003 = 10 with none accepted. The reviewer was the owner, not a buyer. | **A buyer's two rounds would have been exhausted before acceptance in all three productions.** INFERENCE: the revision promise is priced on the assumption that internal QA absorbs rounds 1–3; the cases show it did not. |
| **Presenter 35-40 s, same person; two-speaker Hindi 8-10 s; 30-60 s films, 2-4 working days** (l.91) | `multi_shot_story`, `two_speaker_dialogue`, presenter kinds all outside Alpha-1 (C-7); presenter has "no Registry cell" (001 RO-01 n=1); speaker micro-qualification is a *candidate* pattern. | Presenter: one accepted 8 s take (RO-01), chained extends degraded (RO-02); the 57 s film took 7 h 54 m. Two-speaker: six sealed EVAL-040 clips reused (002 tile 10) — not produced for the profile. 30-60 s film: 003 is the only attempt at a product-story film for a brand and was rejected 3/3. | **Presenter: one n=1 success. Two-speaker: lab evidence only. Films: 0 for 1 on a real brand.** "2 to 4 working days" is Nadia's default (LOG.md l.581 open question), never measured. |
| **"Delivery note lists the models used"** (l.89) vs **"no tool or model names in any customer-visible text"** (QA E3) | E2 requires models used in the delivery note; E3 forbids tool names in customer-visible text. | Cumin DELIVERY-NOTE.md names no model (conforms to E3). | **Internal contradiction** between overview l.89 and QA E3; unresolved. |
| **"Never reused for another buyer"** (l.89) | DESIGN_REUSE_PROVENANCE (QA G1–G4) tracks reuse of *treatments*, not buyer exclusivity. | Tile 2 Hindi four-sizes reuse the Aarohi packshot (MANIFEST.json sources); tile 10 reuses sealed lab clips. All invented brands, so no buyer conflict yet. | Untested; cheap to keep. |

**Where the architecture is ahead of the promise:** preflight packet, per-geometry QA, ledgered spend, TTAO stamps, verbatim verdict capture, design-reuse provenance — none of which a buyer sees, all of which the promise silently depends on.

**Where the promise is ahead of the architecture:** any clock enforcement; any deterministic product-fidelity measure; any accepted voice route; any ad-structure doctrine reaching the job (003 `canon_gaps`: `commercial_communication` "fired, uncompiled" while ABCD knowledge "exists in accepted Canon").

Eight-state ladder applied to the two sharpest gaps:
- *Ad structure (003 V2):* knowledge exists (Canon google-abcd) → **not retrieved** (pack uncompiled, `canon.packs_injected: [composition_and_attention, product_appearance]` only) → never in context → decision wrong (no product close, no opening) → QA did not detect (no gate) → human detected: "did cannon say nothing about product positioning? … canon had this knowledge. how's that possible?" (003 HUMAN-VERDICTS l.42). Provable up to "not retrieved".
- *Product drift (003 plate-A-r1):* knowledge exists (PROFILE decision 7) → retrieved into QA-CHECKLIST B2 → entered context (JOB.yaml plan cites "product fidelity is checked at B2 against Slide_01 on every plate") → changed a decision (regenerate, att-008) → correct → survived (plates accepted) → **QA detected**. Provable end to end, on a *brand reference photo*, n=1.

---

## 4. Did the system optimise toward internal benchmark success (A-TEXT, OCR) and drift from what a buyer considers a strong ad?

**Evidence that it did:**
- The authored brief bank carries exact text in 28/30 briefs while the marketplace bank carries it in 1/18 (COVERAGE-REPORT l.14–24; CURRENT-30-BANK-COVERAGE-AUDIT.md l.29, l.74: "93% is a scope assumption, not an evidence-backed weighting"). The audit's own line l.89: "The two things the world most demonstrably asks for, we do not test. The two things we test most heavily, the world has not been shown to ask for."
- The commercial positioning was built on the Lab's exact-text result (PLAN §1 "4/4 … code-set text"), then on 14 Sep re-positioned to speed because the portfolio benchmark showed exact text is "table stakes" (PROFILE l.51: "offers, prices and codes already appear on a third to all of the competitors' ads, so exact text is table stakes we must be flawless at, not the headline").
- The gates the runtime owns are all typographic/geometric (`check_text_bounds`, `check_contrast`, `check_fit`, `check_geometry`, `check_disjoint`) plus frame text hygiene. In 003 "every gate that existed passed on every version; the user rejected on what no gate measured" (003 HUMAN-VERDICTS l.54): VO overlap, subject obstruction, ad structure, voice quality.
- 003 V2 verdict is the direct buyer-side statement: "it does not look like ad at all. the opening is missing too." The job's plan had 10 Canon packs selected, 2 injected, 8 "missing_domains" (JOB.yaml canon block) — the missing eight are exactly the ad-craft ones (concept, critique/effectiveness, editing/pacing, typography/copy, commercial_communication).
- The portfolio itself: tiles 8 (Kora) and 9 (Brewa) were judged "REJECT as an ad" by the owner's own five-question rubric (UPM README) and published anyway as "range" and "fidelity proof". The "Jonah's five" rubric (offer? button? readable? finished?) is a static-ad rubric; nothing equivalent exists for video.

**Evidence that it did not (or corrected):**
- The human, not the gate, was the release authority in every case (SKILL "Human release"); no version shipped on gate-pass alone. 001 V4.1 was accepted only after the *commercial* fixes ("AND IT CAN'T SUCK" restored, Express strengthened, Kora range beat added) — commercial_positioning is a named root-cause class (001 REVISION-TRACE l.132–141).
- The tile rubric explicitly demanded an offer and a CTA button before a static counted as an ad; the profile plan demanded "offers and prices on at least two-thirds of the ads" from the competitor benchmark — buyer-normed, not OCR-normed.
- The 003 job record cites 13 production learnings applied (JOB.yaml `learning_applied`) and 5 voice rounds by the human's ear before dependents — the system spent most of its effort on subjective quality, not on text.
- The 26-Aug marketplace study already told the project (sources l.104) that "character or product consistency across a series is the single thing that flips an AI-video job from productized to custom" — and identity continuity (D3), cross-clip voice continuity (D14) and design-reuse provenance are now in the QA checklist. The drift was noticed and partially corrected between 27 Aug and 16 Sep.

**Net (INFERENCE):** the *evaluation* programme optimised for measurability (text OCR, geometry); the *production* programme was pulled back toward buyer criteria by human verdicts, at the cost of 5/5/10 review cycles. The uncorrected residue is doctrine: ad structure is in Canon and not in the job, and no video-ad acceptance rubric exists that a buyer would recognise.

---

## 5. What the Upwork productions taught that the original test programme did not represent

1. **The clock is dominated by humans, not models.** 001: generation wait ≈ 14–24 % of TTAO; "human review and unattributed gaps" 3:49:34 ≈ 48 % (TIME-AND-COST l.63–85). The capability battery measured per-call pass rates; it had no notion of versions, review cycles or re-architecture.
2. **Acceptance is chat-only and multi-asset.** All three cases: `acceptance_evidence: chat_only_human_evidence`; OUTCOME-EVENT-v1 "cannot carry honestly" 5 versions × ~25 assets × 9 routes × 3 pools (001 README l.31–41); COMPLEX_PRODUCTION_EVENT trigger "MET" after 002. The brief bank assumed one job → one route → one acceptance.
3. **Presence ≠ delivery.** "Required words are present" passed a 2.9 s narration hole (002 README l.48–52); 16/16 verbatim Sarvam transcripts were rejected by ear (001 RO-05). The OCR/transcript evaluators the battery relies on are necessary, not sufficient.
4. **Format is not a rendition.** Acceptance at 16:9 did not transfer to 1:1/4:5/9:16 (002 HD-03/06/07/08; 003 SD-09). The 30-bank asked for aspect ratios as a delivery field, never as separate acceptance objects.
5. **Cross-asset invariants.** Two clips, two narrators (002 HD-13b); same presenter across takes (001 RO-02 degraded on extend). The battery tested within-clip consistency only (PLAN §1: "Only within-clip consistency is proven").
6. **Provider liquidity and transients are production facts.** fal cash USD 0.26 killed two slots (001 SD-11); Veo UNAVAILABLE ×2; Lyria 503 ×3; ElevenLabs quota at 54 credits (003). None of this exists in a benchmark.
7. **Copy origination is part of the job.** 002 PD-02: copy "invented by the operator during execution"; 003 froze a deck before spend. The brief bank supplied copy as a fixture; real work has to originate it and get it approved.
8. **Buyers judge ad-ness, structure and voice.** 003 V2/V3 verdicts. No brief in either bank states "must look like an ad" because it is assumed; the runtime had no way to check it.
9. **Real brand assets bring legal constraints.** Cumin intake `forbidden:` list (no health/PTFE/patent claims, no film actress, no implied endorsement) and "Unsolicited spec work" legal line — absent from every authored brief.
10. **The proposal is the real product surface.** Buyers ask "which model", want a shot approach before generation, want paid tests. Nadia's proposals answer these with tile names and milestone structures the runtime cannot yet fulfil on a clock (e.g. "$120 interior test shot due 18 Sep" — sent 15 Sep, LOG l.5).
11. **Speed proof needs a real order.** The clock board was deleted because no honest elapsed time existed (LOG l.115). The programme had no instrument that starts at "brief complete + words approved" and ends at buyer acceptance; TTAO now approximates it from the *owner's* acceptance.

---

## 6. Persona verdicts

Citations: 001 = `production-learning/cases/UPWORK-INTRO-001/HUMAN-VERDICTS.yaml @ 3bb9a3c`; 002 = `…/UPWORK-PORTFOLIO-002/HUMAN-VERDICTS.yaml @ 3bb9a3c`; 003 = `production-learning/cases/CUMINCO-CHOPSTICKS-003/HUMAN-VERDICTS.yaml @ 1de2b37` (PR #103, unmerged) and `agency/jobs/AGY-2026-09-15-CUMINCO-CHOPSTICKS-001/JOB.yaml @ de1f978` `versions:`.

| Persona | Expectation | What the current system supports | Observed failure (cases) |
|---|---|---|---|
| **Founder / Brand Owner** (Cumin-like DTC founder) | "Make my product look like my product, in a piece that looks like an ad, without inventing claims." | Reference-image plates with human B2 fidelity check; frozen copy from the brand's own words; forbidden-claims list in intake (003 JOB.yaml). | 003 SD-01 garbled embossed mark caught pre-review (good); 003 V2 "did cannon say nothing about product positioning? the closing shot should have cumin product and final caption. it does not look like ad at all." No product hero, no end card, no brand early. The founder would have received three rejected films. |
| **CMO** | Brand-safe, on-register work with a review cycle I can predict; two rounds max. | Verbatim verdict capture; bounded repair per layer; delivery note with rights line. | 001 needed 5 versions ("competent, not extraordinary" V2; V3 "reject … voice horribly robotic"); 002 first export had 13 defects incl. "dhaba 47 1x1. text on image. bg and text colour combo not looking good." A CMO's two rounds are spent before round 3 of internal repair. |
| **Performance Marketer** | Many variants of a winning concept, offer/price/code exact, fast, in every placement size, launched this week. | Deterministic variant composition; exact-copy byte-check; four sizes from one layout; C-final per-geometry QA. | 002 HD-01 "9X 16 motion is getting text cutoff"; HD-08 "banner cutting plant"; HD-03 Kora headline over the garment in every crop. Variants were produced; placements failed on first export. No buyer-side speed evidence (clock board deleted). |
| **Media Buyer** | Re-captionable 9:16 + 1:1/4:5 masters, hooks as separate files, clean audio, no AI tells (hands, text, morphing). | Frame-sampled text hygiene (D1), hands/faces (B4/D4), delivered-vs-declared (D12), contact sheets (D13). | 003 V1 "the video has got some random audio. her lips are omving. the text is coming on figures. all messed up"; 003 V3 "the voices are overlapping". 003 SD-09: feed formats had no copy zone. A media buyer would have rejected all three cuts on audio alone. |
| **DTC Growth Lead** (retainer buyer, catalog C) | "Every request within 24 hours", weekly drops, Hindi versions, unlimited hooks; a system, not a film. | Retainer priced at $900–2,800 with +$30/+$40 express per request; compositor makes variants at ~USD 0; TTAO measured. | No retainer request has ever been fulfilled; TTAO evidence is 7 h 54 m (film), 1 h 07 m (tiles, owner-judged, 13 defects), 14 h 27 m (rejected). 002 process "NON-CONFORMANT" when speed was prioritised: "i suspect you didnt use the pipeline either properly". Growth lead's risk: the 24 h promise is met by skipping the workflow. |
| **Agency Account Director** (Mumbai agency post; "AI Video Production $50k+/mo") | Capacity, workflow, team, tool transparency, batches of 4–8 cuts in 3–5 working days, interiors that hold straight lines. | One operator, one Claude session, credits-only pools; job record + ledger + QA table per job; honest "interiors are the one shot I have not published" (proposal 1). | 001 TIME-AND-COST: one 57 s asset ≈ 8 h and 54 dispatches; 003: 50 attempts, 26 voice takes, 10 review cycles for 18 s. An AD reading these would not underwrite 4–8 cuts per batch on a schedule. Proposal 1 promised "$120 interior test shot due 18 Sep" — no interior i2v has ever been run (proposal's own admission). |
| **Skeptical Agency Owner** ("show me the money and the misses") | Proof of paid work, reviews, a repeatable margin; no invented metrics. | Nadia's honesty rules (no metrics, no tool names, "Demonstration · invented brand" on every board); ACCOUNTABILITY.md floor USD 250 net/month; kill test; ledger-true CpAO (001 corrects the pilot's USD 7.31 to USD 15.39; 002 corrects chat USD 3.9 to USD 4.66). | Zero orders, 2 proposals sent, 0 viewed (LOG l.5); month-1 target USD 1,000 with Claude Max USD 200 + Connects as fixed cost; Nadia's own estimate "about 30% for one paid order inside 30 days on 100 Connects" (first-proposals-plan l.7). Proposal 4 sent to a "0-hire client" against the filter's own zero-hire rule (LOG l.5 "why it should not have been drafted"). The owner's verdict: the cost side is honest and the revenue side is unproven. |

---

## 7. Classification of what was found

**Durable creative knowledge** (holds regardless of model):
- Ads carry the offer: prices/codes on a third to all competitor creatives; 20–40 words is normal; grids beat single ads; reviews beat metrics (portfolio benchmark l.123–129).
- Ad structure: brand early and throughout, product close/end card, a Direction, see-and-say — exists in accepted Canon (google-abcd) and was the 003 V2 rejection reason. Status: **known, uncompiled, not reaching jobs** (003 `canon_gaps`).
- "The text is the ad" for statics; for video, "presence is not delivery" (voice cadence, holes, overlaps).
- A concept must be approved at one aspect ratio *per delivered geometry*; a 9:16 macro cannot be cropped into feed formats (003 GEOMETRY_NEEDS_ITS_OWN_PLATES).
- A still with a clip needs a still fallback (competitor players failed to load; tiles carry storyboards).

**Empirical model knowledge** (directional, n small, routing_authority none — as the cases label it):
- Sarvam bulbul:v3 long/emotive reads rejected by ear (001 RO-05 n=16; 003 n=8, 0 accepted).
- Native generated narration not identity-stable across generations (002 RO-02 n=2).
- Veo 3.1 Fast i2v animates mouths under VO unless told otherwise (003 n=7); extend chains degrade (001 RO-02); t2v+extend split narration (002 RO-01).
- Seedream 5 Pro edit: geometry held 6/6 on generated packshots (001 RO-07) but 2/4 on supplied packs (PLAN §1).
- GPT Image 2 medium: textless packshots 4/4, 3/3 (001 RO-08, 002 RO-03).
- Nano Banana 2 with inline references: 5/6 bowl fidelity, 1/6 garbled mark (003).
- Kling i2v sharpens blurred signage into letters (001 RO-06).
- Gemini TTS Leda accepted by ear once; one PROHIBITED_CONTENT false positive (003).

**Production pattern** (workflow, some promoted, some candidate):
- Promoted: TEXT_BOUNDS/CONTRAST/CROP_FIT/GEOMETRY/DISJOINT gates; VIDEO_FRAME_TEXT_HYGIENE; PROVIDER_POOL_AVAILABILITY; TRANSIENT_ERROR_CLASSIFICATION (001); QA_COVERAGE_ENFORCEMENT, FORMAT_SPECIFIC_REVALIDATION, PAID_PRODUCTION_PREFLIGHT, CROSS_CLIP_VOICE_CONTINUITY, REJECTED_DESIGN_REUSE (002); VO_SCHEDULE_GATE (003, PR #103 unmerged).
- Candidate: SPEAKER_MICROQUALIFICATION, STILLS_FIRST, SINGLE_VOICE_SOURCE, VO_FIRST_TIMELINE, CLOSED_MOUTH_UNDER_VO, AD_STRUCTURE_MINIMUM, VOICE_BY_EAR_FIRST, GEOMETRY_NEEDS_ITS_OWN_PLATES, READABILITY_MARGIN, STACK_LEVEL_FIT, SUBJECT_AWARE_CROP.
- Measurement pattern: TTAO from first input; ledger governs over chat figures; two clocks never mixed; verdicts transcribed verbatim.

**Customer-commercial requirement** (what the market and the profile impose):
- Clock semantics: starts at brief-complete + words approved; 09:00–19:00 IST Mon–Sat; express refund on miss; revisions within 24 h; catalog field can only hold whole days.
- Two revision rounds; delivery note (AI-generated, human-directed; rights; brief-complete and files-sent times); no tool names in customer-visible text (contradicts overview l.89 "lists the models used").
- Product-fidelity hard gate with a clean cut-out fallback and a "one in five" trigger to demote the claim.
- Buyer method mandates: image-to-video from a controlled still; product never regenerated; text/logos in the edit; shot approach before generation; paid test milestone; project-file handoff; re-captionable version; 9:16 + 1:1/4:5 + sometimes 16:9.
- Per-approved-video unit pricing (Knox Deco $30–45; university $20) and paid-trial-then-retainer shapes.
- Buyers ask "which model" — the profile's no-tool-names rule must bend in proposals (Nadia's rule from the 26th run).
- Legal/claims constraints on real brands (no efficacy/patent claims; unsolicited-spec labelling).
- Accountability: net ≥ USD 250/month after Claude Max + Connects + pipeline; month-1 USD 1,000.

**Historical prior only** (superseded, keep dated):
- v1 profile copy (PROFILE l.347+), the 15 Sep 07:38 "Not offered" paragraph, the intro-video script's "no presenters, no lip-sync" (research/2026-09-14-intro-video-script.md l.3 vs the film as made).
- PLAN-2026-09-09 Fiverr gig plan and "Use Sarvam" verdict (contradicted by 001/003 by ear).
- The 30-bank's 93 % exact-text weighting as a demand claim.
- Nadia's 30 % probability estimate; the clock-board plan; specialised-profile drafts (feature removed by Upwork 28 May 2026).
- rentok-ad and the Aight gallery (see §8).

---

## 8. Local non-git directories

| Dir | What it is (OBSERVED) | Relevance | Evidence I would use |
|---|---|---|---|
| `~/Vaibhav_Personal_Projects/rentok-ad` | Two rendered ads (16:9 28 s, 9:16), `ad_script.json` with four Veo scene prompts and Hinglish spoken lines ("Kisne rent diya, kisne nahi diya…"), end card "RentOk. Renting Ka Superapp.", `assets/brief.md` with a real brand's verified site copy, palette, five customer pains and Canon constraints in the brief (Murch, Heath, StoryBrand, Hopkins, Ogilvy, Ondaatje), `source-shots/` A/B/C. Dated 30 Aug 2026. No verdict file, no ledger. | **Relevant as a historical prior**: a pre-MI, pre-agency multi-scene Hinglish dialogue ad for a real brand with doctrine injected into the brief by hand — the exact family (native speech, multi-shot story) that C-7 later excluded and that 003 failed on. Evidence of the "doctrine in brief" approach working or not is absent (no verdict). | `ad_script.json`, `assets/brief.md`, the two MP4s (ffprobe duration/loudness), `assets/copy.json`, `prompts.json`. Would ask: who judged it, was it sent, did the Hinglish lines render verbatim. |
| `~/Vaibhav_Personal_Projects/voice-workshop-agent` | "Swara", an Azure Voice Live Hinglish voice agent for an Aight × Microsoft workshop, 5 Aug 2026 (README, SPEC.md). | **Unrelated** to media production. Only signal: Aight brand and Hindi voice interest predate the programme. | none |
| `~/Vaibhav_Personal_Projects/aight-website` (assets/gallery + README) | July 2026 "hear it before you buy it" gallery: blind-test manifest with Sarvam voices (Priya/Kavya/Ishita/Aditya) on one Hindi order-confirmation script, ElevenLabs Sarah, Nano vs Seedream "chai headline"/textless images, a Wan chai-sign video with a Devanagari overlay comp; honesty rules ("only real, dated recordings", no ₹ rate card, no invented latency). | **Historical prior**: the earliest artefact of the exact-Devanagari-text thesis (textless plate + overlay comp) and of the honesty rules that Nadia later applied to tiles. Not evidence for the Upwork promise. | `assets/gallery/manifest.json`, `gallery-plan-2026-07-23.md` §0 decisions, the four voice files (same Sarvam voices later rejected by ear in 003 — a directional continuity worth noting). |

---

## Findings ranked

1. **The speed positioning has no evidence behind it.** Title and catalog sell 24 h / 4 h; the only sub-4-hour clock is a 26 m 52 s generation-to-bundle stamp inside a rejected version; the owner deleted every time claim from the portfolio (LOG.md @ ff06dab l.115); no runtime component knows about a deadline (`PRODUCTION-JOB-v1.yaml` l.139 optional field only). OBSERVED.
2. **Voice-over is sold in the standard tier and has no accepted route.** Every VO heard in production was rejected by ear at least once (001 RO-05; 003 voice rounds 1–4; 002 HD-13). C-7 excludes native speech from Alpha-1. OBSERVED.
3. **"Your product photo placed in a new scene" has never been done with a customer photo.** All packshots in the tiles are GPT Image 2 generations; Cumin used a brand JPEG as a reference and 1/6 garbled the mark. The decision-7 gate is a human checklist row, not a measurement. OBSERVED + INFERENCE.
4. **Buyers do not ask for exact text; they ask for method and fidelity.** 0/18 marketplace cases state on-screen copy (computed); Nadia's three best posts ask for image-to-video from a still, product never regenerated, text in the edit, shot approach first. The profile's headline claims answer questions buyers did not ask; its process line is the part that matched. OBSERVED.
5. **Ad-craft doctrine exists in Canon and does not reach jobs.** 003 V2 rejected "does not look like ad at all" with `commercial_communication` uncompiled and 8 of 10 selected packs missing (JOB.yaml @ de1f978 canon block). This is the one gap the buyer personas all hit. OBSERVED.
6. **Revision economics are inverted.** Two rounds promised; 5/5/10 owner review cycles observed. INFERENCE: internal QA must absorb at least three rounds before a buyer sees anything, and today it absorbs zero on dimensions no gate measures (voice, structure, obstruction).
7. **Speed and process conformance traded against each other once already.** 002 hit 1 h 07 m by bypassing the workflow and shipped 13 known-class defects to the reviewer. OBSERVED.
8. **The commercial funnel is untested, and one filter rule was already broken.** 2 proposals sent, 0 viewed; proposal 4 sent to a 0-hire client against the plan's zero-hire rule (LOG l.5). OBSERVED.
9. **Two internal contradictions in the offer text:** overview l.89 "delivery note lists the models used" vs QA-CHECKLIST E3 "No tool or model name in any customer-visible … text"; intro-script "no presenters" vs the film as made (documented as history). OBSERVED.
10. **What is genuinely strong and buyer-relevant:** deterministic variants and exact characters on statics; per-geometry QA; honest ledgers and TTAO; the proposal filter and proposal shape (method described back to the buyer). OBSERVED.

## Open questions / unknowns

- UNKNOWN: whether proposal 1 ($1,000, Mumbai agency) has been viewed or answered after 16 Sep 11:30 IST; whether the "$120 interior test shot due 18 Sep" can be produced — no interior i2v run exists anywhere in the repos.
- UNKNOWN: the actual smallest value of Upwork's catalog delivery dropdown (PROFILE l.205 asks Vaibhav to confirm); whether the express refund line is enforceable inside Upwork's milestone flow.
- UNKNOWN: whether a supplied real product photo through Seedream/Nano Banana holds within the decision-7 5 % / hue tolerance — the only evidence is 2/4 on a constructed stand-in and n=6 on a brand JPEG.
- UNKNOWN: an accepted voice route for Hindi or Indian English at production length; Leda "bubbly" was accepted for five short English lines only.
- UNKNOWN: whether PR #103 (case 003 + VO_SCHEDULE_GATE) has merged; at `3bb9a3c` main does not contain case 003, so the Cumin learning is not yet in the authority the agency reads.
- UNRESOLVED CONFLICT: PLAN-2026-09-09 §1 "Sarvam bulbul v3 6/6 … Use Sarvam" vs 001/003 by-ear rejections; PROFILE overview still sells Hindi/Indian-English VO on that basis.
- UNRESOLVED CONFLICT: overview l.89 (models listed in delivery note) vs QA E3 (no model names customer-visible).
- Not verified by me: anything Nadia read off Upwork pages (proposal counts, client spend, catalog approval) — repo text only; screenshots are not on disk.
- Not opened: `proposals/2026-09-15-1440-cloud-blocked.md` beyond its title; LOG.md entries outside the state of record and grep hits; the MKT case bodies beyond customer_brief/R08/R16; rentok-ad MP4 bytes (no ffprobe run).
