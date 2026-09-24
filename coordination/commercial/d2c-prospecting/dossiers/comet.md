# Dossier — Comet

**Research date:** 2026-09-17 · **updated 2026-09-21 (run 04)** · **re-verified 2026-09-24 (run 05)**
**Run:** `runs/2026-09-17.md`, updated by `runs/2026-09-21.md`, re-verified by `runs/2026-09-24.md`

> ### Run 05 update (2026-09-24) — no change; score held at 87
>
> - **Footprint re-OBSERVED 2026-09-24, unchanged:** Pixel `663517755793437` **CAPI-on**,
>   `AW-11256510101`, `G-7VX8KTRTYC`, `GT-KFTM99T`, Shopify, Judge.me, Razorpay.
>   **Still no GTM — the page source shows the whole picture.**
> - **YouTube `@wearcomet` re-confirmed ZERO uploads, 2026-09-24.**
> - **`Astra` independently corroborated:** LocalSamosa's third-week-of-September 2026 roundup lists
>   *"Comet — Astra Women's Sneaker inspired by ballet aesthetics"* (INFERRED), matching run 04's
>   primary-evidence finding from the storefront.
> - The `new-arrivals` collection handle returned no JSON this run — **a handle difference, not a signal.**
> - **The Instagram hand-check remains the open question** and is unchanged as the next action.
**Pipeline score:** **87/100** (was 84 — +3 on new primary evidence, run 04)
**Top-3 rank:** **#2**
**Stage:** `SHORTLISTED`

> **⚠ UPDATED 2026-09-21 — the selected product has changed.** Comet published **`Astra`**, their
> first women's-only silhouette, on **2026-09-09** — eight colourways, ₹4,899. It is twelve days old
> and it is the freshest trigger in the pipeline. **§2 now selects Astra; the previous `X Lows`
> selection is preserved below it as §2a for reference.** Two further additions this run: §5a records
> the first real read we have of Comet's creative language (the `Maachis` campaign), and §1 records
> the re-verified catalogue figures.

> **What this document is.** The handoff to the eventual production agent. It assembles what is known,
> separates what was seen from what was read, and marks what must not be assumed.
> **It does not choose the final ad.**

> **⚠ Before any spend: Meta Ad Library + Instagram check recommended by hand.**
> Ad Library returned **HTTP 403** on 2026-09-17; Instagram does not render unauthenticated.
> **We have never seen Comet's paid creative** — and with a reported 500,000+ Instagram following,
> the Instagram check matters more here than for any other Top-3 brand.

> **⚠ Domain warning — read before fetching anything.**
> **`cometshoes.com` is NOT Comet's store.** It is Cloudflare-walled and its `/sitemap.xml` returns a
> hand-written 404 page, not a Shopify sitemap. **The real storefront is `https://wearcomet.com/`**,
> confirmed by `Shopify.shop` in source and by `x-lows-*` product handles matching their published
> product names. Likewise on YouTube: **`@cometshoes` is not the brand** (its own description reads
> *"Only for college assignment purpose"*) and neither is `@cometofficial` (an unrelated personal
> channel). The brand channel is **`@wearcomet`**, carrying their registered tagline
> *"Never Shy, Never Sorry"*. Three wrong identifications were caught during this research; do not
> repeat them.

---

## 1. Brand overview

Comet is an Indian D2C sneaker and slides brand founded in **2023** by **Utkarsh Gupta** and
**Dishant Daryani**, headquartered in Bengaluru. It sells primarily through its own site, increasingly
through its own stores, and is built around **named collaboration drops** rather than a standing
seasonal range.

**Commercial position (INFERRED — press, fetched 2026-09-17):**

| | |
|---|---|
| Latest round | **₹100 Cr (~$10.5 Mn) Series B**, September 2026, **led by Verlinvest** |
| Participating | Elevation Capital and Nexus Venture Partners (both doubling down); angels incl. Abhiraj Singh Bhal (Urban Company), Ajit Mohan (Snap Inc.), Anand Ahuja (Bhaane / VegNonVeg) |
| Reported terms | ~**3.2× valuation premium** |
| FY25 revenue | **₹29 Cr**, roughly 4× year on year; loss ₹4.39 Cr. FY26 not yet filed |
| Reported growth | **9× revenue since the 2024 Series A**; **₹4–5 Cr monthly sales** |
| Retail | **10 stores** as of September 2026 → target **20 by FY27** |
| Prior round | ₹42.3 Cr Series A led by Elevation Capital, 2024 |
| Social | **500,000+ Instagram followers** |
| Stated use of funds | Retail expansion, product portfolio, and **proprietary sole designs and tooling** |

