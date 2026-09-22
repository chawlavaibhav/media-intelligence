# Addendum D — Five-brief questioning experiment: frozen inputs

Date: 2026-09-20. Controller order steps 1–4 (freeze, run, evaluate independently, reconcile). No media generated, no provider called, no spend. Canon frozen at MI `main @ 3bb9a3c3da484e43d4d54ae20543d1d246769ac6`. Everything below is OBSERVED from committed bytes unless marked.

## Roles in this run

| Role | Who | Context |
|---|---|---|
| Producer (five-stage pathway) | the lead auditor session (Claude Fable 5.1) | full audit context; **same model family as the authors of every existing plan; hindsight of every recorded rejection** — a stated bias, not removable in a paper run |
| Existing pathway | the plans as committed at the time, verbatim excerpts | none re-written |
| Independent checker | a separate Claude Sonnet session, fresh context, one file, no audit, no transcript, plans blind-labelled | see `02-checker-input.md` |
| Controller | Vaibhav Chawla | reads `04-RECONCILIATION.md` |

## The five briefs and their existing plans

| # | Job | Customer brief (verbatim source) | Existing pathway plan (what was actually written before spend) | Known outcome |
|---|---|---|---|---|
| 1 | Cumin Co. chopsticks film | `de1f978:agency/jobs/AGY-2026-09-15-CUMINCO-CHOPSTICKS-001/JOB.yaml brief.verbatim` (13:17Z 15 Sep) | `86ec183:…/JOB.yaml` intake + blueprint (13:27Z) — the `/media-agency` path with 2 of 10 packs injected | REJECTED ×3 (HD-01…07) |
| 2 | Nivaas Homes tile | `upwork-project @ ff06dab PROFILE.md` L305 and L504: "Three-shot story (exterior, interior, offer card), Indian-English VO, 15 s"; "Three-shot story clip (same people within the clip), Indian-English voice-over, plus WhatsApp still"; "Four-size set with price and possession date" | case 002 N1/N2 as executed (`REVISION-TRACE.yaml`), copy deck `b4b77fa:pilots/upwork-intro-video-2026-09-14/v4/plan/COPY-PF.yaml nivaas` — no plan existed before the first paid call (PD-01); the executed sequence is the plan | REJECTED ×2, tile skipped (HD-13a/b) |
| 3 | Upwork intro film | v2 brief paragraph `PROFILE.md` L216-218 (quoted in `f6ca66f:…/preprod/COMMERCIAL-BRIEF.md` §6b) + the owner's 14 Sep instruction recorded in the same file: fully AI-made, "a character speaking to camera", "crazy good because it IS the demo" | `7629894:pilots/upwork-intro-video-2026-09-14/plan/CONCEPT-v2.md` (the V1 concept: two-hander, 55 s, 16:9) | V1 specific repair, V2 rebuild, V3 reject, V4 repair, V4.1 ACCEPT |
| 4 | RentOK vertical ad | `eval/experiments/EVAL-037/common/briefs/B01.txt` (+ `common/websites/rentok.com/page.txt` as the only permitted source) | `origin/work/eval-037-sonnet-no-canon:eval/experiments/EVAL-037/runs/sonnet-no-canon/packages/E037-sonnet-no-canon-B01-R1.txt` (Sonnet, no Canon) | judged as a package only; CONTROLLED_CANON led B01 per `CONCLUSION.md` (uncommitted judging) |
| 5 | Skincare UGC video | `eval/experiments/EVAL-037/common/briefs/B04.txt` | `…/E037-sonnet-no-canon-B04-R1.txt` (Sonnet, no Canon) | judged as a package only; NO_CANON led B04 |

Brief texts verbatim:

**B1 Cumin** — "I am thiknig to make an ad for cumin. co. I would prefer making a video ad instead of image. They have some classy cookware products and the d2c brand discovery routine got a lot of information about them. i would be keen to make a video on how to hold chopsticks for them using their product images. they also wrote a blog post about it. preferably a short video, a very calm empathetic voice doing a voice over. A charchater trying to hold the chopsticks with a bowl or sorts from cumin co infront of him- mostly a young adult. the girl trying to explain him hoe to hold- step 1, step 2, step 3. the steps are visual with a very short text companion. the boy fails but they still happily eat through their cumin cookware."

