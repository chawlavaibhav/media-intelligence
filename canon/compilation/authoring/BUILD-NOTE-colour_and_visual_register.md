# Build note — colour_and_visual_register (CV)

Authority: `coordination/decisions/CONTROLLER-CANON-COMPLETION-2026-09-22.md`. USD 0; no model call.
Files written: `PACK-colour_and_visual_register.authoring.yaml`, this note. Compiler output:
`canon/compilation/PACK-colour_and_visual_register-v0.yaml` (10 decisions, 61 sk objects, 20
waivers, 4 conflicts, 2,497 terse tokens). Applicability: static_image, video, image_sequence.

## 1. Decisions

- **CV-D1** palette: one saturated element on a graded-down ground, and it is the product (ogl_0014, ms_0016, ms_0019, vig_0009, vig_0011).
- **CV-D2** one attention cue per beat in a moving frame — colour, static blocking, hidden move; never rack focus; every move and hold has a reason (ms_0016/0017/0010/0019/0002/0018, alt_0014).
- **CV-D3** colour is judged against its neighbours on the real frame, never a swatch; lightness measured (alb_0006/0011/0012/0013/0014/0015/0007/0018).
- **CV-D4** brand colour by value, verified on delivered pixels in context; supplied mark untouched; logotype contrast exemption only under brand mandate (alb_0001/0002/0003/0012/0006, vig_0013/0011, ogl_0007, wcag_0004/0034).
- **CV-D5** product-to-ground separation by tone, surviving without hue; ≥ 3:1 measured (alt_0015/0017/0003, wcag_0007/0038, alb_0018).
- **CV-D6** mood from light character and grade, not level; one direction; level follows the dramatic line (alt_0025/0013/0026/0027/0022).
- **CV-D7** key of the whole piece from genre before any scene; still from a fictional source; brief override only (alt_0018/0022/0011).
- **CV-D8** the grade must leave measured contrast for anything readable (sam_0021, wcag_0001/0014/0021/0002/0031/0022/0033/0018/0027/0003/0035, alb_0005/0018).
- **CV-D9** Indian register as the contributors state it: saturation is a documented convention not a rule, never by audience class; regional iconographic codes; bazaar borrowing; vernacular setting; Hindi originated (jgb_0020/0090/0040/0130/0070, nnn_0043/0019/0021/0052).
- **CV-D10** overall register is quality, not loud; consistency; selling over style (ogl_0008/0007/0014/0021, vig_0009/0011).

## 2. Seed coverage — 23 of 23

| seed | decision | seed | decision |
|---|---|---|---|
| sk_ms_c003_0019 | D1, D2 | sk_vig_c003_0009 | D1, D10 |
| sk_ogl_c003_0014 | D1, D10 | sk_wcag_0004 | D4 |
| sk_sam_c003_0021 | D8 | sk_wcag_0007 | D5 |
| sk_vig_c003_0013 | D4 | sk_wcag_0022 | D8 |
| sk_wcag_0001 | D8 | sk_wcag_0031 | D8 |
| sk_wcag_0002 | D8 | sk_alt_c003_0014 | D2 |
| sk_alb_c003_0005 | D8 | sk_alt_c003_0015 | D5 |
| sk_alb_c003_0006 | D3, D4 | sk_alt_c003_0022 | D6, D7 |
| sk_alb_c003_0011 | D3 | sk_alt_c003_0018 | D7 |
| sk_alb_c003_0018 | D3, D5, D8 | sk_ms_c003_0002 | D2 |
| sk_ms_c003_0016 | D1, D2 | sk_ms_c003_0017 | D2 |
| sk_nnn_0052 | D9 | | |

`canon_done.py --pack colour_and_visual_register`: seed 23 · cited 23 · missing 0 (exit 2 = PROPOSED, expected).