**Catalogue (OBSERVED 2026-09-17):** **194 product URLs** — a large number for a sneaker brand, and
the reason is structural: **each colourway ships as its own product page** (`x-lows-light`,
`x-lows-beach`, `x-lows-sky`, `x-lows-pinecone`, `x-lows-tiramisu`, `x-lows-lagoon`). Collections
include `/drops`, `/multi-color-collection`, `/all-white-collection`, `/members-club-collection`,
`/cred-comet`, plus per-drop collections (`/mirage`, `/icegola`, `/crater-exclusive`, `/pumpkin`,
`/blue-jay`, `/swatch-ludo`).

**Ad-spend footprint (OBSERVED 2026-09-17, from raw page source):**
Meta Pixel **`663517755793437`** (Shopify web-pixels id `2004779315`) with
**`facebookCapiEnabled: true`** · Google Ads **`AW-11256510101`** · GA4 `G-7VX8KTRTYC` · `GT-KFTM99T` ·
platform **Shopify** · Judge.me, Razorpay, Microsoft Clarity.
**No GTM container** — which is unusually *useful* evidence: with no container to hide tags inside,
what appears in source is the complete picture, and it shows Meta with server-side CAPI **and** Google
Ads both active.

### 1a. Re-verified 2026-09-21 (run 04)

**Catalogue — OBSERVED 2026-09-21:** **169 product URLs** (run 03 recorded 194 — the count *fell*, as
drop colourways sell through and are retired) and **389 collections**, the highest collection count
of any brand in the pipeline. Sitemaps resolve on **`www.wearcomet.com`**.

**YouTube — re-OBSERVED 2026-09-21:** `@wearcomet` still returns `channelOwnerEmptyStateRenderer`,
i.e. **zero uploads**. Unchanged from run 03, now confirmed twice.

**Meta Ad Library — attempted 2026-09-21: `HTTP 403`.** Still never rendered, in any run.

---

## 2. Selected product — **UPDATED 2026-09-21**

### **Astra — ₹4,899 — pitched as the eight-colourway launch system**

`https://www.wearcomet.com/products/astra-pink-butter` and seven siblings.

**OBSERVED 2026-09-21** from the public `/products/<handle>.json` endpoints:

| Handle | Variant colour name | `price` | `compare_at_price` | Images |
|---|---|---|---|---|
| `astra-pink-butter` | Astra Multi Beige | **`4899.00`** | **empty — none** | 9 |
| `astra-chrome-kiss` | Astra Silver White | `4899.00` | empty | 8 |
| `astra-matcha-cream` | Astra Green Cream | `4899.00` | empty | 8 |
| `astra-wild-bloom` | — | `4899.00` | empty | — |
| `astra-vanilla-cloud` | — | `4899.00` | empty | — |
| `astra-day-dream` | — | `4899.00` | empty | — |
| `astra-burnt-toast` | — | `4899.00` | empty | — |
| `astra-wild-poppy` | — | `4899.00` | empty | — |

`vendor: wearcomet` · `product_type: Astra` · sizes 3/4/5+ ·
**`created_at: 2026-09-02` · `published_at: 2026-09-09`**

**Note the count.** Trade press (LocalSamosa, third week September 2026) reported **seven**
colourways. The store shows **eight**. Primary evidence governs — but do not repeat the press number.

**What it is (INFERRED — LocalSamosa, Sept 2026):** Comet's first sneaker silhouette designed
exclusively for women. Ballet-inspired, low-profile, with transparent mesh detailing, double lacing
and a mix of materials.

**Why this product rather than X Lows.**

1. **It is twelve days old.** A brand-new silhouette in a brand-new customer segment is the moment a
   brand is most short of creative and most willing to look at someone else's.
2. **It ships as a system, not a shoe.** Eight colourways published simultaneously is the
   re-render-per-colourway argument made for us, by them, on day one.
3. **It is a segment entry, not a restock.** Launching women's-only footwear means new audiences, new
   placements and new creative — not a refresh of existing assets.
