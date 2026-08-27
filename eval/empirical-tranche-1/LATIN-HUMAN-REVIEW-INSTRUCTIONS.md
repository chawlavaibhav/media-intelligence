# EMP-001 Latin Human Perceptibility Review Instructions

**Status:** REQUIRED ZERO-SPEND HUMAN PREREQUISITE  
**External calls:** 0  
**Spend:** USD 0 / INR 0

This is a human observation task. Do not ask a model/agent to fill the verdicts and do not infer them from the mechanical pixel check.

The frozen rule comes from `docs/superpowers/plans/2026-08-26-first-empirical-tranche.md`:

- every **mismatch** item must receive `visible_difference=yes`;
- every item must receive `usable_surface=yes`;
- any rejected item means the builder source list is corrected and the **whole manifest is rebuilt before fingerprint freeze**;
- never patch only the reviewed CSV row in place.

## 1. Materialise the exact review images on macOS

From repository root:

```bash
python3 eval/empirical-tranche-1/text_qualification/render_latin_pack.py
```

The renderer is intentionally pinned to:

```text
/System/Library/Fonts/Supplemental/Arial.ttf
point size 64
```

Do not substitute another font silently. The mechanical record fingerprints the exact font bytes used.

Expected outputs:
- images: `eval/empirical-tranche-1/text_qualification/build/images/`
- mechanical record: `eval/empirical-tranche-1/text_qualification/perceptibility-mechanical.json`
- human sheet: `eval/empirical-tranche-1/text_qualification/perceptibility-review.csv`

The script must report 0 mechanically invisible mismatch items before the human review starts.

## 2. Review the 96 surfaces

For each row, inspect the rendered image together with its record in:

`eval/empirical-tranche-1/text_qualification/latin-pack-v1.jsonl`

### For all 96 items

Set:

`usable_surface=yes`

only if the rendered surface is a plausible, legible commercial text surface on which it is reasonable to test a text judge.

If any item is not usable, set `usable_surface=no` and explain briefly in `reviewer_note`.

### For the 48 mismatch items only

Set:

`visible_difference=yes`

only if a normal human reader can actually notice the corruption relative to the target/clean form.

If the corruption is technically present but not human-noticeable, set `visible_difference=no` and explain briefly in `reviewer_note`.

For the 48 clean/match items, `visible_difference` is not a required verdict and may remain blank.

## 3. Acceptance rule

The human prerequisite passes only if:
- all 96 rows have `usable_surface=yes`; and
- all 48 mismatch rows have `visible_difference=yes`.

Anything else is a pack correction signal, not permission to waive the item.

## 4. If anything fails

Do **not** edit the reviewed item in `latin-pack-v1.jsonl` directly and do not change only the CSV.

Instead:
1. correct the fixed base/source list in `build_latin_pack.py`;
2. rebuild the entire 96-item manifest;
3. regenerate its SHA-256 fingerprint;
4. re-render the whole pack with the pinned font;
5. rerun mechanical perceptibility;
6. repeat the human review against the rebuilt pack.

That preserves the pack's deterministic lineage.

## 5. What to return to the Controller

Return:
- the completed `perceptibility-review.csv`;
- reviewer name/identifier sufficient to establish that a real person performed the review;
- confirmation the review used the current `latin-pack-v1.sha256`;
- whether any item failed.

Do not include API keys or other secrets.
