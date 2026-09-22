# Check — pilot pack extensions (product_appearance, composition_and_attention)

Diff checked: `git diff 41c58ab..534bc73` on the two authoring files. Scope: only the extension
(new/rewritten defaults, checks, conflicts, waivers, pack_limits added today). PA-D1..D10 /
CA-D1..D11's original content, as accepted in the pilot, is out of scope except where the diff
shows a rewrite.

## Verdict

- **product_appearance: PASS WITH EDITS.**
- **composition_and_attention: PASS WITH EDITS.**

Neither fails: every new/rewritten clause I traced to its cited ids is SUPPORTED, all waivers
judged hold up, tightening did not drop a hedge or flip a meaning, and the coverage-delta lines
are true. The edits below are about decision shape (folding), not claim support.

## 1. Clause-by-clause (new/rewritten only)

| Decision | Verdict | Note |
|---|---|---|
| PA-D7 (ext.) | SUPPORTED | hop_sa_0014 says exactly "one imagined typical buyer... do what he would do face to face... do not amuse/boast/show off" — matches verbatim. |
| PA-D11 (new) | SUPPORTED, one clause flagged | fre_0017 (zone not coordinate), fre_0008 (oppose two elements, long axis), fre_0024 (figure supplies scale, size gated on print/delivered size), fre_0025 (late-found element must stay findable) all match their claims closely. The closing clause — "the camera is the audience's eye; too much movement covers up (alt_0014)" — is SUPPORTED as a claim-fidelity matter (alt_0014 says this verbatim) but answers a different question than PA-D11 asks ("where does the product sit... scale... second read" vs. camera movement). The build note calls this "the one stretch" itself; I'd call the check clause "each move names what it concentrates on" the weak spot — it's the one line in PA-D11 that doesn't cash out into anything the rest of the check tests. Not OVERREACH on the claim, but a bolt-on.  |
| PA-D12 (new) | SUPPORTED | dpci_0040/0070/0120 (props/dress/figure as codes the audience holds) and dpci_0190 (source's own expiry notice, "a thing of the past") match closely; "Hindi-cinema codes to 2002" is accurate to the source's own date. |
| CA-D1 (ext.) | SUPPORTED | Same fre_0024/0025 and dpci quartet as above, correctly folded into "what reads" (scale/findability/coded-reading all bear on read order). |
| CA-D2 (ext.) | SUPPORTED, one clause flagged | sam_0021 (text-over-image value contrast, plays off the image, follows structure beneath) matches verbatim. vig_0013 (established-logo equity) is about *not redesigning* an established mark when asked to — CA-D2's "the supplied mark is placed, never redrawn" is a plausible transfer to a generation-pipeline context but "never redrawn" is stronger than what vig_0013 states (it argues against replacement-for-its-own-sake, not against any alteration ever). Mild OVERREACH in wording, not in substance. |
| CA-D5 (ext.) | SUPPORTED | alt_0015/0017 correctly kept as a scoped contradiction via new CF-18 (subject-against-ground either direction vs. staged depth planes dark-near/light-far) rather than conflated. alt_0018 (genre sets key before any scene; comedy lit high) and alt_0022 (drama follows dramatic line: gay bright, sad low, tragedy deep blacks/glaring whites) match closely. |
| CA-D7 (ext.) | SUPPORTED | murch_0013 (editor's material is order/rate of information release) and ms_0016 (colour tied to figure in earlier closer shot, found blurred) both match. |
| CA-D9 (ext.) | SUPPORTED | gos_0006 ("constant physical rules of direction and distance") matches verbatim. |
| CA-D10 (ext.) | SUPPORTED | gote_0028 (dissolve reads by duration, jump-cut vs. superimposition, never the software default), gote_0031 (dissolves "said to" read languid/sombre — hedge correctly kept as received opinion), gote_0037 (fade bounds act/scene/programme or time-place change), gote_0048 (sound creates reality faster, stimulate ear to help eye) all match. |
| CA-D11 (ext.) | SUPPORTED | alt_0014 matches verbatim, same claim as PA-D11's closing clause — here it fits: CA-D11's question already is "does the camera move, and why." |

No MISATTRIBUTED or CONTRADICTED clauses found in the extension.

## 2. Tightening (PA-D1..D10, CA-D1..D11 pre-existing text)

Spot-checked every rewritten default/check line in the diff. All are compression (dropped
redundant words, `sk_lsm_c003_0001`→`lsm_0001` shorthand, moved a repeated rule into the conflict
entry that already states it verbatim — e.g. PA-D5's "never both on one surface" now lives only in
CF-02, unchanged there). No hedge was dropped: "probably" (fre_0020), "said to read" (gote_0031),
"the source calls it alarming" (gote_0052), "weights hedged, intervals the point" (murch_0029),
"'bad' is film-relative" (murch_0011), "as bad as none" (alt_0014) all survive verbatim in the new
text. PA-D10's check widened from "PA-D1..PA-D9" to "any PA decision" — a deliberate, declared
scope extension to cover D11/D12, not a meaning change to D1-D9. No meaning changes found.

## 3. Waivers

All six judged correct — the partner's content would not change the citing decision's default:

- PA hop_sa_0014→0008: 0008 is the salesmanship analogy 0014 derives from; PA-D7 already states the
  analogy's conclusion via 0026. Consuming 0008 adds nothing new.
- PA/CA dpci_0120→0100 (same waiver, two packs): 0100 is Bachchan-specific star-portrait
  recognition (1970s-80s); PA-D12/CA-D1 only use the character-type-as-code mechanism, which
  doesn't depend on star recognition.
- PA fre_0017→0016: 0016 (rejects placement rules, notes tension with classical proportion) —
  0017 itself already states "any rule of thirds can only be approximate," so the qualification is
  baked into what's cited; the deeper tension is correctly pointed at CA-D2/CF-05 instead.
- CA ms_0016↔0014: trade-off is a lens choice (blur vs. reflection); CA-D7 decides no lens.
- CA alt_0018→0011: 0011 is source-agreement for fictional light placement; CA-D5 decides key/level
  by category only and doesn't touch source agreement — that's PA-D4/PA-CF-03's territory, correctly
  not duplicated here.
- CA CF-13→gote_0035/0012 and CF-17→murch_0025/0026 (converted from pilot conflicts): both checked —
  the partner (30-degree rule; the tradition murch_0025 argues against) is genuinely uncited and
  unconsumed by CA-D7/CA-D8's actual defaults. Converting from conflict to waiver preserves the
  same visibility; nothing is hidden.

## 4. CA's folding into CA-D10, CA-D5, CA-D2

- **CA-D10** ("how long may a shot hold; what joins shots?"): forced. Shot-duration and
  transition-type (dissolve duration/register, fade boundary, audio-first) are two different
  questions bolted together by a semicolon; the build note itself drafted this as a separate
  decision (CA-D14) before folding for budget.
- **CA-D5** ("balance or restless; depth and key in tone?"): most forced of the three. It now
  answers three distinct questions — spatial balance, depth-by-tonal-separation, and lighting-key-by-genre
  across a whole film. The last is a different domain (lighting/mood) papered over by "tone is
  weight" in the build note, which is a stretch justification, not a real unification.
- **CA-D2** ("where do subject, text and mark sit?"): borderline but defensible as one question
  (placement of every element in the frame — subject, type, logo), since all three answers are
  literally "where/how does X sit."

## 5. Coverage-delta lines

Checked against what's actually cited: dwyer-patel (dpci_0040/0070/0120/0190), freeman
(fre_0008/0017/0024/0025), and alton (alt_0014/0015/0017/0018/0022) are now compiled, matching the
"now compiled" claim. jain-gods-in-the-bazaar and carroll-read-this-photographs have zero ids in
either diff — correctly declared uncompiled. samara-grid: only sam_0021 (a different, non-grid
claim) is compiled; the grid/negative-space term (t_sam_0018) stays uncompiled as declared — no
contradiction. hopkins ch8-21: the two new hop_sa ids (0014, 0008) are sourced from
`hopkins-scientific-advertising-ch1-7`, not ch8-21 — the "ch8-21 uncompiled" line is accurate.

## 6. Mechanics

- `canon_done.py --pack product_appearance`: seed 13 · cited 13 · missing 0, exit 2 (PROPOSED).
- `canon_done.py --pack composition_and_attention`: seed 32 · cited 32 · missing 0, exit 2 (PROPOSED).
- `validate_compiled_pack.py`: PASS for both packs (PA 12 decisions/45 sk/2500 tokens; CA 11
  decisions/90 sk/2500 tokens), plus all other structural checks (reproducibility, HOLD-id scan,
  pack-triggers budget) PASS.
- `compile_pilot_packs.py --check --only product_appearance` and `--only composition_and_attention`:
  each "check OK: 1 pack(s) recompile byte-identically."

Session token estimate for this check: ~55k.
