# Dossier — uppercase

**Status:** Top 3 — **#3 to produce for** (run 04, 2026-09-21). Score **85/100**. Stage: `SHORTLISTED`.
**Research date:** 2026-09-21. **Researcher:** scheduled D2C prospecting agent (unattended cloud run).

> **What this file is.** The handoff to the eventual production agent. It does **not** choose the
> final ad — the Media Intelligence / Creative Director production process does that later. It
> assembles what is known, separates what was **OBSERVED** from what is **INFERRED**, and marks every
> reference source as *verified-fetched* or *unverified*.

> **Standing hand-check before any spend.** **Meta Ad Library + Instagram check recommended by hand.**
> The Ad Library returned `HTTP 403` on 2026-09-21 as in every run to date, and Instagram
> (`uppercase_ecobags`) cannot be read from an unattended cloud run. **Everything in §5 and §6 about
> what their advertising actually looks like is INFERRED from a trade article that is 20 months old.**
> That is the single largest uncertainty in this dossier.

> **Second hand-check.** Confirm **Ramya Ramachandran** still holds the marketing brief (§14). The
> only source is January 2025.

---

## 1. Brand overview

uppercase is a Made-in-India travel-gear brand — hard and soft trolleys, backpacks, duffles, slings,
messenger bags, laptop sleeves and school bags — built on recycled plastic and GRS certification. It
is operated by **Acefour Accessories Pvt Ltd** and was founded in 2021 by **Sudip Ghose** with Uday
Sodhi, Arnob Mondal, Dheeraj Goyal and Nidhi Rajora.

**Commercial position — FACTS (INFERRED; Entrackr 2026-04-03, Inc42, Indian Retailer, India Retailing):**

| Item | Figure |
|---|---|
| FY25 operating revenue | **₹83 Cr** (+34% on ₹62 Cr FY24) |
| FY25 loss | **₹35 Cr** |
| Most recent round | **₹20 Cr, 3 April 2026** — Accel India and Volrado Venture Partners, ₹10 Cr each |
| Valuation | **₹534 Cr** (~$57 M), **flat** to the August 2024 Series B |
| Total raised | ~$22.1 M over 6 rounds |
| Channel mix | ~60% offline retail / 40% D2C + marketplaces |
| Stated retail plan | 1,800 → **2,500 multi-brand outlets** + **50 standalone stores**; 100 stores by 2027-28 |
| Recognition | **Inc42 FAST42 2026, rank 8**; first Indian luggage brand at New York Fashion Week |

**Read that P&L honestly.** ₹35 Cr of loss on ₹83 Cr of revenue, at a flat valuation, describes a
brand buying growth hard. For us that cuts both ways: it is strong evidence of real, continuing media
spend (and the footprint in §1.1 confirms it), and it is a reason they may be under pressure to
improve creative efficiency — which is the pitch. It is also a reason they could cut.

### 1.1 Ad-spend footprint — **OBSERVED 2026-09-21**

Read first-hand from live page source at `https://uppercase.co.in` (666 KB), browser-header fetch.

| Signal | Value |
|---|---|
| **Meta Pixel** | **`1182483172310307`** — present *both* as a `connect.facebook.net` / `fbq('init', '1182483172310307')` tag **and** in the Shopify web-pixels config |
| **Meta CAPI** | **`facebookCapiEnabled: true`** — server-side conversions on |
| **Google Ads** | **`AW-10955550349`** |
| GA4 / GT | `G-GZDRNZ5CSJ`, `GT-NMCG2PB8` |
| **GTM** | **`GTM-NZH98437`** |
| Commerce platform | **Shopify** (`uppercase-india.myshopify.com`) |
| Other tags | GoKwik + Shopflo checkout, Hotjar, Razorpay |

**Meta Pixel + CAPI + Google Ads together = active paid acquisition, confirmed first-hand.**
Note the GTM container: tags inside it are invisible to this check, so the real stack is **at least**
this, never less.

