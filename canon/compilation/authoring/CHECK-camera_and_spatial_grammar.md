# Checker report — PACK camera_and_spatial_grammar (CG)

Checked against `canon/compilation/authoring/PACK-camera_and_spatial_grammar.authoring.yaml`,
`BUILD-NOTE-camera_and_spatial_grammar.md` and all 73 cited/partner claims fetched in full by id
(decisions, conflicts and waivers). USD 0.

## Verdict: PASS WITH EDITS

Sentence-level support is strong across the pack — every decision's clauses trace to their cited
claims. Four concrete text edits and one scope finding:

1. **CG-D8**: "Music channels an emotion the film has already created, **never** supplies one
   (conv_0007)" — `sk_conv_c003_0007`'s own words are "music **seems to** function best when it
   channels an emotion... **rather than** supplying one," and its caveat: "'seems to' and 'best'
   are both hedges; this is stated as a tendency, not a rule." Change "never" to "seldom" or
   "rather than." (This is the identical clause the sibling pack `editing_pacing_and_short_form`
   flagged and fixed on its own EP-D8; CG-D8 carries the unfixed wording on the same claim.)
2. **CG-D6**: "its register is languid and sombre — romantic or sad passages **only** (0031)" —
   `sk_gote_c003_0031` says dissolves "are **effective in** romantic or sad sequences," with no
   exclusivity claim. Drop "only."
3. **CG-D7**: "a met higher criterion hides a failed lower one, **not the reverse** (0028)" —
   `sk_murch_c003_0028`'s own text: "**the general principle seems to be**..." — a hedged
   tendency, not the flat rule CG-D7 states. Soften to "usually hides."
