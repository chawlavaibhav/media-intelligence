# Build note — product_appearance, extension to the seed list (2026-09-22)

Authority: `coordination/decisions/CONTROLLER-CANON-COMPLETION-2026-09-22.md` ruling 3. Files
touched: `PACK-product_appearance.authoring.yaml` (edited) and this note; the compiler rewrote
`canon/compilation/PACK-product_appearance-v0.yaml`. USD 0; no model call.

State before: 10 decisions, 35 sk objects, seed 13 / cited 4 / missing 9, 2,473 terse tokens.
State after: **12 decisions, 45 sk objects, seed 13 / cited 13 / missing 0, 2,500 terse tokens
(9,998 chars of 10,000)**; compile OK, `canon_done --pack` missing 0 (exit 2 = still PROPOSED,
adoption is the Controller's step), validator PASS, `--check --only` byte-stable.

## 1. Decisions (one line each; PA-D1..D10 keep their ids and meaning)

- PA-D1..D6, D8..D10 — unchanged in substance; prose tightened (see §7).
- PA-D7 (extended) — imagery earns its space; now also: plan the picture for one imagined typical
  buyer and do what a salesman would face to face — never amuse, boast or show off (hop_sa_0014).
- **PA-D11 (new)** — where the product sits and how height, scale and a second read register:
  placement by zone not coordinate (fre_0017); a vertical frame is not itself tallness, oppose two
  elements at the ends of the long axis (0008); a small figure supplies scale, as small as possible
  yet still seen at the delivered size (0024); a late-found second element must stay findable
  (0025); the camera is the audience's eye, too much movement covers up (alt_0014).
- **PA-D12 (new)** — what props, dress and figures staged with the product signal: each is a code the
  audience already holds (dpci_0040 props, 0070 dress, 0120 character type), Hindi-cinema codes to
  2002 whose style the source itself dates as ended (0190); use as deliberate, dated period codes,
  never the current default; the code tables sit in indian_indic_context IN-D3 (cross-reference,
  not duplicated).

## 2. Seed coverage — 13 of 13

| seed | decision |
|---|---|
| sk_hop_sa_0014 | PA-D7 |
| sk_hop_sa_0026 | PA-D7 (already) |
| sk_dpci_0040, sk_dpci_0070, sk_dpci_0120 | PA-D12 |
| sk_fre_c003_0008, sk_fre_c003_0017, sk_fre_c003_0024, sk_fre_c003_0025 | PA-D11 |
| sk_alt_c003_0014 | PA-D11 |
| sk_alt_c003_0015 | PA-D5 (already) |
| sk_alt_c003_0018, sk_alt_c003_0022 | PA-D6 (already) |

Non-seed id added for closure and because it changes the default: sk_dpci_0190 (the source's own
expiry notice on the three cinema codes) — cited in PA-D12, not waived, because "the style is a
thing of the past" is exactly what turns the codes into period codes.

Fit of seeds to questions, honestly: alt_0014 (camera = audience's attention) does not answer a
packshot question on its own; it is compiled in PA-D11 as the attention rider for a moving camera
on the product, and its narrative-film scope is declared in the transfer limit. fre_0008/0024 are
landscape claims and 0017 a 3:2 still-frame claim; they answer the placement/scale question as
stated, and the transfer to packshots and 9:16 is declared untested rather than assumed.

## 3. Closure holes and resolutions

- sk_hop_sa_0014 depends_on sk_hop_sa_0008 — **waived**: 0008 is the salesmanship analogy the method
  derives from; PA-D7 consumes the method and its prohibitions as stated and already treats the
  picture as a salesman (0026). Compiled as doctrine in commercial_communication CC-D9. Its own
  qualifier 0031 is already waived on this pack for 0035 on the same scope ground.
- sk_dpci_0040 / 0070 / 0120 qualified_by sk_dpci_0190 — **cited** (see §2).
- sk_dpci_0120 depends_on sk_dpci_0100 — **waived** (same waiver as indian_indic_context IN-D3 and
  concept_and_distinctiveness CD-D3): 0100 is the star-portrait carrier, bounded to Bachchan in the
  1970s–80s; a staged product-ad figure is not a film-star portrait; the star-recognition
  mechanism does not change the default. Film-poster star doctrine (0100, 0080) is not compiled in
  any pack.
- sk_fre_c003_0017 qualified_by sk_fre_c003_0016 — **waived**: 0016 is the source's rejection of
  placement rules (on grounds of fun and imagination) and its contradiction with the source's nod
  to classical proportion (0028). PA-D11 consumes only what 0017 itself states (three approximate
  zones, "any rule of thirds can only be approximate"), so the default already carries the
  qualification; the rejection-versus-proportion tension is arbitrated where the balance doctrine
  lives (composition_and_attention CA-D2 / CF-05) and does not change a placement-by-zone default.
- sk_fre_c003_0025 depends_on sk_fre_c003_0024 — cited in the same decision.
- sk_alt_c003_0014, sk_fre_c003_0008, sk_fre_c003_0024, sk_dpci_0190 — no guard partners.

No new conflicts entries; the eleven existing ones are kept (rules shortened, §7).

## 4. Limit lines

- LSM later-chapters caveat — verbatim (validator-grepped); unchanged.
- PA-D9 packshot limit — verbatim (spec §5); unchanged. PA-D9 still cites one claim; the new
  freeman/alton material was deliberately NOT put under PA-D9 so that "this default is one 1949
  cinema-era claim" stays true of the hero-angle criterion.
- **Coverage delta — rewritten** (the extension now compiles two of the three sources it named):
  dwyer-patel (PA-D12) and freeman (PA-D11) are compiled; the line now declares
  jain-gods-in-the-bazaar (frontality/darshan staging, iconographic codes — pointed at CV-D9 and
  IN-D2), carroll-read-this-photographs and hopkins ch8-21 as listed contributors with nothing
  compiled here, absent not arbitrated.
- Category-surface gap (watches, anisotropic brushed/sunburst) — kept, shortened.
- **New: transfer-untested line** — fre_0008/0024 landscape, fre_0017 a 3:2 still, alt_0014
  narrative film, dpci codes one audience to 2002: packshots, 9:16 frames and other audiences
  assume neither way. (Written as one pack limit rather than two decision limits to fit the budget.)

## 5. Deliberately not compiled

- jain-gods-in-the-bazaar, carroll-read-this-photographs, hopkins ch8-21: no hand-retrieved claim
  from them for this pack; declared in the coverage delta rather than compiled speculatively.
- The star-portrait doctrine (dpci_0100, 0080) and the rest of dwyer-patel: outside a product pack.
- The remaining light-science-magic-beyond-ch3 claims: still deferred (LSM caveat, unchanged).

## 6. Terse tokens

2,500 (9,998 chars). The pack sat at 2,473 before; the two new decisions and the PA-D7 rider cost
~2,000 chars, recovered by tightening (§7) — nothing dropped, no id removed.

## 7. What was tightened (meaning unchanged)

- Full ids in defaults (`sk_lsm_c003_0001`) replaced by the legend's short form (`lsm_0001`) —
  the composition pack already used it; ~200 chars.
- PA-D1..D10 defaults and checks: redundant words removed ("in frame", "of the product", "the
  three reflection types" → "the three types" where the contrast set is already named, "a
  brightness slider" → "brightness", etc.). PA-D5's default no longer repeats CF-02's rule
  ("decide per object, never both on one surface") — it points to CF-02, which carries it verbatim.
  PA-D10's check reads "every deviation from a PA decision" instead of "PA-D1..PA-D9" so it covers
  D11/D12.
- Conflict rules CF-01..CF-11 shortened; the three "not compiled into this pack; named so the
  boundary is visible" parentheticals become "(NNNN, uncompiled)" — the ids still appear, so the
  boundary is still visible. CF-11's "the metal finishing tools are deferred to the full live-37
  compile" is dropped from the rule (it is stated in the LSM caveat line).
- Coverage delta and category-gap lines shortened as in §4.
- Hedges kept: "assume the viewer decides" (0035); "as bad as none — it covers up" (0014); "as small
  as possible yet still seen at the delivered size" (0024); "a style the source dates as ended"
  (0190); hop_sa_0014's three prohibitions rendered as the source's own "do not" ("never amuse,
  boast or show off"), no condition added.

## 8. Red flags / what I could not do

- Nothing left over budget; no seed forced. The one stretch is alt_0014 in a packshot pack (§2),
  declared as such.
- Job records referencing PA-D1..D10 keep their meaning; PA-D7-check now also asks for the one
  typical buyer, which is an addition, not a change.
- Session tokens used (estimate, both packs together): ~330k, of which roughly 40 per cent was the
  budget squeeze (measure → tighten → re-measure loops).
