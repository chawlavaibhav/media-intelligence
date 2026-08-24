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
| **Candidate pool** | 54 independent items, built deterministically (`build-candidate-pool.py`) |
| **Expected usable after rejections** | ~30–45; the pool is oversized so the reader can reject unreadable crops |
| **Unseen reserve** | **BSTD — 25,246 images, never opened.** Different lineage (Bhashini / IIT Jodhpur) |

**Why the reserve exists.** A checker measured only on photography it has already met looks better
than it is. BSTD is the only genuinely different lineage available, so it is held back untouched.

**Why the two CVIT sources count as one.** 173 files are byte-identical across them, and those 173
are **98% of everything IIIT-ILST has labelled** — only 3 labelled IIIT-ILST images are unique. For
our purposes the development material is effectively one source, and BSTD is the only real
cross-lineage check.

**Independence of the 54.** Each is a distinct photograph by SHA-256. Files appearing in both CVIT
datasets are excluded outright; duplicate copies within a source collapse to one item; one region
per photograph, so the same picture cannot contribute twice.

---

## 3 · Stages, and exactly what is blind at each

### Stage 1 — Blind human transcription **(human time)**
The reader sees crop + item ID. **No expected answer, no dataset label, no checker output** —
verified mechanically: the generated pack contains no Devanagari character at all.
Output: `item_id, human_transcription, status, notes`. `cannot_read` and `ambiguous` are valid.

**Cost: ~1.5–2 hours of a Hindi first-language reader.** Nothing else in this plan consumes human
time until stage 5.

### Stage 2 — Freeze
Human readings are frozen and hashed. Nothing downstream may edit them. Items marked `cannot_read`
are excluded from scoring and **reported**, not quietly dropped — a high rejection rate is a fact
about the material, not a nuisance.

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

### Stage 4 — Confirm the broken targets **(short human check, separate from stage 1)**
The reader confirms, for `broken` items only, that the altered string is in fact different from what
is visible. Any item that fails this check is reclassified or dropped, and that is recorded.

**This happens after stage 1 is frozen, and the reader is not told during stage 1 which items will
be altered.** That ordering is what keeps stage 1 blind. Estimated **20–30 minutes**.

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

**Crop materialisation is an unsolved prerequisite.** The manifest carries crop boxes, not cropped
files. EVAL-003 deliberately did not create crops: the only image tool available here is `sips`,
whose offset semantics could not be verified without pixel inspection, and silently mis-cropping
would mean a reader and a checker judging the wrong region. **The approved run must implement and
verify cropping before stage 1.**

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

**The ceiling is not 100%.** Two expert teams annotating the *same* photographs agreed only **67%**
of the time (1,082 same-region comparisons; 725 identical). Even counting spelling-convention
differences as agreement, it is ~73%. **A checker cannot sensibly be held to a standard above the
observed human-to-human rate on this material**, and our reader's transcription is one reading, not
truth.

**Reading is not drawing.** A checker that passes this can read Devanagari from photographs. Whether
it can judge *generated* Hindi text is a further question — generated text fails differently, often
looking clean while being semantically wrong. This screen is necessary, not sufficient.

---

## 5 · Exactly what the next task would spend

| Stage | Human time | API spend | Notes |
|---|---|---|---|
| 1 · Blind transcription | **1.5–2 h**, Hindi first-language reader | ₹0 | the main human cost |
| 2 · Freeze | 0 | ₹0 | mechanical |
| 3 · Derive targets | 0 | ₹0 | deterministic |
| 4 · Confirm broken targets | **20–30 min**, same reader | ₹0 | after stage 1 is frozen |
| 5 · Run checkers | 0 | **first API spend** | ~54 images × N checkers × 3 repeats for the leader |
| 6 · Score | 0 | ₹0 | mechanical |
| — | **≈ 2–2.5 h total** | per-call cost × volume | |

**API cost cannot be stated here.** Doing so needs a model roster, and selecting one is explicitly
outside EVAL-003. At ~₹0.90 per check (our recorded figure), 54 images across a small roster with
repeats is a low-tens-of-rupees order of magnitude — an estimate from an old figure, not a quote.

**No Registry entry may be written from this run** unless the checker passes and the entry records
the qualification-gate framing rather than an accuracy claim.

---

## 6 · What would make this run invalid

Stop and report rather than continuing if:

- crop materialisation cannot be verified — a mis-cropped region invalidates both reader and checker;
- the reader rejects so many items that fewer than ~20 usable remain, leaving too few opportunities
  to screen anything;
- stage 4 finds that many deterministic alterations did not actually change the visible reading;
- any checker is run before stage 2 is frozen — that would leak the answer;
- the rubric, thresholds or predicate are edited after results are seen. **That is an experiment-
  mutation stop**, and it is the failure this whole sequence is arranged to prevent.
