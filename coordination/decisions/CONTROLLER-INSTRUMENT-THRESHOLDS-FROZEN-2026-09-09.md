# Controller — Instrument Thresholds Frozen as Proposed — 2026-09-09

**Status:** APPROVED CONTROLLER DECISION.
**Role:** Writer Controller, recording the human Controller's words.
**Applies to:** `eval/harness-v2/instruments/PASS-CRITERIA-v0.yaml` (EVAL-039C, morning decision MD-C1).

## Authority — the Controller's words (2026-09-09)

Put to the Controller: *"Freeze the instrument thresholds in `PASS-CRITERIA-v0.yaml`, or say 'freeze as proposed'."*

> **"freeze as proposed"**

## Decision

The six deterministic-instrument criteria proposed by EVAL-039C are frozen exactly as written:
`format_probe` (container / dimensions / aspect ±1 % / duration ±0.5 s / fps / audio presence),
`masked_diff` (edit preservation: MAE ≤ 8/255 and SSIM ≥ 0.90 outside the edit mask),
`brand_colour` (CIE76 ΔE*ab ≤ 5 in the masked region), `av_offset` (registered as
`audio_track_offset_vs_drive`, |lag| ≤ 80 ms, a partial claim), `repeat_consistency`
(held-seed dHash Hamming ≤ 4; unseeded repeats report variance, no pass/fail), `ledger_metrics`
(latency, error and refusal rates, trial cost, reproducibility from the ledger).
`gate_wrapper` stays observation-only and never yields a row.

Consequences:

1. From this moment the instruments emit verdicts instead of `criterion_not_frozen`, and the harness may
   write Capability Registry rows for the eight deterministic capabilities through `write_registry_row`,
   with `n_items`, `repeats_per_item`, `uncertainty.status: computed` and `independence_status: NOT
   ESTABLISHED` unless evidence establishes it (schema v1).
2. The first rows come from Image Round 1's sealed records (`img-r1`, `img-r1-redo`, `img-r1-composite`),
   re-evaluated under the frozen criteria — task EVAL-041.
3. A threshold change is a new decision and a new criteria version; rows carry the criteria file sha256.
4. Q1 geometry: `spatial_relationship_2d` and `size_aspect` stand as qualified (MD-C2); `attribute_binding`
   stays `qualified: null` until a colour tolerance is proposed; `object_count` stays disqualified.

Not decided here: anything about human acceptance (product evidence, never a row), the Canon verdict,
or any spend.
