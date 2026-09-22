# Check — PACK-commercial_communication (CC)

Verdict: **PASS** (adoptable as is).

## 1. Decisions → verdict

| Decision | Verdict | Note |
|---|---|---|
| CC-D1 one message | SUPPORTED | hea_mts_0009/0008 ("proverbs are the ideal," not sound bites); whip_0004 (three things = three ads); abcd_0017/0018 tension resolved per CF-04 (engagement inside the point); sb_0015/0018 (grunt test, "buy the products they can understand the fastest"). |
| CC-D2 CTA/objective | SUPPORTED | abcd_0022 (core-then-tailor two-stage rule); 0020 ("intentional," tied to objective); 0019 (four vehicles incl. story scene); 0021+0014 (voice-over pairs on-screen CTA, audio-heard premise); 0026 (full-funnel CTAs throughout, more direct). |
| CC-D3 brand presence | SUPPORTED | abcd_0011 (from start, never lapsing) + 0010/0013/0022 (early/often/richly, vary asset by message/objective) + 0012/0014 (say and show); ogx_0039 (name in 10s, end on pack, misattribution risk); abcd_0026 (full-funnel open-mixed/end-product). |
| CC-D4 hero | SUPPORTED | ogl_0014 + ogx_0041 (product hero, in use/end-result/close-up); hop_sa_0026 (picture earns its space, sized by importance); sb_0008 + whip_0015 (customer hero, brand archetype/guide, one adjective); ogl_0021 (sell not style). |
| CC-D5 conflict/stakes | SUPPORTED | whip_0011 ("cuts to the end of the movie") + 0013 (deprivation beats presence); sb_0012 (stakes named, salt-dosed); sb_0014 (want/obstacle/either-way test); sb_0004 (story pre-orders message); hea_mts_0018 (mental flight simulator). |
| CC-D6 opening | SUPPORTED | ogx_0040 (open with the fire, visual burr, scene-parade below average); abcd_0006/0007/0005 (jump in, mid-action/close-up, hook+sustain); hea_mts_0011 (surprise decays, gap-fill). mla_0010 used for "curiosity activates most" is the general sentence in that claim ("No other activating factor compares with curiosity") but its scoped condition is gift/premium disclosure, not ad openings — read literally the general clause supports the default; flag as a thin stretch, not enough to fail. |
| CC-D7 claims/lines | SUPPORTED | ogx_0009 (specifics vs Brag-and-Boast); hop_sa_0014 (no boasting, typical buyer); ogl_0016 (good not better, among good rivals); hea_mts_0012/0016 (concrete, one individual); ogx_0034/0038 (unpolished user vs celebrity, both "below average" language kept literal); whip_0031 (exaggeration on a truth); whip_0005/0007 (clear/clever overlap, wit as partial travel); whip_0029/0033 (no puns/rhymes, no exclamation marks). |
| CC-D8 humour/register | SUPPORTED | whip_0058 (interesting first, funny is an accent, no slapstick on a hospital); mla_0064+hop_sa_0014 (amusement banned, money is serious — matches hop_sa_0014's own third prohibition); ogx_0032 (dated reversal, bounded to the very few); abcd_0018/0017 (braked by focus, per CF-04); ogx_0038 (cartoons/vignettes). |
| CC-D9 audience/language | SUPPORTED | hop_sa_0014/0008 (typical buyer, salesman standard); hop_sa_0031 (headline hails only the interested); ogx_0007 (word or city flags the reader); hop_sa_0043 (limited-class offer); nnn_0052 (origination vs translation — default's "separates language from idea" is near-verbatim nnn_0052's source_stated_problems); ppm_0001 (respect/context/delight, not intimidate). |
| CC-D10 audio layer | SUPPORTED | ogx_0042 (on-camera > VO, supers match spoken words verbatim, music null, jingles below average); abcd_0021+0014 (CTA super voiced, audio-heard premise); abcd_0012 (brand name spoken); abcd_0026 (full-funnel audio hook). |

**Item (a) — CF-03 judged correct.** No stored GUARD relation links sk_mla_0064 and sk_ogx_0032, but ogx_0032's own text names and reverses the identical claim: it quotes "Claude Hopkins... thundered, 'People don't buy from clowns'" — the exact line mla_0064 states ("People do not buy from clowns") — and says the reversal is dated and bounded to "very, very few writers." The contradiction is genuinely in the claims' content, not string-matched by the compiler; `kind: contradicts` without a stored relation is justified here. The resolution_rule's "brief clause" framing is the compiler's own operationalization (not sourced verbatim from either claim) but does not misstate either side and is consistent with the same pattern used at CF-05/CF-07.

0/10 OVERREACH, 0/10 MISATTRIBUTED, 0/10 CONTRADICTED, 10/10 SUPPORTED (one noted as a thin-but-defensible stretch on mla_0010 in CC-D6).

## 2. Seed coverage

`canon_done.py --pack commercial_communication`: **seed 41 · cited 41 · missing 0.**

Checked every seed id listed in the build note against its decision's default text (all 41): every one is reflected by specific, attributable content in the prose, not merely listed in the `ids:` array. **CONSUMED: 41/41. LISTED-ONLY: 0.** (Non-seed ids added for closure — e.g. hea_mts_0008 and whip_0058 inside CC-D7's id list — are GUARD-relation closures, matching the build note's own accounting, not free-floating citations.)

## 3. Waivers — all 7 checked, none WRONG

- hop_sa_0026→0021 (depends_on): 0021 is Hopkins' epistemic ground ("mail order is the severest test... figures which do not lie") — meta-claim about evidential authority, not about pictures/heroes. Would not change CC-D4's default.
- ogl_0014 contradicts 0020: 0020's content is direct-response format practice ("two-minute rather than thirty-second," "late-night," "long copy") — unrelated to hero framing. Would not change CC-D4.
- whip_0005 qualified_by 0016: 0016 is brief-writing precision (vague/too-precise strategy, Dru's "could this exist without the brief" test) — a decision point before CC-D7's execution-level craft. Would not change the default.
- whip_0004 depends_on 0003: 0003 is print layout-reduction arithmetic ("get it down to one thing" via composition) — composition-pack territory, not the message-count rule CC-D1 states. Would not change it.
- whip_0004 qualified_by 0061: 0061 is entirely client-revision defence tactics (post-brief). CC-D1 decides at brief time. Would not change it.
- ogx_0038 depends_on 0031: 0031 supplies the brand-preference-vs-recall measurement basis behind "below average." CC-D7/D8 already use the source's own "below average" language; consuming 0031 explains why, not what. Would not change the defaults.
- ogx_0042 depends_on 0031: same reasoning, for CC-D10's jingle judgement. Would not change it.

Conflicts (8) spot-checked for resolution_rule support: all separate their two claims by a condition the claims' own text carries (CF-01 temporal: surprise-then-name-by-10s; CF-02/CF-03 by mla_0064's own trades_off/contradicts language; CF-04 abcd's own "avoid doing too much" brake; CF-05 by ogl_0021's "if it doesn't sell it isn't creative"; CF-06 by sb_0017's own caveat conceding tension with sb_0012's dosing; CF-07 by ogx's stored trades_off relation; CF-08 by whip_0001's stored trades_off with whip_0007/0005). None unsupported.

## 4. Missing questions

Domains covered are thorough for message/CTA/brand/hero/conflict/credibility/humour/audience/audio. Two concrete producer questions neither a decision nor a limit line answers:

- **Price, discount and offer-display conventions** (MRP, "flat X% off," EMI, rupee formatting) — CC-D7 covers claim specificity generically (percentages, time, money saved) but nothing addresses how a price/offer clause should be phrased or verified for an Indian product ad, despite this being a near-universal element of Indian commercial creative.
- **Interactive/platform CTA vehicles specific to Indian short-form funnels** (WhatsApp-order, swipe-up/link-sticker, call-now) — CC-D2/CC-D9 give the CTA-clarity and audience-hailing rules but the four named CTA vehicles (abcd_0019) are generic (written/graphic/audio/story-scene); nothing treats the platform-native tap targets that dominate 9:16 Indian D2C ads, and this isn't named in the pack_limits either (the limits cover 9:16 format and sound-off viewing generally, not CTA mechanics on that format).

## 5. Mechanics

- `validate_compiled_pack.py`: `PASS PACK-commercial_communication-v0.yaml (10 decisions, 58 sk objects, 2498/2500 terse tokens)`
- `compile_pilot_packs.py --check --only commercial_communication`: `check OK: 1 pack(s) recompile byte-identically`
- `canon_done.py --pack commercial_communication`: `seed 41 · cited 41 · missing 0`

Session-token estimate: ~95k.
