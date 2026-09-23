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
| Layout templates | `data/templates.yaml` | 6 poster layouts + 2 end cards: where the block sits, alignment, corners, picture placement, headline size limits; 9:16 laid out inside Instagram's safe area |
| Brand kit | `engine.BrandKit` | the customer shelf's typography: colours, logo (+ dark-ground variant), brand fonts, fixed system or moods, preferred templates, whether the logo may be reversed |
| Engine | `engine.py` | fits the exact copy: balanced line breaks (no widows), largest headline that fits, sizes stepped down the scale, product kept as large as possible, ink chosen by measured contrast |
| Checks | `checks.py` | blocking: exact copy, ≤ 2 typefaces, phone legibility, safe area, contrast, calm ground, product clear, no collisions, logo size/contrast. Flags: hierarchy, line length, widows, product scale |
| Picker | `picker.py` | renders every template × type system, drops blocked ones, ranks by craft score + the founder's taste weights (+ an optional vision judge, off by default) |
| Taste test | `taste.py` | a one-file page of side-by-side pairs; the founder's picks become weights in `data/taste.yaml` and measure how often the picker already agreed |
| Adapter | `adapter.py` | `still_ad(...)` / `end_card(...)` with the same return shape as `product/compose.py`, for the P1 v2 build to switch over behind a flag |
| Demo | `demo.py` | renders all candidates + a contact sheet for any picture and copy |

## How it learns (the "training")

The engine is code, so it never misspells. Taste comes from three places that grow over time:
1. **Templates and type systems** — curated data files. A human designer adds or edits them; each change is reviewed.
2. **The customer shelf** — once a brand approves a layout, its template, system and sizes go on its shelf (`preferred_templates`,
   `system`, `fonts`), so every later job starts from the approved look. This is the per-brand memory.
3. **The founder's taste** — `python -m product.typeset.taste page --dir <candidates>` builds the pair page; the founder
   picks; `taste ingest` turns the picks into weights the picker adds. The same run reports `picker_agreed`.

**Qualification (proposed pass mark, founder to confirm):** the picker's top choice agrees with the founder on ≥ 75 % of
pairs across two different products. Until then the founder picks from the top 3.

## Run it (no spend)

```bash
PYTHONPATH=. python -m unittest product.tests.test_typeset          # 16 tests, ~2 s
PYTHONPATH=. python -m product.typeset.demo --out /tmp/ts --format 4:5 --kind poster \
  --plate <plate.png> --product-box 0.13 0.18 0.86 0.86 --logo <logo.png> \
  --headline "Room for the long way home." --small "mokobara.com" --moods premium calm travel
PYTHONPATH=. python -m product.typeset.taste page --dir /tmp/ts
```

## Not done yet (next steps, in order)

1. **Founder taste rounds** on the Mokobara samples, then on a second, different brand.
2. **More templates from a human designer** (the 8 here are a starting set), especially Devanagari-first and offer/price layouts.
3. **Film supers** (captions over video) through the same engine; v1's `super_overlay` still draws them.
4. **Letter-spacing for all-caps labels** and optical kerning pairs (Pillow draws default spacing).
5. **Vision judge wiring**: `picker.JUDGE_PROMPT` is written; connecting it to a cheap vision model is a paid step for later.
6. **Brand onboarding**: collecting brand fonts (with licence confirmation) and a dark-ground logo onto the customer shelf.
   **The logo is never recoloured by default** (Canon TC-D10; the founder briefly allowed reversal to white on 2026-09-23,
   then withdrew it the same day). On a dark ground the brand must supply its own variant (`logo_on_dark`); otherwise a
   dark logo on a dark band is refused. A brand that explicitly permits reversal can set `logo_reversible: true` on its shelf.
