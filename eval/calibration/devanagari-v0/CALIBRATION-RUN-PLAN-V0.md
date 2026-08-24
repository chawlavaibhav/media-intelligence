# Devanagari checker calibration — V0 run plan

**Task:** EVAL-003 · **Status: PLAN ONLY. Nothing in it has been executed.**
Executing any stage below requires Controller approval of human time and API spend.

---

## 1 · What this run would answer

**Can a candidate AI checker read Devanagari from a real photograph?**

Not "is the generator good at Hindi" — that is a different, later question. This is the prerequisite:
if a checker cannot reliably read the script, its verdicts about generated Hindi are worthless
however carefully we design everything downstream.

The dangerous error is specific. A language model reads *toward* the plausible word, so as a
verifier it fails by **passing things that are actually wrong**. In our founding study one checker
reported six visibly misspelled signs as correct matches. This run is built to catch that.

---

## 2 · The material

| | |
|---|---|
| **Development material** | CVIT lineage — IndicSTR12 + IIIT-ILST, real photographed signage |
| **Candidate pool** | **54 Hindi-labelled photographs**, from 173 eligible Hindi candidates |
| **Configuration** | `--overlap-policy admit-once --language-filter hindi --target-n 54` |
| **Expected usable after rejections** | ~30–45; the pool is oversized so readers can reject unreadable crops |
| **Unseen reserve** | **BSTD — 25,246 images, never opened.** Different lineage (Bhashini / IIT Jodhpur) |

**Why the reserve exists.** A checker measured only on photography it has already met looks better
than it is. BSTD is the only genuinely different lineage available, so it is held back untouched.

**Why the two CVIT sources count as one.** 173 files are byte-identical across them, and those 173
are **98% of everything IIIT-ILST has labelled** — only 3 labelled IIIT-ILST images are unique. For
our purposes the development material is effectively one source, and BSTD is the only real
cross-lineage check.

**Independence of the 54.** Each is a distinct photograph by SHA-256 — verified: 54 items, 54
distinct hashes. A photograph present in **both** CVIT releases is admitted **once**, attributed
deterministically to one source record for provenance; the two dataset names are **not** treated as
independent evidence about it. Duplicate copies within a source collapse to one item, and one region
is taken per photograph, so the same picture cannot contribute twice.

**Every Hindi-labelled photograph is a shared one** — all 173 appear in both releases. That is why
`admit-once` is required to obtain any Hindi at all, and why nothing here claims two independent
sources for these items.

---

## 3 · Stages, and exactly what is blind at each

### Stage 1 — Blind transcription by **two independent readers** *(human time)*

> **Corrected 24 Aug 2026.** An earlier draft used one reader as the reference. That would have made
> a single person's reading the answer key with no way to distinguish a confident misreading from a
> correct one — every checker that read such an item correctly would have been scored wrong.

Each reader independently sees crop + item ID. **No expected answer, no dataset label, no checker
output, and no sight of the other reader's responses** — blinding is verified mechanically: the
generated pack contains no Devanagari character at all.

Both readers see the **same materialised crop files** the checker will later receive — byte-identical,
verified by hash — so there is no possibility of reader and checker judging different regions.

Output per reader: `item_id, human_transcription, status, notes`, with `cannot_read` and `ambiguous`
as valid answers.

**Cost: ~1.5–2 hours per reader.**

### Stage 2 — Freeze, then compare the two readings

Both readers' answers are frozen and hashed. Nothing downstream may edit them. Then:

| Case | Treatment |
|---|---|
| **Both readers agree exactly** | becomes high-confidence V0 reference material |
| **Readers disagree** | **not** resolved in either reader's favour. Either excluded from the hard pass/fail gate, or sent to a recorded adjudication step. Reported either way |
| **Either marks `cannot_read`** | excluded from scoring and **reported**, not quietly dropped |

**Neither reader alone becomes ground truth.** Records say "read by two independent readers on this
date, agreed / disagreed", never "this is what the sign says". The agreement rate between the two
readers is itself a reported result, and it bounds how much of the pool can carry a strict gate.

A high rejection or disagreement rate is a fact about the material, not a nuisance to be worked
around.

### Stage 3 — Derive intact and broken targets *(deterministic, no human, no API)*
Only now, **after stage 2 is frozen**, is each usable item assigned:

