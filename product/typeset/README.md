# Typeset — the compositor's typography engine

A separate track from the P1 v2 build (founder, 2026-09-23). It replaces the v1 "sign painter" (`product/compose.py`,
system Arial/DejaVu, one fixed layout) with a small design system: licensed fonts, type systems, layout templates, a
layout engine, typography checks, a picker and the founder's taste test. **No AI is needed to render; nothing here spends money.**

## Why

On 23 September the v1 compositor shipped a generic Arial poster, an end card that typed "Mokobara" under the Mokobara
logo, a tiny tagline, and white "Mokobara" text across the bag in shot 1. It measured legibility and bounds, but made no
typographic choices: no typefaces, no scale, no grid, no layouts to choose from.

## What it is

| Part | File | What it holds |
|---|---|---|
| Font library | `fonts/`, `data/fonts.yaml` | 14 OFL families (Latin + Devanagari) from Google Fonts' GitHub, with licences and SHA-256 in `fonts/SOURCES.json` |
| Type systems | `data/fonts.yaml` → `systems` | 9 pairings (display face + text face + modular scale), tagged by mood (premium, calm, bold, playful, heritage, mass…), each with a Devanagari companion |
| Layout templates | `data/templates.yaml` | 7 poster layouts (incl. `offer_stack` for a price/discount hero) + 2 end cards: where the block sits, alignment, corners, picture placement, headline size limits; 9:16 laid out inside Instagram's safe area |
| Brand kit | `engine.BrandKit` | the customer shelf's typography: colours, logo (+ dark-ground variant), brand fonts, fixed system or moods, preferred templates, whether the logo may be reversed |
| Engine | `engine.py` | fits the exact copy: balanced line breaks (no widows), largest headline that fits, sizes stepped down the scale, product kept as large as possible, ink chosen by measured contrast |
| Checks | `checks.py` | blocking: exact copy, ≤ 2 typefaces, phone legibility, safe area, contrast, calm ground, product clear, no collisions, logo size/contrast. Flags: hierarchy, line length, widows, product scale |
| Picker | `picker.py` | renders every template × type system, drops blocked ones, ranks by craft score + the founder's taste weights (+ an optional vision judge, off by default) |
| Style profile | `style.py`, `data/style.yaml` | the founder's taste as design features (text position, alignment, band, serif/sans, headline scale, product placement), global + per brand |
| Controlled test | `experiment.py` | builds taste rounds where each pair differs in exactly one feature, and reads the verdicts |
| Taste test | `taste.py` | a one-file page of side-by-side pairs; the founder's picks become weights in `data/taste.yaml` and measure how often the picker already agreed |
| Adapter | `adapter.py` | `still_ad(...)` / `end_card(...)` with the same return shape as `product/compose.py`, for the P1 v2 build to switch over behind a flag |
| Film supers | `supers.py` | on-screen captions judged across several frames of the shot: kept clear of the product and hands, readable in every frame, opaque brand pill only when the picture is busy, reading-time check (0.6 s + 3 words/s) |
| Demo | `demo.py` | renders all candidates + a contact sheet for any picture and copy; detects the product on a studio packshot |

## How it learns (the "training")

The engine is code, so it never misspells. Taste comes from three places that grow over time:
1. **Templates and type systems** — curated data files. A human designer adds or edits them; each change is reviewed.
2. **The customer shelf** — once a brand approves a layout, its template, system and sizes go on its shelf (`preferred_templates`,
   `system`, `fonts`), so every later job starts from the approved look. This is the per-brand memory.
3. **The founder's taste** — `python -m product.typeset.taste page --dir <candidates>` builds the pair page; the founder
   picks; `taste ingest` turns the picks into weights the picker adds. The same run reports `picker_agreed`.

**Qualification (proposed pass mark, founder to confirm):** the picker's top choice agrees with the founder on ≥ 75 % of
pairs across two different products. Until then the founder picks from the top 3.

