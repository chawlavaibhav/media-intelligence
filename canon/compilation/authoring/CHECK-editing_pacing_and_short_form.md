# Checker report — PACK editing_pacing_and_short_form (EP)

Checked against `canon/compilation/authoring/PACK-editing_pacing_and_short_form.authoring.yaml`,
`BUILD-NOTE-editing_pacing_and_short_form.md` and 59 claims fetched in full by id. USD 0.

## Verdict: PASS WITH EDITS

Two clauses overreach their cited claim by dropping a stated hedge. Everything else — seed
coverage, waivers, conflicts, mechanics — holds. Edits:

1. EP-D6: change "**Prefer** moving attention inside one shot" to "**where possible**, move
   attention inside one shot" (or drop the preference framing). `sk_ms_c003_0010`'s own caveat:
   "the source does not argue that continuous shots are better than cutting in general; it says
   cutting is fine but less flowing." No claim ranks in-shot movement over cutting.
2. EP-D8: change "Score channels an emotion the picture has already created, **never** supplies
   one" to "...**seldom** supplies one" or similar. `sk_conv_c003_0007`'s caveat: "'seems to' and
   'best' are both hedges; this is stated as a tendency, not a rule." The claim text itself is
   "music seems to function best when it channels an emotion... already created" — a tendency,
   not the absolute the pack states.

## Decisions (10)

| Decision | Verdict | Note |
|---|---|---|
| EP-D1 | SUPPORTED | Opening constructions (0007), pacing/framing (0006), hook+sustain (0005), prelude effect (conv_0024), unmet-expectation fault (conv_0023) all match claim text. |
| EP-D2 | SUPPORTED | Information-to/motivation-from (gote_0004/0006), cut conditions (0027), order-and-rate-of-release (murch_0013) all match. |
| EP-D3 | SUPPORTED | Six-criteria ranking (0019), 51%>other-five (0020: 51 > sum of 23+10+7+5+4=49, literally true), aim-for-all-six (0031), bottom-up sacrifice (0027) all match. Limit line correctly carries the claim's own "(for me)"/narrative-film scoping. |
| EP-D4 | SUPPORTED | Describe-aloud duration (0053), felt beat (0009), murch pointing-guide (0018) match. "Sub-three-second norm is no rule" fairly reflects 0052, which attributes the norm to "some producers and directors" and calls it "alarming" — not the source's own rule. |
| EP-D5 | SUPPORTED | Screen direction, action line, crossing-the-line, side-of-frame continuity (0017/0054/0055/0018) all match. |
| EP-D6 | OVERREACH (see edit 1) | Motivation rule (0002), colour pre-establishment (0016), static-wide blocking (0017, scope correctly handled by CF-02), no-rack-focus (0019) all SUPPORTED; only the "prefer" framing on 0010 overreaches. |
| EP-D7 | SUPPORTED | Cut-as-default (0027), dissolve register/duration (0031/0028), fade-as-boundary + audio-under-black (0037) all match. |
| EP-D8 | OVERREACH (see edit 2) | Sound-creates-reality (0048), sound bridge (gote_0007), source-music-route (conv_0009), withdrawn-dialogue (conv_0019) all SUPPORTED; only the "never supplies" framing on conv_0007 overreaches. |
| EP-D9 | SUPPORTED | Early-and-throughout (0011), richly=variety (0010), asset list (0013), core-then-tailor/nothing-dropped (0022 — the "nothing dropped" phrase is inside the claim's own text, its caveat just flags it as inferred by the claim's author, not unstated), full-funnel close (0026) all match. |
| EP-D10 | SUPPORTED | CTA vehicles (0019), objective-tied CTA (0020), CTA+VO pairing (0021), brand+audio pairing (0012), reinforce-not-compete (0008), sound-on/YouTube-only scope (0014, correctly carried as a limit line), full-funnel CTA cadence (0026) all match. |

Counts: SUPPORTED 8, OVERREACH 2, MISATTRIBUTED 0, CONTRADICTED 0.

## Seed coverage

`canon_done.py --pack editing_pacing_and_short_form` → seed 29, cited 29, missing 0. Spot-checked
content (not just id presence) for all 29 seeds against their decisions: all 29 CONSUMED, none
LISTED-ONLY — e.g. sk_gote_c003_0052/0053 (EP-D4) drive both the default text and the CF-01
conflict resolution; sk_murch_c003_0020's 51%-figure is checked arithmetically against the other
five weights (EP-D3); sk_abcd_0014's YouTube-only scope is carried into the EP-D10 limit line, not
just cited.

## Waivers (14) — none WRONG

Checked every partner's fetched text against what the decision consumes. In each case the
partner addresses a different axis (equipment vs. technique content, set-membership vs.
sequencing rule, perceptual justification vs. ranking itself, overuse-bound vs. route-selection,
lens choice vs. colour-identification rule, sound-level vs. frame-side) and would not change the
stated default. Closest call: `sk_murch_c003_0019 qualified_by sk_murch_c003_0011` (bad-bit
criterion is "film-relative" vs. the six-criteria ranking) — genuine tension noted by the source
itself, but EP-D3 only consumes the ranking for choosing among candidate cuts, not the bad-bit
removal criterion, and the narrative-film scope is already carried as EP-D3's limit line. Waiver
holds.

## Conflicts (3) — all resolution rules supported

- CF-01 (gote_0053 vs 0052): conditions drawn straight from the claims — 0053 scoped to
  "informational or establishing shot," 0052's own text exempts "action sequence" from its norm.
- CF-02 (ms_0017 vs 0010): 0017 conditioned on "continuous movement between two people," 0010 on
  "scenes with more than one point of interest" — the resolution's scene-type split matches both
  claims' stated conditions.
- CF-03 (murch_0018 vs 0033): 0018 is about cut frequency ("changes shots too frequently"), 0033
  about in-shot misdirection; 0033's own caveat records the tension with 0018 directly, and the
  resolution's frequency-vs.-placement split is the same distinction the source draws.

## Missing questions (item 4)

None of the four brief-named red flags apply (build note §7 confirms; independently verified).
But for a 15–30s vertical Indian feed ad, three editing/pacing questions get no decision and no
limit line:
1. **Caption/subtitle timing for sound-off autoplay** — pack_limits says 9:16/sound-off transfer
   is "untested," but that is a scope disclaimer, not an answer; no decision or limit addresses
   how long a burned-in caption should hold when it is carrying the audio track's job.
2. **Loop point for looping short-form** (Reels/Shorts autoloop) — not mentioned; EP-D1 covers the
   open and EP-D7 covers transitions, but the seam where the film re-starts is a distinct pacing
   question this domain would own.
3. **Cutdown/multi-duration versioning** (one master edit producing 6s/15s/30s variants) — not
   addressed; every decision assumes one fixed runtime.

## Mechanics

- `python3 canon/validation/canon_done.py --pack editing_pacing_and_short_form` → `seed 29 · cited 29 · missing 0`.
- `python3 canon/validation/validate_compiled_pack.py` → `PASS PACK-editing_pacing_and_short_form-v0.yaml (10 decisions, 45 sk objects, 2497/2500 terse tokens)`; full run green (no other pack failing at time of check).
- `python3 canon/compilation/compile_pilot_packs.py --check --only editing_pacing_and_short_form` → `check OK: 1 pack(s) recompile byte-identically`.

## Session tokens

~130k.