4. **The colour names are already the creative brief.** *Pink Butter · Chrome Kiss · Matcha Cream ·
   Wild Bloom · Vanilla Cloud · Day Dream · Burnt Toast · Wild Poppy* — food-and-flora naming that
   hands a treatment its palette and its mood without us inventing a thing.

**The same honest constraint as before, re-verified.** **No Astra SKU carries a
`compare_at_price`.** There is no brand-supplied discount to overlay. Deterministic copy is limited
to the product name, the colourway name and **₹4,899**. **We invent no offer and imply no discount.**

**Asset availability:** 8–9 public images per colourway, i.e. **roughly 68 public reference images
across the line** — ample for reference-led work.

---

## 2a. Previous selection (run 03) — retained for reference

### **X Lows — ₹4,299 — pitched as the colourway system, led by `X Lows LIGHT`**

`https://www.wearcomet.com/products/x-lows-light` · handle `x-lows-light`

**OBSERVED 2026-09-17** from the public `/products/x-lows-light.json`:

| Field | Value |
|---|---|
| Title | X Lows LIGHT |
| Product type | X Lows |
| Vendor | wearcomet |
| Options | `Color` × 1 (*Lows White*), `Size` × **10** |
| `price` | **`4299.00`** |
| `compare_at_price` | **empty — none** |
| Public images | **9** |
| `published_at` | 2023-06-01 |
| `updated_at` | **2026-09-16** (the day before this run) |

**Why this product.** X Lows is the spine of the catalogue, and its sibling products —
`x-lows-beach`, `x-lows-sky`, `x-lows-pinecone`, `x-lows-tiramisu`, `x-lows-lagoon` — are the same
silhouette in different colourways, each as a separate product page. **That architecture is the
pitch**: every new colourway is a new page and a new creative requirement, permanently. A single
composition that re-renders per colourway maps onto their catalogue one to one.

**An honest constraint, stated up front.** X Lows carries **no `compare_at_price`**. Unlike Mokobara
there is **no brand-supplied discount to overlay**. The deterministic copy is therefore limited to the
product name and the ₹4,299 price — or to values the brand supplies directly. **We invent no offer and
imply no discount.** If offer-led copy is wanted, it must come from Comet.

**The `/drops` alternative.** The drops collection lists named releases at ₹5,299–₹6,499 — *UNO x
COMET · MAACHIS · ORANGE · COMET x FARAK "AASMAAN" · COMET x ODDNOTEVEN · COMET x NARU · COMET x
VERONICA'S · RADIOACTIVE · FUT SHIK UP · X Lows "MONOPOLY" Standard Edition · DECIBEL · "Extra
Toppings Only"* — with at least one further page. A drop is the more exciting creative object, but a
**collaboration** drop carries a third party's IP. **Prefer a Comet-owned colourway for spec work**;
do not build a spec ad on a named partner's collaboration.

---

## 3. Current positioning

