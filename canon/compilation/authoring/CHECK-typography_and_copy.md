# Checker report — PACK-typography_and_copy (TC)

Checker did not build this pack. Verified against `canon/compilation/authoring/PACK-typography_and_copy.authoring.yaml`
and `BUILD-NOTE-typography_and_copy.md` on branch `work/canon-done-2026-09-22`. USD 0, no model call.

## Verdict: PASS WITH EDITS

The pack is well-built: every decision I checked is SUPPORTED by its cited claims with close
paraphrase, not invention; the 16 waivers are honestly reasoned and none is wrong; the 5 conflicts
are resolved by relations the sources state themselves (GUARD `trades_off_with`/`contradicts`
fields confirm the pack's own resolution logic). One edit is needed before adoption (TC-D8's limit
line), and two producer questions are unanswered by any decision or limit line (below).

## Decisions → verdict

| Decision | Verdict | Note |
|---|---|---|
| TC-D1 | SUPPORTED | sb_0015 grunt test, sb_0018 "buy the product they understand fastest", sb_0002/0003 filtering+effort, sb_0014 three questions — all quoted near-verbatim. |
| TC-D2 | SUPPORTED | whip_0015 covers both "archetype not hero" and "Brand = adjective" — single claim, not two forced together. |
| TC-D3 | SUPPORTED | whip_0011 "Area Bank Not Robbed" verbatim; sb_0012 stakes "dosed like salt" verbatim. |
| TC-D4 | SUPPORTED | whip_0060's own GUARD relation says it "qualifies" whip_0001 as the medium-dependent fuse bound — matches CF-01/02/03's resolution exactly. |
| TC-D5 | SUPPORTED | whip_0058/0029/0033/0031/0035/0034 all direct restatements (exclamation "jazz hands", asterisk "we're lying", no fake names). |
| TC-D6 | SUPPORTED | vig_0009 "bold against light... vulgarity" quoted almost verbatim; whip_0037/0057/0053 direct. |
| TC-D7 | SUPPORTED, disclosed transfer | fre_0008/0024/0025 are landscape-still claims (figure-in-landscape, cinematic reveal) applied to composed text/zones; the pack's own limit line names this. Fair reading, not hidden. |
| TC-D8 | SUPPORTED, but limit line under-discloses | see item (a) below — needs a stronger limit line, not a content fix. |
| TC-D9 | SUPPORTED | alb_0004/0005 word-picture and all-caps claims exact; wcag_0007/0038 colour-alone rule exact. |
| TC-D10 | SUPPORTED | vig_0013 equity/retouch language exact; wcag_0004 cited only for "exempt," wcag_0034 cited only for "only under a brand mandate" — citation boundary matches which id says what (see item below on SC1.4.3 vs SC1.4.11 tension). |
| TC-D11 | SUPPORTED | wcag_0008/0025/0027/0035 — "none generated," decoration = "words swappable," exact matches. |

## (a) TC-D8 contrast thresholds vs. composited-frame claim

Every fetched WCAG claim (0001, 0002, 0003, 0014, 0018, 0021, 0022, 0031, 0033) is scoped
explicitly to `web_content_accessibility_conformance` / "web content being assessed for
conformance." None claims applicability to a composited (rendered, flattened) ad frame. The
build note's limit line says only: *"wcag_* are Level AA web thresholds; the source does not
claim they optimise readability on a phone feed."* That is true but weaker than what TC-D7 does
for its own borrowed claims (*"transfer to composed copy is this pack's reading"* — an explicit
admission of transfer). TC-D8's check line ("Each text block reports its ratio... no exemption on
a message word") reads as an unqualified hard gate, with the transfer-disclosure buried in a
negative statement about optimization rather than a positive statement about scope-transfer.
**Edit needed**: reword the D8 limit line to state plainly, as D7 does, that these are web
conformance thresholds applied to a flattened frame as a producer's best available proxy, untested
for composited stills/video. Content itself (4.5:1, 3:1, unrounded, outline-vs-halo) is quoted
correctly and is not overreach — this is a disclosure-strength issue, not a claim-fidelity one.

One more nuance in TC-D10: wcag_0004's unconditional logotype exemption is under SC 1.4.3/1.4.6;
wcag_0034's "only under a brand mandate" narrowing is stated by its own source text to apply under
SC 1.4.11 (non-text contrast) — the source itself calls this a "tension between levels." TC-D10's
citation boundary (0004 for "exempt," 0034 for "only under...") is defensible as a producer
simplification but merges two different criteria without flagging the source's own caveat. Minor;
does not change the default, so not scored as MISATTRIBUTED, but worth a one-clause footnote.

## (b) The 16 waivers

All 16 checked against their partner claim's actual text. None is WRONG — in each case the
partner's content genuinely would not change TC-D8/D11's default if consumed:

- wcag_0014→0017 is the strongest case: 0017's own caveat says the half-specified-colour failure
  "has no counterpart in a flattened raster" — the source concedes the waiver's reasoning itself.
- wcag_0014→0016 (white-background default), →0019 (user-agent recolouring), →0015
  (anti-aliasing-off measurement, already covered by 0033's nominal-pass warning) — all web-markup
  conditions with no counterpart in a fixed composited frame. Correctly waived.
- wcag_0001→0030 and wcag_0021→0024 are pure provenance/derivation notes (where 4.5 and 18pt/14pt
  came from) — they explain the number, they don't change it. Correctly waived.
- wcag_0008→0009 (AAA form) and →0028 (Essential test): TC-D11's default ("none generated") is
  already stricter than what either partner would require. Correctly waived.
- fre_0017→0016 and whip_0004→0061 / whip_0005→0016: brief-level and revision-defense doctrine
  that operates above the execution-level decisions TC-D2/D4/D7 make. Correctly waived.

No waiver judged wrong.

## (c) The three Sullivan trade-off conflicts (CF-01/02/03)

whip_0060's own GUARD relation states it "qualifies → sk_whip_0001 (dwell time in the medium sets
how long a fuse may be)," and whip_0001's GUARD relation independently lists `trades_off_with`
whip_0005 and whip_0007, and whip_0048 lists `trades_off_with` whip_0001 — i.e. the pack's
resolution ("keep the spin only while the two-second get holds") is not an invented tie-breaker;
it is the source's own stated relation, just executed. SUPPORTED — the "two-second get" is a real
operationalization (whip_0060: "show it to a friend for two seconds... ask what it said"), not a
loose gloss.

## Seed coverage — 29/29, `canon_done --pack`: `seed 29 · cited 29 · missing 0`

All 29 seeds CONSUMED (substantively reflected in the decision's default/check text, not merely
listed):

| Seed | Decision | Status |
|---|---|---|
| sb_0015, sb_0004, sb_0014 | D1 | CONSUMED |
| sb_0008, whip_0015 | D2 | CONSUMED |
| whip_0011, sb_0012 | D3 | CONSUMED |
| whip_0005 | D4 | CONSUMED |
| whip_0058, 0029, 0033, 0031 | D5 | CONSUMED |
| vig_0009 | D6 | CONSUMED |
| fre_0017, 0008, 0024, 0025, sam_0021 | D7 | CONSUMED |
| alb_0018, 0006, 0011, wcag_0001, 0002, 0031, 0022, sam_0021 | D8 | CONSUMED (alb_0011 is thin — cited alongside 0006 for "no colour seen alone," but 0011's own content is the broader "most relative medium" claim; still substantively connected via its own `depends_on 0006` relation, not padding) |
| alb_0005, wcag_0022, 0007 | D9 | CONSUMED |
| vig_0013, wcag_0004 | D10 | CONSUMED |

## Missing questions (item 4)

Two producer questions in this pack's own domain are answered by neither a decision nor a limit
line:

1. **Contrast over a moving ground.** TC-D8's method ("measure the pixels under the letters," at
   "darkest and lightest point of its ground") is a single-frame test. The pack's own
   applicability list includes `video`, where the ground under a text overlay changes throughout
   the shot. No decision or limit line says whether to test contrast at every frame, at the worst
   frame, or only at the still key frame — a real gap for a 15–30s vertical film, not just the
   already-disclosed "no hold duration" limit.
2. **Platform safe-zones for vertical video text.** TC-D7 gives placement zones (centre,
   off-centre, edge) and a phone-delivery-size check, but nothing addresses the UI overlays
   (captions, username, engagement buttons) that Instagram Reels/YouTube Shorts/WhatsApp Status
   place over the bottom and top thirds of a 9:16 frame — a standard "will my text get covered by
   the platform's own UI" question for an Indian D2C vertical ad that this pack does not raise
   even as a limit line.

## Mechanics

- `python3 canon/validation/canon_done.py --pack typography_and_copy` → `status 'PROPOSED...' · seed 29 · cited 29 · missing 0`
- `python3 canon/compilation/compile_pilot_packs.py --only typography_and_copy --check` → `check OK: 1 pack(s) recompile byte-identically`
- `python3 canon/validation/validate_compiled_pack.py` (repo-wide, run once for visibility only — not depended on for this pack's verdict) → all 11 deliverables PASS at time of this check, including `PACK-typography_and_copy-v0.yaml (11 decisions, 62 sk objects, 2495/2500 terse tokens)`; no error from another builder's in-progress pack was present at check time.

## Session-token estimate

About 45k tokens (claim fetches in 4 batches by id, no whole-file reads, no re-fetches).
