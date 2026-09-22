# Addendum D — Five-stage records (producer output), five briefs

Written 2026-09-20 by the lead session as **producer**. Same Canon (`3bb9a3c`), same source material as each existing plan. Format per brief: Stage 1 intent contract with field operations (`preserve` = customer said; `derive` = follows from facts; `decide` = we chose, veto-able; `ask` = needs the customer; `flag` = contradiction or risk) and a verification method per mandatory requirement; Stage 2 structure (facts, each marked `verified` / `fetch` / `assumed`); Stage 3 creative question records (question → source → answer → destination); Stage 4 selection; Stage 5 verification plan; Unresolved; Gate outcomes. Canon ids are cited where a claim was used; **no-knowledge** is written where Canon has nothing. Bias statement: producer has hindsight of every recorded rejection.

---

## B1 — Cumin Co. chopsticks film

*(Full record in Addendum B §3; summary here so the checker sees all five in one form.)*

### Stage 1 — Intent contract
| Field | Op | Value | Verification |
|---|---|---|---|
| Deliverable | preserve | video ad; "how to hold chopsticks" is the content device | — |
| Objective | ask (default: consideration) | show the Ramen Bowl fitting into noodle night | human at P1 |
| Product / hero | decide | 15 cm Ceramic Ramen Bowl (Kairi + Rosé); hero in frame 0 and last frame | frame check, first and last frame (checker/human) |
| Mandatory events | preserve | girl shows step 1/2/3; boy fails; they eat happily with Cumin cookware | board frame per event; human at P2 |
| Voice | preserve + decide | calm, empathetic, Indian-English female VO; cast by ear before plates | human ear at P3 |
| Text | preserve | short text companion per step; five blog fragments; **add** product name + URL (ask) | byte check (code) |
| Formats | decide | 9:16 master; 4:5, 1:1 composed separately | per-geometry check (code) |
| Forbidden | derive (PDP/brand) | no health/PTFE/patent claims; no standing chopsticks; no endorsement | text scan + human |
| Spend / approver | ask | USD 8; the user | ledger |
| Acceptance | ask | 5 statements (Addendum B §3.6) | as listed |

### Stage 2 — Structure
Reels 9:16 1080×1920; safe zone top 14 % / bottom 35 % / sides 6 % (**fetch**, Meta Ads Guide); ad on Reels must contain: hook ≤ 2–3 s, brand recognisable early, an ask at the close, product last (sk_abcd_0007/0010/0011/0019/0026 — **verified** Canon); duration derived from VO (not fixed 18 s); product facts **verified** from PDP/blog (notch holds chopsticks or spoon; 15 cm; two glazes).

### Stage 3 — Creative question records
Q1 opening → sk_abcd_0006/0007 → macro on the mint bowl, crossed sticks, noodle sliding back, wordmark at t=0 → beat 1. Q2 brand over time → sk_abcd_0010/0011/0012/0013 → wordmark from 0 s, bowl every frame, packshot end card, spoken brand → beats 1–6. Q3 ask → sk_abcd_0019/0020/0021, qa_abcd_0011, sk_sb_c003_0011 → "cuminco.com" on card and spoken, after context → beat 6. Q4 close → sk_abcd_0026, sk_ogx_0039 → end card from the brand's own packshot → beat 6. Q5 selling frame (PA-D7 honest) → sk_hop_sa_0026 → the notch shot, ≥ 3 s → beat 5. Q6 supers = VO → qa_ogx_0073 → VO 2–4 = supers verbatim. Q7 copy zone per geometry → CA-D2, sk_wcag_0001, MF P16 → reserved wall zone in each plate prompt. Q8 timing → **no-knowledge (Canon)**; MF `assemble.py` → VO first, measured. Q9 voice → **no-knowledge (Canon)**; MF P8, 001 RO-05 → three candidates, longest line, before plates. Q10 cuts/holds → CA-D7/D10/D11 (compiled) → kept; beat 2 must move. Q11 mouths under VO → **no-knowledge**; RO-02/DF-03 → "mouths closed" clause. Q12 end-card ground → qa_lsmx_0039 → background carries the extreme.
Board: six frames (Addendum B §3.3).

