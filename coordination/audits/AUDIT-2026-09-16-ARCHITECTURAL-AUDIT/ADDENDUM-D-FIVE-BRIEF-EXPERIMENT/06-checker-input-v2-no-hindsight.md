# Checker input v2 — two plans (one per brief), written by a producer with no project history

You are the independent checker. You did not write these plans. Evaluate each plan on its own against its brief and the permitted facts. Do not rewrite, do not guess authorship. Use only this file.

For each plan produce:

**Part A — four questions, each scored 0 (no), 1 (partly), 2 (yes) with one sentence of evidence quoted or paraphrased from the plan:**
A1. Did the plan correctly establish what the customer asked for, without silently adding requirements the customer did not state or dropping ones they did?
A2. Did the plan identify and resolve the factual, structural, creative and production questions that this job needs before money is spent?
A3. Are the plan's decisions concrete enough to execute (shots, timings, text, voice, formats, order of work) rather than described in general terms?
A4. Did the plan introduce unsupported assumptions, facts not in the permitted sources, unnecessary questions, or complexity the brief did not ask for? (2 = none; 1 = one; 0 = more than one) — name what you found.

**Part B — fourteen lines, YES or NO, one sentence of evidence each. If the plan does not say, NO.**
1. Is the product named as the hero, and is it in the first frame and the last frame?
2. Is there a brand mark or spoken brand name within the first 3–5 seconds, and is the brand present throughout?
3. Does the film ask the viewer to do something, on screen and/or spoken?
4. Does the film end on the product or brand (pack shot, app screen, end card)?
5. Is the opening a close-up or mid-action moment rather than a wide establishing shot or a logo?
6. Is the key event the brief asked for specified as a concrete frame or shot? (RentOK: the turn from chaos to the clean system. Skincare: the demonstration.)
7. Which numbered shot or frame would sell the product on its own without reading any copy? YES only if the plan names a numbered frame and describes what is in it.
8. Are voice or spoken-line durations measured (or planned to be measured) before shot timings are fixed?
9. Is the voice cast by listening to candidates on a full line, before the visuals are made?
10. Is on-screen text kept off hands, faces and the product in every delivered format, with each format composed separately rather than cropped?
11. Do the on-screen text lines match the spoken lines where both exist?
12. Which shot carries the highest generative risk? Use this evidence, not the plan's own label: the known high-risk elements are hands and fingers, two objects in contact, falling or small moving objects, faces speaking under a voice, legible text or UI in generated motion, identity across separately generated shots, chained extensions, non-English speech from a video model. YES only if the shot the plan tests first is one that contains such an element.
13. Does every mandatory requirement in the intent contract carry a stated verification method (a code check, a named human look, or a measurement)? YES only if each mandatory item has one.
14. Does the plan state, for every fact it uses, where the fact comes from (customer, permitted source, "fetch from …", or a cited knowledge id)? YES only if no fact is asserted without a source.

**Part C — two lines:**
C1. List every consequential decision the plan leaves unresolved (things a producer would have to invent on the day). "none" if none.
C2. List every claim, fact, number or platform rule the plan states that is not supported by the brief or the permitted facts. "none" if none.

Output: `## B4 — Plan Z` then A1–A4, B1–B14, C1, C2; `## B5 — Plan Z` likewise; then one line `B4: A=<sum>/8 B=<k>/14 · B5: A=<sum>/8 B=<m>/14`. Nothing else.

---

# B4 — RentOK

**Brief (verbatim):** "I am RentOK. Create a commercially strong vertical video ad for owners who run hostels and PGs in India. Managing rent collection, tenant records, KYC, move-outs, complaints and compliance through WhatsApp, notebooks or scattered spreadsheets creates leakages and missed follow-ups. Make that operational chaos painfully recognisable and then position RentOK as the clean system for managing the property. It should feel contemporary, credible and Indian, not like a generic Silicon Valley SaaS explainer. You may use only RentOK's official website, https://rentok.com, for company, product and brand information. Target duration: about 30 seconds. Aspect ratio: 9:16."

**Permitted facts (site snapshot):** the site spells the name "RentOk"; features: Complaint Management, Tenant Verification, Autopay ("Collect rent automatically every month"), Smart Attendance, WhatsApp Communication ("Send whatsapp using your own number"), Legal Services, Whitelabel App, CA & Accounting Services, Verification Services, Marketing Services; tools: rent receipt, food menu, rent agreement, logo generators; web app, mobile app, demo videos; taglines "The easiest way to manage your PGs", "Join India's largest network of Smart Properties", "Save time. Work less. Earn more."; statistics: 4.9 (rating), 15,000+ (properties), 3 Lacs+, 2.3 Lacs+ (tenants), 100 Cr+ (collection), "Join 15000+ property owners who trust RentOk". No pricing on the page. The producer was given a list of knowledge claims by id (sk_abcd_…, sk_ogx_0039, sk_hop_sa_0026, sk_sb_c003_0011, sk_wcag_0001, qa_abcd_0011/0019, qa_ogx_0073); a cited id counts as a source.