- **`intact`** — target = the human transcription, character for character.
- **`broken`** — target = the human transcription with one deterministic alteration applied.

Assignment is seeded and roughly 50/50, recorded in the run manifest.

**The alteration rules** — pure string operations, no Hindi judgement:

| Rule | Operation | Why this rule |
|---|---|---|
| `confusion_swap` | swap a character from an observed confusion pair (ब↔व, य↔थ) | these are **our own observed generator failures**; a checker that misses them misses the defect we actually have |
| `matra_substitute` | replace one vowel sign with another fixed one | vowel signs attach in several directions and are a plausible failure point |
| `char_delete` | delete the nth Devanagari character | tests sensitivity to omission |
| `char_transpose` | swap two adjacent characters | tests order sensitivity |

Applied in fixed precedence; the first applicable rule wins; the rule used is recorded per item.

⚠️ **Known limit, deliberately not resolved here.** A deterministic edit can accidentally produce
another real word, or — worse — accidentally produce the *correct* reading of an ambiguous crop. That
would turn a "broken" item into an intact one and corrupt the false-pass count. **Whether an altered
string genuinely differs from what is visible is a Hindi-language judgement**, so stage 4 exists.

### Stage 4 — Confirm the altered targets **(short human check)**

> **Corrected 24 Aug 2026.** An earlier draft said this check must not be done by the reader who
> established that item's reading. Since **both** readers read **every** item, that left nobody
> eligible and would have forced a third specialist into the budget. Withdrawn.

**Either of the two readers may perform this check.** It is safe for a structural reason rather than
a matter of trust: by this stage **the reference is already frozen**, and this check has no power to
edit or replace it. The only question asked is:

> *Is this proposed altered string visibly different from the agreed reference and the image?*

**Rules:**
- Runs **only after both stage-1 passes are frozen** and the agreed reference is fixed.
- Applies only to items that already carry an agreed reference. Items where the readers disagreed
  never enter the gate set, so they are never altered.
- **If there is any doubt, drop or reclassify the item.** Never adjust the reference to fit a target.
- **Record which reader performed the check**, per item.
- Neither reader is told during stage 1 which items will later be altered.

A third independent adjudicator would be a separate human-time decision, not part of EVAL-003.

Estimated **20–30 minutes**.

### Stage 5 — Run candidate checkers *(API spend)*
Each checker receives the image and the assigned target. It does **not** see the human transcription,
the intact/broken label, or any other checker's output.

```
node eval/scripts/check-vlm.mjs --items <run-items.jsonl> --out <results.json> --model <id>
```

The per-item target mode added in EVAL-003 is what makes this possible; the judgement predicate is
unchanged and that was verified against all 27 stored historical cases.

**Repeat runs.** The leading checker is run **3 times over the full set** to measure whether it gives
the same answer twice — currently unmeasured, and a checker that is right on average but unstable
per-item is not usable as a gate.

**Crop materialisation is now solved and verified** (correction pass). `materialise-crops.py`
produces one crop file per item, and **both the reviewer interface and the checker input reference
those same files** — equivalence by identity rather than by two computations agreeing, confirmed by
hash across all 54 items.

Crop geometry is proven, not assumed: `--self-test` writes a synthetic image in which every pixel
encodes its own coordinates, crops known rectangles, and decodes the result with a dependency-free
PNG reader to confirm the returned pixels carry the expected source coordinates.

That self-test found a real defect: **`sips --cropOffset 0 0` is treated as "no offset" and silently
returns a CENTRE crop.** Any region at the exact image origin would have been silently wrong. A
verified flip-crop-flip workaround handles that case, and the self-test covers it.

### Stage 6 — Score
| Metric | Question | Consumer |
|---|---|---|
| **Gate accuracy** | did it correctly say match / no-match? | routing |
| **False-pass count** | how often did it pass a `broken` item? | **the disqualifying measure** |
| **False-fail count** | how often did it fail an `intact` item? | tolerable; costs a regeneration |
| **Transcription accuracy** | how close was its reading, by character edit distance? | repair, diagnosis |
| **Repeat consistency** | same verdict across 3 runs? | reliability |

Gate and transcription accuracy are stored **separately**. Our existing checker scored 14/14 on
verdicts while silently correcting a misspelling — right gate, incomplete diagnosis. One number
would have hidden that.