**YouTube — OBSERVED 2026-09-21:** **no owned channel found.** The site footer links Instagram and
Facebook only, with **no YouTube link at all**; the homepage carries one embedded video
(`youtube.com/embed/2swiWYvxkTo`). The handle `@uppercaseofficial` **was checked and is not them** —
it belongs to a phone-case seller (1 video, 2 views, 3 years old). Logged as an impostor handle.

**Meta Ad Library — attempted 2026-09-21, `HTTP 403`, not renderable from cloud.** Never logged in,
never worked around.

### 1.2 Catalogue scale — **OBSERVED 2026-09-21**

**725 product URLs · 47 collections** — read from `sitemap_products_1.xml` and
`sitemap_collections_1.xml`. **This is the largest catalogue recorded in this workstream** (Mokobara
107, Comet 169, Assembly 338).

The structure is the commercially important part. Products are named
**design line × colour × size × set**:

```
jfk-red-cabin-soft-trolley      topo-blue-medium-soft-trolley     bullet-silver-cabin-trolley
jfk-red-medium-soft-trolley     topo-blue-large-soft-trolley      jfk-duo-white-and-teal-blue-cabin-trolley
jfk-red-large-soft-trolley      topo-black-cabin-trolley          drawstring-lime-green-backpack
jfk-red-set-of-3-s-m-l-soft-trolley                               fantasy-school-backpack-dino
```

Named design lines observed: **JFK · TOPO · BULLET · DRIP · FANTASY · CUBO · FLUX**, plus Eco
Backpack, Eco Duffle, Eco Shoulder Bag and laptop-sleeve ranges.

Collections reveal the campaign calendar: `school-backpack-2026`, `school-backpacks`,
`serendipity-collection`, `2025-wrapped`, `women-s-day`, `shop-gifts-under-1500`, `pro-series`,
`new-arrivals`, `best-seller`, plus a functional merchandising grid (`tsa-lock-trolley-bags`,
`anti-theft-trolley-bags`, `trolley-bags-with-packing-cubes`, `laptop-backpacks`).

---

## 2. Selected product

### **Bullet Silver Cabin Trolley — ₹4,125 (from ₹5,500) — SKU `5600EHT1SLR`**

**OBSERVED 2026-09-21** via the public endpoint
`https://uppercase.co.in/products/bullet-silver-cabin-trolley.json`:

| Field | Value (as the brand publishes it) |
|---|---|
| `title` | Bullet Silver Cabin Trolley |
| `product_type` | Eco Trolley Bags |
| `vendor` | uppercase |
| `variants[0].title` | Silver |
| **`variants[0].price`** | **`4125.00`** |
| **`variants[0].compare_at_price`** | **`5500.00`** |
| `variants[0].sku` | `5600EHT1SLR` |
| `tags` | `Best Selle`[sic] |
| `images` | **7** |
| `created_at` | 2023-11-20 |

**The offer copy is published by the brand.** ₹4,125 and ₹5,500 are read from `price` and
`compare_at_price`, not composed by us. Under Alpha 1 both are set onto the plate **by code**
(exact-text mechanism B), so they are exact by construction.

**Two sibling SKUs for the same treatment, also OBSERVED 2026-09-21:**
`topo-black-cabin-trolley` — ₹3,120 from ₹5,200, SKU `5900EHT1BLK`, 6 images;
`jfk-black-cabin-trolley` — ₹2,700 from ₹4,500, SKU `5100EHT1BLK`, 7 images.

---

## 3. Why this product

1. **It is the brand's own flagged best-seller** (`tags: Best Selle`) at the cabin size, which carries
   the category's highest purchase frequency and the lowest consideration barrier.
2. **Silver hard-shell is the most demanding and most rewarding surface in the catalogue.** Ribbing,
   anodised sheen and specular roll-off are exactly what a still photograph flattens and what
   controlled computed light can make extraordinary. If we want one frame that proves the point, it
   is this one — not a black shell and not a fabric backpack.
3. **No skin, no speech, no claims, no identifiable person.** It sits entirely inside Alpha 1.
4. **The offer is brand-published**, so there is no number to invent and no legal exposure in the copy.
5. It generalises: BULLET exists in multiple colourways and three sizes, so one accepted treatment is
   immediately a system (§15).

