# D2C brand discovery + commercial research

**Owner:** the scheduled D2C prospecting agent (unattended cloud run, Mon + Thu, 09:00 IST).
**Scope:** this folder only. The agent writes nothing outside `coordination/commercial/d2c-prospecting/`.

## What this workstream is for

To find real Indian D2C / consumer brands for which **one exceptionally strong unsolicited spec ad**
has a credible chance of producing: a real production test for the runtime; a send-worthy portfolio
asset; a conversation with the brand; and recurring paid creative work.

The loop it feeds: promising brand → understood advertising opportunity → one brand chosen → one spec
ad produced → **the Controller judges SEND / PORTFOLIO ONLY / DISCARD** → send if appropriate →
measure response → if converted, run real paid briefs through the runtime.

This is commercial prospecting. It does not modify the Media Intelligence architecture, Canon, the
Capability Registry, evidence, or any policy profile.

## Files

| File | What it is |
|---|---|
| `PROSPECT-PIPELINE.md` | Durable source of truth. One row per brand. Stages from `CONTACTED` onward are set by the Controller only. |
| `runs/YYYY-MM-DD.md` | One dated record per run: funnel, quick-screen, deep research, scoring, admissions, rejections, top 3. |
| `dossiers/<brand-slug>.md` | Top-3 only. The handoff to the eventual production agent. A dossier does **not** choose the final ad. |

## Standing rules the agent operates under

- **Evidence honesty.** Every evidence item is labelled `OBSERVED` (the page was fetched and seen) or
  `INFERRED` (press, job post, marketplace, second-hand, or a search-engine summary of a page that
  could not be fetched), and carries the date it was gathered. Never "they are running N Meta
  creatives" unless observed.
- **Meta Ad Library + Instagram check recommended by hand for the Top 3 before spend.** From an
  unattended cloud run these cannot be logged into and largely do not render.
- **No contact.** The agent never contacts a brand, DMs a founder, emails anyone, or submits a form.
  No public claim that any brand is a client. No personal phone numbers or private emails are sourced.
- **No invented relationships or conflicts.** Warm paths are recorded only where the repository's
  authorised project context states one. As of the first run the repository states none.
- **Scoring is not inflated.** 85–100 exceptional · 75–84 strong · 70–74 worth retaining ·
  60–69 watchlist · <60 discard. Only 70+ enters the active shortlist.

## Fetching from the cloud — method notes (learned the hard way)

Recorded so no future run rediscovers these. Full detail in `runs/2026-09-17.md` §0.

- **Many Indian D2C sites reject a bare `curl` user-agent** with `HTTP 429 "Verifying your
  connection..."` or `403 "Just a moment..."`. This is site-level bot protection, **not** the agent
  proxy, and it is why run 02 left five rows unverified. They serve normally to a **complete browser
  header set** (`User-Agent`, `Accept`, `Accept-Language`, `Sec-Fetch-Dest/Mode/Site`,
  `Upgrade-Insecure-Requests`, HTTP/1.1). This reads ordinary public page source — no login, no wall
  bypassed. It unblocked 8 of 9 sites in run 03.
- **On Shopify, the Meta pixel is usually not a `connect.facebook.net` script tag.** It sits in the
  web-pixels manager config as `\"pixel_id\":\"…\",\"pixel_type\":\"facebook_pixel\"`, with
  server-side state in `\"facebookCapiEnabled\":true|false`. **Grepping only for
  `connect.facebook.net` under-reports pixels** and will wrongly suggest a brand runs no Meta ads.
- **`/products/<handle>.json` is public** on Shopify stores and is the correct source for exact
  prices, `compare_at_price`, colourway names and the full image list. Read exact-copy values from it
  rather than retyping them. Note it carries **no `available` field**, so it cannot confirm stock.
- **`sitemap_products_*.xml` / `sitemap_collections_*.xml`** give true catalogue scale and reveal
  campaign structure (gifting, price-band and per-drop collections).
- **YouTube:** read `ytInitialData` on `/@handle/videos`. `channelOwnerEmptyStateRenderer` means the
  channel has **zero** uploads. **Verify the handle belongs to the brand** — run 03 caught three
  impostor/unrelated handles and one wrong domain before they reached the pipeline.
- **Widen the pixel grep (learned run 04).** Grepping only `"pixel_id":"…"` misses stores that emit
  the web-pixels config with **escaped** quotes (`\\"pixel_id\\":\\"…\\"`). Four stores in run 04 showed
  `facebookCapiEnabled: true` with no pixel matched until the pattern was widened to
  `pixel_id.{0,8}[0-9]{13,17}`. Use the wide form, or pixels will be under-reported again.
