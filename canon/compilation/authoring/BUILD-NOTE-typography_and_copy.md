# Build note — PACK-typography_and_copy (TC)

Authority: `coordination/decisions/CONTROLLER-CANON-COMPLETION-2026-09-22.md`. USD 0; no model call.
Files written: `PACK-typography_and_copy.authoring.yaml` (this dir) and this note; the compiler wrote
`canon/compilation/PACK-typography_and_copy-v0.yaml`. Status PROPOSED. Applicability:
static_image, video, image_sequence.

## 1. Decisions (11)

- TC-D1 What the words do: grunt test in five seconds; clarity beats superiority; relevance and processing-cost cuts; the three story questions answerable at any moment.
- TC-D2 Whose story, how many points: customer hero, brand guide/archetype; one point per execution; one adjective per brand.
- TC-D3 Conflict and stakes: an opposing force in the line; deprivation over presence; stakes named and dosed.
- TC-D4 Clever vs fast: flat statement then spin; clear/clever overlap; quick get outranks creativity; 5–40% viewer travel; seven-word and two-second outdoor tests; removal test.
- TC-D5 Register and prohibitions: interesting before funny; no puns/rhymes, no exclamation marks, exaggeration only on a truth, no reassurance signals, no invented names or model numbers.
- TC-D6 Boss element and hierarchy: postcard/letter fork; one entry point; one clever element; no see-say; polarity; rank by scale and weight (visual strength not impact); headline that needs explaining failed; tagline conditions.
- TC-D7 Placement and secondary-line size: three zones not coordinates; oppose ends of the long axis in a vertical frame; text follows the image's structure; small elements sized to the delivered size; a second-read line must stay findable.
- TC-D8 Contrast: measure by luminance ratio (few judge lightness across hues; colour never seen alone); 4.5:1, 3:1 for large text with the size/weight test and thin-face warning; unrounded thresholds; outline vs halo; exemptions only for decoration/incidental text; measure against the pixels under the letters.
- TC-D9 Letterforms, case, colour-alone: word-picture reading, no all-caps running lines, no thin/unfamiliar faces at low contrast; colour never the only means, a 3:1 lightness difference as the second means.
- TC-D10 Brand mark: place the supplied mark unchanged; logotype contrast exemption only under a brand mandate.
- TC-D11 Generated vs composed text: none generated; real text over image of text; incidental or purely decorative letterforms only inside the picture.

Feeds: alongside the brief's list the pack uses `CORE_CREATIVE_IDEA` and
`DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS`, which INJECTION-CONTRACT §3.4 maps to this pack.

## 2. Seed coverage — 29 of 29 (`canon_done --pack`: seed 29 · cited 29 · missing 0)

D1: sb_c003_0015, 0004, 0014 · D2: sb_c003_0008, whip_0015 · D3: whip_0011, sb_c003_0012 ·
D4: whip_0005 · D5: whip_0058, 0029, 0033, 0031 · D6: vig_c003_0009 · D7: fre_c003_0017, 0008, 0024,
0025, sam_c003_0021 · D8: alb_c003_0018, 0006, 0011, wcag_0001, 0002, 0031, 0022, sam_c003_0021 ·
D9: alb_c003_0005, wcag_0022, 0007 · D10: vig_c003_0013, wcag_0004.
Non-seed ids added (all read in full): sb_c003_0002, 0003, 0018; whip_0001, 0002, 0003, 0004, 0006,
0007, 0013, 0032, 0034, 0035, 0037, 0043, 0045, 0048, 0053, 0057, 0060; vig_c003_0011; alb_c003_0004;
wcag_0003, 0008, 0014, 0018, 0021, 0025, 0027, 0033, 0034, 0035, 0038. 62 sk objects cited.

## 3. Closure holes and resolution (compiler undirected union)

