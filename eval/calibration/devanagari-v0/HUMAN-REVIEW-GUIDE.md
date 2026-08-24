# Guide for the Hindi reader — blind transcription pass

**Task:** EVAL-003 · **Status: prepared, NOT yet to be performed.** Doing this work needs Controller
approval of human time. Nothing here has been asked of anyone.

---

## 1 · What you are being asked to do, and why it is unusual

You will be shown **54 cropped photographs of real Devanagari signage** — shop signs, boards,
notices, photographed in the street. For each one you write down **exactly what you can see drawn.**

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
transcriptions, and we checked how much those agree with each other. On 1,082 regions where two
expert teams annotated the exact same photograph, **they disagreed about one time in three.** Your
reading is a third independent one, and it is only worth having if it was made independently.

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

**Time.** 54 items, roughly 1–2 minutes each: about **1.5 to 2 hours**, including breaks. You can
stop and resume — your answers are saved as you go.

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

**They will become:** the reference used to score candidate AI checkers. When a checker reads an
image, its answer is compared against yours. Agreement counts in the checker's favour; disagreement
counts against it.

**They will not become:** the project's settled truth about what any sign says.

That distinction is deliberate. Your transcription is **one expert reading**, and we have direct
evidence from this same material that expert readings of the same photograph differ about a third
of the time. So the record will say *"as read by a Hindi first-language reader on this date"*, not
*"this is what the sign says."*

**A consequence worth knowing:** no checker can be expected to agree with you more often than
another equally-qualified reader would. If we ever set a bar for a machine that is higher than the
observed human-to-human agreement on this material, we would be demanding something no reader
achieves.

**Nothing you write is used to train anything.** This material is for internal evaluation only.

---

## 6 · What happens after your pass

1. Your answers are frozen. Nothing is edited afterwards.
2. **Only then** is a second set of items derived, in which the target string is deliberately
   altered from what you wrote — so we can test whether a checker correctly *rejects* a mismatch.
   That derivation happens after your pass precisely so it cannot influence it, and you are not
   told which items will be used that way.
3. Candidate checkers are run against the images, blind to your answers.
4. The comparison is made.

You may later be asked a **separate, much shorter** question: whether particular altered strings
are in fact different from what is visible. That is a different task, done after this one is closed.

---

## 7 · What to do if something seems wrong

**Stop and ask.** Do not improvise. In particular, if the images do not load, if a crop appears to
show no text at all, or if many items look like the same sign, something has gone wrong upstream and
continuing would waste your time and contaminate the reference.