---

## 4. Current positioning — in the brand's own words

Quoted verbatim from `https://uppercase.co.in/pages/about-us` (**verified-fetched 2026-09-21**):

> "uppercase, a **design-first and environmentally sensitive brand of Travel Gear** for the young with
> a taste for things that don't just help them look or feel good, but also do good."

> "A backpack is a backpack. Right? Not really. While it would appear so when you see **the sea of
> sameness in the luggage market**, for us travel gear is **fashion that you carry with you**."

> "Not only are our products made from **recycled plastic**, our strict protocols in energy management
> or waste disposal and no use of hazardous chemicals help our products be **GRS-certified**."

Their three stated pillars: **Standout Fashion · Data-driven Functionality · Sustainability.**

**Note that middle quote.** *"The sea of sameness in the luggage market"* is the brand's own framing
of its own category. Any creative territory that makes a single object refuse to be generic is
speaking their language back to them, using their sentence.

---

## 5. Target consumer

**INFERRED** from brand copy and campaign choices: urban Indian 20–35, "the restless young", Gen-Z
skewed, style-led rather than spec-led, sustainability-receptive, price-sensitive at the
₹2,700–₹5,500 cabin band. Purchase occasions are leisure travel, wedding-season travel, and the
school/college backpack cycle (which has its own 2026 collection).

---

## 6. Current creative patterns

**INFERRED — SocialSamosa, published 2025-01-15. This source is 20 months old; treat every line as
requiring the hand-check in the header.**

- Influencer reels and stories built around sustainable-travel destinations (Georgia, Abu Dhabi).
- Creator range from **Jannat (49 M followers)** to **Ashish Bhatia (1 M+)**.
- **Sunburn festival** associate sponsorship, targeting concert-going audiences.
- Targeted placements on **MakeMyTrip, Goibibo and RedBus** — i.e. intent-led travel-context media.
- Positioned as "focused marketing initiatives targeting Gen Z consumers, along with influencer-led
  campaigns".

**OBSERVED 2026-09-21:** no owned YouTube channel; Instagram- and Facebook-first. PDP photography is
clean, well-lit, multi-angle studio work — 6 to 14 images per SKU, plus lifestyle frames.

---

## 7. Brand visual codes — OBSERVED 2026-09-21

- **Wordmark:** lower-case "uppercase" — the name is the joke, and it is always set lower-case.
- **Site accent:** a deep teal, `#0a5b70`, used on the primary checkout button in the live stylesheet.
- **Product colour language:** saturated, named, fashion-forward — Lime Green, Royal Blue, Teal Blue,
  Denim Blue, Maroon, Silver, plus "Duo" two-tone shells (`jfk-duo-white-and-teal-blue`).
- **Shell design:** ribbed hard shells; 8-wheel systems; in-built TSA locks; packing cubes; laundry
  compartments — functional detail is part of the visual story, not hidden.
- **Photography:** studio-clean, high-key, neutral backgrounds, product isolated and multi-angle.

---

## 8. Exact logo / product / reference sources

All URLs below are **public**. Marked *verified-fetched* only where this run actually retrieved them.

