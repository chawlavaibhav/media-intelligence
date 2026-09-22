# Build note — PACK camera_and_spatial_grammar (CG)

Authored: `canon/compilation/authoring/PACK-camera_and_spatial_grammar.authoring.yaml`.
Compiled: `canon/compilation/PACK-camera_and_spatial_grammar-v0.yaml` (8 decisions, 58 sk objects,
2,498 terse tokens, 7 conflicts, 15 waivers). All four loop commands green; `canon_done --pack`
exits 2 (PROPOSED, as expected) with `seed 25 · cited 25 · missing 0`.

## 1. Decisions

- **CG-D1** Plan per beat — size, lens, key: outside-in (gos_0017), coverage (0001), best angle per
  beat (murch_0009, conv_0027), director owns lens (ms_0003), lens/face (conv_0025), key decided
  first and level on the dramatic line (alt_0018, 0022).
- **CG-D2** Line of action, screen direction and side of frame across cuts (gos_0006, 0005, 0009, 0010,
  0012, 0007, 0013; gote_0054, 0055, 0017, 0018, 0016).
- **CG-D3** Eye-lines and reciprocal coverage (gos_0008, 0016, 0011, 0015; gote_0056).
- **CG-D4** Angle, height and depth staging of the product (conv_0015; alt_0010, 0015, 0017, 0016).
- **CG-D5** Move or hold (ms_0002, 0010, 0017, 0016, 0019; alt_0014, 0021).
- **CG-D6** What joins the shots, 30° separation, hold length (murch_0013; gote_0004, 0006, 0027,
  0028, 0031, 0037, 0053, 0052; gos_0014).
- **CG-D7** When the spatial rules yield — Murch's six, sacrifice upward (murch_0019, 0020, 0027,
  0028, 0031; gos_0013).
- **CG-D8** The soundtrack and the space (gote_0048, 0019; conv_0007, 0009, 0023, 0019).

## 2. Seed coverage — 25 of 25

CG-D1: alt_0018, alt_0022. CG-D2: gos_0006, gos_0007, gote_0017. CG-D4: alt_0015. CG-D5: ms_0002,
ms_0016, ms_0017, ms_0019, alt_0014. CG-D6: gote_0004, gote_0006, gote_0031, gote_0037, gote_0052,
gote_0053, murch_0013. CG-D7: murch_0019, murch_0020, murch_0027. CG-D8: gote_0048, conv_0007,
conv_0019, conv_0023.

Two seeds needed a question outside camera grammar proper and got an honest one rather than a forced
one: the four sound/music seeds sit under CG-D8 ("what does the soundtrack do for the space the
camera shows", feeding AUDIO_AND_EDIT, which the injection contract assigns to this pack as well as
editing); alt_0018/alt_0022 (key of the picture, level on the dramatic line) sit in CG-D1 because
Alton states them as the decision made *before* scene work, the same planning pass as the shot list,
and 0022 gives the long shot's job.

## 3. Closure holes and how each was resolved

Conflicts (all `between` ids read in full):
- CF-01 gos_0007 ↔ gos_0012 (contradicts): direction holds; a far-side shot only under 0013's reason.
- CF-02 gos_0010 ↔ gos_0012 (contradicts): arc rule governs; far-side setup needs 0013 + bridge (0016).
- CF-03 ms_0017 ↔ ms_0010 (contradicts): by scene — two people moving = static wide; shift of place =
  hidden move; either with its reason (0002).
- CF-04 alt_0015 ↔ alt_0017 (contradicts): 0015 subject-vs-ground either direction; 0017 only across
  three or more staged planes.
- CF-05 gote_0053 ↔ gote_0052 (qualified_by): readable shot holds describe-aloud; fast cuts only in an
  action passage.
- CF-06 gote_0019 ↔ gote_0021 (qualified_by; 0021 not compiled): continuity by default; removal or
  contradiction is a declared device, a deviation on CG-D8.
- CF-07 alt_0018 ↔ alt_0011 (contradicts; 0011 not compiled): product film is not the exempt genre;
  key agrees with the fictional source unless the brief names a pastiche.