- **Verify every domain and every social handle before trusting it.** Run 03 caught four traps, run 04
  caught seven: `uppercase.shop` (dead — the real domain is `uppercase.co.in`), `uniqyou.in` (an
  unrelated international school), `blueteaworld.com` (parked/expired), `spinbot.in` (114-byte empty
  body — the same signature as Nothing But), `assembly.com` vs `assemblytravel.com`, `bagline.in` →
  `bagline.com`, and `@uppercaseofficial` on YouTube (a phone-case seller, not the luggage brand).
- **`/collections/<handle>/products.json?limit=N` is the fastest true trigger check (learned run 05).**
  It returns `published_at` per SKU, so a brand's *actual* launch cadence is readable first-hand in one
  call — far better than trusting a press date. In run 05 this single call **refreshed Mokobara's trigger**
  (a 13-day-old ₹12,999 hero launch run 04 did not have), **exposed uppercase's stale one** (no new arrival
  in 4.5 months), **killed The Pant Project** (a heavy paid stack against a `new-arrivals` shelf whose newest
  SKU was a year old), and **corrected Salty's** (the "recent" bags vertical is eleven months old).
  **Make this a standing check on every deep-researched brand, including incumbents.**
- **`sitemap_products_1.xml` is not at the store root on many Shopify stores (learned run 05).** Fetch
  `/sitemap.xml` first and follow the `<loc>` entries it indexes. Five stores returned a product count of
  0 in run 05 until this was corrected.
- **A 114-byte body is a recurring trap, not a footprint result.** `ikonicme.com` and `solvedskin.com` both
  returned `HTTP 200` with a **114-byte** body in run 05 — the same signature already recorded for Nothing
  But and SpinBot. Treat 114 bytes (and `HTTP 000` / 0 bytes) as **"domain not established"**, never as
  "no ad tags".
- **Read YouTube upload counts as unique `"videoId"` matches** on `/@handle/videos`. The
  `accessibilityData` label parse returns nothing on current YouTube markup (run 05). Confirm the handle via
  `vanityChannelUrl` + channel description before trusting it.
- **Job-board discovery searches are near-zero yield (run 05).** Phrased as a web search they return SEO
  listicles, not brand-level signals. Not worth repeating in that form.
- **Meta Ad Library has returned HTTP 403 in every run to date** (run 04: five queries, 481-byte
  bodies). Record it and move on; never attempt to log in or scrape around it.

## Discovery sources that have earned a standing read

| Source | What it gives | Caveat |
|---|---|---|
| **LocalSamosa, "Brand Announcements, Launches and Releases"** (weekly) | The best **current-trigger** source found to date — dated, brand-level, launch-level. It produced the Comet `Astra` and AntiNorm updates in run 04, and **~75 dated launch items across two weekly editions in run 05** (the run's highest-yield source by a wide margin) | Mixes D2C with conglomerates, hospitality and spirits; screen hard — run 05 dropped ~20 of its items as MNC, alcohol or hospitality |
| **Inc42 FAST42 (D2C growth ranking)** | A legitimate pool of real operating consumer brands in the "large enough to pay, small enough to reach" band, with growth data. **Not** the same object as the "Top 20 Funded D2C Startups" index rejected in run 02 | Carries **no current trigger** — every name still needs one |
| **Entrackr weekly funding report** | The funding window, reliably dated | Consumer yield is often thin |
| `niharkhandelwal.substack.com` deal roundups | High-yield consumer deal flow (run 03) | Check the RSS date before mining — editions can lag |
| **Entrackr `/tags/d2c` index** | **Do not use.** Returned 2025-dated items as its most recent content (run 03) | — |

## What the product can actually make today — read before writing a spec-ad hypothesis

Every spec-ad hypothesis in this folder is shaped to the frozen Alpha-1 family
(`runtime/ALPHA-1.md`; Controller ruling C-7, `coordination/CONTROL-STATE.md` §2):

- **In:** one static commercial ad whose exact copy (price, offer, legal line, brand name) is
  **composed onto the plate by code**, so it is exact by construction and script-independent;
  optionally one **short silent motion version derived only from the accepted still**.
- **Out by ruling:** talking heads, lip-sync, native speech / voiceover, multi-shot stories, and
  **generated in-scene exact text**.
- **Conditional:** supplied-photo work, behind the identifiable-person consent gate, and today routed
  to a person (the `IMG-EDIT` / `IMG-REF` evidence is directional only).

A brand whose core creative need is creator-led talking-head UGC is therefore a **weaker** target than
its brand strength suggests, however well it is doing.

**And note the current hard dependency:** the runtime has never called a provider. Every run to date
is dry, `spend_authority.status: none` on every profile, and live transport is deliberately unwired.
Producing the first spec ad needs the three things named in `coordination/CONTROL-STATE.md` §9 —
a decision on where the plan comes from, live transport behind `ExecutionBridge.run()`, and a signed
runtime spend record. **This workstream can select a brand; it cannot unblock production.**