### Stage 4 — Selection
NB2 + refs → Veo 3.1 fast i2v 6 s silent (credits only; fal excluded). Riskiest: the miss (hands + crossing sticks + falling noodle) → micro-qualify first, two draws. Text and end card by code. Voice: Gemini TTS / one non-Western ElevenLabs voice / Sarvam on a rhythm-rewritten script — ear at P3. Cost delta ≈ +USD 0.35 (extra plates).

### Stage 5 — Verification
Code: byte-exact strings; VO non-overlap and end-before-film (`check_vo_schedule`); no super/card/mark intersects hand/face/bowl mask per geometry; 4:5 and 1:1 own compositions; duration; loudness. Checker: bowl in first/last frame; wordmark at t=0; the miss on a frame; the notch on a frame. Human: voice register; release.

### Unresolved
Objective default; embossed mark; proposition veto; whether Veo returns a usable first second (EMC).
### Gates
1 ready pending 3 customer answers · 2 ready (one fetch) · 3 ready after checker · 4 ready · 5 defined.

---

## B2 — Nivaas Homes three-shot story tile

### Stage 1 — Intent contract
| Field | Op | Value | Verification |
|---|---|---|---|
| Deliverable | preserve | 15-s three-shot story clip 9:16 (exterior → interior → offer card) + WhatsApp still + four-size static set with price and possession date | file list (code) |
| Purpose | derive | portfolio tile proving "three shots, one story, one voice, 15 s" for real-estate buyers; invented brand | — |
| Mandatory events | preserve | exterior shot; interior shot; offer card; **same people within the clip**; Indian-English VO | frame check per shot; identity check across shots (human/checker); VO presence (code) |
| Copy | decide (invented brand) | pill "POSSESSION MARCH 2027", headline "2 & 3 BHK, WHITEFIELD.", support "FROM ₹1.2 CR", CTA "BOOK A SITE VISIT" — **legal "RERA registered" flag**: an unverifiable regulatory claim on an invented brand; use "RERA details on request" or omit | byte check; claim scan |
| Voice | decide | one narrator, one generation, split across the cut (never two generations) | single-source check (code: one VO file); ear |
| Timing | decide | shot durations derived from the measured VO; card enters after line 2 ends | schedule check |
| Formats | decide | 9:16 clip; WA 800×800 still; 1:1, 4:5, 9:16, WA statics composed from the full-res stills, not video frames | per-geometry check |
| Spend / approver | ask | owner; cap | ledger |
| Acceptance | decide | 5 statements below | — |

Acceptance: (1) three distinct shots present in order; (2) the same two people recognisable in exterior and interior (checker/human); (3) exactly one narrator voice (one VO file; human ear); (4) no silence > 0.8 s inside a VO line (`silencedetect`); (5) statics rendered from ≥ 1080-px stills, all copy byte-exact and inside safe zones.

### Stage 2 — Structure
Reels 9:16 (**fetch** safe zone); WhatsApp still 800×800 (**verified**, PROFILE); real-estate ad conventions: price, possession, location, a direction (**assumed** from the tile brief; no Canon source on real-estate ads — no-knowledge); RERA disclosure norms **fetch/verify** before any real client; ABCD applies (video ad): brand early, product (the home) as hero, ask at close (sk_abcd_0010/0011/0019/0026).

### Stage 3 — Creative question records
Q1 what is the hero? → sk_hop_sa_0026 → the home, not the people; people give scale and warmth → exterior at golden hour, interior with the couple, card over the interior. Q2 how do two clips hold one story? → CA-D7/D9 (new information per cut; screen direction) + MF P10 (never chain; per-clip voice drift) → two i2v clips from two stills that share light and palette; one continuous VO. Q3 brand early → sk_abcd_0011 → "NIVAAS HOMES" mark from frame 0, small. Q4 ask → sk_abcd_0019/0020/0021 → "BOOK A SITE VISIT" on card **and** spoken. Q5 supers = VO → qa_ogx_0073 → line 2 = card copy verbatim ("From ₹1.2 crore. Book a site visit this weekend."). Q6 hold lengths → CA-D10 → exterior ≥ 4 s, interior ≥ 4 s, card ≥ 4 s. Q7 voice → **no-knowledge (Canon)**; MF P8 / 001 RO-05 / 002 HD-13b → one TTS narrator cast by ear on line 1 at final pace before stills; never native per-clip narration.
Board: F1 exterior golden hour, mark at t=0, VO line 1 begins; F2 interior, couple at a window, VO line 1 ends; F3 card slides up, VO line 2 = card copy; end on the card with the home visible behind.