---

## 4 · What a clean result would let us say — and what it would not

Suppose ~30 usable items, ~15 of them `broken`. A false pass can only occur on a `broken` item, so
there are **~15 opportunities**, not 30.

**If a checker gets all 15 right:**

> ✅ *"This checker passed our V0 qualification screen: zero false passes in 15 opportunities on real
> photographed Devanagari."*

> ❌ *"This checker is accurate."* Zero in 15 is consistent with a true false-pass rate of **up to
> ~18%** (95% upper bound). A checker that genuinely misses one broken item in ten has roughly a
> **1-in-5 chance** of scoring perfectly on 15.

Supporting a real "under 5%" claim needs **59 opportunities**; under 1% needs ~299. Neither is
proposed. This is the same bound EVAL-001 §2b already established, now with real material behind it.

**Two further limits specific to this material:**

**The source labels are not a usable answer key.** Two releases from the same source lineage assign
different transcriptions to the same regions 33% of the time (1,082 one-to-one matched regions).
That is why the reference is established by our own readers rather than adopted from the datasets.

> ⚠️ **This figure is not a human-performance ceiling and must not be used to set a threshold.** The
> repository holds no provenance showing those annotations were produced by independent annotators.
> An earlier draft of this plan treated 67% as a ceiling on achievable checker accuracy. **That is
> withdrawn.**

**Reading is not drawing.** A checker that passes this can read Devanagari from photographs. Whether
it can judge *generated* Hindi text is a further question — generated text fails differently, often
looking clean while being semantically wrong. This screen is necessary, not sufficient.

**Language composition — Controller-approved Hindi-primary pack.** The committed V0 pack is
**54 Hindi-labelled photographs**, drawn from 173 eligible Hindi candidates.

A clean result therefore licenses a claim about **reading Hindi from photographed signage**. It does
**not** automatically transfer to Marathi or to Devanagari-language use in general. A Marathi stress
subset is **deferred, not rejected**; it would need readers with Marathi competence and would be
reported separately.

## 5 · Exactly what the next task would spend

| Stage | Human time | API spend | Notes |
|---|---|---|---|
| 1 · Blind transcription, **reader A** | **1.5–2 h** | ₹0 | Devanagari-capable reader |
| 1 · Blind transcription, **reader B** | **1.5–2 h** | ₹0 | independent; no sight of A |
| 2 · Freeze and compare | 0 | ₹0 | mechanical |
| 2b · Adjudicate disagreements *(if wanted)* | **0–30 min** | ₹0 | otherwise disagreements are simply excluded from the gate |
| 3 · Derive targets | 0 | ₹0 | deterministic |
| 4 · Confirm altered targets | **20–30 min** | ₹0 | either reader; the reference is frozen and cannot be edited |
| 5 · Run checkers | 0 | **first API spend** | ~54 crops × N checkers × 3 repeats for the leader |
| 6 · Score | 0 | ₹0 | mechanical |
| — | **≈ 3.5–4.5 h total across two readers** | per-call cost × volume | |

**This is roughly double the single-reader estimate**, and that is the point: a single reader's
transcription silently becomes the answer key, and there is no way to tell a confident misreading
from a correct one.

**API cost cannot be stated here.** Doing so needs a model roster, and selecting one is explicitly
outside EVAL-003. At ~₹0.90 per check (our recorded figure), 54 images across a small roster with
repeats is a low-tens-of-rupees order of magnitude — an estimate from an old figure, not a quote.

**No Registry entry may be written from this run** unless the checker passes and the entry records
the qualification-gate framing rather than an accuracy claim.

---

## 6 · What would make this run invalid

Stop and report rather than continuing if:

- crop geometry self-test fails on the machine doing the run — a mis-cropped region invalidates both
  reader and checker, and the self-test is what stands between us and that;
- the two readers disagree so often that too few agreed items remain to screen anything;
- the reader rejects so many items that fewer than ~20 usable remain, leaving too few opportunities
  to screen anything;
- stage 4 finds that many deterministic alterations did not actually change the visible reading;
- any checker is run before stage 2 is frozen — that would leak the answer;
- the rubric, thresholds or predicate are edited after results are seen. **That is an experiment-
  mutation stop**, and it is the failure this whole sequence is arranged to prevent.
