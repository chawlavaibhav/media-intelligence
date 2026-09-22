# Build note — PACK-critique_and_effectiveness (CE)

Authority: `coordination/decisions/CONTROLLER-CANON-COMPLETION-2026-09-22.md`. USD 0; no model call.
Files written: `PACK-critique_and_effectiveness.authoring.yaml` (this dir) and this note; the compiler
wrote `canon/compilation/PACK-critique_and_effectiveness-v0.yaml`. Status PROPOSED. Applicability:
static_image, video, image_sequence.

Framing: this is the universal "critique" pack, so every decision is a question a checker asks of a
finished board or artifact. Many seeds are also compiled in the other packs through the same sources;
here they are consumed as check questions, and the note says which pack owns the production decision.

## 1. Decisions (10)

- CE-D1 One core, every element earning its place: grunt test; core by exclusion (proverb standard);
  one adjective / one point; dilution arithmetic as the removal check; a picture earns its space.
- CE-D2 Sells or merely entertains; product the hero: the measure is brand-preference change (recall
  appears uncorrelated with purchase); liked ≠ selling; product as hero, in use / end result / close-up;
  amusement draws the uninterested, no amusing / boasting / showing off, one typical buyer; celebrity,
  adult cartoons and vignette parades below average.
- CE-D3 Claim credible and concrete: specifics over generalities, no superlatives; actions and sensory
  detail, one individual; flag the buyer or place; exaggeration knowingly and on a truth; no
  exclamation marks, puns or rhymes.
- CE-D4 Attention earned, held, credited to the brand: first frame as gate, one burr, no scene parade;
  surprise decays so open and fill a gap; the material is the release order; the still reveal and its
  findability floor (scale figure vs print size); name by 10 s, end on the pack; one device for years;
  established mark retouched, never replaced.
- CE-D5 Story: customer hero, brand guide; no conflict no story, no opening after purchase; stakes
  named and dosed; the three questions answerable at any moment; story pre-orders and rehearses.
- CE-D6 Audio: supers = spoken words verbatim; on-camera speech holds better than VO; background music
  no measurable good, effects can help, jingles below average and deciphered before air; sound creates
  reality faster than picture; music "seems to" work best channelling an emotion already made; opening
  music must not promise a register the piece never keeps; withdrawn dialogue makes sound read as speech.
- CE-D7 Register: interesting first, funny an accent, register = product × audience; clear/clever
  overlap and its two rejection marks; universal miscomprehension (19–40 %) so be crystal clear; humour
  can now sell but only the few (vs Hopkins, CF-03); what they remember is how they felt; respect and
  delight; Indian-language lines originated, not translated.
- CE-D8 Every cut earns itself and the space holds: new information / motivated departure; describe-it-
  aloud length against the fast-cut norm; dissolve and fade registers; camera as the audience's eye,
  too much movement covers up; constant film-world rules; screen direction until a change is shown;
  break shot for a contradicting shot.
- CE-D9 Nothing judged alone: colour against neighbours, the most relative medium; value across hues
  unreliable by eye; tonal separation subject/ground; genre key and level following the dramatic line;
  text-over-image value contrast; letter differentiation, all-caps hardest; strength = contrast, not
  impact; three zones not a coordinate; vertical frame ≠ tallness.
- CE-D10 How the verdict is stated and what gives first: analysis against the brief's objectives, not
  reaction or redesign; finding = element + objective + why; the good note; symptom vs cause; a right
  alarm with a wrong diagnosis still helps; the six-criteria sacrifice order, emotion first.

Feeds: alongside the brief's list the pack uses `OBJECTIVE_INTERPRETATION` and `CORE_CREATIVE_IDEA`
(INJECTION-CONTRACT §3.4 maps critique_and_effectiveness to FAILURE_PREVENTION; the check ids are the
consumption point).

## 2. Seed coverage — 63 of 63 (`canon_done --pack`: seed 63 · cited 63 · missing 0)

