# D2C prospect pipeline — durable source of truth

**Created:** 2026-09-14 (first run). **Last updated:** 2026-09-14.
One row per brand. See `README.md` for the rules this file is maintained under.

**Stage values:** `DISCOVERED` · `SHORTLISTED` · `SELECTED_FOR_SPEC` · `IN_PRODUCTION` · `SEND` ·
`PORTFOLIO_ONLY` · `DISCARD` · `CONTACTED` · `REPLIED` · `CALL` · `PAID_PILOT` · `PAID_RECURRING` ·
`NO_RESPONSE` · `NOT_NOW`.

**Stages from `CONTACTED` onward are set by the Controller only.** The prospecting agent never sets
them and never downgrades a later-stage row; the most advanced legitimate status wins unless explicit
new evidence requires a downgrade, which must be stated in the run file.

**Evidence caveat on every row below:** all of it is `INFERRED (search-summary)` gathered 2026-09-14.
This session's egress policy blocked every external host, so **no page was fetched and seen** — see
`runs/2026-09-14.md` §0. Hand-verify before spending.

## Active shortlist (score ≥ 70)

| Brand | Category | Product | Score | Why now | Creative opening | Stage | Last researched | Next action | Dossier | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| **Salty** | Fashion accessories / jewellery | The **Salty Bags** launch range (new vertical) | 88 | ₹30.1 Cr Series A (Jan 2026) funding an expansion into watches, sunglasses, scarves, belts, bag charms + a new bags vertical + a flagship store | Majority of budget is performance marketing on micro-creator and offer-led creative; hard-surface accessories are the best physical fit for a code-overlay static hero + short silent motion | SHORTLISTED | 2026-09-14 | Hand-check Meta Ad Library + Instagram; confirm Salty Bags has actually launched; then Controller decides spend | `dossiers/salty.md` | **Top 3 — #1 to produce for.** ₹4–4.5 Cr/month revenue; 30% of revenue via quick commerce (Blinkit key) |
| **Typsy Beauty** | Colour cosmetics + fragrance | A **Spritz by Typsy** fragrance SKU | 84 | ₹20 Cr led by Saama announced **6 Aug 2026**; 10+ new products stated as imminent; simultaneous quick-commerce and offline push | 27 SKUs at ₹600–900 premium; founder-led/BTS organic content implies little premium product-led motion; every launch needs offer creative for Blinkit/Zepto/Nykaa/Amazon | SHORTLISTED | 2026-09-14 | Hand-check Meta Ad Library + Instagram; confirm which Spritz SKU is current hero | `dossiers/typsy-beauty.md` | **Top 3 — #2.** Freshest trigger in the run. Fragrance bottles are the lowest-fidelity-risk product here |
| **Farmley** | Healthy snacking (makhana, dates) | Flavoured **Makhana** lead SKU | 84 | FY26 growth target of 60–70% on ₹370 Cr FY25 + first EBITDA profitability; expansion into healthy desserts and on-the-go snacks; rural offline push | Reported near-100% digital media spend and quick-commerce-led growth ⇒ very high creative throughput; pack-led hero + price overlay is exactly our shape | DISCOVERED | 2026-09-14 | Controller call: highest value if converted, slowest to answer. Swap into Top 3 if optimising for contract size | — | **Highest ability to pay in the run** and best fit to the Controller's FMCG advantage. Funding trigger is stale (May 2025) |
| **AntiNorm** | Multitasking beauty / personal care | The **all-in-one hair cream** | 79 | ₹28 Cr seed led by Fireside (Jan 2026); **up to 7 new products over the coming year**; hiring across growth and R&D | Founded 2024 with only 3 SKUs — the brand's visual language is still forming, so the whitespace is genuine rather than inferred | SHORTLISTED | 2026-09-14 | Hand-check current creative; confirm SKU count and any new launch since Jan | `dossiers/antinorm.md` | **Top 3 — #3.** Best reachability in the run (single identifiable founder, no incumbent creative partner) |
| **Foxtale** | Skincare | TBD — hero SKU to be confirmed | 78 | ₹199 Cr FY25 (2.4× YoY); losses widened specifically on an aggressive marketing push; targeting ₹400–450 Cr gross | Enormous creative throughput implied by the marketing spend | DISCOVERED | 2026-09-14 | Revisit next run; identify a single hero SKU | — | Marked down on AI fit: skincare creative leans on efficacy claims and derm/UGC talking heads, which C-7 excludes. Founder Romita Mazumdar unusually visible |
| **Insight Cosmetics** | Mass colour cosmetics | TBD | 71 | 16 → **60 exclusive brand outlets by end-2026** (~45 new, metros + Tier 2/3) | Large SKU range across a 35,000-store footprint | DISCOVERED | 2026-09-14 | Retain; re-screen for performance-marketing evidence next run | — | Trigger is retail expansion, not media spend. Mass-cosmetics shade fidelity is a real generation risk |
| **Nothing But** | Freeze-dried fruit snacks | Freeze-dried fruit pack | 71 | Seed round from an operator-heavy cap table (Noise, Innovist, Arata, DailyObjects, The Be Life); quick-commerce and NPD expansion | **Highest AI creative potential in the run (17/20)** — freeze-dried fruit is visually striking and needs no human performance | DISCOVERED | 2026-09-14 | Watch for a priced round, then re-score | — | Held back only by ability to pay (5/10). Upgrade trigger: any institutional round |