### Stage 4 — Selection
Stills: GPT Image 2 (IMG-CORE 6/8 clean; 002 RO-03 packshots 3/3) 1080×1920. Motion: Veo 3.1 fast i2v **silent** (5/8 clean) or Kling v3 Pro i2v (8/8, fal) — pool-dependent; **never** t2v+extend (RO-01 hole) and never native narration ×2 (RO-02 two voices). VO: Gemini TTS (accepted once, 003) vs Sarvam (RO-05 caveat) — ear. Riskiest: interior with two people (identity across shots) → generate both stills first, check identity, then motion. Card by code.

### Stage 5 — Verification
Code: one VO file; no internal silence > 0.8 s; VO ends before card exit; copy byte-exact; safe zones; statics from stills (source hash). Checker: same people in both shots; hero = home. Human: voice; release.

### Unresolved
Whether a real client would supply RERA number (ask on a real order); tone (aspirational vs plain) — decide, veto-able.
### Gates
1 ready (no customer; owner approves copy) · 2 ready (one fetch) · 3 ready after checker · 4 ready · 5 defined.

---

## B3 — Upwork intro film

### Stage 1 — Intent contract
| Field | Op | Value | Verification |
|---|---|---|---|
| Deliverable | preserve | 60-s film; "the video is the demo" | duration (code) |
| Mandatory content | preserve | brief arriving (photo + offer line with price and code) with time on screen; words approved; QA moment (wrong character caught, fixed); four sizes + one 10–15 s clip landing with elapsed time; exact offer text readable in every frame; English and once in Hindi; every ad shown produced by the pipeline (eight tiles); studio name spoken once; last line "AI-generated, human-directed, custom per order"; clock reads a 09:00–19:00 IST timestamp | shot list check per item (checker); byte check on offer text; source hash for every ad shown |
| Forbidden | preserve | no 4-hour promise without the window; no metrics; nothing not on the menu | text scan; human |
| Presenter | **flag** | v2 brief: "no presenter, no lip-synced person, no recurring character"; owner's later instruction: "a character speaking to camera"; live profile: presenters "not on the menu"; Upwork help: intro video "must be a video of you and no one else" (**fetch/verify** — the existing concept cites it via search only) | **ask** — this is the single decision the whole film depends on |
| Voice | preserve | Indian English | ear |
| Hosting / aspect | ask (default 16:9 YouTube-hosted) | — | — |
| Spend / approver | ask | owner | ledger |
| Acceptance | decide | mandatory-content list above as 10 statements + "no text over the work" + contrast ≥ 4.5:1 on panels | — |

### Stage 2 — Structure
Upwork profile-video rules (**fetch**: length limit, "video of you" rule, hosting via YouTube/Vimeo); 16:9 1920×1080 if YouTube-hosted; brand rules from the profile (banned words: avatar, spokesperson, talking head); the eight tiles as the only permitted proofs (**verified**, on disk); explainer structure: script lock → VO → timing to track (Part 8 I2); every proof ≥ 3 s full-frame (001 template `important_still_min_hold_s 3.3`).