Seeds that belong more naturally to another pack, cited here for coverage: sam_0021, wcag_0001/0002/0004/0022/0031, alb_0005 and vig_0013 are typography_and_copy's (TC-D8/D9/D10); ms_0002/0017/0019 and alt_0014 are camera_and_spatial_grammar's (CG-D5). Here they are compiled from the colour side — the grade must leave the text its contrast (D8), the brand colour and mark survive on real pixels (D4), colour is one of the attention cues and must not compete (D1/D2). alt_0015/0017/0003 also sit in product_appearance PA-D5; here they are cited for the ground only (finish, highlights and hero angle stay PA-D1/D2/D5/D9).

Non-seed ids added: alb_0001/0002/0003/0007/0012/0013/0014/0015; alt_0003/0011/0013/0017/0025/0026/0027; ms_0010/0018; ogl_0007/0008/0021; vig_0011; wcag_0003/0014/0018/0021/0027/0033/0034/0035/0038; jgb_0020/0040/0070/0090/0130; nnn_0019/0021/0043. Every one read in full via `pack_seed.py --claim`.

## 3. Closure holes and resolution

Conflicts (4):
- CF-01 alt_0015 vs alt_0017 (D5) — same rule as PA CF-01 / CG CF-04: ground vs staged planes.
- CF-02 alt_0018 vs alt_0011 (D7) — musical-comedy exemption; product ad is not the exempt genre; pastiche = deviation.
- CF-03 ms_0017 vs ms_0010 (D2) — static master vs hidden move; scoped by scene structure (as CG CF-03).
- CF-04 ogl_0014 vs ogl_0021 (D10) — product-hero vs style; selling decides (as CC CF).

