# Checker report — critique_and_effectiveness (CE)

Checker: independent session, did not build this pack. Branch `work/canon-done-2026-09-22`
(unchanged). Compiler run only with `--only critique_and_effectiveness`.

## Verdict: PASS (adoptable as is)

All 10 decisions read as SUPPORTED against their cited claims. No hardened hedges, no
default-level rules beyond what the cited ids state. Operationalisations (grunt-test counting,
grayscale test, one-viewing get, delivery-size visibility) are confined to `check` lines, exactly
as the builder represents. Mechanics green for this pack.

## Decision table

| Decision | Verdict | Note |
|---|---|---|
| CE-D1 | SUPPORTED | sb_0015 grunt test, hea_0009/0008 proverb-not-sound-bite, whip_0015/0004/0003 one-point/dilution, hop_sa_0026 picture-earns-space — all matched near-verbatim. |
| CE-D2 | SUPPORTED | "recall appears uncorrelated with purchase" preserves ogx_0031's own "there appears to be no correlation" hedge. ogl_0021 "seldom the same," ogl_0014 "no dull products only dull writers," ogx_0041 in-use/food-in-motion/close-ups, mla_0064+hop_sa_0014 amusement/typical-buyer, ogx_0038 celebrity/cartoon/vignette all matched. Scope (1983 US TV) not restated per-decision but carried at pack_limits level — same pattern used pack-wide, not a violation. |
| CE-D3 | SUPPORTED | ogx_0009 specifics-over-superlatives, hea_0012/0016 concreteness ("only way," kept unhardened), ogx_0007 flag-the-buyer, whip_0031 exaggeration-on-a-truth, whip_0033/0029 exclamation/pun bans — all traced to source wording. |
| CE-D4 | SUPPORTED | "judged on brand-preference change" is ogx_0031's own frame; "name by 10 s" is ogx_0039's literal instruction ("use the name within the first ten seconds"); "end on the pack" fairly paraphrases the reported package-ending finding. hea_0011 gap/fill, murch_0013 release-order, fre_0025/0024 still-reveal/scale-floor, vig_0013 retouch-not-replace all matched. |
| CE-D5 | SUPPORTED | sb_0008/whip_0015 hero/guide, whip_0011 conflict-required, sb_0012 stakes-dosed-like-salt, sb_0014 three-questions, sb_0004/hea_0018 pre-order/rehearse — matched. |
| CE-D6 | SUPPORTED | ogx_0042 supers/on-camera/music/effects/jingle test, gote_0048 sound-faster-than-picture, conv_0007 "seems to" kept, conv_0023 opening-register fault, conv_0019 withdrawn-dialogue — all matched with hedges intact. |
| CE-D7 | SUPPORTED | whip_0058 interesting-first/register, whip_0005 clear/clever overlap, ogx_0043 19–40% miscomprehension figure exact, ogx_0032 "can now sell... unless you are one of the few" kept, murch_0020 how-they-felt, ppm_0001 respect/context/delight (near-verbatim), nnn_0052 originated-not-translated. CF-03's "unless the brief asks... record it" is the pack-wide DOCTRINE_DEVIATIONS convention (used identically in camera_and_spatial_grammar and colour_and_visual_register for their genre exceptions), not an invented condition. |
| CE-D8 | SUPPORTED | gote_0004/0006 new-info/motivated-departure, gote_0053/0052 describe-aloud vs 3-second norm, gote_0031 "it is often said" dissolve register kept as hedge, gote_0037 fade/audio-first, alt_0014 camera-as-eye, gos_0006/0007 constant rules/exit-left-enter-right, gote_0017 break-shot remedy — matched. |
| CE-D9 | SUPPORTED | alb_0006 "almost never" kept, alb_0011 most-relative-medium, alb_0018 few-judge-value, alt_0015/0018/0022 tonal separation/genre-key/dramatic-line, sam_0021 text-over-image contrast, alb_0005 differentiated-letters/all-caps, vig_0009 contrast-not-impact ("never" is the source's own word), fre_0017/0008 zones/long-axis. Grayscale test is check-line only, as claimed. |
| CE-D10 | SUPPORTED | disc_0005/0006 analysis-against-objectives + three-element finding (not reaction, not redesign, not a change list) traced to source's own exclusions. cat_0015 five-property good note, cat_0011 symptom-vs-cause, cat_0017 right-alarm-wrong-diagnosis all matched. murch_0019/0027/0020 sacrifice order and 51%-emotion weight matched. Every disc_*/cat_* clause is said by its own id — none borrowed from an uncited neighbour. |

Counts: 10/10 SUPPORTED, 0 OVERREACH, 0 MISATTRIBUTED, 0 CONTRADICTED.

## Seed coverage

`canon_done.py --pack critique_and_effectiveness` → `seed 63 · cited 63 · missing 0`.

Checked every seed's decision against its full claim text (all 63, across 8 fetch calls): every
one is reflected in the decision's `default` prose, not merely listed in `ids`. **63 CONSUMED, 0
LISTED-ONLY** — matches the build note's own mechanical check.

## Waivers and conflicts

**Waivers whose partner is itself a seed claim: 0 of 37** (checked by script intersection against
the 63-seed set from `HAND-RETRIEVED-CLAIMS`/`CANON-V1-LIVE37-COVERAGE` contributors). No seed is
waived away from its own decision.

Sampled 10 non-seed waivers in full (hop_sa_0008→0014, murch_0011→0019, ogl_0020→0014,
whip_0013→0011, whip_0053→0003, mla_0010→0064, sb_0017→0012, vig_0011→0009, disc_0032→0005,
gos_0008→0007). All 10 correctly reasoned: each partner's content is either orthogonal to what the
decision consumes (format practice, hierarchy precondition, timelessness credo, sight-lines vs.
movement) or is a harder/contradicting framing the builder deliberately did *not* fold in (sb_0017's
"rules that cannot be broken" against the softer sb_0012 the decision actually uses; disc_0032's
approval-gate, which GUARD-contradicts disc_0005, correctly scoped out to "the Controller's step,
outside this pack"). None would change its default if consumed. **0 waivers judged WRONG** in
sample + full seed-overlap check.

Conflicts (8): all resolution_rules trace to the cited pair's own text. On the specific question —
**CF-05 (gos_0007/0012)**: honest, not a dodge. gos_0012 is a real GUARD-contradiction of gos_0007
(jumping the line reverses maintained screen direction), but it is bound to a "frozen regression
trio" (0007/0010/0013) per the build note; citing it would pull two more claims this pack doesn't
need. The resolution_rule's actual content — "crossed line = fault... unless a shown change or a
break shot" — is fully sourced from the ids CE-D8 *does* cite (gos_0007's own maintained-direction
rule and gote_0017's break-shot remedy), not from 0012's uncited text. Naming without citing, with
the reason stated in the build note, is the same convention used for CF-02/04/06/08 and for
alt_0011/gote_0021 in camera_and_spatial_grammar — a disclosed pack-wide practice, not specific
evasion.

## Missing questions

1. **Still-image scope for time-based decisions.** Pack applicability declares `static_image` and
   `image_sequence` alongside `video`, but CE-D4 (10-second name/pack-ending attribution), CE-D6
   (audio), and CE-D8 (cut-by-cut editing) are entirely duration- and motion-based in their cited
   content. No decision or pack_limits line says which of the 10 decisions a producer checking a
   single still or a carousel should even apply. A real Indian-ad producer building a static
   Instagram creative would ask this and get no answer here.
2. Pack_limits already and honestly flags: no 9:16/sound-off-autoplay/sub-10s/thumb-stop coverage,
   no ASCI/category-code coverage, no pre-testing or emotion-quantification coverage. These are
   real gaps but are disclosed, so not "missing" — they are correctly limited rather than silently
   absent.

## Mechanics

- `python3 canon/validation/validate_compiled_pack.py`: `PASS PACK-critique_and_effectiveness-v0.yaml (10 decisions, 74 sk objects, 2494/2500 terse tokens)`. (Repo-wide run FAILs on `composition_and_attention` — another session's pack, out of scope here, not touched.)
- `python3 canon/compilation/compile_pilot_packs.py --only critique_and_effectiveness --check`: `check OK: 1 pack(s) recompile byte-identically`.

Session-token estimate: ~55k tokens (63 seed claims + ~15 waiver/conflict-partner claims fetched
individually via `pack_seed.py --claim`, no whole-file reads).