D1: sb_0015, hea_mts_0009, whip_0015, hop_sa_0026 · D2: ogl_0014, ogx_0041, mla_0064, hop_sa_0014,
ogx_0038 · D3: ogx_0009, hea_mts_0012, 0016, ogx_0007, whip_0031, 0033, 0029 · D4: ogx_0040,
hea_mts_0011, murch_0013, fre_0025, 0024, ogx_0039, ogx_0041, vig_0013 · D5: sb_0008, whip_0015, 0011,
sb_0012, 0014, 0004, hea_mts_0018 · D6: ogx_0042, gote_0048, conv_0007, 0023, 0019 · D7: whip_0058,
0005, ogx_0032, murch_0020, ppm_0001, nnn_0052 · D8: gote_0004, 0006, 0053, 0052, 0031, 0037, alt_0014,
gos_0006, 0007, gote_0017 · D9: alb_0006, 0011, 0018, 0005, alt_0015, 0018, 0022, sam_0021, vig_0009,
fre_0017, 0008 · D10: murch_0019, 0027, 0020.
Every seed is named in the default text of a decision that lists it (mechanically checked: 0 ids
listed-only). Non-seed ids added, all read in full: hea_mts_0008, whip_0004, whip_0003 (the removal
arithmetic CE-D1's check rests on), ogx_0031 (the measure — the closure hub of ogx_0038/0042/0032),
ogl_0021 (liked ≠ selling: squarely a checker question), ogx_0043 (universal miscomprehension),
disc_0005, disc_0006, cat_0015, cat_0011, cat_0017 (the critique-process contributors carry no seed;
CE-D10 is built from them). 74 sk objects cited.

## 3. Closure holes and resolution (compiler undirected union)

Cited: hea_0009 / hea_0012 qualified_by 0008 → cited; hea_0012 qualified_by 0016 (seed); whip_0015
depends_on 0004 → cited; whip_0004 depends_on 0003 → cited; whip_0005 qualified_by 0058 (seed);
gote_0004/0006 pair (seeds); gote_0052/0053 pair (seeds); alb_0011 depends_on 0006 (seed); fre_0025
depends_on 0024 (seed); ogx_0038, 0042 depends_on 0031 and ogx_0032 qualifies 0031 → 0031 cited;
ogx_0043 qualifies 0031 → both cited; disc_0005 depends_on 0006 → cited; cat_0011 qualified_by 0017 →
cited.
Conflicts (8): CF-01 ogx_0040/0039 trade-off (same rule as CC/CD CF-01); CF-02 whip_0005/0001
trade-off (0001 named, not cited; the one-viewing get as in CD CF-02); CF-03 mla_0064 vs ogx_0032 —
`contradicts` without a stored relation, justified by ogx_0032's own text quoting and reversing
Hopkins' line (same ruling as CC CF-03); CF-04 alt_0018 vs 0011 (0011 named; as PA CF-03); CF-05
gos_0007 vs gos_0012 (0012 named, not cited — citing it would pull the frozen regression trio 0007/0010/
0013); CF-06 alt_0015 vs 0017 (0017 named; as PA CF-01); CF-07 ogl_0014 vs 0021, both cited: hero is the
form, selling the criterion (CC carries the same pair as CF-05); CF-08 ogx_0031 vs 0006 (0006 named, not
cited): scope by medium — the print recall figures do not predict here.
Waivers (37): hop_sa_0014 → 0008 (salesmanship analogy), → 0031 (hailing headline is CC-D9);
hop_sa_0026 → 0021 (mail-order evidential ground); murch_0019 → 0011, 0028, 0029, 0032 and murch_0027 →
0030, 0031 (film-relative bad bit, perceptual asymmetry, hedged weights, audience standpoint, top-three
binding, aim-for-all-six — the sacrifice order consumed is unchanged by each; 0031 is the complement of
the default's own condition); ogl_0014 → 0020 (direct-response format); whip_0005 → 0006 (writing
procedure, TC-D4), → 0007 (5–40 % travel, bounded by CF-02), → 0016 (strategy precision); whip_0011 →
0013 (deprivation shape, "usually", is CD-D4's choice); whip_0003 → 0053 (the boss element is TC-D6);
whip_0004 → 0061 (revision defence); alb_0018 → 0014 (light and hue at once — supports, does not narrow);
conv_0007 → 0009 (source music route; score-vs-source is EP-D8 / CD-D10); gote_0031 → 0028 (dissolve
duration is EP-D7); gote_0017 → 0054 (action line is CG-D2); gos_0007 → 0005 (frame-edge definition),
→ 0008 (sight lines; eye-lines are CG-D3); mla_0064 → 0010 (curiosity endorsed while amusement refused;
curiosity as a hold device is CE-D4 via hea_0011); ogx_0038 → 0034 (testimonial casting is CC-D7);
sb_0004 → 0003 (processing-cost cause); sb_0012 → 0006 (seven-element framework), → 0017 (rules-cannot-
be-broken framing, as CD); vig_0009 and vig_0013 → 0011 (timelessness credo); disc_0005 → 0022 (the
brief supplies the objectives; foundation-building is upstream), → 0003 (the reaction form the
definition excludes), → 0032 (the approval gate is the Controller's step, not this check), → 0020 (not
a consensus mechanism — stands); cat_0015 → 0018 (how a note lands vs what it contains); fre_0017 → 0016
(placement rules rejected outright — the "not a coordinate" hedge is kept); ogx_0031 → 0036 (emotion
unquantified — carried as a limit line), → 0021 (print/recall celebrity statement; the television
statement 0038 is the one consumed).

## 4. Limit lines

- Coverage delta: Ogilvy TV 1983 on brand preference; Hopkins 1920s print; Grammar of the Edit/Shot,
  Murch, Ondaatje, Alton = film and TV craft; Connor-Irizarry / Catmull = design and animation review
  rooms. No contributor treats 9:16 feeds, sound-off autoplay, sub-10 s ads or thumb-stop metrics, and
  none says whether a piece must work with the audio removed — CE-D6 governs only the audio present
  (the "works with sound off" question in the task brief is unanswerable from the corpus; said so).
- India: only Pandey (2015 credo) and Parameswaran (agency history) are Indian; ASCI, category and
  festival codes, regional-language register uncovered — check ASCI outside Canon.
- Uncovered predictors: liking, views, engagement (ogx_0031 rejects recall for TV only); emotion's
  effect is stated as unquantified (ogx_0036); pre-testing method; checker independence and
  aggregation (Kahneman/Sibony/Sunstein not compiled — see §5); "enough" value contrast (sam_0021).
- Devanagari line added by the compiler.

## 5. Deliberately not compiled, and honesty notes

- Seeds whose production decision lives elsewhere are consumed here only as check questions: the
  Grammar/Murch/Ondaatje/Alton seeds (EP-D2/D4/D7/D8, CG-D2/D5, CD-D9/D10, CV-D6/D7, PA-D5/D6); the
  Albers/Samara/Vignelli/Freeman seeds (CV-D3/D8, TC-D8/D9, CA); the Ogilvy/Hopkins/Sullivan/Miller/
  Heath seeds (CC-D1..D10, CD-D1..D8, TC-D4/D5). No production rule is duplicated; the check lines are
  written at the checker's level. Applying feature-film craft to a 15–30 s ad is a transfer the sources
  do not make; the coverage limit says so.
- Seeds that sit oddly under a critique question and are cited for what a checker can inspect only:
  gote_0031/0037 (transition registers — "is said to" kept), alt_0022 (level across a whole film,
  checked as "level follows the emotional line"), fre_0008/0024 (frame orientation and print-size
  floor), nnn_0052 (an agency history; consumed as the origination-not-translation check its stated
  problem supports). None is forced into a question it does not answer.
- Hedges kept: conv_0007 "seems to"; gote_0031 "are said to"; ogx_0031 "appears uncorrelated";
  ogx_0032 "can now sell"; whip_0058 "maybe the wrong one"; alb_0006 "almost never"; fre_0017 "not a
  coordinate"; murch_0027 conditioned on "when a cut cannot meet all six".
- Operationalisations that are the checker's, not the source's, are confined to the check lines:
  "grayscale" (from alb_0018's value-across-hues finding), "a stranger gets it in one viewing" (whip_0001
  via CF-02), "at delivery size" (fre_0024's print-size condition).
- Not compiled for budget: eic_0028 (Binet & Field's refusal of universal rules — was cited, dropped at
  the last 40 tokens; the marker legend already carries the caveat) and the rest of Binet & Field's
  effectiveness findings (consideration, brand/activation balance — no seed, and they are budget-level,
  not artifact-level, checks); Kahneman/Sibony/Sunstein (nse_0024 independence, nse_0035 accuracy not
  self-expression — checker-process claims; recorded as an uncovered limit); disc_0036 (findings not a
  change list — the check line says it via disc_0005/0006), disc_0034/0045; cat_0010 (no power to
  mandate); ogx_0034; whip_0001/0007/0013/0060; sut_alc_*, bay_*, bij_*, son_*, carroll_* (no seed).
- Two merges were needed to fit: the brand-registration decision into CE-D4 (CF-01 binds the pair
  anyway) and cut logic with spatial continuity into CE-D8. Twelve decisions rendered at 3,354 tokens;
  eleven at 2,747; ten at 2,494. No seed dropped; one non-seed id (eic_0028) dropped.
- The working tree also shows `product_appearance` authoring and compiled files modified by another
  session; this build did not touch them.

## 6. Terse tokens

2,494 of 2,500 (9,975 chars). `canon_done --pack`: seed 63 · cited 63 · missing 0 (exit 2, PROPOSED).
`validate_compiled_pack.py`: PASS (10 decisions, 74 sk objects, 2494/2500); the whole run PASSed and
`--check` reported 10 packs byte-identical at 2494 tokens. On the final re-run both global commands
failed on another builder's in-progress pack (`composition_and_attention`, over budget at the time of
writing; its authoring file is modified in the working tree by that session, not by this one) — not on
this pack. Re-run the two global commands once that pack is green.

## 7. Session tokens (estimate)

About 230k tokens, of which ~95k reading the seed packet in sections and ~45 partner / candidate claims
by id, and ~60k in the compile-trim loop (six budget passes).

## Post-check (Controller, from CHECK-critique_and_effectiveness.md — PASS)

- The checker's missing question added as a limit: CE-D4, D6, D8 are timeline craft and nothing in the pack replaces them for a still or carousel.
- Prose trimmed (punctuation, no content) to fit 2,500 tokens; 63/63 seeds unchanged.