4. **CG-D4 / CF-04**: the condition "across three or more staged planes" attached to
   `sk_alt_c003_0017` (in both the CG-D4 default and CF-04's `resolution_rule`) is not in
   0017's fetched text, which only says "the spot that should appear most distant should be the
   lightest" — no plane-count is stated anywhere in 0015 or 0017. Either find the textual basis
   or drop the "three or more" qualifier.

## Decisions (8)

| Decision | Verdict | Note |
|---|---|---|
| CG-D1 | SUPPORTED | Outside-in (gos_0017), coverage (gos_0001), best-angle-per-beat (murch_0009, conv_0027), director-owns-lens (ms_0003), lens/face (conv_0025) all match cited text. The two Alton seeds (alt_0018 key-of-picture, alt_0022 level-follows-drama) are genuinely consumed but see scope finding below. |
| CG-D2 | SUPPORTED | Constant world rules/frame edges (gos_0006/0005), line via sight-line/movement (0009, gote_0054), one-side arc (gos_0010), far-side reversal (0012, gote_0055), exit/enter (gos_0007), continued movement (gote_0017), side-of-frame (0018), bridge (0016), creative exception (gos_0013) all match. |
| CG-D3 | SUPPORTED | Sight-line (gos_0008), eye-line payoff (0016), single keeps side (0011), reciprocal match (gos_0015, gote_0056) all match. |
| CG-D4 | SUPPORTED | Neutral-hat/presence (conv_0015), most-surfaces angle (alt_0010), tonal separation either direction (0015), distance-is-lightest progression (0017, CF-04 resolves the contradiction — but see edit 4), shadow/mirror (0016) match. |
| CG-D5 | SUPPORTED | Motivated move/stillness (ms_0002), too-much-movement (alt_0014), hide move behind action (0010) vs static-wide (0017, CF-03 resolves by scene type), colour anchors attention (0016), no rack focus (0019), two-lighting move (alt_0021) all match. |
| CG-D6 | OVERREACH (edit 2) | Order/rate of info (murch_0013), info-in/motivation-out (gote_0004/0006), cut-by-default 3 conditions (0027), 30° rule (gos_0014), dissolve-reads-by-duration (0028), fade-bounds-programme + audio-under-black (0037), describe-aloud/fast-cut split (0053/0052, CF-05) all SUPPORTED; only the "only" on 0031 overreaches. |
| CG-D7 | OVERREACH (edit 3) | Six-criteria/aim-for-all (0019/0031), emotion-outweighs-five (0020: 51 > 23+10+7+5+4=49), sacrifice-upward (0027), creative-exception (gos_0013) all SUPPORTED; only "not the reverse" on 0028 overreaches. The "for me"/narrative-film hedge on Murch's six is correctly carried as CG-D7's own limit line, not dropped — see item (c) below. |
| CG-D8 | OVERREACH (edit 1) + scope finding | Sound-creates-reality (0048), same-place continuity/perspective (gote_0019), source-music route (conv_0009), withdraw-dialogue (conv_0019), opening-cue-mismatch (conv_0023) all SUPPORTED at sentence level; "never" on conv_0007 overreaches. See (a) below for the deeper scope question. |

Counts: **SUPPORTED 5** (D1–D5) · **OVERREACH 3** (D6, D7, D8) · **MISATTRIBUTED 0** · **CONTRADICTED 0**.

## (a) Sound/music and Alton seeds "at the edge of camera grammar"

**CG-D8** ("what does the soundtrack do for the space the camera shows") cites 6 claims, of
which 2 are actually about space (`gote_c003_0019` — sound/perspective continuity across a
same-place cut — and, loosely, `gote_c003_0048` — the ear-helps-the-eye framing line). The other
three seeded claims — `conv_c003_0007` (music channels an existing emotion), `conv_c003_0019`
(withdrawn dialogue reads as speech), `conv_c003_0023` (opening-cue mismatch is a fault) — are
general film-music/sound craft with **no spatial content**; nothing in their text concerns camera
position, cuts, or the space the camera shows. Each is genuinely **CONSUMED** (drives real default
text, not a bare id), so this is not a LISTED-ONLY problem — it is a **forced question**: the
build note itself admits the reason is that "the injection contract assigns AUDIO_AND_EDIT to this
pack as well as editing." That is honest about *why*, but doesn't make the content on-topic. Worth
noting: `editing_pacing_and_short_form`'s own EP-D8 independently seeds the *same three ids*
(gote_0048, conv_0007, conv_0019) — i.e., this content is double-seeded across two packs under two
different questions.

**CG-D1**'s two Alton seeds (alt_0018 genre-sets-the-key, alt_0022 level-follows-the-dramatic-line)
are lighting/mood claims bundled into a shot-size/lens/key planning question. The limit line
("Alton's key categories are 1949 genres — the order transfers, not the table") shows the builder
is aware of the stretch and correctly declines to import the genre table itself. This is a thinner
connection to camera/spatial grammar than the rest of CG-D1, but it is disclosed rather than
hidden — a defensible, if edge-of-domain, reading, unlike CG-D8's three off-domain sound seeds.

## Seed coverage

`canon_done.py --pack camera_and_spatial_grammar` → **seed 25 · cited 25 · missing 0**. All 25
seeds are **CONSUMED** (content drives default/check text) — **none LISTED-ONLY**. This includes
the 6 seeds flagged in (a): consumption is real, the finding there is about domain fit, not
nominal citation.

## Waivers (15) — none WRONG

Checked each partner's fetched text against what the decision actually consumes. All 15 hold:
each partner addresses a different axis from what its ref claim is cited for (rig vs. geometry,
checklist vs. lighting fact, set-construction vs. in-frame remedy, sound-level vs. frame-side,
overuse-bound vs. routing, invisibility-test vs. motivation-rule, etc.) and would not change the
stated default. **Closest call**: `sk_murch_c003_0019 qualified_by sk_murch_c003_0011` — 0011's
film-relative "bad bit" criterion genuinely tensions with the six-criteria ranking (both claims'
own caveats flag this). CG-D7 only consumes 0019 for the ranked tie-break among candidate cuts,
not the bad-bit-removal criterion itself, and the narrative-film scope is separately carried as
CG-D7's limit line — waiver holds, but it is the one worth a second look.

## Conflicts (7) — resolution rules supported, with one caveat

CF-01, CF-02 (gos_0007/0010 vs 0012), CF-03 (ms_0017 vs 0010), CF-05 (gote_0053 vs 0052), CF-06
(gote_0019 vs 0021), CF-07 (alt_0018 vs 0011) all separate their claims by conditions the claims'
own text supports. **CF-04** (alt_0015 vs alt_0017) is resolved by a "three or more staged planes"
condition not present in either claim's text — see edit 4.

## (c) CG-D7 vs. Murch's own scope

Murch's six-criteria list is self-scoped — `sk_murch_c003_0019`: "An ideal cut **(for me)**..." —
and its caveat notes the framework is for narrative film. CG-D7 does not drop this hedge into the
default text; instead it is correctly carried as CG-D7's own limit line ("Murch's six are scoped
'for me' and to narrative film; product-film transfer untested"). Applying the six only as a
tie-break for *this pack's own* spatial rules (line, side of frame, 30°) — not importing the whole
editing framework — is a tight, defensible use. This is honest; the only overreach in CG-D7 is the
narrower hedge-drop on 0028 (edit 3), unrelated to the "for me"/narrative scoping.

## Missing questions

Neither a decision nor a limit line answers: **what motivates a camera move or cut on a
product-only beat with no talent** (e.g., a turntable/rotation shot common in Indian D2C product
ads)? CG-D5's move/hold defaults (ms_0002, 0010, 0016, 0017, 0019) are all stated for actors or
actor-adjacent staging (arguments, reflections, blocking); CG-D4 covers angle/depth on a product
but not motion. Pack_limits flags "no camera default for a product alone" for line/eye-line/
reciprocal rules specifically, but that disclaimer does not extend to CG-D5's move/hold question,
which is silently left unanswered for the product-only case.

## Mechanics

- `python3 canon/validation/canon_done.py --pack camera_and_spatial_grammar` → `status
  'PROPOSED...' · seed 25 · cited 25 · missing 0`.
- `python3 canon/compilation/compile_pilot_packs.py` (full run, not `--only`) → `wrote
  canon/compilation/PACK-camera_and_spatial_grammar-v0.yaml (8 decisions, 58 sk objects, 2498
  terse tokens, 42430 bytes)`; `git status` before and after was clean — the run reproduced
  committed bytes exactly for every pack, so no other builder's in-progress work was disturbed.
  Flagging per the brief's caution: re-run with `--only camera_and_spatial_grammar` in future
  checks rather than the bare command.
- `python3 canon/validation/validate_compiled_pack.py` → `PASS PACK-camera_and_spatial_grammar-v0.yaml
  (8 decisions, 58 sk objects, 2498/2500 terse tokens)`; overall `PASS: all compiled-pack checks
  hold.`

Session-token estimate: ~40k (brief + yaml + build note ~5k; 73 claims fetched in 4 batches ~28k;
mechanics runs ~2k; writing this report ~5k).