| Source | URL | State |
|---|---|---|
| Hero SKU JSON (price, `compare_at_price`, SKU, full image list) | `https://uppercase.co.in/products/bullet-silver-cabin-trolley.json` | **verified-fetched 2026-09-21** |
| Sibling SKU JSON | `https://uppercase.co.in/products/topo-black-cabin-trolley.json` | **verified-fetched 2026-09-21** |
| Sibling SKU JSON | `https://uppercase.co.in/products/jfk-black-cabin-trolley.json` | **verified-fetched 2026-09-21** |
| Product image (JFK Black, clean packshot naming) | `https://cdn.shopify.com/s/files/1/0675/3914/0858/files/5100eht1blk_01.png` | **URL observed in verified-fetched JSON**; image bytes not downloaded |
| Product image (JFK Black, second angle) | `https://cdn.shopify.com/s/files/1/0675/3914/0858/files/5100eht1blk_02.png` | **URL observed in verified-fetched JSON**; image bytes not downloaded |
| Product image (Topo Black) | `https://cdn.shopify.com/s/files/1/0675/3914/0858/files/1_611e30aa-f53e-47b7-9222-bb6e60e575c1.png` | **URL observed in verified-fetched JSON**; image bytes not downloaded |
| Brand copy / positioning | `https://uppercase.co.in/pages/about-us` | **verified-fetched 2026-09-21** |
| Full catalogue | `https://uppercase.co.in/sitemap_products_1.xml` | **verified-fetched 2026-09-21** |
| Collection structure | `https://uppercase.co.in/sitemap_collections_1.xml` | **verified-fetched 2026-09-21** |
| New-arrivals feed | `https://uppercase.co.in/collections/new-arrivals/products.json` | **verified-fetched 2026-09-21** |
| Official Instagram | `https://www.instagram.com/uppercase_ecobags/` | **unverified** — link read from site footer; page not fetched |
| Official Facebook | `https://www.facebook.com/uppercase.ecobags/` | **unverified** — link read from site footer; page not fetched |
| Company LinkedIn | `https://www.linkedin.com/company/acefour-accessories-pvt-ltd` | **unverified** — from search results |
| Homepage embedded video | `https://www.youtube.com/embed/2swiWYvxkTo` | **unverified** — embed URL observed in page source; video not watched |

**There is no owned YouTube channel to cite.** `@uppercaseofficial` is **not** uppercase.

---

## 9. Claims we can safely make — from public brand copy

Each of these is the brand's own published wording or a direct restatement of it
(`/pages/about-us`, verified-fetched 2026-09-21), or a value read from their own product JSON:

- Made from **recycled plastic**; **GRS-certified**.
- **100% Made in India.**
- **Design-first and environmentally sensitive travel gear.**
- Product features the brand itself lists: **8-wheel system, in-built TSA lock, packing cubes,
  2000-day international warranty**.
- The exact price and the exact struck-through price: **₹4,125** and **₹5,500** — because they are
  `price` and `compare_at_price` on the brand's own endpoint.
- The product name, colour name and SKU exactly as published.

---

## 10. Claims we should NOT infer

- **Nothing about efficacy, durability testing, or drop/crush performance** beyond the warranty the
  brand itself states. Do not stage a destruction test; Samsonite and Urban Jungle own that territory
  and it invites a claim we cannot substantiate.
- **No recycled-content percentage, no carbon or landfill figure, no "X bottles per bag".** They are
  not published on the pages fetched.
- **No market-share, rank or "India's No. 1" claim.** FAST42 rank 8 is Inc42's ranking, not a
  consumer claim, and must not be presented as one.
- **No revenue, funding or valuation figure in creative.** Those are commercial context for us, not
  ad copy.
- **Nothing about a person.** No creator likeness, no borrowed influencer, no Sunburn or
  MakeMyTrip/Goibibo/RedBus co-branding — those are their partners, not ours to depict.
- **Do not name or show a competitor**, and do not lean on their own "sea of sameness" line in a way
  that disparages a named rival.
- **No stock availability claim.** The public `/products/*.json` endpoint carries **no `available`
  field**, so stock cannot be confirmed from it.

---

## 11. Creative whitespace

Three things are true at once, all from evidence:

1. **uppercase has no owned video channel.** (OBSERVED 2026-09-21.)
2. **A direct competitor already proves the category rewards computed imagery.** Bagline is described
   running **CGI, AR and VR content on Instagram and YouTube** in the same season
   (INFERRED — SocialSamosa 2025-01-15), and Bagline's own paid stack is verified
   (Pixel `777305122865335` CAPI-on, `AW-11098568520`, OBSERVED 2026-09-21).
3. **uppercase's current creative is people-led** — creators, destinations, festival sponsorship —
   while the product itself, which is genuinely well designed, is largely carried by static studio
   photography.

So the opening is a **format** gap sitting next to a **competitor proof point**. It requires no
criticism of uppercase's photography, which is good. The sentence to a buyer is roughly: *your
category has already shown computed product imagery works, your competitor is using it, and you have
725 SKUs that each need assets.*