## B4 — Plan Z

**Intent contract**
Deliverable: one 9:16 vertical video ad, ~30s, for RentOK, targeting hostel/PG owners in India who run rent, records, KYC, move-outs, complaints and compliance through WhatsApp, notebooks or spreadsheets. Viewer should feel "this chaos is mine," then feel relief that RentOk removes it, and take an action — Q: which specific action (sign up, book a demo, download the app)? — proceeding default: "Book a free demo," the lowest-friction claim-safe CTA (sk_abcd_0020). Brand/product: "RentOk" (site spelling) must appear; feature names shown on screen must be exact (Complaint Management, Tenant Verification, Autopay, Smart Attendance, WhatsApp Communication). Mandatory events, customer's words: (1) "make operational chaos painfully recognisable" — verified by a frame of notebook/WhatsApp/spreadsheet disorder before any brand appears; (2) "position RentOK as the clean system" — verified by a frame where the product UI replaces the chaos and holds through the close. Forbidden: generic Silicon-Valley SaaS visual language (the brief's own negative example); any statistic not on the permitted-facts list; the spelling "RentOK" on-screen where the source spells "RentOk" — Q: which spelling for the ad itself? — default: match the site, "RentOk." Tone: contemporary, credible, Indian — Q: reference ad for tone? — default: Hinglish VO, plainspoken PG-owner cadence, no corporate register. Language: Q: Hindi/Hinglish/English per surface? — default: Hinglish VO, English on-screen text (matches site). Where it runs: not stated — Q: platform? — default: Instagram/Facebook Reels. Cap, deadline, approver: fetch: from customer. Acceptance statements: (a) chaos precedes brand; (b) RentOk named within 10s (qa_ogx_0073); (c) product UI is the last frame; (d) no invented statistic appears; (e) CTA is explicit and singular. No contradictions found. My decisions: the specific chaos vignette and the "clean" visual metaphor — cost of wrong choice is tone mismatch, correctable at review.

**Structure**
Duration/safe zones: fetch from the confirmed platform's spec page. Shape: hook in the first beats (sk_abcd_0005, sk_abcd_0007 — open mid-chaos, not a logo card); brand early and repeated (sk_abcd_0010, sk_abcd_0011, qa_ogx_0073 — name within 10s); ask after context is set (qa_abcd_0011); close on product (sk_ogx_0039). Claims permitted: 4.9 rating, 15,000+ properties, 100 Cr+ collection, the given taglines — each sourced to this file's site snapshot, no other stat. Assets: no logo file, UI capture, font or palette supplied — fetch: RentOk logo (vector), live app screen recordings, brand color/type spec from rentok.com or the customer. Sound: muted-first with captions (Reels default muted) — default yes. Loudness: fetch platform spec. Single 9:16 deliverable, composed once.

**Creative** — Proposition: "Your PG runs on WhatsApp chaos; RentOk runs it clean." Board: 1) mid-action chaos, owner juggling phone/notebook, no brand (opening event, sk_abcd_0007); 2) WhatsApp/spreadsheet close-up, a complaint missed; 3) RentOk UI enters, VO names "RentOk" (brand timeline starts ≤10s, qa_ogx_0073); 4) Autopay screen, "Collect rent automatically every month"; 5) Tenant Verification/KYC screen; 6) Complaint Management resolving the earlier missed complaint (closes the mandatory-event loop); 7) owner relaxed, VO + on-screen CTA together (sk_abcd_0021, sk_sb_c003_0011); 8) RentOk logo/pack shot, last frame (sk_ogx_0039). On-screen lines mirror VO exactly; copy zones clear of hands/faces/UI per frame. Voice: one Indian VO artist, warm register, cast for the "relief" turn from frame 3.

**Selection** — Highest risk: legible in-app UI (route via real screen recordings, never generated lettering) and hands with phone/notebook (image-to-video from an approved still, ≤3-4 references, tested first). VO generated once; duration measured before shot timings lock. Order: voice → riskiest shot (hands/UI composite) → plates → board with measured VO → remaining clips → assembly.

**Verification** — "RentOk" spelling and feature names exact; contrast ≥4.5:1 (sk_wcag_0001); no text over the subject; VO ends before film ends, no silence >0.8s; duration/safe zones per fetched spec; no generated lettering on any UI frame; chaos-then-clean and brand-naming each land on a frame; human release before ship.

**Unresolved** — platform and its spec; CTA action; deadline/cap/approver; brand assets (logo, UI capture, palette); language-mix confirmation; RentOk vs. RentOK spelling in ad copy.

---

# B5 — Skincare UGC

**Brief (verbatim):** "Create a 9:16 performance-oriented UGC video for a fictional Indian D2C skincare brand. The product is a fragrance-free 2% salicylic-acid facial serum for adults with oily, blemish-prone skin. One believable Indian woman should speak directly to camera, naturally demonstrate the product and communicate one clear purchase reason. It should feel like credible creator content rather than a polished television commercial, while remaining visually controlled and commercially usable. Do not invent clinical statistics, guarantees or medical claims. Target duration: about 25 seconds. No external website."