## Taste rounds so far

| Round | Brand / format | Pairs | Picker agreed before learning | What the founder preferred |
|---|---|---:|---:|---|
| 1 | Mokobara backpack, 4:5 | 15 | 5 (33 %) | text under the product; rejected dark bottom bands (1 win, 7 losses) |
| 2 | Cumin Co. bowl, 4:5 | 15 | **10 (67 %) — blind**, scored with round-1 learning only | text under the product again (5–0); the big headline won 3–0; the band at the bottom **won** 3–1 (sage green, no logo) though it lost 1–7 on Mokobara (navy, logo) |

| 3 | **Controlled**: Mokobara + Cumin Co., one difference per pair | 12 | — | both brands: **text above the product**, **product off-centre**. Split by brand: Mokobara = left-aligned, serif, modest headline, no band; Cumin Co. = centred, sans, big headline, colour band |

**Rounds 1–2 were bad tests (founder, 2026-09-23):** each pair differed in several ways at once and the win was credited
to the template's name. They almost never compared text-above with text-below directly (1 of 30 pairs), so their
"text under the product" signal was an artefact. Round-3 preferences, applied back to rounds 1–2, agree on 6/15 and 4/15
(the rest ties or misses) — i.e. rounds 1–2 cannot confirm or refute them. **Taste now lives in `data/style.yaml` as
style features** (`style.py`), global where both brands agreed, per brand where they split; the picker scores every
layout by the features it has, and tries an off-centre product when that is preferred. `data/taste.yaml` (template-name
weights) is kept as history and no longer used for scoring.

**Evidence strength:** one controlled pick per feature per brand. Next: repeat round 3 on a different format (1:1 or
9:16) — a preference that repeats is kept; one that flips is treated as "doesn't matter" and left to the brand's default.

**What the two rounds say (superseded by round 3, kept for the record).** One preference held across both brands: text under the product (`bottom_center`, 11 wins, 1 loss).
Others depend on the brand, so taste is now stored at two levels: **global** (moves half as fast; what holds across
brands) and **per brand** (in `taste.yaml → brands`, keyed by `BrandKit.name`, the customer shelf's memory). The picker adds
both. **Qualification not yet met:** 67 % blind agreement against the proposed 75 %. Next: a third brand, blind.

## Run it (no spend)

```bash
PYTHONPATH=. python -m unittest product.tests.test_typeset          # 23 tests, ~5 s
PYTHONPATH=. python -m product.typeset.demo --out /tmp/ts --format 4:5 --kind poster \
  --plate <plate.png> --product-box 0.13 0.18 0.86 0.86 --logo <logo.png> \
  --headline "Room for the long way home." --small "mokobara.com" --moods premium calm travel
PYTHONPATH=. python -m product.typeset.taste page --dir /tmp/ts
```

## Not done yet (next steps, in order)

1. **Founder taste rounds** on the Mokobara samples, then on a second, different brand.
2. **More templates from a human designer** (the 8 here are a starting set), especially Devanagari-first and offer/price layouts.
3. ~~Film supers~~ — built (`supers.py`); the pipeline still has to call it instead of v1's `super_overlay`.
4. ~~Letter-spacing for all-caps~~ — built (capitals tracked open automatically). Optical kerning pairs: still default.
5. **Vision judge wiring**: `picker.JUDGE_PROMPT` is written; connecting it to a cheap vision model is a paid step for later.
6. **Brand onboarding**: collecting brand fonts (with licence confirmation) and a dark-ground logo onto the customer shelf.
   **The logo is never recoloured by default** (Canon TC-D10; the founder briefly allowed reversal to white on 2026-09-23,
   then withdrew it the same day). On a dark ground the brand must supply its own variant (`logo_on_dark`); otherwise a
   dark logo on a dark band is refused. A brand that explicitly permits reversal can set `logo_reversible: true` on its shelf.
