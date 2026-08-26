# Family 5 — Speech / audio / AV instruments

**Judges:** spoken words, pronunciation, lip sync, speaker turns, delivery.
**Status: NOT QUALIFIED. Pack does not exist. Partly constructible, partly not.**

---

## The trap this family must not fall into

It is the **same trap as the founding Devanagari failure**, in a different medium.

If we generate speech from a script, transcribe it with a speech-recognition
system, and the transcript matches the script — that proves the **words** were
right. It does **not** prove they were **pronounced acceptably**.

A robust ASR system is *trained to be forgiving*: it will normalise a
mispronounced Hindi brand name into the correct word, exactly as the vision
checker silently corrected a misspelling. The instrument's helpfulness destroys
the measurement.

> **Word correctness and pronunciation acceptability are separate results, with
> separate instruments, and must never be reported as one number.**

Word correctness is machine-comparable. Pronunciation acceptability requires a
first-language listener. For Hindi and Hinglish that is not optional — a
globally strong voice model that mispronounces Indian brand names is unusable
for this product.

---

## What can be constructed without humans

| Deterministic perturbation | Known answer |
|---|---|
| Shift audio by a known number of milliseconds | exact A/V offset |
| Swap speaker channels in a two-speaker clip | known wrong turn assignment |
| Swap turn order against the transcript | known turn-order error |
| Substitute a word in the transcript | known transcript mismatch |
| Truncate the audio track | known missing audio |

These qualify the **mechanical** half — sync measurement, turn assignment,
transcript comparison — with no human labelling.

## What cannot

Pronunciation acceptability, prosodic register fit, and the *acceptability
threshold* for lip sync all require listeners.

⚠️ **Do not invent a millisecond tolerance for "acceptable sync".** Inject known
offsets, have listeners judge acceptability across that range, and derive a
**calibration curve** — then propose a threshold from the data. Inventing a
number now would repeat precisely the error the project already paid for with
statistical bounds.

## Gate — split, and reported separately

- **Deterministic half:** exact recovery of injected offsets within a stated measurement precision; exact recovery of swapped turns; exact transcript comparison under a declared normalisation.
- **Human half:** agreement between the instrument and first-language listeners, reported per language (English / Hindi / Hinglish), never pooled — pooling would let strong English performance hide unusable Hindi.

## Qualification inputs

| Need | State |
|---|---|
| 24 single-speaker + 12 two-speaker clean AV clips | ❌ not held |
| Transcripts | ❌ not held |
| **Turn boundaries** for two-speaker clips | ❌ not held — **these are what make wrong assignment machine-detectable**, and they are easy to forget to request |
| First-language Hindi listener time | ❌ not budgeted |
| Perturbation code | ❌ not written |
| Sync tolerance | ❌ deliberately not proposed before data |

**One recorded provider-shaped failure belongs here:** a provider changed valid
speaker names between versions. Error classes in this lane are schema-shaped
information, not noise, and must be recorded as classes rather than counted as
generic failures.