**Permitted facts:** fictional brand (a name may be invented, must be flagged for approval); product as stated; no clinical statistics, guarantees, medical claims; no website. Knowledge ids as above count as sources.

## B5 — Plan Z

**Intent contract**
Deliverable: one 9:16 UGC-style video, ~25s, for a fictional Indian D2C skincare brand, a fragrance-free 2% salicylic-acid serum for adults with oily, blemish-prone skin. Viewer should feel "this creator looks like me and this solved her problem" and take a purchase action — Q: which action/vehicle? — default: spoken + on-screen CTA, "Shop now — link in bio" (sk_abcd_0019, sk_abcd_0021). One believable Indian woman speaks direct to camera; brand name is invented and must be flagged for approval — proposed placeholder pending sign-off (Q: does the customer have a preferred name/wordmark? — default: proceed with a placeholder, swap before delivery). Mandatory events, customer's words: (1) "naturally demonstrate the product" — verified by a frame of hand-to-face application; (2) "communicate one clear purchase reason" — verified by a single spoken+on-screen line stating that reason. Forbidden: clinical statistics, guarantees, medical claims, any invented product fact beyond "fragrance-free, 2% salicylic acid, oily/blemish-prone skin." Tone: candid creator register, not TVC-polished — Q: reference creator/tone example? — default: handheld framing, natural light, conversational pacing (sk_abcd_0006, "jump in"). Language: Q: Hindi/Hinglish/English? — default: Hinglish, since "believable Indian woman" implies natural code-switching. Where it runs: not stated — Q: platform? — default: Instagram Reels (performance framing implies paid social). Cap/deadline/approver: fetch: from customer. Acceptance statements: (a) exactly one purchase reason stated; (b) no clinical/medical claim appears; (c) "2% salicylic acid" stated correctly; (d) brand name flagged, not finalized without approval; (e) demonstration reads as hand-applied, not generated. No contradictions found. My decision: which single purchase reason to foreground (oil control vs. blemish control) — cost of a wrong choice is limited to re-shooting the spoken line.

**Structure** — Duration/safe zones: fetch from the confirmed platform's spec page. Shape: hook at the open (sk_abcd_0005, sk_abcd_0007 — close-up on skin or product); product introduced early and held (sk_abcd_0010, sk_abcd_0011 — the pack substitutes for "brand" here since none exists yet); ask after context (qa_abcd_0011); close on product (sk_ogx_0039). Claims permitted: fragrance-free, 2% salicylic acid, target skin type only — no percentage-improvement, endorsement or before/after claim, since none is supplied and none may be invented. Assets: no product exists — fetch: pack render/label design (created and approved before shoot) and talent — Q: cast real talent or generate a presenter? — default: real cast talent, since faces speaking is a known generative risk and this is a credibility-dependent performance ad. Sound: muted-first captions on, exact-string captions of the spoken line. Loudness: fetch platform spec. Single 9:16 deliverable.

**Creative** — Proposition: "One ingredient, one honest reason, on real skin." Board: 1) close-up on skin/product in hand, opening event (sk_abcd_0007); 2) presenter turns to camera, names her concern — product's first appearance; 3) pack shown, label legible, "2% salicylic acid, fragrance-free" stated; 4) natural application to face/hands; 5) the one purchase reason spoken direct-to-camera; 6) spoken CTA + matching on-screen text (sk_abcd_0021); 7) pack shot, last frame, product held (sk_ogx_0039). Captions mirror every spoken line exactly; copy zone kept off her face/hands/product per frame. Voice: the presenter, cast once, synced live — no separate VO generation for her lines.

**Selection** — Highest risk: faces speaking (lip sync) and hands-in-contact with product/skin — mitigated by filming the presenter live wherever her mouth is on camera; any generated cutaway (product-only, no face) is tested first. Pack text is composited, never generated. Route: real-shoot presenter footage for all speaking frames; generated plates only for non-face beauty shots, image-to-video from an approved still, ≤3-4 references. Order: pack design finalized → riskiest shot (any generated product plate) → presenter capture → board assembly with measured line timings → remaining clips → assembly.

**Verification** — Exact strings: "2% salicylic acid," "fragrance-free," the purchase-reason line, the CTA; contrast ≥4.5:1 for captions (sk_wcag_0001); no text over her face/hands; captions match spoken audio exactly, no internal silence >0.8s; duration/safe zone per fetched spec; no generated lettering on the pack; both mandatory events land on a frame; no clinical/medical claim present; brand name explicitly flagged unresolved; human release before ship.

**Unresolved** — platform and its spec; brand/product name and pack-design approval; which purchase reason to lead with; talent-casting source; language mix; CTA vehicle/wording; deadline/cap/approver.

---

End of input. Produce the output exactly in the format specified at the top.