Cited: wcag_0001 qualified_by 0002/0003/0004 and depends_on 0014 → all cited; 0002 depends_on 0021
→ cited; 0002 qualified_by 0022/0031 (seeds); 0021 qualified_by 0022 → cited; 0004 qualified_by 0034
→ cited; 0007 qualified_by 0038 → cited; 0003 depends_on 0027 and qualified_by 0035 → cited (D11);
0008 depends_on 0025 → cited; 0014 qualified_by 0018 → cited; whip_0005 qualified_by 0007/0058 →
cited; 0001 depends_on 0002, qualified_by 0060 → cited; 0002/0004/0053 depends_on 0003 → cited;
0003/0045/0043 depends_on 0053 → cited; 0043 qualified_by 0032 → cited; 0032 depends_on 0048 →
cited; 0057 qualified_by 0003 → cited; 0011 depends_on 0013 → cited; 0015 depends_on 0004 → cited;
vig_0009 depends_on 0011 and vig_0013 qualified_by 0011 → cited; alb_0011 depends_on 0006 (seed);
fre_0025 depends_on 0024 (seed).
Conflicts (5): CF-01 whip_0005/0001 trade-off; CF-02 whip_0007/0001 trade-off; CF-03 whip_0048/0001
trade-off (all three resolved by the two-second get, 0060); CF-04 sb_0012 contradicts sb_0017 (0017
named, not cited — same ruling as commercial_communication CF-06); CF-05 sb_0002/0003 trade-off
(both cited; jointly necessary cuts).
Waivers (16): whip_0004→0061 and whip_0005→0016 (same reasons as commercial_communication);
fre_0017→0016 (rejection of placement rules already carried by giving zones, no ratio); wcag_0001→0030
(derivation of 4.5); wcag_0014→0020, 0015, 0016, 0017, 0019, 0032 (luminance arithmetic and
web-rendering evaluation notes — a composited frame always has both colours, no user-agent
recolouring, no white default; hue-insensitivity confirms the measure-by-luminance default);
wcag_0021→0023, 0024 (delivered size = frame size; provenance of 18/14 pt); wcag_0008→0009 (AAA form
already satisfied by "none generated"), →0028 qualified_by and depends_on (no Essential exception is
claimed; logotype handled as a supplied file in D10); wcag_0025→0026 (programmatic-determinability
half is web markup).

## 4. Limit lines

- D7 limit: fre_0008/0024/0025 are landscape-still claims about pictorial elements; their transfer to composed copy is this pack's reading (the honest way to carry three seeds that were retrieved for text-placement jobs).
- D8 limit: wcag_* are Level AA web thresholds; the source does not claim they optimise readability on a phone feed (the source says so itself).
- Coverage delta: every contributor predates or sits outside 9:16 feed video and animated type; the seven-word figure is a roadside-poster number; no type size, line count or hold duration exists for on-screen text.
- A14 has no contributor: no Devanagari or Indic default; Hindi origination lives in CC-D9. Devanagari line added by the compiler.
- Grids (A07): Samara's column/module/reflow doctrine not compiled beyond sam_0021.

## 5. Deliberately not compiled

- A twelfth decision "Postcard or letter — how much copy?" (whip_0045, 0060, 0053) was authored and
  merged into TC-D6 for the terse budget; twelve decisions rendered at 3,011 tokens. No seed dropped.
- Samara's grid doctrine (77 of 79 claims), WCAG's resize/reflow/spacing criteria (0010–0013) and AAA
  enhanced contrast (0005), Freeman's framing/division claims, and Sullivan's process and platform
  claims (0009–0028, 0062–0070): no seed fell on them and no producer question about text on an ad
  frame needs them. whip_0049 (own a visual territory) was considered for D10 and left out: its
  dependency 0050 would have cost budget for a brand-level, not execution-level, claim.
- sam_0022 (text obeys alignment) was considered for D7 and left out: four qualifiers (0024, 0026,
  0027, 0028) on ragged edges, centred axes, hanging bullets and row guides are editorial-page detail.
- Hindi/Indic origination: no contributor in this pack's domains; stated as a limit and pointed at
  CC-D9 rather than citing nnn_0052 from outside the pack's contributor set.
- Red-flag check: sb_0008, sb_0014, whip_0011, whip_0031 and whip_0058 are also cited in
  commercial_communication; here they are compiled at the line level (what the words say), there at
  the idea level. fre_0008 (vertical frame ≠ tallness) is the weakest fit — carried in D7 with the
  limit line rather than forced into a separate decision.

## 6. Terse tokens

2,495 of 2,500 (9,980 chars). `compile --only typography_and_copy`: green; `canon_done --pack`:
missing 0 (exit 2, PROPOSED); validator: PASS for this pack; byte-stable across two compiles
(sha256 3d30cfa7…). At the time of this note the repo-wide validator and `--check` report one
error from another builder's in-progress pack (`camera_and_spatial_grammar`, 2,691 tokens) — not
touched here.

## 7. Session tokens (estimate)

About 190k tokens, of which ~95k reading the seed packet in sections and claims by id, and ~40k in
the trim loop (nine compile passes from 3,011 down to 2,495).

## Post-check edits (Controller, from CHECK-typography_and_copy.md — PASS WITH EDITS)

- TC-D8 limit reworded as a scope transfer ("applying [WCAG thresholds] to a composited frame is this pack's reading, not the source's") and the single-frame method declared (no default over a moving video ground).
- Platform UI safe zones for 9:16 text added to the coverage-delta limit line.
- Limit lines tightened to fit; 2,500 terse tokens; 29/29 seeds unchanged.