**B2 Nivaas** — profile tile rows only (above). No customer prompt exists; the "customer" was the owner's portfolio plan; the copy (two VO lines, pill "POSSESSION MARCH 2027", headline "2 & 3 BHK, WHITEFIELD.", support "FROM ₹1.2 CR", CTA "BOOK A SITE VISIT", legal "RERA registered. T&Cs apply.") was invented by the operator during execution (case 002 PD-02).

**B3 Upwork intro** — "The video is the demo, so it must do the one thing the profile promises: show finished ad creatives coming back inside four hours from a one-line brief, with the text exactly right. Dramatise the clock, not the technology: open on a brief arriving (product photo, one offer line with a price and a code) with the time on screen; cut to the words being approved; cut to the QA moment where a wrong character is caught and fixed, because reliability is the second promise; end on the four sizes plus one 10-15 second clip landing back with the elapsed time in large type and the exact offer text readable in every frame, in English and once in Hindi. It is AI-made and must look exceptional, but every ad shown in it must be one the pipeline actually produced (the eight portfolio tiles are the source), and the studio name is spoken once, as before. Sixty seconds, no presenter, no lip-synced person, no recurring character; the voice is Indian English, and the last line is the standard line: AI-generated, human-directed, custom per order. What it must not do: promise 4 hours without the window (the on-screen clock should read a 09:00-19:00 IST timestamp), show any metric (CTR, ROAS), or show anything that is not on the menu." Plus the owner's later instruction (14 Sep, recorded in COMMERCIAL-BRIEF): fully AI-made, a character speaking to camera, "crazy good because it IS the demo".

**B4 RentOK** — "I am RentOK. Create a commercially strong vertical video ad for owners who run hostels and PGs in India. Managing rent collection, tenant records, KYC, move-outs, complaints and compliance through WhatsApp, notebooks or scattered spreadsheets creates leakages and missed follow-ups. Make that operational chaos painfully recognisable and then position RentOK as the clean system for managing the property. It should feel contemporary, credible and Indian, not like a generic Silicon Valley SaaS explainer. You may use only RentOK's official website, https://rentok.com, for company, product and brand information. Target duration: about 30 seconds. Aspect ratio: 9:16." Site facts available (page.txt): features Complaint Management, Tenant Verification, Autopay ("Collect rent automatically every month"), Smart Attendance, WhatsApp Communication ("Send whatsapp using your own number"), Legal Services, Whitelabel App, CA & Accounting, Verification, Marketing; tools: rent receipt, food menu, rent agreement, logo generators; web app, mobile app, demo videos. No customer counts, no ratings, no pricing on the page.

**B5 Skincare** — "Create a 9:16 performance-oriented UGC video for a fictional Indian D2C skincare brand. The product is a fragrance-free 2% salicylic-acid facial serum for adults with oily, blemish-prone skin. One believable Indian woman should speak directly to camera, naturally demonstrate the product and communicate one clear purchase reason. It should feel like credible creator content rather than a polished television commercial, while remaining visually controlled and commercially usable. Do not invent clinical statistics, guarantees or medical claims. Target duration: about 25 seconds. No external website."

## Knowledge available to the producer (frozen)

- Canon claims by id from `canon/knowledge/current/**` @ 3bb9a3c (the ids cited in the records were each read; text in council 06/15 and Addendum B).
- The two compiled packs' 21 decisions (PA-D1–D10, CA-D1–D11) with their DEFAULT text.
- Q&A items `qa_abcd_0010/0011/0019`, `qa_ogx_0073`, `qa_lsmx_0039` (copied, id-cited; not retrieval).
- Routing evidence map cells and taint status @ 3bb9a3c; case notes RO-01…RO-06 (003), RO-01…RO-10 (001), RO-01…RO-06 (002); MF priors P7/P8/P10/P16.
- Platform facts: Meta 9:16 safe zone 14 % / 35 % / 6 % (Meta Ads Guide, Part 8 H2) — marked **fetch-and-verify** in every record, never asserted as current.

## Evaluation criteria given to the checker

The Controller's four questions (§4 of the Controller response), plus the twelve-line structure checklist from Addendum B (lines 7 and 12 rephrased as that run required) for the four advertising jobs, a "consequential decision changed?" line, and an "unresolved creative decision remains?" line. See `02-checker-input.md`.
