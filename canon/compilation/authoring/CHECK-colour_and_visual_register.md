# Check — colour_and_visual_register (CV)

Independent checker session. Did not build this pack. Verified against
`canon/compilation/authoring/PACK-colour_and_visual_register.authoring.yaml`,
`BUILD-NOTE-colour_and_visual_register.md`, and `canon/validation/CANON-DONE-v0.md`.

## Verdict: PASS

No hardened hedges found (the specific failure pattern flagged for this checker round — "seems
to"→"never", conditions the claims do not state — is absent here). The one place the pack reads
past its sources (CV-D1) is disclosed in `pack_limits` as "this pack's reading," which is the
correct place for it. The one domain-transfer conflict resolution (CV-D7/CF-02) is a compiler
judgment, correctly kept out of the decision `default` and stated in the `conflicts` block where
it can be checked, not smuggled in as a sourced claim.

## Decisions

| id | verdict | note |
|---|---|---|
| CV-D1 | SUPPORTED (flagged reading) | ms_0016: "Color can be used to direct the audience's attention just as effectively as any camera move," identification only "provided the association... was made in an earlier, closer shot." vig_0009: impact "usually... visual vulgarity." Pack's "one saturated element... is the product" is *not* stated by either claim — and `pack_limits` says so explicitly: "No source names a palette size, hue, saturation value... CV-D1 is this pack's reading of ms_0016 and vig_0009." Disclosed, not hidden. |
| CV-D2 | SUPPORTED | ms_0019 "focusing backward and forward... confuses"; matches "never rack focus." |
| CV-D3 | SUPPORTED | alb_0006/0018 language reused faithfully ("almost never," "very few judge lightness"). |
| CV-D4 | SUPPORTED | vig_0011 timelessness/primary colours and vig_0013 equity correctly paired for "identity is the system." |
| CV-D5 | SUPPORTED, domain-stretched (disclosed) | wcag_0038's 3:1 is scoped to "content that distinguishes states, categories or elements by colour" (UI), not product-to-ground image separation. Applying it to a product edge is a transfer; `pack_limits` covers it generally ("wcag_* = Level AA web thresholds... every default transfers untested") but does not name CV-D5 specifically the way it names CV-D1. Minor: could add an explicit flag here too. |
| CV-D6 | SUPPORTED | alt_0025/0022 language matches ("quality of light," "dramatic line"). |
| CV-D7 | SUPPORTED; CF-02 resolution is a judgment call, correctly scoped | alt_0018 vs alt_0011 do contradict in-source (alt_0018's own caveat says so). The "brief-clause override... product ad is not the exempt genre" condition is not stated by either claim — it is the compiler's applicability reasoning, and it is kept in the `conflicts` block, not folded into the `default` as if sourced. Acceptable; conservative direction (defaults to the stricter rule). |
| CV-D8 | SUPPORTED | wcag_0002/0021/0022/0031 content directly reused ("wider strokes read at lower contrast," "never a thin... face"). |
| CV-D9 | SUPPORTED | jgb_0020 matches almost verbatim ("practice outlived its own justification," "makers... denigrate... as... 'gaudy'"). jgb_0090's "rhetoric... does not actually correspond to aesthetically enforced social distinctions" supports "not an enforced taste line." The "never pick saturation by audience class" line synthesizes 0020 (saturation) + 0090 (audience rhetoric unreliable) — reasonable combination, not literal in either alone, but the waiver note owns this explicitly. |
| CV-D10 | SUPPORTED | ogl_0008/0007, vig_0009/0011, ogl_0014/0021 all reused faithfully. |

Count: 10 SUPPORTED, 0 OVERREACH, 0 MISATTRIBUTED, 0 CONTRADICTED.

## Seeds: 23/23 CONSUMED, 0 LISTED-ONLY

Spot-verified ms_0016/0019, vig_0009/0011/0013, ogl_0007/0008/0014, wcag_0001/0002/0007/0021/
0022/0031/0038, alb_0006/0018, alt_0011/0015/0017/0018/0022, jgb_0020/0090, nnn_0052 — each
seed's specific finding is paraphrased into a decision `default`, not merely cited. `canon_done.py
--pack colour_and_visual_register`: seed 23 · cited 23 · missing 0.

## Waivers (20): none judged WRONG

Checked the five most exposed: ogl_0014/ogl_0020 (0020 is direct-response format/copy-length,
unrelated to product-as-hero — correct waive), ogl_0007/ogl_0013+0017 (durability test and
"repeat until it stops selling" are about campaign duration/scheduling, not "same image every
year" — correct waive), alt_0003/alt_0004 (0004 is shiny-prop specular highlights, product_appearance's
territory per the pack's own note — correct waive), jgb_0090/jgb_0180 (0180 types the evidence as
interview narrative, doesn't touch the caution itself — correct waive), alb_0012/alb_0009+0016+0017
(classroom method/grading criterion/pedagogy — the shift-effect itself is what's consumed — correct
waive). No partner would flip a default. **Conflicts**: all 4 resolution rules are separated by a
condition the source claims themselves state or (CF-02 only) an explicitly-scoped applicability
judgment kept outside the `default` — none unsupported.

## Missing questions (domain silence, item 4)

Not named in `pack_limits` or any decision: (1) last-mile colour rendering — how the graded
palette survives WhatsApp/Instagram recompression and phone-display "vivid mode" oversaturation,
the actual viewing condition for most Indian mobile ad delivery; (2) non-Latin script legibility —
CV-D8's contrast/weight rules (thin-face fail, all-caps hardest) are stated for Latin type only;
Devanagari/other Indic scripts with conjuncts and matras have no stated stroke-weight or
contrast-at-small-size guidance.

## Mechanics

- `canon_done.py --pack colour_and_visual_register`: seed 23 · cited 23 · missing 0 (exit 2,
  PROPOSED — expected).
- `validate_compiled_pack.py`: `PASS PACK-colour_and_visual_register-v0.yaml (10 decisions, 61 sk
  objects, 2497/2500 terse tokens)`. Overall run reports `FAIL (1 error)` — that error is
  `concept_and_distinctiveness` (another session's in-progress pack, over its token budget), not
  this pack.
- `compile_pilot_packs.py --check --only colour_and_visual_register`: `check OK: 1 pack(s)
  recompile byte-identically`.

## Session tokens

Roughly 20–25k tokens (brief + authoring yaml + build note read once; ~20 claims fetched by id in
four batched calls; three mechanics commands; no whole-file re-reads).