Cited partners: gos_0005, 0012, 0013 (for 0007/0010/0014/0015); gote_0054 (for 0017); gote_0055 (for
0056); gote_0028 (for 0031); gote_0006 (for 0004); conv_0009 (for 0007); murch_0031 (for 0027);
murch_0028 (for 0019); alt_0017 (for 0015); gos_0008 (qualifies 0007); gos_0017 (qualifies 0015).
Regression rule honoured: gos_0012 is cited with gos_0007, 0010 and 0013.

Waivers (15): ms_0003→0014; ms_0016→0014; ms_0019→0008, 0014; ms_0010→0001, 0004; ms_0002→0018;
alt_0021→0020; alt_0016→0002; gote_0018→0008; murch_0019→0011, 0029, 0032; murch_0027→0030;
conv_0009→0011. Each reason states what the decision consumes and why the partner does not change
it (reflection technique, rig-independence, reader's-own-test status, rehearsal checklist, set
construction, sound-level rule carried elsewhere, percentages/underlying preoccupation, overuse bound).

## 4. Limit lines

- CG-D1: no product focal length or size ladder; lens claims are about faces; Alton's genre table is
  1949 — only the order (key first) transfers.
- CG-D7: Murch's six are "for me" and narrative film; product-film transfer untested.
- Pack: every contributor assumes a cinema/TV frame — no 9:16, no 15–30 s, no sound-off autoplay;
  transfer of arc, 30°, hold and sound defaults untested.
- Pack: no Indian contributor; no frontality/darshan claim; no packshot or frontal-product
  convention in Canon — assume neither way (the task asked for darshan "where the contributors say
  so"; none does).
- Pack: line/eye-line/reciprocal rules are stated for talent, not a product alone; static_image gets
  CG-D1 and D4 only; CG-D8 needs an audio track.
- Devanagari line added by the compiler.

## 5. Deliberately not compiled

- gote_0012/0013/0026/0011/0060/0035 (edit-side 30°, jump cut, composition difference, wipe
  exemption): cut for budget after a first draft carried them with three more conflicts; the shot-side
  30° rule (gos_0014) carries the same floor. The wipe and its two exemptions are therefore absent.
- murch_0025/0026 (3-D continuity ranks last, against tradition): the ranking in 0019/0027 already
  places space last; citing 0025 would have pulled in the 0026 contradiction for no new default.
- gote_0030/0034 (dissolve/wipe conditions): the dissolve register (0031) was the seed; 0030 drags in
  the wipe contradiction.
- alt_0011 and gote_0021 are named in conflicts but not cited (both marked "not compiled here").
- A separate key/level decision (first draft CG-D10) was folded into CG-D1 for budget; a separate
  depth decision was folded into CG-D4 (both rest on alt_0010).

## 6. Terse tokens

2,498 of 2,500 (9,990 chars). The pack fit only after two structural merges (10 → 8 decisions);
no seed was dropped and no id was cut to make room.

## 7. Session tokens (estimate)

Roughly 95k tokens: brief + spec + contract + style references (~25k), seed packet in sections plus
~45 extra claims by id (~35k), six compile/measure iterations and the two files (~35k).

## Post-check edits (Controller, from CHECK-camera_and_spatial_grammar.md — PASS WITH EDITS)

- CG-D8: "never supplies one" → "seldom supplies one — a tendency, not a rule" (conv_0007 is hedged; same fix as EP-D8).
- CG-D6: "romantic or sad passages only" → "effective in romantic or sad passages" (gote_0031 is not exclusive).
- CG-D7: "not the reverse" dropped; "seems to hide" (murch_0028's own words).
- CG-D4 / CF-04: the "three or more staged planes" condition was not in alt_0015 or alt_0017; replaced by the claims' own wording (most distant part lightest, a full black-to-white scale) for both the default and the conflict rule.
- The checker's missing question (what motivates a move or cut on a product-only beat, e.g. a turntable shot) added to the talent-rules limit line as a declared gap.
- Noted, not changed: conv_0007/0019/0023 are cited by both CG-D8 and EP-D8 (duplicate seeding across two packs, allowed by coverage; the injection contract assigns audio to this pack). Decision texts trimmed to fit 2,500 tokens; 25/25 seeds unchanged.