**And the honest counterweight:** their "why now" is the weakest of the Top 3. The funding is from
April, the newest item in `new-arrivals` is **May 2026** (the `Cubo` and `Flux` slings — the 2026
daily-carry diversification, which did ship). This is a **standing** need, not a this-week event.
That is precisely why uppercase ranks #3 and not #2.

---

## 12. Creative territories (high-level — production chooses the final ad)

Offered as directions, not scripts. **None of them requires a person, speech, or generated in-scene text.**

**A. "The sea of sameness."** Their own sentence, made literal and then broken. A field of
identical, anonymous, colourless cabin shells; one Bullet Silver resolves out of it — catching a
light none of the others catch. Product-led, no people, no comparison to a named brand. The copy
block (₹4,125 from ₹5,500) composes on at the end by code.

**B. "Fashion that you carry with you."** Also their line. Treat the silver shell as a material
study rather than a suitcase: extreme-macro travel across ribbing, hinge, wheel housing and TSA lock,
lit like a product of industrial design rather than luggage, then pulling back to the whole object in
one continuous move. Sells the design-first pillar with zero claims.

**C. "Made of what came before."** The recycled-plastic story told through material and light only —
the shell reading as something with a history rather than a finish — without a single sustainability
number on screen, because we have none we can substantiate. Highest risk of drifting into a claim;
the guardrail is that nothing quantitative ever appears.

All three are **one static hero + one short silent motion version derived from the accepted still**,
which is exactly the Alpha-1 shape.

---

## 13. AI production risks

| Risk | Severity | Note |
|---|---|---|
| **Wheel and telescopic-handle micro-geometry** | **High** | This is where hard-luggage fidelity fails first. Framing that keeps the wheel housing at macro scale or out of frame is safer than a full three-quarter hero |
| **The embossed `uppercase` wordmark on the shell** | **High** | Must be **overlay-composed or supplied reference** — never generated in-scene. Generated in-scene exact text is excluded from Alpha 1 by ruling C-7 |
| **Silver specular behaviour** | Medium | The reason to pick this SKU is also the reason it is hard: anodised silver is unforgiving, and a wrong roll-off reads as plastic |
| **Colour fidelity across a colourway system** | Medium | If one accepted treatment is to generalise to 11 colourways (§15), the colour must be reproducible, not re-invented per run |
| **Ribbing moiré in motion** | Medium | Fine parallel ribbing plus a moving camera is an aliasing hazard in the derived motion version |
| Drift into a sustainability claim | Medium | Guardrail in §10: nothing quantitative, ever |
| Identifiable person | **None** | No person is in any territory in §12 — the consent gate is not engaged |

**Standing dependency, not specific to uppercase.** The runtime has never called a provider. Every
run to date is dry, `spend_authority.status: none` on every profile, and live transport is
deliberately unwired. This workstream can select a brand; it cannot unblock production. See
`coordination/CONTROL-STATE.md` §9.

---

## 14. Likely decision maker