Waivers (20), each stating what is consumed and why the partner does not change it:
- ogl_0014 contradicts ogl_0020 (direct-response format claims not consumed; same as CC).
- ms_0016 trades_off_with ms_0014 (lens/reflection technique not compiled; same as CG).
- ms_0010 qualified_by ms_0001, ms_0004 (rig-independence; reader's-own-test status; same as CG).
- alb_0012 depends_on alb_0009; qualified_by alb_0017, alb_0016 (classroom method, grading criterion, pedagogy — the effect is consumed, not the exercise).
- jgb_0090 qualified_by jgb_0180 (author's evidential bound on interview material; types the evidence, does not change the caution).
- alt_0003 trades_off_with alt_0004 (shiny props = product_appearance; ground rule unchanged).
- ogl_0007 qualified_by ogl_0013, ogl_0017 (thirty-year test; repeat-until-it-stops-selling — scheduling, not this pack).
- wcag_0001 qualified_by wcag_0030; wcag_0014 depends_on 0020, qualified_by 0015/0016/0017/0019/0032; wcag_0021 qualified_by 0023/0024 — identical reasoning to typography_and_copy (web-markup notions with no counterpart in a composited frame; derivations do not change the number).

Note on the seed packet: it lists outgoing `qualifies` edges (e.g. ms_0019 → ms_0008/0014, alb_0018 → alb_0014) as guards; the compiler normalises `qualifies` onto the target only, so these are not holes for the citing object and were not waived. Where the target mattered it was cited (alb_0014 in D3).

Cited partners rather than waived, because they change or sharpen the default: alt_0017 (conflict), alt_0011 (conflict), ms_0010 (conflict), wcag_0034 (narrows the logotype exemption — D4), wcag_0038 (makes lightness the second means — D5), wcag_0003/0027/0035 (the exemptions and their intent test — D8), wcag_0033 (unrounded, nominal pass — D8), jgb_0130 (why regional codes are stringent — D9), jgb_0090 (turns jgb_0020 from "saturation for the masses" into "never by audience class" — D9; this partner genuinely changes what a naive default would have said, so it was cited, not waived).

## 4. Limit lines and why

Per-decision limits were removed to fit the budget; all caveats now sit in `pack_limits` (2 authored + compiler's Devanagari line):
1. Coverage delta — every contributor's medium and era (Albers 1963 paper; Alton 1949 monochrome; Kenworthy narrative film; Jain's Sivakasi trade; Parameswaran single plates; WCAG web AA); nobody treats colour grading (B13 has no contributor), 9:16 feeds or phones. Written because a producer's first question — "what grade for a phone feed?" — has no source.
2. Nothing in the corpus names a palette size, hue, saturation value or colour temperature; CV-D1's one-saturated-element default is flagged as this pack's reading of ms_0016 + vig_0009 (kept because a producer must decide it, and it is the closest thing the contributors say). Colour harmony, warm/cool psychology, category colour codes, festival palettes, skin tones and Indian daylight are named as uncovered. Restraint vs saturation is stated as unarbitrated: Vignelli/Ogilvy prescribe quality; Jain documents the saturated convention without recommending it and her informants denigrate it — no condition separates the two, so the brief decides and records it (red-flag case, written here rather than blended).

## 5. Deliberately not compiled

- jgb_0040's regional taste discourse ("Bengali taste softest, south most intense") — Jain reports it as a trade stereotype; not a default (named in limit 2).
- jgb_0050/0150 (vernacularising capitalism; post-liberalisation template) — political-economy claims, no production decision; 0150 carries severe freshness risk.
- jgb_0010/0030 (frontal gaze; anti-muscularity) — iconography of deities, not colour/register; belong to indian_indic_context if ever compiled.
- nnn_0018 (J&N white ground / red block), nnn_0016 (Tuffs purple field) — single plates with no stated outcome; nnn_0021/0019 kept as the two with a stated mechanism, hedged "one plate".
- ogl_0015 (parity products differentiated by style) — would need ogl_0009/0016; style-differentiation is commercial_communication's ground.
- alt_0004 (shiny props), alt_0016 (mirrors, cast shadows), alt_0012 (filler/multiple shadows) — product_appearance / lighting recipe, not register.
- ms_0008/0014 (combine techniques; reflection technique) — not consumed; not guards on this pack's cited objects.
- alb_0004 (reading by word picture) — typography's (TC-D9); alb_0005 was a seed here and is cited, 0004 is not needed for it.
- wcag_0005/0009/0025/0028 (AAA, images-of-text criteria) — typography's TC-D11 territory.

Hedges kept as the sources have them: "almost never" (alb_0006), "very few" (alb_0018), "most products" (ogl_0008), "wherever possible" (ogl_0014), "usually vulgarity" (vig_0009), "practitioner theory" and "its makers call gaudy" (jgb_0020), "one plate" (nnn_0019/0021 in limit 1), "stated for monochrome film" (alt_0003). Nothing became "always"/"never" that the source did not state; the "never" lines (never alone, never the only means, never by author choice, never rack focus) are the sources' own.

## 6. Terse tokens

2,497 / 2,500 (9,986 chars). First compile was 3,643; the pack fit by tightening defaults and checks and folding per-decision limits into `pack_limits` — no seed dropped, no id removed. Loop results: compile OK; `canon_done --pack` missing 0 (exit 2, PROPOSED); `validate_compiled_pack.py` PASS for PACK-colour_and_visual_register-v0.yaml. The validator's overall FAIL and `--check`'s failure at the time of writing come from another session's in-progress pack (concept_and_distinctiveness over budget), not from this pack; re-run `--check` once that pack lands.

## 7. Session tokens

Roughly 110–130k tokens (seed packet read in sections, ~45 extra claims fetched by id, ~10 compile iterations for the budget).

## Post-check edits (Controller, from CHECK-colour_and_visual_register.md — PASS)

- Coverage-delta limit now states that CV-D5's 3:1 is a UI colour-coding rule transferred to product/ground separation (the checker's one scope note), and declares the two uncovered questions: platform recompression / 'vivid' display modes, and non-Latin script legibility for CV-D8's thresholds.
- Prose trimmed to fit 2,500 tokens; 23/23 seeds unchanged; no decision content changed.
