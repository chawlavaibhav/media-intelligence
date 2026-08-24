# EVAL-005 human validation — FROZEN record

**Status: complete and Controller-accepted. Decision: PRUNE, DO NOT REBUILD.**
**No checker/model/API call · no threshold change · no Registry entry · no BSTD · no Marathi ·
checker qualification NOT started.**

Machine-readable form: [`human-validation-v1.json`](human-validation-v1.json) — that file governs;
this one explains it.

---

## What was reviewed

One Hindi-competent reviewer worked through the review packet with fingerprint
**`e1cedf564603a94d`**, generated from the 106-item deterministic build whose `items.jsonl` has
sha256 `9c69cac2…fea6d09d`.

| Section | Answered | Result |
|---|---|---|
| Words — *is this a real, well-formed Hindi word as written?* | **53 / 53** | 48 YES · **5 NO** · 0 UNSURE |
| Perceptibility — *can you see a difference between these two images?* | **25 / 25** | 21 YES · 4 CLOSE · **0 NO** |
| Rendering — *does this look like normal Hindi text?* | **20 / 20** | 18 NORMAL · **2 BROKEN** |
| **Total** | **98 / 98** | **0 unanswered · 0 UNSURE** |

Raw responses are preserved verbatim in [`responses/`](responses/), with sha256 recorded in the
JSON record. Two files, because the reviewer exported the word section separately: the CSV carries
the 53 word answers, the JSON carries the 25 perceptibility and 20 rendering answers. **The JSON's
own words section is blank** — that is expected, not a gap.

## ⚠ What these answers are, and are not

**They are provenance. They are not universal linguistic ground truth.**

One reader. No second reader, no adjudication, no agreement measurement. A judgement here records
what one competent person said about one string on one day. **No threshold, rate, bound or checker
claim may be derived from these answers**, and they must never be cited as evidence about Hindi in
general.

This matters because the battery's own ground truth does *not* come from a human — every image is
rendered from a string we chose, so what it contains is known by construction. Human validation
answers a narrower question: *is the base word a plausible real word for a model to autocorrect
toward?* A mistake here degrades the battery. It cannot corrupt the answer key.

**Cross-question consistency is not independent evidence.** `चाँदपोल` and `लीजिए।` were flagged in
both the word question and the rendering question. Per Controller decision this is **within-reader
cross-question consistency** — the same person, twice — and it is recorded as such, not as
corroboration from an independent source.

## The five rejected lexical items

Reasons are reproduced exactly as supplied; two were left blank by the reviewer and are recorded
blank rather than filled in.

| `word_id` | word | reason as supplied |
|---|---|---|
| `w-087a06b2a452` | इंग्लीश | wrong spelling |
| `w-256fc61187e0` | टुंग | *(none given)* |
| `w-43026df8d365` | चाँदपोल | *(none given)* |
| `w-803fda438f74` | भेंट- | extra punctuation |
| `w-ac25b420b8be` | लीजिए। | extra punctuation |

**`राज -` was explicitly accepted (yes) and is preserved as supplied.** An apparent tension with the
"extra punctuation" rejections was raised at adjudication; the Controller decided not to
reclassify. It is not re-judged here.

## Decisions applied

**Excluded — exactly ten items**, being every item resting on a rejected base word:

```
dx-0000  dx-0003  dx-0005  dx-0020  dx-0039        (mismatch)
dx-0053  dx-0056  dx-0058  dx-0073  dx-0092        (match)
```

Each rejected word backed exactly one match and one mismatch, so the 50/50 balance survives
untouched. **Nothing is replaced and no alternate item is generated.**

**Perceptibility CLOSE — retained.** `dx-0004`, `dx-0010`, `dx-0021`, `dx-0022` were judged visible
only on close inspection. **No pair was judged "cannot see a difference."** CLOSE is a difficulty
signal reported separately; it is not a failure and it excludes nothing.

**The two BROKEN clean renders create no additional exclusions.** `images/img-0039.png` and
`images/img-0073.png` sit on `चाँदपोल` and `लीजिए।`, both already rejected lexically.

## Resulting battery state

| | Before validation | **After** |
|---|---:|---:|
| Items | 106 | **96** |
| Match / mismatch | 53 / 53 | **48 / 48** |
| Hard opportunities (= distinct hard base words) | 37 | **33** |
| Distinct base words | 53, unvalidated | **48, all human-accepted** |
| Failure classes represented | 20 / 20 | **20 / 20** |
| Failure groups represented | 5 / 5 | **5 / 5** |
| iid **reference** figure, zero false passes | 7.78% | **8.68%** |

⚠ That percentage is a sizing calculation under an iid/exchangeable Bernoulli model **EVAL-005 does
not establish**. It is not a bound on any checker's real error rate, and human validation did not
change that.

**Three classes now rest on a single surviving item: `NASAL_SUBSTITUTE`, `NUKTA_REMOVE`,
`REPH_TO_FULL_RA`.** This is **thin diagnostic coverage, not class loss** — all 20 classes remain
represented, and per-class figures were already diagnostic signals rather than rates.

## How a checker run gets the right items

The 106-item build is **historical source material and is unchanged**. The validated view is a
filter over it, not a rebuild:

```
python3 build_items.py --total 120                     # the historical 106-item build
python3 apply_human_validation.py --from-build build   # writes build/validated/
python3 apply_human_validation.py --from-build build --verify
```

`build/validated/` holds the 96 items in original order with original content, plus the two
checker-facing projections and the evaluator-side scoring key — written through the same blind
check that guards the full battery. Image paths resolve against the parent build directory.

**It fails closed.** The ten excluded ids identify items in *one* build; applied to a different one
they would remove different items. So the sha256 of `items.jsonl` is checked against the recorded
value and a mismatch is fatal. It never rebuilds and never re-derives the exclusions.

**Why filter rather than rebuild.** Regenerating from the surviving 48 words would produce a
different allocation that no human has seen, while borrowing the authority of a validation
performed on something else. And editing the generator to pretend the rejected words never existed
would erase a finding: two of five rejections were punctuation artifacts and one a spelling error,
which is evidence about the EVAL-003 lexical pool worth keeping.

## Consequence for sourcing

The battery-size planning target of 84–90 validated words now sits against **48**, not 53. The
outstanding request in `eval/tasks/EVAL-005-RESOURCES-REQUEST.md` therefore grows from ~31–37 to
**~36–42** items, and candidate strings should be free of trailing punctuation before entering the
pool.