## Watchlist (60–69 — not for spend)

| Brand | Category | Product | Score | Why now | Creative opening | Stage | Last researched | Next action | Dossier | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| Indian Snack House | South Indian snacks & sweets | Clean-label snack range | 64 | ₹2.2 Cr pre-seed led by Titan Capital; expanding cities and online platforms | Photogenic regional-sweets category with no established ad language | DISCOVERED | 2026-09-14 | Re-check in ~2 quarters | — | Reachable and appealing; no credible recurring creative budget yet |
| MetaMan | Men's jewellery + fragrance | — | 63 | Perfume-range expansion; ~$1.22M raised | — | DISCARD | 2026-09-14 | None | — | **Negative filter:** core creative depends on celebrity likeness (Suniel Shetty; KL Rahul a co-founder). Unusable by us |
| Sid's Farm | Premium dairy | Milk / dairy range | 61 | **₹81 Cr pre-Series B, July 2026** (Omnivore, Dodla Dairy, NSFO) — a genuinely fresh trigger | Weak: subscription dairy, low SKU variety, low refresh need | DISCOVERED | 2026-09-14 | Re-check if it launches a value-added range | — | Core claim (safety; 10,000 tests/day) needs process footage we cannot generate |

## Rejected this run (not scored, or filtered on principle)

| Brand | Reason |
|---|---|
| Bonhomia / Indulge Beverages | Only funding evidence found dates to **2016**; current activity could not be established. Rejected on stale evidence, not merit |
| Beast Life | Creator-led — the core creative *is* the founder's face (Gaurav Taneja). Worst possible fit for the Alpha-1 family |
| Phitku | Campaign is celebrity/film-IP-led (Mirzapur partnership, Sept 2026) |
| Cosmix | Acquired by Marico — now inside a conglomerate; slow procurement |
| Waggies (Reliance) · HappyFur (Wipro) · Ninja (Godrej) | Conglomerate-owned; unsolicited spec work disappears into procurement |
| Country Delight · The Label Life · Built · Moe Puppy · Heads Up For Tails · Blue Tokai · Rage Coffee | Dropped at quick-screen — no current trigger, subscription-utility creative, celebrity-curator model, too small, or likely mature in-house/agency creative |
| The Whole Truth · Moxie · Sleepy Owl · SBOOCH | Deprioritised at quick-screen, worth revisiting — see `runs/2026-09-14.md` §4 |
| "Get Daily" | Could not be corroborated at all beyond a single unverifiable mention. Not carried |