### Stage 3 — Creative question records
Q1 proposition → sk_hop_sa_0026, sk_abcd_0020 → "ad creatives back in four hours with the text exactly right; and it can't suck" (the film's one memorable line, from V4.1 evidence) → card 2. Q2 opening → sk_abcd_0007 → open on a finished ad full-frame within 3 s while the first sentence is spoken (not on a presenter, not on a clock) → beat 1. Q3 presenter → flagged; if allowed: disclosed AI, ≤ 20 s total, bookends, one anchored still, no extend chains (001 RO-02) → beats 1 and 10. Q4 proof scale → 001 V1 verdict ("proof too small", "phone mock-ups") + CA-D2 → every proof full-frame ≥ 3 s, no phone frames → beats 3–7. Q5 brand → sk_abcd_0010/0012 → studio name spoken once (brief) and wordmark on the end card only (brief constraint) → beat 10. Q6 ask → sk_abcd_0019/0021 → "Send your product link + offer. Get a straight price for the first test pack." on card and spoken → beat 10. Q7 supers = VO → qa_ogx_0073 → cards carry the spoken words verbatim. Q8 voice → **no-knowledge (Canon)**; MF P8 / RO-05 → one voice source; if TTS, cast on the **longest** paragraph at final pace; if native presenter speech, one take micro-qualified. Q9 the QA moment → decide → a Devanagari glyph flagged and corrected on screen, 3 s. Q10 pacing → CA-D10 → no card < 2.5 s.
Board: F1 finished ad full-frame + first line; F2 "AND IT CAN'T SUCK."; F3 brief arrives (photo, offer, clock 10:14 IST); F4 words approved; F5 ad builds itself (plate → panel → pill → headline → button); F6 four sizes + six hooks + Hindi flip; F7 the QA catch; F8 the 10–15 s clip in motion; F9 "STANDARD 24 HOURS / 4-HOUR EXPRESS (09:00–19:00 IST)"; F10 end card + spoken close.

### Stage 4 — Selection
Stills: reuse the eight tiles (USD 0; source-hashed). Motion: sealed EVAL-040 clips at USD 0 where they fit; new i2v from tile plates on Kling/Veo fast. Presenter (if allowed): Veo 3.1 fast i2v + native speech from one still (001 RO-01, the only accepted take) — one take, ear + transcript before anything depends on it. TTS: Gemini TTS or ElevenLabs non-Western voice; **not** Sarvam for 48 s (RO-05). Riskiest: the presenter take → first. Compositor: shared gates (bounds, contrast, fit, geometry tokens, disjoint).

### Stage 5 — Verification
Code: every mandatory item present (shot-list schema); offer text byte-exact in every frame it appears; contrast; bounds; no crop of a creative (contain); one voice file or one take; duration 55–62 s. Checker: opening is a finished ad; proofs full-frame; brand spoken once. Human: presenter naturalness; release.

### Unresolved
**Presenter yes/no** (flag; blocks stage 3); hosting; whether the Upwork rule permits an AI presenter on a profile video (fetch).
### Gates
1 **blocked** on the presenter flag · 2 ready after fetch · 3 two variants prepared (with / without presenter) · 4 ready · 5 defined.

---

## B4 — RentOK vertical ad (30 s, 9:16)

### Stage 1 — Intent contract
| Field | Op | Value | Verification |
|---|---|---|---|
| Deliverable | preserve | ~30-s 9:16 video ad | duration (code) |
| Audience | preserve | owners of hostels/PGs in India | — |
| Objective | derive | consideration → action: recognise the chaos, see RentOK as the system, know the next step | — |
| Mandatory content | preserve | chaos "painfully recognisable" (rent collection, tenant records, KYC, move-outs, complaints, compliance via WhatsApp/notebooks/spreadsheets); then RentOK as the clean system; contemporary, credible, Indian | checker on the board; human |
| Facts | derive, **verify against rentok.com only** | features that may be named: Complaint Management, Tenant Verification, Autopay, Smart Attendance, WhatsApp Communication (own number), Legal/CA/Verification/Marketing services, Whitelabel app; tools: receipt, menu, agreement generators; web + mobile app | claim scan: every named feature must match page.txt |
| Permitted claims | derive, **verified** | `page.txt` L177–232: taglines "The easiest way to manage your PGs", "Save time. Work less. Earn more."; statistics 4.9 (rating), 15,000+ (properties), 3 Lacs+, 2.3 Lacs+ (tenants), 100 Cr+ (collection), "Join 15000+ property owners who trust RentOk" — these **may** be used verbatim | claim scan: every number on screen must match page.txt |
| **Producer error, logged** | — | The first draft of this row (written before the full snapshot was read) asserted "no statistic exists on the site" and flagged the existing plan's trust stat as invented. A grep of the frozen snapshot on 2026-09-20 proved the opposite. The existing plan was correct; the producer was wrong. Left in the record as evidence that (a) the producer session is fallible on facts and (b) "verify every number against the permitted source" is the right method — it caught the producer, not just the plan | — |
| Ask | decide | "Download the RentOK app" / "See the demo on rentok.com" (site has demo videos) — **ask** the customer which | byte check |
| Language | decide (veto) | Hinglish supers, Hindi-English VO; site is English — confirm register | ask |
| Brand assets | ask | logo file, app screens (must be real screens or clearly composited UI in brand colours — never generated UI) | source hash |
| Spend / approver | ask | — | — |
| Acceptance | decide | 6 statements: chaos block ≥ 3 named pains on screen; RentOK named by t ≤ 5 s (brand early) or the ask confirmed as end-loaded; every feature named appears on rentok.com; no invented numbers; ask on card + spoken; product (the app) in the last frame |

### Stage 2 — Structure
9:16 1080×1920, ~30 s; Reels/Shorts safe zones (**fetch**); ABCD structural rules: 2+ shots in first 5 s, brand in first 5 s, on-screen person saying the brand beats VO, CTA after context, specific verb (sk_abcd_0006/0011/0012/0019/0020/0021 — verified); System1: logos in context beat overlays; sonic asset in 2 s (Part 8 H5, external); claims: only what page.txt supports.

### Stage 3 — Creative question records
Q1 how is chaos "painfully recognisable" in 5 s? → sk_abcd_0005/0006/0007 (hook + sustain; jump in; open mid-action) → open on the owner's phone mid-scroll, a rent reminder typed by thumb at 11 pm, notebook open beside it → beat 1. Q2 where does the brand enter? → sk_abcd_0010/0011; qa_abcd_0019 (no brand until the end fails all three) → RentOK wordmark small from t = 0 in the corner **or** the owner says "RentOK" at the turn ≤ 12 s; not only at 26 s (the existing plan's brand-at-close is the qa_abcd_0019 shape) → beats 1, 5. Q3 how does the turn prove the fix? → sk_hop_sa_0026 (picture as salesman) + site features → mirror structure: each pain → the real feature by name (Autopay, Tenant Verification, Complaint Management, WhatsApp from own number) on a real or brand-coloured composited screen → beats 5–8. Q4 ask → sk_abcd_0019/0020/0021, qa_abcd_0011 → after context: "See how it works — rentok.com" (or app download) on card + spoken → beat 9. Q5 Indian, not Valley → CA-D2/D5 + brief → PG textures (tube light, steel almirah, laminated rent chart) kept; **no invented signage text** (LIMIT-TEXT) — signage composited or blurred. Q6 supers = VO → qa_ogx_0073 → Hinglish pain labels spoken as well as shown. Q7 same owner, same room → CA-D9 + MF P10/001 RO-02 → one actor still anchors every shot; no extend chains. Q8 voice → **no-knowledge**; if VO, cast by ear on the longest line; prefer the on-screen owner saying the brand (sk_abcd_0012). Q9 what does the last frame show? → sk_abcd_0026 → the app on the phone with the wordmark, not a logo animation alone.
Board: F1 phone mid-scroll, 11 pm, wordmark corner; F2 notebook, red pen; F3 KYC photo lost in a chat; F4 owner at the cluttered table, exhales; F5 he taps RentOK, says the name; F6 Autopay screen "rent collected"; F7 Tenant Verification screen; F8 Complaint resolved, tenant nods; F9 phone with the app + "See how it works — rentok.com".