**Registered tagline (OBSERVED 2026-09-17, from the brand's YouTube channel title):**
**"Never Shy, Never Sorry"**

**Founder-stated strategy (INFERRED — Inc42, Storyboard18, founder interviews, fetched 2026-09-17).**
Utkarsh Gupta, quoted:

> *"No one is telling stories through sneakers in India. Most brands rely on celebrities and
> traditional marketing, but we didn't have the budget for that. What we did have is a deep
> understanding of emotions and culture."*

> *"the naming, the packaging, the scarcity, the UGC, the way people naturally want to show it off,
> everything works together"* — *"when the product has a story, the packaging becomes content."*

This is a brand that has **publicly and deliberately staked itself on story over celebrity**, and has
said plainly that the reason was budget. Both halves of that matter commercially: the philosophy
aligns with product-led creative, and the cost constraint is the thing we can move.

**The drop names are the positioning made literal (OBSERVED):** *MAACHIS · RADIOACTIVE · DECIBEL ·
FUT SHIK UP · "Extra Toppings Only" · MONOPOLY · AASMAAN*. These are concepts, not SKU codes.

---

## 4. Target consumer

**ESTIMATE, from price points, catalogue structure and social scale (OBSERVED/INFERRED):**

Young urban Indian consumers, roughly 18–30, buying sneakers as cultural signal rather than
performance footwear. At ₹4,299–₹6,499 the brand sits above mass Indian footwear and well below
international sneaker-culture pricing — accessible aspiration. The `/members-club-collection` and
`/cred-comet` collections imply a loyalty/partnership layer and a consumer who opts in to the brand
rather than merely buying from it. A reported 500,000+ Instagram following against ₹29 Cr of FY25
revenue indicates an audience substantially larger than the customer base — a community brand.

Men's and women's ranges both exist (`/men-sneakers`, `/women-sneakers`).

---

## 5. Current creative patterns

**What was OBSERVED, 2026-09-17:**

- **The official YouTube channel has zero videos.** `youtube.com/@wearcomet`, channel title
  "Comet (Never Shy, Never Sorry)". The Videos tab returns `channelOwnerEmptyStateRenderer` — an
  empty state. The channel exists and is branded; nothing has been published.
- **Concept-led naming across the catalogue** — 12+ named drops on page one of `/drops` alone.
- **Modest per-SKU photography** — 9 images on `x-lows-light`, against Mokobara's 35–96. Their asset
  investment is visibly lighter.

**What was NOT observed — and must not be assumed:**

- **Their Meta creative** (Ad Library 403) and **their Instagram output** (no unauthenticated render).
  Given a 500k+ following that is described in press as central to the brand, **the Instagram gap in
  our knowledge is significant.** Their primary creative engine is very likely there, and we have not
  seen it.

**The legitimate inference, and the illegitimate one.**

*Legitimate:* Comet does not maintain a public video library on YouTube.

*Not legitimate:* "Comet has no video creative." Press describes UGC as a core part of their model,
which implies substantial video activity on Instagram. **Do not design against, or write, a claim that
they lack video.** Treat the YouTube absence as exactly what it is.

---

## 5a. Comet's creative language — the first real read we have (**NEW 2026-09-21**)

Run 03 recorded that *"their Meta creative has never been seen"*. The Instagram hand-check is still
outstanding, but a trade writeup now gives a genuine read of how this brand thinks about marketing.

**INFERRED — medianews4u, published 2026-06-24, on the `Maachis` campaign:**

- The campaign is built entirely on **a product detail as the story**: a functional match-striker
  strip concealed beneath the sneaker's heel tab.
- Design language: beige suede with bold red detailing, drawn from **vintage Indian matchbox
  graphics**; shipped in a **life-sized matchbox** with butter paper and retro graphics.
- Co-founder **Utkarsh Gupta**, quoted: *"Every detail, from the vintage-inspired graphics to the
  life-sized matchbox packaging and the functional striker strip, was designed to create moments of
  discovery."*

**Why this matters more than it looks.** It de-risks the pitch substantially. It says Comet already
builds marketing on **product-design discovery — no celebrity, no talking head, no borrowed fame**.
That is precisely the shape of the frozen Alpha-1 family. We are not asking them to change what they
believe about advertising; we are offering to execute the thing they already believe at a cadence and
cost-per-asset they currently cannot reach with zero owned video.

**Use it carefully.** This is a single trade article, not their ad account. It describes one campaign
from June 2026. It is **not** evidence about what is running on Meta today — that remains unseen and
is the reason the Instagram hand-check is still the first action on this brand.

---

## 6. Current ad examples

**None available.** No Comet advertisement was seen by this agent.

- Meta Ad Library: `…&country=IN&q=Comet shoes` → **HTTP 403, not renderable from cloud** (2026-09-17).
  No login attempted.
- Instagram: not renderable unauthenticated.
- YouTube: **zero uploads** (OBSERVED).

**Deliberately empty rather than filled with inference.** Ask the Controller for the hand-check output
before finalising a creative direction — and here, prioritise **Instagram** over the Ad Library.

---

## 7. Brand visual codes

**OBSERVED:**

- **Naming is the loudest visual code.** Products are named as concepts — *MAACHIS, RADIOACTIVE,
  DECIBEL, ORANGE, FUT SHIK UP, "Extra Toppings Only"* — and the collection structure treats colour as
  the organising idea (`/multi-color-collection`, `/all-white-collection`, `/aeon-multicolor`,
  `/icegola-multicolor-swatch`, `/crater-multicolor`).
- **Product families** are named: *X Lows · Aeons · Aeon V2 · Crater · Mirage · Icegola*.
- **Tone** is declarative and a little defiant — *"Never Shy, Never Sorry"*.
- **Packaging is treated as content** by the brand's own account (*"when the product has a story, the
  packaging becomes content"*), which means the box is a legitimate creative subject, not an
  afterthought.

**NOT established:** brand hex values, typefaces, logo lockup rules, photography conventions.
**Sample these from the actual assets in §8 before production; do not guess.**

---

## 8. Exact logo / product / reference sources

All URLs public, no authentication required.

| Asset | URL | Status |
|---|---|---|
| X Lows LIGHT — full product record, 9 images, 10 sizes, ₹4,299 | `https://www.wearcomet.com/products/x-lows-light.json` | **verified-fetched 2026-09-17** |
| First product image (pattern for the rest) | `https://cdn.shopify.com/s/files/1/0738/5559/8899/files/lateral_3_-min_1.jpg` | **verified-fetched 2026-09-17** (URL returned in the JSON) |
| Shopify CDN asset root | `https://cdn.shopify.com/s/files/1/0738/5559/8899/` | **verified** — store id confirmed from fetched image URLs |
| Full product index (194 URLs) | `https://www.wearcomet.com/sitemap_products_1.xml?from=8314222969139&to=10455546200371` | **verified-fetched 2026-09-17** |
| Collection index | `https://www.wearcomet.com/sitemap_collections_1.xml?from=439577936179&to=511837634867` | **verified-fetched 2026-09-17** |
| Drops collection — 12 named drops with prices | `https://www.wearcomet.com/collections/drops` | **verified-fetched 2026-09-17** |
| Homepage (footprint source) | `https://wearcomet.com/` | **verified-fetched 2026-09-17** |
| Official YouTube channel | `https://www.youtube.com/@wearcomet/videos` | **verified-fetched 2026-09-17** — empty |
| Sibling colourway records (`x-lows-beach`, `-sky`, `-pinecone`, `-tiramisu`, `-lagoon`) | `https://www.wearcomet.com/products/<handle>.json` | **unverified — handles confirmed from the sitemap, records not individually fetched** |
| **Logo / wordmark source file** | — | **UNVERIFIED — not located.** Source before production; do **not** generate the wordmark |
| Instagram | `https://www.instagram.com/wearcomet/` | **UNVERIFIED** — handle inferred from the domain, not confirmed; does not render unauthenticated |
| Meta Ad Library | `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=IN&q=Comet` | **UNVERIFIED — HTTP 403 from cloud** |
| `cometshoes.com` | — | **NOT the brand's store.** Do not use |

---

## 9. Claims we can safely make from public brand copy

- **"Never Shy, Never Sorry"** — their own registered tagline (OBSERVED on the brand channel).
- **₹4,299** as the X Lows LIGHT price — published on their PDP as structured data.
- The product family and colourway names as published: *X Lows*, *LIGHT*, *Lows White*, and the
  sibling colourway names in the sitemap.
- Drop names and their listed prices as published on `/drops`.
- That the product is a sneaker, sold by Comet, in men's and women's ranges.

## 10. Claims we should NOT infer

- **Any discount or offer.** X Lows LIGHT has **no `compare_at_price`**. Do not imply a saving.
- **Any scarcity claim.** The rendered collection pages label nearly every item `SOLD OUT`, but the
  JSON endpoint carries no `available` field and a blanket sell-out across the whole catalogue is more
  likely a rendering artefact than fact. **Stock state is unknown.** Do not write "sold out",
  "limited", "restocked", or "drops fast" — even though scarcity is plainly part of their real
  marketing, we did not verify any specific instance of it.
- **Any performance or comfort claim** — cushioning, arch support, durability, materials, waterproofing.
  None verified.
- **Any claim about the proprietary sole.** Press reports the Series B funds *"proprietary sole designs
  and tooling"*. That is a plan, not a shipped product feature. Do not advertise it.
- **Any claim about their advertising**, ours versus theirs, or their performance results.
- **Any collaboration partner's IP.** UNO, FARAK, ODDNOTEVEN, NARU, VERONICA'S and MONOPOLY are third
  parties. **Do not build spec work on a collaboration.**
- **Any celebrity or investor association**, including the named angel investors.
- **Any revenue, growth or market-position claim** — all such figures here are press-reported.

---

## 11. Creative whitespace

**The plain opening.** A 500k-follower, drop-driven brand with **zero videos** on its official YouTube
channel and visibly light per-SKU photography (9 images).

**The real opening — and it is a cost argument, not a quality argument.** Comet's own thesis is that
the product carries the story, and their founder has said outright that they went this way because
they *could not afford* celebrity marketing. A named concept like *RADIOACTIVE* or *MAACHIS* wants a
built visual world. **Building a new world per drop, a dozen times a year, is precisely what
conventional production cannot do at a sane cost** — which is why the drop names are currently doing
more conceptual work than the imagery behind them appears to.

We would not be asking Comet to change their philosophy. We would be offering to run the philosophy
they already have at a cadence their current cost base cannot support. That is a materially easier
conversation than telling a brand its creative is wrong.

**The negative filter runs in our favour.** Run 01 discarded MetaMan and Phitku for celebrity and
film-IP dependence, and this run downgraded Foxtale for the same reason. Comet has publicly committed
to the opposite, which removes the most common structural blocker in this category.

**Not whitespace:** community and UGC. They are demonstrably good at it, and it is not what we sell.

---

## 12. Creative territories (high-level — production chooses)

All inside Alpha 1: a static plate with code-composed exact copy, optionally followed by one short
silent motion version derived from the accepted still.

**A. The drop world, built.**
Take one Comet-owned colourway name and construct the visual world the name implies, with the sneaker
literal and exact at its centre. The deliverable doubles as a **template**: the next drop name swaps
into the same structure. *Strength:* it is their stated strategy, executed at a scale they have not
been able to buy; it argues the recurring case by existing. *Risk:* concept-led scenes pull attention
away from product fidelity, and the sneaker must stay exact.

**B. One composition, six colourways.**
A single strong product composition re-rendered across the X Lows colourway family. The deliverable is
a **system**, not an image — direct proof that colourway number seven is cheap. *Strength:* lowest
fidelity risk, and it maps exactly onto a catalogue where each colourway is already its own product.
*Risk:* less exciting to a brand that trades on drama; may read as a catalogue exercise.

**C. The object, oversized.**
The sneaker treated as sculpture — scale, material and light beyond what a product shoot allows, while
keeping silhouette and colour exact. *Strength:* closest to sneaker-culture visual language and the
clearest demonstration of what generation adds. *Risk:* knit and mesh upper texture at large scale is
the single hardest fidelity case on this product.

**A live question for production, not resolved here:** footwear is conventionally advertised **on
foot**. All three territories are product-only, because Alpha 1 excludes human performance and the
identifiable-person gate applies to supplied photography. **Whether Comet will accept product-only
hero creative is genuinely unknown** and is the main format risk on this brand.

---

## 13. AI production risks

1. **Knit / mesh upper texture — highest risk.** Woven and knitted uppers are among the hardest
   surfaces to render convincingly, and they dominate this silhouette.
2. **Sole tooling geometry.** The Series B is explicitly funding **proprietary sole designs** — the
   exact geometry they care most about is the exact geometry most likely to render wrong. Treat the
   sole profile as a fidelity-critical region.
3. **Thin reference base.** 9 images per SKU versus Mokobara's 35–96. Less to condition on, less to
   verify against.
4. **Logo and wordmark fidelity.** Composite, never generate. Source file not yet located (§8).
5. **Colourway accuracy** on named proprietary colours.
6. **Format acceptance** (§12) — product-only versus on-foot. A commercial risk more than a technical
   one, but it can sink the send.
7. **Third-party IP.** Collaboration drops carry partner marks. **Stay on Comet-owned colourways.**
8. **The C-7 boundary is not at risk:** no talking head, no lip-sync, no native speech, no multi-shot
   story, no generated in-scene exact text.
9. **The hard dependency, restated.** Per `coordination/CONTROL-STATE.md` §9: **the runtime has never
   called a provider**; `spend_authority.status: none`. **This workstream selects a brand; it cannot
   unblock production.**

---

## 14. Likely decision maker

### **Utkarsh Gupta — Co-Founder**

He gives the creative-strategy interviews, so creative is demonstrably his. At roughly ₹29 Cr of
revenue with two founders and no CMO layer, **a spec ad reaches a decision-maker directly** — there is
no procurement process and no agency-of-record gatekeeper to survive.

**Secondary:** **Dishant Daryani**, Co-Founder.

**Contact route — public only.** Public LinkedIn `in.linkedin.com/in/utk410`; public contact routes
published on `wearcomet.com`. **No personal phone number or private email was sourced, and none should
be.** **No warm path exists** — the repository's authorised context states no relationship with Comet,
and none is claimed.

**One framing note for whoever writes the approach:** their founder has said publicly that they chose
story over celebrity *because of budget*. An approach that leads with cost-per-asset and cadence will
land better than one that leads with novelty.

---

## 15. Recurring commercial opportunity

The unit of work is **the drop**, and it is defined by their business model, not by our pitch:

| Multiplier | Observed value |
|---|---|
| Product URLs | **194** (each colourway its own product) |
| Named drops on page one of `/drops` | **12**, with at least one further page |
| Implied cadence | roughly **1–2 drops per month** |
| Retail expansion | **10 → 20 stores** by FY27 |
| Ranges | men's and women's; sneakers and slides |
| Partnership surfaces | `/members-club-collection`, `/cred-comet` |

**A plausible shape, to be tested not assumed:** a per-drop pack of *1 hero plate + 6–10 colourway and
format variations*, plus per-store-launch creative through the 10 → 20 expansion.

**This is one of the few prospects where the recurring need is visible directly in the catalogue
architecture** rather than inferred from company size. A brand that ships a named drop every few weeks
has an unavoidable, permanent creative requirement.

**Ability to pay — stated honestly.** ₹29 Cr FY25 revenue is small. The case rests on ₹100 Cr raised
this month and reported monthly sales of ₹4–5 Cr. **Capacity to pay is new, not proven** — which is
why this scores 8/10 on that criterion and ranks second rather than first.

---

## 16. Source links

**Primary — fetched and read directly (OBSERVED 2026-09-17):**
- `https://wearcomet.com/` — footprint source
- `https://www.wearcomet.com/collections/drops` — 12 named drops with prices
- `https://www.wearcomet.com/products/x-lows-light.json` — selected product record
- `https://www.wearcomet.com/sitemap_products_1.xml?from=8314222969139&to=10455546200371` — 194 products
- `https://www.wearcomet.com/sitemap_collections_1.xml?from=439577936179&to=511837634867`
- `https://www.youtube.com/@wearcomet/videos` — empty Videos tab
- `https://cdn.shopify.com/s/files/1/0738/5559/8899/` — asset root
- `https://cometshoes.com/` and `/sitemap.xml` — confirmed **not** the brand's store

**Attempted and refused (OBSERVED as unavailable, 2026-09-17):**
- `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=IN&q=Comet shoes` — **HTTP 403**
- Instagram — no unauthenticated render

**Secondary — press (INFERRED, fetched 2026-09-17):**
- Storyboard18 — "Comet raises Rs 100 cr in Series B funding led by Verlinvest", 10→20 stores, use of funds
- Business Standard; YourStory; DealStreetAsia — Series B coverage
- Inc42 — "Can Comet Stir Up A Sneaker Revolution With Its Storytelling Playbook?" — founder quotes
- `niharkhandelwal.substack.com` — Deal Roundup, 31 Aug–06 September 2026 (discovery source)
- Public LinkedIn — Utkarsh Gupta, Co-Founder

---

## 17. Research date

**2026-09-17** (IST). All OBSERVED items fetched on this date. All INFERRED items read on this date
from sources published earlier.

**Re-verify before production if more than ~14 days have passed** — a drop-led catalogue turns over
quickly, and the exact-copy value in §2 (₹4,299) is what would be composed onto the plate.

**Outstanding before spend:**
1. **Instagram hand-check — the priority for this brand**, ahead of the Ad Library. A reported 500k+
   following is described in press as central to the model, and their primary creative engine is very
   likely there and entirely unseen by us.
2. **Meta Ad Library hand-check.**
3. **Confirm the Instagram handle** — `@wearcomet` is inferred from the domain, not verified.
4. **Locate an authoritative logo/wordmark source file** (§8) — never generate it.
5. **Resolve the format question** (§12): will a sneaker brand accept product-only hero creative?
6. **Confirm the runtime production dependency** (§13.9) before committing to produce.
