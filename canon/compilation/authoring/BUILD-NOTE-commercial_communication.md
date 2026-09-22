# Build note — PACK-commercial_communication (CC)

Authority: `coordination/decisions/CONTROLLER-CANON-COMPLETION-2026-09-22.md`. USD 0; no model call.
Files written: `PACK-commercial_communication.authoring.yaml` (this dir) and this note; the compiler
wrote `canon/compilation/PACK-commercial_communication-v0.yaml`. Status PROPOSED.

## 1. Decisions (10)

- CC-D1 One message: one point per execution, core by exclusion, grunt test in five seconds.
- CC-D2 CTA and objective: core principles then weight to the one objective; one CTA, voiced and shown.
- CC-D3 Brand presence: from the start and never lapsing; early/often/richly; name within ten seconds; end on the pack.
- CC-D4 Hero: product is the hero of the picture, customer the hero of the story; judge by selling not style.
- CC-D5 Story conflict and stakes: an opposing force, deprivation, stakes named and dosed, want/obstacle/either-way answerable.
- CC-D6 Opening: surprise in frame one, jump in, hook and sustain, gap opened then filled, one visual burr.
- CC-D7 Claims and lines: specifics not superlatives, no boasting, concrete and individual, real-user testimony, clear/clever overlap, no puns/rhymes/exclamation marks.
- CC-D8 Humour and register: interesting before funny; register from product and audience; humour only under a brief clause.
- CC-D9 Audience and language: one typical buyer, headline hails them only, copy originated in the audience's language with respect.
- CC-D10 Audio layer: on-camera over voice-over, supers = spoken words, name spoken, music null, effects help, jingles below average.

Feeds: alongside the brief's list the pack uses `CORE_CREATIVE_IDEA`, `OBJECTIVE_INTERPRETATION`
and `DETERMINISTIC_OR_NON_GENERATIVE_ELEMENTS`, which INJECTION-CONTRACT §3.4 maps to this pack.

## 2. Seed coverage — 41 of 41 (`canon_done --pack`: seed 41 · cited 41 · missing 0)

D1: hea_mts_0009 · D2: abcd_0019, 0020, 0021, 0026 · D3: abcd_0010, 0011, 0012, 0013, ogx_0039 ·
D4: ogl_c003_0014, ogx_0041, hop_sa_0026, sb_c003_0008, whip_0015 · D5: whip_0011, sb_c003_0012,
0014, 0004, hea_mts_0018 · D6: ogx_0040, abcd_0006, 0007, hea_mts_0011 · D7: ogx_0009, hop_sa_0014,
hea_mts_0012, 0016, ogx_0038, whip_0031, 0005, 0029, 0033 · D8: whip_0058, mla_0064, ogx_0032 ·
D9: ogx_0007, nnn_0052, ppm_0001 · D10: ogx_0042. Non-seed ids added (all read in full): abcd_0005,
0014, 0017, 0018, 0022; hea_mts_0008; hop_sa_0008, 0031, 0043; ogl_c003_0016, 0021; whip_0004,
0007, 0013; mla_0010; ogx_0034; sb_c003_0018. 58 sk objects cited.

## 3. Closure holes and resolution (compiler undirected union)

Cited: abcd_0011↔0026 (both seeds); abcd_0012/0021 depends_on+qualified_by 0014 → cited 0014;
abcd_0013/0020 depends_on 0022 → cited; hea_0009/0012 qualified_by 0008 → cited; hea_0012
qualified_by 0016 (seed); hop_sa_0014 depends_on 0008 → cited; 0008 qualified_by 0031 → cited;
0031 qualified_by 0043 → cited; whip_0011 depends_on 0013 → cited; whip_0015 depends_on 0004 →
cited; whip_0005 qualified_by 0007 and 0058 → cited; abcd_0017↔0018 → cited both.
Conflicts (8): CF-01 ogx_0040/0039 trade-off; CF-02 mla_0064/0010 trade-off; CF-03 mla_0064 vs
ogx_0032 — kind `contradicts` without a stored relation, because ogx_0032 itself names Hopkins'
"people don't buy from clowns" and reverses it (the disagreement is in the accepted claim, not
string-joined); CF-04 abcd_0017/0018; CF-05 ogl_0014/0021; CF-06 sb_0012/0017 (0017 named, not
cited); CF-07 ogx_0038/0034; CF-08 whip_0005/0001 (0001 named, not cited; also closes
whip_0007↔0001).
Waivers (7): hop_sa_0026→0021 (evidential basis, same as product_appearance); ogl_0014 contradicts
0020 (0020's format/copy-length content not consumed); whip_0005 qualified_by 0016 (brief-precision
qualification; pack operates on a given brief); whip_0004 depends_on 0003 and qualified_by 0061
(layout arithmetic and client-revision doctrine not consumed); ogx_0038 and ogx_0042 depends_on
0031 (judgements repeated in the source's own brand-preference terms; the measure not compiled).

## 4. Limit lines

- Coverage delta: Ogilvy TV = 1983 US 30 s broadcast on brand preference; Hopkins = 1920s print/mail order; ABCD = YouTube 2022 publisher guidance, sound on; nothing treats 9:16, sound-off or sub-10 s ads; D3/D6/D10 video-only; audio-only ads uncovered.
- India: only Hindi origination and Pandey's credo compiled; other languages, Hinglish, regional markets, Bijapurkar and Parameswaran's celebrity/ASCI claims not compiled — ASCI checked outside Canon.
- Objective mix: Binet & Field not compiled; no budget split or reach set.
- Devanagari line added by the compiler.

## 5. Deliberately not compiled

- T3 cross-source tension (t_hop_sa_0023 vs t_eic_0008, ledger xj_0021, narrow address vs
  penetration) was authored as CF-09 and cut for the terse budget; the "Objective mix" limit
  names the gap. Worth restoring if the budget is ever raised.
- The "hero" homonym (Ogilvy product-hero vs Miller customer-hero; ledger xj_0027 records them as
  compatible) is handled by scoping inside CC-D4's default from the accepted claims alone; no
  candidate content consumed.
- Binet & Field (28 claims), Bijapurkar, Godin, Sutherland and Parameswaran's celebrity/regulatory
  claims: no seed fell on them and the budget did not allow more decisions; named in limits.
- Two decisions were merged to fit: copy craft (whip_0005/0007/0029/0033) into CC-D7, and
  language/stance (nnn_0052, ppm_0001) into CC-D9. Twelve decisions rendered at 3,592 tokens; ten
  at 2,498. No seed was dropped.

## 6. Terse tokens

2,498 of 2,500 (9,992 chars). Validator PASS; `--check` byte-stable across 4 packs.

## 7. Session tokens (estimate)

About 240k tokens used, of which ~110k reading the seed packet in sections and claims by id.
Note: the shared scratchpad file `seed.txt` was overwritten mid-session by the other builder's
packet; this pack's packet was regenerated to a pack-specific path and the seed set re-verified (41).
