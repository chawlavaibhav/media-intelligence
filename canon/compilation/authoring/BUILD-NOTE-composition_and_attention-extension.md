# Build note — composition_and_attention, extension to the seed list (2026-09-22)

Authority: `coordination/decisions/CONTROLLER-CANON-COMPLETION-2026-09-22.md` ruling 3. Files
touched: `PACK-composition_and_attention.authoring.yaml` (edited) and this note; the compiler
rewrote `canon/compilation/PACK-composition_and_attention-v0.yaml`. USD 0; no model call.

State before: 11 decisions, 69 sk objects, seed 32 / cited 15 / missing 17, 2,497 terse tokens.
State after: **11 decisions, 90 sk objects, seed 32 / cited 32 / missing 0, 2,500 terse tokens
(9,997 chars of 10,000)**; compile OK, `canon_done --pack` missing 0 (exit 2 = still PROPOSED),
validator PASS, `--check --only` byte-stable.

## 0. The budget forced a shape decision — read this first

Seventeen seeds had to enter a pack already at 2,497 of 2,500 tokens. Three of them ask questions
the pack did not answer (what joins shots; depth and key in tone; how text and the mark sit on the
image). I authored them first as three new decisions (CA-D12..D14) — 14 decisions, 19 conflicts —
which rendered at 3,268 tokens. The brief's rule for this case is "cut decisions, not ids". So the
new material was folded into the existing decision whose question it extends, each time widening
that decision's question rather than changing it:

- joins (gote_0028, 0031, 0037, 0048) → **CA-D10** "How long may a shot hold; what joins shots?"
- depth and key in tone (alt_0015, 0017, 0018, 0022) → **CA-D5** "Balance or restless; depth and
  key in tone?" (A03 visual weight lists Alton as its contributor; tone is weight)
- text and the mark (sam_0021, vig_0013, 0011) → **CA-D2** "Where do subject, text and mark sit?"

Every CA-D1..D11 id and its original meaning survive; the checks are supersets of the old checks.
No new decision id exists in this pack. If the Controller prefers three separate decisions, the
cost is ~700 chars over budget — the compiled tokens are the constraint, not the doctrine.

## 1. Decisions (what changed)

- CA-D1 (extended) — reads first/second/third; now also: a late-found second element must stay
  findable (fre_0025); a scale figure registers only above a size the delivered size sets (0024);
  coded figures, dress and props read as the code the audience holds (dpci_0120, 0070, 0040), a
  style the source dates as ended (0190) — state the meaning, period code only.
- CA-D2 (extended) — placement zones; now also text over the image (value contrast, playing off
  the image, following the structure beneath — sam_0021) and the supplied mark placed, never
  redrawn (vig_0013; timelessness 0011).
- CA-D3, D4, D6, D8 — unchanged in substance; tightened.
- CA-D5 (extended) — balance; now also depth by tonal separation either direction (alt_0015; 0017
  per CF-18) and key set for the whole piece by category before any scene, level following the
  dramatic line (0018, 0022).
- CA-D7 (extended) — the edit is when and in what order information is released (murch_0013);
  colour tied to the figure in an earlier closer shot as a fourth attention device (ms_0016).
- CA-D9 (extended) — the off-frame world keeps constant rules of direction and distance (gos_0006).
- CA-D10 (extended) — see §0: dissolve by duration and register, fade as boundary with audio first,
  sound creates reality faster than picture.
- CA-D11 (extended) — the camera is the audience's eye; too much movement covers up (alt_0014).

## 2. Seed coverage — 32 of 32

| seed | decision |
|---|---|
| murch_0013 | CA-D7 |
| sam_0021, vig_0013 | CA-D2 |
| dpci_0040, 0070, 0120 | CA-D1 |
| fre_0024, fre_0025 | CA-D1 |
| gos_0006 | CA-D9 |
| gote_0031, 0037, 0048 | CA-D10 |
| ms_0016 | CA-D7 |
| alt_0014 | CA-D11 |
| alt_0015, 0022, 0018 | CA-D5 |
| the 15 already cited (gos_0007, gote_0004/0006/0017/0052/0053, ms_0002/0017/0019, murch_0019/0020/0027, vig_0009, fre_0008/0017) | unchanged homes |

