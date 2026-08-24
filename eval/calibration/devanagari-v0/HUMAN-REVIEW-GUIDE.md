# Guide for readers — blind transcription pass

**Task:** EVAL-003 (corrected) · **Status: prepared, NOT yet to be performed.** Doing this work needs
Controller approval of human time. Nothing here has been asked of anyone.

> **This protocol uses TWO independent readers, not one.** An earlier draft made a single reader's
> transcription the reference. That was wrong: it would have quietly turned one person's reading into
> project ground truth, with no way to tell a confident misreading from a correct one. See §8.

---

## 1 · What you are being asked to do, and why it is unusual

You will be shown **54 cropped photographs of real Devanagari signage** — shop signs, boards,
notices, photographed in the street. For each one you write down **exactly what you can see drawn.**

**Two readers do this separately.** You will not see the other reader's answers, and they will not
see yours. Please do not discuss the items until both passes are complete.

**Language.** Every item in this pack is **Hindi-labelled** — 54 of 54. Readers should be
**Hindi-competent**. If a future pack includes Marathi — the same Devanagari script, but a different
language — that would need readers with Marathi competence and would be run and reported separately.
**Being able to read Hindi does not automatically qualify someone to read Marathi.**

The unusual instruction is this:

> **Write what the letters actually are, not what the sign was meant to say.**

If a sign painter wrote **सुवह** where the word should be **सुबह**, we want **सुवह** — the mistake,
exactly as drawn. If a letter is malformed, damaged or missing a stroke, write what is there.

**Why we are asking for this.** We are not trying to find out what the shop is called. We are
building a reference to test whether an AI can *read Devanagari from a photograph at all.* If it
cannot, then its opinions about generated Hindi text are worthless, no matter how confident they
sound.

We already know one AI checker looked at six visibly misspelled Devanagari signs and reported all
six as correct — because language models are built to read *toward* the plausible word. That is the
exact failure we need to be able to catch, and we can only catch it if the reference says what is
genuinely on the sign.

---

## 2 · What you will NOT be shown, and why

**You will not see any expected answer.** No suggested transcription, no dataset label, no AI output.

This is deliberate and it is verified mechanically — the review pack was checked and contains no
Devanagari character anywhere in its files.

The reason is that **the pull toward the plausible word acts on people too.** A reader shown
"सुबह की पहली चाय" and asked "does the sign match?" will tend to see a match. A reader shown only
the image and asked "what does it say?" will not be pulled in any particular direction.

There is a second, quieter reason. The datasets these images came from already carry their own
transcriptions, and we checked how much those agree with each other. On 1,082 regions covering the
same photographs, **two dataset releases assign different transcriptions about one time in three.**

We do **not** know who produced those annotations or whether they were made independently, so that
figure says nothing about how well people read — only that **the existing labels cannot simply be
adopted as correct.** Your reading is made independently for exactly that reason.

---

## 3 · How to record each item

For every item, one of three answers:

| Status | Use it when | What to type |
|---|---|---|
| **transcribed** | you can see the letters | exactly what is drawn, letter for letter |
| **cannot read** | too blurred, dark, small, cut off or occluded | leave the text box empty |
| **ambiguous** | it could genuinely be read more than one way | your best reading, **and say why in notes** |

**`cannot read` is a real answer and a useful one.** Please use it rather than guessing. A guess
recorded as a confident reading is worse for us than an honest blank, because we will treat it as
truth and score a machine against it.

**Preserve exactly what you type.** Do not normalise spelling, do not add or remove nukta dots or
vowel signs to make a word look right, and do not convert to a different spelling convention.

**Order.** Please work through the pack in the order given and do not skip ahead to compare items.

**Time.** 54 items, roughly 1–2 minutes each: about **1.5 to 2 hours per reader**, including breaks.
You can stop and resume — your answers are saved as you go.

---

## 4 · How to run the pack

1. Open `review-pack/index.html` in a browser on a machine that has the image corpus available.
   If images do not appear, the pack was generated with the wrong image path — ask before
   continuing rather than working from blank frames.
2. Work through the items. Each screen shows one cropped region and the item's ID.
3. Answers save automatically in the browser.
4. When finished, press **Export CSV** and return the file.

The exported file has four columns: `item_id`, `human_transcription`, `status`, `notes`.
`review-pack/RESPONSE-SCHEMA.json` describes them precisely.

---

## 5 · What your answers will and will not become

**Where the two readers agree exactly**, that reading becomes high-confidence reference material for
scoring candidate AI checkers.

**Where the two readers disagree**, the item is *not* silently resolved in either reader's favour.
It is either kept out of the strict pass/fail test, or adjudicated in a separate recorded step. A
disagreement between two careful readers is a fact about how hard the item is, and it is more useful
recorded than hidden.

**Neither reader alone becomes ground truth**, and the project's records will say *"read by two
independent readers on this date, agreed / disagreed"* rather than *"this is what the sign says."*

**Nothing you write is used to train anything.** This material is for internal evaluation only.

---

## 6 · What happens after your pass

1. Both readers' answers are frozen. Nothing is edited afterwards.
2. Agreements and disagreements are counted and recorded.
3. **Only then** are altered target strings derived for some items, so we can test whether a checker
   correctly *rejects* a mismatch. This happens after both passes are frozen precisely so it cannot
   influence them, and neither reader is told which items will be used that way.
4. Candidate checkers are run against the crops, blind to both readers' answers.
5. The comparison is made.

**A later, separate and much shorter task** asks one of you to confirm that particular altered
strings really are different from what is visible. **Either reader may do this.** It is safe because
by then the agreed reference is **frozen** — the check cannot change it. The only question is whether
a proposed altered string differs from what is agreed and visible; if there is any doubt the item is
dropped rather than the reference adjusted. We record who did the check.

---

## 8 · Why two readers, and what it costs

**The problem with one reader.** A single reader's transcription becomes, in practice, the answer
key. If they misread an item, every checker that reads it correctly is scored *wrong*, and nothing in
the process would reveal it. With no second opinion there is no way to distinguish "the checker
failed" from "the reference was wrong".

**What two independent readers buy.** Where they agree exactly, that is materially stronger evidence
than one reading. Where they disagree, we learn the item is genuinely hard — and we can keep it out
of a pass/fail gate rather than scoring machines against a coin flip.

**What it costs.** Roughly double the reading time: **about 3–4 hours total** rather than 1.5–2, plus
20–30 minutes for the later altered-string check, and a short adjudication step if disagreements need
resolving. Estimated total: **≈ 3.5–4.5 hours across two readers.**

**What we still cannot claim.** Two readers agreeing does not make a reading certain, and this
protocol does not measure "how well people read Devanagari" — it has no controlled design for that.
It establishes reference material with a known agreement level, and nothing more.

---

## 7 · What to do if something seems wrong

**Stop and ask.** Do not improvise. In particular, if the images do not load, if a crop appears to
show no text at all, or if many items look like the same sign, something has gone wrong upstream and
continuing would waste your time and contaminate the reference.