### Stage 4 — Selection
Stills: NB2/GPT Image 2 for the owner and room (IMG-CORE clean), one identity still reused with references (≤ 3). Motion: Kling v3 Pro i2v (8/8) or Veo fast i2v; **no native text in video** (VID-TOPO3 native text 0/4) — all screens and labels composited (RR-1/RR-6). App screens: real screenshots from the customer (ask) or brand-coloured mock UI by code, never generated. Riskiest: phone-screen shots with legible UI in motion → composite the screen onto a tracked phone (mechanism B) and test one first. Voice: owner's line native (Veo fast i2v + speech, 001 RO-01) micro-qualified, or TTS.

### Stage 5 — Verification
Code: every named feature ∈ page.txt (string match); no digits on screen unless from the customer; duration; safe zones; text bounds/contrast; no generated lettering (frame hygiene). Checker: brand ≤ 5 s; chaos ≥ 3 pains; mirror structure; last frame = app + wordmark. Human: credibility of the owner; release.

### Unresolved
The ask (app download vs demo); real app screens; Hinglish register; whether any number may be shown.
### Gates
1 ready pending 3 asks · 2 ready (one fetch) · 3 ready after checker · 4 ready · 5 defined.

---

## B5 — Skincare UGC video (25 s, 9:16)

### Stage 1 — Intent contract
| Field | Op | Value | Verification |
|---|---|---|---|
| Deliverable | preserve | 9:16 performance UGC video, ~25 s | duration |
| Product | preserve | fragrance-free 2 % salicylic-acid serum, adults, oily/blemish-prone skin; fictional Indian D2C brand | — |
| Mandatory | preserve | one believable Indian woman to camera; natural demonstration; **one** clear purchase reason; creator feel, visually controlled, commercially usable | checker on script + board |
| Forbidden | preserve | no clinical statistics, guarantees, medical claims; no external website | claim scan (regex for %, "clinically", "cures", "guarantee", URLs) |
| Purchase reason | decide (veto) | "fragrance-free and weightless: it disappears in seconds, so I actually use it every night" — one reason, sensory, non-medical | script check |
| Brand | decide | a name and a bottle; name spoken by her (sk_abcd_0012) and on the bottle | frame + transcript |
| Ask | decide | soft: "link in bio" spoken + small end text (no URL) | transcript + byte check |
| Language | decide (veto) | Indian English with one Hindi phrase max | — |
| Spend / approver | ask | — | — |
| Acceptance | decide | 6 statements: one woman, same identity all shots; brand name spoken; bottle visible ≥ 2 shots; exactly one purchase reason stated; no forbidden claim; ask present |

