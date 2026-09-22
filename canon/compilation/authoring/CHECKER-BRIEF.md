# Checker brief — verify one compiled doctrine pack

You did not build this pack. You verify it against the accepted corpus and the definition of
done (`canon/validation/CANON-DONE-v0.md`). USD 0; no model or provider call. You write exactly
one file: `canon/compilation/authoring/CHECK-<PACK_ID>.md`. You edit nothing else — not the
authoring file, not the compiled pack, not the build note. Findings go in your report; the
builder or the Controller acts on them.

## What to verify

1. **Every decision says only what its cited claims say.** For each decision in
   `canon/compilation/authoring/PACK-<PACK_ID>.authoring.yaml`, fetch its ids in full
   (`python3 canon/compilation/pack_seed.py --claim <id> …`; concept systems with
   `--systems <source_dir>`) and judge the `default` and `check` text: SUPPORTED (the claims say
   this), OVERREACH (the text goes beyond the claims — quote the words that are not in any
   claim), MISATTRIBUTED (an id is cited for something it does not say), or CONTRADICTED (a cited
   claim says the opposite). Quote the claim text you relied on, briefly.
2. **Seed coverage is real, not nominal.** `python3 canon/validation/canon_done.py --pack
   <PACK_ID>` must report `missing 0`. Then, for every seed claim, does the decision that cites it
   actually consume its content, or is the id merely listed? Mark each seed CONSUMED / LISTED-ONLY.
3. **Closure was resolved honestly.** For every `waivers` entry: fetch the partner claim; would
   its content change the decision's default if it were consumed? If yes, the waiver is WRONG
   (should be a cite or a conflict). For every `conflicts` entry: does the `resolution_rule`
   separate the two claims by a condition that the claims themselves support?
4. **Limits are where the silence is.** Read the build note's "did not compile" and limit lines;
   name any obvious question in this pack's domains that a producer of an Indian product ad
   (still or 15–30 s vertical film) would ask and that neither a decision nor a limit line
   answers.
5. **Mechanics.** Run `python3 canon/validation/validate_compiled_pack.py` and
   `python3 canon/compilation/compile_pilot_packs.py --check`; record the lines for this pack.

## The report (`CHECK-<PACK_ID>.md`)

- Verdict: PASS (adoptable as is) / PASS WITH EDITS (list the exact edits) / FAIL (why).
- Table: decision → verdict (SUPPORTED / OVERREACH / MISATTRIBUTED / CONTRADICTED) → note.
- Seed table: seed id → decision → CONSUMED / LISTED-ONLY.
- Waivers judged WRONG, with the partner's words. Conflicts judged unsupported.
- Missing questions (item 4).
- Mechanics lines. Your session-token estimate.

Be specific and short. A verdict without the claim words behind it is not a finding.