Non-seed ids added: dpci_0190 (expiry notice; changes the default, cited), gote_0028 (dissolve
duration; 0031's register is attributed to it, cited), vig_0011 (qualifies 0013; cited),
alt_0017 (0015's contradicting partner; cited and arbitrated in CF-18).

Cross-references, not duplicates: the dpci trio is compiled fully in indian_indic_context IN-D3
and dated in concept_and_distinctiveness CD-D3; here it enters only as "what a coded element is
read as", one sentence. sam_0021 / vig_0013 are compiled in typography_and_copy TC-D7/D10 and
colour CV-D4/D8; here only as placement of text and mark. Jain (CV-D9, IN-D2) stays uncompiled
in this pack — no hand-retrieved claim from it.

Fit, honestly: gote_0048 (sound creates reality faster than picture) sits under "what joins
shots" because the source states it as the reason the ear is stimulated to help the eye across a
join; it is not a composition claim and is not dressed up as one. alt_0018/0022 (key, level) are
lighting claims placed under tone because visual-weight is the domain that lists Alton; the
source-agreement rule they contradict (alt_0011) is product_appearance PA-D4's, not this pack's.

## 3. Closure holes and resolutions

- dpci_0040/0070/0120 qualified_by dpci_0190 — cited.
- dpci_0120 depends_on dpci_0100 — waived (same reason as IN-D3 / CD-D3 / PA-D12: star-portrait
  carrier, bounded to Bachchan 1970s–80s, not a product-ad figure).
- ms_0016 trades_off_with ms_0014 — waived (same waiver as camera CG-D5, colour CV-D1/D2, editing
  EP-D6): the trade-off is a lens choice; CA-D7 decides no lens; the reflection technique is not
  compiled.
- gote_0031 depends_on gote_0028 — cited.
- vig_0013 qualified_by vig_0011 — cited; the pilot's waiver of vig_0009 depends_on vig_0011 is
  therefore removed (its partner is now in the pack).
- alt_0015 contradicts / qualified_by alt_0017 — cited both; **CF-18** (new) carries the scope rule
  (subject-against-ground either direction vs three-plus staged depth planes), mirroring PA CF-01.
- alt_0018 contradicts alt_0011 — **waived**, not conflicted: 0011 (light agrees with an established
  source) is not consumed by CA-D5, which decides key and level by category only; source agreement
  and its musical-comedy exemption are arbitrated in product_appearance PA-D4 / CF-03. Named so the
  exemption is visible before anyone reads "comedy high" as licence to ignore the source.
- fre_0025 depends_on fre_0024 — cited together. gos_0006, gote_0037, gote_0048, alt_0014,
  alt_0022, murch_0013, sam_0021 — no guard partners.

Two pilot conflicts became waivers for budget, with identical content: **CF-13** (gote_0035 vs
gote_0012, the wipe waiving the thirty-degree rule — 0012 uncited, camera_and_spatial_grammar
scope) and **CF-17** (murch_0025 vs murch_0026, the tradition the source argues against — "named
for closure, not doctrine"). In both the partner is uncited and the decision does not consume it,
which is the waiver condition; the visibility moves from the terse text to the compiled waiver
list. Conflict ids are not reused: CF-13 and CF-17 are gaps, the new entry is CF-18.

## 4. Limit lines

- CA-D6 aspect limit (9:16 untested) — verbatim, unchanged.
- **Coverage delta — rewritten**: dwyer-patel (CA-D1) and alton (CA-D5, D11) are now compiled; the
  line names jain-gods-in-the-bazaar (darshan order, symmetry-as-authority; CV-D9, IN-D2),
  samara's grid (t_sam_0018 only, CF-16) and carroll-read-this-photographs as uncompiled, absent
  not arbitrated. carroll was a listed contributor the pilot line omitted.
- No per-seed transfer line fitted; the markers carry DATED / CULTURE-BOUND / MEDIUM-UNTESTED on
  every decision that took cinema or Hindi-poster claims.

## 5. Deliberately not compiled

jain (no seed); samara beyond sam_0021 and the T4 term; carroll; the rest of dwyer-patel (star
doctrine, darshan inside the film — IN-D4's); alt_0011 (PA-D4's).

## 6. Terse tokens

2,500 (9,997 chars). Before: 2,497.

## 7. What was tightened (meaning unchanged)

- Every default and check shortened; ~1,900 chars recovered. Typical moves: "competing cues confuse
  rather than direct (repeated focus-shifting is the type case, ms_0019)" → "competing cues confuse
  (ms_0019)" (the example dropped, the claim kept); "misdirection (murch_0033) is the scoped
  exception, only to set up a reveal" → "(murch_0018; misdirection 0033 per CF-15)" — the rule
  lives in CF-15 verbatim; CA-D9's far-side clause likewise points to CF-10/11, which carry it.
- Questions shortened where words were idle ("How does the frame hold the subject at its edges?"
  → "How do the edges hold the subject?"; "(video)" dropped from CA-D7 — the applicability list
  says it).
- Conflict rules CF-01..CF-16 shortened; none changed side or condition.
- Hedges kept: "probably" (fre_0020), "said to read" (gote_0031 — received opinion), "the source
  calls it alarming" (0052), "weights hedged, intervals the point" (murch_0029), "'bad' is
  film-relative" (0011), "a style the source dates as ended" (dpci_0190), "as bad as none"
  (alt_0014).

## 8. Red flags / what I could not do

- Could not keep three new decisions inside the budget (§0). Folded, not dropped.
- The dpci trio is a one-sentence rider in an attention decision; a checker may judge that too
  thin for A02's "Hindi-cinema attention order" and prefer IN-D3 to carry it alone — I kept it
  because the seeds were hand-retrieved for this pack's domains and the coverage test requires
  the citation, and because "read as the code the audience holds" is what dpci_0120 says.
- Session tokens (estimate, both packs): ~330k; see the PA note.
