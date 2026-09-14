# D2C prospect pipeline — durable source of truth

**Created:** 2026-09-14 (run 01). **Last updated:** 2026-09-14 (run 02 — first run with working
external fetch). One row per brand. See `README.md` for the rules this file is maintained under.

**Stage values:** `DISCOVERED` · `SHORTLISTED` · `SELECTED_FOR_SPEC` · `IN_PRODUCTION` · `SEND` ·
`PORTFOLIO_ONLY` · `DISCARD` · `CONTACTED` · `REPLIED` · `CALL` · `PAID_PILOT` · `PAID_RECURRING` ·
`NO_RESPONSE` · `NOT_NOW`.

**Stages from `CONTACTED` onward are set by the Controller only.** The prospecting agent never sets
them and never downgrades a later-stage row; the most advanced legitimate status wins unless explicit
new evidence requires a downgrade, which must be stated in the run file.

## Evidence status — read before trusting a row

Run 01 (2026-09-14) could not fetch **any** external host, so every row it wrote was
`INFERRED (search-summary)`. **Run 02 (2026-09-14) had working external fetch** and re-verified the
three `SHORTLISTED` rows plus all new admissions.

| Evidence state | Brands |
|---|---|
| **OBSERVED** — site fetched, ad-spend footprint read from live page source, pixel IDs quoted | Salty · Cumin Co. · Open Secret · AntiNorm · Typsy Beauty · The Indus Valley · Plum |
| **OBSERVED (Ad Library)** — hand-checked by the Controller, `runs/2026-09-14.md` §9 | Salty · Typsy Beauty · AntiNorm |
| **INFERRED only — NOT YET VERIFIED** | **Farmley · Foxtale · Insight Cosmetics · Nothing But · Supertails** |

**Meta Ad Library is HTTP 403 from the cloud environment** and was never rendered by the agent. Every
statement about what a brand's *ads actually look like* comes either from the Controller's hand-check
or is explicitly absent. **Meta Ad Library + Instagram check recommended by hand for the Top 3 before
spend** — and is **outstanding for Cumin Co.**, the current #1.

## Active shortlist (score ≥ 70)