### Stage 2 — Structure
9:16 1080×1920, ~25 s; Reels safe zones (**fetch**); UGC conventions: lo-fi register beats gloss for attention but halves brand ID unless early branding is engineered (System1 × TikTok, Part 8 H5 — external, global evidence, no India-specific data); ABCD: on-screen person mentions the brand > VO (sk_abcd_0012); logo **in context** (on the bottle in hand) beats an overlay (H5); CTA after context (qa_abcd_0011); captions for muted play (H7).

### Stage 3 — Creative question records
Q1 hook in ≤ 3 s → sk_abcd_0005/0007 → she opens mid-action, serum already on two fingers, "if your skin is oily by noon, this is the only one that didn't make it worse" — bottle in hand from frame 0 → shot 1. Q2 brand early without breaking the creator feel → sk_abcd_0011/0012/0013; H5 (logos in context) → the bottle label readable in her hand at 0–3 s; she says the name at the demo, not as a logo card → shots 1, 3. Q3 one purchase reason → brief + sk_hop_sa_0026 → the sensory reason above; the script never adds a second (no "and it cleared my skin") → script. Q4 proof → demo of absorption: two drops, pat, ten seconds later she touches her cheek and it is dry → shot 3–4 (a *visible* proof, no claim). Q5 ask → sk_abcd_0019/0021, qa_abcd_0011 → "link in bio" spoken at the end + small text → shot 5. Q6 captions = speech → qa_ogx_0073 → burned captions verbatim. Q7 identity across five shots → CA-D9; 001 RO-02 → one anchored still, every shot i2v from it with ≤ 3 references; no extend. Q8 register: lo-fi vs controlled → brief ("visually controlled") → handheld feel but locked identity, window light, no filter → prompts. Q9 voice → **no-knowledge (Canon)**; native speech per shot has identity risk (002 HD-13b) → **one** take strategy: either one continuous 8-s native take for the speaking parts + silent b-roll, or TTS over silent clips with mouths closed — decide after micro-qualifying one native take. Q10 bottle text → LIMIT-TEXT → label composited on a textless bottle plate; never generated.
Board: F1 mid-action hook, bottle in hand; F2 the problem ("smell, greasy by noon"); F3 two drops, pat; F4 dry-touch proof; F5 "it's [brand]; link in bio", bottle to camera, caption.

### Stage 4 — Selection
Still: NB2/GPT Image 2 for the woman (identity still) + a textless bottle plate; label by code. Motion: Veo 3.1 fast i2v + native speech from the anchored still for the speaking shots (001 RO-01: one accepted take; RO-02: no chains) — micro-qualify shot 1 first (face + speech + bottle in hand = the riskiest); Kling i2v silent for the demo inserts. Captions by code. No Sarvam (register is conversational English; RO-05).

### Stage 5 — Verification
Code: forbidden-claim regex on script and captions; no URL; captions = transcript; one identity still referenced by every shot; duration; safe zones; bottle label byte-exact. Checker: brand spoken; one purchase reason; bottle ≥ 2 shots; hook ≤ 3 s. Human: does she read as real; release.

### Unresolved
Brand name (fictional — decide, veto); one vs several native takes (EMC); whether the dry-touch proof reads as a claim (checker).
### Gates
1 ready · 2 ready (one fetch) · 3 ready after checker · 4 ready after one micro-qualification · 5 defined.
