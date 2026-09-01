# EVAL-038 — blinded judging protocol (Controller-facing)

Authority: DN-07. You (the Controller / human acceptance authority) judge packages and
media. Models never judge themselves; this executor session made no creative judgment —
the only selection it performed is the committed structural-defect rule in
`tools/select_package.py` (fewest missing required sections/fields; ties to the lowest
repetition number).

## What exists to judge

1. **Packages, per brief (B01–B06):** blinded, stripped copies of
   - haiku-packs (weak model + compiled doctrine, unconditional injection), 2 reps;
   - sonnet-no-canon (strong model alone, committed EVAL-037 baseline, freeze
     `baseline/sonnet-no-canon/FREEZE-COMMIT.txt`), 3 reps.
   Stripping removes FAILURE_PREVENTION, DOCTRINE_DEVIATIONS and
   KNOWLEDGE_AND_WEBSITE_USE from EVERY package uniformly (they are where treatment
   self-discloses; GAP-06), and a mechanical scan proves no treatment marker survives.
2. **Media, product learning only (never Registry evidence):**
   - B06 image pair: one from the selected haiku-packs package's generation prompt,
     one from the selected sonnet-no-canon package's, same route
     (`gemini-3.1-flash-image`, 4:5).
   - B01 video pair: same construction, route `veo-3.1-lite-generate-preview`
     (8s, 9:16, 720p — one representative hero shot per package, the same shot slot
     for both).

## Blinding mechanics (the corrected value-gate pattern)

- `tools/strip_blind.py blind` wrote blinded copies `judging/packages/<brief>/P01…Pnn.txt`
  in an order derived from an OS-entropy key.
- The key and label mapping are OFF-repo (`~/.eval038-blinding-key.json` on the
  execution machine). What IS committed before judging:
  `judging/packages/<brief>/BLINDING-COMMITMENT.json` — a salted SHA-256 commitment of
  the key.
- Media files are committed under blinded names `judging/media/M01/M02` (images) and
  `judging/media/V01/V02` (videos) by the same mechanism.
- After ALL your verdicts are committed, the key + salt are revealed and committed;
  anyone can recompute the commitment and the mapping.

## How to judge (per the EVAL-038 design, §1 and §4)

For each brief, read every blinded package and record, in a file you write (or dictate
to a fresh session that has NOT seen this branch's construction):

```
brief: B0X
ranking: [P03, P01, ...]        # best first
per_package_notes: one line each — would you send this to production?
```

For media: for the image pair and video pair separately, record which artifact you
would accept for the brief (either, both, or neither), and why, in one line each.

Verdict semantics for the substitution question: for each brief, a haiku-packs package
"wins" against the strong baseline if it outranks every sonnet-no-canon package;
"ties" if it outranks at least one. The design's programme-level read requires
weak+pack ≥ strong-alone on ≥3 of 6 briefs; anything less is a real negative result
and is committed as one.

**Deviation from the design, recorded:** the design asked for two independent
reviewers with unanimity. DN-07's execution order names you as the judge of packages
and media; a second independent reviewer can be added later by re-running this
protocol from the committed blinded artifacts — the blinding survives until the key
is revealed, so do not reveal until all reviewers you intend are done.

## What NOT to do

- Do not read `runs/haiku-packs/`, `baseline/`, the key file, or this branch's diffs
  before judging — only `judging/**`.
- Do not judge the two run-1 truncated haiku trials (committed failed evidence).
- Do not treat B02/B06 verdicts as tests of colour/register doctrine: the
  colour_and_visual_register pack is uncompiled and was never injected
  (`canon/findings/EVAL-038-RETRO-TEST-PILOT-001.md`, residual-gap note).