| Brand | Category | Product | Score | Why now | Creative opening | Stage | Last researched | Next action | Dossier | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| **Salty** | Fashion accessories / jewellery | The **Salty Bags** range — 19 SKUs, ₹799–₹2,099 | **89** (+1) | ₹30.1 Cr Series A (Jan 2026) funded an expansion into bags, watches, sunglasses, belts, bag charms — **now confirmed live on site** | **Premium bags vertical is live, already discounting ("Price Drop"), and in zero active Meta ads** — a gap that needs no criticism of their working creative | SHORTLISTED | **2026-09-14 (run 02)** | Controller spend decision. Pitch = the unadvertised bags vertical; fallback = the ₹999 combo mechanic | `dossiers/salty.md` | **Top 3 — #2.** **OBSERVED 2026-09-14:** Meta Pixel `361781499194146` CAPI-on, `AW-10892904816`, GTM, Shopify, Gokwik. **Catalogue in the thousands** (9 product sitemaps; 994 URLs in file 1) vs **~25 active ads**. No meaningful YouTube (2 handles checked). Hand-check: offer-led video, copy reused, no product-led motion; IG 276.6k |
| **Cumin Co.** | Premium enamel cast iron cookware | **No. 9 Enamel Cast Iron Kadai LITE 2.1L — ₹3,999 (from ₹6,599)** | **87** (new) | **$5 Mn Pre-Series A** (Fireside, Huddle, Alteria; $6.5 Mn total) + stated **₹100 Cr ARR target by FY27** + festive gifting live + adjacent categories launching (glass, knives, ceramics) | Best physical fit in the pipeline for Alpha 1 — hard-surface, non-skin, no claims, no human performance; price delta already printed on their own PDP so overlay copy is **supplied, not invented** | SHORTLISTED | **2026-09-14 (run 02)** | Controller to choose axis: creative-system buyer (Cumin) vs clearest gap (AntiNorm/Salty); pull colourway packshots from PDPs before any spec | `dossiers/cumin-co.md` | **Top 3 — #1 to produce for.** **OBSERVED 2026-09-14:** Meta Pixel `1791814054986834` CAPI-on, `AW-11561016836`, `GTM-5GXSJWGB`, Shopify, MoEngage, Gokwik. **113 SKUs ₹1,599–₹11,999.** Tiered offers CUMIN5/CUMIN8. YouTube **29.6K subs / 95 videos** (healthy organic ratio). Founders ex-**Meta** growth + ex-Zomato growth — buyers who evaluate creative for a living. **Their ads have never been seen** **Hand-checked 2026-09-14 (OBSERVED):** ~270 active Meta ads (page-filtered), newest 11 Sep, already premium product-led per-SKU/per-colour films + creator + offer ads — NOT a quality gap; pitch = launch-cadence capacity. IG @cuminco_india 80.4K; "Cumin Co. - USA" page exists. See run 02 §12. |
| **Open Secret** | Healthy packaged snacking | **Ragi Chips — Korean Mirchi 30g, ₹40** | **85** (new) | **₹50 Cr raised 15 Jul 2026** for retail expansion + product innovation, at ~10% MoM growth; festive gifting packs live and already discounted | 94 SKUs × four channels (D2C, qcomm, MT, GT) = a **repeatable pack-creative system** problem, not a one-hero-film problem | DISCOVERED | **2026-09-14 (run 02)** | **Controller call: highest ability to pay + best category fit; slowest to answer. Swap into Top 3 if optimising for contract size** | — | **Highest ability to pay (10/10) and best category advantage (5/5) in the pipeline.** **OBSERVED 2026-09-14:** **two** Meta pixels (`606540495154699` + direct signals `974281006276497`), CAPI-on, `AW-683914363`, `GT-T53FCQD` (IN), doubleclick, `GTM-59KH9Q9G`, Shopify, MoEngage — **heaviest ad stack observed**. ₹200 Cr ARR, EBITDA profitable. Founder Ahana Gautam. **Risk: pack artwork is exact in-scene text — C-7 constraint is real here** |
| **Farmley** | Healthy snacking (makhana, dates) | Flavoured **Makhana** lead SKU | 84 | FY26 growth target of 60–70% on ₹370 Cr FY25 + first EBITDA profitability; expansion into healthy desserts; rural offline push | Reported near-100% digital media spend and quick-commerce-led growth ⇒ very high creative throughput | DISCOVERED | 2026-09-14 (run 01) | **Footprint-check on the Thursday run before promoting** | — | **NOT YET VERIFIED — all evidence INFERRED.** Funding trigger stale (May 2025). Now outranked by Open Secret on the same "highest value if converted" argument, because Open Secret's footprint is verified and this is not |
| **AntiNorm** | Multitasking beauty / personal care | **Facial in a Flash — ₹1,199** (refill ₹699) | **84** (+5) | ₹28 Cr seed (Fireside, Jan 2026); **8 of 18 SKUs badged "New"**; **Festive Gift Box live at ₹3,499 from ₹4,999**; ads launching daily 3–14 Sep | **Clearest format gap in the pipeline** — ~170 active ads that are mostly **static + long benefit copy**, no product-led motion | SHORTLISTED | **2026-09-14 (run 02)** | Controller spend decision. Keep any spec ad **off efficacy claims** — product, mechanic and price only | `dossiers/antinorm.md` | **Top 3 — #3.** Best reply odds; lower ceiling. **OBSERVED 2026-09-14:** Meta Pixel `1239591777687494` CAPI-on, `AW-17055092464`, Wigzo, Shopify. **18 SKUs, not 3** — run-01 read was stale. Claims on site (pigmentation, bacne, hair growth, SPF) are a live hazard. IG 26.4k |
| **The Indus Valley** | Kitchenware / cookware | TBD — hero SKU to be confirmed | **79** (new) | $17 Mn raised; toxin-free cookware positioning | Same excellent hard-surface fit as Cumin Co. (AI 18/20), with more money behind it | DISCOVERED | **2026-09-14 (run 02)** | Retain as the **natural fallback if Cumin Co. does not respond**; identify a hero SKU | — | **OBSERVED 2026-09-14:** Meta Pixel, `AW-874123083`, `GTM-5J6MJGL`, Shopify, WebEngage, Gokwik. Larger and older than Cumin Co. ⇒ reachability only 6/10 and an incumbent creative partner is likely |
| **Foxtale** | Skincare | TBD — hero SKU to be confirmed | 78 | ₹199 Cr FY25 (2.4× YoY); losses widened specifically on an aggressive marketing push | Enormous creative throughput implied by the marketing spend | DISCOVERED | 2026-09-14 (run 01) | **Footprint-check on the Thursday run** | — | **NOT YET VERIFIED — all evidence INFERRED.** Marked down on AI fit: skincare creative leans on efficacy claims and derm/UGC talking heads, which C-7 excludes |
| **Typsy Beauty** | Colour cosmetics + fragrance | — (**Spritz fragrance pitch withdrawn**) | **73** (**−11**) | ₹20 Cr led by Saama (6 Aug 2026); 10+ launches stated as imminent | **Weak.** Saturated, not starved — ~990 active ads and established vendors | SHORTLISTED | **2026-09-14 (run 02)** | **Do not produce for.** Revisit only if it opens a non-creator-led category | `dossiers/typsy-beauty.md` | **DOWNGRADED out of the Top 3 — see `runs/2026-09-14-02.md` §3.3.** YouTube **544 videos / 2,880 subs** = ad-asset dump, not an audience. Creative engine is creator-whitelisted reels = exactly what C-7 excludes (no talking heads, lip-sync, native speech). Lip colour on skin is our weakest fidelity case. **OBSERVED:** pixel `547920049532820` CAPI-on, `AW-10854431086`, Shopify |
| **Plum** | Beauty & personal care | TBD | **73** (new) | ₹500 Cr FY26 revenue with profit doubled (reported 3 Sep 2026) | Large, established creative operation — little whitespace | DISCOVERED | **2026-09-14 (run 02)** | Watch only. Not for spend | — | **OBSERVED 2026-09-14:** Meta Pixel, `AW-974186061`, `GTM-P7N3BVB`, Shopify, Gokwik. Marked down on AI fit (12/20, claims + face-led UGC) and reachability (5/10 — at ₹500 Cr, spec work meets a marketing organisation, not a founder) |
| **Insight Cosmetics** | Mass colour cosmetics | TBD | 71 | 16 → **60 exclusive brand outlets by end-2026** | Large SKU range across a 35,000-store footprint | DISCOVERED | 2026-09-14 (run 01) | Re-screen for performance-marketing evidence | — | **NOT YET VERIFIED — all evidence INFERRED.** Trigger is retail expansion, not media spend. Mass-cosmetics shade fidelity is a real generation risk |
| **Nothing But** | Freeze-dried fruit snacks | Freeze-dried fruit pack | 71 | Seed round from an operator-heavy cap table (Noise, Innovist, Arata, DailyObjects, The Be Life) | **Highest AI creative potential scored so far (17/20)** — freeze-dried fruit is visually striking and needs no human performance | DISCOVERED | 2026-09-14 (run 01) | Watch for a priced round, then re-score | — | **NOT YET VERIFIED — all evidence INFERRED.** Held back only by ability to pay (5/10). Upgrade trigger: any institutional round |
| **Supertails** | Pet care | — | **71** (new) | $30 Mn Series C Feb 2026 at ~$130 Mn valuation; targeting ₹500 Cr ARR | Platform (vet + pharmacy + retail), not a single product brand — weakens a packshot-led pitch | DISCOVERED | **2026-09-14 (run 02)** | Watch only | — | ₹113.3 Cr FY25 (+68.4%), net loss ₹52.5 Cr. Live-animal generation fidelity is a real risk. **Footprint not checked** |

