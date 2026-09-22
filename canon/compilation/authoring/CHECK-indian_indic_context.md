# Check — indian_indic_context (IN)

**Verdict: PASS (adoptable as is).**

The pack under-claims rather than over-claims. Every decision I traced carries the source's own
hedges into the default text; the one place a critical checker would expect hardening — the
dpci_0190 "filmi is a thing of the past" expiry notice on the sari/prop/character-type codes — is
written into IN-D3's default text itself ("deliberate period codes, never the current default"),
not left as a passive citation. IN-D4 explicitly refuses to default frontality for a product ad.
IN-D6 states ASCI as an institution plus the 2007 cable sanction and nowhere states a rule.

## Decisions

| id | verdict | note |
|---|---|---|
| IN-D1 | SUPPORTED | nnn_0052 (origination vs translation), dpci_0130 ("rarely use text"/"cultural barrier" — exact quotes), ppm_0001/ppm_0030 credo/structure — all matched, all hedged ("a credo", "asserted"). |
| IN-D2 | SUPPORTED | rbwl_0170 "no longer wise" quoted correctly; jgb_0040 pre-press-rejection claim matched; rbwl_0090 caveated "over-prediction cases only" mirrors source's own asymmetry caveat; rbwl_0120 correctly splits "keep the unbundling mechanism, drop the DNA framing" per the source's own instruction; dpci_0090 star-recognition bound to culture matches stage-two boundary exactly. |
| IN-D3 | SUPPORTED | dpci_0070/0120/0040/0030 content matched claim-for-claim (sari colour code, character types, prop list, "glamorous realism"). Confirms brief item (a): dpci_0190's expiry notice is carried into the *default* text, not merely cited — "their 'filmi' style is 'a thing of the past' by 2002 ... deliberate period codes, never the current default." |
| IN-D4 | SUPPORTED | jgb_0010/0130 frontal-gaze mechanism and its devotional-belief precondition matched; dpci_0020/0010 frontality-as-reading-category and Dwyer's own bounded darshan endorsement matched. Confirms brief item (a) for D4: default is "decide per shot... do not default a product ad to frontal" — the corpus is not stretched into a frontality rule. |
| IN-D5 | SUPPORTED | ppm_0031, nnn_0041/0040/0042/0043 all matched, including nnn_0041's own caveat flagging the 0042 tension (used as CF-01). |
| IN-D6 | SUPPORTED | nnn_0012 confirms: institution (1985, UK model), CCC/BoG mechanism, 2007 Cable TV Rules sanction — no ASCI rule content anywhere. Confirms brief item (b): "check outside Canon" is the only clearance instruction; nothing is smuggled in. nnn_0013 (AWBI, censor cert) and nnn_0011 (gori→nikhri, "not endorsed") both matched. |

No OVERREACH, MISATTRIBUTED, or CONTRADICTED found.

## Seeds

| seed | decision | status |
|---|---|---|
| sk_dpci_0040 | IN-D3 | CONSUMED (full prop enumeration reproduced) |
| sk_dpci_0070 | IN-D3 | CONSUMED (colour code + cinematic use reproduced) |
| sk_dpci_0120 | IN-D3 | CONSUMED (type code + "not universally recognized" quoted) |
| sk_nnn_0052 | IN-D1 | CONSUMED (origination/translation distinction reproduced) |
| sk_ppm_0001 | IN-D1 | CONSUMED (credo content reproduced, not just named) |

`canon_done.py --pack indian_indic_context`: `seed 5 · cited 5 · missing 0` (exit 2, PROPOSED — expected).

## Waivers (item c) — all judged CORRECT

Fetched all 5 partners: jgb_0180 (Jain's own evidential-bound statement — types 0010 as interview
narrative, doesn't change the constraint), rbwl_0040 (middle-class sizing debate — IN-D2 only
needs the naming instruction, not the sizing argument), rbwl_0060 (value-orientation segmentation
model — same reason), dpci_0110 (overpainting, a closed 1970s–80s craft, its "secular darshan"
explicitly weaker than the bound IN-D4 already applies), dpci_0100 (Bachchan-specific star-portrait
carrier — IN-D3 only draws the clothing carrier, 0070, already cited). None would change its
decision's default if consumed. No waiver judged wrong.

## CF-01 (item c)

sk_nnn_0041 vs sk_nnn_0042 confirmed as a genuine, source-acknowledged conflict — nnn_0041's own
caveat states "this claim and the reported Cogito aura finding (sk_nnn_0042) pull in different
directions and the source reconciles them nowhere." The resolution_rule separates them by
question (0042 = which star/aura, 0041 = how the star is used/character-casting), a split the
claims themselves support, and correctly notes neither is measured. Sound.

## Missing questions (item 4)

Not answered by any decision or pack-limit line, and plausible for a 2026 Indian product-ad
producer:
1. **National symbols** — no line on flag, national emblem, currency or map-of-India depiction
   restrictions (a real legal-clearance question, adjacent to IN-D6 but absent from it and from
   pack_limits).
2. **Skin-tone / colorism casting guidance** — IN-D3 covers dress/prop/setting codes in detail but
   the pack is silent on how to cast/render skin tone; "body norms" in pack_limits gestures at it
   but does not name it.

Everything else a producer would ask (Hinglish, non-Hindi scripts, voice-over language, festival
colour beyond Diwali, family/gender norms, menswear, humour by region, A14 typography) is already
named explicitly in `pack_limits`.

## Mechanics

- `canon/validation/canon_done.py --pack indian_indic_context` → `seed 5 · cited 5 · missing 0` (exit 2, expected for PROPOSED).
- `canon/validation/validate_compiled_pack.py` → `PASS PACK-indian_indic_context-v0.yaml (6 decisions, 27 sk objects, 2463/2500 terse tokens)`. Overall run: `FAIL (1 error)` — sole failure is `critique_and_effectiveness` (GAP-11, sk_disc_0005/0003), a different builder's pack, not this one.
- `canon/compilation/compile_pilot_packs.py --only indian_indic_context --check` → `check OK: 1 pack(s) recompile byte-identically`.

## Session tokens

~55k tokens (seed packet, five `--claim` batches covering all 27 cited ids plus 5 waiver
partners, three mechanics runs).
