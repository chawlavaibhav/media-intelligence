# How the person / product / on-screen-text tags were established

**Task:** RES-005 · **Date:** 28 Aug 2026

Three of the tags the temporal qualification plan needs cannot be established by any local tool
honestly:

| Tag | Why a tool cannot settle it |
|---|---|
| `person` | Face detection would answer a different question, and would not distinguish a photographed human from a rendered character — a distinction that matters for whether an identity-swap result transfers to real people. |
| `product_object` | "Is there a manufactured object in frame" is a semantic judgement. A detector's class list is not the question. |
| `on_screen_text` | Tesseract can be run, and is — but EVAL-022 and EVAL-023 established that Tesseract false-passes as an exact-text judge on this project's material. It is used here as a **screen** for "is there rendered text at all", never as authority. |

So each clip is rendered to a **twelve-frame contact sheet** at
`resources/corpus/raw/mat-av-min/contact-sheets/<clip_id>.jpg`, and the sheet is inspected
directly. `frame-inspection.json` records the resulting tag per clip together with what was
actually seen, so a reviewer can open the same sheet and disagree.

Two conventions matter:

- **`person` is split.** `real` means a photographed human being. `rendered` means an animated or
  illustrated character. They are recorded differently because an identity-preservation result
  measured on a rendered character is not evidence about a photographed face, and merging them
  would hide that.
- **A tag is `no`, not blank, when the sheet shows its absence.** `not_established` is reserved
  for cases where the sheet genuinely does not settle the question.

The mechanical measurements — cut count, motion, freezes, black frames, interlacing, audio — are
in `qualification-measurements.json` and were not adjusted by inspection.