## Watchlist (60–69 — not for spend)

| Brand | Category | Product | Score | Why now | Creative opening | Stage | Last researched | Next action | Dossier | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| **Snitch** | Menswear | — | **69** (new) | 60-minute quick-commerce launch; expanding into bags, footwear, sunglasses | Weak for us — apparel advertising is on-model human performance | DISCOVERED | 2026-09-14 (run 02) | Revisit only if the accessories lines get their own creative need | — | Real scale and a genuine trigger, but the **weakest Alpha-1 fit of any brand at this scale**. `GTM-M4TXDKJG` present; **ad tags inside the container and not verifiable** — explicitly *not* evidence of no ad spend |
| Indian Snack House | South Indian snacks & sweets | Clean-label snack range | 64 | ₹2.2 Cr pre-seed led by Titan Capital | Photogenic regional-sweets category with no established ad language | DISCOVERED | 2026-09-14 (run 01) | Re-check in ~2 quarters | — | Reachable and appealing; no credible recurring creative budget yet |
| MetaMan | Men's jewellery + fragrance | — | 63 | Perfume-range expansion; ~$1.22M raised | — | DISCARD | 2026-09-14 (run 01) | None | — | **Negative filter:** core creative depends on celebrity likeness (Suniel Shetty; KL Rahul a co-founder) |
| Sid's Farm | Premium dairy | Milk / dairy range | 61 | ₹81 Cr pre-Series B, July 2026 | Weak: subscription dairy, low SKU variety, low refresh need | DISCOVERED | 2026-09-14 (run 01) | Re-check if it launches a value-added range | — | Core claim (safety; 10,000 tests/day) needs process footage we cannot generate |