### **Sudip Ghose — Founder & Managing Director**
Publicly identified on the brand's own About page, and press-active (Inc42, Indian Retailer,
ImagesBoF interviews). Described there as "one of the most respected names in the travel gear
industry". He is the person who decides whether a design-first brand buys design-first creative.
**Confidence: HIGH** (named on the brand's own site, verified-fetched 2026-09-21).

### **Ramya Ramachandran — Head of Marketing**
Quoted as uppercase's Head of Marketing in SocialSamosa, **2025-01-15**.
**Confidence: LOW — the source is 20 months old and the role has not been re-verified.**
**Do not address anything to this name until it is confirmed by hand.**

### Also named publicly as co-founders
Uday Sodhi, Arnob Mondal, Dheeraj Goyal, Nidhi Rajora (INFERRED — Indian Retailer/Inc42).

**Contact route — public only.** Company LinkedIn (`linkedin.com/company/acefour-accessories-pvt-ltd`,
operating entity **Acefour Accessories Pvt Ltd**) and the public contact page on `uppercase.co.in`.
**No personal phone number or private email has been sourced, and none should be.** No contact has
been made and none is authorised from this workstream.

---

## 15. Recurring commercial opportunity

**725 products in a line × colour × size matrix is a production-system problem, not a one-film problem.**
That is the whole commercial argument here, and it is stronger than for any other brand in the pipeline.

A plausible shape, to be tested rather than asserted:

- **2 hero treatments per design line per quarter** across JFK, TOPO, BULLET, DRIP, FANTASY, CUBO,
  FLUX — a line-level visual language that then propagates.
- **12–20 colourway cutdowns per month**, since each colour is already its own product with its own
  PDP and its own paid-social need.
- **Seasonal spikes** the collection structure already proves exist: `school-backpack-2026`, festive
  and wedding travel, `shop-gifts-under-1500`, `women-s-day`, a year-end `wrapped`.
- **Offline support.** With 60% of revenue offline and 1,800 → 2,500 MBOs plus 50 standalone stores
  planned, the same assets have an in-store and trade life beyond Meta.

### The category argument — the reason this dossier matters beyond uppercase

**Three of the four leading premium Indian D2C travel-goods brands — Mokobara, Comet and uppercase —
have no owned video channel at all** (each verified first-hand on 2026-09-21), and the fourth
(Assembly) posts explainers reaching 36–73 views. All of them run verified Meta + Google paid stacks.
All of them sell rigid, colourway-driven, claim-free, human-free objects — the best-matched subject
found to the frozen Alpha-1 family.

**One exceptional luggage product film is therefore not a single-prospect asset.** Mokobara,
uppercase, Assembly, Arista Vault, Nasher Miles and Bagline are all live, all buying media, all
reachable. The marginal cost of the second approach in this category is close to zero.

---

## 16. Source links

**Primary — verified-fetched 2026-09-21**
- `https://uppercase.co.in/` — homepage source, ad-spend footprint
- `https://uppercase.co.in/pages/about-us` — positioning and brand copy, §4 and §9
- `https://uppercase.co.in/products/bullet-silver-cabin-trolley.json` — hero SKU
- `https://uppercase.co.in/products/topo-black-cabin-trolley.json`, `.../jfk-black-cabin-trolley.json`
- `https://uppercase.co.in/sitemap_products_1.xml`, `.../sitemap_collections_1.xml`
- `https://uppercase.co.in/collections/new-arrivals/products.json`
- `https://www.youtube.com/@uppercaseofficial/videos` — checked, **not uppercase**
- `https://www.facebook.com/ads/library/?...&q=uppercase` — **`HTTP 403`, not renderable from cloud**

**Secondary — INFERRED, with dates**
- Entrackr, **2026-04-03** — ₹20 Cr round, ₹534 Cr flat valuation, FY25 ₹83 Cr / ₹35 Cr loss:
  `https://entrackr.com/exclusive/exclusive-uppercase-raises-fresh-capital-from-existing-investors-11449759`
- SocialSamosa, **2025-01-15** — luggage-category creative read, uppercase influencer strategy,
  Bagline CGI/AR/VR, Ramya Ramachandran:
  `https://www.socialsamosa.com/experts-speak/luggage-brands-packing-pop-culture-innovation-india-travel-season-8623495`
- Inc42 FAST42 2026 (rank 8):
  `https://inc42.com/startups/fast42-2026-announcing-the-ranking-of-indias-fastest-growing-d2c-brands/`
- Inc42 — recycled-plastic profile:
  `https://inc42.com/startups/how-this-sustainable-luggage-brand-is-transforming-recycled-plastic-into-coveted-travel-gear/`
- Indian Retailer — ₹511 Cr valuation interview, $9 M Series B, D2C 100 profile, 2026 roadmap

---

## 17. Research date

**2026-09-21** (run 04). All `OBSERVED` items were fetched on this date. All `INFERRED` items carry
their own source date above; the oldest and most load-bearing is the **2025-01-15** SocialSamosa
creative read, which is the reason §6 and §11 carry an explicit hand-check warning.

**Score at this date: 85/100.** Full criterion-by-criterion breakdown in
`runs/2026-09-21.md` §6.1.