## Rejected (not scored, or filtered on principle)

| Brand | Reason | Run |
|---|---|---|
| **Nestasia** | **Cloudflare 403 on both fetch routes — could not be verified at all.** Only trigger found is a $8.35 Mn round from **September 2024**, 24 months stale. Re-attempt Thursday | 02 |
| **Que** | **Negative filter:** celebrity-anchored (Shikhar Dhawan-backed) | 02 |
| **Dermatouch** | **Negative filter:** acquired by **Wipro Consumer Care, 18 Aug 2026 ($41 Mn)** — conglomerate procurement | 02 |
| **Dil Foods** | ₹72 Cr Series B Aug 2026, but virtual-restaurant operator — no packaged product, no packshot to advertise | 02 |
| **Kroslo** | Right category (cookware), ~an order of magnitude too small vs Cumin Co. (₹5 Cr seed) | 02 |
| **DecorTwist** | $200K bridge — far too small | 02 |
| Elitty · Gush · Baked Beauty · ClayCo · Diam · Type Beauty · Simply Nam · Love Child by Masaba | Colour cosmetics with the same structural problem as Typsy: creator/face-led creative and on-skin colour — the weakest Alpha-1 fit | 02 |
| TAC (The Ayurveda Co) · Asaya · Juicy Chemistry · SkinInspired · Secret Alchemist · Numour · Eze · Nirvasa | Deprioritised at quick-screen, **worth revisiting** — fragrance in particular is a good physical fit but showed no evidenced ad spend or scale this run | 02 |
| ~30 further BPC/home brands swept from two directory lists | Skinvest · DeBelle · Wishcare · Vilvah · Dermabay · By Naked Fact · Be Clinical · The Formularx · The Skin Story · Truth & Hair · Not Just Vanilla · Plenaire · Alanna · Aminu · Curlup · Deyga · Earth Rhythm · Carmesi · Bombae · Ghar Soaps · indē wild · Old School Rituals · Rubys Organics · The Love Co · The Natural Wash · Beauty Garage · Neothera · Traya · mCaffeine · EcoSoul · Rare Planet · Chumbak — none showed a *current* trigger **plus** evidenced ad spend | 02 |
| Bonhomia / Indulge Beverages | Only funding evidence dates to **2016**. **The dating trap recurred in run 02** — an undated summary re-presented it as current. Rejection stands; do not re-litigate | 01, re-confirmed 02 |
| Beast Life | Creator-led — the core creative *is* the founder's face (Gaurav Taneja). Worst possible fit for the Alpha-1 family | 01 |
| Phitku | Campaign is celebrity/film-IP-led (Mirzapur partnership, Sept 2026) | 01 |
| Cosmix | Acquired by Marico — now inside a conglomerate; slow procurement | 01 |
| Waggies (Reliance) · HappyFur (Wipro) · Ninja (Godrej) | Conglomerate-owned; unsolicited spec work disappears into procurement | 01 |
| Country Delight · The Label Life · Built · Moe Puppy · Heads Up For Tails · Blue Tokai · Rage Coffee | Dropped at quick-screen — no current trigger, subscription-utility creative, celebrity-curator model, too small, or likely mature in-house/agency creative | 01 |
| The Whole Truth · Moxie · Sleepy Owl · SBOOCH | Deprioritised at quick-screen, worth revisiting — see `runs/2026-09-14.md` §4 | 01 |
| "Get Daily" | Could not be corroborated beyond a single unverifiable mention. Not carried | 01 |
| **Inc42 "Top 20 Funded D2C Startups 2026"** | **Not a brand source.** It lists marketplaces and classifieds (Flipkart, Udaan, Snapdeal, Quikr, Cars24). Recorded so it is not fetched again | 02 |
